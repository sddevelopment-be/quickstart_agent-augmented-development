# Repository Workflows

_Version: 1.0.0_  
_Generated: 2025-11-23T22:36:42Z_  
_Agent: Bootstrap Bill_  
_Task: 2025-11-23T2157-bootstrap-bill-repomap-update_

## Overview

This document describes the operational workflows in the quickstart_agent-augmented-development repository, with emphasis on file-based multi-agent orchestration patterns. It serves as a playbook for understanding how tasks flow through the system and how agents coordinate work.

## Table of Contents

1. [File-Based Orchestration Workflow](#file-based-orchestration-workflow)
2. [Task Lifecycle](#task-lifecycle)
3. [Agent Execution Patterns](#agent-execution-patterns)
4. [Multi-Agent Coordination](#multi-agent-coordination)
5. [CI/CD Automation](#cicd-automation)
6. [Validation Workflows](#validation-workflows)
7. [Documentation Workflows](#documentation-workflows)
8. [Error Handling and Recovery](#error-handling-and-recovery)

---

## File-Based Orchestration Workflow

### Core Principle

All orchestration state is maintained in Git-tracked YAML files. Task progression is visible through file movements between directories. No central database or server required.

### Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     File-Based Orchestration                      │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   Human/System creates │
                    │   task YAML in inbox/  │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Agent Orchestrator     │
                    │ - Scans inbox/         │
                    │ - Routes to agent queue│
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Task → assigned/<agent>│
                    │ Status: assigned       │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Agent polls queue      │
                    │ Picks up task          │
                    │ Status: in_progress    │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Agent processes task   │
                    │ - Reads context        │
                    │ - Creates artifacts    │
                    │ - Updates status       │
                    └────────────┬───────────┘
                                 │
                    ┌────────────┴───────────┐
                    ▼                        ▼
        ┌───────────────────┐    ┌──────────────────┐
        │ Success           │    │ Error            │
        │ Status: done      │    │ Status: error    │
        │ Add result block  │    │ Add error block  │
        └─────────┬─────────┘    └────────┬─────────┘
                  │                       │
                  ▼                       ▼
        ┌───────────────────┐    ┌──────────────────┐
        │ Move to done/     │    │ Stays in queue   │
        │ Optional: handoff │    │ Requires human   │
        └─────────┬─────────┘    └──────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ Orchestrator      │
        │ creates follow-up │
        │ (if handoff)      │
        └───────────────────┘
```

### Directory Flow

```
work/
├── inbox/                    # Entry point (new tasks)
│   └── [task].yaml           # status: new
│
├── assigned/<agent>/         # Agent-specific queues
│   └── [task].yaml           # status: assigned → in_progress
│
├── done/                     # Completed tasks
│   └── [task].yaml           # status: done (with result block)
│
└── archive/<YYYY-MM>/        # Long-term storage
    └── [task].yaml           # Archived after 30 days
```

---

## Task Lifecycle

### State Machine

```
                  ┌─────┐
                  │ new │ ◄────────── Initial state (inbox/)
                  └──┬──┘
                     │
                     │ Orchestrator assignment
                     ▼
              ┌──────────┐
              │ assigned │ ◄────────── Routed to agent queue
              └─────┬────┘
                    │
                    │ Agent picks up
                    ▼
            ┌─────────────┐
            │ in_progress │ ◄────────── Agent actively working
            └──────┬──────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    ┌──────┐              ┌───────┐
    │ done │              │ error │ ◄─── Requires intervention
    └──┬───┘              └───────┘
       │
       │ After 30 days
       ▼
  ┌─────────┐
  │ archive │ ◄──────────────────── Long-term storage
  └─────────┘
```

### State Transitions (Agent Responsibility)

#### 1. new → assigned

**Performed By:** Agent Orchestrator

**Actions:**
```yaml
# Before (inbox/):
status: "new"
created_at: "2025-11-23T15:00:00Z"

# After (assigned/<agent>/):
status: "assigned"
assigned_at: "2025-11-23T15:01:00Z"
```

#### 2. assigned → in_progress

**Performed By:** Agent

**Actions:**
```yaml
status: "in_progress"
started_at: "2025-11-23T15:05:00Z"
```

**Agent Updates File In-Place:**
```bash
# Read task
task_data = load_yaml("work/assigned/architect/task.yaml")

# Update status
task_data["status"] = "in_progress"
task_data["started_at"] = current_timestamp()

# Write back
save_yaml("work/assigned/architect/task.yaml", task_data)
```

#### 3. in_progress → done

**Performed By:** Agent

**Actions:**
```yaml
status: "done"
result:
  summary: "Completed architecture design"
  artefacts:
    - docs/architecture/design/api.md
  metrics:
    token_count: 12500
    duration_seconds: 1500
  completed_at: "2025-11-23T15:30:00Z"
```

**Agent Moves File:**
```bash
# Update task file
task_data["status"] = "done"
task_data["result"] = {
    "summary": "...",
    "artefacts": [...],
    "completed_at": current_timestamp()
}
save_yaml("work/assigned/architect/task.yaml", task_data)

# Move to done/
move_file(
    "work/assigned/architect/task.yaml",
    "work/done/task.yaml"
)
```

#### 4. in_progress → error

**Performed By:** Agent

**Actions:**
```yaml
status: "error"
error:
  message: "Missing required context"
  details: "Need authentication requirements specification"
  failed_at: "2025-11-23T15:10:00Z"
  retry_allowed: true
```

**Agent Leaves File In Queue:**
```bash
# Update status but don't move file
task_data["status"] = "error"
task_data["error"] = {
    "message": "...",
    "details": "...",
    "failed_at": current_timestamp()
}
save_yaml("work/assigned/architect/task.yaml", task_data)
```

### Task File Evolution

**Initial (inbox/):**
```yaml
id: "2025-11-23T1500-architect-design-api"
agent: "architect"
status: "new"
title: "Design REST API"
artefacts:
  - docs/architecture/design/api.md
created_at: "2025-11-23T15:00:00Z"
created_by: "stijn"
```

**Assigned (assigned/architect/):**
```yaml
id: "2025-11-23T1500-architect-design-api"
agent: "architect"
status: "assigned"
title: "Design REST API"
artefacts:
  - docs/architecture/design/api.md
created_at: "2025-11-23T15:00:00Z"
created_by: "stijn"
assigned_at: "2025-11-23T15:01:00Z"
```

**In Progress (assigned/architect/):**
```yaml
id: "2025-11-23T1500-architect-design-api"
agent: "architect"
status: "in_progress"
title: "Design REST API"
artefacts:
  - docs/architecture/design/api.md
created_at: "2025-11-23T15:00:00Z"
created_by: "stijn"
assigned_at: "2025-11-23T15:01:00Z"
started_at: "2025-11-23T15:05:00Z"
```

**Completed (done/):**
```yaml
id: "2025-11-23T1500-architect-design-api"
agent: "architect"
status: "done"
title: "Design REST API"
artefacts:
  - docs/architecture/design/api.md
created_at: "2025-11-23T15:00:00Z"
created_by: "stijn"
assigned_at: "2025-11-23T15:01:00Z"
started_at: "2025-11-23T15:05:00Z"
result:
  summary: "Completed REST API design with OpenAPI spec"
  artefacts:
    - docs/architecture/design/api.md
  metrics:
    token_count: 12500
    duration_seconds: 1500
  completed_at: "2025-11-23T15:30:00Z"
```

---

## Agent Execution Patterns

### Polling Pattern (Recommended)

Agents continuously poll their assigned directory for new tasks.

**Pseudocode:**
```python
class Agent:
    def run(self):
        while True:
            tasks = list_files(f"work/assigned/{self.agent_name}/")
            
            for task_file in tasks:
                task = load_yaml(task_file)
                
                if task["status"] == "assigned":
                    self.process_task(task_file)
            
            sleep(30)  # Poll every 30 seconds
```

**Reference Implementation:** `ops/scripts/orchestration/example_agent.py`

### Single-Shot Pattern

Agent processes one task and exits. Suitable for CI/CD integration.

**Pseudocode:**
```python
class Agent:
    def run_once(self):
        tasks = list_files(f"work/assigned/{self.agent_name}/")
        
        if tasks:
            task_file = tasks[0]
            task = load_yaml(task_file)
            
            if task["status"] == "assigned":
                self.process_task(task_file)
```

### Base Interface

All agents inherit from `ops/scripts/orchestration/agent_base.py`:

```python
from work.scripts.agent_base import AgentBase

class MyAgent(AgentBase):
    def get_agent_name(self) -> str:
        return "my-agent"
    
    def process_task(self, task_file: str) -> bool:
        # 1. Update status to in_progress
        task = self.load_task(task_file)
        task["status"] = "in_progress"
        task["started_at"] = self.current_timestamp()
        self.save_task(task_file, task)
        
        # 2. Perform work
        try:
            artifacts = self.do_work(task)
            
            # 3. Add result block
            task["result"] = {
                "summary": "Work completed",
                "artefacts": artifacts,
                "completed_at": self.current_timestamp()
            }
            task["status"] = "done"
            self.save_task(task_file, task)
            
            # 4. Move to done/
            self.move_to_done(task_file)
            
            return True
            
        except Exception as e:
            # 5. Handle errors
            task["error"] = {
                "message": str(e),
                "failed_at": self.current_timestamp()
            }
            task["status"] = "error"
            self.save_task(task_file, task)
            
            return False
```

---

## Multi-Agent Coordination

### Handoff Workflow

Agents create follow-up tasks by adding handoff information to the `result` block.

**Pattern:**

```yaml
# Task 1 (architect completes):
status: "done"
result:
  summary: "Architecture design completed"
  artefacts:
    - docs/architecture/design/api.md
  next_agent: "backend-dev"
  next_task_title: "Implement user API endpoints"
  next_artefacts:
    - src/api/users.py
  next_task_notes:
    - "Follow design in docs/architecture/design/api.md"
  completed_at: "2025-11-23T15:30:00Z"
```

**Orchestrator Action:**

Creates new task in inbox:

```yaml
id: "2025-11-23T1530-backend-dev-implement-api"
agent: "backend-dev"
status: "new"
title: "Implement user API endpoints"
artefacts:
  - src/api/users.py
context:
  parent_task_id: "2025-11-23T1500-architect-design-api"
  notes:
    - "Follow design in docs/architecture/design/api.md"
created_at: "2025-11-23T15:30:30Z"
created_by: "agent-orchestrator"
```

### Sequential Workflow Example

**Scenario:** Design → Implement → Test

```
┌────────────┐
│ architect  │ Design API spec
└──────┬─────┘
       │ handoff: backend-dev
       ▼
┌────────────┐
│ backend-dev│ Implement endpoints
└──────┬─────┘
       │ handoff: test-agent
       ▼
┌────────────┐
│ test-agent │ Write E2E tests
└────────────┘
```

**Task Chain:**

1. **Task 1:** `2025-11-23T1500-architect-design-api.yaml`
   - Agent: architect
   - Artifact: docs/architecture/design/api.md
   - Handoff: backend-dev

2. **Task 2:** `2025-11-23T1530-backend-dev-implement-api.yaml`
   - Agent: backend-dev
   - Artifact: src/api/users.py
   - Parent: Task 1
   - Handoff: test-agent

3. **Task 3:** `2025-11-23T1600-test-agent-test-api.yaml`
   - Agent: test-agent
   - Artifact: tests/api/test_users.py
   - Parent: Task 2

### Parallel Workflow Example

**Scenario:** Design → (Implement Frontend + Implement Backend)

```
┌────────────┐
│ architect  │ Design system
└──────┬─────┘
       │
       ├────── handoff: frontend
       │
       └────── handoff: backend-dev
       │
       ▼
┌────────────┐     ┌────────────┐
│ frontend   │     │ backend-dev│
│ (parallel) │     │ (parallel) │
└────────────┘     └────────────┘
```

**Implementation:**

Architect creates multiple handoffs:

```yaml
result:
  summary: "System design completed"
  handoffs:
    - agent: "frontend"
      title: "Implement UI components"
      artefacts: ["src/ui/components.tsx"]
    - agent: "backend-dev"
      title: "Implement API endpoints"
      artefacts: ["src/api/endpoints.py"]
  completed_at: "2025-11-23T15:30:00Z"
```

Orchestrator creates both tasks simultaneously in inbox.

### Collaboration Artifacts

**Agent Status Dashboard:** `work/collaboration/AGENT_STATUS.md`

Updated by orchestrator:

```markdown
| Agent | Status | Last Active | Pending | In Progress | Completed (24h) |
|-------|--------|-------------|---------|-------------|-----------------|
| architect | active | 2025-11-23T15:30:00Z | 0 | 1 | 5 |
| backend-dev | idle | 2025-11-23T14:00:00Z | 2 | 0 | 3 |
```

**Handoff Log:** `work/collaboration/HANDOFFS.md`

```markdown
## 2025-11-23T15:30:00Z: architect → backend-dev

**Parent Task:** 2025-11-23T1500-architect-design-api
**New Task:** 2025-11-23T1530-backend-dev-implement-api
**Artifacts:** src/api/users.py
**Context:** Follow design in docs/architecture/design/api.md
```

**Workflow Log:** `work/collaboration/WORKFLOW_LOG.md`

```markdown
[2025-11-23T15:00:00Z] Task created: 2025-11-23T1500-architect-design-api
[2025-11-23T15:01:00Z] Task assigned: architect
[2025-11-23T15:05:00Z] Task started: architect
[2025-11-23T15:30:00Z] Task completed: architect
[2025-11-23T15:30:30Z] Handoff created: backend-dev
```

---

## CI/CD Automation

### Automated Orchestration

**Workflow:** `.github/workflows/orchestration.yml`

**Trigger:**
- Cron: `*/15 * * * *` (every 15 minutes)
- Manual: workflow_dispatch

**Steps:**
1. Checkout repository
2. Setup Python 3.x
3. Install dependencies (`requirements.txt`)
4. Run `python ops/scripts/orchestration/agent_orchestrator.py`
5. Commit changes (task movements, status updates)
6. Push to branch

**Configuration:**
```yaml
name: Agent Orchestration

on:
  schedule:
    - cron: '*/15 * * * *'
  workflow_dispatch:

jobs:
  orchestrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt
      - run: python ops/scripts/orchestration/agent_orchestrator.py
      - run: |
          git config user.name "Agent Orchestrator"
          git config user.email "orchestrator@example.com"
          git add work/
          git commit -m "chore: orchestrator update" || true
          git push
```

### Validation on Push

**Workflow:** `.github/workflows/validation.yml`

**Trigger:** Push, Pull Request

**Steps:**
1. Validate task YAML schemas
2. Validate work directory structure
3. Validate task naming conventions
4. Report validation errors

**Configuration:**
```yaml
name: Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - name: Validate task schemas
        run: |
          for task in work/collaboration/inbox/*.yaml work/collaboration/assigned/*/*.yaml; do
            python validation/validate-task-schema.py "$task" || exit 1
          done
      - name: Validate work structure
        run: bash validation/validate-work-structure.sh
```

### Diagram Rendering

**Workflow:** `.github/workflows/diagram-rendering.yml`

**Trigger:** Push with `.puml` changes

**Steps:**
1. Detect modified PlantUML files
2. Generate PNG diagrams
3. Commit rendered images

---

## Validation Workflows

### Pre-Task Validation

**Before creating task:**

```bash
# 1. Validate naming convention
bash validation/validate-task-naming.sh work/collaboration/inbox/task.yaml

# 2. Validate YAML schema
python validation/validate-task-schema.py work/collaboration/inbox/task.yaml

# 3. Validate structure
bash validation/validate-work-structure.sh
```

### Post-Task Validation

**After completing task:**

```bash
# 1. Verify artifacts created
for artifact in $(yq '.artefacts[]' task.yaml); do
  test -f "$artifact" || echo "Missing: $artifact"
done

# 2. Verify status updated
yq '.status' task.yaml  # Should be "done"

# 3. Verify moved to done/
test -f "work/done/task.yaml"
```

---

## Documentation Workflows

### Creating ADRs

**Workflow:**

1. Copy template: `cp docs/templates/architecture/adr-template.md docs/architecture/adrs/ADR-XXX-title.md`
2. Fill in sections (Status, Context, Decision, Consequences)
3. Update `docs/architecture/adrs/README.md` index
4. Submit PR
5. After merge, update status to "Accepted"

### Updating HOW_TO_USE Guides

**Workflow:**

1. Identify guide: `docs/HOW_TO_USE/<topic>.md`
2. Make updates (ensure examples work)
3. Update version/timestamp
4. Cross-reference related ADRs
5. Submit PR

### Generating Diagrams

**Workflow:**

1. Create PlantUML: `docs/architecture/diagrams/<name>.puml`
2. Push to branch
3. CI renders PNG automatically
4. Commit includes both `.puml` and `.png`

---

## Error Handling and Recovery

### Task Failure Workflow

**Agent Detects Error:**

```yaml
status: "error"
error:
  message: "Missing authentication specification"
  details: "Cannot proceed without auth requirements"
  failed_at: "2025-11-23T15:10:00Z"
  retry_allowed: true
  required_action: "Add context.auth_spec field"
```

**Human Intervention:**

1. Review error details
2. Update task context
3. Reset status to `assigned`
4. Agent retries on next poll

**Recovery Pattern:**

```bash
# Edit task file
vi work/assigned/architect/task.yaml

# Add missing context
yq eval '.context.auth_spec = "docs/auth-requirements.md"' -i task.yaml

# Reset status
yq eval '.status = "assigned"' -i task.yaml

# Remove error block
yq eval 'del(.error)' -i task.yaml

# Agent will retry on next poll
```

### Stuck Task Detection

**Orchestrator monitors timeouts:**

```python
# Default timeout: 2 hours
if task["status"] == "in_progress":
    elapsed = now() - parse_time(task["started_at"])
    
    if elapsed > timedelta(hours=2):
        log_warning(f"Task {task['id']} timeout")
        # Alert human via WORKFLOW_LOG
```

### Orphaned Task Cleanup

**Validation script detects:**

```bash
# Finds tasks in incorrect directories
bash validation/validate-work-structure.sh

# Reports:
# - Tasks in wrong agent queue
# - Tasks with invalid status
# - Tasks missing timestamps
```

---

## Summary: Key Workflows

| Workflow | Type | Trigger | Output |
|----------|------|---------|--------|
| Task Creation | Manual | Human/System | YAML in inbox/ |
| Task Assignment | Automated | Orchestrator | Move to assigned/ |
| Task Processing | Agent-driven | Agent poll | Artifacts + done/ |
| Task Handoff | Agent-driven | result.next_agent | New task in inbox/ |
| CI Orchestration | Automated | Cron | State updates |
| Validation | Automated | Push/PR | Pass/Fail |
| Diagram Render | Automated | .puml push | PNG images |
| Error Recovery | Manual | Human intervention | Reset status |

---

## Related Documentation

- **REPO_MAP.md**: Repository structure
- **SURFACES.md**: Public interfaces
- **DEPENDENCIES.md**: Dependency inventory
- **work/README.md**: Orchestration system guide
- **docs/HOW_TO_USE/multi-agent-orchestration.md**: Detailed orchestration guide
- **docs/architecture/adrs/ADR-003-task-lifecycle-state-management.md**: State machine spec
- **docs/architecture/adrs/ADR-008-file-based-async-coordination.md**: Coordination architecture

---

_Generated by Bootstrap Bill (Task: 2025-11-23T2157-bootstrap-bill-repomap-update)_  
_For updates, assign new task to `bootstrap-bill` agent_  
_Workflow changes: Track via Git history on this file_
