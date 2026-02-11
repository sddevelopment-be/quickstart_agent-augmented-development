"""
⚠️ DEPRECATED: This file has moved to src/domain/collaboration/task_schema.py

This location is preserved for backwards compatibility during migration.

Import from new location:
    from src.domain.collaboration.task_schema import read_task, write_task

Migration: ADR-046 Task 2
See: src/common/MIGRATION_GUIDE.md
"""

# Re-export from new location for backwards compatibility
# NOTE: This will be removed in a future version
try:
    from src.domain.collaboration.task_schema import (
        TaskSchemaError,
        TaskValidationError,
        TaskIOError,
        read_task,
        write_task,
        load_task_safe,
    )
    
    __all__ = [
        "TaskSchemaError",
        "TaskValidationError",
        "TaskIOError",
        "read_task",
        "write_task",
        "load_task_safe",
    ]
except ImportError:
    # If imports break during migration, provide helpful error
    import warnings
    warnings.warn(
        "task_schema.py has moved to src.domain.collaboration.task_schema\n"
        "Update your imports to: from src.domain.collaboration.task_schema import ...",
        DeprecationWarning,
        stacklevel=2
    )
    raise
