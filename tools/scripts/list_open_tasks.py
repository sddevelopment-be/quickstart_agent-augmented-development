#!/usr/bin/env python3
"""
List Open Tasks Script

Lists all tasks that are not in terminal states (done/error).
Supports filtering by status, agent, and priority.

Usage:
    python list_open_tasks.py [--work-dir PATH] [--status STATUS] [--agent AGENT] [--priority PRIORITY] [--format FORMAT]

Examples:
    # List all open tasks
    python list_open_tasks.py

    # List assigned tasks for python-pedro
    python list_open_tasks.py --status assigned --agent python-pedro

    # List high priority tasks as JSON
    python list_open_tasks.py --priority high --format json

Related ADRs:
    - ADR-042: Shared Task Domain Model
    - ADR-043: Status Enumeration Standard

Directive Compliance:
    - 017 (TDD): Implemented with test coverage
    - 021 (Locality): Uses extracted query functions from src/framework/orchestration/task_query.py

Note:
    Query functions (find_task_files, load_open_tasks, filter_tasks) were extracted
    to src/framework/orchestration/task_query.py for reuse by dashboard and other
    production components. This script now imports from the shared module.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Import shared query functions from production module (extracted from this script)
# See: src/framework/orchestration/task_query.py
from src.framework.orchestration.task_query import (
    find_task_files,
    load_open_tasks,
    filter_tasks,
)


def format_tasks_table(tasks: list[dict[str, Any]]) -> str:
    """
    Format tasks as a human-readable table.

    Args:
        tasks: List of task dictionaries

    Returns:
        Formatted table string
    """
    if not tasks:
        return "No open tasks found."

    # Calculate column widths
    id_width = max(len(t.get("id", "")) for t in tasks) if tasks else 10
    id_width = max(id_width, len("Task ID"))

    status_width = max(len(t.get("status", "")) for t in tasks) if tasks else 10
    status_width = max(status_width, len("Status"))

    agent_width = max(len(t.get("agent", "")) for t in tasks) if tasks else 10
    agent_width = max(agent_width, len("Agent"))

    priority_width = 8  # "Priority"

    # Build header
    header = (
        f"{'Task ID':<{id_width}}  "
        f"{'Status':<{status_width}}  "
        f"{'Agent':<{agent_width}}  "
        f"{'Priority':<{priority_width}}"
    )
    separator = "-" * len(header)

    lines = [header, separator]

    # Build rows
    for task in tasks:
        task_id = task.get("id", "N/A")
        status = task.get("status", "N/A")
        agent = task.get("agent", "N/A")
        priority = task.get("priority", "N/A")

        row = (
            f"{task_id:<{id_width}}  "
            f"{status:<{status_width}}  "
            f"{agent:<{agent_width}}  "
            f"{priority:<{priority_width}}"
        )
        lines.append(row)

    lines.append(f"\nTotal: {len(tasks)} task(s)")

    return "\n".join(lines)


def format_tasks_json(tasks: list[dict[str, Any]]) -> str:
    """
    Format tasks as JSON.

    Args:
        tasks: List of task dictionaries

    Returns:
        JSON string
    """
    # Extract only relevant fields for cleaner output
    simplified = []
    for task in tasks:
        simplified.append({
            "id": task.get("id"),
            "status": task.get("status"),
            "agent": task.get("agent"),
            "priority": task.get("priority"),
            "title": task.get("title"),
        })

    return json.dumps(simplified, indent=2)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List all open tasks (not done/error)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --status assigned
  %(prog)s --agent python-pedro --priority high
  %(prog)s --format json
        """,
    )

    parser.add_argument(
        "--work-dir",
        type=Path,
        default=REPO_ROOT / "work" / "collaboration",
        help="Work collaboration directory (default: work/collaboration)",
    )

    parser.add_argument(
        "--status",
        choices=["assigned", "in_progress", "blocked", "new", "inbox"],
        help="Filter by task status",
    )

    parser.add_argument(
        "--agent",
        help="Filter by agent name",
    )

    parser.add_argument(
        "--priority",
        choices=["low", "medium", "high", "critical"],
        help="Filter by priority level",
    )

    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format (default: table)",
    )

    args = parser.parse_args()

    # Validate work directory
    if not args.work_dir.exists():
        print(f"Error: Work directory not found: {args.work_dir}", file=sys.stderr)
        return 1

    # Load open tasks
    try:
        tasks = load_open_tasks(args.work_dir)
    except Exception as e:
        print(f"Error loading tasks: {e}", file=sys.stderr)
        return 1

    # Apply filters
    filtered_tasks = filter_tasks(
        tasks,
        status=args.status,
        agent=args.agent,
        priority=args.priority,
    )

    # Format output
    if args.format == "json":
        output = format_tasks_json(filtered_tasks)
    else:
        output = format_tasks_table(filtered_tasks)

    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
