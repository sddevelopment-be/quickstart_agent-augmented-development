# Common Utilities

Shared infrastructure utilities with no domain semantics, providing repository-aware path resolution for all bounded contexts.

## Bounded Context

This is explicitly **not** a bounded context. It is a shared utility layer that exists to prevent duplication of generic infrastructure code across the domain contexts. The critical invariant: **nothing in this module should encode business rules or domain knowledge**.

If a utility begins to accumulate domain-specific logic (for example, understanding task states or directive categories), it has outgrown this module and should be relocated to the appropriate bounded context.

## Key Utilities

- **Path resolution**: Repository-aware path utilities that locate the repository root, work directory, and agents directory from any script location. These support the file-based coordination model without embedding knowledge of what those directories contain.

## Design Principles

- **Leaf dependency**: This module depends on nothing within `src/domain/`. All bounded contexts may depend on it, but it must never depend on them. This makes it the foundation of the dependency graph.
- **No domain logic**: Validators, parsers, and formatters belong here only if they are truly generic (for example, "is this valid YAML?" not "is this a valid task?").
- **Stability over features**: Changes to this module ripple across all contexts. Additions should be conservative and well-justified.

## Dependency Rules

- **Depends on**: Nothing within the domain layer (leaf dependency)
- **Depended on by**: `collaboration/`, `doctrine/`, `specifications/`

## Related ADRs

- **ADR-046**: Domain Module Refactoring -- defined this module's role as the shared utility layer with explicit constraints against domain logic

## Glossary References

- [Bounded Context](../../../doctrine/GLOSSARY.md#bounded-context)
