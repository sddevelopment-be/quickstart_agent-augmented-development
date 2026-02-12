---
packaged: false
audiences: [process_architect, agentic-framework-core-team]
note: High-level feature framing for Planning Petra.
last_updated: 2026-02-11
---

# High-Level Feature Overview — 2026-02-11 (Updated)

**Recent Updates (2026-02-11):**
- ✅ **ADR-045** (Doctrine Concept Domain Model) - Accepted
- ✅ **ADR-046** (Domain Module Refactoring) - Accepted
- ✅ **DDR-001** (Primer Execution Matrix) - Established
- ✅ **DDR-002** (Framework Guardian Role) - Established
- ✅ **SPEC-TERM-001** (Terminology Alignment) - Draft, ready for review
- ✅ **Conceptual Alignment Initiative** - Proposed
- ✅ **Dependency Violation Fixes** - Completed (2026-02-10)
- ✅ **Generator Implementations** - Agent/Rules/ClaudeMD generators complete

**Strategic Context:**
This document tracks features emerging from architectural decisions (ADRs), doctrine decisions (DDRs), and strategic initiatives. The latest work focuses on **conceptual alignment** - establishing domain boundaries, terminology clarity, and runtime introspection of doctrine artifacts.

The open tasks inside `work/collaboration/` signal where the plan still lacks feature coverage. Themes and features below translate those signals into actionable planning anchors.

---

## 🆕 NEW: Conceptual Alignment Features (2026-02-11)

### Feature: Refactoring Techniques and Pattern-Informed Tactics (SPEC-REFACTOR-001)

- **Value Proposition:** Convert preferred refactoring and refactor-to-pattern approaches into reusable doctrine tactics so generated code quality is more consistent, explicit, and maintainable.
- **Project Fit:** Extends doctrine execution quality through procedural tactics, complements Directive 036 (Boy Scout Rule), and provides concrete execution patterns linked from refactoring directives.
- **Relative Importance:** `HIGH` for maintainability and framework consistency; `MEDIUM-HIGH` for agent onboarding and review predictability.
- **Status:** ✅ Initiative specification created (`specifications/initiatives/refactoring-techniques/initiative.md`), ✅ planning tasks created, 🔄 awaiting assignment/execution.
- **Linked Work & Dependencies:**
  - Research matrix by Researcher Ralph from canonical sources in `work/tasks/learning_refactoring_plan.md`
  - Tactic authoring and directive/index integration by Curator Claire
  - Validation pass by Code Reviewer Cindy
- **Related Specs:** `specifications/initiatives/refactoring-techniques/initiative.md`
- **Related Decisions:** DDR-001, DDR-003, DDR-010

### Feature: Doctrine Concept Domain Model (ADR-045)

- **Value Proposition:** Create Python dataclasses representing doctrine artifacts (Directive, Approach, Tactic, AgentProfile, etc.) enabling programmatic introspection, type-safe access, and automated compliance validation.
- **Project Fit:** Enables SPEC-DIST-001 (vendor tool distribution), SPEC-DASH-008 (dashboard doctrine display), and language-first architecture operationalization. Foundation for runtime doctrine queries.
- **Relative Importance:** `CRITICAL` for Language-First Architecture maturation; `HIGH` for Dashboard UI and Distribution initiatives.
- **Status:** ✅ ADR-045 Accepted (2026-02-11), ❌ Implementation tasks not yet created
- **Linked Work & Dependencies:**
  - **Prerequisites:** ADR-046 (domain module refactoring) should complete first
  - **Blocked By:** No tasks created yet
  - **Estimated Effort:** 16-24 hours (dataclasses, parsers, validators, integration)
  - **Implementation Phases:**
    1. Create `src/domain/doctrine/models.py` with dataclasses (4h)
    2. Implement parsers for directive/approach/tactic markdown (6h)
    3. Implement agent profile parser (4h)
    4. Create validators and tests (4h)
    5. Integrate with dashboard and exporters (2-6h)
- **Related Specs:** SPEC-DIST-001, SPEC-DASH-008
- **Related Decisions:** ADR-045, ADR-046, DDR-001

### Feature: Domain Module Refactoring (ADR-046)

- **Value Proposition:** Refactor `src/common/` → `src/domain/` with bounded context modules (collaboration, doctrine, specifications) reducing conceptual drift and making linguistic boundaries explicit in code structure.
- **Project Fit:** Operationalizes language-first architecture approach, addresses task polysemy identified in conceptual alignment assessment, prepares codebase for domain model implementation (ADR-045).
- **Relative Importance:** `CRITICAL` for Conceptual Alignment; blocks ADR-045 implementation.
- **Status:** ✅ ADR-046 Accepted (2026-02-11), ❌ Implementation tasks not yet created
- **Linked Work & Dependencies:**
  - **Prerequisites:** None (can start immediately)
  - **Blocks:** ADR-045 implementation (domain model needs bounded context structure)
  - **Estimated Effort:** 8-12 hours (create structure, move files, update imports, tests, docs)
  - **Implementation Phases:**
    1. Create `src/domain/` directory structure with bounded contexts (1h)
    2. Move files from `src/common/` to appropriate modules (2h)
    3. Update all import statements across codebase (3h)
    4. Update and run test suite (2h)
    5. Update documentation and architecture diagrams (2h)
- **Migration Impact:** ~50 files with import updates, coordination required during active development
- **Related Decisions:** ADR-046, ADR-042 (Shared Task Domain Model)

### Feature: Terminology Alignment and Code Refactoring (SPEC-TERM-001)

- **Value Proposition:** Systematically eliminate generic class names (Manager/Handler/Processor), standardize terminology (State/Status, Load/read, Persist/write), and implement bounded context boundaries reducing 15-20% maintenance overhead and accelerating onboarding from 2 weeks to 1 week.
- **Project Fit:** Implements language-first architecture approach from doctrine, addresses "task polysemy" (189 occurrences across 3 contexts), prevents future linguistic drift through directive enforcement.
- **Relative Importance:** `HIGH` for Language-First Architecture maturation; `HIGH` for Team Velocity and Onboarding.
- **Status:** ✅ SPEC-TERM-001 Draft (ready for review), ❌ No implementation tasks created
- **Epic:** Language-First Architecture Maturation
- **Total Estimated Effort:** ~120 hours across 7 features
- **Linked Work & Dependencies:**
  - **7 Features Defined:**
    - FEAT-TERM-001-01: Directive Updates (4h) - Can start immediately
    - FEAT-TERM-001-02: Top 5 Generic Class Refactors (31h) - High ROI quick wins
    - FEAT-TERM-001-03: Terminology Standardization (6h)
    - FEAT-TERM-001-04: Task Context Boundary Implementation (40h) - Requires ADR
    - FEAT-TERM-001-05: CQRS Research (8h)
    - FEAT-TERM-001-06: Remaining 14 Generic Refactors (52h) - Opportunistic
    - FEAT-TERM-001-07: Glossary Automation (30 min/week) - Continuous
  - **Phasing Strategy:** Phase 1 (directives + top 5 refactors) = 35h, can parallel with other work
  - **Critical Classes to Refactor:**
    - `ModelConfigurationManager` → `ModelRouter`
    - `TemplateManager` → `TemplateRenderer`
    - `TaskAssignmentHandler` → `TaskAssignmentService`
    - `OrchestrationConfigLoader` → Domain-specific name needed
    - `AgentSpecRegistry` → Domain-specific name needed
- **Related Specs:** Conceptual Alignment Initiative
- **Related Decisions:** ADR-042, ADR-045, ADR-046
- **ROI:** Prevents ~40 hours/quarter of debugging and refactoring costs

### Feature: Conceptual Alignment Initiative (Living Glossary)

- **Value Proposition:** Establish unified glossary (50-70 terms) combining framework + DDD terminology with Contextive IDE integration and visual concept mapping, creating single source of truth for ubiquitous language.
- **Project Fit:** Complements SPEC-TERM-001 by providing terminology reference, integrates ubiquitous language experiment research with doctrine framework, enables PR-level terminology validation.
- **Relative Importance:** `MEDIUM-HIGH` for Language-First Architecture; `MEDIUM` for Developer Experience.
- **Status:** ✅ Initiative Proposed, ❌ No planning doc created yet
- **Owner:** Analyst Annie
- **Estimated Effort:** 3 weeks (18-24 hours)
- **Linked Work & Dependencies:**
  - **Phase 1 (Week 1):** Glossary expansion (40+ DDD terms), Contextive integration
  - **Phase 2 (Week 2):** Contextive setup guide, stakeholder validation
  - **Phase 3 (Week 3):** Concept map generation, usage guide, spec audit
  - **Prerequisites:** None (can start immediately)
  - **Related Materials:** `docs/architecture/experiments/ubiquitous-language/`
- **Success Criteria:**
  - 50-70 core terms in `doctrine/GLOSSARY.md`
  - Contextive glossaries organized by bounded context
  - >80% of specifications reference glossary terms
- **Related Specs:** SPEC-TERM-001
- **Related Approaches:** `doctrine/approaches/living-glossary-practice.md`

---

## Open Task Themes

| Theme | Description | Linked Tasks |
| --- | --- | --- |
| Toolchain Governance & Lifecycle | Align preinstalled tooling upgrades, documentation, and telemetry so the Copilot setup remains reliable and observable. | `work/collaboration/assigned/manager/2025-11-24T0955-manager-tooling-enhancements-coordination.yaml`, `work/collaboration/assigned/architect/2025-11-24T0950-architect-version-policy-documentation.yaml`, `work/collaboration/assigned/build-automation/2025-11-24T0949-build-automation-security-checksum-verification.yaml`, `work/collaboration/assigned/build-automation/2025-11-24T0953-build-automation-parallel-installation.yaml`, `work/collaboration/assigned/build-automation/2025-11-24T0954-build-automation-telemetry-collection.yaml`, `work/collaboration/assigned/curator/2025-11-24T0951-curator-tooling-best-practices-guide.yaml`, `work/collaboration/assigned/curator/2025-11-24T0952-curator-maintenance-checklist-templates.yaml`. |
| Collaboration Infrastructure Hardening | Finish the script reorganization follow-through, add manifest upkeep, and automate lifecycle hygiene for collaboration work items. | `work/collaboration/inbox/2025-11-25T1837-curator-validate-refactor.yaml`, `work/collaboration/inbox/2025-11-25T1838-writer-editor-update-docs.yaml`, `work/collaboration/inbox/2025-11-25T1839-build-automation-test-workflows.yaml`, `work/collaboration/inbox/2025-11-28T0426-build-automation-manifest-maintenance-script.yaml`, `work/collaboration/inbox/2025-11-28T0427-build-automation-work-items-cleanup-script.yaml`. |
| Insight & Reporting Clarity | Maintain actionable narratives and efficiency guardrails coming out of POC3 and the efficiency ADRs. | `work/collaboration/inbox/2025-11-27T1956-writer-editor-followup-2025-11-24T1756-synthesizer-poc3-followup.yaml`, `work/collaboration/assigned/architect/2025-11-24T1736-architect-framework-efficiency-assessment.yaml`. |
| Multi-Tier Platform Enablement | Execute the Platform Next Steps plan so router configs, orchestrator interfaces, local workers, diagrams, and CI guards exist for the new four-tier runtime. | `work/collaboration/inbox/2025-11-30T1201-build-automation-model-router-config.yaml`, `work/collaboration/inbox/2025-11-30T1202-architect-model-client-interface.yaml`, `work/collaboration/inbox/2025-11-30T1203-scribe-model-selection-template.yaml`, `work/collaboration/inbox/2025-11-30T1204-build-automation-ollama-worker-pipeline.yaml`, `work/collaboration/inbox/2025-11-30T1205-diagrammer-multi-tier-runtime-diagram.yaml`, `work/collaboration/inbox/2025-11-30T1206-build-automation-ci-router-schema-validation.yaml`, `work/collaboration/inbox/2025-12-01T0510-backend-dev-framework-config-loader.yaml`, `work/collaboration/inbox/2025-12-01T0511-backend-dev-agent-profile-parser.yaml`, `work/collaboration/inbox/2025-12-01T0512-build-automation-router-metrics-dashboard.yaml`, `work/collaboration/inbox/2025-12-01T0513-build-automation-framework-ci-tests.yaml`. |
| Orchestration Iteration Enablement | Provide GitHub issue structures and supporting documentation so Manager Mike and companion agents can spin up orchestration cycles with consistent metadata. | _No open tasks._ |

> Distribution / Release enablement currently lacks concrete tasks but remains a mandatory feature before the next release cycle per ADR-013/014 and the 2025-11-24 distribution work log.

## Initiative: Debt / Docs / or Low-Priority Tasks

- **Intent:** Consolidate documentation, tooling governance, and cleanup work that is aging in the work queue so it does not drift further from current repo conventions.
- **Scope:** Documentation updates, policy drafts, checklists, and follow-up validations tied to earlier refactors.

Work Items (from oldest open tasks):
- `work/collaboration/assigned/architect/2025-11-24T0950-architect-version-policy-documentation.yaml` — Document version update policy for preinstalled tools.
- `work/collaboration/assigned/curator/2025-11-24T0951-curator-tooling-best-practices-guide.yaml` — Create tooling setup best practices guide.
- `work/collaboration/assigned/curator/2025-11-24T0952-curator-maintenance-checklist-templates.yaml` — Create maintenance checklist templates.
- `work/collaboration/assigned/architect/2025-11-24T1736-architect-framework-efficiency-assessment.yaml` — Assess agentic framework efficiency trends.
- `work/collaboration/assigned/curator/2025-11-25T1837-curator-validate-refactor.yaml` — Validate script reorganization and code quality improvements.
- `work/collaboration/assigned/writer-editor/2025-11-25T1838-writer-editor-update-docs.yaml` — Update documentation to reflect new script organization.

## Feature: Distribution & Release Enablement

- **Value Proposition:** Ship a portable, auditable release artifact (`quickstart-framework-<version>.zip`) plus Guardian workflows so downstream teams can adopt updates without risking local customizations. Protects portability, auditability, and upgrade confidence.
- **Project Fit:** Anchored in ADR-013 (zip distribution), ADR-014 (Framework Guardian), and ADR-020 (multi-tier runtime). Unlocks the “Distribution / Release” pillar mentioned in architecture design docs and ensures the Guardian agent has concrete automation targets.
- **Relative Importance:** `High` for Release Engineering and Security stakeholders; also satisfies NFRs around portability, integrity, and recoverability.
- **Linked Work & Dependencies:** Needs feature-level issue coverage plus follow-up tasks for packaging pipeline, install/upgrade scripts, manifest schema, and Guardian automation. Depends on `docs/architecture/design/distribution_of_releases_architecture.md`, `docs/architecture/design/distribution_of_releases_technical_design.md`, and work log `work/reports/logs/architect/2025-11-24T2105-distribution-release-architecture.md`.

## Feature: Toolchain Governance & Lifecycle

- **Value Proposition:** Keeps the Copilot toolchain secure, observable, and well-documented so any agent can bootstrap the environment quickly and confidently (lower MTTR, higher developer trust).
- **Project Fit:** Directly responds to the tooling assessment referenced by ADR-019’s trunk discipline and underpins the orchestration workflows mandated in `.github/ISSUE_TEMPLATE/run-iteration.md`.
- **Relative Importance:** `High` for Platform Ops (security checksums) and `Medium` for Documentation/Enablement stakeholders; ensures compliance with directives 016/017 for test-first scripts.
- **Linked Work & Dependencies:** Covers `work/collaboration/assigned/manager/2025-11-24T0955-manager-tooling-enhancements-coordination.yaml`, the architect version-policy task, all build-automation tasks under `.github/copilot/setup.sh`, and the curator documentation/checklist tasks noted above. Feeds into ADR-020 tiering by stabilizing Layer 0 utilities.

## Feature: Collaboration Infrastructure Hardening

- **Value Proposition:** Ensures the refactored automation stack (scripts moved into `ops/` and `validation/`) stays reliable, discoverable, and maintainable, preventing regressions in file-based orchestration.
- **Project Fit:** Required to keep `.github/workflows/*` aligned with the new hierarchy and to provide maintenance scripts (manifest upkeep, cleanup, archival) demanded by the file-based collaboration approach.
- **Relative Importance:** `Medium-High` for Build Automation and Repository Operations; reduces toil by automating manifest reconciliation and work-item hygiene.
- **Linked Work & Dependencies:** Includes curator validation, writer-editor documentation updates, workflow regression tests, manifest maintenance script, and collaboration cleanup automation tasks listed in the theme table.

## Feature: Insight & Efficiency Reporting

- **Value Proposition:** Preserves decision-quality narratives (POC3 synthesis) and quantifies framework efficiency trends so prioritization remains data-informed.
- **Project Fit:** Supports ADR-019 (trunk-based) by ensuring operations decisions rely on current efficiency metrics, and ties into ADR-021’s routing choices by clarifying quality-per-token trends.
- **Relative Importance:** `Medium` for Product/Stakeholder Comms (needs clear POC3 synthesis) and `Medium-Low` for Architecture (efficiency assessment) but blocks strategic planning if stale.
- **Linked Work & Dependencies:** Spans `work/collaboration/inbox/2025-11-27T1956-writer-editor-followup-2025-11-24T1756-synthesizer-poc3-followup.yaml` and `work/collaboration/assigned/architect/2025-11-24T1736-architect-framework-efficiency-assessment.yaml`, plus synthesizer metrics referenced there.

## Feature: Multi-Tier Platform Enablement

- **Value Proposition:** Turns the Platform Next Steps assessment into runnable assets so router configs, orchestration interfaces, local workers, and guardrails exist before we scale to multi-vendor deployments; unlocks deterministic routing plus offline execution.
- **Project Fit:** Directly implements ADR-020 and ADR-021 while honoring earlier portability (ADR-002) and metrics (ADR-009) commitments; provides the “Layer 1–3” scaffolding that Distribution/Release work will depend on.
- **Relative Importance:** `High` for Architecture and Platform Ops (router + CI enforcement), `Medium` for Documentation/Enablement (templates + directives), `Medium` for Observability (metrics, diagrams). Blocks routing rollout if incomplete.
- **Linked Work & Dependencies:** Newly created tasks: `2025-11-30T1201-build-automation-model-router-config`, `2025-11-30T1202-architect-model-client-interface`, `2025-11-30T1203-scribe-model-selection-template`, `2025-11-30T1204-build-automation-ollama-worker-pipeline`, `2025-11-30T1205-diagrammer-multi-tier-runtime-diagram`, `2025-11-30T1206-build-automation-ci-router-schema-validation`, `2025-12-01T0510-backend-dev-framework-config-loader`, `2025-12-01T0511-backend-dev-agent-profile-parser`, `2025-12-01T0512-build-automation-router-metrics-dashboard`, `2025-12-01T0513-build-automation-framework-ci-tests`; depends on `docs/architecture/assessments/platform_next_steps.md`, ADR-020, and ADR-021.

## Feature: Orchestration Iteration Enablement

- **Value Proposition:** Gives the orchestration workflow a dedicated GitHub issue scaffold plus documentation hooks so Manager Mike, Curator Claire, and future automation can spin up iterations without missing required metadata or validation steps.
- **Project Fit:** Extends `.github/ISSUE_TEMPLATE/run-iteration.md` and aligns with `docs/architecture/async_orchestration_technical_design.md`, ensuring file-based collaboration has a mirrored GitHub entry point.
- **Relative Importance:** `Medium` for Coordination stakeholders (Manager Mike, Curator Claire) and `Medium-Low` for Documentation teams; unblocks consistent iteration tracking and cross-repo visibility.
- **Linked Work & Dependencies:** `work/collaboration/inbox/2025-11-23T2134-curator-add-github-issue-type-for-orch-task.yml`, `.github/ISSUE_TEMPLATE/run-iteration.md`, `work/collaboration/AGENT_STATUS.md`, and the orchestration design reference noted above.

---

**Next Steps:** Feature definitions are mirrored inside `ops/planning/agent-scripts/issue-definitions/` so GitHub issues can be generated via `ops/planning/create-issues-from-definitions.sh`.

---

## 📊 Feature Status Summary (2026-02-11)

### Completed This Branch
- ✅ **Dependency Violation Fixes** (2026-02-10) - DDR-NNN format updates
- ✅ **Agent Generator Simplification** (2026-02-10) - Backend Dev
- ✅ **Rules Generator** (2026-02-10) - Backend Dev
- ✅ **Claude.md Generator** (2026-02-10) - Backend Dev
- ✅ **Manager Mike Orchestration Enhancement** - Profile updates
- ✅ **Dashboard Enhancements** (Partial) - Markdown rendering, priority editing, orphan task modal

### In Progress
- 🔄 **M4 Batch 4.3 - Dashboard Initiative Tracking** (Python Pedro, Frontend Freddy)
- 🔄 **Multi-Format Distribution** (Backend Dev) - Parser implementation needed

### Planned (Tasks to be Created)
- 📋 **ADR-046 Implementation** (Domain Module Refactoring) - CRITICAL, 8-12h
- 📋 **ADR-045 Implementation** (Doctrine Domain Model) - CRITICAL, 16-24h
- 📋 **SPEC-TERM-001 Phase 1** (Terminology Alignment) - HIGH, 35h
- 📋 **Conceptual Alignment Initiative** (Living Glossary) - MEDIUM-HIGH, 18-24h

### Backlog
- ⏳ **Distribution & Release Enablement** - Packaging pipeline, Guardian automation
- ⏳ **Multi-Tier Platform Enablement** - Router configs, local workers, CI guards
- ⏳ **Toolchain Governance & Lifecycle** - Version policies, best practices, telemetry

---

_Document maintained by: Planning Petra_  
_Last reviewed: 2026-02-11_  
_Next review: After ADR-046 implementation or M4 4.3 completion_
