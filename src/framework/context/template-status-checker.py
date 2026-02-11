#!/usr/bin/env python3
"""
Template Status Checker

Purpose: Automate status reporting for run-iteration.md issue template.
Replaces template-status-checker.sh with improved maintainability.

Usage:
    python3 template-status-checker.py [--validate] [--format=json]
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for common utilities
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.domain.common.path_utils import get_work_dir


class TemplateStatusChecker:
    """Check status of iteration template tasks."""

    def __init__(self, work_dir: Path | None = None):
        """
        Initialize status checker.

        Args:
            work_dir: Work directory path (defaults to auto-detect)
        """
        if work_dir:
            self.work_dir = Path(work_dir)
        else:
            # Auto-detect using common utility
            self.work_dir = get_work_dir(Path(__file__))

        self.collaboration_dir = self.work_dir / "collaboration"

    def count_tasks(self, directory: Path, pattern: str = "*.yaml") -> int:
        """
        Count task files in a directory (including subdirectories).

        Args:
            directory: Directory to search
            pattern: File pattern to match

        Returns:
            Number of matching files
        """
        if not directory.exists():
            return 0

        # Use rglob to search recursively (including subdirectories for agents)
        return len(list(directory.rglob(pattern)))

    def get_agent_breakdown(self, base_dir: Path) -> dict[str, int]:
        """
        Get task breakdown by agent.

        Args:
            base_dir: Base directory containing agent subdirectories

        Returns:
            Dictionary mapping agent names to task counts
        """
        breakdown = {}
        if not base_dir.exists():
            return breakdown

        for agent_dir in base_dir.iterdir():
            if agent_dir.is_dir():
                count = len(list(agent_dir.glob("*.yaml")))
                if count > 0:
                    breakdown[agent_dir.name] = count

        return breakdown

    def generate_status(self, validate: bool = False) -> dict[str, any]:
        """
        Generate status report.

        Args:
            validate: Whether to run validation checks

        Returns:
            Dictionary containing status information
        """
        status = {
            "inbox": {
                "count": self.count_tasks(self.collaboration_dir / "inbox"),
                "agents": self.get_agent_breakdown(self.collaboration_dir / "inbox"),
            },
            "new": {
                "count": self.count_tasks(self.collaboration_dir / "new"),
                "agents": self.get_agent_breakdown(self.collaboration_dir / "new"),
            },
            "assigned": {
                "count": self.count_tasks(self.collaboration_dir / "assigned"),
                "agents": self.get_agent_breakdown(self.collaboration_dir / "assigned"),
            },
            "in_progress": {
                "count": self.count_tasks(self.collaboration_dir / "in_progress"),
                "agents": self.get_agent_breakdown(
                    self.collaboration_dir / "in_progress"
                ),
            },
            "done": {
                "count": self.count_tasks(self.collaboration_dir / "done"),
                "agents": self.get_agent_breakdown(self.collaboration_dir / "done"),
            },
            "archive": {
                "count": self.count_tasks(self.collaboration_dir / "archive"),
            },
        }

        # Calculate totals
        status["total"] = sum(
            status[key]["count"]
            for key in ["inbox", "new", "assigned", "in_progress", "done", "archive"]
        )

        if validate:
            status["validation"] = self.validate_criteria(status)

        return status

    def validate_criteria(self, status: dict) -> dict[str, bool]:
        """
        Validate success criteria.

        Args:
            status: Status dictionary

        Returns:
            Dictionary of validation results
        """
        return {
            "inbox_empty": status["inbox"]["count"] == 0,
            "no_stalled_tasks": status["in_progress"]["count"] < 5,
            "tasks_completed": status["done"]["count"] > 0,
            "archive_exists": status["archive"]["count"] >= 0,
        }

    def format_text(self, status: dict) -> str:
        """
        Format status as text output.

        Args:
            status: Status dictionary

        Returns:
            Formatted text
        """
        lines = []
        lines.append("Task Status Report")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Total Tasks: {status['total']}")
        lines.append("")

        for stage in ["inbox", "new", "assigned", "in_progress", "done", "archive"]:
            stage_data = status[stage]
            count = stage_data["count"]
            lines.append(f"{stage.replace('_', ' ').title()}: {count}")

            if "agents" in stage_data and stage_data["agents"]:
                for agent, agent_count in sorted(stage_data["agents"].items()):
                    lines.append(f"  - {agent}: {agent_count}")

        if "validation" in status:
            lines.append("")
            lines.append("Validation:")
            for criterion, passed in status["validation"].items():
                symbol = "✅" if passed else "❌"
                lines.append(f"  {symbol} {criterion.replace('_', ' ').title()}")

        return "\n".join(lines)

    def format_json(self, status: dict) -> str:
        """
        Format status as JSON output.

        Args:
            status: Status dictionary

        Returns:
            JSON string
        """
        return json.dumps(status, indent=2)


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Check template status for iteration reporting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Check success criteria and output validation report",
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

    checker = TemplateStatusChecker(args.work_dir)
    status = checker.generate_status(validate=args.validate)

    if args.format == "json":
        print(checker.format_json(status))
    else:
        print(checker.format_text(status))


if __name__ == "__main__":
    main()
