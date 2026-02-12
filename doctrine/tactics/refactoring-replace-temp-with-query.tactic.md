# Tactic: Refactoring.ReplaceTempWithQuery

## Intent
Replace temporary variables that store derived values with query methods so derived logic is explicit and reusable.

Use this tactic when local temp assignments hide intent or duplicate derivation logic across call sites.

---

## Preconditions
- One or more temporary variables store computed values (not external input).
- Behavior tests exist for code paths using the temporary value.
- The derived computation can be extracted without introducing side effects.
- Performance impact of recomputation is acceptable or mitigated.

Do not use this tactic when:
- The expression is expensive and intentionally cached in local scope.
- The expression has side effects or depends on mutation timing.

---

## Execution Steps
1. Identify target temporary variable assignments that represent derived data.
2. Add or verify tests for behavior depending on the temporary value.
3. Extract the derivation into a query method with intention-revealing name.
4. Replace temp variable usages with query method calls incrementally.
5. Run tests after each replacement group.
6. Remove obsolete temp assignments.
7. Stop.

---

## Checks / Exit Criteria
- No target derived temp assignment remains.
- Query method name reflects domain meaning.
- Tests pass with unchanged behavior.
- No unintended performance regression in hot paths.

---

## Failure Modes
- Extracting expressions with hidden side effects.
- Recomputing expensive expressions without guardrails.
- Naming query methods by implementation detail instead of intent.
- Mixing extraction with unrelated behavior changes.

---

## Outputs
- New/updated query method(s) for derived values.
- Removed target temp variable assignments.
- Passing tests demonstrating behavior preservation.
