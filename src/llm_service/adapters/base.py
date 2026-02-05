"""
Base adapter abstract class for LLM tools.

This module defines the ToolAdapter ABC which all concrete tool adapters
must inherit from. It enforces a consistent interface contract for:
- Executing tools with standardized parameters
- Validating tool configurations
- Returning standardized responses

Design Decision: ADR-029 chose Abstract Base Class (ABC) over Protocol
for explicit contract enforcement with runtime validation.

Examples:
    >>> from src.llm_service.adapters.base import ToolAdapter, ToolResponse
    >>> 
    >>> class MyAdapter(ToolAdapter):
    ...     def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
    ...         # Implementation
    ...         return ToolResponse(status="success", output="result", tool_name="my-tool")
    ...     
    ...     def validate_config(self, config: Dict[str, Any]) -> bool:
    ...         return "binary" in config
    ...     
    ...     def get_tool_name(self) -> str:
    ...         return "my-tool"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ToolResponse:
    """
    Standardized response from tool execution.
    
    This dataclass provides a consistent return type for all tool adapters,
    enabling uniform error handling, logging, and telemetry collection.
    
    Attributes:
        status: Execution status - "success" or "error"
        output: Primary output text from the tool (LLM response)
        tool_name: Name of the tool that generated this response
        exit_code: Process exit code (0 for success, non-zero for error)
        stdout: Raw stdout from tool execution (if available)
        stderr: Raw stderr from tool execution (if available)
        duration_seconds: Execution duration in seconds
        metadata: Additional tool-specific metadata (tokens, cost, model, etc.)
    
    Examples:
        >>> response = ToolResponse(
        ...     status="success",
        ...     output="Generated text",
        ...     tool_name="claude-code",
        ...     metadata={"tokens": 150}
        ... )
    """

    status: str
    output: str
    tool_name: str
    exit_code: Optional[int] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    duration_seconds: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class ToolAdapter(ABC):
    """
    Abstract base class for LLM tool adapters.
    
    All concrete tool adapters (claude-code, codex, etc.) must inherit from
    this class and implement the required abstract methods. This design:
    
    1. Enforces explicit contract (fail-fast for incomplete implementations)
    2. Provides runtime validation via ABC mechanism
    3. Enables type checking and IDE support
    4. Documents the required interface clearly
    
    Design Rationale (ADR-029):
        We chose Abstract Base Class over Protocol for:
        - Runtime validation (incomplete adapters fail at instantiation)
        - Explicit interface contract for contributors
        - Better IDE autocomplete and type checker support
        - Familiar Python pattern for extension
    
    Required Methods:
        - execute(): Execute the tool with given parameters
        - validate_config(): Validate tool configuration
        - get_tool_name(): Return the tool's name
    
    Attributes:
        tool_config: Configuration dictionary for this tool adapter
    
    Examples:
        >>> class ClaudeCodeAdapter(ToolAdapter):
        ...     def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
        ...         # Execute claude-code CLI
        ...         return ToolResponse(status="success", output="...", tool_name="claude-code")
        ...     
        ...     def validate_config(self, config: Dict[str, Any]) -> bool:
        ...         return "binary" in config and "models" in config
        ...     
        ...     def get_tool_name(self) -> str:
        ...         return "claude-code"
    """

    def __init__(self, tool_config: Dict[str, Any]):
        """
        Initialize adapter with tool configuration.
        
        Args:
            tool_config: Dictionary containing tool-specific configuration
                        (binary path, models, timeout, etc.)
        """
        self.tool_config = tool_config

    @abstractmethod
    def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
        """
        Execute the tool with given parameters.
        
        This is the primary method that routing engine calls to invoke the
        tool. Concrete implementations should:
        1. Build command from configuration and parameters
        2. Execute the tool via subprocess
        3. Parse and normalize the output
        4. Return standardized ToolResponse
        
        Args:
            prompt: User prompt or input text for the LLM
            model: Model identifier (e.g., "claude-3-opus", "gpt-4")
            **kwargs: Additional tool-specific parameters
        
        Returns:
            ToolResponse with execution results
        
        Raises:
            Exception: Tool execution failures (should be caught and returned
                      as error ToolResponse where possible)
        
        Examples:
            >>> response = adapter.execute(
            ...     prompt="Write a function",
            ...     model="claude-3-opus",
            ...     temperature=0.7
            ... )
            >>> assert response.status == "success"
        """
        pass

    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate tool configuration before execution.
        
        Checks that the configuration contains all required fields for this
        adapter. Called by routing engine before adapter instantiation to
        ensure configuration is valid.
        
        Args:
            config: Tool configuration dictionary to validate
        
        Returns:
            True if configuration is valid, False otherwise
        
        Examples:
            >>> is_valid = adapter.validate_config({
            ...     "binary": "/usr/bin/claude-code",
            ...     "models": ["claude-3-opus"],
            ...     "timeout": 30
            ... })
            >>> assert is_valid is True
        """
        pass

    @abstractmethod
    def get_tool_name(self) -> str:
        """
        Return the name of this tool adapter.
        
        Used for logging, telemetry, and routing decisions. Should return
        a unique identifier for this tool (e.g., "claude-code", "codex").
        
        Returns:
            Tool name as string
        
        Examples:
            >>> name = adapter.get_tool_name()
            >>> assert name == "claude-code"
        """
        pass
