"""
Agent profile loader - dynamically loads agent identities from doctrine/agents.

This module provides functionality to load agent profiles from the doctrine
directory, ensuring single source of truth and avoiding hardcoded drift.

Supports both framework agents (doctrine/agents/) and local custom agents
(.doctrine-config/custom-agents/) per DDR-011 (Agent Specialization Hierarchy).
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


def _repo_root_from_module() -> Path:
    """Auto-detect repository root from this module's location."""
    # From src/domain/doctrine/agent_loader.py -> root/
    return Path(__file__).resolve().parent.parent.parent.parent


class AgentProfileLoader:
    """Loads agent profiles from doctrine/agents and local custom-agents directories."""

    def __init__(
        self,
        doctrine_path: Path | None = None,
        repo_root: Path | None = None,
    ):
        """
        Initialize agent profile loader.

        Args:
            doctrine_path: Path to doctrine directory. If None, auto-detects.
            repo_root: Repository root for local agent discovery. If None, auto-detects.
        """
        if repo_root is None:
            repo_root = _repo_root_from_module()

        if doctrine_path is None:
            doctrine_path = repo_root / "doctrine"

        self.repo_root = Path(repo_root)
        self.doctrine_path = Path(doctrine_path)
        self.agents_path = self.doctrine_path / "agents"
        self.local_agents_path = self.repo_root / ".doctrine-config" / "custom-agents"

        if not self.agents_path.exists():
            logger.warning(f"Agents directory not found: {self.agents_path}")

    def load_agent_names(self) -> list[str]:
        """
        Load all agent names from doctrine/agents/*.agent.md files.

        Returns:
            List of agent name identifiers

        Raises:
            FileNotFoundError: If doctrine/agents directory doesn't exist
        """
        if not self.agents_path.exists():
            raise FileNotFoundError(f"Agents directory not found: {self.agents_path}")

        agent_files = list(self.agents_path.glob("*.agent.md"))
        if not agent_files:
            logger.warning(f"No agent files found in {self.agents_path}")
            return []

        agent_names = []
        for agent_file in agent_files:
            try:
                name = self._extract_agent_name(agent_file)
                if name:
                    agent_names.append(name)
                else:
                    logger.warning(
                        f"Could not extract agent name from {agent_file.name}"
                    )
            except Exception as e:
                logger.error(f"Error reading {agent_file.name}: {e}")

        return sorted(agent_names)

    def load_all_profiles(self, include_local: bool = True) -> dict[str, object]:
        """
        Load full Agent domain objects from framework and local directories.

        Uses AgentParser from the domain layer. Local agents override framework
        agents with the same name (per DDR-011).

        Args:
            include_local: Whether to include .doctrine-config/custom-agents/

        Returns:
            Dict mapping agent id to Agent domain object.
        """
        from .parsers import AgentParser

        parser = AgentParser()
        agents: dict[str, object] = {}

        # Framework agents
        if self.agents_path.exists():
            for agent_file in self.agents_path.glob("*.agent.md"):
                try:
                    agent = parser.parse(agent_file)
                    agents[agent.id] = agent
                except Exception as e:
                    logger.warning(f"Skipping {agent_file.name}: {e}")

        # Local custom agents (override framework agents)
        if include_local and self.local_agents_path.exists():
            for agent_file in self.local_agents_path.glob("*.agent.md"):
                try:
                    agent = parser.parse(agent_file)
                    agents[agent.id] = agent
                except Exception as e:
                    logger.warning(f"Skipping local {agent_file.name}: {e}")

        return agents

    def _extract_agent_name(self, agent_file: Path) -> str | None:
        """
        Extract agent name from frontmatter in agent file.

        Args:
            agent_file: Path to agent markdown file

        Returns:
            Agent name or None if not found
        """
        try:
            content = agent_file.read_text(encoding="utf-8")

            # Match YAML frontmatter between --- markers
            frontmatter_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if not frontmatter_match:
                return None

            frontmatter = frontmatter_match.group(1)

            # Extract name field
            name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
            if name_match:
                return name_match.group(1).strip()

            return None
        except Exception as e:
            logger.error(f"Error extracting name from {agent_file}: {e}")
            return None


# Global instance for convenience
_default_loader: AgentProfileLoader | None = None


def get_agent_loader() -> AgentProfileLoader:
    """Get or create the default agent profile loader."""
    global _default_loader
    if _default_loader is None:
        _default_loader = AgentProfileLoader()
    return _default_loader


def load_agent_identities() -> list[str]:
    """
    Load agent identities from doctrine/agents.

    This is the primary function to use for getting valid agent names.
    It caches the loader instance for performance.

    Returns:
        List of valid agent name identifiers
    """
    loader = get_agent_loader()
    return loader.load_agent_names()
