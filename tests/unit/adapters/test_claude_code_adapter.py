"""
Unit tests for ClaudeCodeAdapter.

Tests the first concrete adapter implementation following TDD approach (Directive 017).
Covers model mapping, binary resolution, command generation, and error handling.
"""

import pytest
import os
import platform
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestClaudeCodeAdapterInitialization:
    """Test ClaudeCodeAdapter initialization and configuration."""
    
    def test_adapter_initialization_with_minimal_config(self):
        """Test creating adapter with minimal configuration."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {}
        
        # Mock shutil.which to return a binary path
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.get_tool_name() == "claude-code"
            assert adapter.binary_path == "/usr/bin/claude-code"
            assert adapter.command_template == adapter.DEFAULT_TEMPLATE
    
    def test_adapter_initialization_with_full_config(self):
        """Test creating adapter with full configuration."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {
            "binary_path": "/custom/path/claude-code",
            "models": ["claude-3-opus"],
            "timeout": 60,
            "template": "{{binary}} --model {{model}} {{prompt}}"
        }
        
        # Mock os.path.exists and os.access to simulate binary exists
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True):
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.binary_path == "/custom/path/claude-code"
            assert adapter.command_template == config["template"]
    
    def test_adapter_initialization_with_explicit_binary_path(self):
        """Test adapter uses explicit binary_path from config."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {
            "binary_path": "/opt/claude/bin/claude-code"
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True):
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.binary_path == "/opt/claude/bin/claude-code"
    
    def test_adapter_initialization_expands_tilde_in_binary_path(self):
        """Test adapter expands ~ in binary_path configuration."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {
            "binary_path": "~/bin/claude-code"
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True), \
             patch("os.path.expanduser") as mock_expand:
            mock_expand.return_value = "/home/user/bin/claude-code"
            
            adapter = ClaudeCodeAdapter(config)
            
            mock_expand.assert_called_with("~/bin/claude-code")
            assert adapter.binary_path == "/home/user/bin/claude-code"


class TestClaudeCodeAdapterGetToolName:
    """Test get_tool_name method."""
    
    def test_get_tool_name_returns_claude_code(self):
        """Test get_tool_name returns 'claude-code'."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.get_tool_name() == "claude-code"


class TestClaudeCodeAdapterValidateConfig:
    """Test validate_config method."""
    
    def test_validate_config_accepts_empty_config(self):
        """Test validate_config accepts empty configuration."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.validate_config(config) is True
    
    def test_validate_config_accepts_valid_config(self):
        """Test validate_config accepts all valid configuration fields."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {
            "binary_path": "/usr/bin/claude-code",
            "models": ["claude-3-opus", "claude-3-haiku"],
            "timeout": 30,
            "template": "{{binary}} --model {{model}}"
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True):
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.validate_config(config) is True
    
    def test_validate_config_rejects_invalid_binary_path_type(self):
        """Test validate_config rejects non-string binary_path."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {"binary_path": 123}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter({})
            
            assert adapter.validate_config(config) is False
    
    def test_validate_config_rejects_invalid_models_type(self):
        """Test validate_config rejects non-list models."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {"models": "claude-3-opus"}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter({})
            
            assert adapter.validate_config(config) is False
    
    def test_validate_config_rejects_invalid_timeout_type(self):
        """Test validate_config rejects non-numeric timeout."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {"timeout": "30"}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter({})
            
            assert adapter.validate_config(config) is False
    
    def test_validate_config_rejects_negative_timeout(self):
        """Test validate_config rejects negative timeout."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {"timeout": -10}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter({})
            
            assert adapter.validate_config(config) is False


class TestClaudeCodeAdapterModelMapping:
    """Test model name mapping functionality."""
    
    def test_model_mapping_claude_3_5_sonnet(self):
        """Test model mapping for claude-3.5-sonnet."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        assert "claude-3.5-sonnet" in ClaudeCodeAdapter.MODEL_MAPPING
        assert ClaudeCodeAdapter.MODEL_MAPPING["claude-3.5-sonnet"] == "claude-3-5-sonnet-20240620"
    
    def test_model_mapping_claude_3_opus(self):
        """Test model mapping for claude-3-opus."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        assert "claude-3-opus" in ClaudeCodeAdapter.MODEL_MAPPING
        assert ClaudeCodeAdapter.MODEL_MAPPING["claude-3-opus"] == "claude-3-opus-20240229"
    
    def test_model_mapping_claude_3_haiku(self):
        """Test model mapping for claude-3-haiku."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        assert "claude-3-haiku" in ClaudeCodeAdapter.MODEL_MAPPING
        assert ClaudeCodeAdapter.MODEL_MAPPING["claude-3-haiku"] == "claude-3-haiku-20240307"
    
    def test_model_mapping_includes_aliases(self):
        """Test model mapping includes convenient aliases."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        # Test aliases exist
        assert "claude-3.5" in ClaudeCodeAdapter.MODEL_MAPPING
        assert "claude-opus" in ClaudeCodeAdapter.MODEL_MAPPING
        assert "claude-haiku" in ClaudeCodeAdapter.MODEL_MAPPING
        
        # Test aliases map correctly
        assert (ClaudeCodeAdapter.MODEL_MAPPING["claude-3.5"] == 
                ClaudeCodeAdapter.MODEL_MAPPING["claude-3.5-sonnet"])


class TestClaudeCodeAdapterExecute:
    """Test execute method for command execution."""
    
    def test_execute_successful_with_plain_text_output(self):
        """Test successful execution with plain text output."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            # Mock subprocess execution
            mock_result = ExecutionResult(
                exit_code=0,
                stdout="This is the LLM response",
                stderr="",
                duration_seconds=2.5,
                command=["claude-code", "--model", "claude-3-opus-20240229", "--prompt", "test"],
                timed_out=False
            )
            
            with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
                response = adapter.execute(prompt="test", model="claude-3-opus")
                
                assert response.status == "success"
                assert response.output == "This is the LLM response"
                assert response.tool_name == "claude-code"
                assert response.exit_code == 0
                assert response.duration_seconds == 2.5
    
    def test_execute_successful_with_json_output(self):
        """Test successful execution with JSON output."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        import json
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            # Mock subprocess execution with JSON output
            json_output = json.dumps({
                "response": "LLM generated text",
                "tokens": 150,
                "model": "claude-3-opus"
            })
            
            mock_result = ExecutionResult(
                exit_code=0,
                stdout=json_output,
                stderr="",
                duration_seconds=1.8,
                command=["claude-code", "--model", "claude-3-opus-20240229", "--prompt", "test"],
                timed_out=False
            )
            
            with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
                response = adapter.execute(prompt="test", model="claude-3-opus")
                
                assert response.status == "success"
                assert response.output == "LLM generated text"
                assert response.metadata["tokens"] == 150
                assert response.tool_name == "claude-code"
    
    def test_execute_fails_with_invalid_model(self):
        """Test execute fails with helpful error for unsupported model."""
        from src.llm_service.adapters.claude_code_adapter import (
            ClaudeCodeAdapter,
            InvalidModelError
        )
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            with pytest.raises(InvalidModelError) as exc_info:
                adapter.execute(prompt="test", model="gpt-4")
            
            assert "gpt-4" in str(exc_info.value)
            assert "Supported models:" in str(exc_info.value)
    
    def test_execute_handles_command_not_found_error(self):
        """Test execute handles binary not found error."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        from src.llm_service.adapters.subprocess_wrapper import CommandNotFoundError
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            # Mock subprocess to raise CommandNotFoundError
            with patch.object(
                adapter.subprocess_wrapper, 
                "execute", 
                side_effect=CommandNotFoundError("Binary not found")
            ):
                response = adapter.execute(prompt="test", model="claude-3-opus")
                
                assert response.status == "error"
                assert "not found" in response.stderr.lower()
                assert "installation instructions" in response.stderr.lower()
    
    def test_execute_handles_timeout(self):
        """Test execute handles command timeout."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {"timeout": 5}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            # Mock subprocess execution with timeout
            mock_result = ExecutionResult(
                exit_code=-1,
                stdout="",
                stderr="Command timed out after 5 seconds",
                duration_seconds=5.0,
                command=["claude-code", "--model", "claude-3-opus-20240229", "--prompt", "test"],
                timed_out=True
            )
            
            with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
                response = adapter.execute(prompt="test", model="claude-3-opus")
                
                assert response.status == "error"
                assert "timed out" in response.stderr.lower()
    
    def test_execute_handles_non_zero_exit_code(self):
        """Test execute handles non-zero exit code."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            # Mock subprocess execution with error
            mock_result = ExecutionResult(
                exit_code=1,
                stdout="",
                stderr="Invalid API key",
                duration_seconds=0.5,
                command=["claude-code", "--model", "claude-3-opus-20240229", "--prompt", "test"],
                timed_out=False
            )
            
            with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
                response = adapter.execute(prompt="test", model="claude-3-opus")
                
                assert response.status == "error"
                assert response.exit_code == 1
                assert "Invalid API key" in response.stderr
    
    def test_execute_uses_correct_command_template(self):
        """Test execute builds command correctly from template."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            mock_result = ExecutionResult(
                exit_code=0,
                stdout="response",
                stderr="",
                duration_seconds=1.0,
                command=["claude-code", "--model", "claude-3-opus-20240229", "--prompt", "test_prompt"],
                timed_out=False
            )
            
            with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result) as mock_exec:
                response = adapter.execute(prompt="test_prompt", model="claude-3-opus")
                
                # Verify command was built correctly
                called_command = mock_exec.call_args[0][0]
                assert called_command[0] == "/usr/bin/claude-code"
                assert "--model" in called_command
                assert "claude-3-opus-20240229" in called_command
                assert "--prompt" in called_command
                assert "test_prompt" in called_command


class TestClaudeCodeAdapterBinaryResolution:
    """Test binary path resolution logic."""
    
    def test_binary_resolution_uses_explicit_config_first(self):
        """Test binary resolution prioritizes explicit config."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {
            "binary_path": "/explicit/path/claude-code"
        }
        
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=True), \
             patch("shutil.which") as mock_which:
            # shutil.which should not be called when explicit path is provided
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.binary_path == "/explicit/path/claude-code"
            mock_which.assert_not_called()
    
    def test_binary_resolution_uses_shutil_which_second(self):
        """Test binary resolution uses shutil.which if no explicit path."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code") as mock_which:
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.binary_path == "/usr/bin/claude-code"
            mock_which.assert_called_once_with("claude-code")
    
    def test_binary_resolution_tries_platform_specific_paths(self):
        """Test binary resolution tries platform-specific default paths."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {}
        
        # Mock shutil.which to return None (not in PATH)
        with patch("shutil.which", return_value=None), \
             patch("platform.system", return_value="Linux"), \
             patch("os.path.exists") as mock_exists, \
             patch("os.access") as mock_access:
            
            # First path doesn't exist, second path exists
            def exists_side_effect(path):
                return path == os.path.expanduser("~/.local/bin/claude-code")
            
            mock_exists.side_effect = exists_side_effect
            mock_access.return_value = True
            
            adapter = ClaudeCodeAdapter(config)
            
            assert adapter.binary_path == os.path.expanduser("~/.local/bin/claude-code")
    
    def test_binary_resolution_raises_error_when_not_found(self):
        """Test binary resolution raises BinaryNotFoundError when not found."""
        from src.llm_service.adapters.claude_code_adapter import (
            ClaudeCodeAdapter,
            BinaryNotFoundError
        )
        
        config = {}
        
        with patch("shutil.which", return_value=None), \
             patch("os.path.exists", return_value=False):
            
            with pytest.raises(BinaryNotFoundError) as exc_info:
                adapter = ClaudeCodeAdapter(config)
            
            error_message = str(exc_info.value)
            assert "not found" in error_message.lower()
            assert "installation instructions" in error_message.lower()
    
    def test_binary_resolution_raises_error_when_not_executable(self):
        """Test binary resolution raises error when binary exists but not executable."""
        from src.llm_service.adapters.claude_code_adapter import (
            ClaudeCodeAdapter,
            BinaryNotFoundError
        )
        
        config = {
            "binary_path": "/usr/bin/claude-code"
        }
        
        # Binary exists but is not executable
        with patch("os.path.exists", return_value=True), \
             patch("os.access", return_value=False):
            
            with pytest.raises(BinaryNotFoundError) as exc_info:
                adapter = ClaudeCodeAdapter(config)
            
            error_message = str(exc_info.value)
            assert "not executable" in error_message.lower()
            assert "chmod +x" in error_message.lower()


class TestClaudeCodeAdapterErrorFormatting:
    """Test error message formatting."""
    
    def test_format_binary_not_found_error_includes_install_instructions(self):
        """Test binary not found error includes installation instructions."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"):
            adapter = ClaudeCodeAdapter(config)
            
            error_msg = adapter._format_binary_not_found_error()
            
            assert "not found" in error_msg.lower()
            assert "npm install" in error_msg.lower()
            assert "@anthropic-ai/claude-code" in error_msg
            assert "binary_path" in error_msg
    
    def test_format_binary_not_found_error_includes_platform_paths(self):
        """Test binary not found error includes platform-specific paths."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {}
        
        with patch("shutil.which", return_value="/usr/bin/claude-code"), \
             patch("platform.system", return_value="Linux"):
            adapter = ClaudeCodeAdapter(config)
            
            error_msg = adapter._format_binary_not_found_error()
            
            # Should include Linux paths
            assert "/usr/local/bin/claude-code" in error_msg
            assert "~/.local/bin/claude-code" in error_msg
