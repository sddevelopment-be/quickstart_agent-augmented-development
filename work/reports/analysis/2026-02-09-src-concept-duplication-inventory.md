# Source Code Concept Duplication Inventory

**Analysis Date:** 2026-02-09  
**Analyst:** Python Pedro  
**Scope:** src/framework/ and src/llm_service/  
**Task ID:** 2026-02-08T0328-review-src-duplicates

---

## Executive Summary

This analysis identifies duplicate and inconsistent representations of core concepts across the `src/framework/orchestration/` and `src/llm_service/` modules. The codebase exhibits **conceptual duplication** in several key abstractions:

- **Task representation:** YAML-based dict manipulation vs. potential dataclass opportunities
- **Agent representation:** Orchestration base classes vs. LLM config schemas
- **Status tracking:** String-based status values without enum enforcement
- **Configuration:** Overlapping config concerns between orchestration and LLM service

**Key Finding:** While there is good separation of concerns at the module level, there are opportunities to consolidate shared abstractions into a common domain model that both modules can reference.

**Risk Level:** ⚠️ MEDIUM - Current duplication is manageable but will increase technical debt as codebase grows.

---

## 1. Concept Map

### 1.1 Task Concept

#### Framework Orchestration Representation
- **Location:** `src/framework/orchestration/`
- **Primary Implementation:** Dict-based YAML manipulation
- **Files:**
  - `task_utils.py` - Utility functions for task file operations
  - `agent_base.py` - Task processing lifecycle (lines 77-81, 94-96)
  - `agent_orchestrator.py` - Task assignment and coordination
  - `task_age_checker.py` - Task aging checks

**Representation:**
```python
# Dict-based, loaded from YAML
task = {
    "id": str,
    "agent": str,
    "status": str,  # "assigned", "in_progress", "done", "error"
    "title": str,
    "artefacts": List[str],
    "context": dict,
    "priority": str,
    "created_at": str,
    "assigned_at": str,
    "started_at": str,
    "completed_at": str,
    "result": dict,
    "error": dict,
}
```

**Operations:**
- `read_task(path)` → dict
- `write_task(path, dict)` → None
- `update_task_status(dict, status, timestamp_field)` → dict

#### LLM Service Representation
- **Location:** `src/llm_service/dashboard/`
- **Primary Implementation:** Dict-based from YAML scanning
- **Files:**
  - `task_linker.py` - Task-to-specification linking
  - `task_priority_updater.py` - Priority management
  - `file_watcher.py` - Real-time task file monitoring

**Representation:**
```python
# Dict-based, same YAML structure
task = {
    "id": str,
    "status": str,
    "specification": str,  # Additional field for spec linking
    "feature": str,  # Additional field for feature linking
    "_path": str,  # Runtime annotation
    # ... same core fields as orchestration
}
```

**Operations:**
- `load_task(path)` → Optional[Dict]
- `scan_tasks()` → List[Dict]
- `group_by_specification()` → Dict[str, List[Dict]]
- `get_task_count_by_status(tasks)` → Dict[str, int]

#### Duplication Analysis

| Aspect | Framework | LLM Service | Duplication Level |
|--------|-----------|-------------|-------------------|
| **Core Structure** | ✅ Dict from YAML | ✅ Dict from YAML | **HIGH** - Identical |
| **Status Values** | Strings | Strings | **HIGH** - Same strings |
| **File I/O** | `task_utils.read/write_task` | `task_linker.load_task` | **MEDIUM** - Similar logic |
| **Status Transitions** | `agent_base.update_task_status` | Implicit in file_watcher | **LOW** - Different concerns |
| **Validation** | Runtime checks | YAML parse only | **LOW** - Different levels |

**Inconsistency:** 
- LLM Service adds `specification` and `feature` fields not validated by orchestration
- Two separate file loading implementations with different error handling
- No shared Task domain model or schema validation

---

### 1.2 Agent Concept

#### Framework Orchestration Representation
- **Location:** `src/framework/orchestration/agent_base.py`
- **Abstraction:** ABC for file-based orchestration agents
- **Purpose:** Runtime agent behavior and task execution

**Representation:**
```python
class AgentBase(ABC):
    """Abstract base for orchestration agents"""
    agent_name: str
    work_dir: Path
    mode: str  # "/analysis-mode", etc.
    
    # Lifecycle hooks
    def validate_task(task: dict) -> bool
    def execute_task(task: dict) -> dict
    def init_task(task: dict) -> None
    def finalize_task(success: bool) -> None
    
    # Task operations
    def find_assigned_tasks() -> List[Path]
    def update_task_status(status: str) -> None
    def create_result_block(...) -> dict
    def create_work_log(...) -> Path
```

**Key Characteristics:**
- Stateful (tracks current_task, start_time, artifacts)
- File-system oriented (reads from assigned/, moves to done/)
- Lifecycle-focused (init → validate → execute → finalize)
- Work log generation built-in

#### LLM Service Representation
- **Location:** `src/llm_service/config/schemas.py`
- **Abstraction:** Pydantic model for agent configuration
- **Purpose:** Agent preferences and routing configuration

**Representation:**
```python
class AgentConfig(BaseModel):
    """Configuration for a single agent"""
    preferred_tool: str
    preferred_model: str
    fallback_chain: List[str]
    task_types: Dict[str, str]  # Task type → model mapping
    
    @field_validator('fallback_chain')
    def validate_fallback_format(cls, v) -> List[str]

class AgentsSchema(BaseModel):
    """Root schema for agents.yaml"""
    agents: Dict[str, AgentConfig]
```

**Key Characteristics:**
- Stateless (pure configuration)
- Routing-focused (tool/model selection)
- Validation via Pydantic
- No execution or lifecycle concerns

#### Duplication Analysis

| Aspect | Framework | LLM Service | Duplication Level |
|--------|-----------|-------------|-------------------|
| **Purpose** | Runtime execution | Configuration only | **NONE** - Different concerns |
| **State** | Stateful (current task) | Stateless (config) | **NONE** |
| **Naming** | `agent_name` attribute | Key in `agents` dict | **LOW** - Semantic overlap |
| **Identity** | Directory name in assigned/ | YAML key in agents.yaml | **MEDIUM** - Same identifier |
| **Capabilities** | execute_task, validate_task | preferred_tool/model | **LOW** - Different dimensions |

**Inconsistency:**
- No guarantee that `AgentBase.agent_name` matches key in `agents.yaml`
- Agent execution classes don't reference their LLM config
- `AgentConfig.task_types` is conceptually similar to task routing but disconnected from orchestration task statuses

**Opportunity:** Bridge between runtime agent instances and their LLM configuration profiles.

---

### 1.3 Status Tracking

#### String-Based Status Values

**Framework Orchestration:**
```python
# From agent_base.py, agent_orchestrator.py
"assigned"      # Task in agent's queue
"in_progress"   # Agent actively working
"done"          # Completed successfully
"error"         # Failed with error block
```

**LLM Service Dashboard:**
```python
# From file_watcher.py, progress_calculator.py, spec_parser.py
"new"           # Newly created (inbox)
"assigned"      # Same as orchestration
"in_progress"   # Same as orchestration
"done"          # Same as orchestration
"blocked"       # Waiting on dependency
"inbox"         # Waiting for assignment
"failed"        # Same as error?
"implemented"   # Specification-level status
"draft"         # Specification-level status
"planned"       # Specification-level status
"deprecated"    # Specification-level status
```

#### Duplication Analysis

| Aspect | Framework | LLM Service | Duplication Level |
|--------|-----------|-------------|-------------------|
| **Type Safety** | Strings (no validation) | Strings (no validation) | **HIGH** - Same weakness |
| **Core Statuses** | assigned/in_progress/done/error | Same + additional | **MEDIUM** - Partial overlap |
| **Enum Definition** | ❌ None | ❌ None | **HIGH** - Both missing |
| **Validation** | Runtime string checks | Literal type hints (schemas) | **LOW** - Different approaches |
| **Status Weights** | N/A | `ProgressCalculator.DEFAULT_STATUS_WEIGHTS` | **LOW** - Dashboard-specific |

**Inconsistencies:**
- Task statuses: `"error"` vs. `"failed"` - are these the same?
- Specification statuses: `"implemented"`, `"draft"`, `"planned"`, `"deprecated"` - completely separate concept
- No shared enum or type definition for valid status values
- Progress weights hardcoded in `ProgressCalculator` (dashboard-specific interpretation)

**Risk:** Typos like `"done"` vs. `"Done"` won't be caught until runtime.

---

### 1.4 Configuration Objects

#### Framework Orchestration Config
- **Hardcoded values** in `agent_orchestrator.py`:
  - `TIMEOUT_HOURS = 2`
  - `ARCHIVE_RETENTION_DAYS = 30`
- **No centralized config file** for orchestration behavior
- **Agent-specific config** passed to `AgentBase.__init__`:
  ```python
  def __init__(self, agent_name: str, work_dir: Path, mode: str, log_level: str)
  ```

#### LLM Service Config
- **Location:** `src/llm_service/config/`
- **Pydantic Schemas:**
  - `AgentsSchema` - Agent preferences (agents.yaml)
  - `ToolsSchema` - Tool configurations (tools.yaml)
  - `ModelsSchema` - Model metadata (models.yaml)
  - `PoliciesSchema` - Cost policies (policies.yaml)
  - `TelemetryConfig` - Telemetry settings
- **Loader:** `ConfigurationLoader` in `loader.py`

#### Duplication Analysis

| Aspect | Framework | LLM Service | Duplication Level |
|--------|-----------|-------------|-------------------|
| **Config File Format** | ❌ None (hardcoded) | ✅ YAML + Pydantic | **NONE** - Different approach |
| **Agent Config** | Constructor params | `AgentConfig` in agents.yaml | **MEDIUM** - Overlapping concern |
| **Validation** | Runtime checks | Pydantic validators | **NONE** - Different mechanisms |
| **Work Directory** | Hardcoded "work" | N/A | **LOW** |
| **Telemetry** | N/A | `TelemetryConfig` | **NONE** |

**Inconsistency:**
- Orchestration has no config file convention
- Agent execution mode (`"/analysis-mode"`) in `AgentBase` disconnected from LLM config
- No shared config schema for framework-wide settings

---

### 1.5 Feature & Specification Abstractions

#### LLM Service Representation Only
- **Location:** `src/llm_service/dashboard/spec_parser.py`
- **Dataclasses:**
  ```python
  @dataclass
  class Feature:
      id: str
      title: str
      status: Optional[str] = None
      
  @dataclass
  class SpecificationMetadata:
      id: str
      title: str
      status: str
      initiative: str
      priority: str
      features: List[Feature]
      completion: Optional[int]
      path: str
      # ... more fields
  ```

**Key Points:**
- Dashboard-specific abstractions for portfolio view (ADR-037)
- No corresponding representation in framework/orchestration
- Tasks link to specs via `specification` field (string path)
- Feature progress calculated from task statuses

**Duplication:** ❌ None - These concepts don't exist in orchestration layer.

**Gap:** Orchestration tasks reference specification paths but don't have a validated model for specifications.

---

### 1.6 Model & Tool Abstractions

#### LLM Service Representation Only
- **Location:** `src/llm_service/adapters/base.py`, `routing.py`
- **Dataclasses & Models:**
  ```python
  @dataclass
  class ToolResponse:
      status: str  # "success" or "error"
      output: str
      tool_name: str
      exit_code: Optional[int]
      metadata: Optional[Dict]
      # ...
      
  @dataclass
  class RoutingDecision:
      tool_name: str
      model_name: str
      reason: str
      fallback_used: bool
      # ...
      
  class ToolAdapter(ABC):
      def execute(prompt, model) -> ToolResponse
      def validate_config(config) -> bool
  ```

**Key Points:**
- LLM routing and execution abstraction (ADR-029)
- No corresponding representation in orchestration
- `ToolResponse.status` is similar to task status but different domain

**Duplication:** ❌ None - Tool/model routing is LLM-specific.

**Gap:** No connection between orchestration task execution results and LLM tool responses.

---

## 2. Duplication Summary

### High-Priority Duplications

#### 2.1 Task File I/O ⚠️
**Files:**
- `src/framework/orchestration/task_utils.py:18-28` - `read_task()`
- `src/llm_service/dashboard/task_linker.py:43-71` - `load_task()`

**Issue:** Both implement YAML task loading with different error handling strategies.

**Impact:** 
- Code maintenance (two places to update)
- Inconsistent error handling (framework raises, dashboard returns None)
- No shared validation

**Recommendation:** Extract to `src/common/task_io.py` with unified error handling.

---

#### 2.2 Status String Values ⚠️
**Files:**
- `src/framework/orchestration/agent_base.py` - Hardcoded status strings
- `src/framework/orchestration/agent_orchestrator.py` - More status strings
- `src/llm_service/dashboard/file_watcher.py` - Status string matching
- `src/llm_service/dashboard/progress_calculator.py` - Status weight mapping

**Issue:** No shared enum or constants for valid status values.

**Impact:**
- Typos not caught until runtime
- Difficult to discover all valid statuses
- Status semantics unclear ("error" vs "failed")

**Recommendation:** Create `src/common/types.py` with:
```python
from enum import Enum

class TaskStatus(str, Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ERROR = "error"
    BLOCKED = "blocked"

class SpecificationStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    DEPRECATED = "deprecated"
```

---

#### 2.3 Agent Identity ⚠️
**Files:**
- `src/framework/orchestration/agent_base.py:42` - `agent_name` parameter
- `src/llm_service/config/schemas.py:44-46` - Keys in `agents` dict

**Issue:** Agent name used as identifier in both places but no validation that they match.

**Impact:**
- Orchestration agent could run with name not in agents.yaml
- Config changes don't automatically update running agents
- No type-safe agent reference

**Recommendation:** Create `AgentIdentity` value object or use NewType for type safety.

---

### Medium-Priority Duplications

#### 2.4 Configuration Patterns
**Files:**
- `src/framework/orchestration/agent_base.py:41-60` - Constructor config
- `src/llm_service/config/schemas.py` - YAML-based config

**Issue:** Inconsistent config approaches (constructor params vs YAML files).

**Impact:**
- Orchestration hardcodes work_dir, mode
- No easy way to change orchestration settings without code changes
- LLM config well-structured but orchestration ad-hoc

**Recommendation:** Create `framework.yaml` config file with Pydantic schema for orchestration settings.

---

#### 2.5 Timestamp Handling
**Files:**
- `src/framework/orchestration/task_utils.py:57-63` - `get_utc_timestamp()`
- Multiple files with inline `datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")`

**Issue:** Timestamp formatting duplicated across multiple files.

**Impact:**
- Inconsistent timestamp format potential
- Repeated code

**Recommendation:** Centralize in `task_utils.py` and import everywhere.

---

### Low-Priority Observations

#### 2.6 Result Block Structure
**Files:**
- `src/framework/orchestration/agent_base.py:151-189` - `create_result_block()`

**Issue:** Result block structure is defined implicitly in method.

**Impact:** Low - Single source of truth exists.

**Recommendation:** Consider TypedDict or Pydantic model for result blocks in future.

---

#### 2.7 Path Handling
**Files:**
- Multiple files use `Path` operations for work directory structure

**Issue:** Directory structure (`work/collaboration/assigned/`) is knowledge spread across files.

**Impact:** Low - Filesystem conventions are relatively stable.

**Recommendation:** Consider constants file with directory structure, or config-driven paths.

---

## 3. Consolidation Recommendations

### 3.1 Immediate Actions (Sprint 1)

#### ✅ Create `src/common/types.py`
```python
"""Shared domain types for orchestration and LLM service."""
from enum import Enum
from typing import NewType

# Agent identity
AgentName = NewType('AgentName', str)

# Task statuses
class TaskStatus(str, Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ERROR = "error"
    BLOCKED = "blocked"

# Specification statuses (separate domain)
class SpecificationStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    DEPRECATED = "deprecated"
```

**Effort:** 2 hours  
**Risk:** Low  
**Impact:** High (prevents future bugs)

---

#### ✅ Create `src/common/task_schema.py`
```python
"""Shared task schema and I/O operations."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import yaml

@dataclass
class TaskMetadata:
    """Core task metadata."""
    id: str
    agent: str
    status: TaskStatus
    title: str
    created_at: str
    # ... other fields

def read_task(path: Path) -> Dict[str, Any]:
    """Unified task reading with validation."""
    # Implementation

def write_task(path: Path, task: Dict[str, Any]) -> None:
    """Unified task writing with validation."""
    # Implementation
```

**Effort:** 4 hours  
**Risk:** Medium (changes in both modules)  
**Impact:** High (single source of truth)

---

### 3.2 Short-Term Actions (Sprint 2)

#### ✅ Refactor Status Checks
- Replace all status string literals with `TaskStatus` enum
- Update `ProgressCalculator` to use enum
- Add type hints for status parameters

**Effort:** 6 hours  
**Risk:** Medium (thorough testing required)  
**Impact:** High (type safety)

---

#### ✅ Create `framework.yaml` Config
- Extract orchestration settings from hardcoded values
- Create Pydantic schema for orchestration config
- Update `AgentBase` to read from config

**Effort:** 4 hours  
**Risk:** Low  
**Impact:** Medium (consistency)

---

### 3.3 Long-Term Actions (Sprint 3+)

#### ✅ Task Domain Model
- Create Pydantic models for Task, Result, Error blocks
- Validate task YAML against schema on load
- Generate TypeScript types for dashboard consumption

**Effort:** 12 hours  
**Risk:** High (breaking changes possible)  
**Impact:** Very High (end-to-end type safety)

---

#### ✅ Agent Registry
- Create `AgentRegistry` to validate orchestration agents match config
- Bridge `AgentBase` runtime instances with `AgentConfig`
- Validate agent directory names against agents.yaml

**Effort:** 8 hours  
**Risk:** Medium  
**Impact:** High (consistency)

---

## 4. Testing Strategy

### Validation Requirements

For each consolidation:

1. **Unit Tests:** New shared modules must have ≥90% coverage
2. **Integration Tests:** Verify both framework and llm_service work with shared code
3. **Regression Tests:** Existing orchestration and dashboard tests must pass
4. **Type Checking:** mypy strict mode on all shared modules

### Test-First Approach (TDD)

Following Directive 017:

1. **RED:** Write failing test for shared abstraction
2. **GREEN:** Implement minimal shared code
3. **REFACTOR:** Update framework and llm_service to use shared code
4. **VERIFY:** Ensure no behavior change

---

## 5. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking changes during refactor | Medium | High | Comprehensive test suite before starting |
| Import cycles between modules | Low | Medium | Keep shared code dependency-free |
| Performance regression | Low | Low | Benchmark task loading before/after |
| Type checking failures | Medium | Medium | Incremental adoption with `type: ignore` |
| Merge conflicts | High | Low | Coordinate with other agents |

---

## 6. Success Metrics

### Quantitative

- **Lines of duplicated code reduced:** Target 200+ lines
- **Shared constants created:** 2+ enum classes
- **Import statements added:** 15+ places using shared code
- **Type errors caught:** 5+ potential bugs prevented
- **Test coverage maintained:** ≥80% after refactor

### Qualitative

- ✅ Single source of truth for task status values
- ✅ Type-safe agent identity references
- ✅ Unified task file I/O with consistent error handling
- ✅ Pydantic validation for all YAML schemas
- ✅ Clear separation between task and specification statuses

---

## 7. ADR References

Consolidation work should reference or create:

- **ADR-029:** Adapter pattern (existing - base.py design)
- **ADR-037:** Dashboard initiative tracking (existing - spec_parser design)
- **ADR-NEW:** Shared domain model for task abstractions (to be created)
- **ADR-NEW:** Status enumeration and lifecycle (to be created)

---

## 8. Open Questions

1. **Should task YAML validation be enforced at load time?**
   - Pro: Fail fast on invalid tasks
   - Con: Existing tasks may fail validation
   
2. **Should TaskStatus enum be string-based or int-based?**
   - Current: String-based (backward compatible)
   - Alternative: Int enum with string serialization
   
3. **Should specification concepts be in shared domain or dashboard-only?**
   - Current: Dashboard-only
   - Future: Orchestration may need spec awareness

4. **Should we use Pydantic for task dicts or keep as dicts?**
   - Pro: Validation and type safety
   - Con: More complex serialization
   
---

## Appendix A: File Reference Map

### Framework Orchestration
```
src/framework/orchestration/
├── agent_base.py           # AgentBase ABC, task lifecycle
├── agent_orchestrator.py   # Coordinator logic
├── task_utils.py          # Task file I/O
├── task_age_checker.py    # Task aging logic
└── example_agent.py       # Example implementation
```

### LLM Service
```
src/llm_service/
├── config/
│   ├── schemas.py         # AgentConfig, ToolConfig, etc.
│   └── loader.py          # ConfigurationLoader
├── dashboard/
│   ├── spec_parser.py     # Feature, SpecificationMetadata
│   ├── task_linker.py     # Task-spec linking
│   ├── progress_calculator.py  # Progress tracking
│   └── file_watcher.py    # Real-time monitoring
├── adapters/
│   └── base.py           # ToolAdapter, ToolResponse
└── routing.py            # RoutingEngine, RoutingDecision
```

---

## Appendix B: Concept Duplication Heatmap

| Concept | Framework | LLM Service | Duplication Score | Priority |
|---------|-----------|-------------|-------------------|----------|
| Task I/O | ⚠️⚠️⚠️ | ⚠️⚠️⚠️ | **HIGH (3/5)** | P0 |
| Status Values | ⚠️⚠️⚠️ | ⚠️⚠️⚠️ | **HIGH (3/5)** | P0 |
| Agent Identity | ⚠️⚠️ | ⚠️⚠️ | **MEDIUM (2/5)** | P1 |
| Timestamps | ⚠️⚠️ | ⚠️⚠️ | **MEDIUM (2/5)** | P1 |
| Config Pattern | ⚠️ | ⚠️ | **LOW (1/5)** | P2 |
| Feature/Spec | - | ✅ | **NONE (0/5)** | P3 |
| Tool/Model | - | ✅ | **NONE (0/5)** | P3 |

Legend:
- ⚠️⚠️⚠️ = High duplication/inconsistency
- ⚠️⚠️ = Medium duplication/inconsistency  
- ⚠️ = Low duplication/inconsistency
- ✅ = Well-defined, no duplication
- \- = Not applicable to this module

---

**End of Inventory Report**

**Next Steps:** Proceed to Abstraction Dependencies Analysis (2026-02-09-src-abstraction-dependencies.md)
