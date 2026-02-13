"""
Dashboard WebSocket Server for LLM Service.

Provides real-time monitoring of LLM operations via WebSocket connections.
Follows ADR-032: Real-Time Execution Dashboard.
Implements ADR-036: Dashboard Markdown Rendering with XSS protection.
Implements ADR-035: Dashboard Task Priority Editing.
"""

import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import Namespace, SocketIO, emit

# Import task query functions from domain layer (ADR-046)
from src.domain.collaboration.task_query import (
    find_task_files,
    load_open_tasks,
)
from src.domain.collaboration.task_schema import load_task_safe
from src.domain.collaboration.types import TaskStatus


def load_tasks_with_filter(
    work_dir: Path, include_done: bool = False, terminal_only: bool = False
) -> list[dict]:
    """
    Load tasks with filtering options.

    Args:
        work_dir: Work collaboration directory
        include_done: Include finished (done/error) tasks
        terminal_only: Return only terminal status tasks

    Returns:
        List of task dictionaries matching filter criteria
    """
    if not include_done and not terminal_only:
        # Use optimized function for active tasks only
        return load_open_tasks(work_dir)

    # Load all tasks including finished ones
    task_files = find_task_files(work_dir, include_done=True)
    filtered_tasks = []

    for task_file in task_files:
        task = load_task_safe(task_file)
        if task is None:
            continue

        # Check status filter
        status = task.get("status", "")
        try:
            task_status = TaskStatus(status)

            if terminal_only:
                # Only include terminal status tasks
                if TaskStatus.is_terminal(task_status):
                    filtered_tasks.append(task)
            elif include_done:
                # Include all tasks
                filtered_tasks.append(task)
            else:
                # Include only active tasks
                if not TaskStatus.is_terminal(task_status):
                    filtered_tasks.append(task)
        except ValueError:
            # Invalid status, skip silently
            continue

    return filtered_tasks


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


def create_app(config: dict[str, Any] | None = None) -> tuple[Flask, SocketIO]:
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

    @app.route("/", methods=["GET"])
    def index():
        """Serve dashboard UI."""
        return app.send_static_file("index.html")

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint for monitoring."""
        return jsonify(
            {
                "status": "healthy",
                "service": "llm-service-dashboard",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.route("/api/stats", methods=["GET"])
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

        # Get task counts from file watcher
        watcher = app.config.get("FILE_WATCHER")
        task_counts = {"inbox": 0, "assigned": 0, "done": 0, "total": 0}

        if watcher:
            snapshot = watcher.get_task_snapshot()

            # Count inbox tasks
            inbox_count = len(snapshot.get("inbox", []))

            # Count assigned tasks (nested by agent)
            assigned_count = sum(
                len(tasks) for tasks in snapshot.get("assigned", {}).values()
            )

            # Count done tasks (nested by agent)
            done_count = sum(len(tasks) for tasks in snapshot.get("done", {}).values())

            task_counts = {
                "inbox": inbox_count,
                "assigned": assigned_count,
                "done": done_count,
                "total": inbox_count + assigned_count + done_count,
            }

        return jsonify(
            {
                "tasks": task_counts,
                "costs": costs,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.route("/api/tasks", methods=["GET"])
    def tasks():
        """
        Return current task state across all workflow directories.

        Query Parameters:
            include_done (bool): Include finished (done/error) tasks. Default: true

        Returns:
            JSON with tasks in nested format: {inbox: [], assigned: {agent: []}, done: {agent: []}}
        """
        # Get include_done parameter (default: true for backward compatibility)
        include_done = request.args.get("include_done", "true").lower() == "true"

        # Get task snapshot from file watcher (always returns nested format)
        watcher = app.config.get("FILE_WATCHER")
        if watcher:
            snapshot = watcher.get_task_snapshot()

            # If include_done=false, remove done and error tasks from snapshot
            if not include_done:
                snapshot = snapshot.copy()
                snapshot["done"] = {}
                snapshot["error"] = {}

            return jsonify(snapshot)

        # Fallback if watcher not initialized
        return jsonify(
            {
                "inbox": [],
                "assigned": {},
                "done": {},
                "error": {},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.route("/api/tasks/finished", methods=["GET"])
    def tasks_finished():
        """
        Return only finished tasks (DONE and ERROR status).

        Returns:
            JSON array with tasks that have terminal status (done/error)
        """
        work_dir = Path(app.config.get("WORK_DIR", "work/collaboration"))
        finished_tasks = load_tasks_with_filter(
            work_dir, include_done=True, terminal_only=True
        )
        return jsonify(finished_tasks)

    def _build_task_list(spec_tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Build task list from specification tasks."""
        return [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "status": t.get("status"),
                "priority": t.get("priority"),
                "agent": t.get("agent"),
            }
            for t in spec_tasks
        ]

    def _calculate_spec_progress(spec_tasks: list[dict[str, Any]]) -> int:
        """Calculate specification progress from tasks."""
        completed_tasks = sum(1 for t in spec_tasks if t.get("status") == "done")
        total_tasks = len(spec_tasks)
        return int(completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    def _determine_initiative_status(specs: list[dict[str, Any]]) -> str:
        """Determine initiative status (most advanced status)."""
        status_priority = {
            "draft": 1,
            "in_progress": 2,
            "implemented": 3,
            "complete": 3,
        }
        return max(
            (spec.get("status", "draft") for spec in specs),
            key=lambda s, priority=status_priority: priority.get(s, 0),
        )

    def _determine_initiative_priority(specs: list[dict[str, Any]]) -> str:
        """Determine initiative priority (highest priority)."""
        priority_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        return max(
            (spec.get("priority", "MEDIUM") for spec in specs),
            key=lambda p, order=priority_order: order.get(p, 2),
        )

    def _calculate_initiative_progress(specs: list[dict[str, Any]]) -> int:
        """Calculate initiative progress from all specifications."""
        total_tasks = sum(spec["task_count"] for spec in specs)
        completed_tasks = sum(
            len([t for t in spec["tasks"] if t.get("status") == "done"])
            for spec in specs
        )
        return int(completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    @app.route("/api/portfolio", methods=["GET"])
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
        from .progress_calculator import ProgressCalculator
        from .spec_parser import SpecificationParser
        from .task_linker import TaskLinker

        # Get directories from config
        spec_dir = app.config.get("SPEC_DIR", "specifications")
        work_dir = app.config.get("WORK_DIR", "work/collaboration")

        # Initialize components
        parser = SpecificationParser(spec_dir)
        linker = TaskLinker(work_dir, spec_dir=spec_dir)
        ProgressCalculator()

        # Parse all specifications
        specifications = parser.scan_specifications(spec_dir)

        # Group tasks by specification
        task_groups = linker.group_by_specification()

        # Build specification objects with their tasks
        from collections import defaultdict

        spec_objects = []

        for spec_meta in specifications:
            # Get tasks for this specification
            from pathlib import Path

            spec_full_path = str(Path(spec_dir) / spec_meta.relative_path)
            spec_tasks = task_groups.get(spec_full_path, [])

            # Build task list (tasks link to specifications, not features)
            tasks = _build_task_list(spec_tasks)

            # Calculate specification progress from tasks
            spec_progress = _calculate_spec_progress(spec_tasks)

            # Build specification object
            spec_objects.append(
                {
                    "id": spec_meta.id,
                    "title": spec_meta.title,
                    "status": spec_meta.status,
                    "priority": spec_meta.priority,
                    "initiative": spec_meta.initiative,
                    "progress": spec_progress,
                    "task_count": len(tasks),
                    "tasks": tasks,
                    "specification_path": spec_meta.relative_path,
                }
            )

        # Group specifications by initiative
        initiatives_grouped = defaultdict(list)
        for spec in spec_objects:
            initiative_name = spec.get("initiative") or "Uncategorized"
            initiatives_grouped[initiative_name].append(spec)

        # Build initiative list
        initiatives = []
        for initiative_name, specs in sorted(initiatives_grouped.items()):
            # Calculate initiative progress from all specifications
            initiative_progress = _calculate_initiative_progress(specs)

            # Determine initiative status (most advanced status)
            initiative_status = _determine_initiative_status(specs)

            # Determine initiative priority (highest priority)
            initiative_priority = _determine_initiative_priority(specs)

            # Calculate task count
            total_tasks = sum(spec["task_count"] for spec in specs)

            initiatives.append(
                {
                    "id": initiative_name.lower().replace(" ", "-"),
                    "title": initiative_name,
                    "status": initiative_status,
                    "priority": initiative_priority,
                    "progress": initiative_progress,
                    "specifications": specs,
                    "spec_count": len(specs),
                    "task_count": total_tasks,
                }
            )

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

        return jsonify(
            {
                "initiatives": initiatives,
                "orphans": orphans,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @app.route("/api/agents/portfolio", methods=["GET"])
    def agent_portfolio():
        """
        Return agent portfolio data with capabilities and compliance.

        Implements ADR-045 Task 5: Dashboard Integration (Portfolio View).

        Returns:
            JSON with agent portfolio data:
            {
                "agents": [
                    {
                        "id": "agent-id",
                        "name": "Agent Name",
                        "specialization": "Description",
                        "capability_descriptions": {...},
                        "directive_compliance": {
                            "required_directives_count": 3,
                            "compliance_percentage": 100.0
                        },
                        "source_file": "path/to/agent.md",
                        "source_hash": "sha256..."
                    }
                ],
                "metadata": {
                    "total_agents": 15,
                    "load_time_ms": 25.3
                }
            }
        """
        from .agent_portfolio import AgentPortfolioService

        try:
            # Initialize service (uses default .github/agents directory)
            service = AgentPortfolioService()

            # Get portfolio data
            portfolio = service.get_portfolio_data()

            # Add timestamp
            portfolio["timestamp"] = datetime.now(timezone.utc).isoformat()

            return jsonify(portfolio)

        except Exception as e:
            app.logger.error(f"Error loading agent portfolio: {e}", exc_info=True)
            return jsonify({"error": "Failed to load agent portfolio"}), 500

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
            ConcurrentModificationError,
            TaskPriorityUpdater,
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

    @app.route("/api/tasks/<task_id>/specification", methods=["PATCH"])
    def update_task_specification(task_id):
        """
        Assign orphan task to specification/feature.

        Implements SPEC-DASH-008: Orphan Task Assignment.

        Request Body:
            {
                "specification": "specifications/llm-service/api-hardening.md",
                "feature": "Rate Limiting",  # Optional
                "last_modified": "2026-02-09T20:00:00Z"  # Optional (optimistic locking)
            }

        Response 200:
            {
                "success": true,
                "task": { ... }
            }

        Errors:
            400: Invalid specification path, task not editable, or file not found
            404: Task not found
            409: Concurrent edit conflict
            500: YAML write failure

        Example:
            PATCH /api/tasks/2026-02-09T2000-task/specification
            Body: {
                "specification": "specifications/llm-service/api-hardening.md",
                "feature": "Rate Limiting"
            }
        """
        from .task_assignment_handler import (
            ConcurrentModificationError,
            InvalidSpecificationError,
            TaskAssignmentHandler,
            TaskNotEditableError,
        )

        # Validate request body
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.json

        if not data or "specification" not in data:
            return jsonify({"error": "Missing specification field"}), 400

        specification = data["specification"]
        feature = data.get("feature")  # Optional
        last_modified = data.get("last_modified")  # Optional (optimistic locking)

        # Get configuration
        work_dir = app.config.get("WORK_DIR", "work/collaboration")
        repo_root = app.config.get("REPO_ROOT", ".")

        try:
            # Initialize handler
            handler = TaskAssignmentHandler(work_dir=work_dir, repo_root=repo_root)

            # Load task before update (for WebSocket old values)
            task_data = handler._get_task_file_path(task_id)
            yaml = handler.yaml
            with open(task_data, encoding="utf-8") as f:
                old_task_data = yaml.load(f)

            # Update task specification with atomic write
            updated_task = handler.update_task_specification(
                task_id=task_id,
                specification=specification,
                feature=feature,
                last_modified=last_modified,
            )

            # Emit WebSocket events for real-time sync
            if hasattr(app, "socketio"):
                # Specific event: task.assigned
                app.socketio.emit(
                    "task.assigned",
                    {
                        "task_id": task_id,
                        "specification": specification,
                        "feature": feature,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                    namespace="/dashboard",
                )

                # Generic event: task.updated
                app.socketio.emit(
                    "task.updated",
                    {
                        "task_id": task_id,
                        "field": "specification",
                        "old_value": old_task_data.get("specification"),
                        "new_value": updated_task["specification"],
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                    namespace="/dashboard",
                )

            return jsonify({"success": True, "task": updated_task}), 200

        except InvalidSpecificationError as e:
            # Invalid specification path or file not found
            return jsonify({"error": str(e)}), 400

        except TaskNotEditableError as e:
            # Task status prevents assignment
            return jsonify({"error": str(e)}), 400

        except ValueError as e:
            # Invalid task_id
            return jsonify({"error": str(e)}), 400

        except FileNotFoundError:
            return jsonify({"error": f"Task not found: {task_id}"}), 404

        except ConcurrentModificationError as e:
            # Optimistic locking conflict
            return jsonify({"error": str(e)}), 409

        except Exception as e:
            # Unexpected error
            app.logger.error(f"Error assigning task specification: {e}", exc_info=True)
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
    print("📡 WebSocket namespace: /dashboard")
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
