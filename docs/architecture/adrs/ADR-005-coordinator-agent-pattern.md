# ADR-005: Coordinator Agent Pattern

**status**: `Accepted`  
**date**: 2025-11-20  
**updated**: 2025-11-23

> **Implementation Note**: The Coordinator pattern described in this ADR is implemented as `agent_orchestrator.py` to more clearly convey its role in orchestrating multiple agents. The term "Coordinator" remains valid as a pattern name, while the implementation uses the more descriptive "Agent Orchestrator" naming.

### Context

In a multi-agent orchestration system where specialized agents operate independently on domain-specific tasks, there is a need for:

- **Task assignment**: Routing incoming tasks to appropriate agents
- **Workflow sequencing**: Creating follow-up tasks based on agent handoffs
- **Conflict detection**: Identifying when multiple agents target the same artifact
- **Status monitoring**: Tracking overall system health and progress
- **Error handling**: Detecting and escalating stalled or failed tasks
- **Audit logging**: Recording system-wide orchestration events

Without coordination:

- Tasks may sit unassigned in inbox indefinitely
- Multi-step workflows require manual intervention between steps
- Conflicting work may go undetected until merge conflicts occur
- System bottlenecks are invisible
- Failed tasks may be lost or forgotten

Possible approaches:

1. **No coordinator**: Humans manually assign all tasks
2. **Coordinator agent**: Dedicated meta-agent for orchestration
3. **Distributed coordination**: Agents self-assign and coordinate peer-to-peer
4. **External orchestrator**: Separate service (GitHub Actions, cron, etc.)

We need a solution that:

- Maintains simplicity and transparency
- Doesn't require running services
- Allows human override at any point
- Scales to multiple concurrent agents
- Provides visibility into system state

### Decision

**We will implement a Coordinator agent as a specialized meta-agent responsible for orchestration tasks but not artifact generation.**

**Responsibilities:**

1. **Task Assignment**
   - Monitor `work/inbox/` for new tasks
   - Match tasks to agents based on `agent:` field
   - Move task files to `work/assigned/<agent>/`
   - Update task status from `new` to `assigned`

2. **Workflow Sequencing**
   - Monitor `work/done/` for completed tasks
   - Read `next_agent:` field from task result
   - Create follow-up tasks in `work/inbox/`
   - Log handoffs in `work/collaboration/HANDOFFS.md`

3. **Conflict Detection**
   - Track which artifacts are being modified by which tasks
   - Warn when multiple in-progress tasks target same artifact
   - Serialize conflicting tasks when necessary

4. **Status Monitoring**
   - Update `work/collaboration/AGENT_STATUS.md` periodically
   - Detect tasks stuck in `in_progress` for too long (timeout)
   - Flag agents that haven't reported activity recently

5. **Error Handling**
   - Monitor tasks in `error` state
   - Log errors to `work/collaboration/WORKFLOW_LOG.md`
   - Escalate to humans via notifications (optional)

6. **Audit Logging**
   - Record all orchestration events in `WORKFLOW_LOG.md`
   - Maintain complete timeline of task movements
   - Provide data for retrospectives and optimization

**Execution Model:**

- **Polling-based**: Coordinator runs periodically (e.g., every 5 minutes via cron or GitHub Actions)
- **Idempotent**: Safe to run multiple times, no side effects from repeated execution
- **Stateless**: All state stored in files, no in-memory state
- **Manual override**: Humans can perform any Coordinator action manually

**Non-Responsibilities:**

- ❌ Does NOT generate artifacts (documentation, code, diagrams)
- ❌ Does NOT execute agent-specific logic
- ❌ Does NOT make strategic decisions (only operational routing)
- ❌ Does NOT modify agent outputs

### Rationale

**Why a dedicated Coordinator agent?**

- **Separation of concerns**: Orchestration logic separated from domain logic
- **Single responsibility**: One agent handles all task routing
- **Consistency**: Centralized logic ensures uniform handling
- **Auditability**: All coordination decisions in one place
- **Simplicity**: Agents focus on their specialization, not coordination

**Why not distributed coordination?**

- **Complexity**: Peer-to-peer coordination requires consensus protocols
- **Race conditions**: Multiple agents claiming same task needs locking
- **Audit trail**: Distributed decisions harder to track
- **Simplicity**: Centralized coordination is easier to reason about

**Why polling-based execution?**

- **No running services**: Can be triggered by cron, GitHub Actions, or manual invocation
- **Git-native**: Operates on committed state, no ephemeral queues
- **Debugging**: Easy to inspect state before/after execution
- **Idempotent**: Safe to run multiple times

**Why stateless design?**

- **Recovery**: No in-memory state to lose on crash
- **Transparency**: All state visible in files
- **Parallel execution**: Multiple Coordinator instances can run (though not recommended)
- **Simplicity**: No need for state persistence or recovery logic

**Trade-offs accepted:**

- **Latency**: Polling introduces delay (5-minute cycles) (acceptable: tasks are long-running anyway)
- **Single point of coordination**: Coordinator is a bottleneck (mitigated by its simplicity and speed)
- **No real-time**: Can't react instantly to task completion (acceptable: asynchronous by design)

**Alternatives considered:**

1. **Manual coordination**: Humans assign all tasks
   - Rejected: Doesn't scale, error-prone, slow
2. **Event-driven coordination**: GitHub Actions on every file change
   - Rejected: Too chatty, rate limits, complex to debug
3. **Agent self-assignment**: Agents watch inbox and claim tasks
   - Rejected: Race conditions, no centralized audit, complex conflict detection
4. **External orchestration service**: Separate Python/Go service
   - Rejected: Requires running service, not Git-native, operational overhead

### Envisioned Consequences

**Positive:**

- ✅ **Automation**: Tasks automatically routed without human intervention
- ✅ **Workflow chaining**: Multi-step workflows happen automatically via `next_agent`
- ✅ **Visibility**: Central view of system state and progress
- ✅ **Safety**: Conflict detection prevents simultaneous editing
- ✅ **Auditability**: Complete log of orchestration decisions
- ✅ **Simplicity**: Agents don't need coordination logic
- ✅ **Human override**: Coordinator is optional, humans can do any task manually

**Negative:**

- ⚠️ **Polling delay**: 5-minute cycles introduce latency (acceptable)
- ⚠️ **Single coordinator**: No redundancy (mitigated by stateless design, easy restart)
- ⚠️ **Complexity**: One more agent to maintain (mitigated by separation of concerns)
- ⚠️ **Bottleneck**: High task volume could overwhelm Coordinator (unlikely given task duration)

**Risks:**

- **Coordinator failure**: Tasks sit unassigned → Manual assignment fallback, alerts
- **Race conditions**: Multiple Coordinators running → Use file locking, document "run one at a time"
- **Conflict detection false positives**: Over-serialization slows workflow → Tune conflict detection heuristics
- **Timeout too aggressive**: Valid long-running tasks flagged as stalled → Make timeout configurable per agent

**Dependencies:**

- Requires Coordinator agent profile (`.github/agents/coordinator.agent.md`)
- Requires `work/assigned/coordinator/` directory
- Requires collaboration artifacts (AGENT_STATUS, HANDOFFS, WORKFLOW_LOG)
- Requires validation scripts to check Coordinator outputs

### Coordinator Workflow

**Main loop (pseudo-code):**

```python
def coordinator_loop():
    # 1. Process inbox
    for task in list_files("work/inbox/*.yaml"):
        agent = read_yaml(task)['agent']
        validate_task(task)
        move_file(task, f"work/assigned/{agent}/")
        update_status(task, "assigned")
        log_event(f"Assigned task {task.id} to {agent}")
    
    # 2. Process completed tasks
    for task in list_files("work/done/*.yaml"):
        result = read_yaml(task)['result']
        if 'next_agent' in result:
            create_followup_task(task, result['next_agent'])
            log_handoff(task.agent, result['next_agent'], task.artefacts)
    
    # 3. Monitor active tasks
    for agent_dir in list_dirs("work/assigned/*/"):
        for task in list_files(f"{agent_dir}/*.yaml"):
            if task.status == "in_progress":
                check_timeout(task)
            if task.status == "error":
                escalate_error(task)
    
    # 4. Detect conflicts
    active_tasks = list_all_active_tasks()
    artifacts = group_by_artifact(active_tasks)
    for artifact, tasks in artifacts.items():
        if len(tasks) > 1:
            log_conflict(artifact, tasks)
    
    # 5. Update status dashboard
    update_agent_status()
    
    # 6. Archive old completed tasks
    archive_old_tasks(retention_days=30)
```

**Scheduling:**

```yaml
# .github/workflows/agent-orchestrator.yml
name: Agent Orchestrator

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:  # Manual trigger

jobs:
  orchestrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Agent Orchestrator
        run: |
          python work/scripts/agent_orchestrator.py
      - name: Commit changes
        run: |
          git config user.name "Agent Orchestrator"
          git config user.email "orchestrator@sddevelopment.be"
          git add work/
          git commit -m "Agent Orchestrator: task routing and status update" || true
          git push
```

**Local execution:**

```bash
# Run manually
python work/scripts/agent_orchestrator.py

# Or via cron (every 5 minutes)
*/5 * * * * cd /path/to/repo && python work/scripts/agent_orchestrator.py
```

### Task Assignment Logic

**Simple assignment:**

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

**Workflow chaining:**

```python
def process_completed_task(task_file):
    task = read_yaml(task_file)
    result = task.get('result', {})
    next_agent = result.get('next_agent')
    
    if next_agent:
        # Create follow-up task
        followup = {
            'id': generate_task_id(next_agent),
            'agent': next_agent,
            'status': 'new',
            'title': result.get('next_task_title', f"Follow-up to {task['id']}"),
            'artefacts': result.get('next_artefacts', task['artefacts']),
            'context': {
                'previous_task': task['id'],
                'previous_agent': task['agent'],
                'notes': result.get('next_task_notes', [])
            },
            'created_at': now_iso8601(),
            'created_by': 'coordinator'
        }
        
        followup_file = f"work/inbox/{followup['id']}.yaml"
        write_yaml(followup_file, followup)
        
        log_handoff(task['agent'], next_agent, task['artefacts'], followup['id'])
```

### Conflict Detection

**Artifact tracking:**

```python
def detect_conflicts():
    # Build map of artifacts to in-progress tasks
    artifact_map = defaultdict(list)
    
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
            # Optionally: pause all but first task
```

### Timeout Detection

**Stalled task identification:**

```python
def check_timeouts():
    timeout_hours = 2  # Configurable per agent
    cutoff = now() - timedelta(hours=timeout_hours)
    
    for agent_dir in glob("work/assigned/*/"):
        for task_file in glob(f"{agent_dir}/*.yaml"):
            task = read_yaml(task_file)
            if task['status'] == 'in_progress':
                started_at = parse_iso8601(task['started_at'])
                if started_at < cutoff:
                    log_warning(f"Task {task['id']} stalled (>{timeout_hours}h)")
                    # Optionally: notify human, mark as error
```

### Status Dashboard

**Agent status tracking:**

```python
def update_agent_status():
    status = {}
    
    for agent_dir in glob("work/assigned/*/"):
        agent = basename(agent_dir)
        tasks = glob(f"{agent_dir}/*.yaml")
        
        in_progress = [t for t in tasks if read_yaml(t)['status'] == 'in_progress']
        assigned = [t for t in tasks if read_yaml(t)['status'] == 'assigned']
        
        status[agent] = {
            'assigned': len(assigned),
            'in_progress': len(in_progress),
            'current_task': in_progress[0]['id'] if in_progress else 'Idle',
            'last_seen': get_last_activity(agent_dir)
        }
    
    write_status_markdown("work/collaboration/AGENT_STATUS.md", status)
```

### Manual Override

**Humans can always:**

- Create tasks manually in `work/inbox/`
- Move tasks between directories
- Edit task YAML directly
- Assign tasks by moving files to `work/assigned/<agent>/`
- Complete tasks by moving to `work/done/`
- Retry failed tasks by resetting status

**Coordinator respects manual actions:**

- Skips already-assigned tasks (checks timestamp or manual flag)
- Logs manual interventions in WORKFLOW_LOG
- Does not override human decisions

### Considered Alternatives

**1. No Coordinator (Pure Manual)**

- **Approach**: Humans perform all task routing and monitoring
- **Pros**: Simplest, no code to maintain, full control
- **Cons**: Doesn't scale, error-prone, slow, humans become bottleneck
- **Reason rejected**: Defeats purpose of multi-agent automation

**2. Agent Self-Assignment**

- **Approach**: Agents watch `work/inbox/` and claim tasks matching their specialization
- **Pros**: Decentralized, no single coordinator needed
- **Cons**: Race conditions, no centralized audit, conflict detection complex, competing agents
- **Reason rejected**: Adds complexity to every agent, harder to debug

**3. GitHub Actions Per Agent**

- **Approach**: Each agent has a workflow triggered on file changes in its directory
- **Pros**: Event-driven, automatic, GitHub-native
- **Cons**: Too chatty (triggers on every file change), rate limits, hard to debug workflow chains
- **Reason rejected**: Polling with Coordinator is simpler and more debuggable

**4. External Orchestration Service**

- **Approach**: Separate Python/Go service with database and API
- **Pros**: Real-time, powerful queries, scalable
- **Cons**: Requires running service, operational overhead, not Git-native, not transparent
- **Reason rejected**: Over-engineered, loses simplicity and transparency

**5. Distributed Consensus (Raft/Paxos)**

- **Approach**: Agents coordinate using consensus protocol
- **Pros**: Decentralized, fault-tolerant, no single point of failure
- **Cons**: Extreme complexity, requires persistent connections, overkill for file-based system
- **Reason rejected**: Massive complexity for minimal benefit

---

**Related ADRs:**

- [ADR-002: File-Based Asynchronous Agent Coordination](ADR-008-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle and State Management](ADR-003-task-lifecycle-state-management.md)
- [ADR-004: Work Directory Structure](ADR-004-work-directory-structure.md)

**References:**

- [Async Multi-Agent Orchestration Architecture](../design/async_multiagent_orchestration.md)
- Issue #8: Asynchronous Multi-Agent Orchestration (File-Driven Model)
