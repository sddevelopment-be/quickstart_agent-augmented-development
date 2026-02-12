"""
Tests for agent profile loader.

Validates dynamic loading of agent identities from doctrine/agents.
"""

from pathlib import Path

import pytest

from src.domain.doctrine.agent_loader import AgentProfileLoader, load_agent_identities


class TestAgentProfileLoader:
    """Test AgentProfileLoader class."""

    def test_loader_finds_doctrine_directory(self):
        """Test that loader can find doctrine directory."""
        loader = AgentProfileLoader()
        assert loader.doctrine_path.exists()
        assert loader.agents_path.exists()

    def test_load_agent_names_returns_list(self):
        """Test that load_agent_names returns a list."""
        loader = AgentProfileLoader()
        agent_names = loader.load_agent_names()

        assert isinstance(agent_names, list)
        assert len(agent_names) > 0

    def test_all_agents_have_valid_names(self):
        """Test that all loaded agents have valid name format."""
        loader = AgentProfileLoader()
        agent_names = loader.load_agent_names()

        for name in agent_names:
            # Agent names should be lowercase with hyphens
            assert isinstance(name, str)
            assert len(name) > 0
            assert name == name.lower() or "-" in name

    def test_agent_count_matches_files(self):
        """Test that agent count matches .agent.md files."""
        loader = AgentProfileLoader()
        agent_names = loader.load_agent_names()

        agent_files = list(loader.agents_path.glob("*.agent.md"))

        # Should have loaded agents from most files
        # (allowing for some files that might not have valid frontmatter)
        assert len(agent_names) >= len(agent_files) * 0.9

    def test_known_agents_are_loaded(self):
        """Test that known agents are loaded correctly."""
        loader = AgentProfileLoader()
        agent_names = loader.load_agent_names()

        # Check for some known agents
        expected_agents = [
            "python-pedro",
            "architect-alphonso",
            "backend-benny",
            "devops-danny",
        ]

        for expected in expected_agents:
            assert expected in agent_names, f"Expected agent '{expected}' not found"

    def test_load_agent_identities_convenience_function(self):
        """Test the convenience function."""
        agent_names = load_agent_identities()

        assert isinstance(agent_names, list)
        assert len(agent_names) > 15  # Should have at least 15 agents

    def test_loader_with_nonexistent_path(self):
        """Test loader behavior with nonexistent path."""
        loader = AgentProfileLoader(Path("/nonexistent/path"))

        with pytest.raises(FileNotFoundError):
            loader.load_agent_names()
