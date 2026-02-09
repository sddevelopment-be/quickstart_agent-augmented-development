"""
Shared type definitions for the agent-augmented development framework.

This module provides type-safe enumerations and type aliases used
across framework orchestration and dashboard modules.

Related ADRs:
- ADR-043: Status Enumeration Standard
- ADR-044: Agent Identity Type Safety
"""

from enum import Enum
from typing import Literal, get_args


class TaskStatus(str, Enum):
    """
    Task lifecycle states.
    
    Tasks flow through these states during execution:
    NEW → INBOX → ASSIGNED → IN_PROGRESS → {DONE | ERROR | BLOCKED}
    
    Inherits from str to maintain YAML serialization compatibility.
    """
    
    # Lifecycle states
    NEW = "new"                    # Task created, awaiting assignment
    INBOX = "inbox"                # Task in inbox, awaiting agent pickup
    ASSIGNED = "assigned"          # Task assigned to specific agent
    IN_PROGRESS = "in_progress"    # Agent actively executing task
    BLOCKED = "blocked"            # Task blocked on dependency/blocker
    DONE = "done"                  # Task successfully completed
    ERROR = "error"                # Task failed with error
    
    @classmethod
    def is_terminal(cls, status: 'TaskStatus') -> bool:
        """Check if status represents a terminal state."""
        return status in {cls.DONE, cls.ERROR}
    
    @classmethod
    def is_active(cls, status: 'TaskStatus') -> bool:
        """Check if status represents an active (non-terminal) state."""
        return status in {cls.ASSIGNED, cls.IN_PROGRESS, cls.BLOCKED}
    
    @classmethod
    def is_pending(cls, status: 'TaskStatus') -> bool:
        """Check if status represents a pending (not yet started) state."""
        return status in {cls.NEW, cls.INBOX}


class FeatureStatus(str, Enum):
    """
    Feature/specification implementation states.
    
    Features flow through these states during development:
    DRAFT → PLANNED → IN_PROGRESS → IMPLEMENTED → {DEPRECATED}
    
    Inherits from str to maintain YAML serialization compatibility.
    """
    
    DRAFT = "draft"                    # Specification in draft, not approved
    PLANNED = "planned"                # Approved, implementation planned
    IN_PROGRESS = "in_progress"        # Implementation ongoing
    IMPLEMENTED = "implemented"        # Complete and deployed
    DEPRECATED = "deprecated"          # No longer relevant
    
    @classmethod
    def is_active(cls, status: 'FeatureStatus') -> bool:
        """Check if feature is actively being worked on."""
        return status in {cls.PLANNED, cls.IN_PROGRESS}
    
    @classmethod
    def is_complete(cls, status: 'FeatureStatus') -> bool:
        """Check if feature implementation is complete."""
        return status == cls.IMPLEMENTED


# Agent Identity Type (Literal for type checking)
AgentIdentity = Literal[
    "architect",           # Architect Alphonso
    "backend-dev",         # Backend Benny  
    "python-pedro",        # Python Pedro
    "frontend",            # Frontend Freddy
    "devops-danny",        # DevOps Danny
    "planning-petra",      # Planning Petra
    "manager-mike",        # Manager Mike
    "curator",             # Curator Claire
    "writer-editor",       # Writer-Editor Eddy
    "scribe",              # Scribe Sally
    "researcher",          # Researcher Ralph
    "diagrammer",          # Diagrammer Diana
    "lexical",             # Lexical Larry
    "synthesizer",         # Synthesizer Sam
    "translator",          # Translator Tanya
    "bootstrap-bill",      # Bootstrap Bill
    "framework-guardian",  # Framework Guardian
    "java-jenny",          # Java Jenny
    "analyst-annie",       # Analyst Annie
    "code-reviewer",       # Code Reviewer Cindy
]


def validate_agent(agent_name: str) -> bool:
    """
    Validate that agent name is recognized.
    
    Args:
        agent_name: Agent identifier to validate
        
    Returns:
        True if agent is valid, False otherwise
    """
    valid_agents = get_args(AgentIdentity)
    return agent_name in valid_agents


def get_all_agents() -> list[str]:
    """
    Get list of all valid agent identifiers.
    
    Returns:
        List of agent name strings
    """
    return list(get_args(AgentIdentity))
