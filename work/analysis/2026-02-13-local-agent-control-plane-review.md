# Architectural Review: Local Agent Control Plane (CQRS)

**Reviewer:** Architect Alphonso
**Date:** 2026-02-13
**Status:** FIRST PASS
**Mode:** `/analysis-mode`
**Documents Reviewed:**
- `tmp/ideas/architectural_prestudy_local_agent_control_plane.md`
- `tmp/ideas/agent_control_plane_architecture_v3_cqrs.puml`

---

## 1. Executive Summary

The prestudy proposes a **Local Agent Control Plane** that provides a unified
command/query surface over heterogeneous CLI-based agent tools, adding an
execution daemon, telemetry store, and CQRS-style read/write separation. The
accompanying PlantUML diagram introduces a **Distributor (Strategy) Layer**
with three distribution strategies (Direct, Queue, Kestra) and a **Query API**
that reads from telemetry and artifact storage.

**Verdict:** The idea is architecturally sound and directionally aligned with
the existing codebase. It represents a natural *next evolution* of what is
already partially built. However, the prestudy introduces several concepts
that overlap with — and in some cases duplicate — existing implemented
components. Adoption requires careful scoping to avoid rework and to preserve
the file-based orchestration foundation (ADR-008/009).

**Risk level:** Medium. The design is valid but scope creep is the primary
danger.

---

## 2. Alignment with Existing ADRs

### 2.1 Strong Alignment

| ADR | Alignment | Notes |
|-----|-----------|-------|
| **ADR-020** (Multi-Tier Runtime) | **High** | The prestudy's layers map cleanly to ADR-020's four tiers: Dashboard/TUI = Layer 0, Task Service = Layer 1, Distributor = Layer 2, Execution Adapters = Layer 3. |
| **ADR-025** (LLM Service Layer) | **High** | The "Coordination ACL / Task Service" in the CQRS diagram is conceptually the same as the existing `RoutingEngine` + adapter registry. The prestudy's tool wrappers map to existing `ToolAdapter` ABCs. |
| **ADR-029** (Adapter Interface) | **High** | CLI Execution Adapter and SDK Execution Adapter in the diagram are specializations of the existing `ToolAdapter` ABC pattern. |
| **ADR-032** (Real-Time Dashboard) | **High** | The prestudy's Dashboard UI is already implemented (Flask + SocketIO + file watcher). Query side of CQRS maps to existing REST API endpoints (`/api/stats`, `/api/tasks`, `/api/portfolio`). |

### 2.2 Tensions and Gaps

| ADR | Tension | Risk |
|-----|---------|------|
| **ADR-008** (File-Based Async Coordination) | The prestudy introduces a **JSONL telemetry store** and **optional SQLite** as primary data stores. This creates a *dual truth* problem: task lifecycle remains in YAML files, but execution telemetry lives in JSONL/SQLite. ADR-008 explicitly chose files over databases for auditability. | **Medium** — Acceptable if JSONL is append-only telemetry (not task state), and YAML remains the source of truth for task lifecycle. The prestudy's framing is correct here but needs explicit boundary statements. |
| **ADR-008** (File-Based Async Coordination) | The Queue Distributor (Redis/NATS) and Kestra Distributor introduce **infrastructure dependencies** that ADR-008 explicitly rejected. | **High** — These should be clearly marked as future/optional extensions, not default paths. The Direct Distributor (straight-through) must remain the default and only required path. |
| **ADR-025** (LLM Service Layer) | ADR-025 explicitly states "local machine usage only, with CLI-based interaction" and rejected remote API services. The prestudy's daemon model is borderline — it runs locally but introduces a service process. | **Low** — A local daemon is acceptable; it's the same pattern as `flask run` for the dashboard. But it should not become a mandatory prerequisite for running agents. |

### 2.3 Missing ADR Coverage

The prestudy introduces concepts that have no existing ADR:

1. **CQRS pattern for local agent orchestration** — Needs its own ADR if adopted.
2. **Distributor / Strategy pattern** — The abstraction over dispatch mechanisms (direct, queue, workflow engine) is new and needs a decision record.
3. **Run as first-class concept** — The prestudy's "Run" (umbrella container) does not exist in the current task model. Tasks exist, but runs-as-containers-of-tasks do not.

---

## 3. Overlap with Existing Code

The codebase already implements significant portions of what the prestudy describes. Here is a mapping:

| Prestudy Component | Existing Implementation | Gap |
|---------------------|------------------------|-----|
| **Dashboard UI** | `src/llm_service/dashboard/app.py` — Flask + SocketIO, REST API, file watcher, WebSocket events, portfolio view | Minimal. Existing dashboard is functional. Prestudy adds no new dashboard capability. |
| **Task Runner / LLM Service** | `src/llm_service/routing.py` — `RoutingEngine` with agent routing, cost optimization, fallback chains, adapter registry, `execute()` method | Moderate. Existing engine is synchronous single-shot. Prestudy envisions a persistent daemon with parallelism and cancellation. |
| **Tool Wrappers** | `src/llm_service/adapters/` — `ToolAdapter` ABC, `ClaudeCodeAdapter`, `GenericYAMLAdapter`, `SubprocessWrapper` | Small. Prestudy's YAML tool config is already implemented via `GenericYAMLAdapter`. |
| **Telemetry Store** | `src/llm_service/telemetry/logger.py` — SQLite cost/usage tracking | Small. SQLite telemetry already exists. Prestudy adds JSONL as primary + SQLite as index, which is a reasonable enrichment. |
| **Task Lifecycle** | `src/domain/collaboration/types.py` — `TaskStatus` state machine, `src/framework/orchestration/agent_orchestrator.py` — coordinator | Small. State machine, validation, file-based lifecycle all implemented. |
| **Concurrency / Parallelism** | Not implemented | **Significant gap.** The existing `RoutingEngine.execute()` is synchronous. The prestudy's asyncio subprocess orchestration is genuinely new. |
| **Cancellation / Timeouts** | `SubprocessWrapper` has timeout; `agent_orchestrator` has `check_timeouts()` | Moderate. Basic timeout exists but graceful cancellation (SIGINT → SIGTERM → SIGKILL) is not implemented. |
| **Interactive mode** | Not implemented | **New.** Pseudo-TTY attachment for interactive tool use is not in the current codebase. |
| **OpenCode TUI** | Not implemented (external tool) | N/A — External dependency, integration point only. |

### Key Observation

The prestudy reads as if it was written *before* the current `src/llm_service/` and `src/domain/` code existed. Many components described as "to be built" are already built. The review should focus on **what is genuinely new**:

1. Asyncio execution engine with parallelism
2. CQRS command/query separation as an explicit pattern
3. Distributor strategy abstraction
4. Run-level container concept
5. Interactive mode (pseudo-TTY)
6. JSONL append-only event log

---

## 4. Feasibility Assessment

### 4.1 Direct Distributor (Straight-Through)

**Feasibility: High.**
This is essentially what exists today — `RoutingEngine.execute()` routes and invokes synchronously. Wrapping this in an asyncio task with lifecycle events is straightforward.

**Effort estimate:** 2-3 days to wrap existing `RoutingEngine` in an async execution loop with event emission.

### 4.2 Queue Distributor (Redis / NATS)

**Feasibility: Medium, but questionable value for local-first.**
Adds infrastructure dependency. For a single-machine, local-first tool, an in-process asyncio task queue (e.g., `asyncio.Queue`) achieves the same concurrency benefits without requiring Redis.

**Recommendation:** Defer. Use `asyncio.Queue` internally. Add Redis/NATS only if multi-machine distribution becomes a requirement (which contradicts current design philosophy).

### 4.3 Kestra Distributor

**Feasibility: Low for near-term.**
Kestra is a workflow orchestration platform. Integrating it introduces a heavy external dependency, requires Kestra to be running, and shifts complexity to workflow definition authoring.

**Recommendation:** Exclude from initial scope. Document as a future extension path in the ADR.

### 4.4 CQRS Split (Command vs. Query)

**Feasibility: High, already partially implemented.**
The dashboard already implements read-only queries (`/api/stats`, `/api/tasks`) separate from write operations (file watcher detects mutations, dashboard emits WebSocket events). The CQRS pattern is *implicit* in the current design.

Making it *explicit* via a `QueryService` / `Repository` facade would improve code organization and testability. This is a refactoring opportunity, not a new build.

**Effort estimate:** 1-2 days to extract a `TaskQueryService` from the dashboard's inline query logic.

### 4.5 JSONL Telemetry

**Feasibility: High.**
Append-only JSONL is trivial to implement. The question is whether it replaces, supplements, or duplicates the existing SQLite telemetry.

**Recommendation:** Use JSONL as the primary event log (append-only, durable). Keep SQLite as a materialized view / index for queries. This matches the prestudy's recommendation and is compatible with the existing `telemetry/logger.py`.

### 4.6 Asyncio Execution Engine

**Feasibility: High but requires careful integration.**
The existing `SubprocessWrapper` uses synchronous `subprocess.run()`. Moving to `asyncio.create_subprocess_exec()` requires:
- Async adapter interface (or async wrapper around existing sync adapters)
- Semaphore-based concurrency control
- Cancellation token / signal handling

This is the most significant implementation effort in the proposal.

**Effort estimate:** 3-5 days for core async engine + cancellation.

---

## 5. Architectural Concerns

### 5.1 Daemon vs. On-Demand

The prestudy implies a persistent daemon process. The current codebase uses on-demand execution (CLI invocations, periodic orchestrator runs). A daemon adds:
- Process management complexity (start, stop, health check, crash recovery)
- Port binding / socket management
- State persistence across restarts

**Recommendation:** Start with on-demand + background execution via the existing dashboard process. The Flask + SocketIO server already runs as a long-lived process and can host the async execution engine. No separate daemon needed initially.

### 5.2 Data Model: Run vs. Task

The prestudy introduces "Run" as a container for multiple tasks. The current model has only tasks (with `next_agent` for chaining). Adding a Run concept means:
- New YAML schema for runs
- Run-to-task relationship tracking
- Run-level aggregation in dashboard
- Run-level cancellation semantics

This is a meaningful data model change. It should be an explicit ADR decision.

### 5.3 Telemetry Dual-Write

Writing events to both JSONL and SQLite creates a consistency question. Which is authoritative? What happens on partial write failure?

**Recommendation:** JSONL is the write-ahead log (append-only, always written). SQLite is derived (rebuilt from JSONL if needed). This gives clear recovery semantics.

### 5.4 SDK Execution Adapter

The CQRS diagram shows an "SDK Execution Adapter (OpenAI / Claude Agents)". This implies direct API integration — calling LLM APIs programmatically rather than through CLI tools. ADR-025 considered and rejected this for MVP ("CLI tools already solve these problems").

**Recommendation:** Keep as a documented future extension. The `ToolAdapter` ABC already supports this — a new `APIAdapter` subclass could call APIs directly. But it's not needed now and adds authentication/rate-limiting complexity.

---

## 6. What to Build (Recommended Scope)

### Phase 1: Async Execution Core (Priority: High)

1. **Async execution wrapper** around existing `RoutingEngine.execute()`
   - `asyncio.create_subprocess_exec()` replacing `subprocess.run()`
   - Semaphore for max parallel tasks
   - Cancellation via signal escalation (SIGINT → SIGTERM → SIGKILL)
2. **JSONL event log** — append-only lifecycle events
   - Event schema (the prestudy's schema is a reasonable starting point)
   - Writer module with fsync guarantee
3. **Direct Distributor** — straight-through dispatch (wrap existing routing)

### Phase 2: Query Separation (Priority: Medium)

4. **TaskQueryService** — extract read logic from dashboard into a facade
   - Read from YAML files (task state) + JSONL (telemetry) + SQLite (cost)
   - Serve dashboard API endpoints through this facade
5. **Dashboard integration** — wire existing dashboard to query service

### Phase 3: Run Container (Priority: Medium)

6. **Run data model** — YAML schema, run-to-task relationships
7. **Run lifecycle** — start, cancel, aggregate status
8. **Dashboard run view** — run-level progress and artifact grouping

### Defer

- Queue Distributor (Redis/NATS) — no current need
- Kestra Distributor — external dependency, enterprise-scale concern
- SDK Execution Adapter — CLI adapters sufficient
- Interactive mode (pseudo-TTY) — complex, niche use case
- Separate daemon process — use dashboard server as host

---

## 7. Proposed Next Steps

1. **Write ADR-047: CQRS Pattern for Local Agent Control Plane**
   - Document the command/query separation decision
   - Capture the Direct Distributor as default strategy
   - Record the JSONL + SQLite telemetry architecture
   - Reference this review

2. **Write ADR-048: Run Container Concept**
   - Define Run as first-class entity
   - Document relationship to existing Task model
   - Schema design

3. **Spike: Async Execution Engine** (2-3 days)
   - Prototype `asyncio` wrapper around `RoutingEngine.execute()`
   - Validate cancellation semantics
   - Measure concurrency behavior with semaphore

4. **Refactor: Extract TaskQueryService** (1-2 days)
   - Pull read-side logic out of `dashboard/app.py` into a dedicated service
   - This is low-risk and immediately improves code organization

5. **Update prestudy document**
   - Annotate with "already built" markers for existing components
   - Narrow scope to genuinely new work

---

## 8. Verdict

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Architectural validity** | ✅ Sound | CQRS, event sourcing, strategy pattern are well-established. Appropriate for the problem. |
| **ADR alignment** | ⚠️ Mostly aligned | Tensions with ADR-008 (infrastructure dependencies) need resolution. Queue/Kestra distributors should be deferred. |
| **Fit with existing code** | ⚠️ Significant overlap | Much of what the prestudy describes already exists. Review should narrow to genuinely new capabilities. |
| **Feasibility** | ✅ High for core | Async engine + JSONL + query separation are all achievable. Kestra integration is not feasible near-term. |
| **Scope risk** | ⚠️ High | The prestudy covers too much ground. Needs aggressive scoping to avoid a 6-month project. |
| **Value** | ✅ Clear | Parallel execution, cancellation, and unified telemetry solve real pain points. |

**Overall: PROCEED with scoped Phase 1 + ADR documentation. Defer infrastructure-dependent components.**

---

*Architect Alphonso — 2026-02-13*
*Review based on: prestudy document, CQRS PlantUML, full codebase analysis of src/, docs/architecture/adrs/, and work/ directory.*
