"""
Agent profile loader - dynamically loads agent identities from doctrine/agents.

This module provides functionality to load agent profiles from the doctrine
directory, ensuring single source of truth and avoiding hardcoded drift.
"""

from pathlib import Path
from typing import List, Optional
import re
import logging

logger = logging.getLogger(__name__)


class AgentProfileLoader:
    """Loads agent profiles from doctrine/agents directory."""
    
    def __init__(self, doctrine_path: Optional[Path] = None):
        """
        Initialize agent profile loader.
        
        Args:
            doctrine_path: Path to doctrine directory. If None, auto-detects.
        """
        if doctrine_path is None:
            # Auto-detect doctrine path relative to this file
            # From src/domain/doctrine/agent_loader.py -> root/doctrine
            doctrine_path = Path(__file__).parent.parent.parent.parent / "doctrine"
        
        self.doctrine_path = Path(doctrine_path)
        self.agents_path = self.doctrine_path / "agents"
        
        if not self.agents_path.exists():
            logger.warning(f"Agents directory not found: {self.agents_path}")
    
    def load_agent_names(self) -> List[str]:
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
                    logger.warning(f"Could not extract agent name from {agent_file.name}")
            except Exception as e:
                logger.error(f"Error reading {agent_file.name}: {e}")
        
        return sorted(agent_names)
    
    def _extract_agent_name(self, agent_file: Path) -> Optional[str]:
        """
        Extract agent name from frontmatter in agent file.
        
        Args:
            agent_file: Path to agent markdown file
            
        Returns:
            Agent name or None if not found
        """
        try:
            content = agent_file.read_text(encoding='utf-8')
            
            # Match YAML frontmatter between --- markers
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if not frontmatter_match:
                return None
            
            frontmatter = frontmatter_match.group(1)
            
            # Extract name field
            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if name_match:
                return name_match.group(1).strip()
            
            return None
        except Exception as e:
            logger.error(f"Error extracting name from {agent_file}: {e}")
            return None


# Global instance for convenience
_default_loader: Optional[AgentProfileLoader] = None


def get_agent_loader() -> AgentProfileLoader:
    """Get or create the default agent profile loader."""
    global _default_loader
    if _default_loader is None:
        _default_loader = AgentProfileLoader()
    return _default_loader


def load_agent_identities() -> List[str]:
    """
    Load agent identities from doctrine/agents.
    
    This is the primary function to use for getting valid agent names.
    It caches the loader instance for performance.
    
    Returns:
        List of valid agent name identifiers
    """
    loader = get_agent_loader()
    return loader.load_agent_names()
