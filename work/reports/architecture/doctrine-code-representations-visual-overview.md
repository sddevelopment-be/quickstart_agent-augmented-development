# Domain Layer Architecture - Visual Overview

**Date:** 2026-02-11  
**Related:** `architectural-analysis-doctrine-code-representations.md`

---

## Layer Dependency Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                          │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  Dashboard      │  │  CLI Tools   │  │  Scripts       │ │
│  │  (FastAPI/      │  │  (kitty.py)  │  │  (run_*.py)    │ │
│  │   Streamlit)    │  │              │  │                │ │
│  └─────────────────┘  └──────────────┘  └────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │ uses
┌───────────────────────────▼─────────────────────────────────┐
│  FRAMEWORK LAYER                                            │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  Orchestration  │  │  Config      │  │  Context       │ │
│  │  (agent_base,   │  │  (loaders)   │  │  (tracking)    │ │
│  │   orchestrator) │  │              │  │                │ │
│  └─────────────────┘  └──────────────┘  └────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │ uses
┌───────────────────────────▼─────────────────────────────────┐
│  DOMAIN LAYER (NEW)                                         │
│  ┌──────────────────────┐  ┌────────────────────────────┐  │
│  │  Collaboration       │  │  Doctrine                  │  │
│  │  ┌────────────────┐  │  │  ┌──────────────────────┐ │  │
│  │  │ AgentProfile   │  │  │  │ Directive            │ │  │
│  │  │ Task           │  │  │  │ Tactic               │ │  │
│  │  │ Batch          │  │  │  │ Approach             │ │  │
│  │  │ Iteration      │  │  │  │ StyleGuide           │ │  │
│  │  │ Cycle          │  │  │  │ Template             │ │  │
│  │  └────────────────┘  │  │  └──────────────────────┘ │  │
│  └──────────────────────┘  └────────────────────────────┘  │
│  ┌──────────────────────┐  ┌────────────────────────────┐  │
│  │  Specifications      │  │  Common                    │  │
│  │  ┌────────────────┐  │  │  ┌──────────────────────┐ │  │
│  │  │ Specification  │  │  │  │ TaskStatus (enum)    │ │  │
│  │  │ Feature        │  │  │  │ FeatureStatus (enum) │ │  │
│  │  │ Initiative     │  │  │  │ TaskMode (enum)      │ │  │
│  │  └────────────────┘  │  │  │ Exceptions           │ │  │
│  └──────────────────────┘  │  └──────────────────────┘ │  │
│                             └────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │ reads from (immutable)
┌───────────────────────────▼─────────────────────────────────┐
│  CONFIGURATION LAYER (FILES)                                │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  doctrine/      │  │  .doctrine-  │  │  work/         │ │
│  │  - agents/      │  │   config/    │  │  - tasks/      │ │
│  │  - directives/  │  │  (overrides) │  │  - specs/      │ │
│  │  - tactics/     │  │              │  │                │ │
│  │  - approaches/  │  │              │  │                │ │
│  │  - templates/   │  │              │  │                │ │
│  └─────────────────┘  └──────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Domain Module Structure

```
src/domain/
│
├── collaboration/           # Agent coordination & task orchestration
│   ├── __init__.py
│   ├── agent.py             # AgentProfile domain object
│   │   └── load_agent_profiles() -> list[AgentProfile]
│   ├── task.py              # Task domain object (enhanced from task_schema)
│   │   ├── Task dataclass
│   │   ├── read_task() -> Task
│   │   └── write_task(task: Task)
│   ├── batch.py             # Batch orchestration concept
│   │   ├── Batch dataclass
│   │   └── calculate_progress()
│   ├── iteration.py         # Iteration planning cycle
│   │   ├── Iteration dataclass
│   │   └── IterationPhase dataclass
│   └── cycle.py             # Recurring process cycles
│       └── Cycle dataclass
│
├── doctrine/                # Doctrine framework artifacts
│   ├── __init__.py
│   ├── directive.py         # Directive domain object
│   │   ├── Directive dataclass
│   │   ├── load_directives() -> list[Directive]
│   │   └── is_required_for_agent(agent_id) -> bool
│   ├── tactic.py            # Tactic + TacticStep
│   │   ├── Tactic dataclass
│   │   ├── TacticStep dataclass
│   │   └── load_tactics() -> list[Tactic]
│   ├── approach.py          # Strategic approaches
│   │   ├── Approach dataclass
│   │   └── load_approaches() -> list[Approach]
│   ├── style_guide.py       # StyleGuide + StyleRule
│   │   ├── StyleGuide dataclass
│   │   ├── StyleRule dataclass
│   │   └── load_style_guides() -> list[StyleGuide]
│   ├── template.py          # Template + TemplateSection
│   │   ├── Template dataclass
│   │   ├── TemplateSection dataclass
│   │   └── load_templates() -> list[Template]
│   └── loaders/             # YAML/Markdown parsers (Phase 3)
│       ├── directive_loader.py
│       ├── tactic_loader.py
│       └── ...
│
├── specifications/          # Specification & feature tracking
│   ├── __init__.py
│   ├── specification.py     # Specification domain object
│   │   ├── Specification dataclass
│   │   └── load_specifications() -> list[Specification]
│   ├── feature.py           # Feature tracking
│   │   └── Feature dataclass
│   └── initiative.py        # Initiative (if formalized)
│       └── Initiative dataclass
│
└── common/                  # Truly shared utilities
    ├── __init__.py
    ├── types.py             # Enums: TaskStatus, FeatureStatus, etc.
    │   ├── TaskStatus (enum)
    │   ├── FeatureStatus (enum)
    │   ├── TaskMode (enum)
    │   ├── TaskPriority (enum)
    │   └── AgentIdentity (Literal)
    └── exceptions.py        # Shared exception types
        ├── DomainError
        ├── ValidationError
        └── LoaderError
```

---

## Adapter Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  src/domain/                                                │
│  (Domain Objects)                                           │
│  - AgentProfile                                             │
│  - Directive                                                │
│  - Tactic                                                   │
└───────────────────┬─────────────────────────────────────────┘
                    │ consumed by
┌───────────────────▼─────────────────────────────────────────┐
│  src/adapters/                                              │
│  (Transform domain → vendor formats)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  base.py: AbstractAdapter                            │  │
│  │  - export_agent(AgentProfile) -> dict               │  │
│  │  - export_directive(Directive) -> dict              │  │
│  │  - validate_export(config) -> list[str]             │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐   │
│  │  OpenCode    │  │  Cursor    │  │  Cody            │   │
│  │  Adapter     │  │  Adapter   │  │  Adapter         │   │
│  └──────────────┘  └────────────┘  └──────────────────┘   │
└───────────────────┬─────────────────────────────────────────┘
                    │ generates
┌───────────────────▼─────────────────────────────────────────┐
│  Vendor Tool Configs                                        │
│  - .opencode/agents.json                                    │
│  - .cursor/config.json                                      │
│  - .sourcegraph/cody.yaml                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Loading Doctrine Configs

```
┌─────────────────────────────────────────────────────────────┐
│  1. Configuration Files                                     │
│     doctrine/agents/backend-benny.agent.md                  │
│     .doctrine-config/agents/backend-benny.agent.md (override)│
└───────────────────┬─────────────────────────────────────────┘
                    │ parsed by
┌───────────────────▼─────────────────────────────────────────┐
│  2. Loader Functions                                        │
│     src/domain/collaboration/agent.py                       │
│     - load_agent_profiles()                                 │
│       1. Parse global: doctrine/agents/*.md                 │
│       2. Parse local: .doctrine-config/agents/*.md          │
│       3. Merge (local overrides win)                        │
│       4. Validate                                           │
└───────────────────┬─────────────────────────────────────────┘
                    │ returns
┌───────────────────▼─────────────────────────────────────────┐
│  3. Domain Objects (Immutable)                              │
│     AgentProfile(                                           │
│       agent_id="backend-benny",                             │
│       display_name="Backend Benny",                         │
│       specialization="Python/FastAPI",                      │
│       default_mode=TaskMode.PROGRAMMING,                    │
│       required_directives=["001", "014", "017"],            │
│       ...                                                   │
│     )                                                       │
└───────────────────┬─────────────────────────────────────────┘
                    │ used by
┌───────────────────▼─────────────────────────────────────────┐
│  4. Application Layer                                       │
│     - Dashboard: Display agent profiles                     │
│     - CLI: `kitty show agents`                              │
│     - Framework: Assign tasks to agents                     │
│     - Adapters: Export to vendor tools                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Migration Path: src/common/ → src/domain/

### Before (Current State)

```
src/
├── common/
│   ├── agent_loader.py      # Loads agents from YAML
│   ├── task_schema.py        # Task I/O (read_task, write_task)
│   └── types.py              # Enums (TaskStatus, AgentIdentity, etc.)
├── framework/
│   └── orchestration/
│       ├── agent_base.py     # Imports from src.common
│       └── orchestrator.py   # Imports from src.common
└── llm_service/
    └── dashboard/
        └── task_linker.py    # Imports from src.common
```

### After (Target State)

```
src/
├── domain/                   # NEW
│   ├── collaboration/
│   │   ├── agent.py          # Migrated from agent_loader.py (enhanced)
│   │   └── task.py           # Migrated from task_schema.py (enhanced)
│   ├── doctrine/
│   │   ├── directive.py      # NEW
│   │   ├── tactic.py         # NEW
│   │   └── ...
│   └── common/
│       ├── types.py          # Migrated from src.common.types
│       └── exceptions.py     # NEW
├── framework/
│   └── orchestration/
│       ├── agent_base.py     # Imports from src.domain.collaboration
│       └── orchestrator.py   # Imports from src.domain.collaboration
└── llm_service/
    └── dashboard/
        └── task_linker.py    # Imports from src.domain.collaboration
```

---

## Validation Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. Load Domain Objects                                     │
│     agents = load_agent_profiles()                          │
│     directives = load_directives()                          │
│     tactics = load_tactics()                                │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│  2. Self-Validation (Individual Objects)                    │
│     for agent in agents:                                    │
│         errors = agent.validate()                           │
│         if errors:                                          │
│             raise ValidationError(errors)                   │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│  3. Cross-Reference Validation                              │
│     - Agent's required_directives exist?                    │
│     - Directive's applies_to_agents are valid agent IDs?    │
│     - Tactic's related_directives exist?                    │
│     - Approach's related_tactics exist?                     │
└───────────────────┬─────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│  4. Report Results                                          │
│     $ kitty validate doctrine                               │
│     ✅ Agents: 15 valid                                     │
│     ✅ Directives: 34 valid                                 │
│     ❌ Tactics: 1 error                                     │
│         - tactic 'incremental-commit' references missing    │
│           directive '099'                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## CLI Inspection Commands (Phase 5)

```bash
# Show all agents
$ kitty show agents
Available Agents:
- architect-alphonso: System decomposition, design interfaces, ADRs
- backend-benny: Python/FastAPI implementation, API design
- curator-claire: Content curation, documentation quality
...

# Show agent details
$ kitty show agents --agent=backend-benny
Agent: Backend Benny
Specialization: Python/FastAPI implementation, API design
Default Mode: /programming
Available Modes: /programming, /analysis-mode, /meta-mode

Required Directives:
  001: CLI & Shell Tooling
  014: Work Log Creation
  017: Test-Driven Development

Output Artifacts:
  - Python code
  - FastAPI endpoints
  - Unit tests

# Show all directives
$ kitty show directives
Active Directives:
  001: CLI & Shell Tooling (required)
  002: Context Notes (recommended)
  ...
  034: Spec-Driven Development (optional)

# Check compliance for agent
$ kitty check compliance --agent=backend-benny
Checking compliance for backend-benny...

Required Directives:
  ✅ 001: CLI & Shell Tooling
  ✅ 014: Work Log Creation
  ❌ 017: Test-Driven Development
      Missing tests in last 3 commits

Recommended Directives:
  ⚠️  018: Documentation Level Framework
      No doc-level comments in recent PRs

# Inspect full doctrine stack
$ kitty inspect stack
Doctrine Stack (current project):

Agents:        15 loaded (13 global, 2 local overrides)
Directives:    34 active, 2 deprecated
Tactics:       18 available
Approaches:    7 documented
Style Guides:  4 active
Templates:     8 available

Configuration Sources:
  Global:  doctrine/ (framework)
  Local:   .doctrine-config/ (project overrides)

Last Validated: 2026-02-11 10:30:00 UTC
Status: ✅ All artifacts valid

# Validate doctrine
$ kitty validate doctrine
Validating doctrine stack...
✅ Agents: 15 valid
✅ Directives: 34 valid
✅ Tactics: 18 valid
✅ Approaches: 7 valid
✅ Style Guides: 4 valid
✅ Templates: 8 valid
✅ Cross-references: All valid

# Export to vendor tool
$ kitty export --format=opencode --output=.opencode/
Exporting to OpenCode format...
✅ Wrote .opencode/agents.json (15 agents)
✅ Wrote .opencode/directives.json (34 directives)
✅ Wrote .opencode/config.yaml
```

---

## Success Metrics Visualization

### Before Implementation

```
┌─────────────────────────────────────────────────────────────┐
│  Current State (Baseline)                                   │
├─────────────────────────────────────────────────────────────┤
│  Domain Objects:        0                                   │
│  Type Coverage:         60% ████████                        │
│  Test Coverage:         70% █████████                       │
│  YAML Parsing Code:     Scattered in 5+ files               │
│  CLI Commands:          0                                   │
│  Vendor Adapters:       0                                   │
└─────────────────────────────────────────────────────────────┘
```

### After Implementation

```
┌─────────────────────────────────────────────────────────────┐
│  Target State (After Phase 6)                               │
├─────────────────────────────────────────────────────────────┤
│  Domain Objects:        15+ ████████████████████████        │
│  Type Coverage:         85% ███████████████████             │
│  Test Coverage:         80% ████████████████  (domain: 90%) │
│  YAML Parsing Code:     Centralized in src/domain/loaders/ │
│  CLI Commands:          5+ (show, inspect, check, validate) │
│  Vendor Adapters:       2+ (OpenCode, Cursor)               │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Documents

- **Architectural Analysis:** `architectural-analysis-doctrine-code-representations.md`
- **Next Steps:** `2026-02-11-doctrine-code-representations-next-steps.md`
- **Work Log:** `work/logs/2026-02-11T0604-doctrine-code-representations-implementation.md`
- **ADR-042:** Shared Task Domain Model (pattern reference)
- **ADR-044:** Agent Identity Type Safety (pattern reference)

---

**Generated:** 2026-02-11  
**Architect:** Alphonso  
**Purpose:** Visual companion to architectural analysis
