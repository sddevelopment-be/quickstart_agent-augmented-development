#!/usr/bin/env python3
"""
Unit Tests for task_utils.py Module

Tests core task utility functions for:
- Reading task YAML files
- Writing task YAML files
- Logging events with timestamps
- Generating UTC timestamps
- Updating task status
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

# Add paths to import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from common.task_schema import TaskIOError, TaskValidationError, read_task
from framework.orchestration.task_utils import (
    get_utc_timestamp,
    log_event,
    update_task_status,
    write_task,
)

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def temp_task_dir(tmp_path: Path) -> Path:
    """Create isolated test directory for task files."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    return task_dir


@pytest.fixture
def sample_task() -> dict:
    """Create sample task dictionary."""
    return {
        "id": "2025-11-28T2000-test-agent-sample-task",
        "agent": "test-agent",
        "status": "new",
        "title": "Sample test task",
        "artefacts": ["test/output/sample.md"],
        "created_at": "2025-11-28T20:00:00Z",
        "created_by": "test-harness",
    }


# ============================================================================
# read_task Tests
# ============================================================================


def test_read_task_valid_file(temp_task_dir: Path, sample_task: dict) -> None:
    """Test reading a valid task YAML file."""
    # Arrange
    task_file = temp_task_dir / "task.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(sample_task, f, default_flow_style=False, sort_keys=False)

    # Assumption Check
    assert task_file.exists(), "Test precondition failed: file should exist"
    assert task_file.exists(), "Test precondition failed: task file should exist"

    # Act
    result = read_task(task_file)

    # Assert
    assert result == sample_task
    assert result["id"] == "2025-11-28T2000-test-agent-sample-task"
    assert result["agent"] == "test-agent"
    assert result["status"] == "new"


def test_read_task_empty_file(temp_task_dir: Path) -> None:
    """Test reading an empty YAML file returns empty dict."""
    # Arrange
    task_file = temp_task_dir / "empty.yaml"
    task_file.write_text("")

    # Assumption Check
    assert task_file.exists(), "Test precondition failed: file should exist"
    assert (
        task_file.stat().st_size == 0
    ), "Test precondition failed: file should be empty"

    # Act & Assert
    with pytest.raises(TaskValidationError, match="Task must be a dictionary"):
        read_task(task_file)


def test_read_task_missing_file(temp_task_dir: Path) -> None:
    """Test reading a non-existent file raises TaskIOError."""
    # Arrange
    task_file = temp_task_dir / "missing.yaml"

    # Assumption Check
    assert not task_file.exists(), "Test precondition failed: file should NOT exist"

    # Act & Assert
    with pytest.raises(TaskIOError, match="Task file not found"):
        read_task(task_file)


def test_read_task_preserves_structure(temp_task_dir: Path) -> None:
    """Test reading preserves nested structure and data types."""
    # Arrange
    complex_task = {
        "id": "test-complex",
        "agent": "test-agent",
        "status": "done",
        "result": {
            "summary": "Task completed",
            "artefacts": ["file1.md", "file2.md"],
            "next_agent": "test-agent-2",
        },
        "context": {
            "notes": ["Note 1", "Note 2"],
            "priority": "high",
        },
    }
    task_file = temp_task_dir / "complex.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(complex_task, f, default_flow_style=False, sort_keys=False)

    # Assumption Check
    assert task_file.exists(), "Test precondition failed: file should exist"
    # Act
    result = read_task(task_file)

    # Assert
    assert result["result"]["next_agent"] == "test-agent-2"
    assert len(result["result"]["artefacts"]) == 2
    assert result["context"]["notes"] == ["Note 1", "Note 2"]


# ============================================================================
# write_task Tests
# ============================================================================


def test_write_task_creates_file(temp_task_dir: Path, sample_task: dict) -> None:
    """Test writing task creates file with correct content."""

    # Act
    task_file = temp_task_dir / "output.yaml"
    write_task(task_file, sample_task)

    assert task_file.exists()

    with open(task_file, encoding="utf-8") as f:
        result = yaml.safe_load(f)

    assert result == sample_task

    # Arrange


def test_write_task_creates_parent_dirs(tmp_path: Path, sample_task: dict) -> None:
    """Test writing task creates parent directories if missing."""
    # Arrange
    task_file = tmp_path / "nested" / "dirs" / "task.yaml"

    # Assumption Check
    assert not task_file.exists(), "Test precondition failed: file should NOT exist"
    assert (
        not task_file.parent.exists()
    ), "Test precondition failed: parent dir should NOT exist"

    # Act
    write_task(task_file, sample_task)

    # Assert
    assert task_file.exists()
    assert task_file.parent.exists()


def test_write_task_overwrites_existing(temp_task_dir: Path, sample_task: dict) -> None:
    """Test writing task overwrites existing file."""

    # Act
    task_file = temp_task_dir / "overwrite.yaml"
    # Write initial task
    initial_task = sample_task.copy()
    initial_task["status"] = "assigned"
    write_task(task_file, initial_task)

    # Overwrite with updated task
    updated_task = sample_task.copy()
    updated_task["status"] = "done"
    write_task(task_file, updated_task)

    result = read_task(task_file)
    assert result["status"] == "done"

    # Arrange


def test_write_task_preserves_order(temp_task_dir: Path) -> None:
    """Test writing task preserves field order (no sort)."""

    # Act
    task_file = temp_task_dir / "order.yaml"
    ordered_task = {
        "id": "test-id",
        "agent": "test-agent",
        "status": "new",
        "title": "Test title",
        "artefacts": ["test.md"],
    }
    write_task(task_file, ordered_task)

    # Read raw YAML to check order
    content = task_file.read_text()
    lines = [line.split(":")[0].strip() for line in content.split("\n") if ":" in line]

    # Verify id comes before agent, status, etc.
    assert lines.index("id") < lines.index("agent")
    assert lines.index("agent") < lines.index("status")
    assert lines.index("status") < lines.index("title")


# ============================================================================
# log_event Tests
# ============================================================================


def test_log_event_creates_file(temp_task_dir: Path) -> None:
    """Test logging event creates log file."""

    # Act
    log_file = temp_task_dir / "test.log"
    log_event("Test message", log_file)

    assert log_file.exists()

    # Arrange


def test_log_event_appends_message(temp_task_dir: Path) -> None:
    """Test logging event appends message with timestamp."""

    # Act
    log_file = temp_task_dir / "test.log"
    log_event("First message", log_file)
    log_event("Second message", log_file)

    content = log_file.read_text()
    assert "First message" in content
    assert "Second message" in content

    # Arrange


def test_log_event_includes_timestamp(temp_task_dir: Path) -> None:
    """Test logging event includes UTC timestamp."""

    # Act
    log_file = temp_task_dir / "test.log"
    message = "Test event"
    log_event(message, log_file)

    content = log_file.read_text()
    assert message in content
    assert "UTC" in content
    # Check timestamp format (YYYY-MM-DD HH:MM:SS UTC)
    assert "-" in content and ":" in content

    # Arrange


def test_log_event_creates_parent_dirs(tmp_path: Path) -> None:
    """Test logging event creates parent directories if missing."""
    # Arrange
    log_file = tmp_path / "nested" / "logs" / "test.log"

    # Assumption Check
    assert not log_file.exists(), "Test precondition failed: log file should NOT exist"
    assert (
        not log_file.parent.exists()
    ), "Test precondition failed: parent dir should NOT exist"

    # Act
    log_event("Test message", log_file)

    # Assert
    assert log_file.exists()
    assert log_file.parent.exists()


def test_log_event_multiple_entries(temp_task_dir: Path) -> None:
    """Test logging multiple events maintains separate entries."""

    # Act
    log_file = temp_task_dir / "test.log"
    log_event("Event 1", log_file)
    log_event("Event 2", log_file)
    log_event("Event 3", log_file)

    content = log_file.read_text()
    # Each event should have its own timestamp
    assert content.count("UTC") == 3
    assert content.count("Event") == 3


# ============================================================================
# get_utc_timestamp Tests
# ============================================================================


def test_get_utc_timestamp_format() -> None:
    """Test UTC timestamp format matches ISO8601 with Z suffix."""

    # Act
    timestamp = get_utc_timestamp()
    # Should match format: YYYY-MM-DDTHH:MM:SS.ffffffZ
    assert timestamp.endswith("Z")
    assert "T" in timestamp
    assert timestamp.count("-") >= 2  # Date separators
    assert timestamp.count(":") >= 2  # Time separators

    # Arrange


def test_get_utc_timestamp_parseable() -> None:
    """Test UTC timestamp is parseable by datetime."""

    # Act
    timestamp = get_utc_timestamp()
    # Should parse without error
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    assert dt.tzinfo is not None

    # Arrange


def test_get_utc_timestamp_current() -> None:
    """Test UTC timestamp represents current time."""

    # Act
    before = datetime.now(timezone.utc)
    timestamp = get_utc_timestamp()
    after = datetime.now(timezone.utc)
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    # Timestamp should be between before and after
    assert before <= dt <= after

    # Arrange


def test_get_utc_timestamp_unique() -> None:
    """Test multiple calls produce different timestamps."""

    # Act
    timestamps = [get_utc_timestamp() for _ in range(3)]
    # At least some should be different (unless running extremely fast)
    # We just verify they're all valid timestamps
    for ts in timestamps:
        assert ts.endswith("Z")
        assert "T" in ts


# ============================================================================
# update_task_status Tests
# ============================================================================


def test_update_task_status_basic() -> None:
    """Test updating task status without timestamp."""

    # Act
    task = {
        "id": "test-id",
        "agent": "test-agent",
        "status": "new",
    }
    result = update_task_status(task, "assigned")

    assert result["status"] == "assigned"
    assert result["id"] == "test-id"  # Other fields preserved

    # Arrange


def test_update_task_status_with_timestamp() -> None:
    """Test updating task status adds timestamp field."""

    # Act
    task = {
        "id": "test-id",
        "agent": "test-agent",
        "status": "new",
    }
    result = update_task_status(task, "assigned", "assigned_at")

    assert result["status"] == "assigned"
    assert "assigned_at" in result
    assert result["assigned_at"].endswith("Z")

    # Arrange


def test_update_task_status_preserves_fields() -> None:
    """Test updating status preserves other task fields."""

    # Act
    task = {
        "id": "test-id",
        "agent": "test-agent",
        "status": "assigned",
        "title": "Test task",
        "artefacts": ["test.md"],
        "context": {"note": "Important"},
    }
    result = update_task_status(task, "in_progress", "started_at")

    assert result["status"] == "in_progress"
    assert result["agent"] == "test-agent"
    assert result["title"] == "Test task"
    assert result["artefacts"] == ["test.md"]
    assert result["context"]["note"] == "Important"
    assert "started_at" in result

    # Arrange


def test_update_task_status_overwrites() -> None:
    """Test updating status overwrites previous status."""

    # Act
    task = {
        "id": "test-id",
        "agent": "test-agent",
        "status": "assigned",
        "assigned_at": "2025-11-28T10:00:00Z",
    }
    result = update_task_status(task, "in_progress", "started_at")

    assert result["status"] == "in_progress"
    assert "assigned_at" in result  # Old timestamp preserved
    assert "started_at" in result  # New timestamp added

    # Arrange


def test_update_task_status_modifies_original() -> None:
    """Test update_task_status modifies original dict reference."""

    # Act
    task = {
        "id": "test-id",
        "agent": "test-agent",
        "status": "new",
    }
    result = update_task_status(task, "assigned")

    # Should return same object (modified in place)
    assert result is task
    assert task["status"] == "assigned"


# ============================================================================
# Integration Tests
# ============================================================================


def test_read_write_roundtrip(temp_task_dir: Path, sample_task: dict) -> None:
    """Test writing then reading task preserves data."""

    # Act
    task_file = temp_task_dir / "roundtrip.yaml"
    write_task(task_file, sample_task)
    result = read_task(task_file)

    assert result == sample_task

    # Arrange


def test_task_workflow_simulation(temp_task_dir: Path) -> None:
    """Test simulating complete task lifecycle with utilities."""

    # Act
    task_file = temp_task_dir / "workflow.yaml"
    log_file = temp_task_dir / "workflow.log"
    # Create new task
    task = {
        "id": "2025-11-28T2000-test-workflow",
        "agent": "test-agent",
        "status": "new",
        "title": "Test workflow",
        "artefacts": ["test.md"],
        "created_at": get_utc_timestamp(),
    }
    write_task(task_file, task)
    log_event("Task created", log_file)

    # Assign task
    task = read_task(task_file)
    task = update_task_status(task, "assigned", "assigned_at")
    write_task(task_file, task)
    log_event("Task assigned", log_file)

    # Start task
    task = read_task(task_file)
    task = update_task_status(task, "in_progress", "started_at")
    write_task(task_file, task)
    log_event("Task started", log_file)

    # Complete task
    task = read_task(task_file)
    task = update_task_status(task, "done", "completed_at")
    task["result"] = {"summary": "Task completed successfully"}
    write_task(task_file, task)
    log_event("Task completed", log_file)

    # Verify final state
    final_task = read_task(task_file)
    assert final_task["status"] == "done"
    assert "assigned_at" in final_task
    assert "started_at" in final_task
    assert "completed_at" in final_task
    assert final_task["result"]["summary"] == "Task completed successfully"

    # Verify log
    log_content = log_file.read_text()
    assert "Task created" in log_content
    assert "Task assigned" in log_content
    assert "Task started" in log_content
    assert "Task completed" in log_content


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
