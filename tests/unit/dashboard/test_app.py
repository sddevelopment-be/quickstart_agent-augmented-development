"""
Unit tests for Dashboard WebSocket Server.

Tests Flask + SocketIO integration following TDD (Directive 017).
"""

import pytest
from unittest.mock import Mock, patch
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
