"""Multi-tier agentic framework package.

This package implements the four-tier runtime architecture defined in ADR-020:
- Layer 0: Human Interface & Utilities (interface module)
- Layer 1: Orchestration & Governance (core module)
- Layer 2: Model Routing (execution module)
- Layer 3: Model Execution (execution module)

References:
    - docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md
    - docs/architecture/adrs/ADR-021-model-routing-strategy.md
"""

from framework import core, execution, interface

__version__ = "0.1.0"
__all__ = ["core", "execution", "interface"]
