# Doctrine Domain

Represents the five-layer governance framework as immutable domain models: agents, directives, tactics, approaches, styleguides, and templates.

## Bounded Context

The doctrine context owns the problem of **how governance artifacts are structured, parsed, validated, and loaded into the runtime**. The framework's governance stack -- agents with capabilities, directives they must follow, tactics they execute, approaches they adopt -- is defined in Markdown files with YAML frontmatter. This context transforms those source artifacts into type-safe, immutable domain objects that the rest of the system can reason about.

This context does not manage task execution or coordination (that belongs to collaboration). It defines *what agents are* and *what rules they follow*, not *how they coordinate work*.

## Key Domain Concepts

- **Agent** (aggregate root): The central domain object representing an AI agent profile. Captures identity, specialization, capabilities, required directives, and execution primers. Supports a specialization hierarchy (DDR-011) where agents can inherit from more general profiles. Enhanced with handoff patterns and primer matrices (ADR-045) for inter-agent collaboration descriptions.

- **Directive**: A mandatory framework rule or policy governing agent behavior. Each directive has a category, scope, enforcement level, and rationale explaining *why* the rule exists.

- **Tactic**: A specific procedural guide or execution pattern (for example, the RED-GREEN-REFACTOR cycle). Defined as an ordered sequence of steps with prerequisites and expected outcomes.

- **Approach**: A recommended technique or mental model for problem-solving. Includes explicit guidance on when to use it and when to avoid it, linked to related directives.

- **StyleGuide**: Coding or documentation standards with enumerated rules and enforcement levels.

- **Template**: Reusable structural patterns for common artifacts (ADRs, task descriptors, specifications), defining required and optional sections.

- **HandoffPattern** (value object): Describes collaboration patterns between agents -- who hands off to whom, in which direction, and for what purpose. Composed into Agent.

- **PrimerEntry** (value object): Maps task types to required execution primers, describing the workflow sequence an agent should follow. Composed into Agent.

## Design Patterns Used

| Pattern | Rationale |
|---|---|
| **Immutable Domain Models** | All dataclasses use `frozen=True` with `frozenset` and `tuple` for collections. Prevents accidental mutation and makes models safe for concurrent access and caching. |
| **Parser Pattern** | Dedicated parsers (DirectiveParser, AgentParser, TacticParser, ApproachParser) transform Markdown with YAML frontmatter into domain objects. Parsing logic is isolated from the models themselves. |
| **Validator Pattern** | Read-only validators (CrossReferenceValidator, MetadataValidator, IntegrityChecker) produce ValidationResult objects rather than raising exceptions, enabling batch validation and reporting. |
| **Source Traceability** | Every model tracks its source file path and SHA-256 content hash. This enables change detection, cache invalidation, and audit trails back to the governance source documents. |
| **Dynamic Loading** | AgentProfileLoader discovers and loads agent profiles from the `doctrine/agents/` directory at runtime, supporting extensibility without code changes. |

## Dependency Rules

- **Depends on**: `common/` (path utilities only)
- **Independent of**: `collaboration/`, `specifications/`
- **Consumed by**: Framework governance layer, agent initialization, validation tooling, dashboard

The doctrine context is a *read-model* over the governance source files. It does not write back to those files or manage their lifecycle.

## Related ADRs

- **ADR-045**: Doctrine Concept Domain Model -- defined the immutable model structure, value objects, and enhanced agent features
- **ADR-046**: Domain Module Refactoring -- established the bounded context boundary and migration path

## Glossary References

- [Agent](../../../doctrine/GLOSSARY.md#agent)
- [Directive](../../../doctrine/GLOSSARY.md#directive)
- [Tactic](../../../doctrine/GLOSSARY.md#tactic)
- [Approach](../../../doctrine/GLOSSARY.md#approach)
- [Template](../../../doctrine/GLOSSARY.md#template)
- [StyleGuide](../../../doctrine/GLOSSARY.md#styleguide)
- [Doctrine Stack](../../../doctrine/GLOSSARY.md#doctrine-stack)
