---
id: "SPEC-CTRL-001"
title: "Local Agent Control Plane"
status: "draft"
initiative: "Control Plane Architecture"
priority: "HIGH"
epic: "Execution and Observability Infrastructure"
target_personas: ["software-engineer", "architect-alphonso", "agentic-framework-core-team"]
features:
  - id: "FEAT-CTRL-001-01"
    title: "JSONL Event Writer"
    priority: "P1"
    status: "planned"
  - id: "FEAT-CTRL-001-02"
    title: "Query Service Facade"
    priority: "P1"
    status: "planned"
  - id: "FEAT-CTRL-001-03"
    title: "Async Execution Engine"
    priority: "P2"
    status: "planned"
  - id: "FEAT-CTRL-001-04"
    title: "Direct Distributor"
    priority: "P2"
    status: "planned"
  - id: "FEAT-CTRL-001-05"
    title: "Run Container Model"
    priority: "P3"
    status: "planned"
created: "2026-02-13"
updated: "2026-02-13"
author: "analyst-annie"
---

# Specification: Local Agent Control Plane

**Status:** Draft
**Created:** 2026-02-13
**Last Updated:** 2026-02-13
**Author:** Analyst Annie
**Stakeholders:** Architect Alphonso, Software Engineers, Agentic Framework Core Team

---

## User Story

**As a** developer operating agent-augmented workflows
**I want** a unified control plane that manages agent execution, provides durable telemetry, and supports cancellation
**So that** I have observability and control over parallel multi-agent work without requiring cloud infrastructure

---

## Overview

The Local Agent Control Plane is a layered, CQRS-informed architecture that serves as the target state for the framework's execution and observability subsystems. It unifies the existing routing engine, task orchestration, and dashboard into a coherent model with clearly separated write (command) and read (query) paths.

**Problem Solved:** The existing subsystems (doctrine governance, file-based orchestration, LLM routing, real-time dashboard) work independently but lack a unifying architecture. This creates an observability gap, prevents parallel task execution, and makes cancellation impossible.

**Constraints:**
- MUST remain local-first. No cloud services required for core operation.
- MUST preserve file-based task orchestration (YAML in `work/collaboration/`, ADR-008).
- MUST maintain backward compatibility with existing CLI scripts and the dashboard.
- MUST NOT introduce infrastructure dependencies (databases, message brokers) for the default path.

**Related Documentation:**
- ADR-047: [CQRS Pattern for Local Agent Control Plane](../../../docs/architecture/adrs/ADR-047-cqrs-local-agent-control-plane.md)
- ADR-048: [Run Container Concept](../../../docs/architecture/adrs/ADR-048-run-container-concept.md)
- ADR-049: [Async Execution Engine with Cancellation](../../../docs/architecture/adrs/ADR-049-async-execution-engine.md)
- Technical Design: [Local Agent Control Plane Architecture](../../../docs/architecture/design/local-agent-control-plane-architecture.md)
- Implementation Mapping: [Control Plane Implementation Mapping](../../../docs/architecture/design/control-plane-implementation-mapping.md)

---

## Functional Requirements (MoSCoW)

### MUST Have

**FR-M1:** The system MUST append all lifecycle and execution events to a durable JSONL event log before acknowledging execution start.
- **Rationale:** Provides a complete audit trail and enables replay-based index recovery (ADR-047).
- **Success Criteria:** Every `task_started`, `task_completed`, `task_cancelled`, and `task_error` event is written to JSONL with `fsync` before the caller receives acknowledgement.

**FR-M2:** The system MUST separate command (write) operations from query (read) operations at the service boundary.
- **Rationale:** CQRS pattern prevents read-path state mutations and clarifies architectural responsibility (ADR-047).
- **Success Criteria:** No read operation in the Query Service mutates state. No write operation in the Coordination Service reads telemetry for its own decisions.

**FR-M3:** The system MUST preserve YAML file-based task state as the source of truth for task lifecycle.
- **Rationale:** ADR-008 is a non-negotiable foundation. Existing scripts and workflows must continue to function.
- **Success Criteria:** Task YAML files in `work/collaboration/` continue to move through the lifecycle (new → assigned → in_progress → done → archive) unchanged.

**FR-M4:** Existing CLI scripts (`start_task.py`, `complete_task.py`, `freeze_task.py`) and the dashboard MUST continue to operate without modification.
- **Rationale:** Backward compatibility is required. The control plane is an overlay, not a replacement.
- **Success Criteria:** All existing tests pass. No CLI script interface changes. Dashboard REST and WebSocket API unchanged.

**FR-M5:** The system MUST provide a unified Query Service facade that the dashboard and future interfaces can share.
- **Rationale:** Query logic is currently scattered across dashboard route handlers, making reuse impossible (implementation mapping gap analysis).
- **Success Criteria:** A `QueryService` class exists that encapsulates task queries, telemetry queries, and spec/progress queries. Dashboard route handlers use it exclusively for reads.

### SHOULD Have

**FR-S1:** The system SHOULD support async subprocess execution to enable parallel task dispatch.
- **Rationale:** Current `subprocess.run()` is blocking. Parallelism requires `asyncio.create_subprocess_exec()` (ADR-049).
- **Workaround if omitted:** Sequential execution only; parallelism deferred.

**FR-S2:** The system SHOULD support task cancellation via signal escalation (SIGINT → SIGTERM → SIGKILL).
- **Rationale:** Human operators must be able to interrupt runaway or misdirected agent execution (ADR-049).
- **Workaround if omitted:** Cancellation requires manual process kill; poor operator experience.

**FR-S3:** The system SHOULD provide an `ExecutionHandle` object returned by dispatch that allows callers to cancel, check state, and await completion.
- **Rationale:** Required for cancellation support and non-blocking monitoring.
- **Workaround if omitted:** No programmatic cancellation interface.

**FR-S4:** The system SHOULD formalize the Direct Distributor as an explicit strategy implementing a `Distributor` ABC.
- **Rationale:** Establishes the extension point for future Queue and Workflow distributors without modifying the Coordination Service (ADR-047).
- **Workaround if omitted:** Future distributor variants require Coordination Service modification.

**FR-S5:** The system SHOULD support a semaphore-based concurrency limit (default: 4 parallel tasks).
- **Rationale:** Prevents resource exhaustion on developer hardware.
- **Workaround if omitted:** Unbounded parallelism; risk of system overload.

### COULD Have

**FR-C1:** The system COULD introduce a Run container that groups related tasks under a single logical execution unit.
- **Rationale:** Provides a higher-level view of coherent work (e.g., one iteration cycle) in dashboard and telemetry (ADR-048).
- **If omitted:** No run-level grouping; tasks remain the only visible unit.

**FR-C2:** The system COULD provide dashboard run-level views showing run status derived from constituent task states.
- **Rationale:** Improves operator situational awareness during multi-task operations.
- **If omitted:** Operators must mentally aggregate individual task states.

**FR-C3:** The system COULD rebuild the SQLite telemetry index from the JSONL log on demand.
- **Rationale:** Provides durability; SQLite loss is recoverable by log replay.
- **If omitted:** SQLite corruption requires manual recovery.

### WON'T Have (This Release)

**FR-W1:** The system will NOT implement a Queue Distributor (Redis, asyncio.Queue).
- **Rationale:** No current need for buffered dispatch. Adds infrastructure dependency contrary to ADR-008 philosophy.

**FR-W2:** The system will NOT implement a Workflow Distributor (Kestra, Temporal).
- **Rationale:** Enterprise-scale concern not applicable to local-first MVP.

**FR-W3:** The system will NOT implement an SDK Execution Adapter (direct OpenAI/Anthropic API).
- **Rationale:** CLI adapters are sufficient. ADR-025 explicitly deferred direct API integration.

**FR-W4:** The system will NOT implement a TUI interface.
- **Rationale:** Nice-to-have, but dependent on Query Service completion. Deferred to a follow-on initiative.

---

## Features

### FEAT-CTRL-001-01: JSONL Event Writer (P1)

**Description:** An append-only JSONL event log writer integrated into the Coordination Service Event Emitter. Every significant lifecycle event is persisted before acknowledgement.

**Event Schema:**
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

**Events to capture:** `task_started`, `task_completed`, `task_cancelled`, `task_error`, `task_frozen`.

**Storage:** Single JSONL file per run in `runs/<RUN-ID>/events.jsonl`. Appended with `fsync`.

**Acceptance Criteria:**
- Every event write completes `fsync` before function returns.
- JSONL file is valid (one JSON object per line) at all times, including after unexpected process termination.
- Estimated effort: 1-2 days.

---

### FEAT-CTRL-001-02: Query Service Facade (P1)

**Description:** A `QueryService` class that consolidates all read-side logic currently scattered across dashboard route handlers. The dashboard becomes a consumer of this facade; future interfaces (TUI, CLI) can reuse it without duplication.

**Responsibilities:**
- Task queries: wraps `src/domain/collaboration/task_query.py`
- Telemetry queries: wraps `src/llm_service/telemetry/logger.py`
- Spec/progress queries: wraps `spec_parser.py`, `task_linker.py`, `progress_calculator.py`
- Aggregation: run-level rollup, agent portfolio, cost summaries

**Key constraint:** The Query Service MUST NOT mutate any state. It is a read-only facade.

**Acceptance Criteria:**
- All existing dashboard route handlers that currently read YAML or SQLite directly are refactored to use `QueryService`.
- `QueryService` has no write-side methods.
- Existing dashboard API responses are identical before and after refactoring (regression test suite passes).
- Estimated effort: 1-2 days.

---

### FEAT-CTRL-001-03: Async Execution Engine (P2)

**Description:** Migration of the execution layer from synchronous `subprocess.run()` to `asyncio.create_subprocess_exec()`. Enables parallel task dispatch and non-blocking cancellation.

**Migration approach:**
- `ToolAdapter` ABC gains optional `async_execute()` method.
- Adapters without `async_execute()` receive a threadpool-wrapped fallback automatically.
- `ClaudeCodeAdapter` is the primary target for native async implementation.

**Concurrency control:** Semaphore with configurable limit (default: 4). Tasks that exceed the limit are queued within the asyncio event loop.

**Acceptance Criteria:**
- `ClaudeCodeAdapter.async_execute()` is implemented and passes existing adapter tests.
- Semaphore prevents more than N tasks running simultaneously (configurable via settings).
- Synchronous `execute()` method remains functional for backward compatibility.
- Estimated effort: 3-5 days.

---

### FEAT-CTRL-001-04: Direct Distributor (P2)

**Description:** Formalize the existing implicit straight-through dispatch as an explicit `DirectDistributor` class implementing the `Distributor` ABC. Returns an `ExecutionHandle` for cancellation and state observation.

**Strategy interface:**
```python
class Distributor(ABC):
    @abstractmethod
    async def dispatch(self, task: Task, adapter: ToolAdapter) -> ExecutionHandle:
        ...

class DirectDistributor(Distributor):
    """Straight-through in-process dispatch. Default strategy."""
    ...
```

**ExecutionHandle interface:**
- `cancel()` — initiates signal escalation (SIGINT → SIGTERM → SIGKILL with configurable timeouts)
- `is_running()` — returns boolean execution state
- `wait()` — awaits completion and returns result

**Cancellation signal escalation:**
1. SIGINT — graceful shutdown request (10s default timeout)
2. SIGTERM — forceful termination (5s default timeout)
3. SIGKILL — hard kill (immediate, last resort)

**Acceptance Criteria:**
- `DirectDistributor.dispatch()` returns an `ExecutionHandle` before the subprocess completes.
- `ExecutionHandle.cancel()` triggers SIGINT and escalates on timeout.
- `ExecutionHandle.is_running()` accurately reflects subprocess state.
- Cancellation emits a `task_cancelled` event to the JSONL log.
- Estimated effort: 1 day (distributor) + 2 days (cancellation) = 3 days.

---

### FEAT-CTRL-001-05: Run Container Model (P3)

**Description:** A first-class Run concept that groups related tasks under a single logical execution unit. Runs have their own YAML schema stored separately from task files. Run state is derived from constituent task states.

**Run YAML schema:**
```yaml
# runs/RUN-20260213-001/run.yaml
id: RUN-20260213-001
created_at: 2026-02-13T10:00:00Z
phase: architecture
agent_role: architect-alphonso
status: running   # pending | running | completed | cancelled | error
tasks:
  - task_id: 2026-02-13T1000-arch-review
    status: completed
  - task_id: 2026-02-13T1015-adr-draft
    status: running
summary: "Architecture review and ADR creation for control plane"
```

**Run state derivation rules:**
- `running` if any constituent task is `in_progress`
- `completed` if all tasks are `done`
- `cancelled` if any task is `cancelled` and none are `in_progress`
- `error` if any task is in an error state

**Dashboard integration:** Run-level views showing aggregated status, progress, and cost per run.

**Acceptance Criteria:**
- Run YAML files are created on run start and updated on task state changes.
- Run state is correctly derived from constituent tasks for all state combinations.
- Dashboard displays run-level view with status, task count, and cost rollup.
- Run YAML files are Git-tracked alongside task files.
- Estimated effort: 1-2 days (schema) + 2-3 days (dashboard view) = 4-5 days.

---

## Scenarios and Behavior

### Scenario 1: Task Execution with Telemetry

**Given** a developer initiates a task via the dashboard or CLI
**When** the Coordination Service receives the start command
**Then** a `task_started` event is appended to the JSONL log with `fsync`
**And** the Direct Distributor dispatches the task to the appropriate CLI execution adapter
**And** the dashboard receives a `task.created` WebSocket event
**And** an `ExecutionHandle` is returned to the caller

### Scenario 2: Task Cancellation

**Given** a task is running under the async execution engine
**When** the operator clicks "Cancel" on the dashboard or calls `ExecutionHandle.cancel()`
**Then** a SIGINT signal is sent to the subprocess
**And** if the process does not exit within 10 seconds, SIGTERM is sent
**And** if the process does not exit within 5 seconds after SIGTERM, SIGKILL is sent
**And** a `task_cancelled` event is appended to the JSONL log
**And** the task YAML file is updated to reflect the cancelled state

### Scenario 3: Query Service Read (No Mutation)

**Given** the dashboard requests the portfolio view
**When** the QueryService is called for initiative progress data
**Then** the QueryService reads from YAML files, SQLite telemetry, and spec parser output
**And** returns aggregated data without modifying any file or database
**And** the response is identical to the pre-refactoring behavior

### Scenario 4: Parallel Execution with Semaphore

**Given** the semaphore limit is set to 4
**And** 6 tasks are dispatched concurrently
**When** the Direct Distributor processes the dispatch queue
**Then** exactly 4 tasks are started immediately
**And** 2 tasks wait in the asyncio queue
**And** as each running task completes, a queued task is started
**And** all 6 tasks complete without resource exhaustion

### Scenario 5: JSONL Recovery

**Given** the SQLite telemetry index is corrupted or deleted
**When** the system restart triggers index rebuild
**Then** the JSONL event log is replayed from the beginning
**And** the SQLite index is fully reconstructed from JSONL events
**And** the dashboard telemetry view shows correct historical data

### Scenario 6: Run Container Grouping

**Given** a developer starts a run for an architecture review phase
**And** the run contains 3 tasks: ADR drafting, review, and implementation mapping
**When** 2 tasks complete and 1 remains in progress
**Then** the run status is `running`
**And** the dashboard run view shows "2/3 tasks complete"
**When** the final task completes
**Then** the run status transitions to `completed`
**And** the run YAML reflects the final state

---

## Acceptance Criteria

### Definition of Done

- [ ] JSONL event writer appends events with `fsync` before acknowledgement (FEAT-CTRL-001-01)
- [ ] JSONL file remains valid JSON Lines after unexpected process termination
- [ ] `QueryService` facade exists and all dashboard route handlers use it for reads
- [ ] `QueryService` has no write-side methods; existing dashboard API responses unchanged
- [ ] `async_execute()` implemented on `ClaudeCodeAdapter`; synchronous `execute()` still functional
- [ ] Semaphore enforces configurable concurrency limit (default 4)
- [ ] `DirectDistributor` implements `Distributor` ABC and returns `ExecutionHandle`
- [ ] `ExecutionHandle.cancel()` triggers SIGINT → SIGTERM → SIGKILL escalation
- [ ] Cancellation emits `task_cancelled` to JSONL log
- [ ] Run YAML schema defined and lifecycle-managed alongside task YAML
- [ ] Run state correctly derived from constituent task states (all state combinations tested)
- [ ] Dashboard displays run-level view
- [ ] Existing CLI scripts (`start_task.py`, `complete_task.py`, `freeze_task.py`) pass all existing tests unchanged
- [ ] Existing dashboard REST and WebSocket API tests pass unchanged
- [ ] Unit tests: JSONL writer, QueryService, async adapter, cancellation, run state derivation
- [ ] Integration test: end-to-end task start → execution → cancellation with JSONL verification

---

## Non-Functional Requirements

| Concern | Requirement |
|---------|-------------|
| Security | All services bind to `127.0.0.1` only. JSONL stores metadata only; prompt content not persisted by default. |
| Performance | JSONL append is O(1). SQLite index rebuild is batch (periodic or on-demand), not per-event. WebSocket events batched at 100ms intervals. |
| Auditability | JSONL log provides complete audit trail. Run and task YAML files are Git-tracked. |
| Recoverability | SQLite loss is recoverable by replaying JSONL. No data loss on process crash after `fsync`. |

---

## Implementation Phasing

| Phase | Features | Estimated Effort | Dependencies |
|-------|----------|-----------------|--------------|
| Phase 1 (Core) | FEAT-CTRL-001-01 (JSONL), FEAT-CTRL-001-02 (Query Service) | ~5 workdays | None |
| Phase 2 (Async) | FEAT-CTRL-001-03 (Async Engine), FEAT-CTRL-001-04 (Direct Distributor) | ~5 workdays | Phase 1 JSONL writer |
| Phase 3 (Run Model) | FEAT-CTRL-001-05 (Run Container) | ~3-5 workdays | Phase 1 complete |

**Total estimated effort:** ~13-15 workdays
**Urgency:** Medium — foundational for scaling agent parallelism
**Estimated value:** High — enables parallel execution, unified telemetry, and cancellation

---

## Open Questions

None at time of drafting. Implementation approach is defined in the approved technical design.

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Async migration breaks existing adapters | HIGH | MEDIUM | Synchronous `execute()` remains as fallback; async is additive |
| Dashboard route refactoring introduces regressions | HIGH | MEDIUM | Write regression tests against current API responses before refactoring |
| Cancellation race conditions | MEDIUM | MEDIUM | Write tests for cancellation semantics before implementation (TDD per project conventions) |
| JSONL file growth over time | LOW | LOW | Runs are isolated per-run; archiving strategy to be defined in Phase 3 |

---

## References

- ADR-047: `docs/architecture/adrs/ADR-047-cqrs-local-agent-control-plane.md`
- ADR-048: `docs/architecture/adrs/ADR-048-run-container-concept.md`
- ADR-049: `docs/architecture/adrs/ADR-049-async-execution-engine.md`
- Technical Design: `docs/architecture/design/local-agent-control-plane-architecture.md`
- Implementation Mapping: `docs/architecture/design/control-plane-implementation-mapping.md`

---

**Prepared by:** Analyst Annie
**Date:** 2026-02-13
**Status:** Draft — ready for implementation planning
