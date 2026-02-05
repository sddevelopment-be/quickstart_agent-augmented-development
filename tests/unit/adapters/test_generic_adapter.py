"""
Unit tests for GenericYAMLAdapter.

Tests the generic YAML-driven adapter implementation following TDD approach (Directive 017).
Covers initialization, binary resolution, command generation, and execution.
"""

import pytest
import os
import platform
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestGenericYAMLAdapterInitialization:
    """Test GenericYAMLAdapter initialization and configuration."""
    
    def test_adapter_initialization_with_minimal_config(self):
        """Test creating adapter with minimal YAML configuration."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        tool_name = "test-tool"
        config = {
            "binary": "test-binary",
            "command_template": "{{binary}} --model {{model}} --prompt {{prompt}}",
            "models": ["model-1", "model-2"]
        }
        
        # Mock shutil.which to return a binary path
        with patch("shutil.which", return_value="/usr/bin/test-binary"):
            adapter = GenericYAMLAdapter(tool_name, config)
            
            assert adapter.get_tool_name() == "test-tool"
            assert adapter.binary_path == "/usr/bin/test-binary"
            assert adapter.tool_config == config
    
    def test_adapter_initialization_with_explicit_binary_path(self):
        """Test adapter uses explicit binary_path from config override."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        tool_name = "custom-tool"
        config = {
            "binary": "custom-binary",
            "binary_path": "/opt/custom/bin/custom-binary",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True):
            adapter = GenericYAMLAdapter(tool_name, config)
            
            assert adapter.binary_path == "/opt/custom/bin/custom-binary"
    
    def test_adapter_initialization_expands_tilde_in_binary_path(self):
        """Test adapter expands ~ in binary_path configuration."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        tool_name = "tool"
        config = {
            "binary": "tool",
            "binary_path": "~/bin/tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True), \
             patch("os.path.expanduser") as mock_expand:
            mock_expand.return_value = "/home/user/bin/tool"
            
            adapter = GenericYAMLAdapter(tool_name, config)
            
            mock_expand.assert_called()
            assert adapter.binary_path == "/home/user/bin/tool"
    
    def test_adapter_initialization_with_platform_paths(self):
        """Test adapter falls back to platform-specific paths."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        tool_name = "platform-tool"
        current_platform = platform.system()
        
        config = {
            "binary": "platform-tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"],
            "platforms": {
                "linux": "/usr/local/bin/platform-tool",
                "macos": "/usr/local/bin/platform-tool",
                "windows": "C:\\Program Files\\platform-tool\\tool.exe"
            }
        }
        
        # Mock shutil.which to return None (not in PATH)
        with patch("shutil.which", return_value=None), \
             patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True), \
             patch("platform.system", return_value="Linux"):
            adapter = GenericYAMLAdapter(tool_name, config)
            
            assert adapter.binary_path == "/usr/local/bin/platform-tool"


class TestGenericYAMLAdapterGetToolName:
    """Test get_tool_name method."""
    
    def test_get_tool_name_returns_configured_name(self):
        """Test get_tool_name returns the tool name from constructor."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        tool_name = "my-awesome-tool"
        config = {
            "binary": "awesome",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/awesome"):
            adapter = GenericYAMLAdapter(tool_name, config)
            
            assert adapter.get_tool_name() == "my-awesome-tool"


class TestGenericYAMLAdapterValidateConfig:
    """Test validate_config method."""
    
    def test_validate_config_with_valid_minimal_config(self):
        """Test validation passes with minimal required fields."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
            assert adapter.validate_config(config) is True
    
    def test_validate_config_fails_without_binary(self):
        """Test validation fails without binary field."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", {"binary": "tool", "command_template": "test", "models": []})
            assert adapter.validate_config(config) is False
    
    def test_validate_config_fails_without_command_template(self):
        """Test validation fails without command_template field."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "binary": "tool",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", {"binary": "tool", "command_template": "test", "models": []})
            assert adapter.validate_config(config) is False
    
    def test_validate_config_fails_without_models(self):
        """Test validation fails without models field."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}"
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", {"binary": "tool", "command_template": "test", "models": []})
            assert adapter.validate_config(config) is False
    
    def test_validate_config_with_optional_fields(self):
        """Test validation passes with optional fields."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"],
            "timeout": 60,
            "platforms": {
                "linux": "/usr/bin/tool"
            }
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
            assert adapter.validate_config(config) is True


class TestGenericYAMLAdapterBinaryResolution:
    """Test binary path resolution logic."""
    
    def test_binary_resolution_config_override_takes_precedence(self):
        """Test explicit binary_path config takes precedence."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "binary": "tool",
            "binary_path": "/opt/override/tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True), \
             patch("shutil.which", return_value="/usr/bin/tool"):  # Should be ignored
            adapter = GenericYAMLAdapter("tool", config)
            
            assert adapter.binary_path == "/opt/override/tool"
    
    def test_binary_resolution_which_fallback(self):
        """Test shutil.which is used when no explicit path."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/local/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
            
            assert adapter.binary_path == "/usr/local/bin/tool"
    
    def test_binary_resolution_platform_fallback(self):
        """Test platform-specific paths used when which returns None."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"],
            "platforms": {
                "linux": "/custom/linux/path/tool",
                "darwin": "/custom/macos/path/tool",
                "windows": "C:\\custom\\windows\\tool.exe"
            }
        }
        
        with patch("shutil.which", return_value=None), \
             patch("platform.system", return_value="Linux"), \
             patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True):
            adapter = GenericYAMLAdapter("tool", config)
            
            assert adapter.binary_path == "/custom/linux/path/tool"
    
    def test_binary_resolution_raises_error_when_not_found(self):
        """Test BinaryNotFoundError raised when binary cannot be found."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter, BinaryNotFoundError
        
        config = {
            "binary": "nonexistent-tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value=None), \
             patch("os.path.exists", return_value=False):
            with pytest.raises(BinaryNotFoundError):
                adapter = GenericYAMLAdapter("tool", config)
    
    def test_binary_resolution_raises_error_when_not_executable(self):
        """Test BinaryNotFoundError raised when binary exists but not executable."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter, BinaryNotFoundError
        
        config = {
            "binary": "tool",
            "binary_path": "/path/to/tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=False):  # Not executable
            with pytest.raises(BinaryNotFoundError) as exc_info:
                adapter = GenericYAMLAdapter("tool", config)
            
            assert "not executable" in str(exc_info.value)


class TestGenericYAMLAdapterExecute:
    """Test execute method."""
    
    def test_execute_success_with_valid_model(self):
        """Test successful execution with valid model."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} --model {{model}} --prompt {{prompt}}",
            "models": ["model-1", "model-2"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
        
        # Mock subprocess execution
        mock_result = ExecutionResult(
            exit_code=0,
            stdout="Success output",
            stderr="",
            duration_seconds=1.5,
            command=["/usr/bin/tool", "--model", "model-1", "--prompt", "test"],
            timed_out=False
        )
        
        with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            response = adapter.execute(prompt="test", model="model-1")
            
            assert response.status == "success"
            assert response.output == "Success output"
            assert response.tool_name == "tool"
            assert response.exit_code == 0
            assert response.duration_seconds == 1.5
    
    def test_execute_fails_with_invalid_model(self):
        """Test execution fails with unsupported model."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter, InvalidModelError
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} --model {{model}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
        
        with pytest.raises(InvalidModelError) as exc_info:
            adapter.execute(prompt="test", model="unsupported-model")
        
        assert "not supported" in str(exc_info.value)
        assert "model-1" in str(exc_info.value)  # Should list supported models
    
    def test_execute_handles_timeout(self):
        """Test execution handles timeout gracefully."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"],
            "timeout": 30
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
        
        # Mock timeout result
        mock_result = ExecutionResult(
            exit_code=-1,
            stdout="",
            stderr="Command timed out after 30 seconds",
            duration_seconds=30.0,
            command=["/usr/bin/tool", "test"],
            timed_out=True
        )
        
        with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            response = adapter.execute(prompt="test", model="model-1")
            
            assert response.status == "error"
            assert "timed out" in response.stderr
    
    def test_execute_handles_nonzero_exit_code(self):
        """Test execution handles non-zero exit code."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
        
        # Mock error result
        mock_result = ExecutionResult(
            exit_code=1,
            stdout="",
            stderr="Error: invalid input",
            duration_seconds=0.5,
            command=["/usr/bin/tool", "test"],
            timed_out=False
        )
        
        with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            response = adapter.execute(prompt="test", model="model-1")
            
            assert response.status == "error"
            assert response.exit_code == 1
            assert "invalid input" in response.stderr
    
    def test_execute_uses_template_parser(self):
        """Test execution uses TemplateParser for command generation."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} --model {{model}} --prompt {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
        
        mock_result = ExecutionResult(
            exit_code=0,
            stdout="output",
            stderr="",
            duration_seconds=1.0,
            command=[],
            timed_out=False
        )
        
        with patch.object(adapter.template_parser, "parse") as mock_parse, \
             patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            mock_parse.return_value = ["/usr/bin/tool", "--model", "model-1", "--prompt", "test"]
            
            adapter.execute(prompt="test", model="model-1")
            
            # Verify template parser was called with correct context
            mock_parse.assert_called_once()
            call_args = mock_parse.call_args
            assert call_args[0][0] == config["command_template"]
            context = call_args[0][1]
            assert context["binary"] == "/usr/bin/tool"
            assert context["model"] == "model-1"
            assert context["prompt"] == "test"
    
    def test_execute_uses_output_normalizer(self):
        """Test execution uses OutputNormalizer for output processing."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        from src.llm_service.adapters.output_normalizer import NormalizedResponse
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
        
        mock_result = ExecutionResult(
            exit_code=0,
            stdout='{"response": "normalized output", "tokens": 100}',
            stderr="",
            duration_seconds=1.0,
            command=[],
            timed_out=False
        )
        
        mock_normalized = NormalizedResponse(
            response_text="normalized output",
            metadata={"tokens": 100},
            errors=[],
            warnings=[],
            raw_output=mock_result.stdout
        )
        
        with patch.object(adapter.output_normalizer, "normalize", return_value=mock_normalized) as mock_norm, \
             patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            
            response = adapter.execute(prompt="test", model="model-1")
            
            # Verify normalizer was called
            mock_norm.assert_called_once_with(mock_result.stdout)
            assert response.output == "normalized output"
            assert response.metadata == {"tokens": 100}
    
    def test_execute_handles_command_generation_error(self):
        """Test execution handles template parsing errors gracefully."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.template_parser import TemplateSyntaxError
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{invalid",  # Invalid syntax
            "models": ["model-1"]
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"):
            adapter = GenericYAMLAdapter("tool", config)
        
        with patch.object(adapter.template_parser, "parse", side_effect=TemplateSyntaxError("Invalid syntax")):
            response = adapter.execute(prompt="test", model="model-1")
            
            assert response.status == "error"
            assert "Failed to build command" in response.stderr


class TestGenericYAMLAdapterIntegration:
    """Integration tests for GenericYAMLAdapter."""
    
    def test_generic_adapter_works_with_claude_code_config(self):
        """Test GenericYAMLAdapter works with claude-code YAML configuration."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        # Simulate claude-code config from YAML
        config = {
            "binary": "claude-code",
            "command_template": "{{binary}} --model {{model}} --prompt {{prompt}}",
            "models": [
                "claude-3.5-sonnet",
                "claude-3-opus",
                "claude-3-haiku"
            ],
            "timeout": 30
        }
        
        with patch("shutil.which", return_value="/usr/local/bin/claude-code"):
            adapter = GenericYAMLAdapter("claude-code", config)
        
        assert adapter.get_tool_name() == "claude-code"
        assert adapter.binary_path == "/usr/local/bin/claude-code"
        
        # Test execution
        mock_result = ExecutionResult(
            exit_code=0,
            stdout="Generated code",
            stderr="",
            duration_seconds=2.5,
            command=[],
            timed_out=False
        )
        
        with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            response = adapter.execute(prompt="Write a function", model="claude-3-opus")
            
            assert response.status == "success"
            assert response.tool_name == "claude-code"
    
    def test_generic_adapter_can_add_new_tool_via_yaml(self):
        """Test adding a completely new tool (codex) via YAML configuration only."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        # New tool config (e.g., OpenAI Codex)
        codex_config = {
            "binary": "openai",
            "command_template": "{{binary}} api completions.create -m {{model}} -p {{prompt}}",
            "models": [
                "gpt-4",
                "gpt-3.5-turbo",
                "text-davinci-003"
            ],
            "timeout": 60,
            "platforms": {
                "linux": "/usr/local/bin/openai",
                "darwin": "/usr/local/bin/openai",
                "windows": "C:\\Program Files\\openai\\openai.exe"
            }
        }
        
        with patch("shutil.which", return_value="/usr/local/bin/openai"):
            adapter = GenericYAMLAdapter("codex", codex_config)
        
        assert adapter.get_tool_name() == "codex"
        assert "gpt-4" in codex_config["models"]
        
        # Test execution works
        mock_result = ExecutionResult(
            exit_code=0,
            stdout='{"choices": [{"text": "Generated code"}]}',
            stderr="",
            duration_seconds=3.0,
            command=[],
            timed_out=False
        )
        
        with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            response = adapter.execute(prompt="Write code", model="gpt-4")
            
            assert response.status == "success"
            assert response.tool_name == "codex"
            # This proves we can add any tool via YAML without code changes!
