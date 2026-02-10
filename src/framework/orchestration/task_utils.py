#!/usr/bin/env python3
"""
Task Utilities - Common functions for task file operations

Provides shared functionality for reading, writing, and manipulating
task YAML files in the orchestration framework.

NOTE: This module now delegates to src.common.task_schema for task I/O.
See ADR-042: Shared Task Domain Model for migration details.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Import shared task I/O from common module (ADR-042)
from common.task_schema import read_task, write_task
from common.types import TaskStatus

# Re-export for backward compatibility
__all__ = [
    "read_task",
    "write_task",
    "log_event",
    "get_utc_timestamp",
    "update_task_status",
    "find_task_file",
]


def log_event(message: str, log_file: Path) -> None:
    """Append event to a log file with timestamp.

    Args:
        message: Log message
        log_file: Path to log file
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n**{timestamp}** - {message}")


def find_task_file(task_id: str, work_dir: Path) -> Path | None:
    """Find task file by ID in assigned directories.

    Searches recursively through the work/assigned directory structure
    to locate a task YAML file matching the given task ID.

    Args:
        task_id: Task identifier (e.g., "2026-02-10T1000-agent-task")
        work_dir: Work collaboration directory (typically "work/")

    Returns:
        Path to task file if found, None otherwise

    Note:
        Consolidated from tools/scripts to eliminate duplication.
        See Enhancement H1 for consolidation rationale.
    """
    assigned_dir = work_dir / "assigned"
    if not assigned_dir.exists():
        return None

    # Search for task in all agent subdirectories using recursive glob
    for task_file in assigned_dir.rglob(f"{task_id}.yaml"):
        return task_file  # Return first match

    return None


def get_utc_timestamp() -> str:
    """Get current UTC timestamp in ISO8601 format with Z suffix.

    Format uses seconds precision (no microseconds) for consistency with
    existing task files and human readability.

    Returns:
        Timestamp string with seconds precision (e.g., "2026-02-10T05:49:43Z")

    Note:
        Uses strftime format for seconds-only precision to match production
        task file conventions. See Enhancement H1 timestamp format decision.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def update_task_status(
    task: dict[str, Any], status: str | TaskStatus, timestamp_field: str | None = None
) -> dict[str, Any]:
    """Update task status and add corresponding timestamp.

    Args:
        task: Task dictionary
        status: New status value (string or TaskStatus enum)
        timestamp_field: Optional timestamp field name (e.g., "assigned_at")

    Returns:
        Updated task dictionary

    Note:
        Accepts both string and TaskStatus enum for backward compatibility.
        Enum usage is preferred (ADR-043).
    """
    # Convert enum to string value if needed
    if isinstance(status, TaskStatus):
        task["status"] = status.value
    else:
        task["status"] = status

    if timestamp_field:
        task[timestamp_field] = get_utc_timestamp()
    return task
