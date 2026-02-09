# Src/ Consolidation Implementation Plan with Architecture Tests

**Agent:** Python Pedro  
**Date:** 2026-02-09  
**Based on:** Architect Alphonso's Review + ADRs 042, 043, 044

---

## Executive Summary

Implementing immediate consolidation of src/ duplications with architecture testing to prevent regression. Following TDD principles per Directive 017, implementing architecture tests per new requirement.

**Total Estimated Time:** 29-39 hours (includes architecture tests)

---

## Phase 1: Setup Architecture Testing (4 hours) 🆕

### 1.1 Add Dependencies (30 min)

**Update pyproject.toml:**
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=25.0",
    "ruff>=0.14.0",
    "mutmut>=3.4.0",
    "mypy>=1.0",
    "types-PyYAML>=6.0",
    "import-linter>=2.0",     # NEW: Module dependency rules
    "pytestarch>=2.0",        # NEW: Architecture testing
]
```

### 1.2 Create import-linter Config (1 hour)

**Create .importlinter:**
```ini
[importlinter]
root_package = src

[importlinter:contract:1]
name = No circular dependencies
type = independence
modules =
    src.framework
    src.llm_service
    src.common

[importlinter:contract:2]
name = Common module is leaf
type = layers
layers =
    src.framework.orchestration
    src.llm_service.dashboard
    src.common
containers =
    src

[importlinter:contract:3]
name = No direct framework-llm_service imports
type = forbidden
source_modules =
    src.framework
forbidden_modules =
    src.llm_service

[importlinter:contract:4]
name = No direct llm_service-framework imports  
type = forbidden
source_modules =
    src.llm_service
forbidden_modules =
    src.framework.orchestration
```

### 1.3 Create Architecture Tests (2.5 hours)

**Create tests/architecture/test_module_dependencies.py:**
```python
"""
Architecture tests for module dependencies.

Validates architectural rules defined in ADRs 042-044.
"""

import pytest
from pytestarch import get_evaluable_architecture, Rule


@pytest.fixture
def architecture():
    """Load architecture for analysis."""
    return get_evaluable_architecture("src", "src")


class TestModuleDependencies:
    """Test module-level architectural rules."""
    
    def test_no_circular_dependencies(self, architecture):
        """Verify no circular dependencies between modules."""
        rule = Rule()
        rule.modules_that().are_sub_modules_of("src.framework").should_not().be_accessed_by_modules_that().are_sub_modules_of("src.llm_service")
        rule.modules_that().are_sub_modules_of("src.llm_service").should_not().be_accessed_by_modules_that().are_sub_modules_of("src.framework")
        
        rule.assert_applies(architecture)
    
    def test_common_is_leaf_module(self, architecture):
        """Verify src.common doesn't import from framework or llm_service."""
        rule = Rule()
        rule.modules_that().are_sub_modules_of("src.common").should_not().import_modules_that().are_sub_modules_of("src.framework")
        rule.modules_that().are_sub_modules_of("src.common").should_not().import_modules_that().are_sub_modules_of("src.llm_service")
        
        rule.assert_applies(architecture)
    
    def test_framework_uses_common(self, architecture):
        """Verify framework imports from common after migration."""
        # This will fail initially (RED phase), pass after migration
        rule = Rule()
        rule.modules_that().are_named("src.framework.orchestration.agent_base").should().import_modules_that().are_named("src.common.types")
        
        rule.assert_applies(architecture)
    
    def test_dashboard_uses_common(self, architecture):
        """Verify dashboard imports from common after migration."""
        # This will fail initially (RED phase), pass after migration
        rule = Rule()
        rule.modules_that().are_named("src.llm_service.dashboard.task_linker").should().import_modules_that().are_named("src.common.task_schema")
        
        rule.assert_applies(architecture)


class TestEnumUsage:
    """Test TaskStatus and FeatureStatus enum usage."""
    
    def test_task_status_enum_exists(self):
        """Verify TaskStatus enum is defined."""
        from src.common.types import TaskStatus
        
        # Verify all expected statuses
        assert TaskStatus.NEW.value == "new"
        assert TaskStatus.ASSIGNED.value == "assigned"
        assert TaskStatus.IN_PROGRESS.value == "in_progress"
        assert TaskStatus.DONE.value == "done"
        assert TaskStatus.ERROR.value == "error"
        assert TaskStatus.BLOCKED.value == "blocked"
    
    def test_feature_status_enum_exists(self):
        """Verify FeatureStatus enum is defined."""
        from src.common.types import FeatureStatus
        
        assert FeatureStatus.DRAFT.value == "draft"
        assert FeatureStatus.PLANNED.value == "planned"
        assert FeatureStatus.IN_PROGRESS.value == "in_progress"
        assert FeatureStatus.IMPLEMENTED.value == "implemented"
    
    def test_agent_identity_type_exists(self):
        """Verify AgentIdentity type is defined."""
        from src.common.types import AgentIdentity, validate_agent
        
        # Verify validation
        assert validate_agent("python-pedro") is True
        assert validate_agent("invalid-agent") is False


class TestTaskSchema:
    """Test unified task schema."""
    
    def test_task_schema_functions_exist(self):
        """Verify task schema functions are defined."""
        from src.common.task_schema import read_task, write_task, load_task_safe
        
        # Functions should be importable
        assert callable(read_task)
        assert callable(write_task)
        assert callable(load_task_safe)
    
    def test_no_duplicate_task_io(self, architecture):
        """Verify no duplicate task I/O implementations after migration."""
        # After migration, only src.common.task_schema should have read/write functions
        rule = Rule()
        
        # Framework should import, not define
        rule.modules_that().are_named("src.framework.orchestration.task_utils").should_not().have_methods_with_name("read_task")
        
        # Dashboard should import, not define  
        rule.modules_that().are_named("src.llm_service.dashboard.task_linker").should_not().have_methods_with_name("load_task")
        
        rule.assert_applies(architecture)
```

**Create tests/architecture/test_type_safety.py:**
```python
"""
Architecture tests for type safety.

Validates type hints and enum usage per ADR-043 and ADR-044.
"""

import ast
import pytest
from pathlib import Path


class TestTypeSafety:
    """Test type safety across codebase."""
    
    def test_no_hardcoded_status_strings(self):
        """Verify no hardcoded status strings after migration."""
        # Scan framework and llm_service for status strings
        forbidden_patterns = [
            '"assigned"',
            '"in_progress"', 
            '"done"',
            '"error"',
        ]
        
        src_files = list(Path("src").rglob("*.py"))
        violations = []
        
        for file_path in src_files:
            if "common/types.py" in str(file_path):
                continue  # Skip enum definitions
            
            content = file_path.read_text()
            for pattern in forbidden_patterns:
                if pattern in content:
                    violations.append(f"{file_path}: Found {pattern}")
        
        # After migration, this should be empty
        assert len(violations) == 0, f"Found hardcoded status strings:\n" + "\n".join(violations)
    
    def test_agent_base_uses_agent_identity(self):
        """Verify AgentBase uses AgentIdentity type."""
        from src.framework.orchestration.agent_base import AgentBase
        import inspect
        
        # Get __init__ signature
        sig = inspect.signature(AgentBase.__init__)
        agent_name_param = sig.parameters.get('agent_name')
        
        # Should have type annotation
        assert agent_name_param is not None
        # After migration, should use AgentIdentity type
        # (This test will evolve during implementation)
```

**Create tests/architecture/conftest.py:**
```python
"""Pytest configuration for architecture tests."""

import pytest


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "architecture: mark test as architecture validation"
    )
```

---

## Phase 2: Create Shared Abstractions (8-12 hours)

### 2.1 Create src/common/ Package (30 min)

```bash
mkdir -p src/common
touch src/common/__init__.py
```

### 2.2 Implement types.py (TDD) (4 hours)

**Test first (RED phase):**
```python
# tests/unit/common/test_types.py

def test_task_status_enum():
    from src.common.types import TaskStatus
    assert TaskStatus.NEW.value == "new"
    # ... all status tests

def test_feature_status_enum():
    # ... all feature status tests

def test_agent_identity_validation():
    from src.common.types import validate_agent
    assert validate_agent("python-pedro") is True
```

**Then implement (GREEN phase):**
```python
# src/common/types.py
# (Implementation from ADR-043 and ADR-044)
```

**Run tests:**
```bash
pytest tests/unit/common/test_types.py -v
```

### 2.3 Implement task_schema.py (TDD) (4 hours)

**Test first (RED phase):**
```python
# tests/unit/common/test_task_schema.py

def test_read_task_valid():
    # Create temp task file
    # Call read_task()
    # Assert correct dict returned

def test_read_task_missing_file():
    # Assert TaskIOError raised

def test_write_task_valid():
    # Write task
    # Read back
    # Assert matches
```

**Then implement (GREEN phase):**
```python
# src/common/task_schema.py
# (Implementation from ADR-042)
```

**Run tests:**
```bash
pytest tests/unit/common/test_task_schema.py -v
```

### 2.4 Run Architecture Tests (Baseline) (30 min)

```bash
# These should FAIL initially (RED phase for architecture tests)
pytest tests/architecture/ -v

# Expected failures:
# - test_framework_uses_common (not migrated yet)
# - test_dashboard_uses_common (not migrated yet)
# - test_no_duplicate_task_io (duplicates still exist)
```

---

## Phase 3: Update Framework Module (6-8 hours)

### 3.1 Update task_utils.py (2 hours)

**Refactor to use shared module:**
```python
# src/framework/orchestration/task_utils.py

from src.common.task_schema import read_task, write_task, TaskIOError
from src.common.types import TaskStatus

# Keep utility functions, remove duplicate I/O
def get_utc_timestamp() -> str:
    # ... existing implementation

def log_event(msg: str) -> None:
    # ... existing implementation
```

**Run tests:**
```bash
pytest tests/framework/orchestration/test_task_utils.py -v
```

### 3.2 Update agent_base.py (3 hours)

**Use TaskStatus enum:**
```python
# src/framework/orchestration/agent_base.py

from src.common.task_schema import read_task, write_task
from src.common.types import TaskStatus, AgentIdentity

class AgentBase(ABC):
    def __init__(self, agent_name: AgentIdentity, ...):
        # ... validation

    def update_task_status(self, status: TaskStatus) -> None:
        self.current_task["status"] = status.value
```

**Run tests:**
```bash
pytest tests/framework/orchestration/test_agent_base.py -v
```

### 3.3 Update agent_orchestrator.py (2 hours)

**Use shared abstractions:**
```python
# src/framework/orchestration/agent_orchestrator.py

from src.common.task_schema import read_task, write_task
from src.common.types import TaskStatus, AgentIdentity
```

**Run tests:**
```bash
pytest tests/framework/orchestration/ -v
```

### 3.4 Validate Framework (1 hour)

```bash
# Run all framework tests
pytest tests/framework/ -v --cov=src/framework

# Run architecture tests (should pass for framework now)
pytest tests/architecture/test_module_dependencies.py::TestModuleDependencies::test_framework_uses_common -v
```

---

## Phase 4: Update LLM Service Module (6-8 hours)

### 4.1 Update task_linker.py (3 hours)

**Remove duplicate load_task():**
```python
# src/llm_service/dashboard/task_linker.py

from src.common.task_schema import read_task, load_task_safe
from src.common.types import TaskStatus

# Remove duplicate load_task() implementation
# Use load_task_safe() instead

def scan_tasks(directory: Path) -> List[Dict]:
    tasks = []
    for path in directory.glob("**/*.yaml"):
        task = load_task_safe(path)
        if task:
            tasks.append(task)
    return tasks
```

**Run tests:**
```bash
pytest tests/unit/dashboard/test_task_linker.py -v
```

### 4.2 Update progress_calculator.py (2 hours)

**Use TaskStatus enum:**
```python
# src/llm_service/dashboard/progress_calculator.py

from src.common.types import TaskStatus

DEFAULT_STATUS_WEIGHTS = {
    TaskStatus.DONE.value: 1.0,
    TaskStatus.IN_PROGRESS.value: 0.5,
    TaskStatus.BLOCKED.value: 0.25,
    TaskStatus.NEW.value: 0.0,
}
```

**Run tests:**
```bash
pytest tests/unit/dashboard/test_progress_calculator.py -v
```

### 4.3 Update spec_parser.py (1 hour)

**Use FeatureStatus enum:**
```python
# src/llm_service/dashboard/spec_parser.py

from src.common.types import FeatureStatus

@dataclass
class SpecificationMetadata:
    status: str  # Validated against FeatureStatus
```

**Run tests:**
```bash
pytest tests/unit/dashboard/test_spec_parser.py -v
```

### 4.4 Validate Dashboard (2 hours)

```bash
# Run all dashboard tests
pytest tests/unit/dashboard/ -v --cov=src/llm_service/dashboard

# Run architecture tests (should pass for dashboard now)
pytest tests/architecture/test_module_dependencies.py::TestModuleDependencies::test_dashboard_uses_common -v

# Manual test: Start dashboard and verify functionality
python -m src.llm_service.dashboard.app
```

---

## Phase 5: Final Validation & Cleanup (2-4 hours)

### 5.1 Run Full Test Suite (1 hour)

```bash
# Unit tests
pytest tests/unit/ -v --cov=src --cov-report=term-missing

# Integration tests
pytest tests/integration/ -v

# Architecture tests (ALL should pass)
pytest tests/architecture/ -v

# import-linter
lint-imports
```

### 5.2 Type Checking (1 hour)

```bash
# Run mypy
mypy src/ --strict

# Fix any type errors
```

### 5.3 Remove Deprecated Code (1 hour)

```bash
# Remove old task I/O implementations
# Verify no remaining status string literals
# Clean up imports
```

### 5.4 Update Documentation (1 hour)

- Update README with architecture testing
- Document src/common/ module
- Update contribution guidelines
- Add architecture decision logs to docs

---

## Success Criteria

### Code Quality
- [ ] All tests passing (unit, integration, architecture)
- [ ] Test coverage >80%
- [ ] mypy passing with --strict
- [ ] import-linter passing all contracts
- [ ] No hardcoded status strings
- [ ] No duplicate task I/O code

### Architecture Tests
- [ ] No circular dependencies validated
- [ ] src/common/ is leaf module validated
- [ ] Framework uses common validated
- [ ] Dashboard uses common validated
- [ ] Enum usage validated
- [ ] Type safety validated

### Performance
- [ ] Task I/O performance ±5% (no regression)
- [ ] Dashboard load time ±5% (no regression)
- [ ] Enum lookup faster than string comparison

### Documentation
- [ ] All 3 ADRs complete
- [ ] Architecture test documentation
- [ ] Migration guide complete
- [ ] Contribution guidelines updated

---

## Rollback Plan

If any phase fails:
1. Git revert to commit before phase
2. Analyze failures
3. Fix issues
4. Re-run tests
5. If unfixable, defer consolidation

**RTO:** <1 hour per phase  
**RPO:** No data loss

---

**Status:** READY TO EXECUTE  
**Agent:** Python Pedro  
**Estimated:** 29-39 hours (including architecture tests)  
**Priority:** IMMEDIATE (per requirements)
