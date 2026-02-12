"""
Collaboration Bounded Context.

This module contains domain models for agent orchestration, task management,
batch execution, and iteration coordination.

Domain: Multi-agent collaboration and coordination

Key Concepts
------------
Task
    A unit of work to be executed by an agent, with status tracking and
    lifecycle management.

TaskDescriptor
    Metadata describing a task, including assignment, priority, dependencies,
    and acceptance criteria.

TaskStatus
    State of a task in its lifecycle (assigned, in_progress, completed, blocked).

AgentIdentity
    Identification and profile information for agents participating in
    collaboration workflows.

Batch
    A collection of related tasks executed together as a logical unit of work.

Iteration
    A time-boxed period of work containing one or more batches.

Orchestrator
    Coordination logic for managing task assignment, execution, and handoffs
    between agents.

Related ADRs
------------
- ADR-046: Domain Module Refactoring
- ADR-042: Shared Task Domain Model

Examples
--------
>>> # Future usage after Task 2 (file migration)
>>> # from src.domain.collaboration import Task, TaskStatus
>>> # task = Task(id="T001", status=TaskStatus.ASSIGNED)
"""

from .task_schema import (
    TaskIOError,
    TaskSchemaError,
    TaskValidationError,
    load_task_safe,
    read_task,
    write_task,
)
from .task_validator import validate_task
from .types import TaskMode, TaskPriority, TaskStatus

__all__ = [
    # Task schema I/O
    "read_task",
    "write_task",
    "load_task_safe",
    # Task validation
    "validate_task",
    # Types and enums
    "TaskStatus",
    "TaskMode",
    "TaskPriority",
    # Exceptions
    "TaskSchemaError",
    "TaskIOError",
    "TaskValidationError",
]
