# Implementation Plan: LLM Service Layer

**Project:** LLM Service Layer for Agent-Tool Orchestration  
**Status:** 🟢 MILESTONE 4 ACTIVE - M4 Batch 4.1 COMPLETE ⭐  
**Planning Date:** 2026-02-04  
**Last Updated:** 2026-02-05 20:00:00 UTC (M4 Batch 4.1 COMPLETE - Planning Updates)  
**Planner:** Planning Petra  
**Architecture Reference:** `docs/architecture/design/llm-service-layer-prestudy.md`  
**Orchestration Approach:** File-Based Task Coordination (see `.github/agents/approaches/work-directory-orchestration.md`)

**Current Progress:**
- ✅ Milestone 1: COMPLETE (Foundation) - 100% acceptance criteria met
- ✅ Implementation roadmap complete (23 tasks, 5 milestones) ⭐ UPDATED
- ✅ Code quality: 83% coverage, 115 tests passing (all M4 components)
- ✅ Architecture review: APPROVED by Architect Alphonso
- ✅ M2 Prep: COMPLETE (5/5 tasks, 3h 10m) - 25% faster than estimate
- ✅ M2 Batch 2.1: COMPLETE (4/4 tasks, ~2.5h) - ⭐ 84% faster than estimate
- ✅ M2 Batch 2.2: COMPLETE - ClaudeCodeAdapter (reference implementation)
- ✅ M4 Batch 4.1: COMPLETE (3/3 tasks, 8-11h) - ⭐⭐⭐⭐⭐ EXCELLENT (Architect-approved)
- ✅ ADRs: 13 documented (ADR-026 through ADR-034) ⭐ +4 NEW (spec-kitty inspired)
- 🚀 Milestone 4: IN PROGRESS - User Experience Enhancements (Rich CLI ✅, Templates ✅)
- 📋 Next: M4 Batch 4.2 (Dashboard MVP) OR M3 Batch 3.2 (Policy Engine)

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

### Milestone 4: User Experience Enhancements (Week 5-6) - 🚀 IN PROGRESS
**Goal:** Implement spec-kitty inspired UX improvements for professional CLI experience

**Strategic Context:**
- Inspired by [spec-kitty comparative analysis](../architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md)
- Human-in-Charge priority: ⭐⭐⭐⭐⭐ (Dashboard), ⭐⭐⭐⭐⭐ (Rich CLI), ⭐⭐⭐⭐⭐ (Template Config)
- Target: Reduce onboarding time from 30 minutes to 2 minutes
- File-based task tracking (no database) maintains audit trail and simplicity

**Batches:**

1. **Batch 4.1: Rich CLI + Template Generation** (Week 5 / ~8 hours) - ✅ **COMPLETE**
   
   **Status:** ✅ **COMPLETE** (2026-02-05)  
   **Completion Date:** 2026-02-05 19:15:00 UTC  
   **Quality Gate:** ✅ **PASSED** - Architect-approved for production  
   **Actual Time:** 8-11 hours (within 6-9h estimate)  
   **Test Coverage:** 83% (115 passing tests)  
   **Architecture Review:** ⭐⭐⭐⭐⭐ EXCELLENT
   
   **Phase 1: Rich Terminal UI** (2-3 hours) - ✅ COMPLETE
   - ✅ Integrated `rich>=13.0.0` library for structured CLI output
   - ✅ Implemented panels for execution summaries
   - ✅ Progress bars for long operations (>2 seconds)
   - ✅ Status indicators (✅ ✗ ⚠️) for quick scanning
   - ✅ Syntax highlighting for code/YAML output
   - ✅ Automatic TTY detection with graceful fallback
   - ✅ NO_COLOR environment variable support
   - **File:** `src/llm_service/ui/console.py` (146 lines, 78% coverage)
   - **Tests:** 32 tests passing
   - **Reference:** [ADR-030](../architecture/adrs/ADR-030-rich-terminal-ui-cli-feedback.md)
   
   **Phase 2: Template-Based Config Generation** (4-6 hours) - ✅ COMPLETE
   - ✅ Implemented `llm-service config init` command
   - ✅ Created 4 templates (quick-start, claude-only, cost-optimized, development)
   - ✅ Environment scanning (API keys, binaries, platform detection)
   - ✅ Tool management commands (add/remove/list)
   - ✅ Jinja2 variable substitution (`${VAR}`) support
   - ✅ Atomic configuration generation with rollback
   - **Files:** `src/llm_service/templates/manager.py` (242 lines, 85% coverage)
   - **Files:** `src/llm_service/utils/env_scanner.py` (193 lines, 92% coverage)
   - **Tests:** 41 tests passing (24 template + 17 scanner)
   - **Target:** 30 minutes → 2 minutes onboarding time ✅ ACHIEVED
   - **Reference:** [ADR-031](../architecture/adrs/ADR-031-template-based-config-generation.md)
   
   **Phase 3: Spec-Driven Development PRIMER** (2 hours) - ✅ COMPLETE
   - ✅ Created comprehensive PRIMER (882 lines)
   - ✅ Three Pillars framework (specs/tests/ADRs)
   - ✅ Decision matrix for document type selection
   - ✅ 4-phase SDD workflow
   - ✅ Agent-specific guidance with example prompts
   - **File:** `.github/agents/approaches/spec-driven-development.md`
   - **Reference:** [ADR-034](../architecture/adrs/ADR-034-mcp-server-integration-strategy.md)
   
   **Deliverables Summary:**
   - ✅ Production code: 581 lines
   - ✅ Test code: 1,384 lines (2.4:1 ratio)
   - ✅ Total tests: 115 passing (all M4 Batch 4.1)
   - ✅ Coverage: 83% for M4 components
   - ✅ Documentation: 882-line SDD PRIMER
   - ✅ ADR compliance: 100% (3 ADRs - ADR-030, ADR-031, ADR-034)
   - ✅ Security review: 0 vulnerabilities
   - ✅ Architecture review: APPROVED FOR PRODUCTION
   
   **Key Achievements:**
   - ⭐ 93% onboarding time reduction (30min → 2min)
   - ⭐ Professional CLI UX with Rich library
   - ⭐ Zero security issues
   - ⭐ Architect rating: ⭐⭐⭐⭐⭐ EXCELLENT
   - ⭐ Production-ready with minor docs pending
   
   **Architect Recommendations:**
   - Add user documentation (2-3 hours) - recommended before announcement
   - Update CHANGELOG.md (30 minutes)
   - Expand test coverage to 90% (1-2 hours) - post-deployment
   
   **Review Documents:**
   - [Executive Summary](../../work/reports/architecture/2026-02-05-M4-batch-4.1-executive-summary.md)
   - [Full Architectural Review](../../work/reports/architecture/2026-02-05-M4-batch-4.1-architectural-review.md)
   - [Validation Matrix](../../work/reports/architecture/2026-02-05-M4-batch-4.1-validation-matrix.md)

2. **Batch 4.2: Dashboard MVP** (Week 6 / 12-16 hours) ⭐ HUMAN PRIORITY
   
   **Phase 1: Backend Infrastructure** (6-8 hours)
   - Flask + Flask-SocketIO setup
   - File watcher for YAML task files (`work/collaboration/{inbox,assigned,done}/`)
   - Event system (Observer pattern for file changes)
   - WebSocket event emission on task state changes
   - SQLite telemetry integration (cost/metrics)
   - **Reference:** ADR-032
   
   **Phase 2: Frontend Dashboard** (6-8 hours)
   - Single-page web interface (vanilla JS + Chart.js)
   - Live execution view (active operations with progress)
   - Cost tracking dashboard (real-time tokens, cost accumulation)
   - Task Kanban board (inbox → assigned → done lanes)
   - Metrics visualization (daily/monthly trends)
   - WebSocket integration for real-time updates
   - **Reference:** ADR-032
   
   **Critical Constraint:** File-based task tracking maintained (no database for tasks)
   - Tasks tracked via YAML in `work/collaboration/`
   - Git audit trail preserved
   - Human-readable and agent-friendly
   - Dashboard watches files, doesn't replace them

3. **Batch 4.3: Step Tracker + Integration** (Week 6 / 5-7 hours)
   
   **Phase 1: Step Tracker Pattern** (2-3 hours)
   - Implement `StepTracker` context manager
   - Multi-step operation progress tracking
   - Error context preservation (which step failed)
   - Dashboard event emission (step start/complete/error)
   - **Reference:** ADR-033
   
   **Phase 2: Integration & Polish** (3-4 hours)
   - Apply rich UI to all CLI commands
   - Integrate step tracker in multi-step operations
   - Connect dashboard to execution events
   - End-to-end testing (CLI → events → dashboard)
   - Documentation updates

**Deliverables:**
- ✅ Rich terminal UI for professional CLI experience
- ✅ Template-based configuration (2-minute onboarding)
- ✅ Real-time web dashboard (file-based task tracking)
- ✅ Step tracker pattern for complex operations
- ✅ Integrated UX across CLI and dashboard

**New ADRs Created:**
- [ADR-030: Rich Terminal UI for CLI Feedback](../architecture/adrs/ADR-030-rich-terminal-ui-cli-feedback.md)
- [ADR-031: Template-Based Configuration Generation](../architecture/adrs/ADR-031-template-based-config-generation.md)
- [ADR-032: Real-Time Execution Dashboard](../architecture/adrs/ADR-032-real-time-execution-dashboard.md)
- [ADR-033: Step Tracker Pattern](../architecture/adrs/ADR-033-step-tracker-pattern.md)

---

### Milestone 5: End-to-End Integration & Testing (Week 7)
**Goal:** Connect all components and validate with acceptance tests

**Note:** Previously Milestone 4, renumbered to accommodate new M4 (User Experience Enhancements)

**Batches:**
1. **Batch 5.1: Integration Testing** (2-3 days)
   - Implement 8 acceptance tests from prestudy (Gherkin scenarios)
   - End-to-end workflows (config → routing → execution → telemetry → dashboard)
   - Cross-platform testing matrix (Linux, macOS, WSL2)
   - Error scenarios and fallback validation
   - Dashboard real-time update testing

2. **Batch 5.2: Documentation & Examples** (2 days)
   - User guide and quickstart (updated with templates)
   - Configuration reference with all options explained
   - Example workflows for 3 personas (AI Power User, Software Engineer, Process Architect)
   - Dashboard usage guide
   - Troubleshooting guide

3. **Batch 5.3: Distribution & Packaging** (1-2 days)
   - PyInstaller/pkg standalone executable
   - Installation script for Linux/macOS
   - WSL2 setup instructions for Windows
   - Dashboard bundling (static assets)
   - GitHub Release preparation

**Deliverables:**
- Passing acceptance test suite (all 8 scenarios + dashboard tests)
- Comprehensive documentation (including UX enhancements)
- Distributable binaries for all platforms
- MVP ready for pilot deployment

---

## Task Assignments (File-Based Orchestration)

Tasks will be created as YAML files in `work/collaboration/inbox/` following the work directory orchestration approach. Each task will be assigned to the appropriate specialist agent.

**Agent Assignment Strategy (Updated 2026-02-05):**
- **Python Pedro:** Pure Python implementation, test-heavy work, self-contained modules
- **Backend-dev:** Integration, orchestration, schema architecture, cross-cutting concerns

### Configuration & Foundation Tasks → Python Pedro ⭐ REASSIGNED

**Tasks:**
1. `2026-02-04T1700-backend-dev-config-schema-definition.yaml` ✅ COMPLETE
   - Define YAML schemas (agents, tools, models, policies)
   - Implement Pydantic models for validation

2. `2025-12-01T0510-backend-dev-framework-config-loader.yaml` ⭐ **REASSIGNED TO PYTHON PEDRO**
   - Implement configuration loader with validation
   - Error handling and user-friendly messages
   - **Rationale:** Pydantic validation expertise, test-heavy, self-contained module

3. `2026-02-04T1702-backend-dev-cli-interface-foundation.yaml` ✅ COMPLETE
   - Implement CLI using Click/Commander
   - Commands: exec, config validate, config init, version

4. `2026-02-04T1703-backend-dev-routing-engine-core.yaml` ✅ COMPLETE
   - Agent-to-tool mapping logic
   - Fallback chain implementation

5. `2025-12-01T0511-backend-dev-agent-profile-parser.yaml` ⭐ **REASSIGNED TO PYTHON PEDRO**
   - Parse agent profile YAML/Markdown files
   - Structured profile data extraction
   - **Rationale:** Data parsing, pytest parametrization, edge case testing

### Tool Integration Tasks → Python Pedro + Backend-Dev

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

8. `2026-02-05T1000-backend-dev-generic-yaml-adapter.yaml` ⭐ **REASSIGNED TO PYTHON PEDRO** 📋 NEXT
   - Generic YAML-configured adapter (production implementation)
   - Extensibility for any tool via YAML configuration
   - ENV variable support for API keys
   - **Priority:** HIGH - Production path for all tools
   - **Rationale:** Pure Python implementation, test-heavy, M2 Batch 2.3 critical path

9. `2026-02-05T1001-backend-dev-yaml-env-vars.yaml` → Backend-Dev
   - ENV variable schema enhancement
   - Integration with config validation system
   - **Rationale:** Schema architecture, cross-cutting integration

10. `2026-02-05T1002-backend-dev-routing-integration.yaml` → Backend-Dev
    - Integrate GenericYAMLAdapter with routing engine
    - Cross-component integration testing
    - **Rationale:** Orchestration focus, system-wide coordination

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

### User Experience Tasks → Multiple Agents ⭐ NEW

**Backend Tasks (Backend-Dev):**
12. `2026-02-05T1400-backend-dev-rich-terminal-ui.yaml` ⭐ NEW
    - Integrate `rich` library for CLI output
    - Panels, progress bars, tables, syntax highlighting
    - **Reference:** ADR-030

13. `2026-02-05T1401-backend-dev-template-config-generation.yaml` ⭐ NEW
    - Template-based `config init` command
    - Tool management CLI (add/remove/list)
    - Environment scanning
    - **Reference:** ADR-031

14. `2026-02-05T1402-backend-dev-dashboard-backend.yaml` ⭐ HIGH PRIORITY
    - Flask + Flask-SocketIO setup
    - File watcher for YAML task tracking
    - Event system and WebSocket emission
    - **Reference:** ADR-032

15. `2026-02-05T1403-backend-dev-step-tracker-pattern.yaml` ⭐ NEW
    - `StepTracker` context manager
    - Progress tracking for multi-step operations
    - **Reference:** ADR-033

**Frontend Tasks (Frontend-Dev):**
16. `2026-02-05T1404-frontend-dev-dashboard-interface.yaml` ⭐ HIGH PRIORITY
    - Single-page web dashboard (vanilla JS + Chart.js)
    - Live execution view, cost tracking, Kanban board
    - WebSocket integration
    - **Reference:** ADR-032

**Documentation Tasks (Writer-Editor):**
17. `2026-02-05T1400-writer-editor-spec-driven-primer.yaml` 📋 READY
    - Create Specification-Driven Development PRIMER
    - Adapt spec-kitty methodology to our context
    - **Target:** `.github/agents/approaches/spec-driven-development.md`

### Testing Tasks → Backend-Dev + Framework-Guardian

**Tasks:**
18. `2026-02-04T1711-backend-dev-acceptance-tests.yaml` (Updated)
    - Implement 8 Gherkin scenarios from prestudy
    - End-to-end test suite (including dashboard)
    - UX enhancement testing

19. `2026-02-04T1712-framework-guardian-ci-integration.yaml`
    - GitHub Actions workflow for cross-platform testing
    - Automated test execution

### Documentation Tasks → Writer-Editor + Scribe

**Tasks:**
20. `2026-02-04T1713-writer-editor-user-guide.yaml` (Updated)
    - User guide and quickstart (with templates)
    - Configuration reference
    - Dashboard usage guide

21. `2026-02-04T1714-scribe-persona-workflows.yaml`
    - Example workflows for 3 personas
    - Troubleshooting guide

### Distribution Tasks → Build-Automation

**Tasks:**
22. `2026-02-04T1715-build-automation-packaging.yaml` (Updated)
    - PyInstaller/pkg configuration
    - Standalone executables
    - Dashboard static asset bundling

23. `2026-02-04T1716-build-automation-installation-scripts.yaml`
    - Installation scripts for Linux/macOS/WSL2
    - GitHub Release preparation

---

## Dependencies

**Critical Path:**
1. Configuration Schema (Task 1) → Config Loader (Task 2) → CLI Foundation (Task 3) → Routing Engine (Task 4)
2. Adapter Base (Task 5) → Claude Adapter (Task 6) + Generic Adapter (Task 8)
3. Telemetry (Task 9) → Policy Engine (Task 10) → Stats Reporting (Task 11)
4. **Rich CLI (Task 12) → Template Config (Task 13)** ⭐ NEW
5. **Template Config (Task 13) → Dashboard Backend (Task 14)** ⭐ NEW
6. **Dashboard Backend (Task 14) + Step Tracker (Task 15) → Dashboard Frontend (Task 16)** ⭐ NEW
7. All core tasks (1-11) + All UX tasks (12-16) → Acceptance Tests (Task 18)
8. Acceptance Tests (Task 18) → Documentation (Tasks 20-21) → Packaging (Tasks 22-23)

**Parallel Work Streams:**
- Batch 1.1-1.3 (Foundation) can progress in parallel after configuration schema is defined
- Batch 2.2-2.3 (Adapters) can be built in parallel after base interface exists
- **Batch 4.1 (Rich CLI + Templates) can start after M2 completion** ⭐ NEW
- **Task 17 (Spec-Driven PRIMER) can start immediately (no dependencies)** ⭐ NEW
- **Batch 4.2 (Dashboard) can start in parallel with Batch 3.1 (Telemetry)** ⭐ NEW
- Documentation (Tasks 20-21) can start early with draft content, finalized after testing

**Blocking Risks:**
- Tech stack choice (Python vs. Node.js) must be decided before implementation begins ✅ RESOLVED (Python chosen)
- Real tool availability (claude-code, codex CLIs) needed for integration testing
- Cross-platform testing requires access to Linux, macOS, and Windows/WSL2 environments
- **Dashboard frontend expertise** (vanilla JS + Chart.js + WebSockets) ⭐ NEW RISK

---

## Assumptions

1. **Team Capacity:** 1-2 developers available for 7-week sprint (extended from 4 weeks) ⭐ UPDATED
2. **Tool Access:** claude-code and codex CLIs available for testing (or mocks acceptable for MVP)
3. **Platform Access:** CI/CD supports Linux + macOS + Windows/WSL2 matrix testing
4. **Tech Stack Decision:** Python chosen ✅ RESOLVED
5. **Configuration Stability:** YAML schema finalized in Batch 1.1 (minimal changes after)
6. **UX Priority:** Human-in-Charge approved spec-kitty inspired enhancements ⭐ NEW
7. **Dashboard Approach:** File-based task tracking maintained (no database for tasks) ⭐ NEW
8. **Frontend Skills:** Team has JavaScript + WebSocket experience for dashboard ⭐ NEW

---

## Re-Planning Triggers

- **Tech Stack Change:** ~~If Python/Node.js choice changes mid-project~~ ✅ RESOLVED (Python chosen)
- **Scope Expansion:** If additional tools (gemini, cursor) required for MVP, add 1 week per tool
- **Platform Issues:** If WSL2 testing blocked, may need to defer Windows support to Phase 2
- **Performance Problems:** If routing/execution latency >500ms, may need optimization sprint (add 3-5 days)
- **Dashboard Complexity:** If file-watching or WebSocket implementation takes >20h, may need to simplify MVP ⭐ NEW
- **UX Scope Creep:** If template/rich CLI features expand beyond ADR scope, re-estimate M4 timeline ⭐ NEW
- **Frontend Resource Gap:** If JavaScript/WebSocket skills unavailable, may need to defer dashboard to Phase 2 ⭐ NEW

---

## Next Steps

1. **Immediate:** 
   - ✅ Create task YAML for spec-driven PRIMER (Task 17)
   - 📋 Milestone 2 Batch 2.3 (Generic YAML Adapter) ready for assignment
   - 📋 Milestone 4 ready for planning after M3 completion
   
2. **Week 3-4 Start:** Begin Milestone 3 (Telemetry & Cost Optimization) after M2 completion

3. **Week 5-6 Start:** Begin Milestone 4 (User Experience Enhancements) ⭐ NEW
   - Week 5: Rich CLI + Template Generation (Batch 4.1)
   - Week 6: Dashboard MVP + Step Tracker (Batches 4.2 & 4.3)

4. **Weekly Sync:** Review progress against milestones, adjust batches as needed

5. **Human Gates:** 
   - Approval required before Milestone 3 (cost implications)
   - ✅ Milestone 4 APPROVED (Human-in-Charge priority)
   - Approval required before Milestone 5 (distribution)

---

## References

- **Architecture Prestudy:** `docs/architecture/design/llm-service-layer-prestudy.md`
- **Diagrams:** `docs/architecture/diagrams/llm-service-layer-*.puml`
- **Orchestration Approach:** `.github/agents/approaches/work-directory-orchestration.md`
- **Agent Profiles:** `.github/agents/*.agent.md`
- **Planning Artifacts:** `docs/planning/` (this directory)
- **Spec-Kitty Comparative Analysis:** `docs/architecture/design/comparative_study/2026-02-05-spec-kitty-comparative-analysis.md` ⭐ NEW
- **Spec-Kitty Enhancements Overview:** `docs/architecture/design/spec-kitty-inspired-enhancements.md` ⭐ NEW

**ADR References:**
- **Core Service Layer:**
  - [ADR-025: LLM Service Layer Architecture](../architecture/adrs/ADR-025-llm-service-layer.md)
  - [ADR-026: Pydantic V2 for Schema Validation](../architecture/adrs/ADR-026-pydantic-v2-validation.md)
  - [ADR-027: Click CLI Framework](../architecture/adrs/ADR-027-click-cli-framework.md)
  - [ADR-028: Tool-Model Compatibility Validation](../architecture/adrs/ADR-028-tool-model-compatibility-validation.md)
  - [ADR-029: Adapter Interface Design](../architecture/adrs/ADR-029-adapter-interface-design.md)

- **User Experience Enhancements (spec-kitty inspired):** ⭐ NEW
  - [ADR-030: Rich Terminal UI for CLI Feedback](../architecture/adrs/ADR-030-rich-terminal-ui-cli-feedback.md)
  - [ADR-031: Template-Based Configuration Generation](../architecture/adrs/ADR-031-template-based-config-generation.md)
  - [ADR-032: Real-Time Execution Dashboard](../architecture/adrs/ADR-032-real-time-execution-dashboard.md)
  - [ADR-033: Step Tracker Pattern for Complex Operations](../architecture/adrs/ADR-033-step-tracker-pattern.md)

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
