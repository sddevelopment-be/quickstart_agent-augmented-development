# Spec Kitty × Doctrine — Analysis Summary

**Date:** 2026-02-14
**Purpose:** Consolidated summary of all analysis work evaluating integration between the Agentic Doctrine framework and Spec Kitty.

---

## What We Investigated

Two complementary questions:

1. **Can doctrine plug into Spec Kitty?** — Architectural vision alignment, governance model compatibility, integration options.
2. **How much of doctrine's surrounding infrastructure does Spec Kitty already cover?** — Gap analysis of 4 architecture design documents against Spec Kitty's actual source code.

---

## Key Finding

**The two systems are complementary, not competing.**

- **Spec Kitty** is a *workflow orchestrator* — it manages *what* work gets done through a spec-driven lifecycle (spec → plan → tasks → implement → review → accept → merge).
- **Doctrine's framework** is *execution infrastructure* — it manages *how* LLM agents are routed, observed, governed, and controlled at the infrastructure level.

The integration path is **layering**: Spec Kitty on top as the developer-facing orchestration surface, doctrine framework infrastructure underneath providing telemetry, model routing, and governance enforcement.

---

## Analysis 1: Integration Feasibility

**File:** `2026-02-14-doctrine-spec-kitty-integration-analysis.md`

### Concept Mapping

| Doctrine Concept | Spec Kitty Equivalent | Alignment |
|-----------------|----------------------|-----------|
| Guidelines (Layer 1) | Constitution | High — different granularity (layered vs single doc) |
| Directives (Layer 2) | Mission rules | Medium — missions are domain-scoped, directives are cross-cutting |
| Approaches (Layer 3) | Command templates | Medium — both provide step-by-step procedures |
| Agent Profiles | Agent config.yaml | High — both define agent capabilities and constraints |
| File-based orchestration | WP frontmatter lanes | High — both use files as coordination substrate |
| Run Container (ADR-048) | Git worktree per WP | High — both isolate work units |

### Recommended Integration: Option C — Doctrine as External Dependency

Doctrine consumed via git subtree into Spec Kitty's project structure. The constitution becomes the "compiled" output of doctrine's layered governance for a specific project context.

### Key Conflicts Identified

- **Two-masters problem:** Both systems define agent behavior rules
- **Parallel coordination:** Two file-based task systems with different schemas
- **Agent identity gap:** Doctrine profiles vs Spec Kitty agent config need a bridge

---

## Analysis 2: Infrastructure Coverage

**File:** `2026-02-14-control-plane-spec-kitty-coverage.md`

### Coverage by Architecture Document

| Document | Coverage | Verdict |
|----------|:--------:|---------|
| Control Plane Reference (CQRS) | ~35% | CLI layer strong; telemetry, CQRS events, distributor strategy missing |
| LLM Service Layer Prestudy | ~20% | Model routing, fallback chains, cost tracking, budget — all missing |
| Error Reporting System | ~5% | Entirely unaddressed by Spec Kitty |
| Local Agent Control Plane | ~25% | Task lifecycle covered; event emission, query service, async execution missing |
| **Weighted Average** | **~25%** | |

### What Spec Kitty Covers Well

- **CLI/TUI interface** — Production-quality Typer + Rich + StepTracker
- **Task lifecycle management** — WP frontmatter with kanban lane transitions
- **Agent coordination** — Multi-agent orchestrator with worktree isolation
- **Quality gates** — Merge preflight, conflict forecasting, validators

### Critical Gaps (must be built)

1. **Telemetry & observability** — No event log, no materialized views, no cost tracking
2. **LLM model routing** — No agent-to-model mapping, no fallback chains
3. **Budget enforcement** — No financial awareness
4. **CQRS event architecture** — No formal event emission or event sourcing
5. **Structured error reporting** — No CI/CD error extraction for agents
6. **Async execution & cancellation** — Synchronous only, no signal escalation

---

## Spec Kitty's Architecture (from source code)

### Ideological Layers

| Layer | Name | Core Idea |
|-------|------|-----------|
| I1 | Philosophy | "Code is source of truth; specs are change requests (deltas)" |
| I2 | Methodology | Spec-Driven Development — prescribed phase sequence |
| I3 | Governance | Constitution model — single governing document |
| I4 | Adaptability | Mission system for domain context switching |

### Technical Layers

| Layer | Name | Key Modules |
|-------|------|-------------|
| T1 | CLI Interface | `cli/` — Typer, StepTracker, 20+ command modules |
| T2 | Core Infrastructure | `core/` — config, git_ops, worktree, VCS abstraction, dependency graph |
| T3 | Mission & Workflow | `missions/` — software-dev, research, documentation adapters |
| T4 | Orchestration | `orchestrator/` — multi-agent coordination, worktree isolation |
| T5 | Quality & Validation | `merge/`, `validators/` — preflight, conflict forecasting |
| T6 | Observability | `dashboard/` — thin diagnostics (largest gap area) |

---

## Recommended Integration Roadmap

| Phase | Action | Rationale |
|-------|--------|-----------|
| **1** | Build telemetry as standalone library | Largest gap; both systems can consume it independently |
| **2** | Implement model routing in doctrine stack | Preserves Spec Kitty's model-agnostic design |
| **3** | Add event emission hooks to Spec Kitty's orchestrator | Enables CQRS read path without restructuring internals |
| **4** | Extend Spec Kitty's dashboard with real-time capabilities | Builds on telemetry + events from phases 1–3 |

---

## Artifacts Produced

| File | Description |
|------|-------------|
| `work/kitty/2026-02-14-doctrine-spec-kitty-integration-analysis.md` | Full integration feasibility analysis |
| `work/kitty/2026-02-14-control-plane-spec-kitty-coverage.md` | Infrastructure coverage gap analysis |
| `docs/architecture/diagrams/spec-kitty-doctrine-layered-integration.puml` | C4 layered integration map (PlantUML) |
| `work/kitty/SUMMARY.md` | This file |
