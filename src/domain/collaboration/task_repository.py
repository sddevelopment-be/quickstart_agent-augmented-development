"""
Task Repository - Data access layer for task entities.

Implements Repository pattern for task domain objects, providing a clean
separation between domain logic and data access concerns. This aligns with
CQRS and DDD principles as outlined in ADR-046.

The repository encapsulates:
- File system operations for task persistence
- Query operations for task discovery
- Read operations with proper error handling

Related ADRs:
    - ADR-042: Shared Task Domain Model
    - ADR-043: Status Enumeration Standard
    - ADR-046: Domain Module Refactoring

Architecture:
    - Domain Layer: Contains task entities, value objects, and this repository
    - Application Layer (Framework/LLM Service): Uses repository for data access
    - No direct file system access outside repository

Usage Example:
    >>> from pathlib import Path
    >>> repo = TaskRepository(Path("work/collaboration"))
    >>> open_tasks = repo.find_open_tasks()
    >>> assigned_tasks = repo.find_by_status(TaskStatus.ASSIGNED)
    >>> pedro_tasks = repo.find_by_agent("python-pedro")
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass

from src.domain.collaboration.task_schema import load_task_safe
from src.domain.collaboration.types import TaskStatus


@dataclass
class TaskQueryResult:
    """Result of a task query operation."""
    tasks: list[dict[str, Any]]
    total_count: int
    
    def filter_by_status(self, status: TaskStatus | str) -> 'TaskQueryResult':
        """Filter results by status."""
        status_value = status.value if isinstance(status, TaskStatus) else status
        filtered = [t for t in self.tasks if t.get("status") == status_value]
        return TaskQueryResult(tasks=filtered, total_count=len(filtered))
    
    def filter_by_agent(self, agent: str) -> 'TaskQueryResult':
        """Filter results by assigned agent."""
        filtered = [t for t in self.tasks if t.get("agent") == agent]
        return TaskQueryResult(tasks=filtered, total_count=len(filtered))


class TaskRepository:
    """
    Repository for task entities.
    
    Provides data access operations for tasks, abstracting file system
    details from the domain and application layers.
    
    This follows the Repository pattern from DDD, providing:
    - Collection-like interface for tasks
    - Query methods returning domain objects
    - Encapsulation of persistence concerns
    """
    
    def __init__(self, work_dir: Path):
        """
        Initialize repository with work directory.
        
        Args:
            work_dir: Path to work/collaboration directory
        """
        self.work_dir = work_dir
    
    def find_all(self, include_done: bool = False) -> TaskQueryResult:
        """
        Find all tasks in the repository.
        
        Args:
            include_done: Include completed tasks from done/ directory
            
        Returns:
            TaskQueryResult with all tasks
        """
        task_files = self._discover_task_files(include_done=include_done)
        tasks = []
        
        for task_file in task_files:
            task = load_task_safe(task_file)
            if task is not None:
                tasks.append(task)
        
        return TaskQueryResult(tasks=tasks, total_count=len(tasks))
    
    def find_open_tasks(self) -> TaskQueryResult:
        """
        Find all tasks not in terminal states.
        
        Returns:
            TaskQueryResult with non-terminal tasks (not done/error)
        """
        task_files = self._discover_task_files(include_done=False)
        open_tasks = []
        
        for task_file in task_files:
            task = load_task_safe(task_file)
            if task is None:
                continue
            
            # Skip terminal states
            status = task.get("status", "")
            try:
                task_status = TaskStatus(status)
                if not TaskStatus.is_terminal(task_status):
                    open_tasks.append(task)
            except ValueError:
                # Invalid status, skip
                continue
        
        return TaskQueryResult(tasks=open_tasks, total_count=len(open_tasks))
    
    def find_by_status(self, status: TaskStatus | str) -> TaskQueryResult:
        """
        Find tasks by status.
        
        Args:
            status: Task status to filter by
            
        Returns:
            TaskQueryResult with matching tasks
        """
        all_tasks = self.find_all(include_done=True)
        return all_tasks.filter_by_status(status)
    
    def find_by_agent(self, agent: str) -> TaskQueryResult:
        """
        Find tasks assigned to specific agent.
        
        Args:
            agent: Agent identifier
            
        Returns:
            TaskQueryResult with matching tasks
        """
        open_tasks = self.find_open_tasks()
        return open_tasks.filter_by_agent(agent)
    
    def find_by_id(self, task_id: str) -> Optional[dict[str, Any]]:
        """
        Find a single task by ID.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task dictionary or None if not found
        """
        all_tasks = self.find_all(include_done=True)
        for task in all_tasks.tasks:
            if task.get("id") == task_id:
                return task
        return None
    
    def count_by_status(self) -> dict[str, int]:
        """
        Count tasks grouped by status.
        
        Returns:
            Dictionary mapping status to count
        """
        open_tasks = self.find_open_tasks()
        counts: dict[str, int] = {}
        
        for task in open_tasks.tasks:
            status = task.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        
        return counts
    
    def count_by_agent(self) -> dict[str, int]:
        """
        Count tasks grouped by assigned agent.
        
        Returns:
            Dictionary mapping agent to count
        """
        open_tasks = self.find_open_tasks()
        counts: dict[str, int] = {}
        
        for task in open_tasks.tasks:
            agent = task.get("agent", "unassigned")
            counts[agent] = counts.get(agent, 0) + 1
        
        return counts
    
    def _discover_task_files(self, include_done: bool = False) -> list[Path]:
        """
        Discover task YAML files in the work directory.
        
        Internal method that handles file system traversal.
        
        Args:
            include_done: Include tasks from done/ directory
            
        Returns:
            List of paths to task YAML files
        """
        task_files: list[Path] = []
        
        # Search inbox
        inbox_dir = self.work_dir / "inbox"
        if inbox_dir.exists():
            task_files.extend(inbox_dir.glob("*.yaml"))
        
        # Search assigned (recursive for agent subdirs)
        assigned_dir = self.work_dir / "assigned"
        if assigned_dir.exists():
            task_files.extend(assigned_dir.rglob("*.yaml"))
        
        # Optionally include done
        if include_done:
            done_dir = self.work_dir / "done"
            if done_dir.exists():
                task_files.extend(done_dir.rglob("*.yaml"))
        
        return sorted(task_files)
