# LLM Service Layer - Task Creation Checklist

**Date:** 2026-02-04  
**Prepared By:** Planning Petra  
**Purpose:** Detailed list of 14 missing tasks to be created as YAML files

---

## Summary

- **Total Tasks:** 17 (per roadmap)
- **Created:** 3 ✅
- **Missing:** 14 ❌
- **Creation Priority:** Sequential by milestone/batch
- **Estimated Creation Time:** 6-7 hours total

---

## Batch 1: Critical Foundation (CREATE FIRST) ⚡

**Priority:** CRITICAL  
**Timeline:** Create today (2026-02-04)  
**Estimated Creation Time:** 2 hours

### Task 1: Configuration Schema & Validation ❌

**Filename:** `2026-02-04T1700-backend-dev-config-schema-definition.yaml`  
**Agent:** backend-dev  
**Effort:** 3-4 days  
**Priority:** critical  
**Dependencies:** None

**Artefacts:**
- `src/llm_service/config/schemas.py` (or `config/schemas.js` for Node.js)
- `src/llm_service/config/models.py` (Pydantic models)
- `config/schemas/agent-schema.yaml`
- `config/schemas/tool-schema.yaml`
- `config/schemas/model-schema.yaml`
- `config/schemas/policy-schema.yaml`
- `config/sample-config.yaml`
- `tests/test_config_schema.py`
- `docs/configuration-schema.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  architecture_ref: "docs/architecture/design/llm-service-layer-prestudy.md"
  milestone: "Milestone 1: Foundation"
  batch: "Batch 1.1: Configuration Schema & Validation"
  notes:
    - "Define YAML schemas for: agents, tools, models, policies"
    - "Use Pydantic (Python) or JSON Schema (Node.js) for validation"
    - "Sample config must include claude-code and codex tool definitions"
    - "Schema should be extensible for future tools without code changes"
```

**Acceptance Criteria:**
- YAML schemas defined for all 4 entity types
- Pydantic models validate configuration with detailed error messages
- Sample configuration files validate successfully
- Unit tests cover schema validation edge cases (>80% coverage)
- Documentation explains schema structure with examples

**Blocks:** Tasks 2-17 (ALL remaining tasks depend on this)

---

### Task 2: Configuration Loader Implementation ❌

**Filename:** `2026-02-04T1701-backend-dev-config-loader-implementation.yaml`  
**Agent:** backend-dev  
**Effort:** 2-3 days  
**Priority:** critical  
**Dependencies:** Task 1

**Artefacts:**
- `src/llm_service/config/loader.py` (or `loader.js`)
- `src/llm_service/config/validator.py`
- `src/llm_service/config/merger.py` (config file merging logic)
- `tests/test_config_loader.py`
- `tests/fixtures/valid-config.yaml`
- `tests/fixtures/invalid-config.yaml`
- `docs/configuration-guide.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 1: Foundation"
  batch: "Batch 1.1: Configuration Schema & Validation"
  notes:
    - "Load YAML configuration from file or directory"
    - "Validate against schemas from Task 1"
    - "Support config merging (base + overrides)"
    - "Environment variable substitution (e.g., $API_KEY)"
    - "User-friendly error messages with line numbers"
```

**Acceptance Criteria:**
- Loads and validates configuration files
- Merges multiple config files (base + environment-specific)
- Environment variables interpolated correctly
- Validation errors show line numbers and helpful messages
- Unit tests >80% coverage

**Blocks:** Tasks 3-17 (12 tasks)

---

### Task 3: CLI Interface Foundation ❌

**Filename:** `2026-02-04T1702-backend-dev-cli-interface-foundation.yaml`  
**Agent:** backend-dev  
**Effort:** 2-3 days  
**Priority:** high  
**Dependencies:** Task 2

**Artefacts:**
- `src/llm_service/cli.py` (or `cli.js`)
- `src/llm_service/commands/exec.py`
- `src/llm_service/commands/config.py`
- `src/llm_service/commands/version.py`
- `tests/test_cli.py`
- `docs/cli-reference.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 1: Foundation"
  batch: "Batch 1.2: CLI Interface Foundation"
  notes:
    - "Use Click (Python) or Commander.js (Node.js)"
    - "Commands: exec, config validate, config init, version"
    - "Colored output for errors/success/info"
    - "Help text with examples for each command"
    - "JSON output mode for automation (--json flag)"
```

**Acceptance Criteria:**
- CLI accepts all 4 commands with correct arguments
- Help text explains usage with examples
- Error handling with user-friendly messages
- JSON output mode for scripting
- Integration tests for each command

**Blocks:** User interaction, end-to-end testing

---

### Task 4: Routing Engine Core ❌

**Filename:** `2026-02-04T1703-backend-dev-routing-engine-core.yaml`  
**Agent:** backend-dev  
**Effort:** 3-4 days  
**Priority:** high  
**Dependencies:** Task 2

**Artefacts:**
- `src/llm_service/routing/engine.py` (or `engine.js`)
- `src/llm_service/routing/selector.py` (model selection logic)
- `src/llm_service/routing/fallback.py` (fallback chain handler)
- `tests/test_routing.py`
- `docs/routing-logic.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 1: Foundation"
  batch: "Batch 1.3: Routing Engine Core"
  notes:
    - "Agent-to-tool mapping from configuration"
    - "Model selection based on agent preferences"
    - "Fallback chain traversal on errors/unavailability"
    - "Cost-based routing (prefer cheaper model if task_complexity='low')"
    - "Policy evaluation (budget limits, rate limits)"
```

**Acceptance Criteria:**
- Agent mapped to correct tool based on config
- Model selected according to preferences and policies
- Fallback chain tried in order on failures
- Cost optimization logic selects cheaper model when appropriate
- Unit tests >80% coverage with various scenarios

**Blocks:** Tool execution, telemetry, policy enforcement

---

## Batch 2: Tool Integration (CREATE AFTER TECH STACK DECISION)

**Priority:** HIGH  
**Timeline:** Create Week 1-2 (after Task 2 progress)  
**Estimated Creation Time:** 1.5 hours

### Task 5: Tool Adapter Base Interface ❌

**Filename:** `2026-02-04T1704-backend-dev-adapter-base-interface.yaml`  
**Agent:** backend-dev  
**Effort:** 2 days  
**Priority:** high  
**Dependencies:** Task 2

**Artefacts:**
- `src/llm_service/adapters/base.py` (or `base.js`)
- `src/llm_service/adapters/executor.py` (subprocess wrapper)
- `src/llm_service/adapters/normalizer.py` (output normalization)
- `tests/test_base_adapter.py`
- `docs/adapter-architecture.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 2: Tool Integration"
  batch: "Batch 2.1: Tool Adapter Architecture"
  notes:
    - "Abstract base class or interface for adapters"
    - "Command template parsing: '{binary} {prompt_file} --model {model}'"
    - "Parameter substitution with validation"
    - "Subprocess execution with timeout and error handling"
    - "Output normalization framework"
```

**Acceptance Criteria:**
- Base adapter class/interface defined
- Command template parser functional
- Subprocess wrapper handles timeouts, errors, signals
- Output normalization framework extensible
- Unit tests with mocked subprocess calls

**Blocks:** Tasks 6-8 (all adapter implementations)

---

### Task 6: Claude-Code Adapter ✅

**Filename:** `2026-02-04T1705-backend-dev-claude-code-adapter.yaml` ✅  
**Status:** CREATED (already in inbox)  
**Note:** Dependencies need update to reflect Task 5 requirement

---

### Task 7: Codex Adapter ❌

**Filename:** `2026-02-04T1706-backend-dev-codex-adapter.yaml`  
**Agent:** backend-dev  
**Effort:** 2-3 days  
**Priority:** medium  
**Dependencies:** Task 5

**Artefacts:**
- `src/llm_service/adapters/codex.py` (or `codex.js`)
- `tests/test_codex_adapter.py`
- `tests/mocks/codex_mock.py`
- `docs/adapters/codex-adapter.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 2: Tool Integration"
  batch: "Batch 2.3: Codex Adapter"
  notes:
    - "Implement codex adapter using base interface from Task 5"
    - "Command template from tools.yaml: 'codex {prompt_file} --model {model}'"
    - "Handle codex-specific parameters (temperature, max_tokens)"
    - "Error handling for: API rate limits, authentication, network issues"
    - "Integration tests with mocked codex CLI"
```

**Acceptance Criteria:**
- Adapter invokes mocked codex CLI correctly
- Parameter formatting matches codex expectations
- Error handling covers rate limits, auth, timeout
- Integration tests >70% coverage
- Documentation explains configuration

---

### Task 8: Generic YAML-Based Adapter ❌

**Filename:** `2026-02-04T1707-backend-dev-generic-yaml-adapter.yaml`  
**Agent:** backend-dev  
**Effort:** 2 days  
**Priority:** medium  
**Dependencies:** Task 5

**Artefacts:**
- `src/llm_service/adapters/generic.py` (or `generic.js`)
- `tests/test_generic_adapter.py`
- `config/tools/sample-tool.yaml` (example tool definition)
- `docs/adapters/generic-adapter.md`
- `docs/contributing/adding-tools.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 2: Tool Integration"
  batch: "Batch 2.4: Generic YAML-Based Adapter"
  notes:
    - "Read tool definition entirely from YAML configuration"
    - "No code changes needed to add new tools"
    - "Demonstrate adding a hypothetical tool (e.g., 'gemini-cli')"
    - "Document process for community contributions"
```

**Acceptance Criteria:**
- Adapter reads all configuration from YAML
- New tool added via YAML without code changes
- Tests demonstrate adding a mock tool
- Documentation explains tool contribution process
- Example YAML for fictional tool provided

---

## Batch 3: Cost Optimization (CREATE WEEK 2-3)

**Priority:** MEDIUM  
**Timeline:** Create Week 2 (as Tasks 1-5 progress)  
**Estimated Creation Time:** 1 hour

### Task 9: Telemetry Infrastructure ❌

**Filename:** `2026-02-04T1708-backend-dev-telemetry-infrastructure.yaml`  
**Agent:** backend-dev  
**Effort:** 2-3 days  
**Priority:** medium  
**Dependencies:** Task 4

**Artefacts:**
- `src/llm_service/telemetry/logger.py` (or `logger.js`)
- `src/llm_service/telemetry/database.py` (SQLite schema)
- `src/llm_service/telemetry/migrations/001_initial.sql`
- `tests/test_telemetry.py`
- `docs/telemetry-privacy.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 3: Cost Optimization & Telemetry"
  batch: "Batch 3.1: Telemetry Infrastructure"
  notes:
    - "SQLite database for invocation logs"
    - "Schema: invocation_id, agent, tool, model, tokens, cost, latency, timestamp"
    - "Privacy controls: metadata-only mode (no prompts/responses)"
    - "Database initialization and migration support"
    - "Optional full logging mode (opt-in)"
```

**Acceptance Criteria:**
- SQLite database schema created
- Invocation logging functional with all metrics
- Privacy mode excludes sensitive data
- Database migrations work forward/backward
- Unit tests cover logging scenarios

**Blocks:** Tasks 10-11 (policy engine, stats reporting)

---

### Task 10: Policy Engine ✅

**Filename:** `2026-02-04T1709-backend-dev-policy-engine.yaml` ✅  
**Status:** CREATED (already in inbox)  
**Note:** Dependencies need update to reflect Task 9 requirement

---

### Task 11: Stats & Reporting ❌

**Filename:** `2026-02-04T1710-backend-dev-stats-reporting.yaml`  
**Agent:** backend-dev  
**Effort:** 2 days  
**Priority:** medium  
**Dependencies:** Task 10

**Artefacts:**
- `src/llm_service/commands/stats.py` (CLI stats command)
- `src/llm_service/reporting/cost_report.py`
- `src/llm_service/reporting/exporters.py` (CSV/JSON export)
- `tests/test_stats.py`
- `docs/cost-analysis.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 3: Cost Optimization & Telemetry"
  batch: "Batch 3.3: Stats & Reporting"
  notes:
    - "llm-service stats command implementation"
    - "Reports: daily/monthly cost summaries"
    - "Breakdowns: per-agent, per-model, per-tool"
    - "CSV/JSON export for external analysis"
    - "Visualization-friendly output format"
```

**Acceptance Criteria:**
- Stats command shows daily/monthly summaries
- Per-agent and per-model breakdowns accurate
- CSV/JSON export functional
- Reports match telemetry data
- Integration tests with sample data

---

## Batch 4: Integration & Distribution (CREATE WEEK 3-4)

**Priority:** LOW-MEDIUM  
**Timeline:** Create Week 3 (as Milestones 1-3 near completion)  
**Estimated Creation Time:** 2 hours

### Task 12: Acceptance Tests ❌

**Filename:** `2026-02-04T1711-backend-dev-acceptance-tests.yaml`  
**Agent:** backend-dev  
**Effort:** 2-3 days  
**Priority:** high  
**Dependencies:** Tasks 1-11 (all core implementation)

**Artefacts:**
- `tests/acceptance/test_scenarios.py` (or `.js`)
- `tests/acceptance/features/*.feature` (Gherkin scenarios)
- `tests/acceptance/steps/*.py` (step definitions)
- `docs/testing/acceptance-tests.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 4: End-to-End Integration & Testing"
  batch: "Batch 4.1: Integration Testing"
  notes:
    - "Implement 8 acceptance tests from prestudy"
    - "Gherkin scenarios: routing, fallback, budget limits, tool invocation"
    - "End-to-end workflows: config → routing → execution → telemetry"
    - "Cross-platform matrix: Linux, macOS, WSL2"
    - "Use mocked tool CLIs for testing"
```

**Acceptance Criteria:**
- All 8 Gherkin scenarios passing
- End-to-end workflows tested
- Cross-platform validation (3 OSes)
- Error scenarios and fallback tested
- Test coverage report >80%

**Blocks:** Documentation, packaging, distribution (Tasks 13-17)

---

### Task 13: CI Integration ❌

**Filename:** `2026-02-04T1712-framework-guardian-ci-integration.yaml`  
**Agent:** framework-guardian  
**Effort:** 2-3 days  
**Priority:** medium  
**Dependencies:** Task 12

**Artefacts:**
- `.github/workflows/llm-service-tests.yml`
- `.github/workflows/llm-service-cross-platform.yml`
- `tests/ci/matrix-config.json`
- `docs/ci-integration.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 4: End-to-End Integration & Testing"
  batch: "Batch 4.1: Integration Testing"
  notes:
    - "GitHub Actions workflow for automated testing"
    - "Cross-platform matrix: ubuntu-latest, macos-latest, windows-latest"
    - "Run acceptance tests, unit tests, linting"
    - "Automated test execution on PR and main branch"
```

**Acceptance Criteria:**
- GitHub Actions workflow runs on all 3 platforms
- All tests pass in CI environment
- Workflow triggers on PR and merge
- Test results reported clearly
- CI badge added to README

---

### Task 14: User Guide ❌

**Filename:** `2026-02-04T1713-writer-editor-user-guide.yaml`  
**Agent:** writer-editor  
**Effort:** 2 days  
**Priority:** medium  
**Dependencies:** Task 12

**Artefacts:**
- `docs/user-guide.md`
- `docs/quickstart.md`
- `docs/configuration-reference.md`
- `docs/troubleshooting.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 4: End-to-End Integration & Testing"
  batch: "Batch 4.2: Documentation & Examples"
  notes:
    - "User guide with installation and quickstart"
    - "Configuration reference explaining all options"
    - "Example workflows for 3 personas: AI Power User, Software Engineer, Process Architect"
    - "Troubleshooting guide for common issues"
```

**Acceptance Criteria:**
- User guide covers installation through advanced usage
- Configuration reference documents all YAML options
- Persona workflows demonstrate real use cases
- Troubleshooting addresses common error messages
- Non-technical person can follow quickstart

---

### Task 15: Persona Workflows ✅

**Filename:** `2026-02-04T1714-scribe-persona-workflows.yaml` ✅  
**Status:** CREATED (already in inbox)  
**Note:** Dependencies need update to reflect Task 14 requirement

---

### Task 16: Packaging ❌

**Filename:** `2026-02-04T1715-build-automation-packaging.yaml`  
**Agent:** build-automation  
**Effort:** 1-2 days  
**Priority:** medium  
**Dependencies:** Task 14

**Artefacts:**
- `packaging/pyinstaller.spec` (or `pkg` config for Node.js)
- `packaging/build.sh`
- `dist/llm-service-linux-x64` (binary)
- `dist/llm-service-macos-x64` (binary)
- `dist/llm-service-win-x64.exe` (binary)
- `docs/distribution.md`

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 4: End-to-End Integration & Testing"
  batch: "Batch 4.3: Distribution & Packaging"
  notes:
    - "PyInstaller (Python) or pkg (Node.js) for standalone executables"
    - "Build for Linux, macOS, Windows/WSL2"
    - "Bundle all dependencies in single binary"
    - "Testing: binary works without Python/Node runtime"
```

**Acceptance Criteria:**
- Standalone executables built for all 3 platforms
- Binaries work without runtime dependencies
- File size reasonable (<50MB per binary)
- Help command functional in packaged version
- Build script documented

**Blocks:** Task 17 (installation scripts)

---

### Task 17: Installation Scripts ❌

**Filename:** `2026-02-04T1716-build-automation-installation-scripts.yaml`  
**Agent:** build-automation  
**Effort:** 1-2 days  
**Priority:** medium  
**Dependencies:** Task 16

**Artefacts:**
- `install.sh` (Linux/macOS)
- `install.ps1` (Windows/WSL2)
- `docs/installation.md`
- `CHANGELOG.md`
- `README.md` (updated with installation instructions)

**Context:**
```yaml
context:
  project: "LLM Service Layer"
  milestone: "Milestone 4: End-to-End Integration & Testing"
  batch: "Batch 4.3: Distribution & Packaging"
  notes:
    - "Installation script for Linux/macOS using curl/wget"
    - "PowerShell script for Windows/WSL2"
    - "Detect platform and download correct binary"
    - "Add to PATH and create config directory"
    - "GitHub Release preparation"
```

**Acceptance Criteria:**
- Installation scripts work on all 3 platforms
- Scripts download correct binary for platform
- Binary added to PATH automatically
- Config directory created in correct location
- GitHub Release artifacts prepared

---

## Creation Timeline

### Day 1 (2026-02-04): Foundation Tasks ⚡
- [ ] Task 1: Config Schema (30 min)
- [ ] Task 2: Config Loader (30 min)
- [ ] Task 3: CLI Foundation (30 min)
- [ ] Task 4: Routing Engine (30 min)
- **Total:** 2 hours

### Week 1 (Feb 4-11): Tool Integration Tasks
- [ ] Task 5: Adapter Base (20 min)
- [ ] Task 7: Codex Adapter (20 min)
- [ ] Task 8: Generic Adapter (20 min)
- **Total:** 1 hour

### Week 2 (Feb 11-18): Cost Optimization Tasks
- [ ] Task 9: Telemetry (20 min)
- [ ] Task 11: Stats Reporting (20 min)
- **Total:** 40 minutes

### Week 3 (Feb 18-25): Integration & Distribution Tasks
- [ ] Task 12: Acceptance Tests (30 min)
- [ ] Task 13: CI Integration (20 min)
- [ ] Task 14: User Guide (20 min)
- [ ] Task 16: Packaging (20 min)
- [ ] Task 17: Installation Scripts (20 min)
- **Total:** 1 hour 50 minutes

---

## Dependency Validation

### Task 1 (Config Schema)
- **Prerequisites:** None ✅
- **Blocks:** Tasks 2-17 (all remaining tasks)

### Task 2 (Config Loader)
- **Prerequisites:** Task 1 ✅
- **Blocks:** Tasks 3-17 (12 tasks)

### Task 3 (CLI Foundation)
- **Prerequisites:** Task 2 ✅
- **Blocks:** User interaction, end-to-end tests

### Task 4 (Routing Engine)
- **Prerequisites:** Task 2 ✅
- **Blocks:** Tasks 5-11, tool execution

### Task 5 (Adapter Base)
- **Prerequisites:** Task 2 ✅
- **Blocks:** Tasks 6-8 (all adapters)

### Tasks 6-8 (Adapters)
- **Prerequisites:** Task 5 ✅
- **Can execute in parallel:** Yes ✅

### Task 9 (Telemetry)
- **Prerequisites:** Task 4 ✅
- **Blocks:** Tasks 10-11

### Task 10 (Policy Engine)
- **Prerequisites:** Task 9 ✅
- **Blocks:** Task 11

### Task 11 (Stats Reporting)
- **Prerequisites:** Task 10 ✅
- **Blocks:** None (optional for MVP)

### Task 12 (Acceptance Tests)
- **Prerequisites:** Tasks 1-11 (all core implementation) ✅
- **Blocks:** Tasks 13-17 (validation gate)

### Tasks 13-17 (CI, Docs, Distribution)
- **Prerequisites:** Task 12 ✅
- **Can execute in parallel:** Mostly (13-14-15 parallel, 16→17 sequential)

---

## Success Criteria

**Task Creation Complete When:**
- [ ] All 14 YAML files created in `work/collaboration/inbox/`
- [ ] All files pass schema validation (`validate-task-schema.py`)
- [ ] Dependencies correctly specified in each task
- [ ] Priority levels assigned appropriately
- [ ] Estimated efforts documented
- [ ] Artefacts lists are complete
- [ ] Acceptance criteria are testable

**Quality Checks:**
- [ ] No circular dependencies
- [ ] Critical path identified correctly
- [ ] Parallel opportunities noted
- [ ] Agent assignments balanced
- [ ] Tech stack decision documented as context

---

## Next Actions

1. **Review** this checklist with stakeholders
2. **Decide** tech stack (Python vs. Node.js) - BLOCKS creation details
3. **Create** Batch 1 tasks (Tasks 1-4) - highest priority
4. **Validate** created tasks with schema validator
5. **Assign** Task 1 to backend-dev for immediate execution
6. **Update** roadmap status after task creation

---

**Prepared By:** Planning Petra  
**Date:** 2026-02-04  
**Status:** ✅ Ready for task creation  
**Estimated Total Creation Time:** 6-7 hours (spread across 3-4 weeks)
