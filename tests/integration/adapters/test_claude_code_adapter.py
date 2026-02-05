"""
Integration tests for ClaudeCodeAdapter with mocked CLI.

Tests end-to-end execution flow using fake_claude_cli.py to simulate
the real claude-code CLI behavior without requiring actual tool installation.
"""

import pytest
import os
import sys
import json
from pathlib import Path


# Get path to fake CLI
FIXTURES_DIR = Path(__file__).parent.parent.parent / "fixtures"
FAKE_CLI_PATH = FIXTURES_DIR / "fake_claude_cli.py"


class TestClaudeCodeAdapterIntegration:
    """Integration tests with fake claude CLI."""
    
    @pytest.fixture
    def fake_cli_config(self):
        """Configuration pointing to fake CLI."""
        return {
            "binary_path": str(FAKE_CLI_PATH),
            "timeout": 30
        }
    
    def test_successful_execution_plain_text(self, fake_cli_config):
        """Test successful execution with plain text output."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Write a function to add two numbers",
            model="claude-3-opus"
        )
        
        assert response.status == "success"
        assert "def example_function" in response.output
        assert response.tool_name == "claude-code"
        assert response.exit_code == 0
        assert response.duration_seconds is not None
        assert response.duration_seconds > 0
    
    def test_successful_execution_with_different_models(self, fake_cli_config):
        """Test execution works with different supported models."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        models = ["claude-3-opus", "claude-3.5-sonnet", "claude-3-haiku"]
        
        for model in models:
            response = adapter.execute(
                prompt="Test prompt",
                model=model
            )
            
            assert response.status == "success"
            assert response.tool_name == "claude-code"
            assert response.exit_code == 0
            assert len(response.output) > 0
    
    def test_successful_execution_json_output(self, fake_cli_config):
        """Test successful execution with JSON output format."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        # Override template to request JSON format
        fake_cli_config["template"] = '{{binary}} --model {{model}} --prompt "{{prompt}}" --format json'
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Write a pytest test",
            model="claude-3-opus"
        )
        
        assert response.status == "success"
        assert "test" in response.output.lower() or "pytest" in response.output.lower()
        assert response.metadata is not None
        # JSON format should extract metadata
        assert "tokens" in response.metadata or "model" in response.metadata
    
    def test_model_mapping_to_cli_parameters(self, fake_cli_config):
        """Test that model names are correctly mapped to CLI parameters."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        # Test alias mapping
        response = adapter.execute(
            prompt="Test",
            model="claude-opus"  # Alias should map to claude-3-opus-20240229
        )
        
        assert response.status == "success"
        assert response.exit_code == 0
    
    def test_invalid_model_error(self, fake_cli_config):
        """Test error handling for invalid model."""
        from src.llm_service.adapters.claude_code_adapter import (
            ClaudeCodeAdapter,
            InvalidModelError
        )
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        with pytest.raises(InvalidModelError) as exc_info:
            adapter.execute(
                prompt="Test",
                model="gpt-4"  # Unsupported model
            )
        
        assert "gpt-4" in str(exc_info.value)
        assert "Supported models:" in str(exc_info.value)
    
    def test_cli_error_handling_api_error(self, fake_cli_config):
        """Test handling of CLI errors (API authentication failure)."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        # Override template to trigger API error in fake CLI
        fake_cli_config["template"] = '{{binary}} --model {{model}} --prompt "{{prompt}}" --error api-error'
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Test",
            model="claude-3-opus"
        )
        
        assert response.status == "error"
        assert response.exit_code == 2
        assert "api" in response.stderr.lower() or "authentication" in response.stderr.lower()
    
    def test_timeout_handling(self, fake_cli_config):
        """Test handling of command timeout."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        # Set very short timeout
        fake_cli_config["timeout"] = 1
        # Override template to trigger slow response
        fake_cli_config["template"] = '{{binary}} --model {{model}} --prompt "{{prompt}}" --delay 2'
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Test",
            model="claude-3-opus"
        )
        
        assert response.status == "error"
        assert "timeout" in response.stderr.lower() or "timed out" in response.stderr.lower()
    
    def test_binary_not_found_error(self):
        """Test error handling when binary is not found."""
        from src.llm_service.adapters.claude_code_adapter import (
            ClaudeCodeAdapter,
            BinaryNotFoundError
        )
        
        config = {
            "binary_path": "/nonexistent/path/claude-code"
        }
        
        with pytest.raises(BinaryNotFoundError) as exc_info:
            adapter = ClaudeCodeAdapter(config)
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_output_parsing_plain_text(self, fake_cli_config):
        """Test output parsing for plain text responses."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Write a function",
            model="claude-3-opus"
        )
        
        assert response.status == "success"
        assert isinstance(response.output, str)
        assert len(response.output) > 0
        # Plain text output should have response text
        assert "def" in response.output or "function" in response.output
    
    def test_output_parsing_json_format(self, fake_cli_config):
        """Test output parsing for JSON formatted responses."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        # Request JSON format
        fake_cli_config["template"] = '{{binary}} --model {{model}} --prompt "{{prompt}}" --format json'
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Write a test",
            model="claude-3-opus"
        )
        
        assert response.status == "success"
        # Should extract response text from JSON
        assert isinstance(response.output, str)
        assert len(response.output) > 0
        # Should parse metadata
        assert response.metadata is not None
        assert isinstance(response.metadata, dict)
    
    def test_execution_with_special_characters_in_prompt(self, fake_cli_config):
        """Test execution handles special characters in prompt safely."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        # Prompt with various special characters
        special_prompt = "Test with 'quotes', \"double quotes\", and $pecial ch@rs"
        
        response = adapter.execute(
            prompt=special_prompt,
            model="claude-3-opus"
        )
        
        # Should not fail due to special characters
        assert response.status == "success"
        assert response.exit_code == 0
    
    def test_execution_duration_tracking(self, fake_cli_config):
        """Test that execution duration is tracked correctly."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Test",
            model="claude-3-opus"
        )
        
        assert response.status == "success"
        assert response.duration_seconds is not None
        assert isinstance(response.duration_seconds, float)
        assert response.duration_seconds > 0
        # Should complete quickly (fake CLI has 0.1s delay by default)
        assert response.duration_seconds < 5.0


class TestClaudeCodeAdapterBinaryResolutionIntegration:
    """Integration tests for binary path resolution."""
    
    def test_explicit_binary_path_resolution(self):
        """Test adapter uses explicit binary_path configuration."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        config = {
            "binary_path": str(FAKE_CLI_PATH)
        }
        
        adapter = ClaudeCodeAdapter(config)
        
        assert adapter.binary_path == str(FAKE_CLI_PATH)
        
        # Verify it works
        response = adapter.execute(prompt="Test", model="claude-3-opus")
        assert response.status == "success"
    
    def test_tilde_expansion_in_binary_path(self, tmp_path):
        """Test that ~ is expanded in binary_path."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        import shutil
        
        # Create a fake binary in user's home directory
        home_bin = Path.home() / ".local" / "bin"
        home_bin.mkdir(parents=True, exist_ok=True)
        fake_binary = home_bin / "fake_claude_test"
        
        # Copy fake CLI to test location
        shutil.copy(FAKE_CLI_PATH, fake_binary)
        fake_binary.chmod(0o755)
        
        try:
            config = {
                "binary_path": "~/.local/bin/fake_claude_test"
            }
            
            adapter = ClaudeCodeAdapter(config)
            
            # Should expand ~ to actual home directory
            assert adapter.binary_path == str(fake_binary)
            assert "~" not in adapter.binary_path
            
            # Verify it works
            response = adapter.execute(prompt="Test", model="claude-3-opus")
            assert response.status == "success"
        
        finally:
            # Cleanup
            if fake_binary.exists():
                fake_binary.unlink()


class TestClaudeCodeAdapterErrorScenarios:
    """Integration tests for various error scenarios."""
    
    @pytest.fixture
    def fake_cli_config(self):
        """Configuration pointing to fake CLI."""
        return {
            "binary_path": str(FAKE_CLI_PATH),
            "timeout": 30
        }
    
    def test_cli_returns_non_zero_exit_code(self, fake_cli_config):
        """Test handling when CLI returns non-zero exit code."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        # Trigger invalid-model error in fake CLI
        fake_cli_config["template"] = '{{binary}} --model {{model}} --prompt "{{prompt}}" --error invalid-model'
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        response = adapter.execute(
            prompt="Test",
            model="claude-3-opus"
        )
        
        assert response.status == "error"
        assert response.exit_code == 1
        assert len(response.stderr) > 0
    
    def test_empty_output_handling(self, fake_cli_config):
        """Test handling when CLI returns empty output."""
        from src.llm_service.adapters.claude_code_adapter import ClaudeCodeAdapter
        
        adapter = ClaudeCodeAdapter(fake_cli_config)
        
        # Even with empty prompt, fake CLI should return something
        response = adapter.execute(
            prompt="",
            model="claude-3-opus"
        )
        
        # Should still succeed (fake CLI generates a response)
        assert response.status == "success"
        assert response.exit_code == 0
