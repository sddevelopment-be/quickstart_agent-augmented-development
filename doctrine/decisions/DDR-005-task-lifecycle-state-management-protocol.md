# DDR-005: Task Lifecycle and State Management Protocol

**Status:** Active  
**Date:** 2026-02-11  
**Supersedes:** Repository-specific lifecycle implementations (elevated from ADR-003)

---

## Context

File-based multi-agent orchestration systems require well-defined task lifecycles to ensure predictable execution, clear ownership, and proper error handling. Without explicit lifecycle management, universal problems emerge:

- Agents may process the same task multiple times (duplicate work)
- Failed tasks may be lost or stuck indefinitely (unrecoverable errors)
- State transitions become ambiguous (coordination confusion)
- Audit trails are incomplete (lost accountability)
- Recovery from failures is unclear (no retry protocol)

The framework needs a universal lifecycle pattern that:
- Provides clear ownership at each stage
- Prevents duplicate processing
- Handles errors gracefully
- Enables recovery and retry
- Maintains complete audit trail
- Remains simple enough to implement reliably
- Supports both automated and manual intervention

## Decision

**We establish a five-state task lifecycle as the framework's standard state machine, enforced through directory structure and status field synchronization.**

### States

1. **`new`** - Task created, awaiting assignment
2. **`assigned`** - Task assigned to specific agent
3. **`in_progress`** - Agent actively working on task
4. **`done`** - Task completed successfully
5. **`error`** - Task failed, requires intervention

### State Machine

```
new → assigned → in_progress → done → archived
                       ↓
                     error
```

### Transition Rules

| From State     | To State      | Triggered By                  | Requirements                          |
|----------------|---------------|-------------------------------|---------------------------------------|
| `new`          | `assigned`    | Coordinator or human          | Agent exists, task valid              |
| `assigned`     | `in_progress` | Assigned agent                | Agent claims task                     |
| `in_progress`  | `done`        | Assigned agent                | Result block populated                |
| `in_progress`  | `error`       | Assigned agent or timeout     | Error metadata documented             |
| `error`        | `assigned`    | Human intervention            | Error resolved, task reset            |
| `done`         | `archived`    | Periodic cleanup              | Retention period exceeded             |

### State Persistence

- **Primary:** Directory location (filesystem structure)
- **Secondary:** Status field in task file (YAML/JSON)
- **Validation:** Both must match (consistency check)
- **Atomicity:** Directory moves are atomic operations

## Rationale

### Five-State Design

**Why five states (not three or seven)?**

- **`new`:** Clear staging prevents premature execution, enables queuing
- **`assigned`:** Explicit ownership prevents task claiming conflicts
- **`in_progress`:** Visibility into active work, timeout detection possible
- **`done`:** Clear completion signal, separates finished from active
- **`error`:** Explicit failure state, targeted recovery without retrying successes

Three states (new, active, done) lose the assignment vs. execution distinction, making stalled task detection harder. Seven or more states (e.g., validating, reviewing, approving) add complexity without proportional benefit for most agent workflows.

### Directory + Status Field Pattern

**Why both directory location and status field?**

- **Directory:** Primary source of truth, enables simple filesystem polling
- **Status field:** Redundancy for validation, enables queries without filesystem
- **Consistency check:** Detects corrupted state (file in wrong directory)
- **Atomicity:** Filesystem rename operations are atomic within same mount

### Framework-Level Pattern

This lifecycle applies universally because:
- All task-based systems need state tracking
- All frameworks benefit from explicit ownership
- All systems require error handling and recovery
- All adopters need audit trails and timeout detection

## Consequences

### Positive

- ✅ **Clarity:** Always clear which agent owns a task
- ✅ **Duplicate prevention:** Assignment state prevents concurrent claims
- ✅ **Error recovery:** Failed tasks explicitly marked and retrievable
- ✅ **Monitoring:** Simple state counts (`ls -1 work/inbox/ | wc -l`)
- ✅ **Debugging:** State history visible in version control log
- ✅ **Timeout detection:** Long-running `in_progress` tasks identifiable
- ✅ **Human override:** Manual task file movements respected

### Negative (Accepted Trade-offs)

- ⚠️ **State drift risk:** Status field and directory can diverge (mitigated by validation)
- ⚠️ **Manual cleanup:** Archive state requires periodic maintenance (automation recommended)
- ⚠️ **Limited granularity:** `in_progress` doesn't show detailed progress (agents can log internally)
- ⚠️ **Manual error recovery:** No automatic retry (human judgment required)

## Implementation

Repositories adopting this framework should:

### Directory Structure

Map states to directories:

```
work/
  inbox/                     # State: new
  assigned/<agent>/          # State: assigned or in_progress
  done/                      # State: done
  archive/                   # State: archived
```

Tasks in `assigned/<agent>/` may have status `assigned` or `in_progress` (both owned by same agent).

### Task File Schema

```yaml
id: "unique-task-identifier"
agent: "target-agent-name"
status: "new"  # Must match directory state
created_at: "2026-02-11T14:30:00Z"

# Additional fields populated at transitions
assigned_at: "2026-02-11T14:31:00Z"      # When moved to assigned
started_at: "2026-02-11T14:32:00Z"       # When in_progress
completed_at: "2026-02-11T15:00:00Z"     # When done

# Error state
error:
  message: "Failure description"
  timestamp: "2026-02-11T14:35:00Z"
  retry_count: 0
```

### State Transition Protocols

**new → assigned:**

```bash
# Coordinator or human
mv work/inbox/task-123.yaml work/assigned/structural/

# Update status field
status: assigned
assigned_at: "2026-02-11T14:31:00Z"
```

**assigned → in_progress:**

```yaml
# Agent updates file in-place
status: in_progress
started_at: "2026-02-11T14:32:00Z"
```

**in_progress → done:**

```bash
# Agent adds result, updates status, moves file
status: done
result:
  summary: "Completed successfully"
  completed_at: "2026-02-11T15:00:00Z"

# Move to done directory
mv work/assigned/structural/task-123.yaml work/done/
```

**in_progress → error:**

```yaml
# Agent or timeout detector updates status
status: error
error:
  message: "Timeout: no progress in 2 hours"
  timestamp: "2026-02-11T16:32:00Z"
  retry_count: 0

# File remains in assigned directory for visibility
```

**error → assigned (retry):**

```yaml
# Human reviews error, resets status
status: assigned
error: null  # Clear error block
retry_count: 1  # Increment retry counter
```

**done → archived:**

```bash
# Periodic cleanup script
# Archive tasks older than retention period (e.g., 30 days)
find work/done/ -name "*.yaml" -mtime +30 -exec mv {} work/archive/ \;
```

### Validation Rules

Repositories should validate:

1. **Directory-status match:** 
   - Files in `inbox/` must have `status: new`
   - Files in `assigned/<agent>/` must have `status: assigned` or `in_progress`
   - Files in `done/` must have `status: done`

2. **Required fields:**
   - All tasks: `id`, `agent`, `status`, `created_at`
   - Assigned tasks: `assigned_at`
   - In-progress tasks: `started_at`
   - Done tasks: `completed_at`, `result` block

3. **Status values:**
   - Only allowed: `new`, `assigned`, `in_progress`, `done`, `error`
   - No custom or misspelled states

4. **Ownership:**
   - Tasks in `work/assigned/<agent>/` must have `agent: <agent>`

5. **Timestamp ordering:**
   - `assigned_at` ≥ `created_at`
   - `started_at` ≥ `assigned_at`
   - `completed_at` ≥ `started_at`

### Error Handling

**Timeout Detection:**

Repositories should implement timeout monitoring:

```python
# Pseudo-code example
timeout_hours = 2  # Configurable per agent
cutoff = now() - timedelta(hours=timeout_hours)

for task in in_progress_tasks():
    if task.started_at < cutoff:
        log_warning(f"Task {task.id} stalled (>{timeout_hours}h)")
        # Optionally: mark as error automatically
```

**Error Recovery:**

Human intervention workflow:
1. Review error in `work/assigned/<agent>/task-error.yaml`
2. Fix root cause (e.g., missing context file, invalid parameters)
3. Reset task status to `assigned`, clear error block
4. Agent retries task

Alternatively:
1. Mark task as unrecoverable
2. Move to `work/archive/` with error documentation
3. Create new task if work still needed

### Archive Strategy

Repositories should implement retention policies:

**Retention periods:**
- Keep in `done/` for configurable period (e.g., 30 days)
- Move to `archive/` after retention period
- Optionally compress archives periodically
- Purge or cold-store after extended period (e.g., 1 year)

**Archive organization:**

```
work/archive/
  2026-02/              # Monthly grouping
    task-123.yaml
    task-456.yaml
  2026-03/
    ...
```

## Related

- **Doctrine:** DDR-004 (File-Based Coordination) - coordination mechanism
- **Doctrine:** DDR-006 (Work Directory Structure) - directory layout
- **Doctrine:** DDR-007 (Coordinator Pattern) - orchestration responsibilities
- **Approach:** State machine pattern (framework principles)
- **Implementation:** See repository-specific ADRs for automation scripts
