"""
Unit tests for base adapter abstract class.

Tests the ToolAdapter ABC contract, ToolResponse dataclass,
and base adapter utilities following TDD approach (Directive 017).
"""

from typing import Any

import pytest


class TestToolResponse:
    """Test ToolResponse dataclass for standardized output."""

    def test_tool_response_creation_with_all_fields(self):
        """Test creating ToolResponse with all fields."""
        from src.llm_service.adapters.base import ToolResponse

        response = ToolResponse(
            status="success",
            output="Generated text response",
            tool_name="claude-code",
            exit_code=0,
            stdout="Command output",
            stderr="",
            duration_seconds=2.5,
            metadata={"tokens": 150, "model": "claude-3-opus"},
        )

        assert response.status == "success"
        assert response.output == "Generated text response"
        assert response.tool_name == "claude-code"
        assert response.exit_code == 0
        assert response.stdout == "Command output"
        assert response.stderr == ""
        assert response.duration_seconds == 2.5
        assert response.metadata == {"tokens": 150, "model": "claude-3-opus"}

    def test_tool_response_creation_minimal_fields(self):
        """Test creating ToolResponse with only required fields."""
        from src.llm_service.adapters.base import ToolResponse

        response = ToolResponse(
            status="success",
            output="Simple response",
            tool_name="test-tool",
        )

        assert response.status == "success"
        assert response.output == "Simple response"
        assert response.tool_name == "test-tool"
        assert response.exit_code is None
        assert response.stdout is None
        assert response.stderr is None
        assert response.duration_seconds is None
        assert response.metadata is None

    def test_tool_response_error_status(self):
        """Test ToolResponse with error status."""
        from src.llm_service.adapters.base import ToolResponse

        response = ToolResponse(
            status="error",
            output="",
            tool_name="failing-tool",
            exit_code=1,
            stderr="Command failed",
        )

        assert response.status == "error"
        assert response.exit_code == 1
        assert response.stderr == "Command failed"

    def test_tool_response_is_dataclass(self):
        """Test that ToolResponse is a proper dataclass."""
        from dataclasses import is_dataclass

        from src.llm_service.adapters.base import ToolResponse

        assert is_dataclass(ToolResponse)


class TestToolAdapter:
    """Test ToolAdapter abstract base class."""

    def test_tool_adapter_is_abstract(self):
        """Test that ToolAdapter cannot be instantiated directly."""
        from src.llm_service.adapters.base import ToolAdapter

        # Should raise TypeError when trying to instantiate ABC
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            ToolAdapter(tool_config={})

    def test_tool_adapter_requires_execute_method(self):
        """Test that subclass must implement execute() method."""
        from src.llm_service.adapters.base import ToolAdapter

        class IncompleteAdapter(ToolAdapter):
            """Adapter missing execute method."""

            def validate_config(self, config: dict[str, Any]) -> bool:
                return True

            def get_tool_name(self) -> str:
                return "incomplete"

        # Should raise TypeError for missing abstract method
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAdapter(tool_config={})

    def test_tool_adapter_requires_validate_config_method(self):
        """Test that subclass must implement validate_config() method."""
        from src.llm_service.adapters.base import ToolAdapter, ToolResponse

        class IncompleteAdapter(ToolAdapter):
            """Adapter missing validate_config method."""

            def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
                return ToolResponse(
                    status="success", output="test", tool_name="incomplete"
                )

            def get_tool_name(self) -> str:
                return "incomplete"

        # Should raise TypeError for missing abstract method
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAdapter(tool_config={})

    def test_tool_adapter_requires_get_tool_name_method(self):
        """Test that subclass must implement get_tool_name() method."""
        from src.llm_service.adapters.base import ToolAdapter, ToolResponse

        class IncompleteAdapter(ToolAdapter):
            """Adapter missing get_tool_name method."""

            def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
                return ToolResponse(
                    status="success", output="test", tool_name="incomplete"
                )

            def validate_config(self, config: dict[str, Any]) -> bool:
                return True

        # Should raise TypeError for missing abstract method
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAdapter(tool_config={})

    def test_concrete_adapter_implementation(self):
        """Test that concrete adapter with all methods can be instantiated."""
        from src.llm_service.adapters.base import ToolAdapter, ToolResponse

        class ConcreteAdapter(ToolAdapter):
            """Complete adapter implementation for testing."""

            def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
                return ToolResponse(
                    status="success",
                    output=f"Executed with {model}",
                    tool_name=self.get_tool_name(),
                )

            def validate_config(self, config: dict[str, Any]) -> bool:
                return "binary" in config

            def get_tool_name(self) -> str:
                return "test-adapter"

        # Should instantiate successfully
        config = {"binary": "test-cli", "models": ["model-1"]}
        adapter = ConcreteAdapter(tool_config=config)

        assert adapter.get_tool_name() == "test-adapter"
        assert adapter.validate_config(config) is True
        assert adapter.tool_config == config

    def test_adapter_execute_returns_tool_response(self):
        """Test that execute() returns ToolResponse object."""
        from src.llm_service.adapters.base import ToolAdapter, ToolResponse

        class TestAdapter(ToolAdapter):
            def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
                return ToolResponse(
                    status="success",
                    output="Test output",
                    tool_name="test",
                    metadata={"prompt_length": len(prompt)},
                )

            def validate_config(self, config: dict[str, Any]) -> bool:
                return True

            def get_tool_name(self) -> str:
                return "test"

        adapter = TestAdapter(tool_config={})
        response = adapter.execute(prompt="Test prompt", model="test-model")

        assert isinstance(response, ToolResponse)
        assert response.status == "success"
        assert response.output == "Test output"
        assert response.metadata["prompt_length"] == 11

    def test_adapter_stores_tool_config(self):
        """Test that adapter stores tool configuration."""
        from src.llm_service.adapters.base import ToolAdapter, ToolResponse

        class TestAdapter(ToolAdapter):
            def execute(self, prompt: str, model: str, **kwargs) -> ToolResponse:
                return ToolResponse(status="success", output="test", tool_name="test")

            def validate_config(self, config: dict[str, Any]) -> bool:
                return True

            def get_tool_name(self) -> str:
                return "test"

        config = {
            "binary": "/usr/bin/test",
            "models": ["model-1", "model-2"],
            "timeout": 30,
        }
        adapter = TestAdapter(tool_config=config)

        assert adapter.tool_config == config
        assert adapter.tool_config["binary"] == "/usr/bin/test"
        assert adapter.tool_config["timeout"] == 30


class TestToolAdapterTypeHints:
    """Test type hints on ToolAdapter methods."""

    def test_execute_method_signature(self):
        """Test execute() method has correct type hints."""
        import inspect

        from src.llm_service.adapters.base import ToolAdapter, ToolResponse

        sig = inspect.signature(ToolAdapter.execute)

        # Check parameter annotations
        assert sig.parameters["prompt"].annotation == str
        assert sig.parameters["model"].annotation == str

        # Check return annotation
        assert sig.return_annotation == ToolResponse

    def test_validate_config_method_signature(self):
        """Test validate_config() method has correct type hints."""
        import inspect

        from src.llm_service.adapters.base import ToolAdapter

        sig = inspect.signature(ToolAdapter.validate_config)

        # Check parameter annotations
        assert sig.parameters["config"].annotation == dict[str, Any]

        # Check return annotation
        assert sig.return_annotation == bool

    def test_get_tool_name_method_signature(self):
        """Test get_tool_name() method has correct type hints."""
        import inspect

        from src.llm_service.adapters.base import ToolAdapter

        sig = inspect.signature(ToolAdapter.get_tool_name)

        # Check return annotation
        assert sig.return_annotation == str
