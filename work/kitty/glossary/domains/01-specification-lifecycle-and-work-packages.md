# Domain 01: Specification Lifecycle and Work Package Management

## Conceptual Focus
How Spec Kitty names and structures feature intent, planning, task decomposition, and progression through lanes.

## Canonical Terms
- `specify`
- `plan`
- `tasks`
- `work package (WPxx)`
- `lane` (`planned`, `doing`, `for_review`, `done`)
- `finalize-tasks`
- `review`
- `accept`

## Domain Semantics
- The lifecycle terms encode a strict command sequence from intent to delivery.
- `work package` is the primary delivery atom and is expected to be independently testable/deliverable.
- `lane` represents workflow state, not branch integration state.

## Evidence Anchors
- `README.md` workflow command sections.
- `spec-driven.md` command explanations.
- `docs/tutorials/your-first-feature.md` lifecycle walkthrough.
- `src/specify_cli/templates/tasks-template.md` WP and lane conventions.
