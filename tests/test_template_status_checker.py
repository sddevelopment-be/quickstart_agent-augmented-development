#!/usr/bin/env python3
"""
Unit Tests for template-status-checker.py

Tests template status checker functionality:
- Task counting across different states
- Agent breakdown by directory
- Validation criteria checking
- Text and JSON output formatting
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

# Add framework directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "framework" / "context"))

# Import the module directly
import importlib.util

spec = importlib.util.spec_from_file_location(
    "template_status_checker",
    Path(__file__).parent.parent
    / "src"
    / "framework"
    / "context"
    / "template-status-checker.py",
)
template_status_checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(template_status_checker)
TemplateStatusChecker = template_status_checker.TemplateStatusChecker

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def temp_work_dir(tmp_path: Path) -> Path:
    """Create isolated test work directory structure."""
    work_dir = tmp_path / "work"
    collab_dir = work_dir / "collaboration"

    # Create standard directory structure
    for state_dir in ["inbox", "new", "assigned", "in_progress", "done", "archive"]:
        (collab_dir / state_dir).mkdir(parents=True)

    return work_dir


@pytest.fixture
def sample_task() -> dict:
    """Create sample task dictionary."""
    return {
        "id": "2025-11-30T1200-test-agent-sample-task",
        "agent": "test-agent",
        "status": "new",
        "title": "Sample test task",
        "artefacts": ["test/output/sample.md"],
        "created_at": "2025-11-30T12:00:00Z",
        "created_by": "test-harness",
    }


def create_task_file(directory: Path, task: dict) -> Path:
    """Helper to create a task YAML file."""
    task_file = directory / f"{task['id']}.yaml"
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task, f, default_flow_style=False, sort_keys=False)
    return task_file


# ============================================================================
# Task Counting Tests
# ============================================================================


def test_count_tasks_empty_directory(temp_work_dir: Path) -> None:
    """Test counting tasks in empty directory."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)

    # Act
    count = checker.count_tasks(temp_work_dir / "collaboration" / "inbox")

    # Assert
    assert count == 0


def test_count_tasks_single_task(temp_work_dir: Path, sample_task: dict) -> None:
    """Test counting single task in directory."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"
    create_task_file(inbox_dir, sample_task)

    # Act
    count = checker.count_tasks(inbox_dir)

    # Assert
    assert count == 1


def test_count_tasks_multiple_tasks(temp_work_dir: Path, sample_task: dict) -> None:
    """Test counting multiple tasks in directory."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"

    # Create 3 tasks
    for i in range(3):
        task = sample_task.copy()
        task["id"] = f"2025-11-30T120{i}-test-agent-task-{i}"
        create_task_file(inbox_dir, task)

    # Act
    count = checker.count_tasks(inbox_dir)

    # Assert
    assert count == 3


def test_count_tasks_in_subdirectories(temp_work_dir: Path, sample_task: dict) -> None:
    """Test counting tasks in agent subdirectories (assigned/done)."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    assigned_dir = temp_work_dir / "collaboration" / "assigned"

    # Create agent subdirectories with tasks
    (assigned_dir / "architect").mkdir(parents=True)
    (assigned_dir / "curator").mkdir(parents=True)

    task1 = sample_task.copy()
    task1["id"] = "2025-11-30T1201-architect-task"
    task1["agent"] = "architect"
    create_task_file(assigned_dir / "architect", task1)

    task2 = sample_task.copy()
    task2["id"] = "2025-11-30T1202-curator-task"
    task2["agent"] = "curator"
    create_task_file(assigned_dir / "curator", task2)

    # Act
    count = checker.count_tasks(assigned_dir)

    # Assert
    assert count == 2


# ============================================================================
# Agent Breakdown Tests
# ============================================================================


def test_get_agent_breakdown_empty(temp_work_dir: Path) -> None:
    """Test agent breakdown for empty directory."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    assigned_dir = temp_work_dir / "collaboration" / "assigned"

    # Act
    breakdown = checker.get_agent_breakdown(assigned_dir)

    # Assert
    assert breakdown == {}


def test_get_agent_breakdown_single_agent(
    temp_work_dir: Path, sample_task: dict
) -> None:
    """Test agent breakdown with one agent."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    assigned_dir = temp_work_dir / "collaboration" / "assigned"
    (assigned_dir / "architect").mkdir(parents=True)

    task = sample_task.copy()
    task["id"] = "2025-11-30T1201-architect-task"
    task["agent"] = "architect"
    create_task_file(assigned_dir / "architect", task)

    # Act
    breakdown = checker.get_agent_breakdown(assigned_dir)

    # Assert
    assert breakdown == {"architect": 1}


def test_get_agent_breakdown_multiple_agents(
    temp_work_dir: Path, sample_task: dict
) -> None:
    """Test agent breakdown with multiple agents."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    assigned_dir = temp_work_dir / "collaboration" / "assigned"

    # Create multiple agents with different task counts
    for agent, count in [("architect", 2), ("curator", 3), ("build-automation", 1)]:
        agent_dir = assigned_dir / agent
        agent_dir.mkdir(parents=True)

        for i in range(count):
            task = sample_task.copy()
            task["id"] = f"2025-11-30T120{i}-{agent}-task-{i}"
            task["agent"] = agent
            create_task_file(agent_dir, task)

    # Act
    breakdown = checker.get_agent_breakdown(assigned_dir)

    # Assert
    assert breakdown == {"architect": 2, "curator": 3, "build-automation": 1}


# ============================================================================
# Status Generation Tests
# ============================================================================


def test_generate_status_all_empty(temp_work_dir: Path) -> None:
    """Test status generation with no tasks."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)

    # Act
    status = checker.generate_status()

    # Assert
    assert status["total"] == 0
    assert status["inbox"]["count"] == 0
    assert status["new"]["count"] == 0
    assert status["assigned"]["count"] == 0
    assert status["in_progress"]["count"] == 0
    assert status["done"]["count"] == 0
    assert status["archive"]["count"] == 0


def test_generate_status_with_tasks(temp_work_dir: Path, sample_task: dict) -> None:
    """Test status generation with tasks in different states."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    collab_dir = temp_work_dir / "collaboration"

    # Create tasks in different states
    for state, count in [("inbox", 2), ("assigned", 3), ("done", 5)]:
        state_dir = collab_dir / state
        if state in ["assigned", "done"]:
            # Create agent subdirectory
            (state_dir / "test-agent").mkdir(parents=True)
            state_dir = state_dir / "test-agent"

        for i in range(count):
            task = sample_task.copy()
            task["id"] = f"2025-11-30T120{i}-{state}-task-{i}"
            task["status"] = state
            create_task_file(state_dir, task)

    # Act
    status = checker.generate_status()

    # Assert
    assert status["inbox"]["count"] == 2
    assert status["assigned"]["count"] == 3
    assert status["done"]["count"] == 5
    assert status["total"] == 10


# ============================================================================
# Validation Tests
# ============================================================================


def test_validate_criteria_inbox_empty(temp_work_dir: Path) -> None:
    """Test validation when inbox is empty."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    status = checker.generate_status(validate=True)

    # Assert
    assert status["validation"]["inbox_empty"] is True


def test_validate_criteria_inbox_not_empty(
    temp_work_dir: Path, sample_task: dict
) -> None:
    """Test validation when inbox has tasks."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    inbox_dir = temp_work_dir / "collaboration" / "inbox"
    create_task_file(inbox_dir, sample_task)

    # Act
    status = checker.generate_status(validate=True)

    # Assert
    assert status["validation"]["inbox_empty"] is False


def test_validate_criteria_tasks_completed(
    temp_work_dir: Path, sample_task: dict
) -> None:
    """Test validation when tasks are completed."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    done_dir = temp_work_dir / "collaboration" / "done"
    (done_dir / "test-agent").mkdir(parents=True)

    task = sample_task.copy()
    task["status"] = "done"
    create_task_file(done_dir / "test-agent", task)

    # Act
    status = checker.generate_status(validate=True)

    # Assert
    assert status["validation"]["tasks_completed"] is True


# ============================================================================
# Output Formatting Tests
# ============================================================================


def test_format_text_basic(temp_work_dir: Path) -> None:
    """Test text formatting of status report."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    status = checker.generate_status()

    # Act
    output = checker.format_text(status)

    # Assert
    assert "Task Status Report" in output
    assert "Total Tasks: 0" in output
    assert "Inbox: 0" in output


def test_format_json_basic(temp_work_dir: Path) -> None:
    """Test JSON formatting of status report."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    status = checker.generate_status()

    # Act
    output = checker.format_json(status)

    # Assert
    parsed = json.loads(output)
    assert parsed["total"] == 0
    assert parsed["inbox"]["count"] == 0
    assert isinstance(parsed, dict)


def test_format_json_with_validation(temp_work_dir: Path) -> None:
    """Test JSON formatting includes validation results."""
    # Arrange
    checker = TemplateStatusChecker(temp_work_dir)
    status = checker.generate_status(validate=True)

    # Act
    output = checker.format_json(status)

    # Assert
    parsed = json.loads(output)
    assert "validation" in parsed
    assert isinstance(parsed["validation"], dict)
