"""
Agent identity type definitions for doctrine domain.

This module provides agent-related types and validation
for agent profiles and identities.

Related ADRs:
- ADR-044: Agent Identity Type Safety
- ADR-046: Domain Module Refactoring
"""

from typing import TYPE_CHECKING, Literal, get_args

# Import agent loader for dynamic agent identity loading
if TYPE_CHECKING:
    # Stub for type checking (mypy strict mode)
    def load_agent_identities() -> list[str] | None:
        """Load agent identities from doctrine/agents/*.agent.md files."""
        ...

else:
    try:
        from .agent_loader import load_agent_identities
    except ImportError:
        # Fallback if agent_loader not available
        def load_agent_identities() -> list[str] | None:
            """
            Fallback implementation for loading agent identities.
            
            Returns None when the agent_loader module is not available.
            
            Returns:
                None (fallback implementation)
            """
            return None


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
    fallback_agents: tuple[str, ...] = get_args(AgentIdentity)
    return agent_name in fallback_agents


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
