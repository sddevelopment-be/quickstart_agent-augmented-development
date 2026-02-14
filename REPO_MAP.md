# Repository Map

_Version: 3.0.0_  
_Last Updated: 2026-02-13_  
_Agent: Bootstrap Bill_  
_Purpose: Comprehensive structural overview and navigation guide_

---

## Overview

**Repository:** `sddevelopment-be/quickstart_agent-augmented-development`  
**Purpose:** AI-augmented development quickstart with doctrine-driven agent framework  
**Status:** Production-ready template for agent-augmented workflows  
**License:** MIT

This repository serves as both a **working example** and a **reusable template** for teams adopting AI-augmented development practices, built on the **Doctrine Stack**—a five-layer governance framework that ensures predictable, inspectable, and repeatable agent behavior.

### Quick Stats

| Metric | Value |
|--------|-------|
| **Framework Version** | 1.1.0 |
| **Doctrine Version** | 1.0.0 |
| **Agent Profiles** | 21 specialized agents |
| **Directives** | 34 operational instructions |
| **Tactics** | 50 procedural guides |
| **Test Suite** | 665 passing tests (88.7%) |
| **Code Quality** | 670+ issues fixed (Sprint 1) |
| **Coverage Integration** | ✅ SonarCloud enabled |

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Navigation by Persona](#navigation-by-persona)
4. [Core Framework Components](#core-framework-components)
5. [Key Documentation](#key-documentation)
6. [Development Workflows](#development-workflows)
7. [Quick Reference](#quick-reference)

---

## Architecture Overview

### The Doctrine Stack

Five-layer governance system with clear precedence:

```
┌─────────────────────────────────────────────┐
│ Guidelines (values, preferences)            │ ← Highest precedence
├─────────────────────────────────────────────┤
│ Approaches (mental models, philosophies)    │
├─────────────────────────────────────────────┤
│ Directives (instructions, constraints)      │ ← Select tactics
├─────────────────────────────────────────────┤
│ Tactics (procedural execution guides)       │ ← Execute work
├─────────────────────────────────────────────┤
│ Templates (output structure contracts)      │ ← Lowest precedence
└─────────────────────────────────────────────┘
```

**Key Insight:** Directives select tactics; tactics execute work procedurally. Human retains approval authority ("Human in Charge").

**See:** [`doctrine/DOCTRINE_STACK.md`](doctrine/DOCTRINE_STACK.md) for complete framework explanation.

### Repository Structure Philosophy

This repository follows a **four-directory separation** for clear boundaries:

```
repository-root/
├── src/          # Production code (runtime, importable)
├── tools/        # Development utilities (exporters, validators, scripts)
├── tests/        # All test code (unit, integration, e2e)
└── fixtures/     # Test fixtures and example data
```

**Plus:**
- `doctrine/` - Portable agentic framework (distributable via git subtree)
- `docs/` - Project intent, architecture, and guides
- `work/` - Multi-agent coordination workspace
- `specifications/` - Functional requirements (optional but recommended)

---

## Directory Structure

### Root Level

```
.
├── AGENTS.md                 # Agent Specification Document (ASD) - initialization protocol
├── README.md                 # Project overview and quickstart
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT license
├── REPO_MAP.md              # This file - structural overview
├── SURFACES.md              # API surfaces and integration points
├── VISION.md                # Project vision and strategic goals
│
├── doctrine/                # Portable agentic framework (201 files, 0 dependencies)
├── docs/                    # Documentation root (architecture, guides, templates)
├── work/                    # Multi-agent orchestration workspace
├── specifications/          # Functional specifications (recommended)
│
├── src/                     # Production code
├── framework/               # Legacy framework (to be consolidated)
├── tools/                   # Development utilities
├── tests/                   # Test suite
├── fixtures/                # Test fixtures
│
├── config/                  # Configuration files
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependencies
├── package.json             # Node.js dependencies (validation)
└── sonar-project.properties # SonarCloud configuration
```

### `doctrine/` - Agentic Framework (Portable)

**Purpose:** Standalone, zero-dependency framework for agent governance. Distributable via git subtree.

```
doctrine/
├── DOCTRINE_STACK.md        # Framework conceptual reference
├── GLOSSARY.md              # Standardized terminology (350+ terms)
├── CHANGELOG.md             # Doctrine version history
│
├── agents/                  # 21 specialized agent profiles
│   ├── analyst-annie.agent.md
│   ├── architect.agent.md
│   ├── backend-dev.agent.md
│   ├── bootstrap-bill.agent.md      # ← This agent
│   ├── build-automation.agent.md
│   ├── code-reviewer-cindy.agent.md
│   ├── curator.agent.md
│   ├── diagrammer.agent.md
│   ├── framework-guardian.agent.md
│   ├── frontend.agent.md
│   ├── java-jenny.agent.md
│   ├── lexical.agent.md
│   ├── manager.agent.md
│   ├── project-planner.agent.md
│   ├── python-pedro.agent.md
│   ├── researcher.agent.md
│   ├── reviewer.agent.md
│   ├── scribe.agent.md
│   ├── synthesizer.agent.md
│   ├── translator.agent.md
│   └── writer-editor.agent.md
│
├── directives/              # 34 operational instructions (load on-demand)
│   ├── 001_cli_shell_tooling.md
│   ├── 002_context_notes.md
│   ├── 003_repository_quick_reference.md
│   ├── 004_documentation_context_files.md
│   ├── 005_agent_profiles.md
│   ├── 006_version_governance.md
│   ├── 007_agent_declaration.md
│   ├── ... (34 total)
│   └── manifest.json
│
├── tactics/                 # 50 procedural execution guides
│   ├── README.md            # Tactics index and discovery guide
│   ├── stopping-conditions.tactic.md
│   ├── premortem-risk-identification.tactic.md
│   ├── adversarial-testing.tactic.md
│   ├── AMMERSE-quality-assessment.tactic.md
│   ├── safe-to-fail-experiment-design.tactic.md
│   ├── ATDD_adversarial-acceptance.tactic.md
│   ├── ... (50 total)
│   └── template.tactic.md
│
├── approaches/              # Mental models and philosophies
│   ├── trunk-based-development.md
│   ├── decision-first-development.md
│   ├── locality-of-change.md
│   └── file-based-orchestration.md
│
├── guidelines/              # Core behavioral guidelines (highest precedence)
│   ├── general_guidelines.md      # Broad operational principles
│   ├── operational_guidelines.md  # Tone, honesty, reasoning discipline
│   ├── bootstrap.md               # Initialization protocol
│   └── rehydrate.md               # State recovery protocol
│
├── templates/               # Output structure contracts
│   ├── architecture/        # ADRs, design docs
│   ├── automation/          # Scripts, workflows
│   ├── project/             # Project management
│   └── tactic.md            # Tactic document template
│
├── shorthands/              # Command aliases and shortcuts
└── examples/                # Example usage and patterns
```

**Key Files:**
- **DOCTRINE_STACK.md**: Framework conceptual model (5 layers, precedence rules)
- **GLOSSARY.md**: 350+ standardized terms for consistent communication
- **tactics/README.md**: Complete tactics catalog with applicability matrix
- **agents/**: 21 specialist profiles with clear boundaries and collaboration rules

**Configuration:** `.doctrine-config/config.yaml` (created by Bootstrap Bill during setup)

### `docs/` - Documentation Root

**Purpose:** Project-specific documentation, architecture decisions, and guides.

```
docs/
├── VISION.md                # Project vision and strategic goals
├── SURFACES.md              # API surfaces and integration points
├── WORKFLOWS.md             # Detailed workflow patterns
├── README.md                # Documentation navigation
├── DEPENDENCIES.md          # Dependency inventory
│
├── architecture/            # Technical architecture
│   ├── adrs/                # Architecture Decision Records
│   │   ├── README.md        # ADR index
│   │   ├── ADR-001-modular-agent-directive-system.md
│   │   ├── ADR-012-atdd-tdd-workflow.md
│   │   ├── ADR-017-traceable-decisions.md
│   │   ├── ADR-045-doctrine-concept-domain-model.md
│   │   └── ... (45+ ADRs)
│   ├── design/              # Design documents
│   │   ├── DOCTRINE_MAP.md  # Doctrine framework navigation
│   │   ├── async_orchestration_technical_design.md
│   │   ├── dashboard-interface-technical-design.md
│   │   └── directive_system_architecture.md
│   ├── diagrams/            # PlantUML C4 diagrams
│   └── patterns/            # Reusable design patterns
│
├── audience/                # Audience-specific documentation
│   ├── automation_agent.md  # Agent responsibilities and guidelines
│   └── developer.md         # Developer onboarding
│
├── guides/                  # How-to guides and tutorials
│   ├── multi-agent-orchestration.md
│   ├── creating-agents.md
│   ├── ci-orchestration.md
│   ├── copilot-tooling-setup.md
│   └── testing-orchestration.md
│
├── quickstart/              # Quick start guides
│   └── QUICKSTART.md
│
├── templates/               # Document templates
│   ├── architecture/        # ADR template
│   ├── agent-tasks/         # Task YAML templates (8 files)
│   ├── automation/          # Script templates
│   └── specifications/      # Feature spec template
│
├── styleguides/             # Writing and coding style guides
├── planning/                # Project planning artifacts
├── workflows/               # Workflow documentation
└── reports/                 # Generated reports and summaries
```

**Key Files:**
- **architecture/adrs/**: 45+ Architecture Decision Records tracking major decisions
- **architecture/design/DOCTRINE_MAP.md**: Complete doctrine framework navigation
- **guides/multi-agent-orchestration.md**: File-based orchestration deep dive
- **templates/agent-tasks/**: Complete task YAML schema templates

### `work/` - Multi-Agent Coordination

**Purpose:** File-based asynchronous task coordination. All orchestration state visible in Git.

```
work/
├── README.md                # Work directory usage guide
│
├── inbox/                   # New tasks awaiting assignment
├── assigned/                # Agent-specific task queues (21 agents)
│   ├── architect/
│   ├── backend-dev/
│   ├── bootstrap-bill/      # ← This agent's queue
│   ├── curator/
│   ├── synthesizer/
│   └── ... (21 total)
├── done/                    # Completed tasks
└── archive/                 # Long-term storage (by month)
│
├── collaboration/           # Cross-agent coordination artifacts
│   ├── AGENT_STATUS.md      # Real-time agent status dashboard
│   ├── HANDOFFS.md          # Handoff log
│   ├── WORKFLOW_LOG.md      # Event timeline
│   └── inbox/               # Collaboration task inbox
│
├── reports/                 # Work reports and summaries
│   ├── SPRINT1_EXECUTIVE_SUMMARY.md
│   ├── logs/                # Agent execution work logs (Directive 014)
│   │   ├── architect/
│   │   ├── manager-mike/
│   │   ├── prompts/         # Prompt documentation (Directive 015)
│   │   └── ... (per agent)
│   ├── analysis/            # Analysis reports
│   ├── synthesis/           # Cross-cutting synthesis
│   ├── validation/          # Validation reports
│   └── exec_summaries/      # Executive summaries
│
├── notes/                   # Informal planning and ideation
│   ├── ideation/            # Early-stage exploration
│   └── tmp/                 # Temporary workspace
│
├── planning/                # Structured planning artifacts
├── schemas/                 # Task YAML schemas (placeholder)
└── scripts/                 # Orchestration automation
    ├── agent_orchestrator.py         # Task routing engine (~800 LOC)
    ├── agent_base.py                 # Agent interface (~300 LOC)
    ├── example_agent.py              # Reference implementation (~200 LOC)
    ├── validate-task-schema.py       # Schema validator (~350 LOC)
    ├── validate-task-naming.sh       # Naming convention checker
    └── test_orchestration_e2e.py     # E2E test suite (~400 LOC)
```

**Workflow Pattern:**
```
inbox/ (new) → assigned/<agent>/ (assigned) → (in_progress) → done/ (done) → archive/
                                                        ↓
                                                    (error) → requires intervention
```

**Key Artifacts:**
- **collaboration/AGENT_STATUS.md**: Real-time dashboard of all agents
- **collaboration/HANDOFFS.md**: Complete handoff audit trail
- **reports/SPRINT1_EXECUTIVE_SUMMARY.md**: Sprint 1 completion report (670 fixes)

### `src/` - Production Code

**Purpose:** Production runtime code. Importable by production systems.

```
src/
├── README.md                # Production code guidelines
│
├── framework/               # Core framework runtime
│   ├── core/                # Task, Agent, Orchestrator abstractions
│   ├── execution/           # Task execution engine
│   ├── interface/           # Client interfaces (CLI, API)
│   ├── orchestration/       # Runtime agent dispatch & task routing
│   ├── context/             # Context assembly & directive loading
│   ├── config/              # Model routing configuration
│   └── schemas/             # Production JSON schemas
│
├── domain/                  # Domain models (ADR-045)
│   ├── models/              # Immutable dataclasses
│   │   ├── agent_model.py
│   │   ├── directive_model.py
│   │   ├── adr_model.py
│   │   ├── milestone_model.py
│   │   ├── guideline_model.py
│   │   └── primer_model.py
│   ├── parsers/             # YAML/Markdown parsers
│   │   ├── agent_parser.py
│   │   ├── directive_parser.py
│   │   ├── adr_parser.py
│   │   └── guideline_parser.py
│   └── validators/          # Cross-reference validators
│       ├── agent_validator.py
│       ├── directive_validator.py
│       └── adr_validator.py
│
├── llm_service/             # LLM dashboard service
│   ├── cli.py
│   ├── dashboard/           # Web dashboard
│   └── file_watcher.py
│
└── common/                  # Shared utilities
```

**Key Components:**
- **framework/orchestration/**: Runtime agent dispatch and task routing
- **framework/context/**: Context assembly and directive loading
- **domain/**: Type-safe doctrine models and validators (ADR-045, 92% test coverage)
- **llm_service/**: Live dashboard with WebSocket updates

### `tools/` - Development Utilities

**Purpose:** Development-time tooling. Not imported by production.

```
tools/
├── README.md                # Tooling overview
├── QUICKSTART.md            # Quick start for tools
│
├── exporters/               # Agent profile exporters
│   ├── copilot/             # GitHub Copilot format
│   ├── claude/              # Claude Desktop format
│   └── opencode/            # OpenCode format
│
├── validators/              # CI validation scripts
│   ├── structure/           # Repository structure validation
│   ├── schema/              # JSON/YAML schema validation
│   └── naming/              # Naming convention checks
│
├── scripts/                 # Utility scripts
│   ├── generate-error-summary.py    # Error reporting (agent-friendly)
│   ├── generate-error-summary.sh    # Shell wrapper
│   └── planning/            # Planning automation
│
├── dashboards/              # Development dashboards
│   └── dashboard_app.py     # Live task dashboard
│
├── release/                 # Release automation
└── model_router/            # LLM model routing
```

**Key Tools:**
- **exporters/**: Convert agent profiles to Copilot/Claude/OpenCode formats
- **validators/**: CI validation suite for structure, schemas, naming
- **scripts/generate-error-summary.py**: Agent-friendly error reporting (ADR-028)

### `tests/` - Test Suite

**Purpose:** All test code (unit, integration, e2e).

```
tests/
├── conftest.py              # Test configuration
│
├── framework/               # Framework unit tests
├── orchestration/           # Orchestration tests
├── integration/             # Integration test suites
├── unit/                    # Unit tests
│   ├── dashboard/
│   └── domain/              # Domain model tests (195 tests, 92% coverage)
├── dashboards/              # Dashboard tests
└── maintenance/             # Maintenance tests
```

**Current Status:**
- **Passing:** 665 tests (88.7%)
- **Skipped:** 85 tests
- **Known Issue:** Framework module naming conflict (see TESTING_STATUS.md)

---

## Navigation by Persona

### 🆕 New Contributors

**Start here:**
1. [`README.md`](README.md) - Repository overview
2. [`VISION.md`](VISION.md) - Project vision
3. [`AGENTS.md`](AGENTS.md) - Agent framework introduction
4. [`doctrine/DOCTRINE_STACK.md`](doctrine/DOCTRINE_STACK.md) - Governance framework
5. [`docs/guides/creating-agents.md`](docs/guides/creating-agents.md) - Agent development

**Your workflow:**
1. Read AGENTS.md → Load bootstrap protocol
2. Review doctrine/guidelines/ → Understand core principles
3. Browse doctrine/agents/ → See specialist profiles
4. Try work/ orchestration → Submit a task YAML
5. Create your first agent → Use agent_base.py

### 🏗️ Architects & Decision-Makers

**Start here:**
1. [`VISION.md`](VISION.md) - Strategic goals
2. [`docs/architecture/adrs/README.md`](docs/architecture/adrs/README.md) - Decision history
3. [`docs/architecture/design/DOCTRINE_MAP.md`](docs/architecture/design/DOCTRINE_MAP.md) - Framework navigation
4. [`work/reports/SPRINT1_EXECUTIVE_SUMMARY.md`](work/reports/SPRINT1_EXECUTIVE_SUMMARY.md) - Recent progress
5. [`CHANGELOG.md`](CHANGELOG.md) - Version history

**Your priorities:**
- Review ADRs for major architectural decisions
- Understand doctrine stack precedence model
- Evaluate multi-agent orchestration patterns
- Assess code quality improvements (Sprint 1: 670 fixes)
- Consider specifications/ directory for complex features

### 🤖 Agent Developers

**Start here:**
1. [`AGENTS.md`](AGENTS.md) - Agent Specification Document
2. [`doctrine/agents/`](doctrine/agents/) - 21 specialist profiles
3. [`doctrine/directives/`](doctrine/directives/) - 34 operational instructions
4. [`doctrine/tactics/README.md`](doctrine/tactics/README.md) - 50 procedural guides
5. [`work/scripts/agent_base.py`](work/scripts/agent_base.py) - Agent interface

**Your workflow:**
1. Read your agent profile in `doctrine/agents/`
2. Load required directives via `/require-directive NNN`
3. Poll `work/assigned/<agent-name>/` for tasks
4. Update task status (`assigned` → `in_progress` → `done`)
5. Create work log in `work/reports/logs/<agent>/` (Directive 014)
6. Optional: Create handoff in `result.next_agent` block

**Key Directives:**
- **007**: Agent Declaration (authority affirmation)
- **014**: Work Log Creation (documentation standards)
- **016**: Acceptance Test-Driven Development
- **017**: Test-Driven Development
- **018**: Traceable Decisions (ADR protocol)
- **036**: Boy Scout Rule (mandatory pre-task cleanup)

### 💻 Framework Users & Implementers

**Start here:**
1. [`SURFACES.md`](SURFACES.md) - API surfaces
2. [`docs/guides/multi-agent-orchestration.md`](docs/guides/multi-agent-orchestration.md) - Orchestration guide
3. [`work/scripts/`](work/scripts/) - Orchestration implementation
4. [`src/framework/`](src/framework/) - Runtime code
5. [`tools/exporters/`](tools/exporters/) - Agent profile exporters

**Your integration points:**
- Task submission: `work/inbox/*.yaml`
- Task validation: `work/scripts/validate-task-schema.py`
- Orchestrator: `work/scripts/agent_orchestrator.py`
- Error reporting: `tools/scripts/generate-error-summary.py`
- Exporters: Copilot/Claude/OpenCode formats

### 📝 Documentation Writers

**Start here:**
1. [`docs/templates/`](docs/templates/) - Document templates
2. [`docs/styleguides/`](docs/styleguides/) - Writing style guides
3. [`doctrine/templates/`](doctrine/templates/) - Artifact templates
4. [`doctrine/directives/004_documentation_context_files.md`](doctrine/directives/004_documentation_context_files.md) - Documentation standards
5. [`doctrine/directives/018_traceable_decisions.md`](doctrine/directives/018_traceable_decisions.md) - Documentation levels

**Your templates:**
- **ADR**: `docs/templates/architecture/adr-template.md`
- **Feature Spec**: `docs/templates/specifications/feature-spec-template.md`
- **Task YAML**: `docs/templates/agent-tasks/task-descriptor.yaml`
- **Tactic**: `doctrine/templates/tactic.md`

### 🧪 QA & Test Engineers

**Start here:**
1. [`TESTING_STATUS.md`](TESTING_STATUS.md) - Test suite status
2. [`tests/`](tests/) - Test suite (665 passing tests)
3. [`doctrine/directives/016_atdd.md`](doctrine/directives/016_atdd.md) - Acceptance TDD
4. [`doctrine/directives/017_tdd.md`](doctrine/directives/017_tdd.md) - Test-Driven Development
5. [`doctrine/directives/028_bugfixing_techniques.md`](doctrine/directives/028_bugfixing_techniques.md) - Bug fixing workflow

**Your focus:**
- Run tests: `python3 -m pytest` (see TESTING_STATUS.md for ignores)
- Coverage: `python3 -m pytest --cov=src --cov-report=html`
- E2E orchestration: `work/scripts/test_orchestration_e2e.py`
- Domain model tests: `tests/unit/domain/` (195 tests, 92% coverage)
- Known issue: Framework module naming conflict (85 skipped tests)

### 🔧 DevOps & CI/CD Engineers

**Start here:**
1. [`SONARCLOUD_FIXES.md`](SONARCLOUD_FIXES.md) - Code quality status
2. [`.github/workflows/`](.github/workflows/) - CI/CD workflows
3. [`sonar-project.properties`](sonar-project.properties) - SonarCloud config
4. [`tools/scripts/generate-error-summary.py`](tools/scripts/generate-error-summary.py) - Error reporting
5. [`work/reports/SPRINT1_EXECUTIVE_SUMMARY.md`](work/reports/SPRINT1_EXECUTIVE_SUMMARY.md) - Sprint 1 results

**Your workflows:**
- **validation-enhanced.yml**: Code quality, tests, schemas, coverage
- **orchestration.yml**: Automated agent task processing
- **copilot-setup.yml**: CLI tooling installation (rg, fd, ast-grep, jq, yq, fzf)
- **diagram-rendering.yml**: PlantUML to PNG conversion

**Recent Sprint 1 Wins:**
- ✅ Coverage integration for SonarCloud
- ✅ 670 code quality fixes (Black + Ruff)
- ✅ Critical security fix (B108 tempfile)
- ✅ 711/711 unit tests passing
- ✅ Health score: 62 → 70 (+8 points)

---

## Core Framework Components

### Doctrine Framework

**Location:** `doctrine/`  
**Distribution:** Git subtree (standalone, zero dependencies)  
**Version:** 1.0.0

**Components:**

| Component | Count | Purpose |
|-----------|-------|---------|
| **Agent Profiles** | 21 | Specialized agent personas with clear boundaries |
| **Directives** | 34 | Modular operational instructions (load on-demand) |
| **Tactics** | 50 | Procedural execution guides (directive-invoked) |
| **Approaches** | 4+ | Mental models and philosophies |
| **Guidelines** | 4 | Core behavioral principles (highest precedence) |
| **Templates** | 20+ | Output structure contracts |

**Key Doctrine Files:**
- **DOCTRINE_STACK.md**: Five-layer governance framework
- **GLOSSARY.md**: 350+ standardized terms
- **tactics/README.md**: Complete tactics catalog with applicability matrix
- **agents/bootstrap-bill.agent.md**: This agent's profile

### Multi-Agent Orchestration

**Location:** `work/`  
**Philosophy:** File-based asynchronous coordination (ADR-008)

**Core Scripts:**

| Script | LOC | Purpose |
|--------|-----|---------|
| `agent_orchestrator.py` | ~800 | Task routing, lifecycle management, handoff creation |
| `agent_base.py` | ~300 | Abstract base class for agent implementations |
| `example_agent.py` | ~200 | Reference implementation demonstrating patterns |
| `validate-task-schema.py` | ~350 | YAML schema validation (required fields, timestamps) |
| `test_orchestration_e2e.py` | ~400 | End-to-end orchestration test suite |

**Task Lifecycle:**

```
inbox/ (new) → assigned/<agent>/ (assigned) → (in_progress) → done/ (done) → archive/
                                                        ↓
                                                    (error) → requires human intervention
```

### Domain Models (ADR-045)

**Location:** `src/domain/`  
**Coverage:** 92% (195 tests)  
**Status:** Production-ready

**Immutable Models:**

| Model | Purpose | Validation |
|-------|---------|------------|
| `AgentModel` | Agent profile data | Specialization, modes, collaboration rules |
| `DirectiveModel` | Directive metadata | Applicability rules, cross-references |
| `ADRModel` | Architecture decision | Status tracking, consequences |
| `MilestoneModel` | Project milestone | Completion tracking |
| `GuidelineModel` | Guideline data | Priority levels, examples |
| `PrimerModel` | Execution primer | Mode-specific templates |

---

## Development Workflows

### Agent Workflow (File-Based Orchestration)

**Key Steps:**
1. Task creation in `work/inbox/<timestamp>-<agent>-<slug>.yaml`
2. Orchestrator assignment to `work/assigned/<agent>/`
3. Agent polls queue (every 30 seconds)
4. Agent updates task status (`assigned` → `in_progress` → `done`)
5. Agent creates artifacts (code, docs, etc.)
6. Agent creates work log in `work/reports/logs/<agent>/` (Directive 014)
7. Optional: Agent creates handoff in `result.next_agent` block
8. Task moves to `work/done/`

**See:** [`docs/guides/multi-agent-orchestration.md`](docs/guides/multi-agent-orchestration.md)

### Test-First Development (Directives 016, 017, 028)

**ATDD Workflow (Directive 016):**
1. Write acceptance test from specification
2. Run test (should fail)
3. Implement feature incrementally
4. Run test (should pass)
5. Document decision if architectural change (ADR)

**TDD Workflow (Directive 017):**
1. Write unit test for smallest behavior
2. Run test (should fail)
3. Write minimal code to pass
4. Run test (should pass)
5. Refactor, keeping tests green

---

## Quick Reference

### Essential Commands

```bash
# Initialize work directory
bash work/scripts/init-work-structure.sh

# Validate task YAML
python work/scripts/validate-task-schema.py work/inbox/task.yaml

# Run orchestrator
python work/scripts/agent_orchestrator.py

# Run tests
python3 -m pytest  # See TESTING_STATUS.md for current ignores

# Run tests with coverage
python3 -m pytest --cov=src --cov-report=html

# Generate error summary (agent-friendly)
python tools/scripts/generate-error-summary.py

# Validate repository structure
bash validation/validate_repo.sh

# Export agents to Copilot format
python tools/exporters/copilot/export_to_copilot.py

# Install CLI tooling (rg, fd, ast-grep, jq, yq, fzf)
bash .github/copilot/setup.sh
```

### Key Files & Locations

| Need | Location |
|------|----------|
| **Agent initialization** | `AGENTS.md` |
| **Doctrine framework** | `doctrine/DOCTRINE_STACK.md` |
| **Agent profiles** | `doctrine/agents/*.agent.md` |
| **Directives** | `doctrine/directives/NNN_*.md` |
| **Tactics** | `doctrine/tactics/*.tactic.md` |
| **Task templates** | `docs/templates/agent-tasks/*.yaml` |
| **ADR template** | `docs/templates/architecture/adr-template.md` |
| **Work logs** | `work/reports/logs/<agent>/` |
| **Collaboration** | `work/collaboration/AGENT_STATUS.md` |
| **Test status** | `TESTING_STATUS.md` |
| **Sprint 1 summary** | `work/reports/SPRINT1_EXECUTIVE_SUMMARY.md` |

---

## Related Artifacts

- **[SURFACES.md](SURFACES.md)**: API surfaces and integration points
- **[VISION.md](VISION.md)**: Project vision and strategic goals
- **[docs/WORKFLOWS.md](docs/WORKFLOWS.md)**: Detailed workflow patterns
- **[DEPENDENCIES.md](DEPENDENCIES.md)**: Complete dependency inventory
- **[TESTING_STATUS.md](TESTING_STATUS.md)**: Test suite status and known issues
- **[SONARCLOUD_FIXES.md](SONARCLOUD_FIXES.md)**: Code quality status
- **[CHANGELOG.md](CHANGELOG.md)**: Version history

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11 | Initial repository structure |
| 2.0.0 | 2025-11-23 | Orchestration framework, Copilot tooling |
| 3.0.0 | 2026-02-13 | Comprehensive rebuild: doctrine integration, domain models, Sprint 1 completion |

---

_Generated by Bootstrap Bill_  
_For updates: Assign task to `bootstrap-bill` agent in `work/inbox/`_  
_Last Updated: 2026-02-13_
