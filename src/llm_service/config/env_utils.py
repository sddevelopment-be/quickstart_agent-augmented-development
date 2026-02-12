"""
Environment variable utilities for LLM service configuration.

This module provides utilities for handling environment variables in tool configuration:
- Variable expansion: ${VAR} and ${VAR:default} syntax
- Validation: Required environment variables checking
- Error handling: Clear error messages for missing vars

Design Rationale:
    Tools need API keys and other sensitive configuration passed via environment.
    Support ${VAR} expansion to reference system environment with optional defaults.
    Validate required vars early (at adapter initialization) for fail-fast behavior.

Examples:
    >>> # Expand environment variables
    >>> env_vars = {"API_KEY": "${ANTHROPIC_API_KEY}", "DEFAULT": "${MISSING:fallback}"}
    >>> expanded = expand_env_vars(env_vars)
    >>> print(expanded)
    {'API_KEY': 'actual-key-value', 'DEFAULT': 'fallback'}

    >>> # Validate required variables
    >>> validate_required_env_vars(["ANTHROPIC_API_KEY", "SECRET_TOKEN"])
"""

import os
import re


class EnvVarNotFoundError(Exception):
    """Raised when required environment variable is not found."""

    pass


# Regex to match ${VAR} or ${VAR:default}
ENV_VAR_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]*))?\}")


def expand_env_vars(env_vars: dict[str, str] | None) -> dict[str, str]:
    """
    Expand environment variables in configuration.

    Supports two formats:
    - ${VAR}: Expand from system environment (raises error if not found)
    - ${VAR:default}: Expand from system environment, use default if not found
    - Literal values: Passed through unchanged

    Args:
        env_vars: Dictionary of environment variable definitions

    Returns:
        Dictionary with expanded values

    Raises:
        EnvVarNotFoundError: If ${VAR} references missing environment variable

    Examples:
        >>> os.environ["API_KEY"] = "secret"
        >>> expand_env_vars({"KEY": "${API_KEY}"})
        {'KEY': 'secret'}

        >>> expand_env_vars({"KEY": "${MISSING:default}"})
        {'KEY': 'default'}

        >>> expand_env_vars({"KEY": "literal"})
        {'KEY': 'literal'}
    """
    if not env_vars:
        return {}

    expanded = {}

    for key, value in env_vars.items():
        # Check if value contains ${VAR} pattern
        match = ENV_VAR_PATTERN.search(value)

        if match:
            var_name = match.group(1)
            default_value = match.group(2)  # None if no default specified

            # Get value from system environment
            env_value = os.environ.get(var_name)

            if env_value is not None:
                # Replace ${VAR} or ${VAR:default} with actual value
                expanded[key] = ENV_VAR_PATTERN.sub(env_value, value)
            elif default_value is not None:
                # Use default value
                expanded[key] = ENV_VAR_PATTERN.sub(default_value, value)
            else:
                # No value and no default - raise error
                raise EnvVarNotFoundError(
                    f"Environment variable '{var_name}' not found and no default provided. "
                    f"Referenced in env_vars['{key}'] = '{value}'\n"
                    f"Set the environment variable with: export {var_name}=<value>"
                )
        else:
            # Literal value - pass through unchanged
            expanded[key] = value

    return expanded


def validate_required_env_vars(env_required: list[str] | None) -> None:
    """
    Validate that required environment variables are set.

    Checks system environment for presence of required variables.
    Raises error with clear message if any are missing.

    Args:
        env_required: List of required environment variable names

    Raises:
        EnvVarNotFoundError: If any required variable is not set

    Examples:
        >>> os.environ["API_KEY"] = "value"
        >>> validate_required_env_vars(["API_KEY"])  # Passes

        >>> validate_required_env_vars(["MISSING"])  # Raises EnvVarNotFoundError
    """
    if not env_required:
        return

    missing = []

    for var_name in env_required:
        if var_name not in os.environ:
            missing.append(var_name)

    if missing:
        raise EnvVarNotFoundError(
            f"Required environment variables not set: {', '.join(missing)}. "
            "Please set these variables in your environment before running the tool."
        )
