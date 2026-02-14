# Domain Core: Component Overview

The domain layer (`src/domain/`) implements the core business concepts of the agentic framework as independent bounded contexts following Domain-Driven Design principles (ADR-046).

## Architecture

The domain layer is organized into four modules -- three bounded contexts and one shared utility layer. Each bounded context models a distinct problem space with its own vocabulary, patterns, and invariants. Contexts are independent of each other; cross-context communication happens at the application layer through shared identifiers.

```
src/domain/
  collaboration/   Task orchestration and lifecycle management
  doctrine/        Governance artifacts as immutable domain models
  specifications/  Product planning and requirements tracking (emerging)
  common/          Shared utilities with no domain semantics
```

## Bounded Contexts

### Collaboration

**Problem space**: How agents discover, claim, execute, and complete units of work.

The collaboration context models the task lifecycle as a state machine (7 states with validated transitions), priority scheduling, and repository-based querying. The domain enforces valid state transitions at the type level -- invalid moves are impossible without explicit bypass. A Repository pattern decouples query operations from file-system persistence, and a chainable TaskQueryResult supports CQRS read-side projections.

**Key patterns**: State Machine, Repository, Value Objects, CQRS separation

**See**: [`src/domain/collaboration/README.md`](../../src/domain/collaboration/README.md) for detailed context documentation.

### Doctrine

**Problem space**: How governance artifacts (agents, directives, tactics, approaches, styleguides, templates) are structured, parsed, validated, and loaded.

The doctrine context transforms Markdown source files with YAML frontmatter into frozen, immutable domain objects. Every model tracks its source file and SHA-256 content hash for change detection and audit trails. Dedicated parsers handle the Markdown-to-object transformation, while read-only validators produce result objects for batch validation without exception-based control flow.

**Key patterns**: Immutable Domain Models, Parser Pattern, Validator Pattern, Source Traceability, Dynamic Loading

**See**: [`src/domain/doctrine/README.md`](../../src/domain/doctrine/README.md) for detailed context documentation.

### Specifications

**Problem space**: How product-level planning artifacts are structured and tracked through the development lifecycle.

This is an emerging context, currently seeded with the FeatureStatus enumeration establishing the boundary and conventions. Richer domain models (Specification, Feature, Initiative, Portfolio) are planned as dashboard and portfolio management capabilities mature. The context follows the same enum pattern (ADR-043) as collaboration to ensure consistency.

**See**: [`src/domain/specifications/README.md`](../../src/domain/specifications/README.md) for detailed context documentation.

### Common

**Problem space**: None -- this is explicitly not a bounded context.

A shared utility layer providing generic path resolution and infrastructure helpers. The critical invariant: nothing in this module encodes business rules or domain knowledge. It serves as the leaf dependency in the domain graph.

**See**: [`src/domain/common/README.md`](../../src/domain/common/README.md) for detailed documentation.

## Cross-Context Dependency Graph

```
  collaboration ──┐
  doctrine ───────┤──> common  (leaf, no domain semantics)
  specifications ─┘

  No direct dependencies between collaboration, doctrine, and specifications.
  Cross-context queries resolved at the application layer.
```

## Shared Design Principles

1. **Immutability**: Domain models use `@dataclass(frozen=True)` with `frozenset` and `tuple` for collections, preventing accidental mutation
2. **Bounded Context Independence**: No cross-context imports; shared identifiers link concepts at the application layer
3. **Repository Pattern**: Data access abstracted behind collection-like interfaces, decoupling domain logic from persistence
4. **YAML Serialization Compatibility**: All status enums use `str, Enum` mixin for seamless YAML round-tripping (ADR-043)
5. **Source Traceability**: Governance models track source file paths and SHA-256 hashes for change detection
6. **Validation as Data**: Validators return result objects rather than raising exceptions, enabling batch reporting

## Diagrams

- [C4 Container: Domain Core Layer](diagrams/domain-core-c4-container.puml) -- bounded context overview with dependencies
- [Collaboration Classes](diagrams/domain-collaboration-classes.puml) -- task lifecycle state machine, repository, query result
- [Doctrine Classes](diagrams/domain-doctrine-classes.puml) -- immutable models, parsers, validators
- [Specifications Classes](diagrams/domain-specifications-classes.puml) -- feature status lifecycle
- [Common Utilities](diagrams/domain-common-classes.puml) -- path resolution utilities

## Related ADRs

- **ADR-042**: Shared Task Domain Model
- **ADR-043**: Status Enumeration Standard
- **ADR-045**: Doctrine Concept Domain Model
- **ADR-046**: Domain Module Refactoring
- **ADR-047**: CQRS Pattern for Local Agent Control Plane

## Glossary References

- [Bounded Context](../../doctrine/GLOSSARY.md#bounded-context)
- [C4 Model](../../doctrine/GLOSSARY.md#c4-model)
- [CQRS](../../doctrine/GLOSSARY.md#cqrs)
- [Task Lifecycle](../../doctrine/GLOSSARY.md#task-lifecycle)
- [Orchestration](../../doctrine/GLOSSARY.md#orchestration)
- [Doctrine Stack](../../doctrine/GLOSSARY.md#doctrine-stack)

---

_Maintained by: Architect agents_
_Last updated: 2026-02-14_
