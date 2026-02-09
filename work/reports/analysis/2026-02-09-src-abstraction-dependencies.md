# Source Code Abstraction Dependencies Analysis

**Analysis Date:** 2026-02-09  
**Analyst:** Python Pedro  
**Scope:** src/framework/ and src/llm_service/  
**Task ID:** 2026-02-08T0328-review-src-duplicates

---

## Executive Summary

This analysis maps the dependency relationships between modules in `src/framework/` and `src/llm_service/` to identify:
- Import patterns and coupling levels
- Circular dependency risks
- Shared abstraction usage
- Refactoring order for consolidation work

**Key Findings:**
- ✅ **Good:** No circular dependencies detected between framework and llm_service
- ✅ **Good:** Clean module separation at the top level
- ⚠️ **Concern:** Both modules independently implement similar abstractions (see duplication inventory)
- ⚠️ **Concern:** No shared domain model - missed opportunity for DRY principles

**Architecture Pattern:** Currently **Independent Silos** with opportunity to evolve to **Shared Core**.

---

## 1. Module Dependency Graph

### 1.1 High-Level Module Structure

```
src/
├── framework/
│   ├── context/              # Agent context assembly
│   │   ├── assemble-agent-context.py
│   │   ├── load_directives.py
│   │   └── template-status-checker.py
│   └── orchestration/        # Task orchestration
│       ├── agent_base.py
│       ├── agent_orchestrator.py
│       ├── task_utils.py
│       ├── task_age_checker.py
│       ├── branch_age_checker.py
│       ├── benchmark_orchestrator.py
│       └── example_agent.py
│
└── llm_service/              # LLM routing & dashboard
    ├── adapters/             # Tool adapters
    │   ├── base.py
    │   ├── generic_adapter.py
    │   ├── claude_code_adapter.py
    │   ├── subprocess_wrapper.py
    │   ├── output_normalizer.py
    │   └── template_parser.py
    ├── config/               # Configuration schemas
    │   ├── schemas.py
    │   ├── loader.py
    │   └── env_utils.py
    ├── dashboard/            # Dashboard backend
    │   ├── app.py
    │   ├── spec_parser.py
    │   ├── task_linker.py
    │   ├── task_priority_updater.py
    │   ├── progress_calculator.py
    │   ├── file_watcher.py
    │   └── telemetry_api.py
    ├── telemetry/            # Telemetry logging
    │   └── logger.py
    ├── templates/            # Template management
    │   └── manager.py
    ├── ui/                   # Console UI
    │   └── console.py
    ├── utils/                # Utilities
    │   └── env_scanner.py
    ├── routing.py            # Routing engine
    └── cli.py                # CLI entry point
```

---

## 2. Import Relationship Analysis

### 2.1 Framework Orchestration Dependencies

#### `task_utils.py`
```python
# External dependencies
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml

# Internal dependencies
# NONE - Leaf module
```
**Dependency Score:** 0 internal  
**Purpose:** Utility functions for task file operations  
**Coupling:** Low - No internal dependencies

---

#### `agent_base.py`
```python
# External dependencies
import time
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Internal dependencies
from task_utils import get_utc_timestamp, log_event, read_task, write_task
```
**Dependency Score:** 1 internal (task_utils)  
**Purpose:** Abstract base class for agents  
**Coupling:** Low - Depends only on task_utils

**Import Analysis:**
- ✅ Clean import from same package (relative import: `from task_utils`)
- ✅ No cross-package dependencies
- ⚠️ Hardcoded directory structure (`self.work_dir / "collaboration"`)

---

#### `agent_orchestrator.py`
```python
# External dependencies
import shutil
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Internal dependencies
from task_utils import log_event, read_task, write_task
```
**Dependency Score:** 1 internal (task_utils)  
**Purpose:** Multi-agent coordination and task assignment  
**Coupling:** Low - Depends only on task_utils

**Import Analysis:**
- ✅ Clean import from task_utils
- ⚠️ Hardcoded directory structure (COLLAB_DIR, INBOX_DIR, etc.)
- ❌ No import of agent_base (coordination is file-based, not class-based)

---

#### `task_age_checker.py`, `branch_age_checker.py`, `example_agent.py`
```python
# All import task_utils for task operations
from task_utils import read_task, write_task, get_utc_timestamp
```
**Dependency Score:** 1 internal each  
**Coupling:** Low

---

#### `assemble-agent-context.py` (context module)
```python
# External dependencies
import argparse
import subprocess
import sys
from pathlib import Path

# Internal dependencies
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.path_utils import get_agents_dir, get_repo_root
```
**Dependency Score:** 1 internal (common.path_utils)  
**Purpose:** Agent context assembly  
**Coupling:** Low - Imports from common utilities

**Note:** References `common/` module not in src/ - likely repo-level utilities.

---

### 2.2 LLM Service Dependencies

#### `config/schemas.py`
```python
# External dependencies
from typing import Dict, List, Optional, Literal
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

# Internal dependencies
# NONE - Leaf module (pure schemas)
```
**Dependency Score:** 0 internal  
**Purpose:** Pydantic configuration schemas  
**Coupling:** None - Pure data models

---

#### `config/loader.py`
```python
# External dependencies
from pathlib import Path
from typing import Dict, Optional
import yaml

# Internal dependencies
from .schemas import (
    AgentsSchema, ToolsSchema, ModelsSchema, 
    PoliciesSchema, TelemetryConfig
)
```
**Dependency Score:** 1 internal (config.schemas)  
**Purpose:** Load and validate configuration files  
**Coupling:** Low - Depends only on schemas in same package

---

#### `adapters/base.py`
```python
# External dependencies
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

# Internal dependencies
# NONE - Leaf module (abstract base)
```
**Dependency Score:** 0 internal  
**Purpose:** Abstract base class for tool adapters  
**Coupling:** None - Defines interface only

---

#### `adapters/generic_adapter.py`
```python
# Internal dependencies
from .base import ToolAdapter, ToolResponse
from .subprocess_wrapper import SubprocessWrapper
from .output_normalizer import OutputNormalizer
from .template_parser import TemplateParser
```
**Dependency Score:** 4 internal (same package)  
**Purpose:** Generic YAML-based adapter implementation  
**Coupling:** Medium - Coordinates multiple adapter components

---

#### `routing.py`
```python
# External dependencies
from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass

# Internal dependencies
from .config.schemas import AgentsSchema, ToolsSchema, ModelsSchema, PoliciesSchema
from .adapters.generic_adapter import GenericYAMLAdapter
from .adapters.base import ToolResponse
```
**Dependency Score:** 2 internal packages (config, adapters)  
**Purpose:** Route requests to appropriate tools/models  
**Coupling:** Medium - Coordinates config and adapters

**Import Analysis:**
- ✅ Clean package imports
- ✅ Uses adapter registry pattern
- ✅ Type-safe with dataclasses and type hints

---

#### `dashboard/spec_parser.py`
```python
# External dependencies
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
import re
import yaml
import logging

# Internal dependencies
# NONE - Operates on filesystem directly
```
**Dependency Score:** 0 internal  
**Purpose:** Parse specification frontmatter  
**Coupling:** None - Standalone parser

---

#### `dashboard/task_linker.py`
```python
# External dependencies
from pathlib import Path
from typing import Dict, List, Optional, Set
import yaml
import logging

# Internal dependencies
# NONE - Operates on filesystem directly
```
**Dependency Score:** 0 internal  
**Purpose:** Link tasks to specifications  
**Coupling:** None - Standalone linker

**Critical Observation:**
- ❌ **Does NOT import** `src/framework/orchestration/task_utils.py`
- ❌ Reimplements `load_task()` instead of reusing `read_task()`
- ⚠️ This is the clearest example of duplication

---

#### `dashboard/progress_calculator.py`
```python
# External dependencies
from typing import List, Dict, Optional
import logging

# Internal dependencies
# NONE - Pure calculation logic
```
**Dependency Score:** 0 internal  
**Purpose:** Calculate progress percentages  
**Coupling:** None - Stateless calculator

---

#### `dashboard/file_watcher.py`
```python
# External dependencies
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from typing import Callable
import logging

# Internal dependencies
# NONE - Uses watchdog for file monitoring
```
**Dependency Score:** 0 internal (external: watchdog)  
**Purpose:** Real-time task file monitoring  
**Coupling:** None - External library integration

---

#### `dashboard/app.py`
```python
# Internal dependencies (inferred)
from .spec_parser import SpecificationParser
from .task_linker import TaskLinker
from .progress_calculator import ProgressCalculator
from .telemetry_api import TelemetryAPI
```
**Dependency Score:** 4 internal (dashboard components)  
**Purpose:** Dashboard application assembly  
**Coupling:** High - Coordinates all dashboard components

---

### 2.3 Cross-Module Dependencies

**Critical Finding:** ❌ **ZERO direct imports between framework and llm_service**

```
framework/orchestration/ ←→ llm_service/
        (NO IMPORTS)
```

**Implications:**
1. ✅ No circular dependency risk
2. ✅ Independent deployment possible
3. ⚠️ Duplicated concepts (Task, Agent, Status)
4. ⚠️ No shared abstractions despite overlapping domains

**Coupling via Filesystem:**
Both modules operate on the same filesystem structure:
- `work/collaboration/inbox/*.yaml`
- `work/collaboration/assigned/**/*.yaml`
- `work/collaboration/done/**/*.yaml`

This is **implicit coupling** through shared file format (YAML structure).

---

## 3. Dependency Diagram

### 3.1 Framework Module Dependencies

```
┌─────────────────────────────────────────────────────┐
│                 FRAMEWORK                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐                                   │
│  │ task_utils  │ ← Leaf module (no internal deps)  │
│  └──────┬──────┘                                    │
│         │                                           │
│         ├──────────┐                                │
│         ↓          ↓                                │
│  ┌──────────┐  ┌──────────────────┐                │
│  │agent_base│  │agent_orchestrator│                │
│  └────┬─────┘  └────────┬─────────┘                │
│       │                 │                           │
│       ↓                 ↓                           │
│  ┌────────────────────────────────┐                │
│  │  example_agent, age_checkers   │                │
│  │  (consumers of task_utils)     │                │
│  └────────────────────────────────┘                │
│                                                     │
│  context/                                           │
│  ┌───────────────────────────────┐                 │
│  │ assemble-agent-context.py     │                 │
│  │ (imports common.path_utils)   │                 │
│  └───────────────────────────────┘                 │
└─────────────────────────────────────────────────────┘
```

**Depth:** 2 levels (task_utils → agent_base → example_agent)  
**Coupling:** Low - Linear dependency chain

---

### 3.2 LLM Service Module Dependencies

```
┌──────────────────────────────────────────────────────┐
│                  LLM SERVICE                         │
├──────────────────────────────────────────────────────┤
│                                                      │
│  config/                                             │
│  ┌──────────┐                                        │
│  │ schemas  │ ← Leaf (Pydantic models)              │
│  └────┬─────┘                                        │
│       │                                              │
│       ↓                                              │
│  ┌──────────┐                                        │
│  │  loader  │                                        │
│  └──────────┘                                        │
│                                                      │
│  adapters/                                           │
│  ┌───────┐    ┌───────────┐   ┌──────────┐          │
│  │ base  │ ←──│ subprocess│   │  output  │          │
│  └───┬───┘    │  wrapper  │   │normalizer│          │
│      │        └───────────┘   └──────────┘          │
│      │        ┌──────────────┐                       │
│      │        │   template   │                       │
│      │        │    parser    │                       │
│      │        └──────────────┘                       │
│      ↓              ↓                                │
│  ┌─────────────────────────┐                         │
│  │  generic_adapter        │                         │
│  │  (coordinates all)      │                         │
│  └─────────────────────────┘                         │
│                                                      │
│  dashboard/                                          │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐          │
│  │spec_     │  │task_      │  │progress_ │          │
│  │parser    │  │linker     │  │calculator│          │
│  └────┬─────┘  └────┬──────┘  └────┬─────┘          │
│       │             │              │                │
│       └─────────────┴──────────────┘                │
│                     ↓                               │
│              ┌──────────────┐                        │
│              │  app.py      │                        │
│              │  (assembler) │                        │
│              └──────────────┘                        │
│                                                      │
│  Top Level:                                          │
│  ┌──────────────────────────────────┐                │
│  │  routing.py                      │                │
│  │  (uses config + adapters)        │                │
│  └──────────────────────────────────┘                │
└──────────────────────────────────────────────────────┘
```

**Depth:** 3 levels (base → generic_adapter → routing)  
**Coupling:** Medium - More complex dependency graph

---

### 3.3 Cross-Module Dependency (Current State)

```
┌─────────────────┐           ┌─────────────────┐
│    FRAMEWORK    │           │   LLM SERVICE   │
│  orchestration/ │           │   llm_service/  │
└────────┬────────┘           └────────┬────────┘
         │                             │
         │   NO DIRECT IMPORTS         │
         │                             │
         ↓                             ↓
    ┌─────────────────────────────────────┐
    │    Filesystem (work/collaboration)   │
    │         *.yaml task files           │
    └─────────────────────────────────────┘
              ↑                    ↑
              │                    │
         read_task()          load_task()
         (framework)          (dashboard)
              │                    │
         DUPLICATED IMPLEMENTATION
```

---

## 4. Circular Dependency Analysis

### 4.1 Detection Method

Analyzed all import statements in Python files:
```bash
grep -r "^import\|^from" src/ --include="*.py" | grep -v "^Binary"
```

Cross-referenced to identify potential cycles.

### 4.2 Results

✅ **No circular dependencies detected.**

**Reason:** Clear unidirectional dependency flow:
- Framework: task_utils → agent_base → implementations
- LLM Service: schemas → loader, base → generic_adapter → routing
- Cross-module: None

### 4.3 Risk Assessment

**Current Risk:** ✅ **LOW**

**Future Risk if Consolidation Without Care:** ⚠️ **MEDIUM**

If shared abstractions are introduced incorrectly:
```
# ANTI-PATTERN - would create cycle
src/common/task_model.py:
    from src.llm_service.dashboard.task_linker import TaskLinker
    
src/llm_service/dashboard/task_linker.py:
    from src.common.task_model import Task
    
# CYCLE: task_model → task_linker → task_model
```

**Prevention:** Shared abstractions must be **pure data models** with no imports from either framework or llm_service.

---

## 5. Refactoring Order & Strategy

### 5.1 Dependency-Safe Refactoring Order

To avoid breaking changes, refactor in this order:

#### Phase 1: Create Shared Foundation (No Breaking Changes)
1. ✅ Create `src/common/types.py` (enums, NewTypes)
   - TaskStatus, SpecificationStatus enums
   - AgentName NewType
   - **No dependencies on existing code**
   - **Risk:** None

2. ✅ Create `src/common/task_schema.py` (I/O utilities)
   - Extract `read_task()` and `write_task()` from task_utils
   - Add validation logic
   - **Depends on:** common/types.py
   - **Risk:** Low (new code)

#### Phase 2: Update Framework (Low Risk)
3. ✅ Update `src/framework/orchestration/task_utils.py`
   - Import from common/task_schema
   - Keep backward-compatible wrappers for existing code
   - **Depends on:** common/task_schema
   - **Risk:** Low (backward compatible)

4. ✅ Update `src/framework/orchestration/agent_base.py`
   - Replace status strings with TaskStatus enum
   - Import from common/types
   - **Depends on:** common/types, task_utils
   - **Risk:** Medium (need thorough testing)

5. ✅ Update other framework modules
   - agent_orchestrator, age_checkers, example_agent
   - Replace status strings with enums
   - **Depends on:** common/types
   - **Risk:** Medium

#### Phase 3: Update LLM Service (Low Risk)
6. ✅ Update `src/llm_service/dashboard/task_linker.py`
   - Replace `load_task()` with import from common/task_schema
   - **Depends on:** common/task_schema
   - **Risk:** Low (similar implementation)

7. ✅ Update `src/llm_service/dashboard/progress_calculator.py`
   - Replace status weight dict keys with TaskStatus enum
   - **Depends on:** common/types
   - **Risk:** Low (internal logic)

8. ✅ Update `src/llm_service/dashboard/file_watcher.py`
   - Use TaskStatus enum for status matching
   - **Depends on:** common/types
   - **Risk:** Low

#### Phase 4: Validation & Cleanup (Safety Net)
9. ✅ Run full test suite
   - Unit tests for all modified modules
   - Integration tests for workflow
   - **Risk:** None (verification)

10. ✅ Remove deprecated wrappers
    - Remove compatibility code from task_utils if tests pass
    - **Risk:** Low

---

### 5.2 Dependency Graph After Refactoring

```
┌──────────────────────────────────────────────────────────┐
│                    SHARED CORE                           │
│                  src/common/                             │
│  ┌──────────┐         ┌────────────────┐                │
│  │  types   │ ←───────│ task_schema    │                │
│  │ (enums)  │         │ (I/O + models) │                │
│  └────┬─────┘         └───────┬────────┘                │
└───────┼───────────────────────┼─────────────────────────┘
        │                       │
        │                       │
   ┌────┴───────────────────────┴────┐
   │                                 │
   ↓                                 ↓
┌─────────────────┐          ┌─────────────────┐
│   FRAMEWORK     │          │  LLM SERVICE    │
│ orchestration/  │          │  llm_service/   │
│                 │          │                 │
│ task_utils      │          │ task_linker     │
│ agent_base      │          │ progress_calc   │
│ orchestrator    │          │ file_watcher    │
└─────────────────┘          └─────────────────┘
```

**Benefits:**
- ✅ Single source of truth for Task I/O
- ✅ Type-safe status values
- ✅ No circular dependencies
- ✅ Both modules can import from common without coupling to each other

---

## 6. Import Impact Analysis

### 6.1 Modules Requiring Updates

| Module | Import Changes | Lines Affected | Risk |
|--------|---------------|----------------|------|
| `framework/orchestration/task_utils.py` | Add `from common import task_schema` | ~10 | Low |
| `framework/orchestration/agent_base.py` | Add `from common.types import TaskStatus` | ~15 | Medium |
| `framework/orchestration/agent_orchestrator.py` | Add `from common.types import TaskStatus` | ~12 | Medium |
| `llm_service/dashboard/task_linker.py` | Replace load_task with import | ~30 | Low |
| `llm_service/dashboard/progress_calculator.py` | Add `from common.types import TaskStatus` | ~8 | Low |
| `llm_service/dashboard/file_watcher.py` | Add `from common.types import TaskStatus` | ~5 | Low |

**Total Modules:** 6  
**Total Lines:** ~80 (estimated)  
**Overall Risk:** Medium (need comprehensive testing)

---

### 6.2 Test Requirements

For each updated module:

1. **Unit Tests:**
   - Verify enum serialization (enum → string → YAML)
   - Verify deserialization (YAML → string → enum)
   - Test task I/O with new shared functions
   - Coverage target: ≥90%

2. **Integration Tests:**
   - Framework orchestration full cycle (inbox → assigned → done)
   - Dashboard task scanning and linking
   - Status transitions validated
   - Coverage target: ≥80%

3. **Type Checking:**
   ```bash
   mypy src/common/ --strict
   mypy src/framework/orchestration/ --strict
   mypy src/llm_service/dashboard/ --strict
   ```

4. **Regression Tests:**
   - Existing task YAML files must still parse
   - Dashboard must still display correctly
   - Orchestration agents must still execute

---

## 7. Performance Considerations

### 7.1 Import Overhead

Adding imports from `src/common/` introduces minimal overhead:
- **Enum definitions:** ~0.1ms to import
- **Task schema functions:** ~0.5ms to import
- **Total impact:** <1ms per module load

**Assessment:** ✅ Negligible performance impact

---

### 7.2 Runtime Performance

Status enum comparison vs string comparison:
```python
# Before (string)
if task.get("status") == "done":  # String comparison

# After (enum)
if task.get("status") == TaskStatus.DONE:  # Enum comparison
```

**Performance:** Identical (enums inherit from str, comparison is same)

---

### 7.3 File I/O Performance

Shared task_schema with validation:
```python
# Before (framework)
with open(task_file) as f:
    task = yaml.safe_load(f)  # ~1-5ms per file

# After (common)
task = read_task(task_file)  # Same + validation ~0.5ms
```

**Performance Impact:** +0.5ms per task load (negligible)

**Assessment:** ✅ No significant performance degradation

---

## 8. Testing Strategy for Consolidation

### 8.1 Test-First Approach (TDD - Directive 017)

For each shared abstraction:

#### Step 1: Write Tests for Shared Module
```python
# tests/common/test_task_schema.py
def test_read_task_valid_yaml():
    """Verify task reading with valid YAML."""
    # RED: Test fails (module doesn't exist yet)
    
def test_read_task_invalid_yaml():
    """Verify error handling for malformed YAML."""
    # RED: Test fails
    
def test_write_task_preserves_fields():
    """Verify task writing preserves all fields."""
    # RED: Test fails
```

#### Step 2: Implement Shared Module
```python
# src/common/task_schema.py
def read_task(path: Path) -> Dict[str, Any]:
    """Load task YAML with validation."""
    # GREEN: Minimal implementation to pass tests
```

#### Step 3: Refactor Framework to Use Shared
```python
# src/framework/orchestration/task_utils.py
from common.task_schema import read_task  # Import shared
```

**Run tests:** Verify framework still works with shared code.

#### Step 4: Refactor LLM Service to Use Shared
```python
# src/llm_service/dashboard/task_linker.py
from common.task_schema import read_task  # Import shared
```

**Run tests:** Verify dashboard still works with shared code.

---

### 8.2 Integration Test Coverage

```python
# tests/integration/test_orchestration_with_shared.py
def test_full_task_lifecycle_with_enums():
    """Verify orchestration workflow with TaskStatus enums."""
    # 1. Create task in inbox with status="new"
    # 2. Assign task (status → TaskStatus.ASSIGNED)
    # 3. Start task (status → TaskStatus.IN_PROGRESS)
    # 4. Complete task (status → TaskStatus.DONE)
    # 5. Verify all status transitions logged correctly
    
# tests/integration/test_dashboard_with_shared.py
def test_dashboard_scans_tasks_with_enums():
    """Verify dashboard can read tasks with status enums."""
    # 1. Create tasks with various statuses
    # 2. Scan with TaskLinker
    # 3. Calculate progress with ProgressCalculator
    # 4. Verify correct status interpretation
```

---

## 9. Migration Checklist

### Pre-Migration
- [ ] Create feature branch for consolidation work
- [ ] Ensure all existing tests pass on main
- [ ] Baseline performance metrics captured

### Phase 1: Create Shared Modules
- [ ] Create `src/common/types.py` with TaskStatus, SpecificationStatus
- [ ] Create `src/common/task_schema.py` with read_task, write_task
- [ ] Write unit tests for common modules (≥90% coverage)
- [ ] Verify mypy strict mode passes

### Phase 2: Update Framework
- [ ] Update `task_utils.py` to import from common
- [ ] Update `agent_base.py` to use TaskStatus enum
- [ ] Update `agent_orchestrator.py` to use TaskStatus enum
- [ ] Run framework unit tests
- [ ] Run framework integration tests

### Phase 3: Update LLM Service
- [ ] Update `task_linker.py` to use common task_schema
- [ ] Update `progress_calculator.py` to use TaskStatus enum
- [ ] Update `file_watcher.py` to use TaskStatus enum
- [ ] Run llm_service unit tests
- [ ] Run dashboard integration tests

### Phase 4: Validation
- [ ] Run full test suite (framework + llm_service)
- [ ] Performance regression test
- [ ] Manual smoke test: orchestration workflow
- [ ] Manual smoke test: dashboard display
- [ ] Create ADR documenting consolidation decisions

### Post-Migration
- [ ] Remove deprecated code paths
- [ ] Update documentation (README, architecture docs)
- [ ] Create work log per Directive 014
- [ ] Merge feature branch

---

## 10. Risk Mitigation Strategies

### 10.1 Rollback Plan

If consolidation causes issues:

1. **Immediate Rollback:**
   ```bash
   git revert <consolidation-commit>
   git push
   ```

2. **Partial Rollback:**
   - Keep shared modules but revert imports
   - Use compatibility wrappers temporarily

3. **Forward Fix:**
   - Fix failing tests
   - Add type: ignore where needed temporarily
   - Iterate to resolution

---

### 10.2 Incremental Adoption

Instead of big-bang migration:

1. **Week 1:** Create shared modules, keep existing code unchanged
2. **Week 2:** Update framework only, verify in isolation
3. **Week 3:** Update llm_service only, verify in isolation
4. **Week 4:** Integration testing and cleanup

This allows catching issues early with smaller blast radius.

---

## 11. Success Criteria

### Quantitative Metrics

- [ ] All existing tests pass after refactor
- [ ] Test coverage maintained at ≥80%
- [ ] No performance regression (>5% slower)
- [ ] mypy strict mode passes on all modules
- [ ] ≤5 `type: ignore` comments added

### Qualitative Metrics

- [ ] Status values enforced by enum (no string typos possible)
- [ ] Task I/O unified in single module
- [ ] Import graph shows clear dependency on shared core
- [ ] No circular dependencies introduced
- [ ] Code review approved by 2+ agents

---

## 12. Open Questions for Architecture Review

1. **Should common/ be a separate package with its own pyproject.toml?**
   - Pro: Clear ownership, separate versioning
   - Con: More complex to maintain

2. **Should we use Pydantic models for Task instead of dicts?**
   - Pro: Full validation, type safety
   - Con: More complex serialization

3. **Should specification concepts move to common/?**
   - Currently: Dashboard-only
   - Future: May need in orchestration

4. **How to handle backward compatibility for existing YAML files?**
   - Option 1: Migration script to update all files
   - Option 2: Support both string and enum in read_task()

---

## Appendix A: Import Dependency Matrix

| Module | task_utils | agent_base | orchestrator | schemas | adapters | task_linker |
|--------|-----------|-----------|--------------|---------|----------|-------------|
| **task_utils** | - | ❌ | ❌ | ❌ | ❌ | ❌ |
| **agent_base** | ✅ | - | ❌ | ❌ | ❌ | ❌ |
| **orchestrator** | ✅ | ❌ | - | ❌ | ❌ | ❌ |
| **schemas** | ❌ | ❌ | ❌ | - | ❌ | ❌ |
| **adapters/base** | ❌ | ❌ | ❌ | ❌ | - | ❌ |
| **adapters/generic** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **routing** | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| **task_linker** | ❌ | ❌ | ❌ | ❌ | ❌ | - |
| **progress_calc** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

Legend:
- ✅ = Direct import dependency
- ❌ = No dependency
- **Bold** = Module name (row depends on column)

---

## Appendix B: Proposed Import Matrix After Consolidation

| Module | common/types | common/task_schema | task_utils | schemas |
|--------|-------------|-------------------|-----------|---------|
| **common/types** | - | ❌ | ❌ | ❌ |
| **common/task_schema** | ✅ | - | ❌ | ❌ |
| **task_utils** | ✅ | ✅ | - | ❌ |
| **agent_base** | ✅ | ❌ | ✅ | ❌ |
| **orchestrator** | ✅ | ❌ | ✅ | ❌ |
| **task_linker** | ✅ | ✅ | ❌ | ❌ |
| **progress_calc** | ✅ | ❌ | ❌ | ❌ |

**New Dependencies:**
- All modules depend on common/types (enums)
- task_utils and task_linker depend on common/task_schema
- No circular dependencies introduced

---

**End of Dependencies Analysis**

**Next Steps:** Begin Phase 1 (Create Shared Foundation) with TDD approach
