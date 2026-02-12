"""
Unit tests for Dashboard File Watcher.

Tests watchdog integration for YAML task file monitoring following TDD (Directive 017).
"""

import shutil
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock

import yaml


class TestFileWatcher:
    """Test suite for file watcher system."""

    def test_watcher_initialization(self):
        """Test: FileWatcher can be initialized with watch directory."""
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = FileWatcher(watch_dir=tmpdir)

            assert watcher is not None
            assert watcher.watch_dir == Path(tmpdir)

    def test_watcher_with_socketio(self):
        """Test: FileWatcher can accept SocketIO instance for event emission."""
        from llm_service.dashboard.file_watcher import FileWatcher

        mock_socketio = Mock()
        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = FileWatcher(watch_dir=tmpdir, socketio=mock_socketio)

            assert watcher.socketio is mock_socketio

    def test_watcher_start_stop(self):
        """Test: FileWatcher can be started and stopped."""
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = FileWatcher(watch_dir=tmpdir)

            watcher.start()
            assert watcher.is_running

            watcher.stop()
            assert not watcher.is_running

    def test_yaml_file_creation_detected(self):
        """Test: Watcher detects YAML file creation in inbox."""
        from llm_service.dashboard.file_watcher import FileWatcher

        mock_socketio = Mock()
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir) / "inbox"
            inbox_dir.mkdir()

            watcher = FileWatcher(watch_dir=tmpdir, socketio=mock_socketio)
            watcher.start()

            # Create a YAML file
            task_file = inbox_dir / "test-task.yaml"
            task_data = {
                "id": "test-task",
                "title": "Test Task",
                "agent": "test-agent",
                "status": "new",
            }
            with open(task_file, "w") as f:
                yaml.dump(task_data, f)

            # Give watcher time to detect
            time.sleep(0.2)

            watcher.stop()

            # Verify event was emitted
            assert mock_socketio.emit.called

    def test_yaml_file_moved_to_assigned(self):
        """Test: Watcher detects file move from inbox to assigned."""
        from llm_service.dashboard.file_watcher import FileWatcher

        mock_socketio = Mock()
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir) / "inbox"
            assigned_dir = Path(tmpdir) / "assigned" / "test-agent"
            inbox_dir.mkdir()
            assigned_dir.mkdir(parents=True)

            # Create initial file in inbox
            task_file = inbox_dir / "test-task.yaml"
            task_data = {"id": "test-task", "status": "new"}
            with open(task_file, "w") as f:
                yaml.dump(task_data, f)

            watcher = FileWatcher(watch_dir=tmpdir, socketio=mock_socketio)
            watcher.start()

            # Move file to assigned
            shutil.move(str(task_file), str(assigned_dir / "test-task.yaml"))

            time.sleep(0.2)
            watcher.stop()

            # Should emit task.assigned event
            assert mock_socketio.emit.called

    def test_parse_yaml_task_file(self):
        """Test: Watcher can parse YAML task file and extract metadata."""
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = FileWatcher(watch_dir=tmpdir)

            task_file = Path(tmpdir) / "test-task.yaml"
            task_data = {
                "id": "test-123",
                "title": "Test Task",
                "agent": "backend-dev",
                "status": "new",
                "priority": "HIGH",
            }
            with open(task_file, "w") as f:
                yaml.dump(task_data, f)

            parsed = watcher.parse_task_file(task_file)

            assert parsed["id"] == "test-123"
            assert parsed["title"] == "Test Task"
            assert parsed["agent"] == "backend-dev"
            assert parsed["status"] == "new"

    def test_malformed_yaml_handled_gracefully(self):
        """Test: Watcher handles malformed YAML without crashing."""
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = FileWatcher(watch_dir=tmpdir)

            task_file = Path(tmpdir) / "bad-task.yaml"
            with open(task_file, "w") as f:
                f.write("invalid: yaml: content: [[[")

            parsed = watcher.parse_task_file(task_file)

            # Should return None or empty dict for invalid YAML
            assert parsed is None or parsed == {}

    def test_non_yaml_files_ignored(self):
        """Test: Watcher ignores non-YAML files."""
        from llm_service.dashboard.file_watcher import FileWatcher

        mock_socketio = Mock()
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir) / "inbox"
            inbox_dir.mkdir()

            watcher = FileWatcher(watch_dir=tmpdir, socketio=mock_socketio)
            watcher.start()

            # Create non-YAML file
            text_file = inbox_dir / "readme.txt"
            text_file.write_text("This is not YAML")

            time.sleep(0.2)
            watcher.stop()

            # Should not emit events for non-YAML files
            if mock_socketio.emit.called:
                # If called, verify it wasn't for the .txt file
                call_args = mock_socketio.emit.call_args_list
                for call in call_args:
                    if len(call[0]) > 1:
                        data = call[0][1]
                        assert "readme.txt" not in str(data)

    def test_detect_task_status_from_directory(self):
        """Test: Watcher infers task status from directory (inbox/assigned/done)."""
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = FileWatcher(watch_dir=tmpdir)

            inbox_path = Path(tmpdir) / "inbox" / "task.yaml"
            assigned_path = Path(tmpdir) / "assigned" / "agent" / "task.yaml"
            done_path = Path(tmpdir) / "done" / "agent" / "task.yaml"

            assert watcher.infer_status_from_path(inbox_path) == "new"
            assert watcher.infer_status_from_path(assigned_path) == "assigned"
            assert watcher.infer_status_from_path(done_path) == "done"

    def test_get_current_task_snapshot(self):
        """Test: Watcher can return current snapshot of all tasks."""
        from llm_service.dashboard.file_watcher import FileWatcher

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create directory structure
            inbox_dir = Path(tmpdir) / "inbox"
            assigned_dir = Path(tmpdir) / "assigned" / "test-agent"
            done_dir = Path(tmpdir) / "done" / "test-agent"

            for dir_path in [inbox_dir, assigned_dir, done_dir]:
                dir_path.mkdir(parents=True)

            # Create sample tasks
            (inbox_dir / "task1.yaml").write_text(
                yaml.dump({"id": "task1", "status": "new"})
            )
            (assigned_dir / "task2.yaml").write_text(
                yaml.dump({"id": "task2", "status": "assigned"})
            )
            (done_dir / "task3.yaml").write_text(
                yaml.dump({"id": "task3", "status": "done"})
            )

            watcher = FileWatcher(watch_dir=tmpdir)
            snapshot = watcher.get_task_snapshot()

            assert "inbox" in snapshot
            assert "assigned" in snapshot
            assert "done" in snapshot
            assert len(snapshot["inbox"]) == 1
            assert len(snapshot["assigned"]) >= 1  # May have nested structure
            assert len(snapshot["done"]) >= 1
