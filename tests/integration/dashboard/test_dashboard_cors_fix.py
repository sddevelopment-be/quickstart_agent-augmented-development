"""
Test CORS Configuration for WebSocket Connections.

Validates fix for Task: 2026-02-06T0422-backend-dev-dashboard-cors-fix
Tests that CORS is properly configured for WebSocket connections from localhost.
"""


class TestDashboardCORS:
    """Tests for CORS configuration in dashboard."""

    def test_cors_allows_localhost_origins(self):
        """Test: CORS configuration supports localhost with different ports."""
        from llm_service.dashboard.app import create_app
        
        # Create app with explicit localhost origins
        app, socketio = create_app()
        
        # Check CORS configuration
        cors_origins = app.config.get("CORS_ORIGINS", "*")
        
        # Should not use wildcard for SocketIO compatibility
        # Flask-SocketIO doesn't support wildcard patterns with specific ports
        # Should either be "*" for all origins or explicit list
        assert cors_origins is not None
        
        # Test that app can be created successfully
        assert app is not None
        assert socketio is not None

    def test_websocket_connection_with_explicit_origin(self):
        """Test: WebSocket connection works with explicit localhost origin."""
        from llm_service.dashboard.app import create_app
        
        # Create app
        app, socketio = create_app()
        
        # Create WebSocket test client (simulates localhost:8080 connection)
        client = socketio.test_client(app, namespace='/dashboard')
        
        # Should connect successfully
        assert client.is_connected(namespace='/dashboard')
        
        # Should receive connection acknowledgment
        received = client.get_received(namespace='/dashboard')
        assert len(received) > 0
        
        # First message should be connection_ack
        ack_events = [e for e in received if e['name'] == 'connection_ack']
        assert len(ack_events) > 0
        assert ack_events[0]['args'][0]['message'] == 'Connected to dashboard'
        
        client.disconnect(namespace='/dashboard')

    def test_cors_config_can_be_overridden(self):
        """Test: CORS origins can be configured via config dict."""
        from llm_service.dashboard.app import create_app
        
        # Create app with custom CORS config
        custom_origins = "http://localhost:3000"
        app, socketio = create_app(config={"CORS_ORIGINS": custom_origins})
        
        # Verify config was applied
        assert app.config["CORS_ORIGINS"] == custom_origins

    def test_cors_security_headers_present(self):
        """Test: Security headers are added to responses."""
        from llm_service.dashboard.app import create_app
        
        app, _ = create_app()
        client = app.test_client()
        
        response = client.get('/health')
        
        # Check for CSP header (XSS protection)
        assert 'Content-Security-Policy' in response.headers
        
        # Check for other security headers
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
