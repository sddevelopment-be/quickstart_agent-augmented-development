# Adapter Interface Design Review
## LLM Service Layer - Milestone 2 Preparation

**Date:** 2026-02-04  
**Author:** Architect Alphonso  
**Purpose:** Evaluate adapter interface options to unblock Milestone 2 Batch 2.1  
**Status:** Design Review (Final Recommendation Provided)

---

## Executive Summary

**Decision Point:** Choose interface pattern for tool adapters in Milestone 2

**Recommendation:** **Abstract Base Class (ABC) with explicit interface contract**

**Key Rationale:**
- ✅ Explicit interface contract prevents implementation errors
- ✅ Runtime validation ensures adapter completeness
- ✅ Excellent testability with clear mocking boundaries
- ✅ Familiar pattern for Python developers
- ✅ Strong IDE support and type checking

**Impact:** Unblocks M2 Batch 2.1 (base adapter implementation)

---

## Context

### Problem Statement

Milestone 2 requires implementing tool adapters that execute LLM tools (claude-code, codex) based on YAML configuration. The adapter architecture must support:

1. **Multiple Implementations**: claude-code, codex, and generic YAML-based adapters
2. **Consistent Interface**: All adapters must provide the same execution contract
3. **Testability**: Easy to mock adapters in routing engine tests
4. **Extensibility**: Community contributors can add new tools
5. **Type Safety**: Catch adapter implementation errors early

### Batch 2.1 Requirements

From implementation plan:
- Base adapter interface/abstract class
- Command template parsing and substitution
- Subprocess execution wrapper with error handling
- Output normalization framework

### Key Constraints

- **Python 3.10+**: Can use modern Python features (ABC, Protocol, type hints)
- **Testing Focus**: Must support easy mocking for routing engine tests
- **Community Contributions**: Interface should be clear for external contributors
- **YAML-Driven**: Generic adapter must work with YAML-only definitions

---

## Option 1: Abstract Base Class (ABC)

### Description

Define an abstract base class using `abc.ABC` with abstract methods that concrete adapters must implement.

### Code Example

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class ToolAdapter(ABC):
    """
    Abstract base class for tool adapters.
    
    All concrete adapters must implement execute() and get_capabilities().
    """
    
    def __init__(self, tool_config: ToolConfig):
        self.tool_config = tool_config
    
    @abstractmethod
    def execute(
        self,
        prompt_file: str,
        model: str,
        output_file: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute tool with given parameters.
        
        Args:
            prompt_file: Path to prompt file
            model: Model name
            output_file: Path for output
            **kwargs: Additional tool-specific parameters
        
        Returns:
            Dict with keys: 'status', 'output', 'tokens', 'cost_usd'
        
        Raises:
            ToolExecutionError: If tool execution fails
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of tool capabilities."""
        pass
    
    def validate_model(self, model: str) -> bool:
        """Validate if model is supported (concrete implementation)."""
        return model in self.tool_config.models


# Concrete Implementation
class ClaudeCodeAdapter(ToolAdapter):
    def execute(self, prompt_file: str, model: str, output_file: str, **kwargs) -> Dict[str, Any]:
        # Implementation...
        command = self._build_command(prompt_file, model, output_file)
        result = subprocess.run(command, capture_output=True, check=True)
        return self._parse_output(result)
    
    def get_capabilities(self) -> List[str]:
        return self.tool_config.capabilities
```

### Usage Example

```python
# Router uses adapter through interface
adapter: ToolAdapter = ClaudeCodeAdapter(tool_config)
result = adapter.execute(prompt_file="prompt.txt", model="claude-sonnet", output_file="out.txt")

# Type checker ensures all required methods implemented
# Runtime error if concrete class doesn't implement abstract methods
```

### Pros

1. ✅ **Explicit Contract**: Interface clearly defined in base class
2. ✅ **Runtime Validation**: Python raises `TypeError` if abstract methods not implemented
3. ✅ **IDE Support**: Excellent autocomplete and error detection
4. ✅ **Familiar Pattern**: Well-known Python pattern, easy for contributors to understand
5. ✅ **Mypy Support**: Strong static type checking for implementations
6. ✅ **Testing**: Easy to create test fixtures inheriting from ABC
7. ✅ **Documentation**: Base class docstrings document interface contract

### Cons

1. ⚠️ **Inheritance Required**: Concrete classes must inherit from base class
2. ⚠️ **Slightly More Boilerplate**: Must define base class and abstract methods
3. ⚠️ **Runtime Check**: Interface compliance checked at instantiation, not import time

### Evaluation

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Type Safety | ⭐⭐⭐⭐⭐ | Strong runtime and static checking |
| Testability | ⭐⭐⭐⭐⭐ | Easy to mock, clear interface boundaries |
| Extensibility | ⭐⭐⭐⭐⭐ | Clear contract for contributors |
| Python Idioms | ⭐⭐⭐⭐⭐ | Standard Python pattern |
| Maintenance | ⭐⭐⭐⭐ | Base class changes propagate to all adapters |

---

## Option 2: Protocol (typing.Protocol)

### Description

Define a structural subtype using `typing.Protocol` - adapters automatically satisfy the protocol if they have matching methods (structural typing, not nominal).

### Code Example

```python
from typing import Protocol, Dict, Any, List

class ToolAdapter(Protocol):
    """
    Protocol for tool adapters (structural typing).
    
    Any class with matching methods satisfies this protocol.
    """
    tool_config: ToolConfig
    
    def execute(
        self,
        prompt_file: str,
        model: str,
        output_file: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute tool with given parameters."""
        ...
    
    def get_capabilities(self) -> List[str]:
        """Return list of tool capabilities."""
        ...
    
    def validate_model(self, model: str) -> bool:
        """Validate if model is supported."""
        ...


# Concrete Implementation (NO inheritance required)
class ClaudeCodeAdapter:
    def __init__(self, tool_config: ToolConfig):
        self.tool_config = tool_config
    
    def execute(self, prompt_file: str, model: str, output_file: str, **kwargs) -> Dict[str, Any]:
        # Implementation...
        pass
    
    def get_capabilities(self) -> List[str]:
        return self.tool_config.capabilities
    
    def validate_model(self, model: str) -> bool:
        return model in self.tool_config.models
```

### Usage Example

```python
# Type checker validates adapter matches protocol
def route_request(adapter: ToolAdapter, prompt: str, model: str) -> Dict[str, Any]:
    return adapter.execute(prompt, model, "output.txt")

# ClaudeCodeAdapter automatically satisfies ToolAdapter protocol
adapter = ClaudeCodeAdapter(tool_config)
result = route_request(adapter, "prompt.txt", "claude-sonnet")

# No runtime check - only mypy validates protocol compliance
```

### Pros

1. ✅ **No Inheritance**: Concrete classes don't need to inherit from base
2. ✅ **Structural Typing**: More flexible than nominal typing
3. ✅ **Mypy Support**: Static type checking validates protocol compliance
4. ✅ **Modern Python**: Pythonic approach (PEP 544)
5. ✅ **Flexible**: Classes can satisfy multiple protocols

### Cons

1. ❌ **No Runtime Validation**: Protocol compliance only checked by mypy, not at runtime
2. ❌ **Less Discoverable**: No explicit inheritance relationship in code
3. ❌ **Silent Failures**: Incomplete implementations may pass runtime but fail mypy
4. ❌ **Weaker IDE Support**: Some IDEs don't autocomplete protocol methods
5. ❌ **No Shared Implementation**: Can't provide default methods in protocol

### Evaluation

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Type Safety | ⭐⭐⭐ | Static only, no runtime validation |
| Testability | ⭐⭐⭐⭐ | Easy to mock, but no runtime interface checks |
| Extensibility | ⭐⭐⭐ | Less explicit for contributors |
| Python Idioms | ⭐⭐⭐⭐ | Modern Python, but less common |
| Maintenance | ⭐⭐⭐⭐ | Protocol changes require coordinated updates |

---

## Option 3: Duck Typing (No Formal Interface)

### Description

No formal interface definition - rely on Python's duck typing. If an object has the required methods, it works.

### Code Example

```python
# No interface definition - just documentation

class ClaudeCodeAdapter:
    """
    Tool adapter for claude-code CLI.
    
    Interface Contract (informal):
    - execute(prompt_file, model, output_file, **kwargs) -> Dict[str, Any]
    - get_capabilities() -> List[str]
    - validate_model(model) -> bool
    """
    
    def __init__(self, tool_config: ToolConfig):
        self.tool_config = tool_config
    
    def execute(self, prompt_file: str, model: str, output_file: str, **kwargs) -> Dict[str, Any]:
        # Implementation...
        pass
    
    def get_capabilities(self) -> List[str]:
        return self.tool_config.capabilities
    
    def validate_model(self, model: str) -> bool:
        return model in self.tool_config.models
```

### Usage Example

```python
# No type hint for adapter - any object with execute() works
def route_request(adapter, prompt: str, model: str):
    return adapter.execute(prompt, model, "output.txt")

# Runtime AttributeError if method missing
adapter = ClaudeCodeAdapter(tool_config)
result = route_request(adapter, "prompt.txt", "claude-sonnet")
```

### Pros

1. ✅ **Minimal Boilerplate**: No interface definition needed
2. ✅ **Maximum Flexibility**: Any object with matching methods works
3. ✅ **No Inheritance**: No base class required
4. ✅ **Pythonic**: "If it walks like a duck..."

### Cons

1. ❌ **No Type Safety**: No static or runtime validation
2. ❌ **Poor Discoverability**: Interface contract only in documentation
3. ❌ **Runtime Errors**: Method signature mismatches caught late (AttributeError)
4. ❌ **Weak IDE Support**: No autocomplete or error detection
5. ❌ **No Mypy Validation**: Type checker can't verify interface compliance
6. ❌ **Maintenance Burden**: Interface changes require manual coordination

### Evaluation

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Type Safety | ⭐ | No validation whatsoever |
| Testability | ⭐⭐⭐ | Mocking works, but no interface guarantees |
| Extensibility | ⭐⭐ | Contributors must reverse-engineer interface |
| Python Idioms | ⭐⭐⭐⭐ | Classic Python duck typing |
| Maintenance | ⭐⭐ | High risk of interface drift |

---

## Comparison Matrix

| Criterion | ABC | Protocol | Duck Typing |
|-----------|-----|----------|-------------|
| **Type Safety (Runtime)** | ✅ Strong | ❌ None | ❌ None |
| **Type Safety (Static)** | ✅ Mypy | ✅ Mypy | ❌ None |
| **IDE Support** | ✅ Excellent | ⚠️ Partial | ❌ None |
| **Testability** | ✅ Excellent | ✅ Good | ⚠️ Workable |
| **Extensibility** | ✅ Explicit | ⚠️ Implicit | ⚠️ Undocumented |
| **Boilerplate** | ⚠️ Some | ✅ Minimal | ✅ None |
| **Familiar Pattern** | ✅ Very | ⚠️ Moderate | ✅ Very |
| **Error Detection** | ✅ Early | ⚠️ Static only | ❌ Runtime only |
| **Community Clarity** | ✅ Clear | ⚠️ Less clear | ❌ Unclear |
| **Maintenance** | ✅ Good | ⚠️ Coordinated | ❌ Risky |

---

## Recommendation: Abstract Base Class (ABC)

### Final Decision

**Use Abstract Base Class (ABC) for tool adapter interface.**

### Key Rationale

1. **Explicit Interface Contract**
   - Base class clearly defines required methods
   - Docstrings document expected behavior
   - Contributors know exactly what to implement

2. **Runtime Validation**
   - Python raises `TypeError` if abstract methods not implemented
   - Catches incomplete adapters at instantiation time
   - No silent failures in production

3. **Excellent Developer Experience**
   - IDE autocomplete shows required methods
   - Type checker validates implementations
   - Clear error messages for missing methods

4. **Strong Testing Support**
   - Easy to create mock adapters for routing tests
   - Clear interface boundaries for test fixtures
   - Can provide test utilities in base class

5. **Community Extensibility**
   - Clear pattern for contributors to follow
   - Well-documented Python pattern (familiar)
   - Explicit inheritance makes adapter relationship obvious

6. **Shared Implementation**
   - Base class can provide utility methods (e.g., `validate_model()`)
   - Reduces code duplication across adapters
   - Default implementations where appropriate

### Why NOT Protocol?

- **No Runtime Validation**: Protocol only provides static type checking
- **Risk for Community**: Contributors may miss methods without runtime error
- **Less Familiar**: Protocol is modern but less widely used than ABC

### Why NOT Duck Typing?

- **High Risk**: No validation until runtime failures
- **Poor Contributor Experience**: Interface contract not explicit
- **Maintenance Burden**: Interface drift likely over time

### Trade-offs Accepted

1. **Inheritance Required**: Adapters must inherit from `ToolAdapter` ABC
   - *Mitigation*: Acceptable - clear inheritance relationship aids understanding

2. **Slight Boilerplate**: Must define abstract methods in base class
   - *Mitigation*: One-time cost, benefits all future adapters

---

## Implementation Guidance

### Recommended Base Class Structure

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ExecutionResult:
    """Result of tool execution."""
    status: str  # 'success' or 'error'
    output: str
    tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    error_message: Optional[str] = None


class ToolAdapter(ABC):
    """
    Abstract base class for LLM tool adapters.
    
    Concrete adapters must implement:
    - execute(): Execute tool with given parameters
    - get_capabilities(): Return tool capabilities
    
    Provided utilities:
    - validate_model(): Check if model supported by tool
    - parse_command_template(): Substitute placeholders in command template
    """
    
    def __init__(self, tool_config: ToolConfig):
        """
        Initialize adapter with tool configuration.
        
        Args:
            tool_config: Tool configuration from tools.yaml
        """
        self.tool_config = tool_config
    
    @abstractmethod
    def execute(
        self,
        prompt_file: str,
        model: str,
        output_file: str,
        **kwargs
    ) -> ExecutionResult:
        """
        Execute tool with given parameters.
        
        Args:
            prompt_file: Path to prompt file
            model: Model name (must be in tool_config.models)
            output_file: Path for output
            **kwargs: Additional tool-specific parameters
        
        Returns:
            ExecutionResult with status, output, tokens, cost
        
        Raises:
            ToolExecutionError: If tool execution fails
            ValidationError: If parameters invalid
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return list of tool capabilities.
        
        Returns:
            List of capability strings (e.g., ['code_generation', 'code_review'])
        """
        pass
    
    def validate_model(self, model: str) -> bool:
        """
        Validate if model is supported by this tool.
        
        Args:
            model: Model name to validate
        
        Returns:
            True if model supported, False otherwise
        """
        return model in self.tool_config.models
    
    def parse_command_template(
        self,
        prompt_file: str,
        model: str,
        output_file: str
    ) -> List[str]:
        """
        Parse command template with parameter substitution.
        
        Substitutes placeholders:
        - {binary}: tool binary path
        - {prompt_file}: prompt file path
        - {model}: model name
        - {output_file}: output file path
        
        Args:
            prompt_file: Path to prompt file
            model: Model name
            output_file: Path for output
        
        Returns:
            List of command arguments for subprocess
        """
        template = self.tool_config.command_template
        command_str = template.format(
            binary=self.tool_config.binary,
            prompt_file=prompt_file,
            model=model,
            output_file=output_file
        )
        return command_str.split()
```

### Example Concrete Adapter

```python
class ClaudeCodeAdapter(ToolAdapter):
    """Adapter for claude-code CLI tool."""
    
    def execute(
        self,
        prompt_file: str,
        model: str,
        output_file: str,
        **kwargs
    ) -> ExecutionResult:
        """Execute claude-code with given parameters."""
        # Validate model
        if not self.validate_model(model):
            raise ValidationError(f"Model '{model}' not supported by claude-code")
        
        # Build command using template
        command = self.parse_command_template(prompt_file, model, output_file)
        
        # Execute subprocess
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=300  # 5 minute timeout
            )
            
            # Parse output
            return ExecutionResult(
                status='success',
                output=result.stdout,
                tokens=self._parse_tokens(result.stdout),
                cost_usd=self._calculate_cost(model, tokens)
            )
        
        except subprocess.CalledProcessError as e:
            return ExecutionResult(
                status='error',
                output='',
                error_message=e.stderr
            )
    
    def get_capabilities(self) -> List[str]:
        """Return claude-code capabilities."""
        return self.tool_config.capabilities
    
    def _parse_tokens(self, output: str) -> Optional[int]:
        """Parse token count from claude output."""
        # Implementation...
        pass
    
    def _calculate_cost(self, model: str, tokens: int) -> Optional[float]:
        """Calculate cost based on model and tokens."""
        # Implementation...
        pass
```

---

## Next Steps

1. **ADR-029 Draft**: Create ADR documenting ABC selection (ready for finalization during M2)
2. **M2 Batch 2.1**: Implement `ToolAdapter` base class in `src/llm_service/adapters/base.py`
3. **Adapter Tests**: Create test fixtures and mocks using ABC
4. **Documentation**: Document adapter interface in `docs/architecture/patterns/tool-adapters.md`

---

## Appendix: Decision Factors

### Type Safety Priority

- MVP requires adapters for 2 tools (claude-code, codex)
- Community will contribute additional adapters
- Runtime validation prevents incomplete implementations reaching production
- Static + runtime checking provides strongest guarantees

### Testing Requirements

- Routing engine must mock adapters for unit tests
- Clear interface boundaries simplify test design
- ABC provides explicit contract for test fixtures

### Community Extensibility

- Contributors need clear guidance for adding tools
- Explicit interface contract reduces ambiguity
- Familiar pattern (ABC) lowers contribution barrier

---

**Prepared By:** Architect Alphonso  
**Date:** 2026-02-04  
**Status:** Final Recommendation - Ready for M2 Batch 2.1  
**Review:** Unblocks Milestone 2 implementation
