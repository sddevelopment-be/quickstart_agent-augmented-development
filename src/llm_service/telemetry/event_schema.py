"""
Event schema for JSONL telemetry (ADR-047).

Defines lifecycle and execution event types and the Event dataclass
for the append-only JSONL telemetry store.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
import json
import uuid


class EventType(str, Enum):
    """Lifecycle and execution event types per ADR-047."""

    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    EXECUTION_START = "execution_start"
    EXECUTION_COMPLETE = "execution_complete"
    COST_UPDATE = "cost_update"


@dataclass(frozen=True)
class Event:
    """
    Immutable telemetry event per ADR-047 schema.

    Fields match the JSONL schema defined in the Local Agent Control Plane
    technical design document.
    """

    event: EventType
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    run_id: Optional[str] = None
    task_id: Optional[str] = None
    phase: Optional[str] = None
    agent_role: Optional[str] = None
    tool: Optional[str] = None
    mode: Optional[str] = None
    status: Optional[str] = None
    log_paths: Optional[dict] = None
    summary: Optional[str] = None
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_json(self) -> str:
        """Serialize to a single JSON line (no newlines in output)."""
        data = asdict(self)
        data["event"] = self.event.value
        # Remove None values for compact output
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, separators=(",", ":"))

    @classmethod
    def from_json(cls, line: str) -> "Event":
        """Deserialize from a JSON line."""
        data = json.loads(line)
        data["event"] = EventType(data["event"])
        return cls(**data)
