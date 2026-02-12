"""Factory function for creating framework clients."""

from pathlib import Path

from framework.interface.framework_client import FrameworkClient


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
