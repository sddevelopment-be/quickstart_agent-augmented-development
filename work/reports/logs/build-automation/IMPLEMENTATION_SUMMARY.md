# Data-Driven Issue Creation System - Implementation Summary

**Date:** 2025-11-27  
**Implementer:** DevOps Danny  
**Approach:** Extract-Transform-Load from legacy bash scripts to YAML definitions

## What Was Accomplished

### ✅ Core System Built

1. **Generic Issue Creation Engine** (`create-issues-from-definitions.sh`)
   - 400+ lines of bash using only grep/awk (no external dependencies like yq)
   - Parses YAML definitions for epics and issues
   - Supports single documents and arrays
   - Taskset filtering capability
   - Dry-run mode for previewing
   - Epic number tracking for parent-child linking
   - Color-coded output with progress indicators

2. **3-Tier Architecture Maintained**
   - **Tier 1 (API):** `create-issues-from-definitions.sh` - Main orchestration
   - **Tier 2 (Logic):** YAML definitions in `agent-scripts/issue-definitions/`
   - **Tier 3 (Helpers):** `github-helpers/create-github-issue.sh` - Tracker abstraction

3. **YAML Definition Format Established**
   ```yaml
   type: epic | issue
   taskset: category-name
   title: "Issue Title"
   labels: comma,separated,labels
   epic_ref: parent-epic-file  # For issues only
   assignee: ""  # Optional
   priority: high | normal | low  # Optional
   body: |
     Multiline markdown content
   ```

### ✅ Full Migration Completed (27/27 issues + 6 epics)

**All Tasksets Migrated:**

1. **Housekeeping** (6 issues + 1 epic)
   - Files: `housekeeping-epic.yml`, `housekeeping-issues.yml`
   - Priority: High

2. **POC3** (4 issues + 1 epic)
   - Files: `poc3-epic.yml`, `poc3-issues.yml`
   - Priority: High

3. **Documentation** (4 issues + 1 epic)
   - Files: `documentation-epic.yml`, `documentation-issues.yml`
   - Priority: Normal

4. **Build/CI-CD** (5 issues + 1 epic)
   - Files: `build-cicd-epic.yml`, `build-cicd-issues.yml`
   - Priority: High

5. **Architecture** (3 issues + 1 epic)
   - Files: `architecture-epic.yml`, `architecture-issues.yml`
   - Priority: Normal

6. **Curator/Quality** (3 issues + 1 epic)
   - Files: `curator-quality-epic.yml`, `curator-quality-issues.yml`
   - Priority: Normal

7. **Follow-up** (2 issues, no epic)
   - Files: `followup-issues.yml`
   - Priority: Normal

## Benefits Over Legacy Approach

### Old Way (Bash Scripts with Heredocs)
```bash
create_issue \
  "Title" \
  "$(cat <<'EOF'
# Body content inline
EOF
)" \
  "labels" \
  "$EPIC_REF"
```

❌ Data mixed with logic  
❌ Hard to modify without bash knowledge  
❌ Duplication across scripts  
❌ No easy filtering  
❌ Complex for agents to generate

### New Way (YAML Definitions + Engine)
```yaml
- type: issue
  taskset: housekeeping
  title: "Title"
  labels: label1,label2
  body: |
    # Body content
```

✅ Clean data separation  
✅ Easy to edit (just YAML)  
✅ Single engine, reusable  
✅ Filter by taskset  
✅ Simple for agents to generate

## Usage Examples

```bash
# List available tasksets
ops/scripts/planning/create-issues-from-definitions.sh --list-tasksets
# Output:
#   - housekeeping
#   - poc3

# Preview what would be created
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping --dry-run

# Create issues for real
export GH_TOKEN="your_token"
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping

# Create multiple tasksets
ops/scripts/planning/create-issues-from-definitions.sh --taskset housekeeping,poc3

# Create ALL issues
ops/scripts/planning/create-issues-from-definitions.sh
```

## Technical Notes

### Key Implementation Challenges Solved

1. **YAML Parsing Without Dependencies**
   - Used grep/awk instead of yq
   - Custom `parse_yaml_field()` function
   - Handles both simple fields and multiline body content

2. **Array Document Processing**
   - Detects arrays with `grep -q "^- type:"`
   - Splits into individual items
   - Removes 2-space indentation from YAML array syntax
   - Processes each item independently

3. **Terminal Interaction Issues**
   - Applied Directive 001 remediation technique
   - Piped output to files for reliable reading
   - Documented flaky terminal behavior

4. **Field Parsing Edge Cases**
   - Trim newlines from simple fields (`tr -d '\n\r'`)
   - Handle quoted strings (`sed 's/^"\(.*\)"$/\1/'`)
   - Extract multiline body with awk flag-based parsing

### File Permissions
All YAML files require read permissions (644):
```bash
chmod 644 ops/scripts/planning/agent-scripts/issue-definitions/*.yml
```

## Documentation Updates

Updated files:
- `ops/scripts/planning/README.md` - Added "Data-Driven Issue Creation" section
- `ops/README.md` - Updated planning scripts section
- `ops/QUICKSTART.md` - Updated with new script paths

## Legacy Script Status

### ✅ Deprecated (Migration Complete)
- ~~`ops/scripts/planning/agent-scripts/create_housekeeping_issues.sh`~~ → Moved to `legacy/`
- ~~`ops/scripts/planning/agent-scripts/create_all_task_issues.sh`~~ → Moved to `legacy/`
- `ops/scripts/planning/create-follow-up-issues.sh` → Can be deprecated (migrated to `followup-issues.yml`)

### Completed Actions
1. ✅ All tasksets migrated to YAML definitions
2. ✅ Legacy scripts moved to `agent-scripts/legacy/` directory
3. ✅ Deprecation notice added (`legacy/README.md`)
4. ⏳ Update `create-github-issues.sh` to use data-driven engine by default (optional)
5. ✅ Documentation updated with new approach

## Next Steps (Optional Enhancements)

### Optional: Update Main Orchestration Script
Update `create-github-issues.sh` to use the data-driven engine by default:
- Keep backward compatibility with legacy scripts
- Add option to use YAML definitions
- Simplify workflow for future use

### Optional: Enhance YAML Engine
Potential improvements:
- Add validation for YAML schema
- Support for project fields (GitHub Projects integration)
- Dependency tracking between issues
- Bulk operations (close, update labels, etc.)

### For Agents: Creating New Issues
Agents should now create YAML definition files instead of bash scripts:

```yaml
---
- type: issue
  taskset: new-feature
  title: "Implement new feature"
  labels: enhancement,feature
  body: |
    Description goes here
```

---

**Implementation Complete:** ✅ 100% migration done  
**Migration Progress:** 100% (27/27 issues + 6 epics)  
**Ready for:** Production use with all tasksets  
**Legacy Scripts:** Deprecated and moved to `legacy/` directory


