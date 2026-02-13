"""
GenericYAMLAdapter - Generic adapter for any CLI tool configured via YAML.

This module implements a generic adapter that reads tool configuration from YAML,
eliminating the need for concrete adapter implementations per tool. New tools can
be added via YAML configuration without code changes.

Features:
- YAML-driven configuration (binary, command template, models, timeout)
- Binary path resolution (config override > PATH lookup > platform-specific paths)
- Command generation via TemplateParser
- Output normalization
- Cross-platform support

Design Rationale (ADR-029 updated 2026-02-05):
    Pivot from concrete adapters per tool to single generic adapter reading YAML.
    This approach:
    - Eliminates code changes for new tool additions
    - Centralizes adapter logic
    - Maintains infrastructure from Batch 2.1
    - Uses ClaudeCodeAdapter as reference pattern

Examples:
    >>> # Configure tool in tools.yaml
    >>> config = {
    ...     "binary": "claude-code",
    ...     "command_template": "{{binary}} --model {{model}} --prompt {{prompt}}",
    ...     "models": ["claude-3-opus", "claude-3.5-sonnet"],
    ...     "timeout": 30
    ... }
    >>>
    >>> # Create adapter
    >>> adapter = GenericYAMLAdapter("claude-code", config)
    >>> response = adapter.execute(prompt="Write code", model="claude-3-opus")
    >>> print(response.output)
"""

import os
import platform
import shutil
from typing import Any

from ..config.env_utils import (
    expand_env_vars,
    validate_required_env_vars,
)
from .base import ToolAdapter, ToolResponse
from .output_normalizer import OutputNormalizer
from .subprocess_wrapper import CommandNotFoundError, SubprocessWrapper
from .template_parser import TemplateParser


class GenericYAMLAdapterError(Exception):
    """Base exception for GenericYAMLAdapter errors."""

    pass


class BinaryNotFoundError(GenericYAMLAdapterError):
    """Raised when tool binary cannot be found."""

    pass


class InvalidModelError(GenericYAMLAdapterError):
    """Raised when an unsupported model is requested."""

    pass


class GenericYAMLAdapter(ToolAdapter):
    """
    Generic adapter for CLI tools configured via YAML.

    Implements the ToolAdapter interface for any CLI tool with configuration
    provided via YAML. This adapter:
    - Reads all behavior from YAML configuration (no tool-specific code)
    - Resolves binary paths (config > PATH > platform-specific)
    - Generates commands from templates
    - Normalizes outputs
    - Handles errors consistently

    This is the primary adapter for the LLM service - new tools are added by
    creating YAML configuration files, not by writing code.

    Configuration Fields (from tools.yaml):
        binary: Binary name for PATH lookup (required)
        command_template: Command template with {{placeholders}} (required)
        models: List of supported model names (required)
        binary_path: Optional explicit path override
        timeout: Optional command timeout in seconds (default: 30)
        platforms: Optional platform-specific binary paths
            linux: Path for Linux systems
            darwin: Path for macOS systems
            windows: Path for Windows systems

    Platform Support:
        Automatically detects platform and uses appropriate binary path.
        Falls back gracefully through resolution chain.

    Examples:
        >>> # Add tool via YAML
        >>> config = {
        ...     "binary": "my-tool",
        ...     "command_template": "{{binary}} --model {{model}} {{prompt}}",
        ...     "models": ["model-1", "model-2"]
        ... }
        >>> adapter = GenericYAMLAdapter("my-tool", config)
        >>> response = adapter.execute("prompt", "model-1")
    """

    def __init__(self, tool_name: str, tool_config: dict[str, Any]):
        """
        Initialize GenericYAMLAdapter with tool name and configuration.

        Args:
            tool_name: Name of the tool (used for logging and identification)
            tool_config: Configuration dictionary from YAML with fields:
                - binary: Binary name (required)
                - command_template: Command template (required)
                - models: Supported models list (required)
                - binary_path: Optional explicit path
                - timeout: Optional timeout in seconds
                - platforms: Optional platform-specific paths
                - env_vars: Optional environment variables (supports ${VAR} expansion)
                - env_required: Optional list of required environment variables

        Raises:
            BinaryNotFoundError: If binary cannot be found or is not executable
            EnvVarNotFoundError: If required environment variables are not set
        """
        super().__init__(tool_config)

        # Store tool name
        self._tool_name = tool_name

        # Validate and expand environment variables
        env_required = tool_config.get("env_required", [])
        env_vars = tool_config.get("env_vars", {})

        # Validate required environment variables are set
        if env_required:
            validate_required_env_vars(env_required)

        # Expand environment variables (${VAR} -> actual values)
        self.env_vars = expand_env_vars(env_vars) if env_vars else {}

        # Initialize infrastructure components
        self.template_parser = TemplateParser(
            allowed_placeholders=["binary", "model", "prompt"]
        )
        self.subprocess_wrapper = SubprocessWrapper(
            timeout=tool_config.get("timeout", 30)
        )
        self.output_normalizer = OutputNormalizer()

        # Resolve binary path using resolution chain
        self.binary_path = self._resolve_binary_path()

        # Store command template
        self.command_template = tool_config.get("command_template", "")

    def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
        """
        Execute the tool with given parameters.

        Builds command from template, executes via subprocess, normalizes output.

        Args:
            prompt: User prompt or input text for the tool
            model: Model identifier (must be in config.models list)
            **kwargs: Additional tool-specific parameters (currently unused)

        Returns:
            ToolResponse with execution results

        Raises:
            InvalidModelError: If model is not in supported models list

        Examples:
            >>> response = adapter.execute("Write code", "claude-3-opus")
            >>> assert response.status == "success"
        """
        # Validate model is supported
        supported_models = self.tool_config.get("models", [])
        if model not in supported_models:
            raise InvalidModelError(
                f"Model '{model}' not supported by tool '{self._tool_name}'. "
                f"Supported models: {', '.join(sorted(supported_models))}"
            )

        # Build command from template
        try:
            command_args = self.template_parser.parse(
                self.command_template,
                {
                    "binary": self.binary_path,
                    "model": model,
                    "prompt": prompt,
                },
            )
        except Exception as e:
            return ToolResponse(
                status="error",
                output="",
                tool_name=self.get_tool_name(),
                stderr=f"Failed to build command: {str(e)}",
            )

        # Execute command with environment variables
        try:
            # Pass expanded env vars to subprocess if configured
            env = self.env_vars if self.env_vars else None
            result = self.subprocess_wrapper.execute(command_args, env=env)
        except CommandNotFoundError:
            return ToolResponse(
                status="error",
                output="",
                tool_name=self.get_tool_name(),
                stderr=self._format_binary_not_found_error(),
            )
        except Exception as e:
            return ToolResponse(
                status="error",
                output="",
                tool_name=self.get_tool_name(),
                stderr=f"Execution failed: {str(e)}",
            )

        # Handle timeout
        if result.timed_out:
            return ToolResponse(
                status="error",
                output="",
                tool_name=self.get_tool_name(),
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr,
                duration_seconds=result.duration_seconds,
            )

        # Handle non-zero exit code
        if result.exit_code != 0:
            return ToolResponse(
                status="error",
                output="",
                tool_name=self.get_tool_name(),
                exit_code=result.exit_code,
                stdout=result.stdout,
                stderr=result.stderr
                or f"Command failed with exit code {result.exit_code}",
                duration_seconds=result.duration_seconds,
            )

        # Normalize output
        normalized = self.output_normalizer.normalize(result.stdout)

        # Build successful response
        return ToolResponse(
            status="success",
            output=normalized.response_text,
            tool_name=self.get_tool_name(),
            exit_code=result.exit_code,
            stdout=result.stdout,
            stderr=result.stderr,
            duration_seconds=result.duration_seconds,
            metadata=normalized.metadata,
        )

    def validate_config(self, config: dict[str, Any]) -> bool:
        """
        Validate tool configuration.

        Checks that configuration contains all required fields and validates types.
        Required fields: binary, command_template, models

        Args:
            config: Configuration dictionary to validate

        Returns:
            True if configuration is valid, False otherwise

        Examples:
            >>> config = {
            ...     "binary": "tool",
            ...     "command_template": "{{binary}} {{prompt}}",
            ...     "models": ["model-1"]
            ... }
            >>> assert adapter.validate_config(config) is True
        """
        # Check required fields
        if not self._validate_required_fields(config):
            return False

        # Validate field types
        if not self._validate_field_types(config):
            return False

        # Validate optional fields if present
        if not self._validate_optional_fields(config):
            return False

        return True

    def _validate_required_fields(self, config: dict[str, Any]) -> bool:
        """Validate that all required fields are present."""
        required_fields = ["binary", "command_template", "models"]
        return all(field in config for field in required_fields)

    def _validate_field_types(self, config: dict[str, Any]) -> bool:
        """Validate types of required fields."""
        if not isinstance(config["binary"], str):
            return False

        if not isinstance(config["command_template"], str):
            return False

        if not isinstance(config["models"], list):
            return False

        if not all(isinstance(m, str) for m in config["models"]):
            return False

        return True

    def _validate_optional_fields(self, config: dict[str, Any]) -> bool:
        """Validate optional fields if present."""
        if "binary_path" in config and not isinstance(config["binary_path"], str):
            return False

        if "timeout" in config:
            if not isinstance(config["timeout"], (int, float)):
                return False
            if config["timeout"] <= 0:
                return False

        if "platforms" in config:
            if not isinstance(config["platforms"], dict):
                return False

        return True

    def get_tool_name(self) -> str:
        """
        Return the name of this tool adapter.

        Returns:
            Tool name as provided in constructor

        Examples:
            >>> adapter = GenericYAMLAdapter("my-tool", config)
            >>> assert adapter.get_tool_name() == "my-tool"
        """
        return self._tool_name

    def _resolve_binary_path(self) -> str:
        """
        Resolve tool binary path using resolution chain.

        Resolution order:
        1. Explicit tool_config["binary_path"] (if provided)
        2. shutil.which(binary) - system PATH lookup
        3. Platform-specific paths from tool_config["platforms"]

        Returns:
            Resolved binary path

        Raises:
            BinaryNotFoundError: If binary cannot be found or is not executable

        Examples:
            >>> # With explicit config
            >>> config = {"binary_path": "/usr/bin/tool", ...}
            >>> path = adapter._resolve_binary_path()
            >>> assert path == "/usr/bin/tool"
        """
        # 1. Check explicit config override (binary_path)
        if "binary_path" in self.tool_config:
            binary_path = self.tool_config["binary_path"]
            # Expand user home directory (~)
            binary_path = os.path.expanduser(binary_path)

            # Verify it exists and is executable
            if os.path.exists(binary_path) and os.access(binary_path, os.X_OK):
                return binary_path
            elif os.path.exists(binary_path):
                raise BinaryNotFoundError(
                    f"Binary exists but is not executable: {binary_path}\n"
                    f"Run: chmod +x {binary_path}"
                )
            else:
                raise BinaryNotFoundError(
                    f"Configured binary_path not found: {binary_path}"
                )

        # Get binary name for PATH lookup
        binary_name = self.tool_config.get("binary", "")

        # 2. Try shutil.which() - checks system PATH
        which_result = shutil.which(binary_name)
        if which_result:
            return which_result

        # 3. Try platform-specific paths from config
        if "platforms" in self.tool_config and self.tool_config["platforms"]:
            system = platform.system()

            # Map platform.system() to config keys (case-insensitive)
            platform_map = {
                "Linux": "linux",
                "Darwin": "macos",  # macOS
                "Windows": "windows",
            }

            config_key = platform_map.get(system)
            if config_key:
                platforms = self.tool_config["platforms"]

                # Convert Pydantic model to dict if needed
                if hasattr(platforms, "model_dump"):
                    platforms = platforms.model_dump()
                elif hasattr(platforms, "__dict__"):
                    platforms = dict(platforms)

                # Try both the mapped key and "darwin" for macOS
                paths_to_try = []
                if (
                    isinstance(platforms, dict)
                    and config_key in platforms
                    and platforms[config_key]
                ):
                    paths_to_try.append(platforms[config_key])
                if (
                    system == "Darwin"
                    and isinstance(platforms, dict)
                    and "darwin" in platforms
                    and platforms["darwin"]
                ):
                    paths_to_try.append(platforms["darwin"])

                for path_str in paths_to_try:
                    # Expand user home directory
                    expanded_path = os.path.expanduser(path_str)

                    if os.path.exists(expanded_path) and os.access(
                        expanded_path, os.X_OK
                    ):
                        return expanded_path

        # Binary not found - raise error with helpful message
        raise BinaryNotFoundError(self._format_binary_not_found_error())

    def _format_binary_not_found_error(self) -> str:
        """
        Format helpful error message when binary is not found.

        Returns:
            Formatted error message with resolution suggestions
        """
        binary_name = self.tool_config.get("binary", "unknown")

        message = [
            f"Binary '{binary_name}' not found for tool '{self._tool_name}'.",
            "",
            "Resolution suggestions:",
            f"1. Install the tool and ensure '{binary_name}' is in your PATH",
            "2. Specify explicit path in configuration:",
            "   tools:",
            f"     {self._tool_name}:",
            f'       binary_path: "/path/to/{binary_name}"',
        ]

        # Add platform-specific paths if configured
        if "platforms" in self.tool_config and self.tool_config["platforms"]:
            message.append("")
            message.append("3. Or use platform-specific paths:")
            platforms = self.tool_config["platforms"]

            # Convert Pydantic model to dict if needed
            if hasattr(platforms, "model_dump"):
                platforms = platforms.model_dump()
            elif hasattr(platforms, "__dict__"):
                platforms = dict(platforms)

            if isinstance(platforms, dict):
                for platform_name, path in platforms.items():
                    if path:  # Skip None values
                        message.append(f"   {platform_name}: {path}")

        return "\n".join(message)
