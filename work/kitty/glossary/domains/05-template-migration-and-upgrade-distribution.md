# Domain 05: Template, Migration, and Upgrade Distribution

## Conceptual Focus
Language around how templates are sourced, propagated, migrated, and versioned across projects/agents.

## Canonical Terms
- `template source`
- `command templates`
- `migration`
- `migration registry`
- `upgrade`
- `manifest`
- `packaging safety`

## Domain Semantics
- Templates are treated as canonical assets with strict source-of-truth constraints.
- Migration terms encode compatibility maintenance and version evolution.
- Upgrade terminology formalizes safe transition across project states and versions.

## Evidence Anchors
- `CLAUDE.md` template source guidance.
- `src/specify_cli/template/manager.py`
- `src/specify_cli/upgrade/registry.py`
- `src/specify_cli/upgrade/runner.py`
- `RELEASE_CHECKLIST.md`
