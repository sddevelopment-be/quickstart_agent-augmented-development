# ADR-026: Use Pydantic V2 for Configuration Schema Validation

**status**: Accepted  
**date**: 2026-02-04

## Context

The LLM Service Layer requires robust validation of YAML configuration files (`agents.yaml`, `tools.yaml`, `models.yaml`, `policies.yaml`). Configuration validation must provide:

1. **Type Safety**: Enforce correct data types (strings, integers, lists, dictionaries)
2. **Field Validation**: Validate individual fields (e.g., costs ≥ 0, context windows > 0)
3. **Cross-Reference Validation**: Validate relationships between configs (e.g., agent's `preferred_tool` exists in `tools.yaml`)
4. **Developer Experience**: Provide clear error messages, IDE support, and autocomplete

During Milestone 1 implementation (2026-02-04), the team needed to select a validation framework. The choice needed to balance developer productivity, type safety, and maintainability while supporting complex validation scenarios including field-level validation and cross-configuration reference checking.

**Key Forces:**
- Need for runtime validation of external YAML files
- Desire for strong Python type integration for IDE support
- Requirement for clear, actionable error messages for configuration issues
- Team familiarity with Python type hints and modern Python patterns
- Trade-off between framework complexity and validation capability

**Reference Documentation:**
- Technical Prestudy: `docs/architecture/design/llm-service-layer-prestudy.md`
- Implementation: `src/llm_service/config/schemas.py`
- Implementation Plan: `docs/planning/llm-service-layer-implementation-plan.md`

## Decision

**We will use Pydantic v2 for configuration schema validation in the LLM Service Layer.**

Pydantic v2 will be used to:
1. Define configuration models as Python classes with type hints
2. Validate YAML content during configuration loading
3. Provide field-level validators for custom validation logic
4. Support cross-configuration validation after all files are loaded

**Key Implementation Pattern:**

```python
from pydantic import BaseModel, Field, field_validator

class AgentConfig(BaseModel):
    preferred_tool: str = Field(..., description="Default tool for this agent")
    preferred_model: str = Field(..., description="Default model for this agent")
    fallback_chain: List[str] = Field(default_factory=list)
    
    @field_validator('fallback_chain')
    @classmethod
    def validate_fallback_format(cls, v):
        for entry in v:
            if ':' not in entry:
                raise ValueError(f"Fallback entry must be 'tool:model' format: {entry}")
        return v
```

Validation occurs in two stages:
1. **Schema Validation**: Each YAML file is validated against its Pydantic model during load
2. **Cross-Reference Validation**: A separate `validate_agent_references()` function validates relationships after all configurations are loaded

## Rationale

### Why Pydantic V2?

**Strengths:**
1. **Excellent Developer Experience**
   - Type hints provide IDE autocomplete and static analysis
   - Clear, actionable error messages with field paths
   - Python-native API with no DSL to learn
   - Comprehensive documentation and examples

2. **Comprehensive Validation Framework**
   - Decorator-based field validators for custom logic
   - Model validators for cross-field validation
   - Built-in validators for common patterns (URLs, emails, ranges)
   - Automatic type coercion with strict mode option

3. **Strong Type Safety**
   - Runtime type checking matches static type hints
   - Mypy integration for compile-time checks
   - Type hints surfaced in IDE for better discovery

4. **Proven Production Track Record**
   - Used by FastAPI, Hugging Face, LangChain, SQLModel
   - Large ecosystem with extensive plugin support
   - Active community and regular updates
   - Battle-tested in production systems

5. **Performance and Modern Design**
   - V2 uses Rust core for 5-10x faster validation
   - Improved error messages over V1
   - Cleaner decorator-based API in V2
   - Active development with long-term support

**Trade-offs Accepted:**
1. **Learning Curve**: Team must learn Pydantic-specific patterns and decorators
   - *Mitigation*: Excellent documentation, pattern examples in codebase, strong community
   
2. **External Dependency**: Adds Pydantic as a required dependency
   - *Mitigation*: Acceptable for the significant value provided; dependency is stable and well-maintained
   
3. **V2 Breaking Changes**: Pydantic V2 has breaking changes from V1
   - *Mitigation*: Acceptable for new project; V2 is stable (released 2023) with long-term support

### Why NOT Alternative Options?

**JSON Schema + jsonschema library:**
- ❌ No native Python type integration or IDE support
- ❌ Verbose schema definitions (separate from Python code)
- ❌ Manual error message formatting required
- ❌ Separate validation step from type definitions

**Marshmallow:**
- ❌ More boilerplate code required
- ❌ Less type-safe than Pydantic (types not enforced at runtime)
- ❌ Pre-dates modern Python type hints (older design patterns)
- ❌ Separate schema classes from data classes

**attrs + custom validators:**
- ❌ No built-in validation framework (must implement manually)
- ❌ Smaller ecosystem compared to Pydantic
- ❌ No field validation decorators
- ❌ More code required for equivalent validation

**Raw dict validation:**
- ❌ No type safety or IDE support
- ❌ Verbose and error-prone validation code
- ❌ Poor error messages without significant effort
- ❌ High maintenance burden

### Why Pydantic V2 Specifically Over V1?

Pydantic v2 offers significant improvements:
- ✅ **5-10x faster validation** (Rust-based core)
- ✅ **Better error messages** with more detail and context
- ✅ **Cleaner API** with improved decorator patterns
- ✅ **Long-term support** (V2 is the future)
- ⚠️ **Breaking changes** from V1 (acceptable for new projects)

## Envisioned Consequences

### Positive Consequences

1. ✅ **Developer Productivity**
   - Fast iteration with type-safe schemas
   - IDE autocomplete for configuration fields
   - Clear validation errors guide fixes
   - Reduced debugging time

2. ✅ **Configuration Quality**
   - Catches errors before execution (fail-fast)
   - Validates relationships between configurations
   - Prevents invalid configurations from loading
   - Consistent validation across all config files

3. ✅ **Maintainability**
   - Schema changes localized to Pydantic models
   - Type hints serve as inline documentation
   - Easy to add new validation rules
   - Test-friendly models (easy to instantiate)

4. ✅ **User Experience**
   - Helpful error messages with field context
   - Example error: `"Agent 'backend-dev' references unknown tool: nonexistent-tool"`
   - Clear guidance on fixing configuration issues

### Negative Consequences

1. ⚠️ **Learning Curve**
   - Team must learn Pydantic patterns and decorators
   - Understanding field validators and model validators required
   - *Mitigation*: Pattern examples documented in `src/llm_service/config/schemas.py`

2. ⚠️ **External Dependency**
   - Adds Pydantic as required dependency
   - Version pinning required: `pydantic>=2.0,<3.0`
   - *Mitigation*: Acceptable trade-off; Pydantic is stable and widely-used

3. ⚠️ **Future Migration Risk**
   - V2→V3 migration may require code changes (future)
   - *Mitigation*: V2 is stable with long-term support; migration will be well-documented

### Risk Mitigation Strategies

**Learning Curve:**
- Provide pattern documentation in `docs/architecture/patterns/`
- Include comprehensive examples in `src/llm_service/config/schemas.py`
- Reference Pydantic official docs for detailed guidance

**Dependency Management:**
- Pin Pydantic version: `pydantic>=2.0,<3.0`
- Monitor Pydantic releases for security updates
- Include in dependency review process

**Future Migration:**
- Document Pydantic usage patterns for easier migration
- Monitor Pydantic roadmap for V3 planning
- V2 expected to have long-term support (multi-year)

## Considered Alternatives

### Alternative 1: JSON Schema with jsonschema library

**Description:** Define schemas as JSON Schema documents and validate YAML after parsing.

**Pros:**
- Language-agnostic schema definition
- Widely adopted standard
- Tool support for schema generation

**Cons:**
- No native Python integration
- Verbose schema definitions
- Manual error message formatting
- Separate validation from type definitions

**Rejected Because:** Poor developer experience, no IDE support, verbose definitions.

### Alternative 2: Marshmallow

**Description:** Use Marshmallow for serialization and validation.

**Pros:**
- Mature library with extensive features
- Serialization and deserialization support
- Field-level validation

**Cons:**
- More boilerplate code
- Less type-safe than Pydantic
- Pre-dates modern Python type hints
- Separate schemas from data classes

**Rejected Because:** More boilerplate, less type-safe, older design patterns.

### Alternative 3: attrs with custom validators

**Description:** Use attrs for data classes and implement custom validation logic.

**Pros:**
- Lightweight and simple
- Good for basic validation
- Minimal dependencies

**Cons:**
- No built-in validation framework
- Must implement validation manually
- Smaller ecosystem than Pydantic
- More code for equivalent validation

**Rejected Because:** No validation framework, more manual effort, smaller ecosystem.

## Implementation Evidence

**Configuration Schema Implementation:**
- `src/llm_service/config/schemas.py` - All Pydantic models (AgentConfig, ToolConfig, ModelConfig, PolicyConfig)
- `src/llm_service/config/loader.py` - Uses Pydantic validation during YAML loading

**Test Coverage:**
- `tests/unit/config/test_schemas.py` - 25 validation tests covering all validation paths
- **100% schema coverage** - All validation rules tested
- **93% overall coverage** - Configuration layer thoroughly tested

**Example Validation Error:**
```
Configuration validation failed:
  - Agent 'backend-dev' references unknown tool: nonexistent-tool
  - Agent 'backend-dev' preferred_model 'gpt-4' is not supported by tool 'claude-code'
  - Agent 'planner' fallback references unknown model: invalid-model
```

**Key Achievements:**
- ✅ Field-level validation with custom decorators
- ✅ Cross-reference validation between configurations
- ✅ Clear error messages with field context
- ✅ Type-safe configuration loading

## References

**External Documentation:**
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Pydantic V1→V2 Migration Guide](https://docs.pydantic.dev/latest/migration/)

**Related ADRs:**
- [ADR-025: LLM Service Layer for Agent-Tool Orchestration](ADR-025-llm-service-layer.md) - Approved architecture
- ADR-028: Tool-Model Compatibility Validation (uses Pydantic cross-validation)

**Related Documents:**
- `docs/architecture/design/llm-service-layer-prestudy.md` - Original architecture vision
- `docs/planning/llm-service-layer-implementation-plan.md` - Implementation roadmap
- `src/llm_service/README.md` - Configuration examples and usage

---

**Decision Made By:** Backend-dev Benny (implementation), Architect Alphonso (architecture review)  
**Date:** 2026-02-04  
**Status:** Accepted (Milestone 1 implementation complete, 93% test coverage achieved)
