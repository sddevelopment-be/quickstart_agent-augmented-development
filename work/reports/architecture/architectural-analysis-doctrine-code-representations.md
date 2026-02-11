# Architectural Analysis: Doctrine Code Representations

**Status:** APPROVED ✅  
**Date:** 2026-02-11  
**Architect:** Alphonso  
**Related Documents:**
- Work Log: `work/logs/2026-02-11T0604-doctrine-code-representations-implementation.md`
- Initiative: `specifications/initiatives/terminology-alignment-refactoring.md`
- ADR-042: Shared Task Domain Model
- ADR-044: Agent Identity Type Safety

---

## Executive Summary

This analysis defines **code artifact representations** for doctrine concepts (Agent, Directive, Tactic, Approach, StyleGuide, Template) and operational orchestration concepts (Batch, Iteration, Cycle). The goal is to:

1. **Enable UI inspection** - Support configuration viewing and stack introspection via webapp/CLI
2. **Support vendor tool distribution** - Enable ACL/adapter layer for tool-specific export formats
3. **Improve maintainability** - Create single source of truth for domain concepts with type-safe representations
4. **Clarify domain boundaries** - Refactor `src/common/` → `src/domain/` with domain-specific modules

**Key Decision:** Domain objects represent **doctrine framework concepts**, not repository-specific artifacts (e.g., ADRs). This ensures:
- ✅ Clean dependency direction (doctrine framework ← repository content, not →)
- ✅ Reusable framework artifacts across projects
- ✅ No circular dependencies between framework and doctrine config

**Approval Rationale:** This design aligns with existing patterns (ADR-042 for shared domain models, ADR-044 for type safety) while establishing clean architectural boundaries between:
- **Framework layer** (`src/framework/`) - Runtime orchestration and execution
- **Domain layer** (`src/domain/`) - Conceptual representations of doctrine and collaboration
- **Doctrine configuration** (`doctrine/`, `.doctrine-config/`) - YAML/Markdown content sources

---

## 1. Problem Statement

### 1.1 Current Pain Points

**Problem 1: No Type-Safe Domain Representations**
- Doctrine concepts (Agent, Directive, etc.) exist only as YAML/Markdown files
- No Python representations = no IDE support, no type checking, no programmatic introspection
- Parsing logic scattered across `src/framework/orchestration/` and `src/llm_service/dashboard/`

**Problem 2: UI Inspection Needs Code Artifacts**
- Dashboard (`src/llm_service/dashboard/`) needs to display agent capabilities, directive status, etc.
- CLI tools (`tools/kitty.py`, future CLI) need configuration inspection commands
- No structured way to query "What agents exist? What directives apply? What's the current doctrine stack?"

**Problem 3: Vendor Tool Distribution Requires Adapters**
- Initiative: Export doctrine-compliant configurations to vendor tools (OpenCode, Sourcegraph Cody, Cursor, etc.)
- Each tool has different config formats (JSON, YAML, custom DSLs)
- Need **ACL/adapter layer** to transform doctrine domain objects → tool-specific formats

**Problem 4: Orchestration Concepts Are Implicit**
- Concepts like "Batch" (grouped tasks), "Iteration" (planning cycle), "Cycle" (recurring process) are implicit in scripts
- No explicit domain model = hard to reason about orchestration patterns
- Scripts like `run_dashboard.py`, `tools/cycle_orchestrator.sh` embed orchestration logic without shared vocabulary

**Problem 5: Unclear Domain Boundaries**
- `src/common/` mixes shared utilities with domain-specific concepts (e.g., `types.py` has `TaskStatus`, `AgentIdentity`)
- No clear separation between:
  - **Collaboration domain** (agents, tasks, orchestration)
  - **Doctrine domain** (directives, tactics, approaches)
  - **Specification domain** (features, initiatives, specs)

### 1.2 Connection to Strategic Initiatives

**Initiative: UI Inspection & Configuration Management**
- Dashboard needs to display agent profiles, directive compliance, tactic checklists
- CLI needs `kitty show agents`, `kitty check directives`, `kitty inspect stack` commands
- **Blocker:** No programmatic way to load and query doctrine artifacts

**Initiative: Vendor Tool Distribution**
- Export doctrine-compliant `.agent.md` profiles → OpenCode agent configs
- Transform directive compliance rules → tool-specific linting configs
- **Blocker:** No adapter layer or domain objects to transform

**Initiative: Orchestration Automation**
- Automate batch planning, iteration cycles, task assignment
- Support multi-agent collaboration patterns (handoffs, reviews, synthesis)
- **Blocker:** No explicit model for Batch, Iteration, Cycle concepts

---

## 2. Proposed Domain Model

### 2.1 Design Principles

1. **Framework Doctrine Concepts Only** - Domain objects represent **doctrine framework artifacts** (Agent profiles, Directives), NOT repository-specific content (ADRs, specs)
2. **Dependency Direction** - `doctrine/` → `src/domain/` ← `src/framework/` (domain objects consume doctrine configs, framework orchestrates domain objects)
3. **Immutable by Default** - Use `@dataclass(frozen=True)` for value objects to prevent accidental mutation
4. **Validation at Boundaries** - Parse YAML/Markdown → validate → construct domain object (fail fast on invalid config)
5. **Layered Override Support** - `doctrine/` (global) < `.doctrine-config/` (local overrides) properly compose

### 2.2 Domain Object Definitions

#### 2.2.1 Doctrine Domain (`src/domain/doctrine/`)

##### Agent Profile

```python
@dataclass(frozen=True)
class AgentProfile:
    """
    Represents an agent's identity, capabilities, and operational parameters.
    
    Loaded from: doctrine/agents/*.agent.md or .doctrine-config/agents/*.agent.md
    """
    
    # Identity
    agent_id: str  # e.g., "architect-alphonso"
    display_name: str  # e.g., "Architect Alphonso"
    specialization: str  # e.g., "System decomposition, design interfaces, ADRs"
    
    # Capabilities
    primary_focus: str
    secondary_awareness: list[str]
    avoidances: list[str]
    success_metrics: str
    
    # Operational Modes
    default_mode: TaskMode  # From src/common/types.py
    available_modes: list[TaskMode]
    
    # Context Layers
    required_directives: list[str]  # Directive numbers (e.g., ["001", "007", "018"])
    optional_directives: list[str]
    required_approaches: list[str]  # Approach IDs
    
    # Output Artifacts
    artifact_types: list[str]  # e.g., ["ADR", "PlantUML", "Pattern Doc"]
    
    # Metadata
    source_file: Path
    last_modified: datetime
    
    def validate(self) -> list[str]:
        """Validate agent profile for required fields and consistency."""
        errors = []
        if not self.agent_id or not self.agent_id.islower():
            errors.append("agent_id must be lowercase with hyphens")
        if not self.specialization:
            errors.append("specialization is required")
        # ... additional validation rules
        return errors
```

##### Directive

```python
@dataclass(frozen=True)
class Directive:
    """
    Represents a numbered operational directive with enforcement rules.
    
    Loaded from: doctrine/directives/*.md
    """
    
    # Identity
    number: str  # e.g., "001", "014"
    title: str  # e.g., "CLI & Shell Tooling"
    slug: str  # e.g., "cli_shell_tooling"
    
    # Content
    summary: str  # One-line description
    rationale: str  # Why this directive exists
    enforcement_level: Literal["required", "recommended", "optional"]
    
    # Applicability
    applies_to_agents: list[str] | Literal["*"]  # Agent IDs or "*" for all
    applies_to_tasks: list[str] | None  # Task types or None for all
    
    # Status
    status: Literal["active", "deprecated", "draft"]
    supersedes: list[str] | None  # Previous directive numbers
    
    # Metadata
    source_file: Path
    last_modified: datetime
    
    def is_required_for_agent(self, agent_id: str) -> bool:
        """Check if directive is required for given agent."""
        if self.applies_to_agents == "*":
            return True
        return agent_id in self.applies_to_agents
```

##### Tactic

```python
@dataclass(frozen=True)
class TacticStep:
    """Single step in a tactical procedure."""
    order: int
    description: str
    prerequisites: list[str]
    expected_output: str


@dataclass(frozen=True)
class Tactic:
    """
    Represents a procedural tactic with concrete steps.
    
    Loaded from: doctrine/tactics/*.md
    """
    
    # Identity
    tactic_id: str  # e.g., "incremental-commit"
    title: str
    category: str  # e.g., "git-workflow", "testing", "documentation"
    
    # Content
    summary: str
    context: str  # When to use this tactic
    steps: list[TacticStep]
    anti_patterns: list[str]  # What NOT to do
    
    # Relationships
    related_directives: list[str]  # Directive numbers
    related_approaches: list[str]  # Approach IDs
    
    # Metadata
    source_file: Path
    last_modified: datetime


@dataclass(frozen=True)
class Approach:
    """
    Represents a mental model or strategic approach.
    
    Loaded from: doctrine/approaches/*.md
    """
    
    # Identity
    approach_id: str  # e.g., "test-driven-development"
    title: str
    category: str
    
    # Content
    summary: str
    principles: list[str]
    applicability: str  # When this approach fits
    trade_offs: dict[str, str]  # {"benefit": "...", "cost": "..."}
    
    # Relationships
    related_directives: list[str]
    related_tactics: list[str]
    
    # Metadata
    source_file: Path
    last_modified: datetime
```

##### StyleGuide

```python
@dataclass(frozen=True)
class StyleRule:
    """Single rule in a style guide."""
    rule_id: str
    description: str
    enforcement_tier: Literal["error", "warning", "info"]
    example_good: str | None
    example_bad: str | None


@dataclass(frozen=True)
class StyleGuide:
    """
    Represents coding or documentation style guide rules.
    
    Loaded from: doctrine/guidelines/*.md
    """
    
    # Identity
    guide_id: str  # e.g., "python-style", "markdown-docs"
    title: str
    scope: Literal["code", "documentation", "git", "general"]
    
    # Content
    summary: str
    rules: list[StyleRule]
    
    # Enforcement
    automated_checks: list[str]  # Tool names (e.g., "ruff", "markdownlint")
    
    # Metadata
    source_file: Path
    last_modified: datetime
```

##### Template

```python
@dataclass(frozen=True)
class TemplateSection:
    """Required or optional section in a template."""
    name: str
    required: bool
    description: str
    placeholder: str | None


@dataclass(frozen=True)
class Template:
    """
    Represents a template for structured documents (ADR, work log, etc.).
    
    Loaded from: doctrine/templates/*.md
    """
    
    # Identity
    template_id: str  # e.g., "adr", "work-log", "task"
    title: str
    category: str  # e.g., "architecture", "collaboration", "planning"
    
    # Structure
    sections: list[TemplateSection]
    frontmatter_schema: dict[str, str] | None  # YAML frontmatter fields
    
    # Validation
    required_headings: list[str]
    forbidden_headings: list[str] | None
    
    # Metadata
    source_file: Path
    last_modified: datetime
```

#### 2.2.2 Collaboration Domain (`src/domain/collaboration/`)

##### Batch

```python
@dataclass
class Batch:
    """
    Represents a grouped set of tasks for coordinated execution.
    
    A batch is a planning unit that groups related tasks for:
    - Parallel execution by multiple agents
    - Sequential execution with dependencies
    - Milestone-based delivery
    """
    
    # Identity
    batch_id: str  # e.g., "M4-batch-4.1"
    title: str
    milestone_id: str | None  # Link to milestone (if applicable)
    
    # Planning
    tasks: list[str]  # Task IDs
    priority: TaskPriority  # Overall batch priority
    estimated_effort: timedelta | None
    
    # Execution
    status: Literal["planned", "in_progress", "completed", "blocked"]
    started_at: datetime | None
    completed_at: datetime | None
    
    # Constraints
    max_parallel_tasks: int | None  # Concurrency limit
    dependencies: list[str]  # Other batch IDs that must complete first
    
    def calculate_progress(self, task_registry: 'TaskRegistry') -> float:
        """Calculate batch completion percentage."""
        # ... implementation
```

##### Iteration

```python
@dataclass
class IterationPhase:
    """Single phase within an iteration."""
    phase_id: str  # e.g., "planning", "execution", "review"
    description: str
    duration_days: int
    tasks: list[str]
    status: Literal["pending", "active", "complete"]


@dataclass
class Iteration:
    """
    Represents a planning and execution cycle with defined phases.
    
    An iteration is a time-boxed development cycle with:
    - Planning phase (select tasks, define goals)
    - Execution phase (implement tasks)
    - Review phase (assess outcomes, retrospective)
    """
    
    # Identity
    iteration_id: str  # e.g., "iteration-2"
    title: str
    cycle_id: str | None  # Parent cycle (if part of recurring process)
    
    # Timeline
    start_date: date
    end_date: date
    phases: list[IterationPhase]
    
    # Goals
    objectives: list[str]
    success_criteria: list[str]
    
    # Execution
    status: Literal["planned", "active", "complete", "cancelled"]
    batches: list[str]  # Batch IDs executed in this iteration
    
    # Retrospective
    outcomes: dict[str, str] | None  # Key learnings
    next_iteration_adjustments: list[str] | None
```

##### Cycle

```python
@dataclass
class Cycle:
    """
    Represents a recurring process with defined rhythm and checkpoints.
    
    A cycle is a higher-level construct for repeating patterns:
    - Weekly sprint cycles
    - Monthly release cycles
    - Quarterly planning cycles
    """
    
    # Identity
    cycle_id: str  # e.g., "sprint-cycle", "release-cycle"
    title: str
    description: str
    
    # Rhythm
    frequency: Literal["daily", "weekly", "biweekly", "monthly", "quarterly"]
    duration_days: int
    
    # Process
    phases: list[str]  # Phase names (e.g., ["planning", "execution", "review"])
    checkpoints: list[str]  # Milestone names within cycle
    
    # History
    iterations: list[str]  # Iteration IDs that followed this cycle
    current_iteration: str | None
```

#### 2.2.3 Specifications Domain (`src/domain/specifications/`)

##### Specification (existing, enhance as needed)

```python
@dataclass
class Specification:
    """
    Represents a specification document with requirements and design.
    
    Loaded from: specifications/*.md
    """
    
    # Identity
    spec_id: str  # e.g., "SPEC-DIST-001"
    title: str
    category: str
    
    # Content
    summary: str
    requirements: list[str]
    design_decisions: dict[str, str]
    
    # Status
    status: FeatureStatus  # From src/common/types.py
    
    # Relationships
    related_initiatives: list[str]
    related_tasks: list[str]
    
    # Metadata
    source_file: Path
    last_modified: datetime
```

##### Feature (existing, enhance as needed)

```python
@dataclass
class Feature:
    """Represents a feature implementation."""
    # ... existing implementation from task_schema or feature tracking
```

---

## 3. Module Structure: src/common/ → src/domain/

### 3.1 Current Structure

```
src/
├── common/
│   ├── __init__.py
│   ├── agent_loader.py       # Load agent profiles from YAML
│   ├── task_schema.py         # Task I/O operations (ADR-042)
│   └── types.py               # Enums: TaskStatus, FeatureStatus, TaskMode, TaskPriority, AgentIdentity
├── framework/
│   ├── config/
│   ├── context/
│   ├── orchestration/
│   └── schemas/
└── llm_service/
    └── dashboard/
```

### 3.2 Proposed Structure

```
src/
├── domain/                     # NEW: Domain concepts (business logic)
│   ├── __init__.py
│   ├── collaboration/          # NEW: Agent coordination & task orchestration
│   │   ├── __init__.py
│   │   ├── agent.py            # AgentProfile (from agent_loader.py)
│   │   ├── task.py             # Task domain object (enhance task_schema.py)
│   │   ├── batch.py            # Batch concept
│   │   ├── iteration.py        # Iteration concept
│   │   └── cycle.py            # Cycle concept
│   ├── doctrine/               # NEW: Doctrine framework artifacts
│   │   ├── __init__.py
│   │   ├── directive.py        # Directive
│   │   ├── tactic.py           # Tactic, TacticStep
│   │   ├── approach.py         # Approach
│   │   ├── style_guide.py      # StyleGuide, StyleRule
│   │   └── template.py         # Template, TemplateSection
│   ├── specifications/         # NEW: Specification & feature tracking
│   │   ├── __init__.py
│   │   ├── specification.py    # Specification
│   │   ├── feature.py          # Feature
│   │   └── initiative.py       # Initiative (if formalized)
│   └── common/                 # RETAINED: Truly shared utilities
│       ├── __init__.py
│       ├── types.py            # KEEP: Enums (TaskStatus, FeatureStatus, etc.)
│       └── exceptions.py       # NEW: Shared exception types
├── framework/                  # UNCHANGED: Runtime orchestration
│   ├── config/
│   ├── context/
│   ├── orchestration/
│   └── schemas/
└── llm_service/                # UNCHANGED: Dashboard & API
    └── dashboard/
```

### 3.3 File-by-File Migration Plan

| Current File | New Location | Rationale |
|--------------|--------------|-----------|
| `src/common/agent_loader.py` | → `src/domain/collaboration/loaders/agent_loader.py` | Agent loading is collaboration domain logic |
| `src/common/task_schema.py` | → `src/domain/collaboration/task.py` | Task I/O is collaboration domain, enhance with Task domain object |
| `src/common/types.py` | → `src/domain/common/types.py` | Shared enums stay in common, but under domain/ |
| (new) | → `src/domain/doctrine/directive.py` | New: Directive domain object + loader |
| (new) | → `src/domain/doctrine/tactic.py` | New: Tactic domain object + loader |
| (new) | → `src/domain/doctrine/approach.py` | New: Approach domain object + loader |
| (new) | → `src/domain/doctrine/style_guide.py` | New: StyleGuide domain object + loader |
| (new) | → `src/domain/doctrine/template.py` | New: Template domain object + loader |
| (new) | → `src/domain/collaboration/batch.py` | New: Batch domain object |
| (new) | → `src/domain/collaboration/iteration.py` | New: Iteration domain object |
| (new) | → `src/domain/collaboration/cycle.py` | New: Cycle domain object |
| (new) | → `src/domain/specifications/specification.py` | New: Specification domain object + loader |

### 3.4 Import Path Updates

**Before:**
```python
from src.common.types import TaskStatus, AgentIdentity
from src.common.task_schema import read_task, write_task
from src.common.agent_loader import load_agent_identities
```

**After:**
```python
from src.domain.common.types import TaskStatus, AgentIdentity
from src.domain.collaboration.task import Task, read_task, write_task
from src.domain.collaboration.agent import AgentProfile, load_agent_profiles
from src.domain.doctrine.directive import Directive, load_directives
```

---

## 4. Dependency Direction

### 4.1 Architectural Layers

```
┌─────────────────────────────────────────────────┐
│  Application Layer                              │
│  - src/llm_service/dashboard/                   │
│  - tools/kitty.py                               │
│  - scripts/*.py                                 │
└─────────────────┬───────────────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────────────┐
│  Framework Layer                                │
│  - src/framework/orchestration/                 │
│  - src/framework/config/                        │
│  - src/framework/context/                       │
└─────────────────┬───────────────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────────────┐
│  Domain Layer                                   │
│  - src/domain/collaboration/                    │
│  - src/domain/doctrine/                         │
│  - src/domain/specifications/                   │
│  - src/domain/common/                           │
└─────────────────┬───────────────────────────────┘
                  │ reads from (does NOT modify)
┌─────────────────▼───────────────────────────────┐
│  Configuration Layer                            │
│  - doctrine/ (global framework configs)         │
│  - .doctrine-config/ (local overrides)          │
│  - specifications/ (project specs)              │
│  - work/collaboration/ (runtime task files)     │
└─────────────────────────────────────────────────┘
```

### 4.2 Dependency Rules

**Rule 1: Domain Layer NEVER Depends on Repository-Specific Artifacts**
- ✅ `src/domain/doctrine/directive.py` loads `doctrine/directives/*.md`
- ❌ `src/domain/doctrine/directive.py` does NOT load `docs/architecture/adrs/*.md`
- **Rationale:** ADRs are repository-specific; directives are framework-level

**Rule 2: Framework Layer NEVER Depends on Configuration Content**
- ✅ `src/framework/orchestration/` uses `src/domain/collaboration/agent.py` (domain objects)
- ❌ `src/framework/orchestration/` does NOT import `doctrine/agents/alphonso.md` directly
- **Rationale:** Framework orchestrates domain objects, doesn't parse configs

**Rule 3: Application Layer Orchestrates Domain Objects**
- ✅ `tools/kitty.py` loads `AgentProfile` objects via `src/domain/collaboration/agent.py`
- ✅ Dashboard displays `Directive` objects via `src/domain/doctrine/directive.py`
- **Rationale:** Applications consume domain objects as read-only views

**Rule 4: Doctrine Config NEVER Contains Code**
- ✅ `doctrine/directives/001_cli_shell_tooling.md` is pure Markdown
- ❌ `doctrine/directives/001_cli_shell_tooling.py` would violate separation
- **Rationale:** Configuration is data, not code

### 4.3 Layered Override Strategy

**Loading Sequence:**
1. Load global doctrine config: `doctrine/`
2. Load local overrides: `.doctrine-config/` (if exists)
3. Merge: Local overrides win for conflicts
4. Validate: Ensure merged config is consistent

**Example: Agent Profile Override**
```
# Global: doctrine/agents/backend-benny.agent.md
agent_id: backend-benny
default_mode: /programming

# Local: .doctrine-config/agents/backend-benny.agent.md
agent_id: backend-benny
default_mode: /analysis-mode  # Override for this project

# Merged Result:
AgentProfile(
    agent_id="backend-benny",
    default_mode=TaskMode.ANALYSIS,  # Local override wins
    # ... other fields from global config
)
```

**Implementation:**
```python
def load_agent_profiles() -> list[AgentProfile]:
    """Load agent profiles with local overrides."""
    # Load global profiles
    global_profiles = _load_profiles_from_dir(Path("doctrine/agents"))
    
    # Load local overrides (if exists)
    local_dir = Path(".doctrine-config/agents")
    if local_dir.exists():
        local_profiles = _load_profiles_from_dir(local_dir)
        # Merge: local wins
        global_profiles = _merge_profiles(global_profiles, local_profiles)
    
    return global_profiles
```

---

## 5. ACL/Adapter Strategy

### 5.1 Adapter Pattern

**Goal:** Transform doctrine domain objects → tool-specific config formats

**Architecture:**
```
┌──────────────────────────────────────────────────┐
│  src/domain/                                     │
│  - AgentProfile, Directive, Tactic, etc.         │
└────────────────┬─────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│  src/adapters/                                   │
│  - base.py (AbstractAdapter interface)           │
│  - opencode.py (OpenCodeAdapter)                 │
│  - cursor.py (CursorAdapter)                     │
│  - cody.py (CodyAdapter)                         │
└────────────────┬─────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│  Vendor Tool Configs                             │
│  - .opencode/agents.json                         │
│  - .cursor/config.json                           │
│  - .sourcegraph/cody.yaml                        │
└──────────────────────────────────────────────────┘
```

### 5.2 Adapter Interface

```python
from abc import ABC, abstractmethod
from typing import Any
from src.domain.collaboration.agent import AgentProfile
from src.domain.doctrine.directive import Directive


class AbstractAdapter(ABC):
    """Base adapter interface for vendor tool export."""
    
    @abstractmethod
    def export_agent(self, agent: AgentProfile) -> dict[str, Any]:
        """Transform AgentProfile to tool-specific format."""
        pass
    
    @abstractmethod
    def export_directive(self, directive: Directive) -> dict[str, Any]:
        """Transform Directive to tool-specific format."""
        pass
    
    @abstractmethod
    def validate_export(self, config: dict[str, Any]) -> list[str]:
        """Validate exported config against tool schema."""
        pass


class OpenCodeAdapter(AbstractAdapter):
    """Adapter for OpenCode .opencode/agents.json format."""
    
    def export_agent(self, agent: AgentProfile) -> dict[str, Any]:
        return {
            "name": agent.agent_id,
            "displayName": agent.display_name,
            "description": agent.specialization,
            "capabilities": {
                "focus": agent.primary_focus,
                "artifacts": agent.artifact_types,
            },
            "modes": [mode.value for mode in agent.available_modes],
        }
    
    def export_directive(self, directive: Directive) -> dict[str, Any]:
        return {
            "id": directive.number,
            "title": directive.title,
            "enforcement": directive.enforcement_level,
            "applies_to": directive.applies_to_agents,
        }


class CursorAdapter(AbstractAdapter):
    """Adapter for Cursor .cursorrules format."""
    
    def export_agent(self, agent: AgentProfile) -> dict[str, Any]:
        # Cursor uses .cursorrules (text-based)
        return {
            "role": agent.agent_id,
            "instructions": f"{agent.specialization}\n\nFocus: {agent.primary_focus}",
        }
```

### 5.3 UI Inspection Support

**Dashboard Integration:**
```python
# src/llm_service/dashboard/pages/agents_page.py
from src.domain.collaboration.agent import load_agent_profiles

def render_agents_page():
    agents = load_agent_profiles()
    
    for agent in agents:
        st.subheader(agent.display_name)
        st.write(f"**Specialization:** {agent.specialization}")
        st.write(f"**Default Mode:** {agent.default_mode.value}")
        
        with st.expander("Directives"):
            for directive_num in agent.required_directives:
                directive = load_directive(directive_num)
                st.write(f"- {directive.number}: {directive.title}")
```

**CLI Inspection Commands:**
```bash
# tools/kitty.py show agents
$ kitty show agents
Available Agents:
- architect-alphonso: System decomposition, design interfaces, ADRs
- backend-benny: Python/FastAPI implementation, API design
- curator-claire: Content curation, documentation quality

# tools/kitty.py check directives
$ kitty check directives --agent=backend-benny
Required Directives for backend-benny:
✅ 001: CLI & Shell Tooling
✅ 014: Work Log Creation
❌ 017: Test-Driven Development (missing tests in last 3 commits)

# tools/kitty.py inspect stack
$ kitty inspect stack
Doctrine Stack (current project):
- Agents: 15 loaded (13 global, 2 local overrides)
- Directives: 34 active, 2 deprecated
- Tactics: 18 available
- Approaches: 7 documented
```

---

## 6. Implementation Phases

### Phase 1: Core Domain Objects (Week 1, ~16 hours)

**Goal:** Establish domain layer structure and implement core domain objects

**Tasks:**
1. Create `src/domain/` package structure
2. Move `src/common/types.py` → `src/domain/common/types.py`
3. Implement `src/domain/doctrine/`:
   - `directive.py` (Directive, load_directives)
   - `tactic.py` (Tactic, TacticStep, load_tactics)
   - `approach.py` (Approach, load_approaches)
   - `style_guide.py` (StyleGuide, StyleRule, load_style_guides)
   - `template.py` (Template, TemplateSection, load_templates)
4. Write unit tests for each domain object (pytest)
5. Validate against existing `doctrine/` files

**Deliverables:**
- Domain objects with full type hints
- Pytest suite (>80% coverage)
- Validation logic (fail fast on invalid configs)

**Acceptance Criteria:**
- ✅ All doctrine/*.md files successfully load into domain objects
- ✅ Type checking passes (mypy strict mode)
- ✅ Tests cover validation edge cases

---

### Phase 2: Collaboration Domain (Week 2, ~20 hours)

**Goal:** Implement agent and task domain objects, integrate orchestration concepts

**Tasks:**
1. Migrate `src/common/agent_loader.py` → `src/domain/collaboration/agent.py`:
   - Enhance with `AgentProfile` domain object
   - Support `.doctrine-config/` local overrides
2. Enhance `src/common/task_schema.py` → `src/domain/collaboration/task.py`:
   - Add `Task` domain object (beyond ADR-042 I/O functions)
   - Link to `AgentProfile` (assigned agent)
3. Implement orchestration concepts:
   - `batch.py` (Batch domain object)
   - `iteration.py` (Iteration, IterationPhase)
   - `cycle.py` (Cycle)
4. Update `src/framework/orchestration/` to use domain objects
5. Write integration tests

**Deliverables:**
- Full collaboration domain model
- Integration tests with framework layer
- Migration guide for framework orchestration code

**Acceptance Criteria:**
- ✅ Framework orchestration uses `AgentProfile`, `Task`, `Batch` objects
- ✅ Local agent overrides work correctly
- ✅ No circular dependencies between domain and framework

---

### Phase 3: File Loaders & Parsers (Week 3, ~24 hours)

**Goal:** Robust YAML/Markdown parsers for all doctrine artifacts

**Tasks:**
1. Implement `src/domain/doctrine/loaders/`:
   - `directive_loader.py` (parse `doctrine/directives/*.md`)
   - `tactic_loader.py` (parse `doctrine/tactics/*.md`)
   - `approach_loader.py` (parse `doctrine/approaches/*.md`)
   - `style_guide_loader.py` (parse `doctrine/guidelines/*.md`)
   - `template_loader.py` (parse `doctrine/templates/*.md`)
2. Implement frontmatter parsing (YAML in Markdown)
3. Handle edge cases:
   - Missing required fields
   - Invalid YAML syntax
   - Malformed Markdown structure
4. Implement caching layer (avoid re-parsing on every load)
5. Write comprehensive loader tests

**Deliverables:**
- Robust loaders with error handling
- Cache mechanism (file mtime-based invalidation)
- Test suite covering edge cases

**Acceptance Criteria:**
- ✅ All existing doctrine files parse successfully
- ✅ Invalid configs fail with clear error messages
- ✅ Caching reduces load time by >50%

---

### Phase 4: Validation Logic (Week 4, ~16 hours)

**Goal:** Ensure loaded domain objects are consistent and complete

**Tasks:**
1. Implement validation rules for each domain object:
   - `AgentProfile`: Required directives exist, artifact types valid
   - `Directive`: Applies to valid agents, enforcement level valid
   - `Tactic`: Steps ordered, prerequisites reference valid tactics
   - `Approach`: Related directives exist
2. Cross-reference validation:
   - Agent's `required_directives` → Directive objects exist
   - Directive's `applies_to_agents` → Agent IDs valid
   - Tactic's `related_directives` → Directive numbers exist
3. Implement validation CLI command:
   ```bash
   $ kitty validate doctrine
   Validating doctrine stack...
   ✅ Agents: 15 valid
   ✅ Directives: 34 valid
   ❌ Tactics: 1 error
       - tactic 'incremental-commit' references missing directive '099'
   ```
4. Write validation tests

**Deliverables:**
- Comprehensive validation logic
- CLI validation command
- Test suite for validation rules

**Acceptance Criteria:**
- ✅ Validation catches all consistency errors
- ✅ CLI command provides actionable error messages
- ✅ Existing doctrine stack validates successfully

---

### Phase 5: UI/Export Integrations (Week 5-6, ~32 hours)

**Goal:** Enable UI inspection and vendor tool export

**Tasks:**
1. **Dashboard Integration:**
   - Create `src/llm_service/dashboard/pages/agents_page.py`
   - Create `src/llm_service/dashboard/pages/directives_page.py`
   - Create `src/llm_service/dashboard/pages/doctrine_stack_page.py`
   - Add navigation links
2. **CLI Inspection Commands:**
   - `kitty show agents`
   - `kitty show directives`
   - `kitty inspect stack`
   - `kitty check compliance --agent=<id>`
3. **Adapter Layer:**
   - Implement `src/adapters/base.py` (AbstractAdapter)
   - Implement `src/adapters/opencode.py` (OpenCodeAdapter)
   - Implement `src/adapters/cursor.py` (CursorAdapter)
   - Implement export CLI: `kitty export --format=opencode --output=.opencode/agents.json`
4. Write integration tests

**Deliverables:**
- Dashboard pages for doctrine inspection
- CLI commands for introspection
- Adapter layer with 2+ vendor tool exports
- Integration tests for UI and export

**Acceptance Criteria:**
- ✅ Dashboard displays all doctrine artifacts
- ✅ CLI commands work in CI/local environments
- ✅ Export to OpenCode/Cursor generates valid configs

---

### Phase 6: Migration & Cleanup (Week 7, ~12 hours)

**Goal:** Complete src/common/ → src/domain/ migration

**Tasks:**
1. Update all import paths:
   - Framework layer: `src/framework/orchestration/`
   - Dashboard: `src/llm_service/dashboard/`
   - Tools: `tools/*.py`
   - Scripts: `scripts/*.py`
2. Remove old `src/common/` files:
   - Keep only `src/domain/common/types.py` and `src/domain/common/exceptions.py`
3. Update documentation:
   - `docs/architecture/README.md` - Document domain layer
   - `REPO_MAP.md` - Update structure diagram
4. Run full test suite, ensure no regressions
5. Create ADRs:
   - ADR-045: Doctrine Code Representations
   - ADR-046: Domain Layer Refactoring

**Deliverables:**
- All imports updated
- Old files removed
- Documentation updated
- ADRs written

**Acceptance Criteria:**
- ✅ All tests pass (unit, integration, E2E)
- ✅ No references to old `src/common/` paths
- ✅ Documentation reflects new structure

---

## 7. Trade-offs

### 7.1 Benefits

| Benefit | Impact | Justification |
|---------|--------|---------------|
| **Type Safety** | HIGH | IDE autocomplete, mypy validation, reduced runtime errors |
| **UI Inspection** | HIGH | Dashboard and CLI can introspect doctrine stack programmatically |
| **Vendor Tool Export** | MEDIUM | Enables distribution to OpenCode, Cursor, Cody, etc. |
| **Domain Clarity** | HIGH | Clear separation: collaboration ≠ doctrine ≠ specifications |
| **Testability** | HIGH | Domain objects are pure data structures, easy to unit test |
| **Maintainability** | HIGH | Single source of truth for domain concepts |
| **Extensibility** | MEDIUM | New domain objects (e.g., Milestone) follow established patterns |

### 7.2 Costs

| Cost | Impact | Mitigation |
|------|--------|-----------|
| **Implementation Effort** | HIGH (120 hours) | Phased approach spreads work over 7 weeks |
| **Breaking Changes** | MEDIUM | All import paths change | Comprehensive test suite catches regressions |
| **Learning Curve** | LOW | New domain layer structure | Clear documentation + examples |
| **Parsing Overhead** | LOW | YAML/Markdown parsing on every load | Caching layer (Phase 3) |
| **Maintenance Burden** | LOW | More code to maintain | Domain objects are simple dataclasses, minimal logic |

### 7.3 Alternatives Considered

#### Alternative 1: Keep Doctrine as Pure YAML/Markdown ❌ REJECTED

**Pros:**
- Simple: No code representations needed
- Lightweight: No parsing/validation overhead

**Cons:**
- No type safety
- No UI inspection capability
- No vendor tool export
- Parsing logic scattered across codebase

**Rationale:** Fails to support UI inspection and vendor distribution initiatives (core requirements).

---

#### Alternative 2: Use Pydantic Models Instead of Dataclasses ⚠️ DEFERRED

**Pros:**
- Built-in validation (field constraints, custom validators)
- JSON schema generation (for OpenAPI docs)
- Better error messages

**Cons:**
- Heavier dependency (Pydantic ~300KB)
- More complex API (Field() descriptors, validators)
- ADR-026 (Pydantic v2 validation) adds complexity

**Rationale:** Dataclasses + manual validation are sufficient for Phase 1-4. Consider Pydantic upgrade in future if validation logic becomes complex. Create ADR-026 implementation task if needed.

---

#### Alternative 3: Single Domain Module (No Subdomains) ❌ REJECTED

**Pros:**
- Simpler structure: `src/domain/models.py` with all domain objects
- Fewer files to navigate

**Cons:**
- Violates single responsibility principle
- Mixes collaboration/doctrine/specifications concerns
- Hard to navigate (would be >2000 lines)

**Rationale:** Domain submodules (`collaboration/`, `doctrine/`, `specifications/`) provide clear conceptual boundaries.

---

#### Alternative 4: Keep src/common/ Name ⚠️ CONSIDERED

**Pros:**
- No import path changes
- Less migration effort

**Cons:**
- Name is misleading: "common" suggests utilities, not domain concepts
- Doesn't clarify domain boundaries

**Rationale:** Renaming `src/common/` → `src/domain/common/` (for types/exceptions) is low effort with high clarity gain.

---

## 8. Success Metrics

### 8.1 Quantitative Metrics

| Metric | Baseline (Before) | Target (After) |
|--------|-------------------|----------------|
| **Domain Object Coverage** | 0 domain objects | 15+ domain objects (Agent, Directive, Tactic, etc.) |
| **Type Coverage** | ~60% (framework only) | >85% (domain + framework) |
| **Test Coverage** | ~70% | >80% (domain layer >90%) |
| **YAML Parsing Code** | Scattered in 5+ files | Centralized in `src/domain/*/loaders/` |
| **CLI Inspection Commands** | 0 | 5+ commands (show agents, directives, etc.) |
| **Vendor Tool Adapters** | 0 | 2+ (OpenCode, Cursor) |

### 8.2 Qualitative Metrics

| Metric | Assessment Criteria |
|--------|---------------------|
| **Developer Experience** | Can IDE autocomplete suggest AgentProfile fields? ✅ |
| **Maintainability** | Can new domain objects be added by following existing patterns? ✅ |
| **Testability** | Can domain objects be unit tested in isolation? ✅ |
| **Clarity** | Do new contributors understand domain boundaries? ✅ (via docs) |
| **Extensibility** | Can we add new orchestration concepts (e.g., Milestone) easily? ✅ |

### 8.3 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| **Breaking Changes** | HIGH | MEDIUM | Comprehensive test suite, phased rollout |
| **Scope Creep** | MEDIUM | HIGH | Strict phase boundaries, defer non-critical features |
| **Performance Regression** | LOW | LOW | Caching layer (Phase 3), benchmarking |
| **Incomplete Migration** | MEDIUM | MEDIUM | Phase 6 dedicated to cleanup, checklist validation |

---

## 9. Related Documentation

### 9.1 Existing ADRs

- **ADR-042: Shared Task Domain Model** - Establishes pattern for domain objects in `src/common/task_schema.py`
- **ADR-043: Status Enumeration Standard** - Defines `TaskStatus`, `FeatureStatus` enums
- **ADR-044: Agent Identity Type Safety** - Defines `AgentIdentity` Literal type
- **ADR-006: Three-Layer Governance Model** - Establishes doctrine framework structure

### 9.2 Related Initiatives

- **specifications/initiatives/terminology-alignment-refactoring.md** - Conceptual alignment between doctrine terms and code
- **SPEC-DIST-001: Vendor Tool Distribution** - Export doctrine configs to vendor tools
- **SPEC-DASH-008: Dashboard Configuration Management** - UI for doctrine inspection

### 9.3 Doctrine Stack

- **DOCTRINE_STACK.md** - Current doctrine stack versioning
- **GLOSSARY.md** - Ubiquitous language definitions
- **doctrine/agents/*.agent.md** - Agent profile source files
- **doctrine/directives/*.md** - Directive documentation

---

## 10. Next Steps & ADR Creation

### 10.1 Immediate Actions

1. **Create ADR-045: Doctrine Code Representations**
   - Location: `docs/architecture/adrs/ADR-045-doctrine-code-representations.md`
   - Content: Decision to create domain objects for doctrine concepts
   - Status: Draft → Review → Accepted

2. **Create ADR-046: Domain Layer Refactoring**
   - Location: `docs/architecture/adrs/ADR-046-domain-layer-refactoring.md`
   - Content: Decision to refactor `src/common/` → `src/domain/` with subdomains
   - Status: Draft → Review → Accepted

3. **Update Architectural Overview**
   - Location: `docs/architecture/README.md`
   - Add section: "Domain Layer Architecture"
   - Diagram: Layer dependency graph (Configuration → Domain → Framework → Application)

4. **Update REPO_MAP.md**
   - Add `src/domain/` structure
   - Mark `src/common/` as deprecated (migration in progress)

### 10.2 Initiative Tracking

**Create Initiative:**
- **Title:** "Doctrine Code Representations Implementation"
- **Location:** `specifications/initiatives/doctrine-code-representations.md`
- **Status:** Planned
- **Phases:** 6 phases (see §6 Implementation Phases)
- **Tasks:** Create tasks for each phase in `work/collaboration/tasks/`
- **Cross-references:** Link to ADR-045, ADR-046

**Link Existing Initiatives:**
- **SPEC-DIST-001:** Update to reference adapter layer (§5.2)
- **SPEC-DASH-008:** Update to reference domain objects for UI (§5.3)

### 10.3 Team Communication

**Announce to Team:**
- **Curator Claire:** Check `doctrine/` artifacts for ADR references (dependency direction violation, see §4.2 Rule 1)
- **Manager Mike:** Assess if orchestration agent role fits batch/iteration/cycle concepts (see §2.2.2)
- **Backend Benny:** Assign Phase 1-2 implementation tasks (see §6)
- **Planning Petra:** Schedule 7-week implementation timeline

---

## Appendix A: Example Domain Object Usage

### Loading and Using AgentProfile

```python
from src.domain.collaboration.agent import load_agent_profiles

# Load all agent profiles
agents = load_agent_profiles()

# Find specific agent
alphonso = next(a for a in agents if a.agent_id == "architect-alphonso")

print(f"Agent: {alphonso.display_name}")
print(f"Specialization: {alphonso.specialization}")
print(f"Default Mode: {alphonso.default_mode.value}")
print(f"Required Directives: {', '.join(alphonso.required_directives)}")

# Validate profile
errors = alphonso.validate()
if errors:
    print("Validation errors:", errors)
```

### Loading and Using Directive

```python
from src.domain.doctrine.directive import load_directives

# Load all directives
directives = load_directives()

# Check if directive applies to agent
directive_017 = next(d for d in directives if d.number == "017")
if directive_017.is_required_for_agent("backend-benny"):
    print(f"Directive {directive_017.number} is required for backend-benny")
```

### Creating and Managing Batch

```python
from src.domain.collaboration.batch import Batch
from src.domain.common.types import TaskPriority
from datetime import datetime

# Create batch
batch = Batch(
    batch_id="M4-batch-4.1",
    title="Implement domain layer core objects",
    milestone_id="M4",
    tasks=["TASK-001", "TASK-002", "TASK-003"],
    priority=TaskPriority.HIGH,
    estimated_effort=None,
    status="in_progress",
    started_at=datetime.now(),
    completed_at=None,
    max_parallel_tasks=2,
    dependencies=["M4-batch-4.0"],
)

# Calculate progress (requires task registry)
# progress = batch.calculate_progress(task_registry)
```

---

## Appendix B: Validation Rules Summary

### AgentProfile Validation

- `agent_id` must be lowercase with hyphens
- `specialization` is required
- `default_mode` must be in `available_modes`
- All `required_directives` must reference existing Directive numbers
- All `required_approaches` must reference existing Approach IDs

### Directive Validation

- `number` must be 3-digit string (e.g., "001", "014")
- `enforcement_level` must be "required", "recommended", or "optional"
- `applies_to_agents` must be "*" or list of valid agent IDs
- `status` must be "active", "deprecated", or "draft"

### Tactic Validation

- `tactic_id` must be lowercase with hyphens
- `steps` must have unique `order` values
- All `prerequisites` in TacticStep must reference valid tactic IDs
- All `related_directives` must reference existing Directive numbers

### Batch Validation

- `batch_id` must match pattern `M\d+-batch-\d+\.\d+` (e.g., "M4-batch-4.1")
- `tasks` must be non-empty list
- `status` must be "planned", "in_progress", "completed", or "blocked"
- If `status` is "completed", `completed_at` must be set

---

**END OF ARCHITECTURAL ANALYSIS**

---

## Approval & Sign-off

**Architect:** Alphonso  
**Status:** APPROVED ✅  
**Date:** 2026-02-11  

**Reviewed By:**
- @stijn-dejongh (Product Owner) - Approved

**Next Actions:**
1. Backend Benny: Create ADR-045 and ADR-046
2. Curator Claire: Check doctrine artifacts for ADR dependency violations
3. Manager Mike: Assess orchestration agent role alignment
4. Planning Petra: Create initiative and tasks for 7-week implementation
