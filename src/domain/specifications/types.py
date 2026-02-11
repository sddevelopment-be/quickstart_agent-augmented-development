"""
Feature/specification type definitions for specifications domain.

This module provides feature-related status enumerations
used in product planning and specification tracking.

Related ADRs:
- ADR-043: Status Enumeration Standard
- ADR-046: Domain Module Refactoring
"""

from enum import Enum


class FeatureStatus(str, Enum):
    """
    Feature/specification implementation states.

    Features flow through these states during development:
    DRAFT → PLANNED → IN_PROGRESS → IMPLEMENTED → {DEPRECATED}

    Inherits from str to maintain YAML serialization compatibility.
    """

    DRAFT = "draft"  # Specification in draft, not approved
    PLANNED = "planned"  # Approved, implementation planned
    IN_PROGRESS = "in_progress"  # Implementation ongoing
    IMPLEMENTED = "implemented"  # Complete and deployed
    DEPRECATED = "deprecated"  # No longer relevant

    @classmethod
    def is_active(cls, status: "FeatureStatus") -> bool:
        """Check if feature is actively being worked on."""
        return status in {cls.PLANNED, cls.IN_PROGRESS}

    @classmethod
    def is_complete(cls, status: "FeatureStatus") -> bool:
        """Check if feature implementation is complete."""
        return status == cls.IMPLEMENTED
