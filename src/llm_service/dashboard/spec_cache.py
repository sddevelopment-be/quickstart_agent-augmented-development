"""
Specification Frontmatter Caching Layer.

Implements two-tier caching strategy for specification frontmatter parsing:
- Tier 1: In-memory cache (process lifetime)
- Tier 2: File watcher invalidation (watchdog library)

Performance requirements (NFR-P2):
- Initial load (startup): <2 seconds for 50 specs
- Cached reads: <50ms
- Cache invalidation: <100ms

References:
- Task: 2026-02-09T2034-python-pedro-frontmatter-caching.yaml
- Specification: SPEC-DASH-008 v1.0.0
- Implements ATDD (Directive 016) and TDD (Directive 017)
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

if TYPE_CHECKING:
    from src.llm_service.dashboard.spec_parser import SpecificationMetadata

logger = logging.getLogger(__name__)


class SpecChangeHandler(FileSystemEventHandler):
    """
    File system event handler for specification file changes.

    Monitors .md files in specifications/ directory and invalidates
    cache entries when files are modified or deleted.
    """

    def __init__(self, cache: 'SpecificationCache'):
        """
        Initialize handler with reference to parent cache.

        Args:
            cache: Parent SpecificationCache instance
        """
        super().__init__()
        self.cache = cache

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handle file modification events.

        When a .md file is modified, invalidate its cache entry.

        Args:
            event: File system event
        """
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Only process markdown files
        if file_path.suffix.lower() == '.md':
            logger.debug(f"Detected modification: {file_path}")
            self.cache.invalidate(str(file_path))

    def on_deleted(self, event: FileSystemEvent) -> None:
        """
        Handle file deletion events.

        When a .md file is deleted, remove it from cache.

        Args:
            event: File system event
        """
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() == '.md':
            logger.debug(f"Detected deletion: {file_path}")
            self.cache.invalidate(str(file_path))


class SpecificationCache:
    """
    High-performance cache for specification frontmatter.

    Provides:
    - In-memory caching of parsed specification metadata
    - Automatic cache invalidation on file changes (via watchdog)
    - Batch preloading for startup performance
    - Graceful error handling for missing/malformed specs

    Usage:
        >>> cache = SpecificationCache("specifications/")
        >>> cache.start_file_watcher()
        >>> cache.preload_all()
        >>> spec = cache.get_spec("specifications/my-spec.md")
        >>> all_specs = cache.get_all_specs()
        >>> cache.stop_file_watcher()
    """

    def __init__(self, base_dir: str):
        """
        Initialize specification cache.

        Args:
            base_dir: Base directory containing specification files
        """
        self.base_dir = Path(base_dir)

        # Convert to absolute path for consistency
        if not self.base_dir.is_absolute():
            self.base_dir = self.base_dir.absolute()

        # Initialize empty cache
        # Structure: {spec_path: SpecificationMetadata}
        self.cache: dict[str, SpecificationMetadata] = {}

        # File watcher (initialized by start_file_watcher)
        self.file_watcher: Observer | None = None

        # Import SpecificationParser (lazy to avoid circular dependencies)
        from src.llm_service.dashboard.spec_parser import SpecificationParser
        self.parser = SpecificationParser(str(self.base_dir))

        logger.info(f"SpecificationCache initialized with base_dir: {self.base_dir}")

    def get_spec(self, spec_path: str) -> Optional['SpecificationMetadata']:
        """
        Get specification frontmatter (cached or parsed).

        On cache miss, parses the specification and caches the result.
        On cache hit, returns cached metadata without file I/O.

        Args:
            spec_path: Path to specification markdown file

        Returns:
            SpecificationMetadata instance, or None if parsing fails or file doesn't exist
        """
        # Check cache first (cache hit)
        if spec_path in self.cache:
            logger.debug(f"Cache hit: {spec_path}")
            return self.cache[spec_path]

        # Cache miss - parse and cache
        logger.debug(f"Cache miss: {spec_path}")
        return self._parse_and_cache(spec_path)

    def _parse_and_cache(self, spec_path: str) -> Optional['SpecificationMetadata']:
        """
        Parse specification and store in cache.

        Args:
            spec_path: Path to specification file

        Returns:
            Parsed SpecificationMetadata, or None if parsing fails
        """
        # Use existing SpecificationParser
        metadata = self.parser.parse_frontmatter(spec_path)

        if metadata is not None:
            # Store in cache
            self.cache[spec_path] = metadata
            logger.debug(f"Cached spec: {spec_path}")

        return metadata

    def invalidate(self, spec_path: str) -> None:
        """
        Invalidate cache entry for specified path.

        Removes the spec from cache. Next get_spec() call will re-parse.
        Safe to call even if spec_path is not in cache.

        Args:
            spec_path: Path to specification file to invalidate
        """
        if spec_path in self.cache:
            del self.cache[spec_path]
            logger.debug(f"Invalidated cache: {spec_path}")

    def preload_all(self) -> None:
        """
        Preload all specifications from base directory into cache.

        Scans base_dir recursively for .md files and parses their frontmatter.
        Designed for startup performance - loads all specs in batch.

        Invalid or missing specs are skipped without raising exceptions.
        """
        start_time = datetime.now()

        logger.info(f"Preloading specifications from {self.base_dir}")

        if not self.base_dir.exists():
            logger.warning(f"Base directory not found: {self.base_dir}")
            return

        # Find all .md files recursively
        count = 0
        for md_file in self.base_dir.rglob("*.md"):
            # Parse and cache
            metadata = self._parse_and_cache(str(md_file))
            if metadata:
                count += 1

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(f"Preloaded {count} specifications in {elapsed:.3f}s")

    def get_all_specs(self) -> list['SpecificationMetadata']:
        """
        Get list of all cached specifications.

        Returns only specs currently in cache. If cache is empty, returns empty list.
        Call preload_all() first to ensure all specs are loaded.

        Returns:
            List of SpecificationMetadata instances
        """
        return list(self.cache.values())

    def start_file_watcher(self) -> None:
        """
        Start watchdog file watcher for specifications directory.

        Monitors base_dir recursively for .md file changes and automatically
        invalidates cache entries when files are modified or deleted.

        Safe to call multiple times (idempotent).
        """
        if self.file_watcher is not None and self.file_watcher.is_alive():
            logger.debug("File watcher already running")
            return

        logger.info(f"Starting file watcher on {self.base_dir}")

        # Create observer and handler
        self.file_watcher = Observer()
        handler = SpecChangeHandler(self)

        # Schedule handler to watch base_dir recursively
        self.file_watcher.schedule(handler, str(self.base_dir), recursive=True)

        # Start observer thread
        self.file_watcher.start()

        logger.info("File watcher started")

    def stop_file_watcher(self) -> None:
        """
        Stop watchdog file watcher.

        Cleanly shuts down the observer thread.
        Safe to call even if watcher is not running.
        """
        if self.file_watcher is None:
            return

        if self.file_watcher.is_alive():
            logger.info("Stopping file watcher")
            self.file_watcher.stop()
            self.file_watcher.join(timeout=2.0)
            logger.info("File watcher stopped")

    def clear(self) -> None:
        """
        Clear all cached specifications.

        Useful for testing or manual cache reset.
        """
        self.cache.clear()
        logger.debug("Cache cleared")

    def __del__(self):
        """Destructor - ensure file watcher is stopped."""
        self.stop_file_watcher()
