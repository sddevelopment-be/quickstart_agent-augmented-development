# Distribution & Exporter Path Compatibility Analysis

**Date:** 2026-02-08  
**Agent:** DevOps Danny  
**Context:** Post-refactoring compatibility review for distribution/exporter infrastructure  

---

## Executive Summary

⚠️ **CRITICAL ISSUES IDENTIFIED** - Multiple hardcoded paths to old structure locations found across distribution scripts, workflows, and configuration files.

**Impact Assessment:**
- 🔴 **HIGH**: Release packaging will fail (references `ops/release/` scripts that moved to `tools/release/`)
- 🔴 **HIGH**: GitHub workflows reference non-existent `validation/` and `examples/prompts/` paths
- 🟡 **MEDIUM**: Exporter scripts reference `docs/templates/prompts/` (may still exist but duplicated in `doctrine/`)
- 🟡 **MEDIUM**: Jest configuration references old `ops/` paths

---

## Refactoring Context

### Completed Migrations
1. **ops/** → split between:
   - **src/framework/** (production code)
   - **tools/** (development tooling)

2. **validation/** → split between:
   - **tests/** (test code)
   - **fixtures/** (test data)

3. **examples/prompts/** → **fixtures/prompts/**

---

## Critical Findings

### 1. ❌ Release Packaging Scripts (HIGH PRIORITY)

#### Issue: Hardcoded `ops/release/` paths in distribution configuration

**File:** `tools/release/distribution-config.yaml`

```yaml
# Lines 114-119
scripts:
- path: ops/release/framework_install.sh  # ❌ OLD PATH
  description: Installation script
  required: true
- path: ops/release/framework_upgrade.sh  # ❌ OLD PATH
  description: Upgrade script
  required: true
```

**Actual Location:** `tools/release/framework_install.sh` ✅ (confirmed exists)

**Impact:**
- Release artifact builder will fail to find installation scripts
- Packaged releases will be incomplete
- Downstream installations will fail

**Recommendation:**
```yaml
scripts:
- path: tools/release/framework_install.sh  # ✅ CORRECT PATH
  description: Installation script
  required: true
- path: tools/release/framework_upgrade.sh  # ✅ CORRECT PATH
  description: Upgrade script
  required: true
```

---

#### Issue: Build script references old `ops/release/` paths

**File:** `tools/release/build_release_artifact.py`

```python
# Line 66-67
SCRIPTS_TO_INCLUDE = [
    "ops/release/framework_install.sh",  # ❌ OLD PATH
    "ops/release/framework_upgrade.sh",  # ❌ OLD PATH
]
```

**Recommendation:**
```python
SCRIPTS_TO_INCLUDE = [
    "tools/release/framework_install.sh",  # ✅ CORRECT PATH
    "tools/release/framework_upgrade.sh",  # ✅ CORRECT PATH
]
```

**Note:** The script has a config file override mechanism, so fixing `distribution-config.yaml` may be sufficient, but the default fallback should also be updated for consistency.

---

### 2. ❌ GitHub Workflows (HIGH PRIORITY)

#### Issue: References to non-existent `validation/` directory

**Files Affected:**
- `.github/workflows/validate-prompts.yml` (lines 9-10)
- `.github/workflows/test-ops-changes.yml` (lines 7, 13, 53, 62, 118)
- `.github/workflows/pr-quality-gate.yml` (lines 44, 58, 77, 83, 119, 190, 364)
- `.github/workflows/validation.yml` (lines 41, 72, 94, 102, 114, 212-214)

**Example from `validate-prompts.yml`:**
```yaml
paths:
  - 'examples/prompts/**.yaml'  # ❌ MOVED TO fixtures/prompts
  - 'ops/validation/prompt-validator*.js'  # ❌ MOVED TO tools/validators
  - 'validation/schemas/prompt-schema.json'  # ❌ MOVED TO fixtures/schemas
```

**Example from `pr-quality-gate.yml` (lines 44, 58):**
```bash
# Black formatting check
black --check validation/ ops/orchestration/ ops/portability/ ...
# ❌ validation/ doesn't exist
# ❌ ops/orchestration, ops/portability moved to src/framework/

# Ruff linting check
ruff check validation/ ops/orchestration/ ops/portability/ ...
# ❌ Same issues
```

**Example from `test-ops-changes.yml`:**
```yaml
on:
  push:
    paths:
      - 'ops/**'  # ❌ Most code moved to src/framework/ or tools/
      - 'validation/**'  # ❌ Moved to tests/
```

**Example from `validation.yml`:**
```bash
# Line 41
bash validation/validate-work-structure.sh  # ❌ Moved to tests/

# Line 72
python validation/validate-task-schema.py "$file"  # ❌ Moved to tests/

# Lines 102, 114
validation/test_orchestration_e2e.py  # ❌ Moved to tests/
```

**Impact:**
- CI/CD workflows will fail
- Quality gates won't run
- PR validation will be incomplete
- E2E tests won't execute

**Recommendations:**

1. **For workflow triggers:**
```yaml
on:
  push:
    paths:
      - 'src/framework/**'  # Production code
      - 'tools/**'           # Development tools
      - 'tests/**'           # Test code
```

2. **For test commands:**
```bash
# OLD
python validation/validate-task-schema.py
bash validation/validate-work-structure.sh

# NEW
python tests/validation/validate-task-schema.py
bash tests/validation/validate-work-structure.sh
```

3. **For linting:**
```bash
# OLD
black --check validation/ ops/orchestration/ ops/portability/

# NEW
black --check tests/ src/framework/ tools/
```

---

### 3. ⚠️ Exporter Scripts (MEDIUM PRIORITY)

#### Issue: `docs/templates/prompts/` reference (may be duplicate)

**Files Affected:**
- `tools/scripts/deploy-skills.js` (line 33, 640, 642)
- `tools/scripts/skills-exporter.js` (line 23)
- `tools/validators/prompt-validator-cli.js` (usage examples)

**Example from `deploy-skills.js`:**
```javascript
// Line 33
const PROMPTS_SOURCE_DIR = path.join(__dirname, '..', 'docs', 'templates', 'prompts');
// ⚠️ May be duplicate - prompts exist in doctrine/templates/prompts/
```

**Verification Needed:**
- Check if `docs/templates/prompts/` still exists
- Determine canonical location: `doctrine/templates/prompts/` OR `docs/templates/prompts/`
- If both exist, identify which is authoritative

**Current State:**
- `doctrine/templates/prompts/` ✅ EXISTS (confirmed 200+ KB of prompt files)
- `docs/templates/prompts/` ❓ UNKNOWN (needs verification)

**Recommendation:**
1. Verify which directory is canonical
2. If `doctrine/templates/prompts/` is canonical, update references:
```javascript
const PROMPTS_SOURCE_DIR = path.join(__dirname, '..', 'doctrine', 'templates', 'prompts');
```

---

### 4. ⚠️ Jest Configuration (MEDIUM PRIORITY)

#### Issue: Coverage collection from old `ops/` paths

**File:** `jest.config.js`

```javascript
// Lines 4-8
collectCoverageFrom: [
  'ops/exporters/**/*.js',  // ❌ MOVED TO tools/exporters/
  'ops/deploy-skills.js',   // ❌ MOVED TO tools/scripts/deploy-skills.js
  '!ops/exporters/**/*.test.js',
  '!ops/__tests__/**/*.js'
],

// Lines 18-21
testMatch: [
  '**/validation/agent_exports/**/*.test.js',  // ❌ validation/ moved
  '**/ops/__tests__/**/*.test.js'              // ❌ ops/ moved
],
```

**Recommendation:**
```javascript
collectCoverageFrom: [
  'tools/exporters/**/*.js',
  'tools/scripts/deploy-skills.js',
  '!tools/exporters/**/*.test.js',
  '!tools/__tests__/**/*.js'
],

testMatch: [
  '**/tests/integration/exporters/**/*.test.js',
  '**/tools/__tests__/**/*.test.js'
],
```

---

### 5. ⚠️ Package.json Scripts (MEDIUM PRIORITY)

#### Issue: Script paths reference old locations

**File:** `package.json`

```json
// Lines 34-37 - Validation scripts using fixtures/ path
"validate:prompts": "node tools/validators/prompt-validator-cli.js fixtures/prompts",
// ✅ CORRECT - fixtures/prompts exists

// Line 38 - Reference to old ops/ path in commented/legacy script
"test:anchors": "node ops/scripts/test-markua-anchors.mjs",
// ❌ ops/scripts moved to tools/scripts
```

**Recommendation:**
```json
"test:anchors": "node tools/scripts/test-markua-anchors.mjs",
```

---

### 6. ⚠️ Python Path Utilities (LOW PRIORITY - Documentation)

#### Issue: Comments reference old `ops/` structure

**File:** `tools/common/path_utils.py`

```python
# Lines 10-11
"""
Assumes scripts are in ops/* subdirectories, so repo root is 2-3 levels up.
# ⚠️ Outdated comment - scripts now in tools/*
"""

# Lines 18-30
# From ops/subdir/script.py -> go up 3 levels
# From ops/script.py -> go up 2 levels
current = Path(current_file).resolve()

# Check if we're in ops/subdir/
if current.parent.parent.name == "ops":  # ❌ Should check "tools"
    return current.parent.parent.parent
# Check if we're in ops/
elif current.parent.name == "ops":  # ❌ Should check "tools"
    return current.parent.parent
```

**Recommendation:**
- Update comments to reference `tools/` instead of `ops/`
- Update logic to check for `"tools"` instead of `"ops"`
- Maintain backward compatibility if scripts still exist in both locations

---

### 7. 🟢 Distribution Config - Outdated Directory References (INFORMATIONAL)

#### Issue: Distribution config references old `ops/` subdirectories

**File:** `tools/release/distribution-config.yaml` (lines 39-71)

```yaml
core_directories:
  # ... other directories ...
  - path: ops/common          # ❌ MOVED TO tools/common
  - path: ops/config          # ❌ MOVED TO src/framework/config
  - path: ops/dashboards      # ❌ MOVED TO tools/dashboards
  - path: ops/exporters       # ❌ MOVED TO tools/exporters
  - path: ops/framework-core  # ❌ MOVED TO src/framework/
  - path: ops/orchestration   # ❌ MOVED TO src/framework/orchestration
  - path: ops/planning        # ❌ MOVED TO tools/planning
  - path: ops/portability     # ❌ MOVED TO src/framework/portability
  - path: ops/scripts         # ❌ MOVED TO tools/scripts
  - path: ops/utils           # ❌ MOVED TO tools/common or src/framework/utils
  - path: ops/validation      # ❌ MOVED TO tests/ and fixtures/
```

**Note:** These paths define what gets included in release artifacts. If the refactoring is complete, these directories won't exist and won't be packaged (non-fatal but creates warning noise).

**Recommendation:**
Update to new structure:
```yaml
core_directories:
  # Production code
  - path: src/framework
    description: 'Core framework production code'
    required: true
  
  # Development tools
  - path: tools/exporters
    description: 'Export generation tools'
    required: false
  - path: tools/dashboards
    description: 'Metrics and monitoring dashboards'
    required: false
  - path: tools/scripts
    description: 'Utility scripts'
    required: false
  
  # Test infrastructure
  - path: tests
    description: 'Test suites'
    required: false
  - path: fixtures
    description: 'Test fixtures and reference data'
    required: false
```

---

## Files Requiring Updates

### 🔴 Critical (Blocks Release/CI)

1. **tools/release/distribution-config.yaml**
   - Lines 114-119: Update script paths from `ops/release/` to `tools/release/`
   - Lines 39-71: Update core_directories from `ops/*` to `src/framework/`, `tools/*`, `tests/`

2. **tools/release/build_release_artifact.py**
   - Lines 66-67: Update SCRIPTS_TO_INCLUDE paths

3. **.github/workflows/validate-prompts.yml**
   - Line 8: Change `examples/prompts/` to `fixtures/prompts/`
   - Line 9: Change `ops/validation/` to `tools/validators/`
   - Line 10: Change `validation/schemas/` to `fixtures/schemas/`

4. **.github/workflows/test-ops-changes.yml**
   - Lines 7, 13: Update trigger paths from `ops/**`, `validation/**` to new structure
   - Lines 53, 62, 118: Update test command paths from `validation/` to `tests/`

5. **.github/workflows/pr-quality-gate.yml**
   - Lines 44, 58: Update Black/Ruff paths from `validation/ ops/...` to `tests/ src/framework/ tools/`
   - Lines 77, 83: Update error messages with correct paths
   - Lines 119, 190: Update pytest paths from `validation/` to `tests/`

6. **.github/workflows/validation.yml**
   - Lines 41, 94: Update shell script paths from `validation/` to `tests/validation/`
   - Lines 72, 102, 114: Update Python script paths from `validation/` to `tests/`
   - Lines 212-214: Update help text with correct paths

### 🟡 Important (Affects Exporters)

7. **tools/scripts/deploy-skills.js**
   - Line 33: Verify and update PROMPTS_SOURCE_DIR if needed

8. **tools/scripts/skills-exporter.js**
   - Line 23: Verify and update PROMPTS_DIR if needed

9. **tools/validators/prompt-validator-cli.js**
   - Update usage examples if needed

10. **jest.config.js**
    - Lines 4-8: Update collectCoverageFrom from `ops/` to `tools/`
    - Lines 18-21: Update testMatch from `validation/` and `ops/` to new paths

### 🟢 Nice-to-Have (Documentation/Comments)

11. **tools/common/path_utils.py**
    - Lines 10-30: Update comments and logic from `ops/` to `tools/`

12. **package.json**
    - Line 38: Update `test:anchors` script path

---

## Manual Testing Recommendations

### Test 1: Release Artifact Build
```bash
# DRY RUN (safe, won't create files)
cd tools/release
python build_release_artifact.py --version 1.0.0-test --dry-run

# Expected: Should find all files without errors
# Watch for: Missing script warnings
```

### Test 2: Exporter Pipeline
```bash
# Export skills
npm run export:skills

# Expected: Should complete without file-not-found errors
# Verify: dist/skills/ populated

# Deploy skills
npm run deploy:all

# Expected: Should deploy to .claude/, .github/instructions/, .opencode/
# Verify: Deployment targets populated
```

### Test 3: Validation Workflows (Local)
```bash
# Simulate workflow validation steps
cd tests/validation  # IF EXISTS

# Run validation scripts
bash validate-work-structure.sh
python validate-task-schema.py ../fixtures/prompts/valid-deployment-task.yaml

# Run pytest tests
pytest test_orchestration_e2e.py -v
```

### Test 4: Jest Tests
```bash
# Run all integration tests
npm run test:exporters

# Expected: Tests should find and execute correctly
# Watch for: Path resolution errors
```

---

## Recommended Action Plan

### Phase 1: Critical Fixes (Block Release)
1. ✅ Update `tools/release/distribution-config.yaml` script paths
2. ✅ Update `tools/release/build_release_artifact.py` default paths
3. ✅ Run dry-run release build: `python build_release_artifact.py --version test-$(date +%Y%m%d) --dry-run`
4. ✅ Verify no missing file warnings

### Phase 2: CI/CD Workflows
5. ✅ Update all `.github/workflows/*.yml` files with new paths
6. ✅ Update workflow trigger paths
7. ✅ Update test command paths
8. ✅ Commit workflow fixes in single atomic change
9. ⚠️ **DO NOT MERGE TO MAIN** - Test in feature branch first
10. ✅ Trigger workflows manually to verify

### Phase 3: Exporter Infrastructure
11. ✅ Verify prompt template canonical location (`doctrine/` vs `docs/`)
12. ✅ Update exporter script paths if needed
13. ✅ Update jest.config.js paths
14. ✅ Run full test suite: `npm test && npm run test:exporters`

### Phase 4: Documentation & Polish
15. ✅ Update path_utils.py comments and logic
16. ✅ Update package.json script paths
17. ✅ Update any user-facing documentation referencing old paths
18. ✅ Update REPO_MAP.md if it references old structure

### Phase 5: Validation & Deployment
19. ✅ Run complete export/deploy cycle: `npm run build`
20. ✅ Test release packaging: `python tools/release/build_release_artifact.py --version test-release --dry-run`
21. ✅ Review generated artifacts and manifests
22. ⚠️ Consider running actual release build to verify zip creation
23. ✅ Document any remaining known issues

---

## Risk Assessment

### High Risk
- **Release packaging broken** - Will fail to create valid distribution artifacts
- **CI/CD workflows broken** - PRs won't validate, tests won't run
- **Downstream installations broken** - Install scripts missing from packages

### Medium Risk
- **Exporter pipeline confusion** - May read from wrong/stale directories
- **Test coverage gaps** - Jest may not find test files correctly

### Low Risk
- **Documentation drift** - Comments/docs reference old structure
- **Developer confusion** - Local dev flows may reference outdated paths

---

## Success Criteria

✅ **Packaging Works:**
- `python tools/release/build_release_artifact.py --version test --dry-run` completes without errors
- Generated MANIFEST.yml includes install scripts
- No "file not found" warnings in build output

✅ **CI/CD Works:**
- All GitHub workflow trigger paths updated
- Test commands use correct paths
- Workflows execute successfully in feature branch

✅ **Exporters Work:**
- `npm run export:all` completes successfully
- `npm run deploy:all` deploys to correct locations
- `npm run test:exporters` passes

✅ **Tests Work:**
- `npm test` passes
- Jest finds and executes all test files
- Coverage collection works correctly

---

## Notes

- **Validation directory still exists** - Contains only `framework-core/__pycache__/` (likely stale)
- **Examples directory removed** - Confirmed doesn't exist
- **Fixtures directory active** - Contains test prompts and schemas
- **Tools/release scripts exist** - framework_install.sh and framework_upgrade.sh confirmed in tools/release/

---

## Next Steps

**Immediate:**
1. 🔴 Fix critical release packaging paths (Phase 1)
2. 🔴 Test release build in dry-run mode
3. 🔴 Fix CI/CD workflow paths (Phase 2)

**Short-term:**
4. 🟡 Resolve exporter path questions (Phase 3)
5. 🟡 Update test configuration (Phase 3)

**Long-term:**
6. 🟢 Clean up documentation and comments (Phase 4)
7. 🟢 Remove stale `validation/` directory if confirmed empty

---

**Analysis Complete**  
**Recommendation:** Proceed with Phase 1 fixes immediately to unblock release capability.
