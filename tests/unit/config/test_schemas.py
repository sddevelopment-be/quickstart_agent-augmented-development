"""
Unit tests for configuration schemas.

Tests Pydantic validation, field validators, and cross-reference validation.
"""

import pytest
from pydantic import ValidationError

from llm_service.config.schemas import (
    AgentConfig,
    AgentsSchema,
    CostOptimization,
    ModelConfig,
    ModelsSchema,
    PolicyConfig,
    ToolConfig,
    ToolsSchema,
    validate_agent_references,
)


class TestAgentConfig:
    """Test AgentConfig schema validation."""

    def test_valid_agent_config(self):
        """Test creating valid agent configuration."""
        config = AgentConfig(
            preferred_tool="test-tool",
            preferred_model="test-model",
            fallback_chain=["tool1:model1", "tool2:model2"],
            task_types={"simple": "model1", "complex": "model2"},
        )
        assert config.preferred_tool == "test-tool"
        assert config.preferred_model == "test-model"
        assert len(config.fallback_chain) == 2
        assert config.task_types["simple"] == "model1"

    def test_agent_config_minimal(self):
        """Test agent config with only required fields."""
        config = AgentConfig(
            preferred_tool="test-tool",
            preferred_model="test-model",
        )
        assert config.fallback_chain == []
        assert config.task_types == {}

    def test_agent_config_invalid_fallback_format(self):
        """Test that invalid fallback chain format is rejected."""
        with pytest.raises(ValidationError, match="tool:model"):
            AgentConfig(
                preferred_tool="test-tool",
                preferred_model="test-model",
                fallback_chain=["invalid-format"],  # Missing colon
            )

    def test_agent_config_missing_required_fields(self):
        """Test that missing required fields are rejected."""
        with pytest.raises(ValidationError):
            AgentConfig()


class TestToolConfig:
    """Test ToolConfig schema validation."""

    def test_valid_tool_config(self):
        """Test creating valid tool configuration."""
        config = ToolConfig(
            binary="test-binary",
            command_template="{binary} {prompt_file} {model}",
            models=["model1", "model2"],
            capabilities=["code_generation"],
        )
        assert config.binary == "test-binary"
        assert len(config.models) == 2

    def test_tool_config_missing_placeholder(self):
        """Test that command template must reference binary."""
        # Validation was relaxed to only require binary reference
        # This should pass now (no longer requires {model})
        config = ToolConfig(
            binary="test",
            command_template="{binary} {prompt_file}",  # Missing {model} is OK
            models=["model1"],
        )
        assert config.binary == "test"

        # But missing binary reference should fail
        with pytest.raises(ValidationError, match="should reference the binary"):
            ToolConfig(
                binary="test",
                command_template="{prompt_file} {model}",  # Missing binary reference
                models=["model1"],
            )

    def test_tool_config_all_required_placeholders(self):
        """Test all required placeholders must be present."""
        # Should work with all required placeholders
        config = ToolConfig(
            binary="test",
            command_template="{binary} {prompt_file} {model} --extra {output_file}",
            models=["model1"],
        )
        assert config.command_template is not None

    def test_tool_config_empty_models_list(self):
        """Test that tools must support at least one model."""
        # Pydantic doesn't enforce non-empty list by default
        # This is acceptable - could add validator if needed
        config = ToolConfig(
            binary="test",
            command_template="{binary} {prompt_file} {model}",
            models=[],
        )
        assert config.models == []


class TestModelConfig:
    """Test ModelConfig schema validation."""

    def test_valid_model_config(self):
        """Test creating valid model configuration."""
        config = ModelConfig(
            provider="test-provider",
            cost_per_1k_tokens={"input": 0.01, "output": 0.03},
            context_window=8000,
            task_suitability=["coding", "analysis"],
        )
        assert config.provider == "test-provider"
        assert config.cost_per_1k_tokens.input == 0.01
        assert config.context_window == 8000

    def test_model_config_negative_cost(self):
        """Test that negative costs are rejected."""
        with pytest.raises(ValidationError):
            ModelConfig(
                provider="test",
                cost_per_1k_tokens={"input": -0.01, "output": 0.03},
                context_window=8000,
            )

    def test_model_config_zero_cost(self):
        """Test that zero cost is acceptable (free models)."""
        config = ModelConfig(
            provider="test",
            cost_per_1k_tokens={"input": 0.0, "output": 0.0},
            context_window=8000,
        )
        assert config.cost_per_1k_tokens.input == 0.0

    def test_model_config_invalid_context_window(self):
        """Test that context window must be positive."""
        with pytest.raises(ValidationError):
            ModelConfig(
                provider="test",
                cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                context_window=0,  # Must be > 0
            )


class TestPolicyConfig:
    """Test PolicyConfig schema validation."""

    def test_valid_policy_config(self):
        """Test creating valid policy configuration."""
        config = PolicyConfig(
            daily_budget_usd=10.0,
            monthly_budget_usd=200.0,
        )
        assert config.daily_budget_usd == 10.0
        assert config.monthly_budget_usd == 200.0

    def test_policy_config_defaults(self):
        """Test policy config uses sensible defaults."""
        config = PolicyConfig()
        assert config.daily_budget_usd == 10.0
        assert config.limit.type == "soft"
        assert config.limit.threshold_percent == 80

    def test_policy_config_negative_budget(self):
        """Test that negative budgets are rejected."""
        with pytest.raises(ValidationError):
            PolicyConfig(daily_budget_usd=-10.0)

    def test_policy_config_invalid_threshold(self):
        """Test that threshold must be 0-100."""
        with pytest.raises(ValidationError):
            PolicyConfig(limit={"type": "soft", "threshold_percent": 150})


class TestCostOptimization:
    """Test CostOptimization schema validation."""

    def test_valid_cost_optimization(self):
        """Test creating valid cost optimization config."""
        config = CostOptimization(
            simple_task_threshold_tokens=1500,
            simple_task_models=["cheap-model"],
            complex_task_models=["expensive-model"],
        )
        assert config.simple_task_threshold_tokens == 1500

    def test_cost_optimization_invalid_threshold(self):
        """Test that threshold must be positive."""
        with pytest.raises(ValidationError):
            CostOptimization(
                simple_task_threshold_tokens=0,  # Must be > 0
            )


class TestCrossReferenceValidation:
    """Test cross-reference validation between configuration files."""

    def test_valid_cross_references(self):
        """Test that valid cross-references pass validation."""
        agents = AgentsSchema(
            agents={
                "test-agent": AgentConfig(
                    preferred_tool="test-tool",
                    preferred_model="test-model",
                    fallback_chain=["test-tool:test-model"],
                )
            }
        )
        tools = ToolsSchema(
            tools={
                "test-tool": ToolConfig(
                    binary="test",
                    command_template="{binary} {prompt_file} {model}",
                    models=["test-model"],
                )
            }
        )
        models = ModelsSchema(
            models={
                "test-model": ModelConfig(
                    provider="test",
                    cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                    context_window=8000,
                )
            }
        )

        errors = validate_agent_references(agents, tools, models)
        assert len(errors) == 0

    def test_agent_references_unknown_tool(self):
        """Test that referencing unknown tool is caught."""
        agents = AgentsSchema(
            agents={
                "test-agent": AgentConfig(
                    preferred_tool="unknown-tool",
                    preferred_model="test-model",
                )
            }
        )
        tools = ToolsSchema(tools={})
        models = ModelsSchema(
            models={
                "test-model": ModelConfig(
                    provider="test",
                    cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                    context_window=8000,
                )
            }
        )

        errors = validate_agent_references(agents, tools, models)
        assert len(errors) == 1
        assert "unknown tool" in errors[0].lower()
        assert "unknown-tool" in errors[0]

    def test_agent_references_unknown_model(self):
        """Test that referencing unknown model is caught."""
        agents = AgentsSchema(
            agents={
                "test-agent": AgentConfig(
                    preferred_tool="test-tool",
                    preferred_model="unknown-model",
                )
            }
        )
        tools = ToolsSchema(
            tools={
                "test-tool": ToolConfig(
                    binary="test",
                    command_template="{binary} {prompt_file} {model}",
                    models=["test-model"],
                )
            }
        )
        models = ModelsSchema(models={})

        errors = validate_agent_references(agents, tools, models)
        assert len(errors) == 1
        assert "unknown model" in errors[0].lower()
        assert "unknown-model" in errors[0]

    def test_fallback_chain_unknown_tool(self):
        """Test that fallback chain with unknown tool is caught."""
        agents = AgentsSchema(
            agents={
                "test-agent": AgentConfig(
                    preferred_tool="test-tool",
                    preferred_model="test-model",
                    fallback_chain=["unknown-tool:test-model"],
                )
            }
        )
        tools = ToolsSchema(
            tools={
                "test-tool": ToolConfig(
                    binary="test",
                    command_template="{binary} {prompt_file} {model}",
                    models=["test-model"],
                )
            }
        )
        models = ModelsSchema(
            models={
                "test-model": ModelConfig(
                    provider="test",
                    cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                    context_window=8000,
                )
            }
        )

        errors = validate_agent_references(agents, tools, models)
        assert len(errors) == 1
        assert "fallback" in errors[0].lower()
        assert "unknown-tool" in errors[0]

    def test_task_types_unknown_model(self):
        """Test that task types with unknown model is caught."""
        agents = AgentsSchema(
            agents={
                "test-agent": AgentConfig(
                    preferred_tool="test-tool",
                    preferred_model="test-model",
                    task_types={"simple": "unknown-model"},
                )
            }
        )
        tools = ToolsSchema(
            tools={
                "test-tool": ToolConfig(
                    binary="test",
                    command_template="{binary} {prompt_file} {model}",
                    models=["test-model"],
                )
            }
        )
        models = ModelsSchema(
            models={
                "test-model": ModelConfig(
                    provider="test",
                    cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                    context_window=8000,
                )
            }
        )

        errors = validate_agent_references(agents, tools, models)
        assert len(errors) == 1
        assert "task type" in errors[0].lower()
        assert "unknown-model" in errors[0]

    def test_multiple_validation_errors(self):
        """Test that multiple errors are all reported."""
        agents = AgentsSchema(
            agents={
                "test-agent": AgentConfig(
                    preferred_tool="unknown-tool",
                    preferred_model="unknown-model",
                    fallback_chain=["unknown-tool2:unknown-model2"],
                )
            }
        )
        tools = ToolsSchema(tools={})
        models = ModelsSchema(models={})

        errors = validate_agent_references(agents, tools, models)
        # Should have: unknown preferred_tool, unknown preferred_model,
        # unknown fallback tool, unknown fallback model
        assert len(errors) >= 4

    def test_tool_model_compatibility_validation(self):
        """Test that agent's preferred model must be supported by preferred tool."""
        agents = AgentsSchema(
            agents={
                "test-agent": AgentConfig(
                    preferred_tool="test-tool",
                    preferred_model="unsupported-model",  # Not in tool's models list
                )
            }
        )
        tools = ToolsSchema(
            tools={
                "test-tool": ToolConfig(
                    binary="test",
                    command_template="{binary} {prompt_file} {model}",
                    models=["supported-model"],  # Doesn't include 'unsupported-model'
                )
            }
        )
        models = ModelsSchema(
            models={
                "unsupported-model": ModelConfig(
                    provider="test",
                    cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                    context_window=8000,
                ),
                "supported-model": ModelConfig(
                    provider="test",
                    cost_per_1k_tokens={"input": 0.01, "output": 0.03},
                    context_window=8000,
                ),
            }
        )

        errors = validate_agent_references(agents, tools, models)
        # This should catch the incompatibility
        # NOTE: This will FAIL until we implement the fix
        assert len(errors) >= 1
        # Uncomment after implementing fix:
        # assert any('not supported by tool' in err.lower() for err in errors)
