# Tactic: Refactoring.IntroduceNullObject

## Intent
Replace repetitive null-check branching with a dedicated null-object implementation that preserves the same interface.

Use this tactic when default do-nothing or fallback behavior is legitimate and repeated null handling obscures flow.

---

## Preconditions
- Repeated null checks exist for one role/interface.
- A safe default behavior can be explicitly defined.
- Tests cover both null and non-null behavior paths.
- The null-object can implement the same public contract.

Do not use this tactic when:
- Null currently signals an exceptional condition that must fail fast.
- Default behavior would hide errors that should be surfaced.

---

## Execution Steps
1. Identify repeated null-check pattern for the same collaborator role.
2. Define the collaborator interface/contract used by both real and null implementations.
3. Add or verify tests for current null and non-null outcomes.
4. Implement a null-object class with explicit safe default behavior.
5. Replace null-injection points with null-object provisioning.
6. Remove redundant null checks incrementally from callers.
7. Run tests after each caller migration.
8. Stop.

---

## Checks / Exit Criteria
- Target callers no longer contain redundant null checks.
- Null-object behavior matches previously validated null semantics.
- Real-object behavior remains unchanged.
- Tests pass for both null-object and real-object paths.

---

## Failure Modes
- Using null-object where absence should throw/alert.
- Creating silent behavior masking genuine data integrity issues.
- Divergence between interface contract and null-object implementation.
- Mixing null-object introduction with unrelated refactors.

---

## Outputs
- New null-object implementation.
- Updated call sites using interface-based polymorphism.
- Passing tests for null and non-null execution paths.
