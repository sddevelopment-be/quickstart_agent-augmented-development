"""
Domain Module: Bounded Context Structure.

This package contains domain models organized by bounded contexts following
Domain-Driven Design (DDD) principles as defined in ADR-046.

Bounded Contexts
----------------
collaboration/
    Agent orchestration, task management, batch execution, iteration coordination.
    Domain: Multi-agent coordination
    Key Concepts: Task, Agent, Batch, Iteration

doctrine/
    Doctrine artifact representations (directives, approaches, tactics, agent profiles).
    Domain: Framework governance
    Key Concepts: Directive, Approach, Tactic, AgentProfile

specifications/
    Feature specifications, initiatives, portfolio management, progress tracking.
    Domain: Product planning
    Key Concepts: Specification, Feature, Initiative, Portfolio

common/
    Truly shared utilities with NO domain semantics (validation, parsing, filesystem).
    Domain: None (generic utilities)
    Key Concepts: Validators, Parsers, File utilities

Related ADRs
------------
- ADR-046: Domain Module Refactoring (src/common → src/domain)
- ADR-045: Doctrine Concept Domain Model
- ADR-042: Shared Task Domain Model

Migration Status
----------------
✅ Directory structure created (Task 1)
⏳ Files moved to bounded contexts (Task 2)
⏳ Imports updated (Task 3)
⏳ Tests passing, old src/common/ removed (Task 4)
"""

__version__ = "0.1.0"
__all__ = [
    "collaboration",
    "doctrine",
    "specifications",
    "common",
]
