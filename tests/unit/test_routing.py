"""
Unit tests for routing engine.
"""

import pytest
import yaml
from pathlib import Path

from llm_service.routing import RoutingEngine, RoutingDecision, RoutingError
from llm_service.config.loader import load_configuration


@pytest.fixture
def basic_config(tmp_path):
    """Create basic test configuration."""
    agents_data = {
        'agents': {
            'test-agent': {
                'preferred_tool': 'test-tool',
                'preferred_model': 'expensive-model',
                'fallback_chain': ['backup-tool:expensive-model', 'test-tool:cheap-model'],
                'task_types': {
                    'simple': 'cheap-model',
                    'complex': 'expensive-model',
                }
            }
        }
    }
    tools_data = {
        'tools': {
            'test-tool': {
                'binary': 'test',
                'command_template': '{binary} {prompt_file} {model}',
                'models': ['expensive-model', 'cheap-model']
            },
            'backup-tool': {
                'binary': 'backup',
                'command_template': '{binary} {prompt_file} {model}',
                'models': ['expensive-model']
            }
        }
    }
    models_data = {
        'models': {
            'expensive-model': {
                'provider': 'test',
                'cost_per_1k_tokens': {'input': 0.03, 'output': 0.06},
                'context_window': 8000
            },
            'cheap-model': {
                'provider': 'test',
                'cost_per_1k_tokens': {'input': 0.001, 'output': 0.002},
                'context_window': 4000
            }
        }
    }
    policies_data = {
        'policies': {
            'default': {
                'daily_budget_usd': 10.0
            }
        },
        'cost_optimization': {
            'simple_task_threshold_tokens': 1500,
            'simple_task_models': ['cheap-model'],
            'complex_task_models': ['expensive-model']
        }
    }
    
    (tmp_path / "agents.yaml").write_text(yaml.dump(agents_data))
    (tmp_path / "tools.yaml").write_text(yaml.dump(tools_data))
    (tmp_path / "models.yaml").write_text(yaml.dump(models_data))
    (tmp_path / "policies.yaml").write_text(yaml.dump(policies_data))
    
    return load_configuration(str(tmp_path))


def test_routing_engine_basic_routing(basic_config):
    """Test basic routing with agent preferences."""
    engine = RoutingEngine(
        basic_config['agents'],
        basic_config['tools'],
        basic_config['models'],
        basic_config['policies'],
    )
    
    decision = engine.route('test-agent')
    
    assert decision.tool_name == 'test-tool'
    assert decision.model_name == 'expensive-model'
    assert not decision.fallback_used
    assert 'preferred configuration' in decision.reason


def test_routing_engine_task_type_override(basic_config):
    """Test task type override for model selection."""
    engine = RoutingEngine(
        basic_config['agents'],
        basic_config['tools'],
        basic_config['models'],
        basic_config['policies'],
    )
    
    decision = engine.route('test-agent', task_type='simple')
    
    assert decision.tool_name == 'test-tool'
    assert decision.model_name == 'cheap-model'
    assert 'Task type' in decision.reason


def test_routing_engine_cost_optimization(basic_config):
    """Test cost optimization for small prompts."""
    engine = RoutingEngine(
        basic_config['agents'],
        basic_config['tools'],
        basic_config['models'],
        basic_config['policies'],
    )
    
    # Small prompt should trigger cost optimization
    decision = engine.route('test-agent', prompt_size_tokens=1000)
    
    assert decision.model_name == 'cheap-model'
    assert 'cost optimization' in decision.reason


def test_routing_engine_no_cost_optimization_large_prompt(basic_config):
    """Test that large prompts don't trigger cost optimization."""
    engine = RoutingEngine(
        basic_config['agents'],
        basic_config['tools'],
        basic_config['models'],
        basic_config['policies'],
    )
    
    # Large prompt should not trigger optimization
    decision = engine.route('test-agent', prompt_size_tokens=5000)
    
    assert decision.model_name == 'expensive-model'
    assert 'cost optimization' not in decision.reason


def test_routing_engine_agent_not_found(basic_config):
    """Test error when agent doesn't exist."""
    engine = RoutingEngine(
        basic_config['agents'],
        basic_config['tools'],
        basic_config['models'],
        basic_config['policies'],
    )
    
    with pytest.raises(RoutingError, match="not found"):
        engine.route('nonexistent-agent')


def test_routing_engine_get_model_cost(basic_config):
    """Test getting model cost information."""
    engine = RoutingEngine(
        basic_config['agents'],
        basic_config['tools'],
        basic_config['models'],
        basic_config['policies'],
    )
    
    cost = engine.get_model_cost('expensive-model')
    assert cost['input'] == 0.03
    assert cost['output'] == 0.06
    
    cost = engine.get_model_cost('cheap-model')
    assert cost['input'] == 0.001
    assert cost['output'] == 0.002


def test_routing_engine_list_agent_capabilities(basic_config):
    """Test listing agent capabilities."""
    engine = RoutingEngine(
        basic_config['agents'],
        basic_config['tools'],
        basic_config['models'],
        basic_config['policies'],
    )
    
    caps = engine.list_agent_capabilities('test-agent')
    
    assert caps['agent_name'] == 'test-agent'
    assert caps['preferred_tool'] == 'test-tool'
    assert caps['preferred_model'] == 'expensive-model'
    assert len(caps['fallback_chain']) == 2
    assert 'simple' in caps['task_types']


def test_routing_decision_dataclass():
    """Test RoutingDecision dataclass."""
    decision = RoutingDecision(
        tool_name='test-tool',
        model_name='test-model',
        reason='test reason',
        fallback_used=True,
        original_tool='original-tool',
        original_model='original-model',
    )
    
    assert decision.tool_name == 'test-tool'
    assert decision.model_name == 'test-model'
    assert decision.reason == 'test reason'
    assert decision.fallback_used is True
    assert decision.original_tool == 'original-tool'
    assert decision.original_model == 'original-model'
