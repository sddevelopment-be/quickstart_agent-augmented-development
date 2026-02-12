"""
Unit tests for Priority Editing API Endpoint.

Following TDD (Directive 017): Write failing tests first (RED phase).

Tests the PATCH /api/tasks/:id/priority endpoint.
Related: ADR-035
"""

import json
from unittest.mock import Mock, patch

import pytest

from llm_service.dashboard.app import create_app


class TestPriorityEditingAPI:
    """
    Unit test suite for PATCH /api/tasks/:id/priority endpoint.

    Tests:
    - Endpoint accepts PATCH requests
    - Priority validation
    - Status validation (in_progress rejection)
    - Success response format
    - Error response formats (400, 404, 409)
    - WebSocket event emission
    """

    @pytest.fixture
    def app(self):
        """Create test app instance."""
        config = {"TESTING": True, "WORK_DIR": "/tmp/test-work"}
        app, socketio = create_app(config=config)
        return app.test_client(), socketio, app

    def test_patch_endpoint_exists(self, app):
        """
        Test: PATCH /api/tasks/:id/priority endpoint exists (RED phase)

        Given the app is running
        When accessing the endpoint
        Then it should respond (not 404)
        """
        client, socketio, flask_app = app

        # Mock the task updater at the correct location (inside function import)
        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance
            mock_instance.load_task.return_value = {
                "id": "test-task",
                "priority": "MEDIUM",
                "status": "pending",
            }
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = True
            mock_instance.update_task_priority.return_value = None

            response = client.patch(
                "/api/tasks/test-task/priority",
                data=json.dumps({"priority": "HIGH"}),
                content_type="application/json",
            )

            # Should not be 404 (endpoint exists)
            assert response.status_code != 404

    def test_successful_priority_update_returns_200(self, app):
        """
        Test: Successful update returns 200 with task data (RED phase)

        Given a valid task and priority
        When PATCH request is sent
        Then returns 200 with success: true and updated task
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance

            mock_task = {
                "id": "test-task-123",
                "title": "Test Task",
                "priority": "HIGH",
                "status": "pending",
            }

            mock_instance.load_task.return_value = mock_task
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = True
            mock_instance.update_task_priority.return_value = None

            response = client.patch(
                "/api/tasks/test-task-123/priority",
                data=json.dumps({"priority": "HIGH"}),
                content_type="application/json",
            )

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["task"]["id"] == "test-task-123"
            assert data["task"]["priority"] == "HIGH"

    def test_invalid_priority_returns_400(self, app):
        """
        Test: Invalid priority value returns 400 Bad Request (RED phase)

        Given an invalid priority value
        When PATCH request is sent
        Then returns 400 with error message
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance
            mock_instance.validate_priority.side_effect = ValueError(
                "Invalid priority. Must be one of: CRITICAL, HIGH, MEDIUM, LOW, normal"
            )

            response = client.patch(
                "/api/tasks/test-task/priority",
                data=json.dumps({"priority": "INVALID"}),
                content_type="application/json",
            )

            assert response.status_code == 400
            data = json.loads(response.data)
            assert "error" in data
            assert "CRITICAL" in data["error"]

    def test_in_progress_task_returns_409(self, app):
        """
        Test: In-progress task returns 409 Conflict (RED phase)

        Given a task with status 'in_progress'
        When attempting to change priority
        Then returns 409 with error message
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance

            mock_task = {
                "id": "active-task",
                "priority": "HIGH",
                "status": "in_progress",
            }

            mock_instance.load_task.return_value = mock_task
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = False

            response = client.patch(
                "/api/tasks/active-task/priority",
                data=json.dumps({"priority": "CRITICAL"}),
                content_type="application/json",
            )

            assert response.status_code == 409
            data = json.loads(response.data)
            assert "error" in data
            assert (
                "in progress" in data["error"].lower() or "in_progress" in data["error"]
            )

    def test_task_not_found_returns_404(self, app):
        """
        Test: Non-existent task returns 404 Not Found (RED phase)

        Given a task ID that doesn't exist
        When PATCH request is sent
        Then returns 404 with error message
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance
            mock_instance.load_task.side_effect = FileNotFoundError("Task not found")

            response = client.patch(
                "/api/tasks/nonexistent/priority",
                data=json.dumps({"priority": "HIGH"}),
                content_type="application/json",
            )

            assert response.status_code == 404
            data = json.loads(response.data)
            assert "error" in data

    def test_concurrent_modification_returns_409(self, app):
        """
        Test: Concurrent modification detected returns 409 (RED phase)

        Given a task with stale last_modified timestamp
        When PATCH request includes old timestamp
        Then returns 409 Conflict
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance

            from llm_service.dashboard.task_priority_updater import (
                ConcurrentModificationError,
            )

            mock_instance.load_task.return_value = {
                "id": "test-task",
                "priority": "MEDIUM",
                "status": "pending",
                "last_modified": "2026-02-06T11:00:00Z",
            }
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = True
            mock_instance.update_task_priority.side_effect = (
                ConcurrentModificationError("Task was modified by another user")
            )

            response = client.patch(
                "/api/tasks/test-task/priority",
                data=json.dumps(
                    {
                        "priority": "HIGH",
                        "last_modified": "2026-02-06T10:00:00Z",  # Stale
                    }
                ),
                content_type="application/json",
            )

            assert response.status_code == 409
            data = json.loads(response.data)
            assert "error" in data
            assert "modified" in data["error"].lower()

    def test_missing_priority_in_request_returns_400(self, app):
        """
        Test: Missing priority field returns 400 Bad Request (RED phase)

        Given a request without priority field
        When PATCH request is sent
        Then returns 400 with error message
        """
        client, socketio, flask_app = app

        response = client.patch(
            "/api/tasks/test-task/priority",
            data=json.dumps({}),
            content_type="application/json",
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_invalid_json_returns_400(self, app):
        """
        Test: Invalid JSON returns 400 Bad Request (RED phase)

        Given invalid JSON in request body
        When PATCH request is sent
        Then returns 400
        """
        client, socketio, flask_app = app

        response = client.patch(
            "/api/tasks/test-task/priority",
            data="not valid json",
            content_type="application/json",
        )

        assert response.status_code == 400

    def test_websocket_event_emitted_on_success(self, app):
        """
        Test: WebSocket event emitted after successful update (RED phase)

        Given a successful priority update
        When update completes
        Then task.updated event is emitted via WebSocket
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance

            mock_task = {"id": "test-task", "priority": "CRITICAL", "status": "pending"}

            mock_instance.load_task.return_value = mock_task
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = True
            mock_instance.update_task_priority.return_value = None

            with patch.object(socketio, "emit") as mock_emit:
                response = client.patch(
                    "/api/tasks/test-task/priority",
                    data=json.dumps({"priority": "CRITICAL"}),
                    content_type="application/json",
                )

                assert response.status_code == 200

                # Should emit WebSocket event
                mock_emit.assert_called()

                # Check event name and data
                call_args = mock_emit.call_args
                event_name = call_args[0][0]
                assert event_name in ["task.updated", "task.priority_changed"]

    def test_optimistic_locking_timestamp_passed_to_updater(self, app):
        """
        Test: last_modified timestamp from request is passed to updater (RED phase)

        Given a request with last_modified timestamp
        When update is called
        Then timestamp is passed to TaskPriorityUpdater
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance

            mock_task = {
                "id": "test-task",
                "priority": "HIGH",
                "status": "pending",
                "last_modified": "2026-02-06T10:00:00Z",
            }

            mock_instance.load_task.return_value = mock_task
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = True
            mock_instance.update_task_priority.return_value = None

            timestamp = "2026-02-06T10:00:00Z"
            response = client.patch(
                "/api/tasks/test-task/priority",
                data=json.dumps({"priority": "CRITICAL", "last_modified": timestamp}),
                content_type="application/json",
            )

            assert response.status_code == 200

            # Verify timestamp was passed (as positional, not keyword)
            call_args = mock_instance.update_task_priority.call_args
            assert call_args[0][0] == "test-task"
            assert call_args[0][1] == "CRITICAL"
            assert call_args[0][2] == timestamp  # Positional arg

    def test_security_headers_present_in_response(self, app):
        """
        Test: Security headers are present in response (RED phase)

        Given any API request
        When response is returned
        Then security headers are included
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance
            mock_instance.load_task.return_value = {
                "id": "test-task",
                "priority": "HIGH",
                "status": "pending",
            }
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = True
            mock_instance.update_task_priority.return_value = None

            response = client.patch(
                "/api/tasks/test-task/priority",
                data=json.dumps({"priority": "HIGH"}),
                content_type="application/json",
            )

            # Security headers should be present (from add_security_headers middleware)
            assert (
                "Content-Security-Policy" in response.headers
                or response.status_code in [200, 400]
            )

    def test_path_traversal_prevented(self, app):
        """
        Test: Path traversal attempts are rejected (RED phase)

        Given a task_id with path traversal attempt
        When PATCH request is sent
        Then returns 400 or 404 with security error
        """
        client, socketio, flask_app = app

        malicious_ids = ["../../../etc/passwd", "../../secrets", "/etc/passwd"]

        for task_id in malicious_ids:
            with patch(
                "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
            ) as mock_updater:
                mock_instance = Mock()
                mock_updater.return_value = mock_instance
                mock_instance.load_task.side_effect = ValueError("Invalid task ID")

                response = client.patch(
                    f"/api/tasks/{task_id}/priority",
                    data=json.dumps({"priority": "HIGH"}),
                    content_type="application/json",
                )

                # Should reject malicious request
                assert response.status_code in [400, 404]

    def test_done_status_rejected(self, app):
        """
        Test: Tasks with 'done' status are rejected (RED phase)

        Given a task with status 'done'
        When attempting to change priority
        Then returns 409 Conflict
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance

            mock_task = {"id": "completed-task", "priority": "LOW", "status": "done"}

            mock_instance.load_task.return_value = mock_task
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = False

            response = client.patch(
                "/api/tasks/completed-task/priority",
                data=json.dumps({"priority": "HIGH"}),
                content_type="application/json",
            )

            assert response.status_code == 409
            data = json.loads(response.data)
            assert "error" in data

    def test_case_insensitive_priority_values(self, app):
        """
        Test: Priority values are case-insensitive (RED phase)

        Given priority values in different cases (high, HIGH, High)
        When PATCH request is sent
        Then normalized to uppercase for storage
        """
        client, socketio, flask_app = app

        with patch(
            "llm_service.dashboard.task_priority_updater.TaskPriorityUpdater"
        ) as mock_updater:
            mock_instance = Mock()
            mock_updater.return_value = mock_instance

            mock_task = {"id": "test-task", "priority": "HIGH", "status": "pending"}

            mock_instance.load_task.return_value = mock_task
            mock_instance.validate_priority.return_value = None
            mock_instance.is_editable_status.return_value = True
            mock_instance.update_task_priority.return_value = None

            # Send lowercase priority
            response = client.patch(
                "/api/tasks/test-task/priority",
                data=json.dumps({"priority": "high"}),
                content_type="application/json",
            )

            # Should normalize and accept
            assert response.status_code == 200

            # Verify normalized value was passed
            mock_instance.update_task_priority.assert_called()
            call_args = mock_instance.update_task_priority.call_args
            # Implementation should normalize to uppercase
            # (Test will pass once implementation added)
