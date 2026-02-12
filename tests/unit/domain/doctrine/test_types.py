"""
Tests for shared type definitions.

Tests TaskStatus, FeatureStatus, TaskMode, TaskPriority enums and AgentIdentity validation.
"""

import pytest
from src.domain.collaboration.types import TaskStatus, TaskMode, TaskPriority
from src.domain.doctrine.types import AgentIdentity, validate_agent, get_all_agents
from src.domain.specifications.types import FeatureStatus


class TestTaskStatus:
    """Test TaskStatus enum."""
    
    def test_task_status_values(self):
        """Verify all TaskStatus values."""
        assert TaskStatus.NEW.value == "new"
        assert TaskStatus.INBOX.value == "inbox"
        assert TaskStatus.ASSIGNED.value == "assigned"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.BLOCKED.value == "blocked"
        assert TaskStatus.DONE.value == "done"
        assert TaskStatus.ERROR.value == "error"
    
    def test_task_status_is_terminal(self):
        """Test is_terminal() classifier."""
        assert TaskStatus.is_terminal(TaskStatus.DONE) is True
        assert TaskStatus.is_terminal(TaskStatus.ERROR) is True
        assert TaskStatus.is_terminal(TaskStatus.IN_PROGRESS) is False
        assert TaskStatus.is_terminal(TaskStatus.ASSIGNED) is False
    
    def test_task_status_is_active(self):
        """Test is_active() classifier."""
        assert TaskStatus.is_active(TaskStatus.ASSIGNED) is True
        assert TaskStatus.is_active(TaskStatus.IN_PROGRESS) is True
        assert TaskStatus.is_active(TaskStatus.BLOCKED) is True
        assert TaskStatus.is_active(TaskStatus.DONE) is False
        assert TaskStatus.is_active(TaskStatus.NEW) is False
    
    def test_task_status_is_pending(self):
        """Test is_pending() classifier."""
        assert TaskStatus.is_pending(TaskStatus.NEW) is True
        assert TaskStatus.is_pending(TaskStatus.INBOX) is True
        assert TaskStatus.is_pending(TaskStatus.ASSIGNED) is False
        assert TaskStatus.is_pending(TaskStatus.DONE) is False
    
    def test_task_status_string_inheritance(self):
        """Test that TaskStatus inherits from str."""
        status = TaskStatus.DONE
        assert isinstance(status, str)
        assert isinstance(status.value, str)
        assert str(status.value) == "done"


class TestTaskStatusStateMachine:
    """Test TaskStatus state machine methods."""
    
    # ============================================================
    # Test valid_transitions() method
    # ============================================================
    
    def test_new_valid_transitions(self):
        """Test valid transitions from NEW state."""
        transitions = TaskStatus.NEW.valid_transitions()
        assert transitions == {TaskStatus.INBOX, TaskStatus.ASSIGNED, TaskStatus.ERROR}
    
    def test_inbox_valid_transitions(self):
        """Test valid transitions from INBOX state."""
        transitions = TaskStatus.INBOX.valid_transitions()
        assert transitions == {TaskStatus.ASSIGNED, TaskStatus.ERROR}
    
    def test_assigned_valid_transitions(self):
        """Test valid transitions from ASSIGNED state."""
        transitions = TaskStatus.ASSIGNED.valid_transitions()
        assert transitions == {TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED, TaskStatus.ERROR}
    
    def test_in_progress_valid_transitions(self):
        """Test valid transitions from IN_PROGRESS state."""
        transitions = TaskStatus.IN_PROGRESS.valid_transitions()
        assert transitions == {TaskStatus.DONE, TaskStatus.BLOCKED, TaskStatus.ERROR}
    
    def test_blocked_valid_transitions(self):
        """Test valid transitions from BLOCKED state."""
        transitions = TaskStatus.BLOCKED.valid_transitions()
        assert transitions == {TaskStatus.IN_PROGRESS, TaskStatus.ERROR}
    
    def test_done_valid_transitions(self):
        """Test DONE state has no valid transitions (terminal)."""
        transitions = TaskStatus.DONE.valid_transitions()
        assert transitions == set()
    
    def test_error_valid_transitions(self):
        """Test ERROR state has no valid transitions (terminal)."""
        transitions = TaskStatus.ERROR.valid_transitions()
        assert transitions == set()
    
    # ============================================================
    # Test can_transition_to() method - Valid transitions
    # ============================================================
    
    def test_can_transition_new_to_inbox(self):
        """Test NEW can transition to INBOX."""
        assert TaskStatus.NEW.can_transition_to(TaskStatus.INBOX) is True
    
    def test_can_transition_new_to_assigned(self):
        """Test NEW can transition to ASSIGNED."""
        assert TaskStatus.NEW.can_transition_to(TaskStatus.ASSIGNED) is True
    
    def test_can_transition_new_to_error(self):
        """Test NEW can transition to ERROR."""
        assert TaskStatus.NEW.can_transition_to(TaskStatus.ERROR) is True
    
    def test_can_transition_inbox_to_assigned(self):
        """Test INBOX can transition to ASSIGNED."""
        assert TaskStatus.INBOX.can_transition_to(TaskStatus.ASSIGNED) is True
    
    def test_can_transition_assigned_to_in_progress(self):
        """Test ASSIGNED can transition to IN_PROGRESS."""
        assert TaskStatus.ASSIGNED.can_transition_to(TaskStatus.IN_PROGRESS) is True
    
    def test_can_transition_in_progress_to_done(self):
        """Test IN_PROGRESS can transition to DONE."""
        assert TaskStatus.IN_PROGRESS.can_transition_to(TaskStatus.DONE) is True
    
    def test_can_transition_blocked_to_in_progress(self):
        """Test BLOCKED can transition back to IN_PROGRESS."""
        assert TaskStatus.BLOCKED.can_transition_to(TaskStatus.IN_PROGRESS) is True
    
    # ============================================================
    # Test can_transition_to() method - Invalid transitions
    # ============================================================
    
    def test_cannot_transition_new_to_in_progress(self):
        """Test NEW cannot transition directly to IN_PROGRESS."""
        assert TaskStatus.NEW.can_transition_to(TaskStatus.IN_PROGRESS) is False
    
    def test_cannot_transition_new_to_done(self):
        """Test NEW cannot transition directly to DONE."""
        assert TaskStatus.NEW.can_transition_to(TaskStatus.DONE) is False
    
    def test_cannot_transition_inbox_to_in_progress(self):
        """Test INBOX cannot transition directly to IN_PROGRESS."""
        assert TaskStatus.INBOX.can_transition_to(TaskStatus.IN_PROGRESS) is False
    
    def test_cannot_transition_assigned_to_done(self):
        """Test ASSIGNED cannot transition directly to DONE."""
        assert TaskStatus.ASSIGNED.can_transition_to(TaskStatus.DONE) is False
    
    def test_cannot_transition_done_to_any(self):
        """Test DONE cannot transition to any state (terminal)."""
        assert TaskStatus.DONE.can_transition_to(TaskStatus.NEW) is False
        assert TaskStatus.DONE.can_transition_to(TaskStatus.INBOX) is False
        assert TaskStatus.DONE.can_transition_to(TaskStatus.ASSIGNED) is False
        assert TaskStatus.DONE.can_transition_to(TaskStatus.IN_PROGRESS) is False
        assert TaskStatus.DONE.can_transition_to(TaskStatus.BLOCKED) is False
        assert TaskStatus.DONE.can_transition_to(TaskStatus.ERROR) is False
    
    def test_cannot_transition_error_to_any(self):
        """Test ERROR cannot transition to any state (terminal)."""
        assert TaskStatus.ERROR.can_transition_to(TaskStatus.NEW) is False
        assert TaskStatus.ERROR.can_transition_to(TaskStatus.INBOX) is False
        assert TaskStatus.ERROR.can_transition_to(TaskStatus.ASSIGNED) is False
        assert TaskStatus.ERROR.can_transition_to(TaskStatus.IN_PROGRESS) is False
        assert TaskStatus.ERROR.can_transition_to(TaskStatus.BLOCKED) is False
        assert TaskStatus.ERROR.can_transition_to(TaskStatus.DONE) is False
    
    # ============================================================
    # Test validate_transition() class method - Valid transitions
    # ============================================================
    
    def test_validate_transition_assigned_to_in_progress(self):
        """Test validate_transition allows ASSIGNED → IN_PROGRESS."""
        # Should not raise
        TaskStatus.validate_transition(TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS)
    
    def test_validate_transition_in_progress_to_done(self):
        """Test validate_transition allows IN_PROGRESS → DONE."""
        # Should not raise
        TaskStatus.validate_transition(TaskStatus.IN_PROGRESS, TaskStatus.DONE)
    
    def test_validate_transition_blocked_to_in_progress(self):
        """Test validate_transition allows BLOCKED → IN_PROGRESS."""
        # Should not raise
        TaskStatus.validate_transition(TaskStatus.BLOCKED, TaskStatus.IN_PROGRESS)
    
    # ============================================================
    # Test validate_transition() class method - Invalid transitions
    # ============================================================
    
    def test_validate_transition_done_to_assigned_raises(self):
        """Test validate_transition raises for DONE → ASSIGNED."""
        with pytest.raises(ValueError, match="Invalid transition.*DONE.*ASSIGNED"):
            TaskStatus.validate_transition(TaskStatus.DONE, TaskStatus.ASSIGNED)
    
    def test_validate_transition_new_to_done_raises(self):
        """Test validate_transition raises for NEW → DONE."""
        with pytest.raises(ValueError, match="Invalid transition.*NEW.*DONE"):
            TaskStatus.validate_transition(TaskStatus.NEW, TaskStatus.DONE)
    
    def test_validate_transition_inbox_to_in_progress_raises(self):
        """Test validate_transition raises for INBOX → IN_PROGRESS."""
        with pytest.raises(ValueError, match="Invalid transition.*INBOX.*IN_PROGRESS"):
            TaskStatus.validate_transition(TaskStatus.INBOX, TaskStatus.IN_PROGRESS)
    
    def test_validate_transition_assigned_to_done_raises(self):
        """Test validate_transition raises for ASSIGNED → DONE."""
        with pytest.raises(ValueError, match="Invalid transition.*ASSIGNED.*DONE"):
            TaskStatus.validate_transition(TaskStatus.ASSIGNED, TaskStatus.DONE)
    
    def test_validate_transition_error_to_in_progress_raises(self):
        """Test validate_transition raises for ERROR → IN_PROGRESS (terminal state)."""
        with pytest.raises(ValueError, match="Invalid transition.*ERROR.*IN_PROGRESS"):
            TaskStatus.validate_transition(TaskStatus.ERROR, TaskStatus.IN_PROGRESS)
    
    # ============================================================
    # Test edge cases
    # ============================================================
    
    def test_self_transition_not_allowed(self):
        """Test that transitioning to the same state is not allowed."""
        # Self-transitions should not be in valid_transitions
        for status in TaskStatus:
            transitions = status.valid_transitions()
            assert status not in transitions, f"{status} should not transition to itself"
    
    def test_all_non_terminal_states_have_error_transition(self):
        """Test that all non-terminal states can transition to ERROR."""
        non_terminal = [
            TaskStatus.NEW,
            TaskStatus.INBOX,
            TaskStatus.ASSIGNED,
            TaskStatus.IN_PROGRESS,
            TaskStatus.BLOCKED,
        ]
        
        for status in non_terminal:
            assert TaskStatus.ERROR in status.valid_transitions(), \
                f"{status} should be able to transition to ERROR"
    
    def test_terminal_states_have_no_transitions(self):
        """Test that terminal states have no outgoing transitions."""
        terminal = [TaskStatus.DONE, TaskStatus.ERROR]
        
        for status in terminal:
            assert len(status.valid_transitions()) == 0, \
                f"Terminal state {status} should have no valid transitions"
    
    def test_validate_transition_error_message_format(self):
        """Test that validation error messages are informative."""
        try:
            TaskStatus.validate_transition(TaskStatus.DONE, TaskStatus.ASSIGNED)
            pytest.fail("Expected ValueError to be raised")
        except ValueError as e:
            error_msg = str(e)
            # Check that error message contains both states
            assert "DONE" in error_msg or "done" in error_msg
            assert "ASSIGNED" in error_msg or "assigned" in error_msg
            # Check that it indicates it's invalid
            assert "invalid" in error_msg.lower() or "cannot" in error_msg.lower()


class TestFeatureStatus:
    """Test FeatureStatus enum."""
    
    def test_feature_status_values(self):
        """Verify all FeatureStatus values."""
        assert FeatureStatus.DRAFT.value == "draft"
        assert FeatureStatus.PLANNED.value == "planned"
        assert FeatureStatus.IN_PROGRESS.value == "in_progress"
        assert FeatureStatus.IMPLEMENTED.value == "implemented"
        assert FeatureStatus.DEPRECATED.value == "deprecated"
    
    def test_feature_status_is_active(self):
        """Test is_active() classifier."""
        assert FeatureStatus.is_active(FeatureStatus.PLANNED) is True
        assert FeatureStatus.is_active(FeatureStatus.IN_PROGRESS) is True
        assert FeatureStatus.is_active(FeatureStatus.DRAFT) is False
        assert FeatureStatus.is_active(FeatureStatus.IMPLEMENTED) is False
    
    def test_feature_status_is_complete(self):
        """Test is_complete() classifier."""
        assert FeatureStatus.is_complete(FeatureStatus.IMPLEMENTED) is True
        assert FeatureStatus.is_complete(FeatureStatus.PLANNED) is False
        assert FeatureStatus.is_complete(FeatureStatus.IN_PROGRESS) is False
    
    def test_feature_status_string_inheritance(self):
        """Test that FeatureStatus inherits from str."""
        status = FeatureStatus.IMPLEMENTED
        assert isinstance(status, str)
        assert isinstance(status.value, str)


class TestAgentIdentity:
    """Test AgentIdentity validation."""
    
    def test_validate_agent_valid(self):
        """Test validation of valid agent names."""
        # Use actual names from doctrine/agents
        assert validate_agent("python-pedro") is True
        assert validate_agent("architect-alphonso") is True
        assert validate_agent("backend-benny") is True
        assert validate_agent("devops-danny") is True
    
    def test_validate_agent_invalid(self):
        """Test validation of invalid agent names."""
        assert validate_agent("invalid-agent") is False
        assert validate_agent("pythonpedro") is False  # Wrong format
        assert validate_agent("") is False
        assert validate_agent("random-name") is False
    
    def test_get_all_agents(self):
        """Test getting list of all agents."""
        agents = get_all_agents()
        assert isinstance(agents, list)
        assert len(agents) >= 20  # At least 20 agents
        assert "python-pedro" in agents
        assert "architect-alphonso" in agents
        assert "backend-benny" in agents
    
    def test_agent_identity_completeness(self):
        """Verify all expected agents are defined."""
        expected_agents = [
            "analyst-annie",
            "architect-alphonso",
            "backend-benny",
            "bootstrap-bill",
            "code-reviewer-cindy",
            "curator-claire",
            "devops-danny",
            "diagram-daisy",
            "frontend-freddy",
            "java-jenny",
            "lexical-larry",
            "manager-mike",
            "planning-petra",
            "python-pedro",
            "researcher-ralph",
            "scribe-sally",
            "synthesizer-sam",
            "translator-tanya",
        ]
        
        agents = get_all_agents()
        for expected in expected_agents:
            assert expected in agents, f"Missing agent: {expected}"


class TestTaskMode:
    """Test TaskMode enum."""
    
    def test_task_mode_values(self):
        """Verify all TaskMode values."""
        assert TaskMode.ANALYSIS.value == "/analysis-mode"
        assert TaskMode.CREATIVE.value == "/creative-mode"
        assert TaskMode.META.value == "/meta-mode"
        assert TaskMode.PROGRAMMING.value == "/programming"
        assert TaskMode.PLANNING.value == "/planning"
    
    def test_task_mode_string_inheritance(self):
        """Test that TaskMode inherits from str for YAML compatibility."""
        mode = TaskMode.ANALYSIS
        assert isinstance(mode, str)
        assert isinstance(mode.value, str)
        assert str(mode.value) == "/analysis-mode"
    
    def test_task_mode_all_values(self):
        """Test that all modes can be enumerated."""
        modes = list(TaskMode)
        assert len(modes) == 5
        assert TaskMode.ANALYSIS in modes
        assert TaskMode.CREATIVE in modes
        assert TaskMode.META in modes
        assert TaskMode.PROGRAMMING in modes
        assert TaskMode.PLANNING in modes
    
    def test_task_mode_value_set(self):
        """Test creating a set of mode values (used by validator)."""
        mode_values = {mode.value for mode in TaskMode}
        assert mode_values == {
            "/analysis-mode",
            "/creative-mode",
            "/meta-mode",
            "/programming",
            "/planning",
        }


class TestTaskPriority:
    """Test TaskPriority enum."""
    
    def test_task_priority_values(self):
        """Verify all TaskPriority values."""
        assert TaskPriority.CRITICAL.value == "critical"
        assert TaskPriority.HIGH.value == "high"
        assert TaskPriority.MEDIUM.value == "medium"
        assert TaskPriority.NORMAL.value == "normal"
        assert TaskPriority.LOW.value == "low"
    
    def test_task_priority_string_inheritance(self):
        """Test that TaskPriority inherits from str for YAML compatibility."""
        priority = TaskPriority.HIGH
        assert isinstance(priority, str)
        assert isinstance(priority.value, str)
        assert str(priority.value) == "high"
    
    def test_task_priority_ordering(self):
        """Test priority comparison (higher priority = lower numeric value)."""
        assert TaskPriority.CRITICAL.order < TaskPriority.HIGH.order
        assert TaskPriority.HIGH.order < TaskPriority.MEDIUM.order
        assert TaskPriority.MEDIUM.order < TaskPriority.NORMAL.order
        assert TaskPriority.NORMAL.order < TaskPriority.LOW.order
    
    def test_task_priority_is_urgent(self):
        """Test is_urgent() helper method."""
        assert TaskPriority.is_urgent(TaskPriority.CRITICAL) is True
        assert TaskPriority.is_urgent(TaskPriority.HIGH) is True
        assert TaskPriority.is_urgent(TaskPriority.MEDIUM) is False
        assert TaskPriority.is_urgent(TaskPriority.NORMAL) is False
        assert TaskPriority.is_urgent(TaskPriority.LOW) is False
    
    def test_task_priority_all_values(self):
        """Test that all priorities can be enumerated."""
        priorities = list(TaskPriority)
        assert len(priorities) == 5
        assert TaskPriority.CRITICAL in priorities
        assert TaskPriority.HIGH in priorities
        assert TaskPriority.MEDIUM in priorities
        assert TaskPriority.NORMAL in priorities
        assert TaskPriority.LOW in priorities
    
    def test_task_priority_value_set(self):
        """Test creating a set of priority values (used by validator)."""
        priority_values = {priority.value for priority in TaskPriority}
        assert priority_values == {
            "critical",
            "high",
            "medium",
            "normal",
            "low",
        }
