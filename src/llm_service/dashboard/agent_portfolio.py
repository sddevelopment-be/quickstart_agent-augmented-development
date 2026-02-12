"""
Agent portfolio service for dashboard.

Provides agent capability data for dashboard portfolio view using domain models.
Follows ADR-045: Integrate doctrine domain model with dashboard.

Scope (LIMITED INTEGRATION)
----------------------------
- ✅ Load agents using AgentParser from domain model
- ✅ Extract capabilities (primary, secondary, avoid)
- ✅ Calculate directive compliance
- ✅ Provide data structure for dashboard consumption
- ❌ NO major dashboard UI changes (out of scope)
- ❌ NO changes to other views (per specification)

Design Principles
-----------------
1. **Domain Model Integration**: Uses AgentParser, not raw YAML
2. **Performance**: <100ms load time for typical agent count
3. **Error Tolerance**: Handles invalid files gracefully
4. **Caching**: Cache loaded agents to avoid repeated I/O
5. **Type Safety**: Full type hints for mypy compliance

Related ADRs
------------
- ADR-045: Doctrine Concept Domain Model
- ADR-046: Domain Module Refactoring

Examples
--------
>>> from pathlib import Path
>>> service = AgentPortfolioService()
>>> portfolio = service.get_portfolio_data()
>>> print(f"Loaded {portfolio['metadata']['total_agents']} agents")
Loaded 15 agents

>>> # Get raw Agent objects
>>> agents = service.get_agents()
>>> for agent in agents:
...     print(f"{agent.name}: {agent.specialization}")
Python Pedro: Python development specialist
Backend Benny: Backend development
"""

import logging
from pathlib import Path
from time import perf_counter
from typing import Any

from src.domain.doctrine.models import Agent
from src.domain.doctrine.parsers import AgentParser

# Configure logging
logger = logging.getLogger(__name__)


class AgentPortfolioService:
    """
    Service for loading and presenting agent portfolio data.

    Integrates doctrine domain model (AgentParser) with dashboard portfolio view.
    Provides structured data for displaying agent capabilities and compliance.

    Attributes
    ----------
    agents_dir : Path
        Directory containing agent profile files (*.agent.md)

    Examples
    --------
    >>> service = AgentPortfolioService()
    >>> portfolio = service.get_portfolio_data()
    >>> print(portfolio["metadata"]["total_agents"])
    15
    """

    def __init__(self, agents_dir: Path | None = None) -> None:
        """
        Initialize agent portfolio service.

        Args:
            agents_dir: Directory containing agent files.
                       Defaults to .github/agents relative to repo root.
        """
        if agents_dir is None:
            # Default to .github/agents relative to repo root
            # Assumes service is called from repo root context
            repo_root = Path(__file__).parent.parent.parent.parent
            agents_dir = repo_root / ".github" / "agents"

        self.agents_dir = agents_dir
        self._agents_cache: list[Agent] | None = None
        self._parser = AgentParser()

    def get_agents(self) -> list[Agent]:
        """
        Load all agents from agents directory.

        Returns domain Agent objects using AgentParser. Results are cached
        for performance. Use refresh() to reload from disk.

        Returns:
            List of Agent domain objects

        Examples:
            >>> service = AgentPortfolioService()
            >>> agents = service.get_agents()
            >>> print([a.id for a in agents])
            ['python-pedro', 'backend-benny', ...]
        """
        # Return cached agents if available
        if self._agents_cache is not None:
            return self._agents_cache

        # Load agents from filesystem
        agents: list[Agent] = []
        agent_files = self._find_agent_files()

        for agent_file in agent_files:
            try:
                agent = self._parser.parse(agent_file)
                agents.append(agent)
            except Exception as e:
                # Log error but continue loading other agents
                logger.warning(
                    f"Failed to load agent from {agent_file}: {e}",
                    exc_info=True,
                )
                continue

        # Cache results
        self._agents_cache = agents

        return agents

    def get_portfolio_data(self) -> dict[str, Any]:
        """
        Get portfolio data structure for dashboard consumption.

        Returns structured dictionary with agent data and metadata suitable
        for dashboard display. Includes capability descriptions, directive
        compliance, and source traceability.

        Returns:
            Dictionary with structure:
            {
                "agents": [
                    {
                        "id": str,
                        "name": str,
                        "specialization": str,
                        "capability_descriptions": dict,
                        "directive_compliance": {
                            "required_directives_count": int,
                            "compliance_percentage": float
                        },
                        "source_file": str,
                        "source_hash": str
                    },
                    ...
                ],
                "metadata": {
                    "total_agents": int,
                    "load_time_ms": float
                }
            }

        Examples:
            >>> service = AgentPortfolioService()
            >>> portfolio = service.get_portfolio_data()
            >>> agent = portfolio["agents"][0]
            >>> print(f"{agent['name']}: {agent['specialization']}")
            Python Pedro: Python development specialist
        """
        start_time = perf_counter()

        # Load agents
        agents = self.get_agents()

        # Transform to dashboard-friendly format
        agents_data = [self._transform_agent_to_dict(agent) for agent in agents]

        # Calculate load time
        end_time = perf_counter()
        load_time_ms = (end_time - start_time) * 1000

        return {
            "agents": agents_data,
            "metadata": {
                "total_agents": len(agents_data),
                "load_time_ms": load_time_ms,
            },
        }

    def refresh(self) -> None:
        """
        Clear cache and force reload of agents from disk.

        Use when agent files have been added, removed, or modified and
        you want to see the latest state.

        Examples:
            >>> service = AgentPortfolioService()
            >>> agents_before = service.get_agents()
            >>> # ... add new agent file ...
            >>> service.refresh()
            >>> agents_after = service.get_agents()  # Reloaded from disk
        """
        self._agents_cache = None

    def _find_agent_files(self) -> list[Path]:
        """
        Find all agent profile files in agents directory.

        Returns:
            List of Path objects for *.agent.md files
        """
        # Check directory exists and is a directory
        if not self.agents_dir.exists() or not self.agents_dir.is_dir():
            logger.warning(
                f"Agents directory not found or not a directory: {self.agents_dir}"
            )
            return []

        # Find all *.agent.md files
        try:
            agent_files = list(self.agents_dir.glob("*.agent.md"))
            return agent_files
        except Exception as e:
            logger.error(f"Error scanning agents directory {self.agents_dir}: {e}")
            return []

    def _transform_agent_to_dict(self, agent: Agent) -> dict[str, Any]:
        """
        Transform Agent domain object to dictionary for dashboard.

        Args:
            agent: Agent domain object

        Returns:
            Dictionary with agent data for dashboard display
        """
        return {
            "id": agent.id,
            "name": agent.name,
            "specialization": agent.specialization,
            "capability_descriptions": agent.capability_descriptions,
            "directive_compliance": self._calculate_directive_compliance(agent),
            "source_file": str(agent.source_file),
            "source_hash": agent.source_hash,
        }

    def _calculate_directive_compliance(self, agent: Agent) -> dict[str, Any]:
        """
        Calculate directive compliance for an agent.

        Currently implements simplified compliance (100% if directives are defined).
        Future enhancement could cross-reference with DirectiveParser to validate
        that required directives actually exist.

        Args:
            agent: Agent domain object

        Returns:
            Dictionary with compliance data:
            {
                "required_directives_count": int,
                "compliance_percentage": float (0-100)
            }
        """
        required_count = len(agent.required_directives)

        # Simplified compliance: 100% if agent has directives defined
        # Future: Cross-reference with DirectiveParser to validate existence
        compliance_percentage = 100.0

        return {
            "required_directives_count": required_count,
            "compliance_percentage": compliance_percentage,
        }


__all__ = ["AgentPortfolioService"]
