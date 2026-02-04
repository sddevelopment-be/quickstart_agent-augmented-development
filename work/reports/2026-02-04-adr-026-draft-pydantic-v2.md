# ADR Template: Pydantic V2 for Schema Validation

**ADR Number:** 026  
**Title:** Use Pydantic V2 for Configuration Schema Validation  
**Status:** Draft (Needs Approval)  
**Date:** 2026-02-04  
**Decision-Makers:** Backend-dev (Benny), Architect Alphonso  
**Context:** LLM Service Layer Milestone 1 - Configuration validation framework selection

---

## Context

The LLM Service Layer requires robust validation of YAML configuration files (agents.yaml, tools.yaml, models.yaml, policies.yaml). Configuration validation must:

1. **Type Safety:** Enforce correct data types (strings, integers, lists, dicts)
2. **Field Validation:** Validate individual fields (e.g., costs ≥ 0, context windows > 0)
3. **Cross-Reference Validation:** Validate relationships between configs (e.g., agent's preferred_tool exists in tools.yaml)
4. **Developer Experience:** Provide clear error messages, IDE support, autocomplete

**Alternatives Considered:**

| Option | Pros | Cons |
|--------|------|------|
| **JSON Schema** | Language-agnostic, widely adopted | No native Python integration, verbose schema definitions |
| **Marshmallow** | Mature serialization library | More boilerplate, less type-safe than Pydantic |
| **attrs + validators** | Lightweight, simple | No built-in validation framework |
| **Pydantic v2** | Python-native, excellent DX, field validators | Pydantic-specific, V1→V2 migration issues in ecosystem |

---

## Decision

**We will use Pydantic v2 for configuration schema validation.**

**Key Implementation Details:**

1. **Configuration Models:**
   - Each YAML file maps to a Pydantic `BaseModel` subclass
   - Example: `AgentConfig`, `ToolConfig`, `ModelConfig`, `PolicyConfig`

2. **Field Validation:**
   - Use Pydantic `@field_validator` decorator for field-level validation
   - Example: Validate fallback chain format (`tool:model`), cost values ≥ 0

3. **Cross-Reference Validation:**
   - Separate validation function `validate_agent_references()` after all configs loaded
   - Validates agent references to tools/models exist and are compatible

4. **Error Handling:**
   - Pydantic `ValidationError` caught and converted to user-friendly `ConfigurationError`
   - Error messages include field path and specific validation failure

**Example Schema:**

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

---

## Rationale

### Why Pydantic V2?

1. **Excellent Developer Experience:**
   - Type hints provide IDE autocomplete and static analysis
   - Clear, actionable error messages
   - Python-native API (no schema DSL to learn)

2. **Comprehensive Validation:**
   - Field validators for custom logic
   - Cross-validation support via `@model_validator`
   - Built-in validators for common patterns (URLs, emails, etc.)

3. **Strong Type Safety:**
   - Runtime type checking matches static type hints
   - Automatic type coercion with strict mode option
   - Mypy integration for compile-time checks

4. **Proven in Production:**
   - Used by FastAPI, Hugging Face, LangChain
   - Large ecosystem, active community
   - Well-documented with extensive examples

### Why NOT JSON Schema?

- **Verbose:** Requires separate schema definition files or large dicts
- **No Type Integration:** JSON Schema doesn't provide Python type hints
- **Manual Validation:** Must manually validate parsed YAML against schema

### Why NOT Marshmallow?

- **More Boilerplate:** Requires separate schema classes and serialization methods
- **Less Type-Safe:** Type hints not enforced at runtime
- **Older Design:** Pre-dates modern Python type hints

### Why NOT attrs?

- **No Validation Framework:** Must implement validation logic manually
- **Limited Ecosystem:** Fewer integrations compared to Pydantic

### Why V2 Specifically?

Pydantic v2 offers significant improvements over v1:

- ✅ **Performance:** 5-10x faster validation (Rust core)
- ✅ **Better Error Messages:** More detailed validation errors
- ✅ **Improved API:** Cleaner decorator-based validators
- ⚠️ **Breaking Changes:** V1→V2 migration requires code updates (acceptable for new project)

---

## Consequences

### Positive Consequences

1. ✅ **Developer Productivity:** Fast iteration with type-safe schemas
2. ✅ **Configuration Quality:** Catches errors before execution (fail-fast)
3. ✅ **Maintainability:** Schema changes localized to Pydantic models
4. ✅ **Testing:** Easy to instantiate models for unit tests

### Negative Consequences

1. ⚠️ **Learning Curve:** Team must learn Pydantic-specific patterns
2. ⚠️ **Dependency:** Pydantic is external dependency (acceptable trade-off)
3. ⚠️ **V2 Migration:** Future Pydantic upgrades may require migration

### Mitigation Strategies

**Learning Curve:**
- Document common patterns in `docs/architecture/patterns/`
- Provide examples in `src/llm_service/config/schemas.py`

**Dependency Management:**
- Pin Pydantic version in `requirements.txt`: `pydantic>=2.0,<3.0`
- Monitor Pydantic releases for security updates

**V2 Migration:**
- Acceptable risk: Pydantic v2 is stable (released 2023)
- V2→V3 migration (future) will be well-documented by Pydantic team

---

## Alternatives Rejected

### Alternative 1: JSON Schema + jsonschema library

**Why Rejected:**
- No Python type integration
- Verbose schema definitions
- Must manually map validation errors to user-friendly messages

### Alternative 2: Marshmallow

**Why Rejected:**
- More boilerplate code
- Less type-safe than Pydantic
- Pre-dates modern Python type hints

### Alternative 3: attrs + custom validators

**Why Rejected:**
- No validation framework (must implement manually)
- Smaller ecosystem compared to Pydantic

---

## Implementation Evidence

**Files Implementing This Decision:**

- `src/llm_service/config/schemas.py` - Pydantic models for all schemas
- `src/llm_service/config/loader.py` - Uses Pydantic validation during YAML loading
- `tests/unit/config/test_schemas.py` - Comprehensive validation tests (25 tests, 100% coverage)

**Key Metrics:**

- ✅ **100% schema coverage** - All validation paths tested
- ✅ **25 validation tests** - Field validators, cross-references, edge cases
- ✅ **93% overall coverage** - Configuration layer thoroughly tested

**Example Validation Error:**

```
Configuration validation failed:
  - Agent 'backend-dev' references unknown tool: nonexistent-tool
  - Agent 'backend-dev' preferred_model 'gpt-4' is not supported by tool 'claude-code'
  - Agent 'planner' fallback references unknown model: invalid-model
```

---

## References

**Documentation:**
- Pydantic V2 Docs: https://docs.pydantic.dev/latest/
- Migration Guide: https://docs.pydantic.dev/latest/migration/

**Related ADRs:**
- ADR-025: LLM Service Layer for Agent-Tool Orchestration
- ADR-028: Tool-Model Compatibility Validation (uses Pydantic cross-validation)

**Related Documents:**
- `src/llm_service/README.md` - Configuration examples
- `docs/architecture/design/llm-service-layer-prestudy.md` - Original architecture vision

---

## Review Notes

**Approvers Needed:**
- Backend-dev (implementer)
- Architect Alphonso (architecture review)
- Human-in-Charge (strategic approval)

**Review Checklist:**
- [ ] Rationale clearly explains trade-offs
- [ ] Alternatives considered and rejected with justification
- [ ] Consequences (positive and negative) documented
- [ ] Implementation evidence provided
- [ ] Related ADRs cross-referenced

---

**Status:** Draft  
**Created By:** Architect Alphonso (based on Milestone 1 implementation)  
**Date:** 2026-02-04  
**Next Step:** Submit for review and approval
