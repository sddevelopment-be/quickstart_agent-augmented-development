# Code Artifacts Refactoring Proposal

**Date:** 2026-02-08  
**Status:** Proposed  
**Goal:** Consolidate code into clear, maintainable structure with sensible boundaries

---

## Problems with Current Structure

1. **Test fragmentation**: tests/ (llm_service tests) vs validation/ (ops tests) - unclear ownership
2. **Fixture duplication**: validation/fixtures/ + examples/prompts/ + validation/test-data/
3. **Framework ambiguity**: framework/ vs ops/ - what's portable vs repo-specific?
4. **Tooling sprawl**: ops/ contains exporters, orchestration, validation, scripts, dashboards
5. **Examples isolation**: examples/prompts/ disconnected from other test fixtures

---

## Proposed Structure: Clear Separation of Concerns

```
repository-root/
│
├── src/                          # Production code only
│   ├── llm_service/             # LLM routing service (current)
│   └── framework/               # Portable framework abstractions (move from root)
│
├── tools/                        # Operational tooling (rename from ops/)
│   ├── exporters/               # Format converters (IR, OpenCode, Copilot)
│   ├── orchestration/           # Agent orchestration examples
│   ├── validation/              # Schema validators
│   ├── dashboards/              # Monitoring dashboards
│   ├── release/                 # Release automation
│   └── scripts/                 # Maintenance scripts
│
├── tests/                        # All tests consolidated
│   ├── unit/                    # Unit tests
│   │   ├── llm_service/        # Tests for src/llm_service/
│   │   ├── framework/          # Tests for src/framework/
│   │   └── tools/              # Tests for tools/ (from validation/)
│   ├── integration/             # Integration tests
│   │   ├── llm_service/
│   │   └── framework/
│   └── fixtures/                # All test data consolidated
│       ├── agents/              # Agent IR/OpenCode/Copilot examples
│       ├── prompts/             # Prompt validation examples (from examples/)
│       ├── configs/             # Configuration samples
│       ├── validators/          # Validation test cases
│       └── schemas/             # JSON schemas
│
└── [keep existing]
    ├── doctrine/                # Framework documentation (no change)
    ├── docs/                    # Repository documentation (no change)
    ├── work/                    # Orchestration workspace (no change)
    └── specifications/          # Feature specs (no change)
```

---

## Key Changes

### 1. Consolidate Production Code → `src/`

**Move:** `framework/` → `src/framework/`

**Rationale:**
- Framework IS production code (used by llm_service and tools)
- Having all production code under src/ clarifies what's deployable
- Matches Python packaging conventions (src layout)

**Impact:**
- Update imports: `from framework.core import Task` → `from src.framework.core import Task`
- Update setup.py/pyproject.toml to include src/framework/
- Low risk: Only import path changes

---

### 2. Rename `ops/` → `tools/`

**Rationale:**
- "ops" suggests operational infrastructure (CI/CD, deployment)
- "tools" better describes utilities for development and automation
- More accurate: these are scripts/utilities, not infrastructure

**Impact:**
- Update references in documentation
- Update CI/CD paths
- Low risk: Directory rename only

---

### 3. Consolidate All Tests → `tests/`

**Structure:**
```
tests/
├── unit/
│   ├── llm_service/          # From tests/unit/
│   ├── framework/            # From validation/framework/
│   └── tools/                # From validation/ (all ops tests)
│       ├── exporters/        # From validation/agent_exports/
│       ├── orchestration/    # From validation/test_*.py
│       ├── validation/       # From validation/validator/
│       ├── release/          # From validation/release/
│       └── dashboards/       # From validation/dashboards/
├── integration/
│   ├── llm_service/          # From tests/integration/
│   └── framework/            # From validation/framework/
└── fixtures/                 # All test data
```

**Rationale:**
- Single source of truth: all tests in one place
- Structure mirrors src/ and tools/ directories
- Easy to understand: tests/unit/X/ tests src/X/ or tools/X/

**Impact:**
- Move ~22 test files from validation/ to tests/unit/tools/
- Update test discovery paths in pytest.ini
- Update CI test commands
- Medium risk: Import paths change, CI needs updates

---

### 4. Consolidate Test Fixtures → `tests/fixtures/`

**Before (scattered):**
```
validation/fixtures/agents/       # Agent examples
validation/fixtures/ir/           # IR samples
validation/fixtures/opencode/     # OpenCode samples
validation/fixtures/copilot/      # Copilot samples
validation/test-data/             # Config samples
examples/prompts/                 # Prompt examples
```

**After (consolidated):**
```
tests/fixtures/
├── agents/                       # All agent format examples
│   ├── architect-alphonso.ir.json
│   ├── architect-alphonso.opencode.json
│   ├── architect-alphonso.copilot-skill.json
│   ├── backend-benny.ir.json
│   ├── backend-benny.opencode.json
│   └── backend-benny.copilot-skill.json
├── prompts/                      # From examples/prompts/
│   ├── valid-deployment-task.yaml
│   ├── invalid-bug-fix.yaml
│   └── README.md
├── configs/                      # From validation/test-data/
│   ├── valid-config.json
│   └── invalid-config.json
├── validators/                   # From validation/fixtures/validator/
│   ├── valid.json
│   └── invalid.json
└── schemas/                      # JSON schemas
    └── prompt-schema.json
```

**Rationale:**
- Single location for all test data
- Easier to maintain: no duplication
- Clear: tests/fixtures/ contains data for tests/

**Impact:**
- Move ~30 fixture files
- Update fixture import paths in tests
- Update CI/CD fixture references
- Medium risk: Many import updates needed

---

## Migration Plan

### Phase 1: Documentation & Preparation (Low Risk)

**Tasks:**
1. Create tests/README.md explaining new structure
2. Create tools/README.md (rename from ops/README.md)
3. Document fixture locations in tests/fixtures/README.md
4. Add migration checklist

**Effort:** 1 hour  
**Risk:** None - documentation only

---

### Phase 2: Move Framework Code (Low-Medium Risk)

**Tasks:**
1. Move framework/ → src/framework/
2. Update imports in llm_service
3. Update imports in tools/ (ops/)
4. Update pyproject.toml/setup.py
5. Run full test suite

**Effort:** 2-3 hours  
**Risk:** Medium - Import changes, but automated with IDE refactoring

**Commands:**
```bash
# Move directory
git mv framework src/framework

# Update imports with sed (or IDE refactoring)
find . -name "*.py" -exec sed -i 's/from framework\./from src.framework./g' {} \;
find . -name "*.py" -exec sed -i 's/import framework/import src.framework/g' {} \;

# Test
python -m pytest tests/
```

---

### Phase 3: Rename ops/ → tools/ (Low Risk)

**Tasks:**
1. Rename directory: ops/ → tools/
2. Update CI/CD paths (.github/workflows/)
3. Update package.json scripts
4. Update documentation references

**Effort:** 1 hour  
**Risk:** Low - Simple rename, easy to verify

**Commands:**
```bash
# Rename
git mv ops tools

# Update references
grep -rl "ops/" . --include="*.md" --include="*.yml" --include="*.yaml" | xargs sed -i 's|ops/|tools/|g'
```

---

### Phase 4: Consolidate Tests (Medium Risk)

**Tasks:**
1. Create tests/unit/tools/ directory
2. Move validation test files to appropriate locations:
   - validation/test_*.py → tests/unit/tools/orchestration/
   - validation/agent_exports/ → tests/unit/tools/exporters/
   - validation/framework/ → tests/unit/framework/
   - validation/model_router/ → tests/unit/framework/
3. Update pytest.ini test discovery paths
4. Update CI test commands
5. Run full test suite

**Effort:** 3-4 hours  
**Risk:** Medium - Many moves, import updates needed

**Validation:**
```bash
# Verify test discovery
python -m pytest --collect-only

# Run all tests
python -m pytest tests/ -v

# Verify coverage
python -m pytest tests/ --cov=src --cov=tools
```

---

### Phase 5: Consolidate Fixtures (Medium Risk)

**Tasks:**
1. Create tests/fixtures/ structure
2. Move fixture files:
   - validation/fixtures/agents/* → tests/fixtures/agents/
   - validation/fixtures/ir/* → tests/fixtures/agents/ (merge)
   - validation/fixtures/opencode/* → tests/fixtures/agents/ (merge)
   - validation/fixtures/copilot/* → tests/fixtures/agents/ (merge)
   - examples/prompts/* → tests/fixtures/prompts/
   - validation/test-data/* → tests/fixtures/configs/
3. Update fixture imports in all tests
4. Update CI fixture paths
5. Remove old validation/ directory

**Effort:** 4-5 hours  
**Risk:** Medium - Many import updates, CI changes

**Validation:**
```bash
# Search for old fixture paths
grep -r "validation/fixtures" tests/
grep -r "examples/prompts" .

# Run tests
python -m pytest tests/ -v
```

---

### Phase 6: Cleanup & Verification (Low Risk)

**Tasks:**
1. Remove empty directories (validation/, examples/)
2. Update .gitignore if needed
3. Update REPO_MAP.md
4. Run full CI/CD pipeline
5. Update onboarding documentation

**Effort:** 1 hour  
**Risk:** Low - Cleanup only

---

## Benefits of This Refactoring

### 1. Clear Boundaries
✅ **Production code:** `src/` (llm_service + framework)  
✅ **Development tools:** `tools/` (exporters, orchestration, scripts)  
✅ **All tests:** `tests/` with clear unit/integration split  
✅ **All test data:** `tests/fixtures/` in one place

### 2. Predictable Structure
- Want to test src/framework/? → tests/unit/framework/
- Want to test tools/exporters/? → tests/unit/tools/exporters/
- Need agent fixtures? → tests/fixtures/agents/
- Need prompt examples? → tests/fixtures/prompts/

### 3. Reduced Confusion
- No more "where do tests for X go?" → tests/unit/X/
- No more "where's the fixture for Y?" → tests/fixtures/Y/
- No more "is this framework or tooling?" → src/ vs tools/

### 4. Easier Maintenance
- Add new tool → tools/new_tool/ + tests/unit/tools/new_tool/
- Add new fixture → tests/fixtures/
- All test data in one place → easier to update

### 5. Standard Python Layout
- Matches Python packaging best practices (src layout)
- Familiar to Python developers
- Easier to package and distribute

---

## Summary Comparison

| Aspect | Before | After |
|--------|--------|-------|
| **Production code** | src/ + framework/ (split) | src/ (consolidated) |
| **Test location** | tests/ + validation/ (fragmented) | tests/ (unified) |
| **Test fixtures** | validation/fixtures/ + examples/ (scattered) | tests/fixtures/ (consolidated) |
| **Tooling** | ops/ (unclear) | tools/ (clear purpose) |
| **Framework location** | Root level | src/framework/ (with production code) |
| **Examples** | Isolated in examples/ | Integrated as tests/fixtures/prompts/ |

---

## Risk Assessment

| Phase | Risk Level | Mitigation |
|-------|-----------|------------|
| Phase 1 (Docs) | None | Documentation only |
| Phase 2 (Framework move) | Medium | IDE refactoring, automated tests |
| Phase 3 (Rename ops) | Low | Simple rename, easy rollback |
| Phase 4 (Test consolidation) | Medium | Careful validation, incremental moves |
| Phase 5 (Fixture consolidation) | Medium | Update references incrementally |
| Phase 6 (Cleanup) | Low | Verification step |

**Overall Risk:** Medium (manageable with careful execution)  
**Overall Benefit:** High (clarity, maintainability, standards compliance)

---

## Effort Estimate

- **Phase 1:** 1 hour
- **Phase 2:** 2-3 hours
- **Phase 3:** 1 hour
- **Phase 4:** 3-4 hours
- **Phase 5:** 4-5 hours
- **Phase 6:** 1 hour

**Total:** 12-15 hours (1.5-2 days)

---

## Alternative: Minimal Refactoring

If full refactoring is too risky, a minimal approach:

1. **Just consolidate fixtures:**
   - Move examples/prompts/ → validation/fixtures/prompts/
   - Move validation/test-data/ → validation/fixtures/configs/
   - Effort: 2 hours, Low risk

2. **Just document boundaries:**
   - Add READMEs explaining structure
   - Add comments in framework/ vs ops/
   - Effort: 1 hour, No risk

This achieves 40% of the benefit with 20% of the effort.

---

## Recommendation

**Full refactoring** is worth the investment because:
1. Structure is confusing to new contributors
2. Test organization will only get worse as codebase grows
3. Framework portability requires clear boundaries
4. One-time effort provides long-term maintainability

**Preferred approach:** Execute phases sequentially with validation between each phase. Can pause/rollback at any phase boundary.

**Start with:** Phase 1 (docs) + Phase 3 (rename ops) as low-risk wins, then assess before continuing.
