"""
Task Priority Updater - YAML file operations with comment preservation.

Implements priority editing for dashboard tasks using ruamel.yaml.
Follows ADR-035: Dashboard Task Priority Editing.

Key Features:
- Comment preservation using ruamel.yaml
- Atomic file writes (temp file + rename)
- Priority validation against schema
- Status validation (reject in_progress/done)
- Optimistic locking with last_modified timestamps
- Path traversal prevention

Related:
- ADR-035: Dashboard Task Priority Editing
- Specification: specifications/llm-dashboard/task-priority-editing.md
"""

import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


class ConcurrentModificationError(Exception):
    """Raised when concurrent file modification is detected."""

    pass


class TaskPriorityUpdater:
    """
    Handles task priority updates with YAML comment preservation.

    Responsibilities:
    - Load task YAML files with ruamel.yaml
    - Validate priority values against schema
    - Check task status for editability
    - Update priority field atomically
    - Preserve comments and field order
    - Implement optimistic locking

    Attributes:
        work_dir: Base directory containing task files
        yaml: ruamel.yaml instance for round-trip preservation
    """

    # Valid priority values from task schema
    VALID_PRIORITIES = frozenset(["CRITICAL", "HIGH", "MEDIUM", "LOW", "normal"])

    # Non-editable status values
    NON_EDITABLE_STATUSES = frozenset(["in_progress", "done", "failed"])

    def __init__(self, work_dir: str | Path) -> None:
        """
        Initialize TaskPriorityUpdater.

        Args:
            work_dir: Base directory containing task YAML files

        Example:
            >>> updater = TaskPriorityUpdater('work/collaboration')
            >>> updater.update_task_priority('task-123', 'HIGH')
        """
        self.work_dir = Path(work_dir)
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.default_flow_style = False

    def load_task(self, task_id: str) -> dict[str, Any]:
        """
        Load task YAML file with comment preservation.

        Args:
            task_id: Task ID (used to construct filename)

        Returns:
            Task data as dictionary

        Raises:
            FileNotFoundError: If task file doesn't exist
            ValueError: If task_id contains path traversal attempt

        Example:
            >>> task = updater.load_task('2026-02-06T1500-backend-dev-task')
            >>> print(task['priority'])
            'MEDIUM'
        """
        task_file = self._get_task_file_path(task_id)

        if not task_file.exists():
            raise FileNotFoundError(f"Task file not found: {task_id}")

        with open(task_file, encoding="utf-8") as f:
            task_data = self.yaml.load(f)

        # Type assertion: ruamel.yaml.load returns Any, but we know it's a dict
        if not isinstance(task_data, dict):
            raise ValueError(f"Invalid YAML structure in task file: {task_id}")

        return task_data

    def validate_priority(self, priority: str) -> None:
        """
        Validate priority value against schema.

        Args:
            priority: Priority value to validate

        Raises:
            ValueError: If priority is invalid

        Example:
            >>> updater.validate_priority('HIGH')  # OK
            >>> updater.validate_priority('INVALID')  # Raises ValueError
        """
        if not isinstance(priority, str) or not priority:
            valid_list = ", ".join(sorted(self.VALID_PRIORITIES))
            raise ValueError(f"Invalid priority. Must be one of: {valid_list}")

        # Normalize to uppercase for comparison
        priority_upper = priority.upper()

        if priority_upper not in self.VALID_PRIORITIES and priority not in ["normal"]:
            valid_list = ", ".join(sorted(self.VALID_PRIORITIES))
            raise ValueError(f"Invalid priority. Must be one of: {valid_list}")

    def is_editable_status(self, task_data: dict[str, Any]) -> bool:
        """
        Check if task status allows priority editing.

        Tasks with status 'in_progress', 'done', or 'failed' cannot be edited.

        Args:
            task_data: Task data dictionary

        Returns:
            True if editable, False otherwise

        Example:
            >>> task = {'status': 'pending'}
            >>> updater.is_editable_status(task)
            True
            >>> task = {'status': 'in_progress'}
            >>> updater.is_editable_status(task)
            False
        """
        status = task_data.get("status", "pending")
        return status not in self.NON_EDITABLE_STATUSES

    def update_task_priority(
        self, task_id: str, new_priority: str, last_modified: str | None = None
    ) -> None:
        """
        Update task priority with atomic write and comment preservation.

        Uses temp file + rename for atomic writes to prevent corruption.
        Preserves YAML comments and field order.
        Implements optimistic locking if last_modified provided.

        Args:
            task_id: Task ID to update
            new_priority: New priority value (CRITICAL, HIGH, MEDIUM, LOW, normal)
            last_modified: Optional timestamp for optimistic locking

        Raises:
            ValueError: If priority is invalid or task_id malicious
            FileNotFoundError: If task doesn't exist
            ConcurrentModificationError: If file was modified (optimistic locking)

        Example:
            >>> updater.update_task_priority('task-123', 'HIGH')
            >>> # With optimistic locking:
            >>> updater.update_task_priority(
            ...     'task-123',
            ...     'CRITICAL',
            ...     last_modified='2026-02-06T10:00:00Z'
            ... )
        """
        # Validate inputs
        self.validate_priority(new_priority)
        task_file = self._get_task_file_path(task_id)

        if not task_file.exists():
            raise FileNotFoundError(f"Task file not found: {task_id}")

        # Load task with ruamel.yaml (preserves comments)
        with open(task_file, encoding="utf-8") as f:
            task_data = self.yaml.load(f)

        # Optimistic locking check
        if last_modified is not None:
            current_modified = task_data.get("last_modified")
            if current_modified and str(current_modified) != str(last_modified):
                raise ConcurrentModificationError(
                    "Task was modified by another user. "
                    f"Current: {current_modified}, Provided: {last_modified}"
                )

        # Update priority field
        # Normalize priority (keep 'normal' lowercase, others uppercase)
        if new_priority.lower() == "normal":
            task_data["priority"] = "normal"
        else:
            task_data["priority"] = new_priority.upper()

        # Update last_modified timestamp
        task_data["last_modified"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        # Atomic write: Write to temp file, then rename
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=".yaml", dir=task_file.parent, text=True
        )

        try:
            # Write to temp file
            with os.fdopen(temp_fd, "w", encoding="utf-8") as temp_file:
                self.yaml.dump(task_data, temp_file)

            # Atomic rename (overwrites destination on POSIX)
            os.replace(temp_path, task_file)

        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    def _get_task_file_path(self, task_id: str) -> Path:
        """
        Get validated task file path, preventing path traversal.

        Validates task_id to prevent directory traversal attacks.
        Searches for task file in inbox, assigned, and done directories.

        Args:
            task_id: Task identifier

        Returns:
            Path to task file

        Raises:
            ValueError: If task_id contains path traversal characters

        Example:
            >>> path = updater._get_task_file_path('2026-02-06T1500-task')
            >>> print(path)
            PosixPath('/work/collaboration/inbox/2026-02-06T1500-task.yaml')
        """
        # Security: Prevent path traversal
        if ".." in task_id or "/" in task_id or "\\" in task_id:
            raise ValueError(
                f"Invalid task ID: contains path traversal characters: {task_id}"
            )

        # Allow only alphanumeric, dash, underscore, and .yaml/.yml extension
        if not re.match(r"^[a-zA-Z0-9_-]+(?:\.ya?ml)?$", task_id):
            raise ValueError(
                f"Invalid task ID format: {task_id}. "
                "Must contain only alphanumeric characters, dashes, underscores, and optional .yaml extension."
            )

        # Search for task file in common locations
        # Try with and without .yaml extension
        task_filename = task_id if task_id.endswith(".yaml") else f"{task_id}.yaml"

        # Search paths: inbox, assigned/*, done/*
        search_paths = [
            self.work_dir / "inbox" / task_filename,
            self.work_dir / task_filename,  # Direct path
        ]

        # Also search assigned and done subdirectories
        for subdir in ["assigned", "done"]:
            subdir_path = self.work_dir / subdir
            if subdir_path.exists():
                # Search agent subdirectories
                for agent_dir in subdir_path.iterdir():
                    if agent_dir.is_dir():
                        search_paths.append(agent_dir / task_filename)

        # Return first existing path
        for path in search_paths:
            if path.exists():
                return path

        # Not found - return inbox path for FileNotFoundError
        return self.work_dir / "inbox" / task_filename
