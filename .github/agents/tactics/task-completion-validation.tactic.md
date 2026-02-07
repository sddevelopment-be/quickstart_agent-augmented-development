# Tactic: Task Completion with Schema Validation

**Purpose:** Ensure task YAML files comply with schema before marking tasks as done, preventing validation errors that accumulate in the done/ directory.

**Context:** Invoked by Directive 014 (Work Log Creation) when completing orchestrated tasks. Prevents common schema violations: missing result blocks, invalid types, malformed context fields.

**Frequency:** Every orchestrated task completion

---

## Procedure

### 1. Update Task Status and Timestamps

```yaml
status: done
completed_at: "YYYY-MM-DDTHH:MM:SSZ"  # ISO8601 with Z suffix
```

**Checklist:**
- [ ] `status` changed from `assigned`/`in_progress` to `done`
- [ ] `completed_at` timestamp added with Z suffix
- [ ] Timestamp format: ISO8601 (e.g., `2026-02-07T13:30:00Z`)

### 2. Add Required Result Block

```yaml
result:
  summary: "Brief 1-2 sentence description of what was accomplished"
  artifacts:  # or "artefacts" (British spelling)
    - "path/to/artifact1.md"
    - "path/to/artifact2.py"
  completed_at: "YYYY-MM-DDTHH:MM:SSZ"
```

**Checklist:**
- [ ] `result` block exists (required for status:done)
- [ ] `result.summary` is a non-empty string
- [ ] `result.artifacts` is a list of strings (file paths)
- [ ] All files in `result.artifacts` actually exist
- [ ] `result.completed_at` has Z suffix

**Optional Result Fields:**
```yaml
result:
  # ... required fields above ...
  handoff_to: "next-agent-name"  # if passing work to another agent
  notes: "Additional completion context"
```

### 3. Validate Existing Fields

**Context Field (if present):**
```yaml
context:  # Must be a mapping (dict), NOT a string
  repo: "owner/repo"
  branch: "feature-branch"
  notes:
    - "Context item 1"
    - "Context item 2"
```

**Checklist:**
- [ ] `context` is a dict/mapping (NOT a multiline string with `|`)
- [ ] If context was a string, convert to structured dict

**Priority Field:**
```yaml
priority: high  # Must be lowercase
```

**Allowed values:** `critical`, `high`, `medium`, `normal`, `low`

**Checklist:**
- [ ] `priority` is lowercase (NOT `HIGH`, `CRITICAL`)
- [ ] `priority` is one of allowed values

**Artifacts/Artefacts Field:**
```yaml
artefacts:  # or "artifacts" (American spelling)
  - "path/to/file1.md"
  - "path/to/file2.py"
```

**Checklist:**
- [ ] `artefacts`/`artifacts` is a list of strings
- [ ] NOT an object/dict, NOT a single string

**Status Field:**
```yaml
status: done
```

**Allowed values:** `new`, `assigned`, `in_progress`, `done`, `error`

**Checklist:**
- [ ] `status` is one of allowed values (NOT `inbox`, `completed`, `finished`)

### 4. Run Validation Script

**Command (use existing GitHub Actions validator):**
```bash
# Direct validator (used in CI)
python validation/validate-task-schema.py work/collaboration/done/<agent>/<task-id>.yaml

# OR use convenience wrapper
./ops/scripts/validate-task.sh work/collaboration/done/<agent>/<task-id>.yaml
```

**Expected Output:**
```
✅ Task schema validation passed
```

**If Validation Fails:**
1. Review error messages
2. Fix indicated issues
3. Re-run validation
4. Do NOT proceed until validation passes

**Checklist:**
- [ ] Validation script executed
- [ ] Validation passed (green checkmark)
- [ ] No error messages

### 5. Move Task to Agent-Specific done/ Directory

**Correct Path Pattern:**
```
work/collaboration/done/<agent-name>/<task-id>.yaml
```

**Examples:**
- `work/collaboration/done/curator/2026-02-07T1400-curator-guide.yaml`
- `work/collaboration/done/architect/2026-02-07T1400-architect-adr.yaml`

**NOT:**
- ❌ `work/collaboration/done/2026-02-07T1400-task.yaml` (missing agent dir)
- ❌ `work/collaboration/assigned/<agent>/...` (wrong lifecycle dir)

**Checklist:**
- [ ] Task moved to `work/collaboration/done/<agent>/`
- [ ] NOT in root `done/` directory
- [ ] File named `<task-id>.yaml` (matches `id` field)

---

## Quick Reference: Common Violations

| Error | Fix |
|-------|-----|
| `result block required for completed tasks` | Add `result:` with `summary` and `artifacts` |
| `context must be a mapping when provided` | Change `context: \|` to `context:` dict |
| `invalid priority 'HIGH'` | Lowercase: `priority: high` |
| `artefacts/artifacts must be a list` | Use `- item1` list format, not object |
| `invalid status 'inbox'` | Use allowed status: `new`, `assigned`, `in_progress`, `done`, `error` |
| `result.summary is required` | Add non-empty string to `result.summary` |
| `completed_at must be ISO8601 with Z suffix` | Use format: `2026-02-07T13:30:00Z` |

---

## Integration with Directive 014

**Work Log Creation Step (updated):**

When completing an orchestrated task:

1. **Update task YAML** (this tactic - steps 1-3)
2. **Validate task YAML** (this tactic - step 4)
3. **Move task to done/<agent>/** (this tactic - step 5)
4. Create detailed work log in `work/reports/logs/<agent-name>/`
5. Create handoff task (if applicable)
6. Commit all changes together

**The validation step is mandatory. Do not skip.**

---

## CLI Helper Script

**Quick Validation (uses same validator as GitHub Actions):**
```bash
# Validate current task before completion
python validation/validate-task-schema.py work/collaboration/assigned/<agent>/<task-id>.yaml
# OR: ./ops/scripts/validate-task.sh work/collaboration/assigned/<agent>/<task-id>.yaml

# Validate after moving to done/
python validation/validate-task-schema.py work/collaboration/done/<agent>/<task-id>.yaml

# Validate all done tasks for an agent
python validation/validate-task-schema.py work/collaboration/done/<agent>/*.yaml
```

**Note:** The wrapper script `ops/scripts/validate-task.sh` is a convenience alias that calls `validation/validate-task-schema.py` (the same script used in `.github/workflows/validation.yml`).

---

## Metadata

- **Invoked By:** Directive 014 (Work Log Creation)
- **Frequency:** Every task completion
- **Failure Mode:** Validation errors accumulate in done/ directory, blocking CI/CD
- **Success Metric:** Zero schema validation errors in done/ directory
- **Related:** Directive 019 (File-Based Collaboration)
- **Version:** 1.0.0
- **Created:** 2026-02-07
