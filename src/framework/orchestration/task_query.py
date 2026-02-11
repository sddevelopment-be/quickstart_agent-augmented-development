"""
Task Query Module - Backward compatibility wrapper.

DEPRECATED: This module has been moved to src.domain.collaboration.task_query
as part of ADR-046 Domain Module Refactoring.

This file re-exports functions from the domain layer for backward compatibility.
New code should import directly from src.domain.collaboration.task_query.

Related ADRs:
    - ADR-042: Shared Task Domain Model
    - ADR-043: Status Enumeration Standard
    - ADR-046: Domain Module Refactoring

Migration Path:
    Old: from src.framework.orchestration.task_query import find_task_files
    New: from src.domain.collaboration.task_query import find_task_files
"""

from __future__ import annotations

# Re-export all functions from domain layer for backward compatibility
from src.domain.collaboration.task_query import (
    find_task_files,
    load_open_tasks,
    filter_tasks,
    count_tasks_by_status,
    count_tasks_by_agent,
)

__all__ = [
    "find_task_files",
    "load_open_tasks",
    "filter_tasks",
    "count_tasks_by_status",
    "count_tasks_by_agent",
]
