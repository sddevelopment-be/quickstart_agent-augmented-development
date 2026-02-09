"""
Test File Watcher Integration with Dashboard.

Validates fix for Task: 2026-02-06T0423-backend-dev-dashboard-file-watcher-integration
Tests that file watcher is properly initialized and connected to API endpoints.
"""

from pathlib import Path
import tempfile
import yaml


class TestFileWatcherIntegration:
    """Tests for file watcher integration with dashboard."""

    def test_file_watcher_initialized_in_create_app(self):
        """Test: File watcher can be initialized via create_app config."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create app with file watcher in config
            watcher = FileWatcher(watch_dir=tmpdir)
            app, socketio = create_app(config={"FILE_WATCHER": watcher})
            
            # Verify watcher is accessible from app
            assert app.config.get("FILE_WATCHER") is not None
            assert isinstance(app.config["FILE_WATCHER"], FileWatcher)

    def test_api_tasks_endpoint_uses_file_watcher(self):
        """Test: /api/tasks endpoint returns data from file watcher."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create inbox with a task
            inbox_dir = Path(tmpdir) / 'inbox'
            inbox_dir.mkdir()
            
            task_file = inbox_dir / 'test-task.yaml'
            task_data = {
                'id': 'test-task-001',
                'title': 'Test Task',
                'status': 'new',
                'agent': 'test-agent'
            }
            with open(task_file, 'w') as f:
                yaml.dump(task_data, f)
            
            # Create app with watcher
            watcher = FileWatcher(watch_dir=tmpdir)
            app, socketio = create_app(config={"FILE_WATCHER": watcher})
            
            # Test API endpoint
            client = app.test_client()
            response = client.get('/api/tasks')
            
            assert response.status_code == 200
            data = response.get_json()
            
            # Should have task data from watcher
            assert 'inbox' in data
            assert len(data['inbox']) == 1
            assert data['inbox'][0]['id'] == 'test-task-001'

    def test_api_stats_uses_file_watcher_for_task_counts(self):
        """Test: /api/stats endpoint includes task counts from file watcher."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create tasks in different statuses
            inbox_dir = Path(tmpdir) / 'inbox'
            inbox_dir.mkdir()
            
            # Create 2 inbox tasks
            for i in range(2):
                task_file = inbox_dir / f'task-{i}.yaml'
                with open(task_file, 'w') as f:
                    yaml.dump({'id': f'task-{i}', 'status': 'new'}, f)
            
            # Create watcher and app
            watcher = FileWatcher(watch_dir=tmpdir)
            app, socketio = create_app(config={"FILE_WATCHER": watcher})
            
            # Get stats
            client = app.test_client()
            response = client.get('/api/stats')
            
            assert response.status_code == 200
            data = response.get_json()
            
            # Should have tasks data from file watcher
            assert 'tasks' in data
            assert 'inbox' in data['tasks']
            assert 'assigned' in data['tasks']
            assert 'done' in data['tasks']

    def test_file_watcher_without_socketio_works(self):
        """Test: File watcher can function without SocketIO (for testing)."""
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir) / 'inbox'
            inbox_dir.mkdir()
            
            # Create watcher without socketio
            watcher = FileWatcher(watch_dir=tmpdir, socketio=None)
            
            # Should still be able to get snapshots
            snapshot = watcher.get_task_snapshot()
            assert 'inbox' in snapshot
            assert 'assigned' in snapshot
            assert 'done' in snapshot

    def test_run_dashboard_initializes_file_watcher(self):
        """Test: run_dashboard() properly initializes file watcher."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # This tests the pattern used in run_dashboard()
            app, socketio = create_app()
            watcher = FileWatcher(watch_dir=tmpdir, socketio=socketio)
            app.config["FILE_WATCHER"] = watcher
            
            # Verify watcher is configured correctly
            assert app.config["FILE_WATCHER"] is not None
            assert app.config["FILE_WATCHER"].socketio is socketio
            assert not watcher.is_running  # Not started yet
            
            # Start and stop watcher
            watcher.start()
            assert watcher.is_running
            
            watcher.stop()
            assert not watcher.is_running
