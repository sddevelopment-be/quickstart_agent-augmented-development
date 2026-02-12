"""
LLM Tool Adapters Package.

This package provides abstract base classes and concrete implementations
for adapting external LLM tools (claude-code, codex, etc.) to the
routing engine's standard interface.

Public API:
    - ToolAdapter: Abstract base class for all tool adapters
    - ToolResponse: Standardized response dataclass
    - TemplateParser: Command template parser with security
    - SubprocessWrapper: Safe subprocess execution wrapper
    - OutputNormalizer: Output normalization framework
    - NormalizedResponse: Normalized output dataclass
    - ExecutionResult: Subprocess execution result dataclass

Examples:
    >>> from src.llm_service.adapters import (
    ...     ToolAdapter, ToolResponse, TemplateParser,
    ...     SubprocessWrapper, OutputNormalizer
    ... )
    >>>
    >>> # Create custom adapter
    >>> class MyAdapter(ToolAdapter):
    ...     def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
    ...         # Build command from template
    ...         parser = TemplateParser()
    ...         command = parser.parse(self.tool_config["command_template"], {...})
    ...
    ...         # Execute via subprocess
    ...         wrapper = SubprocessWrapper(timeout=30)
    ...         result = wrapper.execute(command)
    ...
    ...         # Normalize output
    ...         normalizer = OutputNormalizer()
    ...         normalized = normalizer.normalize(result.stdout)
    ...
    ...         # Return standardized response
    ...         return ToolResponse(
    ...             status="success" if result.exit_code == 0 else "error",
    ...             output=normalized.response_text,
    ...             tool_name=self.get_tool_name(),
    ...             exit_code=result.exit_code,
    ...             stdout=result.stdout,
    ...             stderr=result.stderr,
    ...             duration_seconds=result.duration_seconds,
    ...             metadata=normalized.metadata
    ...         )
"""

from .base import ToolAdapter, ToolResponse
from .generic_adapter import (
    BinaryNotFoundError,
    GenericYAMLAdapter,
    GenericYAMLAdapterError,
    InvalidModelError,
)
from .output_normalizer import NormalizedResponse, OutputNormalizer
from .subprocess_wrapper import (
    CommandNotFoundError,
    ExecutionResult,
    InvalidCommandError,
    SubprocessExecutionError,
    SubprocessWrapper,
)
from .template_parser import (
    TemplateParser,
    TemplatePlaceholderError,
    TemplateSyntaxError,
)

__all__ = [
    # Base adapter
    "ToolAdapter",
    "ToolResponse",
    # Template parser
    "TemplateParser",
    "TemplateSyntaxError",
    "TemplatePlaceholderError",
    # Subprocess wrapper
    "SubprocessWrapper",
    "ExecutionResult",
    "CommandNotFoundError",
    "InvalidCommandError",
    "SubprocessExecutionError",
    # Output normalizer
    "OutputNormalizer",
    "NormalizedResponse",
    # Generic YAML adapter
    "GenericYAMLAdapter",
    "BinaryNotFoundError",
    "InvalidModelError",
    "GenericYAMLAdapterError",
]
