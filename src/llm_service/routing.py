"""
Routing Engine for LLM Service Layer

This module implements the core routing logic that determines which tool and model
to use for a given agent request based on configuration and policies.
"""

from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass

from .config.schemas import AgentsSchema, ToolsSchema, ModelsSchema, PoliciesSchema


@dataclass
class RoutingDecision:
    """
    Represents a routing decision made by the engine.
    """
    tool_name: str
    model_name: str
    reason: str
    fallback_used: bool = False
    original_tool: Optional[str] = None
    original_model: Optional[str] = None


class RoutingError(Exception):
    """Raised when routing cannot determine a valid tool/model combination."""
    pass


class RoutingEngine:
    """
    Routes agent requests to appropriate LLM tools and models.
    
    The routing engine considers:
    - Agent preferences (preferred_tool, preferred_model)
    - Task-specific overrides (task_types mapping)
    - Fallback chains (when primary tool/model unavailable)
    - Cost optimization (simple tasks → cheaper models)
    """
    
    def __init__(
        self,
        agents: AgentsSchema,
        tools: ToolsSchema,
        models: ModelsSchema,
        policies: PoliciesSchema,
    ):
        """
        Initialize routing engine with configuration.
        
        Args:
            agents: Agent configuration
            tools: Tool configuration
            models: Model configuration
            policies: Policy configuration
        """
        self.agents = agents
        self.tools = tools
        self.models = models
        self.policies = policies
    
    def route(
        self,
        agent_name: str,
        task_type: Optional[str] = None,
        prompt_size_tokens: Optional[int] = None,
    ) -> RoutingDecision:
        """
        Determine which tool and model to use for an agent request.
        
        Args:
            agent_name: Name of the agent making the request
            task_type: Optional task type (e.g., "simple", "complex", "coding")
            prompt_size_tokens: Optional prompt size for cost optimization
        
        Returns:
            RoutingDecision with selected tool and model
        
        Raises:
            RoutingError: If agent not found or routing fails
        """
        # Get agent configuration
        if agent_name not in self.agents.agents:
            available = ', '.join(self.agents.agents.keys())
            raise RoutingError(
                f"Agent '{agent_name}' not found. Available: {available}"
            )
        
        agent_config = self.agents.agents[agent_name]
        
        # Start with agent preferences
        selected_tool = agent_config.preferred_tool
        selected_model = agent_config.preferred_model
        reason = f"Agent '{agent_name}' preferred configuration"
        
        # Check for task-specific override
        if task_type and agent_config.task_types:
            if task_type in agent_config.task_types:
                override_model = agent_config.task_types[task_type]
                selected_model = override_model
                reason = f"Task type '{task_type}' override for agent '{agent_name}'"
        
        # Apply cost optimization if enabled and prompt size provided
        if prompt_size_tokens is not None:
            optimized = self._apply_cost_optimization(
                selected_model,
                prompt_size_tokens,
                task_type,
            )
            if optimized:
                selected_model, cost_reason = optimized
                reason = f"{reason} + {cost_reason}"
        
        # Validate tool and model exist
        if selected_tool not in self.tools.tools:
            # Try fallback chain
            fallback = self._try_fallback_chain(agent_config.fallback_chain)
            if fallback:
                selected_tool, selected_model = fallback
                return RoutingDecision(
                    tool_name=selected_tool,
                    model_name=selected_model,
                    reason=f"Primary tool unavailable, using fallback",
                    fallback_used=True,
                    original_tool=agent_config.preferred_tool,
                    original_model=agent_config.preferred_model,
                )
            else:
                raise RoutingError(
                    f"Tool '{selected_tool}' not found and no valid fallback available"
                )
        
        if selected_model not in self.models.models:
            raise RoutingError(
                f"Model '{selected_model}' not found in configuration"
            )
        
        # Verify tool supports the model
        tool_config = self.tools.tools[selected_tool]
        if selected_model not in tool_config.models:
            # Try to find compatible tool for this model
            compatible_tool = self._find_compatible_tool(selected_model)
            if compatible_tool:
                selected_tool = compatible_tool
                reason = f"{reason} + tool switched to {compatible_tool} (model compatibility)"
            else:
                raise RoutingError(
                    f"Tool '{selected_tool}' does not support model '{selected_model}'"
                )
        
        return RoutingDecision(
            tool_name=selected_tool,
            model_name=selected_model,
            reason=reason,
            fallback_used=False,
        )
    
    def _apply_cost_optimization(
        self,
        current_model: str,
        prompt_size_tokens: int,
        task_type: Optional[str],
    ) -> Optional[Tuple[str, str]]:
        """
        Apply cost optimization to model selection.
        
        Args:
            current_model: Currently selected model
            prompt_size_tokens: Size of prompt in tokens
            task_type: Optional task type
        
        Returns:
            Tuple of (optimized_model, reason) if optimization applied, else None
        """
        # Check if cost optimization is configured
        if not self.policies.cost_optimization:
            return None
        
        cost_opt = self.policies.cost_optimization
        
        # Check if prompt is under threshold for simple task optimization
        if prompt_size_tokens < cost_opt.simple_task_threshold_tokens:
            # Use cheaper model for simple tasks
            if cost_opt.simple_task_models:
                cheaper_model = cost_opt.simple_task_models[0]
                if cheaper_model in self.models.models:
                    current_cost = self.models.models[current_model].cost_per_1k_tokens.input
                    cheaper_cost = self.models.models[cheaper_model].cost_per_1k_tokens.input
                    
                    if cheaper_cost < current_cost:
                        return (
                            cheaper_model,
                            f"cost optimization (prompt {prompt_size_tokens} tokens < {cost_opt.simple_task_threshold_tokens})"
                        )
        
        return None
    
    def _try_fallback_chain(
        self,
        fallback_chain: List[str],
    ) -> Optional[Tuple[str, str]]:
        """
        Try to find a valid tool:model pair from fallback chain.
        
        Args:
            fallback_chain: List of "tool:model" fallback pairs
        
        Returns:
            Tuple of (tool, model) if found, else None
        """
        for fallback_entry in fallback_chain:
            tool_name, model_name = fallback_entry.split(':')
            
            # Check if both tool and model exist
            if tool_name in self.tools.tools and model_name in self.models.models:
                # Check if tool supports model
                tool_config = self.tools.tools[tool_name]
                if model_name in tool_config.models:
                    return (tool_name, model_name)
        
        return None
    
    def _find_compatible_tool(self, model_name: str) -> Optional[str]:
        """
        Find a tool that supports the given model.
        
        Args:
            model_name: Model to find tool for
        
        Returns:
            Tool name if found, else None
        """
        for tool_name, tool_config in self.tools.tools.items():
            if model_name in tool_config.models:
                return tool_name
        return None
    
    def get_model_cost(self, model_name: str) -> Dict[str, float]:
        """
        Get cost information for a model.
        
        Args:
            model_name: Model name
        
        Returns:
            Dictionary with 'input' and 'output' costs per 1K tokens
        
        Raises:
            RoutingError: If model not found
        """
        if model_name not in self.models.models:
            raise RoutingError(f"Model '{model_name}' not found")
        
        model_config = self.models.models[model_name]
        return {
            'input': model_config.cost_per_1k_tokens.input,
            'output': model_config.cost_per_1k_tokens.output,
        }
    
    def list_agent_capabilities(self, agent_name: str) -> Dict[str, Any]:
        """
        Get capabilities and configuration for an agent.
        
        Args:
            agent_name: Agent name
        
        Returns:
            Dictionary with agent configuration details
        
        Raises:
            RoutingError: If agent not found
        """
        if agent_name not in self.agents.agents:
            raise RoutingError(f"Agent '{agent_name}' not found")
        
        agent_config = self.agents.agents[agent_name]
        
        return {
            'agent_name': agent_name,
            'preferred_tool': agent_config.preferred_tool,
            'preferred_model': agent_config.preferred_model,
            'fallback_chain': agent_config.fallback_chain,
            'task_types': agent_config.task_types or {},
        }
