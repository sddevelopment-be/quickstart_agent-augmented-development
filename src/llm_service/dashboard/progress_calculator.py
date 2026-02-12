"""
Progress Calculator for Initiative Tracking.

Calculates completion percentages for features and initiatives based on
task status with weighted progress values.

Implements ADR-037: Dashboard Initiative Tracking.
"""

import logging

# Import status enums (ADR-043)
from src.domain.collaboration.types import TaskStatus

logger = logging.getLogger(__name__)


class ProgressCalculator:
    """
    Calculates progress percentages for features and initiatives.

    Uses weighted task statuses (ADR-043):
    - done: 100% (weight 1.0)
    - in_progress: 50% (weight 0.5)
    - blocked: 25% (weight 0.25)
    - inbox/assigned: 0% (weight 0.0)
    """

    DEFAULT_STATUS_WEIGHTS = {
        TaskStatus.DONE.value: 1.0,
        TaskStatus.IN_PROGRESS.value: 0.5,
        TaskStatus.BLOCKED.value: 0.25,
        TaskStatus.INBOX.value: 0.0,
        TaskStatus.ASSIGNED.value: 0.0,
        TaskStatus.ERROR.value: 0.0,
    }

    def __init__(
        self, status_weights: dict[str, float] | None = None, enable_cache: bool = False
    ):
        """
        Initialize progress calculator.

        Args:
            status_weights: Custom status weight mappings (optional)
            enable_cache: Enable caching of calculations (future optimization)
        """
        self.status_weights = status_weights or self.DEFAULT_STATUS_WEIGHTS.copy()
        self.enable_cache = enable_cache
        self.cache_hits = 0
        self._cache: dict[str, int] = {}

    def get_status_weight(self, status: str) -> float:
        """
        Get weight for a task status.

        Args:
            status: Task status string

        Returns:
            Weight value (0.0 to 1.0), defaults to 0.0 for unknown statuses
        """
        return self.status_weights.get(status.lower(), 0.0)

    def calculate_feature_progress(
        self, tasks: list[dict], feature_id: str | None = None
    ) -> int:
        """
        Calculate completion percentage for a feature based on its tasks.

        Progress formula:
        progress = (sum of task weights) / (number of tasks) * 100

        Args:
            tasks: List of task dictionaries with 'status' field
            feature_id: Optional feature ID for caching (future)

        Returns:
            Progress percentage (0-100)
        """
        if not tasks:
            return 0

        # Check cache if enabled (future optimization)
        if self.enable_cache and feature_id:
            if feature_id in self._cache:
                self.cache_hits += 1
                return self._cache[feature_id]

        # Calculate weighted progress
        total_weight = 0.0

        for task in tasks:
            status = task.get("status", TaskStatus.INBOX.value)
            weight = self.get_status_weight(status)
            total_weight += weight

        # Calculate percentage
        progress_fraction = total_weight / len(tasks)
        progress_percent = int(progress_fraction * 100)

        # Clamp to 0-100 range
        progress_percent = max(0, min(100, progress_percent))

        # Cache result if enabled
        if self.enable_cache and feature_id:
            self._cache[feature_id] = progress_percent

        return progress_percent

    def calculate_initiative_progress(
        self, features: list[dict], manual_override: int | None = None
    ) -> int:
        """
        Calculate initiative progress by averaging feature progress.

        Args:
            features: List of feature dictionaries with 'progress' field
            manual_override: Manual completion percentage (takes precedence)

        Returns:
            Progress percentage (0-100)
        """
        # Use manual override if provided
        if manual_override is not None:
            return max(0, min(100, manual_override))

        if not features:
            return 0

        # Average feature progress
        total_progress = sum(f.get("progress", 0) for f in features)
        avg_progress = total_progress / len(features)

        # Round to integer
        progress_percent = int(avg_progress)

        # Clamp to 0-100
        return max(0, min(100, progress_percent))

    def calculate_initiative_progress_with_override(self, metadata: dict) -> int:
        """
        Calculate initiative progress with support for manual completion override.

        Checks metadata['completion'] for manual override before calculating
        from features.

        Args:
            metadata: Specification metadata dictionary with optional 'completion'

        Returns:
            Progress percentage (0-100)
        """
        manual_completion = metadata.get("completion")

        if manual_completion is not None:
            return max(0, min(100, manual_completion))

        # Calculate from features
        features = metadata.get("features", [])

        if not features:
            return 0

        return self.calculate_initiative_progress(features)

    def calculate_weighted_initiative_progress(self, features: list[dict]) -> int:
        """
        Calculate initiative progress with weighted features (future enhancement).

        Allows features to have different importance weights.

        Args:
            features: List of feature dicts with 'progress' and optional 'weight' fields

        Returns:
            Weighted progress percentage (0-100)
        """
        if not features:
            return 0

        # Calculate weighted average
        total_weighted_progress = 0.0
        total_weight = 0.0

        for feature in features:
            progress = feature.get("progress", 0)
            weight = feature.get("weight", 1.0)  # Default weight of 1.0

            total_weighted_progress += progress * weight
            total_weight += weight

        if total_weight == 0:
            return 0

        weighted_avg = total_weighted_progress / total_weight
        progress_percent = int(weighted_avg)

        return max(0, min(100, progress_percent))

    def invalidate_cache(self, feature_id: str | None = None):
        """
        Invalidate progress cache.

        Args:
            feature_id: Specific feature to invalidate, or None to clear all
        """
        if feature_id:
            self._cache.pop(feature_id, None)
        else:
            self._cache.clear()

    def get_feature_status_summary(self, tasks: list[dict]) -> dict[str, int]:
        """
        Get summary of task counts by status for a feature.

        Args:
            tasks: List of task dictionaries

        Returns:
            Dictionary mapping status to count
        """
        summary: dict[str, int] = {}

        for task in tasks:
            status = task.get("status", "unknown")
            summary[status] = summary.get(status, 0) + 1

        return summary

    def get_initiative_summary(
        self, features: list[dict], all_tasks: list[dict]
    ) -> dict:
        """
        Get comprehensive summary for an initiative.

        Args:
            features: List of features in the initiative
            all_tasks: All tasks for the initiative

        Returns:
            Summary dictionary with progress, counts, and status
        """
        total_features = len(features)
        completed_features = sum(1 for f in features if f.get("progress", 0) == 100)
        in_progress_features = sum(
            1 for f in features if 0 < f.get("progress", 0) < 100
        )

        task_status_counts = {}
        for task in all_tasks:
            status = task.get("status", "unknown")
            task_status_counts[status] = task_status_counts.get(status, 0) + 1

        overall_progress = self.calculate_initiative_progress(features)

        return {
            "progress": overall_progress,
            "features": {
                "total": total_features,
                "completed": completed_features,
                "in_progress": in_progress_features,
                "not_started": total_features
                - completed_features
                - in_progress_features,
            },
            "tasks": {
                "total": len(all_tasks),
                "by_status": task_status_counts,
            },
        }
