# Tactic: Refactoring.ConditionalToStrategy

## Intent
Replace algorithm-selection conditionals with Strategy implementations behind a stable interface.

Use this tactic when branch logic repeatedly selects between interchangeable algorithms.

---

## Preconditions
- Conditional branches represent stable algorithm variants.
- Tests exist for each branch and fallback behavior.
- A strategy interface can be defined with clear context boundaries.

Do not use this tactic when:
- Variation is incidental and unlikely to recur.
- Branches represent lifecycle state transitions (use State-oriented guidance instead).

---

## Execution Steps
1. Identify the conditional selecting algorithm variants.
2. Add or verify tests for each branch outcome.
3. Define strategy interface for the algorithm contract.
4. Implement one strategy per branch variant.
5. Introduce strategy selection mechanism in context (factory/mapping/injection).
6. Replace conditional execution path with strategy dispatch.
7. Run tests after each migration step.
8. Remove obsolete branch conditional.
9. Stop.

---

## Checks / Exit Criteria
- Algorithm selection no longer relies on large branch conditionals.
- Strategy implementations cover previously tested variants.
- Context object keeps orchestration responsibility only.
- Tests pass with unchanged behavior.

---

## Failure Modes
- Over-engineering simple two-branch logic with unnecessary abstractions.
- Leaking context internals into strategy implementations.
- Incomplete branch migration causing mixed old/new paths.

---

## Outputs
- Strategy interface and concrete implementations.
- Refactored context dispatch logic.
- Passing tests for all migrated variants.
