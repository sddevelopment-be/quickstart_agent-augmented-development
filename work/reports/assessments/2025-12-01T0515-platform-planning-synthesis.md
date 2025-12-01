# Platform Planning & Diagram Synthesis — 2025-12-01

## Inputs Considered
- ADRs: ADR-019 through ADR-021, plus architectural_vision.md and async_orchestration_technical_design.md.
- Planning Petra updates in `docs/planning/FEATURES_OVERVIEW.md` and new epic definitions under `ops/planning/agent-scripts/issue-definitions/`.
- Platform Next Steps assessment (`docs/architecture/assessments/platform_next_steps.md`).
- Diagram Daisy revisions under `docs/architecture/diagrams/framework/*.puml`.

## Consolidated Signals
1. **Multi-Tier Enablement:** Router catalog, orchestrator interface, and local worker automation all demand explicit tasks plus CI hooks.
2. **Iteration Support Gap:** Orchestration cycles lacked a GitHub issue template anchor; new feature + epic now track this requirement.
3. **Governance Alignment:** Distribution/Release and Toolchain features retain `High` priority and act as dependencies for routing work.

## Feature & Epic Updates
- `docs/planning/FEATURES_OVERVIEW.md` now lists six feature pillars (Distribution, Toolchain, Collaboration Hardening, Insight & Reporting, Multi-Tier Platform, Orchestration Iteration).
- New epic definition `Feature: Orchestration Iteration Enablement` ensures Manager Mike + Curator flows are represented in `planning-features-epic.yml`.
- Multi-Tier entry expanded with the following follow-up tasks to close Platform Next Steps gaps:
  - `2025-12-01T0510-backend-dev-framework-config-loader`
  - `2025-12-01T0511-backend-dev-agent-profile-parser`
  - `2025-12-01T0512-build-automation-router-metrics-dashboard`
  - `2025-12-01T0513-build-automation-framework-ci-tests`
- All new tasks validated via `python3 validation/validate-task-schema.py <taskfile>` and logged as passing.

## Diagram Inventory (C4-based)
- `framework-context.puml`: now includes Platform Operator persona, clarifying router governance responsibilities.
- `framework-container.puml`: highlights Platform Operator interactions with ops tooling + router config.
- `framework-component.puml`: adds DirectiveLoader and ConfigLoader components, showing how new tasks fit into the framework module.

## Recommended Next Steps
1. **Issue Generation:** Run `ops/planning/create-issues-from-definitions.sh --taskset planning --dry-run` once GitHub helper scripts accept indented `taskset` values (current grep pattern ignores indents).
2. **Work Intake:** Assign the four new inbox tasks via Agent Orchestrator; ensure Manager Mike iteration references the new Orchestration feature.
3. **Documentation Hooks:** Update `work/collaboration/inbox/INDEX.md` and `docs/metrics/README.md` once router metrics task progresses to keep indices synchronized.
