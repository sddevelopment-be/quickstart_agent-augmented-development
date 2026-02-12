# Refactoring Conditional Variants to Strategy/State

Purpose: Guide when conditional-heavy logic should remain local, move to Strategy, or move to State.

## Decision Guide

| Signal | Preferred Move | Target Pattern | Caution |
|---|---|---|---|
| One method has deep nested conditionals but stable flow | Guard Clauses first | none yet (local simplification) | Avoid early class proliferation |
| Branches represent interchangeable algorithms | Replace Conditional with Polymorphism | Strategy | Ensure context object does not leak all logic into strategies |
| Branches mutate lifecycle/transitions over time | Replace state-altering conditionals | State | Define legal transitions explicitly to prevent invalid state hops |
| Branches are rare edge-cases only | Keep local + clarify with extraction | none | Patternization likely over-engineering |

## Staged Sequence

1. Flatten conditionals with guard clauses.
2. Extract branch-specific logic into named methods.
3. Evaluate if variation is algorithmic (Strategy) or lifecycle-driven (State).
4. Apply pattern only when variation remains stable and recurring.

## Integration Notes

- Use this reference with `refactoring-guard-clauses-before-polymorphism.tactic.md`.
- Use `refactoring-conditional-to-strategy.tactic.md` when Strategy is selected by this guide.
- Keep Strategy/State adoption explicit in ADRs for non-trivial domains.
