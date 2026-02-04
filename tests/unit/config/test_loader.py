"""
Unit tests for configuration loader.
"""

import pytest
import tempfile
from pathlib import Path
import yaml

from llm_service.config.loader import ConfigurationLoader, ConfigurationError, load_configuration
from llm_service.config.schemas import AgentsSchema, ToolsSchema, ModelsSchema, PoliciesSchema


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
    
    def test_load_agents_valid(self, tmp_path):
        """Test loading valid agents configuration."""
        agents_file = tmp_path / "agents.yaml"
        agents_data = {
            'agents': {
                'test-agent': {
                    'preferred_tool': 'test-tool',
                    'preferred_model': 'test-model',
                    'fallback_chain': ['test-tool:test-model']
                }
            }
        }
        agents_file.write_text(yaml.dump(agents_data))
        
        loader = ConfigurationLoader(tmp_path)
        agents = loader.load_agents()
        assert isinstance(agents, AgentsSchema)
        assert 'test-agent' in agents.agents
    
    def test_load_all_valid(self, tmp_path):
        """Test loading all configurations with valid cross-references."""
        # Create valid configuration files
        agents_data = {
            'agents': {
                'test-agent': {
                    'preferred_tool': 'test-tool',
                    'preferred_model': 'test-model',
                    'fallback_chain': ['test-tool:test-model']
                }
            }
        }
        tools_data = {
            'tools': {
                'test-tool': {
                    'binary': 'test',
                    'command_template': '{binary} {prompt_file} {model}',
                    'models': ['test-model']
                }
            }
        }
        models_data = {
            'models': {
                'test-model': {
                    'provider': 'test',
                    'cost_per_1k_tokens': {'input': 0.01, 'output': 0.03},
                    'context_window': 8000
                }
            }
        }
        policies_data = {
            'policies': {
                'default': {
                    'daily_budget_usd': 10.0
                }
            }
        }
        
        (tmp_path / "agents.yaml").write_text(yaml.dump(agents_data))
        (tmp_path / "tools.yaml").write_text(yaml.dump(tools_data))
        (tmp_path / "models.yaml").write_text(yaml.dump(models_data))
        (tmp_path / "policies.yaml").write_text(yaml.dump(policies_data))
        
        loader = ConfigurationLoader(tmp_path)
        config = loader.load_all()
        
        assert 'agents' in config
        assert 'tools' in config
        assert 'models' in config
        assert 'policies' in config
        assert isinstance(config['agents'], AgentsSchema)


def test_load_configuration_convenience_function(tmp_path):
    """Test the convenience function for loading configuration."""
    # Create minimal valid configuration
    agents_data = {'agents': {'test-agent': {'preferred_tool': 'test-tool', 'preferred_model': 'test-model', 'fallback_chain': []}}}
    tools_data = {'tools': {'test-tool': {'binary': 'test', 'command_template': '{binary} {prompt_file} {model}', 'models': ['test-model']}}}
    models_data = {'models': {'test-model': {'provider': 'test', 'cost_per_1k_tokens': {'input': 0.01, 'output': 0.03}, 'context_window': 8000}}}
    policies_data = {'policies': {'default': {'daily_budget_usd': 10.0}}}
    
    (tmp_path / "agents.yaml").write_text(yaml.dump(agents_data))
    (tmp_path / "tools.yaml").write_text(yaml.dump(tools_data))
    (tmp_path / "models.yaml").write_text(yaml.dump(models_data))
    (tmp_path / "policies.yaml").write_text(yaml.dump(policies_data))
    
    config = load_configuration(str(tmp_path))
    assert 'agents' in config
