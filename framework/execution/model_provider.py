"""Model provider enumeration."""

from enum import Enum


class ModelProvider(Enum):
    """Supported model providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"
    OPENCODE = "opencode"
    OLLAMA = "ollama"
