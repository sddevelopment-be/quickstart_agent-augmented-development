"""Orchestrator class.

Core orchestration engine managing task assignment, lifecycle transitions,
agent coordination, and directive loading per AGENTS.md specification.
"""

from pathlib import Path

from framework.core.agent_profile import AgentProfile
from framework.core.task import Task
from framework.core.task_status import TaskStatus


class Orchestrator:
    """Core orchestration engine.

    Manages task assignment, lifecycle transitions, agent coordination,
    and directive loading per AGENTS.md specification.
    """

    def __init__(self, agents_dir: Path, work_dir: Path) -> None:
        """Initialize orchestrator.

        Args:
            agents_dir: Path to .github/agents/ directory.
            work_dir: Path to work/ directory for task coordination.

        Raises:
            FileNotFoundError: If required directories don't exist.
        """
        if not agents_dir.exists():
            raise FileNotFoundError(f"Agents directory not found: {agents_dir}")
        if not work_dir.exists():
            raise FileNotFoundError(f"Work directory not found: {work_dir}")

        self.agents_dir = agents_dir
        self.work_dir = work_dir
        self._profiles: dict[str, AgentProfile] = {}
        self._directives: dict[str, str] = {}

    def load_agent_profiles(self) -> None:
        """Load agent profiles from .github/agents/*.agent.md files.

        Raises:
            RuntimeError: If profile parsing fails.
        """
        # TODO: Parse agent profile markdown files
        # TODO: Validate profile structure
        # TODO: Store in _profiles dict
        pass

    def load_directives(self, directive_codes: list[str]) -> None:
        """Load specified directives from .github/agents/directives/.

        Args:
            directive_codes: List of directive codes to load (e.g., ['001', '014']).

        Raises:
            FileNotFoundError: If directive file not found.
        """
        # TODO: Load directive markdown files
        # TODO: Store in _directives dict
        pass

    def assign_task(self, task: Task) -> AgentProfile:
        """Assign task to appropriate agent based on specialization.

        Args:
            task: Task to assign.

        Returns:
            Selected agent profile.

        Raises:
            ValueError: If no suitable agent found.
        """
        if not self._profiles:
            raise RuntimeError("No agent profiles loaded")

        # TODO: Implement agent selection logic
        # TODO: Check agent capabilities match task requirements
        # TODO: Update task status and agent field
        # TODO: Move task file to work/assigned/<agent>/

        raise NotImplementedError("Task assignment not yet implemented")

    def transition_task(
        self,
        task: Task,
        new_status: TaskStatus,
    ) -> None:
        """Transition task to new status per lifecycle rules.

        Args:
            task: Task to transition.
            new_status: Target status.

        Raises:
            ValueError: If transition is invalid.
        """
        valid_transitions = {
            TaskStatus.INBOX: [TaskStatus.ASSIGNED, TaskStatus.CANCELLED],
            TaskStatus.ASSIGNED: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
            TaskStatus.IN_PROGRESS: [
                TaskStatus.BLOCKED,
                TaskStatus.DONE,
                TaskStatus.CANCELLED,
            ],
            TaskStatus.BLOCKED: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
        }

        if task.status not in valid_transitions:
            raise ValueError(f"Cannot transition from terminal state: {task.status}")

        if new_status not in valid_transitions[task.status]:
            raise ValueError(
                f"Invalid transition: {task.status} -> {new_status}. "
                f"Valid targets: {valid_transitions[task.status]}"
            )

        # TODO: Move task file to appropriate directory
        # TODO: Update task YAML status field
        task.status = new_status
