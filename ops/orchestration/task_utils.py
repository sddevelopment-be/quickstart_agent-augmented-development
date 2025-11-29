#!/usr/bin/env python3
"""
Task Utilities - Common functions for task file operations

Provides shared functionality for reading, writing, and manipulating
task YAML files in the orchestration framework.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import yaml


def read_task(task_file: Path) -> Dict[str, Any]:
    """Load task YAML file.
    
    Args:
        task_file: Path to task YAML file
        
    Returns:
        Dictionary containing task data
    """
    with open(task_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_task(task_file: Path, task: Dict[str, Any]) -> None:
    """Save task to YAML file.
    
    Args:
        task_file: Path to task YAML file
        task: Dictionary containing task data
    """
    task_file.parent.mkdir(parents=True, exist_ok=True)
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task, f, default_flow_style=False, sort_keys=False)


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


def get_utc_timestamp() -> str:
    """Get current UTC timestamp in ISO8601 format with Z suffix.
    
    Returns:
        Timestamp string (e.g., "2025-11-25T18:30:00Z")
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def update_task_status(
    task: Dict[str, Any],
    status: str,
    timestamp_field: str | None = None
) -> Dict[str, Any]:
    """Update task status and add corresponding timestamp.
    
    Args:
        task: Task dictionary
        status: New status value
        timestamp_field: Optional timestamp field name (e.g., "assigned_at")
        
    Returns:
        Updated task dictionary
    """
    task["status"] = status
    if timestamp_field:
        task[timestamp_field] = get_utc_timestamp()
    return task
