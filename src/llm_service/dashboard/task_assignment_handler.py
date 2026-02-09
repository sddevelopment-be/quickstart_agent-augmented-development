"""
Task Assignment Handler - Assigns orphan tasks to specifications/features.

Implements SPEC-DASH-008: Orphan Task Assignment with YAML comment preservation.
Follows patterns from ADR-035: Dashboard Task Priority Editing.

Key Features:
- Comment preservation using ruamel.yaml
- Atomic file writes (temp file + rename)
- Specification path validation (whitelist specifications/**/*.md)
- Status validation (reject in_progress/done/failed)
- Optimistic locking with last_modified timestamps
- Path traversal prevention
- WebSocket event emission (task.assigned, task.updated)

Related:
- ADR-035: Dashboard Task Priority Editing
- Specification: specifications/initiatives/dashboard-enhancements/orphan-task-assignment.md
"""

import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


class InvalidSpecificationError(Exception):
    """Raised when specification path is invalid or file doesn't exist."""

    pass


class TaskNotEditableError(Exception):
    """Raised when task status prevents assignment."""

    pass


class ConcurrentModificationError(Exception):
    """Raised when concurrent file modification is detected."""

    pass


class TaskAssignmentHandler:
    """
    Handles assignment of orphan tasks to specifications/features.

    Responsibilities:
    - Validate specification paths (prevent path traversal)
    - Check specification file exists
    - Load task YAML files with ruamel.yaml
    - Validate task status for editability
    - Update specification and feature fields atomically
    - Preserve comments and field order
    - Implement optimistic locking

    Attributes:
        work_dir: Base directory containing task files
        repo_root: Repository root directory (contains specifications/)
        yaml: ruamel.yaml instance for round-trip preservation
    """

    # Non-editable status values
    NON_EDITABLE_STATUSES = frozenset(["in_progress", "done", "failed"])

    def __init__(self, work_dir: str | Path, repo_root: str | Path) -> None:
        """
        Initialize TaskAssignmentHandler.

        Args:
            work_dir: Base directory containing task YAML files
            repo_root: Repository root directory (for resolving specification paths)

        Example:
            >>> handler = TaskAssignmentHandler(
            ...     work_dir='work/collaboration',
            ...     repo_root='.'
            ... )
        """
        self.work_dir = Path(work_dir)
        self.repo_root = Path(repo_root)
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.default_flow_style = False

    def validate_specification_path(self, spec_path: str) -> None:
        """
        Validate specification path to prevent security issues.

        Whitelist: specifications/**/*.md
        Rejects: Path traversal, absolute paths, non-markdown files

        Args:
            spec_path: Specification path to validate

        Raises:
            InvalidSpecificationError: If path is invalid

        Example:
            >>> handler.validate_specification_path('specifications/llm-service/api.md')  # OK
            >>> handler.validate_specification_path('../../../etc/passwd')  # Raises
        """
        # Reject path traversal attempts
        if ".." in spec_path:
            raise InvalidSpecificationError(
                f"Invalid specification path: contains path traversal: {spec_path}"
            )

        # Reject absolute paths
        if spec_path.startswith("/") or (len(spec_path) > 1 and spec_path[1] == ":"):
            raise InvalidSpecificationError(
                f"Invalid specification path: must be relative: {spec_path}"
            )

        # Ensure starts with specifications/
        if not spec_path.startswith("specifications/"):
            raise InvalidSpecificationError(
                f"Invalid specification path: must start with 'specifications/': {spec_path}"
            )

        # Ensure .md extension
        if not spec_path.endswith(".md"):
            raise InvalidSpecificationError(
                f"Invalid specification path: must be a .md file: {spec_path}"
            )

        # Additional validation: no backslashes (Windows path separators)
        if "\\" in spec_path:
            raise InvalidSpecificationError(
                f"Invalid specification path: contains backslashes: {spec_path}"
            )

    def check_specification_exists(self, spec_path: str) -> None:
        """
        Check that specification file exists.

        Args:
            spec_path: Specification path relative to repo root

        Raises:
            InvalidSpecificationError: If file doesn't exist

        Example:
            >>> handler.check_specification_exists('specifications/llm-service/api.md')
        """
        full_path = self.repo_root / spec_path

        if not full_path.exists():
            raise InvalidSpecificationError(
                f"Specification file not found: {spec_path}"
            )

        if not full_path.is_file():
            raise InvalidSpecificationError(
                f"Specification path is not a file: {spec_path}"
            )

    def is_task_editable(self, task_data: dict[str, Any]) -> bool:
        """
        Check if task status allows assignment.

        Tasks with status 'in_progress', 'done', or 'failed' cannot be assigned.

        Args:
            task_data: Task data dictionary

        Returns:
            True if editable, False otherwise

        Example:
            >>> task = {'status': 'pending'}
            >>> handler.is_task_editable(task)
            True
            >>> task = {'status': 'in_progress'}
            >>> handler.is_task_editable(task)
            False
        """
        status = task_data.get("status", "pending")
        return status not in self.NON_EDITABLE_STATUSES

    def update_task_specification(
        self,
        task_id: str,
        specification: str,
        feature: str | None = None,
        last_modified: str | None = None,
    ) -> dict[str, Any]:
        """
        Assign task to specification/feature with atomic write and comment preservation.

        Uses temp file + rename for atomic writes to prevent corruption.
        Preserves YAML comments and field order.
        Implements optimistic locking if last_modified provided.

        Args:
            task_id: Task ID to update
            specification: Specification path (e.g., 'specifications/llm-service/api.md')
            feature: Optional feature name/title
            last_modified: Optional timestamp for optimistic locking

        Returns:
            Updated task data as dictionary

        Raises:
            InvalidSpecificationError: If specification path is invalid or doesn't exist
            TaskNotEditableError: If task status prevents assignment
            ConcurrentModificationError: If file was modified (optimistic locking)
            FileNotFoundError: If task doesn't exist
            ValueError: If task_id is malicious

        Example:
            >>> updated = handler.update_task_specification(
            ...     task_id='task-123',
            ...     specification='specifications/llm-service/api.md',
            ...     feature='Rate Limiting'
            ... )
            >>> print(updated['specification'])
            'specifications/llm-service/api.md'
        """
        # Validate specification path
        self.validate_specification_path(specification)

        # Check specification file exists
        self.check_specification_exists(specification)

        # Get task file path
        task_file = self._get_task_file_path(task_id)

        if not task_file.exists():
            raise FileNotFoundError(f"Task file not found: {task_id}")

        # Load task with ruamel.yaml (preserves comments)
        with open(task_file, encoding="utf-8") as f:
            task_data = self.yaml.load(f)

        # Type assertion: ruamel.yaml.load returns Any, but we know it's a dict
        if not isinstance(task_data, dict):
            raise ValueError(f"Invalid YAML structure in task file: {task_id}")

        # Check if task is editable
        if not self.is_task_editable(task_data):
            status = task_data.get("status", "unknown")
            raise TaskNotEditableError(
                f"Cannot assign tasks with status '{status}'. "
                f"Tasks that are currently being worked on (in_progress, done, failed) cannot be reassigned."
            )

        # Optimistic locking check
        if last_modified is not None:
            current_modified = task_data.get("last_modified")
            if current_modified and str(current_modified) != str(last_modified):
                raise ConcurrentModificationError(
                    f"This task was modified by another user. "
                    f"Current: {current_modified}, Provided: {last_modified}"
                )

        # Update fields
        task_data["specification"] = specification

        if feature is not None:
            task_data["feature"] = feature
        # Note: If feature is None, we don't remove existing feature field
        # This preserves existing data if feature parameter is omitted

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

        return task_data

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
            >>> path = handler._get_task_file_path('2026-02-09T2000-task')
            >>> print(path)
            PosixPath('/work/collaboration/inbox/2026-02-09T2000-task.yaml')
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
