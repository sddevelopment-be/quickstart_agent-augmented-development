"""
LLM Service Layer - Configuration Schemas

This module defines Pydantic models for validating YAML configuration files.
Supports agents.yaml, tools.yaml, models.yaml, and policies.yaml.

Tech Stack: Python 3.10+, Pydantic v2
"""

from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field, validator


# Agent Configuration Schema
class TaskTypeConfig(BaseModel):
    """Task-specific model overrides for an agent."""
    pass  # Dynamic keys, values are model names


class AgentConfig(BaseModel):
    """Configuration for a single agent."""
    preferred_tool: str = Field(..., description="Default tool for this agent")
    preferred_model: str = Field(..., description="Default model for this agent")
    fallback_chain: List[str] = Field(
        default_factory=list,
        description="Fallback tool:model pairs (e.g., 'claude-code:claude-sonnet-20240229')"
    )
    task_types: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Task type to model mapping"
    )

    @validator('fallback_chain')
    def validate_fallback_format(cls, v):
        """Ensure fallback chain entries follow 'tool:model' format."""
        for entry in v:
            if ':' not in entry:
                raise ValueError(f"Fallback entry must be 'tool:model' format: {entry}")
        return v


class AgentsSchema(BaseModel):
    """Root schema for agents.yaml configuration."""
    agents: Dict[str, AgentConfig] = Field(..., description="Agent configurations")


# Tool Configuration Schema
class PlatformPaths(BaseModel):
    """Platform-specific binary paths."""
    linux: Optional[str] = None
    macos: Optional[str] = None
    windows: Optional[str] = None


class ToolConfig(BaseModel):
    """Configuration for a single LLM tool."""
    binary: str = Field(..., description="Binary name or path")
    command_template: str = Field(
        ...,
        description="Command template with placeholders: {binary}, {prompt_file}, {model}, {output_file}"
    )
    platforms: Optional[PlatformPaths] = Field(
        default=None,
        description="Platform-specific binary paths"
    )
    models: List[str] = Field(..., description="Supported model names")
    capabilities: List[str] = Field(
        default_factory=list,
        description="Tool capabilities (e.g., code_generation, code_review)"
    )

    @validator('command_template')
    def validate_template_placeholders(cls, v):
        """Ensure command template contains required placeholders."""
        required = ['{binary}', '{prompt_file}', '{model}']
        for placeholder in required:
            if placeholder not in v:
                raise ValueError(f"Command template missing required placeholder: {placeholder}")
        return v


class ToolsSchema(BaseModel):
    """Root schema for tools.yaml configuration."""
    tools: Dict[str, ToolConfig] = Field(..., description="Tool configurations")


# Model Configuration Schema
class CostPerToken(BaseModel):
    """Token cost structure."""
    input: float = Field(..., ge=0, description="Cost per 1K input tokens (USD)")
    output: float = Field(..., ge=0, description="Cost per 1K output tokens (USD)")


class ModelConfig(BaseModel):
    """Configuration for a single model."""
    provider: str = Field(..., description="Provider name (e.g., openai, anthropic)")
    cost_per_1k_tokens: CostPerToken = Field(..., description="Token costs")
    context_window: int = Field(..., gt=0, description="Context window size")
    task_suitability: List[str] = Field(
        default_factory=list,
        description="Suitable task types"
    )


class ModelsSchema(BaseModel):
    """Root schema for models.yaml configuration."""
    models: Dict[str, ModelConfig] = Field(..., description="Model configurations")


# Policy Configuration Schema
class BudgetLimit(BaseModel):
    """Budget limit configuration."""
    type: Literal['soft', 'hard'] = Field(
        'soft',
        description="Enforcement type: 'soft' warns, 'hard' blocks"
    )
    threshold_percent: int = Field(
        80,
        ge=0,
        le=100,
        description="Warn/block threshold percentage"
    )


class CostOptimization(BaseModel):
    """Cost optimization rules."""
    simple_task_threshold_tokens: int = Field(
        1500,
        gt=0,
        description="Token threshold for simple task classification"
    )
    simple_task_models: List[str] = Field(
        default_factory=list,
        description="Models to use for simple tasks"
    )
    complex_task_models: List[str] = Field(
        default_factory=list,
        description="Models to use for complex tasks"
    )


class RateLimiting(BaseModel):
    """Rate limiting configuration."""
    max_requests_per_minute: Optional[Dict[str, int]] = Field(
        default_factory=dict,
        description="Per-tool rate limits (requests/minute)"
    )
    max_requests_per_hour: Optional[Dict[str, int]] = Field(
        default_factory=dict,
        description="Per-tool rate limits (requests/hour)"
    )


class PolicyConfig(BaseModel):
    """Single policy configuration."""
    daily_budget_usd: float = Field(10.0, ge=0, description="Daily budget limit (USD)")
    monthly_budget_usd: Optional[float] = Field(None, ge=0, description="Monthly budget limit (USD)")
    limit: BudgetLimit = Field(default_factory=BudgetLimit, description="Budget enforcement")
    prefer_cheaper_models_under_tokens: Optional[int] = Field(
        None,
        gt=0,
        description="Prefer cheaper models for prompts under this token count"
    )
    auto_fallback_on_rate_limit: bool = Field(True, description="Auto-fallback on rate limits")
    log_prompts: bool = Field(False, description="Log full prompt content")
    log_metadata: bool = Field(True, description="Log invocation metadata")
    require_justification_over_usd: Optional[float] = Field(
        None,
        ge=0,
        description="Require justification for requests over this cost"
    )


class PoliciesSchema(BaseModel):
    """Root schema for policies.yaml configuration."""
    policies: Dict[str, PolicyConfig] = Field(..., description="Policy configurations")
    cost_optimization: Optional[CostOptimization] = None
    rate_limiting: Optional[RateLimiting] = None


# Cross-Validation Functions
def validate_agent_references(
    agents: AgentsSchema,
    tools: ToolsSchema,
    models: ModelsSchema
) -> List[str]:
    """
    Validate cross-references between configuration files.
    
    Returns list of validation errors, empty if all valid.
    """
    errors = []
    
    for agent_name, agent_config in agents.agents.items():
        # Validate preferred_tool exists
        if agent_config.preferred_tool not in tools.tools:
            errors.append(
                f"Agent '{agent_name}' references unknown tool: {agent_config.preferred_tool}"
            )
        
        # Validate preferred_model exists
        if agent_config.preferred_model not in models.models:
            errors.append(
                f"Agent '{agent_name}' references unknown model: {agent_config.preferred_model}"
            )
        
        # Validate fallback chain references
        for fallback in agent_config.fallback_chain:
            tool_name, model_name = fallback.split(':')
            if tool_name not in tools.tools:
                errors.append(
                    f"Agent '{agent_name}' fallback references unknown tool: {tool_name}"
                )
            if model_name not in models.models:
                errors.append(
                    f"Agent '{agent_name}' fallback references unknown model: {model_name}"
                )
        
        # Validate task_types models exist
        for task_type, model_name in (agent_config.task_types or {}).items():
            if model_name not in models.models:
                errors.append(
                    f"Agent '{agent_name}' task type '{task_type}' references unknown model: {model_name}"
                )
    
    return errors


# Validation summary
__all__ = [
    'AgentConfig', 'AgentsSchema',
    'ToolConfig', 'ToolsSchema',
    'ModelConfig', 'ModelsSchema',
    'PolicyConfig', 'PoliciesSchema',
    'validate_agent_references'
]
