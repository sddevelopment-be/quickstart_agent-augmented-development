"""Execution module: Model routing and execution interfaces.

This module implements Layer 2 (Model Routing) and Layer 3 (Model Execution):
- Router configuration and selection (OpenRouter, OpenCode.ai)
- Direct API clients (OpenAI, Anthropic)
- Local model interfaces (Ollama)
- Fallback and retry logic

References:
    - docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md
    - docs/architecture/adrs/ADR-021-model-routing-strategy.md
"""

from framework.execution.execution_client import ExecutionClient
from framework.execution.model_capabilities import ModelCapabilities
from framework.execution.model_config import ModelConfig
from framework.execution.model_provider import ModelProvider
from framework.execution.model_router import ModelRouter
from framework.execution.ollama_client import OllamaClient

__all__ = [
    "ExecutionClient",
    "ModelCapabilities",
    "ModelConfig",
    "ModelProvider",
    "ModelRouter",
    "OllamaClient",
]
