# Tactic: Refactoring.MoveField

## Intent
Move a field to the class that uses and owns it most, aligning data placement with behavior.

Use this tactic when field access patterns show ownership drift and current placement increases coupling.

---

## Preconditions
- A field is primarily read/modified by another class.
- Tests exist for behavior touching the field.
- Target class has clear ownership semantics for the field.
- Field visibility and lifecycle can be preserved after move.

Do not use this tactic when:
- Field represents shared cross-boundary state without clear owner.
- Move would create circular dependencies or layer violations.

---

## Execution Steps
1. Identify field usage distribution across classes.
2. Confirm target class ownership rationale.
3. Add or verify tests for all affected behaviors.
4. Introduce field in target class while keeping source access via delegation/accessors.
5. Update methods to use target-owned field incrementally.
6. Run tests after each migration step.
7. Remove source field and obsolete access paths once callers are migrated.
8. Stop.

---

## Checks / Exit Criteria
- Target class owns the migrated field.
- Source class no longer stores redundant field state.
- Behavior tests remain green.
- No encapsulation or layer boundary violations introduced.

---

## Failure Modes
- Moving field without explicit ownership rationale.
- Breaking invariants tied to constructor/init order.
- Partial migrations that duplicate state in both classes.
- Migrating all usages in one batch without checkpoints.

---

## Outputs
- Field relocated to target owner class.
- Updated access/call paths.
- Passing tests confirming unchanged behavior.
