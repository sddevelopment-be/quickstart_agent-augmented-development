"""Task status lifecycle enumeration.

References:
    - docs/architecture/adrs/ADR-003-task-lifecycle-state-management.md
"""

from enum import Enum


class TaskStatus(Enum):
    """Task lifecycle states per ADR-003."""

    INBOX = "inbox"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"
