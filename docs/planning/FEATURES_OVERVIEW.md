---
packaged: false
audiences: [process_architect, agentic-framework-core-team]
note: High-level feature framing for Planning Petra.
---

# High-Level Feature Overview — 2025-12-01

The latest ADRs (ADR-019 through ADR-021) expand runtime responsibilities across distribution, routing, and trunk discipline. The open tasks inside `work/collaboration/` signal where the plan still lacks feature coverage. Themes and features below translate those signals into actionable planning anchors.

## Open Task Themes

| Theme | Description | Linked Tasks |
| --- | --- | --- |
| Toolchain Governance & Lifecycle | Align preinstalled tooling upgrades, documentation, and telemetry so the Copilot setup remains reliable and observable. | `work/collaboration/assigned/manager/2025-11-24T0955-manager-tooling-enhancements-coordination.yaml`, `work/collaboration/assigned/architect/2025-11-24T0950-architect-version-policy-documentation.yaml`, `work/collaboration/assigned/build-automation/2025-11-24T0949-build-automation-security-checksum-verification.yaml`, `work/collaboration/assigned/build-automation/2025-11-24T0953-build-automation-parallel-installation.yaml`, `work/collaboration/assigned/build-automation/2025-11-24T0954-build-automation-telemetry-collection.yaml`, `work/collaboration/assigned/curator/2025-11-24T0951-curator-tooling-best-practices-guide.yaml`, `work/collaboration/assigned/curator/2025-11-24T0952-curator-maintenance-checklist-templates.yaml`. |
| Collaboration Infrastructure Hardening | Finish the script reorganization follow-through, add manifest upkeep, and automate lifecycle hygiene for collaboration work items. | `work/collaboration/inbox/2025-11-25T1837-curator-validate-refactor.yaml`, `work/collaboration/inbox/2025-11-25T1838-writer-editor-update-docs.yaml`, `work/collaboration/inbox/2025-11-25T1839-build-automation-test-workflows.yaml`, `work/collaboration/inbox/2025-11-28T0426-build-automation-manifest-maintenance-script.yaml`, `work/collaboration/inbox/2025-11-28T0427-build-automation-work-items-cleanup-script.yaml`. |
| Insight & Reporting Clarity | Maintain actionable narratives and efficiency guardrails coming out of POC3 and the efficiency ADRs. | `work/collaboration/inbox/2025-11-27T1956-writer-editor-followup-2025-11-24T1756-synthesizer-poc3-followup.yaml`, `work/collaboration/assigned/architect/2025-11-24T1736-architect-framework-efficiency-assessment.yaml`. |
| Multi-Tier Platform Enablement | Execute the Platform Next Steps plan so router configs, orchestrator interfaces, local workers, diagrams, and CI guards exist for the new four-tier runtime. | `work/collaboration/inbox/2025-11-30T1201-build-automation-model-router-config.yaml`, `work/collaboration/inbox/2025-11-30T1202-architect-model-client-interface.yaml`, `work/collaboration/inbox/2025-11-30T1203-scribe-model-selection-template.yaml`, `work/collaboration/inbox/2025-11-30T1204-build-automation-ollama-worker-pipeline.yaml`, `work/collaboration/inbox/2025-11-30T1205-diagrammer-multi-tier-runtime-diagram.yaml`, `work/collaboration/inbox/2025-11-30T1206-build-automation-ci-router-schema-validation.yaml`, `work/collaboration/inbox/2025-12-01T0510-backend-dev-framework-config-loader.yaml`, `work/collaboration/inbox/2025-12-01T0511-backend-dev-agent-profile-parser.yaml`, `work/collaboration/inbox/2025-12-01T0512-build-automation-router-metrics-dashboard.yaml`, `work/collaboration/inbox/2025-12-01T0513-build-automation-framework-ci-tests.yaml`. |
| Orchestration Iteration Enablement | Provide GitHub issue structures and supporting documentation so Manager Mike and companion agents can spin up orchestration cycles with consistent metadata. | `work/collaboration/inbox/2025-11-23T2134-curator-add-github-issue-type-for-orch-task.yml`. |

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
