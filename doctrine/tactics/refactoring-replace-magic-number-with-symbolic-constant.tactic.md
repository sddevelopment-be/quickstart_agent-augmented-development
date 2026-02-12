# Tactic: Refactoring.ReplaceMagicNumberWithSymbolicConstant

## Intent
Replace unexplained numeric literals with named constants to improve readability and change safety.

Use this tactic when numeric values encode business policy, thresholds, limits, or protocol semantics.

---

## Preconditions
- At least one numeric literal lacks clear semantic meaning in context.
- Tests exist for behavior that depends on the literal value.
- A stable domain-oriented name can be assigned to the value.
- Constant placement (module/class scope) is clear.

Do not use this tactic when:
- Literal is language-conventional and self-evident (`0`, `1` in trivial index/math contexts).
- Value is intentionally dynamic and should come from configuration.

---

## Execution Steps
1. Locate target magic numbers and group duplicates by meaning.
2. Add or verify tests covering behavior tied to each target value.
3. Define one named constant per distinct meaning in the correct scope.
4. Replace literal usages with the named constant incrementally.
5. Re-run tests after each replacement batch.
6. Consolidate duplicate constants that represent the same meaning.
7. Remove obsolete literals and dead code paths.
8. Stop.

---

## Checks / Exit Criteria
- No unexplained numeric literals remain in the targeted scope.
- Constant names communicate domain intent.
- Duplicated values with same meaning use one shared constant.
- Tests pass with no behavior changes.

---

## Failure Modes
- Creating constants with vague names that hide meaning.
- Over-abstracting trivial literals and reducing readability.
- Replacing values across unrelated contexts that need different semantics.
- Mixing constant extraction with behavior changes.

---

## Outputs
- Named constants for previously magic numeric literals.
- Updated code paths using semantic constants.
- Passing tests verifying unchanged behavior.
