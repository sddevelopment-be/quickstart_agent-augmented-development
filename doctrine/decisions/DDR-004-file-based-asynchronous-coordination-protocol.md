# DDR-004: File-Based Asynchronous Coordination Protocol

**Status:** Active  
**Date:** 2026-02-11  
**Supersedes:** Repository-specific coordination implementations (elevated from ADR-008)

---

## Context

Multi-agent systems require coordination mechanisms to distribute work, track progress, and ensure artifacts are produced consistently. Traditional approaches introduce infrastructure dependencies and operational complexity:

- **Message queues:** Require dedicated services, operational expertise, network dependencies
- **RPC/API calls:** Require running processes, introduce coupling and availability concerns
- **Shared databases:** Add persistence layers, schema management, query complexity
- **In-memory coordination:** Lost on crash, not transparent, not portable

Agent-augmented development workflows operate on human timescales (minutes to hours, not milliseconds), making asynchronous coordination acceptable. The framework needs a universal pattern that:

- Works without additional infrastructure or running services
- Remains transparent and human-inspectable at all times
- Leaves complete audit trails
- Integrates naturally with version control workflows
- Requires minimal setup for new adopters
- Supports both automated (CI) and manual (local) execution

## Decision

**We establish file-based task coordination as the framework's fundamental coordination mechanism.**

Repositories adopting this framework coordinate agents through:

### 1. Task Representation

Each task is a **structured file** (YAML, JSON, or similar) with:
- Unique identifier
- Target agent assignment
- Current status
- Required artifacts
- Context and parameters
- Result block (populated on completion)

### 2. State Transitions via Directory Structure

Task status changes through **atomic file movements** between directories:
- Filesystem move operations provide atomicity guarantees
- Directory location reflects current state
- Status field in file mirrors directory state
- Consistency validation detects mismatches

### 3. Agent Assignment Pattern

Tasks assigned by **moving files to agent-specific directories**:
- Each agent watches its designated directory
- File presence = assignment signal
- Multiple agents can work concurrently on different tasks
- No polling of central queue required

### 4. Result Communication

Agents update **task files with result blocks**:
- Result data written to same file
- Result includes artifacts produced, status, and metadata
- Git commits provide change history
- Human and automated reviewers read results from files

### 5. Workflow Sequencing

Multi-step workflows via **explicit agent handoff markers**:
- Task result specifies `next_agent` field
- Coordinator or automation creates follow-up tasks
- Handoff chain documented in task history
- Human override possible at any transition

### 6. Audit Trail

All coordination state tracked in **version control commits**:
- Every state change is a commit
- Full history via version control log
- Diff capability for debugging
- Rollback via version control primitives

## Rationale

### Universal Benefits

**Git-Native Integration:**
- Every state change is a commit, providing full history
- Diff and blame tools show decision progression
- Rollback via standard version control operations
- Branching supports parallel workflow experimentation

**Transparency:**
- YAML/JSON human-readable and editable
- No hidden state or opaque queues
- Problems visible by inspecting files
- Debugging doesn't require special tools

**Zero Infrastructure:**
- No services to run, maintain, secure, or monitor
- No databases requiring schema migrations
- No message brokers requiring cluster management
- Works anywhere with filesystem and version control

**Portability:**
- Works in CI, locally, on any system with file access
- No network dependencies for coordination
- Cross-platform: Linux, macOS, Windows
- Cloud-agnostic: GitHub, GitLab, Bitbucket, on-prem Git

**Recoverability:**
- Version control provides complete state history
- Rollback via `git revert` or `git reset`
- No database restore procedures required
- Lost tasks recoverable from commit history

### Framework-Level Pattern

This pattern applies universally because:
- All repositories have filesystem and version control
- Agent tasks operate on human timescales (asynchronous acceptable)
- Transparency benefits all adopters (debugging, auditing, onboarding)
- Infrastructure simplicity reduces adoption friction

## Consequences

### Positive

- ✅ **Simplicity:** No additional infrastructure or services
- ✅ **Transparency:** Full visibility into task state at any point
- ✅ **Auditability:** Complete history in version control log
- ✅ **Portability:** Works across CI systems, local environments, LLM toolchains
- ✅ **Recoverability:** Rollback via standard version control operations
- ✅ **Extensibility:** Adding agents requires only directory creation
- ✅ **Debuggability:** Read files to understand state, no log aggregation
- ✅ **Collaboration:** Humans can inspect, modify, create tasks manually

### Negative (Accepted Trade-offs)

- ⚠️ **Latency:** File-based coordination operates on seconds-to-minutes scale, not milliseconds (acceptable: agent tasks are long-running)
- ⚠️ **Commit volume:** Many small commits may clutter history (addressed via archive strategies and commit squashing)
- ⚠️ **Race conditions:** Multiple processes modifying same file needs coordination (mitigated by directory-based state and coordinator serialization)
- ⚠️ **Filesystem limits:** Very large task volumes may hit directory size limits (addressed via archive cleanup policies)
- ⚠️ **No ACID transactions:** Multi-file operations are not atomic (mitigated by task design and coordinator patterns)

## Implementation

Repositories adopting this framework should:

### Directory Structure

Organize work directories by lifecycle state:

```
work/
  inbox/              # New tasks awaiting assignment
  assigned/
    <agent-name>/     # Tasks assigned to specific agent
  done/               # Completed tasks
  archive/            # Long-term retention
```

*(See DDR-006 for complete directory structure specifications)*

### Task File Schema

Structured format (YAML example):

```yaml
id: "2026-02-11T1430-agent-task-slug"
agent: "target-agent-name"
status: "new"  # new, assigned, in_progress, done, error
title: "Human-readable task description"
artefacts:
  - "path/to/artifact1.md"
  - "path/to/artifact2.md"
context:
  notes: "Additional context for agent"
created_at: "2026-02-11T14:30:00Z"
result:
  # Populated by agent on completion
  summary: "What was accomplished"
  artifacts_produced: []
  completed_at: "2026-02-11T15:00:00Z"
  next_agent: "follow-up-agent"  # Optional workflow chaining
```

### State Transition Protocol

**Assignment:**
```bash
# Coordinator or human moves task to agent directory
mv work/inbox/task-123.yaml work/assigned/structural/
# Update status field to match
sed -i 's/status: new/status: assigned/' work/assigned/structural/task-123.yaml
```

**Execution:**
```yaml
# Agent updates status in file
status: in_progress
started_at: "2026-02-11T14:30:00Z"
```

**Completion:**
```yaml
# Agent adds result and moves to done
status: done
result:
  summary: "Generated REPO_MAP and SURFACES"
  completed_at: "2026-02-11T14:45:00Z"
```

### Workflow Chaining

Agents specify next steps in result block:

```yaml
result:
  next_agent: "lexical"
  next_task_title: "Voice and style pass on generated documents"
  next_artefacts: ["docs/REPO_MAP.md", "docs/SURFACES.md"]
```

Coordinator or automation creates follow-up task:

```yaml
id: "2026-02-11T1445-lexical-voice-pass"
agent: "lexical"
status: "new"
context:
  previous_task: "2026-02-11T1430-structural-repomap"
  notes: "Apply voice and style guidelines to structural outputs"
```

### Validation Requirements

Repositories should validate:
- **Consistency:** Status field matches directory location
- **Required fields:** All tasks have id, agent, status, artifacts
- **Status values:** Only allowed states (new, assigned, in_progress, done, error)
- **Timestamps:** Status changes include appropriate timestamps
- **Ownership:** Tasks in agent directories match assigned agent

### Atomic Operations

Leverage filesystem guarantees:
- **POSIX rename:** Atomic within same filesystem
- **Directory moves:** Atomic state transitions
- **File locking:** Optional for concurrent write protection
- **Coordinator serialization:** Single coordinator prevents conflicts

## Related

- **Doctrine:** DDR-005 (Task Lifecycle Protocol) - defines state machine
- **Doctrine:** DDR-006 (Work Directory Structure) - specifies directory layout
- **Doctrine:** DDR-007 (Coordinator Pattern) - orchestration responsibilities
- **Approach:** Asynchronous coordination approach (framework principles)
- **Implementation:** See repository-specific ADRs for tooling and automation
