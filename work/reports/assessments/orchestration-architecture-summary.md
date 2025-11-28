# Async Multi-Agent Orchestration - Architecture Summary

_Created: 2025-11-20_  
_Issue: #8_  
_Architect: Alphonso_

## Executive Summary

This document summarizes the architectural artifacts created for the asynchronous, file-driven multi-agent orchestration system. The design enables safe, transparent, and predictable collaboration between specialized agents without requiring real-time communication or running services.

## What Was Created

### 1. Architecture Documentation

**Main Architecture Document** (`docs/architecture/async_multiagent_orchestration.md`)
- Overview of file-driven orchestration model
- Directory structure and task representation
- Task lifecycle (new → assigned → in_progress → done → archive)
- Agent roles (specialized agents + Coordinator)
- Workflow patterns (sequential, parallel, convergent)
- GitHub Actions integration
- Quality attributes and security considerations
- ~430 lines, comprehensive system overview

### 2. Architecture Decision Records (ADRs)

**ADR-002: File-Based Asynchronous Agent Coordination**
- Decision: Use file-based task YAML files for coordination
- Rationale: Git-native, transparent, no infrastructure required
- Trade-offs: Latency acceptable, git overhead mitigated by archival
- Alternatives considered: Message queues, databases, GitHub Issues, event buses
- ~156 lines

**ADR-003: Task Lifecycle and State Management**
- Decision: Five-state lifecycle (new, assigned, in_progress, done, error)
- Rationale: Clear ownership, prevents duplicate processing, enables recovery
- Implementation: Directory structure + YAML status field
- Validation rules and error handling
- ~301 lines

**ADR-004: Work Directory Structure and Conventions**
- Decision: Hierarchical structure under `work/` organized by state and agent
- Layout: `inbox/`, `assigned/<agent>/`, `done/`, `archive/`, `collaboration/`
- Naming conventions: ISO 8601 timestamps + agent + slug
- Archive strategy: Monthly subdirectories
- ~464 lines

**ADR-005: Coordinator Agent Pattern**
- Decision: Dedicated meta-agent for orchestration, not artifact generation
- Responsibilities: Task assignment, workflow sequencing, conflict detection, monitoring
- Execution model: Polling-based, idempotent, stateless
- Alternative considered: Manual coordination, agent self-assignment, external service
- ~448 lines

### 3. Technical Design

**Technical Design Document** (`docs/architecture/async_orchestration_technical_design.md`)
- Complete implementation specifications
- Task YAML schema definition with examples
- Directory setup script (`init-work-structure.sh`)
- Coordinator implementation (`coordinator.py`) with full source code
- Agent execution protocol template
- Validation scripts and monitoring tools
- GitHub Actions workflow examples
- ~851 lines including code samples

### 4. Implementation Plan

**Implementation Plan** (`work/collaboration/orchestration-implementation-plan.md`)
- Five phases: Core Infrastructure, Coordinator, Agent Integration, CI, Validation
- 41 discrete tasks with agent assignments
- Timeline: 14-20 workdays (3-4 weeks)
- Success metrics and risk management
- Clear dependencies and critical path
- ~299 lines

## Core Design Decisions

### File-Driven Coordination

**Why Files?**
- Git-native: Every state change is a commit
- Zero infrastructure: No services to run or maintain
- Human-readable: YAML is easy to inspect and edit
- Portable: Works in CI, locally, or any environment
- Debuggable: Read files to understand state

**Trade-off:** Latency (seconds to minutes) vs real-time
- **Acceptable because:** Agent tasks run for minutes to hours, not milliseconds

### Task Lifecycle

**States:** new → assigned → in_progress → done → archive

**Why This Model?**
- Clear ownership at each stage
- Prevents duplicate processing
- Explicit failure handling
- Complete audit trail

**Implementation:** Directory location + YAML status field

### Directory Structure

```
work/
  inbox/              # New tasks
  assigned/
    structural/       # Per-agent directories
    lexical/
    curator/
    ...
  done/               # Completed
  archive/            # Long-term
  collaboration/      # Cross-agent artifacts
```

**Why Hierarchical?**
- Natural separation by state and agent
- Atomic file moves for state transitions
- Simple polling (watch one directory)
- Clear ownership

### Coordinator Agent

**Responsibilities:**
- Assign tasks from inbox to agents
- Create follow-up tasks based on `next_agent`
- Detect timeouts and conflicts
- Update status dashboard
- Archive old tasks

**Why Dedicated Coordinator?**
- Separation of concerns (orchestration vs domain work)
- Centralized audit trail
- Consistent handling of all tasks
- Agents focus on specialization

**Execution:** Polling-based (every 5 minutes), idempotent, stateless

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       work/inbox/                            │
│              (New tasks awaiting assignment)                 │
└───────────────┬────────────────────────────────────────────┘
                │
                │ Coordinator assigns
                ↓
┌─────────────────────────────────────────────────────────────┐
│                   work/assigned/                             │
│  ┌──────────────┬──────────────┬──────────────┬──────────┐  │
│  │ structural/  │ lexical/     │ curator/     │ ...      │  │
│  │              │              │              │          │  │
│  │ Agent polls  │ Agent polls  │ Agent polls  │          │  │
│  │ & executes   │ & executes   │ & executes   │          │  │
│  └──────────────┴──────────────┴──────────────┴──────────┘  │
└───────────────┬────────────────────────────────────────────┘
                │
                │ Agent completes, moves to done
                ↓
┌─────────────────────────────────────────────────────────────┐
│                       work/done/                             │
│              (Completed tasks with results)                  │
└───────────────┬────────────────────────────────────────────┘
                │
                │ Coordinator checks next_agent
                │
                ├──→ Follow-up task? → work/inbox/ (loop)
                │
                └──→ After 30 days → work/archive/
```

## Workflow Example

**Scenario:** Generate structural documentation, then perform lexical analysis

1. **Human creates task:**
   ```yaml
   # work/inbox/2025-11-20T1430-structural-repomap.yaml
   agent: structural
   status: new
   artefacts: [docs/REPO_MAP.md, docs/SURFACES.md]
   ```

2. **Coordinator assigns:**
   - Moves file to `work/assigned/structural/`
   - Updates status to `assigned`
   - Logs event in WORKFLOW_LOG

3. **Structural agent executes:**
   - Polls `work/assigned/structural/`
   - Updates status to `in_progress`
   - Generates artifacts
   - Adds result with `next_agent: lexical`
   - Moves to `work/done/`

4. **Coordinator creates follow-up:**
   - Reads `next_agent: lexical`
   - Creates new task in `work/inbox/`
   - Logs handoff in HANDOFFS.md

5. **Lexical agent executes:**
   - Same pattern as Structural
   - Completes without `next_agent`
   - Task moves to `work/done/`

6. **Archive (30 days later):**
   - Coordinator moves old tasks to `work/archive/2025-11/`

## Key Features

### Transparency
- Every state visible in Git
- All tasks are YAML files you can read
- Complete audit trail in Git log

### Safety
- No silent failures (errors logged in task YAML)
- Conflict detection warns on overlapping work
- Validation scripts enforce consistency
- Human can intervene at any point

### Simplicity
- No running services or databases
- Pure file operations
- Standard tools (Python, Bash, YAML)
- Works locally and in CI

### Composability
- Each agent handles one domain
- Complex workflows via `next_agent` chains
- Parallel execution naturally supported
- Easy to add new agents (create directory + profile)

## Implementation Phases

**Phase 1: Core Infrastructure (CRITICAL)**
- Setup directory structure
- Define task schema
- Create validation scripts
- Agent: Build Automation
- Time: 2-3 workdays

**Phase 2: Coordinator Implementation (CRITICAL)**
- Implement coordinator.py
- Task routing, sequencing, monitoring
- Agent: Build Automation
- Time: 3-4 workdays

**Phase 3: Agent Integration (HIGH)**
- Update all agent profiles
- Test end-to-end workflows
- Agents: Each updates itself
- Time: 5-7 workdays

**Phase 4: GitHub Actions (MEDIUM, optional)**
- CI automation for Coordinator
- Agent: Build Automation
- Time: 2-3 workdays

**Phase 5: Validation & Monitoring (MEDIUM, optional)**
- Enhanced validation tools
- Agent: Build Automation
- Time: 2-3 workdays

**Critical Path:** Phase 1 → Phase 2 → Phase 3 (10-14 workdays)

## Benefits

### For Humans
- ✅ Full visibility into agent activity
- ✅ Can inspect, modify, or create tasks manually
- ✅ Complete audit trail for accountability
- ✅ Simple to understand (just files and directories)

### For Agents
- ✅ Clear task assignment mechanism
- ✅ No coordination logic needed (Coordinator handles it)
- ✅ Focus on specialization, not orchestration
- ✅ Natural workflow chaining via `next_agent`

### For System
- ✅ No infrastructure to maintain
- ✅ Portable across environments
- ✅ Scales to hundreds of tasks
- ✅ Git provides versioning and rollback

## Success Metrics

### Immediate (After Phase 3)
- [ ] Tasks created and automatically assigned
- [ ] End-to-end workflow tested (Structural → Lexical)
- [ ] Coordinator operates reliably
- [ ] Status dashboard provides visibility

### Long-term (After Phase 5)
- [ ] All agents integrated
- [ ] Multi-step workflows automatic
- [ ] Conflicts detected and logged
- [ ] Complete audit trail maintained
- [ ] System scales to 100+ tasks

## Risk Management

| Risk | Mitigation |
|------|------------|
| Coordinator bugs | Extensive testing, Git history recovery |
| Agent integration breaks workflows | Incremental integration, manual fallback |
| GitHub Actions rate limits | Add delays, manual execution fallback |
| Schema evolution | Version schema, migration scripts |
| Directory corruption | Validation scripts in CI, .gitkeep tracking |

## Next Steps

1. **Review and Approve:**
   - Human reviews architecture artifacts
   - Architect validates completeness
   - Planning Agent reviews timeline

2. **Begin Implementation:**
   - Planning Agent creates tasks for Phase 1
   - Build Automation Agent starts directory setup
   - Coordinator assigns tasks

3. **Iterate:**
   - Complete Phase 1, validate
   - Begin Phase 2 with Coordinator
   - Test thoroughly before Phase 3

## Questions?

- **Why files instead of a database?** → Git-native, transparent, no infrastructure
- **Why polling instead of events?** → Simpler, more debuggable, CI-compatible
- **What if Coordinator fails?** → Stateless design, just restart; Git history preserves state
- **Can humans intervene?** → Yes! Move files, edit YAML, create tasks manually
- **How do agents coordinate?** → They don't directly; Coordinator routes tasks
- **What about conflicts?** → Coordinator detects and warns; serialize when needed

## Documentation Map

```
docs/architecture/
  ├── async_multiagent_orchestration.md    (START HERE - overview)
  ├── ADR-002-file-based-async-coordination.md
  ├── ADR-003-task-lifecycle-state-management.md
  ├── ADR-004-work-directory-structure.md
  ├── ADR-005-coordinator-agent-pattern.md
  └── async_orchestration_technical_design.md (implementation details)

work/collaboration/
  ├── orchestration-implementation-plan.md (task breakdown)
  └── orchestration-architecture-summary.md (this document)
```

**Read order:**
1. This summary (you are here)
2. Main architecture doc (overview)
3. ADRs (design rationale)
4. Technical design (implementation)
5. Implementation plan (tasks and timeline)

---

**Status:** ✅ Architecture complete, awaiting approval  
**Next:** Human review → Planning Agent creates tasks → Build Automation starts Phase 1

_Maintained by: Architect Alphonso_  
_Version: 1.0.0_
