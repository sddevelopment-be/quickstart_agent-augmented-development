# Initiatives Directory

This directory contains **specifications grouped by initiative** — strategic themes that group related features and improvements.

## Structure

```
specifications/initiatives/
├── control-plane/              # Local Agent Control Plane Architecture
├── dashboard-enhancements/     # Real-Time Dashboard & Portfolio View
├── framework-distribution/     # Multi-Tool Distribution Architecture
├── quickstart-onboarding/      # Repository Initialization & Setup Wizard
├── refactoring-techniques/     # Refactoring Tactics and Pattern References
├── src-consolidation/          # Code Consolidation & Shared Abstractions
└── [cold-storage]/             # Superseded or deferred initiatives
```

---

## Active Initiatives

### Dashboard Enhancements
**Status:** In Progress  
**Priority:** CRITICAL  
**Specifications:** 9 active  

Portfolio view, real-time execution tracking, configuration management, orphan task assignment, and docsite integration.

**Key Specs:**
- SPEC-DASH-007: Real-Time Execution Dashboard (CRITICAL)
- SPEC-DASH-003: Initiative Tracking and Portfolio View (HIGH)
- SPEC-DASH-001: Task Priority Editing (HIGH)

### Control Plane Architecture
**Status:** Draft
**Priority:** HIGH
**Specifications:** 1 active

Layered, CQRS-informed execution and observability infrastructure for the local agent control plane. Introduces a durable JSONL event log, a unified Query Service facade, async execution with cancellation support, and a Run container grouping model.

**Key Specs:**
- SPEC-CTRL-001: Local Agent Control Plane (JSONL telemetry, Query Service, async execution, Run model)

**Related ADRs:** ADR-047 (CQRS), ADR-048 (Run Container), ADR-049 (Async Execution)

### Framework Distribution
**Status:** In Progress
**Priority:** HIGH
**Specifications:** 2 active

Multi-format distribution architecture for Doctrine framework (GitHub Copilot, Claude Desktop, OpenCode AI, VSCode).

**Key Specs:**
- SPEC-DIST-001: Doctrine Framework Multi-Tool Distribution Architecture
- SPEC-DIST-002: Claude Code Distribution Optimization (CLAUDE.md, rules/, simplified agents)

### Quickstart & Onboarding
**Status:** Proposed  
**Priority:** HIGH  
**Specifications:** 2 active  

Enhanced repository initialization with interactive setup wizard, reducing setup time from hours to <15 minutes with best practices by default.

**Key Specs:**
- SPEC-QUICK-001: Enhanced Repository Initialization Sequence (automated/guided/wizard modes)
- SPEC-QUICK-002: Repository Setup Wizard (interactive Python + Rich UI)

### Src Consolidation
**Status:** Proposed  
**Priority:** HIGH  
**Specifications:** 1 active  

Consolidate duplicated abstractions between `src/framework/` and `src/llm_service/` into shared `src/common/` layer.

**Key Specs:**
- SPEC-CONSOLIDATION-001: Src/ Code Consolidation Initiative

### Refactoring Techniques
**Status:** Draft
**Priority:** HIGH
**Specifications:** 1 active

Research-backed initiative to convert preferred refactoring methods and pattern transitions into reusable doctrine tactics and directive integrations.

**Key Specs:**
- SPEC-REFACTOR-001: Refactoring Techniques and Pattern-Informed Tactics Initiative

---

## Cold Storage

Tasks and initiatives that are **superseded, completed, or deferred** are moved to `work/collaboration/fridge/` for archival purposes. They remain in version control for historical reference but are not actively tracked in the portfolio view.

### Cold Storage Categories

#### `work/collaboration/fridge/docsite-study/`
**Reason:** Feasibility study completed, ADR-022 decision made  
**Date Archived:** 2026-02-09  
**Tasks:** 5  

- Architecture diagrams for docsite metadata separation
- Feasibility documents polish and review
- Validation tooling prototype
- Stakeholder review orchestration

**Outcome:** Feasibility study concluded. Docsite metadata separation approach documented in ADR-022. No immediate implementation planned.

#### `work/collaboration/fridge/legacy-tooling/`
**Reason:** Outdated priorities, superseded by current work  
**Date Archived:** 2026-02-09  
**Tasks:** 7  

- Telemetry collection for tool usage (2025-11-24)
- Parallel installation optimization (2025-11-24)
- Workflow verification post-refactor (2025-11-25)
- Work items cleanup automation (2025-11-28)
- Router metrics dashboard integration (2025-12-01)
- Multi-tier runtime diagrams (2025-11-30)

**Rationale:** 2025-era tasks with low priority. Current focus on dashboard enhancements and framework distribution takes precedence.

#### `work/collaboration/fridge/complete/`
**Reason:** Tasks completed but pre-date current portfolio tracking  
**Tasks:** Variable (historical completed work)

#### `work/collaboration/fridge/outdated/`
**Reason:** Tasks superseded by architectural changes or requirement shifts  
**Tasks:** Variable (deprecated work items)

---

## Adding New Initiatives

When creating a new initiative:

1. **Create Directory:** `specifications/initiatives/[initiative-name]/`
2. **Add Specifications:** Individual feature specifications as `.md` files
3. **Frontmatter Format:**
   ```yaml
   ---
   id: "SPEC-XXX-NNN"
   title: "Feature Name"
   status: "draft|in_progress|implemented|complete"
   priority: "CRITICAL|HIGH|MEDIUM|LOW"
   initiative: "Initiative Name"
   features: [...]  # Optional metadata
   ---
   ```
4. **Link Tasks:** Set `specification: specifications/initiatives/[initiative]/[file].md` in task YAML files
5. **Update This README:** Add initiative to "Active Initiatives" section

---

## Retiring Initiatives

When an initiative is complete or superseded:

1. **Move Tasks:** `work/collaboration/assigned/ → work/collaboration/fridge/[category]/`
2. **Update Status:** Set `status: complete` or `status: superseded` in specification frontmatter
3. **Document in README:** Add entry to "Cold Storage" section with rationale
4. **Keep Specifications:** Do NOT delete specification files (historical reference)
5. **Update Portfolio:** Dashboard will automatically exclude cold-storage tasks

---

## Dashboard Integration

The **Portfolio View** (`/api/portfolio`) automatically:
- Groups specifications by `initiative:` frontmatter field
- Calculates progress from linked task completion
- Excludes tasks in `work/collaboration/fridge/` directories
- Shows 3-level hierarchy: **Initiative → Specification → Task**

**Note:** The `features:` array in specification frontmatter is **metadata only**, not a rendering level. Tasks link directly to specifications, not to individual features.

---

## Related Documentation

- **Doctrine Glossary:** `doctrine/GLOSSARY.md` (definitions of Initiative, Specification, Task)
- **Portfolio View:** Dashboard at `http://localhost:8080` (Initiative Tracking)
- **Work Directory:** `work/collaboration/` (task lifecycle)
- **ADRs:** `docs/architecture/adrs/` (architectural decisions)

---

**Last Updated:** 2026-02-09  
**Maintained By:** Planning Petra, Python Pedro
