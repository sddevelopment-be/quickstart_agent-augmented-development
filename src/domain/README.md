# Domain Module: Bounded Context Structure

This directory contains domain models organized by bounded contexts per Domain-Driven Design (DDD) principles as defined in ADR-046.

## Purpose

The domain module provides a clear, structured organization of business concepts and domain logic. By separating code into bounded contexts, we:

- **Reduce conceptual drift**: Each context has clear boundaries and vocabulary
- **Improve maintainability**: Changes are localized to specific domains
- **Enable parallel development**: Teams can work independently on different contexts
- **Support future extraction**: Contexts can be extracted into separate packages if needed

## Bounded Contexts

### collaboration/

**Purpose**: Agent orchestration, task management, batch execution, iteration coordination

**Domain**: Multi-agent collaboration and coordination

**Key Concepts**:
- `Task`: A unit of work to be executed by an agent
- `TaskDescriptor`: Metadata describing a task (assignment, priority, dependencies)
- `TaskStatus`: State of a task in its lifecycle (assigned, in_progress, completed)
- `AgentIdentity`: Identification and profile information for agents
- `Batch`: A collection of related tasks executed together
- `Iteration`: A time-boxed period of work containing batches
- `Orchestrator`: Coordination logic for managing task execution

**Current Files** (will be moved in Task 2):
- `src/common/task_schema.py` → `src/domain/collaboration/task.py`
- Parts of `src/common/types.py` → `src/domain/collaboration/types.py`

### doctrine/

**Purpose**: Doctrine artifact representations (directives, approaches, tactics, agent profiles)

**Domain**: Framework governance and agentic doctrine management

**Key Concepts**:
- `Directive`: A documented rule or guideline governing agent behavior
- `Approach`: A strategic pattern or methodology for problem-solving
- `Tactic`: A specific technique for executing an approach
- `AgentProfile`: An agent's specialization, capabilities, and behavioral guidelines
- `StyleGuide`: Conventions for code, documentation, or communication
- `Template`: Reusable patterns for common artifacts

**Current Files** (will be moved in Task 2):
- `src/common/agent_loader.py` → `src/domain/doctrine/agent_profile.py`
- Parts of `src/common/types.py` → `src/domain/doctrine/types.py`

### specifications/

**Purpose**: Feature specifications, initiatives, portfolio management, progress tracking

**Domain**: Product planning and requirements management

**Key Concepts**:
- `Specification`: A formal description of a feature with requirements and acceptance criteria
- `Feature`: A discrete unit of functionality delivered to users
- `Initiative`: A collection of related features delivering a cohesive capability
- `Epic`: A large body of work broken down into features or initiatives
- `Portfolio`: A high-level view of all initiatives and features
- `Progress`: Metrics and status tracking for features and initiatives

**Current Files** (will be moved in Task 2):
- None yet (future dashboard work will populate this context)

### common/

**Purpose**: Truly shared utilities with NO domain semantics

**Domain**: None (generic utilities only)

**Key Concepts**:
- Generic validators (schema validation, format checking)
- Generic parsers (YAML, JSON, Markdown)
- File system utilities (reading, writing, path manipulation)
- String utilities (slugify, sanitize, format)

**Important**: This module should NOT contain domain logic. If a utility is specific to collaboration, doctrine, or specifications, it belongs in that bounded context instead.

**Current Files** (will be moved in Task 2):
- Generic utilities from `src/common/` (to be identified during refactoring)

## Import Patterns

After Task 2 (file migration) and Task 3 (import updates) are complete, imports will follow these patterns:

```python
# Collaboration domain
from src.domain.collaboration import Task, TaskStatus, AgentIdentity
from src.domain.collaboration import Batch, Iteration

# Doctrine domain
from src.domain.doctrine import AgentProfile, Directive
from src.domain.doctrine import Approach, Tactic

# Specifications domain
from src.domain.specifications import Specification, Feature, Initiative
from src.domain.specifications import Portfolio

# Common utilities
from src.domain.common import validate_yaml_schema
from src.domain.common import sanitize_filename
```

## Dependency Rules

1. **Bounded contexts should be independent**: Avoid dependencies between collaboration, doctrine, and specifications
2. **All contexts can depend on common/**: Common utilities are shared infrastructure
3. **Domain depends on framework, not vice versa**: Framework provides infrastructure, domain provides business logic
4. **Prefer composition over inheritance**: Use interfaces and protocols for cross-context communication

## Related ADRs

- **ADR-046**: Domain Module Refactoring (src/common → src/domain) - Primary decision for this structure
- **ADR-045**: Doctrine Concept Domain Model - Defines doctrine bounded context
- **ADR-042**: Shared Task Domain Model - Defines collaboration bounded context

## Migration Status

The refactoring from `src/common/` to `src/domain/` is happening in phases:

- [x] **Task 1**: Directory structure created (✅ COMPLETE)
- [ ] **Task 2**: Files moved to bounded contexts (⏳ IN PROGRESS)
- [ ] **Task 3**: Imports updated across codebase (⏳ PENDING)
- [ ] **Task 4**: Tests passing, old `src/common/` removed (⏳ PENDING)

## Contributing

When adding new domain concepts:

1. **Identify the bounded context**: Does it belong in collaboration, doctrine, specifications, or common?
2. **Check for domain semantics**: If it has business logic, it's NOT common
3. **Follow naming conventions**: Use clear, domain-specific names
4. **Add type hints**: All domain models should have comprehensive type annotations
5. **Write tests**: Unit tests in `tests/unit/domain/`, integration tests in `tests/integration/`
6. **Document**: Add docstrings explaining the concept's purpose and relationships

## Questions?

If you're unsure which bounded context a concept belongs in, ask:

- **Is it about agents coordinating work?** → `collaboration/`
- **Is it about doctrine artifacts or agent profiles?** → `doctrine/`
- **Is it about product planning or requirements?** → `specifications/`
- **Is it a generic utility with no domain knowledge?** → `common/`

When in doubt, consult ADR-046 or discuss with the architecture team.
