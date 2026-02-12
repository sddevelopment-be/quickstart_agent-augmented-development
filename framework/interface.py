"""Interface module: User-facing utilities and shorthand entry points.

This module provides ergonomic, high-level interfaces for interacting with
the multi-tier agentic framework. It abstracts orchestration complexity and
provides convenient entry points for common operations.

Layer: 0 (Human Interface & Utilities)

References:
    - docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md
"""

from pathlib import Path
from typing import Any


class FrameworkClient:
    """High-level client for framework interaction.

    Provides simplified interfaces to core orchestration and execution
    capabilities without requiring detailed knowledge of internal
    implementation.

    Attributes:
        config_path: Path to framework configuration file.
        mode: Current operational mode (analysis, creative, meta).
    """

    def __init__(
        self,
        config_path: Path | None = None,
        mode: str = "analysis",
    ) -> None:
        """Initialize framework client.

        Args:
            config_path: Optional path to configuration file. If None,
                uses default location.
            mode: Initial operational mode. Must be one of:
                'analysis', 'creative', 'meta'.

        Raises:
            ValueError: If mode is invalid.
        """
        valid_modes = {"analysis", "creative", "meta"}
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode '{mode}'. Must be one of: {valid_modes}")

        self.config_path = config_path or Path(".github/agents/config.yaml")
        self.mode = mode
        self._initialized = False

    def initialize(self) -> None:
        """Initialize framework components.

        Loads configuration, validates directives, and prepares
        orchestration and execution layers.

        Raises:
            FileNotFoundError: If configuration file not found.
            RuntimeError: If initialization fails.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration not found: {self.config_path}")

        # TODO: Load configuration
        # TODO: Initialize core orchestrator
        # TODO: Initialize execution layer
        self._initialized = True

    def execute_task(
        self,
        task_path: Path,
        agent_profile: str | None = None,
    ) -> dict[str, Any]:
        """Execute a task from YAML descriptor.

        Args:
            task_path: Path to task YAML file.
            agent_profile: Optional agent profile override. If None,
                selects based on task requirements.

        Returns:
            Dictionary containing execution results, artifacts, and metadata.

        Raises:
            RuntimeError: If framework not initialized.
            FileNotFoundError: If task file not found.
        """
        if not self._initialized:
            raise RuntimeError("Framework not initialized. Call initialize() first.")

        if not task_path.exists():
            raise FileNotFoundError(f"Task file not found: {task_path}")

        # TODO: Delegate to core orchestrator
        return {
            "status": "pending",
            "task_path": str(task_path),
            "agent": agent_profile,
        }

    def list_available_models(self) -> list[dict[str, Any]]:
        """List available models from routing layer.

        Returns:
            List of model dictionaries with metadata (name, vendor,
            context_window, capabilities).

        Raises:
            RuntimeError: If framework not initialized.
        """
        if not self._initialized:
            raise RuntimeError("Framework not initialized. Call initialize() first.")

        # TODO: Query execution layer for available models
        return []


def create_client(
    config_path: Path | None = None,
    mode: str = "analysis",
    auto_initialize: bool = True,
) -> FrameworkClient:
    """Factory function to create and optionally initialize a client.

    Args:
        config_path: Optional path to configuration file.
        mode: Operational mode.
        auto_initialize: If True, calls initialize() before returning.

    Returns:
        Initialized or uninitialized FrameworkClient instance.

    Raises:
        ValueError: If mode is invalid.
        FileNotFoundError: If auto_initialize is True and config not found.
    """
    client = FrameworkClient(config_path=config_path, mode=mode)
    if auto_initialize:
        client.initialize()
    return client
