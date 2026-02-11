"""
Specifications Bounded Context.

This module contains domain models for feature specifications, initiatives,
portfolio management, and progress tracking.

Domain: Product planning and requirements management

Key Concepts
------------
Specification
    A formal description of a feature or capability, including requirements,
    acceptance criteria, and test scenarios.

Feature
    A discrete unit of functionality delivered to users. Features are described
    by specifications and grouped into initiatives.

Initiative
    A collection of related features that deliver a cohesive capability or
    strategic goal. Initiatives span multiple iterations.

Epic
    A large body of work that can be broken down into multiple features or
    initiatives. Represents major product themes.

Portfolio
    A high-level view of all initiatives, features, and their relationships.
    Used for strategic planning and progress tracking.

Progress
    Metrics and status tracking for features and initiatives, including
    completion percentage, health indicators, and risk assessments.

Related ADRs
------------
- ADR-046: Domain Module Refactoring

Examples
--------
>>> # Future usage after Task 2 (file migration)
>>> # from src.domain.specifications import Specification, Feature, Initiative
>>> # spec = Specification(id="SPEC-001", title="User Authentication")
>>> # feature = Feature(id="F001", specification=spec)
>>> # initiative = Initiative(id="I001", features=[feature])
"""

__all__ = []  # Will be populated in Task 2 when files are moved
