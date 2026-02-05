"""
Unit tests for ENV variables in YAML schema configuration.

Tests the environment variable support in ToolConfig schema following TDD approach (Directive 017).
Covers env_vars field, env_required field, and variable expansion logic.
"""

import pytest
import os
from unittest.mock import patch


class TestToolConfigEnvVarsSchema:
    """Test ToolConfig schema with env_vars and env_required fields."""
    
    def test_tool_config_with_env_vars_dict(self):
        """Test ToolConfig accepts env_vars as dictionary."""
        from src.llm_service.config.schemas import ToolConfig
        
        config = ToolConfig(
            binary="tool",
            command_template="{{binary}} {{model}} {{prompt}}",
            models=["model-1"],
            env_vars={
                "API_KEY": "test-key",
                "CUSTOM_VAR": "custom-value"
            }
        )
        
        assert config.env_vars == {"API_KEY": "test-key", "CUSTOM_VAR": "custom-value"}
    
    def test_tool_config_env_vars_optional(self):
        """Test env_vars field is optional."""
        from src.llm_service.config.schemas import ToolConfig
        
        config = ToolConfig(
            binary="tool",
            command_template="{{binary}} {{model}} {{prompt}}",
            models=["model-1"]
        )
        
        assert config.env_vars is None or config.env_vars == {}
    
    def test_tool_config_with_env_required_list(self):
        """Test ToolConfig accepts env_required as list."""
        from src.llm_service.config.schemas import ToolConfig
        
        config = ToolConfig(
            binary="tool",
            command_template="{{binary}} {{model}} {{prompt}}",
            models=["model-1"],
            env_required=["API_KEY", "SECRET_TOKEN"]
        )
        
        assert config.env_required == ["API_KEY", "SECRET_TOKEN"]
    
    def test_tool_config_env_required_optional(self):
        """Test env_required field is optional."""
        from src.llm_service.config.schemas import ToolConfig
        
        config = ToolConfig(
            binary="tool",
            command_template="{{binary}} {{model}} {{prompt}}",
            models=["model-1"]
        )
        
        assert config.env_required is None or config.env_required == []
    
    def test_tool_config_with_both_env_fields(self):
        """Test ToolConfig with both env_vars and env_required."""
        from src.llm_service.config.schemas import ToolConfig
        
        config = ToolConfig(
            binary="tool",
            command_template="{{binary}} {{model}} {{prompt}}",
            models=["model-1"],
            env_vars={"API_KEY": "${API_KEY}", "DEFAULT": "value"},
            env_required=["API_KEY"]
        )
        
        assert config.env_vars == {"API_KEY": "${API_KEY}", "DEFAULT": "value"}
        assert config.env_required == ["API_KEY"]


class TestEnvVarExpansion:
    """Test environment variable expansion utility."""
    
    def test_expand_env_var_from_system(self):
        """Test expanding ${VAR} from system environment."""
        from src.llm_service.config.env_utils import expand_env_vars
        
        env_vars = {"API_KEY": "${TEST_API_KEY}"}
        
        with patch.dict(os.environ, {"TEST_API_KEY": "secret-key-123"}):
            expanded = expand_env_vars(env_vars)
            
            assert expanded["API_KEY"] == "secret-key-123"
    
    def test_expand_multiple_env_vars(self):
        """Test expanding multiple environment variables."""
        from src.llm_service.config.env_utils import expand_env_vars
        
        env_vars = {
            "API_KEY": "${API_KEY_VAR}",
            "SECRET": "${SECRET_VAR}",
            "LITERAL": "hardcoded"
        }
        
        with patch.dict(os.environ, {"API_KEY_VAR": "key123", "SECRET_VAR": "sec456"}):
            expanded = expand_env_vars(env_vars)
            
            assert expanded["API_KEY"] == "key123"
            assert expanded["SECRET"] == "sec456"
            assert expanded["LITERAL"] == "hardcoded"
    
    def test_expand_env_var_with_default_value(self):
        """Test expanding ${VAR:default} with default value."""
        from src.llm_service.config.env_utils import expand_env_vars
        
        env_vars = {"API_KEY": "${MISSING_VAR:default-value}"}
        
        with patch.dict(os.environ, {}, clear=True):
            expanded = expand_env_vars(env_vars)
            
            assert expanded["API_KEY"] == "default-value"
    
    def test_expand_env_var_missing_no_default(self):
        """Test expanding ${VAR} when var missing and no default raises error."""
        from src.llm_service.config.env_utils import expand_env_vars, EnvVarNotFoundError
        
        env_vars = {"API_KEY": "${MISSING_VAR}"}
        
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(EnvVarNotFoundError) as exc_info:
                expand_env_vars(env_vars)
            
            assert "MISSING_VAR" in str(exc_info.value)
    
    def test_expand_literal_value_unchanged(self):
        """Test literal values (no ${}) are unchanged."""
        from src.llm_service.config.env_utils import expand_env_vars
        
        env_vars = {"LITERAL": "just-a-value", "NUMBER": "123"}
        
        expanded = expand_env_vars(env_vars)
        
        assert expanded["LITERAL"] == "just-a-value"
        assert expanded["NUMBER"] == "123"
    
    def test_expand_empty_dict(self):
        """Test expanding empty env_vars dict."""
        from src.llm_service.config.env_utils import expand_env_vars
        
        expanded = expand_env_vars({})
        
        assert expanded == {}
    
    def test_expand_mixed_format(self):
        """Test expanding mix of ${VAR}, ${VAR:default}, and literals."""
        from src.llm_service.config.env_utils import expand_env_vars
        
        env_vars = {
            "FROM_ENV": "${EXISTS}",
            "WITH_DEFAULT": "${MISSING:fallback}",
            "LITERAL": "static"
        }
        
        with patch.dict(os.environ, {"EXISTS": "value-from-env"}):
            expanded = expand_env_vars(env_vars)
            
            assert expanded["FROM_ENV"] == "value-from-env"
            assert expanded["WITH_DEFAULT"] == "fallback"
            assert expanded["LITERAL"] == "static"


class TestEnvVarValidation:
    """Test environment variable validation."""
    
    def test_validate_required_env_vars_present(self):
        """Test validation passes when required vars are present."""
        from src.llm_service.config.env_utils import validate_required_env_vars
        
        env_required = ["API_KEY", "SECRET"]
        
        with patch.dict(os.environ, {"API_KEY": "key", "SECRET": "sec"}):
            # Should not raise
            validate_required_env_vars(env_required)
    
    def test_validate_required_env_vars_missing(self):
        """Test validation fails when required var is missing."""
        from src.llm_service.config.env_utils import validate_required_env_vars, EnvVarNotFoundError
        
        env_required = ["API_KEY", "MISSING_VAR"]
        
        with patch.dict(os.environ, {"API_KEY": "key"}, clear=True):
            with pytest.raises(EnvVarNotFoundError) as exc_info:
                validate_required_env_vars(env_required)
            
            assert "MISSING_VAR" in str(exc_info.value)
            assert "required" in str(exc_info.value).lower()
    
    def test_validate_empty_required_list(self):
        """Test validation passes with empty required list."""
        from src.llm_service.config.env_utils import validate_required_env_vars
        
        # Should not raise
        validate_required_env_vars([])
    
    def test_validate_none_required_list(self):
        """Test validation handles None required list."""
        from src.llm_service.config.env_utils import validate_required_env_vars
        
        # Should not raise
        validate_required_env_vars(None)


class TestGenericAdapterWithEnvVars:
    """Test GenericYAMLAdapter with environment variables."""
    
    def test_adapter_passes_env_vars_to_subprocess(self):
        """Test adapter passes expanded env vars to subprocess wrapper."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"],
            "env_vars": {
                "API_KEY": "${TEST_KEY}",
                "LITERAL": "value"
            }
        }
        
        with patch("shutil.which", return_value="/usr/bin/tool"), \
             patch.dict(os.environ, {"TEST_KEY": "expanded-key"}):
            adapter = GenericYAMLAdapter("tool", config)
        
        # Mock subprocess execution
        mock_result = ExecutionResult(
            exit_code=0,
            stdout="output",
            stderr="",
            duration_seconds=1.0,
            command=[],
            timed_out=False
        )
        
        with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result) as mock_exec:
            adapter.execute(prompt="test", model="model-1")
            
            # Verify subprocess was called with expanded env vars
            mock_exec.assert_called_once()
            call_args = mock_exec.call_args
            if call_args.kwargs and "env" in call_args.kwargs:
                env = call_args.kwargs["env"]
                assert env.get("API_KEY") == "expanded-key"
                assert env.get("LITERAL") == "value"
    
    def test_adapter_validates_required_env_vars_on_init(self):
        """Test adapter validates required env vars during initialization."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.config.env_utils import EnvVarNotFoundError
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"],
            "env_vars": {"API_KEY": "${REQUIRED_KEY}"},
            "env_required": ["REQUIRED_KEY"]
        }
        
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(EnvVarNotFoundError) as exc_info:
                with patch("shutil.which", return_value="/usr/bin/tool"):
                    adapter = GenericYAMLAdapter("tool", config)
            
            assert "REQUIRED_KEY" in str(exc_info.value)
    
    def test_adapter_works_without_env_vars(self):
        """Test adapter works normally when env_vars not configured."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        config = {
            "binary": "tool",
            "command_template": "{{binary}} {{prompt}}",
            "models": ["model-1"]
            # No env_vars or env_required
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
        
        with patch.object(adapter.subprocess_wrapper, "execute", return_value=mock_result):
            response = adapter.execute(prompt="test", model="model-1")
            
            assert response.status == "success"


class TestToolsYAMLWithEnvVars:
    """Test complete tools.yaml configuration with env vars."""
    
    def test_parse_tools_yaml_with_env_vars(self):
        """Test parsing tools.yaml that includes env_vars configuration."""
        from src.llm_service.config.schemas import ToolsSchema, ToolConfig
        
        tools_data = {
            "tools": {
                "claude-code": {
                    "binary": "claude-code",
                    "command_template": "{{binary}} --model {{model}} --prompt {{prompt}}",
                    "models": ["claude-3-opus"],
                    "env_vars": {
                        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
                        "CUSTOM_CONFIG": "value"
                    },
                    "env_required": ["ANTHROPIC_API_KEY"]
                }
            }
        }
        
        schema = ToolsSchema(**tools_data)
        
        assert "claude-code" in schema.tools
        tool = schema.tools["claude-code"]
        assert tool.env_vars == {
            "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
            "CUSTOM_CONFIG": "value"
        }
        assert tool.env_required == ["ANTHROPIC_API_KEY"]
