"""
Task Query Module - Production-grade task discovery and filtering.

Provides query operations for finding and filtering tasks across the
work/collaboration directory structure. Used by dashboard, CLI tools,
and orchestration components.

Related ADRs:
    - ADR-042: Shared Task Domain Model
    - ADR-043: Status Enumeration Standard

Directive Compliance:
    - 017 (TDD): Test coverage required before use
    - 021 (Locality): Extracted from tools/scripts for reusability
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from common.task_schema import load_task_safe
from common.types import TaskStatus


def find_task_files(work_dir: Path, include_done: bool = False) -> list[Path]:
    """
    Find all task YAML files in the collaboration directory.

    Scans the work directory for task files across different lifecycle stages.
    By default excludes completed tasks in done/ directory for performance.

    Args:
        work_dir: Work collaboration directory (work/collaboration)
        include_done: Include tasks from done/ directory (default: False)

    Returns:
        List of paths to task YAML files

    Example:
        >>> work_dir = Path("work/collaboration")
        >>> tasks = find_task_files(work_dir)
        >>> len(tasks)
        12
        >>> tasks[0].name
        '2026-02-09T2033-python-pedro-test-task.yaml'
    """
    task_files: list[Path] = []

    # Search in inbox directory
    inbox_dir = work_dir / "inbox"
    if inbox_dir.exists():
        task_files.extend(inbox_dir.glob("*.yaml"))

    # Search in assigned directories (recursive for agent subdirs)
    assigned_dir = work_dir / "assigned"
    if assigned_dir.exists():
        task_files.extend(assigned_dir.rglob("*.yaml"))

    # Optionally include completed tasks
    if include_done:
        done_dir = work_dir / "done"
        if done_dir.exists():
            task_files.extend(done_dir.rglob("*.yaml"))

    return sorted(task_files)  # Sort for deterministic ordering


def load_open_tasks(work_dir: Path) -> list[dict[str, Any]]:
    """
    Load all tasks that are not in terminal states.

    Finds and loads all tasks excluding those in terminal states (done, error).
    Useful for dashboard displays, active task lists, and orchestration queries.

    Args:
        work_dir: Work collaboration directory

    Returns:
        List of task dictionaries with non-terminal status

    Example:
        >>> work_dir = Path("work/collaboration")
        >>> open_tasks = load_open_tasks(work_dir)
        >>> all(not TaskStatus.is_terminal(TaskStatus(t['status'])) for t in open_tasks)
        True
    """
    task_files = find_task_files(work_dir, include_done=False)
    open_tasks = []

    for task_file in task_files:
        task = load_task_safe(task_file)
        if task is None:
            continue

        # Skip terminal states (done, error)
        status = task.get("status", "")
        try:
            task_status = TaskStatus(status)
            if not TaskStatus.is_terminal(task_status):
                open_tasks.append(task)
        except ValueError:
            # Invalid status, skip silently
            continue

    return open_tasks


def filter_tasks(
    tasks: list[dict[str, Any]],
    status: str | TaskStatus | None = None,
    agent: str | None = None,
    priority: str | None = None,
) -> list[dict[str, Any]]:
    """
    Filter tasks based on criteria.

    Provides flexible filtering for task lists based on common query patterns.
    All filters are AND conditions (task must match all provided criteria).

    Args:
        tasks: List of task dictionaries
        status: Filter by status (string or TaskStatus enum)
        agent: Filter by agent identifier
        priority: Filter by priority level

    Returns:
        Filtered list of tasks matching all criteria

    Example:
        >>> tasks = load_open_tasks(work_dir)
        >>> assigned = filter_tasks(tasks, status=TaskStatus.ASSIGNED)
        >>> pedro_tasks = filter_tasks(assigned, agent="python-pedro")
        >>> high_priority = filter_tasks(pedro_tasks, priority="high")
    """
    filtered = tasks

    if status:
        status_value = status.value if isinstance(status, TaskStatus) else status
        filtered = [t for t in filtered if t.get("status") == status_value]

    if agent:
        filtered = [t for t in filtered if t.get("agent") == agent]

    if priority:
        filtered = [t for t in filtered if t.get("priority") == priority]

    return filtered


def count_tasks_by_status(work_dir: Path) -> dict[str, int]:
    """
    Count tasks grouped by status.

    Provides summary statistics for task distribution across lifecycle states.
    Useful for dashboard metrics and orchestration monitoring.

    Args:
        work_dir: Work collaboration directory

    Returns:
        Dictionary mapping status values to counts

    Example:
        >>> counts = count_tasks_by_status(work_dir)
        >>> counts
        {'assigned': 5, 'in_progress': 3, 'blocked': 1}
    """
    tasks = load_open_tasks(work_dir)
    counts: dict[str, int] = {}

    for task in tasks:
        status = task.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1

    return counts


def count_tasks_by_agent(work_dir: Path) -> dict[str, int]:
    """
    Count tasks grouped by assigned agent.

    Provides workload distribution metrics across agents.
    Useful for load balancing and capacity planning.

    Args:
        work_dir: Work collaboration directory

    Returns:
        Dictionary mapping agent identifiers to task counts

    Example:
        >>> counts = count_tasks_by_agent(work_dir)
        >>> counts
        {'python-pedro': 4, 'backend-benny': 3, 'frontend-freddy': 2}
    """
    tasks = load_open_tasks(work_dir)
    counts: dict[str, int] = {}

    for task in tasks:
        agent = task.get("agent", "unassigned")
        counts[agent] = counts.get(agent, 0) + 1

    return counts
