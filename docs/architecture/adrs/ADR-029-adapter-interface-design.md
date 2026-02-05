# ADR-029: Use Abstract Base Class for Tool Adapter Interface

**status**: Accepted (Updated 2026-02-05 with Generic Adapter Decision)  
**date**: 2026-02-04  
**updated**: 2026-02-05

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
**Status:** Accepted  
**Updated:** 2026-02-05 - Generic Adapter Decision  
**Next Step:** Implement `GenericYAMLAdapter` using the validated base infrastructure

---

## Update (2026-02-05): Generic YAML-Driven Adapter Decision

**Context:** After implementing M2 Batch 2.1 (adapter base infrastructure) and M2 Batch 2.2 (ClaudeCodeAdapter as reference implementation), architecture review identified that concrete adapters are largely redundant with YAML configuration.

### Architecture Review Findings

**Analysis Document:** `work/analysis/generic-yaml-adapter-architecture-review.md`

**Key Finding:** ClaudeCodeAdapter (~400 lines) primarily delegates to generic infrastructure:
- Model mapping → Redundant (YAML lists models)
- Binary path resolution → Redundant (YAML has platform-specific paths)
- Command generation → Delegates to TemplateParser
- Subprocess execution → Delegates to SubprocessWrapper
- Output normalization → Delegates to OutputNormalizer

**Value-Add from Concrete Adapter:**
- User-friendly error messages
- Reference implementation for patterns
- Test fixtures validating tool integration

### Decision: Generic YAML-Driven Adapter

**We will implement a single `GenericYAMLAdapter` that reads configuration from YAML files.**

This approach:
1. ✅ **Eliminates code duplication** - One adapter implementation for all tools
2. ✅ **Enables YAML-based extensibility** - Add new tools without code changes
3. ✅ **Faster to MVP** - No need for per-tool adapter implementations
4. ✅ **Community-friendly** - Contributors add tools via YAML config, not Python code
5. ✅ **Aligns with design philosophy** - YAML-driven configuration throughout system

### Implementation Strategy

**GenericYAMLAdapter class:**
```python
class GenericYAMLAdapter(ToolAdapter):
    """
    Generic adapter that reads tool configuration from YAML.
    No code changes needed to add new tools.
    """
    
    def __init__(self, tool_name: str, tool_config: ToolConfig):
        self.tool_name = tool_name
        self.tool_config = tool_config
        self.template_parser = TemplateParser()
        self.subprocess_wrapper = SubprocessWrapper()
        self.output_normalizer = OutputNormalizer()
    
    def execute(self, prompt: str, model: str, params: Dict = None) -> ToolResponse:
        # 1. Validate model is in YAML config
        if model not in self.tool_config.models:
            raise InvalidModelError(f"Model {model} not supported")
        
        # 2. Resolve binary path from YAML or PATH
        binary = self._resolve_binary()
        
        # 3. Generate command from YAML template
        context = {"binary": binary, "model": model, "prompt": prompt}
        command = self.template_parser.parse(
            self.tool_config.command_template, 
            context
        )
        
        # 4. Execute via subprocess with ENV vars from YAML
        env = self._prepare_env(params)
        result = self.subprocess_wrapper.execute(command, env=env)
        
        # 5. Normalize output
        normalized = self.output_normalizer.normalize(result.stdout, self.tool_name)
        
        return ToolResponse(
            output=normalized.response_text,
            metadata=normalized.metadata
        )
```

### Role of ClaudeCodeAdapter

**ClaudeCodeAdapter is retained as:**
1. **Reference Implementation** - Demonstrates adapter pattern for contributors
2. **Test Fixture** - Integration tests validate tool integration patterns
3. **Documentation** - Shows how adapters work with real tool

**NOT used for production** - `GenericYAMLAdapter` handles all tools via YAML config.

### Benefits of This Approach

**Extensibility:**
```yaml
# Add new tool by editing YAML - no code changes
tools:
  gemini-cli:
    binary: gemini
    command_template: "{binary} --model {model} < {prompt_file}"
    models: [gemini-1.5-pro, gemini-1.5-flash]
    env_vars:
      GOOGLE_API_KEY: "${GOOGLE_API_KEY}"
```

**Simplicity:**
- ~100 lines of generic adapter code vs. ~400 lines per concrete adapter
- Single adapter handles all tools (claude-code, codex, gemini, future tools)

**Maintenance:**
- Changes to adapter logic happen in one place
- Tool-specific configuration in YAML (easy to update)

### Test Strategy

**Integration tests are kept as documentation:**
- `tests/integration/adapters/test_claude_code_adapter.py` - Validates claude-code integration
- `tests/fixtures/fake_claude_cli.py` - Mock CLI for testing
- Can add similar tests for other tools (codex, gemini) as needed

These tests:
1. Document expected tool behavior
2. Validate generic adapter works with different tools
3. Serve as examples for community contributors

### Consequences

**Positive:**
1. ✅ Faster development (one adapter vs. many)
2. ✅ More extensible (YAML config vs. code)
3. ✅ Easier community contributions
4. ✅ Lower maintenance burden
5. ✅ Test fixtures provide clear documentation

**Trade-offs:**
1. ⚠️ Less tool-specific optimization (acceptable for MVP)
2. ⚠️ Complex tools might need custom normalizers (handled via pluggable normalizers)
3. ⚠️ Must ensure generic adapter handles edge cases (validated by integration tests)

### Migration Plan

**Phase 1: Implement Generic Adapter (Immediate)**
- Task: `2026-02-05T1000-backend-dev-generic-yaml-adapter.yaml`
- Deliverable: `src/llm_service/adapters/generic_adapter.py`
- Uses existing infrastructure from Batch 2.1
- Estimated effort: 2-3 hours

**Phase 2: Update Routing Engine (Next Batch)**
- Integrate `GenericYAMLAdapter` with routing engine
- Remove concrete adapter dependency
- Keep ClaudeCodeAdapter for tests only

**Phase 3: Documentation (Concurrent)**
- Update README with YAML-based tool addition
- Document how to add new tools
- Provide YAML templates for common tools

---

**Decision Rationale:** Generic adapter maximizes extensibility and minimizes code duplication while maintaining test coverage and documentation through integration test fixtures. ClaudeCodeAdapter validated the infrastructure and now serves as reference implementation.

**Approved By:** Human-in-Charge  
**Date:** 2026-02-05
