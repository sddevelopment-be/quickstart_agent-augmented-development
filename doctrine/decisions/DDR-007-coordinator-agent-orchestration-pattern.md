# DDR-007: Coordinator Agent Orchestration Pattern

**Status:** Active  
**Date:** 2026-02-11  
**Supersedes:** Repository-specific orchestration implementations (elevated from ADR-005)

---

## Context

Multi-agent orchestration systems require coordination for:

- **Task assignment:** Routing incoming tasks to appropriate agents
- **Workflow sequencing:** Creating follow-up tasks based on agent handoffs
- **Conflict detection:** Identifying when multiple agents target same artifacts
- **Status monitoring:** Tracking overall system health and progress
- **Error handling:** Detecting and escalating stalled or failed tasks
- **Audit logging:** Recording system-wide orchestration events

Without coordination, universal problems emerge:
- Tasks sit unassigned indefinitely
- Multi-step workflows require manual intervention between steps
- Conflicting work goes undetected until merge conflicts
- System bottlenecks remain invisible
- Failed tasks are lost or forgotten

Possible coordination approaches:
1. **Manual:** Humans assign all tasks
2. **Coordinator agent:** Dedicated meta-agent for orchestration
3. **Distributed:** Agents self-assign and coordinate peer-to-peer
4. **External orchestrator:** Separate service (workflow engine, scheduler)

The framework needs a pattern that:
- Maintains simplicity and transparency
- Doesn't require running services
- Allows human override at any point
- Scales to multiple concurrent agents
- Provides visibility into system state

## Decision

**We establish the Coordinator agent pattern as the framework's standard orchestration mechanism: a specialized meta-agent responsible for orchestration tasks but not artifact generation.**

### Responsibilities

1. **Task Assignment**
   - Monitor inbox for new tasks
   - Match tasks to agents based on assignment field
   - Move task files to agent directories
   - Update task status from `new` to `assigned`

2. **Workflow Sequencing**
   - Monitor completed tasks for handoff markers
   - Read `next_agent` field from task results
   - Create follow-up tasks in inbox
   - Log handoffs in coordination artifacts

3. **Conflict Detection**
   - Track which artifacts are being modified by which tasks
   - Warn when multiple in-progress tasks target same artifact
   - Optionally serialize conflicting tasks

4. **Status Monitoring**
   - Update agent status dashboards periodically
   - Detect tasks stuck in `in_progress` for excessive duration
   - Flag agents without recent activity

5. **Error Handling**
   - Monitor tasks in `error` state
   - Log errors to coordination artifacts
   - Escalate to humans via configured notifications

6. **Audit Logging**
   - Record all orchestration events
   - Maintain complete timeline of task movements
   - Provide data for retrospectives and optimization

### Execution Model

- **Polling-based:** Runs periodically (e.g., every 5 minutes via cron, CI, or scheduler)
- **Idempotent:** Safe to run multiple times, no side effects from repeated execution
- **Stateless:** All state stored in files, no in-memory persistence
- **Manual override:** Humans can perform any Coordinator action manually

### Non-Responsibilities

The Coordinator does NOT:
- ❌ Generate artifacts (documentation, code, diagrams)
- ❌ Execute agent-specific logic
- ❌ Make strategic decisions (only operational routing)
- ❌ Modify agent outputs

## Rationale

### Why Dedicated Coordinator?

**Separation of concerns:**
- Orchestration logic separated from domain logic
- Agents focus on specialization, not coordination
- Single responsibility principle applied

**Consistency:**
- Centralized logic ensures uniform handling
- All coordination decisions in one place
- Predictable behavior across workflows

**Auditability:**
- All coordination visible in one agent's log
- Clear responsibility for routing decisions
- Traceable workflow chains

**Simplicity:**
- Agents don't need coordination code
- Cleaner agent implementations
- Easier to reason about system behavior

### Why Polling-Based Execution?

**No running services:**
- Can be triggered by cron, CI, or manual invocation
- Works in any environment with filesystem access
- No operational overhead for service management

**Git-native:**
- Operates on committed state
- No ephemeral queues or in-memory state
- Version control provides complete history

**Debuggable:**
- Easy to inspect state before/after execution
- Can run manually for testing
- State transitions visible in filesystem

**Idempotent:**
- Safe to run multiple times
- Recovers gracefully from interruptions
- No duplicate work on retry

### Why Stateless Design?

**Recovery:**
- No in-memory state to lose on crash
- Restart anywhere without recovery procedures
- All state visible in filesystem

**Transparency:**
- Complete state inspection via file reading
- No hidden coordinator state
- Debugging via file inspection

**Simplicity:**
- No state persistence logic required
- No recovery protocols needed
- Coordination state = file state

### Framework-Level Pattern

This pattern applies universally because:
- All multi-agent systems need task routing
- All frameworks benefit from centralized orchestration
- All adopters need audit trails and monitoring
- All systems require conflict detection

## Consequences

### Positive

- ✅ **Automation:** Tasks routed without human intervention
- ✅ **Workflow chaining:** Multi-step workflows automatic via `next_agent`
- ✅ **Visibility:** Central view of system state and progress
- ✅ **Safety:** Conflict detection prevents simultaneous editing
- ✅ **Auditability:** Complete log of orchestration decisions
- ✅ **Simplicity:** Agents don't need coordination logic
- ✅ **Human override:** Coordinator is optional, humans can intervene

### Negative (Accepted Trade-offs)

- ⚠️ **Polling delay:** Introduces latency (acceptable: agent tasks are long-running)
- ⚠️ **Single coordinator:** No redundancy (mitigated by stateless design)
- ⚠️ **Complexity:** One more agent to maintain (mitigated by separation of concerns)
- ⚠️ **Potential bottleneck:** High task volume could overwhelm (unlikely given task duration)

## Implementation

Repositories adopting this framework should:

### Coordinator Workflow

Main coordination loop (pseudo-code):

```python
def coordinator_loop():
    # 1. Process inbox
    for task in list_tasks("work/inbox/"):
        agent = read_task(task)['agent']
        validate_task(task)
        move_task(task, f"work/assigned/{agent}/")
        update_status(task, "assigned")
        log_event(f"Assigned {task.id} to {agent}")
    
    # 2. Process completed tasks
    for task in list_tasks("work/done/"):
        result = read_task(task)['result']
        if 'next_agent' in result:
            create_followup_task(task, result['next_agent'])
            log_handoff(task.agent, result['next_agent'])
    
    # 3. Monitor active tasks
    for agent in list_agents():
        for task in list_tasks(f"work/assigned/{agent}/"):
            if task.status == "in_progress":
                check_timeout(task)
            if task.status == "error":
                escalate_error(task)
    
    # 4. Detect conflicts
    active_tasks = list_all_active_tasks()
    conflicts = detect_artifact_conflicts(active_tasks)
    for conflict in conflicts:
        log_warning(conflict)
    
    # 5. Update status dashboard
    update_agent_status()
    
    # 6. Archive old tasks
    archive_old_tasks(retention_days=30)
```

### Task Assignment Logic

```python
def assign_task(task_file):
    task = read_yaml(task_file)
    agent = task['agent']
    
    # Validate agent exists
    if not exists(f"work/assigned/{agent}/"):
        log_error(f"Unknown agent: {agent}")
        task['status'] = 'error'
        task['error'] = {'message': f"Agent '{agent}' not found"}
        write_yaml(task_file, task)
        return
    
    # Move to assigned directory
    dest = f"work/assigned/{agent}/{basename(task_file)}"
    move_file(task_file, dest)
    
    # Update status
    task['status'] = 'assigned'
    task['assigned_at'] = now_iso8601()
    write_yaml(dest, task)
    
    log_event(f"Assigned {task['id']} to {agent}")
```

### Workflow Chaining

```python
def process_completed_task(task_file):
    task = read_yaml(task_file)
    result = task.get('result', {})
    next_agent = result.get('next_agent')
    
    if next_agent:
        followup = {
            'id': generate_task_id(next_agent),
            'agent': next_agent,
            'status': 'new',
            'title': result.get('next_task_title', f"Follow-up to {task['id']}"),
            'artefacts': result.get('next_artefacts', task['artefacts']),
            'context': {
                'previous_task': task['id'],
                'previous_agent': task['agent']
            },
            'created_at': now_iso8601(),
            'created_by': 'coordinator'
        }
        
        followup_file = f"work/inbox/{followup['id']}.yaml"
        write_yaml(followup_file, followup)
        
        log_handoff(task['agent'], next_agent, followup['id'])
```

### Conflict Detection

```python
def detect_conflicts():
    artifact_map = defaultdict(list)
    
    # Build map of artifacts to in-progress tasks
    for agent_dir in glob("work/assigned/*/"):
        for task_file in glob(f"{agent_dir}/*.yaml"):
            task = read_yaml(task_file)
            if task['status'] == 'in_progress':
                for artifact in task['artefacts']:
                    artifact_map[artifact].append(task['id'])
    
    # Warn on conflicts
    for artifact, task_ids in artifact_map.items():
        if len(task_ids) > 1:
            log_warning(f"Conflict: {artifact} targeted by {task_ids}")
```

### Timeout Detection

```python
def check_timeouts():
    timeout_hours = 2  # Configurable
    cutoff = now() - timedelta(hours=timeout_hours)
    
    for agent_dir in glob("work/assigned/*/"):
        for task_file in glob(f"{agent_dir}/*.yaml"):
            task = read_yaml(task_file)
            if task['status'] == 'in_progress':
                started_at = parse_iso8601(task['started_at'])
                if started_at < cutoff:
                    log_warning(f"Task {task['id']} stalled (>{timeout_hours}h)")
```

### Scheduling Options

**Option 1: Cron (Unix)**

```bash
# Run every 5 minutes
*/5 * * * * cd /path/to/repo && python work/scripts/coordinator.py
```

**Option 2: CI/CD (GitHub Actions example)**

```yaml
name: Coordinator
on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:       # Manual trigger

jobs:
  orchestrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Coordinator
        run: python work/scripts/coordinator.py
      - name: Commit changes
        run: |
          git config user.name "Coordinator"
          git config user.email "coordinator@example.com"
          git add work/
          git commit -m "Coordinator: task routing" || true
          git push
```

**Option 3: Manual Execution**

```bash
# Run manually
python work/scripts/coordinator.py

# Or as part of workflow
./run-coordinator.sh
```

### Manual Override

Humans can always:
- Create tasks manually in `work/inbox/`
- Move tasks between directories
- Edit task YAML directly
- Assign tasks by moving to `work/assigned/<agent>/`
- Complete tasks by moving to `work/done/`
- Retry failed tasks by resetting status

The Coordinator respects manual actions and does not override human decisions.

## Related

- **Doctrine:** DDR-004 (File-Based Coordination) - coordination mechanism
- **Doctrine:** DDR-005 (Task Lifecycle) - state management
- **Doctrine:** DDR-006 (Work Directory Structure) - directory layout
- **Approach:** Orchestration pattern (framework principles)
- **Implementation:** See repository-specific ADRs for coordinator implementation
