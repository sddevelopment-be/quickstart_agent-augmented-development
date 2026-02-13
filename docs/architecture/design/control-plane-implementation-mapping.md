# Implementation Mapping: Current Code → Control Plane Reference Architecture

**Version:** 1.0.0
**Date:** 2026-02-13
**Author:** Architect Alphonso
**Status:** Active
**Related:** `local-agent-control-plane-architecture.md`

---

## Purpose

This document maps the current codebase to the Local Agent Control Plane
reference architecture, identifying what exists, what is partial, and what
is missing. It serves as a gap analysis and implementation guide.

---

## Layer-by-Layer Mapping

### 1. Control Planes

#### Localhost Dashboard — IMPLEMENTED

| Reference Component | Current Implementation | Status |
|---------------------|----------------------|--------|
| Real-time task view | `src/llm_service/dashboard/app.py` — REST + WebSocket | Complete |
| File watcher | `src/llm_service/dashboard/file_watcher.py` — watchdog on `work/collaboration/` | Complete |
| Cost tracking | `src/llm_service/dashboard/telemetry_api.py` — SQLite queries | Complete |
| Portfolio view | `src/llm_service/dashboard/agent_portfolio.py`, `progress_calculator.py` | Complete |
| Task priority editing | `src/llm_service/dashboard/task_priority_updater.py` — PATCH endpoint | Complete |
| WebSocket events | `task.created`, `task.assigned`, `task.completed`, `task.updated`, `cost.update` | Complete |
| Static frontend | `src/llm_service/dashboard/static/` — Vanilla JS + Socket.IO | Complete |
| CSP security headers | `app.py` — `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection` | Complete |

**Gap:** Dashboard currently reads task YAML directly in route handlers.
Should be refactored to use Query Service facade for consistency with CQRS
model.

#### Interactive Console — PARTIAL

| Reference Component | Current Implementation | Status |
|---------------------|----------------------|--------|
| CLI task management | `tools/scripts/start_task.py`, `complete_task.py`, `freeze_task.py`, `list_open_tasks.py` | Complete |
| LLM service CLI | `src/llm_service/` — routing + execution via `RoutingEngine.execute()` | Complete |
| TUI interface | Not implemented | Missing |

**Gap:** No unified TUI that combines task management, execution
monitoring, and log viewing. Current interaction is via separate CLI
scripts.

---

### 2. Service Layer: Coordination Service — PARTIAL

| Reference Component | Current Implementation | Status |
|---------------------|----------------------|--------|
| Agent routing | `src/llm_service/routing.py` — `RoutingEngine.route()` | Complete |
| Cost optimization | `RoutingEngine._apply_cost_optimization()` | Complete |
| Fallback chains | `RoutingEngine._try_fallback_chain()` | Complete |
| Config validation | `src/llm_service/config/schemas.py` — Pydantic v2 schemas | Complete |
| Task assignment | `src/framework/orchestration/agent_orchestrator.py` — `assign_tasks()` | Complete |
| Timeout detection | `agent_orchestrator.check_timeouts()` — 2-hour threshold | Complete |
| Conflict detection | `agent_orchestrator.detect_conflicts()` | Complete |
| Agent status reporting | `agent_orchestrator.update_agent_status()` — writes AGENT_STATUS.md | Complete |
| **Command handler (unified)** | Not implemented — routing and orchestration are separate systems | **Missing** |
| **Governance validator** | Not implemented — policies exist in config but no pre-dispatch validation | **Missing** |
| **Event emitter (JSONL)** | Not implemented — SQLite telemetry only, no JSONL event log | **Missing** |
| **Async dispatch** | Not implemented — `RoutingEngine.execute()` is synchronous | **Missing** |

**Key insight:** The routing engine and orchestrator exist as independent
subsystems. The Coordination Service unifies them behind a single command
interface with governance validation and event emission.

---

### 3. Distributor Layer — NOT IMPLEMENTED

| Reference Component | Current Implementation | Status |
|---------------------|----------------------|--------|
| Strategy interface | Not implemented | Missing |
| Direct Distributor | Implicit — `RoutingEngine.execute()` dispatches synchronously | Implicit |
| Queue Distributor | Not applicable (deferred) | Deferred |
| Workflow Distributor | Not applicable (deferred) | Deferred |

**Key insight:** The Direct Distributor is functionally equivalent to the
existing `RoutingEngine.execute()` call. Formalizing it as a strategy
requires:
1. Extracting the dispatch step from `execute()` into a strategy interface
2. Wrapping it in an async coroutine
3. Adding `ExecutionHandle` for cancellation support

---

### 4. Execution Layer — IMPLEMENTED

| Reference Component | Current Implementation | Status |
|---------------------|----------------------|--------|
| ToolAdapter ABC | `src/llm_service/adapters/base.py` — `execute()`, `validate_config()`, `get_tool_name()` | Complete |
| ToolResponse dataclass | `src/llm_service/adapters/base.py` — status, output, exit_code, metadata | Complete |
| ClaudeCodeAdapter | `src/llm_service/adapters/claude_code_adapter.py` — cross-platform binary, model mapping | Complete |
| GenericYAMLAdapter | `src/llm_service/adapters/generic_adapter.py` — YAML-configured command templates | Complete |
| SubprocessWrapper | `src/llm_service/adapters/subprocess_wrapper.py` — timeout support | Complete |
| Output normalizer | `src/llm_service/adapters/output_normalizer.py` | Complete |
| Template parser | `src/llm_service/adapters/template_parser.py` — `{{binary}} --model {{model}}` | Complete |
| Adapter registry | `RoutingEngine._create_adapter_registry()` — creates adapters for all configured tools | Complete |
| **Async execution** | Not implemented — uses `subprocess.run()` | **Missing** |
| **Signal-based cancellation** | Not implemented — timeout only, no SIGINT/SIGTERM escalation | **Missing** |
| **SDK Execution Adapter** | Not applicable (deferred) | Deferred |

**Key insight:** The execution layer is the most complete part of the
reference architecture. The primary gap is async execution and
cancellation, which requires migrating from `subprocess.run()` to
`asyncio.create_subprocess_exec()`.

---

### 5. Query Side — IMPLICIT

| Reference Component | Current Implementation | Status |
|---------------------|----------------------|--------|
| Task query | `src/domain/collaboration/task_query.py` — `load_open_tasks()`, `find_task_files()` | Complete (domain) |
| Task schema I/O | `src/domain/collaboration/task_schema.py` — `read_task()`, `write_task()` | Complete (domain) |
| Task validation | `src/domain/collaboration/task_validator.py` | Complete (domain) |
| Status state machine | `src/domain/collaboration/types.py` — `TaskStatus` enum with transitions | Complete (domain) |
| Telemetry query | `src/llm_service/telemetry/logger.py` — SQLite `get_today_cost()`, `get_monthly_cost()` | Complete |
| Telemetry API | `src/llm_service/dashboard/telemetry_api.py` | Complete |
| Spec parsing | `src/llm_service/dashboard/spec_parser.py`, `spec_cache.py` | Complete |
| Task-to-spec linking | `src/llm_service/dashboard/task_linker.py` | Complete |
| Progress calculation | `src/llm_service/dashboard/progress_calculator.py` | Complete |
| **Unified Query Service facade** | Not implemented — query logic is scattered across dashboard route handlers | **Missing** |

**Key insight:** All the query building blocks exist. The gap is
organizational: extracting them into a `QueryService` facade that the
dashboard and future TUI can share. This is a refactoring task, not a
new-build task.

---

### 6. Storage Layer — MOSTLY IMPLEMENTED

| Reference Component | Current Implementation | Status |
|---------------------|----------------------|--------|
| Task State (YAML) | `work/collaboration/{inbox,assigned,done,archive}/` | Complete |
| Task lifecycle scripts | `tools/scripts/start_task.py`, `complete_task.py`, `freeze_task.py` | Complete |
| SQLite telemetry | `src/llm_service/telemetry/logger.py` | Complete |
| Artifact storage | Agents write to `work/reports/`, `output/` | Complete |
| **JSONL event log** | Not implemented | **Missing** |
| **Run container YAML** | Not implemented | **Missing** |

---

## Implementation Priority Matrix

Based on gap analysis, ordered by value and dependency:

| Priority | Component | Effort | Dependencies | Value |
|----------|-----------|--------|--------------|-------|
| **P1** | JSONL event writer | 1-2 days | None | Enables telemetry foundation |
| **P1** | Query Service facade extraction | 1-2 days | None | Improves code organization, enables TUI reuse |
| **P2** | Async execution wrapper | 3-5 days | JSONL writer | Enables parallelism and cancellation |
| **P2** | Direct Distributor (formalized) | 1 day | Async wrapper | Establishes strategy pattern |
| **P2** | ExecutionHandle + cancellation | 2 days | Async wrapper | Enables task control |
| **P3** | Run container schema | 1-2 days | JSONL writer | Enables grouped execution tracking |
| **P3** | Dashboard run view | 2-3 days | Run container, Query Service | User-visible feature |
| **P3** | Coordination Service (unified) | 3-5 days | All P1/P2 | Unifies routing + orchestration |
| **Deferred** | Queue Distributor | - | Coordination Service | No current need |
| **Deferred** | Workflow Distributor | - | Coordination Service | Enterprise concern |
| **Deferred** | SDK Execution Adapter | - | Async wrapper | CLI adapters sufficient |
| **Deferred** | TUI interface | - | Query Service | Nice-to-have |

---

## File Location Summary

Current implementation files mapped to reference architecture layers:

```
CONTROL PLANES
  src/llm_service/dashboard/           ← Dashboard (complete)
  tools/scripts/                       ← CLI scripts (complete)

SERVICE LAYER
  src/llm_service/routing.py           ← Routing engine (partial Coordination Service)
  src/framework/orchestration/         ← Task orchestration (partial Coordination Service)

EXECUTION LAYER
  src/llm_service/adapters/            ← Tool adapters (complete)
    base.py                            ← ToolAdapter ABC
    claude_code_adapter.py             ← Claude-specific adapter
    generic_adapter.py                 ← YAML-configured generic adapter
    subprocess_wrapper.py              ← Subprocess execution

QUERY SIDE
  src/domain/collaboration/            ← Task domain model (scattered)
    types.py                           ← TaskStatus state machine
    task_schema.py                     ← Task YAML I/O
    task_query.py                      ← Task discovery
  src/llm_service/telemetry/           ← Cost/usage queries
  src/llm_service/dashboard/           ← Dashboard-specific queries (needs extraction)

STORAGE
  work/collaboration/                  ← Task YAML state
  src/llm_service/telemetry/logger.py  ← SQLite telemetry
```

---

## Recommendations

1. **Start with P1 items** (JSONL writer + Query Service extraction). These
   are low-risk, zero-dependency improvements that create the foundation
   for everything else.

2. **Avoid "big bang" Coordination Service** build. Instead, incrementally
   wrap existing `RoutingEngine` and `AgentOrchestrator` behind the new
   interfaces. The existing code continues to work while the unified
   service grows around it.

3. **Write tests first** for the async execution wrapper. Cancellation
   semantics are tricky — signal handling, race conditions, and partial
   output all need coverage before implementation.

4. **Use the reference diagram** (`control-plane-reference-architecture.puml`)
   as the canonical map for contributor onboarding and ADR cross-references.

---

*Architect Alphonso — 2026-02-13*
