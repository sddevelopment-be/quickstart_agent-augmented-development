# Domain 02: Workspace and Branch Topology

## Conceptual Focus
Terminology for git/worktree isolation, dependency handling, branch routing, and merge execution.

## Canonical Terms
- `workspace-per-WP`
- `worktree`
- `workspace context`
- `base workspace`
- `target branch`
- `dependency graph`
- `merge preflight`
- `status resolver`
- `multi-parent merge`

## Domain Semantics
- Work packages are isolated into separate workspaces/worktrees for parallelism.
- Dependency relationships drive base selection and merge ordering.
- `done` does not imply merged target branch state; merge has separate semantics and tooling.

## Evidence Anchors
- `docs/explanation/workspace-per-wp.md`
- `src/specify_cli/core/worktree.py`
- `src/specify_cli/core/dependency_graph.py`
- `src/specify_cli/merge/preflight.py`
- `src/specify_cli/merge/status_resolver.py`
- `architecture/adrs/2026-02-04-21-done-means-review-complete-not-merged.md`
