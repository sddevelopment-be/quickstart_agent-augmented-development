# Architecture Decision Records

## ADR-047: CQRS Pattern for Local Agent Control Plane

**status**: `Accepted`
**date**: 2026-02-13
**decision-makers**: Architect Alphonso, Human-in-Charge
**consulted**: Process Architects, Software Engineers

### Context

The framework has grown into several partially integrated subsystems:

1. **File-based task orchestration** (ADR-008) — YAML task lifecycle in `work/collaboration/`
2. **LLM routing and execution** (ADR-025) — `RoutingEngine` with tool adapters
3. **Real-time dashboard** (ADR-032) — Flask + SocketIO monitoring UI
4. **Task domain model** (ADR-042/043/046) — `TaskStatus` state machine, YAML I/O

These subsystems work independently but lack a unifying architectural model.
Write operations (starting tasks, executing tools, updating state) and read
operations (querying status, viewing costs, browsing artifacts) are
interleaved in the same code paths, particularly in the dashboard route
handlers.

As the framework moves toward parallel multi-agent execution, the need for
clear separation between command and query paths becomes acute:

- **Parallel execution** requires async command dispatch — but dashboard
  queries must not block on execution.
- **Telemetry durability** requires write-ahead semantics — but read queries
  should not pay the cost of fsync.
- **Extension points** (new distributors, new query consumers) need stable
  interfaces — mixing read/write makes these interfaces fragile.

**Prestudy reference:** `tmp/ideas/architectural_prestudy_local_agent_control_plane.md`
**Review:** `work/analysis/2026-02-13-local-agent-control-plane-review.md`

### Decision

Adopt a **CQRS (Command Query Responsibility Segregation)** pattern for the
Local Agent Control Plane, with the following structural commitments:

1. **Command path** (write side): Control planes (dashboard, CLI) send
   commands to a Coordination Service, which validates governance
   constraints, dispatches to a Distributor, and emits lifecycle events
   to a JSONL telemetry store.

2. **Query path** (read side): Control planes read through a Query Service
   facade that aggregates data from YAML task files, JSONL/SQLite
   telemetry, and the artifact filesystem.

3. **Distributor Strategy Pattern**: The Coordination Service dispatches
   via a strategy interface. The **Direct Distributor** (in-process,
   straight-through) is the default and only required implementation.
   Queue and workflow distributors are documented as deferred extensions.

4. **JSONL as write-ahead log**: All lifecycle and execution events are
   appended to a JSONL file before acknowledgement. SQLite serves as a
   materialized index for query performance.

5. **File-based task state preserved**: YAML files in `work/collaboration/`
   remain the source of truth for task lifecycle (ADR-008 unchanged).

**Reference architecture diagram:**
`docs/architecture/diagrams/control-plane-reference-architecture.puml`

**Technical design:**
`docs/architecture/design/local-agent-control-plane-architecture.md`

### Rationale

**Why CQRS?**

- **Separation of concerns**: Write-side complexity (async dispatch,
  governance validation, event emission) does not leak into read-side code.
- **Independent scaling**: Query Service can cache aggressively without
  worrying about stale-write issues. Command path can batch events without
  blocking queries.
- **Testability**: Write side tested with event assertions. Read side
  tested with fixture data. No cross-contamination.
- **Extension points**: New distributors implement one interface. New query
  consumers call one facade. Neither needs to understand the other.

**Why Direct Distributor as default?**

- The framework is local-first, single-machine. In-process dispatch has
  zero infrastructure overhead and sub-millisecond latency.
- Queue/workflow distributors add dependencies (Redis, Kestra) that
  contradict ADR-008's no-infrastructure philosophy.
- The strategy interface preserves the option without forcing the cost.

**Why JSONL + SQLite (not SQLite-only or JSONL-only)?**

- JSONL is append-only, crash-safe (partial writes are detectable), and
  trivially parseable. It serves as the durable event log.
- SQLite provides fast indexed queries for dashboard aggregations. It is
  derived data — rebuildable from JSONL.
- This mirrors write-ahead log patterns common in databases and event
  sourcing systems.

**Why preserve file-based task state?**

- ADR-008 established YAML files as the coordination medium. The entire
  orchestration system, all CLI scripts, and the dashboard depend on it.
- Migrating task state to a database would break backward compatibility
  and lose Git auditability.
- CQRS is applied at the telemetry/execution layer, not the task
  lifecycle layer.

### Envisioned Consequences

**Positive:**

- **Agility:** Clear interfaces enable parallel development of write-side
  (async engine) and read-side (query optimizations) without coordination.
- **Maintainability:** Dashboard route handlers become thin — delegate to
  Query Service for reads, Coordination Service for writes.
- **Modifiability:** Adding a TUI or API consumer requires only calling
  the Query Service and Coordination Service — no dashboard code changes.
- **Repeatability:** JSONL event log provides complete replay capability
  for debugging and auditing.
- **Ergonomics:** Unified command interface means consistent behavior
  regardless of which control plane (dashboard, CLI, TUI) initiates work.

**Negative:**

- **Agility:** Initial refactoring overhead to extract Query Service from
  dashboard inline code (~1-2 days).
- **Maintainability:** Two event stores (JSONL + SQLite) require
  consistency management. Mitigated by SQLite being derived/rebuildable.
- **Ergonomics:** Contributors must understand which path (command vs.
  query) to extend. Mitigated by clear documentation and reference diagram.

### Considered Alternatives

**Alternative 1: Monolithic Service**
- Single service handling both reads and writes with shared state.
- Rejected: Current codebase is already exhibiting the problems this
  creates — dashboard handlers mix query logic with mutation triggers.

**Alternative 2: Event Sourcing (full)**
- All state derived from event log, no YAML task files.
- Rejected: Would require rewriting the entire orchestration system.
  File-based coordination (ADR-008) is foundational and valued for its
  transparency and Git auditability.

**Alternative 3: Microservices**
- Separate processes for command and query services.
- Rejected: Over-engineered for single-machine, local-first deployment.
  In-process separation provides the same benefits without IPC complexity.

**Alternative 4: No formal pattern — incremental ad-hoc growth**
- Continue adding features to existing subsystems without a unifying model.
- Rejected: The current integration gaps are already causing friction.
  A reference architecture prevents further fragmentation.

### Related Documents

- **Technical design:** `docs/architecture/design/local-agent-control-plane-architecture.md`
- **Implementation mapping:** `docs/architecture/design/control-plane-implementation-mapping.md`
- **Reference diagram:** `docs/architecture/diagrams/control-plane-reference-architecture.puml`
- **Architectural review:** `work/analysis/2026-02-13-local-agent-control-plane-review.md`
- **Prestudy:** `tmp/ideas/architectural_prestudy_local_agent_control_plane.md`
- **ADR-008:** File-Based Async Coordination (preserved)
- **ADR-020:** Multi-Tier Agentic Runtime (aligned)
- **ADR-025:** LLM Service Layer (extended)
- **ADR-032:** Real-Time Execution Dashboard (integrated)
- **ADR-048:** Run Container Concept (companion decision)

---

**Status:** Accepted (2026-02-13)
**Approved By:** Human-in-Charge, Architect Alphonso
