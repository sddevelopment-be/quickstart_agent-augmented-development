"""
Dashboard WebSocket Server for LLM Service.

Provides real-time monitoring of LLM operations via WebSocket connections.
Follows ADR-032: Real-Time Execution Dashboard.
Implements ADR-036: Dashboard Markdown Rendering with XSS protection.
Implements ADR-035: Dashboard Task Priority Editing.
"""

from flask import Flask, jsonify, make_response, request
from flask_socketio import SocketIO, emit, Namespace
from flask_cors import CORS
from datetime import datetime, timezone
from typing import Dict, Optional, Any
import os
import secrets


def add_security_headers(response):
    """
    Add security headers to all HTTP responses.
    Implements Content Security Policy (CSP) per ADR-036.

    CSP Configuration:
    - default-src 'self': Only load resources from same origin
    - script-src 'self' cdn.jsdelivr.net cdn.socket.io: Allow scripts from CDNs
    - style-src 'self' 'unsafe-inline': Allow inline styles (for dynamic styling)
    - img-src 'self' https: data:: Allow HTTPS images and data URIs
    - connect-src 'self' ws: wss:: Allow WebSocket connections
    - font-src 'self': Only fonts from same origin
    - object-src 'none': Block plugins (Flash, Java, etc.)
    - base-uri 'self': Prevent base tag hijacking
    - form-action 'self': Prevent form submission to external sites
    - frame-ancestors 'none': Prevent clickjacking (no iframes)

    Args:
        response: Flask response object

    Returns:
        Modified response with security headers
    """
    # Content Security Policy (XSS protection)
    csp = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net https://cdn.socket.io; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' https: data:; "
        "connect-src 'self' ws: wss:; "
        "font-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers["Content-Security-Policy"] = csp

    # Additional security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


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
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    # Default configuration
    app.config["SECRET_KEY"] = os.environ.get(
        "DASHBOARD_SECRET_KEY", secrets.token_hex(32)
    )
    # CORS origins: Flask-SocketIO doesn't support wildcard ports, use explicit list or '*'
    # For development: allow all origins. For production: set explicit list via config
    app.config["CORS_ORIGINS"] = os.environ.get("DASHBOARD_CORS_ORIGINS", "*")

    # Override with custom config
    if config:
        app.config.update(config)

    # Enable CORS for localhost connections
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Initialize SocketIO
    socketio = SocketIO(
        app, cors_allowed_origins=app.config["CORS_ORIGINS"], async_mode="threading"
    )

    # Store socketio reference in app for endpoint access
    app.socketio = socketio

    # Initialize TelemetryAPI
    from .telemetry_api import TelemetryAPI

    telemetry_db = app.config.get("TELEMETRY_DB", "telemetry.db")
    telemetry = TelemetryAPI(telemetry_db, socketio)
    app.config["TELEMETRY_API"] = telemetry

    # Register security headers middleware (ADR-036)
    app.after_request(add_security_headers)

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

    @app.route("/")
    def index():
        """Serve dashboard UI."""
        return app.send_static_file("index.html")

    @app.route("/health")
    def health():
        """Health check endpoint for monitoring."""
        return jsonify(
            {
                "status": "healthy",
                "service": "llm-service-dashboard",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.route("/api/stats")
    def stats():
        """
        Return current dashboard statistics.

        Returns:
            JSON with task counts and cost metrics
        """
        # Get telemetry API
        telemetry = app.config.get("TELEMETRY_API")

        # Prepare cost data
        costs = {"today": 0.0, "month": 0.0, "total": 0.0}

        if telemetry:
            costs["today"] = telemetry.get_today_cost()
            costs["month"] = telemetry.get_monthly_cost()
            costs["total"] = telemetry.get_total_cost()

        # TODO: Integrate with file watcher for real task counts
        return jsonify(
            {
                "tasks": {"inbox": 0, "assigned": 0, "done": 0, "total": 0},
                "costs": costs,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.route("/api/tasks")
    def tasks():
        """
        Return current task state across all workflow directories.

        Returns:
            JSON with tasks grouped by status (inbox/assigned/done)
        """
        # Get task snapshot from file watcher
        watcher = app.config.get("FILE_WATCHER")
        if watcher:
            return jsonify(watcher.get_task_snapshot())

        # Fallback if watcher not initialized
        return jsonify(
            {
                "inbox": [],
                "assigned": {},
                "done": {},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.route("/api/portfolio")
    def portfolio():
        """
        Return portfolio view with initiatives, features, and tasks.
        
        Implements ADR-037: Dashboard Initiative Tracking.
        
        Returns:
            JSON with initiative hierarchy and progress:
            {
                "initiatives": [
                    {
                        "id": "spec-id",
                        "title": "Initiative Title",
                        "status": "in_progress",
                        "priority": "HIGH",
                        "progress": 65,
                        "features": [
                            {
                                "id": "feat-001",
                                "title": "Feature Title",
                                "status": "in_progress",
                                "progress": 75,
                                "tasks": [...]
                            }
                        ]
                    }
                ],
                "orphans": [...]
            }
        """
        from .spec_parser import SpecificationParser
        from .task_linker import TaskLinker
        from .progress_calculator import ProgressCalculator
        
        # Get directories from config
        spec_dir = app.config.get("SPEC_DIR", "specifications")
        work_dir = app.config.get("WORK_DIR", "work/collaboration")
        
        # Initialize components
        parser = SpecificationParser(spec_dir)
        linker = TaskLinker(work_dir, spec_dir=spec_dir)
        calculator = ProgressCalculator()
        
        # Parse all specifications
        specifications = parser.scan_specifications(spec_dir)
        
        # Group tasks by specification
        task_groups = linker.group_by_specification()
        
        # Build initiative list
        initiatives = []
        
        for spec_meta in specifications:
            # Get tasks for this specification
            # Tasks use full relative path: "specifications/llm-dashboard/filename.md"
            # Specs have relative_path as just filename: "filename.md"
            # Need to construct full path for matching
            from pathlib import Path
            spec_full_path = str(Path(spec_dir) / spec_meta.relative_path)
            spec_tasks = task_groups.get(spec_full_path, [])
            
            # DEBUG
            if spec_meta.id == "SPEC-DASH-001":
                logger.info(f"DEBUG SPEC-DASH-001: spec_full_path='{spec_full_path}'")
                logger.info(f"DEBUG SPEC-DASH-001: spec_tasks count={len(spec_tasks)}")
                if spec_tasks:
                    logger.info(f"DEBUG SPEC-DASH-001: first task={spec_tasks[0].get('id')}")
            
            # Build feature list with progress
            features = []
            for feature in spec_meta.features:
                # Get tasks for this feature
                # Include tasks that explicitly match feature.id OR have no feature field
                # (tasks without feature: implement entire specification, show under all features)
                feature_tasks = [
                    t for t in spec_tasks 
                    if t.get("feature") == feature.id or t.get("feature") is None
                ]
                
                # DEBUG
                if spec_meta.id == "SPEC-DASH-001":
                    logger.info(f"DEBUG SPEC-DASH-001: feature={feature.id}, matched={len(feature_tasks)} tasks")
                # Calculate feature progress
                feature_progress = calculator.calculate_feature_progress(feature_tasks)
                
                # Build feature response
                features.append({
                    "id": feature.id,
                    "title": feature.title,
                    "status": feature.status or "unknown",
                    "progress": feature_progress,
                    "task_count": len(feature_tasks),
                    "tasks": [
                        {
                            "id": t.get("id"),
                            "title": t.get("title"),
                            "status": t.get("status"),
                            "priority": t.get("priority"),
                            "agent": t.get("agent"),
                        }
                        for t in feature_tasks
                    ]
                })
            
            # Calculate initiative progress (with manual override support)
            initiative_progress = calculator.calculate_initiative_progress(
                features,
                manual_override=spec_meta.completion
            )
            
            # Build initiative response
            initiatives.append({
                "id": spec_meta.id,
                "title": spec_meta.title,
                "status": spec_meta.status,
                "priority": spec_meta.priority,
                "initiative": spec_meta.initiative,
                "progress": initiative_progress,
                "features": features,
                "specification_path": spec_meta.relative_path,
            })
        
        # Get orphan tasks (tasks without specification links)
        orphan_tasks = linker.get_orphan_tasks()
        orphans = [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "status": t.get("status"),
                "priority": t.get("priority"),
                "agent": t.get("agent"),
            }
            for t in orphan_tasks
        ]
        
        return jsonify({
            "initiatives": initiatives,
            "orphans": orphans,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    @app.route("/api/tasks/<task_id>/priority", methods=["PATCH"])
    def update_task_priority(task_id: str):
        """
        Update task priority via PATCH request.

        Implements ADR-035: Dashboard Task Priority Editing.

        Request Body:
            {
                "priority": "HIGH",
                "last_modified": "2026-02-06T10:00:00Z"  # Optional for optimistic locking
            }

        Returns:
            200: Success with updated task data
            400: Invalid priority or missing field
            404: Task not found
            409: Conflict (in_progress status or concurrent modification)

        Example:
            PATCH /api/tasks/2026-02-06T1500-task/priority
            Body: {"priority": "HIGH"}
        """
        from .task_priority_updater import (
            TaskPriorityUpdater,
            ConcurrentModificationError,
        )

        # Validate request body
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.json

        if not data or "priority" not in data:
            return jsonify({"error": "Missing priority field"}), 400

        new_priority = data["priority"]
        last_modified = data.get("last_modified")

        # Get work directory from config
        work_dir = app.config.get("WORK_DIR", "work/collaboration")

        try:
            # Initialize updater
            updater = TaskPriorityUpdater(work_dir)

            # Validate priority first (fail fast)
            updater.validate_priority(new_priority)

            # Load task to check status
            task_data = updater.load_task(task_id)

            # Check if task is editable (reject in_progress, done, failed)
            if not updater.is_editable_status(task_data):
                return (
                    jsonify(
                        {
                            "error": f"Cannot edit task with status '{task_data.get('status')}'. "
                            "Tasks that are in_progress, done, or failed cannot be edited."
                        }
                    ),
                    409,
                )

            # Update priority with atomic write
            updater.update_task_priority(task_id, new_priority, last_modified)

            # Reload task to get updated data
            updated_task = updater.load_task(task_id)

            # Emit WebSocket event for real-time sync
            if hasattr(app, "socketio"):
                app.socketio.emit(
                    "task.updated",
                    {
                        "task_id": task_id,
                        "field": "priority",
                        "old_value": task_data.get("priority"),
                        "new_value": updated_task["priority"],
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                    namespace="/dashboard",
                )

            return jsonify({"success": True, "task": updated_task}), 200

        except ValueError as e:
            # Invalid priority or task_id
            return jsonify({"error": str(e)}), 400

        except FileNotFoundError:
            return jsonify({"error": f"Task not found: {task_id}"}), 404

        except ConcurrentModificationError as e:
            # Optimistic locking conflict
            return jsonify({"error": str(e)}), 409

        except Exception as e:
            # Unexpected error
            app.logger.error(f"Error updating task priority: {e}", exc_info=True)
            return jsonify({"error": "Internal server error"}), 500


def register_socketio_handlers(socketio: SocketIO) -> None:
    """
    Register WebSocket event handlers.

    Handlers:
        - connect: Client connection event
        - disconnect: Client disconnection event
        - ping: Keep-alive ping from client
    """

    @socketio.on("connect", namespace="/dashboard")
    def handle_connect():
        """Handle client connection to dashboard namespace."""
        emit(
            "connection_ack",
            {
                "message": "Connected to dashboard",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @socketio.on("disconnect", namespace="/dashboard")
    def handle_disconnect():
        """Handle client disconnection."""
        # Log disconnection (could integrate with telemetry)
        pass

    @socketio.on("ping", namespace="/dashboard")
    def handle_ping():
        """Respond to client ping for keep-alive."""
        emit("pong", {"timestamp": datetime.now(timezone.utc).isoformat()})


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
        emit(
            "connection_ack",
            {
                "message": "Connected to dashboard",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    def on_disconnect(self):
        """Handle client disconnection."""
        pass

    def on_ping(self):
        """Respond to ping for connection health."""
        emit("pong", {"timestamp": datetime.now(timezone.utc).isoformat()})


def run_dashboard(
    host: str = "localhost",
    port: int = 8080,
    debug: bool = False,
    watch_dir: str = "work/collaboration",
) -> None:
    """
    Run the dashboard server with file watcher.

    Args:
        host: Host to bind to (default: localhost)
        port: Port to bind to (default: 8080)
        debug: Enable debug mode (default: False)
        watch_dir: Directory to watch for task files (default: work/collaboration)

    Example:
        >>> run_dashboard(host='0.0.0.0', port=5000, debug=True)
    """
    from .file_watcher import FileWatcher

    app, socketio = create_app()

    # Initialize file watcher
    watcher = FileWatcher(watch_dir, socketio)
    app.config["FILE_WATCHER"] = watcher

    print(f"🚀 Dashboard starting at http://{host}:{port}")
    print(f"📡 WebSocket namespace: /dashboard")
    print(f"💚 Health check: http://{host}:{port}/health")
    print(f"👀 Watching: {watch_dir}")

    # Start file watcher and run server with cleanup
    try:
        watcher.start()
        socketio.run(app, host=host, port=port, debug=debug)
    finally:
        watcher.stop()


if __name__ == "__main__":
    # Allow running directly for development
    run_dashboard(debug=True)
