"""
Task Linker for Initiative Tracking.

Links tasks to specifications and features by scanning task YAML files
and matching them to specification paths.

Implements ADR-037: Dashboard Initiative Tracking.
"""

from pathlib import Path
import logging

# Import shared task loading function (ADR-042)
from src.domain.collaboration.task_schema import load_task_safe

logger = logging.getLogger(__name__)


class TaskLinker:
    """
    Links tasks to specifications and groups them by features.

    Scans work/collaboration directory for task YAML files and matches them
    to specification files via the `specification:` field.
    """

    def __init__(self, work_dir: str, spec_dir: str | None = None):
        """
        Initialize task linker.

        Args:
            work_dir: Base work directory (work/collaboration)
            spec_dir: Base specifications directory (optional, for validation)
        """
        self.work_dir = Path(work_dir)
        self.spec_dir = Path(spec_dir) if spec_dir else None

        if not self.work_dir.is_absolute():
            self.work_dir = self.work_dir.absolute()

        if self.spec_dir and not self.spec_dir.is_absolute():
            self.spec_dir = self.spec_dir.absolute()

    def load_task(self, task_path: str) -> dict | None:
        """
        Load and parse task YAML file.

        NOTE: This method delegates to src.common.task_schema.load_task_safe()
        for consistent task loading across framework and dashboard (ADR-042).

        Args:
            task_path: Path to task YAML file

        Returns:
            Task data dictionary, or None if loading fails
        """
        task_data = load_task_safe(Path(task_path))

        if task_data:
            # Add path to task data for reference (dashboard-specific)
            task_data['_path'] = task_path

        return task_data

    def scan_tasks(self) -> list[dict]:
        """
        Scan work directory for all task YAML files.

        Scans:
        - work/collaboration/inbox/*.yaml
        - work/collaboration/assigned/**/*.yaml
        - work/collaboration/done/**/*.yaml

        Returns:
            List of task dictionaries
        """
        tasks = []

        if not self.work_dir.exists():
            logger.warning(f"Work directory not found: {self.work_dir}")
            return tasks

        # Scan all YAML files recursively
        for yaml_file in self.work_dir.rglob("*.yaml"):
            task = self.load_task(str(yaml_file))
            if task:
                tasks.append(task)

        logger.info(f"Scanned {self.work_dir}: found {len(tasks)} tasks")
        return tasks

    def validate_spec_path(self, spec_path: str) -> bool:
        """
        Validate specification path for security (prevent path traversal).

        Args:
            spec_path: Specification path from task YAML

        Returns:
            True if path is safe, False if potentially malicious
        """
        # Reject paths with parent directory traversal
        if ".." in spec_path:
            logger.warning(f"Rejected specification path with '..' traversal: {spec_path}")
            return False

        # Reject absolute paths
        if Path(spec_path).is_absolute():
            logger.warning(f"Rejected absolute specification path: {spec_path}")
            return False

        return True

    def resolve_spec_path(self, spec_path: str) -> str:
        """
        Resolve specification path to absolute filesystem path.

        Args:
            spec_path: Relative specification path from task YAML

        Returns:
            Absolute path to specification file
        """
        if not self.spec_dir:
            # If no spec_dir provided, just return the path as-is
            return spec_path

        # Resolve relative to spec_dir
        resolved = self.spec_dir / spec_path
        return str(resolved.absolute())

    def spec_exists(self, spec_path: str) -> bool:
        """
        Check if specification file exists.

        Args:
            spec_path: Relative specification path

        Returns:
            True if file exists, False otherwise
        """
        if not self.spec_dir:
            return False

        full_path = Path(self.resolve_spec_path(spec_path))
        return full_path.exists()

    def group_by_specification(self) -> dict[str, list[dict]]:
        """
        Group tasks by their specification field.

        Returns:
            Dictionary mapping specification paths to lists of tasks
        """
        groups: dict[str, list[dict]] = {}

        tasks = self.scan_tasks()

        for task in tasks:
            spec_path = task.get("specification")

            if not spec_path:
                continue  # Skip tasks without specification field

            # Validate path
            if not self.validate_spec_path(spec_path):
                continue

            # Normalize path (remove leading ./ if present)
            spec_path = spec_path.lstrip("./")

            if spec_path not in groups:
                groups[spec_path] = []

            groups[spec_path].append(task)

        return groups

    def group_by_feature(self, spec_path: str) -> dict[str | None, list[dict]]:
        """
        Group tasks for a specific specification by feature.

        Args:
            spec_path: Specification path to filter by

        Returns:
            Dictionary mapping feature IDs to lists of tasks
            Uses None key for tasks without feature field
        """
        feature_groups: dict[str | None, list[dict]] = {}

        all_groups = self.group_by_specification()

        # Normalize path for lookup
        normalized_path = spec_path.lstrip("./")

        if normalized_path not in all_groups:
            return feature_groups

        tasks = all_groups[normalized_path]

        for task in tasks:
            feature_id = task.get("feature")

            if feature_id not in feature_groups:
                feature_groups[feature_id] = []

            feature_groups[feature_id].append(task)

        return feature_groups

    def get_tasks_for_specification(self, spec_path: str) -> list[dict]:
        """
        Get all tasks linked to a specific specification.

        Args:
            spec_path: Specification path

        Returns:
            List of task dictionaries
        """
        all_groups = self.group_by_specification()
        normalized_path = spec_path.lstrip("./")
        return all_groups.get(normalized_path, [])

    def get_orphan_tasks(self) -> list[dict]:
        """
        Get tasks without specification links (orphans).

        Includes:
        - Tasks with no `specification` field
        - Tasks with invalid/missing specification files

        Returns:
            List of orphan task dictionaries
        """
        orphans = []
        tasks = self.scan_tasks()

        for task in tasks:
            spec_path = task.get("specification")

            # No specification field
            if not spec_path:
                orphans.append(task)
                continue

            # Invalid path (security check)
            if not self.validate_spec_path(spec_path):
                orphans.append(task)
                continue

            # Specification file doesn't exist
            if self.spec_dir and not self.spec_exists(spec_path):
                orphans.append(task)
                continue

        return orphans

    def get_task_count_by_status(self, tasks: list[dict]) -> dict[str, int]:
        """
        Count tasks by status.

        Args:
            tasks: List of task dictionaries

        Returns:
            Dictionary mapping status to count
        """
        counts: dict[str, int] = {}

        for task in tasks:
            status = task.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1

        return counts
