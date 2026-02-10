"""
Tests for shared type definitions.

Tests TaskStatus, FeatureStatus, TaskMode, TaskPriority enums and AgentIdentity validation.
"""

import pytest
from src.common.types import (
    TaskStatus,
    FeatureStatus,
    TaskMode,
    TaskPriority,
    AgentIdentity,
    validate_agent,
    get_all_agents,
)


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
