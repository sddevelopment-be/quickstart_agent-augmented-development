"""
⚠️ DEPRECATED: This file has moved to src/domain/doctrine/agent_loader.py

This location is preserved for backwards compatibility during migration.

Import from new location:
    from src.domain.doctrine.agent_loader import AgentProfileLoader, load_agent_identities

Migration: ADR-046 Task 2
See: src/common/MIGRATION_GUIDE.md
"""

# Re-export from new location for backwards compatibility
# NOTE: This will be removed in a future version
try:
    from src.domain.doctrine.agent_loader import (
        AgentProfileLoader,
        get_agent_loader,
        load_agent_identities,
    )
    
    __all__ = [
        "AgentProfileLoader",
        "get_agent_loader",
        "load_agent_identities",
    ]
except ImportError:
    # If imports break during migration, provide helpful error
    import warnings
    warnings.warn(
        "agent_loader.py has moved to src.domain.doctrine.agent_loader\n"
        "Update your imports to: from src.domain.doctrine.agent_loader import ...",
        DeprecationWarning,
        stacklevel=2
    )
    raise
