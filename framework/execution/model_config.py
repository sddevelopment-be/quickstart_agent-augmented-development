"""Model configuration dataclass."""

from dataclasses import dataclass

from framework.execution.model_capabilities import ModelCapabilities
from framework.execution.model_provider import ModelProvider


@dataclass
class ModelConfig:
    """Model configuration and metadata.

    Attributes:
        id: Model identifier (vendor-specific).
        provider: Model provider.
        name: Human-readable model name.
        capabilities: Model capabilities.
        cost_per_1k_tokens: Approximate cost per 1000 tokens (input + output).
        is_local: Whether model runs locally.
    """

    id: str
    provider: ModelProvider
    name: str
    capabilities: ModelCapabilities
    cost_per_1k_tokens: float = 0.0
    is_local: bool = False
