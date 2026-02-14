# Control Plane Architecture — Spec Kitty Coverage Analysis

**Author:** Architect Alphonso
**Date:** 2026-02-14
**Status:** Draft
**Scope:** Assesses how much of the framework surrounding doctrine (4 architecture design docs) is already covered by the Spec Kitty ecosystem.

---

## 1. Executive Summary

**Overall coverage estimate: ~35–40%**

Spec Kitty provides strong coverage of the **Control Plane** (CLI/UI) and **Task Lifecycle** layers, partial coverage of the **Execution Layer** (agent coordination, worktree isolation), but has significant gaps in **telemetry/observability**, **LLM service routing**, **CQRS query infrastructure**, and **structured error reporting**. The two systems are architecturally complementary: Spec Kitty excels at developer-facing workflow orchestration while the doctrine framework's surrounding architecture targets infrastructure-level concerns (model routing, cost tracking, telemetry materialization, signal-based cancellation).

---

## 2. Layer-by-Layer Coverage Matrix

Assessed against the 5-layer Control Plane Reference Architecture (CQRS):

| Layer | Component | Spec Kitty Coverage | Notes |
|-------|-----------|:-------------------:|-------|
| **Control Planes** | Localhost Dashboard | 🟡 Partially | `dashboard/` module provides diagnostics, but not real-time SocketIO-based task state or cost metrics |
| | Interactive Console (CLI/TUI) | ✅ Fully Covered | Typer-based CLI with StepTracker, 13+ commands, Rich UI. Strong match. |
| **Service Layer** | Coordination Service | 🟡 Partially | `orchestrator/` handles multi-agent coordination; lacks formal command/event pattern (CQRS), governance validator, structured event emission |
| **Distributor Layer** | Direct Distributor | 🔄 Different Approach | Spec Kitty uses worktree-per-WP isolation + agent config, not an in-process dispatch strategy pattern |
| | Queue Distributor | ❌ Not Covered | No buffered dispatch with backpressure (deferred in doctrine design too) |
| | Workflow Distributor | ❌ Not Covered | No Kestra/Temporal integration (deferred in doctrine design too) |
| **Execution Layer** | CLI Execution Adapter | 🟡 Partially | Agent invocation via config.yaml and worktree, but no formal ToolAdapter ABC or subprocess lifecycle management |
| | SDK Execution Adapter | ❌ Not Covered | No direct LLM API calls (deferred in doctrine design too) |
| | YAML Tool Adapters | 🔄 Different Approach | Mission system (mission.yaml) provides YAML-configured workflows, but at a higher abstraction level than individual tool invocation |
| **Storage Layer** | Telemetry Store (JSONL + SQLite) | ❌ Not Covered | No append-only event log or materialized views |
| | Artifacts & Logs | 🟡 Partially | Worktree isolation provides per-WP artifact separation; no structured stdout/stderr capture |
| | Task State (YAML) | ✅ Fully Covered | WP files with frontmatter lanes provide file-based task lifecycle. Strong match with different schema. |

### Summary by Layer

| Layer | Coverage |
|-------|----------|
| Control Planes | 🟡 ~70% |
| Service Layer | 🟡 ~30% |
| Distributor Layer | ❌ ~5% (deferred items excluded) |
| Execution Layer | 🟡 ~25% |
| Storage Layer | 🟡 ~35% |

---

## 3. LLM Service Layer Gap Analysis

Assessed against the 8 acceptance tests from `llm-service-layer-prestudy.md`:

| AT | Scenario | Spec Kitty | Rating |
|----|----------|------------|:------:|
| AT-1 | Agent-to-tool routing (agent profile → CLI tool mapping) | Agent config.yaml maps agents to directories and settings; no runtime routing based on agent profiles | 🟡 |
| AT-2 | Task-based model selection (complexity → model choice) | No model routing. Agents use whatever model their host tool provides. | ❌ |
| AT-3 | Fallback chains (primary unavailable → automatic failover) | No fallback chain mechanism | ❌ |
| AT-4 | Config validation (schema enforcement for YAML configs) | Mission system validates mission.yaml; constitution provides governance validation | 🟡 |
| AT-5 | Telemetry & cost tracking (per-agent cost aggregation) | No cost tracking or telemetry aggregation | ❌ |
| AT-6 | Budget enforcement (spending limits with alerts) | No budget enforcement | ❌ |
| AT-7 | Cross-platform CLI compatibility | Typer + Rich provides cross-platform CLI. Strong match. | ✅ |
| AT-8 | Context chaining (pass context between sequential invocations) | Worktree + spec artifacts provide implicit context continuity; no explicit context-passing protocol | 🟡 |

**LLM Service Layer coverage: ~20%** — Spec Kitty deliberately sits above the LLM service layer. It orchestrates *what* work to do, not *how* to route LLM calls.

---

## 4. Error Reporting Coverage

| Capability | Spec Kitty | Rating |
|------------|------------|:------:|
| Structured JSON error reports | No structured error output format | ❌ |
| Markdown error summaries | No error summarization | ❌ |
| GitHub Actions integration | No CI/CD error action | ❌ |
| Agent-friendly error parsing | Validators module exists but focused on spec/config validation, not CI error parsing | ❌ |
| Extensible ErrorParser class | No equivalent | ❌ |
| Error artifact download + fix cycle | No equivalent | ❌ |

**Error Reporting coverage: ~5%** — This is a pure infrastructure concern that Spec Kitty does not address. Spec Kitty's validators serve a different purpose (spec compliance, not CI error extraction).

---

## 5. Control Plane Architecture Coverage

Assessed against `local-agent-control-plane-architecture.md`:

### Coordination Service

| Component | Spec Kitty | Rating |
|-----------|------------|:------:|
| Command Handler (start/cancel/retry) | CLI commands handle start; no formal cancel/retry semantics | 🟡 |
| Governance Validator | Constitution provides project-level governance; no per-command validation hook | 🟡 |
| Event Emitter | No structured event emission system | ❌ |
| Dispatcher | Orchestrator module dispatches to agents; different pattern than strategy-based dispatch | 🔄 |

### Query Service

| Component | Spec Kitty | Rating |
|-----------|------------|:------:|
| Task Query Repository | WP file frontmatter provides queryable task state | 🟡 |
| Telemetry Query | No telemetry query layer | ❌ |
| Artifact Index | No artifact indexing | ❌ |
| Aggregation Layer | Dashboard provides some aggregation; not query-service level | 🟡 |

### Run Container Model (ADR-048)

| Capability | Spec Kitty | Rating |
|------------|------------|:------:|
| First-class run grouping | Work Packages serve as grouping concept. Conceptually similar. | 🟡 |
| YAML schema for runs | WP frontmatter provides metadata schema | 🟡 |
| Run lifecycle (pending → running → completed/failed) | WP lane transitions (spec → plan → tasks → implement → review → accept → merge) | 🔄 |

### Infrastructure

| Capability | Spec Kitty | Rating |
|------------|------------|:------:|
| JSONL telemetry | Not present | ❌ |
| SQLite materialized views | Not present | ❌ |
| asyncio execution | Synchronous CLI execution | ❌ |
| Signal escalation cancellation | No signal-based cancellation | ❌ |

**Control Plane Architecture coverage: ~25%**

---

## 6. Spec Kitty's Ideological and Technical Layers

### Ideological Layers

**Layer 1 — Philosophy: "Code is Source of Truth"** (from `spec-driven.md`)

Specs are *change requests* (deltas), not permanent truth. Once implemented, the code supersedes the spec. This inverts traditional spec-driven development where specs remain authoritative. Implications: specs are ephemeral artifacts that drive work but don't accumulate as governance debt.

**Layer 2 — Methodology: Spec-Driven Development (SDD)**

A prescribed workflow: spec → plan → tasks → implement → review → accept → merge. Each phase produces artifacts that feed the next. The methodology is opinionated about *sequence* but flexible about *content* through the mission system.

**Layer 3 — Governance: Constitution Model**

The constitution (generated via 4-phase interactive discovery) captures project-level standards, code quality rules, tribal knowledge, and governance policies. This is the closest analogue to doctrine's governance stack, but it's a single document rather than a layered precedence system. It governs agent behavior within Spec Kitty's workflow.

**Layer 4 — Adaptability: Mission System**

Missions (software-dev, research, documentation) provide domain-specific workflow customization. Each mission defines phases, artifacts, validation rules, and agent context. This allows Spec Kitty to serve different development contexts without modifying core logic.

### Technical Layers

**Layer T1 — CLI Interface** (`src/specify_cli/cli/`)

Typer-based command framework with Rich UI. StepTracker pattern provides user-facing progress indication. 20+ command modules covering the full SDD lifecycle. This is the primary human interaction surface.

Key modules: `step_tracker.py`, `ui_helpers.py`, individual command files (`spec.py`, `plan.py`, `task.py`, `implement.py`, `review.py`, `accept.py`, `merge.py`, etc.)

**Layer T2 — Core Infrastructure** (`src/specify_cli/core/`)

Foundation services: configuration management, git operations, VCS abstraction (supporting both git and jujutsu), dependency graph resolution, worktree management, feature detection, project resolution. This layer is VCS-aware and provides the substrate for isolation and state management.

Key modules: `config.py`, `git_ops.py`, `worktree.py`, `vcs.py`, `dependency_graph.py`, `feature_detection.py`, `project_resolver.py`

**Layer T3 — Mission & Workflow Engine** (`src/specify_cli/missions/`)

Domain adapters that customize the SDD workflow for specific contexts. Each mission provides: workflow phase definitions, required/optional artifacts, path conventions, validation rules, MCP tool exposure, agent context configuration, and command customization via `mission.yaml`.

Missions: `software-dev/`, `research/`, `documentation/`

**Layer T4 — Orchestration & Multi-Agent** (`src/specify_cli/orchestrator/`)

Multi-agent coordination layer. Manages agent assignment, work distribution, and parallel execution across worktree-isolated workspaces. This is where Spec Kitty's multi-agent story lives.

**Layer T5 — Quality & Validation** (`src/specify_cli/merge/`, `src/specify_cli/validators/`)

Merge state persistence, preflight validation, conflict forecasting. Validators enforce spec compliance and structural correctness. This layer ensures work products meet quality gates before progression.

**Layer T6 — Observability** (`src/specify_cli/dashboard/`)

Diagnostics and status reporting. Currently focused on project state visibility rather than telemetry or cost tracking. This is the thinnest layer and the largest gap relative to the doctrine framework's architecture.

---

## 7. Synergy Opportunities

| Opportunity | Doctrine Framework Provides | Spec Kitty Provides | Combined Value |
|-------------|---------------------------|---------------------|----------------|
| **Unified CLI** | Rich TUI concepts, dashboard design | Production CLI framework (Typer + Rich + StepTracker) | Spec Kitty's CLI as the control plane UI for both systems |
| **Governance Stack** | 5-layer doctrine precedence system | Single-document constitution | Constitution as the "compiled" output of doctrine layers for a specific project |
| **Task Lifecycle** | YAML-based file orchestration in `work/collaboration/` | WP frontmatter lanes with kanban workflow | Spec Kitty's WP system as the task engine, doctrine's collaboration as the inter-agent protocol |
| **Execution Isolation** | Run Container model (ADR-048) | Git worktree-per-WP | Worktrees as the isolation mechanism for Run Containers |
| **Agent Management** | Agent profiles with model routing policies | 12 agent directories with config.yaml SSOT | Doctrine profiles feeding Spec Kitty's agent config |
| **Quality Gates** | Governance Validator in Coordination Service | Preflight validation, conflict forecasting | Doctrine governance rules enforced through Spec Kitty's validation pipeline |

---

## 8. Gaps Requiring New Development

Ranked by priority (impact × feasibility):

### Critical Gaps (not in Spec Kitty, essential for framework)

1. **Telemetry & Observability** — JSONL event log, SQLite materialized views, cost tracking. No equivalent in Spec Kitty. Must be built from scratch or integrated as a library.

2. **LLM Model Routing** — Agent-to-model mapping, fallback chains, task-based selection. Spec Kitty is model-agnostic by design. This is a distinct infrastructure layer.

3. **Budget Enforcement** — Spending limits, alerts, per-agent cost attribution. No financial awareness in Spec Kitty.

### Significant Gaps (partially addressed, need extension)

4. **CQRS Event Architecture** — Spec Kitty has command/query separation implicitly (CLI commands vs dashboard reads) but no formal event-sourced architecture. Extending Spec Kitty's core with event emission would bridge this.

5. **Structured Error Reporting** — CI/CD error extraction, agent-friendly parsing. Could be added as a Spec Kitty plugin or mission extension.

6. **Async Execution & Cancellation** — Spec Kitty runs synchronously. Adding asyncio execution with signal escalation would be a significant core change.

### Lower Priority Gaps (deferred in both systems)

7. **Queue/Workflow Distributors** — Redis-backed dispatch, Kestra/Temporal integration. Deferred in doctrine design; not needed short-term.

8. **SDK Execution Adapters** — Direct LLM API calls bypassing CLI tools. Deferred in doctrine design.

---

## 9. Recommendations

### Phase 1: Telemetry Foundation (highest ROI)
Build the JSONL telemetry layer as a standalone Python library that both Spec Kitty and the doctrine framework can consume. This addresses the largest gap (observability) without requiring changes to Spec Kitty's core.

### Phase 2: Model Routing as Doctrine Extension
Implement LLM service routing within the doctrine stack (not Spec Kitty). This preserves Spec Kitty's model-agnostic design while providing the infrastructure layer the framework needs. Expose via a clean API that Spec Kitty's orchestrator can optionally call.

### Phase 3: Event Bridge
Add lightweight event emission hooks to Spec Kitty's orchestrator and command pipeline. This enables the CQRS read path without restructuring Spec Kitty's internals. Events flow into the telemetry library from Phase 1.

### Phase 4: Unified Dashboard
Extend Spec Kitty's dashboard module with the real-time capabilities designed in the control plane architecture (SocketIO, cost metrics, artifact links). This builds on the telemetry and event infrastructure from Phases 1–3.

---

## Coverage Summary Table

| Architecture Document | Coverage | Key Gaps |
|-----------------------|:--------:|----------|
| Control Plane Reference (CQRS) | 🟡 ~35% | Telemetry, CQRS event architecture, distributor strategy |
| LLM Service Layer Prestudy | ❌ ~20% | Model routing, fallback, cost tracking, budget |
| Error Reporting System | ❌ ~5% | Entire system not addressed |
| Local Agent Control Plane | 🟡 ~25% | Event emission, query service, async execution, cancellation |
| **Weighted Average** | **~25%** | |

The framework surrounding doctrine targets a lower infrastructure level than Spec Kitty operates at. Spec Kitty is a workflow orchestrator; these architecture documents describe execution infrastructure. The integration path is not replacement but layering: Spec Kitty on top, doctrine framework infrastructure underneath.
