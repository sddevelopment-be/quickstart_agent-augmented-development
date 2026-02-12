"""Agent profile dataclass.

Represents agent metadata, specialization, and capabilities.
"""

from dataclasses import dataclass


@dataclass
class AgentProfile:
    """Agent profile metadata.

    Attributes:
        name: Agent identifier (e.g., 'devops-danny', 'curator-clara').
        specialization: Primary focus area.
        directives: List of required directive codes.
        mode_default: Default reasoning mode.
        capabilities: List of operational verbs.
    """

    name: str
    specialization: str
    directives: list[str]
    mode_default: str = "analysis"
    capabilities: list[str] | None = None

    def __post_init__(self) -> None:
        """Validate profile after initialization."""
        if not self.name:
            raise ValueError("Agent name cannot be empty")
        if not self.specialization:
            raise ValueError("Agent specialization cannot be empty")
        if self.capabilities is None:
            self.capabilities = []
