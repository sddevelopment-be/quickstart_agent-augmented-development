"""Core module: Orchestration and governance logic.

This module implements Layer 1 (Orchestration & Governance) responsibilities:
- Agent specification parsing and validation
- Task lifecycle management
- Directive loading and context assembly
- Handoff protocol enforcement

References:
    - docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md
    - AGENTS.md (core specification)
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class TaskStatus(Enum):
    """Task lifecycle states per ADR-003."""

    INBOX = "inbox"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


@dataclass
class AgentProfile:
    """Agent profile metadata.

    Attributes:
        name: Agent identifier (e.g., 'devops-danny', 'curator-clara').
        specialization: Primary focus area.
        directives: List of required directive codes.
        mode_default: Default reasoning mode.
        capabilities: List of operational verbs.
    """

    name: str
    specialization: str
    directives: list[str]
    mode_default: str = "analysis"
    capabilities: Optional[list[str]] = None

    def __post_init__(self) -> None:
        """Validate profile after initialization."""
        if not self.name:
            raise ValueError("Agent name cannot be empty")
        if not self.specialization:
            raise ValueError("Agent specialization cannot be empty")
        if self.capabilities is None:
            self.capabilities = []


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
    agent: str | None = None
    priority: str = "normal"
    description: str = ""
    acceptance_criteria: Optional[list[str]] = None
    dependencies: Optional[list[str]] = None

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
