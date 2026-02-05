"""
Dashboard module for real-time LLM service monitoring.

Provides:
- Flask + SocketIO server for WebSocket connections
- File watcher for YAML task monitoring
- Telemetry API for cost/metrics queries
- Real-time event emission to connected clients
"""

__version__ = "0.1.0"

from .app import create_app, run_dashboard

__all__ = ['create_app', 'run_dashboard']
