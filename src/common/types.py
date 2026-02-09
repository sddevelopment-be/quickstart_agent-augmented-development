"""
Shared type definitions for the agent-augmented development framework.

This module provides type-safe enumerations and type aliases used
across framework orchestration and dashboard modules.

Related ADRs:
- ADR-043: Status Enumeration Standard
- ADR-044: Agent Identity Type Safety
"""

from enum import Enum
from typing import TYPE_CHECKING, Literal, get_args

# Import agent loader for dynamic agent identity loading
if not TYPE_CHECKING:
    try:
        from .agent_loader import load_agent_identities
    except ImportError:
        # Fallback if agent_loader not available
        def load_agent_identities():
            return []


class TaskStatus(str, Enum):
    """
    Task lifecycle states.

    Tasks flow through these states during execution:
    NEW → INBOX → ASSIGNED → IN_PROGRESS → {DONE | ERROR | BLOCKED}

    Inherits from str to maintain YAML serialization compatibility.
    """

    # Lifecycle states
    NEW = "new"  # Task created, awaiting assignment
    INBOX = "inbox"  # Task in inbox, awaiting agent pickup
    ASSIGNED = "assigned"  # Task assigned to specific agent
    IN_PROGRESS = "in_progress"  # Agent actively executing task
    BLOCKED = "blocked"  # Task blocked on dependency/blocker
    DONE = "done"  # Task successfully completed
    ERROR = "error"  # Task failed with error

    @classmethod
    def is_terminal(cls, status: "TaskStatus") -> bool:
        """Check if status represents a terminal state."""
        return status in {cls.DONE, cls.ERROR}

    @classmethod
    def is_active(cls, status: "TaskStatus") -> bool:
        """Check if status represents an active (non-terminal) state."""
        return status in {cls.ASSIGNED, cls.IN_PROGRESS, cls.BLOCKED}

    @classmethod
    def is_pending(cls, status: "TaskStatus") -> bool:
        """Check if status represents a pending (not yet started) state."""
        return status in {cls.NEW, cls.INBOX}


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


# Agent Identity Type (Literal for type checking)
# NOTE: For static type checking, we keep a baseline Literal type.
# At runtime, validation uses dynamically loaded agents from doctrine/agents.
AgentIdentity = Literal[
    "analyst-annie",
    "architect-alphonso",
    "backend-benny",
    "bootstrap-bill",
    "code-reviewer-cindy",
    "curator-claire",
    "devops-danny",
    "diagram-daisy",
    "framework-guardian",
    "frontend-freddy",
    "java-jenny",
    "lexical-larry",
    "manager-mike",
    "planning-petra",
    "python-pedro",
    "researcher-ralph",
    "reviewer",
    "scribe-sally",
    "synthesizer-sam",
    "translator-tanya",
]


def validate_agent(agent_name: str) -> bool:
    """
    Validate that agent name is recognized.

    This function dynamically loads agent names from doctrine/agents
    to ensure single source of truth and avoid drift.

    Args:
        agent_name: Agent identifier to validate

    Returns:
        True if agent is valid, False otherwise
    """
    try:
        valid_agents = load_agent_identities()
        if valid_agents:
            return agent_name in valid_agents
    except Exception:
        # Fallback to Literal type if dynamic loading fails
        pass

    # Fallback to static Literal type for type checking context
    valid_agents = get_args(AgentIdentity)
    return agent_name in valid_agents


def get_all_agents() -> list[str]:
    """
    Get list of all valid agent identifiers.

    This function dynamically loads agent names from doctrine/agents
    to ensure single source of truth.

    Returns:
        List of agent name strings
    """
    try:
        agents = load_agent_identities()
        if agents:
            return agents
    except Exception:
        # Fallback to Literal type if dynamic loading fails
        pass

    # Fallback to static Literal type
    return list(get_args(AgentIdentity))
