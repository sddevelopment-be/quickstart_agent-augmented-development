"""
Unit tests for JSONL event schema (ADR-047).

Validates EventType enum, Event dataclass immutability,
JSON serialization roundtrip, and schema conformance.
"""

import json
import pytest
from datetime import datetime, timezone

from llm_service.telemetry.event_schema import Event, EventType


class TestEventType:
    """EventType enum covers all ADR-047 lifecycle + execution events."""

    def test_lifecycle_events_exist(self):
        assert EventType.TASK_STARTED == "task_started"
        assert EventType.TASK_COMPLETED == "task_completed"
        assert EventType.TASK_FAILED == "task_failed"

    def test_execution_events_exist(self):
        assert EventType.EXECUTION_START == "execution_start"
        assert EventType.EXECUTION_COMPLETE == "execution_complete"
        assert EventType.COST_UPDATE == "cost_update"

    def test_enum_has_six_members(self):
        assert len(EventType) == 6

    def test_string_value_roundtrip(self):
        for et in EventType:
            assert EventType(et.value) is et


class TestEvent:
    """Event dataclass conforms to ADR-047 JSONL schema."""

    def test_minimal_event(self):
        event = Event(event=EventType.TASK_STARTED)
        assert event.event is EventType.TASK_STARTED
        assert event.ts is not None
        assert event.event_id is not None

    def test_full_event(self):
        event = Event(
            event=EventType.TASK_COMPLETED,
            ts="2026-02-14T10:00:00+00:00",
            run_id="RUN-20260214-001",
            task_id="2026-02-14T1000-test",
            phase="implementation",
            agent_role="python-pedro",
            tool="claude-code",
            mode="batch",
            status="completed",
            log_paths={"stdout": "runs/RUN-20260214-001/stdout.log"},
            summary="Test completed",
            event_id="test-uuid-123",
        )
        assert event.run_id == "RUN-20260214-001"
        assert event.log_paths["stdout"] == "runs/RUN-20260214-001/stdout.log"

    def test_event_is_frozen(self):
        event = Event(event=EventType.TASK_STARTED)
        with pytest.raises(AttributeError):
            event.status = "changed"

    def test_to_json_produces_single_line(self):
        event = Event(event=EventType.TASK_STARTED, summary="hello")
        json_line = event.to_json()
        assert "\n" not in json_line

    def test_to_json_is_valid_json(self):
        event = Event(
            event=EventType.EXECUTION_START,
            task_id="t-1",
            agent_role="backend-dev",
        )
        parsed = json.loads(event.to_json())
        assert parsed["event"] == "execution_start"
        assert parsed["task_id"] == "t-1"

    def test_to_json_omits_none_values(self):
        event = Event(event=EventType.COST_UPDATE)
        parsed = json.loads(event.to_json())
        assert "run_id" not in parsed
        assert "tool" not in parsed

    def test_from_json_roundtrip(self):
        original = Event(
            event=EventType.TASK_FAILED,
            run_id="RUN-1",
            task_id="t-1",
            phase="testing",
            agent_role="python-pedro",
            tool="codex",
            mode="interactive",
            status="failed",
            summary="Test failure",
        )
        json_line = original.to_json()
        restored = Event.from_json(json_line)
        assert restored.event is EventType.TASK_FAILED
        assert restored.run_id == original.run_id
        assert restored.task_id == original.task_id
        assert restored.summary == original.summary
        assert restored.event_id == original.event_id

    def test_from_json_with_log_paths(self):
        event = Event(
            event=EventType.EXECUTION_COMPLETE,
            log_paths={"stdout": "/tmp/out.log", "stderr": "/tmp/err.log"},
        )
        restored = Event.from_json(event.to_json())
        assert restored.log_paths == {"stdout": "/tmp/out.log", "stderr": "/tmp/err.log"}

    def test_unique_event_ids(self):
        e1 = Event(event=EventType.TASK_STARTED)
        e2 = Event(event=EventType.TASK_STARTED)
        assert e1.event_id != e2.event_id

    def test_ts_is_iso_format(self):
        event = Event(event=EventType.TASK_STARTED)
        # Should parse as ISO 8601
        datetime.fromisoformat(event.ts)
