# Stale Task Mitigation Strategies

_Date: 2025-11-30_  
_Context: Issue #10 - Stale work / waste avoidance improvements_  
_Status: Ideation / Recommendations_

## Problem Statement

Task staleness in async orchestration causes:
- Outdated context (paths, numbers, branches)
- Wasted agent effort on incorrect specifications
- Post-execution reconciliation overhead
- Documentation inconsistencies

As evidenced by the 2025-11-30T0708 reconciliation work log, an 18-hour gap between task creation and execution resulted in:
- ADR numbering conflicts (expected ADR-011, actual ADR-015)
- Path reference conflicts (work/logs/ vs work/reports/logs/)
- Missing artifacts that contradicted recommendations
- Branch context staleness

## Implemented Solutions

### 1. Task Age Detection ✅
**Status:** Implemented (ops/orchestration/task_age_checker.py)

- Detects tasks older than configurable threshold (default 24h)
- Checks inbox, new, assigned, in_progress states
- Ignores done/archive (expected to be old)
- Provides text and JSON output formats
- Can fail builds or warn-only mode

**Usage:**
```bash
# Check with default 24h threshold
python ops/orchestration/task_age_checker.py --warn-only

# Check with custom 48h threshold
python ops/orchestration/task_age_checker.py --threshold 48 --warn-only

# Fail on stale tasks (for CI/CD)
python ops/orchestration/task_age_checker.py
```

### 2. Schema Enhancement ✅
**Status:** Implemented (validation/validate-task-schema.py)

Added `artefacts_not_created` field to task schema:
```yaml
artefacts_not_created:
  - name: "optional-diagram.png"
    rationale: "Task was rejected, diagram would contradict recommendation"
```

Allows agents to document intentionally omitted artifacts with clear rationale.

### 3. Path Convention Documentation ✅
**Status:** Implemented (agents/directives/003_repository_quick_reference.md)

- Consolidated path conventions in single authoritative location
- Added Standard Path Conventions section
- Examples for task files, work logs, ADRs
- Fixed Directive 014 path inconsistencies

### 4. ADR Numbering Guidance ✅
**Status:** Implemented (docs/templates/architecture/adr.md)

- Added numbering guide to ADR template
- Command to find latest ADR number
- Recommendation to use descriptive names in planning
- Reserve number by creating file immediately

## Recommended Future Enhancements

### Short-Term (Next Iteration)

#### 1. Task Context Validation Step
**Priority:** High  
**Effort:** Medium

Add pre-execution validation step:
```python
def validate_task_context(task_file):
    """Validate task context before execution."""
    checks = [
        check_branch_exists(task.context.branch),
        check_paths_exist(task.context.references),
        check_adr_numbers_available(task.expected_adrs),
        check_dependencies_met(task.dependencies),
    ]
    return all(checks)
```

Integrate into orchestrator before delegating to agents.

#### 2. Task Auto-Refresh Mechanism
**Priority:** High  
**Effort:** Medium

```python
def refresh_task_context(task_file):
    """Update task context from current repository state."""
    task = load_task(task_file)
    
    # Update branch reference
    task.context.branch = get_current_branch()
    
    # Revalidate paths
    task.context.references = update_path_references(task.context.references)
    
    # Check ADR numbers
    task.expected_adrs = resolve_adr_descriptive_names(task.expected_adrs)
    
    write_task(task_file, task)
    return task
```

Could be manual or automatic based on age threshold.

#### 3. Task Expiration Policy
**Priority:** Medium  
**Effort:** Low

Implement automatic archival:
- Tasks >48h in inbox: Move to archive with "expired" reason
- Tasks >72h in assigned: Flag for review or archive
- Notification to task creator on expiration

Configuration in task YAML:
```yaml
expiration:
  max_age_hours: 48
  action: archive  # or: warn, refresh, fail
```

### Medium-Term (Next 2-3 Iterations)

#### 4. Parallel Execution Coordination
**Priority:** Medium  
**Effort:** High

**Problem:** Multiple agents editing same areas without coordination.

**Solution:** Lightweight resource locking:
```yaml
# Task specification
locks_required:
  - "docs/architecture/adrs/"
  - "agents/directives/014_worklog_creation.md"
```

Orchestrator checks locks before assignment:
```python
def acquire_locks(task, timeout_minutes=30):
    """Acquire locks with timeout."""
    for resource in task.locks_required:
        if not lock_manager.acquire(resource, timeout_minutes):
            raise LockTimeout(f"Could not acquire lock on {resource}")
```

#### 5. ADR Number Reservation
**Priority:** Low  
**Effort:** Medium

Create ADR reservation system:
```bash
# Reserve next ADR number
python ops/orchestration/reserve_adr.py --title "follow-up-task-lookup"
# Output: Reserved ADR-015 for follow-up-task-lookup

# Create ADR with reserved number
python ops/orchestration/create_adr.py --reservation ADR-015
```

Reservation stored in `.adr_reservations.json` with timestamp.

#### 6. Directive Conflict Detection
**Priority:** Low  
**Effort:** Medium

Tool to find contradictions in directives:
```bash
python validation/check_directive_conflicts.py

# Example output:
# ⚠️  Directive 014 path conflict:
#     Line 212: work/logs/
#     Line 232: work/reports/logs/
#     Recommendation: Use work/reports/logs/ consistently
```

### Long-Term (Future Consideration)

#### 7. Smart Context Tracking
**Priority:** Low  
**Effort:** High

Track what changed between task creation and execution:
```python
class TaskContextDelta:
    def __init__(self, task_file):
        self.created_at = task.created_at
        self.repo_state_at_creation = capture_repo_state()
        
    def compute_delta(self):
        current_state = capture_repo_state()
        return {
            "new_adrs": current_state.adrs - self.repo_state_at_creation.adrs,
            "new_directives": ...,
            "branch_changes": ...,
            "path_migrations": ...,
        }
```

Provide delta report to agent before execution.

#### 8. Task Dependency Graph
**Priority:** Low  
**Effort:** High

Visualize and track task dependencies:
- Detect when dependency context has changed
- Auto-update dependent tasks
- Prevent execution if dependencies stale

```yaml
dependencies:
  - task_id: "2025-11-24T0950-architect-version-policy"
    status_required: "done"
    artifacts_required:
      - "docs/architecture/adrs/ADR-014-version-policy.md"
```

## ROI Estimation

### Time Saved by Implemented Solutions

**Before (Issue #10 reconciliation):**
- Agent execution: ~30 minutes (2 agents)
- Reconciliation: ~90 minutes
- Total: ~120 minutes

**After (with detection):**
- Age check: ~1 minute
- Context validation: ~5 minutes
- Agent execution: ~30 minutes
- Total: ~36 minutes

**Savings:** ~84 minutes per stale task incident (70% reduction)

### Projected Impact

Assuming 1 stale task incident per week:
- Weekly savings: ~84 minutes
- Monthly savings: ~6 hours
- Yearly savings: ~72 hours (9 working days)

Additional benefits:
- Reduced cognitive load
- Better documentation consistency
- Fewer post-execution fixes
- Improved agent trust/reliability

## Implementation Priority

1. **Critical (This Iteration):**
   - [x] Task age detection
   - [x] Schema enhancement
   - [x] Path documentation
   - [x] ADR numbering guide

2. **High (Next Iteration):**
   - [ ] Task context validation step
   - [ ] Task auto-refresh mechanism
   - [ ] Task expiration policy

3. **Medium (Next 2-3 Iterations):**
   - [ ] Parallel execution coordination
   - [ ] ADR number reservation
   - [ ] Directive conflict detection

4. **Future Consideration:**
   - [ ] Smart context tracking
   - [ ] Task dependency graph

## Success Metrics

Track these metrics to measure improvement:
- Number of stale task detections per week
- Average task age at execution
- Reconciliation time per task
- Task context accuracy (% with correct paths/numbers)
- Agent rework rate (tasks requiring fixes)

## Related Work

- Issue #10 - Stale work / waste avoidance
- Work Log: 2025-11-30T0708-issue-10-reconciliation.md
- Directive 014 - Work Log Creation
- Directive 003 - Repository Quick Reference

---

_Next Steps:_
1. Integrate task_age_checker into CI/CD pipeline
2. Update orchestrator to run validation before assignment
3. Create follow-up tasks for high-priority enhancements
4. Monitor stale task metrics for 2-3 iterations
5. Refine thresholds based on actual usage patterns
