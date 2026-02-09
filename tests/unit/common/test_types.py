"""
Tests for shared type definitions.

Tests TaskStatus, FeatureStatus enums and AgentIdentity validation.
"""

import pytest
from src.common.types import (
    TaskStatus,
    FeatureStatus,
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
        assert validate_agent("python-pedro") is True
        assert validate_agent("architect") is True
        assert validate_agent("backend-dev") is True
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
        assert len(agents) == 20  # Current count
        assert "python-pedro" in agents
        assert "architect" in agents
        assert "backend-dev" in agents
    
    def test_agent_identity_completeness(self):
        """Verify all expected agents are defined."""
        expected_agents = [
            "architect",
            "backend-dev",
            "python-pedro",
            "frontend",
            "devops-danny",
            "planning-petra",
            "manager-mike",
            "curator",
            "writer-editor",
            "scribe",
            "researcher",
            "diagrammer",
            "lexical",
            "synthesizer",
            "translator",
            "bootstrap-bill",
            "framework-guardian",
            "java-jenny",
            "analyst-annie",
            "code-reviewer",
        ]
        
        agents = get_all_agents()
        for expected in expected_agents:
            assert expected in agents, f"Missing agent: {expected}"
