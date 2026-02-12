# Refactoring Techniques Evidence Matrix (First-Wave)

Date: 2026-02-12  
Owner: researcher-ralph  
Initiative: SPEC-REFACTOR-001

## Scope and Selection Method

This matrix prioritizes techniques from the source set in `work/tasks/learning_refactoring_plan.md` using four criteria:

1. Frequency in real maintenance work
2. Low-to-moderate execution risk for agents
3. Strong fit with doctrine tactic structure (deterministic steps + exit criteria)
4. Clear pathway from low-level refactor to pattern-level target

## First-Wave Recommendations

| Technique | Problem Signal | When to Apply | Risk / Failure Mode | Pattern Trajectory | Priority |
|---|---|---|---|---|---|
| Extract Variable | Complex, opaque expressions | Improve readability before deeper extraction | Over-extraction can add noise; can alter short-circuit behavior if misapplied | Enables Compose Method / clearer guard logic | P1 |
| Move Method | Feature envy / behavior in wrong class | Improve cohesion and reduce coupling | Breaks callers if not migrated atomically | Supports Facade and ACL boundary shaping | P1 |
| Extract Class | Large class with mixed responsibilities | Split responsibilities along domain boundaries | Wrong cut increases chatty interfaces | Supports Facade/Adapter and bounded contexts | P1 |
| Replace Magic Number with Symbolic Constant | Unlabeled literals in business logic | Improve semantic clarity and change safety | Poor naming can still hide intent | Enables policy-driven Strategy/State rules | P1 |
| Replace Nested Conditional with Guard Clauses | Deep if/else pyramids | Flatten flow and clarify exceptional paths | Guard order mistakes can change behavior | Pre-step for Replace Conditional with Polymorphism | P1 |
| Replace Conditional with Polymorphism | Type/branch logic spread over conditionals | Encapsulate variant behavior | Wrong polymorphic boundaries create class explosion | Strategy/State/Command transition | P1 |
| Introduce Parameter Object | Repeated parameter groups | Reduce parameter coupling and make intent explicit | Bloated parameter object if not cohesive | Encapsulation and eventual domain value objects | P2 |
| Replace Inheritance with Delegation | Fragile hierarchies / refused bequest | Prefer composition over inheritance for variation | Excess indirection if boundaries unclear | Strategy/Decorator/Facade-friendly composition | P2 |
| Form Template Method (catalog) | Algorithm shape duplicated across variants | Standardize skeleton with controlled overrides | Over-rigid skeleton can limit extension | Template Method target state | P2 |
| Replace Conditional Logic with Strategy (catalog) | Runtime algorithm switching via conditionals | Isolate interchangeable algorithms | Mis-scoped strategy interface | Strategy target state | P2 |
| Introduce Null Object (catalog) | Repeated null checks with alternate behavior | Remove null-branch clutter in client code | Incorrect null behavior can hide failures | Null Object pattern target | P2 |
| Strangler Fig (architecture pattern) | Incremental migration from legacy modules | Phase replacement with facade/proxy routing | Facade can become bottleneck/SPoF | Strangler + ACL modernization path | P3 |

## Source-Backed Notes

- Refactoring.Guru defines refactoring as stepwise improvement without changing external behavior and emphasizes test runs after each change; this supports low-blast-radius tactic design.
- Extract Variable is a high-safety readability move and a frequent precursor to Extract Method/Compose Method style refactors.
- Move Method / Extract Class are core cohesion refactors and strong candidates for doctrine tactics due to deterministic preconditions and clear structural outcomes.
- Replace Nested Conditional with Guard Clauses is a practical bridge toward polymorphic dispatch where branch complexity currently blocks extraction.
- Replace Conditional with Polymorphism and Replace Inheritance with Delegation align with composition-oriented design and reduce brittle branching hierarchies.
- Industrial Logic’s Refactoring-to-Patterns framing supports sequencing low-level refactors toward pattern targets instead of early pattern injection.
- Azure ACL and Strangler Fig patterns provide migration-safe trajectories for larger boundary-level refactors.
- Fowler CQRS guidance is useful as a selective architecture pattern, not a default refactor destination.

## Candidate Tactic Backlog (for Curator)

1. `refactoring-guard-clauses-before-polymorphism.tactic.md`
2. `refactoring-move-method-to-boundary.tactic.md`
3. `refactoring-extract-class-by-responsibility-split.tactic.md`
4. `refactoring-parameter-object-for-call-cohesion.tactic.md`
5. `refactoring-inheritance-to-delegation.tactic.md`
6. `refactoring-conditional-to-strategy.tactic.md`

## Recommended Next Step

Proceed with Curator task `0911` and begin with P1 techniques only. Keep P2/P3 as explicitly staged follow-ups after validation of initial tactic quality and directive integration.

## Sources

- https://refactoring.guru/refactoring
- https://refactoring.guru/extract-variable
- https://refactoring.guru/move-method
- https://refactoring.guru/extract-class
- https://refactoring.guru/replace-nested-conditional-with-guard-clauses
- https://refactoring.guru/replace-conditional-with-polymorphism
- https://refactoring.guru/introduce-parameter-object
- https://refactoring.guru/replace-inheritance-with-delegation
- https://refactoring.guru/design-patterns/strategy
- https://refactoring.guru/design-patterns/facade
- https://www.industriallogic.com/refactoring-to-patterns/
- https://www.industriallogic.com/refactoring-to-patterns/catalog/
- https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
- https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig
- https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs
- https://martinfowler.com/bliki/CQRS.html
