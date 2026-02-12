#!/usr/bin/env python3
"""
Agent Base Class - Standard Template for File-Based Orchestration Agents

Provides standardized lifecycle hooks, status transitions, error handling,
and work log creation for agents in the file-based orchestration framework.

Usage:
    class MyAgent(AgentBase):
        def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
            # Implement your agent-specific logic here
            return {"output": "result"}
"""

from __future__ import annotations

import time
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from task_utils import get_utc_timestamp, log_event, read_task, write_task

from src.domain.collaboration.types import TaskStatus


class AgentBase(ABC):
    """
    Abstract base class for file-based orchestration agents.

    Handles:
    - Task loading from assigned/<agent>/ directory
    - Status transition enforcement (assigned → in_progress → done/error)
    - Timing metrics capture
    - Result block generation
    - Work log creation
    - Error handling with proper error status
    - Artifact validation
    """

    def __init__(
        self,
        agent_name: str,
        work_dir: Path | str = "work",
        mode: str = "/analysis-mode",
        log_level: str = "INFO",
    ):
        """
        Initialize the agent.

        Args:
            agent_name: Name of the agent (must match directory under work/assigned/)
            work_dir: Path to work directory (default: "work")
            mode: Reasoning mode (/analysis-mode, /creative-mode, /meta-mode)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.agent_name = agent_name
        self.work_dir = Path(work_dir)
        self.mode = mode
        self.log_level = log_level

        # Directory paths
        self.collaboration_dir = self.work_dir / "collaboration"
        self.assigned_dir = self.collaboration_dir / "assigned" / agent_name
        self.done_dir = self.collaboration_dir / "done" / agent_name
        self.reports_dir = self.work_dir / "reports"
        self.logs_dir = self.reports_dir / "logs" / agent_name

        # Ensure directories exist
        self.collaboration_dir.mkdir(parents=True, exist_ok=True)
        self.assigned_dir.mkdir(parents=True, exist_ok=True)
        self.done_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Task tracking
        self.current_task: dict[str, Any] | None = None
        self.current_task_file: Path | None = None
        self.start_time: float | None = None
        self.artifacts_created: list[str] = []

        self._log(f"✅ Agent '{agent_name}' initialized in mode: {mode}")

    def _log(self, message: str, level: str = "INFO") -> None:
        """Log a message with timestamp."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"[{timestamp}] [{level}] {message}")

    def _log_event(self, message: str) -> None:
        """Append event to workflow log."""
        log_file = self.collaboration_dir / "WORKFLOW_LOG.md"
        log_event(f"[{self.agent_name}] {message}", log_file)

    def read_task(self, task_file: Path) -> dict[str, Any]:
        """Load task YAML."""
        return read_task(task_file)

    def write_task(self, task_file: Path, task: dict[str, Any]) -> None:
        """Save task YAML."""
        write_task(task_file, task)

    def find_assigned_tasks(self) -> list[Path]:
        """Find all tasks assigned to this agent."""
        return sorted(self.assigned_dir.glob("*.yaml"))

    def update_task_status(
        self,
        status: str | TaskStatus,
        additional_fields: dict[str, Any] | None = None,
    ) -> None:
        """
        Update task status and write to file.

        Args:
            status: New status (TaskStatus enum or string: assigned, in_progress, done, error)
            additional_fields: Additional fields to add to task

        Note:
            Accepts both string and TaskStatus enum for backward compatibility (ADR-043).
        """
        if not self.current_task or not self.current_task_file:
            raise RuntimeError("No current task to update")

        # Convert enum to string value if needed
        status_value = status.value if isinstance(status, TaskStatus) else status
        self.current_task["status"] = status_value

        if (
            status_value == TaskStatus.IN_PROGRESS.value
            and "started_at" not in self.current_task
        ):
            self.current_task["started_at"] = get_utc_timestamp()

        if additional_fields:
            self.current_task.update(additional_fields)

        self.write_task(self.current_task_file, self.current_task)
        self._log(f"Updated task {self.current_task['id']} to status: {status_value}")

    def validate_artifacts(self, artifacts: list[str]) -> tuple[list[str], list[str]]:
        """
        Validate that artifacts exist.

        Returns:
            Tuple of (existing_artifacts, missing_artifacts)
        """
        existing = []
        missing = []

        for artifact in artifacts:
            artifact_path = Path(artifact)
            if artifact_path.exists():
                existing.append(artifact)
            else:
                missing.append(artifact)

        return existing, missing

    def create_result_block(
        self,
        summary: str,
        artifacts: list[str] | None = None,
        next_agent: str | None = None,
        next_task_title: str | None = None,
        next_artifacts: list[str] | None = None,
        next_task_notes: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Create a result block for successful task completion.

        Args:
            summary: Brief description of work completed
            artifacts: List of artifacts created/modified
            next_agent: Optional agent to hand off to
            next_task_title: Optional title for follow-up task
            next_artifacts: Optional artifacts for follow-up task
            next_task_notes: Optional notes for follow-up task

        Returns:
            Result dictionary to add to task
        """
        result = {
            "summary": summary,
            "artefacts": artifacts or self.artifacts_created,
            "completed_at": get_utc_timestamp(),
        }

        if next_agent:
            result["next_agent"] = next_agent
            if next_task_title:
                result["next_task_title"] = next_task_title
            if next_artifacts:
                result["next_artefacts"] = next_artifacts
            if next_task_notes:
                result["next_task_notes"] = next_task_notes

        return result

    def create_error_block(
        self,
        error_message: str,
        retry_count: int = 0,
        stacktrace: str | None = None,
    ) -> dict[str, Any]:
        """
        Create an error block for failed task.

        Args:
            error_message: Description of what went wrong
            retry_count: Number of retry attempts
            stacktrace: Optional detailed error trace

        Returns:
            Error dictionary to add to task
        """
        error = {
            "message": error_message,
            "timestamp": get_utc_timestamp(),
            "agent": self.agent_name,
            "retry_count": retry_count,
        }

        if stacktrace:
            error["stacktrace"] = stacktrace

        return error

    def move_to_done(self) -> None:
        """Move current task file to done directory."""
        if not self.current_task_file:
            raise RuntimeError("No current task file to move")

        dest = self.done_dir / self.current_task_file.name
        self.current_task_file.rename(dest)
        self._log(f"Moved task {self.current_task['id']} to done/")
        self._log_event(f"Task {self.current_task['id']} completed successfully")
        self.current_task_file = dest

    def create_work_log(
        self,
        title: str,
        context: str,
        approach: str,
        execution_steps: list[str],
        outcomes: str,
        lessons_learned: str,
        directives_used: dict[str, Any] | None = None,
        additional_sections: dict[str, str] | None = None,
    ) -> Path:
        """
        Create a work log following Directive 014 standards.

        Args:
            title: Brief title for work log
            context: What prompted this work
            approach: Explanation of approach taken
            execution_steps: Chronological list of actions
            outcomes: Results of the work
            lessons_learned: Reflections for improvement
            directives_used: Which guidelines/directives were used
            additional_sections: Optional extra sections

        Returns:
            Path to created work log file
        """
        if not self.current_task:
            raise RuntimeError("No current task for work log")

        timestamp = datetime.now(timezone.utc)
        slug = (
            self.current_task["id"].split("-", 3)[-1]
            if "id" in self.current_task
            else "work"
        )
        log_filename = (
            f"{timestamp.strftime('%Y-%m-%dT%H%M')}-{self.agent_name}-{slug}.md"
        )
        log_file = self.logs_dir / log_filename

        duration = time.time() - self.start_time if self.start_time else 0
        duration_str = f"{duration:.2f}s"
        if duration > 60:
            duration_str = f"{duration/60:.2f}m"

        directives = directives_used or {
            "general_guidelines": True,
            "operational_guidelines": True,
            "specific_directives": ["014"],
            "agent_profile": self.agent_name,
            "reasoning_mode": self.mode,
        }

        content = f"""# Work Log: {title}

**Agent:** {self.agent_name}
**Task ID:** {self.current_task.get('id', 'N/A')}
**Date:** {timestamp.isoformat().replace('+00:00', 'Z')}
**Status:** completed

## Context

{context}

## Approach

{approach}

## Guidelines & Directives Used

- General Guidelines: {"yes" if directives.get("general_guidelines") else "no"}
- Operational Guidelines: {"yes" if directives.get("operational_guidelines") else "no"}
- Specific Directives: {', '.join(directives.get("specific_directives", []))}
- Agent Profile: {directives.get("agent_profile", self.agent_name)}
- Reasoning Mode: {directives.get("reasoning_mode", self.mode)}

## Execution Steps

"""

        for i, step in enumerate(execution_steps, 1):
            content += f"{i}. {step}\n"

        content += """
## Artifacts Created

"""
        for artifact in self.artifacts_created:
            content += f"- `{artifact}` - Created/modified by {self.agent_name}\n"

        content += """
## Outcomes

""" + outcomes + """

## Lessons Learned

""" + lessons_learned + """

## Metadata

- **Duration:** """ + duration_str + """
- **Token Count:**
  - Input tokens: (estimated from context)
  - Output tokens: (estimated from artifacts)
  - Total tokens: (estimated)
- **Context Size:** {len(execution_steps)} steps
- **Handoff To:** {self.current_task.get('result', {}).get('next_agent', 'N/A')}
- **Related Tasks:** {self.current_task.get('id', 'N/A')}
"""

        if additional_sections:
            for section_title, section_content in additional_sections.items():
                content += f"\n## {section_title}\n\n{section_content}\n"

        with open(log_file, "w", encoding="utf-8") as f:
            f.write(content)

        self._log(f"Created work log: {log_file}")
        return log_file

    # Abstract methods to be implemented by subclasses

    @abstractmethod
    def validate_task(self, task: dict[str, Any]) -> bool:
        """
        Validate that the task is suitable for this agent.

        Args:
            task: Task dictionary loaded from YAML

        Returns:
            True if task is valid, False otherwise

        Raises:
            ValueError: If task is invalid with explanation
        """
        pass

    @abstractmethod
    def execute_task(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the agent-specific task logic.

        Args:
            task: Task dictionary with all requirements

        Returns:
            Dictionary with execution results

        Raises:
            Exception: If task execution fails
        """
        pass

    # Lifecycle hooks (optional overrides)

    def init_task(self, task: dict[str, Any]) -> None:  # noqa: B027
        """
        Initialize task-specific state before execution.

        Override this method to perform setup actions.
        """
        pass

    def finalize_task(self, success: bool) -> None:  # noqa: B027
        """
        Clean up after task execution.

        Override this method to perform cleanup actions.

        Args:
            success: Whether task completed successfully
        """
        pass

    # Main execution flow

    def process_next_task(self) -> bool:
        """
        Find and process the next assigned task.

        Returns:
            True if a task was processed, False if no tasks available
        """
        tasks = self.find_assigned_tasks()

        if not tasks:
            self._log("No tasks assigned", level="INFO")
            return False

        # Pick first task with status "assigned"
        for task_file in tasks:
            task = self.read_task(task_file)
            if task.get("status") == TaskStatus.ASSIGNED.value:
                self._process_task(task_file, task)
                return True

        self._log("No tasks with status 'assigned'", level="INFO")
        return False

    def _process_task(self, task_file: Path, task: dict[str, Any]) -> None:
        """Internal method to process a single task."""
        self.current_task = task
        self.current_task_file = task_file
        self.start_time = time.time()
        self.artifacts_created = []

        task_id = task.get("id", task_file.name)
        self._log(f"🤖 Processing task: {task_id}")
        self._log_event(f"Started task {task_id}")

        try:
            # Update to in_progress
            self.update_task_status("in_progress")

            # Validate task
            if not self.validate_task(task):
                raise ValueError("Task validation failed")

            # Initialize
            self.init_task(task)

            # Execute
            result_data = self.execute_task(task)

            # Create result block
            result = self.create_result_block(
                summary=result_data.get("summary", "Task completed successfully"),
                artifacts=result_data.get("artifacts", self.artifacts_created),
                next_agent=result_data.get("next_agent"),
                next_task_title=result_data.get("next_task_title"),
                next_artifacts=result_data.get("next_artifacts"),
                next_task_notes=result_data.get("next_task_notes"),
            )

            # Update task with result
            self.update_task_status("done", {"result": result})

            # Move to done
            self.move_to_done()

            # Finalize
            self.finalize_task(success=True)

            self._log(f"✅ Task {task_id} completed successfully")

        except Exception as exc:
            self._log(f"❗️ Task {task_id} failed: {exc}", level="ERROR")
            self._log_event(f"Task {task_id} failed: {exc}")

            error = self.create_error_block(
                error_message=str(exc),
                retry_count=task.get("error", {}).get("retry_count", 0),
                stacktrace=traceback.format_exc(),
            )

            self.update_task_status("error", {"error": error})
            self.finalize_task(success=False)

            raise

    def run(self, continuous: bool = False) -> None:
        """
        Run the agent to process tasks.

        Args:
            continuous: If True, keep polling for tasks; if False, process one task and exit
        """
        self._log(f"🚀 Agent {self.agent_name} starting...")

        if continuous:
            self._log("Running in continuous mode (Ctrl+C to stop)")
            try:
                while True:
                    processed = self.process_next_task()
                    if not processed:
                        time.sleep(5)  # Poll every 5 seconds
            except KeyboardInterrupt:
                self._log("Agent stopped by user")
        else:
            self.process_next_task()


def timing_decorator(func):
    """Decorator to capture timing metrics for methods."""

    def wrapper(*args, **kwargs):
        """Inner wrapper function that executes the decorated function."""
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        if hasattr(args[0], "_log"):
            args[0]._log(f"Method {func.__name__} took {duration:.2f}s")

        return result

    return wrapper
