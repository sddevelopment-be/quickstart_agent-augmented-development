"""
⚠️ DEPRECATED: This file has moved to src/domain/common/path_utils.py

This location is preserved for backwards compatibility during migration.

Import from new location:
    from src.domain.common.path_utils import get_repo_root, get_work_dir

Migration: ADR-046 Task 2
See: src/common/MIGRATION_GUIDE.md
"""

# Re-export from new location for backwards compatibility
# NOTE: This will be removed in a future version
try:
    from src.domain.common.path_utils import (
        get_repo_root,
        get_work_dir,
        get_agents_dir,
    )
    
    __all__ = [
        "get_repo_root",
        "get_work_dir",
        "get_agents_dir",
    ]
except ImportError:
    # If imports break during migration, provide helpful error
    import warnings
    warnings.warn(
        "path_utils.py has moved to src.domain.common.path_utils\n"
        "Update your imports to: from src.domain.common.path_utils import ...",
        DeprecationWarning,
        stacklevel=2
    )
    raise
