"""
Dashboard WebSocket Server for LLM Service.

Provides real-time monitoring of LLM operations via WebSocket connections.
Follows ADR-032: Real-Time Execution Dashboard.
"""

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit, Namespace
from flask_cors import CORS
from datetime import datetime, timezone
from typing import Dict, Optional, Any
import os
import secrets


def create_app(config: Optional[Dict[str, Any]] = None) -> tuple[Flask, SocketIO]:
    """
    Create and configure the Flask + SocketIO dashboard application.
    
    Args:
        config: Optional configuration dictionary to override defaults
        
    Returns:
        Tuple of (Flask app, SocketIO instance)
        
    Example:
        >>> app, socketio = create_app()
        >>> socketio.run(app, host='localhost', port=8080)
    """
    # Specify static folder for dashboard assets
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # Default configuration
    app.config['SECRET_KEY'] = os.environ.get('DASHBOARD_SECRET_KEY', secrets.token_hex(32))
    app.config['CORS_ORIGINS'] = ['http://localhost:*', 'http://127.0.0.1:*']
    
    # Override with custom config
    if config:
        app.config.update(config)
    
    # Enable CORS for localhost connections
    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS']
        }
    })
    
    # Initialize SocketIO
    socketio = SocketIO(
        app,
        cors_allowed_origins=app.config['CORS_ORIGINS'],
        async_mode='threading'
    )
    
    # Register routes
    register_routes(app)
    
    # Register WebSocket handlers
    register_socketio_handlers(socketio)
    
    return app, socketio


def register_routes(app: Flask) -> None:
    """
    Register HTTP REST API routes.
    
    Routes:
        GET / - Dashboard UI (serves index.html)
        GET /health - Health check endpoint
        GET /api/stats - Current dashboard statistics
        GET /api/tasks - Current task state (inbox/assigned/done)
    """
    
    @app.route('/')
    def index():
        """Serve dashboard UI."""
        return app.send_static_file('index.html')
    
    @app.route('/health')
    def health():
        """Health check endpoint for monitoring."""
        return jsonify({
            'status': 'healthy',
            'service': 'llm-service-dashboard',
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    @app.route('/api/stats')
    def stats():
        """
        Return current dashboard statistics.
        
        Returns:
            JSON with task counts and cost metrics
        """
        # TODO: Integrate with file watcher for real task counts
        return jsonify({
            'tasks': {
                'inbox': 0,
                'assigned': 0,
                'done': 0,
                'total': 0
            },
            'costs': {
                'today': 0.0,
                'month': 0.0,
                'total': 0.0
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    @app.route('/api/tasks')
    def tasks():
        """
        Return current task state across all workflow directories.
        
        Returns:
            JSON with tasks grouped by status (inbox/assigned/done)
        """
        # TODO: Integrate with file watcher for real task data
        return jsonify({
            'inbox': [],
            'assigned': {},
            'done': {},
            'timestamp': datetime.now(timezone.utc).isoformat()
        })


def register_socketio_handlers(socketio: SocketIO) -> None:
    """
    Register WebSocket event handlers.
    
    Handlers:
        - connect: Client connection event
        - disconnect: Client disconnection event
        - ping: Keep-alive ping from client
    """
    
    @socketio.on('connect', namespace='/dashboard')
    def handle_connect():
        """Handle client connection to dashboard namespace."""
        emit('connection_ack', {
            'message': 'Connected to dashboard',
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    @socketio.on('disconnect', namespace='/dashboard')
    def handle_disconnect():
        """Handle client disconnection."""
        # Log disconnection (could integrate with telemetry)
        pass
    
    @socketio.on('ping', namespace='/dashboard')
    def handle_ping():
        """Respond to client ping for keep-alive."""
        emit('pong', {
            'timestamp': datetime.now(timezone.utc).isoformat()
        })


# Convenience class for organized event emission
class DashboardNamespace(Namespace):
    """
    Namespace handler for /dashboard WebSocket connections.
    
    Events emitted by server:
        - task.created: New task added to inbox
        - task.assigned: Task assigned to agent
        - task.completed: Task completed by agent
        - cost.update: Cost metrics updated
        - telemetry.update: Real-time telemetry data
    """
    
    def on_connect(self):
        """Handle client connection."""
        emit('connection_ack', {
            'message': 'Connected to dashboard',
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
    
    def on_disconnect(self):
        """Handle client disconnection."""
        pass
    
    def on_ping(self):
        """Respond to ping for connection health."""
        emit('pong', {
            'timestamp': datetime.now(timezone.utc).isoformat()
        })


def run_dashboard(host: str = 'localhost', port: int = 8080, debug: bool = False) -> None:
    """
    Run the dashboard server.
    
    Args:
        host: Host to bind to (default: localhost)
        port: Port to bind to (default: 8080)
        debug: Enable debug mode (default: False)
        
    Example:
        >>> run_dashboard(host='0.0.0.0', port=5000, debug=True)
    """
    app, socketio = create_app()
    
    print(f"🚀 Dashboard starting at http://{host}:{port}")
    print(f"📡 WebSocket namespace: /dashboard")
    print(f"💚 Health check: http://{host}:{port}/health")
    
    socketio.run(app, host=host, port=port, debug=debug)


if __name__ == '__main__':
    # Allow running directly for development
    run_dashboard(debug=True)
