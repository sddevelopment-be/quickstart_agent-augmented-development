# Evaluation: Doctrine Governance Extension for Spec Kitty

**Date:** 2026-02-14
**Basis:** `work/kitty/2026-02-14-doctrine-spec-kitty-integration-analysis.md`, `work/kitty/2026-02-14-control-plane-spec-kitty-coverage.md`, `work/kitty/spec-kitty-vs-quickstart-terminology-comparison.md`, `work/kitty/glossary/*`

## Decision
Your idea is **viable and strategically strong**, with one constraint:
- **Yes** to extending Spec Kitty governance with Doctrine + local doctrine overrides from this repository.
- **Yes** to building orchestration concerns as Spec Kitty extensions/features.
- **Conditional yes** to task-to-model routing inside Spec Kitty: do it via a **pluggable routing provider** boundary, not hard-wired into core workflow logic.

## Why This Fits
1. The analyses consistently show complementarity:
- Spec Kitty: workflow/lifecycle orchestration (what/when).
- Doctrine: behavioral governance and policy stack (how/constraints).

2. Existing recommendation already points to this direction:
- Option C (external Doctrine dependency) is the preferred integration path in `2026-02-14-doctrine-spec-kitty-integration-analysis.md`.

3. Terminology/domain mapping confirms alignment potential:
- Strong conceptual overlap in governance, validation, and multi-agent coordination.
- Differences are mostly surface vocabulary and control-plane abstraction levels.

## Main Risk If Implemented Naively
If routing/orchestration/governance are all implemented directly in core Spec Kitty, you create a brittle “two-masters” model:
- Constitution/mission rules vs doctrine guidelines/directives.
- WP lane lifecycle vs doctrine collaboration workflow semantics.
- Agent key config vs rich doctrine profile capabilities.

## Recommended Shape (Pragmatic)
1. **Governance Extension (Phase 1)**
- Mount Doctrine as optional external dependency (git subtree or sync) at `doctrine/`.
- Mount local overrides from this repository style at `.doctrine-config/`.
- Add explicit precedence contract in generated constitution:
  - Constitution -> Doctrine Guidelines -> Doctrine Directives -> Mission guidance -> Tactics/Templates.

2. **Adapter Layer (Phase 2)**
- Add term/lifecycle crosswalk adapter:
  - SK `lane` lifecycle <-> doctrine task-state vocabulary.
  - SK mission context <-> doctrine approach/directive loading hints.

3. **Routing Extension (Phase 3)**
- Introduce `RoutingProvider` interface in Spec Kitty extension surface:
  - `route_task(task_context) -> model/tool/agent profile decision`.
- First provider can load policies from doctrine (`.doctrine-config/model_router.yaml` style) without forcing it into SK core.

4. **Orchestration Extension (Phase 4)**
- Keep WP/worktree as primary execution model.
- Emit structured events from workflow transitions and let extension consume for policy checks/telemetry.

## What To Avoid
- Do not merge doctrine collaboration file schema directly into Spec Kitty WP lane files.
- Do not make Doctrine mandatory for all Spec Kitty users.
- Do not embed model-vendor specifics into SK core commands.

## Confidence
- **High** for governance-layer extension with Doctrine + overrides.
- **High** for orchestration extensions in Spec Kitty.
- **Medium** for “entirely inside Spec Kitty” model routing unless you enforce plugin/provider boundaries from day one.

## Recommended Next Step
Create a small design spec for a `governance-doctrine` extension package with:
- extension entrypoints,
- config precedence contract,
- routing provider interface,
- migration/rollback strategy.
