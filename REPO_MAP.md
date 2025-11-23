# Repository Map

_Version: 2.0.0_  
_Generated: 2025-11-23T22:36:42Z_  
_Agent: Bootstrap Bill_  
_Task: 2025-11-23T2157-bootstrap-bill-repomap-update_

## Overview

**Repository:** `sddevelopment-be/quickstart_agent-augmented-development`  
**Purpose:** AI-augmented workflow starter with file-based multi-agent orchestration  
**Primary Language:** Markdown (documentation), Python (orchestration)  
**Architecture:** Layered directive system with specialized agents and async task coordination

## Repository Statistics

| Metric | Count |
|--------|-------|
| Total Files | 289 |
| Markdown Files | 154 |
| Python Files | 7 |
| YAML Files | 59 |
| Lines of Python | ~2,501 |
| Lines of Markdown | ~32,021 |
| Total Disk Usage | ~2.6 MB |

## Directory Structure

### Root Level

```
.
├── .github/              # GitHub configuration and agent framework [404K]
├── .gitignore            # Git exclusions
├── AGENTS.md             # Agent Specification Document (ASD) - core governance [8.4K]
├── LICENSE               # Repository license
├── README.md             # Repository overview and quickstart [2.8K]
├── agents -> .github/agents  # Symlink to agent definitions
├── docs/                 # Documentation root [908K]
├── opencode-config.json  # OpenCode portability configuration [6.3K]
├── ops/                  # Operations and automation scripts [68K]
├── requirements.txt      # Python dependencies [335 bytes]
├── using_agents.png      # Visual guide for GitHub agent panel [92K]
├── validation/           # Repository validation scripts [8K]
└── work/                 # Multi-agent orchestration workspace [1.2M]
```

### `.github/` - GitHub & Agent Framework (404K)

Core platform configuration and agentic instruction system.

```
.github/
├── ISSUE_TEMPLATE/       # GitHub issue templates
├── agents/               # Agent framework - CORE INSTRUCTION LAYER
│   ├── QUICKSTART.md     # Getting started with agents
│   ├── aliases.md        # Command shortcuts and operational aliases
│   ├── approaches/       # Agent methodology patterns
│   │   ├── README.md
│   │   └── file-based-orchestration.md  # Orchestration strategy
│   ├── directives/       # Externalized instruction modules
│   │   ├── 001_cli_shell_tooling.md
│   │   ├── 002_context_notes.md
│   │   ├── 003_repository_quick_reference.md
│   │   ├── 004_documentation_context_files.md
│   │   ├── 005_agent_profiles.md
│   │   ├── 006_version_governance.md
│   │   ├── 007_agent_declaration.md
│   │   ├── 008_artifact_templates.md
│   │   ├── 009_role_capabilities.md
│   │   ├── 010_mode_protocol.md
│   │   ├── 011_risk_escalation.md
│   │   ├── 012_operating_procedures.md
│   │   ├── 013_tooling_setup.md
│   │   ├── 014_worklog_creation.md
│   │   ├── 015_store_prompts.md
│   │   └── manifest.json
│   └── guidelines/       # Core behavioral guidelines
│       ├── bootstrap.md
│       ├── general_guidelines.md
│       ├── operational_guidelines.md
│       └── rehydrate.md
├── copilot/              # GitHub Copilot CLI tooling setup
│   └── setup.sh          # Pre-installs rg, fd, ast-grep, jq, yq, fzf [7.5K]
├── labels.yml            # GitHub label definitions
├── prompts/              # Prompt templates for agent interactions
├── semantic.yml          # Semantic versioning configuration
└── workflows/            # GitHub Actions CI/CD
    ├── copilot-setup.yml         # Copilot tooling installation workflow
    ├── diagram-rendering.yml     # PlantUML diagram generation
    ├── orchestration.yml         # Automated agent orchestration
    ├── reusable-config-mapping.yml
    ├── update_readme.yml
    └── validation.yml            # Task/schema validation
```

#### Agent Framework Components

**Core Governance:**
- `AGENTS.md` (root): Agent Specification Document - initialization protocol
- `.github/agents/guidelines/`: Operational & general behavior rules
- `.github/agents/directives/`: 15 externalized instruction modules (001-015)

**Agent Patterns:**
- `.github/agents/approaches/`: Strategic methodologies (file-based orchestration)

**Tooling:**
- `.github/copilot/setup.sh`: Installs CLI tools (rg, fd, ast-grep, jq, yq, fzf)

### `docs/` - Documentation Root (908K)

Centralized knowledge base for vision, architecture, guides, and templates.

```
docs/
├── CHANGELOG.md          # Version history
├── VISION.md             # Project vision and long-term goals
├── specific_guidelines.md # Project-specific operational rules
├── HOW_TO_USE/           # User guides and tutorials
│   ├── ISSUE_TEMPLATES_GUIDE.md
│   ├── QUICKSTART.md
│   ├── ci-orchestration.md           # CI/CD integration patterns
│   ├── copilot-tooling-setup.md      # Copilot CLI setup guide
│   ├── creating-agents.md            # Agent development guide
│   ├── multi-agent-orchestration.md  # Orchestration system guide
│   └── testing-orchestration.md      # Testing strategies
├── architecture/         # Technical architecture documentation
│   ├── adrs/             # Architecture Decision Records
│   │   ├── ADR-001-modular-agent-directive-system.md
│   │   ├── ADR-002-portability-enhancement-opencode.md
│   │   ├── ADR-003-task-lifecycle-state-management.md
│   │   ├── ADR-004-work-directory-structure.md
│   │   ├── ADR-005-coordinator-agent-pattern.md
│   │   ├── ADR-006-adopt-three-layer-governance-model.md
│   │   ├── ADR-007-repository-restructuring-layer-separation.md
│   │   ├── ADR-008-file-based-async-coordination.md
│   │   ├── ADR-009-orchestration-metrics-standard.md
│   │   ├── README.md
│   │   └── _historical/  # Superseded ADRs
│   ├── assessments/      # Technical assessments
│   ├── design/           # Design documents
│   ├── diagrams/         # PlantUML and other diagrams
│   ├── patterns/         # Reusable design patterns
│   ├── recommendations/  # Architecture recommendations
│   └── synthesis/        # Cross-cutting analysis
│       └── poc3-orchestration-metrics-synthesis.md
├── audience/             # Audience-specific documentation
├── planning/             # Project planning artifacts
├── styleguides/          # Writing and coding style guides
└── templates/            # Document and artifact templates
    ├── LEX/              # Lexical templates
    ├── agent-tasks/      # Task YAML templates
    │   ├── task-base.yaml
    │   ├── task-context.yaml
    │   ├── task-descriptor.yaml
    │   ├── task-error.yaml
    │   ├── task-examples.yaml
    │   ├── task-result.yaml
    │   ├── task-templates-README.md
    │   └── task-timestamps.yaml
    ├── architecture/     # Architecture document templates
    ├── automation/       # Automation script templates
    ├── project/          # Project management templates
    └── structure/        # Directory structure templates
```

#### Key Documentation Additions (Recent)

**HOW_TO_USE Guides:**
- `multi-agent-orchestration.md`: Complete orchestration system guide
- `creating-agents.md`: Agent development lifecycle
- `copilot-tooling-setup.md`: CLI tooling setup instructions
- `ci-orchestration.md`: CI/CD integration patterns
- `testing-orchestration.md`: Testing strategies

**Architecture Decision Records:**
- `ADR-009-orchestration-metrics-standard.md`: Metrics and observability standard

**Synthesis:**
- `poc3-orchestration-metrics-synthesis.md`: POC3 metrics analysis

**Templates:**
- `docs/templates/agent-tasks/`: Complete task YAML schema templates (8 files)

### `work/` - Multi-Agent Orchestration Workspace (1.2M)

File-based asynchronous task coordination system.

```
work/
├── README.md             # Work directory overview and usage guide
├── inbox/                # New tasks awaiting assignment
├── assigned/             # Agent-specific task queues
│   ├── architect/
│   ├── backend-dev/
│   ├── bootstrap-bill/   # This agent's queue
│   ├── build-automation/
│   ├── coordinator/
│   ├── curator/
│   ├── diagrammer/
│   ├── frontend/
│   ├── lexical/
│   ├── manager/
│   ├── planning/
│   ├── project-planner/
│   ├── researcher/
│   ├── scribe/
│   ├── structural/
│   ├── synthesizer/
│   ├── test-agent/
│   ├── translator/
│   └── writer-editor/
├── done/                 # Completed tasks
│   └── build-automation/
├── archive/              # Long-term task storage (by month)
├── logs/                 # Agent execution work logs
│   ├── architect/
│   ├── build-automation/
│   ├── curator/
│   ├── diagrammer/
│   ├── generic/
│   ├── lexical/
│   ├── manager/
│   ├── prompts/
│   └── synthesizer/
├── collaboration/        # Cross-agent coordination artifacts
│   ├── AGENT_STATUS.md
│   ├── HANDOFFS.md
│   ├── WORKFLOW_LOG.md
│   ├── orchestration-implementation-plan.md
│   └── orchestration-architecture-summary.md
├── notes/                # Informal planning notes
├── planning/             # Structured planning artifacts
├── schemas/              # Task YAML JSON schemas (placeholder)
├── scripts/              # Orchestration automation
│   ├── agent_base.py             # Base agent interface [~300 LOC]
│   ├── agent_orchestrator.py    # Task routing and lifecycle [~800 LOC]
│   ├── example_agent.py          # Reference implementation [~200 LOC]
│   ├── fixtures/                 # Test fixtures
│   ├── init-work-structure.sh   # Directory structure init
│   ├── test_orchestration_e2e.py # E2E test suite [~400 LOC]
│   ├── validate-task-naming.sh
│   ├── validate-task-schema.py   # YAML schema validator [~350 LOC]
│   └── validate-work-structure.sh
└── synthesizer/          # Synthesizer agent working space
```

#### Orchestration Framework (work/scripts/)

**Core Components:**
- `agent_orchestrator.py`: Assigns tasks, monitors lifecycle, creates handoffs
- `agent_base.py`: Abstract base class for agent implementations
- `example_agent.py`: Reference agent demonstrating patterns

**Validation:**
- `validate-task-schema.py`: Enforces task YAML schema
- `validate-task-naming.sh`: Validates naming conventions
- `validate-work-structure.sh`: Ensures directory integrity

**Testing:**
- `test_orchestration_e2e.py`: End-to-end orchestration tests

**Setup:**
- `init-work-structure.sh`: Creates work directory structure

### `ops/` - Operations & Automation (68K)

Operational tooling and validation.

```
ops/
├── scripts/              # Utility scripts
│   ├── convert-agents-to-opencode.py  # OpenCode conversion [~450 LOC]
│   └── opencode-spec-validator.py     # Spec validation [~280 LOC]
└── test-data/            # Test fixtures and sample data
```

### `validation/` - Repository Validation (8K)

Scripts ensuring repository integrity and consistency.

```
validation/
└── validate_repo.sh      # Repository structure validation
```

## Key Files

### Root Level

| File | Purpose | Size |
|------|---------|------|
| `AGENTS.md` | Agent Specification Document - core initialization protocol | 8.4K |
| `README.md` | Repository overview and quickstart guide | 2.8K |
| `requirements.txt` | Python dependencies (PyYAML, pytest, jsonschema) | 335B |
| `opencode-config.json` | OpenCode portability configuration | 6.3K |
| `LICENSE` | Repository license | 1K |
| `.gitignore` | Git exclusions | 266B |

### Agent Framework

| File | Purpose |
|------|---------|
| `.github/agents/QUICKSTART.md` | Agent framework quickstart |
| `.github/agents/guidelines/general_guidelines.md` | General behavioral principles |
| `.github/agents/guidelines/operational_guidelines.md` | Operational discipline |
| `.github/agents/guidelines/bootstrap.md` | Initialization protocol |
| `.github/agents/guidelines/rehydrate.md` | State recovery protocol |
| `.github/agents/directives/001_cli_shell_tooling.md` | CLI tool usage (rg, fd, ast-grep) |
| `.github/agents/directives/014_worklog_creation.md` | Work log standards |
| `.github/agents/approaches/file-based-orchestration.md` | Orchestration strategy |

### Documentation

| File | Purpose |
|------|---------|
| `docs/VISION.md` | Project vision and goals |
| `docs/specific_guidelines.md` | Project-specific rules |
| `docs/HOW_TO_USE/multi-agent-orchestration.md` | Orchestration system guide |
| `docs/HOW_TO_USE/creating-agents.md` | Agent development guide |
| `docs/architecture/adrs/ADR-009-orchestration-metrics-standard.md` | Metrics standard |
| `work/README.md` | Work directory usage guide |

### Orchestration

| File | Purpose | LOC |
|------|---------|-----|
| `work/scripts/agent_orchestrator.py` | Task routing & lifecycle mgmt | ~800 |
| `work/scripts/agent_base.py` | Base agent interface | ~300 |
| `work/scripts/example_agent.py` | Reference implementation | ~200 |
| `work/scripts/validate-task-schema.py` | YAML schema validator | ~350 |
| `work/scripts/test_orchestration_e2e.py` | E2E test suite | ~400 |

## Agent Profiles

The repository supports multiple specialized agents coordinated via file-based orchestration:

| Agent | Queue Location | Purpose |
|-------|---------------|---------|
| architect | work/assigned/architect/ | Architecture design and documentation |
| backend-dev | work/assigned/backend-dev/ | Backend implementation |
| bootstrap-bill | work/assigned/bootstrap-bill/ | Repository mapping and scaffolding |
| build-automation | work/assigned/build-automation/ | CI/CD and automation |
| coordinator | work/assigned/coordinator/ | Meta-orchestration |
| curator | work/assigned/curator/ | Content curation |
| diagrammer | work/assigned/diagrammer/ | Diagram generation |
| frontend | work/assigned/frontend/ | Frontend implementation |
| lexical | work/assigned/lexical/ | Language and terminology |
| manager | work/assigned/manager/ | Project management |
| planning | work/assigned/planning/ | Planning and strategy |
| project-planner | work/assigned/project-planner/ | Project planning |
| researcher | work/assigned/researcher/ | Research and analysis |
| scribe | work/assigned/scribe/ | Documentation writing |
| structural | work/assigned/structural/ | Structural refactoring |
| synthesizer | work/assigned/synthesizer/ | Cross-cutting synthesis |
| test-agent | work/assigned/test-agent/ | Testing |
| translator | work/assigned/translator/ | Translation |
| writer-editor | work/assigned/writer-editor/ | Content editing |

## Workflows and CI/CD

### GitHub Actions Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| `copilot-setup.yml` | Install CLI tooling (rg, fd, ast-grep, jq, yq, fzf) | On demand |
| `orchestration.yml` | Automated agent orchestration | Cron / manual |
| `validation.yml` | Validate task schemas and structure | Push / PR |
| `diagram-rendering.yml` | Generate PNG from PlantUML | Push with .puml changes |
| `update_readme.yml` | README updates | Push to main |

### Task Lifecycle Workflow

```
┌─────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────┐     ┌─────────┐
│ inbox/  │ ──> │ assigned/    │ ──> │ in_progress │ ──> │ done/│ ──> │ archive/│
│  (new)  │     │ <agent>/     │     │             │     │      │     │         │
└─────────┘     └──────────────┘     └─────────────┘     └──────┘     └─────────┘
                                             │
                                             │
                                             v
                                         ┌───────┐
                                         │ error │
                                         └───────┘
```

**See also:** `docs/architecture/diagrams/task-lifecycle-state-machine.puml`

## Dependencies

### Python

From `requirements.txt`:

```python
PyYAML>=6.0        # YAML parsing (orchestration, validation)
pytest>=7.0        # Testing framework
jsonschema>=4.0    # JSON schema validation (optional)
```

### External Tools

Installed via `.github/copilot/setup.sh`:

| Tool | Version | Purpose |
|------|---------|---------|
| `rg` (ripgrep) | latest | Fast text search |
| `fd` | latest | Fast file finding |
| `ast-grep` | latest | AST-based code search |
| `jq` | latest | JSON processing |
| `yq` | latest | YAML processing |
| `fzf` | latest | Fuzzy finder |

### GitHub Actions

- Standard GitHub Actions runtime
- PlantUML for diagram rendering

## Configuration Files

| File | Purpose | Format |
|------|---------|--------|
| `opencode-config.json` | OpenCode portability spec | JSON |
| `.github/labels.yml` | GitHub label definitions | YAML |
| `.github/semantic.yml` | Semantic versioning config | YAML |
| `.gitignore` | Git exclusions | Text |
| `requirements.txt` | Python dependencies | Text |

## Architectural Principles

1. **Layered Governance**: Three-layer agent instruction system (AGENTS.md → guidelines → directives)
2. **File-Based Coordination**: All orchestration state visible in Git
3. **Async Task Processing**: Agents poll queues, no central server required
4. **Transparent State**: Every transition recorded in YAML + Git history
5. **Composable Workflows**: Complex flows emerge from simple handoffs
6. **Specialization**: Agents focused on narrow domains for high fidelity
7. **Portability**: OpenCode integration for multi-platform agent support

## Recent Major Additions

### Orchestration Framework (Nov 2025)
- `work/scripts/agent_orchestrator.py`: Task routing system
- `work/scripts/agent_base.py`: Agent interface abstraction
- `work/scripts/example_agent.py`: Reference implementation
- Task validation and E2E testing
- Work directory structure with 18+ agent queues

### Copilot Tooling (Nov 2025)
- `.github/copilot/setup.sh`: CLI tool installer
- `.github/workflows/copilot-setup.yml`: Automated setup workflow

### Documentation (Nov 2025)
- HOW_TO_USE guides (7 files)
- ADR-009: Orchestration metrics standard
- Task YAML templates (8 files)
- Synthesis documents

### CI/CD (Nov 2025)
- Orchestration workflow
- Enhanced validation workflow
- Diagram rendering automation

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11 | Initial repository structure |
| 2.0.0 | 2025-11-23 | Orchestration framework, Copilot tooling, expanded documentation |

## Related Artifacts

- **SURFACES.md**: Public interfaces and entry points
- **WORKFLOWS.md**: Detailed workflow patterns
- **DEPENDENCIES.md**: Complete dependency inventory

---

_Generated by Bootstrap Bill (Task: 2025-11-23T2157-bootstrap-bill-repomap-update)_  
_For updates, assign new task to `bootstrap-bill` agent_  
_Machine-readable: YAML-compatible structure, grep-friendly formatting_
