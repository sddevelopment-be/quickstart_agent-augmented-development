#!/usr/bin/env python3
"""
End-to-End Test Harness for Agent Orchestration System

Validates full orchestration lifecycle:
- Task creation → assignment → processing → completion → archival
- Sequential, parallel, and convergent workflow patterns
- Error handling and recovery scenarios
- Dashboard updates and logging

Test scenarios:
1. Simple single-agent task (inbox → assigned → done)
2. Sequential workflow (Agent A → Agent B via next_agent)
3. Parallel workflow (Multiple agents working simultaneously)
4. Convergent workflow (Multiple agents targeting shared artifacts)
5. Timeout detection (Task stuck in in_progress)
6. Conflict detection (Overlapping artifact targets)
7. Archive execution (Old tasks moved to archive)
8. Error handling (Invalid task schema, missing agent)
"""

from __future__ import annotations

import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import orchestrator module
import agent_orchestrator as orchestrator


@pytest.fixture
def temp_work_env(tmp_path: Path) -> Path:
    """Create isolated test environment with work directory structure."""
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    
    # Create directory structure
    (work_dir / "inbox").mkdir()
    (work_dir / "done").mkdir()
    (work_dir / "archive").mkdir()
    (work_dir / "collaboration").mkdir()
    
    assigned_dir = work_dir / "assigned"
    assigned_dir.mkdir()
    
    # Create test agent directories
    for agent in ["test-agent", "test-agent-2", "test-agent-3"]:
        (assigned_dir / agent).mkdir()
    
    # Monkey-patch orchestrator paths
    orchestrator.WORK_DIR = work_dir
    orchestrator.INBOX_DIR = work_dir / "inbox"
    orchestrator.ASSIGNED_DIR = work_dir / "assigned"
    orchestrator.DONE_DIR = work_dir / "done"
    orchestrator.ARCHIVE_DIR = work_dir / "archive"
    orchestrator.COLLAB_DIR = work_dir / "collaboration"
    
    return work_dir


def create_task(
    task_id: str,
    agent: str,
    status: str = "new",
    artefacts: list[str] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a test task dictionary."""
    task = {
        "id": task_id,
        "agent": agent,
        "status": status,
        "artefacts": artefacts or [f"test/output/{task_id}.md"],
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "created_by": "test-harness",
    }
    task.update(kwargs)
    return task


def write_task(work_dir: Path, location: str, task: dict[str, Any]) -> Path:
    """Write task to specified location (inbox, assigned/<agent>, done)."""
    if location == "inbox":
        task_file = work_dir / "inbox" / f"{task['id']}.yaml"
    elif location == "done":
        task_file = work_dir / "done" / f"{task['id']}.yaml"
    elif location.startswith("assigned/"):
        agent = location.split("/")[1]
        task_file = work_dir / "assigned" / agent / f"{task['id']}.yaml"
    else:
        raise ValueError(f"Invalid location: {location}")
    
    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task, f, default_flow_style=False, sort_keys=False)
    
    return task_file


def read_task(task_file: Path) -> dict[str, Any]:
    """Read task from file."""
    with open(task_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# ============================================================================
# Test Scenario 1: Simple Single-Agent Task
# ============================================================================


def test_simple_task_flow(temp_work_env: Path) -> None:
    """Test basic inbox → assigned → done flow for single agent."""
    work_dir = temp_work_env
    
    # Create task in inbox
    task = create_task(
        "2025-11-23T0800-test-agent-simple-task",
        "test-agent",
        title="Simple test task",
    )
    write_task(work_dir, "inbox", task)
    
    # Run assignment
    assigned = orchestrator.assign_tasks()
    assert assigned == 1
    
    # Verify task moved to assigned
    assigned_file = work_dir / "assigned" / "test-agent" / f"{task['id']}.yaml"
    assert assigned_file.exists()
    
    assigned_task = read_task(assigned_file)
    assert assigned_task["status"] == "assigned"
    assert "assigned_at" in assigned_task
    
    # Simulate agent processing - mark as in_progress
    assigned_task["status"] = "in_progress"
    assigned_task["started_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with open(assigned_file, "w", encoding="utf-8") as f:
        yaml.dump(assigned_task, f, default_flow_style=False, sort_keys=False)
    
    # Simulate agent completion - move to done
    assigned_task["status"] = "done"
    assigned_task["result"] = {
        "summary": "Task completed successfully",
        "artefacts": task["artefacts"],
        "completed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    done_file = work_dir / "done" / f"{task['id']}.yaml"
    with open(done_file, "w", encoding="utf-8") as f:
        yaml.dump(assigned_task, f, default_flow_style=False, sort_keys=False)
    assigned_file.unlink()
    
    # Verify task in done
    assert done_file.exists()
    assert not assigned_file.exists()
    
    done_task = read_task(done_file)
    assert done_task["status"] == "done"
    assert "result" in done_task


# ============================================================================
# Test Scenario 2: Sequential Workflow (Agent Handoff)
# ============================================================================


def test_sequential_workflow(temp_work_env: Path) -> None:
    """Test Agent A → Agent B via next_agent handoff."""
    work_dir = temp_work_env
    
    # Create initial task with handoff
    task = create_task(
        "2025-11-23T0900-test-agent-sequential-task",
        "test-agent",
        title="Sequential task with handoff",
    )
    done_file = write_task(work_dir, "done", task)
    
    # Add result with next_agent
    done_task = read_task(done_file)
    done_task["status"] = "done"
    done_task["result"] = {
        "summary": "Phase 1 complete",
        "artefacts": task["artefacts"],
        "next_agent": "test-agent-2",
        "next_task_title": "Phase 2: Follow-up processing",
        "next_artefacts": ["test/output/phase2.md"],
        "next_task_notes": ["Continue from phase 1"],
        "completed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    with open(done_file, "w", encoding="utf-8") as f:
        yaml.dump(done_task, f, default_flow_style=False, sort_keys=False)
    
    # Process completed tasks
    followups = orchestrator.process_completed_tasks()
    assert followups == 1
    
    # Verify follow-up task created in inbox
    inbox_files = list((work_dir / "inbox").glob("*.yaml"))
    assert len(inbox_files) == 1
    
    followup_task = read_task(inbox_files[0])
    assert followup_task["agent"] == "test-agent-2"
    assert followup_task["status"] == "new"
    assert followup_task["title"] == "Phase 2: Follow-up processing"
    assert followup_task["context"]["previous_agent"] == "test-agent"
    
    # Verify handoff log created
    handoff_log = work_dir / "collaboration" / "HANDOFFS.md"
    assert handoff_log.exists()
    handoff_content = handoff_log.read_text()
    assert "test-agent → test-agent-2" in handoff_content


# ============================================================================
# Test Scenario 3: Parallel Workflow
# ============================================================================


def test_parallel_workflow(temp_work_env: Path) -> None:
    """Test multiple agents working simultaneously."""
    work_dir = temp_work_env
    
    # Create multiple tasks for different agents
    tasks = [
        create_task("2025-11-23T1000-test-agent-parallel-1", "test-agent"),
        create_task("2025-11-23T1001-test-agent-2-parallel-2", "test-agent-2"),
        create_task("2025-11-23T1002-test-agent-3-parallel-3", "test-agent-3"),
    ]
    
    for task in tasks:
        write_task(work_dir, "inbox", task)
    
    # Run assignment
    assigned = orchestrator.assign_tasks()
    assert assigned == 3
    
    # Verify all tasks assigned to correct agents
    for task in tasks:
        agent = task["agent"]
        assigned_file = work_dir / "assigned" / agent / f"{task['id']}.yaml"
        assert assigned_file.exists()
        
        assigned_task = read_task(assigned_file)
        assert assigned_task["status"] == "assigned"
    
    # Update agent status
    orchestrator.update_agent_status()
    
    # Verify status dashboard
    status_file = work_dir / "collaboration" / "AGENT_STATUS.md"
    assert status_file.exists()
    status_content = status_file.read_text()
    assert "test-agent" in status_content
    assert "test-agent-2" in status_content
    assert "test-agent-3" in status_content


# ============================================================================
# Test Scenario 4: Convergent Workflow (Conflict Detection)
# ============================================================================


def test_conflict_detection(temp_work_env: Path) -> None:
    """Test detection of multiple agents targeting same artifact."""
    work_dir = temp_work_env
    
    shared_artifact = "test/output/shared_artifact.md"
    
    # Create two tasks targeting same artifact
    task1 = create_task(
        "2025-11-23T1100-test-agent-conflict-1",
        "test-agent",
        artefacts=[shared_artifact],
    )
    task2 = create_task(
        "2025-11-23T1101-test-agent-2-conflict-2",
        "test-agent-2",
        artefacts=[shared_artifact],
    )
    
    # Write both tasks as in_progress
    task1["status"] = "in_progress"
    task1["started_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    task2["status"] = "in_progress"
    task2["started_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    write_task(work_dir, "assigned/test-agent", task1)
    write_task(work_dir, "assigned/test-agent-2", task2)
    
    # Run conflict detection
    conflicts = orchestrator.detect_conflicts()
    assert conflicts == 1
    
    # Verify workflow log contains conflict warning
    workflow_log = work_dir / "collaboration" / "WORKFLOW_LOG.md"
    assert workflow_log.exists()
    log_content = workflow_log.read_text()
    assert "Conflict" in log_content
    assert shared_artifact in log_content


# ============================================================================
# Test Scenario 5: Timeout Detection
# ============================================================================


def test_timeout_detection(temp_work_env: Path) -> None:
    """Test detection of tasks stuck in in_progress."""
    work_dir = temp_work_env
    
    # Create task with old started_at timestamp
    task = create_task(
        "2025-11-23T1200-test-agent-timeout-task",
        "test-agent",
        status="in_progress",
    )
    
    # Set started_at to 3 hours ago (beyond 2 hour timeout)
    # Use format that orchestrator expects (with Z suffix)
    old_time = datetime.now(timezone.utc) - timedelta(hours=3)
    task["started_at"] = old_time.isoformat().replace("+00:00", "Z")
    
    write_task(work_dir, "assigned/test-agent", task)
    
    # Run timeout check
    timeouts = orchestrator.check_timeouts()
    assert timeouts == 1
    
    # Verify workflow log contains timeout warning
    workflow_log = work_dir / "collaboration" / "WORKFLOW_LOG.md"
    assert workflow_log.exists()
    log_content = workflow_log.read_text()
    assert "stalled" in log_content or "timeout" in log_content.lower()


# ============================================================================
# Test Scenario 6: Archive Execution
# ============================================================================


def test_archive_old_tasks(temp_work_env: Path) -> None:
    """Test archival of old completed tasks."""
    work_dir = temp_work_env
    
    # Create old task (31 days ago, beyond 30 day retention)
    old_date = (datetime.now(timezone.utc) - timedelta(days=31)).strftime("%Y-%m-%d")
    old_task_id = f"{old_date}T1300-test-agent-old-task"
    
    task = create_task(old_task_id, "test-agent", status="done")
    task["result"] = {
        "summary": "Old task completed",
        "artefacts": task["artefacts"],
        "completed_at": f"{old_date}T13:00:00Z",
    }
    
    done_file = write_task(work_dir, "done", task)
    assert done_file.exists()
    
    # Run archival
    archived = orchestrator.archive_old_tasks()
    assert archived == 1
    
    # Verify task moved to archive with year-month structure
    year_month = old_date[:7]  # YYYY-MM
    archive_file = work_dir / "archive" / year_month / f"{old_task_id}.yaml"
    assert archive_file.exists()
    assert not done_file.exists()


# ============================================================================
# Test Scenario 7: Error Handling - Invalid Schema
# ============================================================================


def test_error_handling_invalid_schema(temp_work_env: Path) -> None:
    """Test handling of invalid task files."""
    work_dir = temp_work_env
    
    # Create task with missing required field (agent)
    invalid_task = {
        "id": "2025-11-23T1400-invalid-task",
        "status": "new",
        "artefacts": ["test/output/invalid.md"],
    }
    
    write_task(work_dir, "inbox", invalid_task)
    
    # Run assignment - should log error but not crash
    assigned = orchestrator.assign_tasks()
    assert assigned == 0  # Task not assigned due to missing agent
    
    # Verify task still in inbox
    inbox_file = work_dir / "inbox" / "2025-11-23T1400-invalid-task.yaml"
    assert inbox_file.exists()
    
    # Verify workflow log contains warning
    workflow_log = work_dir / "collaboration" / "WORKFLOW_LOG.md"
    assert workflow_log.exists()
    log_content = workflow_log.read_text()
    assert "missing 'agent'" in log_content


# ============================================================================
# Test Scenario 8: Error Handling - Missing Agent Directory
# ============================================================================


def test_error_handling_missing_agent(temp_work_env: Path) -> None:
    """Test handling of tasks for non-existent agents."""
    work_dir = temp_work_env
    
    # Create task for non-existent agent
    task = create_task(
        "2025-11-23T1500-nonexistent-agent-task",
        "nonexistent-agent",
    )
    
    write_task(work_dir, "inbox", task)
    
    # Run assignment - should log error but not crash
    assigned = orchestrator.assign_tasks()
    assert assigned == 0  # Task not assigned due to unknown agent
    
    # Verify task still in inbox
    inbox_file = work_dir / "inbox" / f"{task['id']}.yaml"
    assert inbox_file.exists()
    
    # Verify workflow log contains error
    workflow_log = work_dir / "collaboration" / "WORKFLOW_LOG.md"
    assert workflow_log.exists()
    log_content = workflow_log.read_text()
    assert "Unknown agent" in log_content


# ============================================================================
# Integration Test: Full Orchestrator Cycle
# ============================================================================


def test_full_orchestrator_cycle(temp_work_env: Path) -> None:
    """Test complete orchestrator cycle with all functions."""
    work_dir = temp_work_env
    
    # Setup: Create tasks in inbox
    task1 = create_task("2025-11-23T1600-test-agent-cycle-1", "test-agent")
    task2 = create_task("2025-11-23T1601-test-agent-2-cycle-2", "test-agent-2")
    write_task(work_dir, "inbox", task1)
    write_task(work_dir, "inbox", task2)
    
    # Run full cycle using main() to get complete behavior
    start_time = time.time()
    
    orchestrator.main()
    
    cycle_time = time.time() - start_time
    
    # Verify cycle completed quickly (should be <5 seconds for test environment)
    assert cycle_time < 5.0
    
    # Verify tasks were processed (both assigned)
    assigned_files = list((work_dir / "assigned" / "test-agent").glob("*.yaml"))
    assigned_files.extend(list((work_dir / "assigned" / "test-agent-2").glob("*.yaml")))
    assert len(assigned_files) == 2
    
    # Verify collaboration artifacts created
    assert (work_dir / "collaboration" / "AGENT_STATUS.md").exists()
    assert (work_dir / "collaboration" / "WORKFLOW_LOG.md").exists()
    
    # Verify workflow log has cycle summary
    workflow_log = work_dir / "collaboration" / "WORKFLOW_LOG.md"
    log_content = workflow_log.read_text()
    assert "Coordinator cycle" in log_content


# ============================================================================
# Performance Test: Orchestrator Cycle Time
# ============================================================================


@pytest.mark.timeout(60)
def test_orchestrator_performance(temp_work_env: Path) -> None:
    """Test orchestrator completes cycle in <60 seconds (acceptance criteria)."""
    work_dir = temp_work_env
    
    # Create multiple tasks to simulate load
    for i in range(10):
        task = create_task(
            f"2025-11-23T{1700+i:04d}-test-agent-perf-{i}",
            "test-agent",
        )
        write_task(work_dir, "inbox", task)
    
    # Measure full cycle time
    start_time = time.time()
    
    orchestrator.assign_tasks()
    orchestrator.process_completed_tasks()
    orchestrator.check_timeouts()
    orchestrator.detect_conflicts()
    orchestrator.archive_old_tasks()
    orchestrator.update_agent_status()
    
    cycle_time = time.time() - start_time
    
    # Should complete well under 60 seconds
    assert cycle_time < 60.0
    print(f"\nOrchestrator cycle completed in {cycle_time:.2f} seconds")


# ============================================================================
# Coverage Test: All Orchestrator Functions
# ============================================================================


def test_orchestrator_function_coverage(temp_work_env: Path) -> None:
    """Verify all major orchestrator functions are exercised."""
    work_dir = temp_work_env
    
    # Test log_event
    orchestrator.log_event("Test event")
    workflow_log = work_dir / "collaboration" / "WORKFLOW_LOG.md"
    assert workflow_log.exists()
    
    # Test read_task / write_task
    task = create_task("2025-11-23T1800-test-coverage", "test-agent")
    task_file = write_task(work_dir, "inbox", task)
    read_task_data = orchestrator.read_task(task_file)
    assert read_task_data["id"] == task["id"]
    
    # Test assign_tasks
    assigned = orchestrator.assign_tasks()
    assert assigned >= 0
    
    # Test process_completed_tasks
    followups = orchestrator.process_completed_tasks()
    assert followups >= 0
    
    # Test check_timeouts
    timeouts = orchestrator.check_timeouts()
    assert timeouts >= 0
    
    # Test detect_conflicts
    conflicts = orchestrator.detect_conflicts()
    assert conflicts >= 0
    
    # Test update_agent_status
    orchestrator.update_agent_status()
    assert (work_dir / "collaboration" / "AGENT_STATUS.md").exists()
    
    # Test archive_old_tasks
    archived = orchestrator.archive_old_tasks()
    assert archived >= 0
    
    # Test log_handoff
    orchestrator.log_handoff("test-agent", "test-agent-2", ["test.md"], "test-id")
    handoff_log = work_dir / "collaboration" / "HANDOFFS.md"
    assert handoff_log.exists()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
