"""
Test stats endpoint integration with file watcher.

Validates that /api/stats returns actual task counts from file watcher.
"""

import sqlite3
import tempfile
from pathlib import Path

import yaml


class TestStatsFileWatcherIntegration:
    """Tests for stats endpoint file watcher integration."""

    def test_stats_returns_actual_task_counts(self):
        """Test: /api/stats returns real task counts from file watcher."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create directories
            inbox_dir = Path(tmpdir) / "inbox"
            assigned_dir = Path(tmpdir) / "assigned" / "test-agent"
            done_dir = Path(tmpdir) / "done" / "test-agent"

            for d in [inbox_dir, assigned_dir, done_dir]:
                d.mkdir(parents=True)

            # Create tasks in each status
            # 3 inbox tasks
            for i in range(3):
                task_file = inbox_dir / f"inbox-task-{i}.yaml"
                with open(task_file, "w") as f:
                    yaml.dump({"id": f"inbox-{i}", "status": "new"}, f)

            # 2 assigned tasks
            for i in range(2):
                task_file = assigned_dir / f"assigned-task-{i}.yaml"
                with open(task_file, "w") as f:
                    yaml.dump({"id": f"assigned-{i}", "status": "assigned"}, f)

            # 5 done tasks
            for i in range(5):
                task_file = done_dir / f"done-task-{i}.yaml"
                with open(task_file, "w") as f:
                    yaml.dump({"id": f"done-{i}", "status": "done"}, f)

            # Create watcher and app
            watcher = FileWatcher(watch_dir=tmpdir)
            app, socketio = create_app(config={"FILE_WATCHER": watcher})

            # Get stats
            client = app.test_client()
            response = client.get("/api/stats")

            assert response.status_code == 200
            data = response.get_json()

            # Should have actual task counts
            assert "tasks" in data
            tasks = data["tasks"]

            # Verify counts match actual files
            assert tasks["inbox"] == 3, f"Expected 3 inbox tasks, got {tasks['inbox']}"
            assert (
                tasks["assigned"] == 2
            ), f"Expected 2 assigned tasks, got {tasks['assigned']}"
            assert tasks["done"] == 5, f"Expected 5 done tasks, got {tasks['done']}"
            assert (
                tasks["total"] == 10
            ), f"Expected 10 total tasks, got {tasks['total']}"

    def test_stats_with_no_watcher_returns_zeros(self):
        """Test: /api/stats returns zeros when file watcher not configured."""
        from llm_service.dashboard.app import create_app

        # Create app without file watcher
        app, socketio = create_app()

        client = app.test_client()
        response = client.get("/api/stats")

        assert response.status_code == 200
        data = response.get_json()

        # Should return zero counts (no watcher)
        tasks = data["tasks"]
        assert tasks["inbox"] == 0
        assert tasks["assigned"] == 0
        assert tasks["done"] == 0
        assert tasks["total"] == 0

    def test_stats_includes_telemetry_costs(self):
        """Test: /api/stats includes cost metrics from telemetry."""
        from llm_service.dashboard.app import create_app

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create telemetry database with data
            db_path = Path(tmpdir) / "telemetry.db"
            self._create_test_db(db_path)

            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO invocations (
                        invocation_id, tool_name, model_name,
                        total_tokens, cost_usd, status
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                    ("test-inv-1", "test-tool", "test-model", 1000, 1.50, "success"),
                )

            # Create app with custom telemetry DB
            app, socketio = create_app(config={"TELEMETRY_DB": str(db_path)})

            client = app.test_client()
            response = client.get("/api/stats")

            assert response.status_code == 200
            data = response.get_json()

            # Should have cost data
            assert "costs" in data
            costs = data["costs"]
            assert costs["total"] == 1.50

    @staticmethod
    def _create_test_db(db_path: Path):
        """Helper: Create test database with schema."""
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
