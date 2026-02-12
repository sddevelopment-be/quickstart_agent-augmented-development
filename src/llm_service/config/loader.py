"""
Configuration Loader for LLM Service Layer

This module provides functionality to load and validate YAML configuration files
using Pydantic schemas. It handles loading all four configuration types:
- agents.yaml
- tools.yaml
- models.yaml
- policies.yaml
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from .schemas import (
    AgentsSchema,
    ModelsSchema,
    PoliciesSchema,
    ToolsSchema,
    validate_agent_references,
)


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""

    pass


class ConfigurationLoader:
    """
    Loads and validates LLM service configuration files.

    Supports loading from a configuration directory containing:
    - agents.yaml (or agents.yml)
    - tools.yaml (or tools.yml)
    - models.yaml (or models.yml)
    - policies.yaml (or policies.yml)
    """

    def __init__(self, config_dir: Path):
        """
        Initialize configuration loader.

        Args:
            config_dir: Path to directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise ConfigurationError(
                f"Configuration directory does not exist: {config_dir}"
            )
        if not self.config_dir.is_dir():
            raise ConfigurationError(
                f"Configuration path is not a directory: {config_dir}"
            )

    def _find_config_file(self, base_name: str) -> Path | None:
        """
        Find configuration file with .yaml or .yml extension.

        Args:
            base_name: Base name of config file (e.g., 'agents')

        Returns:
            Path to config file, or None if not found
        """
        for ext in [".yaml", ".yml"]:
            path = self.config_dir / f"{base_name}{ext}"
            if path.exists():
                return path
        return None

    def _load_yaml_file(self, file_path: Path) -> dict[str, Any]:
        """
        Load and parse YAML file.

        Args:
            file_path: Path to YAML file

        Returns:
            Parsed YAML content as dictionary

        Raises:
            ConfigurationError: If file cannot be read or parsed
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data is None:
                    raise ConfigurationError(f"Empty configuration file: {file_path}")
                return data
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in {file_path}: {e}")
        except OSError as e:
            raise ConfigurationError(f"Cannot read file {file_path}: {e}")

    def load_agents(self) -> AgentsSchema:
        """
        Load and validate agents configuration.

        Returns:
            Validated AgentsSchema object

        Raises:
            ConfigurationError: If file not found or validation fails
        """
        file_path = self._find_config_file("agents")
        if not file_path:
            raise ConfigurationError(
                f"agents.yaml not found in configuration directory: {self.config_dir}\n"
                f"Expected location: {self.config_dir / 'agents.yaml'} or {self.config_dir / 'agents.yml'}"
            )

        data = self._load_yaml_file(file_path)

        try:
            return AgentsSchema(**data)
        except ValidationError as e:
            raise ConfigurationError(f"Invalid agents configuration: {e}")

    def load_tools(self) -> ToolsSchema:
        """
        Load and validate tools configuration.

        Returns:
            Validated ToolsSchema object

        Raises:
            ConfigurationError: If file not found or validation fails
        """
        file_path = self._find_config_file("tools")
        if not file_path:
            raise ConfigurationError(
                f"tools.yaml not found in configuration directory: {self.config_dir}\n"
                f"Expected location: {self.config_dir / 'tools.yaml'} or {self.config_dir / 'tools.yml'}"
            )

        data = self._load_yaml_file(file_path)

        try:
            return ToolsSchema(**data)
        except ValidationError as e:
            raise ConfigurationError(f"Invalid tools configuration: {e}")

    def load_models(self) -> ModelsSchema:
        """
        Load and validate models configuration.

        Returns:
            Validated ModelsSchema object

        Raises:
            ConfigurationError: If file not found or validation fails
        """
        file_path = self._find_config_file("models")
        if not file_path:
            raise ConfigurationError(
                f"models.yaml not found in configuration directory: {self.config_dir}\n"
                f"Expected location: {self.config_dir / 'models.yaml'} or {self.config_dir / 'models.yml'}"
            )

        data = self._load_yaml_file(file_path)

        try:
            return ModelsSchema(**data)
        except ValidationError as e:
            raise ConfigurationError(f"Invalid models configuration: {e}")

    def load_policies(self) -> PoliciesSchema:
        """
        Load and validate policies configuration.

        Returns:
            Validated PoliciesSchema object

        Raises:
            ConfigurationError: If file not found or validation fails
        """
        file_path = self._find_config_file("policies")
        if not file_path:
            raise ConfigurationError(
                f"policies.yaml not found in configuration directory: {self.config_dir}\n"
                f"Expected location: {self.config_dir / 'policies.yaml'} or {self.config_dir / 'policies.yml'}"
            )

        data = self._load_yaml_file(file_path)

        try:
            return PoliciesSchema(**data)
        except ValidationError as e:
            raise ConfigurationError(f"Invalid policies configuration: {e}")

    def load_all(self) -> dict[str, Any]:
        """
        Load and validate all configuration files.

        Performs cross-reference validation to ensure consistency.

        Returns:
            Dictionary with keys: 'agents', 'tools', 'models', 'policies'

        Raises:
            ConfigurationError: If any file fails validation or cross-references are invalid
        """
        # Load all configurations
        agents = self.load_agents()
        tools = self.load_tools()
        models = self.load_models()
        policies = self.load_policies()

        # Perform cross-reference validation
        errors = validate_agent_references(agents, tools, models)
        if errors:
            error_msg = "Configuration cross-reference validation failed:\n"
            error_msg += "\n".join(f"  - {err}" for err in errors)
            raise ConfigurationError(error_msg)

        return {
            "agents": agents,
            "tools": tools,
            "models": models,
            "policies": policies,
        }


def load_configuration(config_dir: str) -> dict[str, Any]:
    """
    Convenience function to load all configuration files.

    Args:
        config_dir: Path to configuration directory

    Returns:
        Dictionary with validated configuration schemas

    Raises:
        ConfigurationError: If loading or validation fails
    """
    loader = ConfigurationLoader(Path(config_dir))
    return loader.load_all()
