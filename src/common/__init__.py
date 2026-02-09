"""
Shared common package for agent-augmented development framework.

This package provides shared abstractions used across framework
orchestration and llm_service modules.

Modules:
- types: Type-safe enumerations and type aliases
- task_schema: Unified task I/O operations
"""

from .types import TaskStatus, FeatureStatus, AgentIdentity, validate_agent, get_all_agents

__all__ = [
    "TaskStatus",
    "FeatureStatus", 
    "AgentIdentity",
    "validate_agent",
    "get_all_agents",
]
