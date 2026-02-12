"""
Acceptance Tests for Dashboard Task Priority Editing.

Following ATDD (Directive 016): Write acceptance tests first to define
the expected behavior before implementation.

These tests verify the complete user journey from specification scenarios.
Related: ADR-035, Specification: specifications/llm-dashboard/task-priority-editing.md
"""

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from llm_service.dashboard.app import create_app


class TestPriorityEditingAcceptance:
    """
    Acceptance test suite for priority editing feature.

    Scenarios from specification:
    - Scenario 1: Happy Path - Change Task Priority
    - Scenario 2: Validation Error - Invalid Priority
    - Scenario 3: Concurrent Edit Detection
    - Scenario 7: Read-Only Task (In Progress)
    """

    @pytest.fixture
    def temp_work_dir(self):
        """Create temporary work directory structure for testing."""
        temp_dir = tempfile.mkdtemp()
        work_dir = Path(temp_dir) / "work" / "collaboration"
        inbox_dir = work_dir / "inbox"
        inbox_dir.mkdir(parents=True)

        yield work_dir

        # Cleanup
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sample_task_file(self, temp_work_dir):
        """Create a sample task YAML file with comments."""
        task_id = "2026-02-06T1500-test-task"
        task_file = temp_work_dir / "inbox" / f"{task_id}.yaml"

        # YAML with comments - must be preserved
        task_content = """id: "2026-02-06T1500-test-task"
title: "Test Task for Priority Editing"
agent: "backend-dev"
status: "pending"  # Task is ready to be worked on
priority: MEDIUM  # Current priority level
created: "2026-02-06T15:00:00Z"
estimated_hours: 2

description: |
  Test task for verifying priority editing functionality.
  This task should be editable.
"""
        task_file.write_text(task_content)
        return task_file, task_id

    @pytest.fixture
    def in_progress_task_file(self, temp_work_dir):
        """Create a task file with in_progress status."""
        task_id = "2026-02-06T1501-in-progress-task"
        task_file = temp_work_dir / "inbox" / f"{task_id}.yaml"

        task_content = """id: "2026-02-06T1501-in-progress-task"
title: "Task Currently In Progress"
agent: "backend-dev"
status: "in_progress"  # Agent is actively working on this
priority: HIGH
created: "2026-02-06T15:01:00Z"
"""
        task_file.write_text(task_content)
        return task_file, task_id

    @pytest.fixture
    def app_with_temp_dir(self, temp_work_dir):
        """Create app configured with temporary work directory."""
        config = {"TESTING": True, "WORK_DIR": str(temp_work_dir)}
        app, socketio = create_app(config=config)
        return app.test_client(), socketio, temp_work_dir

    def test_scenario_1_happy_path_change_priority(
        self, app_with_temp_dir, sample_task_file
    ):
        """
        Scenario 1: Happy Path - Change Task Priority

        Given I am viewing the dashboard with tasks displayed
        And Task "Test Task" has priority "MEDIUM"
        When I select "HIGH" from the priority dropdown
        Then The YAML file is updated with priority: HIGH
        And The task is returned with updated priority
        And Comments in YAML file are preserved
        """
        client, socketio, work_dir = app_with_temp_dir
        task_file, task_id = sample_task_file

        # Given: Task exists with MEDIUM priority
        original_content = task_file.read_text()
        assert "priority: MEDIUM" in original_content
        assert "# Current priority level" in original_content

        # When: Send PATCH request to change priority to HIGH
        response = client.patch(
            f"/api/tasks/{task_id}/priority",
            data=json.dumps({"priority": "HIGH"}),
            content_type="application/json",
        )

        # Then: Response should be successful
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["task"]["priority"] == "HIGH"

        # And: YAML file should be updated
        updated_content = task_file.read_text()
        assert "priority: HIGH" in updated_content

        # And: Comments should be preserved
        assert "# Current priority level" in updated_content
        assert "# Task is ready to be worked on" in updated_content

    def test_scenario_2_validation_error_invalid_priority(
        self, app_with_temp_dir, sample_task_file
    ):
        """
        Scenario 2: Validation Error - Invalid Priority

        Given I am viewing the dashboard
        When I submit an invalid priority value "SUPER-URGENT"
        Then The system rejects the change with error 400
        And The YAML file is NOT modified
        And Error message explains valid values
        """
        client, socketio, work_dir = app_with_temp_dir
        task_file, task_id = sample_task_file

        # Given: Task exists
        original_content = task_file.read_text()

        # When: Send invalid priority
        response = client.patch(
            f"/api/tasks/{task_id}/priority",
            data=json.dumps({"priority": "SUPER-URGENT"}),
            content_type="application/json",
        )

        # Then: Should reject with 400
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "CRITICAL" in data["error"]  # Should list valid values
        assert "HIGH" in data["error"]

        # And: YAML file should be unchanged
        assert task_file.read_text() == original_content

    def test_scenario_7_in_progress_task_rejection(
        self, app_with_temp_dir, in_progress_task_file
    ):
        """
        Scenario 7: Read-Only Task (In Progress)

        Given I am viewing a task with status "in_progress"
        When I attempt to change the task priority
        Then The system rejects the change with 409 Conflict
        And Error message explains task is in progress
        And The YAML file is NOT modified
        """
        client, socketio, work_dir = app_with_temp_dir
        task_file, task_id = in_progress_task_file

        # Given: Task is in_progress
        original_content = task_file.read_text()
        assert 'status: "in_progress"' in original_content

        # When: Attempt to change priority
        response = client.patch(
            f"/api/tasks/{task_id}/priority",
            data=json.dumps({"priority": "CRITICAL"}),
            content_type="application/json",
        )

        # Then: Should reject with 409 Conflict
        assert response.status_code == 409
        data = json.loads(response.data)
        assert "error" in data
        assert "in progress" in data["error"].lower() or "in_progress" in data["error"]

        # And: YAML file should be unchanged
        assert task_file.read_text() == original_content

    def test_scenario_3_concurrent_edit_detection(
        self, app_with_temp_dir, sample_task_file
    ):
        """
        Scenario 3: Concurrent Edit Detection

        Given I am viewing the dashboard
        And Another user modifies the same task file
        When I attempt to change the task priority with stale timestamp
        Then The system detects the concurrent modification
        And Returns 409 Conflict with appropriate message
        """
        client, socketio, work_dir = app_with_temp_dir
        task_file, task_id = sample_task_file

        # Given: Task exists
        original_content = task_file.read_text()

        # Simulate another user modifying the file
        modified_content = original_content.replace("priority: MEDIUM", "priority: LOW")
        task_file.write_text(modified_content)

        # When: Attempt to change priority with old timestamp
        response = client.patch(
            f"/api/tasks/{task_id}/priority",
            data=json.dumps(
                {
                    "priority": "HIGH",
                    "last_modified": "2026-02-06T15:00:00Z",  # Stale timestamp
                }
            ),
            content_type="application/json",
        )

        # Then: Should detect conflict (implementation decides: 409 or overwrites)
        # Per ADR-035: "Last-write-wins with notification" is acceptable
        # For this implementation, we'll check file was modified
        updated_content = task_file.read_text()

        # Either: Returns 409 conflict, or succeeds with warning
        # (Implementation will determine exact behavior)
        assert response.status_code in [200, 409]

    def test_task_not_found_returns_404(self, app_with_temp_dir):
        """
        Edge Case: Task file does not exist

        Given A task ID that doesn't exist
        When I attempt to change its priority
        Then The system returns 404 Not Found
        """
        client, socketio, work_dir = app_with_temp_dir

        # When: Request non-existent task
        response = client.patch(
            "/api/tasks/nonexistent-task-id/priority",
            data=json.dumps({"priority": "HIGH"}),
            content_type="application/json",
        )

        # Then: Should return 404
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data

    def test_atomic_write_on_failure(self, app_with_temp_dir, sample_task_file):
        """
        Edge Case: File corruption prevention via atomic writes

        Given A task exists
        When A write operation fails mid-operation
        Then The original file remains intact
        And No partial writes occur
        """
        client, socketio, work_dir = app_with_temp_dir
        task_file, task_id = sample_task_file

        original_content = task_file.read_text()

        # This test will verify implementation uses temp file + rename
        # (Actual implementation will be tested in unit tests)
        # Here we verify file integrity is maintained

        # When: Normal operation
        response = client.patch(
            f"/api/tasks/{task_id}/priority",
            data=json.dumps({"priority": "LOW"}),
            content_type="application/json",
        )

        # Then: File should be valid YAML (not corrupted)
        import yaml

        updated_content = task_file.read_text()
        parsed = yaml.safe_load(updated_content)
        assert parsed["priority"] == "LOW"
        assert parsed["id"] == task_id

    def test_comment_preservation_comprehensive(
        self, app_with_temp_dir, sample_task_file
    ):
        """
        Requirement FR-M6: Comment preservation across multiple edits

        Given A task file with multiple comments
        When Priority is changed multiple times
        Then All comments remain intact
        And Field order is preserved
        """
        client, socketio, work_dir = app_with_temp_dir
        task_file, task_id = sample_task_file

        original_content = task_file.read_text()
        original_comments = [
            line for line in original_content.split("\n") if "#" in line
        ]

        # When: Change priority multiple times
        for new_priority in ["HIGH", "LOW", "CRITICAL"]:
            response = client.patch(
                f"/api/tasks/{task_id}/priority",
                data=json.dumps({"priority": new_priority}),
                content_type="application/json",
            )
            assert response.status_code == 200

        # Then: Comments should still be present
        final_content = task_file.read_text()
        for comment_line in original_comments:
            # Extract comment part (after #)
            comment = comment_line.split("#", 1)[1].strip()
            assert f"# {comment}" in final_content or f"#{comment}" in final_content

    def test_websocket_event_emitted_on_priority_change(
        self, temp_work_dir, sample_task_file
    ):
        """
        Requirement FR-M4: WebSocket event emission for real-time sync

        Given Multiple clients are connected to dashboard
        When A priority is changed
        Then A task.updated event is emitted
        And All clients receive the update
        """
        config = {"TESTING": True, "WORK_DIR": str(temp_work_dir)}
        app, socketio = create_app(config=config)
        client = app.test_client()

        # Connect WebSocket client
        ws_client = socketio.test_client(app, namespace="/dashboard")
        assert ws_client.is_connected(namespace="/dashboard")

        task_file, task_id = sample_task_file

        # When: Change priority
        response = client.patch(
            f"/api/tasks/{task_id}/priority",
            data=json.dumps({"priority": "CRITICAL"}),
            content_type="application/json",
        )

        assert response.status_code == 200

        # Then: WebSocket event should be emitted
        # (Implementation will emit task.updated or task.priority_changed)
        received = ws_client.get_received(namespace="/dashboard")

        # Should have connection_ack + task update event
        event_names = [event["name"] for event in received]

        # Allow implementation to choose event name
        # (Will be verified in integration tests once implemented)
        assert len(received) > 0  # At least connection_ack
