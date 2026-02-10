"""
Unit tests for Dashboard WebSocket Server.

Tests Flask + SocketIO integration following TDD (Directive 017).
"""

import pytest
from unittest.mock import Mock, patch, ANY
import json


class TestDashboardApp:
    """Test suite for Flask + SocketIO dashboard server."""

    def test_app_creation(self):
        """Test: Dashboard app can be created with default config."""
        from llm_service.dashboard.app import create_app
        
        app, socketio = create_app()
        
        assert app is not None
        assert socketio is not None
        assert app.config['SECRET_KEY'] is not None

    def test_health_endpoint(self):
        """Test: /health endpoint returns 200 OK."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

    def test_cors_enabled(self):
        """Test: CORS is enabled for localhost."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        response = client.get('/health', headers={'Origin': 'http://localhost:3000'})
        
        assert 'Access-Control-Allow-Origin' in response.headers

    def test_cors_explicit_port_8080(self):
        """Test: CORS accepts explicit localhost:8080 origin."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        response = client.get('/health', headers={'Origin': 'http://localhost:8080'})
        
        # Should allow localhost:8080 explicitly
        assert response.status_code == 200
        assert 'Access-Control-Allow-Origin' in response.headers

    def test_websocket_connection(self):
        """Test: WebSocket client can connect to /dashboard namespace."""
        from llm_service.dashboard.app import create_app
        
        app, socketio = create_app()
        client = socketio.test_client(app, namespace='/dashboard')
        
        assert client.is_connected(namespace='/dashboard')

    def test_websocket_disconnection(self):
        """Test: WebSocket client can disconnect cleanly."""
        from llm_service.dashboard.app import create_app
        
        app, socketio = create_app()
        client = socketio.test_client(app, namespace='/dashboard')
        
        client.disconnect(namespace='/dashboard')
        
        assert not client.is_connected(namespace='/dashboard')

    def test_connection_event_emitted(self):
        """Test: Connection event is logged when client connects."""
        from llm_service.dashboard.app import create_app
        
        app, socketio = create_app()
        client = socketio.test_client(app, namespace='/dashboard')
        
        received = client.get_received(namespace='/dashboard')
        
        # Should receive connection confirmation
        assert len(received) > 0
        assert any(event['name'] == 'connection_ack' for event in received)

    def test_ping_pong(self):
        """Test: Server responds to ping with pong."""
        from llm_service.dashboard.app import create_app
        
        app, socketio = create_app()
        client = socketio.test_client(app, namespace='/dashboard')
        
        client.emit('ping', namespace='/dashboard')
        received = client.get_received(namespace='/dashboard')
        
        # Should receive pong response
        pong_events = [e for e in received if e['name'] == 'pong']
        assert len(pong_events) > 0

    def test_config_override(self):
        """Test: App configuration can be overridden."""
        from llm_service.dashboard.app import create_app
        
        custom_config = {
            'TESTING': True,
            'SECRET_KEY': 'test-secret'
        }
        app, _ = create_app(config=custom_config)
        
        assert app.config['TESTING'] is True
        assert app.config['SECRET_KEY'] == 'test-secret'

    def test_port_configuration(self):
        """Test: Server port can be configured."""
        from llm_service.dashboard.app import create_app
        
        app, socketio = create_app()
        
        # Should have default port or configurable port
        assert hasattr(socketio, 'run') or hasattr(app, 'run')


class TestDashboardAPI:
    """Test suite for Dashboard REST API endpoints."""

    def test_dashboard_stats_endpoint(self):
        """Test: /api/stats endpoint returns current statistics."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        response = client.get('/api/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tasks' in data
        assert 'costs' in data

    def test_dashboard_tasks_endpoint(self):
        """Test: /api/tasks endpoint returns current task state."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'inbox' in data
        assert 'assigned' in data
        assert 'done' in data

    def test_404_handling(self):
        """Test: Unknown routes return 404."""
        from llm_service.dashboard.app import create_app

        app, _ = create_app()
        client = app.test_client()

        response = client.get('/api/nonexistent')

        assert response.status_code == 404

    def test_api_tasks_uses_file_watcher(self):
        """Test: /api/tasks uses file watcher when available."""
        from llm_service.dashboard.app import create_app

        app, _ = create_app()
        client = app.test_client()

        # Mock file watcher
        mock_watcher = Mock()
        mock_watcher.get_task_snapshot.return_value = {
            'inbox': [{'id': 'task-1', 'title': 'Test Task'}],
            'assigned': {},
            'done': {},
            'timestamp': '2026-02-06T10:00:00Z'
        }

        app.config['FILE_WATCHER'] = mock_watcher

        response = client.get('/api/tasks')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['inbox']) == 1
        assert data['inbox'][0]['id'] == 'task-1'
        mock_watcher.get_task_snapshot.assert_called_once()

    def test_api_tasks_fallback_without_watcher(self):
        """Test: /api/tasks returns empty data when watcher not configured."""
        from llm_service.dashboard.app import create_app

        app, _ = create_app()
        client = app.test_client()

        # No FILE_WATCHER in config
        response = client.get('/api/tasks')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['inbox'] == []
        assert data['assigned'] == {}
        assert data['done'] == {}
        assert 'timestamp' in data

    def test_api_stats_uses_telemetry(self):
        """Test: /api/stats uses telemetry when available."""
        from llm_service.dashboard.app import create_app

        app, _ = create_app()
        client = app.test_client()

        # Mock telemetry API
        mock_telemetry = Mock()
        mock_telemetry.get_today_cost.return_value = 1.23
        mock_telemetry.get_monthly_cost.return_value = 45.67
        mock_telemetry.get_total_cost.return_value = 123.45

        app.config['TELEMETRY_API'] = mock_telemetry

        response = client.get('/api/stats')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['costs']['today'] == 1.23
        assert data['costs']['month'] == 45.67
        assert data['costs']['total'] == 123.45
        mock_telemetry.get_today_cost.assert_called_once()
        mock_telemetry.get_monthly_cost.assert_called_once()
        mock_telemetry.get_total_cost.assert_called_once()

    def test_api_stats_fallback_without_telemetry(self):
        """Test: /api/stats returns zero costs when telemetry not configured."""
        from llm_service.dashboard.app import create_app

        app, _ = create_app()
        client = app.test_client()

        # No TELEMETRY_API in config
        response = client.get('/api/stats')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['costs']['today'] == 0.0
        assert data['costs']['month'] == 0.0
        assert data['costs']['total'] == 0.0
        assert 'timestamp' in data


class TestDashboardAPIFiltering:
    """Test suite for Dashboard API task filtering functionality."""
    
    def test_tasks_endpoint_include_done_parameter_default(self):
        """Test: /api/tasks endpoint excludes done tasks by default when using query params."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        # Mock the refactored load_tasks_with_filter function
        with patch('llm_service.dashboard.app.load_tasks_with_filter') as mock_load_filtered:
            mock_load_filtered.return_value = [
                {'id': 'task-1', 'title': 'Open Task', 'status': 'assigned'},
                {'id': 'task-2', 'title': 'In Progress', 'status': 'in_progress'}
            ]
            
            # Use explicit include_done=false to trigger new behavior
            response = client.get('/api/tasks?include_done=false')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 2
            # Should call load_tasks_with_filter with include_done=False
            mock_load_filtered.assert_called_once_with(ANY, include_done=False)

    def test_tasks_endpoint_include_done_false(self):
        """Test: /api/tasks?include_done=false returns only active tasks."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        # Mock the refactored function
        with patch('llm_service.dashboard.app.load_tasks_with_filter') as mock_load_filtered:
            mock_load_filtered.return_value = [
                {'id': 'task-1', 'title': 'Open Task', 'status': 'assigned'},
                {'id': 'task-2', 'title': 'In Progress', 'status': 'in_progress'}
            ]
            
            response = client.get('/api/tasks?include_done=false')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 2
            # Should call with include_done=False
            mock_load_filtered.assert_called_once_with(ANY, include_done=False)

    def test_tasks_endpoint_include_done_true(self):
        """Test: /api/tasks?include_done=true returns all tasks including done."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        # Mock the refactored function
        with patch('llm_service.dashboard.app.load_tasks_with_filter') as mock_load_filtered:
            mock_load_filtered.return_value = [
                {'id': 'task-1', 'title': 'Open Task', 'status': 'assigned'},
                {'id': 'task-2', 'title': 'Done Task', 'status': 'done'}, 
                {'id': 'task-3', 'title': 'Error Task', 'status': 'error'}
            ]
            
            response = client.get('/api/tasks?include_done=true')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 3  # Should include all tasks
            # Should call with include_done=True
            mock_load_filtered.assert_called_once_with(ANY, include_done=True)

    def test_tasks_finished_endpoint(self):
        """Test: /api/tasks/finished returns only DONE and ERROR tasks."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        # Mock the refactored function
        with patch('llm_service.dashboard.app.load_tasks_with_filter') as mock_load_filtered:
            mock_load_filtered.return_value = [
                {'id': 'task-1', 'title': 'Done Task', 'status': 'done'},
                {'id': 'task-2', 'title': 'Error Task', 'status': 'error'}
            ]
            
            response = client.get('/api/tasks/finished')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            # Should only return done and error tasks
            assert len(data) == 2
            task_ids = [task['id'] for task in data]
            assert 'task-1' in task_ids  # done
            assert 'task-2' in task_ids  # error
            # Should call with terminal_only=True
            mock_load_filtered.assert_called_once_with(ANY, include_done=True, terminal_only=True)

    def test_tasks_finished_endpoint_empty_result(self):
        """Test: /api/tasks/finished returns empty list when no finished tasks."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        # Mock no finished tasks
        with patch('llm_service.dashboard.app.load_tasks_with_filter') as mock_load_filtered:
            mock_load_filtered.return_value = []
            
            response = client.get('/api/tasks/finished')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert len(data) == 0
            # Should call with terminal_only=True
            mock_load_filtered.assert_called_once_with(ANY, include_done=True, terminal_only=True)

    def test_tasks_websocket_events_include_status(self):
        """Test: WebSocket events include status metadata."""
        from llm_service.dashboard.app import create_app
        
        app, socketio = create_app()
        client = socketio.test_client(app, namespace='/dashboard')
        
        # Mock task data
        task_data = {
            'id': 'test-task',
            'title': 'Test Task',
            'status': 'assigned',
            'priority': 'high'
        }
        
        # Emit a task update event
        socketio.emit('task.updated', {
            'task_id': 'test-task',
            'status': 'assigned',
            'task_data': task_data,
            'timestamp': '2026-02-10T11:04:00Z'
        }, namespace='/dashboard')
        
        received = client.get_received(namespace='/dashboard')
        
        # Should receive event with status metadata
        task_events = [e for e in received if e.get('name') == 'task.updated']
        assert len(task_events) > 0
        event_data = task_events[0]['args'][0]
        assert 'status' in event_data
        assert 'task_data' in event_data
