"""Execution module: Model routing and execution interfaces.

This module implements Layer 2 (Model Routing) and Layer 3 (Model Execution):
- Router configuration and selection (OpenRouter, OpenCode.ai)
- Direct API clients (OpenAI, Anthropic)
- Local model interfaces (Ollama)
- Fallback and retry logic

References:
    - docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md
    - docs/architecture/adrs/ADR-021-model-routing-strategy.md
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ModelProvider(Enum):
    """Supported model providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"
    OPENCODE = "opencode"
    OLLAMA = "ollama"


@dataclass
class ModelCapabilities:
    """Model capability metadata.

    Attributes:
        context_window: Maximum context tokens.
        supports_tools: Whether model supports function/tool calling.
        supports_structured_output: Whether model supports structured JSON.
        supports_streaming: Whether model supports streaming responses.
    """

    context_window: int
    supports_tools: bool = False
    supports_structured_output: bool = False
    supports_streaming: bool = False


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


class ModelRouter:
    """Model routing and selection engine.

    Implements router-first strategy per ADR-021 with fallback chains
    and cost-aware selection.
    """

    def __init__(self, config_path: str | None = None) -> None:
        """Initialize model router.

        Args:
            config_path: Path to model router configuration YAML.
                Defaults to .doctrine-config/model_router.yaml.
        """
        self.config_path = config_path or ".doctrine-config/model_router.yaml"
        self._models: dict[str, ModelConfig] = {}
        self._fallback_chains: dict[str, list[str]] = {}

    def load_config(self) -> None:
        """Load router configuration from YAML.

        Raises:
            FileNotFoundError: If configuration file not found.
            ValueError: If configuration is invalid.
        """
        # TODO: Load and parse .doctrine-config/model_router.yaml
        # TODO: Validate model IDs and capabilities
        # TODO: Build fallback chains
        pass

    def select_model(
        self,
        task_type: str,
        constraints: dict[str, Any] | None = None,
    ) -> ModelConfig:
        """Select optimal model for task based on requirements.

        Args:
            task_type: Type of task (e.g., 'analysis-long-context',
                'repo-refactor-safe', 'batch-offline').
            constraints: Optional constraints dict with keys:
                - context_window (int): Minimum required context window
                - requires_tools (bool): Whether tool calling is required
                - cost_ceiling (float): Maximum cost per 1k tokens
                - privacy (bool): Whether local model is required

        Returns:
            Selected model configuration.

        Raises:
            ValueError: If no suitable model found.
        """
        if not self._models:
            raise RuntimeError("Router not initialized. Call load_config() first.")

        constraints = constraints or {}

        # TODO: Implement model selection logic
        # TODO: Filter by constraints
        # TODO: Prioritize by task type and cost
        # TODO: Return best match

        raise NotImplementedError("Model selection not yet implemented")

    def get_fallback_chain(self, model_id: str) -> list[str]:
        """Get fallback model chain for given model.

        Args:
            model_id: Primary model identifier.

        Returns:
            Ordered list of fallback model IDs.

        Raises:
            ValueError: If model_id not found.
        """
        if model_id not in self._models:
            raise ValueError(f"Unknown model ID: {model_id}")

        return self._fallback_chains.get(model_id, [])


class ExecutionClient:
    """Base execution client interface.

    Provides common interface for direct API and router-based execution.
    Subclasses implement provider-specific logic.
    """

    def __init__(self, provider: ModelProvider, api_key: str | None = None) -> None:
        """Initialize execution client.

        Args:
            provider: Model provider.
            api_key: Optional API key. If None, reads from environment.
        """
        self.provider = provider
        self.api_key = api_key

    def invoke(
        self,
        model_id: str,
        prompt: str,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Invoke model with prompt and optional tools.

        Args:
            model_id: Model identifier.
            prompt: Input prompt or message.
            tools: Optional list of tool/function definitions.
            **kwargs: Additional provider-specific parameters.

        Returns:
            Response dictionary with 'content', 'tool_calls', 'usage', etc.

        Raises:
            RuntimeError: If invocation fails.
        """
        raise NotImplementedError("Subclass must implement invoke()")


class OllamaClient(ExecutionClient):
    """Local model execution via Ollama.

    Implements Layer 3 local model interface for privacy-sensitive
    and offline tasks.
    """

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        """Initialize Ollama client.

        Args:
            base_url: Ollama API base URL.
        """
        super().__init__(provider=ModelProvider.OLLAMA)
        self.base_url = base_url

    def invoke(
        self,
        model_id: str,
        prompt: str,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Invoke local Ollama model.

        Args:
            model_id: Ollama model name (e.g., 'llama3:70b', 'deepseek-coder').
            prompt: Input prompt.
            tools: Optional tool definitions (limited support).
            **kwargs: Additional parameters (temperature, top_p, etc.).

        Returns:
            Response dictionary.

        Raises:
            RuntimeError: If Ollama service unavailable or model not found.
        """
        # TODO: Implement Ollama HTTP API call
        # TODO: Handle streaming if requested
        # TODO: Parse and structure response
        return {
            "content": "",
            "model": model_id,
            "provider": "ollama",
        }
