# Refactoring First-Wave Selection Reference

Purpose: Define first-wave refactoring choices for doctrine tactics with staged expansion.

## First-Wave (P1) Techniques

1. Replace Nested Conditional with Guard Clauses
2. Replace Magic Number with Symbolic Constant
3. Extract Class by Responsibility Split
4. Move Method (existing tactic)

Rationale:
- High frequency in maintenance work.
- Low-to-moderate execution risk with test-first workflow.
- Clear tactical preconditions and deterministic exit criteria.

## Staged Follow-Up (P2/P3)

- Replace Conditional with Polymorphism
- Introduce Parameter Object
- Replace Inheritance with Delegation
- Strangler Fig (architecture-level modernization)

Apply only after first-wave tactics demonstrate stable adoption and review quality.

## Doctrine Integration Rules

- Tactics must remain procedural (no policy duplication).
- Directive 039 selects when to apply; tactics specify how.
- Reference files in `doctrine/docs/references/` are supporting material and not execution mandates.
- Cross-directory dependencies are disallowed; keep links doctrine-local.
