#!/usr/bin/env python3
"""
Unit Tests for task_age_checker.py

Tests task age detection functionality:
- Age calculation from created_at timestamps
- Stale task detection with configurable thresholds
- Multi-state task checking
- Text and JSON output formatting
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

# Imports (path configured in conftest.py)
from framework.orchestration.task_age_checker import TaskAgeChecker

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def temp_work_dir(tmp_path: Path) -> Path:
    """Create isolated test work directory structure."""
    work_dir = tmp_path / "work"
    collab_dir = work_dir / "collaboration"

    # Create standard directory structure
    for state_dir in ["inbox", "new", "assigned", "in_progress", "done"]:
        (collab_dir / state_dir).mkdir(parents=True)

    return work_dir


def create_task_with_age(
    directory: Path, task_id: str, age_hours: float, agent: str = "test-agent"
) -> Path:
    """
    Helper to create a task YAML file with specific age.

    Args:
        directory: Directory to create task in
        task_id: Task identifier
        age_hours: Age in hours (negative for future, positive for past)
        agent: Agent name

    Returns:
        Path to created task file
    """
    created_at = datetime.now(timezone.utc) - timedelta(hours=age_hours)

    task = {
        "id": task_id,
        "agent": agent,
        "status": "new",
        "title": f"Test task aged {age_hours}h",
        "artefacts": ["test/output/sample.md"],
        "created_at": created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created_by": "test-harness",
    }

    task_file = directory / f"{task_id}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task, f, default_flow_style=False, sort_keys=False)

    return task_file


# ============================================================================
# Age Calculation Tests
# ============================================================================


def test_get_task_age_hours_recent(temp_work_dir: Path) -> None:
    """Test age calculation for recent task (< 1 hour)."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir)
    created_at = datetime.now(timezone.utc) - timedelta(minutes=30)
    task_data = {"created_at": created_at.strftime("%Y-%m-%dT%H:%M:%SZ")}

    # Act
    age_hours = checker.get_task_age_hours(task_data)

    # Assert
    assert age_hours is not None
    assert 0.4 < age_hours < 0.6  # ~30 minutes


def test_get_task_age_hours_old(temp_work_dir: Path) -> None:
    """Test age calculation for old task (> 24 hours)."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir)
    created_at = datetime.now(timezone.utc) - timedelta(hours=30)
    task_data = {"created_at": created_at.strftime("%Y-%m-%dT%H:%M:%SZ")}

    # Act
    age_hours = checker.get_task_age_hours(task_data)

    # Assert
    assert age_hours is not None
    assert 29.5 < age_hours < 30.5  # ~30 hours


def test_get_task_age_hours_missing_created_at(temp_work_dir: Path) -> None:
    """Test age calculation with missing created_at field."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir)
    task_data = {"id": "test-task"}

    # Act
    age_hours = checker.get_task_age_hours(task_data)

    # Assert
    assert age_hours is None


def test_get_task_age_hours_invalid_timestamp(temp_work_dir: Path) -> None:
    """Test age calculation with invalid timestamp format."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir)
    task_data = {"created_at": "not-a-valid-timestamp"}

    # Act
    age_hours = checker.get_task_age_hours(task_data)

    # Assert
    assert age_hours is None


# ============================================================================
# Task File Checking Tests
# ============================================================================


def test_check_task_file_recent(temp_work_dir: Path) -> None:
    """Test checking a recent task (should not be flagged)."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"
    task_file = create_task_with_age(
        inbox_dir, "2025-11-30T1200-test-recent-task", 2.0
    )

    # Act
    result = checker.check_task_file(task_file)

    # Assert
    assert result is None  # Not stale


def test_check_task_file_stale(temp_work_dir: Path) -> None:
    """Test checking a stale task (should be flagged)."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"
    task_file = create_task_with_age(inbox_dir, "2025-11-30T1200-test-stale-task", 30.0)

    # Act
    result = checker.check_task_file(task_file)

    # Assert
    assert result is not None
    assert result["id"] == "2025-11-30T1200-test-stale-task"
    assert result["agent"] == "test-agent"
    assert result["age_hours"] > 24


def test_check_task_file_at_threshold(temp_work_dir: Path) -> None:
    """Test checking a task exactly at threshold (should be flagged)."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"
    task_file = create_task_with_age(
        inbox_dir, "2025-11-30T1200-test-threshold-task", 24.0
    )

    # Act
    result = checker.check_task_file(task_file)

    # Assert
    assert result is not None  # Should be flagged at threshold


# ============================================================================
# Multi-Task Checking Tests
# ============================================================================


def test_check_all_tasks_empty(temp_work_dir: Path) -> None:
    """Test checking with no tasks."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)

    # Act
    stale_tasks = checker.check_all_tasks()

    # Assert
    assert len(stale_tasks) == 0


def test_check_all_tasks_no_stale(temp_work_dir: Path) -> None:
    """Test checking with only recent tasks."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"

    # Create recent tasks
    for i in range(3):
        create_task_with_age(inbox_dir, f"2025-11-30T120{i}-recent-task-{i}", 2.0)

    # Act
    stale_tasks = checker.check_all_tasks()

    # Assert
    assert len(stale_tasks) == 0


def test_check_all_tasks_some_stale(temp_work_dir: Path) -> None:
    """Test checking with mix of recent and stale tasks."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"

    # Create mix of tasks
    create_task_with_age(inbox_dir, "2025-11-30T1201-recent-task", 2.0)
    create_task_with_age(inbox_dir, "2025-11-30T1202-stale-task-1", 30.0)
    create_task_with_age(inbox_dir, "2025-11-30T1203-stale-task-2", 50.0)

    # Act
    stale_tasks = checker.check_all_tasks()

    # Assert
    assert "inbox" in stale_tasks
    assert len(stale_tasks["inbox"]) == 2


def test_check_all_tasks_multiple_states(temp_work_dir: Path) -> None:
    """Test checking tasks across multiple states."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    collab_dir = temp_work_dir / "collaboration"

    # Create stale tasks in different states
    create_task_with_age(collab_dir / "inbox", "2025-11-30T1201-inbox-stale", 30.0)
    create_task_with_age(collab_dir / "new", "2025-11-30T1202-new-stale", 35.0)

    # Create agent subdirectory for assigned
    (collab_dir / "assigned" / "test-agent").mkdir(parents=True)
    create_task_with_age(
        collab_dir / "assigned" / "test-agent",
        "2025-11-30T1203-assigned-stale",
        40.0,
    )

    # Act
    stale_tasks = checker.check_all_tasks()

    # Assert
    assert "inbox" in stale_tasks
    assert "new" in stale_tasks
    assert "assigned" in stale_tasks
    assert len(stale_tasks["inbox"]) == 1
    assert len(stale_tasks["new"]) == 1
    assert len(stale_tasks["assigned"]) == 1


def test_check_all_tasks_done_not_checked(temp_work_dir: Path) -> None:
    """Test that done tasks are not checked (expected to be old)."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    done_dir = temp_work_dir / "collaboration" / "done"
    (done_dir / "test-agent").mkdir(parents=True)

    # Create old done task
    create_task_with_age(
        done_dir / "test-agent", "2025-11-30T1201-done-old", 100.0
    )

    # Act
    stale_tasks = checker.check_all_tasks()

    # Assert
    assert "done" not in stale_tasks  # Done tasks not checked


# ============================================================================
# Custom Threshold Tests
# ============================================================================


def test_custom_threshold_12_hours(temp_work_dir: Path) -> None:
    """Test with custom 12-hour threshold."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=12)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"

    create_task_with_age(inbox_dir, "2025-11-30T1201-task-10h", 10.0)  # Not stale
    create_task_with_age(inbox_dir, "2025-11-30T1202-task-15h", 15.0)  # Stale

    # Act
    stale_tasks = checker.check_all_tasks()

    # Assert
    assert "inbox" in stale_tasks
    assert len(stale_tasks["inbox"]) == 1
    assert stale_tasks["inbox"][0]["id"] == "2025-11-30T1202-task-15h"


def test_custom_threshold_48_hours(temp_work_dir: Path) -> None:
    """Test with custom 48-hour threshold."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=48)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"

    create_task_with_age(inbox_dir, "2025-11-30T1201-task-30h", 30.0)  # Not stale
    create_task_with_age(inbox_dir, "2025-11-30T1202-task-50h", 50.0)  # Stale

    # Act
    stale_tasks = checker.check_all_tasks()

    # Assert
    assert "inbox" in stale_tasks
    assert len(stale_tasks["inbox"]) == 1
    assert stale_tasks["inbox"][0]["id"] == "2025-11-30T1202-task-50h"


# ============================================================================
# Output Formatting Tests
# ============================================================================


def test_format_text_no_stale(temp_work_dir: Path) -> None:
    """Test text formatting with no stale tasks."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    stale_tasks = {}

    # Act
    output = checker.format_text(stale_tasks)

    # Assert
    assert "Task Age Warning Report" in output
    assert "No stale tasks found" in output


def test_format_text_with_stale(temp_work_dir: Path) -> None:
    """Test text formatting with stale tasks."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"
    create_task_with_age(inbox_dir, "2025-11-30T1201-stale-task", 30.0)

    stale_tasks = checker.check_all_tasks()

    # Act
    output = checker.format_text(stale_tasks)

    # Assert
    assert "Task Age Warning Report" in output
    assert "Found 1 stale task" in output
    assert "inbox" in output
    assert "2025-11-30T1201-stale-task" in output


def test_format_json_no_stale(temp_work_dir: Path) -> None:
    """Test JSON formatting with no stale tasks."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    stale_tasks = {}

    # Act
    output = checker.format_json(stale_tasks)

    # Assert
    parsed = json.loads(output)
    assert parsed["total_stale_tasks"] == 0
    assert parsed["has_warnings"] is False
    assert parsed["threshold_hours"] == 24


def test_format_json_with_stale(temp_work_dir: Path) -> None:
    """Test JSON formatting with stale tasks."""
    # Arrange
    checker = TaskAgeChecker(temp_work_dir, age_threshold_hours=24)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"
    create_task_with_age(inbox_dir, "2025-11-30T1201-stale-task", 30.0)

    stale_tasks = checker.check_all_tasks()

    # Act
    output = checker.format_json(stale_tasks)

    # Assert
    parsed = json.loads(output)
    assert parsed["total_stale_tasks"] == 1
    assert parsed["has_warnings"] is True
    assert "inbox" in parsed["stale_by_state"]
    assert len(parsed["stale_by_state"]["inbox"]) == 1
