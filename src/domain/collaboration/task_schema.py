"""
Shared task schema and I/O operations.

This module provides a single source of truth for task file operations,
ensuring consistency across framework orchestration and dashboard modules.

Related ADR:
- ADR-042: Shared Task Domain Model
"""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class TaskSchemaError(Exception):
    """Base exception for task schema operations"""

    pass


class TaskValidationError(TaskSchemaError):
    """Raised when task structure is invalid"""

    pass


class TaskIOError(TaskSchemaError):
    """Raised when task file I/O fails"""

    pass


def read_task(path: Path) -> dict[str, Any]:
    """
    Read and parse a task file.

    Args:
        path: Path to task YAML file

    Returns:
        Task dictionary with all fields

    Raises:
        TaskIOError: If file cannot be read or parsed
        TaskValidationError: If task structure is invalid
    """
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        # Detect common YAML issues before parsing
        if content.count("\n---\n") > 0 or content.count("\n--- \n") > 0:
            # Multiple document separators detected
            raise TaskIOError(
                f"Invalid YAML in {path}: expected a single document in the stream\n"
                f"  Found multiple '---' separators (YAML multi-document format not supported)\n"
                f"  Hint: Remove extra '---' lines or wrap content in 'description: |' block"
            )

        task = yaml.safe_load(content)

    except FileNotFoundError:
        raise TaskIOError(f"Task file not found: {path}")
    except yaml.YAMLError as e:
        # Check if it's the multi-document error
        error_msg = str(e)
        if "expected a single document" in error_msg:
            raise TaskIOError(
                f"Invalid YAML in {path}: expected a single document in the stream\n"
                f"  Hint: Check for multiple '---' separators in the file"
            )
        raise TaskIOError(f"Invalid YAML in {path}: {e}")
    except Exception as e:
        raise TaskIOError(f"Failed to read task {path}: {e}")

    if not isinstance(task, dict):
        raise TaskValidationError(f"Task must be a dictionary, got {type(task)}")

    # Auto-migrate old format: task_id → id (with warning)
    if "task_id" in task and "id" not in task:
        import warnings

        warnings.warn(
            f"Auto-migrating old task format in {path}: 'task_id' → 'id'\n"
            f"  Please update task file to use 'id' field directly",
            DeprecationWarning,
            stacklevel=2,
        )
        task["id"] = task["task_id"]
        # Note: We don't delete task_id to preserve backwards compatibility

    # Validate required fields
    required_fields = {"id", "status"}
    missing_fields = required_fields - set(task.keys())
    if missing_fields:
        raise TaskValidationError(f"Missing required fields: {missing_fields}")

    return task


def write_task(path: Path, task: dict[str, Any]) -> None:
    """
    Write a task to file.

    Args:
        path: Path to task YAML file
        task: Task dictionary to write

    Raises:
        TaskIOError: If file cannot be written
        TaskValidationError: If task structure is invalid
    """
    if not isinstance(task, dict):
        raise TaskValidationError(f"Task must be a dictionary, got {type(task)}")

    # Validate required fields before writing
    required_fields = {"id", "status"}
    missing_fields = required_fields - set(task.keys())
    if missing_fields:
        raise TaskValidationError(
            f"Cannot write task with missing fields: {missing_fields}"
        )

    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(task, f, sort_keys=False, default_flow_style=False)
    except Exception as e:
        raise TaskIOError(f"Failed to write task to {path}: {e}")


def load_task_safe(path: Path) -> dict[str, Any] | None:
    """
    Safely load a task file, returning None on error.

    This is a convenience wrapper for dashboard/monitoring code that
    needs to handle missing or invalid tasks gracefully.

    Args:
        path: Path to task YAML file

    Returns:
        Task dictionary if successful, None otherwise
    """
    try:
        return read_task(path)
    except TaskSchemaError as e:
        logger.warning(f"Failed to load task {path}: {e}")
        return None
