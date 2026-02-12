"""
Unit tests for configuration loader.
"""

from pathlib import Path

import pytest
import yaml

from llm_service.config.loader import (
    ConfigurationError,
    ConfigurationLoader,
    load_configuration,
)
from llm_service.config.schemas import (
    AgentsSchema,
    ModelsSchema,
    PoliciesSchema,
    ToolsSchema,
)


class TestConfigurationLoader:
    """Test ConfigurationLoader class."""

    def test_init_with_valid_directory(self, tmp_path):
        """Test initialization with valid directory."""
        loader = ConfigurationLoader(tmp_path)
        assert loader.config_dir == tmp_path

    def test_init_with_nonexistent_directory(self):
        """Test initialization with nonexistent directory raises error."""
        with pytest.raises(ConfigurationError, match="does not exist"):
            ConfigurationLoader(Path("/nonexistent/path"))

    def test_init_with_file_instead_of_directory(self, tmp_path):
        """Test initialization with file instead of directory raises error."""
        test_file = tmp_path / "testfile.txt"
        test_file.write_text("test")

        with pytest.raises(ConfigurationError, match="not a directory"):
            ConfigurationLoader(test_file)

    def test_load_agents_valid(self, tmp_path):
        """Test loading valid agents configuration."""
        agents_file = tmp_path / "agents.yaml"
        agents_data = {
            "agents": {
                "test-agent": {
                    "preferred_tool": "test-tool",
                    "preferred_model": "test-model",
                    "fallback_chain": ["test-tool:test-model"],
                }
            }
        }
        agents_file.write_text(yaml.dump(agents_data))

        loader = ConfigurationLoader(tmp_path)
        agents = loader.load_agents()
        assert isinstance(agents, AgentsSchema)
        assert "test-agent" in agents.agents

    def test_load_agents_yml_extension(self, tmp_path):
        """Test loading agents config with .yml extension."""
        agents_file = tmp_path / "agents.yml"
        agents_data = {
            "agents": {
                "test-agent": {
                    "preferred_tool": "test-tool",
                    "preferred_model": "test-model",
                }
            }
        }
        agents_file.write_text(yaml.dump(agents_data))

        loader = ConfigurationLoader(tmp_path)
        agents = loader.load_agents()
        assert "test-agent" in agents.agents

    def test_load_agents_not_found(self, tmp_path):
        """Test loading agents when file doesn't exist."""
        loader = ConfigurationLoader(tmp_path)

        with pytest.raises(ConfigurationError, match="agents.yaml not found"):
            loader.load_agents()

    def test_load_agents_invalid_yaml_syntax(self, tmp_path):
        """Test loading agents with invalid YAML syntax."""
        agents_file = tmp_path / "agents.yaml"
        agents_file.write_text("agents:\n  test-agent:\n    invalid: [unclosed bracket")

        loader = ConfigurationLoader(tmp_path)
        with pytest.raises(ConfigurationError, match="Invalid YAML"):
            loader.load_agents()

    def test_load_agents_empty_file(self, tmp_path):
        """Test loading empty agents file."""
        agents_file = tmp_path / "agents.yaml"
        agents_file.write_text("")

        loader = ConfigurationLoader(tmp_path)
        with pytest.raises(ConfigurationError, match="Empty configuration file"):
            loader.load_agents()

    def test_load_agents_invalid_schema(self, tmp_path):
        """Test loading agents with invalid schema."""
        agents_file = tmp_path / "agents.yaml"
        agents_data = {
            "agents": {
                "test-agent": {
                    # Missing required fields
                    "invalid_field": "value"
                }
            }
        }
        agents_file.write_text(yaml.dump(agents_data))

        loader = ConfigurationLoader(tmp_path)
        with pytest.raises(ConfigurationError, match="Invalid agents configuration"):
            loader.load_agents()

    def test_load_tools_valid(self, tmp_path):
        """Test loading valid tools configuration."""
        tools_file = tmp_path / "tools.yaml"
        tools_data = {
            "tools": {
                "test-tool": {
                    "binary": "test",
                    "command_template": "{binary} {prompt_file} {model}",
                    "models": ["test-model"],
                }
            }
        }
        tools_file.write_text(yaml.dump(tools_data))

        loader = ConfigurationLoader(tmp_path)
        tools = loader.load_tools()
        assert isinstance(tools, ToolsSchema)
        assert "test-tool" in tools.tools

    def test_load_tools_not_found(self, tmp_path):
        """Test loading tools when file doesn't exist."""
        loader = ConfigurationLoader(tmp_path)

        with pytest.raises(ConfigurationError, match="tools.yaml not found"):
            loader.load_tools()

    def test_load_models_valid(self, tmp_path):
        """Test loading valid models configuration."""
        models_file = tmp_path / "models.yaml"
        models_data = {
            "models": {
                "test-model": {
                    "provider": "test",
                    "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
                    "context_window": 8000,
                }
            }
        }
        models_file.write_text(yaml.dump(models_data))

        loader = ConfigurationLoader(tmp_path)
        models = loader.load_models()
        assert isinstance(models, ModelsSchema)
        assert "test-model" in models.models

    def test_load_models_not_found(self, tmp_path):
        """Test loading models when file doesn't exist."""
        loader = ConfigurationLoader(tmp_path)

        with pytest.raises(ConfigurationError, match="models.yaml not found"):
            loader.load_models()

    def test_load_policies_valid(self, tmp_path):
        """Test loading valid policies configuration."""
        policies_file = tmp_path / "policies.yaml"
        policies_data = {"policies": {"default": {"daily_budget_usd": 10.0}}}
        policies_file.write_text(yaml.dump(policies_data))

        loader = ConfigurationLoader(tmp_path)
        policies = loader.load_policies()
        assert isinstance(policies, PoliciesSchema)
        assert "default" in policies.policies

    def test_load_policies_not_found(self, tmp_path):
        """Test loading policies when file doesn't exist."""
        loader = ConfigurationLoader(tmp_path)

        with pytest.raises(ConfigurationError, match="policies.yaml not found"):
            loader.load_policies()

    def test_load_all_valid(self, tmp_path):
        """Test loading all configurations with valid cross-references."""
        # Create valid configuration files
        agents_data = {
            "agents": {
                "test-agent": {
                    "preferred_tool": "test-tool",
                    "preferred_model": "test-model",
                    "fallback_chain": ["test-tool:test-model"],
                }
            }
        }
        tools_data = {
            "tools": {
                "test-tool": {
                    "binary": "test",
                    "command_template": "{binary} {prompt_file} {model}",
                    "models": ["test-model"],
                }
            }
        }
        models_data = {
            "models": {
                "test-model": {
                    "provider": "test",
                    "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
                    "context_window": 8000,
                }
            }
        }
        policies_data = {"policies": {"default": {"daily_budget_usd": 10.0}}}

        (tmp_path / "agents.yaml").write_text(yaml.dump(agents_data))
        (tmp_path / "tools.yaml").write_text(yaml.dump(tools_data))
        (tmp_path / "models.yaml").write_text(yaml.dump(models_data))
        (tmp_path / "policies.yaml").write_text(yaml.dump(policies_data))

        loader = ConfigurationLoader(tmp_path)
        config = loader.load_all()

        assert "agents" in config
        assert "tools" in config
        assert "models" in config
        assert "policies" in config
        assert isinstance(config["agents"], AgentsSchema)

    def test_load_all_cross_reference_validation_failure(self, tmp_path):
        """Test that cross-reference validation failures are caught."""
        # Create configs with invalid cross-references
        agents_data = {
            "agents": {
                "test-agent": {
                    "preferred_tool": "nonexistent-tool",  # Invalid reference
                    "preferred_model": "test-model",
                }
            }
        }
        tools_data = {
            "tools": {
                "test-tool": {
                    "binary": "test",
                    "command_template": "{binary} {prompt_file} {model}",
                    "models": ["test-model"],
                }
            }
        }
        models_data = {
            "models": {
                "test-model": {
                    "provider": "test",
                    "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
                    "context_window": 8000,
                }
            }
        }
        policies_data = {"policies": {"default": {"daily_budget_usd": 10.0}}}

        (tmp_path / "agents.yaml").write_text(yaml.dump(agents_data))
        (tmp_path / "tools.yaml").write_text(yaml.dump(tools_data))
        (tmp_path / "models.yaml").write_text(yaml.dump(models_data))
        (tmp_path / "policies.yaml").write_text(yaml.dump(policies_data))

        loader = ConfigurationLoader(tmp_path)
        with pytest.raises(
            ConfigurationError, match="cross-reference validation failed"
        ):
            loader.load_all()

    def test_load_yaml_file_io_error(self, tmp_path):
        """Test handling of file I/O errors."""
        # Create a file and make it unreadable (on Unix-like systems)
        test_file = tmp_path / "test.yaml"
        test_file.write_text("test: data")
        test_file.chmod(0o000)  # No permissions

        loader = ConfigurationLoader(tmp_path)
        try:
            with pytest.raises(ConfigurationError, match="Cannot read file"):
                loader._load_yaml_file(test_file)
        finally:
            test_file.chmod(0o644)  # Restore permissions for cleanup


def test_load_configuration_convenience_function(tmp_path):
    """Test the convenience function for loading configuration."""
    # Create minimal valid configuration
    agents_data = {
        "agents": {
            "test-agent": {
                "preferred_tool": "test-tool",
                "preferred_model": "test-model",
                "fallback_chain": [],
            }
        }
    }
    tools_data = {
        "tools": {
            "test-tool": {
                "binary": "test",
                "command_template": "{binary} {prompt_file} {model}",
                "models": ["test-model"],
            }
        }
    }
    models_data = {
        "models": {
            "test-model": {
                "provider": "test",
                "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
                "context_window": 8000,
            }
        }
    }
    policies_data = {"policies": {"default": {"daily_budget_usd": 10.0}}}

    (tmp_path / "agents.yaml").write_text(yaml.dump(agents_data))
    (tmp_path / "tools.yaml").write_text(yaml.dump(tools_data))
    (tmp_path / "models.yaml").write_text(yaml.dump(models_data))
    (tmp_path / "policies.yaml").write_text(yaml.dump(policies_data))

    config = load_configuration(str(tmp_path))
    assert "agents" in config
