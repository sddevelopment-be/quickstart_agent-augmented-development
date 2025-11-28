# ADR-003: Task Lifecycle and State Management

**status**: `Accepted`  
**date**: 2025-11-20

### Context

In a file-based multi-agent orchestration system, tasks must progress through well-defined states to ensure predictable execution, clear ownership, and proper error handling. Without explicit lifecycle management:

- Agents may process the same task multiple times
- Failed tasks may be lost or stuck indefinitely
- State transitions become ambiguous
- Audit trails are incomplete
- Recovery from failures is unclear

We need a task lifecycle that:

- Provides clear ownership at each stage
- Prevents duplicate processing
- Handles errors gracefully
- Enables recovery and retry
- Maintains complete audit trail
- Is simple enough to implement reliably

The system must support both automated agent execution and manual human intervention at any stage.

### Decision

**We will implement a five-state task lifecycle with explicit state transitions enforced through directory structure and YAML status field.**

**States:**

1. **`new`**: Task created, awaiting assignment (location: `work/inbox/`)
2. **`assigned`**: Task assigned to an agent (location: `work/assigned/<agent>/`)
3. **`in_progress`**: Agent actively working on task (location: `work/assigned/<agent>/`)
4. **`done`**: Task completed successfully (location: `work/done/`)
5. **`error`**: Task failed, requires intervention (location: `work/assigned/<agent>/` with error metadata)

**State transitions:**

```
new → assigned → in_progress → done → archived
                      ↓
                    error
```

**Transition rules:**

- Only Coordinator or humans can move tasks from `new` to `assigned`
- Only assigned agent can transition `assigned` → `in_progress`
- Only assigned agent can transition `in_progress` → `done` or `error`
- Periodic cleanup moves `done` → `archived` after retention period (e.g., 30 days)
- `error` state requires human review before retry or cancellation

**State persistence:**

- **Location**: Directory structure (`work/inbox/`, `work/assigned/<agent>/`, etc.)
- **Status field**: YAML `status:` field must match directory location
- **Atomic transitions**: File move (rename) operations are atomic on POSIX systems

### Rationale

**Why five states?**

- **`new`**: Clear staging area for unassigned work, prevents premature execution
- **`assigned`**: Explicit ownership, prevents multiple agents from claiming same task
- **`in_progress`**: Visibility into active work, enables timeout detection
- **`done`**: Clear completion signal, separates finished from active work
- **`error`**: Explicit failure state, enables targeted recovery without retrying successful tasks

**Why directory + status field?**

- **Directory**: Primary source of truth, enables simple polling and listing
- **Status field**: Redundancy for validation, enables queries without file system access
- **Both**: Consistency check detects corrupted state (file in wrong directory)

**Why atomic file moves?**

- POSIX `rename()` is atomic within same filesystem
- Prevents partial state transitions
- No need for distributed locks or coordination
- Simple to implement reliably

**Trade-offs accepted:**

- **No substates**: `in_progress` doesn't distinguish between "loading context" and "generating artifacts" (acceptable: agents can log detailed progress internally)
- **Manual archive**: No automatic archival (acceptable: periodic cleanup script is simple)
- **Single ownership**: Task can't be split across multiple agents (acceptable: create subtasks if needed)

**Alternatives considered:**

1. **Three-state model** (new, active, done)
   - Rejected: Loses `assigned` vs `in_progress` distinction, harder to detect stalled tasks
2. **Status field only** (no directory structure)
   - Rejected: Loses filesystem-based atomicity and simple polling
3. **Complex substates** (assigned, claimed, validating, executing, reviewing, done)
   - Rejected: Over-engineered for our needs, adds complexity without clear benefit
4. **Event log approach** (append-only state transitions)
   - Rejected: Harder to determine current state, requires replay logic

### Envisioned Consequences

**Positive:**

- ✅ **Clarity**: Always clear which agent owns a task
- ✅ **Prevention**: Duplicate processing prevented by `assigned` state
- ✅ **Recovery**: Failed tasks explicitly marked and retrievable
- ✅ **Monitoring**: Simple to count tasks in each state (`ls -1 work/inbox/ | wc -l`)
- ✅ **Debugging**: State history visible in git log of task file
- ✅ **Timeout detection**: Long-running `in_progress` tasks identifiable by timestamp
- ✅ **Human intervention**: Can manually move task files at any point

**Negative:**

- ⚠️ **State drift**: Status field and directory location can become inconsistent if not validated
- ⚠️ **Manual cleanup**: Archive state requires periodic maintenance
- ⚠️ **Limited granularity**: `in_progress` doesn't show detailed progress
- ⚠️ **Error recovery**: No automatic retry mechanism (requires human intervention)

**Risks:**

- **Inconsistent state**: File moved but status not updated → Validation script detects and corrects
- **Stuck tasks**: Agent crashes during `in_progress` → Timeout detection + manual recovery
- **Lost tasks**: File accidentally deleted → Git history provides recovery
- **Archive growth**: Done tasks accumulate → Periodic cleanup policy + compression

**Dependencies:**

- Requires all agents to follow state transition protocol
- Requires validation script to detect inconsistent state
- Requires Coordinator to enforce assignment rules
- Requires monitoring to detect stalled `in_progress` tasks

### State Transition Protocol

**new → assigned:**

```bash
# Performed by Coordinator or human
mv work/inbox/task-123.yaml work/assigned/structural/
# Update status field in YAML
sed -i 's/status: new/status: assigned/' work/assigned/structural/task-123.yaml
```

**assigned → in_progress:**

```yaml
# Agent updates YAML
status: in_progress
started_at: "2025-11-20T14:30:00Z"
```

**in_progress → done:**

```bash
# Agent adds result block and moves file
# Update YAML with result
cat >> work/assigned/structural/task-123.yaml <<EOF
result:
  summary: "Generated REPO_MAP and SURFACES"
  artefacts:
    - docs/REPO_MAP.md
    - docs/SURFACES.md
  completed_at: "2025-11-20T14:45:00Z"
EOF
# Update status and move
sed -i 's/status: in_progress/status: done/' work/assigned/structural/task-123.yaml
mv work/assigned/structural/task-123.yaml work/done/
```

**in_progress → error:**

```yaml
# Agent updates YAML with error details
status: error
error:
  message: "Failed to generate REPO_MAP: missing context file"
  timestamp: "2025-11-20T14:35:00Z"
  agent: "structural"
  retry_count: 0
```

**done → archived:**

```bash
# Periodic cleanup script (e.g., monthly)
# Archive tasks older than 30 days
find work/done/ -name "*.yaml" -mtime +30 -exec mv {} work/archive/ \;
```

### Validation Rules

**Consistency checks:**

1. **Directory-status match**: File in `work/assigned/X/` must have `status: assigned` or `status: in_progress`
2. **Required fields**: All tasks must have `id`, `agent`, `status`, `artefacts`
3. **Status values**: Only allowed values are `new`, `assigned`, `in_progress`, `done`, `error`
4. **Timestamps**: `in_progress` tasks must have `started_at`, `done` tasks must have `completed_at`
5. **Ownership**: Tasks in `work/assigned/<agent>/` must have `agent: <agent>`

**Validation script:**

```bash
#!/bin/bash
# validation/validate-task-state.sh

for dir in work/inbox work/assigned/* work/done work/archive; do
  for task in $dir/*.yaml; do
    # Check status matches location
    # Check required fields present
    # Report inconsistencies
  done
done
```

### Error Handling

**Timeout detection:**

- Tasks `in_progress` for >2 hours flagged as potentially stalled
- Coordinator logs warning in `work/collaboration/WORKFLOW_LOG.md`
- Human reviews and decides: retry, cancel, or extend timeout

**Error recovery:**

- Agent sets `status: error` and adds error details
- Task remains in `work/assigned/<agent>/` for visibility
- Human reviews error, fixes root cause
- Human resets status to `assigned` and removes error block to retry
- Or moves to `work/archive/` if unrecoverable

**Partial completion:**

- If agent completes some but not all artifacts, mark task `done` with partial result
- Create new task for remaining work if needed
- Document partial completion in result block

### Archive Strategy

**Retention policy:**

- Keep tasks in `work/done/` for 30 days
- Move to `work/archive/` after 30 days
- Compress archive periodically (e.g., monthly)
- Retain archives for 1 year, then purge (or move to cold storage)

**Archive format:**

```
work/archive/
  2025-11/
    2025-11-20T1430-structural-repomap.yaml
    2025-11-20T1500-lexical-voice-analysis.yaml
  2025-12/
    ...
```

### Considered Alternatives

**1. Event Sourcing Model**

- **Approach**: Append-only log of state transitions, replay to determine current state
- **Pros**: Complete history, no state updates (only appends)
- **Cons**: Requires replay logic, harder to query current state, more complex
- **Reason rejected**: Over-engineered for our needs, directory structure provides sufficient state tracking

**2. Database-Backed State**

- **Approach**: Store task state in SQLite or PostgreSQL
- **Pros**: ACID transactions, complex queries, indexing
- **Cons**: Binary format, not Git-native, merge conflicts on DB file
- **Reason rejected**: Loses transparency and Git integration

**3. Lockfile-Based Coordination**

- **Approach**: Create `.lock` files to claim tasks
- **Pros**: Prevents concurrent access explicitly
- **Cons**: Stale locks if agent crashes, requires cleanup logic, doesn't prevent reading
- **Reason rejected**: Directory structure + status field provides equivalent safety with less complexity

**4. Single Active Directory**

- **Approach**: All tasks in one directory, only status field differs
- **Pros**: Simpler directory structure
- **Cons**: Loses natural separation by agent, harder to poll for specific agent tasks, no atomic assignment
- **Reason rejected**: Directory structure provides clear ownership and atomic moves

---

**Related ADRs:**

- [ADR-002: File-Based Asynchronous Agent Coordination](ADR-008-file-based-async-coordination.md)
- [ADR-004: Work Directory Structure](ADR-004-work-directory-structure.md)
- [ADR-005: Coordinator Agent Pattern](ADR-005-coordinator-agent-pattern.md)

**References:**

- [Async Multi-Agent Orchestration Architecture](../design/async_multiagent_orchestration.md)
- Issue #8: Asynchronous Multi-Agent Orchestration (File-Driven Model)
