---
packaged: false
audiences: [manager-mike, coordinator]
note: Kick-off instructions for Distribution & Release enablement batch.
---

# Iteration Prompt — Distribution & Release Enablement

Use `.github/ISSUE_TEMPLATE/run-iteration.md` to open an iteration titled
`[Iteration] Run orchestration cycle - 2025-12-05`. Configure:

```yaml
max_tasks: 3
agent_focus: build-automation,architect,writer-editor
priority_threshold: high
mode: /analysis-mode
```

## Targets

Process the newly queued tasks:

1. `work/collaboration/inbox/2025-12-05T1010-build-automation-release-packaging-pipeline.yaml`
2. `work/collaboration/inbox/2025-12-05T1012-build-automation-install-upgrade-scripts.yaml`
3. `work/collaboration/inbox/2025-12-05T1014-architect-framework-guardian-agent-definition.yaml`
4. `work/collaboration/inbox/2025-12-05T1016-writer-editor-release-documentation-checklist.yaml`

## Execution Notes

- Initialize as Manager Mike, read `work/collaboration/AGENT_STATUS.md`, and
  verify the orchestration framework health before delegating.
- Ensure packaging pipeline work completes before install/upgrade or Guardian items move to `in_progress`.
- Require Directive 014 work logs per agent and capture Guardian template drafts as artefacts.
- Update iteration summary with release readiness metrics (artefact checksum status, Guardian template availability).

## Success Definition

- Packaging pipeline and install/upgrade scripts have active owners and updated statuses.
- Framework Guardian profile + templates drafted or linked for review.
- Release documentation outline established with dependencies tracked.
- `AGENT_STATUS.md` and orchestration metrics reflect Distribution & Release focus.
