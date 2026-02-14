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

from .logger import InvocationRecord, TelemetryLogger
from .event_schema import Event, EventType
from .event_writer import EventWriter

__all__ = [
    "TelemetryLogger",
    "InvocationRecord",
    "Event",
    "EventType",
    "EventWriter",
]
