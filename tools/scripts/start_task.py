#!/usr/bin/env python3
"""
Start Task Script

Marks a task as in_progress by updating its status and adding a started_at timestamp.
Task remains in the assigned/{agent}/ directory.

Usage:
    python start_task.py TASK_ID [--work-dir PATH]

Example:
    python start_task.py 2026-02-09T2033-python-pedro-test-task

Related ADRs:
    - ADR-042: Shared Task Domain Model
    - ADR-043: Status Enumeration Standard

Directive Compliance:
    - 017 (TDD): Implemented with test coverage
    - 021 (Locality): Minimal changes to task state
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from common.task_schema import read_task, write_task
from common.types import TaskStatus
from framework.orchestration.task_utils import find_task_file, get_utc_timestamp


def start_task(task_id: str, work_dir: Path) -> None:
    """
    Start a task by updating status to in_progress.

    Args:
        task_id: Task identifier
        work_dir: Work collaboration directory

    Raises:
        FileNotFoundError: If task file not found
        ValueError: If task is not in 'assigned' state
        TaskValidationError: If task structure is invalid
    """
    # Find task file
    task_file = find_task_file(task_id, work_dir)
    if task_file is None:
        raise FileNotFoundError(f"Task not found: {task_id}")

    # Read task
    task = read_task(task_file)

    # Validate current status
    current_status = task.get("status")
    if current_status != TaskStatus.ASSIGNED.value:
        raise ValueError(
            f"Task must be in 'assigned' state to start. Current status: {current_status}"
        )

    # Update task
    task["status"] = TaskStatus.IN_PROGRESS.value
    task["started_at"] = get_utc_timestamp()

    # Write task back to same location
    write_task(task_file, task)

    print(f"✓ Task {task_id} started successfully")
    print("  Status: assigned → in_progress")
    print(f"  Started at: {task['started_at']}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mark a task as in_progress",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s 2026-02-09T2033-python-pedro-test-task
        """,
    )

    parser.add_argument(
        "task_id",
        help="Task identifier",
    )

    parser.add_argument(
        "--work-dir",
        type=Path,
        default=REPO_ROOT / "work" / "collaboration",
        help="Work collaboration directory (default: work/collaboration)",
    )

    args = parser.parse_args()

    # Validate work directory
    if not args.work_dir.exists():
        print(f"Error: Work directory not found: {args.work_dir}", file=sys.stderr)
        return 1

    # Start task
    try:
        start_task(args.task_id, args.work_dir)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error starting task: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
