"""
Append-only JSONL event writer for telemetry (ADR-047).

Writes lifecycle and execution events to a JSONL file with fsync
guarantee. Crash-safe: partial writes produce incomplete lines that
are detectable on read.
"""

import os
import threading
from pathlib import Path
from typing import Optional

from .event_schema import Event


class EventWriter:
    """
    Append-only JSONL event writer with fsync guarantee.

    Each call to emit() appends one JSON line and calls fsync to ensure
    durability. Thread-safe via a threading lock.

    Args:
        path: Path to the JSONL file. Created if it does not exist.
        max_size_bytes: Optional maximum file size before rotation.
            When exceeded, the current file is renamed with a .1 suffix
            and a new file is started. Set to None to disable rotation.
    """

    def __init__(self, path: Path, max_size_bytes: Optional[int] = None):
        self.path = Path(path)
        self.max_size_bytes = max_size_bytes
        self._lock = threading.Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: Event) -> None:
        """
        Append event as a single JSON line with fsync.

        Args:
            event: Event dataclass to write.
        """
        line = event.to_json() + "\n"
        with self._lock:
            self._maybe_rotate()
            fd = os.open(str(self.path), os.O_WRONLY | os.O_CREAT | os.O_APPEND)
            try:
                os.write(fd, line.encode("utf-8"))
                os.fsync(fd)
            finally:
                os.close(fd)

    def _maybe_rotate(self) -> None:
        """Rotate file if max_size_bytes is set and exceeded."""
        if self.max_size_bytes is None:
            return
        if not self.path.exists():
            return
        if self.path.stat().st_size >= self.max_size_bytes:
            rotated = self.path.with_suffix(self.path.suffix + ".1")
            self.path.rename(rotated)

    def read_events(self) -> list[Event]:
        """
        Read all valid events from the JSONL file.

        Skips incomplete or corrupt lines (crash-safety).

        Returns:
            List of successfully parsed Event objects.
        """
        events = []
        if not self.path.exists():
            return events
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(Event.from_json(line))
                except (ValueError, KeyError, TypeError):
                    # Skip corrupt/incomplete lines (crash-safety)
                    continue
        return events
