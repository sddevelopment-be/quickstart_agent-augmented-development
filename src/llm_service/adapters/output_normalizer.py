"""
Output normalization framework for tool responses.

This module standardizes outputs from different tools (claude-code, codex, etc.)
into a consistent format for telemetry and error handling.

Supports:
- JSON structured output
- Plain text output
- Mixed format (text + metadata)
- Tool-specific format handlers (extensible)

Examples:
    >>> from src.llm_service.adapters.output_normalizer import OutputNormalizer
    >>> 
    >>> normalizer = OutputNormalizer()
    >>> result = normalizer.normalize('{"response": "text", "tokens": 100}', format="json")
    >>> print(result.response_text)
    'text'
    >>> print(result.metadata)
    {'tokens': 100}
"""

import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable


@dataclass
class NormalizedResponse:
    """
    Standardized response from output normalization.
    
    This dataclass provides consistent structure for tool outputs regardless
    of the original format (JSON, text, mixed).
    
    Attributes:
        response_text: Extracted LLM response text (primary output)
        metadata: Extracted metadata (tokens, cost, model, etc.)
        errors: List of error messages found in output
        warnings: List of warning messages found in output
        raw_output: Original unprocessed output
    
    Examples:
        >>> response = NormalizedResponse(
        ...     response_text="Generated text",
        ...     metadata={"tokens": 150},
        ...     errors=[],
        ...     warnings=[],
        ...     raw_output='{"response": "Generated text"}'
        ... )
    """

    response_text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    raw_output: str = ""


class OutputNormalizer:
    """
    Normalize tool outputs to consistent format.
    
    Handles different output formats from various tools:
    - JSON structured (claude-code, openai, etc.)
    - Plain text (simple CLI tools)
    - Mixed format (text with metadata trailer)
    
    Extensible via custom format handlers for tool-specific formats.
    
    Features:
        - Auto-detect format (JSON vs text)
        - Extract response text from various JSON structures
        - Parse metadata (tokens, cost, model)
        - Identify errors and warnings
        - Plugin architecture for custom handlers
    
    Examples:
        >>> normalizer = OutputNormalizer()
        >>> result = normalizer.normalize(tool_output)
        >>> print(result.response_text)
    """

    # Common JSON keys for response text (priority order)
    RESPONSE_KEYS = [
        "response",
        "text",
        "content",
        "output",
        "message",
        "completion",
    ]

    # Common JSON keys for metadata
    TOKEN_KEYS = ["tokens", "total_tokens", "usage.total_tokens"]
    COST_KEYS = ["cost_usd", "cost", "total_cost", "cost.total_usd"]
    MODEL_KEYS = ["model", "model_name", "engine"]

    def __init__(self):
        """Initialize output normalizer with custom format handlers."""
        self._format_handlers: Dict[str, Callable[[str], NormalizedResponse]] = {}

    def register_format_handler(
        self, format_name: str, handler: Callable[[str], NormalizedResponse]
    ):
        """
        Register custom format handler for tool-specific formats.
        
        Args:
            format_name: Name of the format (e.g., "claude-code")
            handler: Function that takes output string and returns NormalizedResponse
        
        Examples:
            >>> def my_handler(output: str) -> NormalizedResponse:
            ...     # Custom parsing logic
            ...     return NormalizedResponse(response_text=output, metadata={})
            >>> 
            >>> normalizer.register_format_handler("custom", my_handler)
        """
        self._format_handlers[format_name] = handler

    def normalize(
        self, output: str, format: Optional[str] = None
    ) -> NormalizedResponse:
        """
        Normalize tool output to standard format.
        
        Auto-detects format if not specified. Extracts response text,
        metadata, errors, and warnings.
        
        Args:
            output: Raw output string from tool
            format: Optional format hint ("json", "text", or custom format)
        
        Returns:
            NormalizedResponse with standardized fields
        
        Examples:
            >>> result = normalizer.normalize('{"response": "text"}')
            >>> print(result.response_text)
            'text'
        """
        # Use custom handler if format is registered
        if format and format in self._format_handlers:
            return self._format_handlers[format](output)

        # Auto-detect format if not specified
        if format is None:
            format = self._detect_format(output)

        # Normalize based on format
        if format == "json":
            return self._normalize_json(output)
        else:
            return self._normalize_text(output)

    def _detect_format(self, output: str) -> str:
        """
        Auto-detect output format.
        
        Args:
            output: Raw output string
        
        Returns:
            Detected format ("json" or "text")
        """
        if not output.strip():
            return "text"

        # Try to parse as JSON
        try:
            json.loads(output)
            return "json"
        except (json.JSONDecodeError, ValueError):
            return "text"

    def _normalize_json(self, output: str) -> NormalizedResponse:
        """
        Normalize JSON formatted output.
        
        Args:
            output: JSON string
        
        Returns:
            NormalizedResponse with extracted fields
        """
        errors = []
        warnings = []
        metadata = {}
        response_text = ""

        try:
            data = json.loads(output)

            # Extract response text (try multiple common keys)
            response_text = self._extract_response_text(data)

            # Extract metadata
            metadata = self._extract_metadata(data)

            # Extract errors
            if "error" in data:
                errors.append(str(data["error"]))
            if "errors" in data and isinstance(data["errors"], list):
                errors.extend(str(e) for e in data["errors"])

            # Extract warnings
            if "warning" in data:
                warnings.append(str(data["warning"]))
            if "warnings" in data and isinstance(data["warnings"], list):
                warnings.extend(str(w) for w in data["warnings"])

        except (json.JSONDecodeError, ValueError) as e:
            # JSON parsing failed - fall back to treating as text
            errors.append(f"JSON parsing failed: {str(e)}")
            response_text = output

        return NormalizedResponse(
            response_text=response_text,
            metadata=metadata,
            errors=errors,
            warnings=warnings,
            raw_output=output,
        )

    def _normalize_text(self, output: str) -> NormalizedResponse:
        """
        Normalize plain text output.
        
        Args:
            output: Plain text string
        
        Returns:
            NormalizedResponse with text as response_text
        """
        return NormalizedResponse(
            response_text=output,
            metadata={},
            errors=[],
            warnings=[],
            raw_output=output,
        )

    def _extract_response_text(self, data: Dict[str, Any]) -> str:
        """
        Extract response text from JSON data structure.
        
        Tries multiple common keys in priority order.
        
        Args:
            data: Parsed JSON dictionary
        
        Returns:
            Extracted response text or empty string
        """
        # Try top-level response keys
        for key in self.RESPONSE_KEYS:
            if key in data:
                value = data[key]
                # Handle nested objects
                if isinstance(value, dict) and "text" in value:
                    return str(value["text"])
                return str(value)

        # Try nested structures
        if "data" in data and isinstance(data["data"], dict):
            nested_response = self._extract_response_text(data["data"])
            if nested_response:
                return nested_response

        # If no recognized key, return empty
        return ""

    def _extract_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract metadata from JSON data structure.
        
        Looks for common metadata fields (tokens, cost, model, etc.).
        
        Args:
            data: Parsed JSON dictionary
        
        Returns:
            Dictionary of extracted metadata
        """
        metadata = {}

        # Check for explicit metadata field
        if "metadata" in data and isinstance(data["metadata"], dict):
            # Merge nested metadata
            metadata.update(data["metadata"])

        # Extract token count
        if "usage" in data and isinstance(data["usage"], dict):
            usage = data["usage"]
            for key in self.TOKEN_KEYS:
                if key.split(".")[-1] in usage:
                    metadata["tokens"] = usage[key.split(".")[-1]]
                    break
        else:
            for key in self.TOKEN_KEYS:
                if key in data:
                    metadata["tokens"] = data[key]
                    break

        # Extract cost
        if "cost" in data and isinstance(data["cost"], dict):
            cost = data["cost"]
            for key in self.COST_KEYS:
                simple_key = key.split(".")[-1]
                if simple_key in cost:
                    metadata["cost_usd"] = cost[simple_key]
                    break
        else:
            for key in self.COST_KEYS:
                if key in data:
                    metadata["cost_usd"] = data[key]
                    break

        # Extract model
        for key in self.MODEL_KEYS:
            if key in data:
                metadata["model"] = data[key]
                break

        # Copy other top-level metadata fields (excluding known response keys)
        for key, value in data.items():
            if (
                key not in self.RESPONSE_KEYS
                and key not in ["usage", "cost", "error", "errors", "warning", "warnings"]
                and not key.startswith("_")
                and isinstance(value, (str, int, float, bool))
            ):
                metadata[key] = value

        return metadata
