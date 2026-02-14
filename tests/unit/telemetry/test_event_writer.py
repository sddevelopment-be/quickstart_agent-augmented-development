"""
Unit tests for JSONL EventWriter (ADR-047).

Validates append-only write with fsync, file rotation, crash-safety
(corrupt line handling), concurrent writes, and read roundtrip.
"""

import json
import threading
import pytest
from pathlib import Path

from llm_service.telemetry.event_schema import Event, EventType
from llm_service.telemetry.event_writer import EventWriter


@pytest.fixture
def jsonl_path(tmp_path):
    """Temporary JSONL file path."""
    return tmp_path / "events.jsonl"


@pytest.fixture
def writer(jsonl_path):
    """EventWriter with no rotation."""
    return EventWriter(jsonl_path)


def _make_event(event_type=EventType.TASK_STARTED, **kwargs):
    """Helper to create test events."""
    return Event(event=event_type, **kwargs)


class TestEventWriterBasic:
    """Core write and read operations."""

    def test_emit_creates_file(self, writer, jsonl_path):
        writer.emit(_make_event())
        assert jsonl_path.exists()

    def test_emit_writes_one_line_per_event(self, writer, jsonl_path):
        writer.emit(_make_event())
        writer.emit(_make_event(EventType.TASK_COMPLETED))
        lines = jsonl_path.read_text().strip().split("\n")
        assert len(lines) == 2

    def test_each_line_is_valid_json(self, writer, jsonl_path):
        writer.emit(_make_event(task_id="t-1"))
        writer.emit(_make_event(EventType.COST_UPDATE, task_id="t-2"))
        for line in jsonl_path.read_text().strip().split("\n"):
            parsed = json.loads(line)
            assert "event" in parsed

    def test_read_events_roundtrip(self, writer):
        events = [
            _make_event(task_id="t-1", agent_role="pedro"),
            _make_event(EventType.EXECUTION_START, tool="claude-code"),
            _make_event(EventType.TASK_COMPLETED, summary="done"),
        ]
        for e in events:
            writer.emit(e)
        read = writer.read_events()
        assert len(read) == 3
        assert read[0].task_id == "t-1"
        assert read[1].tool == "claude-code"
        assert read[2].summary == "done"

    def test_read_events_empty_file(self, writer, jsonl_path):
        jsonl_path.touch()
        assert writer.read_events() == []

    def test_read_events_nonexistent_file(self, writer):
        assert writer.read_events() == []

    def test_append_only(self, writer, jsonl_path):
        writer.emit(_make_event(task_id="first"))
        writer.emit(_make_event(task_id="second"))
        lines = jsonl_path.read_text().strip().split("\n")
        assert json.loads(lines[0])["task_id"] == "first"
        assert json.loads(lines[1])["task_id"] == "second"

    def test_parent_directory_created(self, tmp_path):
        deep_path = tmp_path / "a" / "b" / "c" / "events.jsonl"
        w = EventWriter(deep_path)
        w.emit(_make_event())
        assert deep_path.exists()


class TestEventWriterCrashSafety:
    """Crash-safety: corrupt/incomplete lines are skipped on read."""

    def test_corrupt_line_skipped(self, writer, jsonl_path):
        writer.emit(_make_event(task_id="valid-1"))
        # Inject corrupt line
        with open(jsonl_path, "a") as f:
            f.write("{invalid json\n")
        writer.emit(_make_event(task_id="valid-2"))
        events = writer.read_events()
        assert len(events) == 2
        assert events[0].task_id == "valid-1"
        assert events[1].task_id == "valid-2"

    def test_incomplete_line_skipped(self, writer, jsonl_path):
        writer.emit(_make_event(task_id="good"))
        # Simulate crash mid-write: partial JSON without newline
        with open(jsonl_path, "a") as f:
            f.write('{"event":"task_sta')
        events = writer.read_events()
        assert len(events) == 1
        assert events[0].task_id == "good"

    def test_blank_lines_skipped(self, writer, jsonl_path):
        writer.emit(_make_event())
        with open(jsonl_path, "a") as f:
            f.write("\n\n\n")
        writer.emit(_make_event())
        events = writer.read_events()
        assert len(events) == 2


class TestEventWriterRotation:
    """File rotation when max_size_bytes is exceeded."""

    def test_rotation_creates_backup(self, jsonl_path):
        w = EventWriter(jsonl_path, max_size_bytes=500)
        # Write enough to exceed 500 bytes (each event ~200 bytes)
        for i in range(5):
            w.emit(_make_event(task_id=f"task-{i}", summary="x" * 50))
        rotated = jsonl_path.with_suffix(".jsonl.1")
        assert rotated.exists(), "Rotated file should exist"
        assert jsonl_path.exists(), "New file should exist after rotation"

    def test_rotation_preserves_recent_data(self, jsonl_path):
        w = EventWriter(jsonl_path, max_size_bytes=500)
        for i in range(5):
            w.emit(_make_event(task_id=f"task-{i}", summary="x" * 50))
        # Current file + one rotated backup contain recent data
        rotated = jsonl_path.with_suffix(".jsonl.1")
        total_lines = 0
        for p in [jsonl_path, rotated]:
            if p.exists():
                total_lines += len([l for l in p.read_text().strip().split("\n") if l])
        assert total_lines >= 2, "At least current + rotated data should exist"

    def test_no_rotation_when_disabled(self, jsonl_path):
        w = EventWriter(jsonl_path, max_size_bytes=None)
        for i in range(20):
            w.emit(_make_event(task_id=f"task-{i}", summary="x" * 100))
        rotated = jsonl_path.with_suffix(".jsonl.1")
        assert not rotated.exists()

    def test_no_rotation_under_limit(self, jsonl_path):
        w = EventWriter(jsonl_path, max_size_bytes=100_000)
        for i in range(5):
            w.emit(_make_event(task_id=f"task-{i}"))
        rotated = jsonl_path.with_suffix(".jsonl.1")
        assert not rotated.exists()
        events = w.read_events()
        assert len(events) == 5


class TestEventWriterConcurrency:
    """Thread-safety under concurrent writes."""

    def test_concurrent_writes(self, jsonl_path):
        w = EventWriter(jsonl_path)
        errors = []

        def write_events(start):
            try:
                for i in range(20):
                    w.emit(_make_event(task_id=f"thread-{start}-{i}"))
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=write_events, args=(t,)) for t in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Concurrent write errors: {errors}"
        events = w.read_events()
        assert len(events) == 100  # 5 threads × 20 events


class TestEventWriterCompatibility:
    """Compatibility with existing telemetry (no breaking changes)."""

    def test_does_not_affect_sqlite_telemetry(self, tmp_path):
        """EventWriter operates on JSONL; SQLite logger is independent."""
        from llm_service.telemetry.logger import TelemetryLogger
        db_path = tmp_path / "telemetry.db"
        jsonl_path = tmp_path / "events.jsonl"

        logger = TelemetryLogger(db_path)
        writer = EventWriter(jsonl_path)

        writer.emit(_make_event(task_id="from-writer"))
        # SQLite logger should still work independently
        stats = logger.get_statistics()
        assert stats["total_invocations"] == 0  # No cross-contamination
