"""
Acceptance tests for orphan task assignment feature.

Implements ATDD for SPEC-DASH-008: Orphan Task Assignment.
Tests the PATCH /api/tasks/:task_id/specification endpoint.

Related:
- Specification: specifications/initiatives/dashboard-enhancements/orphan-task-assignment.md
- ADR-035: Dashboard Task Priority Editing (patterns reused)
- Feature: FEAT-DASH-008-03: YAML File Update with Comment Preservation

Acceptance Criteria:
- AC1: Assign Orphan Task to Feature
- AC2: Prevent Assignment of In-Progress Tasks
- AC3: Handle Concurrent Edit Conflict
- AC4: Validate Specification Path
- AC5: Handle Missing Specification File
"""

import json
import time
from datetime import datetime, timezone

import pytest
from ruamel.yaml import YAML

from src.llm_service.dashboard.app import create_app


@pytest.fixture
def temp_work_dir(tmp_path):
    """Create temporary work directory structure for testing."""
    # Create work directory structure
    work_dir = tmp_path / "work" / "collaboration"
    inbox = work_dir / "inbox"
    assigned = work_dir / "assigned" / "python-pedro"
    done = work_dir / "done" / "python-pedro"

    inbox.mkdir(parents=True)
    assigned.mkdir(parents=True)
    done.mkdir(parents=True)

    return work_dir


@pytest.fixture
def temp_spec_dir(tmp_path):
    """Create temporary specifications directory for testing."""
    spec_dir = tmp_path / "specifications" / "llm-service"
    spec_dir.mkdir(parents=True)

    # Create a sample specification file with frontmatter
    spec_file = spec_dir / "api-hardening.md"
    spec_content = """---
id: SPEC-API-HARDENING
title: API Hardening and Rate Limiting
version: 1.0.0
status: READY_FOR_PLANNING
---

# API Hardening and Rate Limiting

## Features

### Rate Limiting
Implement rate limiting to prevent API abuse.

### Input Validation
Add comprehensive input validation.
"""
    spec_file.write_text(spec_content, encoding="utf-8")

    return tmp_path / "specifications"


@pytest.fixture
def app_client(temp_work_dir, temp_spec_dir, tmp_path):
    """Create Flask test client with proper configuration."""
    config = {
        "TESTING": True,
        "WORK_DIR": str(temp_work_dir),
        "SPEC_DIR": str(temp_spec_dir),
        "REPO_ROOT": str(tmp_path),
    }

    app, socketio = create_app(config)

    # Create test client
    with app.test_client() as client:
        yield client, app, socketio


@pytest.fixture
def orphan_task_file(temp_work_dir):
    """Create an orphan task YAML file for testing."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False

    task_id = "2026-02-09T2000-test-orphan-task"
    task_file = temp_work_dir / "inbox" / f"{task_id}.yaml"

    # Task data with comments
    task_data = {
        "id": task_id,
        "agent": "python-pedro",
        "status": "pending",
        "priority": "high",
        "phase": "planning",
        "title": "Implement rate limiting",
        "description": "Add rate limiting to API endpoints",
        "created": "2026-02-09 20:00:00+00:00",
        "created_by": "planning-petra",
        "estimated_hours": 2,
    }

    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task_data, f)

    # Add comment manually (ruamel.yaml programmatic comment API is complex)
    content = task_file.read_text(encoding="utf-8")
    content = "# Task: Implement rate limiting\n" + content
    task_file.write_text(content, encoding="utf-8")

    return task_file, task_id


@pytest.fixture
def in_progress_task_file(temp_work_dir):
    """Create a task with in_progress status for testing."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False

    task_id = "2026-02-09T2001-in-progress-task"
    task_file = temp_work_dir / "assigned" / "python-pedro" / f"{task_id}.yaml"

    task_data = {
        "id": task_id,
        "agent": "python-pedro",
        "status": "in_progress",
        "priority": "high",
        "phase": "implementation",
        "title": "Active development task",
        "description": "Task currently being worked on",
        "created": "2026-02-09 20:01:00+00:00",
        "created_by": "planning-petra",
        "estimated_hours": 3,
    }

    with open(task_file, "w", encoding="utf-8") as f:
        yaml.dump(task_data, f)

    return task_file, task_id


class TestOrphanTaskAssignmentAcceptance:
    """Acceptance tests for orphan task assignment feature (SPEC-DASH-008)."""

    def test_ac1_assign_orphan_task_to_feature(
        self, app_client, orphan_task_file, temp_spec_dir
    ):
        """
        AC1: Assign Orphan Task to Feature

        Given I have an orphan task "Implement rate limiting"
        And I have a specification "specifications/llm-service/api-hardening.md" with feature "Rate Limiting"
        When I send PATCH /api/tasks/:task_id/specification with:
          {
            "specification": "specifications/llm-service/api-hardening.md",
            "feature": "Rate Limiting"
          }
        Then the response status is 200
        And the task YAML file contains:
          specification: specifications/llm-service/api-hardening.md
          feature: "Rate Limiting"
        And the YAML comments are preserved
        And a WebSocket event "task.assigned" is emitted
        """
        client, app, socketio = app_client
        task_file, task_id = orphan_task_file

        # Capture WebSocket events
        events_captured = []

        @socketio.on("task.assigned", namespace="/dashboard")
        def capture_assigned_event(data):
            events_captured.append(("task.assigned", data))

        @socketio.on("task.updated", namespace="/dashboard")
        def capture_updated_event(data):
            events_captured.append(("task.updated", data))

        # Read original content to verify comment preservation
        original_content = task_file.read_text(encoding="utf-8")
        assert "# Task: Implement rate limiting" in original_content

        # Send PATCH request
        response = client.patch(
            f"/api/tasks/{task_id}/specification",
            data=json.dumps(
                {
                    "specification": "specifications/llm-service/api-hardening.md",
                    "feature": "Rate Limiting",
                }
            ),
            content_type="application/json",
        )

        # Verify response status
        assert response.status_code == 200

        # Verify response data
        data = response.get_json()
        assert data["success"] is True
        assert "task" in data
        assert (
            data["task"]["specification"]
            == "specifications/llm-service/api-hardening.md"
        )
        assert data["task"]["feature"] == "Rate Limiting"

        # Verify task file was updated
        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            updated_task = yaml.load(f)

        assert (
            updated_task["specification"]
            == "specifications/llm-service/api-hardening.md"
        )
        assert updated_task["feature"] == "Rate Limiting"

        # Verify comments are preserved
        updated_content = task_file.read_text(encoding="utf-8")
        assert "# Task: Implement rate limiting" in updated_content

        # Note: WebSocket event verification would require socketio test client
        # For now, we verify the emission happens in unit tests

    def test_ac2_prevent_assignment_of_in_progress_tasks(
        self, app_client, in_progress_task_file, temp_spec_dir
    ):
        """
        AC2: Prevent Assignment of In-Progress Tasks

        Given I have a task with status: in_progress
        When I send PATCH /api/tasks/:task_id/specification
        Then the response status is 400
        And the error message is "Cannot assign tasks that are currently being worked on"
        """
        client, app, socketio = app_client
        task_file, task_id = in_progress_task_file

        # Send PATCH request
        response = client.patch(
            f"/api/tasks/{task_id}/specification",
            data=json.dumps(
                {
                    "specification": "specifications/llm-service/api-hardening.md",
                    "feature": "Rate Limiting",
                }
            ),
            content_type="application/json",
        )

        # Verify response status
        assert response.status_code == 400

        # Verify error message
        data = response.get_json()
        assert "error" in data
        assert "Cannot assign tasks" in data["error"]
        assert "in_progress" in data["error"] or "being worked on" in data["error"]

    def test_ac3_handle_concurrent_edit_conflict(
        self, app_client, orphan_task_file, temp_spec_dir
    ):
        """
        AC3: Handle Concurrent Edit Conflict

        Given I have an orphan task
        And another user modifies the task file
        When I send PATCH /api/tasks/:task_id/specification
        Then the response status is 409
        And the error message is "This task was modified by another user"
        """
        client, app, socketio = app_client
        task_file, task_id = orphan_task_file

        # Get current last_modified timestamp
        yaml = YAML()
        with open(task_file, encoding="utf-8") as f:
            task_data = yaml.load(f)

        old_last_modified = task_data.get("last_modified", "2026-02-09T20:00:00Z")

        # Simulate another user modifying the file
        time.sleep(0.1)  # Ensure different timestamp
        task_data["priority"] = "CRITICAL"
        task_data["last_modified"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        with open(task_file, "w", encoding="utf-8") as f:
            yaml.dump(task_data, f)

        # Send PATCH request with old last_modified
        response = client.patch(
            f"/api/tasks/{task_id}/specification",
            data=json.dumps(
                {
                    "specification": "specifications/llm-service/api-hardening.md",
                    "feature": "Rate Limiting",
                    "last_modified": old_last_modified,
                }
            ),
            content_type="application/json",
        )

        # Verify response status
        assert response.status_code == 409

        # Verify error message
        data = response.get_json()
        assert "error" in data
        assert "modified" in data["error"].lower()

    def test_ac4_validate_specification_path(self, app_client, orphan_task_file):
        """
        AC4: Validate Specification Path

        Given I have an orphan task
        When I send PATCH /api/tasks/:task_id/specification with:
          {
            "specification": "../../../etc/passwd"
          }
        Then the response status is 400
        And the error message is "Invalid specification path"
        """
        client, app, socketio = app_client
        task_file, task_id = orphan_task_file

        # Test path traversal attack
        response = client.patch(
            f"/api/tasks/{task_id}/specification",
            data=json.dumps({"specification": "../../../etc/passwd"}),
            content_type="application/json",
        )

        # Verify response status
        assert response.status_code == 400

        # Verify error message
        data = response.get_json()
        assert "error" in data
        assert "Invalid specification path" in data["error"]

    def test_ac5_handle_missing_specification_file(
        self, app_client, orphan_task_file, temp_spec_dir
    ):
        """
        AC5: Handle Missing Specification File

        Given I have an orphan task
        And the specification file "specifications/nonexistent.md" does not exist
        When I send PATCH /api/tasks/:task_id/specification with:
          {
            "specification": "specifications/nonexistent.md"
          }
        Then the response status is 400
        And the error message is "Specification file not found"
        """
        client, app, socketio = app_client
        task_file, task_id = orphan_task_file

        # Send request with non-existent specification
        response = client.patch(
            f"/api/tasks/{task_id}/specification",
            data=json.dumps({"specification": "specifications/nonexistent.md"}),
            content_type="application/json",
        )

        # Verify response status
        assert response.status_code == 400

        # Verify error message
        data = response.get_json()
        assert "error" in data
        assert (
            "not found" in data["error"].lower()
            or "does not exist" in data["error"].lower()
        )
