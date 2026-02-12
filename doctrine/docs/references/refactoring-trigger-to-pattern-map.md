# Refactoring Trigger to Pattern Map

Purpose: Provide a concise mapping from recurring refactoring triggers to pattern-level targets.

## Mapping Table

| Trigger | First Refactoring Move | Pattern-Level Target | Guardrail |
|---|---|---|---|
| Nested conditional pyramid | Replace Nested Conditional with Guard Clauses | Strategy / State | Preserve branch precedence with tests before extraction |
| Type-switch branching across classes | Replace Conditional with Polymorphism | Strategy / Command | Do not introduce subtype explosion; enforce explicit variant boundary |
| Large class with mixed concerns | Extract Class by responsibility split | Facade / Adapter-friendly modules | Split by responsibility, not by line count |
| Behavior closer to foreign data | Move Method | Facade boundary shaping / ACL-friendly contracts | Use copy-delegate-remove sequence to preserve behavior |
| Repeated parameter clusters | Introduce Parameter Object | Value Object / Service input contract | Keep parameter object cohesive and immutable when possible |
| Fragile inheritance hierarchy | Replace Inheritance with Delegation | Strategy / Decorator | Avoid delegating everything blindly; preserve clear ownership |
| Legacy module replacement need | Strangler Fig | Strangler migration with ACL edge | Route incrementally; keep dual-run observability |
| Unnamed numeric policy values | Replace Magic Number with Symbolic Constant | Policy object / strategy-ready rules | Name by domain intent, not implementation details |

## Usage Sequence

1. Detect trigger in code under active change.
2. Apply the first refactoring move with behavior-preserving tests.
3. Re-evaluate complexity and coupling.
4. Escalate to pattern-level target only if repeated variation remains.

## Exclusions

- Do not force pattern adoption when one local refactoring is sufficient.
- Do not treat architecture patterns (ACL, CQRS, Strangler) as default outcomes.
