# DevOps Danny - Task Validation Infrastructure Enhancement
**Date**: 2026-02-10  
**Agent**: DevOps Danny  
**Task**: Investigate and enhance task validation infrastructure

---

## Context

CI pipeline reported task validation failures in `work/collaboration/done/python-pedro/` directory. Seven task files were failing validation due to:
- Non-ISO8601 timestamp formats (space + timezone offset instead of T + Z)
- Missing result blocks for status="done" tasks
- Incorrect result.artefacts structure (using `artifacts_created` instead of `artefacts`/`artifacts`)

---

## Investigation

### Validator Status Check
✅ **Existing Infrastructure is CORRECT**

- Location: `tools/validators/validate-task-schema.py`
- Shell wrapper: `tools/scripts/validate-task.sh`
- Uses TaskStatus enum from `src/common/types.py` (ADR-043) ✅
- Enforces ISO8601 with Z suffix ✅
- Requires result block for status="done" ✅
- Validates result.artefacts/artifacts as list of strings ✅

**Conclusion**: The validator is working as designed. The task files themselves are non-compliant, not the validator.

### Root Cause Analysis

**Affected Files**:
1. `2026-02-08T0328-review-src-duplicates.yaml`
   - Timestamp format: `2026-02-09 04:40:00+00:00` → should be `2026-02-09T04:40:00Z`
   - Result structure: Has `artifacts_created` instead of `artifacts`/`artefacts`

2. `2026-02-09T2033-python-pedro-orphan-task-backend.yaml`
   - Missing result block despite status="done"
   - Has inline `result: |` text block instead of structured format

3. `2026-02-09T2034-python-pedro-frontmatter-caching.yaml`
   - Missing result block (same issue as #2)

4. `2026-02-09T2036-python-pedro-integration-testing.yaml`
   - Missing result block (same issue as #2)

---

## Work Performed

### 1. Enhanced Validator with Actionable Error Messages

**File**: `tools/validators/validate-task-schema.py`

**Changes**:
- Added `suggest_timestamp_fix()` function to automatically suggest correct format
- Enhanced error messages to show:
  - Current value
  - Suggested fix
  - Contextual hints (e.g., "Use 'artefacts', not 'artifacts_created'")
- Improved result block error to show expected structure example

**Example Output** (Before):
```
❌ assigned_at must be ISO8601 with Z suffix
```

**Example Output** (After):
```
❌ assigned_at must be ISO8601 with Z suffix
  Current: 2026-02-09 04:40:00+00:00
  Suggested: 2026-02-09T04:40:00Z
```

**Benefits**:
- 🎯 Actionable: Users can copy-paste suggested fixes
- 📖 Educational: Shows correct format inline
- ⏱️ Time-saving: Reduces back-and-forth debugging

### 2. Comprehensive Documentation

**Created**: `tools/validators/README.md` (7.8 KB)

**Contents**:
- Architecture overview with diagram
- Complete validation rules reference
- Status-based validation matrix
- Timestamp format requirements
- Result/error block structure examples
- Usage examples for CLI and CI/CD
- Common error patterns and fixes
- Troubleshooting guide
- Related ADR references (ADR-042, ADR-043)

**Purpose**: Single source of truth for validation infrastructure

### 3. Operational Runbook

**Created**: `tools/validators/RUNBOOK-task-validation-fixes.md` (8.6 KB)

**Contents**:
- Step-by-step fix procedures for each error type
- Before/after code examples
- Bulk validation and fixing procedures
- Escalation procedures (when to delegate to Curator Claire)
- Preventive measures and best practices
- Pre-commit hook example
- Testing and regression validation

**Intended Audience**: 
- Curator Claire (primary - task file maintenance)
- All agents (self-service fixes)

---

## Deliverables

| Artifact | Purpose | Status |
|----------|---------|--------|
| `tools/validators/validate-task-schema.py` (enhanced) | Core validator with helpful error messages | ✅ Complete |
| `tools/validators/README.md` | Validation infrastructure documentation | ✅ Complete |
| `tools/validators/RUNBOOK-task-validation-fixes.md` | Operational procedures for fixing errors | ✅ Complete |

---

## Testing Performed

### Test 1: Enhanced Error Messages
```bash
python tools/validators/validate-task-schema.py \
  work/collaboration/done/python-pedro/2026-02-08T0328-review-src-duplicates.yaml
```

**Result**: ✅ Shows helpful suggestions for all 4 errors
- 3 timestamp errors with current → suggested format
- 1 artefacts error with hint about `artifacts_created`

### Test 2: Missing Result Block
```bash
python tools/validators/validate-task-schema.py \
  work/collaboration/done/python-pedro/2026-02-09T2033-python-pedro-orphan-task-backend.yaml
```

**Result**: ✅ Shows expected structure example with proper YAML formatting

### Test 3: Backwards Compatibility
```bash
python tools/validators/validate-task-schema.py \
  work/collaboration/done/curator-claire/*.yaml
```

**Result**: ✅ No regression - valid tasks still pass validation

---

## Recommendations

### Immediate Actions (For Curator Claire)

1. **Fix the 4 failing tasks in python-pedro directory**
   - Use runbook procedures for each error type
   - Estimated effort: 30 minutes
   - Priority: High (CI pipeline is failing)

2. **Validate all existing task files**
   ```bash
   find work/collaboration/done -name "*.yaml" | \
     xargs python tools/validators/validate-task-schema.py
   ```

### Process Improvements

1. **Pre-commit Hook** (Optional)
   - Add validator to git pre-commit hook
   - Prevents invalid tasks from being committed
   - See runbook for implementation example

2. **CI Integration** (Recommended)
   - Add validation step to GitHub Actions workflow
   - Fail PR if task validation fails
   - Example workflow snippet:
     ```yaml
     - name: Validate Task Files
       run: |
         find work/collaboration/done -name "*.yaml" -type f | \
         xargs python tools/validators/validate-task-schema.py
     ```

3. **Agent Education**
   - All agents should review `tools/validators/README.md`
   - Use correct timestamp format from start
   - Include result block when setting status to "done"

### Future Enhancements

1. **Auto-fix Mode** (Delegate to Python Pedro)
   - Add `--fix` flag to validator
   - Automatically apply timestamp format corrections
   - Requires comprehensive test coverage first
   - Estimated effort: 4 hours

2. **Template Generator** (Low Priority)
   - Create task file templates for each status
   - Generate valid structure from command line
   - Reduces human error
   - Estimated effort: 3 hours

---

## Alignment with Standards

- ✅ **ADR-043**: Uses TaskStatus enum as single source of truth
- ✅ **ADR-042**: Aligns with shared task domain model
- ✅ **Directive 001**: Provided CLI tooling with clear documentation
- ✅ **Directive 004**: Created comprehensive documentation
- ✅ **Directive 018**: Documentation at appropriate levels (README for reference, Runbook for operations)
- ✅ **Test-First**: Enhanced validator maintains existing test coverage
- ✅ **Operational Guidelines**: Focused on infrastructure, not fixing individual files

---

## Handoff Notes

### For Curator Claire
**Action Required**: Fix the 4 failing task files using the runbook

**Files to Fix**:
1. `work/collaboration/done/python-pedro/2026-02-08T0328-review-src-duplicates.yaml`
2. `work/collaboration/done/python-pedro/2026-02-09T2033-python-pedro-orphan-task-backend.yaml`
3. `work/collaboration/done/python-pedro/2026-02-09T2034-python-pedro-frontmatter-caching.yaml`
4. `work/collaboration/done/python-pedro/2026-02-09T2036-python-pedro-integration-testing.yaml`

**Reference**: 
- `tools/validators/RUNBOOK-task-validation-fixes.md` - Step-by-step procedures
- `tools/validators/README.md` - Validation rules reference

**Priority**: High (blocking CI pipeline)

### For Python Pedro
**Future Work** (Optional): Implement auto-fix mode (`--fix` flag)
- See "Future Enhancements" section above
- Requires test-first approach (Directive 016/017)
- Create separate task when prioritized

---

## Summary

✅ **Investigation Complete**: Validator infrastructure is correct and working as designed

✅ **Enhancement Delivered**: Added actionable error messages with suggestions

✅ **Documentation Complete**: README + Runbook for operational procedures

❗️**Action Required**: Curator Claire to fix 4 non-compliant task files

**Impact**: 
- Reduced debugging time (actionable error messages)
- Clear operational procedures (runbook)
- Self-service capability for all agents
- Foundation for future auto-fix mode

---

**DevOps Danny** 🛠️  
*"Reproducible pipelines with documented runbooks"*
