#!/usr/bin/env python3
"""
Task Age Checker

Purpose: Detect and warn about stale tasks in the orchestration system.
         Helps prevent executing tasks with outdated context.

Usage:
    python ops/orchestration/task_age_checker.py [--threshold HOURS]
    
Options:
    --threshold HOURS    Age threshold in hours (default: 24)
    --warn-only          Only show warnings, don't fail
    --format FORMAT      Output format: text or json (default: text)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Add common utilities to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.path_utils import get_work_dir


class TaskAgeChecker:
    """Check for stale tasks based on creation time."""

    def __init__(
        self,
        work_dir: Path | None = None,
        age_threshold_hours: int = 24,
    ):
        """
        Initialize task age checker.

        Args:
            work_dir: Work directory path (defaults to auto-detect)
            age_threshold_hours: Age threshold in hours for warnings
        """
        if work_dir:
            self.work_dir = Path(work_dir)
        else:
            self.work_dir = get_work_dir(Path(__file__))

        self.collaboration_dir = self.work_dir / "collaboration"
        self.age_threshold_hours = age_threshold_hours

    def get_task_age_hours(self, task_data: dict) -> float | None:
        """
        Calculate task age in hours from created_at timestamp.

        Args:
            task_data: Task dictionary containing created_at field

        Returns:
            Age in hours, or None if created_at is missing/invalid
        """
        created_at = task_data.get("created_at")
        if not created_at:
            return None

        try:
            # Parse ISO8601 timestamp with Z suffix
            created_dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            age_delta = now - created_dt
            return age_delta.total_seconds() / 3600
        except (ValueError, AttributeError):
            return None

    def check_task_file(self, task_file: Path) -> dict | None:
        """
        Check a single task file for staleness.

        Args:
            task_file: Path to task YAML file

        Returns:
            Dict with task info if stale, None otherwise
        """
        try:
            with open(task_file, encoding="utf-8") as f:
                task_data = yaml.safe_load(f) or {}
        except (OSError, yaml.YAMLError):
            return None

        age_hours = self.get_task_age_hours(task_data)
        if age_hours is None:
            return None

        if age_hours >= self.age_threshold_hours:
            return {
                "file": str(task_file.relative_to(self.work_dir.parent)),
                "id": task_data.get("id", "unknown"),
                "agent": task_data.get("agent", "unknown"),
                "status": task_data.get("status", "unknown"),
                "age_hours": round(age_hours, 1),
                "created_at": task_data.get("created_at"),
                "title": task_data.get("title", ""),
            }

        return None

    def check_all_tasks(self) -> dict[str, list[dict]]:
        """
        Check all tasks in collaboration directories.

        Returns:
            Dict mapping state directories to lists of stale tasks
        """
        stale_tasks = {}

        # Check inbox, new, assigned, in_progress states
        # (done and archive are expected to be old)
        for state in ["inbox", "new", "assigned", "in_progress"]:
            state_dir = self.collaboration_dir / state
            if not state_dir.exists():
                continue

            stale_in_state = []

            # Check all YAML files recursively (including agent subdirectories)
            for task_file in state_dir.rglob("*.yaml"):
                stale_info = self.check_task_file(task_file)
                if stale_info:
                    stale_in_state.append(stale_info)

            if stale_in_state:
                stale_tasks[state] = stale_in_state

        return stale_tasks

    def format_text(self, stale_tasks: dict[str, list[dict]]) -> str:
        """
        Format stale tasks report as text.

        Args:
            stale_tasks: Dict mapping states to stale task lists

        Returns:
            Formatted text report
        """
        lines = []
        lines.append("Task Age Warning Report")
        lines.append("=" * 70)
        lines.append(f"Threshold: {self.age_threshold_hours} hours")
        lines.append("")

        total_stale = sum(len(tasks) for tasks in stale_tasks.values())

        if total_stale == 0:
            lines.append("✅ No stale tasks found.")
            return "\n".join(lines)

        lines.append(f"⚠️  Found {total_stale} stale task(s):")
        lines.append("")

        for state, tasks in sorted(stale_tasks.items()):
            lines.append(f"State: {state} ({len(tasks)} task(s))")
            lines.append("-" * 70)

            for task in sorted(tasks, key=lambda t: t["age_hours"], reverse=True):
                age_str = f"{task['age_hours']:.1f}h"
                if task["age_hours"] >= 48:
                    age_str = f"⚠️  {age_str} (>48h)"
                elif task["age_hours"] >= 24:
                    age_str = f"⚠️  {age_str}"

                lines.append(f"  [{age_str:>12}] {task['agent']:>18} | {task['id']}")
                if task["title"]:
                    lines.append(f"               {task['title']}")
                lines.append(f"               File: {task['file']}")
                lines.append("")

        lines.append("=" * 70)
        lines.append("Recommendation:")
        lines.append("  - Review stale tasks for outdated context")
        lines.append("  - Update task specifications if repository has changed")
        lines.append("  - Consider moving very old tasks (>48h) to archive")

        return "\n".join(lines)

    def format_json(self, stale_tasks: dict[str, list[dict]]) -> str:
        """
        Format stale tasks report as JSON.

        Args:
            stale_tasks: Dict mapping states to stale task lists

        Returns:
            JSON string
        """
        total_stale = sum(len(tasks) for tasks in stale_tasks.values())

        report = {
            "threshold_hours": self.age_threshold_hours,
            "total_stale_tasks": total_stale,
            "stale_by_state": stale_tasks,
            "has_warnings": total_stale > 0,
        }

        return json.dumps(report, indent=2)


def main() -> int:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Check for stale tasks in orchestration system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=24,
        help="Age threshold in hours (default: 24)",
    )

    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Only show warnings, don't fail on stale tasks",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--work-dir",
        type=Path,
        help="Path to work directory (default: auto-detect)",
    )

    args = parser.parse_args()

    checker = TaskAgeChecker(
        work_dir=args.work_dir,
        age_threshold_hours=args.threshold,
    )

    stale_tasks = checker.check_all_tasks()

    if args.format == "json":
        print(checker.format_json(stale_tasks))
    else:
        print(checker.format_text(stale_tasks))

    # Exit with error code if stale tasks found and not warn-only
    total_stale = sum(len(tasks) for tasks in stale_tasks.values())
    if total_stale > 0 and not args.warn_only:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
