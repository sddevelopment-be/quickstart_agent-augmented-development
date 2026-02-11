# ADR-043: Status Enumeration Standard

**Status:** ✅ Implemented (superseded by ADR-046 for location)  
**Date:** 2026-02-09  
**Implemented:** 2026-02-11  
**Superseded by:** ADR-046 (types split across `src/domain/collaboration/`, `src/domain/specifications/`)  
**Deciders:** Architect Alphonso  
**Related:** ADR-042 (Shared Task Domain Model), ADR-046 (Domain Refactoring), Python Pedro Analysis (2026-02-09)

> **Note:** This ADR proposed `src/common/types.py`. The file was subsequently split across bounded contexts per ADR-046: `TaskStatus` → `src/domain/collaboration/types.py`, `FeatureStatus` → `src/domain/specifications/types.py`.

---

## Context

### Problem

Task and feature statuses are represented as strings throughout the codebase with no type safety or validation:

**Framework Orchestration:**
```python
# src/framework/orchestration/agent_base.py
task["status"] = "assigned"
task["status"] = "in_progress"
task["status"] = "done"
task["status"] = "error"
```

**Dashboard:**
```python
# src/llm_service/dashboard/progress_calculator.py
if task["status"] == "done": ...
if task["status"] == "in_progress": ...
if task["status"] == "blocked": ...
if task["status"] == "failed": ...
```

**Specification Status:**
```python
# src/llm_service/dashboard/spec_parser.py
spec.status = "draft"
spec.status = "planned"
spec.status = "implemented"
spec.status = "deprecated"
```

### Risks of Current State

1. **Typos Not Caught** - "done" vs "Done" vs "DONE" all compile but fail at runtime
2. **No IDE Support** - No autocomplete, no type checking
3. **Inconsistency** - Different strings in framework vs dashboard ("error" vs "failed")
4. **Late Failure** - Errors only discovered at runtime when string is used
5. **Documentation** - Valid status values not discoverable from code
6. **Maintenance** - Adding new status requires grep and manual updates

### Analysis Findings

From Python Pedro's src/ duplication analysis (2026-02-09):

| Module | Status Strings | Type Safety | Validation |
|--------|---------------|-------------|------------|
| Framework | 4 statuses | ❌ None | Runtime string checks |
| Dashboard | 8+ statuses | ❌ None | Literal type hints (schemas) |
| Specifications | 4 statuses | ❌ None | None |

**Overlapping Statuses:**
- "assigned", "in_progress", "done" - Common to both
- "error" (framework) vs "failed" (dashboard) - Same concept?
- "blocked", "inbox", "new" - Dashboard additions

**Risk Level:** HIGH - No validation, typos possible, maintenance burden

### Requirements

Per architectural review mandate: "intervene NOW, avoid tech debt accumulation"

1. Type-safe status representations
2. Compile-time validation (mypy)
3. IDE autocomplete support
4. Single source of truth for valid statuses
5. Backward compatible with existing YAML files (strings)
6. Clear documentation of status lifecycle

---

## Decision

We will create **status enumerations** in `src/common/types.py` that provide type-safe, validated status values for tasks and features.

### Implementation

**Create:** `src/common/types.py`

```python
"""
Shared type definitions for the agent-augmented development framework.

This module provides type-safe enumerations and type aliases used
across framework orchestration and dashboard modules.
"""

from enum import Enum
from typing import Literal


class TaskStatus(str, Enum):
    """
    Task lifecycle states.
    
    Tasks flow through these states during execution:
    NEW → INBOX → ASSIGNED → IN_PROGRESS → {DONE | ERROR | BLOCKED}
    
    Inherits from str to maintain YAML serialization compatibility.
    """
    
    # Lifecycle states
    NEW = "new"                    # Task created, awaiting assignment
    INBOX = "inbox"                # Task in inbox, awaiting agent pickup
    ASSIGNED = "assigned"          # Task assigned to specific agent
    IN_PROGRESS = "in_progress"    # Agent actively executing task
    BLOCKED = "blocked"            # Task blocked on dependency/blocker
    DONE = "done"                  # Task successfully completed
    ERROR = "error"                # Task failed with error
    
    # Aliases for compatibility
    FAILED = "error"               # Alias for ERROR (dashboard compatibility)
    
    @classmethod
    def is_terminal(cls, status: 'TaskStatus') -> bool:
        """Check if status represents a terminal state."""
        return status in {cls.DONE, cls.ERROR}
    
    @classmethod
    def is_active(cls, status: 'TaskStatus') -> bool:
        """Check if status represents an active (non-terminal) state."""
        return status in {cls.ASSIGNED, cls.IN_PROGRESS, cls.BLOCKED}
    
    @classmethod
    def is_pending(cls, status: 'TaskStatus') -> bool:
        """Check if status represents a pending (not yet started) state."""
        return status in {cls.NEW, cls.INBOX}


class FeatureStatus(str, Enum):
    """
    Feature/specification implementation states.
    
    Features flow through these states during development:
    DRAFT → PLANNED → IN_PROGRESS → IMPLEMENTED → {DEPRECATED}
    
    Inherits from str to maintain YAML serialization compatibility.
    """
    
    DRAFT = "draft"                    # Specification in draft, not approved
    PLANNED = "planned"                # Approved, implementation planned
    IN_PROGRESS = "in_progress"        # Implementation ongoing
    IMPLEMENTED = "implemented"        # Complete and deployed
    DEPRECATED = "deprecated"          # No longer relevant
    
    @classmethod
    def is_active(cls, status: 'FeatureStatus') -> bool:
        """Check if feature is actively being worked on."""
        return status in {cls.PLANNED, cls.IN_PROGRESS}
    
    @classmethod
    def is_complete(cls, status: 'FeatureStatus') -> bool:
        """Check if feature implementation is complete."""
        return status == cls.IMPLEMENTED


# Type aliases for common patterns
TaskStatusValue = str  # For when you need string representation
FeatureStatusValue = str  # For when you need string representation
```

### Status Lifecycle Diagrams

**Task Status Lifecycle:**
```
┌─────┐     ┌───────┐     ┌──────────┐     ┌─────────────┐
│ NEW │ --> │ INBOX │ --> │ ASSIGNED │ --> │ IN_PROGRESS │
└─────┘     └───────┘     └──────────┘     └─────────────┘
                                |                   |
                                |                   v
                                |              ┌─────────┐
                                |              │ BLOCKED │
                                |              └─────────┘
                                |                   |
                                v                   v
                           ┌────────┐         ┌──────┐
                           │ DONE   │    <--  │ERROR │
                           └────────┘         └──────┘
```

**Feature Status Lifecycle:**
```
┌───────┐     ┌─────────┐     ┌─────────────┐     ┌──────────────┐
│ DRAFT │ --> │ PLANNED │ --> │ IN_PROGRESS │ --> │ IMPLEMENTED  │
└───────┘     └─────────┘     └─────────────┘     └──────────────┘
                                                           |
                                                           v
                                                    ┌────────────┐
                                                    │ DEPRECATED │
                                                    └────────────┘
```

### Migration Plan

**Phase 1: Create Enumerations** (2 hours)
1. Create `src/common/__init__.py`
2. Create `src/common/types.py` with TaskStatus and FeatureStatus
3. Write comprehensive tests:
   - Test enum values serialize to strings
   - Test enum methods (is_terminal, is_active, etc.)
   - Test string comparison compatibility
   - Test type checking with mypy

**Phase 2: Update Framework** (3 hours)
1. Update `src/framework/orchestration/agent_base.py`:
   ```python
   from src.common.types import TaskStatus
   
   def update_task_status(self, status: TaskStatus) -> None:
       self.current_task["status"] = status.value
       # ... rest of implementation
   ```
2. Update status transitions:
   ```python
   # Before
   task["status"] = "assigned"
   
   # After
   task["status"] = TaskStatus.ASSIGNED.value
   ```
3. Update status checks:
   ```python
   # Before
   if task["status"] == "done":
       ...
   
   # After
   if TaskStatus(task["status"]) == TaskStatus.DONE:
       ...
   ```
4. Run framework tests

**Phase 3: Update Dashboard** (3 hours)
1. Update `src/llm_service/dashboard/task_linker.py`:
   ```python
   from src.common.types import TaskStatus
   ```
2. Update `src/llm_service/dashboard/progress_calculator.py`:
   ```python
   from src.common.types import TaskStatus
   
   # Update status weights
   DEFAULT_STATUS_WEIGHTS = {
       TaskStatus.DONE.value: 1.0,
       TaskStatus.IN_PROGRESS.value: 0.5,
       TaskStatus.BLOCKED.value: 0.25,
       TaskStatus.NEW.value: 0.0,
   }
   ```
3. Update `src/llm_service/dashboard/spec_parser.py`:
   ```python
   from src.common.types import FeatureStatus
   
   @dataclass
   class SpecificationMetadata:
       status: str  # Validated against FeatureStatus
       # ... other fields
   ```
4. Run dashboard tests

**Phase 4: Add Type Checking** (1 hour)
1. Add mypy to CI pipeline
2. Configure mypy.ini:
   ```ini
   [mypy]
   python_version = 3.9
   warn_return_any = True
   warn_unused_configs = True
   disallow_untyped_defs = True
   ```
3. Fix any type errors discovered
4. Update documentation

**Phase 5: Validation** (1 hour)
1. Add optional validation in task_schema.py:
   ```python
   def read_task(path: Path) -> Dict[str, Any]:
       task = yaml.safe_load(...)
       
       # Optional: validate status
       try:
           TaskStatus(task["status"])
       except ValueError:
           logger.warning(f"Invalid status '{task['status']}' in {path}")
       
       return task
   ```
2. Run full test suite
3. Performance benchmarks

---

## Consequences

### Positive

1. ✅ **Type Safety** - mypy catches typos at compile time
2. ✅ **IDE Support** - Autocomplete for status values
3. ✅ **Documentation** - Valid statuses discoverable from code
4. ✅ **Consistency** - Single source of truth for status values
5. ✅ **Refactoring Safety** - Renaming status updates all uses
6. ✅ **Status Logic** - Helper methods (is_terminal, is_active)
7. ✅ **YAML Compatible** - Enums inherit from str, serialize naturally

### Negative

1. ⚠️ **Verbosity** - `TaskStatus.DONE.value` vs `"done"` (mitigated by type safety benefit)
2. ⚠️ **Migration Effort** - ~30 status string literals to update (10 hours)
3. ⚠️ **Learning Curve** - Team must learn enum usage (minimal - standard Python)

### Neutral

1. 📊 **Backward Compatible** - Enums serialize to same strings in YAML
2. 📊 **Existing Files** - No changes needed to existing task YAML files
3. 📊 **Optional Validation** - Can add validation without breaking changes

---

## Alternatives Considered

### Alternative 1: Type Aliases Only ❌ REJECTED

```python
TaskStatus = Literal["new", "inbox", "assigned", ...]
```

**Pros:** Simple, no migration needed  
**Cons:** No runtime validation, no helper methods, still error-prone

**Verdict:** REJECTED - Doesn't provide runtime safety or helper methods

### Alternative 2: Constants ❌ REJECTED

```python
STATUS_DONE = "done"
STATUS_ERROR = "error"
```

**Pros:** Simple, Python 2 compatible  
**Cons:** Not type-safe, no namespace, no validation

**Verdict:** REJECTED - Inferior to enums in Python 3

### Alternative 3: Defer to Future ❌ REJECTED

**Pros:** No immediate effort  
**Cons:** Violates "intervene NOW" requirement, tech debt grows

**Verdict:** REJECTED - Requirements mandate immediate action

---

## Implementation Status

- [ ] Create src/common/types.py with enums
- [ ] Write comprehensive tests
- [ ] Update framework/orchestration/ status usage
- [ ] Update llm_service/dashboard/ status usage
- [ ] Add mypy type checking to CI
- [ ] Full test suite passing
- [ ] Documentation updated

**Assigned To:** Python Pedro  
**Estimated:** 10 hours  
**Priority:** HIGH (blocking consolidation)

---

## Examples

### Before (String-Based)

```python
# Framework
task["status"] = "assigned"
if task["status"] == "done":
    logger.info("Task complete")

# Dashboard
def get_progress(tasks):
    done_count = sum(1 for t in tasks if t["status"] == "done")
    return done_count / len(tasks)
```

**Problems:**
- Typo "Done" would fail silently
- No IDE autocomplete
- No type checking

### After (Enum-Based)

```python
from src.common.types import TaskStatus

# Framework
task["status"] = TaskStatus.ASSIGNED.value
if TaskStatus(task["status"]) == TaskStatus.DONE:
    logger.info("Task complete")

# Dashboard
def get_progress(tasks):
    done_count = sum(1 for t in tasks 
                     if TaskStatus(t["status"]) == TaskStatus.DONE)
    return done_count / len(tasks)

# Or with helper methods
def get_progress(tasks):
    statuses = [TaskStatus(t["status"]) for t in tasks]
    done_count = sum(1 for s in statuses if s.is_terminal())
    return done_count / len(tasks)
```

**Benefits:**
- Typos caught by mypy at compile time
- IDE autocomplete for TaskStatus.
- Type-safe refactoring

---

## References

- Python Pedro Analysis: `work/reports/analysis/2026-02-09-src-concept-duplication-inventory.md`
- Architectural Review: `work/reports/architecture/2026-02-09-src-consolidation-review.md`
- Related ADR-042: Shared Task Domain Model
- Python Enum Documentation: https://docs.python.org/3/library/enum.html

---

**Decision:** ACCEPTED ✅  
**Date:** 2026-02-09  
**Architect:** Alphonso
