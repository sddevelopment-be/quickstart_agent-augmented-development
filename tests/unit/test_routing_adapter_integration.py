"""
Unit tests for routing engine integration with GenericYAMLAdapter.

Tests the adapter factory and tool registration following TDD approach (Directive 017).
Ensures routing engine instantiates and manages GenericYAMLAdapter instances.
"""

import pytest
import os
from unittest.mock import patch, Mock
from src.llm_service.routing import RoutingEngine
from src.llm_service.config.schemas import AgentsSchema, ToolsSchema, ModelsSchema, PoliciesSchema


@pytest.fixture
def test_config():
    """Create test configuration with GenericYAMLAdapter-compatible tools."""
    agents_data = {
        "agents": {
            "test-agent": {
                "preferred_tool": "claude-code",
                "preferred_model": "claude-3-opus",
                "fallback_chain": [],
                "task_types": {}
            }
        }
    }
    
    tools_data = {
        "tools": {
            "claude-code": {
                "binary": "claude-code",
                "command_template": "{{binary}} --model {{model}} --prompt {{prompt}}",
                "models": ["claude-3-opus", "claude-3.5-sonnet"]
            },
            "codex": {
                "binary": "openai",
                "command_template": "{{binary}} api completions.create -m {{model}} -p {{prompt}}",
                "models": ["gpt-4", "gpt-3.5-turbo"]
            }
        }
    }
    
    models_data = {
        "models": {
            "claude-3-opus": {
                "provider": "anthropic",
                "cost_per_1k_tokens": {"input": 0.015, "output": 0.075},
                "context_window": 200000
            },
            "claude-3.5-sonnet": {
                "provider": "anthropic",
                "cost_per_1k_tokens": {"input": 0.003, "output": 0.015},
                "context_window": 200000
            },
            "gpt-4": {
                "provider": "openai",
                "cost_per_1k_tokens": {"input": 0.03, "output": 0.06},
                "context_window": 8192
            },
            "gpt-3.5-turbo": {
                "provider": "openai",
                "cost_per_1k_tokens": {"input": 0.0015, "output": 0.002},
                "context_window": 4096
            }
        }
    }
    
    policies_data = {
        "policies": {
            "default": {
                "daily_budget_usd": 10.0
            }
        }
    }
    
    return {
        "agents": AgentsSchema(**agents_data),
        "tools": ToolsSchema(**tools_data),
        "models": ModelsSchema(**models_data),
        "policies": PoliciesSchema(**policies_data)
    }


class TestRoutingEngineAdapterFactory:
    """Test adapter factory functionality in routing engine."""
    
    def test_routing_engine_creates_adapter_registry(self, test_config):
        """Test routing engine creates adapter registry from tools config."""
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            # Routing engine should have adapter registry
            assert hasattr(engine, "adapters")
            assert isinstance(engine.adapters, dict)
    
    def test_routing_engine_creates_adapter_for_each_tool(self, test_config):
        """Test routing engine creates GenericYAMLAdapter for each configured tool."""
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            # Should have adapter for each tool
            assert "claude-code" in engine.adapters
            assert "codex" in engine.adapters
    
    def test_routing_engine_uses_generic_yaml_adapter(self, test_config):
        """Test routing engine uses GenericYAMLAdapter class."""
        from src.llm_service.adapters.generic_adapter import GenericYAMLAdapter
        
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            # All adapters should be GenericYAMLAdapter instances
            for tool_name, adapter in engine.adapters.items():
                assert isinstance(adapter, GenericYAMLAdapter)
                assert adapter.get_tool_name() == tool_name
    
    def test_routing_engine_passes_config_to_adapter(self, test_config):
        """Test routing engine passes tool config to adapter constructor."""
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            # Adapter should have config from tools.yaml
            claude_adapter = engine.adapters["claude-code"]
            assert claude_adapter.tool_config["binary"] == "claude-code"
            assert "claude-3-opus" in claude_adapter.tool_config["models"]


class TestRoutingEngineGetAdapter:
    """Test getting adapters from routing engine."""
    
    def test_get_adapter_returns_correct_adapter(self, test_config):
        """Test get_adapter() returns the correct adapter instance."""
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            adapter = engine.get_adapter("claude-code")
            
            assert adapter is not None
            assert adapter.get_tool_name() == "claude-code"
    
    def test_get_adapter_raises_error_for_unknown_tool(self, test_config):
        """Test get_adapter() raises error for unknown tool."""
        from src.llm_service.routing import RoutingError
        
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            with pytest.raises(RoutingError) as exc_info:
                engine.get_adapter("unknown-tool")
            
            assert "unknown-tool" in str(exc_info.value).lower()


class TestRoutingEngineExecute:
    """Test routing engine execute method."""
    
    def test_routing_engine_execute_uses_correct_adapter(self, test_config):
        """Test execute() uses adapter for routed tool."""
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            # Mock adapter execution
            mock_result = ExecutionResult(
                exit_code=0,
                stdout="Success output",
                stderr="",
                duration_seconds=1.5,
                command=[],
                timed_out=False
            )
            
            with patch.object(engine.adapters["claude-code"].subprocess_wrapper, "execute", return_value=mock_result):
                response = engine.execute(
                    agent_name="test-agent",
                    prompt="Write code",
                    model="claude-3-opus"
                )
                
                assert response.status == "success"
                assert response.tool_name == "claude-code"
    
    def test_routing_engine_execute_with_routing_decision(self, test_config):
        """Test execute() routes correctly and uses selected tool."""
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            mock_result = ExecutionResult(
                exit_code=0,
                stdout="Result",
                stderr="",
                duration_seconds=1.0,
                command=[],
                timed_out=False
            )
            
            with patch.object(engine.adapters["claude-code"].subprocess_wrapper, "execute", return_value=mock_result):
                # Execute should: 1) route to find tool, 2) get adapter, 3) execute
                response = engine.execute(
                    agent_name="test-agent",
                    prompt="test prompt"
                )
                
                # Should use agent's preferred tool (claude-code) and model (claude-3-opus)
                assert response.status == "success"
                assert response.tool_name == "claude-code"


class TestAddToolViaYAML:
    """Test adding new tool via YAML configuration without code changes."""
    
    def test_add_new_tool_gemini_via_yaml(self):
        """Demonstrate adding Google Gemini tool via YAML only."""
        from src.llm_service.adapters.subprocess_wrapper import ExecutionResult
        
        # Add Gemini tool to configuration
        tools_data = {
            "tools": {
                "gemini": {
                    "binary": "google-ai",
                    "command_template": "{{binary}} generate --model {{model}} --prompt {{prompt}}",
                    "models": ["gemini-pro", "gemini-ultra"]
                }
            }
        }
        
        agents_data = {
            "agents": {
                "test-agent": {
                    "preferred_tool": "gemini",
                    "preferred_model": "gemini-pro",
                    "fallback_chain": [],
                    "task_types": {}
                }
            }
        }
        
        models_data = {
            "models": {
                "gemini-pro": {
                    "provider": "google",
                    "cost_per_1k_tokens": {"input": 0.0005, "output": 0.0015},
                    "context_window": 30720
                },
                "gemini-ultra": {
                    "provider": "google",
                    "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
                    "context_window": 30720
                }
            }
        }
        
        policies_data = {
            "policies": {
                "default": {
                    "daily_budget_usd": 10.0
                }
            }
        }
        
        config = {
            "agents": AgentsSchema(**agents_data),
            "tools": ToolsSchema(**tools_data),
            "models": ModelsSchema(**models_data),
            "policies": PoliciesSchema(**policies_data)
        }
        
        with patch("shutil.which", return_value="/usr/bin/google-ai"):
            engine = RoutingEngine(
                config["agents"],
                config["tools"],
                config["models"],
                config["policies"]
            )
            
            # Verify Gemini adapter was created
            assert "gemini" in engine.adapters
            gemini_adapter = engine.adapters["gemini"]
            assert gemini_adapter.get_tool_name() == "gemini"
            
            # Verify adapter can execute
            mock_result = ExecutionResult(
                exit_code=0,
                stdout="Gemini response",
                stderr="",
                duration_seconds=1.0,
                command=[],
                timed_out=False
            )
            
            with patch.object(gemini_adapter.subprocess_wrapper, "execute", return_value=mock_result):
                response = gemini_adapter.execute(prompt="test", model="gemini-pro")
                
                assert response.status == "success"
                assert response.tool_name == "gemini"
                
            # This proves we can add ANY tool via YAML configuration alone!
            # No code changes needed - just update tools.yaml and models.yaml


class TestBackwardCompatibility:
    """Test that routing engine changes don't break existing functionality."""
    
    def test_routing_logic_still_works(self, test_config):
        """Test existing routing logic (route method) still works."""
        with patch("shutil.which", return_value="/usr/bin/mock"):
            engine = RoutingEngine(
                test_config["agents"],
                test_config["tools"],
                test_config["models"],
                test_config["policies"]
            )
            
            # Existing route() method should still work
            decision = engine.route("test-agent")
            
            assert decision.tool_name == "claude-code"
            assert decision.model_name == "claude-3-opus"
            assert not decision.fallback_used
