# ADR-042: Shared Task Domain Model

**Status:** Accepted  
**Date:** 2026-02-09  
**Deciders:** Architect Alphonso  
**Related:** ADR-043 (Status Enumeration), Python Pedro Analysis (2026-02-09)

---

## Context

### Problem

Task I/O operations are duplicated across two modules:
- `src/framework/orchestration/task_utils.py` - Framework task operations
- `src/llm_service/dashboard/task_linker.py` - Dashboard task operations

Both modules:
1. Read YAML task files from `work/collaboration/`
2. Parse identical task structure
3. Handle similar error cases
4. Maintain ~150 lines of duplicate code

**Current Implementations:**

**Framework (task_utils.py):**
```python
def read_task(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f:
        task = yaml.safe_load(f)
    # Basic validation
    return task

def write_task(path: Path, task: Dict[str, Any]) -> None:
    with open(path, 'w') as f:
        yaml.dump(task, f, sort_keys=False)
```

**Dashboard (task_linker.py):**
```python
def load_task(path: Path) -> Optional[Dict]:
    try:
        with open(path, 'r') as f:
            task = yaml.safe_load(f)
        return task
    except Exception as e:
        logger.warning(f"Failed to load task {path}: {e}")
        return None
```

### Analysis Findings

From Python Pedro's src/ duplication analysis (2026-02-09):

| Aspect | Duplication Level | Impact |
|--------|-------------------|--------|
| Core Structure | HIGH | Identical YAML parsing logic |
| File I/O | MEDIUM | Similar with different error handling |
| Validation | LOW | Different approaches |

**Risks of Current State:**
1. **Maintenance Burden** - Bug fixes must be applied in two places
2. **Inconsistency** - Implementations diverge over time
3. **Error Handling** - Different behaviors confuse debugging
4. **Tech Debt** - Duplication compounds as features grow

### Requirements

Per architectural review mandate: "intervene NOW, avoid tech debt accumulation"

1. Single source of truth for task I/O operations
2. Consistent error handling across modules
3. Type-safe task schema
4. Backward compatible with existing YAML files
5. No circular dependencies between framework and dashboard

---

## Decision

We will create a **shared task domain model** in `src/common/task_schema.py` that provides unified task I/O operations for both framework and dashboard modules.

### Implementation

**Create:** `src/common/task_schema.py`

```python
"""
Shared task schema and I/O operations.

This module provides a single source of truth for task file operations,
ensuring consistency across framework orchestration and dashboard modules.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
import logging

logger = logging.getLogger(__name__)


class TaskSchemaError(Exception):
    """Base exception for task schema operations"""
    pass


class TaskValidationError(TaskSchemaError):
    """Raised when task structure is invalid"""
    pass


class TaskIOError(TaskSchemaError):
    """Raised when task file I/O fails"""
    pass


def read_task(path: Path) -> Dict[str, Any]:
    """
    Read and parse a task file.
    
    Args:
        path: Path to task YAML file
        
    Returns:
        Task dictionary with all fields
        
    Raises:
        TaskIOError: If file cannot be read or parsed
        TaskValidationError: If task structure is invalid
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            task = yaml.safe_load(f)
    except FileNotFoundError:
        raise TaskIOError(f"Task file not found: {path}")
    except yaml.YAMLError as e:
        raise TaskIOError(f"Invalid YAML in {path}: {e}")
    except Exception as e:
        raise TaskIOError(f"Failed to read task {path}: {e}")
    
    if not isinstance(task, dict):
        raise TaskValidationError(f"Task must be a dictionary, got {type(task)}")
    
    # Validate required fields
    required_fields = {'id', 'status'}
    missing_fields = required_fields - set(task.keys())
    if missing_fields:
        raise TaskValidationError(f"Missing required fields: {missing_fields}")
    
    return task


def write_task(path: Path, task: Dict[str, Any]) -> None:
    """
    Write a task to file.
    
    Args:
        path: Path to task YAML file
        task: Task dictionary to write
        
    Raises:
        TaskIOError: If file cannot be written
        TaskValidationError: If task structure is invalid
    """
    if not isinstance(task, dict):
        raise TaskValidationError(f"Task must be a dictionary, got {type(task)}")
    
    # Validate required fields before writing
    required_fields = {'id', 'status'}
    missing_fields = required_fields - set(task.keys())
    if missing_fields:
        raise TaskValidationError(f"Cannot write task with missing fields: {missing_fields}")
    
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(task, f, sort_keys=False, default_flow_style=False)
    except Exception as e:
        raise TaskIOError(f"Failed to write task to {path}: {e}")


def load_task_safe(path: Path) -> Optional[Dict[str, Any]]:
    """
    Safely load a task file, returning None on error.
    
    This is a convenience wrapper for dashboard/monitoring code that
    needs to handle missing or invalid tasks gracefully.
    
    Args:
        path: Path to task YAML file
        
    Returns:
        Task dictionary if successful, None otherwise
    """
    try:
        return read_task(path)
    except TaskSchemaError as e:
        logger.warning(f"Failed to load task {path}: {e}")
        return None
```

### Migration Plan

**Phase 1: Create Shared Module** (2 hours)
1. Create `src/common/` package
2. Create `src/common/__init__.py`
3. Create `src/common/task_schema.py` with implementation above
4. Write comprehensive tests (pytest)
   - Test successful read/write
   - Test error conditions (missing file, invalid YAML, missing fields)
   - Test backward compatibility with existing task files

**Phase 2: Update Framework Module** (3 hours)
1. Update `src/framework/orchestration/task_utils.py`:
   ```python
   # Import from shared module
   from src.common.task_schema import read_task, write_task, TaskIOError
   
   # Keep existing utility functions
   def get_utc_timestamp() -> str:
       # ... existing code
   
   def log_event(msg: str) -> None:
       # ... existing code
   ```
2. Update `src/framework/orchestration/agent_base.py`:
   ```python
   from src.common.task_schema import read_task, write_task, TaskIOError
   ```
3. Update `src/framework/orchestration/agent_orchestrator.py`:
   ```python
   from src.common.task_schema import read_task, write_task
   ```
4. Run framework tests, verify no regressions

**Phase 3: Update Dashboard Module** (3 hours)
1. Update `src/llm_service/dashboard/task_linker.py`:
   ```python
   from src.common.task_schema import read_task, load_task_safe
   
   # Replace load_task() with load_task_safe()
   def scan_tasks(directory: Path) -> List[Dict]:
       tasks = []
       for path in directory.glob("**/*.yaml"):
           task = load_task_safe(path)
           if task:
               tasks.append(task)
       return tasks
   ```
2. Update other dashboard files using task operations
3. Remove duplicate `load_task()` implementation
4. Run dashboard tests, verify functionality

**Phase 4: Cleanup** (1 hour)
1. Remove old task I/O code from task_utils.py and task_linker.py
2. Update imports across codebase
3. Run full test suite
4. Update documentation

---

## Consequences

### Positive

1. ✅ **Single Source of Truth** - One implementation to maintain
2. ✅ **Consistent Error Handling** - Same exceptions and logging everywhere
3. ✅ **Better Testing** - Centralized tests for task I/O
4. ✅ **Type Safety** - Clear exception types for error handling
5. ✅ **Documentation** - Docstrings explain behavior once
6. ✅ **Reduced Code** - Eliminate ~150 lines of duplication
7. ✅ **No Circular Dependencies** - Clean import hierarchy

### Negative

1. ⚠️ **Breaking Changes** - Internal refactoring (mitigated by backward compatibility)
2. ⚠️ **Import Updates** - All files using task I/O must update imports
3. ⚠️ **Migration Effort** - 9 hours estimated (acceptable for preventing tech debt)

### Neutral

1. 📊 **New Package** - `src/common/` adds one directory level
2. 📊 **Exception Types** - New exception hierarchy (improvement)

---

## Alternatives Considered

### Alternative 1: Keep Duplication ❌ REJECTED

**Rationale:** Violates requirement to "intervene NOW, avoid tech debt"

### Alternative 2: Framework-Only Consolidation ❌ REJECTED

**Rationale:** Would leave dashboard with duplicate code, doesn't solve root cause

### Alternative 3: Wrapper Functions ❌ REJECTED

**Rationale:** Adds complexity without eliminating duplication

---

## Implementation Status

- [ ] Create src/common/task_schema.py with tests
- [ ] Update framework/orchestration/ imports
- [ ] Update llm_service/dashboard/ imports
- [ ] Remove duplicate implementations
- [ ] Full test suite passing
- [ ] Documentation updated

**Assigned To:** Python Pedro  
**Estimated:** 9 hours  
**Priority:** HIGH (blocking consolidation)

---

## References

- Python Pedro Analysis: `work/reports/analysis/2026-02-09-src-concept-duplication-inventory.md`
- Architectural Review: `work/reports/architecture/2026-02-09-src-consolidation-review.md`
- Related ADR-043: Status Enumeration Standard
- Directive 017: Test-Driven Development

---

**Decision:** ACCEPTED ✅  
**Date:** 2026-02-09  
**Architect:** Alphonso
