# Next Batch Recommendation

**Updated:** 2026-02-06 11:15:00 UTC
**Prepared By:** Planning Petra
**Status:** 🟢 **READY FOR ASSIGNMENT**

---

## Recent Completion ✅

**Batch:** Dashboard Integration Wiring (2026-02-06)
- **Duration:** 1.5h actual vs 2.0h estimated (25% faster)
- **Tasks Completed:** 3/3
  - CORS configuration (verified already complete)
  - File watcher integration (completed with tests)
  - Telemetry integration (completed with tests)
- **Test Results:** 17/17 dashboard tests passing
- **Agent:** Backend-dev (Backend Benny)
- **Work Log:** `work/reports/logs/backend-dev/2026-02-06-dashboard-integration-wiring.md`

**Status:** Dashboard integration wiring complete. Dashboard is now production-ready with:
- ✅ WebSocket server with real-time communication
- ✅ CORS properly configured
- ✅ File watcher integration for task monitoring
- ✅ Telemetry integration for cost metrics
- ✅ All tests passing

---

## Next Batch Options

### Option 1: Additional Dashboard Features (COULD)

**Tasks in Inbox:**
1. `2026-02-05T1400-backend-dev-rich-terminal-ui.yaml` - Rich terminal UI (MEDIUM priority)
2. `2026-02-05T1401-backend-dev-template-config-generation.yaml` - Template config generation (MEDIUM priority)

**Estimated Duration:** 1 day (4-6 hours)
**Strategic Value:** ⭐⭐ Nice-to-have enhancements
**Recommendation:** DEFER - Dashboard core complete, focus on LLM-service layer

---

### Option 2: M2 Batch 2.3 - Generic YAML Adapter (HIGH) ⭐⭐⭐⭐⭐

**Batch ID:** `2026-02-05-llm-service-m2-batch-2.3`
**Strategic Importance:** Critical path for LLM-service layer completion

**Tasks (3 Total):**
1. GenericYAMLAdapter Implementation (HIGH, 2-3h)
2. ENV Variables in YAML Schema (MEDIUM, 1-2h)
3. Integration with Routing Engine (HIGH, 2-3h)

**Estimated Duration:** 1 day (5-8 hours)
**Strategic Value:** ⭐⭐⭐⭐⭐ Completes M2 strategic pivot
**Dependencies:** All met ✅ (M2 Batches 2.1 & 2.2 complete)
**Recommendation:** **EXECUTE NEXT** - Critical for LLM-service layer

**Why This Batch:**
- Completes M2 Tool Integration milestone
- Enables YAML-driven tool extensibility (add tools via config, not code)
- Unblocks M3 Telemetry Infrastructure
- High strategic value for project goals

**See Full Details:** Detailed batch plan preserved below (scroll down)

---

### Option 3: Specification Creation (MEDIUM)

**Task:** `2026-02-05T1400-writer-editor-spec-driven-primer.yaml`
**Estimated Duration:** Half day (3-4 hours)
**Strategic Value:** ⭐⭐⭐ Documentation and onboarding
**Recommendation:** DEFER - Complete LLM-service implementation first

---

## Planning Petra's Recommendation

**Execute Next:** **Option 2 - M2 Batch 2.3 (Generic YAML Adapter)**

**Rationale:**
1. **Critical Path:** Completes M2 Tool Integration milestone
2. **Strategic Pivot:** Enables YAML-driven extensibility (core project goal)
3. **Unblocks M3:** Telemetry infrastructure depends on M2 completion
4. **Dependencies Met:** All prerequisites complete (Batches 2.1 & 2.2 done)
5. **High Efficiency:** Backend-dev demonstrated 6x efficiency in previous batches

**Dashboard Status:** Complete and production-ready. Additional features are "nice-to-have" enhancements that can be deferred.

**Next Command:** `/iterate` (will execute M2 Batch 2.3)

---

## Overall Project Health: 🟢 ON TRACK

### LLM-Service Layer
- **Current Milestone:** M2 Tool Integration
- **Progress:** 75% complete (Batches 2.1-2.2 done, Batch 2.3 ready)
- **Next:** M2 Batch 2.3 - GenericYAMLAdapter (5-8h estimated)
- **After That:** M3 Telemetry Infrastructure

### Dashboard
- **Status:** ✅ 100% complete (integration wiring done)
- **Production Ready:** Yes
- **Tests:** 17/17 passing
- **Next:** Optional enhancements (deferred)

### Overall
- **Blockers:** None
- **Decisions Needed:** None
- **Timeline:** On track for milestone targets
- **Risk Level:** LOW

---

## Task Queue Summary

**Inbox (4 tasks):**
- 2 LLM-service tasks (HIGH priority - M2 Batch 2.3) ← **NEXT**
- 1 Dashboard enhancement (MEDIUM - deferred)
- 1 Template config (MEDIUM - deferred)
- 1 Spec creation (MEDIUM - deferred)

**Active:** None (batch just completed)

**Done (today):**
- 3 Dashboard integration tasks (CORS, file watcher, telemetry)

---

# M2 Batch 2.3 - Generic YAML Adapter (Full Details)

**Batch ID**: `2026-02-05-llm-service-m2-batch-2.3`
**Created**: 2026-02-05
**Updated**: 2026-02-06 11:15:00 UTC
**Prepared By**: Planning Petra
**Status**: 🟢 **READY FOR ASSIGNMENT**
**Estimated Duration**: 1 day (5-8 hours)

---

## ⭐ Strategic Context: Generic YAML-Driven Adapter Pivot

**Decision Date:** 2026-02-05
**Decision Maker:** Human-in-Charge
**Reference:** ADR-029 updated, Architecture review in `work/analysis/generic-yaml-adapter-architecture-review.md`

**Strategic Pivot:**
- **FROM:** Multiple concrete adapter classes (ClaudeCodeAdapter, CodexAdapter, etc.)
- **TO:** Single GenericYAMLAdapter that reads tool definitions from YAML
- **IMPACT:** Add new tools via configuration, not code changes

**Rationale:**
1. **Eliminates Code Duplication:** One adapter handles all tools
2. **YAML-Driven Extensibility:** Community can add tools via config
3. **Faster to MVP:** Reduced implementation scope (1 adapter vs. N adapters)
4. **Maintainability:** Changes to YAML, not code deployments
5. **Alignment:** Matches YAML-driven design philosophy throughout service

**ClaudeCodeAdapter Status:**
- ✅ **Kept as reference implementation** - Documents best practices
- ✅ **Kept as test fixture** - `fake_claude_cli.py` used in tests
- ✅ **Validates infrastructure** - Proved Batch 2.1 base classes work
- ❌ **Not production path** - GenericYAMLAdapter is production implementation

---

## Batch Objective

Implement **Generic YAML-Driven Adapter** for LLM Service Layer (Milestone 2):

1. **GenericYAMLAdapter class** - Single adapter for all tools
2. **ENV variable support** - YAML schema enhancement for API keys
3. **Routing integration** - Update routing engine to use generic adapter
4. **Demonstration** - Add new tool (codex) via YAML without code changes

**Success Criteria**:
- GenericYAMLAdapter works with any YAML-defined tool ✓
- ENV variables configurable in YAML (${VAR} expansion) ✓
- Routing engine uses GenericYAMLAdapter for all tools ✓
- Add codex tool via YAML without code changes ✓
- >80% test coverage maintained ✓
- M2 Batch 2.3 complete - ready for M3 (Telemetry) ✓

---

## Context: M2 Batches 2.1 & 2.2 Complete

**Achievement:** ✅ M2 Batch 2.1 & 2.2 COMPLETE
- ✅ Batch 2.1: Adapter infrastructure (~2.5h, 84% faster than estimate)
- ✅ Batch 2.2: ClaudeCodeAdapter reference implementation
- ✅ 93% test coverage, 78/78 tests passing
- ✅ Architecture approved for generic adapter approach
- ✅ NO BLOCKERS for Batch 2.3 start

**Previous Batch Performance:**
- Agent: Backend-dev Benny
- Efficiency: ⭐ 6.4x faster than initial estimates
- Quality: 93% coverage, zero test failures
- Delivery: Infrastructure ready for production adapter

**Why M2 Batch 2.3 Now:**
- Foundation complete: Base classes, template parser, subprocess executor
- Strategic decision approved: Generic YAML adapter approach
- Reference implementation validates infrastructure works
- Ready for production adapter implementation

---

## Selected Tasks (3 Total - Milestone 2 Batch 2.3)

### Task 1: GenericYAMLAdapter Implementation

- **ID**: `2026-02-05T1000-backend-dev-generic-yaml-adapter`
- **Agent**: backend-dev (Benny)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 2-3 hours
- **Mode**: Implementation
- **Strategic Value**: ⭐⭐⭐⭐⭐ Production adapter enabling YAML-driven extensibility

**Why This Task:**
- Implements single adapter that works with ANY YAML-defined tool
- Replaces need for concrete adapter classes per tool
- Enables community to add tools via YAML configuration
- Critical path for M2 completion and Milestone 3 readiness

**Implementation Requirements:**
1. GenericYAMLAdapter class in `src/llm_service/adapters/generic_adapter.py`
2. Extends `ToolAdapter` base class from Batch 2.1
3. Methods to implement:
   - `__init__(tool_name: str, tool_config: ToolConfig)` - Constructor
   - `execute(prompt: str, model: str, params: Dict) -> ToolResponse` - Main execution
   - `_resolve_binary() -> str` - Binary path resolution (config > which > platform)
   - `_prepare_env(params: Dict) -> Dict[str, str]` - ENV variable preparation
   - `_validate_model(model: str) -> None` - Model validation against config
4. Binary resolution priority:
   - tool_config.binary_path (if set) - config override
   - shutil.which(tool_config.binary) - system PATH
   - tool_config.platforms[current_platform] - platform default
5. Command generation using TemplateParser from Batch 2.1
6. Error handling:
   - BinaryNotFoundError with installation instructions
   - InvalidModelError with supported models list
   - ExecutionError with context from SubprocessExecutor

**Deliverables**:
1. `src/llm_service/adapters/generic_adapter.py`
   - GenericYAMLAdapter class (~200-300 lines)
   - Binary resolution logic
   - Model validation
   - ENV variable handling
2. Unit tests (6-8 tests):
   - Basic execution flow
   - Binary resolution (config, PATH, platform)
   - Model validation
   - ENV variable preparation
   - Error handling scenarios

**Dependencies**: Batches 2.1 & 2.2 complete ✅

**Success Criteria**:
- GenericYAMLAdapter passes all unit tests (>80% coverage)
- Works with claude-code tool using existing YAML config
- Binary resolution follows priority order correctly
- Model validation prevents unsupported models
- Error messages are user-friendly
- Ready for routing engine integration (Task 3)

---

### Task 2: ENV Variables in YAML Schema

- **ID**: `2026-02-05T1001-backend-dev-yaml-env-vars`
- **Agent**: backend-dev (Benny)
- **Priority**: MEDIUM
- **Status**: Ready to assign
- **Estimated Effort**: 1-2 hours
- **Mode**: Implementation
- **Strategic Value**: ⭐⭐⭐⭐ Enables declarative ENV var management

**Why This Task:**
- Extends YAML schema to support tool-specific environment variables
- Enables ${VAR} expansion from system environment (API keys)
- Validates required ENV vars at config load time
- Makes ENV var management declarative, not code-based

**Implementation Requirements:**
1. Update ToolConfig schema in `src/llm_service/config/schemas.py`:
   - Add `env_vars: Optional[Dict[str, str]]` field
   - Add `env_required: Optional[List[str]]` field
   - Add validator for ${VAR} expansion (os.path.expandvars)
   - Add validator for env_required (check vars exist in os.environ)
2. Update GenericYAMLAdapter to use tool_config.env_vars:
   - Merge config env_vars with params["env"] (if provided)
   - Config env_vars have lower priority than params override
3. Update YAML examples:
   ```yaml
   tools:
     claude-code:
       env_vars:
         ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"
         CLAUDE_HOME: "${HOME}/.claude"
       env_required:
         - ANTHROPIC_API_KEY
   ```
4. Error handling:
   - ValidationError if required ENV var missing
   - Clear message: "Required environment variable ANTHROPIC_API_KEY not set"

**Deliverables**:
1. `src/llm_service/config/schemas.py` - Updated ToolConfig
2. `config/tools.yaml.example` - Example ENV var usage
3. Unit tests (4-6 tests):
   - ${VAR} expansion works correctly
   - env_required validation fails if var missing
   - env_vars field is optional (backward compatible)
   - env_vars merge with params correctly

**Dependencies**: Task 1 (GenericYAMLAdapter implementation)

**Success Criteria**:
- ToolConfig schema validates env_vars and env_required
- ${VAR} expansion uses os.path.expandvars correctly
- Validation fails with clear message if required var missing
- GenericYAMLAdapter uses env_vars from config
- Example configs show ENV var usage
- Tests passing with >80% coverage

---

### Task 3: Integration with Routing Engine

- **ID**: `2026-02-05T1002-backend-dev-routing-integration`
- **Agent**: backend-dev (Benny)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 2-3 hours
- **Mode**: Integration & Testing
- **Strategic Value**: ⭐⭐⭐⭐⭐ Completes M2 Batch 2.3, proves YAML extensibility

**Why This Task:**
- Integrates GenericYAMLAdapter with routing engine
- Replaces concrete adapter usage with generic adapter
- Demonstrates adding new tool (codex) via YAML without code changes
- Completes M2 Batch 2.3 strategic pivot

**Implementation Requirements:**
1. Update AdapterFactory in `src/llm_service/routing/adapter_factory.py`:
   - Replace concrete adapter imports with GenericYAMLAdapter
   - get_adapter(tool_name) creates GenericYAMLAdapter with tool_config
   - Remove tool-specific conditionals (if any)
2. Validate RoutingEngine uses adapter_factory.get_adapter():
   - No tool-specific logic in routing
   - All tool behavior driven by YAML config
3. Update tests:
   - Adapter factory creates GenericYAMLAdapter for all tools
   - End-to-end routing with GenericYAMLAdapter
   - Add test: "Add new tool via YAML" (e.g., gemini-cli)
4. Update example configs:
   - Add codex tool to tools.yaml.example
   - Show how to add tools without code changes

**Deliverables**:
1. `src/llm_service/routing/adapter_factory.py`
   - Updated to use GenericYAMLAdapter
   - No concrete adapter imports (production code)
2. `tests/unit/routing/test_adapter_factory.py`
   - Factory creates GenericYAMLAdapter
   - Works for multiple tools
   - Tool not found error handling
3. `tests/integration/routing/test_end_to_end_routing.py`
   - Route to claude-code via YAML
   - Route to codex via YAML (new tool)
   - ENV variables passed correctly
   - Add gemini-cli via YAML test
4. `config/tools.yaml.example`
   - Add codex tool definition

**Dependencies**: Tasks 1-2 (GenericYAMLAdapter + ENV vars)

**Success Criteria**:
- AdapterFactory creates GenericYAMLAdapter for all tools
- Routing tests pass with GenericYAMLAdapter
- No concrete adapter imports in production code
- Integration test demonstrates adding new tool via YAML
- >80% test coverage on routing engine
- ClaudeCodeAdapter only used in test fixtures
- M2 Batch 2.3 complete - ready for M3

---

## Execution Plan

### Phase 1: Generic Adapter Implementation (Hours 0-3)

**Sequential Execution:**
```
Task 1: GenericYAMLAdapter Implementation  [2-3h]  HIGH  (backend-dev)
```

**Characteristics:**
- Leverages Batch 2.1 infrastructure (base class, template parser, subprocess executor)
- ClaudeCodeAdapter proves the pattern works (reference implementation)
- Core production adapter for YAML-driven extensibility
- Single adapter replaces N concrete adapters

**Time Estimate:** Half day (2-3 hours)

---

### Phase 2: Schema & Integration (Hours 3-8)

**Sequential Execution (Depends on Task 1):**
```
Task 2: ENV Variable YAML Schema  [1-2h]  MEDIUM  (depends on Task 1)
Task 3: Routing Integration       [2-3h]  HIGH    (depends on Tasks 1-2)
```

**Characteristics:**
- Task 2 enhances YAML schema with ENV var support
- Task 3 integrates GenericYAMLAdapter with routing engine
- Both depend on GenericYAMLAdapter (Task 1)
- Demonstrates YAML-driven tool addition

**Time Estimate:** Half day (3-5 hours)

---

## Timeline & Resource Allocation

**Estimated Duration:** 1 day (5-8 hours)
**Agent:** Backend-dev (Benny)
**Complexity:** LOW-MEDIUM

**Timeline Estimates:**
- **Optimistic** (Based on Batch 2.1 Efficiency): 5-6 hours
- **Realistic** (Conservative Estimate): 1 day (5-8 hours)
- **Recommended:** Plan for 1 day with buffer for validation

---

## Success Metrics

### Task-Level Metrics
- ✅ 3/3 tasks completed within 1 day
- ✅ All unit tests passing (no failures)
- ✅ >80% test coverage on GenericYAMLAdapter
- ✅ Integration tests passing with YAML-defined tools
- ✅ Code follows Python style guide (PEP 8)

### Strategic Metrics
- ✅ GenericYAMLAdapter production-ready
- ✅ Add new tool (codex) via YAML without code changes
- ✅ M2 Batch 2.3 complete - strategic pivot delivered
- ✅ ENV variable support enables API key management
- ✅ Routing engine fully YAML-driven (no tool-specific code)

---

**Prepared By**: Planning Petra
**Date**: 2026-02-06 11:15:00 UTC
**Status**: 🟢 **READY FOR ASSIGNMENT**
**Recommended Start**: Immediate
**Expected Completion**: 1 day (5-8 hours with buffer)

**Next Steps**:
1. Use `/iterate` to execute M2 Batch 2.3
2. Monitor progress per checkpoint schedule
3. Review GenericYAMLAdapter after Task 1 (key deliverable)
4. Validate YAML extensibility demo (add codex tool) after Task 3
5. Approve Milestone 3 kickoff (Telemetry & Cost Optimization) after completion
