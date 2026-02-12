"""
ClaudeCodeAdapter - Concrete adapter for claude-code CLI.

This module implements the first concrete ToolAdapter for the claude-code CLI tool.
It validates the Batch 2.1 adapter infrastructure with real tool integration.

Features:
- Model mapping (claude-3.5-sonnet, claude-3-opus, claude-3-haiku)
- Binary path resolution (cross-platform, config override)
- Command generation via template parser
- Error handling (binary not found, invalid model, CLI failures)

Examples:
    >>> from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
    >>>
    >>> config = {
    ...     "binary_path": "/usr/local/bin/claude-code",
    ...     "models": ["claude-3-opus", "claude-3.5-sonnet"],
    ...     "timeout": 30
    ... }
    >>> adapter = ClaudeCodeAdapter(config)
    >>> response = adapter.execute(prompt="Write a function", model="claude-3-opus")
    >>> print(response.output)
"""

import os
import platform
import shutil
from typing import Any

from .base import ToolAdapter, ToolResponse
from .output_normalizer import OutputNormalizer
from .subprocess_wrapper import CommandNotFoundError, SubprocessWrapper
from .template_parser import TemplateParser


class ClaudeCodeAdapterError(Exception):
    """Base exception for ClaudeCodeAdapter errors."""

    pass


class BinaryNotFoundError(ClaudeCodeAdapterError):
    """Raised when claude-code binary cannot be found."""

    pass


class InvalidModelError(ClaudeCodeAdapterError):
    """Raised when an unsupported model is requested."""

    pass


class ClaudeCodeAdapter(ToolAdapter):
    """
    Concrete adapter for claude-code CLI tool.

    Implements the ToolAdapter interface for the claude-code CLI, providing:
    - Cross-platform binary resolution
    - Model name mapping
    - Command template generation
    - Output normalization
    - Comprehensive error handling

    Supported Models:
        - claude-3.5-sonnet (default)
        - claude-3-opus
        - claude-3-haiku

    Configuration:
        binary_path: Optional explicit path to claude-code binary
        models: List of supported model names
        timeout: Optional command timeout in seconds (default: 30)
        template: Optional command template override

    Platform Support:
        - Linux: /usr/local/bin/claude-code, ~/.local/bin/claude-code
        - macOS: /usr/local/bin/claude-code, ~/bin/claude-code
        - Windows: C:\\Program Files\\claude-code\\claude.exe, AppData paths

    Examples:
        >>> config = {
        ...     "models": ["claude-3-opus"],
        ...     "timeout": 30
        ... }
        >>> adapter = ClaudeCodeAdapter(config)
        >>> response = adapter.execute("Write code", "claude-3-opus")
    """

    # Supported model names and their CLI parameter mappings
    MODEL_MAPPING = {
        "claude-3.5-sonnet": "claude-3-5-sonnet-20240620",
        "claude-3-opus": "claude-3-opus-20240229",
        "claude-3-haiku": "claude-3-haiku-20240307",
        # Aliases for convenience
        "claude-3.5": "claude-3-5-sonnet-20240620",
        "claude-opus": "claude-3-opus-20240229",
        "claude-haiku": "claude-3-haiku-20240307",
    }

    # Default command template
    # Note: {{prompt}} is quoted to handle multi-word prompts correctly
    DEFAULT_TEMPLATE = '{{binary}} --model {{model}} --prompt "{{prompt}}"'

    # Platform-specific default binary paths
    PLATFORM_BINARY_PATHS = {
        "Linux": [
            "/usr/local/bin/claude-code",
            "~/.local/bin/claude-code",
            "/usr/bin/claude-code",
        ],
        "Darwin": [  # macOS
            "/usr/local/bin/claude-code",
            "~/bin/claude-code",
            "/opt/homebrew/bin/claude-code",
        ],
        "Windows": [
            r"C:\Program Files\claude-code\claude.exe",
            r"C:\Program Files (x86)\claude-code\claude.exe",
            "~/AppData/Local/Programs/claude-code/claude.exe",
        ],
    }

    def __init__(self, tool_config: dict[str, Any]):
        """
        Initialize ClaudeCodeAdapter with configuration.

        Args:
            tool_config: Configuration dictionary with optional fields:
                - binary_path: Explicit binary path (overrides auto-detection)
                - models: List of allowed models
                - timeout: Command timeout in seconds (default: 30)
                - template: Command template override
        """
        super().__init__(tool_config)

        # Initialize components
        self.template_parser = TemplateParser(
            allowed_placeholders=["binary", "model", "prompt"]
        )
        self.subprocess_wrapper = SubprocessWrapper(
            timeout=tool_config.get("timeout", 30)
        )
        self.output_normalizer = OutputNormalizer()

        # Resolve binary path
        self.binary_path = self._resolve_binary_path()

        # Store command template
        self.command_template = tool_config.get("template", self.DEFAULT_TEMPLATE)

    def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
        """
        Execute claude-code CLI with given parameters.

        Args:
            prompt: User prompt for the LLM
            model: Model identifier (will be mapped to CLI parameter)
            **kwargs: Additional parameters (currently unused)

        Returns:
            ToolResponse with execution results

        Raises:
            InvalidModelError: If model is not supported
            BinaryNotFoundError: If claude-code binary not found

        Examples:
            >>> response = adapter.execute("Write code", "claude-3-opus")
            >>> assert response.status == "success"
        """
        # Validate model
        if model not in self.MODEL_MAPPING:
            raise InvalidModelError(
                f"Model '{model}' not supported. Supported models: "
                f"{', '.join(sorted(self.MODEL_MAPPING.keys()))}"
            )

        # Map model to CLI parameter
        cli_model = self.MODEL_MAPPING[model]

        # Build command from template
        try:
            command_args = self.template_parser.parse(
                self.command_template,
                {
                    "binary": self.binary_path,
                    "model": cli_model,
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

        # Execute command
        try:
            result = self.subprocess_wrapper.execute(command_args)
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

        Checks for optional fields and validates types.

        Args:
            config: Configuration dictionary to validate

        Returns:
            True if configuration is valid (ClaudeCodeAdapter has no required fields)

        Examples:
            >>> is_valid = adapter.validate_config({"timeout": 30})
            >>> assert is_valid is True
        """
        # ClaudeCodeAdapter has all optional fields
        # Validate types if fields are present

        if "binary_path" in config and not isinstance(config["binary_path"], str):
            return False

        if "models" in config:
            if not isinstance(config["models"], list):
                return False
            if not all(isinstance(m, str) for m in config["models"]):
                return False

        if "timeout" in config:
            if not isinstance(config["timeout"], (int, float)):
                return False
            if config["timeout"] <= 0:
                return False

        if "template" in config and not isinstance(config["template"], str):
            return False

        return True

    def get_tool_name(self) -> str:
        """
        Return the tool name for this adapter.

        Returns:
            "claude-code"

        Examples:
            >>> assert adapter.get_tool_name() == "claude-code"
        """
        return "claude-code"

    def _resolve_binary_path(self) -> str:
        """
        Resolve claude-code binary path.

        Resolution order:
        1. Explicit tool_config["binary_path"] (if provided)
        2. shutil.which("claude-code") - system PATH lookup
        3. Platform-specific default paths

        Returns:
            Resolved binary path

        Raises:
            BinaryNotFoundError: If binary cannot be found

        Examples:
            >>> # With explicit config
            >>> adapter.tool_config["binary_path"] = "/usr/bin/claude-code"
            >>> path = adapter._resolve_binary_path()
        """
        # 1. Check explicit config override
        if "binary_path" in self.tool_config:
            binary_path = self.tool_config["binary_path"]
            # Expand user home directory
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

        # 2. Try shutil.which() - checks system PATH
        which_result = shutil.which("claude-code")
        if which_result:
            return which_result

        # 3. Try platform-specific default paths
        system = platform.system()
        default_paths = self.PLATFORM_BINARY_PATHS.get(system, [])

        for path_str in default_paths:
            # Expand user home directory
            expanded_path = os.path.expanduser(path_str)

            if os.path.exists(expanded_path) and os.access(expanded_path, os.X_OK):
                return expanded_path

        # Binary not found - raise error with helpful message
        raise BinaryNotFoundError(self._format_binary_not_found_error())

    def _format_binary_not_found_error(self) -> str:
        """
        Format helpful error message when binary is not found.

        Returns:
            Formatted error message with installation instructions
        """
        system = platform.system()
        default_paths = self.PLATFORM_BINARY_PATHS.get(system, [])

        message = [
            "claude-code binary not found.",
            "",
            "Installation instructions:",
            "  npm install -g @anthropic-ai/claude-code",
            "",
            "Or install manually and ensure it's in your PATH:",
        ]

        for path in default_paths:
            message.append(f"  - {path}")

        message.extend(
            [
                "",
                "Or specify explicit path in configuration:",
                "  tool:",
                "    claude-code:",
                '      binary_path: "/path/to/claude-code"',
            ]
        )

        return "\n".join(message)
