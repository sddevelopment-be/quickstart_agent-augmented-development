# Refactoring Reference Expansion (Batch 2)

Date: 2026-02-12  
Owner: researcher-ralph  
Initiative: SPEC-REFACTOR-001 (Batch 2)

## Objective

Capture remaining high-value reference material from `work/tasks/learning_refactoring_plan.md` that was not fully operationalized in Batch 1, and propose doctrine-ready follow-up outputs.

## Source Coverage (This Batch)

### Refactoring.Guru (technique families)
- Composing Methods: Inline Temp, Replace Temp with Query
- Moving Features: Move Field
- Simplifying Conditional Expressions: Introduce Null Object
- Dealing with Generalization: Pull Up Field, Push Down Field
- Catalog taxonomy page (technique family map)

### Industrial Logic (Refactoring to Patterns)
- Compose Method
- Replace Conditional Logic with Strategy
- Replace State-Altering Conditionals with State
- Catalog and overview framing

### Microsoft Azure Architecture Patterns
- Anti-Corruption Layer (ACL)
- Backends for Frontends (BFF)
- Pipes and Filters
- Event Sourcing
- Retry
- Asynchronous Request-Reply

### Martin Fowler
- CQRS bliki
- Event-driven architecture clarification
- Focusing on Events narrative

## Evidence Matrix (Remaining/Expanded Topics)

| Topic | Problem Signal | Apply When | Risks / Failure Modes | Doctrine Output Type |
|---|---|---|---|---|
| Inline Temp | Excess temp vars hide simple expressions | Temp variable only aliases trivial expression | Removes intentional cache of expensive computation | tactic (micro) |
| Replace Temp with Query | Expression logic duplicated via local temp storage | Same derived expression appears in method(s) | Repeated call overhead if expression is expensive/impure | tactic |
| Move Field | Field is used mostly by another class | Data ownership and behavior are misaligned | Circular deps, encapsulation leaks | tactic |
| Introduce Null Object | Repeated null-branch checks clutter flow | Default behavior exists and can be modeled polymorphically | Class proliferation, hidden error semantics | tactic |
| Pull Up / Push Down Field | Hierarchy field placement drift | Field semantics are shared or subclass-specific | Premature hierarchy reshaping | reference (decision guide) |
| Compose Method (pattern-directed) | Method intent unclear due to mixed abstraction levels | Need intention-revealing sequence before larger extraction | Cosmetic rewrite without structural gain | reference + tactic linkage |
| Replace Conditional Logic with Strategy | Conditional chooses algorithm variants | Stable algorithm family exists | Over-engineering and context-data leakage into strategies | tactic + reference |
| Replace State-Altering Conditionals with State | Transition rules embedded in branching logic | State model is explicit and persistent enough | State-class explosion, transition bugs | reference (staged) |
| Anti-Corruption Layer | Legacy semantics contaminating new domain | Staged migration/integration across semantic boundary | Added latency and maintenance overhead | reference |
| BFF | One backend overfit to multiple client UIs | Distinct client channels need tailored contracts | Service sprawl and ownership fragmentation | reference |
| Pipes and Filters | Monolithic processing pipeline hard to evolve | Sequential transform stages can be modularized | Idempotency/duplicate-message issues | reference |
| Event Sourcing | Need auditability/replay and high write scalability | Domain history and replay are first-class concerns | System-wide complexity lock-in | reference (high caution) |
| Retry | Transient failures from remote dependencies | Faults are short-lived and retry-safe | Retry storms, masking non-transient failures | tactic (cross-cutting) |
| Async Request-Reply | Long-running backend work behind HTTP interface | Caller needs immediate ack + later status | Polling abuse, weak status semantics | reference |
| CQRS | Read/write model tension in complex bounded context | Domain complexity or read/write scale asymmetry justifies split | High accidental complexity if over-applied | reference (bounded-context guidance) |
| Event-Driven styles (Fowler) | “Event-driven” used ambiguously | Need explicit choice of event notification vs state transfer vs event sourcing | Hidden flow coupling and debugging opacity | reference |

## Proposed Batch 2 Deliverables for Claire

### New Tactics (Recommended)
1. `doctrine/tactics/refactoring-replace-temp-with-query.tactic.md`
2. `doctrine/tactics/refactoring-move-field.tactic.md`
3. `doctrine/tactics/refactoring-introduce-null-object.tactic.md`

### New Doctrine References (Recommended)
1. `doctrine/docs/references/refactoring-hierarchy-field-placement-guide.md`
2. `doctrine/docs/references/refactoring-conditional-variants-to-strategy-state.md`
3. `doctrine/docs/references/refactoring-architecture-pattern-escalation-guide.md`

## Integration Guidance

- Keep architecture patterns (ACL, BFF, Event Sourcing, CQRS) as reference-level escalation guidance, not default tactic outcomes.
- Prefer adding tactics only where execution steps are deterministic and behavior-preservation checks are clear.
- Stage State-pattern and Event-Sourcing-oriented material behind explicit complexity thresholds.

## Sources

- https://refactoring.guru/refactoring/techniques
- https://refactoring.guru/inline-temp
- https://refactoring.guru/replace-temp-with-query
- https://refactoring.guru/move-field
- https://refactoring.guru/introduce-null-object
- https://refactoring.guru/pull-up-field
- https://refactoring.guru/push-down-field
- https://www.industriallogic.com/refactoring-to-patterns/
- https://www.industriallogic.com/refactoring-to-patterns/catalog/
- https://www.industriallogic.com/refactoring-to-patterns/catalog/composeMethod
- https://www.industriallogic.com/refactoring-to-patterns/catalog/conditionalWithStrategy
- https://www.industriallogic.com/refactoring-to-patterns/catalog/alteringConditionalsWithState
- https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer
- https://learn.microsoft.com/en-us/azure/architecture/patterns/backends-for-frontends
- https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters
- https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
- https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply
- https://martinfowler.com/bliki/CQRS.html
- https://martinfowler.com/articles/201701-event-driven.html
- https://martinfowler.com/eaaDev/EventNarrative.html
