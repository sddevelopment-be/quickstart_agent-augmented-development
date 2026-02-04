# ADR-029: Use Abstract Base Class for Tool Adapter Interface

**status**: Draft (To be finalized in Milestone 2)  
**date**: 2026-02-04

## Context

Milestone 2 of the LLM Service Layer implementation requires tool adapters that execute external LLM tools (claude-code, codex, etc.) based on YAML configuration. The adapter architecture must support:

1. **Multiple Implementations**: At least 3 adapters (claude-code, codex, generic YAML-based)
2. **Consistent Interface**: All adapters must provide the same execution contract
3. **Testability**: Easy to mock adapters in routing engine and integration tests
4. **Extensibility**: Community contributors can add new tools without modifying core code
5. **Type Safety**: Catch adapter implementation errors early (fail-fast)

**Architectural Decision Point:**

How should we define the adapter interface to ensure consistency, testability, and extensibility?

**Options Considered:**

1. **Abstract Base Class (ABC)** - Explicit interface with runtime validation
2. **Protocol (typing.Protocol)** - Structural subtyping with static-only validation
3. **Duck Typing** - No formal interface, rely on Python's dynamic nature

**Key Forces:**
- Need for **explicit contract** so contributors know what to implement
- Requirement for **runtime validation** to catch incomplete implementations
- Desire for **strong IDE support** and type checking
- Balance between **flexibility** and **safety**
- **Community extensibility** - clear patterns for external contributions

**Reference Documentation:**
- Implementation Plan: `docs/planning/llm-service-layer-implementation-plan.md` (Milestone 2, Batch 2.1)
- Design Review: `work/analysis/llm-service-adapter-interface-review.md`

## Decision

**We will use Abstract Base Class (ABC) for the tool adapter interface.**

All tool adapters will inherit from `ToolAdapter` base class defined using Python's `abc` module. Concrete adapters must implement abstract methods: `execute()` and `get_capabilities()`.

**Key Implementation:**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ToolAdapter(ABC):
    """Abstract base class for LLM tool adapters."""
    
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
        """Execute tool with given parameters."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of tool capabilities."""
        pass
    
    def validate_model(self, model: str) -> bool:
        """Validate if model supported (concrete implementation)."""
        return model in self.tool_config.models
```

Concrete adapters will inherit and implement abstract methods:

```python
class ClaudeCodeAdapter(ToolAdapter):
    def execute(self, prompt_file: str, model: str, output_file: str, **kwargs):
        # Implementation...
        pass
    
    def get_capabilities(self) -> List[str]:
        return self.tool_config.capabilities
```

## Rationale

### Why Abstract Base Class?

**Strengths:**

1. **Explicit Interface Contract**
   - Base class clearly defines required methods
   - Docstrings document expected behavior and return types
   - Contributors know exactly what to implement

2. **Runtime Validation**
   - Python raises `TypeError` if abstract methods not implemented
   - Errors caught at adapter instantiation, not at runtime execution
   - No silent failures in production

3. **Excellent Developer Experience**
   - IDE autocomplete shows required methods
   - Type checker (mypy) validates implementations
   - Clear error messages for missing/incorrect methods

4. **Strong Testing Support**
   - Easy to create mock adapters inheriting from ABC
   - Clear interface boundaries for test fixtures
   - Can provide test utilities in base class

5. **Community Extensibility**
   - Well-documented Python pattern (familiar to contributors)
   - Explicit inheritance makes adapter relationship obvious
   - Clear guidance: "inherit from ToolAdapter and implement these methods"

6. **Shared Implementation**
   - Base class provides utility methods (e.g., `validate_model()`, `parse_command_template()`)
   - Reduces code duplication across adapters
   - Default implementations where appropriate

**Trade-offs Accepted:**

1. **Inheritance Required**
   - Concrete adapters must inherit from `ToolAdapter`
   - *Mitigation*: Clear inheritance relationship aids understanding
   - *Impact*: Acceptable - single inheritance is standard Python pattern

2. **Slight Boilerplate**
   - Must define base class and abstract methods
   - *Mitigation*: One-time cost, benefits all future adapters
   - *Impact*: Minimal - base class is ~50 lines

### Why NOT Protocol (typing.Protocol)?

**Protocol Evaluated:**
- ✅ No inheritance required (structural subtyping)
- ✅ Modern Python (PEP 544)
- ❌ **No runtime validation** - only static type checking
- ❌ Less discoverable for contributors
- ❌ Weaker IDE support in some environments

**Rejection Rationale:**
- **Runtime validation is critical**: Incomplete adapter implementations would pass instantiation and fail later during execution (poor fail-fast)
- **Risk for community contributions**: Contributors may miss required methods without runtime error
- **Less familiar pattern**: Protocol is modern but less widely used than ABC

### Why NOT Duck Typing?

**Duck Typing Evaluated:**
- ✅ Maximum flexibility
- ✅ Minimal boilerplate
- ❌ **No type safety** - no static or runtime validation
- ❌ Poor discoverability - interface contract only in documentation
- ❌ Runtime errors from method signature mismatches (AttributeError)

**Rejection Rationale:**
- **High risk**: No validation until runtime failures occur
- **Poor contributor experience**: Interface contract not explicit
- **Maintenance burden**: Interface drift likely as system evolves

### Decision Factors

| Factor | ABC | Protocol | Duck Typing | Winner |
|--------|-----|----------|-------------|--------|
| Runtime Validation | ✅ Yes | ❌ No | ❌ No | **ABC** |
| Static Type Checking | ✅ Yes | ✅ Yes | ❌ No | ABC/Protocol |
| IDE Support | ✅ Excellent | ⚠️ Partial | ❌ None | **ABC** |
| Testability | ✅ Excellent | ✅ Good | ⚠️ Workable | **ABC** |
| Community Clarity | ✅ Very Clear | ⚠️ Less Clear | ❌ Unclear | **ABC** |
| Familiar Pattern | ✅ Very | ⚠️ Moderate | ✅ Very | **ABC** |
| Boilerplate | ⚠️ Some | ✅ Minimal | ✅ None | Protocol/Duck |

**Overall Winner:** Abstract Base Class (ABC)

## Envisioned Consequences

### Positive Consequences

1. ✅ **Explicit Contract for Contributors**
   - Clear interface definition in base class
   - Docstrings document expected behavior
   - Reduced ambiguity for community contributions

2. ✅ **Fail-Fast Error Detection**
   - Incomplete adapters fail at instantiation
   - Runtime validation catches missing methods
   - No silent failures in production

3. ✅ **Strong IDE and Type Checker Support**
   - Autocomplete for required methods
   - Mypy validates implementations
   - Early error detection during development

4. ✅ **Excellent Testability**
   - Easy to create mock adapters for tests
   - Clear boundaries for test fixtures
   - Shared test utilities in base class

5. ✅ **Code Reuse via Shared Methods**
   - Utility methods in base class (e.g., `validate_model()`)
   - Reduces duplication across adapters
   - Consistent behavior for common operations

### Negative Consequences

1. ⚠️ **Inheritance Required**
   - Adapters must inherit from `ToolAdapter` base class
   - Single inheritance constraint (Python limitation)
   - *Mitigation*: Standard Python pattern, widely accepted

2. ⚠️ **Slight Boilerplate**
   - Must define base class with abstract methods
   - *Mitigation*: One-time cost, benefits all adapters
   - *Impact*: ~50 lines for base class definition

3. ⚠️ **Base Class Changes Affect All Adapters**
   - Adding/removing abstract methods requires updating all adapters
   - *Mitigation*: Design interface carefully upfront
   - *Impact*: Low - interface is stable for MVP scope

### Risk Mitigation Strategies

**Interface Stability:**
- Design adapter interface carefully during M2 Batch 2.1
- Minimize required abstract methods (only essential methods)
- Use optional methods (concrete implementations) for utilities
- Version adapter interface if breaking changes needed in future

**Testing Strategy:**
- Create comprehensive test suite for base class utilities
- Provide test fixture examples for adapter implementers
- Mock adapters for routing engine tests

## Implementation Guidance

### Adapter Base Class Structure

```python
# src/llm_service/adapters/base.py

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
    
    All concrete adapters must implement:
    - execute(): Execute tool with given parameters
    - get_capabilities(): Return tool capabilities
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
    ) -> ExecutionResult:
        """Execute tool - must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return capabilities - must be implemented by subclasses."""
        pass
    
    # Concrete utility methods
    def validate_model(self, model: str) -> bool:
        return model in self.tool_config.models
    
    def parse_command_template(self, prompt_file: str, model: str, output_file: str) -> List[str]:
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
# src/llm_service/adapters/claude_code.py

class ClaudeCodeAdapter(ToolAdapter):
    """Adapter for claude-code CLI tool."""
    
    def execute(self, prompt_file: str, model: str, output_file: str, **kwargs) -> ExecutionResult:
        if not self.validate_model(model):
            raise ValidationError(f"Model '{model}' not supported")
        
        command = self.parse_command_template(prompt_file, model, output_file)
        result = subprocess.run(command, capture_output=True, check=True)
        
        return ExecutionResult(
            status='success',
            output=result.stdout,
            tokens=self._parse_tokens(result.stdout)
        )
    
    def get_capabilities(self) -> List[str]:
        return self.tool_config.capabilities
```

## Considered Alternatives

### Alternative 1: Protocol (typing.Protocol)

**Description:** Use `typing.Protocol` for structural subtyping - adapters automatically satisfy interface if they have matching methods.

**Pros:**
- No inheritance required
- Structural typing (more flexible)
- Modern Python pattern (PEP 544)

**Cons:**
- No runtime validation (static only)
- Less discoverable for contributors
- Weaker IDE support

**Rejected Because:** Runtime validation is critical for catching incomplete adapter implementations early. Protocol provides only static type checking.

### Alternative 2: Duck Typing (No Formal Interface)

**Description:** No formal interface definition - rely on Python's duck typing.

**Pros:**
- Maximum flexibility
- Minimal boilerplate
- Pythonic approach

**Cons:**
- No type safety (static or runtime)
- Poor discoverability
- Runtime AttributeError for method mismatches

**Rejected Because:** No validation leads to late error discovery and poor contributor experience.

## References

**Design Analysis:**
- `work/analysis/llm-service-adapter-interface-review.md` - Detailed option evaluation

**Related ADRs:**
- [ADR-025: LLM Service Layer for Agent-Tool Orchestration](ADR-025-llm-service-layer.md) - Approved architecture
- [ADR-026: Pydantic V2 for Schema Validation](ADR-026-pydantic-v2-validation.md) - Configuration validation

**Related Documents:**
- `docs/planning/llm-service-layer-implementation-plan.md` - Milestone 2 requirements
- `docs/architecture/design/llm-service-layer-prestudy.md` - Original architecture vision

**External References:**
- [Python ABC Documentation](https://docs.python.org/3/library/abc.html)
- [PEP 3119 - Abstract Base Classes](https://www.python.org/dev/peps/pep-3119/)
- [PEP 544 - Protocols](https://www.python.org/dev/peps/pep-0544/) (considered alternative)

---

**Decision Made By:** Architect Alphonso (design review)  
**Date:** 2026-02-04  
**Status:** Draft - To be finalized during Milestone 2 Batch 2.1 implementation  
**Next Step:** Implement `ToolAdapter` base class in `src/llm_service/adapters/base.py`
