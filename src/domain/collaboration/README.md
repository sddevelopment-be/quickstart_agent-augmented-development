# Collaboration Domain

Multi-agent task orchestration: modeling the lifecycle, priority, and querying of tasks within an asynchronous, file-based coordination system.

## Bounded Context

The collaboration context owns the problem of **how agents discover, claim, execute, and complete units of work**. It captures the rules governing task state transitions, the priority model that drives scheduling decisions, and the query capabilities needed by orchestrators and dashboards to observe system state.

This context does not concern itself with *what* agents are or *how* governance is defined -- those belong to the doctrine context. It focuses purely on the coordination protocol.

## Key Domain Concepts

- **TaskStatus**: A state machine enumeration defining the seven lifecycle states a task can occupy. Terminal states (DONE, ERROR) accept no further transitions. The transition table is encoded directly in the enum, making invalid state changes impossible at the domain level.

- **TaskMode**: Reasoning modes that influence how an agent approaches a task (analytical, creative, meta-cognitive, programming, planning). These are hints to the agent runtime, not hard constraints.

- **TaskPriority**: A five-level priority model (CRITICAL through LOW) with a numeric ordering property for deterministic sorting. Urgency is defined as CRITICAL or HIGH.

- **TaskQueryResult**: A query result container supporting chainable filtering by status and agent. Designed for read-side queries without coupling to persistence.

- **TaskRepository**: Repository pattern abstracting file-system persistence. Provides discovery methods (find by status, agent, ID) and aggregate queries (count by status, count by agent). The repository boundary ensures that persistence mechanics do not leak into domain logic.

- **Task I/O**: Serialization and deserialization of task descriptors to and from YAML files. Includes a safe-loading variant that returns structured errors rather than raising exceptions.

- **Task Validation**: Dedicated validation rules ensuring task integrity (required fields, valid transitions, structural correctness) separated from both I/O and query concerns.

## Design Patterns Used

| Pattern | Rationale |
|---|---|
| **State Machine** (TaskStatus) | Encodes transition rules in the domain model itself, preventing invalid lifecycle changes at the type level rather than through external validation. |
| **Repository** (TaskRepository) | Decouples domain queries from file-system layout. Enables future migration to alternative persistence without changing consumers. |
| **Value Objects** (enums) | TaskStatus, TaskMode, and TaskPriority are immutable value objects. The `str` mixin enables direct YAML serialization without custom encoders. |
| **Separation of Concerns** | Schema I/O, validation, query, and type definitions live in separate modules. Each can evolve independently. |

## Dependency Rules

- **Depends on**: `common/` (path utilities only)
- **Independent of**: `doctrine/`, `specifications/`
- **Consumed by**: Framework orchestration layer, dashboard, CLI task management scripts

Cross-context communication (for example, resolving which agent profile handles a task) happens at the application layer, not within this bounded context.

## Related ADRs

- **ADR-042**: Shared Task Domain Model -- established the collaboration context boundary and task as the central aggregate
- **ADR-043**: Status Enumeration Standard -- standardized the `str, Enum` pattern across all domain status types
- **ADR-046**: Domain Module Refactoring -- defined the bounded context structure and migration from `src/common/`
- **ADR-047**: CQRS Pattern -- separated read-side query capabilities (TaskQueryResult) from write-side state transitions

## Glossary References

- [Task Lifecycle](../../../doctrine/GLOSSARY.md#task-lifecycle)
- [Orchestration](../../../doctrine/GLOSSARY.md#orchestration)
- [Bounded Context](../../../doctrine/GLOSSARY.md#bounded-context)
- [CQRS](../../../doctrine/GLOSSARY.md#cqrs)
