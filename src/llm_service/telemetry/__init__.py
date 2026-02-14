"""
Telemetry module for LLM Service Layer.

Provides cost tracking, performance monitoring, and invocation logging
for all LLM service requests.

Key Components:
- TelemetryLogger: Main logging interface (SQLite)
- InvocationRecord: Data structure for invocation metadata
- EventWriter: Append-only JSONL event writer (ADR-047)
- Event / EventType: JSONL event schema
"""

<<<<<<< HEAD
from .logger import InvocationRecord, TelemetryLogger

__all__ = ["TelemetryLogger", "InvocationRecord"]
=======
from .logger import TelemetryLogger, InvocationRecord
from .event_schema import Event, EventType
from .event_writer import EventWriter

__all__ = [
    'TelemetryLogger',
    'InvocationRecord',
    'Event',
    'EventType',
    'EventWriter',
]
>>>>>>> 67ee06e (python-pedro: M6.1 P1a — Implement JSONL event writer (ADR-047))
