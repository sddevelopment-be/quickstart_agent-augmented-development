# Domain Module Migration Guide

**Migration:** ADR-046 Task 2 - Move Files to Bounded Contexts  
**Date:** 2026-02-11  
**Status:** ⚠️ BREAKING CHANGE - Imports temporarily broken until Task 3 completes

## Overview

Files from `src/common/` have been moved to bounded context directories to improve domain separation and reduce polysemy confusion.

## File Mappings

### Collaboration Domain (Agent Orchestration)

| Old Location | New Location | Description |
|-------------|--------------|-------------|
| `src/common/task_schema.py` | `src/domain/collaboration/task_schema.py` | Task domain model and I/O |
| `src/common/types.py` (partial) | `src/domain/collaboration/types.py` | TaskStatus, TaskMode, TaskPriority |

**Import Changes:**
```python
# OLD
from src.common.task_schema import read_task, write_task
from src.common.types import TaskStatus, TaskPriority

# NEW
from src.domain.collaboration.task_schema import read_task, write_task
from src.domain.collaboration.types import TaskStatus, TaskPriority
```

### Doctrine Domain (Framework Governance)

| Old Location | New Location | Description |
|-------------|--------------|-------------|
| `src/common/agent_loader.py` | `src/domain/doctrine/agent_loader.py` | Agent profile parsing |
| `src/common/types.py` (partial) | `src/domain/doctrine/types.py` | AgentIdentity, validation |

**Import Changes:**
```python
# OLD
from src.common.agent_loader import load_agent_identities
from src.common.types import AgentIdentity, validate_agent

# NEW
from src.domain.doctrine.agent_loader import load_agent_identities
from src.domain.doctrine.types import AgentIdentity, validate_agent
```

### Specifications Domain (Product Planning)

| Old Location | New Location | Description |
|-------------|--------------|-------------|
| `src/common/types.py` (partial) | `src/domain/specifications/types.py` | FeatureStatus |

**Import Changes:**
```python
# OLD
from src.common.types import FeatureStatus

# NEW
from src.domain.specifications.types import FeatureStatus
```

### Common Domain (Generic Utilities)

| Old Location | New Location | Description |
|-------------|--------------|-------------|
| `src/common/path_utils.py` | `src/domain/common/path_utils.py` | Generic path utilities |

**Import Changes:**
```python
# OLD
from src.common.path_utils import get_repo_root

# NEW
from src.domain.common.path_utils import get_repo_root
```

## Migration Strategy

### Phase 1: File Move (Task 2) ✅ COMPLETE
- Files moved with `git mv` to preserve history
- Deprecation stubs created in `src/common/`
- **Result:** Import errors expected (temporary)

### Phase 2: Import Update (Task 3) 🔄 IN PROGRESS
- Update all imports across codebase
- Fix test failures
- Verify all integration points

### Phase 3: Validation (Task 4) ⏳ PENDING
- Run full test suite
- Validate git history preservation
- Update documentation

## Backwards Compatibility

`src/common/` files now contain deprecation notices and re-export imports from new locations.

**Temporary Compatibility:**
```python
# This will still work temporarily (with warnings)
from src.common.task_schema import read_task

# But you should update to:
from src.domain.collaboration.task_schema import read_task
```

**Removal Timeline:**
- Deprecation warnings: Immediate
- Backwards compatibility removal: After Task 3 completes all import updates

## Git History Preservation

All moves used `git mv` to preserve file history:

```bash
# Verify history is preserved
git log --follow src/domain/collaboration/task_schema.py
git log --follow src/domain/doctrine/agent_loader.py
git log --follow src/domain/common/path_utils.py
```

## Commit History

1. **Commit 1:** Move collaboration files
   - `task_schema.py` → `collaboration/`

2. **Commit 2:** Move doctrine files
   - `agent_loader.py` → `doctrine/`

3. **Commit 3:** Split types.py by context
   - `collaboration/types.py`
   - `doctrine/types.py`
   - `specifications/types.py`

4. **Commit 4:** Move generic utilities
   - `path_utils.py` → `common/`

5. **Commit 5:** Add deprecation notices
   - Migration guide
   - Deprecation stubs in `src/common/`

## Rationale (ADR-046)

**Why This Change:**
- **Polysemy Resolution:** "Task" means different things in different contexts
- **Bounded Contexts:** Clear separation of domain concerns
- **Evolutionary Design:** Contexts can evolve independently
- **Foundation for ADR-045:** Doctrine domain model requires clear boundaries

**Affected Areas:**
- Framework orchestration (`framework/`)
- Dashboard modules (`src/dashboard/`)
- Operations scripts (`ops/`)
- Test suites (`tests/`)

## Troubleshooting

### Import Errors After Migration

**Symptom:** `ImportError: cannot import name 'TaskStatus' from 'src.common.types'`

**Solution:**
1. Update import to new location (see mappings above)
2. If you see `ModuleNotFoundError`, verify the file moved correctly:
   ```bash
   ls -la src/domain/collaboration/
   ls -la src/domain/doctrine/
   ```

### Types.py Split Confusion

**Issue:** `types.py` was split into three files

**Resolution:**
- Task-related types → `collaboration/types.py`
- Agent-related types → `doctrine/types.py`
- Feature-related types → `specifications/types.py`

### Git History Lost

**Issue:** Cannot find file history after move

**Solution:**
```bash
# Use --follow flag to track renames
git log --follow -- src/domain/collaboration/task_schema.py
```

## Related Documentation

- **ADR-046:** Domain Module Refactoring
- **ADR-045:** Doctrine Concept Domain Model
- **ADR-043:** Status Enumeration Standard
- **Task:** `2026-02-11T1100-adr046-task2-move-files.yaml`

## Contact

Questions or issues? Contact:
- **Architect Alphonso:** ADR clarifications
- **Manager Mike:** Task coordination
- **Python Pedro:** Technical implementation details
