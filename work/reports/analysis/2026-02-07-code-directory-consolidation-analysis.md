# Code Directory Consolidation Analysis

**Date:** 2026-02-07  
**Status:** Proposed  
**Scope:** ops/, validation/, src/, tests/, framework/ directories

---

## Executive Summary

Analysis of repository code structure revealed three major organizational issues:
1. Test directory fragmentation across `tests/` and `validation/`
2. Unclear boundaries between portable framework code and repo-specific implementation
3. Test fixture duplication across multiple locations

Proposed 4-phase consolidation strategy focuses on reorganization without risky code moves.

---

## Current State

### Directory Inventory

| Directory | Files | Purpose | Test Location |
|-----------|-------|---------|---------------|
| **src/** | 78 files | LLM Service production code | tests/unit/, tests/integration/ |
| **framework/** | 20 files | Framework core abstractions | validation/framework/ |
| **tests/** | 96 files | llm_service unit/integration tests | — |
| **validation/** | 70 files | Tests for ops/ code + fixtures | — |
| **ops/** | 80 files | Operational scripts & tools | validation/ (scattered) |

### Identified Issues

#### Issue 1: Test Directory Fragmentation

**Problem:** Tests split across 3 locations with unclear boundaries:
- `tests/` → Tests for `src/llm_service` code (unit + integration) ✅ Clear
- `validation/` → Tests for `ops/` code (scattered) ⚠️ Unclear structure
- `validation/framework/` → Tests for `framework/` code ⚠️ Inconsistent

**Impact:**
- Confusing when adding new tests
- Unclear which directory to update when making changes
- Hard to maintain test coverage

**Example:**
```
ops/orchestration/agent_orchestrator.py
  → Tests in validation/test_agent_orchestrator.py (root)
  
ops/exporters/copilot-generator.js
  → Tests in validation/agent_exports/test_copilot_generator.py
  
framework/execution/model_router.py
  → Tests in validation/model_router/test_model_router.py
```

#### Issue 2: Framework vs Implementation Confusion

**Problem:** Core framework concepts exist in multiple places without clear boundaries:
- `framework/core.py` → Task/Agent/TaskStatus abstractions (portable)
- `ops/orchestration/` → agent_orchestrator.py, task_utils.py (uses framework)
- `ops/framework-core/` → load_directives.py, template-status-checker.py (utilities)

**Impact:**
- Unclear what's reusable framework vs repo-specific implementation
- Potential duplication as code evolves
- Hard to extract framework for use in other projects

**Current Locations:**
```
framework/
├── core.py              # Portable: TaskStatus, AgentProfile, Task classes
├── execution.py         # Portable: Model routing abstractions
└── interface.py         # Portable: Framework client interface

ops/orchestration/
├── agent_orchestrator.py   # Repo-specific: Example implementation
└── task_utils.py           # Repo-specific: Helper utilities

ops/framework-core/
├── load_directives.py      # Repo-specific: Loads from local structure
└── template-status-checker.py  # Repo-specific: Validation utility
```

#### Issue 3: Test Fixture Duplication

**Problem:** Test data exists in multiple locations:
- `validation/fixtures/` → Agent IR/OpenCode examples, validator samples
- `validation/test-data/` → Config JSON files
- `validation/fixtures/agents/`, `validation/fixtures/ir/`, `validation/fixtures/opencode/` → Agent examples (subdirectories)

**Impact:**
- Hard to maintain; changes must be synchronized
- Unclear which is authoritative
- Duplicated JSON schemas and sample data

---

## Proposed Consolidation Strategy

### Phase 1: Reorganize validation/ to Mirror ops/ Structure

**Goal:** Make test location predictable by mirroring source structure.

**Changes:**
```diff
validation/
├── README.md                  # Add: Clarify purpose and structure
├── fixtures/                  # Keep: Shared test data
+ ├── orchestration/           # NEW: Move scattered orchestration tests here
+ │   ├── test_agent_orchestrator.py  # From validation/ root
+ │   ├── test_orchestration_e2e.py   # From validation/ root
+ │   ├── test_task_age_checker.py    # From validation/ root
+ │   └── test_task_utils.py          # From validation/ root
├── agent_exports/            # Keep: Tests for ops/exporters/
├── framework-core/           # Keep: Tests for ops/framework-core/
├── model_router/             # Keep: Tests for framework/execution/model_router.py
├── release/                  # Keep: Tests for ops/release/
├── maintenance/              # Keep: Tests for ops/scripts/maintenance/
├── dashboards/               # Keep: Tests for ops/dashboards/
└── framework/                # Keep: Tests for framework/ core interfaces
```

**Benefit:** Validation directory structure mirrors ops/ for easier navigation.

**Risk:** Low - Only moving test files, not changing imports significantly.

---

### Phase 2: Document Framework vs Implementation Boundaries

**Goal:** Clarify what's portable vs repo-specific without moving code.

**Changes:**
1. Add `framework/README.md`:
   ```markdown
   # Framework Core Abstractions
   
   **Purpose:** Portable framework components for agent orchestration.
   
   **What belongs here:**
   - Abstract interfaces (Task, Agent, TaskStatus)
   - Model routing and execution abstractions
   - Framework client interfaces
   
   **What doesn't belong here:**
   - Repo-specific implementations → `ops/orchestration/`
   - Repo-specific utilities → `ops/framework-core/`
   ```

2. Add comments to key files:
   ```python
   # framework/core.py
   """
   Portable framework abstractions.
   Used by both llm_service and ops/ tools.
   """
   
   # ops/orchestration/agent_orchestrator.py
   """
   Example implementation of agent orchestration using framework/core.
   Repo-specific: Uses local file structure and conventions.
   """
   ```

**Benefit:** Clear boundaries without code moves.

**Risk:** Very low - Documentation only.

---

### Phase 3: Consolidate Test Fixtures

**Goal:** Single source of truth for all test data.

**Changes:**
```diff
validation/fixtures/
+ ├── agents/              # NEW: Consolidate agent examples
+ │   ├── architect-alphonso.ir.json      # From validation/fixtures/ir/
+ │   ├── architect-alphonso.opencode.json  # From validation/fixtures/opencode/
+ │   ├── architect-alphonso.copilot-skill.json  # From validation/fixtures/copilot/
+ │   ├── backend-benny.ir.json
+ │   ├── backend-benny.opencode.json
+ │   └── backend-benny.copilot-skill.json
+ ├── validators/         # NEW: Rename validation/fixtures/validator/ → here
+ │   ├── valid.json
+ │   ├── invalid.json
+ │   └── malformed.json
+ ├── configs/            # NEW: Move validation/test-data/ → here
+ │   ├── valid-config.json
+ │   ├── invalid-config.json
+ │   └── realistic_example.json
- ├── ir/                # REMOVE: Merge into agents/
- ├── opencode/          # REMOVE: Merge into agents/
- ├── copilot/           # REMOVE: Merge into agents/
- └── validator/         # REMOVE: Rename to validators/
```

**Benefit:** Centralized, easier to maintain, clearer organization.

**Risk:** Low-Medium - Will need to update test imports.

---

### Phase 4: Document tests/ Directory Clearly

**Goal:** Make it obvious that tests/ is only for src/llm_service.

**Changes:**
1. Add `tests/README.md`:
   ```markdown
   # LLM Service Tests
   
   **Purpose:** Tests for `src/llm_service/` code only.
   
   **Structure:**
   - `unit/` → No external dependencies
   - `integration/` → Requires services, file systems
   - `fixtures/` → Shared test helpers (fake_claude_cli, etc.)
   
   **For other code:**
   - Tests for `ops/` code → See `validation/` directory
   - Tests for `framework/` code → See `validation/framework/`
   ```

**Benefit:** Clear documentation prevents confusion.

**Risk:** None - Documentation only.

---

## Summary: What Goes Where

| Code Type | Location | Test Location | Purpose |
|-----------|----------|---------------|---------|
| LLM Service | `src/llm_service/` | `tests/unit/`, `tests/integration/` | Production service code |
| Framework abstractions | `framework/` | `validation/framework/` | Portable runtime abstractions |
| Orchestration examples | `ops/orchestration/` | `validation/orchestration/` | Shows framework usage |
| Exporters | `ops/exporters/` | `validation/agent_exports/` | Format conversion tools |
| Release tools | `ops/release/` | `validation/release/` | Deployment automation |
| Operational utilities | `ops/` | `validation/` (mirrored) | Repo-specific helpers |
| Test fixtures | `validation/fixtures/` | — | Shared across all test suites |

---

## Key Benefits

✅ **Clear boundaries:** Each test directory has single responsibility  
✅ **Reduced confusion:** validation/ structure mirrors ops/ structure  
✅ **Better maintainability:** Test fixtures centralized  
✅ **Distinguishes portable vs repo-specific:** Comments clarify framework vs implementation  
✅ **Supports growth:** Structure scales as new ops/ tools are added  
✅ **No risky moves:** Mostly reorganization, not refactoring

---

## Implementation Estimate

| Phase | Effort | Risk | Files Affected |
|-------|--------|------|----------------|
| Phase 1 | 1-2 hours | Low | ~10 test files moved |
| Phase 2 | 30 minutes | Very low | 3 README files + comments |
| Phase 3 | 2-3 hours | Low-Medium | ~30 fixture files moved, test imports updated |
| Phase 4 | 15 minutes | None | 1 README file |

**Total:** ~4-6 hours of work

---

## Next Steps

1. **Review this analysis** with team/maintainer
2. **Phase 1:** Reorganize validation/ (lowest risk, highest clarity gain)
3. **Phase 2:** Add documentation (no code changes)
4. **Phase 3:** Consolidate fixtures (update test imports)
5. **Phase 4:** Document tests/ (final clarification)

---

## Appendix: Detailed File Inventory

### ops/ (80 files)
```
ops/
├── exporters/              # 15 files - IR/OpenCode/Copilot generators
├── orchestration/          # 10 files - Agent orchestration examples
├── release/                # 8 files - Deployment automation
├── framework-core/         # 6 files - Directive/template utilities
├── dashboards/             # 5 files - Monitoring dashboards
├── scripts/                # 12 files - Maintenance scripts
├── portability/            # 4 files - OpenCode conversion
└── common/                 # 20 files - Shared utilities
```

### validation/ (70 files)
```
validation/
├── fixtures/               # 40 files - Test data (agents, configs, schemas)
├── agent_exports/          # 8 files - Tests for ops/exporters/
├── framework-core/         # 6 files - Tests for ops/framework-core/
├── model_router/           # 4 files - Tests for framework/execution/
├── release/                # 3 files - Tests for ops/release/
├── test_*.py               # 9 files - Scattered root-level tests
└── (other)                 # Various subdirectories
```

### src/ (78 files)
```
src/llm_service/
├── adapters/               # 15 files - LLM provider adapters
├── config/                 # 8 files - Configuration management
├── templates/              # 12 files - Prompt templates
├── dashboard/              # 10 files - Web dashboard
├── ui/                     # 5 files - Console UI
├── telemetry/              # 8 files - Logging and metrics
└── utils/                  # 20 files - Shared utilities
```

### tests/ (96 files)
```
tests/
├── unit/                   # 60 files - Fast, isolated tests
├── integration/            # 30 files - End-to-end tests
└── fixtures/               # 6 files - Shared test helpers
```

### framework/ (20 files)
```
framework/
├── core/                   # 5 files - Task/Agent abstractions
├── execution/              # 8 files - Model routing
└── interface/              # 7 files - Framework clients
```
