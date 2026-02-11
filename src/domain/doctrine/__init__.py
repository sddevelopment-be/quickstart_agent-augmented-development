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
>>> # Future usage after Task 2 (file migration)
>>> # from src.domain.doctrine import AgentProfile, Directive
>>> # profile = AgentProfile.load("python-pedro")
>>> # directive = Directive(code="017", title="Test Driven Development")
"""

__all__ = []  # Will be populated in Task 2 when files are moved
