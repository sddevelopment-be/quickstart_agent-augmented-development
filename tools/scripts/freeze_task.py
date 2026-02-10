#!/usr/bin/env python3
"""
Freeze Task Script

Moves a task to the fridge directory (pause/defer) with a freeze reason and timestamp.
Used when a task needs to be temporarily suspended.

Usage:
    python freeze_task.py TASK_ID --reason REASON [--work-dir PATH]

Example:
    python freeze_task.py 2026-02-09T2033-python-pedro-test-task --reason "Blocked on dependency"

Related ADRs:
    - ADR-042: Shared Task Domain Model
    - ADR-043: Status Enumeration Standard

Directive Compliance:
    - 017 (TDD): Implemented with test coverage
    - 021 (Locality): Preserves original task state
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add parent directory to path for imports
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from common.task_schema import read_task, write_task


def find_task_file(task_id: str, work_dir: Path) -> Path | None:
    """
    Find task file by ID in assigned directories.

    Args:
        task_id: Task identifier
        work_dir: Work collaboration directory

    Returns:
        Path to task file, or None if not found
    """
    assigned_dir = work_dir / "assigned"
    if not assigned_dir.exists():
        return None

    # Search for task in all agent subdirectories
    for task_file in assigned_dir.rglob(f"{task_id}.yaml"):
        return task_file

    return None


def get_utc_timestamp() -> str:
    """
    Get current UTC timestamp in ISO8601 format with Z suffix.

    Returns:
        ISO8601 timestamp string (e.g., "2026-02-09T20:33:00Z")
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def freeze_task(task_id: str, reason: str, work_dir: Path) -> None:
    """
    Freeze a task by moving it to fridge with reason and timestamp.

    Args:
        task_id: Task identifier
        reason: Reason for freezing the task
        work_dir: Work collaboration directory

    Raises:
        FileNotFoundError: If task file not found
        ValueError: If reason is empty
    """
    if not reason or not reason.strip():
        raise ValueError("Freeze reason is required and cannot be empty")

    # Find task file
    task_file = find_task_file(task_id, work_dir)
    if task_file is None:
        raise FileNotFoundError(f"Task not found: {task_id}")

    # Read task
    task = read_task(task_file)

    # Add freeze metadata (preserve original status)
    task["frozen_at"] = get_utc_timestamp()
    task["freeze_reason"] = reason.strip()

    # Determine destination path
    fridge_dir = work_dir / "fridge"
    fridge_dir.mkdir(parents=True, exist_ok=True)

    dest_path = fridge_dir / f"{task_id}.yaml"

    # Write updated task to destination
    write_task(dest_path, task)

    # Remove original file
    task_file.unlink()

    print(f"✓ Task {task_id} frozen successfully")
    print(f"  Status: {task.get('status', 'unknown')} (preserved)")
    print(f"  Frozen at: {task['frozen_at']}")
    print(f"  Reason: {reason}")
    print(f"  Moved to: {dest_path.relative_to(work_dir)}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Freeze a task by moving it to fridge directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  %(prog)s 2026-02-09T2033-python-pedro-test-task --reason "Blocked on dependency"
        """,
    )

    parser.add_argument(
        "task_id",
        help="Task identifier",
    )

    parser.add_argument(
        "--reason",
        required=True,
        help="Reason for freezing the task (required)",
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

    # Freeze task
    try:
        freeze_task(args.task_id, args.reason, args.work_dir)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error freezing task: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
