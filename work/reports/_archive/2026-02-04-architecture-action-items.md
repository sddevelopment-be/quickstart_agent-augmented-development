# Architecture Action Items - LLM Service Layer

**Review Date:** 2026-02-04  
**Architect:** Alphonso  
**Status:** Milestone 1 APPROVED, Action Items for M2 Prep

---

## ✅ Strategic Assessment

**Milestone 1 Quality Gate: PASS**

- ✅ All 10 acceptance criteria met or exceeded
- ✅ 93% test coverage (target: 80%)
- ✅ 100% alignment with ADR-025 prestudy vision
- ✅ Strong architectural integrity (clean separation, low coupling)
- ✅ Production-ready foundation for Milestone 2

**Recommendation:** **APPROVE** progression to Milestone 2 (Tool Integration)

---

## 📋 Required Documentation (Pre-Milestone 2)

### Priority: MEDIUM (2-3 hours total)

These tactical ADRs capture implementation decisions made during Milestone 1:

#### 1. ADR-026: Pydantic V2 for Schema Validation

**File:** `docs/architecture/adrs/ADR-026-pydantic-v2-validation.md`

**Key Decision:** Use Pydantic v2 instead of JSON Schema, Marshmallow, or attrs for configuration validation

**Trade-Offs:**
- ✅ Pro: Built-in field validators, cross-validation support, Python-native
- ✅ Pro: Strong type integration, IDE autocomplete
- ⚠️ Con: Pydantic-specific learning curve
- ⚠️ Con: V1→V2 migration breaking changes in ecosystem

**Rationale:** Pydantic v2 provides excellent developer experience and validation capabilities needed for complex cross-reference validation (e.g., tool-model compatibility check).

---

#### 2. ADR-027: Click for CLI Framework

**File:** `docs/architecture/adrs/ADR-027-click-cli-framework.md`

**Key Decision:** Use Click instead of argparse, Typer, or raw sys.argv for CLI interface

**Trade-Offs:**
- ✅ Pro: Mature ecosystem, excellent testing support (CliRunner)
- ✅ Pro: Subcommand/group composition, automatic help generation
- ⚠️ Con: Not type-safe by default (unlike Typer)
- ⚠️ Con: Less performant than argparse (acceptable for CLI use case)

**Rationale:** Click's testing support (CliRunner) and mature ecosystem outweigh performance concerns for CLI use case.

---

#### 3. ADR-028: Tool-Model Compatibility Validation

**File:** `docs/architecture/adrs/ADR-028-tool-model-compatibility-validation.md`

**Key Decision:** Validate that agent's `preferred_model` is supported by `preferred_tool` during configuration validation

**Context:** This enhancement was added by Backend-dev during implementation and was not in the original prestudy.

**Trade-Offs:**
- ✅ Pro: Prevents runtime errors when agent references unsupported model
- ✅ Pro: Improves configuration quality and catches errors early
- ⚠️ Con: Slightly stricter validation (could reject valid edge cases)

**Rationale:** Fail-fast validation prevents confusing runtime errors. Better to catch configuration issues at `config validate` time.

**Example Error Prevented:**
```yaml
# This would fail validation:
agents:
  backend-dev:
    preferred_tool: claude-code
    preferred_model: gpt-4  # ✗ claude-code doesn't support gpt-4
```

---

## 📋 Optional Documentation (Low Priority)

### Priority: LOW (3-4 hours total)

These documents enhance architectural understanding but are not blocking for Milestone 2:

#### 4. Design Doc: Routing Decision Precedence

**File:** `docs/architecture/design/routing-precedence-design.md`

**Purpose:** Formally document the routing decision chain logic

**Should Cover:**
- Why task_type override takes precedence over cost optimization
- Why fallback chains are linear rather than tree-structured
- Edge cases and decision rationale
- Precedence chain diagram

**Current State:** Logic is documented in code comments and README, but no formal design doc exists.

---

#### 5. Pattern Doc: Cross-Reference Validation Pattern

**File:** `docs/architecture/patterns/cross-reference-validation-pattern.md`

**Purpose:** Document the cross-reference validation pattern for future contributors

**Should Cover:**
- When to use Pydantic field validators vs. global validation function
- How to add new cross-reference checks
- Testing strategy for validation logic
- Extension points for custom validations

**Current State:** Pattern is implemented in `schemas.py::validate_agent_references()` but not documented as a reusable pattern.

---

## 🔍 Milestone 2 Planning Considerations

### Pre-M2 Review Items

Before starting Milestone 2 (Tool Integration), review these architectural decisions:

#### 1. Adapter Base Interface Design

**Decision Point:** How to define the base adapter interface?

**Options:**
1. **Abstract Base Class (ABC)**
   - ✅ Pro: Enforces interface contract at class definition time
   - ✅ Pro: Clear inheritance hierarchy
   - ⚠️ Con: More rigid, harder to mock

2. **Protocol (typing.Protocol)**
   - ✅ Pro: Structural subtyping (duck typing with type safety)
   - ✅ Pro: More flexible, easier to test
   - ⚠️ Con: Requires Python 3.8+ (we're on 3.10+, OK)

3. **Duck Typing (no formal interface)**
   - ✅ Pro: Maximum flexibility
   - ⚠️ Con: No compile-time safety
   - ⚠️ Con: Harder for contributors to understand expected behavior

**Recommendation:** Evaluate during M2 kickoff, document decision in **ADR-029: Tool Adapter Interface Pattern**

---

#### 2. Command Template Security

**Consideration:** Command template substitution could be an injection vector if YAML configuration is untrusted.

**Current Risk Level:** LOW (YAML files are trusted, versioned in Git)

**Example Risk:**
```yaml
# Malicious configuration (if YAML untrusted)
tools:
  malicious-tool:
    command_template: "{binary} {prompt_file}; rm -rf /"
```

**Mitigation Options:**
1. **Whitelist Placeholder Patterns** - Only allow `{binary}`, `{prompt_file}`, `{model}`, `{output_file}`
2. **Escape Shell Arguments** - Use `shlex.quote()` on all substitutions
3. **Use `subprocess` with `shell=False`** - Avoid shell interpretation entirely

**Recommendation:**
- Document security posture in **ADR-029** or separate security doc
- Implement mitigation #3 (`shell=False`) in tool adapters
- Add security testing for command template parsing

---

#### 3. Integration Testing Strategy

**Decision Point:** How to test tool adapters without requiring real LLM CLI tools?

**Options:**
1. **Mocked Subprocess** - Mock `subprocess.run()` to simulate tool responses
2. **Fake CLI Scripts** - Create fake `claude`/`codex` shell scripts for testing
3. **Recorded Responses** - VCR-style recording of real CLI interactions

**Recommendation:** Use **Option 2 (Fake CLI Scripts)** for M2 integration tests
- More realistic than mocks (tests actual command construction)
- No dependency on real API keys/accounts
- Portable across CI/CD environments

**Document in:** Milestone 2 planning docs or test strategy document

---

## 🎯 Strategic Recommendations Summary

### Immediate Actions (Before M2 Start)

1. ✅ **Create ADR-026, ADR-027, ADR-028** (2-3 hours)
   - Captures tactical decisions from M1 implementation
   - Preserves decision context for future maintainers
   - Satisfies Directive 018 (Traceable Decisions)

2. ✅ **Review Adapter Interface Options** (1 hour)
   - Prototype ABC vs. Protocol approach
   - Document decision in ADR-029 before M2 implementation starts

3. ✅ **Plan Command Template Security** (30 min)
   - Define injection prevention strategy
   - Document security posture

**Total Effort:** 4-6 hours (1 day buffer before M2)

---

### Milestone 2 Focus Areas

**Recommended priorities:**

1. **Adapter Base Interface** - Define clear contract for tool adapters
2. **Security Review** - Validate command template substitution safety
3. **Integration Testing** - Real tool execution with fake CLI scripts
4. **Error Handling** - Graceful degradation when tools fail (process crashes, rate limits)

**Risk Mitigation:**
- Prototype adapter interface early (1-2 day spike)
- Test with real claude/codex CLIs if available (optional, for validation)
- Document security assumptions explicitly

---

### Long-Term Considerations (M3 or Post-MVP)

Track these items in backlog for future milestones:

1. **Configuration Versioning** - Add `schema_version` field to YAML configs
2. **Logging Framework** - Implement structured logging for debugging
3. **CLI `config init` Command** - Functional implementation (currently placeholder)
4. **Migration Scripts** - For schema version upgrades

**Severity:** All items are **LOW priority** and non-blocking.

---

## 📊 Quality Gate Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Test Coverage | >80% | 93% | ✅ EXCEEDED |
| Passing Tests | 100% | 65/65 | ✅ PERFECT |
| Acceptance Criteria | 10/10 | 10/10 | ✅ COMPLETE |
| Architecture Alignment | High | 100% | ✅ EXCELLENT |
| Documentation | Complete | Comprehensive | ✅ STRONG |

**Milestone 1 Gate:** ✅ **PASS**

---

## 🚀 Progression Decision

**APPROVE** progression to **Milestone 2: Tool Integration**

**Justification:**
- ✅ Foundation is production-ready
- ✅ Architecture is sound and extensible
- ✅ No blocking technical debt
- ✅ Clear path forward for M2-M4

**Pre-M2 Requirements:**
- Document tactical ADRs (ADR-026, ADR-027, ADR-028)
- Review adapter interface options
- Plan command template security

**Estimated Pre-M2 Effort:** 4-6 hours (1 day)

---

## 📞 Next Actions

1. ✅ **Architect Alphonso:** Create ADR-026, ADR-027, ADR-028
2. ✅ **Planning Petra:** Update Milestone 2 task plan with adapter interface decision point
3. ✅ **Backend-dev:** Prepare for M2 start, review adapter architecture options
4. ✅ **Orchestrator:** Schedule M2 kickoff after ADRs complete

**Target M2 Start Date:** After ADR completion (1 day buffer)

---

**Prepared By:** Architect Alphonso  
**Date:** 2026-02-04  
**Status:** Action Items Identified  
**For:** Orchestrator / Planning Petra / Backend-dev
