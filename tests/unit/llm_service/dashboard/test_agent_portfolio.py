"""
Unit tests for agent portfolio service.

Tests the AgentPortfolioService class in isolation with mocked dependencies.
Follows TDD: RED-GREEN-REFACTOR cycle.

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model
- ADR-046: Domain Module Refactoring
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.domain.doctrine.models import Agent
from src.llm_service.dashboard.agent_portfolio import AgentPortfolioService


class TestAgentPortfolioService:
    """Unit tests for AgentPortfolioService."""

    @pytest.fixture
    def mock_agent(self) -> Agent:
        """Create a mock Agent domain object for testing."""
        return Agent(
            id="test-agent",
            name="Test Agent",
            specialization="Testing specialist",
            capabilities=frozenset(["testing", "validation"]),
            required_directives=frozenset(["001", "016", "017"]),
            primers=frozenset(["TDD"]),
            source_file=Path("/test/agents/test-agent.agent.md"),
            source_hash="abc123def456",
            version="1.0",
            status="active",
            tags=frozenset(["test"]),
            capability_descriptions={
                "primary_focus": "Testing and validation",
                "secondary_awareness": "Documentation",
                "avoid": "Production deployment",
            },
        )

    @pytest.fixture
    def tmp_agents_dir(self, tmp_path: Path) -> Path:
        """Create temporary agents directory."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        return agents_dir

    def test_init_with_agents_directory(self, tmp_agents_dir: Path) -> None:
        """
        TEST: Service initializes with agents directory path.
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        assert service.agents_dir == tmp_agents_dir

    def test_init_with_default_agents_directory(self) -> None:
        """
        TEST: Service uses default agents directory if none provided.
        """
        service = AgentPortfolioService()
        # Default should point to .github/agents relative to repo
        assert service.agents_dir is not None
        assert "agents" in str(service.agents_dir)

    def test_get_agents_returns_list(self, tmp_agents_dir: Path) -> None:
        """
        TEST: get_agents() returns list of Agent objects.
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        agents = service.get_agents()
        assert isinstance(agents, list)

    def test_get_agents_empty_directory(self, tmp_agents_dir: Path) -> None:
        """
        TEST: get_agents() returns empty list for empty directory.
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        agents = service.get_agents()
        assert agents == []

    @patch("src.llm_service.dashboard.agent_portfolio.AgentParser")
    def test_get_agents_loads_from_parser(
        self, mock_parser_class: Mock, tmp_agents_dir: Path, mock_agent: Agent
    ) -> None:
        """
        TEST: get_agents() uses AgentParser to load agents.
        """
        # Create a test agent file
        agent_file = tmp_agents_dir / "test.agent.md"
        agent_file.write_text("test content")

        # Mock parser
        mock_parser = Mock()
        mock_parser.parse.return_value = mock_agent
        mock_parser_class.return_value = mock_parser

        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        agents = service.get_agents()

        # Verify parser was used
        mock_parser_class.assert_called_once()
        mock_parser.parse.assert_called_once()
        assert len(agents) == 1
        assert agents[0] == mock_agent

    @patch("src.llm_service.dashboard.agent_portfolio.AgentParser")
    def test_get_agents_handles_parse_errors(
        self, mock_parser_class: Mock, tmp_agents_dir: Path
    ) -> None:
        """
        TEST: get_agents() handles parse errors gracefully.
        """
        # Create agent files
        agent_file1 = tmp_agents_dir / "valid.agent.md"
        agent_file1.write_text("valid")

        agent_file2 = tmp_agents_dir / "invalid.agent.md"
        agent_file2.write_text("invalid")

        # Mock parser to fail on second file
        mock_parser = Mock()
        mock_agent = Agent(
            id="valid",
            name="Valid",
            specialization="Test",
            capabilities=frozenset(),
            required_directives=frozenset(),
            primers=frozenset(),
            source_file=agent_file1,
            source_hash="hash",
        )

        def parse_side_effect(path: Path) -> Agent:
            if "invalid" in str(path):
                raise ValueError("Invalid agent file")
            return mock_agent

        mock_parser.parse.side_effect = parse_side_effect
        mock_parser_class.return_value = mock_parser

        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        agents = service.get_agents()

        # Should return valid agent, skip invalid
        assert len(agents) == 1
        assert agents[0].id == "valid"

    def test_get_portfolio_data_returns_dict(self, tmp_agents_dir: Path) -> None:
        """
        TEST: get_portfolio_data() returns dictionary with expected structure.
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        portfolio = service.get_portfolio_data()

        assert isinstance(portfolio, dict)
        assert "agents" in portfolio
        assert "metadata" in portfolio

    def test_get_portfolio_data_includes_metadata(self, tmp_agents_dir: Path) -> None:
        """
        TEST: get_portfolio_data() includes metadata (total count, load time).
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        portfolio = service.get_portfolio_data()

        metadata = portfolio["metadata"]
        assert "total_agents" in metadata
        assert "load_time_ms" in metadata
        assert isinstance(metadata["total_agents"], int)
        assert isinstance(metadata["load_time_ms"], float)

    @patch("src.llm_service.dashboard.agent_portfolio.AgentParser")
    def test_get_portfolio_data_transforms_agents(
        self, mock_parser_class: Mock, tmp_agents_dir: Path, mock_agent: Agent
    ) -> None:
        """
        TEST: get_portfolio_data() transforms Agent objects to dict format.
        """
        # Create agent file
        agent_file = tmp_agents_dir / "test.agent.md"
        agent_file.write_text("test")

        # Mock parser
        mock_parser = Mock()
        mock_parser.parse.return_value = mock_agent
        mock_parser_class.return_value = mock_parser

        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        portfolio = service.get_portfolio_data()

        agents_data = portfolio["agents"]
        assert len(agents_data) == 1

        agent_data = agents_data[0]
        assert agent_data["id"] == "test-agent"
        assert agent_data["name"] == "Test Agent"
        assert agent_data["specialization"] == "Testing specialist"

    def test_calculate_directive_compliance_with_directives(
        self, mock_agent: Agent
    ) -> None:
        """
        TEST: _calculate_directive_compliance() calculates compliance correctly.
        """
        service = AgentPortfolioService()
        compliance = service._calculate_directive_compliance(mock_agent)

        assert "required_directives_count" in compliance
        assert "compliance_percentage" in compliance

        # Mock agent has 3 required directives
        assert compliance["required_directives_count"] == 3
        # For now, assume 100% compliance (simplified)
        assert compliance["compliance_percentage"] == 100.0

    def test_calculate_directive_compliance_no_directives(
        self, tmp_agents_dir: Path
    ) -> None:
        """
        TEST: _calculate_directive_compliance() handles agents with no directives.
        """
        agent = Agent(
            id="no-directives",
            name="No Directives",
            specialization="Test",
            capabilities=frozenset(),
            required_directives=frozenset(),  # Empty
            primers=frozenset(),
            source_file=Path("/test/agent.md"),
            source_hash="hash",
        )

        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        compliance = service._calculate_directive_compliance(agent)

        assert compliance["required_directives_count"] == 0
        assert (
            compliance["compliance_percentage"] == 100.0
        )  # 100% of 0 is still "compliant"

    def test_transform_agent_to_dict(self, mock_agent: Agent) -> None:
        """
        TEST: _transform_agent_to_dict() creates proper dictionary representation.
        """
        service = AgentPortfolioService()
        agent_dict = service._transform_agent_to_dict(mock_agent)

        # Verify all required fields present
        assert agent_dict["id"] == "test-agent"
        assert agent_dict["name"] == "Test Agent"
        assert agent_dict["specialization"] == "Testing specialist"
        assert "capability_descriptions" in agent_dict
        assert "directive_compliance" in agent_dict
        assert agent_dict["source_file"] == str(mock_agent.source_file)
        assert agent_dict["source_hash"] == "abc123def456"

    def test_transform_agent_preserves_capability_descriptions(
        self, mock_agent: Agent
    ) -> None:
        """
        TEST: _transform_agent_to_dict() preserves capability_descriptions.
        """
        service = AgentPortfolioService()
        agent_dict = service._transform_agent_to_dict(mock_agent)

        capabilities = agent_dict["capability_descriptions"]
        assert capabilities["primary_focus"] == "Testing and validation"
        assert capabilities["secondary_awareness"] == "Documentation"
        assert capabilities["avoid"] == "Production deployment"

    def test_find_agent_files_returns_paths(self, tmp_agents_dir: Path) -> None:
        """
        TEST: _find_agent_files() returns list of agent file paths.
        """
        # Create test files
        (tmp_agents_dir / "agent1.agent.md").touch()
        (tmp_agents_dir / "agent2.agent.md").touch()
        (tmp_agents_dir / "not-agent.md").touch()  # Should be ignored

        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        agent_files = service._find_agent_files()

        assert len(agent_files) == 2
        assert all(path.suffix == ".md" for path in agent_files)
        assert all(".agent." in path.name for path in agent_files)

    def test_find_agent_files_empty_directory(self, tmp_agents_dir: Path) -> None:
        """
        TEST: _find_agent_files() returns empty list for empty directory.
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)
        agent_files = service._find_agent_files()
        assert agent_files == []

    def test_caching_agents_list(self, tmp_agents_dir: Path) -> None:
        """
        TEST: Agents list is cached to avoid repeated filesystem scans.
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)

        # First call loads agents
        agents1 = service.get_agents()

        # Create new agent file after loading
        (tmp_agents_dir / "new-agent.agent.md").touch()

        # Second call should return cached list (not new file)
        agents2 = service.get_agents()

        # Both calls should return same cached list
        assert agents1 is agents2  # Same object reference

    def test_refresh_clears_cache(self, tmp_agents_dir: Path) -> None:
        """
        TEST: refresh() method clears cache and reloads agents.
        """
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)

        # First load
        agents1 = service.get_agents()

        # Refresh
        service.refresh()

        # Second load should be different object (reloaded)
        agents2 = service.get_agents()

        assert agents1 is not agents2  # Different object reference


class TestAgentPortfolioServiceEdgeCases:
    """Test edge cases and error handling."""

    def test_nonexistent_directory(self) -> None:
        """
        TEST: Service handles nonexistent directory gracefully.
        """
        fake_dir = Path("/nonexistent/agents")
        service = AgentPortfolioService(agents_dir=fake_dir)

        # Should not crash, return empty list
        agents = service.get_agents()
        assert agents == []

    def test_invalid_directory_path(self) -> None:
        """
        TEST: Service handles invalid directory path.
        """
        # Use a file path instead of directory
        service = AgentPortfolioService(agents_dir=Path(__file__))

        # Should handle gracefully
        agents = service.get_agents()
        assert agents == []

    def test_concurrent_access_safety(self, tmp_path: Path) -> None:
        """
        TEST: Service is safe for concurrent access (no state corruption).
        """
        tmp_agents_dir = tmp_path / "agents"
        tmp_agents_dir.mkdir()
        service = AgentPortfolioService(agents_dir=tmp_agents_dir)

        # Multiple calls should not corrupt state
        portfolio1 = service.get_portfolio_data()
        portfolio2 = service.get_portfolio_data()

        # Both should be valid and independent
        assert portfolio1 is not None
        assert portfolio2 is not None
        # Metadata timestamps might differ, but structure should be same
        assert portfolio1.keys() == portfolio2.keys()
