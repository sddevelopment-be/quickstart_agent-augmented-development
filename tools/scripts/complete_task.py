#!/usr/bin/env python3
"""
Complete Task Script

Marks a task as done and moves it from assigned/{agent}/ to done/{agent}/.
Validates that a result block exists before completion (unless --force is used).

Usage:
    python complete_task.py TASK_ID [--work-dir PATH] [--force]

Example:
    python complete_task.py 2026-02-09T2033-python-pedro-test-task
    python complete_task.py 2026-02-09T2033-python-pedro-test-task --force

Related ADRs:
    - ADR-042: Shared Task Domain Model
    - ADR-043: Status Enumeration Standard

Directive Compliance:
    - 017 (TDD): Implemented with test coverage
    - 021 (Locality): Minimal changes, preserves task data
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.domain.collaboration.task_schema import read_task, write_task
from src.domain.collaboration.types import TaskStatus
from src.framework.orchestration.task_utils import find_task_file, get_utc_timestamp


def complete_task(task_id: str, work_dir: Path, force: bool = False) -> None:
    """
    Complete a task by marking it done and moving to done directory.

    Args:
        task_id: Task identifier
        work_dir: Work collaboration directory
        force: Skip result validation if True

    Raises:
        FileNotFoundError: If task file not found
        ValueError: If task validation fails
    """
    # Find task file
    task_file = find_task_file(task_id, work_dir)
    if task_file is None:
        raise FileNotFoundError(f"Task not found: {task_id}")

    # Read task
    task = read_task(task_file)

    # Extract agent from task
    agent = task.get("agent")
    if not agent:
        raise ValueError("Task missing 'agent' field")

    # Validate result block exists (unless force)
    if not force and "result" not in task:
        raise ValueError(
            "Task must have a 'result' block before completion. "
            "Add task result or use --force to skip validation."
        )

    # Validate state transition using centralized state machine
    current_status_str = task.get("status")
    try:
        current_status = TaskStatus(current_status_str)
    except ValueError:
        raise ValueError(f"Invalid current status: {current_status_str}")

    TaskStatus.validate_transition(current_status, TaskStatus.DONE)

    # Update task status
    task["status"] = TaskStatus.DONE.value
    task["completed_at"] = get_utc_timestamp()

    # Determine destination path
    done_dir = work_dir / "done" / agent
    done_dir.mkdir(parents=True, exist_ok=True)

    dest_path = done_dir / f"{task_id}.yaml"

    # Write updated task to destination
    write_task(dest_path, task)

    # Remove original file
    task_file.unlink()

    print(f"✓ Task {task_id} completed successfully")
    print(f"  Status: {current_status.value} → done")
    print(f"  Completed at: {task['completed_at']}")
    print(f"  Moved to: {dest_path.relative_to(work_dir)}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mark a task as done and move to done directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 2026-02-09T2033-python-pedro-test-task
  %(prog)s 2026-02-09T2033-python-pedro-test-task --force
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

    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip result validation and complete anyway",
    )

    args = parser.parse_args()

    # Validate work directory
    if not args.work_dir.exists():
        print(f"Error: Work directory not found: {args.work_dir}", file=sys.stderr)
        return 1

    # Complete task
    try:
        complete_task(args.task_id, args.work_dir, force=args.force)
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error completing task: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
