"""Task dataclass.

Represents task descriptor per file-based orchestration protocol.
"""

from dataclasses import dataclass
from typing import List, Optional

from framework.core.task_status import TaskStatus


@dataclass
class Task:
    """Task descriptor per file-based orchestration protocol.

    Attributes:
        id: Unique task identifier (ISO timestamp + slug).
        title: Human-readable task title.
        status: Current lifecycle state.
        agent: Assigned agent profile name.
        priority: Task priority (critical, high, medium, normal).
        description: Detailed task description.
        acceptance_criteria: List of success criteria.
        dependencies: List of task IDs this task depends on.
    """

    id: str
    title: str
    status: TaskStatus
    agent: Optional[str] = None
    priority: str = "normal"
    description: str = ""
    acceptance_criteria: Optional[List[str]] = None
    dependencies: Optional[List[str]] = None

    def __post_init__(self) -> None:
        """Validate task after initialization."""
        if not self.id:
            raise ValueError("Task ID cannot be empty")
        if not self.title:
            raise ValueError("Task title cannot be empty")

        valid_priorities = {"critical", "high", "medium", "normal"}
        if self.priority not in valid_priorities:
            raise ValueError(
                f"Invalid priority '{self.priority}'. "
                f"Must be one of: {valid_priorities}"
            )

        if self.acceptance_criteria is None:
            self.acceptance_criteria = []
        if self.dependencies is None:
            self.dependencies = []
