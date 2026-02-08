"""Tests for framework.core module.

Tests orchestration and governance logic (Layer 1).

References:
    - docs/styleguides/python_conventions.md (Quad-A pattern)
    - framework/core/
"""

from pathlib import Path

import pytest

from framework.core import AgentProfile, Orchestrator, Task, TaskStatus


class TestTaskStatus:
    """Test suite for TaskStatus enum."""

    def test_task_status_values(self) -> None:
        """Test TaskStatus enum contains expected values."""
        # Arrange
        expected_statuses = {
            "inbox",
            "assigned",
            "in_progress",
            "blocked",
            "done",
            "cancelled",
        }

        # Act
        actual_statuses = {status.value for status in TaskStatus}

        # Assert
        assert actual_statuses == expected_statuses


class TestAgentProfile:
    """Test suite for AgentProfile dataclass."""

    def test_agent_profile_minimal_valid(self) -> None:
        """Test creating agent profile with minimal valid data."""
        # Arrange & Act
        profile = AgentProfile(
            name="test-agent",
            specialization="testing",
            directives=["001", "014"],
        )

        # Assert
        assert profile.name == "test-agent"
        assert profile.specialization == "testing"
        assert profile.directives == ["001", "014"]
        assert profile.mode_default == "analysis"
        assert profile.capabilities == []

    def test_agent_profile_empty_name_raises_error(self) -> None:
        """Test agent profile with empty name raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError) as exc_info:
            AgentProfile(name="", specialization="test", directives=[])

        assert "name cannot be empty" in str(exc_info.value).lower()

    def test_agent_profile_empty_specialization_raises_error(self) -> None:
        """Test agent profile with empty specialization raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError) as exc_info:
            AgentProfile(name="test", specialization="", directives=[])

        assert "specialization cannot be empty" in str(exc_info.value).lower()

    def test_agent_profile_with_capabilities(self) -> None:
        """Test agent profile with custom capabilities."""
        # Arrange
        capabilities = ["analyze", "refactor", "validate"]

        # Act
        profile = AgentProfile(
            name="test-agent",
            specialization="testing",
            directives=["001"],
            capabilities=capabilities,
        )

        # Assert
        assert profile.capabilities == capabilities


class TestTask:
    """Test suite for Task dataclass."""

    def test_task_minimal_valid(self) -> None:
        """Test creating task with minimal valid data."""
        # Arrange & Act
        task = Task(
            id="2025-11-30-test-task",
            title="Test Task",
            status=TaskStatus.INBOX,
        )

        # Assert
        assert task.id == "2025-11-30-test-task"
        assert task.title == "Test Task"
        assert task.status == TaskStatus.INBOX
        assert task.agent is None
        assert task.priority == "normal"
        assert task.acceptance_criteria == []
        assert task.dependencies == []

    def test_task_empty_id_raises_error(self) -> None:
        """Test task with empty ID raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Task(id="", title="Test", status=TaskStatus.INBOX)

        assert "id cannot be empty" in str(exc_info.value).lower()

    def test_task_empty_title_raises_error(self) -> None:
        """Test task with empty title raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Task(id="test-id", title="", status=TaskStatus.INBOX)

        assert "title cannot be empty" in str(exc_info.value).lower()

    def test_task_invalid_priority_raises_error(self) -> None:
        """Test task with invalid priority raises ValueError."""
        # Arrange
        invalid_priority = "super-urgent"

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            Task(
                id="test-id",
                title="Test",
                status=TaskStatus.INBOX,
                priority=invalid_priority,
            )

        assert "invalid priority" in str(exc_info.value).lower()
        assert invalid_priority in str(exc_info.value)

    def test_task_valid_priorities(self) -> None:
        """Test task accepts all valid priority values."""
        # Arrange
        valid_priorities = ["critical", "high", "medium", "normal"]

        # Act & Assert
        for priority in valid_priorities:
            task = Task(
                id=f"test-{priority}",
                title="Test",
                status=TaskStatus.INBOX,
                priority=priority,
            )
            assert task.priority == priority

    def test_task_with_all_fields(self) -> None:
        """Test creating task with all optional fields populated."""
        # Arrange
        acceptance_criteria = ["Criterion 1", "Criterion 2"]
        dependencies = ["dep-1", "dep-2"]

        # Act
        task = Task(
            id="test-id",
            title="Test Task",
            status=TaskStatus.ASSIGNED,
            agent="test-agent",
            priority="high",
            description="Detailed description",
            acceptance_criteria=acceptance_criteria,
            dependencies=dependencies,
        )

        # Assert
        assert task.agent == "test-agent"
        assert task.priority == "high"
        assert task.description == "Detailed description"
        assert task.acceptance_criteria == acceptance_criteria
        assert task.dependencies == dependencies


class TestOrchestrator:
    """Test suite for Orchestrator class."""

    def test_orchestrator_init_valid_dirs(self, tmp_path: Path) -> None:
        """Test orchestrator initialization with valid directories."""
        # Arrange
        agents_dir = tmp_path / "agents"
        work_dir = tmp_path / "work"
        agents_dir.mkdir()
        work_dir.mkdir()

        # Assumption Check
        assert agents_dir.exists(), "Test precondition failed: agents_dir should exist"
        assert work_dir.exists(), "Test precondition failed: work_dir should exist"

        # Act
        orchestrator = Orchestrator(agents_dir=agents_dir, work_dir=work_dir)

        # Assert
        assert orchestrator.agents_dir == agents_dir
        assert orchestrator.work_dir == work_dir

    def test_orchestrator_init_missing_agents_dir_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Test orchestrator init raises FileNotFoundError for missing agents_dir."""
        # Arrange
        missing_agents_dir = tmp_path / "missing_agents"
        work_dir = tmp_path / "work"
        work_dir.mkdir()

        # Assumption Check
        assert not missing_agents_dir.exists(), (
            "Test precondition failed: agents_dir should NOT exist"
        )

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            Orchestrator(agents_dir=missing_agents_dir, work_dir=work_dir)

        assert "agents directory" in str(exc_info.value).lower()

    def test_orchestrator_init_missing_work_dir_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Test orchestrator init raises FileNotFoundError for missing work_dir."""
        # Arrange
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        missing_work_dir = tmp_path / "missing_work"

        # Assumption Check
        assert not missing_work_dir.exists(), (
            "Test precondition failed: work_dir should NOT exist"
        )

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            Orchestrator(agents_dir=agents_dir, work_dir=missing_work_dir)

        assert "work directory" in str(exc_info.value).lower()

    def test_transition_task_valid_transitions(self, tmp_path: Path) -> None:
        """Test valid task status transitions succeed."""
        # Arrange
        agents_dir = tmp_path / "agents"
        work_dir = tmp_path / "work"
        agents_dir.mkdir()
        work_dir.mkdir()

        orchestrator = Orchestrator(agents_dir=agents_dir, work_dir=work_dir)
        task = Task(id="test", title="Test", status=TaskStatus.INBOX)

        # Assumption Check
        assert task.status == TaskStatus.INBOX, (
            "Test precondition failed: task should be in INBOX"
        )

        # Act
        orchestrator.transition_task(task, TaskStatus.ASSIGNED)

        # Assert
        assert task.status == TaskStatus.ASSIGNED

    def test_transition_task_invalid_transition_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Test invalid task transition raises ValueError."""
        # Arrange
        agents_dir = tmp_path / "agents"
        work_dir = tmp_path / "work"
        agents_dir.mkdir()
        work_dir.mkdir()

        orchestrator = Orchestrator(agents_dir=agents_dir, work_dir=work_dir)
        task = Task(id="test", title="Test", status=TaskStatus.INBOX)

        # Assumption Check
        assert task.status == TaskStatus.INBOX, (
            "Test precondition failed: task should be in INBOX"
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            orchestrator.transition_task(task, TaskStatus.DONE)

        assert "invalid transition" in str(exc_info.value).lower()

    def test_assign_task_no_profiles_loaded_raises_error(
        self, tmp_path: Path
    ) -> None:
        """Test assign_task raises RuntimeError when no profiles loaded."""
        # Arrange
        agents_dir = tmp_path / "agents"
        work_dir = tmp_path / "work"
        agents_dir.mkdir()
        work_dir.mkdir()

        orchestrator = Orchestrator(agents_dir=agents_dir, work_dir=work_dir)
        task = Task(id="test", title="Test", status=TaskStatus.INBOX)

        # Assumption Check
        assert not orchestrator._profiles, (
            "Test precondition failed: no profiles should be loaded"
        )

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            orchestrator.assign_task(task)

        assert "no agent profiles" in str(exc_info.value).lower()
