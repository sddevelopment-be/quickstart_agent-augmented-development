"""
End-to-End Dashboard Startup Test.

Validates that the dashboard can start with all components integrated.
"""

import pytest
from pathlib import Path
import tempfile
import yaml


class TestDashboardStartup:
    """End-to-end tests for dashboard startup."""

    def test_dashboard_full_startup_with_all_components(self):
        """
        Test: Dashboard starts successfully with all components integrated.
        
        This test validates the complete fix for:
        - Task 11: CORS configuration
        - Task 12: File watcher integration
        - Task 13: Telemetry API integration (already done)
        """
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up test directories
            inbox_dir = Path(tmpdir) / 'inbox'
            inbox_dir.mkdir()
            
            # Create test task
            task_file = inbox_dir / 'startup-test-task.yaml'
            with open(task_file, 'w') as f:
                yaml.dump({
                    'id': 'startup-test-001',
                    'title': 'Startup Test Task',
                    'status': 'new'
                }, f)
            
            # Create telemetry DB path
            db_path = Path(tmpdir) / 'telemetry.db'
            
            # Initialize all components
            watcher = FileWatcher(watch_dir=tmpdir)
            app, socketio = create_app(config={
                "FILE_WATCHER": watcher,
                "TELEMETRY_DB": str(db_path),
                "CORS_ORIGINS": "*"
            })
            
            # Verify all components are configured
            assert app.config["FILE_WATCHER"] is not None
            assert app.config["TELEMETRY_API"] is not None
            assert app.config["CORS_ORIGINS"] == "*"
            
            # Test HTTP endpoints
            client = app.test_client()
            
            # Health check
            health_response = client.get('/health')
            assert health_response.status_code == 200
            assert health_response.json["status"] == "healthy"
            
            # Dashboard UI
            ui_response = client.get('/')
            assert ui_response.status_code == 200
            assert b'LLM Service Dashboard' in ui_response.data
            
            # Stats endpoint (with file watcher integration)
            stats_response = client.get('/api/stats')
            assert stats_response.status_code == 200
            stats_data = stats_response.json
            
            # Should have task counts from file watcher
            assert 'tasks' in stats_data
            assert stats_data['tasks']['inbox'] == 1
            
            # Should have cost data from telemetry
            assert 'costs' in stats_data
            assert stats_data['costs']['total'] == 0.0
            
            # Tasks endpoint
            tasks_response = client.get('/api/tasks')
            assert tasks_response.status_code == 200
            tasks_data = tasks_response.json
            assert len(tasks_data['inbox']) == 1
            assert tasks_data['inbox'][0]['id'] == 'startup-test-001'
            
            # WebSocket connection
            ws_client = socketio.test_client(app, namespace='/dashboard')
            assert ws_client.is_connected(namespace='/dashboard')
            
            # Should receive connection acknowledgment
            received = ws_client.get_received(namespace='/dashboard')
            assert len(received) > 0
            ack = [e for e in received if e['name'] == 'connection_ack']
            assert len(ack) > 0
            
            # Clean up
            ws_client.disconnect(namespace='/dashboard')

    def test_run_dashboard_function_integration(self):
        """
        Test: run_dashboard() function integrates all components correctly.
        
        This validates the pattern used in run_dashboard.py.
        """
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            inbox_dir = Path(tmpdir) / 'inbox'
            inbox_dir.mkdir()
            
            # Simulate run_dashboard() setup
            app, socketio = create_app()
            watcher = FileWatcher(watch_dir=tmpdir, socketio=socketio)
            app.config["FILE_WATCHER"] = watcher
            
            # Start watcher
            watcher.start()
            assert watcher.is_running
            
            # Test that everything works together
            client = app.test_client()
            
            # Health check should work
            response = client.get('/health')
            assert response.status_code == 200
            
            # Stats should work with watcher
            stats = client.get('/api/stats')
            assert stats.status_code == 200
            assert 'tasks' in stats.json
            
            # Clean up
            watcher.stop()
            assert not watcher.is_running

    def test_cors_configuration_for_production(self):
        """
        Test: CORS can be configured for production use.
        
        Validates Task 11: Fix Dashboard CORS Configuration.
        """
        from llm_service.dashboard.app import create_app
        
        # Production-like configuration
        prod_origins = [
            "https://dashboard.production.example.com",
            "https://app.production.example.com"
        ]
        
        app, socketio = create_app(config={
            "CORS_ORIGINS": prod_origins
        })
        
        # Verify configuration
        assert app.config["CORS_ORIGINS"] == prod_origins
        
        # WebSocket should work
        client = socketio.test_client(app, namespace='/dashboard')
        assert client.is_connected(namespace='/dashboard')
        client.disconnect(namespace='/dashboard')

    def test_all_api_endpoints_return_valid_json(self):
        """Test: All API endpoints return valid JSON responses."""
        from llm_service.dashboard.app import create_app
        from llm_service.dashboard.file_watcher import FileWatcher
        
        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = FileWatcher(watch_dir=tmpdir)
            app, socketio = create_app(config={"FILE_WATCHER": watcher})
            
            client = app.test_client()
            
            # Test all API endpoints
            endpoints = ['/health', '/api/stats', '/api/tasks', '/api/portfolio']
            
            for endpoint in endpoints:
                response = client.get(endpoint)
                assert response.status_code == 200, f"{endpoint} failed"
                
                # Should be valid JSON
                try:
                    data = response.get_json()
                    assert data is not None, f"{endpoint} returned no JSON"
                except Exception as e:
                    pytest.fail(f"{endpoint} returned invalid JSON: {e}")
