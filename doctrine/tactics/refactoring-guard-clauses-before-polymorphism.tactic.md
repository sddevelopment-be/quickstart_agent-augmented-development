# Tactic: Refactoring.GuardClausesBeforePolymorphism

## Intent
Flatten nested conditional logic into ordered guard clauses before introducing polymorphism.

Use this tactic when deep branching obscures control flow and prevents safe extraction of variation points.

---

## Preconditions
- A conditional flow with nested `if/else` blocks exists in one method.
- Existing tests cover expected branches and fallback behavior.
- The branch logic represents stable business variants, not transient feature flags.
- The conditional can be reordered into explicit early-return checks without changing behavior.

Do not use this tactic when:
- Branch ordering is intentionally stateful and cannot be linearized safely.
- Branch logic is experimental and likely to be removed.

---

## Execution Steps
1. Identify the target method containing nested conditionals.
2. List every branch condition and current evaluation order.
3. Add or update tests to lock current branch behavior and precedence.
4. Convert the outermost exceptional/terminal branches into early guard returns.
5. Repeat branch-by-branch until the main execution path is linear.
6. Remove redundant `else` blocks created by early returns.
7. Re-run tests after each structural change.
8. Mark candidate variation points where branch-specific behavior can become subtype or strategy implementations.
9. Stop.

---

## Checks / Exit Criteria
- Method has no avoidable nested `if/else` pyramids.
- Guard clause order matches previously verified branch precedence.
- All branch and fallback tests pass.
- Variation points are explicit and ready for polymorphic extraction.

---

## Failure Modes
- Guard clauses reordered incorrectly, changing behavior.
- Terminal branches converted to guards without preserving side effects.
- Missing tests for fallback/default branch behavior.
- Converting all branches at once and losing isolate-and-verify control.

---

## Outputs
- Refactored method with ordered guard clauses.
- Test updates that verify branch precedence.
- Identified extraction points for follow-up polymorphism tactic.
