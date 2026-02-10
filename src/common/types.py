"""
Shared type definitions for the agent-augmented development framework.

This module provides type-safe enumerations and type aliases used
across framework orchestration and dashboard modules.

Related ADRs:
- ADR-043: Status Enumeration Standard
- ADR-044: Agent Identity Type Safety
"""

from enum import Enum
from typing import TYPE_CHECKING, Literal, get_args

# Import agent loader for dynamic agent identity loading
if TYPE_CHECKING:
    # Stub for type checking (mypy strict mode)
    def load_agent_identities() -> list[str] | None:
        """Load agent identities from doctrine/agents/*.agent.md files."""
        ...

else:
    try:
        from .agent_loader import load_agent_identities
    except ImportError:
        # Fallback if agent_loader not available
        def load_agent_identities() -> list[str] | None:
            return None


class TaskStatus(str, Enum):
    """
    Task lifecycle states.

    Tasks flow through these states during execution:
    NEW → INBOX → ASSIGNED → IN_PROGRESS → {DONE | ERROR | BLOCKED}

    Inherits from str to maintain YAML serialization compatibility.

    State Machine:
    - NEW can transition to: INBOX, ASSIGNED, ERROR
    - INBOX can transition to: ASSIGNED, ERROR
    - ASSIGNED can transition to: IN_PROGRESS, BLOCKED, ERROR
    - IN_PROGRESS can transition to: DONE, BLOCKED, ERROR
    - BLOCKED can transition to: IN_PROGRESS, ERROR
    - DONE is terminal (no transitions)
    - ERROR is terminal (no transitions)
    """

    # Lifecycle states
    NEW = "new"  # Task created, awaiting assignment
    INBOX = "inbox"  # Task in inbox, awaiting agent pickup
    ASSIGNED = "assigned"  # Task assigned to specific agent
    IN_PROGRESS = "in_progress"  # Agent actively executing task
    BLOCKED = "blocked"  # Task blocked on dependency/blocker
    DONE = "done"  # Task successfully completed
    ERROR = "error"  # Task failed with error

    @classmethod
    def is_terminal(cls, status: "TaskStatus") -> bool:
        """Check if status represents a terminal state."""
        return status in {cls.DONE, cls.ERROR}

    @classmethod
    def is_active(cls, status: "TaskStatus") -> bool:
        """Check if status represents an active (non-terminal) state."""
        return status in {cls.ASSIGNED, cls.IN_PROGRESS, cls.BLOCKED}

    @classmethod
    def is_pending(cls, status: "TaskStatus") -> bool:
        """Check if status represents a pending (not yet started) state."""
        return status in {cls.NEW, cls.INBOX}

    def valid_transitions(self) -> set["TaskStatus"]:
        """
        Get valid next states from current state.

        Returns:
            Set of TaskStatus values that are valid transitions from this state.
            Terminal states (DONE, ERROR) return empty set.

        Example:
            >>> TaskStatus.ASSIGNED.valid_transitions()
            {TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED, TaskStatus.ERROR}
        """
        _transitions: dict[TaskStatus, set[TaskStatus]] = {
            TaskStatus.NEW: {TaskStatus.INBOX, TaskStatus.ASSIGNED, TaskStatus.ERROR},
            TaskStatus.INBOX: {TaskStatus.ASSIGNED, TaskStatus.ERROR},
            TaskStatus.ASSIGNED: {TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED, TaskStatus.ERROR},
            TaskStatus.IN_PROGRESS: {TaskStatus.DONE, TaskStatus.BLOCKED, TaskStatus.ERROR},
            TaskStatus.BLOCKED: {TaskStatus.IN_PROGRESS, TaskStatus.ERROR},
            TaskStatus.DONE: set(),  # Terminal state
            TaskStatus.ERROR: set(),  # Terminal state
        }
        return _transitions[self]

    def can_transition_to(self, target: "TaskStatus") -> bool:
        """
        Check if transition from current state to target state is valid.

        Args:
            target: Target state to transition to

        Returns:
            True if transition is allowed, False otherwise

        Example:
            >>> TaskStatus.ASSIGNED.can_transition_to(TaskStatus.IN_PROGRESS)
            True
            >>> TaskStatus.DONE.can_transition_to(TaskStatus.ASSIGNED)
            False
        """
        return target in self.valid_transitions()

    @classmethod
    def validate_transition(cls, current: "TaskStatus", target: "TaskStatus") -> None:
        """
        Validate state transition and raise error if invalid.

        Args:
            current: Current state
            target: Target state to transition to

        Raises:
            ValueError: If transition is not allowed, with descriptive error message

        Example:
            >>> TaskStatus.validate_transition(TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS)
            # No error raised

            >>> TaskStatus.validate_transition(TaskStatus.DONE, TaskStatus.ASSIGNED)
            ValueError: Invalid transition from DONE to ASSIGNED. Valid transitions: none (terminal state)
        """
        if not current.can_transition_to(target):
            valid = current.valid_transitions()
            if valid:
                valid_str = ", ".join(sorted(s.value.upper() for s in valid))
                raise ValueError(
                    f"Invalid transition from {current.value.upper()} to {target.value.upper()}. "
                    f"Valid transitions: {valid_str}"
                )
            else:
                raise ValueError(
                    f"Invalid transition from {current.value.upper()} to {target.value.upper()}. "
                    f"Valid transitions: none (terminal state)"
                )


class FeatureStatus(str, Enum):
    """
    Feature/specification implementation states.

    Features flow through these states during development:
    DRAFT → PLANNED → IN_PROGRESS → IMPLEMENTED → {DEPRECATED}

    Inherits from str to maintain YAML serialization compatibility.
    """

    DRAFT = "draft"  # Specification in draft, not approved
    PLANNED = "planned"  # Approved, implementation planned
    IN_PROGRESS = "in_progress"  # Implementation ongoing
    IMPLEMENTED = "implemented"  # Complete and deployed
    DEPRECATED = "deprecated"  # No longer relevant

    @classmethod
    def is_active(cls, status: "FeatureStatus") -> bool:
        """Check if feature is actively being worked on."""
        return status in {cls.PLANNED, cls.IN_PROGRESS}

    @classmethod
    def is_complete(cls, status: "FeatureStatus") -> bool:
        """Check if feature implementation is complete."""
        return status == cls.IMPLEMENTED


class TaskMode(str, Enum):
    """
    Agent operating modes for task execution.

    Modes influence how agents approach problem-solving:
    - ANALYSIS: Deep analytical thinking and investigation
    - CREATIVE: Exploration of alternative solutions
    - META: Process and quality reflection
    - PROGRAMMING: Implementation and coding
    - PLANNING: Strategic planning and coordination

    Inherits from str to maintain YAML serialization compatibility.
    """

    ANALYSIS = "/analysis-mode"  # Analytical reasoning mode
    CREATIVE = "/creative-mode"  # Creative exploration mode
    META = "/meta-mode"  # Meta-cognitive reflection mode
    PROGRAMMING = "/programming"  # Programming/implementation mode
    PLANNING = "/planning"  # Planning and coordination mode


class TaskPriority(str, Enum):
    """
    Task priority levels for scheduling and triage.

    Priority levels from highest to lowest urgency:
    CRITICAL → HIGH → MEDIUM → NORMAL → LOW

    Inherits from str to maintain YAML serialization compatibility.
    """

    CRITICAL = "critical"  # Immediate attention required
    HIGH = "high"  # Important, schedule soon
    MEDIUM = "medium"  # Normal priority
    NORMAL = "normal"  # Standard priority (default)
    LOW = "low"  # Can be deferred

    @property
    def order(self) -> int:
        """
        Get numeric ordering for priority comparison.

        Lower numbers = higher priority (for sorting).

        Returns:
            Integer ordering value (0=highest, 4=lowest)
        """
        _priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.NORMAL: 3,
            TaskPriority.LOW: 4,
        }
        return _priority_order[self]

    @classmethod
    def is_urgent(cls, priority: "TaskPriority") -> bool:
        """
        Check if priority level requires urgent attention.

        Args:
            priority: Priority level to check

        Returns:
            True if CRITICAL or HIGH priority
        """
        return priority in {cls.CRITICAL, cls.HIGH}


# Agent Identity Type (Literal for type checking)
# NOTE: For static type checking, we keep a baseline Literal type.
# At runtime, validation uses dynamically loaded agents from doctrine/agents.
AgentIdentity = Literal[
    "analyst-annie",
    "architect-alphonso",
    "backend-benny",
    "bootstrap-bill",
    "code-reviewer-cindy",
    "curator-claire",
    "devops-danny",
    "diagram-daisy",
    "framework-guardian",
    "frontend-freddy",
    "java-jenny",
    "lexical-larry",
    "manager-mike",
    "planning-petra",
    "python-pedro",
    "researcher-ralph",
    "reviewer",
    "scribe-sally",
    "synthesizer-sam",
    "translator-tanya",
]


def validate_agent(agent_name: str) -> bool:
    """
    Validate that agent name is recognized.

    This function dynamically loads agent names from doctrine/agents
    to ensure single source of truth and avoid drift.

    Args:
        agent_name: Agent identifier to validate

    Returns:
        True if agent is valid, False otherwise
    """
    try:
        valid_agents = load_agent_identities()
        if valid_agents:
            return agent_name in valid_agents
    except Exception:
        # Fallback to Literal type if dynamic loading fails
        pass

    # Fallback to static Literal type for type checking context
    fallback_agents: tuple[str, ...] = get_args(AgentIdentity)
    return agent_name in fallback_agents


def get_all_agents() -> list[str]:
    """
    Get list of all valid agent identifiers.

    This function dynamically loads agent names from doctrine/agents
    to ensure single source of truth.

    Returns:
        List of agent name strings
    """
    try:
        agents = load_agent_identities()
        if agents:
            return agents
    except Exception:
        # Fallback to Literal type if dynamic loading fails
        pass

    # Fallback to static Literal type
    return list(get_args(AgentIdentity))
