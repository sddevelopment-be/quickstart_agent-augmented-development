"""
File Watcher for Dashboard - Monitors YAML task files.

Uses watchdog to monitor work/collaboration/ directory for changes.
Emits WebSocket events when tasks are created, assigned, or completed.

Critical: Dashboard is READ-ONLY - watches files, doesn't modify them.
"""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)

# File pattern constants
YAML_PATTERN = "*.yaml"


class TaskFileHandler(FileSystemEventHandler):
    """
    Handler for file system events on YAML task files.

    Monitors:
        - File creation (new tasks in inbox)
        - File moves (tasks moving between directories)
        - File modifications (status updates)
    """

    def __init__(self, watcher: "FileWatcher"):
        """
        Initialize handler with reference to parent watcher.

        Args:
            watcher: Parent FileWatcher instance
        """
        super().__init__()
        self.watcher = watcher

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if self._is_yaml_file(file_path):
            self.watcher._handle_file_created(file_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move events (e.g., inbox → assigned)."""
        if event.is_directory:
            return

        src_path = Path(event.src_path)
        dest_path = Path(event.dest_path)

        if self._is_yaml_file(dest_path):
            self.watcher._handle_file_moved(src_path, dest_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if self._is_yaml_file(file_path):
            self.watcher._handle_file_modified(file_path)

    @staticmethod
    def _is_yaml_file(path: Path) -> bool:
        """Check if file is a YAML file."""
        return path.suffix.lower() in [".yaml", ".yml"]


class FileWatcher:
    """
    File watcher for monitoring YAML task files in work/collaboration/.

    Watches:
        - work/collaboration/inbox/
        - work/collaboration/assigned/<agent>/
        - work/collaboration/done/<agent>/

    Emits WebSocket events:
        - task.created: New task in inbox
        - task.assigned: Task moved to assigned
        - task.completed: Task moved to done
        - task.updated: Task file modified
    """

    def __init__(self, watch_dir: str | Path, socketio: Any | None = None):
        """
        Initialize file watcher.

        Args:
            watch_dir: Directory to watch (typically work/collaboration/)
            socketio: SocketIO instance for event emission (optional)
        """
        self.watch_dir = Path(watch_dir)
        self.socketio = socketio
        self.observer: Observer | None = None
        self.is_running = False

        # Debounce tracking (prevent duplicate events)
        self._last_events: dict[str, float] = {}
        self._debounce_seconds = 0.1

    def start(self) -> None:
        """Start watching for file changes."""
        if self.is_running:
            logger.warning("FileWatcher already running")
            return

        self.observer = Observer()
        handler = TaskFileHandler(self)

        # Watch the entire collaboration directory recursively
        self.observer.schedule(handler, str(self.watch_dir), recursive=True)
        self.observer.start()
        self.is_running = True

        logger.info(f"FileWatcher started on {self.watch_dir}")

    def stop(self) -> None:
        """Stop watching for file changes."""
        if not self.is_running or self.observer is None:
            return

        self.observer.stop()
        self.observer.join()
        self.is_running = False

        logger.info("FileWatcher stopped")

    def parse_task_file(self, file_path: Path) -> dict[str, Any] | None:
        """
        Parse YAML task file and extract metadata.

        Args:
            file_path: Path to YAML task file

        Returns:
            Dictionary with task metadata, or None if parsing fails
        """
        try:
            with open(file_path) as f:
                data = yaml.safe_load(f)

                if not isinstance(data, dict):
                    logger.warning(f"Invalid YAML structure in {file_path}")
                    return None

                return data

        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {file_path}: {e}")
            return None

        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None

    def infer_status_from_path(self, file_path: Path) -> str:
        """
        Infer task status from file path.

        Args:
            file_path: Path to task file

        Returns:
            Status string: 'new', 'assigned', 'done', or 'unknown'
        """
        path_str = str(file_path)

        if "/inbox/" in path_str or "\\inbox\\" in path_str:
            return "new"
        elif "/assigned/" in path_str or "\\assigned\\" in path_str:
            return "assigned"
        elif "/done/" in path_str or "\\done\\" in path_str:
            return "done"
        else:
            return "unknown"

    def get_task_snapshot(self) -> dict[str, Any]:
        """
        Get current snapshot of all tasks in the watch directory.

        Returns:
            Dictionary with tasks grouped by status (inbox/assigned/done)
        """
        snapshot = {
            "inbox": [],
            "assigned": {},
            "done": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Scan inbox
        inbox_dir = self.watch_dir / "inbox"
        if inbox_dir.exists():
            for yaml_file in inbox_dir.glob(YAML_PATTERN):
                task = self.parse_task_file(yaml_file)
                if task:
                    snapshot["inbox"].append(task)
            for yml_file in inbox_dir.glob("*.yml"):
                task = self.parse_task_file(yml_file)
                if task:
                    snapshot["inbox"].append(task)

        # Scan assigned (nested by agent)
        assigned_dir = self.watch_dir / "assigned"
        if assigned_dir.exists():
            for agent_dir in assigned_dir.iterdir():
                if agent_dir.is_dir():
                    agent_name = agent_dir.name
                    snapshot["assigned"][agent_name] = []

                    for yaml_file in agent_dir.glob(YAML_PATTERN):
                        task = self.parse_task_file(yaml_file)
                        if task:
                            snapshot["assigned"][agent_name].append(task)
                    for yml_file in agent_dir.glob("*.yml"):
                        task = self.parse_task_file(yml_file)
                        if task:
                            snapshot["assigned"][agent_name].append(task)

        # Scan done (nested by agent)
        done_dir = self.watch_dir / "done"
        if done_dir.exists():
            for agent_dir in done_dir.iterdir():
                if agent_dir.is_dir():
                    agent_name = agent_dir.name
                    snapshot["done"][agent_name] = []

                    for yaml_file in agent_dir.glob(YAML_PATTERN):
                        task = self.parse_task_file(yaml_file)
                        if task:
                            snapshot["done"][agent_name].append(task)
                    for yml_file in agent_dir.glob("*.yml"):
                        task = self.parse_task_file(yml_file)
                        if task:
                            snapshot["done"][agent_name].append(task)

        return snapshot

    def _should_emit(self, event_key: str) -> bool:
        """
        Check if event should be emitted (debouncing).

        Args:
            event_key: Unique key for the event

        Returns:
            True if event should be emitted
        """
        now = datetime.now(timezone.utc).timestamp()
        last_time = self._last_events.get(event_key, 0)

        if now - last_time < self._debounce_seconds:
            return False

        self._last_events[event_key] = now
        return True

    def _handle_file_created(self, file_path: Path) -> None:
        """Handle file creation event."""
        event_key = f"created:{file_path}"
        if not self._should_emit(event_key):
            return

        task_data = self.parse_task_file(file_path)
        if not task_data:
            return

        status = self.infer_status_from_path(file_path)

        if self.socketio:
            self.socketio.emit(
                "task.created",
                {
                    "task": task_data,
                    "status": status,
                    "file_path": str(file_path),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                namespace="/dashboard",
            )

        logger.info(f"Task created: {task_data.get('id', 'unknown')} in {status}")

    def _handle_file_moved(self, src_path: Path, dest_path: Path) -> None:
        """Handle file move event."""
        event_key = f"moved:{dest_path}"
        if not self._should_emit(event_key):
            return

        task_data = self.parse_task_file(dest_path)
        if not task_data:
            return

        old_status = self.infer_status_from_path(src_path)
        new_status = self.infer_status_from_path(dest_path)

        # Determine event type based on status transition
        if old_status == "new" and new_status == "assigned":
            event_name = "task.assigned"
        elif new_status == "done":
            event_name = "task.completed"
        else:
            event_name = "task.moved"

        if self.socketio:
            self.socketio.emit(
                event_name,
                {
                    "task": task_data,
                    "old_status": old_status,
                    "new_status": new_status,
                    "file_path": str(dest_path),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                namespace="/dashboard",
            )

        logger.info(
            f"Task {event_name}: {task_data.get('id', 'unknown')} "
            f"from {old_status} to {new_status}"
        )

    def _handle_file_modified(self, file_path: Path) -> None:
        """Handle file modification event."""
        event_key = f"modified:{file_path}"
        if not self._should_emit(event_key):
            return

        task_data = self.parse_task_file(file_path)
        if not task_data:
            return

        status = self.infer_status_from_path(file_path)

        if self.socketio:
            self.socketio.emit(
                "task.updated",
                {
                    "task": task_data,
                    "status": status,
                    "file_path": str(file_path),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                namespace="/dashboard",
            )

        logger.debug(f"Task updated: {task_data.get('id', 'unknown')}")


def create_watcher(
    collaboration_dir: str | Path, socketio: Any | None = None
) -> FileWatcher:
    """
    Convenience function to create a FileWatcher instance.

    Args:
        collaboration_dir: Path to work/collaboration/ directory
        socketio: SocketIO instance for event emission

    Returns:
        Configured FileWatcher instance

    Example:
        >>> from llm_service.dashboard.app import create_app
        >>> from llm_service.dashboard.file_watcher import create_watcher
        >>> app, socketio = create_app()
        >>> watcher = create_watcher('work/collaboration', socketio)
        >>> watcher.start()
    """
    return FileWatcher(watch_dir=collaboration_dir, socketio=socketio)
