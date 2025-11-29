#!/usr/bin/env python3
"""
Unit Tests for agent_orchestrator.py Module

Tests orchestrator functions for:
- Task assignment from inbox to agents
- Follow-up task creation from completed tasks
- Timeout detection for stalled tasks
- Conflict detection for overlapping artifacts
- Agent status dashboard updates
- Task archival
- Error handling and logging
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

# Add orchestration directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "ops" / "orchestration"))

import agent_orchestrator as orchestrator

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def temp_work_env(tmp_path: Path) -> Path:
    """Create isolated test environment with work directory structure."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    # Create directory structure
    collab_dir = work_dir / "collaboration"
    collab_dir.mkdir()

    inbox_dir = collab_dir / "inbox"
    inbox_dir.mkdir()

    assigned_dir = collab_dir / "assigned"
    assigned_dir.mkdir()

    done_dir = collab_dir / "done"
    done_dir.mkdir()

    archive_dir = collab_dir / "archive"
    archive_dir.mkdir()

    # Create test agent directories
    for agent in ["test-agent", "test-agent-2", "test-agent-3"]:
        (assigned_dir / agent).mkdir()

    # Monkey-patch orchestrator paths
    orchestrator.WORK_DIR = work_dir
    orchestrator.COLLAB_DIR = collab_dir
    orchestrator.INBOX_DIR = inbox_dir
    orchestrator.ASSIGNED_DIR = assigned_dir
    orchestrator.DONE_DIR = done_dir
    orchestrator.ARCHIVE_DIR = archive_dir

    return work_dir


@pytest.fixture
def sample_task() -> dict:
    """Create sample task dictionary."""
    return {
        "id": "2025-11-28T2000-test-agent-sample",
        "agent": "test-agent",
        "status": "new",
        "title": "Sample test task",
        "artefacts": ["test/output/sample.md"],
        "created_at": "2025-11-28T20:00:00Z",
        "created_by": "test-harness",
    }


def write_task(task_file: Path, task: dict) -> None:
    """Helper: Write task to YAML file."""
    task_file.parent.mkdir(parents=True, exist_ok=True)
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task, f, default_flow_style=False, sort_keys=False)


def read_task(task_file: Path) -> dict:
    """Helper: Read task from YAML file."""
    with open(task_file, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ============================================================================
# assign_tasks Tests
# ============================================================================


# Arrange
def test_assign_tasks_empty_inbox(temp_work_env: Path) -> None:
    """Test assigning tasks with empty inbox returns 0."""

    # Act
    assigned = orchestrator.assign_tasks()

    # Assert
    assert assigned == 0

    # Arrange


def test_assign_tasks_single_task(temp_work_env: Path, sample_task: dict) -> None:
    """Test assigning single task from inbox."""

    # Act
    inbox_file = orchestrator.INBOX_DIR / f"{sample_task['id']}.yaml"
    write_task(inbox_file, sample_task)
    assigned = orchestrator.assign_tasks()

    assert assigned == 1
    assert not inbox_file.exists()

    assigned_file = (
        orchestrator.ASSIGNED_DIR / "test-agent" / f"{sample_task['id']}.yaml"
    )
    assert assigned_file.exists()

    result = read_task(assigned_file)
    assert result["status"] == "assigned"
    assert "assigned_at" in result

    # Arrange


def test_assign_tasks_multiple_tasks(temp_work_env: Path) -> None:
    """Test assigning multiple tasks to different agents."""

    # Act
    tasks = [
        {"id": "task-1", "agent": "test-agent", "status": "new"},
        {"id": "task-2", "agent": "test-agent-2", "status": "new"},
        {"id": "task-3", "agent": "test-agent", "status": "new"},
    ]
    for task in tasks:
        inbox_file = orchestrator.INBOX_DIR / f"{task['id']}.yaml"
        write_task(inbox_file, task)

    assigned = orchestrator.assign_tasks()

    assert assigned == 3
    assert len(list(orchestrator.INBOX_DIR.glob("*.yaml"))) == 0

    # Arrange


def test_assign_tasks_missing_agent_field(temp_work_env: Path) -> None:
    """Test assigning task without agent field logs warning."""
    # Arrange
    task = {"id": "task-no-agent", "status": "new"}
    inbox_file = orchestrator.INBOX_DIR / "task-no-agent.yaml"
    write_task(inbox_file, task)

    # Assumption Check
    assert (
        inbox_file.exists()
    ), "Test precondition failed: task file should exist in inbox"

    # Act
    assigned = orchestrator.assign_tasks()

    # Assert
    assert assigned == 0
    assert inbox_file.exists()  # Task remains in inbox

    # Check workflow log
    log_file = orchestrator.COLLAB_DIR / "WORKFLOW_LOG.md"
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "missing 'agent'" in log_content


def test_assign_tasks_unknown_agent(temp_work_env: Path) -> None:
    """Test assigning task to non-existent agent logs error."""

    # Act
    task = {
        "id": "task-unknown",
        "agent": "nonexistent-agent",
        "status": "new",
    }
    inbox_file = orchestrator.INBOX_DIR / "task-unknown.yaml"
    write_task(inbox_file, task)
    assigned = orchestrator.assign_tasks()

    assert assigned == 0
    assert inbox_file.exists()  # Task remains in inbox

    # Check workflow log
    log_file = orchestrator.COLLAB_DIR / "WORKFLOW_LOG.md"
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "Unknown agent" in log_content

    # Arrange


def test_assign_tasks_preserves_task_data(temp_work_env: Path) -> None:
    """Test task assignment preserves all task fields."""

    # Act
    task = {
        "id": "task-preserve",
        "agent": "test-agent",
        "status": "new",
        "title": "Test task",
        "artefacts": ["test1.md", "test2.md"],
        "context": {"note": "Important task"},
        "created_at": "2025-11-28T20:00:00Z",
        "created_by": "test",
    }
    inbox_file = orchestrator.INBOX_DIR / "task-preserve.yaml"
    write_task(inbox_file, task)
    orchestrator.assign_tasks()

    assigned_file = orchestrator.ASSIGNED_DIR / "test-agent" / "task-preserve.yaml"
    result = read_task(assigned_file)

    assert result["title"] == "Test task"
    assert result["artefacts"] == ["test1.md", "test2.md"]
    assert result["context"]["note"] == "Important task"
    assert result["created_by"] == "test"


# ============================================================================
# process_completed_tasks Tests
# ============================================================================


# Arrange
def test_process_completed_no_tasks(temp_work_env: Path) -> None:
    """Test processing completed tasks with no done tasks."""

    # Act
    followups = orchestrator.process_completed_tasks()

    # Assert
    assert followups == 0

    # Arrange


def test_process_completed_no_next_agent(temp_work_env: Path) -> None:
    """Test processing completed task without next_agent."""

    # Act
    task = {
        "id": "task-done",
        "agent": "test-agent",
        "status": "done",
        "result": {"summary": "Task completed"},
    }
    done_file = orchestrator.DONE_DIR / "task-done.yaml"
    write_task(done_file, task)
    followups = orchestrator.process_completed_tasks()

    assert followups == 0
    assert len(list(orchestrator.INBOX_DIR.glob("*.yaml"))) == 0

    # Arrange


def test_process_completed_with_next_agent(temp_work_env: Path) -> None:
    """Test processing completed task creates follow-up."""

    # Act
    task = {
        "id": "task-handoff",
        "agent": "test-agent",
        "status": "done",
        "artefacts": ["output.md"],
        "result": {
            "summary": "Phase 1 complete",
            "next_agent": "test-agent-2",
            "next_task_title": "Phase 2 processing",
            "next_artefacts": ["output-phase2.md"],
            "next_task_notes": ["Continue from phase 1"],
        },
    }
    done_file = orchestrator.DONE_DIR / "task-handoff.yaml"
    write_task(done_file, task)
    followups = orchestrator.process_completed_tasks()

    assert followups == 1

    # Check follow-up task created
    inbox_files = list(orchestrator.INBOX_DIR.glob("*.yaml"))
    assert len(inbox_files) == 1

    followup = read_task(inbox_files[0])
    assert followup["agent"] == "test-agent-2"
    assert followup["status"] == "new"
    assert followup["title"] == "Phase 2 processing"
    assert followup["artefacts"] == ["output-phase2.md"]
    assert followup["context"]["previous_agent"] == "test-agent"
    assert followup["context"]["previous_task"] == "task-handoff"

    # Arrange


def test_process_completed_handoff_logged(temp_work_env: Path) -> None:
    """Test processing completed task logs handoff."""

    # Act
    task = {
        "id": "task-log-handoff",
        "agent": "test-agent",
        "status": "done",
        "result": {
            "summary": "Done",
            "next_agent": "test-agent-2",
            "next_task_title": "Follow-up",
            "next_artefacts": ["output.md"],
        },
    }
    done_file = orchestrator.DONE_DIR / "task-log-handoff.yaml"
    write_task(done_file, task)
    orchestrator.process_completed_tasks()

    # Check handoff log
    handoff_log = orchestrator.COLLAB_DIR / "HANDOFFS.md"
    assert handoff_log.exists()
    content = handoff_log.read_text()
    assert "test-agent → test-agent-2" in content
    assert "output.md" in content

    # Arrange


def test_process_completed_no_duplicate_followup(temp_work_env: Path) -> None:
    """Test processing same completed task twice doesn't create duplicate."""

    # Act
    task = {
        "id": "task-duplicate",
        "agent": "test-agent",
        "status": "done",
        "result": {
            "summary": "Done",
            "next_agent": "test-agent-2",
            "next_task_title": "Follow-up",
        },
    }
    done_file = orchestrator.DONE_DIR / "task-duplicate.yaml"
    write_task(done_file, task)
    # Process twice
    followups1 = orchestrator.process_completed_tasks()
    followups2 = orchestrator.process_completed_tasks()

    assert followups1 == 1
    assert followups2 == 0  # No new follow-ups created

    # Only one follow-up file
    inbox_files = list(orchestrator.INBOX_DIR.glob("*.yaml"))
    assert len(inbox_files) == 1


# ============================================================================
# check_timeouts Tests
# ============================================================================


# Arrange
def test_check_timeouts_no_tasks(temp_work_env: Path) -> None:
    """Test timeout check with no tasks."""

    # Act
    flagged = orchestrator.check_timeouts()

    # Assert
    assert flagged == 0

    # Arrange


def test_check_timeouts_recent_task(temp_work_env: Path) -> None:
    """Test timeout check with recent task doesn't flag."""

    # Act
    task = {
        "id": "task-recent",
        "agent": "test-agent",
        "status": "in_progress",
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    task_file = orchestrator.ASSIGNED_DIR / "test-agent" / "task-recent.yaml"
    write_task(task_file, task)
    flagged = orchestrator.check_timeouts()

    assert flagged == 0

    # Arrange


def test_check_timeouts_stalled_task(temp_work_env: Path) -> None:
    """Test timeout check flags stalled task."""

    # Act
    old_time = datetime.now(timezone.utc) - timedelta(hours=3)
    task = {
        "id": "task-stalled",
        "agent": "test-agent",
        "status": "in_progress",
        "started_at": old_time.isoformat().replace("+00:00", "Z"),
    }
    task_file = orchestrator.ASSIGNED_DIR / "test-agent" / "task-stalled.yaml"
    write_task(task_file, task)
    flagged = orchestrator.check_timeouts()

    assert flagged == 1

    # Check workflow log
    log_file = orchestrator.COLLAB_DIR / "WORKFLOW_LOG.md"
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "stalled" in log_content

    # Arrange


def test_check_timeouts_ignores_assigned_status(temp_work_env: Path) -> None:
    """Test timeout check ignores tasks not in_progress."""

    # Act
    old_time = datetime.now(timezone.utc) - timedelta(hours=5)
    task = {
        "id": "task-assigned",
        "agent": "test-agent",
        "status": "assigned",
        "assigned_at": old_time.isoformat().replace("+00:00", "Z"),
    }
    task_file = orchestrator.ASSIGNED_DIR / "test-agent" / "task-assigned.yaml"
    write_task(task_file, task)
    flagged = orchestrator.check_timeouts()

    assert flagged == 0

    # Arrange


def test_check_timeouts_missing_started_at(temp_work_env: Path) -> None:
    """Test timeout check handles missing started_at gracefully."""
    # Arrange
    task = {
        "id": "task-no-start",
        "agent": "test-agent",
        "status": "in_progress",
    }
    task_file = orchestrator.ASSIGNED_DIR / "test-agent" / "task-no-start.yaml"
    write_task(task_file, task)

    # Assumption Check
    assert task_file.exists(), "Test precondition failed: task file should exist"
    assert (
        "started_at" not in task
    ), "Test precondition failed: task should NOT have started_at"

    # Act
    flagged = orchestrator.check_timeouts()

    # Assert
    assert flagged == 0  # Skips task without error

    # Check warning logged
    log_file = orchestrator.COLLAB_DIR / "WORKFLOW_LOG.md"
    log_content = log_file.read_text()
    assert "missing started_at" in log_content


# ============================================================================
# detect_conflicts Tests
# ============================================================================


# Arrange
def test_detect_conflicts_no_tasks(temp_work_env: Path) -> None:
    """Test conflict detection with no tasks."""

    # Act
    conflicts = orchestrator.detect_conflicts()

    # Assert
    assert conflicts == 0

    # Arrange


def test_detect_conflicts_unique_artifacts(temp_work_env: Path) -> None:
    """Test conflict detection with unique artifacts."""

    # Act
    task1 = {
        "id": "task-1",
        "agent": "test-agent",
        "status": "in_progress",
        "artefacts": ["output1.md"],
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    task2 = {
        "id": "task-2",
        "agent": "test-agent-2",
        "status": "in_progress",
        "artefacts": ["output2.md"],
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    write_task(orchestrator.ASSIGNED_DIR / "test-agent" / "task-1.yaml", task1)
    write_task(orchestrator.ASSIGNED_DIR / "test-agent-2" / "task-2.yaml", task2)

    conflicts = orchestrator.detect_conflicts()

    assert conflicts == 0

    # Arrange


def test_detect_conflicts_overlapping_artifacts(temp_work_env: Path) -> None:
    """Test conflict detection with overlapping artifacts."""

    # Act
    shared_artifact = "shared-output.md"
    task1 = {
        "id": "task-conflict-1",
        "agent": "test-agent",
        "status": "in_progress",
        "artefacts": [shared_artifact],
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    task2 = {
        "id": "task-conflict-2",
        "agent": "test-agent-2",
        "status": "in_progress",
        "artefacts": [shared_artifact],
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    write_task(orchestrator.ASSIGNED_DIR / "test-agent" / "task-conflict-1.yaml", task1)
    write_task(
        orchestrator.ASSIGNED_DIR / "test-agent-2" / "task-conflict-2.yaml", task2
    )

    conflicts = orchestrator.detect_conflicts()

    assert conflicts == 1

    # Check workflow log
    log_file = orchestrator.COLLAB_DIR / "WORKFLOW_LOG.md"
    log_content = log_file.read_text()
    assert "Conflict" in log_content
    assert shared_artifact in log_content

    # Arrange


def test_detect_conflicts_ignores_assigned_status(temp_work_env: Path) -> None:
    """Test conflict detection only checks in_progress tasks."""

    # Act
    shared_artifact = "shared.md"
    task1 = {
        "id": "task-assigned",
        "agent": "test-agent",
        "status": "assigned",
        "artefacts": [shared_artifact],
    }
    task2 = {
        "id": "task-progress",
        "agent": "test-agent-2",
        "status": "in_progress",
        "artefacts": [shared_artifact],
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    write_task(orchestrator.ASSIGNED_DIR / "test-agent" / "task-assigned.yaml", task1)
    write_task(orchestrator.ASSIGNED_DIR / "test-agent-2" / "task-progress.yaml", task2)

    conflicts = orchestrator.detect_conflicts()

    assert conflicts == 0  # Only in_progress counts


# ============================================================================
# update_agent_status Tests
# ============================================================================


# Arrange
def test_update_agent_status_empty(temp_work_env: Path) -> None:
    """Test status update with no tasks."""
    orchestrator.update_agent_status()
    status_file = orchestrator.COLLAB_DIR / "AGENT_STATUS.md"
    assert status_file.exists()
    content = status_file.read_text()
    assert "Agent Status Dashboard" in content

    # Arrange


def test_update_agent_status_with_tasks(temp_work_env: Path) -> None:
    """Test status update includes agent tasks."""

    # Act
    task1 = {
        "id": "task-assigned",
        "agent": "test-agent",
        "status": "assigned",
    }
    task2 = {
        "id": "task-progress",
        "agent": "test-agent",
        "status": "in_progress",
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    write_task(orchestrator.ASSIGNED_DIR / "test-agent" / "task-assigned.yaml", task1)
    write_task(orchestrator.ASSIGNED_DIR / "test-agent" / "task-progress.yaml", task2)

    orchestrator.update_agent_status()

    status_file = orchestrator.COLLAB_DIR / "AGENT_STATUS.md"
    content = status_file.read_text()

    assert "test-agent" in content
    assert "**Assigned**: 1 tasks" in content
    assert "**In Progress**: 1 tasks" in content
    assert "task-progress" in content  # Current task shown

    # Arrange


def test_update_agent_status_idle_agent(temp_work_env: Path) -> None:
    """Test status update shows idle agent."""
    orchestrator.update_agent_status()
    status_file = orchestrator.COLLAB_DIR / "AGENT_STATUS.md"
    content = status_file.read_text()

    # All test agents should show as idle
    assert "test-agent" in content
    assert "Idle" in content


# ============================================================================
# archive_old_tasks Tests
# ============================================================================


# Arrange
def test_archive_old_tasks_no_tasks(temp_work_env: Path) -> None:
    """Test archival with no done tasks."""

    # Act
    archived = orchestrator.archive_old_tasks()

    # Assert
    assert archived == 0

    # Arrange


def test_archive_old_tasks_recent_task(temp_work_env: Path) -> None:
    """Test archival doesn't archive recent tasks."""

    # Act
    recent_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    task = {
        "id": f"{recent_date}T1200-task-recent",
        "agent": "test-agent",
        "status": "done",
    }
    done_file = orchestrator.DONE_DIR / f"{task['id']}.yaml"
    write_task(done_file, task)
    archived = orchestrator.archive_old_tasks()

    assert archived == 0
    assert done_file.exists()  # Still in done

    # Arrange


def test_archive_old_tasks_old_task(temp_work_env: Path) -> None:
    """Test archival moves old tasks to archive."""

    # Act
    old_date = (datetime.now(timezone.utc) - timedelta(days=35)).strftime("%Y-%m-%d")
    task = {
        "id": f"{old_date}T1200-task-old",
        "agent": "test-agent",
        "status": "done",
    }
    done_file = orchestrator.DONE_DIR / f"{task['id']}.yaml"
    write_task(done_file, task)
    archived = orchestrator.archive_old_tasks()

    assert archived == 1
    assert not done_file.exists()

    # Check archived location (YYYY-MM format)
    year_month = old_date[:7]
    archive_file = orchestrator.ARCHIVE_DIR / year_month / f"{task['id']}.yaml"
    assert archive_file.exists()

    # Arrange


def test_archive_old_tasks_multiple(temp_work_env: Path) -> None:
    """Test archival handles multiple old tasks."""

    # Act
    old_date = (datetime.now(timezone.utc) - timedelta(days=40)).strftime("%Y-%m-%d")
    for i in range(3):
        task = {
            "id": f"{old_date}T{1200+i:04d}-task-old-{i}",
            "agent": "test-agent",
            "status": "done",
        }
        done_file = orchestrator.DONE_DIR / f"{task['id']}.yaml"
        write_task(done_file, task)

    archived = orchestrator.archive_old_tasks()

    assert archived == 3


# ============================================================================
# log_handoff Tests
# ============================================================================


# Arrange
def test_log_handoff_creates_file(temp_work_env: Path) -> None:
    """Test log_handoff creates handoff log file."""
    orchestrator.log_handoff("test-agent", "test-agent-2", ["output.md"], "task-123")
    handoff_log = orchestrator.COLLAB_DIR / "HANDOFFS.md"
    assert handoff_log.exists()

    # Arrange


def test_log_handoff_content(temp_work_env: Path) -> None:
    """Test log_handoff writes correct content."""
    orchestrator.log_handoff(
        "test-agent", "test-agent-2", ["file1.md", "file2.md"], "task-456"
    )
    handoff_log = orchestrator.COLLAB_DIR / "HANDOFFS.md"
    content = handoff_log.read_text()

    assert "test-agent → test-agent-2" in content
    assert "file1.md" in content
    assert "file2.md" in content
    assert "task-456" in content
    assert "Created" in content

    # Arrange


def test_log_handoff_appends(temp_work_env: Path) -> None:
    """Test multiple handoffs are appended to log."""
    orchestrator.log_handoff("agent-1", "agent-2", ["file1.md"], "task-1")
    orchestrator.log_handoff("agent-2", "agent-3", ["file2.md"], "task-2")
    handoff_log = orchestrator.COLLAB_DIR / "HANDOFFS.md"
    content = handoff_log.read_text()

    assert "agent-1 → agent-2" in content
    assert "agent-2 → agent-3" in content
    assert "task-1" in content
    assert "task-2" in content


# ============================================================================
# Integration Tests
# ============================================================================


# Arrange
def test_orchestrator_main_function(temp_work_env: Path) -> None:
    """Test main orchestrator cycle runs without error."""
    # Create sample tasks

    # Act
    task1 = {
        "id": "2025-11-28T2000-test-main-1",
        "agent": "test-agent",
        "status": "new",
        "artefacts": ["output1.md"],
        "created_at": "2025-11-28T20:00:00Z",
    }
    task2 = {
        "id": "2025-11-28T2001-test-main-2",
        "agent": "test-agent-2",
        "status": "new",
        "artefacts": ["output2.md"],
        "created_at": "2025-11-28T20:01:00Z",
    }
    write_task(orchestrator.INBOX_DIR / "task1.yaml", task1)
    write_task(orchestrator.INBOX_DIR / "task2.yaml", task2)

    # Run main cycle
    orchestrator.main()

    # Verify tasks were assigned
    assert len(list(orchestrator.INBOX_DIR.glob("*.yaml"))) == 0
    assert len(list(orchestrator.ASSIGNED_DIR.glob("**/*.yaml"))) == 2

    # Verify artifacts created
    assert (orchestrator.COLLAB_DIR / "AGENT_STATUS.md").exists()
    assert (orchestrator.COLLAB_DIR / "WORKFLOW_LOG.md").exists()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
