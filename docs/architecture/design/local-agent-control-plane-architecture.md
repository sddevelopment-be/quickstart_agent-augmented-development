# Technical Design: Local Agent Control Plane

**Version:** 1.0.0
**Date:** 2026-02-13
**Author:** Architect Alphonso
**Status:** Approved
**Related ADRs:** ADR-008, ADR-020, ADR-025, ADR-029, ADR-032, ADR-047, ADR-048

---

## Context

The agent-augmented development framework has grown organically into several
partially integrated subsystems: a doctrine governance stack, file-based task
orchestration, an LLM routing/execution service, and a real-time dashboard.
Each subsystem works, but they lack a unifying architectural model that
describes how they compose into a coherent whole.

As the framework matures toward parallel multi-agent execution, unified
telemetry, and cancellation support, a **reference architecture** is needed
to:

- Guide incremental implementation without rework
- Clarify boundaries between command (write) and query (read) paths
- Provide a stable vocabulary for contributor onboarding and ADR authoring
- Establish extension points for future distribution strategies

This document describes the **Local Agent Control Plane** — a layered,
CQRS-informed architecture that serves as the target state for the
framework's execution and observability subsystems.

### Forces

- **Local-first:** All execution happens on the developer's machine. No
  cloud services required for core operation.
- **Human in charge:** Agents execute under human governance. Checkpoints,
  cancellation, and review are first-class concerns.
- **Heterogeneous tooling:** Multiple CLI tools (claude-code, codex,
  opencode) and potentially SDK-based providers must be supported through
  a uniform interface.
- **File-based orchestration:** Task lifecycle state lives in YAML files
  under `work/collaboration/` (ADR-008). This is a non-negotiable
  foundation.
- **Observability gap:** Current execution telemetry is fragmented across
  terminals. Aggregated, traceable event logs are needed.

### References

- Prestudy: `tmp/ideas/architectural_prestudy_local_agent_control_plane.md`
- CQRS diagram: `tmp/ideas/agent_control_plane_architecture_v3_cqrs.puml`
- Architectural review: `work/analysis/2026-02-13-local-agent-control-plane-review.md`

---

## Acceptance Criteria

1. **Layered separation:** Each architectural layer (Control Plane, Service,
   Distributor, Execution, Storage) can be understood, tested, and evolved
   independently.
2. **CQRS compliance:** Write operations (start, cancel, retry) flow through
   the Coordination Service. Read operations (status, history, cost) flow
   through the Query Service. No read path mutates state.
3. **File-based task state preserved:** YAML files in `work/collaboration/`
   remain the source of truth for task lifecycle (ADR-008).
4. **Telemetry durability:** All lifecycle and execution events are persisted
   to an append-only JSONL log before acknowledgement.
5. **Extension via strategy:** New distribution mechanisms (queue, workflow
   engine) can be added without modifying the Coordination Service.
6. **Cancellation support:** Running tasks can be cancelled via signal
   escalation (SIGINT -> SIGTERM -> SIGKILL) from any control plane.
7. **Backward compatibility:** Existing CLI scripts (`start_task.py`,
   `complete_task.py`, dashboard) continue to function unmodified.

---

## Design

### Overview: C4 Level 1 — Context

```
                    ┌──────────────────┐
                    │  Human Operator   │
                    │  (Developer)      │
                    └────────┬─────────┘
                             │ governs, reviews, intervenes
                             ▼
               ┌─────────────────────────────┐
               │  Local Agent Control Plane   │
               │  (this system)               │
               └──────┬──────────────┬───────┘
                      │              │
            executes  │              │ distributes to
                      ▼              ▼
               ┌────────────┐  ┌─────────────────┐
               │  Work Dir   │  │  LLM Providers   │
               │  (YAML)     │  │  (CLI / API)     │
               └────────────┘  └─────────────────┘
```

The Local Agent Control Plane is a single-machine system that mediates
between a human operator and heterogeneous LLM tools. It provides
governance, observability, and execution management for agent-augmented
development workflows.

**External actors:**
- **Human Operator** — developer who initiates, monitors, and governs work
- **Work Directory** — file-based task state (existing, ADR-008)
- **LLM Providers** — CLI tools and API endpoints that perform LLM work

### C4 Level 2 — Container View

See reference diagram: `docs/architecture/diagrams/control-plane-reference-architecture.puml`

The system decomposes into six containers across five layers:

| Layer | Container | Technology | Responsibility |
|-------|-----------|------------|----------------|
| **Control Planes** | Localhost Dashboard | Flask + SocketIO | Real-time monitoring, cost tracking, intervention controls |
| **Control Planes** | Interactive Console | CLI / TUI | Task initiation, log inspection, interactive exploration |
| **Service** | Coordination Service | Python asyncio | Command validation, governance checks, dispatch, event emission |
| **Distributor** | Direct Distributor | In-process | Default straight-through dispatch to execution adapters |
| **Execution** | CLI Execution Adapter | subprocess + asyncio | Wraps CLI tools via ToolAdapter ABC (ADR-029) |
| **Execution** | Other Tool Adapters | GenericYAMLAdapter | YAML-configured invocation for extensibility |
| **Query** | Query Service | Python | Read-model facade over telemetry, task state, artifacts |
| **Storage** | Telemetry Store | JSONL + SQLite | Append-only event log with materialized query index |
| **Storage** | Artifacts & Logs | Filesystem | stdout/stderr captures, generated artifacts |
| **Storage** | Task State | YAML in work/ | File-based orchestration lifecycle (ADR-008) |

#### Deferred containers (shown in yellow on reference diagram)

| Container | Rationale for deferral |
|-----------|----------------------|
| Queue Distributor (Redis / asyncio.Queue) | No current need for buffered dispatch. Adds infrastructure dependency contrary to ADR-008 philosophy. |
| Workflow Distributor (Kestra / Temporal) | Heavy external dependency. Enterprise-scale concern not applicable to local-first MVP. |
| SDK Execution Adapter (OpenAI / Anthropic SDK) | CLI adapters are sufficient. Direct API integration adds auth/rate-limiting complexity. ADR-025 explicitly deferred this. |

### C4 Level 3 — Component View: Coordination Service

The Coordination Service is the central write-side component. It decomposes
into:

```
┌─────────────────────────────────────────────────────┐
│ Coordination Service                                 │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Command       │  │ Governance   │  │ Event     │ │
│  │ Handler       │  │ Validator    │  │ Emitter   │ │
│  │               │  │              │  │           │ │
│  │ parse + route │  │ policy check │  │ JSONL +   │ │
│  │ commands      │  │ checkpoint   │  │ WebSocket │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
│         │                  │                │        │
│  ┌──────▼──────────────────▼────────────────▼─────┐ │
│  │ Dispatcher (Strategy interface)                 │ │
│  │                                                 │ │
│  │  dispatch(task, strategy) → ExecutionHandle     │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

- **Command Handler:** Receives start/cancel/retry commands from control
  planes. Validates input, resolves agent identity, prepares task context.
- **Governance Validator:** Checks governance constraints before dispatch
  (e.g., checkpoint required, budget limit, concurrent task limit).
  Advisory by default; configurable to hard-block.
- **Event Emitter:** Writes lifecycle events to JSONL telemetry store and
  broadcasts to WebSocket subscribers. Guarantees JSONL write before
  acknowledgement (write-ahead semantics).
- **Dispatcher:** Strategy interface that delegates to the configured
  distributor. Default: Direct Distributor (in-process, straight-through).

### C4 Level 3 — Component View: Query Service

```
┌─────────────────────────────────────────────────────┐
│ Query Service                                        │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Task Query   │  │ Telemetry    │  │ Artifact  │ │
│  │ Repository   │  │ Query        │  │ Index     │ │
│  │              │  │              │  │           │ │
│  │ YAML files   │  │ JSONL/SQLite │  │ Filesystem│ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Aggregation Layer                               │ │
│  │  - Run-level rollup                             │ │
│  │  - Agent portfolio                              │ │
│  │  - Cost summaries                               │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

- **Task Query Repository:** Reads task YAML files. Wraps existing
  `src/domain/collaboration/task_query.py`.
- **Telemetry Query:** Reads from SQLite materialized view. Wraps existing
  `src/llm_service/telemetry/logger.py`.
- **Artifact Index:** Resolves artifact paths and metadata from filesystem.
- **Aggregation Layer:** Computes run-level rollups, agent portfolios,
  cost summaries. Wraps existing dashboard logic.

### CQRS Pattern

The architecture applies Command Query Responsibility Segregation at the
container level:

```
  WRITE (Command) PATH              READ (Query) PATH
  ─────────────────                  ──────────────────
  Control Plane                      Control Plane
       │                                  │
       ▼                                  ▼
  Coordination Service              Query Service
       │                                  │
       ▼                                  │
  Distributor                             │
       │                                  │
       ▼                                  │
  Execution Adapter                       │
       │                                  │
       ▼                                  ▼
  Storage (write)                    Storage (read)
  - JSONL append                     - JSONL / SQLite scan
  - YAML file move                   - YAML file read
  - Artifact write                   - Artifact path resolve
```

**Key invariants:**
1. The Query Service never mutates state.
2. The Coordination Service never reads telemetry for its own decisions
   (governance constraints come from policy configuration, not query state).
3. YAML task files are written by the Coordination Service and scripts only.
   The dashboard and Query Service are read-only consumers.

### Distributor Strategy Pattern

The Distributor layer uses the Strategy pattern to decouple dispatch
mechanics from the Coordination Service:

```python
class Distributor(ABC):
    """Strategy interface for task dispatch."""

    @abstractmethod
    async def dispatch(self, task: Task, adapter: ToolAdapter) -> ExecutionHandle:
        """Dispatch task to execution adapter. Returns handle for cancellation."""
        ...

class DirectDistributor(Distributor):
    """Straight-through in-process dispatch. Default strategy."""
    ...

class QueueDistributor(Distributor):          # DEFERRED
    """Buffered dispatch with backpressure."""
    ...

class WorkflowDistributor(Distributor):       # DEFERRED
    """Durable workflow orchestration."""
    ...
```

The Direct Distributor is the only required implementation. It calls the
execution adapter directly within the asyncio event loop, using semaphores
for concurrency control.

### Data Model: Run Container (ADR-048)

The architecture introduces **Run** as a first-class grouping concept:

```yaml
# Example: runs/RUN-20260213-001/run.yaml
id: RUN-20260213-001
created_at: 2026-02-13T10:00:00Z
phase: architecture
agent_role: architect-alphonso
status: running           # pending | running | completed | cancelled | error
tasks:
  - task_id: 2026-02-13T1000-arch-review
    status: completed
  - task_id: 2026-02-13T1015-adr-draft
    status: running
summary: "Architecture review and ADR creation for control plane"
```

- A **Run** is an umbrella container for coherent work (e.g., one iteration
  cycle, one feature implementation).
- **Tasks** remain the atomic execution unit. Their YAML lifecycle in
  `work/collaboration/` is unchanged.
- Runs reference tasks by ID. Run state is derived from constituent task
  states.
- Run YAML files are stored separately from task files to avoid coupling.

### Telemetry Architecture

```
  Event Source          Write Path            Read Path
  ────────────         ──────────            ─────────
  Coordination    ──►  JSONL file   ──────►  SQLite index
  Service               (append)              (materialized)
                                                   │
  Execution       ──►  JSONL file                  │
  Adapter               (append)                   │
                                                   ▼
                                             Query Service
                                                   │
                                                   ▼
                                             Dashboard / TUI
```

**JSONL** is the write-ahead log. Every event is appended with `fsync`
before acknowledgement. Schema per event:

```json
{
  "ts": "2026-02-13T10:05:23Z",
  "run_id": "RUN-20260213-001",
  "task_id": "2026-02-13T1000-arch-review",
  "phase": "architecture",
  "agent_role": "architect-alphonso",
  "tool": "claude-code",
  "mode": "batch",
  "event": "task_started",
  "status": "running",
  "log_paths": {
    "stdout": "runs/RUN-20260213-001/tasks/2026-02-13T1000/stdout.log"
  },
  "summary": "Starting architecture review"
}
```

**SQLite** is a derived index rebuilt from JSONL. It powers fast queries
(cost summaries, agent stats, run history). Loss of SQLite is recoverable
by replaying the JSONL log.

---

## Implementation Considerations

### Async Execution Model

The current `RoutingEngine.execute()` is synchronous (`subprocess.run()`).
The control plane requires async execution for:
- Parallel task dispatch (semaphore-controlled)
- Non-blocking cancellation
- Event emission during execution

Migration path: wrap existing adapters in async coroutines using
`asyncio.create_subprocess_exec()`. The `ToolAdapter` ABC gains an optional
`async_execute()` method; adapters that don't implement it get a
threadpool-wrapped fallback.

### Cancellation Semantics

Signal escalation with configurable timeouts:

1. **SIGINT** — request graceful shutdown (10s default)
2. **SIGTERM** — forceful termination (5s default)
3. **SIGKILL** — hard kill (immediate, last resort)

The `ExecutionHandle` returned by the Distributor provides:
- `cancel()` — initiate signal escalation
- `is_running()` — check execution state
- `wait()` — await completion

### Backward Compatibility

The control plane is designed as an *overlay* on existing infrastructure:

- Existing dashboard continues to work (file watcher, REST API, WebSocket)
- Existing CLI scripts (`start_task.py`, `complete_task.py`) continue to
  work — they mutate YAML files that the Query Service reads
- The `RoutingEngine` is wrapped, not replaced
- New components (Coordination Service, Query Service, JSONL telemetry)
  are additive

### Incremental Adoption

The architecture supports gradual rollout:

1. **Phase 1:** JSONL event log + Direct Distributor wrapping existing
   `RoutingEngine`. Dashboard reads JSONL via Query Service.
2. **Phase 2:** Async execution engine with cancellation. Semaphore-based
   parallelism.
3. **Phase 3:** Run container model. Dashboard shows run-level views.
4. **Phase N:** Queue/workflow distributors if scale demands it.

---

## Cross-cutting Concerns

### Security

- All services bind to `127.0.0.1` only (localhost). No remote access
  by default (ADR-032).
- JSONL telemetry stores metadata only. Prompt content is not persisted
  unless explicitly configured.
- Subprocess execution uses the existing `SubprocessWrapper` with input
  sanitization.

### Performance

- JSONL append is O(1). SQLite index rebuild is batch (periodic or
  on-demand), not per-event.
- Semaphore controls maximum concurrent tasks (configurable, default: 4).
- Dashboard WebSocket events are batched at 100ms intervals to prevent
  client overload (ADR-032 pattern).

### Auditing and Logging

- JSONL event log provides complete audit trail.
- Task YAML files in `work/collaboration/` are Git-tracked (ADR-008).
- Run YAML files follow the same Git-tracking convention.
- Work logs per Directive 014 continue to be generated by agents.

---

## Planning

- **Phase 1 (Core):** ~5 workdays
  - JSONL event writer
  - Direct Distributor wrapping RoutingEngine
  - Query Service facade extraction from dashboard
  - Reference diagram finalization
- **Phase 2 (Async):** ~5 workdays
  - Async execution wrapper
  - Cancellation support
  - Semaphore-based parallelism
- **Phase 3 (Run Model):** ~3 workdays
  - Run YAML schema and lifecycle
  - Dashboard run-level views
  - Run-to-task relationship tracking
- **Urgency:** Medium — foundational for scaling agent parallelism
- **Estimated added value:** High — enables parallel execution, unified
  telemetry, and cancellation
- **Depends on:** ADR-047, ADR-048 acceptance

---

*Architect Alphonso — 2026-02-13*
*Decision markers: [ADR-047], [ADR-048]*
