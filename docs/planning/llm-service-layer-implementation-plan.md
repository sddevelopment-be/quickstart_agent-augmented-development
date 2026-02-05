# Implementation Plan: LLM Service Layer

**Project:** LLM Service Layer for Agent-Tool Orchestration  
**Status:** 🟢 MILESTONE 2 READY TO START - M2 Prep Complete  
**Planning Date:** 2026-02-04  
**Last Updated:** 2026-02-04 20:45:00 UTC (M2 Prep Complete)  
**Planner:** Planning Petra  
**Architecture Reference:** `docs/architecture/design/llm-service-layer-prestudy.md`  
**Orchestration Approach:** File-Based Task Coordination (see `.github/agents/approaches/work-directory-orchestration.md`)

**Current Progress:**
- ✅ Milestone 1: COMPLETE (Foundation) - 100% acceptance criteria met
- ✅ Implementation roadmap complete (17 tasks, 4 milestones)
- ✅ Code quality: 93% coverage, 78/78 tests passing (updated)
- ✅ Architecture review: APPROVED by Architect Alphonso
- ✅ M2 Prep: COMPLETE (5/5 tasks, 3h 10m) - 25% faster than estimate
- ✅ M2 Batch 2.1: COMPLETE (4/4 tasks, ~2.5h) - ⭐ 84% faster than estimate
- ✅ M2 Batch 2.2: COMPLETE - ClaudeCodeAdapter (reference implementation)
- ✅ ADRs: 5 documented (ADR-026, 027, 028, 029 + Generic Adapter decision)
- 🚀 Milestone 2: IN PROGRESS - Generic YAML-driven adapter approach
- 📋 Next: M2 Batch 2.3 - Generic YAML Adapter Implementation

---

## Strategic Context

**Goal:** Build a service layer that routes agent requests to appropriate LLM stacks (claude-code, codex) via configuration-driven policies, enabling cost optimization and unified agent-LLM interaction.

**Approved Decisions:**
- Tech stack: Python or Node.js (team choice)
- Configuration: YAML format
- Budget enforcement: Configurable (soft/hard limits via `limit.type`)
- MVP tools: claude-code + codex with extensible YAML-based tool definitions

**Success Metrics:**
- 30-56% token cost reduction through smart model selection
- Single CLI interface for all agent-LLM interactions
- Cross-platform support (Linux, macOS, Windows/WSL2)
- $3,000-$6,000 annual savings per engineering team

---

## Milestones & Batches

### Milestone 1: Foundation (Weeks 1-2) - ✅ COMPLETE

**Status:** ✅ **COMPLETE** (2026-02-04)  
**Quality Gate:** ✅ **PASSED** - All acceptance criteria met

**Goal:** Establish core infrastructure and configuration management

**Achievements:**
1. ✅ **Configuration Schema & Validation** 
   - 4 YAML schemas defined (agents, tools, models, policies)
   - Pydantic v2 validation with 100% schema coverage
   - Enhanced with tool-model compatibility validation
   - 25 schema validation tests

2. ✅ **CLI Interface Foundation**
   - 4 commands implemented: `exec`, `config validate`, `config init`, `version`
   - Error handling with user-friendly messages
   - Click framework with 83% test coverage
   - Comprehensive help text

3. ✅ **Routing Engine Core**
   - Smart routing logic with preference resolution
   - Cost optimization hooks (token thresholds)
   - Fallback chain implementation
   - 97% test coverage, 14 routing tests

**Deliverables:**
- ✅ Working configuration system (93% loader coverage)
- ✅ Functional CLI with mocked execution
- ✅ Routing engine with 93% overall coverage (exceeded 80% target)

**Key Metrics:**
- **Test Coverage:** 93% (Target: >80%) ✅ EXCEEDED
- **Tests:** 65/65 passing ✅ PERFECT
- **Code Quality:** Zero critical bugs ✅ CLEAN
- **Architecture:** 100% aligned with ADR-025 ✅ APPROVED

---

### Milestone 2: Tool Integration (Weeks 2-3) - 🚀 IN PROGRESS

**Status:** 🚀 **IN PROGRESS** - Batches 2.1 & 2.2 complete, ready for 2.3  
**Blockers:** ✅ NONE - Adapter infrastructure ready, strategic pivot approved  
**Estimated Completion:** End of week 3

**Strategic Pivot (2026-02-05):** ⭐ **Generic YAML-Driven Adapter Approach**
- **Decision:** Use single `GenericYAMLAdapter` instead of multiple concrete adapters
- **Rationale:** Eliminates code duplication, YAML-based extensibility, faster to MVP
- **Impact:** Add new tools via YAML configuration, no code changes needed
- **ClaudeCodeAdapter:** Kept as reference implementation and test fixture
- **Reference:** ADR-029 updated (2026-02-05), Architecture review in `work/analysis/`

**Goal:** Implement generic YAML-driven adapter with tool extensibility

**Batches:**
1. ✅ **Batch 2.1: Tool Adapter Architecture** (~2.5 hours) **COMPLETE**
   - ✅ Base adapter interface/abstract class
   - ✅ Command template parsing and substitution
   - ✅ Subprocess execution wrapper with error handling
   - ✅ Output normalization framework
   - **Achievement:** 84% faster than 12-16h estimate, 93% coverage, 78/78 tests passing
   - **Agent:** Backend-dev Benny (exceptional performance)

2. ✅ **Batch 2.2: ClaudeCodeAdapter Reference Implementation** (1-2 days) **COMPLETE**
   - ✅ Implemented ClaudeCodeAdapter using command template
   - ✅ Platform-specific binary path resolution
   - ✅ Model parameter mapping
   - ✅ Integration tests with mocked claude CLI (`fake_claude_cli.py`)
   - **Status:** Kept as reference implementation and test fixture
   - **Decision:** Generic YAML adapter is production path (see ADR-029 update)

3. 📋 **Batch 2.3: Generic YAML Adapter** (1 day / 5-8 hours) **READY TO START**
   - Implement `GenericYAMLAdapter` that reads tool definitions from YAML
   - Single adapter works with ANY tool defined in YAML configuration
   - Binary resolution from config or PATH
   - ENV variable support for API keys and tool configuration
   - Demonstrate adding new tools (codex, gemini, etc.) via YAML only
   - **Strategic Value:** ⭐⭐⭐⭐⭐ Eliminates code duplication, enables YAML-driven extensibility
   - **Decision:** Production implementation path per ADR-029 (2026-02-05)

4. ~~**Batch 2.4: Codex Adapter**~~ **REMOVED - Replaced by Generic Adapter**
   - ❌ No longer needed - Generic adapter handles codex via YAML
   - ✅ Add codex tool via YAML config instead of code

**Deliverables:**
- ✅ Adapter base infrastructure (Batch 2.1)
- ✅ ClaudeCodeAdapter reference implementation (Batch 2.2) - kept as test fixture
- 📋 Generic YAML adapter enabling tool extensibility without code changes (Batch 2.3)
- Integration with routing engine using GenericYAMLAdapter
- Integration test suite with >70% coverage

---

### Milestone 3: Cost Optimization & Telemetry (Week 3-4)
**Goal:** Implement budget enforcement and usage tracking

**Batches:**
1. **Batch 3.1: Telemetry Infrastructure** (2-3 days)
   - SQLite database schema for invocation logs
   - Telemetry logger with token/cost/latency tracking
   - Database initialization and migration support
   - Privacy controls (metadata-only vs. full logging)

2. **Batch 3.2: Policy Engine** (3-4 days)
   - Budget tracking (daily/monthly limits)
   - Cost optimization (task complexity → model selection)
   - Configurable limit enforcement (soft warnings vs. hard blocks)
   - Rate limiting support

3. **Batch 3.3: Stats & Reporting** (2 days)
   - `llm-service stats` command implementation
   - Daily/monthly cost reports
   - Per-agent and per-model breakdowns
   - CSV/JSON export for external analysis

**Deliverables:**
- Working telemetry system logging all invocations
- Policy engine enforcing budget limits
- Stats command providing actionable cost insights

---

### Milestone 4: End-to-End Integration & Testing (Week 4)
**Goal:** Connect all components and validate with acceptance tests

**Batches:**
1. **Batch 4.1: Integration Testing** (2-3 days)
   - Implement 8 acceptance tests from prestudy (Gherkin scenarios)
   - End-to-end workflows (config → routing → execution → telemetry)
   - Cross-platform testing matrix (Linux, macOS, WSL2)
   - Error scenarios and fallback validation

2. **Batch 4.2: Documentation & Examples** (2 days)
   - User guide and quickstart
   - Configuration reference with all options explained
   - Example workflows for 3 personas (AI Power User, Software Engineer, Process Architect)
   - Troubleshooting guide

3. **Batch 4.3: Distribution & Packaging** (1-2 days)
   - PyInstaller/pkg standalone executable
   - Installation script for Linux/macOS
   - WSL2 setup instructions for Windows
   - GitHub Release preparation

**Deliverables:**
- Passing acceptance test suite (all 8 scenarios)
- Comprehensive documentation
- Distributable binaries for all platforms
- MVP ready for pilot deployment

---

## Task Assignments (File-Based Orchestration)

Tasks will be created as YAML files in `work/collaboration/inbox/` following the work directory orchestration approach. Each task will be assigned to the appropriate specialist agent.

### Configuration & Foundation Tasks → Backend-Dev

**Tasks:**
1. `2026-02-04T1700-backend-dev-config-schema-definition.yaml`
   - Define YAML schemas (agents, tools, models, policies)
   - Implement Pydantic models for validation

2. `2026-02-04T1701-backend-dev-config-loader-implementation.yaml`
   - Implement configuration loader with validation
   - Error handling and user-friendly messages

3. `2026-02-04T1702-backend-dev-cli-interface-foundation.yaml`
   - Implement CLI using Click/Commander
   - Commands: exec, config validate, config init, version

4. `2026-02-04T1703-backend-dev-routing-engine-core.yaml`
   - Agent-to-tool mapping logic
   - Fallback chain implementation

### Tool Integration Tasks → Backend-Dev

**Tasks:**
5. `2026-02-04T1704-backend-dev-adapter-base-interface.yaml` ✅ COMPLETE
   - Base adapter architecture
   - Command template parsing

6. `2026-02-04T1705-backend-dev-claude-code-adapter.yaml` ✅ COMPLETE
   - Claude-Code reference adapter implementation
   - Integration tests
   - **Status:** Kept as reference/test fixture

7. ~~`2026-02-04T1706-backend-dev-codex-adapter.yaml`~~ ❌ REMOVED
   - Replaced by generic YAML adapter approach

8. `2026-02-04T1707-backend-dev-generic-yaml-adapter.yaml` 📋 NEXT
   - Generic YAML-configured adapter (production implementation)
   - Extensibility for any tool via YAML configuration
   - ENV variable support for API keys
   - **Priority:** HIGH - Production path for all tools

### Telemetry & Policy Tasks → Backend-Dev

**Tasks:**
9. `2026-02-04T1708-backend-dev-telemetry-infrastructure.yaml`
   - SQLite database schema
   - Invocation logging

10. `2026-02-04T1709-backend-dev-policy-engine.yaml`
    - Budget tracking and enforcement
    - Cost optimization logic

11. `2026-02-04T1710-backend-dev-stats-reporting.yaml`
    - Stats command implementation
    - Report generation (daily/monthly)

### Testing Tasks → Backend-Dev + Framework-Guardian

**Tasks:**
12. `2026-02-04T1711-backend-dev-acceptance-tests.yaml`
    - Implement 8 Gherkin scenarios from prestudy
    - End-to-end test suite

13. `2026-02-04T1712-framework-guardian-ci-integration.yaml`
    - GitHub Actions workflow for cross-platform testing
    - Automated test execution

### Documentation Tasks → Writer-Editor + Scribe

**Tasks:**
14. `2026-02-04T1713-writer-editor-user-guide.yaml`
    - User guide and quickstart
    - Configuration reference

15. `2026-02-04T1714-scribe-persona-workflows.yaml`
    - Example workflows for 3 personas
    - Troubleshooting guide

### Distribution Tasks → Build-Automation

**Tasks:**
16. `2026-02-04T1715-build-automation-packaging.yaml`
    - PyInstaller/pkg configuration
    - Standalone executables

17. `2026-02-04T1716-build-automation-installation-scripts.yaml`
    - Installation scripts for Linux/macOS/WSL2
    - GitHub Release preparation

---

## Dependencies

**Critical Path:**
1. Configuration Schema (Task 1) → Config Loader (Task 2) → CLI Foundation (Task 3) → Routing Engine (Task 4)
2. Adapter Base (Task 5) → Claude Adapter (Task 6) + Codex Adapter (Task 7) → Generic Adapter (Task 8)
3. Telemetry (Task 9) → Policy Engine (Task 10) → Stats Reporting (Task 11)
4. All core tasks (1-11) → Acceptance Tests (Task 12)
5. Acceptance Tests (Task 12) → Documentation (Tasks 14-15) → Packaging (Tasks 16-17)

**Parallel Work Streams:**
- Batch 1.1-1.3 (Foundation) can progress in parallel after configuration schema is defined
- Batch 2.2-2.3 (Adapters) can be built in parallel after base interface exists
- Documentation (Tasks 14-15) can start early with draft content, finalized after testing

**Blocking Risks:**
- Tech stack choice (Python vs. Node.js) must be decided before implementation begins
- Real tool availability (claude-code, codex CLIs) needed for integration testing
- Cross-platform testing requires access to Linux, macOS, and Windows/WSL2 environments

---

## Assumptions

1. **Team Capacity:** 1-2 developers available for 4-week sprint
2. **Tool Access:** claude-code and codex CLIs available for testing (or mocks acceptable for MVP)
3. **Platform Access:** CI/CD supports Linux + macOS + Windows/WSL2 matrix testing
4. **Tech Stack Decision:** Python or Node.js chosen within first week
5. **Configuration Stability:** YAML schema finalized in Batch 1.1 (minimal changes after)

---

## Re-Planning Triggers

- **Tech Stack Change:** If Python/Node.js choice changes mid-project, re-estimate 2-3 days for port
- **Scope Expansion:** If additional tools (gemini, cursor) required for MVP, add 1 week per tool
- **Platform Issues:** If WSL2 testing blocked, may need to defer Windows support to Phase 2
- **Performance Problems:** If routing/execution latency >500ms, may need optimization sprint (add 3-5 days)

---

## Next Steps

1. **Immediate:** Create task YAML files in `work/collaboration/inbox/` for all 17 tasks
2. **Week 1 Start:** Begin Batch 1.1 (Configuration Schema) after tech stack decision
3. **Weekly Sync:** Review progress against milestones, adjust batches as needed
4. **Human Gates:** Approval required before Milestone 3 (cost implications) and Milestone 4 (distribution)

---

## References

- **Architecture Prestudy:** `docs/architecture/design/llm-service-layer-prestudy.md`
- **Diagrams:** `docs/architecture/diagrams/llm-service-layer-*.puml`
- **Orchestration Approach:** `.github/agents/approaches/work-directory-orchestration.md`
- **Agent Profiles:** `.github/agents/*.agent.md`
- **Planning Artifacts:** `docs/planning/` (this directory)

---

## Current Status Update (2026-02-04 20:45:00 UTC)

### 🎉 MILESTONE 1 & M2 PREP COMPLETE

**Status:** ✅ **COMPLETE** - All acceptance criteria met or exceeded

**Completed Work:**
1. ✅ **Architect Alphonso** - Prestudy + Milestone 1 Architectural Review
   - Created `llm-service-layer-prestudy.md` (4,400+ lines)
   - Reviewed implementation, approved for M2
   - Identified 3 tactical ADRs needed (Pydantic, Click, tool-model validation)
   
2. ✅ **Backend-dev Benny** - Foundation Implementation + Code Enhancement
   - Built configuration system (schemas, loader, routing)
   - Implemented CLI foundation (4 commands)
   - Enhanced test coverage: 81% → 93% (+12%)
   - Added 45 tests (20 → 65 tests)
   - Fixed critical issues (tool-model validation, error messages)

**Quality Metrics:**
- ✅ **Test Coverage:** 93% (target: 80%) - EXCEEDED
- ✅ **Tests Passing:** 65/65 (100%) - PERFECT
- ✅ **Code Quality:** Zero critical bugs
- ✅ **Architecture Review:** APPROVED by Alphonso
- ✅ **Strategic Alignment:** 100% with ADR-025

**Strategic Impact:**
- ✅ Foundation ready for Milestone 2-4 progression
- ✅ Projected savings: $3K-6K annual per team (30-56% token cost reduction)
- ✅ Extensible YAML-driven architecture
- ✅ Clean separation of concerns

**Work Logs Created:**
- `work/reports/logs/architect/2026-02-04T0708-service-layer-prestudy.md`
- `work/reports/logs/backend-dev/2026-02-04T1700-config-schema-definition.md`
- `work/reports/logs/backend-dev/2026-02-04T1927-backend-dev-alphonso-review.md`
- `work/reports/2026-02-04-architect-alphonso-milestone1-review.md` (14-page review)
- `work/reports/2026-02-04T1936-backend-dev-task-completion-summary.md`
- `work/reports/exec_summaries/2026-02-04-llm-service-milestone1-exec-summary.md`

---

### ✅ M2 PREP BATCH COMPLETE (2026-02-04)

**Status:** ✅ **COMPLETE** (5/5 tasks done)  
**Agent:** Architect Alphonso  
**Duration:** 3h 10m (estimated: 4h 15m)  
**Efficiency:** ⭐ **134%** (25% faster than estimate)

**Completed Work:**

1. ✅ **ADR-026: Pydantic V2 for Schema Validation** (12KB, 298 lines)
   - Decision context preserved for validation framework choice
   - Trade-offs documented: Type integration vs. learning curve
   - Status: ACCEPTED

2. ✅ **ADR-027: Click for CLI Framework** (13KB, 376 lines)
   - CLI framework selection rationale documented
   - Trade-offs: Mature ecosystem vs. type safety
   - Status: ACCEPTED

3. ✅ **ADR-028: Tool-Model Compatibility Validation** (14KB, 391 lines)
   - Enhancement decision documented (credits Backend-dev Benny)
   - Prevents runtime configuration errors
   - Status: ACCEPTED

4. ✅ **ADR-029: Adapter Interface Design** (14KB, 383 lines)
   - Decision: Abstract Base Class with Protocol option
   - Enables extensibility + type safety
   - Status: ACCEPTED

5. ✅ **Adapter Interface Review** (20KB, 633 lines)
   - 3 options evaluated (ABC vs. Protocol vs. duck typing)
   - Recommendation: ABC for MVP, Protocol for future extensibility
   - Unblocks M2 Batch 2.1

6. ✅ **Security Review** (14KB, 415 lines)
   - Command template injection risks assessed
   - Current posture: Trusted YAML (low risk)
   - Mitigation strategy documented for M2 implementation

**Total Deliverables:** 7 comprehensive documents (~75KB)

**Quality Metrics:**
- ✅ **Decision Traceability:** 100% compliance with Directive 018
- ✅ **ADR Quality:** All follow standard template
- ✅ **Strategic Alignment:** M2 fully unblocked
- ✅ **Time Efficiency:** 134% (3h 10m vs 4h 15m estimated)

**M2 Readiness:**
- ✅ Tactical ADRs complete
- ✅ Adapter interface design decided
- ✅ Security posture documented
- ✅ NO BLOCKERS for M2 kickoff

---

### 🎉 MILESTONE 2 BATCH 2.1 COMPLETE (2026-02-05)

**Status:** ✅ **COMPLETE** - All tasks delivered ahead of schedule

**Achievement:** M2 Batch 2.1 - Adapter Base Interface  
**Agent:** Backend-dev Benny  
**Actual Duration:** ~2.5 hours (estimated: 12-16h)  
**Efficiency:** ⭐ **84% faster than estimate**

**Completed Deliverables:**
1. ✅ Base adapter abstract class (`ToolAdapter` in `src/llm_service/adapters/base.py`)
2. ✅ Command template parsing and substitution (`CommandTemplateHandler`)
3. ✅ Subprocess execution wrapper with error handling (`SubprocessExecutor`)
4. ✅ Security: Command injection prevention implemented
5. ✅ Platform compatibility: Validated for Linux/macOS/Windows
6. ✅ Test coverage: 93% across all adapter modules
7. ✅ Tests passing: 78/78 (100% success rate)

**Key Achievements:**
- ✅ **Performance:** Completed in ~2.5 hours vs. 12-16h estimate (6.4x faster)
- ✅ **Quality:** Zero test failures, 93% coverage maintained
- ✅ **Security:** Command injection protection implemented
- ✅ **Extensibility:** Clean adapter interface for concrete implementations
- ✅ **Ready for M2 Batch 2.2:** ClaudeCodeAdapter can start immediately

**Files Delivered:**
- `src/llm_service/adapters/base.py` - Abstract base class
- `src/llm_service/adapters/command_template.py` - Template handler
- `src/llm_service/adapters/subprocess_executor.py` - Subprocess wrapper
- `tests/unit/adapters/` - Comprehensive test suite (13 new tests)

---

### ✅ MILESTONE 2 BATCH 2.2 COMPLETE (2026-02-05)

**Status:** ✅ **COMPLETE** - Reference implementation delivered

**Achievement:** M2 Batch 2.2 - ClaudeCodeAdapter Reference Implementation  
**Agent:** Backend-dev Benny  
**Purpose:** Reference implementation and test fixture  
**Strategic Decision:** Generic YAML adapter is production path (ADR-029 updated)

**Completed Deliverables:**
1. ✅ ClaudeCodeAdapter class (~400 lines)
2. ✅ Model parameter mapping
3. ✅ Platform-specific binary path resolution
4. ✅ Integration tests with `fake_claude_cli.py` mock
5. ✅ User-friendly error handling

**Strategic Outcome:**
- ✅ **Validates Infrastructure:** Proves Batch 2.1 base classes work correctly
- ✅ **Reference Implementation:** Documents adapter best practices
- ✅ **Test Fixture:** `fake_claude_cli.py` used for testing framework
- ✅ **Decision Made:** Generic YAML adapter approach approved for production
- ✅ **No Code Duplication:** Future tools added via YAML, not new adapter classes

**Files Delivered:**
- `src/llm_service/adapters/claude_code_adapter.py` - Reference adapter (kept for tests)
- `tests/integration/adapters/test_claude_code_adapter.py` - Integration tests
- `tests/fixtures/fake_claude_cli.py` - Mocked CLI for testing

---

### 📋 NEXT: Milestone 2 Batch 2.3 - Generic YAML Adapter Implementation

**Status:** 🟢 **READY FOR ASSIGNMENT**

**Task:** Implement production generic adapter for YAML-driven tool extensibility  
**Agent:** Backend-dev Benny  
**Estimated Effort:** 1 day (5-8 hours)  
**Dependencies:** ✅ All met (Batches 2.1 & 2.2 complete)

**Deliverables:**
- GenericYAMLAdapter class that works with any YAML-defined tool
- ENV variable support (${VAR} expansion from YAML config)
- Binary resolution from config or PATH
- Integration with routing engine
- Update YAML schema to support env_vars configuration
- Demonstrate adding new tools via YAML without code changes

**Focus Areas:**
- Single adapter replaces need for concrete tool-specific adapters
- YAML-driven extensibility (add tools via config, not code)
- ENV variable support for API keys and configuration
- Production-ready implementation (ClaudeCodeAdapter becomes test-only)

---

### 🚫 Previous Status (Resolved)

~~**Task Creation Progress: 3/17 (18%)**~~ ← No longer relevant

**Resolution:** Milestone 1 completed via direct implementation approach rather than incremental task creation. Tasks 1-4 fully delivered as integrated foundation.

---
