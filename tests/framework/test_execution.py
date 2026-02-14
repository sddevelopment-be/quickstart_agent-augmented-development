"""Tests for framework.execution module.

Tests model routing and execution interfaces (Layers 2 & 3).

References:
    - docs/styleguides/python_conventions.md (Quad-A pattern)
    - framework/execution/
"""

import pytest

from framework.execution import (
    ExecutionClient,
    ModelCapabilities,
    ModelConfig,
    ModelProvider,
    ModelRouter,
    OllamaClient,
)


class TestModelProvider:
    """Test suite for ModelProvider enum."""

    def test_model_provider_values(self) -> None:
        """Test ModelProvider enum contains expected values."""
        # Arrange
        expected_providers = {"openai", "anthropic", "openrouter", "opencode", "ollama"}

        # Act
        actual_providers = {provider.value for provider in ModelProvider}

        # Assert
        assert actual_providers == expected_providers


class TestModelCapabilities:
    """Test suite for ModelCapabilities dataclass."""

    def test_model_capabilities_defaults(self) -> None:
        """Test ModelCapabilities with default values."""
        # Arrange & Act
        caps = ModelCapabilities(context_window=8192)

        # Assert
        assert caps.context_window == 8192
        assert not caps.supports_tools
        assert not caps.supports_structured_output
        assert not caps.supports_streaming

    def test_model_capabilities_custom_values(self) -> None:
        """Test ModelCapabilities with custom values."""
        # Arrange & Act
        caps = ModelCapabilities(
            context_window=128000,
            supports_tools=True,
            supports_structured_output=True,
            supports_streaming=True,
        )

        # Assert
        assert caps.context_window == 128000
        assert caps.supports_tools
        assert caps.supports_structured_output
        assert caps.supports_streaming


class TestModelConfig:
    """Test suite for ModelConfig dataclass."""

    def test_model_config_minimal(self) -> None:
        """Test ModelConfig with minimal required fields."""
        # Arrange
        caps = ModelCapabilities(context_window=8192)

        # Act
        config = ModelConfig(
            id="gpt-4",
            provider=ModelProvider.OPENAI,
            name="GPT-4",
            capabilities=caps,
        )

        # Assert
        assert config.id == "gpt-4"
        assert config.provider == ModelProvider.OPENAI
        assert config.name == "GPT-4"
        assert config.capabilities == caps
        assert config.cost_per_1k_tokens == 0.0
        assert not config.is_local

    def test_model_config_local_model(self) -> None:
        """Test ModelConfig for local model."""
        # Arrange
        caps = ModelCapabilities(context_window=32768, supports_tools=True)

        # Act
        config = ModelConfig(
            id="llama3:70b",
            provider=ModelProvider.OLLAMA,
            name="Llama 3 70B",
            capabilities=caps,
            is_local=True,
        )

        # Assert
        assert config.id == "llama3:70b"
        assert config.provider == ModelProvider.OLLAMA
        assert config.is_local
        assert config.cost_per_1k_tokens == 0.0


class TestModelRouter:
    """Test suite for ModelRouter class."""

    def test_router_init_default_config_path(self) -> None:
        """Test router initialization with default config path."""
        # Arrange & Act
        router = ModelRouter()

        # Assert
        assert router.config_path == ".doctrine-config/model_router.yaml"
        assert router._models == {}
        assert router._fallback_chains == {}

    def test_router_init_custom_config_path(self) -> None:
        """Test router initialization with custom config path."""
        # Arrange
        custom_path = "/custom/path/router.yaml"

        # Act
        router = ModelRouter(config_path=custom_path)

        # Assert
        assert router.config_path == custom_path

    def test_select_model_not_initialized_raises_error(self) -> None:
        """Test select_model raises RuntimeError when router not initialized."""
        # Arrange
        router = ModelRouter()

        # Assumption Check
        assert (
            not router._models
        ), "Test precondition failed: router should have no models loaded"

        # Act & Assert
        with pytest.raises(RuntimeError) as exc_info:
            router.select_model(task_type="analysis")

        assert "not initialized" in str(exc_info.value).lower()

    def test_get_fallback_chain_unknown_model_raises_error(self) -> None:
        """Test get_fallback_chain raises ValueError for unknown model."""
        # Arrange
        router = ModelRouter()
        unknown_model = "unknown-model-id"

        # Assumption Check
        assert (
            unknown_model not in router._models
        ), "Test precondition failed: model should NOT exist"

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            router.get_fallback_chain(unknown_model)

        assert "unknown model" in str(exc_info.value).lower()
        assert unknown_model in str(exc_info.value)

    def test_get_fallback_chain_returns_empty_if_none(self) -> None:
        """Test get_fallback_chain returns empty list when no fallbacks."""
        # Arrange
        router = ModelRouter()
        caps = ModelCapabilities(context_window=8192)
        config = ModelConfig(
            id="test-model",
            provider=ModelProvider.OPENAI,
            name="Test Model",
            capabilities=caps,
        )
        router._models["test-model"] = config

        # Assumption Check
        assert (
            "test-model" in router._models
        ), "Test precondition failed: model should exist"
        assert (
            "test-model" not in router._fallback_chains
        ), "Test precondition failed: no fallback chain should exist"

        # Act
        result = router.get_fallback_chain("test-model")

        # Assert
        assert result == []


class TestExecutionClient:
    """Test suite for ExecutionClient base class."""

    def test_execution_client_init(self) -> None:
        """Test ExecutionClient initialization."""
        # Arrange & Act
        client = ExecutionClient(provider=ModelProvider.OPENAI, api_key="test-key")

        # Assert
        assert client.provider == ModelProvider.OPENAI
        assert client.api_key == "test-key"

    def test_execution_client_invoke_not_implemented(self) -> None:
        """Test ExecutionClient.invoke raises NotImplementedError."""
        # Arrange
        client = ExecutionClient(provider=ModelProvider.OPENAI)

        # Act & Assert
        with pytest.raises(NotImplementedError):
            client.invoke(model_id="gpt-4", prompt="test")


class TestOllamaClient:
    """Test suite for OllamaClient class."""

    def test_ollama_client_init_default_url(self) -> None:
        """Test OllamaClient initialization with default URL."""
        # Arrange & Act
        client = OllamaClient()

        # Assert
        assert client.provider == ModelProvider.OLLAMA
        assert client.base_url == "http://localhost:11434"
        assert client.api_key is None

    def test_ollama_client_init_custom_url(self) -> None:
        """Test OllamaClient initialization with custom URL."""
        # Arrange
        custom_url = "http://nas.local:11434"

        # Act
        client = OllamaClient(base_url=custom_url)

        # Assert
        assert client.base_url == custom_url

    def test_ollama_client_invoke_returns_dict(self) -> None:
        """Test OllamaClient.invoke returns response dictionary."""
        # Arrange
        client = OllamaClient()
        model_id = "llama3:70b"
        prompt = "Test prompt"

        # Act
        result = client.invoke(model_id=model_id, prompt=prompt)

        # Assert
        assert isinstance(result, dict)
        assert "model" in result
        assert result["model"] == model_id
        assert "provider" in result
        assert result["provider"] == "ollama"
