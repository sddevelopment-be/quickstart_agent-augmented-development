"""Interface module: User-facing utilities and shorthand entry points.

This module provides ergonomic, high-level interfaces for interacting with
the multi-tier agentic framework. It abstracts orchestration complexity and
provides convenient entry points for common operations.

Layer: 0 (Human Interface & Utilities)

References:
    - docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md
"""

from framework.interface.create_client import create_client
from framework.interface.framework_client import FrameworkClient

__all__ = ["FrameworkClient", "create_client"]
