# Next Batch: M2 Batch 2.3 - Generic YAML Adapter Implementation

**Batch ID**: `2026-02-05-llm-service-m2-batch-2.3`  
**Created**: 2026-02-05  
**Updated**: 2026-02-05 10:00:00 UTC  
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

### Timeline Estimates

**Optimistic** (Based on Batch 2.1 Efficiency): 5-6 hours
- Morning: Task 1 complete (GenericYAMLAdapter)
- Afternoon: Tasks 2-3 complete (schema + routing integration)
- Assumption: Benny maintains 6x efficiency from Batch 2.1

**Realistic** (Conservative Estimate): 1 day (5-8 hours)
- Morning: Tasks 1-2 complete (adapter + schema)
- Afternoon: Task 3 complete (routing integration)
- Buffer: 2 hours for integration testing + refinement

**Recommended:** Plan for 1 day with buffer for validation and demonstration

---

## Checkpoints & Milestones

### Checkpoint 1: Generic Adapter Complete (Half Day)
**Check**: Task 1 (GenericYAMLAdapter) complete  
**Expected**: 
- GenericYAMLAdapter class implemented and tested ✅
- Works with claude-code tool from YAML config ✅
- Binary resolution follows priority order ✅
- Unit tests passing (>80% coverage) ✅
**Decision**: Proceed to schema enhancement OR refine adapter  
**Trigger**: Backend-dev completes Task 1

### Checkpoint 2: ENV Variables & Schema Complete (Day 1 EOD)
**Check**: Task 2 (ENV var schema) complete  
**Expected**: 
- ToolConfig schema supports env_vars and env_required ✅
- ${VAR} expansion works correctly ✅
- Validation fails if required var missing ✅
- Example configs show ENV var usage ✅
**Decision**: Proceed to routing integration OR enhance schema  
**Trigger**: Backend-dev completes Task 2

### Checkpoint 3: M2 Batch 2.3 Complete (Day 1)
**Check**: All 3 tasks complete + integration tests passing  
**Expected**: 
- GenericYAMLAdapter production-ready ✅
- Routing engine uses GenericYAMLAdapter ✅
- Add codex tool via YAML demonstrated ✅
- All unit + integration tests passing (>80% coverage) ✅
- ClaudeCodeAdapter relegated to test fixtures ✅
- Ready for M3 (Telemetry & Cost Optimization) ✅
**Decision**: Start M3 OR validate with additional tools  
**Trigger**: All 3 tasks complete, human approval

---

## Resource Allocation

| Agent | Tasks | Total Hours | Complexity | Timeline |
|-------|-------|-------------|------------|----------|
| **backend-dev** | 3 | 5-8h | LOW-MEDIUM | 1 day |
| **Total** | **3 tasks** | **5-8h** | **Low-Medium** | **1 day** |

### Agent Workload: Backend-dev Benny

**Workload:** Moderate (5-8 hours over 1 day)
- Task 1: 2-3 hours (GenericYAMLAdapter implementation)
- Task 2: 1-2 hours (ENV variable schema enhancement)
- Task 3: 2-3 hours (Routing integration & tests)

**Characteristics:**
- Single agent (no coordination overhead)
- Low-Medium complexity (leverages Batches 2.1 & 2.2 work)
- High strategic value (completes M2 strategic pivot)
- Estimated based on Batch 2.1 efficiency (6x faster than initial estimates)
- Fits in 1 working day (optimistic) with 1-2h buffer

---

## Risk Assessment & Mitigation

### Risk 1: Generic Adapter Not Flexible Enough
**Description**: GenericYAMLAdapter can't handle tool-specific edge cases  
**Probability**: LOW  
**Impact**: MEDIUM (may need hybrid approach)  
**Mitigation**: 
- ClaudeCodeAdapter serves as reference implementation
- Can add tool-specific adapters later if needed
- Generic adapter supports extensibility hooks (OutputNormalizer)
- Start with 80% use case (most tools are simple CLIs)

### Risk 2: ENV Variable Validation Complexity
**Description**: Validating required ENV vars at config load may be too strict  
**Probability**: LOW  
**Impact**: LOW (usability concern)  
**Mitigation**:
- Make env_required optional (tools can skip validation)
- Validation happens at config load (fail-fast, clear errors)
- Document workarounds (config validation vs. runtime validation)
- Can defer validation to execution time if needed

### Risk 3: Routing Engine Tool-Specific Logic
**Description**: Routing engine may have tool-specific conditionals we haven't seen  
**Probability**: MEDIUM  
**Impact**: MEDIUM (adds 1-2h to Task 3)  
**Mitigation**:
- Review routing engine code in Task 3 before changes
- Refactor tool-specific logic to YAML config
- Document any edge cases that need concrete adapters
- Architecture review approved generic approach

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

### Value Realization
- **Immediate**: YAML-driven tool extensibility achieved
- **Short-term** (M3): Telemetry unblocked, ready for cost optimization
- **Long-term**: Community can contribute tools via YAML, not code

---

## Dependency Management

### Prerequisites (All Met ✅)

| Dependency | Status | Location | Notes |
|------------|--------|----------|-------|
| M1 Foundation Complete | ✅ | src/llm_service/ | 93% coverage, 65/65 tests |
| M2 Prep Complete | ✅ | ADRs 026-029 | All ADRs documented |
| M2 Batch 2.1 Complete | ✅ | src/llm_service/adapters/ | Base infrastructure ready |
| M2 Batch 2.2 Complete | ✅ | src/llm_service/adapters/ | Reference adapter validates pattern |
| Adapter Base Class | ✅ | base.py | ToolAdapter ABC ready |
| Command Template System | ✅ | command_template.py | Template handler ready |
| Subprocess Executor | ✅ | subprocess_executor.py | Execution wrapper ready |
| Test Infrastructure | ✅ | tests/ | 93% coverage, 78/78 tests |

### Internal Dependencies (This Batch)

**Task Dependencies:**
- Task 1 (GenericYAMLAdapter): Depends on Batches 2.1 & 2.2 (infrastructure + validation)
- Task 2 (ENV var schema): Depends on Task 1 (integrates with GenericYAMLAdapter)
- Task 3 (Routing integration): Depends on Tasks 1-2 (uses GenericYAMLAdapter + schema)

**Recommended Execution:**
- **Phase 1**: Task 1 (GenericYAMLAdapter implementation)
- **Phase 2**: Tasks 2-3 sequentially (Task 2 → Task 3)

---

## Handoff to Milestone 3

### Expected Outputs After This Batch

**Code:**
1. ✅ `src/llm_service/adapters/generic_adapter.py` - GenericYAMLAdapter class
2. ✅ `src/llm_service/config/schemas.py` - ENV variable schema support
3. ✅ `src/llm_service/routing/adapter_factory.py` - Uses GenericYAMLAdapter
4. ✅ YAML-driven tool extensibility proven (add tools via config)
5. ✅ ENV variable support for API keys and configuration

**Tests:**
1. ✅ `tests/unit/adapters/test_generic_adapter.py` - Unit tests (6-8 tests)
2. ✅ `tests/unit/config/test_schemas_env_vars.py` - Schema validation tests
3. ✅ `tests/integration/routing/test_end_to_end_routing.py` - E2E routing tests
4. ✅ `config/tools.yaml.example` - Updated with codex tool + ENV var examples

**Milestone 3 Readiness Checklist:**
- ✅ GenericYAMLAdapter production-ready
- ✅ Routing engine YAML-driven (no tool-specific code)
- ✅ ENV variable support for API keys
- ✅ Add tools via YAML demonstrated (codex example)
- ✅ >80% test coverage maintained
- ✅ M2 Batch 2.3 complete - ready for telemetry & cost optimization
- ✅ ClaudeCodeAdapter relegated to test fixtures

**Next Milestone (M3 - Cost Optimization & Telemetry):**
- Batch 3.1: Telemetry Infrastructure (SQLite, invocation logging)
- Batch 3.2: Policy Engine (budget tracking, cost optimization)
- Batch 3.3: Stats & Reporting (CLI stats command)
- Timeline: Week 3-4 (estimated)

---

## Alternative Batches

### Alternative 1: Minimal Scope (Adapter Only)

**If**: Backend-dev has limited availability  
**Execute**: Task 1 only (GenericYAMLAdapter implementation)  
**Duration**: Half day (2-3 hours)  
**Value**: Core adapter ready, schema and integration can be deferred

**Rationale**: GenericYAMLAdapter is the primary deliverable. ENV var schema and routing integration can be added incrementally if needed. Adapter can use params override for ENV vars initially.

---

### Alternative 2: Extended Scope (Add Multiple Tools)

**If**: Want to prove extensibility with multiple tools  
**Add**: Task 4 - Add 2-3 more tools via YAML (gemini, cursor, etc.)  
**Duration**: 1.5-2 days (add 4-6 hours)  
**Value**: Stronger proof of YAML-driven extensibility

**Rationale**: Adding multiple tools via YAML demonstrates the generic adapter scales beyond 2 tools. Provides more confidence for M3 and community contributions.

---

## Comparison to Previous Batch (M2 Batch 2.2)

| Metric | M2 Batch 2.2 | M2 Batch 2.3 | Change |
|--------|--------------|--------------|--------|
| **Tasks** | 3 (concrete adapter) | 3 (generic adapter) | Same |
| **Agents** | 1 (backend-dev) | 1 (backend-dev) | Same |
| **Total Effort** | 4-8h (estimated) | 5-8h (estimated) | Similar |
| **Duration** | 1-2 days | 1 day | Faster |
| **Complexity** | LOW-MEDIUM | LOW-MEDIUM | Same |
| **Strategic** | Reference adapter | Production adapter | HIGHER |

**Key Insights**:
- Similar complexity (both leverage Batch 2.1 infrastructure)
- Same agent (Benny demonstrated 6x efficiency in Batch 2.1)
- Higher strategic value (generic adapter enables YAML extensibility)
- Faster timeline (1 day vs. 1-2 days) - tighter scope
- Completes M2 strategic pivot (YAML-driven approach)

---

## Sign-off

**Prepared By**: Planning Petra  
**Date**: 2026-02-05 10:00:00 UTC  
**Status**: 🟢 **READY FOR ASSIGNMENT**  
**Batch ID**: `2026-02-05-llm-service-m2-batch-2.3`  
**Recommended Start**: Immediate (M2 Batches 2.1 & 2.2 complete, dependencies met)  
**Expected Completion**: 1 day (5-8 hours with buffer)

**Strategic Importance**: ⭐⭐⭐⭐⭐  
This batch completes the M2 strategic pivot to YAML-driven tool extensibility. After completion, adding new LLM tools requires YAML configuration changes only, not code changes. This enables community contributions and faster iteration.

**Next Steps**:
1. Assign Tasks 1-3 to Backend-dev Benny
2. Monitor progress per checkpoint schedule
3. Review GenericYAMLAdapter after Task 1 (key deliverable)
4. Validate YAML extensibility demo (add codex tool) after Task 3
5. Approve Milestone 3 kickoff (Telemetry & Cost Optimization) after completion

---

**Related Documents**:
- **M2 Batch 2.2 Summary:** `work/collaboration/ITERATION_2026-02-05_M2_BATCH_2.2_SUMMARY.md` (when created)
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md`
- **Agent Status:** `work/collaboration/AGENT_STATUS.md`
- **ADR-029:** `docs/architecture/adrs/ADR-029-adapter-interface-design.md` (updated 2026-02-05)
- **Architecture Review:** `work/analysis/generic-yaml-adapter-architecture-review.md`
- **Task Files:** `work/collaboration/inbox/2026-02-05T100X-backend-dev-*.yaml`

---

**Assumptions**:
1. GenericYAMLAdapter can handle 80%+ of tools (simple CLIs)
2. ClaudeCodeAdapter validates the infrastructure works correctly
3. Tool-specific output parsing handled by OutputNormalizer (extensible)
4. ENV variable validation at config load is acceptable (fail-fast)
5. Routing engine doesn't have tool-specific logic requiring refactor

**Re-planning Triggers**:
- GenericYAMLAdapter doesn't handle expected tools → Consider hybrid approach
- ENV var validation too strict → Defer to runtime validation
- Routing engine has tool-specific code → Add refactor task (1-2h)
- Test coverage below 80% → Add testing buffer (1-2h)

