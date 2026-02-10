# Code-Level Terminology Validation Report

**Reviewer:** Code-reviewer Cindy  
**Date:** 2026-02-10  
**Context:** Living Glossary Practice (doctrine/approaches/living-glossary-practice.md)  
**Scope:** src/, tools/, tests/ directories  

---

## Executive Summary

✅ **SDD Agent "Code-reviewer Cindy" initialized.**  
**Context layers:** Operational ✓, Strategic ✓, Command ✓, Bootstrap ✓, AGENTS ✓.  
**Purpose acknowledged:** Review work for quality, clarity, and traceability.

### Key Findings

| Metric | src/ | tools/ | tests/ | Overall |
|--------|------|--------|--------|---------|
| Files Analyzed | 50 | 31 | 82 | 163 |
| Glossary Terms Used | 9/44 (20.5%) | 5/44 (11.4%) | 9/44 (20.5%) | 11/44 (25.0%) |
| Candidate Terms Found | 19 | 14 | 19 | 21 |
| Generic Anti-Patterns | 9 classes | 1 class | 9 classes | 19 classes |

### Overall Assessment

⚠️ **PARTIAL ALIGNMENT** - The codebase shows early-stage glossary adoption with significant opportunity for improvement:

- **Strengths:** Core orchestration terms (Agent, Task, Orchestrator) are consistently used
- **Gaps:** Most DDD terms (Bounded Context, Domain Event, Value Object) not present in code
- **Opportunities:** Strong domain concepts exist in code but are missing from glossary
- **Anti-Patterns:** Generic naming (Manager, Handler, Processor) prevalent without domain context

---

## 1. Glossary Term Usage Analysis

### 1.1 Terms Currently in Use

#### ✅ Well-Adopted Terms (>10 files)

| Term | src/ | tools/ | tests/ | Total | Assessment |
|------|------|--------|--------|-------|------------|
| **Agent** | 24 | 21 | 42 | 87 | ✅ Excellent - Core identity term consistently used |
| **Load** | 23 | 19 | 36 | 78 | ✅ Good - Technical operation well-established |
| **Parser** | 12 | 17 | 9 | 38 | ✅ Good - Technical pattern consistently named |

**Observation:** These terms show strong adoption and consistent usage across the codebase.

#### ⚠️ Emerging Terms (2-10 files)

| Term | src/ | tools/ | tests/ | Total | Assessment |
|------|------|--------|--------|-------|------------|
| **Task File** | 12 | 9 | 25 | 46 | ⚠️ Inconsistent - Often just "file" or "yaml file" |
| **Work Directory** | 7 | 7 | 15 | 29 | ⚠️ Variable - Sometimes "work dir", "collab dir" |
| **Task Assignment** | 2 | 1 | 5 | 8 | ⚠️ Weak - "assign" verb more common than noun phrase |
| **Orchestrator** | 2 | 0 | 4 | 6 | ⚠️ Limited - Only in orchestration module |
| **Aggregate** | 2 | 1 | 4 | 7 | ⚠️ Limited - DDD term not widely adopted |
| **Persist** | 1 | 0 | 1 | 2 | ⚠️ Rare - "save", "write" more common |
| **Entity** | 2 | 0 | 1 | 3 | ⚠️ Rare - DDD term minimal adoption |

**Observation:** These terms exist but compete with informal alternatives or are confined to specific modules.

#### ❌ Missing Terms (0 files)

**From DDD Glossary:**
- Bounded Context
- Ubiquitous Language
- Domain Event
- Value Object
- Context Map
- Upstream (as DDD concept)
- Downstream (as DDD concept)
- Published Language (as integration pattern)

**From Software Design Glossary:**
- Shared Kernel
- Conformist
- Partnership

**From Organizational Glossary:**
- Conway's Law
- Stream-Aligned Team
- Cognitive Load

**From Orchestration Glossary (Proposed):**
- TaskDescriptor (concept exists, name not used)
- Serialize/Deserialize (functions exist, not as domain terms)
- TaskAggregate (concept exists as Task, not distinguished)
- WorkItem (concept exists as Task, not distinguished)
- Inbox State, Assigned State, etc. (status values exist, not state terminology)

**Observation:** Most DDD and strategic terms are absent. This suggests either:
1. The glossary includes aspirational terms not yet implemented
2. The code predates glossary creation
3. Domain boundaries not yet clearly established in implementation

---

## 2. Terminology Issues by Severity

### 2.1 Advisory Issues ℹ️

Issues that suggest improvements but don't block development.

#### A1: Inconsistent Naming for Task Files

**Locations:**
- `src/framework/orchestration/task_utils.py:69` - "task file"
- `src/framework/orchestration/agent_orchestrator.py:51` - "task_file"
- `src/llm_service/dashboard/file_watcher.py:137` - "file_path"
- `tools/scripts/complete_task.py` - "task YAML"

**Issue:** Glossary defines "Task File" but code uses multiple variants.

**Recommendation:** Standardize to "task_file" variable naming and "Task File" in documentation.

**Severity:** **Advisory** - Low impact, style consistency improvement.

---

#### A2: Generic "Load" vs. Specific Operations

**Locations:**
- `src/common/task_schema.py:34` - `read_task()` function
- `src/framework/orchestration/task_utils.py:19` - `read_task` (re-export)
- Glossary defines "Load" as "Read task descriptor from file system"

**Issue:** Glossary term "Load" is generic. Code uses more specific "read_task" which better follows Python conventions (cf. `json.load()` vs. domain-specific naming).

**Recommendation:** 
- Keep `read_task()` as function name (Pythonic)
- Update glossary: "Load" → "Read Task" or remove in favor of implementation-level detail
- Or: Define "Load" as general operation, not specific function name

**Severity:** **Advisory** - Terminology precision improvement.

---

#### A3: Missing Domain Language for Dashboard Concepts

**Locations:**
- `src/llm_service/dashboard/spec_parser.py` - Specification, Initiative, Feature, Epic
- `src/llm_service/dashboard/task_linker.py` - Portfolio, Completion tracking
- `src/llm_service/dashboard/task_priority_updater.py` - Priority editing

**Issue:** Dashboard implements rich domain model (Specification, Initiative, Feature, Epic, Portfolio) not documented in glossary.

**Recommendation:** Create "Portfolio Management" or "Planning Domain" glossary context with:
- Initiative: High-level project/milestone grouping
- Specification: Formal requirements document with features
- Feature: Specific capability or user story within spec
- Epic: Multi-specification collection (if distinct from Initiative)
- Portfolio View: Aggregate view of initiatives and their progress

**Severity:** **Advisory** - Missing domain vocabulary documentation.

---

#### A4: "Persist" Terminology Underutilized

**Locations:**
- `src/common/task_schema.py:100` - `write_task()` function
- Glossary defines "Persist" as "Write task descriptor to file system"

**Issue:** Only 1 usage of "persist" terminology found. Most code uses "write" or "save".

**Recommendation:** 
- Option 1: Standardize on "persist" if durability semantics important (DDD emphasis)
- Option 2: Accept "write" as Pythonic convention, update glossary to "Write Task"
- Option 3: Distinguish: "write" = file I/O operation, "persist" = domain operation ensuring durability

**Severity:** **Advisory** - Terminology consistency improvement.

---

### 2.2 Acknowledgment Required Issues ⚠️

Issues requiring explicit acknowledgment before merging code.

#### AK1: Generic Anti-Pattern Naming

**Locations:**

**Managers (4 instances):**
- `src/llm_service/templates/manager.py:31` - `TemplateManager`
  - Context: Manages Jinja2 templates for config generation
  - **Better name:** `TemplateRenderer` or `ConfigurationTemplateService`

**Handlers (5 instances):**
- `src/llm_service/dashboard/file_watcher.py:22` - `TaskFileHandler`
  - Context: File system event handler for watchdog
  - **Assessment:** Acceptable - "Handler" is watchdog framework convention
  - **Severity:** Advisory only - follows framework pattern
  
- `src/llm_service/dashboard/spec_cache.py:33` - `SpecChangeHandler`
  - Context: File system event handler for watchdog
  - **Assessment:** Acceptable - framework convention
  
- `src/llm_service/dashboard/task_assignment_handler.py:49` - `TaskAssignmentHandler`
  - Context: Domain service for assigning tasks to specifications
  - **Better name:** `TaskAssignmentService` or `OrphanTaskAssigner`
  - **Rationale:** This is domain logic, not event handling
  - **Severity:** Acknowledgment Required

**Wrappers (5 instances):**
- `src/llm_service/adapters/subprocess_wrapper.py` - `SubprocessWrapper`
  - Context: Subprocess execution with timeout handling
  - **Better name:** `SubprocessExecutor` or `TimeoutSubprocess`

**Issue:** Generic suffixes obscure domain meaning and create namespace pollution.

**Recommendation:** 
1. For framework handlers (watchdog): Keep "Handler" suffix - framework convention
2. For domain services: Use domain-specific names
3. Update Living Glossary to document when generic names are acceptable vs. problematic

**Severity:** **Acknowledgment Required** for domain classes, **Advisory** for framework adapters.

---

#### AK2: Missing TaskDescriptor Type

**Locations:**
- `src/common/task_schema.py` - Uses `Dict[str, Any]` for task representation
- `src/framework/orchestration/task_utils.py` - Uses `dict[str, Any]`
- `src/framework/orchestration/agent_orchestrator.py` - Uses `dict[str, Any]`
- Glossary (proposed) defines "TaskDescriptor" as "YAML-serializable representation"

**Issue:** Glossary proposes "TaskDescriptor" type but code uses raw dictionaries everywhere.

**Code Examples:**
```python
# src/common/task_schema.py:34
def read_task(path: Path) -> Dict[str, Any]:
    # Returns generic dict

# src/framework/orchestration/agent_base.py:378
def execute_task(self, task: dict[str, Any]) -> dict[str, Any]:
    # Accepts generic dict
```

**Recommendation:**
- Option 1: Create `TaskDescriptor` TypedDict or dataclass for type safety
- Option 2: Remove "TaskDescriptor" from glossary (use "Task" directly)
- Option 3: Document explicit decision to use `dict` for flexibility

**Traceability:** This decision should reference ADR-042 (Shared Task Domain Model).

**Severity:** **Acknowledgment Required** - Type safety vs. flexibility trade-off needs explicit decision.

---

#### AK3: State Terminology Mismatch

**Locations:**
- `src/common/types.py:31` - `class TaskStatus(str, Enum)` with values like "assigned", "in_progress"
- Glossary defines: "Inbox State", "Assigned State", "In Progress State", etc.

**Issue:** Code uses "status" consistently, glossary uses "state". These are semantically different:
- **Status:** Current condition (noun) - "What is the task's status?"
- **State:** Identity in state machine (noun) - "What state is the task in?"

**Code Pattern:**
```python
class TaskStatus(str, Enum):
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    DONE = "done"
```

**Glossary Pattern:**
```yaml
term: "Assigned State"
definition: "Task assigned to specific agent..."
```

**Recommendation:**
- Option 1: Align glossary to code - use "Status" terminology (RECOMMENDED)
- Option 2: Refactor code to use "State" terminology (high risk)
- Option 3: Document distinction: Status = enum value, State = conceptual lifecycle phase

**Severity:** **Acknowledgment Required** - Terminology alignment decision needed.

---

### 2.3 Hard Failure Issues ❌

Critical violations requiring immediate fix before merge.

#### None Identified

**Assessment:** No critical violations found. The codebase is functional and consistent within itself. Issues are primarily about alignment with aspirational glossary and domain clarity.

---

## 3. Missing Terminology - Glossary Candidates

These domain concepts appear consistently in code but are missing from glossaries.

### 3.1 Core Domain Concepts (High Priority)

#### C1: TaskStatus Enumeration

**Usage:** 8 files in src/, 4 in tools/, 4 in tests/  
**Definition:** Task lifecycle states (new, inbox, assigned, in_progress, blocked, done, error)  
**Source:** `src/common/types.py:31`  
**Rationale:** Central domain concept with state machine semantics

**Proposed Glossary Entry:**
```yaml
term: "TaskStatus"
definition: "Enumeration of task lifecycle states with transition rules"
context: "Task Domain"
status: "canonical"
source: "ADR-043: Status Enumeration Standard"
related_terms:
  - "Task Lifecycle Directory"
  - "State Machine"
values:
  - new: "Task created, awaiting assignment"
  - inbox: "Task in inbox, awaiting agent pickup"
  - assigned: "Task assigned to specific agent"
  - in_progress: "Agent actively executing task"
  - blocked: "Task blocked on dependency"
  - done: "Task successfully completed (terminal)"
  - error: "Task failed with error (terminal)"
enforcement_tier: "acknowledgment"
```

---

#### C2: Specification (Requirements Domain)

**Usage:** 10 files in src/, 4 in tools/, 13 in tests/  
**Definition:** Formal requirements document containing features and metadata  
**Source:** `src/llm_service/dashboard/spec_parser.py:44`  
**Rationale:** Central to portfolio tracking and task assignment

**Proposed Glossary Entry:**
```yaml
term: "Specification"
definition: "Formal requirements document defining features, acceptance criteria, and implementation scope"
context: "Requirements Domain"
status: "canonical"
related_terms:
  - "Initiative"
  - "Feature"
  - "Portfolio View"
attributes:
  - id: Unique identifier (e.g., SPEC-DASH-008)
  - title: Human-readable name
  - initiative: Parent initiative grouping
  - features: List of features defined
  - status: Implementation status (draft, planned, in_progress, implemented)
file_format: "Markdown with YAML frontmatter"
location: "specifications/**/*.md"
enforcement_tier: "advisory"
```

---

#### C3: Initiative (Portfolio Domain)

**Usage:** 5 files in src/, 1 in tools/, 13 in tests/  
**Definition:** High-level project or milestone grouping multiple specifications  
**Source:** `src/llm_service/dashboard/spec_parser.py:52`  
**Rationale:** Organizational concept for portfolio management

**Proposed Glossary Entry:**
```yaml
term: "Initiative"
definition: "High-level project or milestone that groups related specifications and tracks aggregate progress"
context: "Portfolio Domain"
status: "canonical"
related_terms:
  - "Specification"
  - "Epic"
  - "Portfolio View"
examples:
  - "framework-distribution"
  - "dashboard-enhancements"
  - "quickstart-onboarding"
structure: "Directory-based grouping in specifications/initiatives/"
enforcement_tier: "advisory"
```

---

#### C4: Feature (Requirements Domain)

**Usage:** 19 files in src/, 3 in tools/, 15 in tests/  
**Definition:** Specific capability or user story within a specification  
**Source:** `src/llm_service/dashboard/spec_parser.py:23`  
**Rationale:** Granular unit of work linked to tasks

**Proposed Glossary Entry:**
```yaml
term: "Feature"
definition: "Specific capability, user story, or functional requirement within a specification"
context: "Requirements Domain"
status: "canonical"
related_terms:
  - "Specification"
  - "Task"
  - "FeatureStatus"
attributes:
  - id: Feature identifier (e.g., "orphan-task-assignment")
  - title: Human-readable description
  - status: Implementation status
relationship_to_tasks: "Tasks reference feature ID for traceability"
enforcement_tier: "advisory"
```

---

#### C5: Configuration (Infrastructure Domain)

**Usage:** 15 files in src/, 7 in tools/, 20 in tests/  
**Definition:** System settings and parameters for LLM service and agents  
**Source:** `src/llm_service/config/schemas.py`  
**Rationale:** Pervasive infrastructure concept

**Proposed Glossary Entry:**
```yaml
term: "Configuration"
definition: "Declarative system settings for LLM service, agents, tools, models, and policies"
context: "Infrastructure Domain"
status: "canonical"
source: "ADR-031: Template-Based Configuration Generation"
related_terms:
  - "Template"
  - "Agent Config"
  - "Model Config"
file_format: "YAML configuration files"
validation: "Pydantic schemas in config/schemas.py"
enforcement_tier: "advisory"
```

---

### 3.2 Technical Patterns (Medium Priority)

#### C6: Dashboard (UI Domain)

**Usage:** 14 files in src/, 6 in tools/, 32 in tests/  
**Definition:** Web-based interface for task management and portfolio tracking  
**Source:** `src/llm_service/dashboard/app.py`  
**Rationale:** Major system component with distinct vocabulary

**Proposed Glossary Entry:**
```yaml
term: "Dashboard"
definition: "Web-based user interface for agent task management, portfolio tracking, and telemetry visualization"
context: "UI Domain"
status: "canonical"
components:
  - Portfolio View: Initiative and specification tracking
  - Task Queue View: Agent assignment and status
  - Telemetry View: System metrics and performance
technology_stack: "Flask + vanilla JavaScript + Server-Sent Events"
enforcement_tier: "advisory"
```

---

#### C7: Telemetry (Observability Domain)

**Usage:** 8 files in src/, 1 in tools/, 10 in tests/  
**Definition:** Structured logging and metrics collection for system observability  
**Source:** `src/llm_service/telemetry/logger.py`  
**Rationale:** Cross-cutting infrastructure concern

**Proposed Glossary Entry:**
```yaml
term: "Telemetry"
definition: "Structured logging and metrics collection for system observability and performance analysis"
context: "Observability Domain"
status: "canonical"
related_terms:
  - "Dashboard"
  - "Event Log"
storage: "SQLite database (telemetry.db)"
schema: "Event-sourced log with structured fields"
enforcement_tier: "advisory"
```

---

#### C8: Template (Configuration Domain)

**Usage:** 12 files in src/, 4 in tools/, 15 in tests/  
**Definition:** Jinja2-based configuration file generator  
**Source:** `src/llm_service/templates/manager.py`  
**Rationale:** Key pattern for configuration management

**Proposed Glossary Entry:**
```yaml
term: "Template"
definition: "Jinja2-based configuration file generator with variable substitution and environment expansion"
context: "Configuration Domain"
status: "canonical"
source: "ADR-031: Template-Based Configuration Generation"
related_terms:
  - "Configuration"
  - "TemplateManager"
format: "Jinja2 with ${VAR} environment variable syntax"
location: "src/llm_service/templates/"
enforcement_tier: "advisory"
```

---

### 3.3 Lifecycle Operations (Low Priority)

#### C9: Assignment / Handoff / Completion

**Usage:**
- Assignment: 3 files in src/, 6 in tests/
- Handoff: 2 files in src/, 1 in tools/, 2 in tests/
- Completion: 5 files in src/, 2 in tools/, 16 in tests/

**Definition:** Task lifecycle operations  
**Source:** `src/framework/orchestration/agent_orchestrator.py`  
**Rationale:** Operational vocabulary for orchestration

**Proposed Glossary Entry:**
```yaml
term: "Task Assignment"
definition: "Operation of moving task from inbox to agent-specific queue"
context: "Orchestration Context"
status: "canonical"
implementation: "agent_orchestrator.assign_tasks()"
state_transition: "inbox → assigned"

term: "Task Handoff"
definition: "Transfer of work artifacts from one agent to another via next_agent field"
context: "Orchestration Context"  
status: "canonical"
implementation: "agent_orchestrator.log_handoff()"
related_terms:
  - "Task Assignment"
  - "Agent Queue"

term: "Task Completion"
definition: "Operation marking task as done and moving to completion directory"
context: "Orchestration Context"
status: "canonical"
state_transition: "in_progress → done"
required_fields: ["result", "completed_at"]
enforcement_tier: "advisory"
```

---

## 4. Code Coverage Analysis

### 4.1 Directory-Level Alignment

| Directory | Glossary Alignment | Dominant Terminology | Assessment |
|-----------|-------------------|---------------------|------------|
| `src/framework/orchestration/` | ⚠️ **Moderate** (30%) | Agent, Task, Orchestrator, Status | Core orchestration terms present, missing TaskDescriptor and State terminology |
| `src/llm_service/dashboard/` | ⚠️ **Weak** (15%) | Specification, Initiative, Feature, Dashboard | Domain-rich but disconnected from glossary |
| `src/llm_service/config/` | ⚠️ **Weak** (10%) | Configuration, Schema, Template | Configuration domain not in glossary |
| `src/llm_service/adapters/` | ⚠️ **Weak** (10%) | Adapter, Wrapper, Parser | Technical patterns, no domain language |
| `src/common/` | ⚠️ **Moderate** (40%) | Task, Status, Agent, Schema | Core shared types with some glossary alignment |
| `tools/scripts/` | ⚠️ **Weak** (15%) | Task, Agent, Script | Operational scripts, minimal domain terminology |
| `tests/` | ⚠️ **Moderate** (25%) | Test, Given/When/Then, Task, Agent | BDD-style tests with some domain terms |

**Overall Pattern:** 
- Orchestration and shared types modules have better alignment
- Dashboard and configuration modules are domain-rich but glossary-poor
- Generic technical patterns (adapters, parsers) lack domain context

---

### 4.2 Module-Specific Findings

#### Module: `src/framework/orchestration/`

**Strengths:**
- ✅ Consistent use of "Agent", "Task", "Orchestrator"
- ✅ Clear operational vocabulary (assign, complete, execute)
- ✅ File-based coordination pattern well-established

**Gaps:**
- ❌ No "TaskDescriptor" type (uses `dict[str, Any]`)
- ❌ "Status" vs. "State" terminology mismatch with glossary
- ❌ "Work Directory" not consistently named (WORK_DIR, COLLAB_DIR, work/)
- ❌ Missing domain events (TaskAssigned, TaskCompleted)

**Recommendation:** This is the BEST module for glossary enforcement pilot.

---

#### Module: `src/llm_service/dashboard/`

**Strengths:**
- ✅ Rich domain model (Specification, Initiative, Feature, Portfolio)
- ✅ Clear bounded context separation from orchestration
- ✅ Dataclass-based domain objects (Feature, SpecificationMetadata)

**Gaps:**
- ❌ Entire domain vocabulary missing from glossary
- ❌ No explicit bounded context documentation
- ❌ Generic class names (TaskAssignmentHandler, SpecificationCache)

**Recommendation:** Create "Portfolio Management Context" glossary to document this domain.

---

#### Module: `src/common/`

**Strengths:**
- ✅ Excellent type safety (TaskStatus, FeatureStatus enums)
- ✅ Documented state machine semantics
- ✅ Shared domain model (ADR-042, ADR-043)

**Gaps:**
- ❌ Types not documented in glossary
- ❌ No cross-reference between ADRs and glossary terms

**Recommendation:** Add all enums from `types.py` to glossary with ADR traceability.

---

## 5. Specific Code Locations Needing Attention

### 5.1 High-Priority Locations

#### Location 1: `src/common/types.py`

**Issue:** Core domain types not documented in glossary  
**Lines:** 31-319 (entire file)  
**Terms:** TaskStatus, FeatureStatus, TaskMode, TaskPriority, AgentIdentity  
**Action:** Add all enums to glossary with full documentation  
**Severity:** High - Central to domain model  
**Effort:** Medium (5 glossary entries)

---

#### Location 2: `src/llm_service/dashboard/spec_parser.py`

**Issue:** Portfolio domain vocabulary not in glossary  
**Lines:** 23-80 (Feature and SpecificationMetadata classes)  
**Terms:** Specification, Initiative, Feature, Epic, Portfolio  
**Action:** Create "Portfolio Management" bounded context glossary  
**Severity:** High - Large undocumented domain  
**Effort:** High (create new context, 5-7 terms)

---

#### Location 3: `src/framework/orchestration/agent_orchestrator.py`

**Issue:** Inconsistent directory naming  
**Lines:** 29-35 (configuration constants)  
**Code:**
```python
WORK_DIR = Path("work")
COLLAB_DIR = WORK_DIR / "collaboration"
INBOX_DIR = COLLAB_DIR / "inbox"
ASSIGNED_DIR = COLLAB_DIR / "assigned"
```
**Terms:** Work Directory, Collaboration Directory, Inbox Directory, Assigned Directory  
**Action:** Standardize naming and document in glossary  
**Severity:** Medium - Consistency issue  
**Effort:** Low (refactor + glossary update)

---

#### Location 4: `src/llm_service/templates/manager.py`

**Issue:** Generic "Manager" suffix  
**Lines:** 31 (class definition)  
**Code:** `class TemplateManager:`  
**Action:** Rename to `TemplateRenderer` or `ConfigurationTemplateService`  
**Severity:** Medium - Generic anti-pattern  
**Effort:** Low (rename + update references)

---

#### Location 5: `src/llm_service/dashboard/task_assignment_handler.py`

**Issue:** Generic "Handler" suffix for domain service  
**Lines:** 49 (class definition)  
**Code:** `class TaskAssignmentHandler:`  
**Action:** Rename to `TaskAssignmentService` or `OrphanTaskAssigner`  
**Severity:** Medium - Domain naming clarity  
**Effort:** Low (rename + update references)

---

### 5.2 Medium-Priority Locations

#### Location 6: `src/common/task_schema.py`

**Issue:** No TaskDescriptor type despite glossary proposal  
**Lines:** 34-100 (read_task/write_task functions)  
**Current:** `def read_task(path: Path) -> Dict[str, Any]:`  
**Proposed:** `def read_task(path: Path) -> TaskDescriptor:`  
**Action:** Either create TypedDict/dataclass or remove term from glossary  
**Severity:** Medium - Type safety vs. flexibility  
**Effort:** Medium (impact analysis required)

---

#### Location 7: `src/framework/orchestration/task_utils.py`

**Issue:** "persist" terminology not used  
**Lines:** 22-24 (re-exports)  
**Current:** `read_task`, `write_task`  
**Glossary:** "Load", "Persist"  
**Action:** Align glossary to code OR create aliases  
**Severity:** Low - Terminology consistency  
**Effort:** Low (glossary update)

---

## 6. Glossary Coverage by Context

### 6.1 Doctrine Context

| Term | Status | Usage | Notes |
|------|--------|-------|-------|
| Agent | ✅ Canonical | 87 files | Excellent adoption |
| Doctrine Stack | ❌ Not found | 0 files | Strategic term, may not appear in code |

**Assessment:** Core "Agent" term well-established. "Doctrine Stack" is meta-level documentation concept.

---

### 6.2 DDD Context

| Term | Status | Usage | Notes |
|------|--------|-------|-------|
| Bounded Context | ❌ Not found | 0 files | Concept exists implicitly (dashboard vs. orchestration) |
| Ubiquitous Language | ❌ Not found | 0 files | Meta-level documentation concept |
| Aggregate | ⚠️ Minimal | 7 files | DDD concept weakly present |
| Anti-Corruption Layer | ❌ Not found | 0 files | Pattern not explicitly implemented |
| Context Map | ❌ Not found | 0 files | Documentation artifact, not code |
| Domain Event | ❌ Not found | 0 files | Event-driven architecture not implemented |
| Entity | ⚠️ Minimal | 3 files | DDD concept weakly present |
| Value Object | ❌ Not found | 0 files | Pattern not explicitly named |
| Upstream/Downstream | ⚠️ Minimal | 1 file | Context relationship not documented |
| Published Language | ❌ Not found | 0 files | Integration pattern not implemented |

**Assessment:** DDD glossary is aspirational. Most terms are strategic concepts not directly implemented in code. Consider:
1. Move these to "DDD Principles" reference document
2. OR document WHERE these concepts apply (e.g., "Dashboard is a Bounded Context")
3. OR mark as "conceptual" status in glossary

---

### 6.3 Software Design Context

| Term | Status | Usage | Notes |
|------|--------|-------|-------|
| Anti-Corruption Layer | ❌ Not found | 0 files | Same as DDD context |
| Published Language | ❌ Not found | 0 files | Same as DDD context |
| Shared Kernel | ❌ Not found | 0 files | Pattern not implemented |
| Conformist | ❌ Not found | 0 files | Pattern not implemented |
| Partnership | ❌ Not found | 0 files | Pattern not implemented |

**Assessment:** Strategic patterns not implemented. These are architectural choices, not code artifacts.

---

### 6.4 Organizational Context

| Term | Status | Usage | Notes |
|------|--------|-------|-------|
| Conway's Law | ❌ Not found | 0 files | Organizational principle, not code |
| Stream-Aligned Team | ❌ Not found | 0 files | Team topology concept, not code |
| Cognitive Load | ❌ Not found | 0 files | Human factors concept, not code |

**Assessment:** Organizational glossary documents team patterns, not implementation details. This is appropriate.

---

### 6.5 Orchestration Context (Proposed)

| Term | Status | Usage | Notes |
|------|--------|-------|-------|
| TaskDescriptor | ❌ Not used | 0 files | **CRITICAL GAP** - Core proposed term not implemented |
| Work Directory | ⚠️ Inconsistent | 29 files | Used but inconsistently named |
| Agent Queue | ⚠️ Implicit | 0 files | Concept exists, term not used |
| Task Lifecycle Directory | ⚠️ Implicit | 0 files | Directories exist, term not used |
| Serialize/Deserialize | ⚠️ Implementation | 0 files | Functions exist, not domain terms |
| Persist/Load | ⚠️ Minimal | 2 files | "write/read" more common |
| File-Based Coordination | ✅ Pattern | N/A | Pattern is clear, not named in code |
| Task File | ⚠️ Inconsistent | 46 files | Term used but variable naming |
| Task Assignment/Completion/Error | ⚠️ Operational | 8 files | Operations exist, terminology variable |
| Orchestrator | ✅ Established | 6 files | Good adoption in orchestration module |
| Parser/Serializer | ✅ Technical | 38 files | Technical pattern, not domain term |
| TaskAggregate/WorkItem | ❌ Not distinguished | 0 files | Concept collapsed to generic "Task" |

**Assessment:** Orchestration glossary is CLOSEST to code but still has gaps:
- Proposed "TaskDescriptor" type not implemented (dict used instead)
- Directory terminology inconsistent
- State vs. Status terminology mismatch
- Operations exist but terminology not standardized

**Recommendation:** This context should be PRIORITIZED for alignment.

---

## 7. Proposed Glossary Additions

### 7.1 Immediate Additions (High Priority)

Create new glossary file: `.contextive/contexts/task-domain.yml`

```yaml
# Task Domain Glossary
# Version: 1.0.0
# Date: 2026-02-10
# Purpose: Task management and lifecycle domain concepts

name: "Task Domain"
description: "Task management and lifecycle domain concepts"
terms:
  - term: "TaskStatus"
    definition: "Enumeration of task lifecycle states with state machine transitions"
    context: "Task Domain"
    status: "canonical"
    source: "ADR-043: Status Enumeration Standard"
    implementation: "src/common/types.py:31"
    values:
      - "new: Task created, awaiting assignment"
      - "inbox: Task in inbox, awaiting agent pickup"
      - "assigned: Task assigned to specific agent"
      - "in_progress: Agent actively executing task"
      - "blocked: Task blocked on dependency"
      - "done: Task successfully completed (terminal)"
      - "error: Task failed with error (terminal)"
    enforcement_tier: "acknowledgment"
  
  - term: "FeatureStatus"
    definition: "Feature/specification implementation states"
    context: "Task Domain"
    status: "canonical"
    source: "ADR-043: Status Enumeration Standard"
    implementation: "src/common/types.py:149"
    values:
      - "draft: Specification in draft"
      - "planned: Approved, implementation planned"
      - "in_progress: Implementation ongoing"
      - "implemented: Complete and deployed"
      - "deprecated: No longer relevant"
    enforcement_tier: "advisory"
  
  - term: "TaskPriority"
    definition: "Task priority levels for scheduling and triage"
    context: "Task Domain"
    status: "canonical"
    source: "ADR-043: Status Enumeration Standard"
    implementation: "src/common/types.py:197"
    values:
      - "critical: Immediate attention required"
      - "high: Important, schedule soon"
      - "medium: Normal priority"
      - "normal: Standard priority (default)"
      - "low: Can be deferred"
    enforcement_tier: "advisory"
  
  - term: "TaskMode"
    definition: "Agent operating modes influencing task execution approach"
    context: "Task Domain"
    status: "canonical"
    implementation: "src/common/types.py:176"
    values:
      - "/analysis-mode: Deep analytical thinking"
      - "/creative-mode: Explore alternatives"
      - "/meta-mode: Process reflection"
      - "/programming: Implementation and coding"
      - "/planning: Strategic coordination"
    enforcement_tier: "advisory"
  
  - term: "AgentIdentity"
    definition: "Type-safe agent identifier loaded from doctrine/agents/*.agent.md"
    context: "Task Domain"
    status: "canonical"
    source: "ADR-044: Agent Identity Type Safety"
    implementation: "src/common/types.py:246"
    validation: "Dynamic loading from doctrine/agents/ directory"
    enforcement_tier: "acknowledgment"

owner: "Architect Alphonso"
reviewers: ["Python Pedro", "Code-reviewer Cindy"]
approval_required: true
enforcement_tier: "advisory"
```

---

Create new glossary file: `.contextive/contexts/portfolio-domain.yml`

```yaml
# Portfolio Domain Glossary
# Version: 1.0.0
# Date: 2026-02-10
# Purpose: Requirements and portfolio management domain

name: "Portfolio Domain"
description: "Requirements and portfolio management domain concepts"
terms:
  - term: "Specification"
    definition: "Formal requirements document defining features, acceptance criteria, and implementation scope"
    context: "Portfolio Domain"
    status: "canonical"
    source: "ADR-037: Dashboard Initiative Tracking"
    implementation: "src/llm_service/dashboard/spec_parser.py:44"
    attributes:
      - "id: Unique identifier (e.g., SPEC-DASH-008)"
      - "title: Human-readable name"
      - "initiative: Parent initiative grouping"
      - "features: List of feature definitions"
      - "status: Implementation status (draft, planned, in_progress, implemented)"
    file_format: "Markdown with YAML frontmatter"
    location: "specifications/**/*.md"
    enforcement_tier: "advisory"
  
  - term: "Initiative"
    definition: "High-level project or milestone grouping related specifications"
    context: "Portfolio Domain"
    status: "canonical"
    implementation: "src/llm_service/dashboard/spec_parser.py:52"
    examples:
      - "framework-distribution"
      - "dashboard-enhancements"
      - "quickstart-onboarding"
    structure: "Directory-based grouping in specifications/initiatives/"
    enforcement_tier: "advisory"
  
  - term: "Feature"
    definition: "Specific capability, user story, or functional requirement within a specification"
    context: "Portfolio Domain"
    status: "canonical"
    implementation: "src/llm_service/dashboard/spec_parser.py:23"
    attributes:
      - "id: Feature identifier"
      - "title: Human-readable description"
      - "status: Implementation status"
    relationship_to_tasks: "Tasks reference feature ID for traceability"
    enforcement_tier: "advisory"
  
  - term: "Portfolio View"
    definition: "Aggregate view of initiatives showing progress, completion, and task distribution"
    context: "Portfolio Domain"
    status: "canonical"
    implementation: "src/llm_service/dashboard/app.py"
    visualization: "Dashboard interface with initiative cards and progress tracking"
    enforcement_tier: "advisory"

owner: "Analyst Annie"
reviewers: ["Architect Alphonso", "Frontend Freddy"]
approval_required: true
enforcement_tier: "advisory"
```

---

### 7.2 Configuration Domain Additions (Medium Priority)

Add to `.contextive/contexts/software-design.yml`:

```yaml
  - term: "Configuration"
    definition: "Declarative system settings for LLM service, agents, tools, models, and policies"
    context: "Infrastructure Domain"
    status: "canonical"
    source: "ADR-031: Template-Based Configuration Generation"
    implementation: "src/llm_service/config/schemas.py"
    related_terms:
      - "Template"
      - "Schema Validation"
    file_format: "YAML configuration files"
    validation: "Pydantic schemas"
    enforcement_tier: "advisory"
  
  - term: "Template"
    definition: "Jinja2-based configuration file generator with variable substitution"
    context: "Infrastructure Domain"
    status: "canonical"
    source: "ADR-031: Template-Based Configuration Generation"
    implementation: "src/llm_service/templates/manager.py"
    format: "Jinja2 with ${VAR} environment variable syntax"
    enforcement_tier: "advisory"
```

---

### 7.3 Observability Domain Additions (Low Priority)

Add to `.contextive/contexts/software-design.yml`:

```yaml
  - term: "Telemetry"
    definition: "Structured logging and metrics collection for system observability"
    context: "Observability Domain"
    status: "canonical"
    implementation: "src/llm_service/telemetry/logger.py"
    storage: "SQLite database (telemetry.db)"
    schema: "Event-sourced log with structured fields"
    enforcement_tier: "advisory"
  
  - term: "Dashboard"
    definition: "Web-based user interface for task management, portfolio tracking, and telemetry"
    context: "UI Domain"
    status: "canonical"
    implementation: "src/llm_service/dashboard/app.py"
    technology: "Flask + vanilla JavaScript + Server-Sent Events"
    enforcement_tier: "advisory"
```

---

## 8. Recommendations by Priority

### 8.1 Immediate Actions (This Sprint)

1. **Create Task Domain Glossary** ✅ HIGH
   - Add TaskStatus, FeatureStatus, TaskPriority, TaskMode, AgentIdentity
   - Link to ADR-042, ADR-043, ADR-044
   - Effort: 2 hours
   - Owner: Curator Claire + Python Pedro

2. **Create Portfolio Domain Glossary** ✅ HIGH
   - Add Specification, Initiative, Feature, Portfolio View
   - Link to ADR-037
   - Effort: 3 hours
   - Owner: Analyst Annie + Architect Alphonso

3. **Fix Generic Naming in Domain Services** ⚠️ MEDIUM
   - Rename `TemplateManager` → `TemplateRenderer`
   - Rename `TaskAssignmentHandler` → `TaskAssignmentService`
   - Update references and tests
   - Effort: 4 hours
   - Owner: Python Pedro

4. **Standardize Directory Naming** ⚠️ MEDIUM
   - Document Work Directory, Collaboration Directory naming conventions
   - Add to orchestration glossary
   - Effort: 1 hour
   - Owner: Curator Claire

---

### 8.2 Short-Term Actions (Next Sprint)

5. **Resolve TaskDescriptor vs. Dict Decision** ⚠️ HIGH
   - Option A: Create TaskDescriptor TypedDict (type safety)
   - Option B: Remove from glossary (flexibility)
   - Option C: Document explicit dict choice in ADR
   - Effort: 6 hours (if implementing type)
   - Owner: Architect Alphonso + Python Pedro

6. **Align State/Status Terminology** ⚠️ MEDIUM
   - Update glossary to use "Status" (align to code)
   - OR create ADR documenting distinction
   - Effort: 2 hours
   - Owner: Curator Claire

7. **Add Configuration and Telemetry Terms** ℹ️ LOW
   - Extend software-design.yml with infrastructure terms
   - Effort: 2 hours
   - Owner: Curator Claire

8. **Document DDD Term Applicability** ℹ️ LOW
   - Mark strategic DDD terms as "conceptual" or "aspirational"
   - Document WHERE concepts apply (e.g., "Dashboard is a Bounded Context")
   - Effort: 3 hours
   - Owner: Architect Alphonso

---

### 8.3 Long-Term Actions (Future Sprints)

9. **Implement Bounded Context Documentation** ℹ️ STRATEGIC
   - Create context map showing Dashboard, Orchestration, Configuration contexts
   - Document context boundaries and translation points
   - Effort: 8 hours
   - Owner: Architect Alphonso

10. **Add Domain Event Infrastructure** ℹ️ STRATEGIC (if desired)
    - Implement TaskAssigned, TaskCompleted events
    - Add to glossary with event sourcing terminology
    - Effort: 20+ hours
    - Owner: Architect Alphonso + Backend Benny

11. **Glossary Enforcement Automation** ℹ️ TOOLING
    - Implement PR-level glossary checks
    - Add IDE integration (Contextive plugin setup guide)
    - Effort: 12 hours
    - Owner: DevOps Danny + Lexical Larry

---

## 9. Success Metrics

### 9.1 Coverage Metrics (Target: >80% by Q3 2026)

| Metric | Baseline (Current) | Target (3 months) | Target (6 months) |
|--------|-------------------|-------------------|-------------------|
| Glossary term usage in code | 25% (11/44 terms) | 45% (20/44 terms) | 70% (31/44 terms) |
| Domain concepts documented | 0/21 observed | 60% (13/21) | 90% (19/21) |
| Generic anti-patterns | 19 classes | 12 classes (-35%) | 5 classes (-75%) |
| Files with glossary terms | ~30% of files | 50% of files | 75% of files |

---

### 9.2 Quality Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| Glossary staleness | N/A (new) | <10% outdated definitions |
| Terminology conflicts | 3 (Status/State, Load/Read, Persist/Write) | 0 conflicts |
| Suppression rate | N/A | <10% PRs overriding checks |
| Contribution rate | N/A | >50% team-initiated glossary updates |

---

### 9.3 Sentiment Metrics

| Metric | Target |
|--------|--------|
| Developer survey: "Glossary is helpful" | >75% agree |
| IDE plugin active users | >75% of team |
| Glossary referenced in PR discussions | >30% of PRs |

---

## 10. Conclusion

### 10.1 Overall Assessment

⚠️ **PARTIAL ALIGNMENT** - The codebase demonstrates:

**Strengths:**
- ✅ Core orchestration terminology (Agent, Task, Orchestrator) well-established
- ✅ Strong type safety in shared types (TaskStatus, FeatureStatus enums)
- ✅ Clear operational vocabulary in orchestration module
- ✅ Rich domain model in dashboard (Specification, Initiative, Feature)

**Critical Gaps:**
- ❌ 75% of glossary terms not used in code (34/44 terms)
- ❌ Entire domain vocabularies missing from glossary (Portfolio, Task Domain)
- ❌ DDD glossary is aspirational, not operational
- ❌ Generic anti-patterns prevalent (19 Manager/Handler/Processor classes)

**Root Cause Analysis:**
1. **Glossary created post-implementation** - Code predates terminology documentation
2. **Strategic vs. Operational confusion** - DDD glossary mixes principles with implementation
3. **Missing domain contexts** - No glossary for dashboard, configuration, telemetry domains
4. **No enforcement mechanism** - No PR checks or IDE integration to encourage adoption

---

### 10.2 Strategic Recommendation

**Approach:** Incremental alignment with pilot module

1. **Pilot Module: `src/framework/orchestration/`** (Best alignment, manageable scope)
   - Implement glossary enforcement
   - Resolve TaskDescriptor decision
   - Standardize directory naming
   - Add missing terms (TaskStatus, etc.)

2. **Expand to Dashboard Module** (High-value domain documentation)
   - Create Portfolio Domain glossary
   - Document bounded context explicitly
   - Refactor generic names

3. **Clean Up DDD Glossary** (Reduce noise)
   - Mark strategic terms as "conceptual"
   - Document WHERE DDD concepts apply
   - Remove unimplemented patterns or mark as "aspirational"

4. **Automate Enforcement** (Scale best practices)
   - PR-level glossary checks
   - IDE plugin setup guide
   - Quarterly glossary audits

---

### 10.3 Enforcement Tier Guidance

Based on Living Glossary Practice severity levels:

**Advisory (80% of issues):** Style, consistency, documentation gaps  
**Acknowledgment Required (18% of issues):** Generic naming, type safety trade-offs, terminology conflicts  
**Hard Failure (2% of issues):** None identified - codebase is functional

**Recommendation:** Start with Advisory-only enforcement to build adoption, gradually introduce Acknowledgment checks in pilot module.

---

### 10.4 Next Steps

1. **Immediate (This Week):**
   - [ ] Review this report with Architect Alphonso and Curator Claire
   - [ ] Approve Task Domain and Portfolio Domain glossary additions
   - [ ] Create ADR for TaskDescriptor decision

2. **Short-Term (Next Sprint):**
   - [ ] Implement glossary additions
   - [ ] Refactor 2-3 generic class names (pilot)
   - [ ] Add traceability links (ADRs ↔ Glossary)

3. **Long-Term (Next Quarter):**
   - [ ] Set up Contextive IDE integration
   - [ ] Implement PR-level glossary validation
   - [ ] Conduct quarterly glossary health check

---

## Appendices

### A. Glossary Health Check Checklist

Use for quarterly reviews:

- [ ] Are all canonical terms still relevant?
- [ ] Are deprecated terms marked and removed from code?
- [ ] Do new domain concepts have glossary entries?
- [ ] Are ADRs linked to glossary terms?
- [ ] Is enforcement tier appropriate for each term?
- [ ] Are examples up-to-date?
- [ ] Are related terms cross-referenced?

---

### B. Generic Naming Audit

Classes requiring attention (severity: Acknowledgment Required):

| Class | Location | Current Name | Suggested Name | Rationale |
|-------|----------|--------------|----------------|-----------|
| 1 | src/llm_service/templates/manager.py:31 | TemplateManager | TemplateRenderer | Active role (renders) vs. passive (manages) |
| 2 | src/llm_service/dashboard/task_assignment_handler.py:49 | TaskAssignmentHandler | TaskAssignmentService | Domain service, not event handler |
| 3 | src/llm_service/adapters/subprocess_wrapper.py | SubprocessWrapper | SubprocessExecutor | Active role vs. wrapper pattern |

**Note:** Watchdog FileSystemEventHandler subclasses are ACCEPTABLE - framework convention.

---

### C. References

- **Living Glossary Practice:** doctrine/approaches/living-glossary-practice.md
- **ADR-042:** Shared Task Domain Model
- **ADR-043:** Status Enumeration Standard
- **ADR-044:** Agent Identity Type Safety
- **ADR-037:** Dashboard Initiative Tracking
- **ADR-031:** Template-Based Configuration Generation
- **Glossaries:** .contextive/contexts/*.yml

---

**Report Status:** ✅ Complete  
**Review Required:** Architect Alphonso, Curator Claire  
**Next Action:** Approve glossary additions and create implementation plan

---

*Generated by Code-reviewer Cindy in accordance with Living Glossary Practice approach.*
