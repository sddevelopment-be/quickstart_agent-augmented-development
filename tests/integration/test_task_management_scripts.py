#!/usr/bin/env python3
"""
Acceptance Tests for Task Management Scripts (ATDD)

These tests verify the command-line scripts that orchestrators and agents
use to manage task lifecycle and location.

Test Coverage:
- list_open_tasks.py: List tasks not in done/error state
- start_task.py: Move task to in_progress status
- complete_task.py: Move task to done and mark complete
- freeze_task.py: Move task to fridge (pause/defer)

Related ADRs:
- ADR-042: Shared Task Domain Model
- ADR-043: Status Enumeration Standard

Directive Compliance:
- 016 (ATDD): These tests define acceptance criteria before implementation
- 017 (TDD): Unit tests will be added during implementation
- 021 (Locality): Scripts interact only with task files and common modules
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
import yaml

# Add paths to import modules
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from src.domain.collaboration.task_schema import read_task

# Path to scripts under test
SCRIPTS_DIR = REPO_ROOT / "tools" / "scripts"
LIST_SCRIPT = SCRIPTS_DIR / "list_open_tasks.py"
START_SCRIPT = SCRIPTS_DIR / "start_task.py"
COMPLETE_SCRIPT = SCRIPTS_DIR / "complete_task.py"
FREEZE_SCRIPT = SCRIPTS_DIR / "freeze_task.py"


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def temp_work_dir(tmp_path: Path) -> Path:
    """Create isolated work directory structure for testing."""
    work_dir = tmp_path / "work" / "collaboration"

    # Create directory structure
    (work_dir / "assigned" / "python-pedro").mkdir(parents=True)
    (work_dir / "assigned" / "backend-dev").mkdir(parents=True)
    (work_dir / "done" / "python-pedro").mkdir(parents=True)
    (work_dir / "fridge").mkdir(parents=True)

    return work_dir


@pytest.fixture
def sample_assigned_task(temp_work_dir: Path) -> tuple[Path, dict[str, Any]]:
    """Create sample assigned task for testing."""
    task_id = "2026-02-09T2033-python-pedro-test-task"
    task_data = {
        "id": task_id,
        "agent": "python-pedro",
        "status": "assigned",
        "priority": "high",
        "title": "Test Task for Script Validation",
        "created_at": "2026-02-09T20:33:00Z",
        "assigned_at": "2026-02-09T20:35:00Z",
    }

    task_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
    with open(task_path, "w", encoding="utf-8") as f:
        yaml.dump(task_data, f, sort_keys=False)

    return task_path, task_data


@pytest.fixture
def multiple_tasks(temp_work_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    """Create multiple tasks with different statuses and agents."""
    tasks = []

    task_configs = [
        ("python-pedro", "assigned", "high", "2026-02-09T1000-python-pedro-task-1"),
        (
            "python-pedro",
            "in_progress",
            "medium",
            "2026-02-09T1100-python-pedro-task-2",
        ),
        ("backend-dev", "assigned", "low", "2026-02-09T1200-backend-dev-task-1"),
        ("backend-dev", "blocked", "high", "2026-02-09T1300-backend-dev-task-2"),
    ]

    for agent, status, priority, task_id in task_configs:
        task_data = {
            "id": task_id,
            "agent": agent,
            "status": status,
            "priority": priority,
            "title": f"Test Task {task_id}",
            "created_at": "2026-02-09T10:00:00Z",
        }

        task_path = temp_work_dir / "assigned" / agent / f"{task_id}.yaml"
        with open(task_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        tasks.append((task_path, task_data))

    return tasks


# ============================================================================
# Acceptance Tests: list_open_tasks.py
# ============================================================================


class TestListOpenTasks:
    """
    Acceptance tests for list_open_tasks.py script.

    Acceptance Criteria:
    - AC1: List all tasks not in done/error state
    - AC2: Filter tasks by status (assigned, in_progress, blocked)
    - AC3: Filter tasks by agent
    - AC4: Filter tasks by priority
    - AC5: Display task id, status, agent, priority
    - AC6: Output as JSON for programmatic consumption
    """

    def test_list_all_open_tasks(self, temp_work_dir: Path, multiple_tasks: list):
        """AC1: List all tasks that are not done/error."""
        result = subprocess.run(
            [sys.executable, str(LIST_SCRIPT), "--work-dir", str(temp_work_dir)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # All 4 tasks should be listed (assigned, in_progress, blocked)
        output_lines = [line for line in result.stdout.split("\n") if line.strip()]
        assert len(output_lines) >= 4, "Should list all non-terminal tasks"

    def test_filter_by_status(self, temp_work_dir: Path, multiple_tasks: list):
        """AC2: Filter tasks by status."""
        result = subprocess.run(
            [
                sys.executable,
                str(LIST_SCRIPT),
                "--work-dir",
                str(temp_work_dir),
                "--status",
                "assigned",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "assigned" in result.stdout.lower()
        # Should only show assigned tasks (2 total)
        assert result.stdout.count("assigned") == 2

    def test_filter_by_agent(self, temp_work_dir: Path, multiple_tasks: list):
        """AC3: Filter tasks by agent."""
        result = subprocess.run(
            [
                sys.executable,
                str(LIST_SCRIPT),
                "--work-dir",
                str(temp_work_dir),
                "--agent",
                "python-pedro",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "python-pedro" in result.stdout
        assert "backend-dev" not in result.stdout

    def test_filter_by_priority(self, temp_work_dir: Path, multiple_tasks: list):
        """AC4: Filter tasks by priority."""
        result = subprocess.run(
            [
                sys.executable,
                str(LIST_SCRIPT),
                "--work-dir",
                str(temp_work_dir),
                "--priority",
                "high",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "high" in result.stdout.lower()

    def test_json_output(self, temp_work_dir: Path, multiple_tasks: list):
        """AC5+AC6: Output in JSON format with required fields."""
        result = subprocess.run(
            [
                sys.executable,
                str(LIST_SCRIPT),
                "--work-dir",
                str(temp_work_dir),
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Parse JSON output
        tasks = json.loads(result.stdout)
        assert isinstance(tasks, list)
        assert len(tasks) == 4

        # Verify required fields present
        for task in tasks:
            assert "id" in task
            assert "status" in task
            assert "agent" in task
            assert "priority" in task

    def test_help_option(self):
        """Verify --help documentation is available."""
        result = subprocess.run(
            [sys.executable, str(LIST_SCRIPT), "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "list" in result.stdout.lower()
        assert "--status" in result.stdout
        assert "--agent" in result.stdout
        assert "--priority" in result.stdout


# ============================================================================
# Acceptance Tests: start_task.py
# ============================================================================


class TestStartTask:
    """
    Acceptance tests for start_task.py script.

    Acceptance Criteria:
    - AC1: Update task status from 'assigned' to 'in_progress'
    - AC2: Add started_at timestamp in ISO8601 format with Z suffix
    - AC3: Keep task in same location (assigned/agent/)
    - AC4: Use TaskStatus enum for validation
    - AC5: Error if task is not in 'assigned' state
    """

    def test_start_assigned_task(
        self, temp_work_dir: Path, sample_assigned_task: tuple
    ):
        """AC1+AC2+AC3: Start an assigned task successfully."""
        task_path, task_data = sample_assigned_task
        task_id = task_data["id"]

        result = subprocess.run(
            [
                sys.executable,
                str(START_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert (
            "started" in result.stdout.lower() or "in_progress" in result.stdout.lower()
        )

        # Verify task file still exists in same location
        assert task_path.exists(), "Task file should remain in assigned directory"

        # Verify task was updated correctly
        updated_task = read_task(task_path)
        assert updated_task["status"] == "in_progress"
        assert "started_at" in updated_task

        # Verify timestamp format (ISO8601 with Z)
        started_at = updated_task["started_at"]
        assert started_at.endswith("Z"), "Timestamp should use Z suffix"
        # Parse to verify valid ISO8601
        datetime.fromisoformat(started_at.replace("Z", "+00:00"))

    def test_cannot_start_non_assigned_task(self, temp_work_dir: Path):
        """AC5: Error when trying to start a task not in 'assigned' state."""
        # Create task already in_progress
        task_id = "2026-02-09T2100-test-inprogress-task"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-09T21:00:00Z",
        }

        task_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(task_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(START_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
            ],
            capture_output=True,
            text=True,
        )

        # Should fail with non-zero exit code
        assert result.returncode != 0
        assert (
            "assigned" in result.stderr.lower()
            or "in_progress" in result.stderr.lower()
        )

    def test_task_not_found(self, temp_work_dir: Path):
        """Error handling: Task ID not found."""
        result = subprocess.run(
            [
                sys.executable,
                str(START_SCRIPT),
                "nonexistent-task-id",
                "--work-dir",
                str(temp_work_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "not found" in result.stderr.lower()


# ============================================================================
# Acceptance Tests: complete_task.py
# ============================================================================


class TestCompleteTask:
    """
    Acceptance tests for complete_task.py script.

    Acceptance Criteria:
    - AC1: Update task status to 'done'
    - AC2: Move task from assigned/agent/ to done/agent/
    - AC3: Add completed_at timestamp
    - AC4: Validate result block exists
    - AC5: Use TaskStatus enum for validation
    - AC6: Accept --summary and --artefacts to build result inline
    """

    def test_complete_task_with_result(self, temp_work_dir: Path):
        """AC1+AC2+AC3: Complete a task and move to done directory."""
        task_id = "2026-02-09T2200-test-complete-task"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-09T22:00:00Z",
            "result": {
                "summary": "Task completed successfully",
                "artefacts": ["file1.py", "file2.py"],
            },
        }

        original_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(original_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(COMPLETE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Verify task moved to done directory
        new_path = temp_work_dir / "done" / "python-pedro" / f"{task_id}.yaml"
        assert new_path.exists(), "Task should be moved to done directory"
        assert not original_path.exists(), "Task should be removed from assigned"

        # Verify task was updated
        completed_task = read_task(new_path)
        assert completed_task["status"] == "done"
        assert "completed_at" in completed_task

        # Verify timestamp format
        completed_at = completed_task["completed_at"]
        assert completed_at.endswith("Z")
        datetime.fromisoformat(completed_at.replace("Z", "+00:00"))

    def test_cannot_complete_without_result(self, temp_work_dir: Path):
        """AC4: Error if result block is missing."""
        task_id = "2026-02-09T2300-test-no-result"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-09T23:00:00Z",
            # No result block
        }

        task_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(task_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(COMPLETE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
            ],
            capture_output=True,
            text=True,
        )

        # Should fail without result block
        assert result.returncode != 0
        assert "result" in result.stderr.lower()

    def test_complete_with_force_flag(self, temp_work_dir: Path):
        """Allow completion without result if --force flag is used."""
        task_id = "2026-02-09T2301-test-force-complete"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-09T23:01:00Z",
        }

        original_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(original_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(COMPLETE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
                "--force",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Verify task moved
        new_path = temp_work_dir / "done" / "python-pedro" / f"{task_id}.yaml"
        assert new_path.exists()

    def test_complete_with_summary_and_artefacts(self, temp_work_dir: Path):
        """AC6: Complete task with --summary and --artefacts flags."""
        task_id = "2026-02-10T0800-test-inline-result"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-10T08:00:00Z",
            # No result block in file
        }

        original_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(original_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(COMPLETE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
                "--summary",
                "Implemented feature X with full test coverage",
                "--artefacts",
                "src/feature_x.py",
                "tests/test_feature_x.py",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Verify task moved to done
        new_path = temp_work_dir / "done" / "python-pedro" / f"{task_id}.yaml"
        assert new_path.exists()

        # Verify result block was created from CLI args
        completed_task = read_task(new_path)
        assert completed_task["status"] == "done"
        assert (
            completed_task["result"]["summary"]
            == "Implemented feature X with full test coverage"
        )
        assert completed_task["result"]["artefacts"] == [
            "src/feature_x.py",
            "tests/test_feature_x.py",
        ]

    def test_complete_with_summary_only(self, temp_work_dir: Path):
        """AC6: Complete task with --summary but no --artefacts."""
        task_id = "2026-02-10T0801-test-summary-only"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-10T08:01:00Z",
        }

        original_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(original_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(COMPLETE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
                "-s",
                "Quick fix applied",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        new_path = temp_work_dir / "done" / "python-pedro" / f"{task_id}.yaml"
        completed_task = read_task(new_path)
        assert completed_task["result"]["summary"] == "Quick fix applied"
        assert completed_task["result"]["artefacts"] == []

    def test_summary_overrides_existing_result(self, temp_work_dir: Path):
        """AC6: --summary overrides pre-existing result block in file."""
        task_id = "2026-02-10T0802-test-summary-override"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-10T08:02:00Z",
            "result": {
                "summary": "Old summary",
                "artefacts": ["old_file.py"],
            },
        }

        original_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(original_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(COMPLETE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
                "-s",
                "Updated summary",
                "-a",
                "new_file.py",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        new_path = temp_work_dir / "done" / "python-pedro" / f"{task_id}.yaml"
        completed_task = read_task(new_path)
        assert completed_task["result"]["summary"] == "Updated summary"
        assert completed_task["result"]["artefacts"] == ["new_file.py"]


# ============================================================================
# Acceptance Tests: freeze_task.py
# ============================================================================


class TestFreezeTask:
    """
    Acceptance tests for freeze_task.py script.

    Acceptance Criteria:
    - AC1: Move task from assigned/agent/ to fridge/
    - AC2: Add frozen_at timestamp
    - AC3: Add freeze_reason field (required)
    - AC4: Preserve original status
    - AC5: Allow freezing from any active state
    """

    def test_freeze_task_with_reason(self, temp_work_dir: Path):
        """AC1+AC2+AC3: Freeze a task with a reason."""
        task_id = "2026-02-10T0100-test-freeze-task"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "assigned",
            "priority": "medium",
        }

        original_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(original_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        freeze_reason = "Blocked on dependency XYZ"

        result = subprocess.run(
            [
                sys.executable,
                str(FREEZE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
                "--reason",
                freeze_reason,
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Verify task moved to fridge
        new_path = temp_work_dir / "fridge" / f"{task_id}.yaml"
        assert new_path.exists(), "Task should be moved to fridge"
        assert not original_path.exists(), "Task should be removed from assigned"

        # Verify task was updated
        frozen_task = read_task(new_path)
        assert "frozen_at" in frozen_task
        assert frozen_task["freeze_reason"] == freeze_reason

        # Verify timestamp format
        frozen_at = frozen_task["frozen_at"]
        assert frozen_at.endswith("Z")
        datetime.fromisoformat(frozen_at.replace("Z", "+00:00"))

    def test_freeze_requires_reason(self, temp_work_dir: Path, sample_assigned_task):
        """AC3: Freeze operation requires a reason."""
        task_path, task_data = sample_assigned_task
        task_id = task_data["id"]

        result = subprocess.run(
            [
                sys.executable,
                str(FREEZE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
                # No --reason provided
            ],
            capture_output=True,
            text=True,
        )

        # Should fail without reason
        assert result.returncode != 0
        assert "reason" in result.stderr.lower()

    def test_freeze_from_in_progress(self, temp_work_dir: Path):
        """AC5: Can freeze task from in_progress state."""
        task_id = "2026-02-10T0200-test-freeze-inprogress"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "in_progress",
            "started_at": "2026-02-10T02:00:00Z",
        }

        original_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(original_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        result = subprocess.run(
            [
                sys.executable,
                str(FREEZE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
                "--reason",
                "Need to work on higher priority task",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Verify task moved and status preserved
        new_path = temp_work_dir / "fridge" / f"{task_id}.yaml"
        frozen_task = read_task(new_path)
        assert frozen_task["status"] == "in_progress"  # Original status preserved


# ============================================================================
# Integration Test: Complete Workflow
# ============================================================================


class TestCompleteWorkflow:
    """
    Integration test demonstrating full task lifecycle using all scripts.
    """

    def test_full_task_lifecycle(self, temp_work_dir: Path):
        """Test complete workflow: list → start → complete."""
        # Create initial assigned task
        task_id = "2026-02-10T0300-test-full-workflow"
        task_data = {
            "id": task_id,
            "agent": "python-pedro",
            "status": "assigned",
            "priority": "high",
            "title": "Full Workflow Test Task",
        }

        task_path = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"
        with open(task_path, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f, sort_keys=False)

        # Step 1: List open tasks
        list_result = subprocess.run(
            [
                sys.executable,
                str(LIST_SCRIPT),
                "--work-dir",
                str(temp_work_dir),
                "--agent",
                "python-pedro",
            ],
            capture_output=True,
            text=True,
        )
        assert list_result.returncode == 0
        assert task_id in list_result.stdout

        # Step 2: Start task
        start_result = subprocess.run(
            [
                sys.executable,
                str(START_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
            ],
            capture_output=True,
            text=True,
        )
        assert start_result.returncode == 0

        # Verify status changed
        updated_task = read_task(task_path)
        assert updated_task["status"] == "in_progress"

        # Step 3: Add result block manually (simulating work completion)
        updated_task["result"] = {
            "summary": "Workflow test completed",
            "artefacts": ["test_file.py"],
        }
        with open(task_path, "w", encoding="utf-8") as f:
            yaml.dump(updated_task, f, sort_keys=False)

        # Step 4: Complete task
        complete_result = subprocess.run(
            [
                sys.executable,
                str(COMPLETE_SCRIPT),
                task_id,
                "--work-dir",
                str(temp_work_dir),
            ],
            capture_output=True,
            text=True,
        )
        assert complete_result.returncode == 0

        # Verify task moved to done
        done_path = temp_work_dir / "done" / "python-pedro" / f"{task_id}.yaml"
        assert done_path.exists()

        completed_task = read_task(done_path)
        assert completed_task["status"] == "done"
        assert "completed_at" in completed_task

        # Step 5: List open tasks again - should not include completed task
        list_result2 = subprocess.run(
            [
                sys.executable,
                str(LIST_SCRIPT),
                "--work-dir",
                str(temp_work_dir),
                "--agent",
                "python-pedro",
            ],
            capture_output=True,
            text=True,
        )
        assert list_result2.returncode == 0
        assert task_id not in list_result2.stdout  # Task is done, not open
