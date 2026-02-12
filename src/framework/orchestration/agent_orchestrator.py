#!/usr/bin/env python3
"""
Agent Orchestrator - Multi-Agent Orchestration

Responsibilities:
- Assign tasks from inbox to agents
- Create follow-up tasks based on next_agent
- Monitor active tasks for timeouts
- Detect artifact conflicts
- Update status dashboard
- Archive old completed tasks
"""

from __future__ import annotations

import shutil
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from task_utils import (
    log_event,
    read_task,
    write_task,
)

from src.domain.collaboration.types import TaskStatus

# Configuration
WORK_DIR = Path("work")
COLLAB_DIR = WORK_DIR / "collaboration"
INBOX_DIR = COLLAB_DIR / "inbox"
ASSIGNED_DIR = COLLAB_DIR / "assigned"
DONE_DIR = COLLAB_DIR / "done"
ARCHIVE_DIR = COLLAB_DIR / "archive"

TIMEOUT_HOURS = 2  # Flag tasks in_progress for > 2 hours
ARCHIVE_RETENTION_DAYS = 30  # Archive tasks older than 30 days


def _log_event(message: str) -> None:
    """Append event to workflow log."""
    log_file = COLLAB_DIR / "WORKFLOW_LOG.md"
    log_event(message, log_file)


def assign_tasks() -> int:
    """Process inbox and assign tasks to agents."""
    tasks_assigned = 0

    for task_file in INBOX_DIR.glob("*.yaml"):
        try:
            task = read_task(task_file)
            agent = task.get("agent")

            if not agent:
                _log_event(f"⚠️ Task {task_file.name} missing 'agent' field")
                continue

            agent_dir = ASSIGNED_DIR / agent
            if not agent_dir.exists():
                _log_event(f"❗️ Unknown agent: {agent}")
                continue

            dest = agent_dir / task_file.name

            task["status"] = TaskStatus.ASSIGNED.value
            task["assigned_at"] = (
                datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            )
            write_task(dest, task)
            task_file.unlink()

            _log_event(f"Assigned task {task['id']} to {agent}")
            tasks_assigned += 1
        except Exception as exc:  # noqa: BLE001
            _log_event(f"❗️ Error assigning {task_file.name}: {exc}")

    return tasks_assigned


def log_handoff(
    from_agent: str, to_agent: str, artefacts: list[str], task_id: str
) -> None:
    """Log agent handoff."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    handoff_log = COLLAB_DIR / "HANDOFFS.md"
    handoff_log.parent.mkdir(parents=True, exist_ok=True)

    with open(handoff_log, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp} - {from_agent} → {to_agent}\n\n")
        f.write(f"**Artefacts:** {', '.join(artefacts)}\n")
        f.write(f"**Task ID:** {task_id}\n")
        f.write("**Status:** Created\n\n")


def process_completed_tasks() -> int:
    """Create follow-up tasks based on next_agent."""
    followups_created = 0

    for task_file in DONE_DIR.glob("**/*.yaml"):
        try:
            task = read_task(task_file)
            result = task.get("result", {})
            next_agent = result.get("next_agent")

            if not next_agent:
                continue

            followup_id = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M')}-{next_agent}-followup-{task['id']}"
            followup_file = INBOX_DIR / f"{followup_id}.yaml"

            if followup_file.exists():
                continue

            followup = {
                "id": followup_id,
                "agent": next_agent,
                "status": TaskStatus.NEW.value,
                "title": result.get("next_task_title", f"Follow-up to {task['id']}"),
                "artefacts": result.get("next_artefacts", task.get("artefacts", [])),
                "context": {
                    "previous_task": task.get("id"),
                    "previous_agent": task.get("agent"),
                    "notes": result.get("next_task_notes", []),
                },
                "created_at": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
                "created_by": "coordinator",
            }

            write_task(followup_file, followup)
            log_handoff(
                task.get("agent", "unknown"),
                next_agent,
                followup.get("artefacts", []),
                followup_id,
            )
            followups_created += 1
        except Exception as exc:  # noqa: BLE001
            _log_event(f"❗️ Error processing {task_file.name}: {exc}")

    return followups_created


def check_timeouts() -> int:
    """Flag tasks stuck in in_progress."""
    timeout_cutoff = datetime.now(timezone.utc) - timedelta(hours=TIMEOUT_HOURS)
    flagged = 0

    for agent_dir in ASSIGNED_DIR.iterdir():
        if not agent_dir.is_dir():
            continue

        for task_file in agent_dir.glob("*.yaml"):
            try:
                task = read_task(task_file)

                if task.get("status") != TaskStatus.IN_PROGRESS.value:
                    continue

                started_at_raw = task.get("started_at")
                if not started_at_raw:
                    _log_event(
                        f"⚠️ Task {task.get('id', task_file.name)} missing started_at; skipping timeout check"
                    )
                    continue

                started_at = datetime.fromisoformat(
                    str(started_at_raw).replace("Z", "+00:00")
                )

                if started_at < timeout_cutoff:
                    _log_event(f"⚠️ Task {task['id']} stalled (>{TIMEOUT_HOURS}h)")
                    flagged += 1
            except Exception as exc:  # noqa: BLE001
                _log_event(f"❗️ Error checking timeout for {task_file.name}: {exc}")

    return flagged


def detect_conflicts() -> int:
    """Warn when multiple tasks target same artifact."""
    artifact_map: dict[str, list[str]] = defaultdict(list)

    for agent_dir in ASSIGNED_DIR.iterdir():
        if not agent_dir.is_dir():
            continue

        for task_file in agent_dir.glob("*.yaml"):
            try:
                task = read_task(task_file)

                if task.get("status") == TaskStatus.IN_PROGRESS.value:
                    for artifact in task.get("artefacts", []):
                        artifact_map[str(artifact)].append(
                            task.get("id", task_file.name)
                        )
            except Exception as exc:  # noqa: BLE001
                _log_event(f"❗️ Error checking conflicts for {task_file.name}: {exc}")

    conflicts = 0
    for artifact, task_ids in artifact_map.items():
        if len(task_ids) > 1:
            _log_event(f"⚠️ Conflict: {artifact} targeted by {task_ids}")
            conflicts += 1

    return conflicts


def update_agent_status() -> None:
    """Update agent status dashboard."""
    status: dict[str, dict[str, Any]] = {}

    for agent_dir in ASSIGNED_DIR.iterdir():
        if not agent_dir.is_dir():
            continue

        agent = agent_dir.name
        tasks = list(agent_dir.glob("*.yaml"))

        in_progress = []
        assigned = []

        for task_file in tasks:
            try:
                task = read_task(task_file)
                if task.get("status") == TaskStatus.IN_PROGRESS.value:
                    in_progress.append(task)
                elif task.get("status") == TaskStatus.ASSIGNED.value:
                    assigned.append(task)
            except Exception:
                continue

        status[agent] = {
            "assigned": len(assigned),
            "in_progress": len(in_progress),
            "current_task": in_progress[0]["id"] if in_progress else "Idle",
            "last_seen": max([t.stat().st_mtime for t in tasks]) if tasks else None,
        }

    status_file = COLLAB_DIR / "AGENT_STATUS.md"
    status_file.parent.mkdir(parents=True, exist_ok=True)
    with open(status_file, "w", encoding="utf-8") as f:
        f.write("# Agent Status Dashboard\n\n")
        f.write(
            f"_Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}_\n\n"
        )

        for agent, info in sorted(status.items()):
            f.write(f"## {agent}\n\n")
            f.write(f"- **Status**: {info['current_task']}\n")
            f.write(f"- **Assigned**: {info['assigned']} tasks\n")
            f.write(f"- **In Progress**: {info['in_progress']} tasks\n")

            if info["last_seen"]:
                last_seen = datetime.fromtimestamp(info["last_seen"], tz=timezone.utc)
                f.write(f"- **Last seen**: {last_seen.strftime('%Y-%m-%d %H:%M:%S')}\n")

            f.write("\n")


def archive_old_tasks() -> int:
    """Move completed tasks to archive."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=ARCHIVE_RETENTION_DAYS)
    archived = 0

    for task_file in DONE_DIR.glob("**/*.yaml"):
        try:
            task_date_str = task_file.name[:10]
            task_date = datetime.strptime(task_date_str, "%Y-%m-%d")

            if task_date.date() < cutoff.date():
                year_month = task_date.strftime("%Y-%m")
                archive_month = ARCHIVE_DIR / year_month
                archive_month.mkdir(parents=True, exist_ok=True)

                dest = archive_month / task_file.name
                shutil.move(str(task_file), str(dest))
                archived += 1
        except Exception as exc:  # noqa: BLE001
            _log_event(f"❗️ Error archiving {task_file.name}: {exc}")

    return archived


def main() -> None:
    """Main coordinator loop."""
    print("🤖 Coordinator Agent - Starting cycle")

    for directory in [INBOX_DIR, ASSIGNED_DIR, DONE_DIR, ARCHIVE_DIR, COLLAB_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    assigned = assign_tasks()
    followups = process_completed_tasks()
    timeouts = check_timeouts()
    conflicts = detect_conflicts()
    archived = archive_old_tasks()
    update_agent_status()

    print("✅ Cycle complete:")
    print(f"   - Assigned: {assigned} tasks")
    print(f"   - Follow-ups created: {followups}")
    print(f"   - Timeouts flagged: {timeouts}")
    print(f"   - Conflicts detected: {conflicts}")
    print(f"   - Archived: {archived} tasks")

    _log_event(
        "Coordinator cycle: "
        f"{assigned} assigned, {followups} follow-ups, "
        f"{timeouts} timeouts, {conflicts} conflicts, {archived} archived"
    )


if __name__ == "__main__":
    main()
