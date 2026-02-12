"""
Integration tests for Dashboard End-to-End functionality.

Tests the full stack: Flask + SocketIO + File Watcher + Telemetry.
"""

import shutil
import sqlite3
import tempfile
import time
from pathlib import Path

import yaml


class TestDashboardIntegration:
    """Integration tests for complete dashboard functionality."""

    def test_dashboard_serves_ui(self):
        """Test: Dashboard serves HTML UI at root path."""
        from llm_service.dashboard.app import create_app

        app, _ = create_app()
        client = app.test_client()

        response = client.get("/")

        assert response.status_code == 200
        assert b"LLM Service Dashboard" in response.data

    def test_file_watcher_to_websocket_flow(self):
        """Test: File creation triggers WebSocket event emission."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir) / "inbox"
            inbox_dir.mkdir()

            # Create app and watcher
            app, socketio = create_app()
            watcher = FileWatcher(watch_dir=tmpdir, socketio=socketio)
            watcher.start()

            # Create WebSocket test client
            client = socketio.test_client(app, namespace="/dashboard")
            assert client.is_connected(namespace="/dashboard")

            # Create a task file
            task_file = inbox_dir / "test-task.yaml"
            task_data = {
                "id": "integration-test-task",
                "title": "Integration Test Task",
                "agent": "test-agent",
                "status": "new",
            }
            with open(task_file, "w") as f:
                yaml.dump(task_data, f)

            # Give watcher time to detect and emit
            time.sleep(0.3)

            # Check for emitted events
            received = client.get_received(namespace="/dashboard")

            watcher.stop()
            client.disconnect(namespace="/dashboard")

            # Verify event was emitted
            assert len(received) > 0
            task_events = [e for e in received if e["name"] == "task.created"]
            assert len(task_events) > 0

    def test_telemetry_to_dashboard_flow(self):
        """Test: Telemetry data flows to dashboard API."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.telemetry_api import TelemetryAPI

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "telemetry.db"

            # Create telemetry database with data
            self._create_test_db(db_path)
            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO invocations (
                        invocation_id, tool_name, model_name, 
                        total_tokens, cost_usd, status
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        "int-test-1",
                        "claude-code",
                        "claude-3.5-sonnet",
                        1000,
                        0.05,
                        "success",
                    ),
                )

            # Create app and telemetry API
            app, socketio = create_app()
            telemetry = TelemetryAPI(db_path=db_path, socketio=socketio)

            # Verify telemetry data is accessible
            total_cost = telemetry.get_total_cost()
            assert total_cost == 0.05

            # Verify dashboard dict
            dashboard_data = telemetry.to_dashboard_dict()
            assert dashboard_data["costs"]["total"] == 0.05

    def test_full_stack_dashboard_startup(self):
        """Test: Full dashboard can start with all components."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        from llm_service.dashboard.telemetry_api import TelemetryAPI

        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up directories
            inbox_dir = Path(tmpdir) / "inbox"
            inbox_dir.mkdir()

            db_path = Path(tmpdir) / "telemetry.db"
            self._create_test_db(db_path)

            # Create all components
            app, socketio = create_app()
            watcher = FileWatcher(watch_dir=tmpdir, socketio=socketio)
            telemetry = TelemetryAPI(db_path=db_path, socketio=socketio)

            # Start watcher
            watcher.start()

            # Test HTTP endpoints
            client = app.test_client()

            health_response = client.get("/health")
            assert health_response.status_code == 200

            stats_response = client.get("/api/stats")
            assert stats_response.status_code == 200

            tasks_response = client.get("/api/tasks")
            assert tasks_response.status_code == 200

            # Test WebSocket connection
            ws_client = socketio.test_client(app, namespace="/dashboard")
            assert ws_client.is_connected(namespace="/dashboard")

            # Clean up
            watcher.stop()
            ws_client.disconnect(namespace="/dashboard")

    def test_task_lifecycle_visualization(self):
        """Test: Task moving through workflow is visualized."""
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create workflow directories
            inbox_dir = Path(tmpdir) / "inbox"
            assigned_dir = Path(tmpdir) / "assigned" / "test-agent"
            done_dir = Path(tmpdir) / "done" / "test-agent"

            for dir_path in [inbox_dir, assigned_dir, done_dir]:
                dir_path.mkdir(parents=True)

            # Create watcher
            watcher = FileWatcher(watch_dir=tmpdir)

            # Create task in inbox
            task_file = inbox_dir / "lifecycle-task.yaml"
            task_data = {"id": "lifecycle-task", "status": "new"}
            with open(task_file, "w") as f:
                yaml.dump(task_data, f)

            # Get initial snapshot
            snapshot1 = watcher.get_task_snapshot()
            assert len(snapshot1["inbox"]) == 1
            assert snapshot1["inbox"][0]["id"] == "lifecycle-task"

            # Move to assigned
            shutil.move(str(task_file), str(assigned_dir / "lifecycle-task.yaml"))
            snapshot2 = watcher.get_task_snapshot()
            assert len(snapshot2["inbox"]) == 0
            assert "test-agent" in snapshot2["assigned"]
            assert len(snapshot2["assigned"]["test-agent"]) == 1

            # Move to done
            shutil.move(
                str(assigned_dir / "lifecycle-task.yaml"),
                str(done_dir / "lifecycle-task.yaml"),
            )
            snapshot3 = watcher.get_task_snapshot()
            assert "test-agent" in snapshot3["done"]
            assert len(snapshot3["done"]["test-agent"]) == 1

    @staticmethod
    def _create_test_db(db_path: Path):
        """Helper: Create test database with schema."""
        schema_path = (
            Path(__file__).parent.parent.parent
            / "src"
            / "llm_service"
            / "telemetry"
            / "schema.sql"
        )

        if schema_path.exists():
            with open(schema_path) as f:
                schema = f.read()
            with sqlite3.connect(db_path) as conn:
                conn.executescript(schema)
        else:
            # Minimal schema fallback
            minimal_schema = """
            CREATE TABLE IF NOT EXISTS invocations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invocation_id TEXT UNIQUE NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                agent_name TEXT,
                tool_name TEXT NOT NULL,
                model_name TEXT NOT NULL,
                prompt_tokens INTEGER DEFAULT 0,
                completion_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                cost_usd REAL DEFAULT 0.0,
                latency_ms INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                error_message TEXT,
                privacy_level TEXT DEFAULT 'metadata'
            );
            """
            with sqlite3.connect(db_path) as conn:
                conn.executescript(minimal_schema)
