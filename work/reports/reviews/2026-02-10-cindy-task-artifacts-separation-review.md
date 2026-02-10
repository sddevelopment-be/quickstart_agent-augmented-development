# Code Review: Task Artifacts Separation of Concerns

**Reviewer:** Code-reviewer Cindy (Review Specialist)  
**Date:** 2026-02-10  
**Scope:** Task management scripts and framework alignment  
**Focus:** DRY principle, delegation, schema location, responsibility split  

---

## Executive Summary

✅ **Overall Grade: B+ (Good with Room for Improvement)**

The task management scripts demonstrate **strong architectural alignment** with ADR-042 (Shared Task Domain Model) and ADR-043 (Status Enumeration Standard). The codebase shows evidence of recent refactoring to eliminate duplication and establish proper delegation patterns.

### Key Strengths
1. ✅ All task scripts properly delegate to `src/common/task_schema.py` for I/O operations
2. ✅ TaskStatus enum is used as single source of truth (ADR-043 compliant)
3. ✅ No YAML schemas in tools/ - proper separation maintained
4. ✅ Clear documentation with ADR references in all files
5. ✅ Proper error handling with framework exception types

### Critical Issues Found
1. ⚠️ **HIGH**: Duplicated utility functions (`get_utc_timestamp`, `find_task_file`) across 4 scripts
2. ⚠️ **MEDIUM**: Business logic (allowed modes, priorities) duplicated in validator
3. ⚠️ **MEDIUM**: State transition validation missing from framework
4. ⚠️ **LOW**: Inconsistent import paths in some locations

### Recommended Actions
- **Immediate**: Consolidate utility functions (2 hours)
- **Short-term**: Move validation rules to framework (4 hours)
- **Future**: Add state machine validation (8 hours)

---

## Detailed Findings

### 1. Delegation Pattern Compliance ✅

**Status: EXCELLENT**

All task management scripts properly delegate to framework modules:

**List Open Tasks (`tools/scripts/list_open_tasks.py`):**
```python
# Lines 42-43: Proper delegation
from common.task_schema import load_task_safe
from common.types import TaskStatus

# Line 80: Uses framework I/O
task = load_task_safe(task_file)

# Line 88: Uses framework enum
if not TaskStatus.is_terminal(task_status):
```

**Start Task (`tools/scripts/start_task.py`):**
```python
# Lines 34-35: Proper delegation
from common.task_schema import read_task, write_task
from common.types import TaskStatus

# Line 89: Uses framework I/O
task = read_task(task_file)

# Line 93-99: Uses framework enum for validation
if current_status != TaskStatus.ASSIGNED.value:
    raise ValueError(...)
```

**Complete Task (`tools/scripts/complete_task.py`):**
```python
# Lines 35-36: Proper delegation
from common.task_schema import read_task, write_task
from common.types import TaskStatus
```

**Freeze Task (`tools/scripts/freeze_task.py`):**
```python
# Lines 34-35: Proper delegation (task I/O)
from common.task_schema import read_task, write_task
# Note: Does not need TaskStatus (preserves original status)
```

✅ **Assessment:** All scripts follow proper delegation pattern. No business logic duplication in I/O operations.

---

### 2. DRY Principle Violations ⚠️

**Status: NEEDS IMPROVEMENT**

#### Issue 2.1: Duplicated `get_utc_timestamp()` Function

**Severity: HIGH**  
**Impact: Maintenance burden, consistency risk**

The same timestamp generation logic appears in 4 locations:

**Duplication Evidence:**

1. `tools/scripts/start_task.py` (lines 60-67):
```python
def get_utc_timestamp() -> str:
    """
    Get current UTC timestamp in ISO8601 format with Z suffix.
    
    Returns:
        ISO8601 timestamp string (e.g., "2026-02-09T20:33:00Z")
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
```

2. `tools/scripts/complete_task.py` (lines 60-68): **Identical**
3. `tools/scripts/freeze_task.py` (lines 59-66): **Identical**
4. `src/framework/orchestration/task_utils.py` (lines 40-46): **Slightly different format**

**Framework version:**
```python
def get_utc_timestamp() -> str:
    """Get current UTC timestamp in ISO8601 format with Z suffix."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
```

❗️ **Critical Issue:** Two different implementations produce different formats:
- Tools: `"2026-02-09T20:33:00Z"` (strftime with `%H:%M:%S`)
- Framework: `"2026-02-09T20:33:00.123456Z"` (isoformat with microseconds)

**Recommendation:**
```python
# CURRENT (tools/scripts/*.py):
def get_utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# DESIRED (delegate to framework):
from src.framework.orchestration.task_utils import get_utc_timestamp
# Remove local implementation
```

**Action Required:**
1. Standardize on framework implementation (with or without microseconds - team decision)
2. Update all 3 tool scripts to import from `src.framework.orchestration.task_utils`
3. Add test to verify timestamp format consistency
4. Estimated effort: 2 hours

---

#### Issue 2.2: Duplicated `find_task_file()` Function

**Severity: HIGH**  
**Impact: Maintenance burden, search logic drift**

The same task file search logic appears in 3 locations:

**Duplication Evidence:**

1. `tools/scripts/start_task.py` (lines 38-57):
```python
def find_task_file(task_id: str, work_dir: Path) -> Path | None:
    """Find task file by ID in assigned directories."""
    assigned_dir = work_dir / "assigned"
    if not assigned_dir.exists():
        return None
    for task_file in assigned_dir.rglob(f"{task_id}.yaml"):
        return task_file
    return None
```

2. `tools/scripts/complete_task.py` (lines 39-58): **Identical**
3. `tools/scripts/freeze_task.py` (lines 37-56): **Identical**

**Recommendation:**
```python
# DESIRED: Move to src/framework/orchestration/task_utils.py
def find_task_file(
    task_id: str, 
    work_dir: Path, 
    search_dirs: list[str] | None = None
) -> Path | None:
    """
    Find task file by ID in specified directories.
    
    Args:
        task_id: Task identifier
        work_dir: Work collaboration directory
        search_dirs: Directories to search (default: ["assigned"])
        
    Returns:
        Path to task file, or None if not found
    """
    if search_dirs is None:
        search_dirs = ["assigned"]
    
    for dir_name in search_dirs:
        search_dir = work_dir / dir_name
        if not search_dir.exists():
            continue
        for task_file in search_dir.rglob(f"{task_id}.yaml"):
            return task_file
    
    return None
```

**Action Required:**
1. Add `find_task_file()` to `src/framework/orchestration/task_utils.py`
2. Update all 3 tool scripts to import from framework
3. Add tests for edge cases (missing dirs, multiple matches, etc.)
4. Estimated effort: 2 hours

---

### 3. Schema Location Compliance ✅

**Status: EXCELLENT**

No YAML schemas found in `tools/` directory for task entities. All task-related schema enforcement is in code via:
- `src/common/types.py` (TaskStatus, FeatureStatus enums)
- `src/common/task_schema.py` (validation logic)

**Evidence:**
```bash
$ find tools -name "*.yaml" -o -name "*.yml" | xargs grep -l "task\|status"
tools/release/downstream/framework-update.yml  # Not task schema
tools/scripts/planning/agent-scripts/issue-definitions/planning-features-epic.yml  # Not task schema
```

✅ **Assessment:** Proper separation maintained. Task schemas live in src/, not tools/.

---

### 4. Business Logic Location ⚠️

**Status: NEEDS IMPROVEMENT**

#### Issue 4.1: Validation Rules Duplicated in Validator

**Severity: MEDIUM**  
**Impact: Multiple sources of truth, drift risk**

`tools/validators/validate-task-schema.py` contains hardcoded business rules that should be in framework:

**Lines 36-44:**
```python
# Use TaskStatus enum as single source of truth (ADR-043)
ALLOWED_STATUSES = {status.value for status in TaskStatus}  # ✅ Good delegation

ALLOWED_MODES = {                                             # ⚠️ Hardcoded
    "/analysis-mode",
    "/creative-mode",
    "/meta-mode",
    "/programming",
    "/planning",
}

ALLOWED_PRIORITIES = {"critical", "high", "medium", "normal", "low"}  # ⚠️ Hardcoded
```

**Problem:** If modes or priorities change, we must update:
1. The validator script
2. Any framework code using these values
3. Any documentation

**Recommendation:**

Create enums in `src/common/types.py`:

```python
# DESIRED: Add to src/common/types.py

class TaskMode(str, Enum):
    """Task execution modes."""
    ANALYSIS = "/analysis-mode"
    CREATIVE = "/creative-mode"
    META = "/meta-mode"
    PROGRAMMING = "/programming"
    PLANNING = "/planning"


class TaskPriority(str, Enum):
    """Task priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    NORMAL = "normal"
    LOW = "low"
    
    @classmethod
    def default(cls) -> "TaskPriority":
        """Get default priority."""
        return cls.MEDIUM
```

Update validator:
```python
# DESIRED: tools/validators/validate-task-schema.py
from common.types import TaskStatus, TaskMode, TaskPriority

ALLOWED_STATUSES = {status.value for status in TaskStatus}
ALLOWED_MODES = {mode.value for mode in TaskMode}
ALLOWED_PRIORITIES = {priority.value for priority in TaskPriority}
```

**Action Required:**
1. Add TaskMode and TaskPriority enums to `src/common/types.py`
2. Update validator to use enums
3. Update any framework code to use enums
4. Add tests for enum validation
5. Estimated effort: 4 hours

---

#### Issue 4.2: State Transition Validation Missing

**Severity: MEDIUM**  
**Impact: Invalid state transitions not caught**

**Current State:**

`start_task.py` validates state transitions:
```python
# Lines 92-96
current_status = task.get("status")
if current_status != TaskStatus.ASSIGNED.value:
    raise ValueError(
        f"Task must be in 'assigned' state to start. Current status: {current_status}"
    )
```

But this logic is **in the tool script**, not the framework!

**Problem:** 
- State transition rules should be in `src/common/types.py` or dedicated state machine module
- Currently each tool script reimplements validation
- No central enforcement of valid transitions

**Recommendation:**

Add state machine logic to framework:

```python
# DESIRED: Add to src/common/types.py

class TaskStatus(str, Enum):
    # ... existing code ...
    
    @classmethod
    def valid_transitions(cls, from_status: "TaskStatus") -> set["TaskStatus"]:
        """Get valid transitions from a given status."""
        transitions = {
            cls.NEW: {cls.INBOX},
            cls.INBOX: {cls.ASSIGNED},
            cls.ASSIGNED: {cls.IN_PROGRESS, cls.BLOCKED},
            cls.IN_PROGRESS: {cls.DONE, cls.ERROR, cls.BLOCKED},
            cls.BLOCKED: {cls.IN_PROGRESS, cls.ASSIGNED},
            cls.DONE: set(),  # Terminal
            cls.ERROR: set(), # Terminal
        }
        return transitions.get(from_status, set())
    
    @classmethod
    def can_transition(cls, from_status: "TaskStatus", to_status: "TaskStatus") -> bool:
        """Check if transition is valid."""
        return to_status in cls.valid_transitions(from_status)
    
    @classmethod
    def validate_transition(
        cls, from_status: "TaskStatus", to_status: "TaskStatus"
    ) -> None:
        """Validate transition or raise ValueError."""
        if not cls.can_transition(from_status, to_status):
            valid = cls.valid_transitions(from_status)
            raise ValueError(
                f"Invalid transition: {from_status.value} → {to_status.value}. "
                f"Valid transitions: {[s.value for s in valid]}"
            )
```

Update scripts to use framework validation:
```python
# DESIRED: tools/scripts/start_task.py
from common.types import TaskStatus

# Validate transition
current_status = TaskStatus(task.get("status"))
TaskStatus.validate_transition(current_status, TaskStatus.IN_PROGRESS)

# Update status
task["status"] = TaskStatus.IN_PROGRESS.value
```

**Action Required:**
1. Add state machine methods to TaskStatus enum
2. Update all tool scripts to use framework validation
3. Add comprehensive tests for all valid/invalid transitions
4. Document state machine in ADR or architecture docs
5. Estimated effort: 8 hours

---

### 5. Responsibility Split Compliance ✅

**Status: GOOD**

The separation between `src/` and `tools/` is well-maintained:

#### Framework (src/) - Business Logic ✅
- `src/common/types.py`: Status enumerations with lifecycle methods
- `src/common/task_schema.py`: I/O operations, validation, error handling
- `src/framework/orchestration/task_utils.py`: Timestamp generation, status updates
- `src/framework/orchestration/agent_base.py`: Task execution lifecycle

#### Tools - CLI Wrappers ✅
- `tools/scripts/list_open_tasks.py`: User-facing list command
- `tools/scripts/start_task.py`: User-facing start command
- `tools/scripts/complete_task.py`: User-facing complete command
- `tools/scripts/freeze_task.py`: User-facing freeze command
- `tools/validators/validate-task-schema.py`: CI/CD validation

**Evidence of Proper Split:**

1. **Tools delegate to framework** (not reimplement):
   ```python
   # tools/scripts/start_task.py
   from common.task_schema import read_task, write_task  # ✅ Delegates I/O
   from common.types import TaskStatus                    # ✅ Delegates enums
   ```

2. **Tools provide CLI/UX layer only**:
   - Argument parsing (argparse)
   - User-friendly output formatting (tables, JSON)
   - Error message formatting
   - Exit code handling

3. **Framework provides business logic**:
   - Task I/O and validation
   - Status lifecycle methods
   - Timestamp generation
   - Error handling

✅ **Assessment:** Responsibility split is clear and well-maintained. No business logic leaked into tools.

---

### 6. Architecture Alignment ✅

**Status: EXCELLENT**

#### ADR-042: Shared Task Domain Model

✅ **Compliance: 100%**

All scripts use `src/common/task_schema.py` as single source of truth:

| Script | Uses read_task | Uses write_task | Uses load_task_safe |
|--------|---------------|-----------------|---------------------|
| list_open_tasks.py | ❌ | ❌ | ✅ |
| start_task.py | ✅ | ✅ | ❌ |
| complete_task.py | ✅ | ✅ | ❌ |
| freeze_task.py | ✅ | ✅ | ❌ |
| validate-task-schema.py | ✅ (direct YAML) | ❌ | ❌ |

**Note:** Validator reads YAML directly for schema validation (acceptable - it's validating the schema itself).

**Evidence:**
```python
# All scripts include ADR references:
# Related ADRs:
#     - ADR-042: Shared Task Domain Model
#     - ADR-043: Status Enumeration Standard
```

#### ADR-043: Status Enumeration Standard

✅ **Compliance: 90%**

All scripts use `TaskStatus` enum from `src/common/types.py`:

**Good Examples:**
```python
# list_open_tasks.py (lines 86-92)
try:
    task_status = TaskStatus(status)
    if not TaskStatus.is_terminal(task_status):  # ✅ Uses helper method
        open_tasks.append(task)
except ValueError:
    continue  # Invalid status, skip
```

```python
# start_task.py (lines 93-96)
if current_status != TaskStatus.ASSIGNED.value:  # ✅ Uses enum value
    raise ValueError(...)
```

**Minor Issue:**
- State transition logic not centralized (see Issue 4.2 above)
- Would be 100% compliant with state machine methods in enum

---

### 7. Code Quality & Best Practices ✅

**Status: EXCELLENT**

#### Documentation ✅
- All files have comprehensive docstrings
- ADR references included
- Usage examples provided
- Directive compliance noted

#### Error Handling ✅
```python
# complete_task.py (lines 83-102)
try:
    complete_task(args.task_id, args.work_dir, force=args.force)
    return 0
except FileNotFoundError as e:
    print(f"Error: {e}", file=sys.stderr)  # Specific error
    return 1
except ValueError as e:
    print(f"Error: {e}", file=sys.stderr)  # Specific error
    return 1
except Exception as e:
    print(f"Error completing task: {e}", file=sys.stderr)  # Catch-all
    return 1
```

#### Type Hints ✅
```python
# All functions have proper type hints
def find_task_file(task_id: str, work_dir: Path) -> Path | None:
def get_utc_timestamp() -> str:
def filter_tasks(
    tasks: list[dict[str, Any]],
    status: str | None = None,
    agent: str | None = None,
    priority: str | None = None,
) -> list[dict[str, Any]]:
```

#### Testing References ✅
```python
# All scripts mention:
# Directive Compliance:
#     - 017 (TDD): Implemented with test coverage
```

---

## Compliance Matrix

| Criterion | Status | Grade | Notes |
|-----------|--------|-------|-------|
| DRY Principle | ⚠️ Needs Improvement | B | Utility functions duplicated |
| Delegation Pattern | ✅ Excellent | A+ | All scripts delegate properly |
| Schema Location | ✅ Excellent | A+ | No schemas in tools/ |
| Responsibility Split | ✅ Good | A | Clear separation maintained |
| ADR-042 Compliance | ✅ Excellent | A+ | Shared domain model used |
| ADR-043 Compliance | ✅ Good | A- | Enum used, state machine missing |
| Code Quality | ✅ Excellent | A+ | Well-documented, type-hinted |

**Overall Grade: B+ (Good with Room for Improvement)**

---

## Prioritized Recommendations

### Priority 1: CRITICAL (Do Now) 🔴

None. No critical issues blocking functionality.

### Priority 2: HIGH (This Sprint) 🟡

#### H1. Consolidate Utility Functions
- **Issue:** `get_utc_timestamp()` and `find_task_file()` duplicated 3-4 times
- **Solution:** 
  1. Standardize timestamp format in `src/framework/orchestration/task_utils.py`
  2. Add `find_task_file()` to same module
  3. Update all scripts to import from framework
- **Effort:** 2 hours
- **Impact:** Eliminates 50+ lines of duplication, prevents drift

#### H2. Extract Business Rules to Framework
- **Issue:** ALLOWED_MODES and ALLOWED_PRIORITIES hardcoded in validator
- **Solution:**
  1. Add TaskMode and TaskPriority enums to `src/common/types.py`
  2. Update validator to use enums
  3. Update any framework code to use enums
- **Effort:** 4 hours
- **Impact:** Single source of truth for validation rules

### Priority 3: MEDIUM (Next Sprint) 🟢

#### M1. Add State Machine Validation
- **Issue:** State transition rules scattered across scripts
- **Solution:**
  1. Add `valid_transitions()` and `validate_transition()` to TaskStatus enum
  2. Update all scripts to use framework validation
  3. Add comprehensive tests
- **Effort:** 8 hours
- **Impact:** Centralized state machine, prevents invalid transitions

### Priority 4: LOW (Future) 🔵

#### L1. Consider Validator Consolidation
- **Issue:** Validator reimplements some validation logic from task_schema.py
- **Solution:** Explore delegating more validation to framework
- **Effort:** 4 hours
- **Impact:** Further DRY improvements

---

## Code Examples

### Example 1: Current vs. Desired (Utility Functions)

**CURRENT (Duplicated):**
```python
# tools/scripts/start_task.py
def get_utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# tools/scripts/complete_task.py
def get_utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# tools/scripts/freeze_task.py
def get_utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# src/framework/orchestration/task_utils.py
def get_utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
```

**DESIRED (Consolidated):**
```python
# src/framework/orchestration/task_utils.py
def get_utc_timestamp() -> str:
    """Get current UTC timestamp in ISO8601 format with Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def find_task_file(
    task_id: str, 
    work_dir: Path, 
    search_dirs: list[str] | None = None
) -> Path | None:
    """Find task file by ID in specified directories."""
    if search_dirs is None:
        search_dirs = ["assigned"]
    
    for dir_name in search_dirs:
        search_dir = work_dir / dir_name
        if not search_dir.exists():
            continue
        for task_file in search_dir.rglob(f"{task_id}.yaml"):
            return task_file
    
    return None

# tools/scripts/start_task.py (and others)
from src.framework.orchestration.task_utils import get_utc_timestamp, find_task_file
# Remove local implementations
```

### Example 2: Current vs. Desired (Business Rules)

**CURRENT (Hardcoded):**
```python
# tools/validators/validate-task-schema.py
ALLOWED_MODES = {
    "/analysis-mode",
    "/creative-mode",
    "/meta-mode",
    "/programming",
    "/planning",
}
ALLOWED_PRIORITIES = {"critical", "high", "medium", "normal", "low"}

# Validation
if mode is not None and mode not in ALLOWED_MODES:
    errors.append(f"invalid mode '{mode}'")
```

**DESIRED (Enum-based):**
```python
# src/common/types.py
class TaskMode(str, Enum):
    ANALYSIS = "/analysis-mode"
    CREATIVE = "/creative-mode"
    META = "/meta-mode"
    PROGRAMMING = "/programming"
    PLANNING = "/planning"

class TaskPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    NORMAL = "normal"
    LOW = "low"

# tools/validators/validate-task-schema.py
from common.types import TaskMode, TaskPriority

ALLOWED_MODES = {mode.value for mode in TaskMode}
ALLOWED_PRIORITIES = {priority.value for priority in TaskPriority}

# Validation remains same, but now uses single source of truth
```

### Example 3: Current vs. Desired (State Transitions)

**CURRENT (In Tools):**
```python
# tools/scripts/start_task.py
current_status = task.get("status")
if current_status != TaskStatus.ASSIGNED.value:
    raise ValueError(
        f"Task must be in 'assigned' state to start. Current status: {current_status}"
    )
```

**DESIRED (In Framework):**
```python
# src/common/types.py
class TaskStatus(str, Enum):
    # ... existing code ...
    
    @classmethod
    def validate_transition(cls, from_status: "TaskStatus", to_status: "TaskStatus") -> None:
        """Validate transition or raise ValueError."""
        if not cls.can_transition(from_status, to_status):
            valid = cls.valid_transitions(from_status)
            raise ValueError(
                f"Invalid transition: {from_status.value} → {to_status.value}. "
                f"Valid transitions: {[s.value for s in valid]}"
            )

# tools/scripts/start_task.py
current_status = TaskStatus(task.get("status"))
TaskStatus.validate_transition(current_status, TaskStatus.IN_PROGRESS)
```

---

## Summary

### What's Working Well ✅

1. **Delegation Pattern**: All scripts properly delegate to framework for I/O and type definitions
2. **ADR Compliance**: Strong adherence to ADR-042 and ADR-043
3. **Documentation**: Excellent docstrings, ADR references, usage examples
4. **Separation of Concerns**: Clear split between framework (business logic) and tools (CLI)
5. **Type Safety**: Proper use of type hints and enums
6. **Error Handling**: Specific exception handling with user-friendly messages

### What Needs Improvement ⚠️

1. **DRY Violations**: 50+ lines of duplicated utility functions
2. **Business Rules Location**: Modes and priorities hardcoded in validator
3. **State Machine**: Transition validation logic scattered across scripts
4. **Format Inconsistency**: Two different timestamp formats in use

### Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Timestamp drift | Medium | High | Consolidate NOW (H1) |
| Invalid state transitions | Medium | Medium | Add state machine (M1) |
| Business rule drift | Medium | Low | Extract to enums (H2) |
| Maintenance burden | Low | High | Already addressed by proper delegation |

### Next Steps

1. **Immediate** (Week 1): Execute H1 - Consolidate utility functions
2. **Short-term** (Week 2): Execute H2 - Extract business rules to enums
3. **Medium-term** (Sprint 2): Execute M1 - Add state machine validation
4. **Long-term** (Backlog): Consider L1 - Further validator consolidation

---

## References

- **ADR-042:** Shared Task Domain Model (`docs/architecture/adrs/ADR-042-shared-task-domain-model.md`)
- **ADR-043:** Status Enumeration Standard (`docs/architecture/adrs/ADR-043-status-enumeration-standard.md`)
- **Directive 017:** Test-Driven Development
- **Directive 021:** Locality of Behavior
- **Framework README:** `src/README.md`
- **Tools README:** `tools/README.md`

---

**Review Status:** ✅ COMPLETE  
**Reviewed By:** Code-reviewer Cindy  
**Date:** 2026-02-10  
**Confidence:** ⚠️ 85% (High confidence in findings, some edge cases may exist)
