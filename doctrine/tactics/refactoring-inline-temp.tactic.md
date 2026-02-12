# Tactic: Refactoring.InlineTemp

## Intent
Inline temporary variables that only alias a simple expression to reduce indirection and improve local readability.

Use this tactic when a temp variable does not add domain meaning and is used once or in a trivial local scope.

---

## Preconditions
- A temporary variable stores a pure expression with no side effects.
- Tests cover behavior of the target code path.
- Inlining will not duplicate expensive computation in hot paths.

Do not use this tactic when:
- The temp name carries important domain meaning.
- The expression is expensive and intentionally cached.

---

## Execution Steps
1. Identify candidate temp variable assignments.
2. Verify expression purity and usage count.
3. Add or verify tests for behavior around the expression.
4. Replace temp usage with the original expression.
5. Remove temp declaration.
6. Run tests.
7. Stop.

---

## Checks / Exit Criteria
- Target temp variable is removed.
- Expression meaning remains clear at call site.
- Tests pass with unchanged behavior.

---

## Failure Modes
- Inlining expressions with side effects.
- Reducing readability by inlining complex expressions.
- Repeating expensive computations unintentionally.

---

## Outputs
- Simplified code with unnecessary temp removed.
- Passing tests confirming behavior preservation.
