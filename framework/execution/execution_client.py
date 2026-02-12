"""Base execution client interface."""

from typing import Any

from framework.execution.model_provider import ModelProvider


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
