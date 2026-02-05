# Next Batch: M2 Batch 2.1 - Adapter Base Interface

**Batch ID**: `2026-02-04-llm-service-m2-batch-2.1`  
**Created**: 2026-02-04  
**Updated**: 2026-02-04 20:45:00 UTC (Post-M2 Prep Completion)  
**Prepared By**: Planning Petra  
**Status**: 🟢 **READY FOR ASSIGNMENT**  
**Estimated Duration**: 2 days (12-16 hours + testing buffer)

---

## Batch Objective

Implement **Adapter Base Interface** for LLM Service Layer Tool Integration (Milestone 2):

1. **Base adapter abstract class** (per ADR-029)
2. **Command template parsing** and substitution
3. **Subprocess execution wrapper** with error handling
4. **Output normalization framework**
5. **Unit tests** with >80% coverage

**Success Criteria**:
- Base adapter interface implemented and tested
- Command template system working with placeholder substitution
- Subprocess execution handles errors gracefully
- Output normalization enables consistent tool responses
- >80% test coverage on adapter base
- Ready for claude-code and codex adapter implementations (Batches 2.2-2.3)

---

## Context: M2 Prep Batch Complete - Milestone 2 Ready

**Achievement:** ✅ M2 Prep COMPLETE (5/5 tasks done in 3h 10m)
- 4 ADRs documented (ADR-026, 027, 028, 029) ✅
- Adapter interface design decided (ABC approach) ✅
- Security posture reviewed ✅
- Decision traceability: 100% compliance ✅
- M2 fully unblocked - NO BLOCKERS ✅

**Previous Batch Performance:**
- Agent: Architect Alphonso
- Efficiency: ⭐ 134% (25% faster than estimate)
- Quality: 100% Directive 018 compliance
- Deliverables: 7 comprehensive documents (~75KB)

**Why M2 Batch 2.1 Now:**
- Foundation complete: 93% test coverage, 65/65 tests passing
- Architecture approved: Alphonso APPROVED for M2
- Design decided: ADR-029 specifies ABC approach for adapters
- Security reviewed: Command template injection risks assessed and mitigated
- Milestone 2 (Tool Integration) ready to start immediately
## Selected Tasks (3 Total - Milestone 2 Batch 2.2)

### Task 1: ClaudeCodeAdapter Implementation

- **ID**: `2026-02-05T0900-backend-dev-claude-code-adapter`
- **Agent**: backend-dev (Benny)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 2-4 hours
- **Mode**: Implementation
- **Strategic Value**: ⭐⭐⭐⭐⭐ First concrete adapter, validates infrastructure

**Why This Task:**
- Implements concrete adapter for claude-code CLI
- Validates Batch 2.1 adapter infrastructure
- Enables real agent-LLM interactions via claude-code
- Critical path for M2 completion

**Implementation Requirements:**
1. ClaudeCodeAdapter class in `src/llm_service/adapters/claude_code_adapter.py`
2. Extends `ToolAdapter` base class from Batch 2.1
3. Methods to implement:
   - `execute(prompt: str, params: Dict) -> ToolResponse`
   - `validate_config(tool_config: ToolConfig) -> bool`
   - `get_tool_name() -> str` (returns "claude-code")
4. Model parameter mapping:
   - Support claude-3.5-sonnet, claude-3-opus, etc.
   - Map service layer model names to claude CLI parameters
5. CLI command generation:
   - Use `CommandTemplateHandler` from Batch 2.1
   - Generate: `claude-code --model {{model}} --prompt "{{prompt}}"`
6. Error handling:
   - Binary not found
   - Invalid model name
   - CLI execution failures

**Deliverables**:
1. `src/llm_service/adapters/claude_code_adapter.py`
   - `ClaudeCodeAdapter` class
   - Model mapping logic
   - CLI command generation
2. Unit tests (4-6 tests):
   - Basic execution flow
   - Model parameter mapping
   - Error handling scenarios

**Dependencies**: Batch 2.1 complete ✅

**Success Criteria**:
- ClaudeCodeAdapter extends ToolAdapter correctly
- Model mapping works for all supported models
- CLI command generation uses template system
- Error handling provides user-friendly messages
- Unit tests passing with >80% coverage

---

### Task 2: Platform Binary Path Resolution

- **ID**: `2026-02-05T0901-backend-dev-binary-path-resolution`
- **Agent**: backend-dev (Benny)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 1-2 hours
- **Mode**: Implementation
- **Strategic Value**: ⭐⭐⭐⭐ Enables cross-platform compatibility

**Why This Task:**
- Resolves claude-code binary path on different platforms
- Handles different installation locations (system, user, custom)
- Enables cross-platform compatibility (Linux/macOS/Windows)
- Validates platform support from Batch 2.1

**Implementation Requirements:**
1. Binary path resolution in `ClaudeCodeAdapter` or helper module
2. Platform-specific logic:
   - Linux: Check `/usr/local/bin/claude-code`, `~/.local/bin/claude-code`
   - macOS: Check `/usr/local/bin/claude-code`, `~/bin/claude-code`
   - Windows: Check `C:\Program Files\claude-code\claude.exe`, user AppData
3. Use `shutil.which()` for cross-platform path lookup
4. Fallback to YAML configuration if binary not found
5. Error handling:
   - Binary not found (user-friendly message with install instructions)
   - Binary not executable (permission issues)

**Deliverables**:
1. Binary path resolution logic in `ClaudeCodeAdapter`
2. Configuration option: `tool.binary_path` (optional override)
3. Unit tests (2-3 tests):
   - Binary found via shutil.which()
   - Binary found via config override
   - Binary not found (error handling)

**Dependencies**: Task 1 (ClaudeCodeAdapter base)

**Success Criteria**:
- Binary resolution works on Linux/macOS
- Windows compatibility validated (or documented as deferred)
- Config override works correctly
- Clear error message when binary not found
- Unit tests passing

---

### Task 3: Integration Tests with Mocked CLI

- **ID**: `2026-02-05T0902-backend-dev-claude-adapter-integration-tests`
- **Agent**: backend-dev (Benny)
- **Priority**: MEDIUM
- **Status**: Ready to assign
- **Estimated Effort**: 2-3 hours
- **Mode**: Testing
- **Strategic Value**: ⭐⭐⭐⭐ Validates end-to-end adapter flow

**Why This Task:**
- Validates ClaudeCodeAdapter with mocked claude CLI
- Tests full execution flow: config → command → execution → response
- Prepares for real claude-code CLI validation
- Ensures error handling works in realistic scenarios

**Implementation Requirements:**
1. Integration tests in `tests/integration/adapters/test_claude_code_adapter.py`
2. Mock claude CLI using fake script:
   - Accepts `--model` and `--prompt` parameters
   - Returns realistic output (JSON or plain text)
   - Simulates errors (invalid model, timeout, etc.)
3. Test scenarios:
   - **Successful execution**: Prompt → response
   - **Model mapping**: Different models → correct CLI parameters
   - **Error handling**: Binary not found, invalid model, timeout
   - **Output parsing**: JSON response → ToolResponse
4. Use `SubprocessExecutor` from Batch 2.1 for execution

**Deliverables**:
1. `tests/integration/adapters/test_claude_code_adapter.py` (4-6 tests)
2. `tests/fixtures/fake_claude_cli.py` or shell script
3. Integration test suite covering:
   - Happy path (successful execution)
   - Error scenarios (binary not found, timeout, etc.)
   - Output parsing (JSON, plain text)

**Dependencies**: Tasks 1-2 (ClaudeCodeAdapter + binary resolution)

**Success Criteria**:
- Integration tests passing with fake claude CLI
- All error scenarios validated
- Output parsing works for JSON and plain text
- Test coverage >80% on ClaudeCodeAdapter
- Ready for real claude-code CLI validation (manual)

---

## Execution Plan

### Phase 1: Adapter Implementation (Hours 0-4)

**Sequential Execution:**
```
Task 1: ClaudeCodeAdapter Implementation  [2-4h]  HIGH  (backend-dev)
```

**Characteristics:**
- Leverages Batch 2.1 infrastructure (base class, template parser, subprocess executor)
- Single focused task: concrete adapter implementation
- Low complexity (infrastructure already proven in Batch 2.1)

**Time Estimate:** Half day (2-4 hours)

---

### Phase 2: Platform & Integration (Hours 4-8)

**Sequential Execution (Depends on Task 1):**
```
Task 2: Binary Path Resolution          [1-2h]  HIGH  (depends on Task 1)
Task 3: Integration Tests               [2-3h]  MEDIUM (depends on Task 1-2)
```

**Characteristics:**
- Task 2 adds platform compatibility to Task 1
- Task 3 validates full adapter flow with mocked CLI
- Both depend on ClaudeCodeAdapter base (Task 1)

**Time Estimate:** Half day (3-5 hours)

---

### Timeline Estimates

**Optimistic** (Based on Batch 2.1 Efficiency): 4-6 hours
- Morning: Task 1 complete (ClaudeCodeAdapter implementation)
- Afternoon: Tasks 2-3 complete (binary resolution + integration tests)
- Assumption: Benny maintains 6x efficiency from Batch 2.1

**Realistic** (Conservative Estimate): 1-2 days
- Day 1: Tasks 1-2 complete (adapter + binary resolution)
- Day 2 Morning: Task 3 complete (integration tests)
- Buffer: 4 hours for platform testing + refinement

**Recommended:** Plan for 1-2 days with buffer for real CLI validation (optional)

---

## Checkpoints & Milestones

### Checkpoint 1: Adapter Implementation Complete (Half Day)
**Check**: Task 1 (ClaudeCodeAdapter) complete  
**Expected**: 
- ClaudeCodeAdapter class implemented and tested ✅
- Model parameter mapping working ✅
- CLI command generation using template system ✅
- Unit tests passing (>80% coverage) ✅
**Decision**: Proceed to platform compatibility OR refine adapter  
**Trigger**: Backend-dev completes Task 1

### Checkpoint 2: Platform Compatibility Complete (Day 1 EOD)
**Check**: Task 2 (binary path resolution) complete  
**Expected**: 
- Binary resolution working on Linux/macOS ✅
- Config override functionality validated ✅
- Error handling for binary not found ✅
- Unit tests passing ✅
**Decision**: Proceed to integration testing OR enhance compatibility  
**Trigger**: Backend-dev completes Task 2

### Checkpoint 3: M2 Batch 2.2 Complete (Day 1-2)
**Check**: All 3 tasks complete + integration tests passing  
**Expected**: 
- ClaudeCodeAdapter fully functional ✅
- Integration tests passing with mocked CLI ✅
- All unit tests passing (>80% coverage) ✅
- Platform compatibility validated ✅
- Ready for M2 Batch 2.3 (CodexAdapter) OR real CLI validation ✅
**Decision**: Start M2 Batch 2.3 (CodexAdapter) OR validate with real claude-code CLI  
**Trigger**: All 3 tasks complete, human approval

---

## Resource Allocation

| Agent | Tasks | Total Hours | Complexity | Timeline |
|-------|-------|-------------|------------|----------|
| **backend-dev** | 3 | 4-8h | LOW-MEDIUM | 1-2 days |
| **Total** | **3 tasks** | **4-8h** | **Low-Medium** | **1-2 days** |

### Agent Workload: Backend-dev Benny

**Workload:** Light-Moderate (4-8 hours over 1-2 days)
- Task 1: 2-4 hours (ClaudeCodeAdapter implementation)
- Task 2: 1-2 hours (Binary path resolution)
- Task 3: 2-3 hours (Integration tests with mocked CLI)

**Characteristics:**
- Single agent (no coordination overhead)
- Low-Medium complexity (leverages Batch 2.1 infrastructure)
- High strategic value (first concrete adapter, validates infrastructure)
- Estimated based on Batch 2.1 efficiency (6x faster than initial estimates)
- Fits in 1 working day (optimistic) or 2 days (conservative)

---

## Risk Assessment & Mitigation

### Risk 1: Claude-Code CLI Availability
**Description**: claude-code CLI not available in CI environment  
**Probability**: MEDIUM  
**Impact**: MEDIUM (blocks real CLI validation)  
**Mitigation**: 
- Use mocked CLI for integration tests (primary approach)
- Document manual validation steps for real CLI
- Defer real CLI testing to local development environment
- Focus on adapter logic correctness, not CLI integration

### Risk 2: Platform-Specific Binary Paths
**Description**: Binary path resolution differs across platforms  
**Probability**: LOW  
**Impact**: LOW (config override available)  
**Mitigation**:
- Use `shutil.which()` for cross-platform path lookup
- Provide config override for custom binary paths
- Document common installation locations per platform
- Test on Linux/macOS, document Windows as deferred

### Risk 3: Test Coverage Target
**Description**: Difficulty achieving >80% test coverage on adapter  
**Probability**: LOW  
**Impact**: LOW (quality concern)  
**Mitigation**:
- Focus on critical paths (execution, error handling)
- Use mocked CLI for integration tests
- Leverage Batch 2.1 test infrastructure (already 93% coverage)
- Track coverage per-module, not just overall

---

## Success Metrics

### Task-Level Metrics
- ✅ 3/3 tasks completed within 1-2 days
- ✅ All unit tests passing (no failures)
- ✅ >80% test coverage on ClaudeCodeAdapter
- ✅ Integration tests passing with mocked CLI
- ✅ Code follows Python style guide (PEP 8)

### Strategic Metrics
- ✅ ClaudeCodeAdapter fully functional
- ✅ First concrete adapter validates Batch 2.1 infrastructure
- ✅ M2 Batch 2.3 (CodexAdapter) unblocked
- ✅ Real agent-LLM interactions enabled (with real CLI)

### Value Realization
- **Immediate**: First concrete adapter for claude-code CLI
- **Short-term** (M2 Batch 2.3): CodexAdapter can reuse same pattern
- **Long-term**: Validates adapter infrastructure for future tools

---

## Dependency Management

### Prerequisites (All Met ✅)

| Dependency | Status | Location | Notes |
|------------|--------|----------|-------|
| M1 Foundation Complete | ✅ | src/llm_service/ | 93% coverage, 65/65 tests |
| M2 Prep Complete | ✅ | ADRs 026-029 | All ADRs documented |
| M2 Batch 2.1 Complete | ✅ | src/llm_service/adapters/ | Base infrastructure ready |
| Adapter Base Class | ✅ | base.py | ToolAdapter ABC ready |
| Command Template System | ✅ | command_template.py | Template handler ready |
| Subprocess Executor | ✅ | subprocess_executor.py | Execution wrapper ready |
| Test Infrastructure | ✅ | tests/ | 93% coverage, 78/78 tests |

### Internal Dependencies (This Batch)

**Task Dependencies:**
- Task 1 (ClaudeCodeAdapter): Depends on Batch 2.1 (base class, template parser, subprocess executor)
- Task 2 (Binary resolution): Depends on Task 1 (integrates into ClaudeCodeAdapter)
- Task 3 (Integration tests): Depends on Tasks 1-2 (validates full adapter)

**Recommended Execution:**
- **Phase 1**: Task 1 (ClaudeCodeAdapter implementation)
- **Phase 2**: Tasks 2-3 sequentially (Task 2 → Task 3)

---

## Handoff to M2 Batch 2.3

### Expected Outputs After This Batch

**Code:**
1. ✅ `src/llm_service/adapters/claude_code_adapter.py` - ClaudeCodeAdapter class
2. ✅ Model parameter mapping for claude-code CLI
3. ✅ Binary path resolution (platform-specific)
4. ✅ CLI command generation using template system
5. ✅ Error handling for tool-specific failures

**Tests:**
1. ✅ `tests/unit/adapters/test_claude_code_adapter.py` - Unit tests (4-6 tests)
2. ✅ `tests/integration/adapters/test_claude_code_adapter.py` - Integration tests (4-6 tests)
3. ✅ `tests/fixtures/fake_claude_cli.py` - Mocked CLI for testing

**M2 Batch 2.3 Readiness Checklist:**
- ✅ ClaudeCodeAdapter fully functional
- ✅ Integration tests passing with mocked CLI
- ✅ Platform compatibility validated (Linux/macOS)
- ✅ >80% test coverage on ClaudeCodeAdapter
- ✅ Error handling validated
- ✅ Ready for CodexAdapter implementation (same pattern)

**Next Batch (M2 Batch 2.3):**
- Task: Implement CodexAdapter (concrete implementation)
- Agent: Backend-dev Benny
- Estimated Effort: 1-2 days (same pattern as ClaudeCodeAdapter)
- Deliverable: Working codex adapter with integration tests

---

## Alternative Batches

### Alternative 1: Minimal Scope (Adapter Only)

**If**: Backend-dev has limited availability  
**Execute**: Task 1 only (ClaudeCodeAdapter implementation)  
**Duration**: Half day (2-4 hours)  
**Value**: Core adapter ready, binary resolution and integration tests can be deferred

**Rationale**: ClaudeCodeAdapter is the primary deliverable. Binary resolution and integration tests can be added incrementally if needed.

---

### Alternative 2: Extended Scope (Add Real CLI Validation)

**If**: Real claude-code CLI available  
**Add**: Task 4 - Real CLI validation and testing  
**Duration**: 2-3 days (add 4-6 hours)  
**Value**: Full validation with real claude-code CLI, not just mocked

**Rationale**: Real CLI validation confirms adapter works in production environment. Reduces risk for pilot deployment.

---

## Comparison to Previous Batch (M2 Batch 2.1)

| Metric | M2 Batch 2.1 | M2 Batch 2.2 | Change |
|--------|--------------|--------------|--------|
| **Tasks** | 4 (infrastructure) | 3 (concrete adapter) | -1 task |
| **Agents** | 1 (backend-dev) | 1 (backend-dev) | Same |
| **Total Effort** | ~2.5h (actual) | 4-8h (estimated) | +3-5.5h |
| **Duration** | ~2.5h | 1-2 days | Conservative |
| **Complexity** | MEDIUM | LOW-MEDIUM | Decreased |
| **Strategic** | Infrastructure | First concrete adapter | Validation |

**Key Insights**:
- Lower complexity (leverages Batch 2.1 infrastructure)
- Same agent (Benny demonstrated 6x efficiency in Batch 2.1)
- More conservative estimate (1-2 days vs. realistic 4-8h)
- High strategic value (first concrete adapter validates infrastructure)
- Low risk (infrastructure already proven in Batch 2.1)

---

## Sign-off

**Prepared By**: Planning Petra  
**Date**: 2026-02-05 08:30:00 UTC  
**Status**: 🟢 **READY FOR ASSIGNMENT**  
**Batch ID**: `2026-02-05-llm-service-m2-batch-2.2`  
**Recommended Start**: Immediate (M2 Batch 2.1 complete, dependencies met)  
**Expected Completion**: 1-2 days (with buffer for platform testing)

**Next Steps**:
1. Assign Tasks 1-3 to Backend-dev Benny
2. Monitor progress per checkpoint schedule
3. Review code quality and test coverage after Task 1
4. Validate platform compatibility (Linux/macOS) after Task 2
5. Approve M2 Batch 2.3 (CodexAdapter) after completion

---

**Related Documents**:
- **M2 Batch 2.1 Summary:** `work/collaboration/ITERATION_2026-02-05_M2_BATCH_2.1_SUMMARY.md`
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md`
- **Agent Status:** `work/collaboration/AGENT_STATUS.md`
- **ADR-029:** `docs/architecture/adrs/ADR-029-adapter-interface-design.md`
- **Batch 2.1 Code:** `src/llm_service/adapters/` (base.py, command_template.py, subprocess_executor.py)
