# Tactic: Refactoring.ExtractClassByResponsibilitySplit

## Intent
Split a large class with mixed concerns into focused classes aligned to single responsibilities.

Use this tactic when one class changes for multiple unrelated reasons or contains separable behavior clusters.

---

## Preconditions
- A class has multiple responsibility clusters (state + behavior) that can be isolated.
- Tests exist for externally observable behavior of the current class.
- A target extraction boundary can be named with domain intent.
- Call sites can be updated incrementally.

Do not use this tactic when:
- Responsibility boundaries are not yet understood.
- Extraction would violate architectural layer constraints.

---

## Execution Steps
1. Identify the source class and map methods/fields into responsibility clusters.
2. Choose one cluster with clear cohesion as the first extraction target.
3. Add or verify tests that protect behavior related to that cluster.
4. Create the new class with only fields and methods required for the chosen cluster.
5. Move the selected methods and supporting fields to the new class.
6. Keep the original class delegating to the new class for migrated behavior.
7. Update one caller at a time to use the new class boundary where appropriate.
8. Re-run tests after each migration step.
9. Remove obsolete members from the original class after all callers are migrated.
10. Stop.

---

## Checks / Exit Criteria
- New class has a single, explicit responsibility.
- Source class size/complexity is reduced for the extracted concern.
- Delegation or call paths preserve original behavior.
- All tests pass after migration.

---

## Failure Modes
- Splitting by file size instead of responsibility boundaries.
- Moving shared utility members that still belong to the original class.
- Introducing chatty interfaces due to poor boundary definition.
- Migrating multiple clusters simultaneously and obscuring regressions.

---

## Outputs
- New extracted class with cohesive responsibility.
- Updated source class and callers with incremental migration history.
- Passing tests validating behavior preservation.
