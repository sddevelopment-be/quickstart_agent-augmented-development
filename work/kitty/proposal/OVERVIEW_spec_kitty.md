# OVERVIEW: Spec Kitty

- Author: lexical
- Date: 2026-02-14

## Main Ideas
1. Spec-first workflow orchestration
- Core sequence: `spec -> plan -> tasks -> implement -> review -> accept -> merge`.

2. Mission-based adaptation
- Missions customize workflow behavior and artifacts per domain context.

3. Work-package execution model
- Work is decomposed into WPs with lane-state progression.

4. Worktree isolation
- WP-level isolation enables parallel multi-agent implementation.

5. Workflow visibility
- Dashboard + command utilities provide operational status.

## Core Terminology
- `Spec-Driven Development (SDD)`: lifecycle model where specs drive implementation phases.
- `Feature Spec`: canonical feature intent artifact in `kitty-specs/<feature>/spec.md`.
- `Plan`: implementation strategy artifact.
- `Work Package (WP)`: independently deliverable implementation slice.
- `Lane`: WP state (`planned`, `doing`, `for_review`, `done`).
- `Finalize Tasks`: operationalization/validation step before execution.
- `Mission`: domain-specific behavior profile.
- `Worktree` / `Workspace`: isolated implementation context.
- `Merge Preflight`: validation prior to merge operations.
- `Status Resolver`: logic that interprets lane/status semantics.

## Architectural Position
Spec Kitty is the primary product/workflow platform. It should remain authoritative for lifecycle, orchestration, and execution flow.
