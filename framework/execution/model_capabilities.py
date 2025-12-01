"""Model capabilities dataclass."""

from dataclasses import dataclass


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
