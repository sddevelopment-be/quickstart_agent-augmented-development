"""
Doctrine Bounded Context.

This module contains domain models for doctrine artifact representations including
directives, approaches, tactics, agent profiles, and style guides.

Domain: Framework governance and agentic doctrine management

Key Concepts
------------
Directive
    A documented rule or guideline that governs agent behavior and decision-making.
    Directives are numbered (e.g., 001, 016, 017) and referenced in agent profiles.

Approach
    A strategic pattern or methodology for solving problems within the framework.
    Approaches define high-level strategies that agents can adopt.

Tactic
    A specific technique or implementation pattern for executing an approach.
    Tactics are concrete, actionable steps within a broader approach.

AgentProfile
    A profile defining an agent's specialization, capabilities, and behavioral
    guidelines. References directives, approaches, and tactics.

StyleGuide
    Conventions for code, documentation, or communication within the framework.

Template
    Reusable patterns for common artifacts (ADRs, task descriptors, work logs).

Related ADRs
------------
- ADR-046: Domain Module Refactoring
- ADR-045: Doctrine Concept Domain Model

Examples
--------
>>> from src.domain.doctrine import Agent, Directive
>>> from pathlib import Path
>>> agent = Agent(
...     id="python-pedro",
...     name="Python Pedro",
...     specialization="Python development specialist",
...     capabilities=frozenset(["python", "tdd"]),
...     required_directives=frozenset(["017"]),
...     primers=frozenset(["TDD"]),
...     source_file=Path("doctrine/agents/python-pedro.agent.md"),
...     source_hash="abc123",
... )
>>> directive = Directive(
...     id="017",
...     number=17,
...     title="Test Driven Development",
...     category="testing",
...     scope="all-agents",
...     enforcement="mandatory",
...     description="Apply TDD",
...     rationale="Reduces bugs",
...     examples=(),
...     source_file=Path("directives/017.md"),
...     source_hash="dir123",
... )
"""

from src.domain.doctrine.models import (
    Agent,
    Approach,
    Directive,
    StyleGuide,
    Tactic,
    Template,
)

__all__ = [
    "Agent",
    "Directive",
    "Tactic",
    "Approach",
    "StyleGuide",
    "Template",
]
