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
## Selected Tasks (4 Total - Milestone 2 Batch 2.1)

### Task 1: Base Adapter Abstract Class

- **ID**: `2026-02-04T2100-backend-dev-adapter-base-class`
- **Agent**: backend-dev (Benny)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 4-6 hours
- **Mode**: `/analysis-mode` (design) + implementation
- **Strategic Value**: ⭐⭐⭐⭐⭐ Foundation for all tool adapters

**Why This Task:**
- Implements ADR-029 decision (Abstract Base Class approach)
- Defines contract for all tool adapters (claude-code, codex, future tools)
- Enables extensibility + type safety
- Critical path for M2 Tool Integration

**Implementation Requirements:**
1. Abstract base class `ToolAdapter` in `src/llm_service/adapters/base.py`
2. Required methods:
   - `execute(prompt: str, params: Dict) -> ToolResponse`
   - `validate_config(tool_config: ToolConfig) -> bool`
   - `get_tool_name() -> str`
3. Template method pattern for common logic
4. Type hints and docstrings (Google style)

**Deliverables**:
1. `src/llm_service/adapters/base.py`
   - `ToolAdapter` abstract base class
   - `ToolResponse` dataclass for standardized output
   - Type definitions for adapter contract
2. `src/llm_service/adapters/__init__.py` (package setup)

**Dependencies**: ADR-029 (COMPLETE ✅)

**Success Criteria**:
- Abstract base class with clear contract
- Type-safe method signatures
- Docstrings for all public methods
- Ready for concrete adapter implementations
- Passes basic instantiation tests

---

### Task 2: Command Template Parser

- **ID**: `2026-02-04T2101-backend-dev-command-template-parser`
- **Agent**: backend-dev (Benny)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 3-4 hours
- **Mode**: Implementation
- **Strategic Value**: ⭐⭐⭐⭐ Enables dynamic tool invocation

**Why This Task:**
- Parses command templates from YAML tool definitions
- Substitutes placeholders ({{model}}, {{prompt}}, {{params}})
- Implements security mitigations per security review
- Enables YAML-based tool extensibility

**Implementation Requirements:**
1. Template parser in `src/llm_service/adapters/template_parser.py`
2. Placeholder substitution:
   - `{{model}}` → agent's preferred model
   - `{{prompt}}` → user prompt (escaped)
   - `{{param_name}}` → additional parameters
3. Security features:
   - Whitelist allowed placeholders
   - Escape shell metacharacters
   - Validate template format
4. Error handling for invalid templates

**Deliverables**:
1. `src/llm_service/adapters/template_parser.py`
   - `TemplateParser` class
   - `parse_template(template: str, context: Dict) -> str`
   - Security validation methods
2. Unit tests for:
   - Basic placeholder substitution
   - Edge cases (missing placeholders, invalid syntax)
   - Security scenarios (injection attempts)

**Dependencies**: None (can run in parallel with Task 1)

**Success Criteria**:
- Template parser handles all placeholder types
- Security validation prevents injection attacks
- Clear error messages for invalid templates
- >80% test coverage on template parser
- Examples work with real YAML tool definitions

---

### Task 3: Subprocess Execution Wrapper

- **ID**: `2026-02-04T2102-backend-dev-subprocess-wrapper`
- **Agent**: backend-dev (Benny)
- **Priority**: HIGH
- **Status**: Ready to assign
- **Estimated Effort**: 3-4 hours
- **Mode**: Implementation
- **Strategic Value**: ⭐⭐⭐⭐ Executes external tools safely

**Why This Task:**
- Executes tool commands via subprocess
- Captures stdout/stderr
- Handles timeouts, errors, and crashes
- Enables integration with claude-code, codex CLIs

**Implementation Requirements:**
1. Subprocess wrapper in `src/llm_service/adapters/subprocess_wrapper.py`
2. Features:
   - Execute command with timeout (configurable)
   - Capture stdout/stderr streams
   - Return exit code + output
   - Handle platform differences (Linux/macOS/Windows)
3. Error handling:
   - Command not found
   - Timeout exceeded
   - Non-zero exit codes
   - Subprocess crashes
4. Security:
   - Use `shell=False` (per security review)
   - No shell expansion
   - Environment variable control

**Deliverables**:
1. `src/llm_service/adapters/subprocess_wrapper.py`
   - `SubprocessExecutor` class
   - `execute(command: List[str], timeout: int) -> ExecutionResult`
   - `ExecutionResult` dataclass (exit_code, stdout, stderr, duration)
2. Unit tests for:
   - Successful execution
   - Timeout scenarios
   - Error handling (command not found, non-zero exit)
   - Platform compatibility

**Dependencies**: Task 2 (template parser) for command generation

**Success Criteria**:
- Subprocess execution works on all platforms
- Timeouts handled gracefully
- Error messages are user-friendly
- >80% test coverage on subprocess wrapper
- Integration tests with fake CLI scripts

---

### Task 4: Output Normalization Framework

- **ID**: `2026-02-04T2103-backend-dev-output-normalization`
- **Agent**: backend-dev (Benny)
- **Priority**: MEDIUM
- **Status**: Ready to assign
- **Estimated Effort**: 2-3 hours
- **Mode**: Implementation
- **Strategic Value**: ⭐⭐⭐ Standardizes tool responses

**Why This Task:**
- Normalizes different tool output formats
- Extracts response, metadata, errors
- Enables consistent telemetry and error handling
- Prepares for M3 telemetry integration

**Implementation Requirements:**
1. Output normalizer in `src/llm_service/adapters/output_normalizer.py`
2. Normalize outputs:
   - Extract LLM response text
   - Parse metadata (tokens, model, cost)
   - Identify errors vs. warnings
   - Standardize format across tools
3. Support different output formats:
   - JSON (structured)
   - Plain text (unstructured)
   - Mixed (text + metadata)
4. Extensibility for new tools

**Deliverables**:
1. `src/llm_service/adapters/output_normalizer.py`
   - `OutputNormalizer` class
   - `normalize(raw_output: str, tool_name: str) -> NormalizedResponse`
   - `NormalizedResponse` dataclass (response_text, metadata, errors)
2. Unit tests for:
   - JSON parsing
   - Plain text extraction
   - Error detection
   - Metadata extraction

**Dependencies**: Task 3 (subprocess wrapper) for raw output

**Success Criteria**:
- Output normalization handles JSON and plain text
- Metadata extracted when available
- Errors identified and standardized
- >80% test coverage on normalizer
- Ready for claude-code and codex adapters (different formats)

---

## Execution Plan

### Phase 1: Core Infrastructure (Hours 0-8)

**Parallel Execution:**
```
Task 1: Base Adapter Class              [4-6h]  HIGH  (backend-dev)
Task 2: Command Template Parser         [3-4h]  HIGH  (backend-dev)
```

**Characteristics:**
- Can execute in parallel (different modules)
- Task 1 is blocking for concrete adapters (Batches 2.2-2.3)
- Task 2 is independent, can complete first

**Time Estimate:** 1 day (max 6 hours for Task 1)

---

### Phase 2: Execution & Normalization (Hours 8-16)

**Sequential Execution (Depends on Task 2):**
```
Task 3: Subprocess Wrapper              [3-4h]  HIGH  (depends on Task 2)
Task 4: Output Normalization            [2-3h]  MEDIUM (depends on Task 3)
```

**Characteristics:**
- Task 3 needs template parser (Task 2) for command generation
- Task 4 needs subprocess wrapper (Task 3) for raw output
- Sequential execution required

**Time Estimate:** 1 day (7 hours with buffer)

---

### Timeline Estimates

**Realistic** (Sequential Execution): 2 days
- Day 1: Tasks 1-2 complete (base class + template parser)
- Day 2: Tasks 3-4 complete (subprocess + normalization)
- Buffer: 4 hours for integration testing + refinement

**Optimistic** (Partial Parallelization): 1.5 days
- Day 1: All 4 tasks complete if Task 1 finishes quickly
- Day 2 Morning: Integration testing + buffer
- No significant blockers expected

**Recommended:** Plan for 2 days with 4-hour buffer for testing

---

## Checkpoints & Milestones

### Checkpoint 1: Core Infrastructure Complete (Day 1 EOD)
**Check**: Tasks 1-2 (base class + template parser) complete  
**Expected**: 
- Base adapter abstract class implemented and tested ✅
- Command template parser working with placeholder substitution ✅
- Unit tests passing (>80% coverage) ✅
**Decision**: Proceed to execution layer OR refine base infrastructure  
**Trigger**: Backend-dev completes Task 2

### Checkpoint 2: Execution Layer Complete (Day 2 Mid)
**Check**: Task 3 (subprocess wrapper) complete  
**Expected**: 
- Subprocess execution working on all platforms ✅
- Timeouts and error handling validated ✅
- Integration tests with fake CLI scripts passing ✅
**Decision**: Proceed to normalization OR enhance execution  
**Trigger**: Backend-dev completes Task 3

### Checkpoint 3: M2 Batch 2.1 Complete (Day 2 EOD)
**Check**: All 4 tasks complete + integration tests passing  
**Expected**: 
- Full adapter infrastructure ready ✅
- All unit tests passing (>80% coverage) ✅
- Integration tests with fake tools working ✅
- Ready for concrete adapter implementations (Batches 2.2-2.3) ✅
**Decision**: Start M2 Batch 2.2 (Claude-Code Adapter) OR address gaps  
**Trigger**: All 4 tasks complete, human approval

---

## Resource Allocation

| Agent | Tasks | Total Hours | Complexity | Timeline |
|-------|-------|-------------|------------|----------|
| **backend-dev** | 4 | 12-16h | MEDIUM | 2 days |
| **Total** | **4 tasks** | **12-16h** | **Medium** | **2 days** |

### Agent Workload: Backend-dev Benny

**Workload:** Moderate (12-16 hours over 2 days)
- Task 1: 4-6 hours (Base adapter class)
- Task 2: 3-4 hours (Template parser)
- Task 3: 3-4 hours (Subprocess wrapper)
- Task 4: 2-3 hours (Output normalization)

**Characteristics:**
- Single agent (no coordination overhead)
- Medium complexity (infrastructure, not algorithms)
- High strategic value (unblocks M2 Batches 2.2-2.3)
- Fits in 2 working days with 4-hour testing buffer

---

## Risk Assessment & Mitigation

### Risk 1: Platform Compatibility Issues
**Description**: Subprocess execution behaves differently on Windows/Linux/macOS  
**Probability**: MEDIUM  
**Impact**: MEDIUM (delays M2 Batch 2.1)  
**Mitigation**: 
- Use `subprocess.run()` with `shell=False` (cross-platform)
- Test on multiple platforms early
- Document platform-specific behaviors
- Defer Windows support if blocked (focus on Linux/macOS)

### Risk 2: Template Parser Complexity
**Description**: Command template substitution becomes complex with edge cases  
**Probability**: LOW  
**Impact**: LOW (not blocking)  
**Mitigation**:
- Keep template syntax simple (only {{placeholder}})
- Use whitelist for allowed placeholders
- Defer advanced features (conditionals, loops) to post-MVP
- Validate templates at config load time

### Risk 3: Test Coverage Target
**Description**: Difficulty achieving >80% test coverage on all modules  
**Probability**: LOW  
**Impact**: LOW (quality concern)  
**Mitigation**:
- Focus on critical paths (execution, error handling)
- Use mocks for external dependencies
- Accept lower coverage on edge cases if needed
- Track coverage per-module, not just overall

---

## Success Metrics

### Task-Level Metrics
- ✅ 4/4 tasks completed within 2 days
- ✅ All unit tests passing (no failures)
- ✅ >80% test coverage per module
- ✅ Integration tests working with fake CLI scripts
- ✅ Code follows Python style guide (PEP 8)

### Strategic Metrics
- ✅ Adapter infrastructure ready for concrete adapters
- ✅ M2 Batch 2.2 (Claude-Code Adapter) unblocked
- ✅ M2 Batch 2.3 (Codex Adapter) unblocked
- ✅ Generic adapter pattern established

### Value Realization
- **Immediate**: Foundation for tool adapter implementations
- **Short-term** (M2 Batches 2.2-2.4): Concrete adapters built on this base
- **Long-term**: Extensibility enables community-contributed tools

---

## Dependency Management

### Prerequisites (All Met ✅)

| Dependency | Status | Location | Notes |
|------------|--------|----------|-------|
| M1 Foundation Complete | ✅ | src/llm_service/ | 93% coverage, approved |
| M2 Prep Complete | ✅ | ADRs 026-029 | All ADRs documented |
| Adapter Design Decided | ✅ | ADR-029 | ABC approach chosen |
| Security Review Done | ✅ | Security analysis | Risks assessed |
| Test Infrastructure | ✅ | tests/unit/ | Pytest + coverage |

### Internal Dependencies (This Batch)

**Task Dependencies:**
- Task 1 (Base class): No dependencies, can start immediately
- Task 2 (Template parser): No dependencies, can run in parallel with Task 1
- Task 3 (Subprocess wrapper): Depends on Task 2 (needs template parser for commands)
- Task 4 (Output normalizer): Depends on Task 3 (needs subprocess output)

**Recommended Execution:**
- **Day 1**: Tasks 1-2 in parallel (independent modules)
- **Day 2**: Tasks 3-4 sequentially (Task 3 → Task 4)

---

## Handoff to M2 Batch 2.2

### Expected Outputs After This Batch

**Code:**
1. ✅ `src/llm_service/adapters/base.py` - Base adapter abstract class
2. ✅ `src/llm_service/adapters/template_parser.py` - Command template parser
3. ✅ `src/llm_service/adapters/subprocess_wrapper.py` - Subprocess executor
4. ✅ `src/llm_service/adapters/output_normalizer.py` - Output normalizer
5. ✅ `src/llm_service/adapters/__init__.py` - Package initialization

**Tests:**
1. ✅ `tests/unit/adapters/test_base.py` - Base adapter tests
2. ✅ `tests/unit/adapters/test_template_parser.py` - Template parser tests
3. ✅ `tests/unit/adapters/test_subprocess_wrapper.py` - Subprocess tests
4. ✅ `tests/unit/adapters/test_output_normalizer.py` - Normalizer tests
5. ✅ `tests/integration/adapters/test_fake_tool.py` - Integration tests

**M2 Batch 2.2 Readiness Checklist:**
- ✅ Base adapter interface defined and tested
- ✅ Command template system working
- ✅ Subprocess execution framework ready
- ✅ Output normalization framework ready
- ✅ >80% test coverage on adapter base
- ✅ Integration tests passing

**Next Batch (M2 Batch 2.2):**
- Task: Implement Claude-Code adapter (concrete implementation)
- Agent: Backend-dev Benny
- Estimated Effort: 2-3 days
- Deliverable: Working claude-code adapter with integration tests

---

## Alternative Batches

### Alternative 1: Core Only (Minimal Scope)

**If**: Backend-dev has limited availability  
**Execute**: Tasks 1-2 (base class + template parser)  
**Duration**: 1 day  
**Value**: Core infrastructure ready, subprocess layer can be deferred

**Rationale**: Base adapter + template parser are critical for concrete adapters. Subprocess wrapper can be built during M2 Batch 2.2 if needed.

---

### Alternative 2: Extended Scope (Add Fake Adapter)

**If**: More time available OR need validation  
**Add**: Task 5 - Fake tool adapter for testing  
**Duration**: 2.5 days (add 4 hours)  
**Value**: Full end-to-end validation before claude-code adapter

**Rationale**: Fake adapter validates entire infrastructure with no external dependencies. Reduces risk for M2 Batch 2.2.

---

## Comparison to Previous Batch (M2 Prep)

| Metric | M2 Prep Batch | M2 Batch 2.1 | Change |
|--------|---------------|--------------|--------|
| **Tasks** | 5 (documentation) | 4 (implementation) | -1 task |
| **Agents** | 1 (architect) | 1 (backend-dev) | Same |
| **Total Effort** | 4.25h | 12-16h | +280% |
| **Duration** | 1 day | 2 days | +100% |
| **Complexity** | LOW | MEDIUM | Increased |
| **Strategic** | Docs/ADRs | Core implementation | Shift to code |

**Key Insights**:
- Higher effort (documentation → implementation)
- Single agent still (no coordination complexity)
- Higher strategic value (unblocks 3 more batches)
- Medium risk (platform compatibility, test coverage)

---

## Sign-off

**Prepared By**: Planning Petra  
**Date**: 2026-02-04 20:45:00 UTC  
**Status**: 🟢 **READY FOR ASSIGNMENT**  
**Batch ID**: `2026-02-04-llm-service-m2-batch-2.1`  
**Recommended Start**: Immediate (M2 prep complete, dependencies met)  
**Expected Completion**: 2 days (with 4-hour testing buffer)

**Next Steps**:
1. Assign Tasks 1-4 to Backend-dev Benny
2. Monitor progress per checkpoint schedule
3. Review code quality and test coverage daily
4. Approve M2 Batch 2.2 after completion
5. Prepare M2 Batch 2.2 (Claude-Code Adapter)

---

**Related Documents**:
- **M2 Prep Summary:** `work/collaboration/ITERATION_2026-02-04_M2_PREP_SUMMARY.md`
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md`
- **Agent Status:** `work/collaboration/AGENT_STATUS.md`
- **ADR-029:** `docs/architecture/adrs/ADR-029-adapter-interface-design.md`
- **Security Review:** `work/analysis/llm-service-command-template-security.md`
- **Adapter Design Review:** `work/analysis/llm-service-adapter-interface-review.md`
