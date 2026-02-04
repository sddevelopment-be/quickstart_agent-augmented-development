# Implementation Plan: LLM Service Layer

**Project:** LLM Service Layer for Agent-Tool Orchestration  
**Status:** Approved - Ready for Implementation  
**Planning Date:** 2026-02-04  
**Planner:** Planning Petra  
**Architecture Reference:** `docs/architecture/design/llm-service-layer-prestudy.md`  
**Orchestration Approach:** File-Based Task Coordination (see `.github/agents/approaches/work-directory-orchestration.md`)

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

### Milestone 1: Foundation (Weeks 1-2)
**Goal:** Establish core infrastructure and configuration management

**Batches:**
1. **Batch 1.1: Configuration Schema & Validation** (3-4 days)
   - Define YAML schemas for agents, tools, models, policies
   - Implement configuration loader with Pydantic/JSON Schema validation
   - Create sample configuration files for MVP tools (claude-code, codex)
   - Unit tests for configuration parsing and validation

2. **Batch 1.2: CLI Interface Foundation** (2-3 days)
   - Implement basic CLI with Click/Commander
   - Commands: `exec`, `config validate`, `config init`, `version`
   - Error handling and user-friendly output formatting
   - Help text and usage examples

3. **Batch 1.3: Routing Engine Core** (3-4 days)
   - Agent-to-tool mapping logic
   - Model selection based on agent preferences
   - Fallback chain traversal
   - Unit tests for routing decisions

**Deliverables:**
- Working configuration system with validation
- Functional CLI accepting commands (mocked execution)
- Routing engine with test coverage >80%

---

### Milestone 2: Tool Integration (Weeks 2-3)
**Goal:** Implement tool adapters and subprocess execution

**Batches:**
1. **Batch 2.1: Tool Adapter Architecture** (2 days)
   - Base adapter interface/abstract class
   - Command template parsing and substitution
   - Subprocess execution wrapper with error handling
   - Output normalization framework

2. **Batch 2.2: Claude-Code Adapter** (2-3 days)
   - Implement Claude-Code adapter using command template
   - Platform-specific binary path resolution
   - Model parameter mapping
   - Integration tests with mocked claude CLI

3. **Batch 2.3: Codex Adapter** (2-3 days)
   - Implement Codex adapter using command template
   - Parameter formatting for codex CLI
   - Error handling for rate limits and auth issues
   - Integration tests with mocked codex CLI

4. **Batch 2.4: Generic YAML-Based Adapter** (2 days)
   - Implement generic adapter that reads tool definitions from YAML
   - Demonstrate adding a new tool without code changes
   - Documentation and examples for community contributions

**Deliverables:**
- Functional claude-code and codex adapters
- Generic adapter enabling YAML-based tool extensibility
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
5. `2026-02-04T1704-backend-dev-adapter-base-interface.yaml`
   - Base adapter architecture
   - Command template parsing

6. `2026-02-04T1705-backend-dev-claude-code-adapter.yaml`
   - Claude-Code adapter implementation
   - Integration tests

7. `2026-02-04T1706-backend-dev-codex-adapter.yaml`
   - Codex adapter implementation
   - Integration tests

8. `2026-02-04T1707-backend-dev-generic-yaml-adapter.yaml`
   - Generic YAML-configured adapter
   - Extensibility documentation

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

**Plan Status:** ✅ Complete - Ready for task creation and assignment  
**Next Action:** Create YAML task files in `work/collaboration/inbox/`
