# ADR-047: Human-in-Charge Directory Structure

**status**: Accepted  
**date**: 2026-02-14  
**supersedes**: None  
**related**: ADR-004 (Work Directory Structure), ADR-008 (File-Based Async Coordination), ADR-005 (Coordinator Agent Pattern)

## Context

The current `work/` directory provides comprehensive agent-to-agent coordination through `work/collaboration/` (task lifecycle, handoffs) and `work/reports/` (completed work outputs). However, there is **no dedicated structure for agent-to-human escalations** requiring review or decisions.

### Current Escalation Patterns (Scattered)

**1. AFK Mode Pauses** (`doctrine/shorthands/afk-mode.md`)
- Line 142-148: "Create checkpoint file" for critical decisions
- Current location: `work/reports/logs/[agent]/[timestamp]-afk-pause-[reason].md`
- Problem: Mixed with routine work logs, hard to discover

**2. Executive Summaries**
- Locations: `work/reports/exec_summaries/` AND `work/reports/executive-summaries/`
- Problem: Two directories with same purpose, inconsistent naming

**3. Blockers**
- Tracked in: Task YAML files with `status: error` or `status: frozen`
- Problem: Requires parsing task files, no dedicated review space

**4. Decision Requests**
- No consistent location
- Problem: Ad-hoc placement in agent logs or collaboration notes

### Use Cases Driving Need

**1. Async Coordination Environments**
- GitHub Copilot Web, Claude Projects, Cursor sync mode
- Human not in real-time conversation with agent
- Agents need "inbox for humans" to review at convenience

**2. AFK Mode Long Sessions**
- Agent working autonomously for hours
- Encounters critical decision (architecture, breaking changes)
- Needs structured way to pause and escalate

**3. Multi-Agent Initiatives**
- Complex work spanning multiple agents (Analyst → Architect → Developer)
- Requires executive summary for HiC to track progress
- Current reports scattered across agent-specific log directories

**4. Blocker Management**
- External dependencies (credentials, PR reviews, clarifications)
- Needs visibility separate from in-progress tasks

### Existing Patterns

**✅ Strengths:**
- File-based async collaboration (ADR-008) enables Git-versioned coordination
- Work directory orchestration (ADR-004) provides structured task lifecycle
- Coordinator pattern (ADR-005) enables routing and escalation

**⚠️ Gaps:**
- No clear escalation path to humans
- Executive content mixed with operational logs
- Decisions tracked inconsistently
- Blockers buried in task status

## Decision

**We will create `work/human-in-charge/` directory structure for agent-human escalations:**

```
work/human-in-charge/
├── README.md                  # Usage guide and conventions
├── executive_summaries/       # High-level summaries requiring HiC review
├── decision_requests/         # Explicit decisions needed from HiC
├── blockers/                  # External blockers awaiting human action
└── problems/                  # Internal problems requiring human judgment
```

### Directory Definitions

#### `executive_summaries/`
**Purpose:** Consolidated summaries of complex multi-phase work for HiC review

**When to use:**
- Multi-agent initiatives (spec → review → implementation)
- Architecture changes affecting multiple modules
- Major refactorings with cross-cutting impact
- Periodic progress reports for long-running work

**File format:**
```yaml
---
type: executive_summary
agent: [agent-name]
initiative: [initiative-id or description]
date: YYYY-MM-DD
status: [pending_review, reviewed, approved]
summary: Brief one-paragraph overview
---

# Executive Summary: [Title]

## Overview
[What was done]

## Key Decisions
[Decisions made during work]

## Impact
[What changed, what's affected]

## Next Steps
[What happens next]

## Review Required
[Specific items needing HiC review]
```

**Naming:** `YYYY-MM-DD-[initiative-slug]-summary.md`

---

#### `decision_requests/`
**Purpose:** Explicit decisions that agents cannot make autonomously

**When to use:**
- Architectural choices (REST vs GraphQL, SQL vs NoSQL)
- Breaking API changes
- Technology stack additions/changes
- Security or privacy policy decisions
- Trade-offs with business impact
- Ambiguous requirements with multiple valid interpretations

**File format:**
```yaml
---
type: decision_request
agent: [agent-name]
date: YYYY-MM-DD
urgency: [low, medium, high, blocking]
context: Brief description
status: [pending, decided, cancelled]
---

# Decision Request: [Title]

## Context
[Why this decision is needed]

## Question
[Specific decision to be made]

## Options

### Option A: [Name]
**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Implications:**
- [What changes]

### Option B: [Name]
[Same structure]

## Agent Recommendation
[Agent's recommended choice with rationale, if applicable]

## Related Work
- [Links to specs, ADRs, tasks]

## Decision
<!-- HiC fills this in -->
**Chosen:** [Option X]
**Rationale:** [Why]
**Date:** YYYY-MM-DD
```

**Naming:** `YYYY-MM-DD-[topic-slug]-decision.md`

---

#### `blockers/`
**Purpose:** External blockers preventing agent progress

**When to use:**
- Missing credentials (API keys, passwords)
- Awaiting PR reviews from humans
- External system dependencies (down services, pending access)
- Clarifications needed from product owner
- Resource provisioning (infrastructure, accounts)

**File format:**
```yaml
---
type: blocker
agent: [agent-name]
task_id: [related-task-id or null]
date: YYYY-MM-DD
blocking: [task-ids or initiative names]
urgency: [low, medium, high, critical]
status: [active, resolved, workaround]
---

# Blocker: [Title]

## Description
[What is blocking progress]

## Impact
- **Blocked tasks:** [List of task IDs]
- **Estimated delay:** [Duration]
- **Workaround available:** [Yes/No]

## What's Needed
[Specific action HiC must take]

## Attempted Solutions
- [Attempt 1: result]
- [Attempt 2: result]

## Workaround
[If any workaround in place]

## Resolution
<!-- HiC fills this in when resolved -->
**Action taken:** [Description]
**Date:** YYYY-MM-DD
```

**Naming:** `YYYY-MM-DD-[blocker-slug].md`

---

#### `problems/`
**Purpose:** Internal problems requiring human judgment

**When to use:**
- Contradictory requirements in specifications
- Tests pass but behavior seems wrong
- Implementation diverges significantly from plan
- Discovered constraints not in requirements
- Unexpected results with unclear cause
- Design conflicts between modules

**File format:**
```yaml
---
type: problem
agent: [agent-name]
date: YYYY-MM-DD
severity: [minor, moderate, major, critical]
status: [open, investigating, resolved]
---

# Problem: [Title]

## Description
[What problem was discovered]

## Context
[Where/when it was discovered]

## Evidence
- [Evidence 1]
- [Evidence 2]

## Impact
[What's affected]

## Attempted Solutions
- [Attempt 1: result]
- [Attempt 2: result]

## Proposed Resolution
[Agent's proposal, if any]

## Questions for HiC
1. [Question 1]
2. [Question 2]

## Resolution
<!-- HiC fills this in -->
**Decision:** [Description]
**Action taken:** [Implementation]
**Date:** YYYY-MM-DD
```

**Naming:** `YYYY-MM-DD-[problem-slug].md`

---

### Integration with Existing Systems

**1. AFK Mode (`doctrine/shorthands/afk-mode.md`)**
- Update line 142: Reference `work/human-in-charge/decision_requests/` for critical decisions
- Update line 114-128: Reference `work/human-in-charge/blockers/` for external blockers
- Update line 117-138: Reference `work/human-in-charge/problems/` for unexpected results

**2. File-Based Collaboration (Directive 019)**
- HiC directory extends file-based collaboration to human-agent boundary
- Same principles: markdown, frontmatter, Git-versioned

**3. Manager Mike Coordination**
- When agents escalate, Manager Mike routes to appropriate HiC subdirectory
- Mike consolidates multiple agent escalations into executive summaries
- Mike monitors HiC directory and notifies agents of resolutions

**4. Work Directory Orchestration**
- HiC directory is peer to `collaboration/`, `reports/`, `planning/`
- Follows same patterns: structured files, clear ownership, traceability

**5. Task Lifecycle**
- Tasks can reference HiC files: `blocker_ref: work/human-in-charge/blockers/2026-02-14-api-key.md`
- Tasks frozen due to blockers link to blocker file
- Decision requests can create follow-up tasks when resolved

### Usage Protocol

**For Agents:**
1. Recognize escalation condition (decision, blocker, problem)
2. Create appropriately formatted file in correct subdirectory
3. Update related task files with reference
4. Log escalation in work log
5. Pause work on blocked items (if applicable)
6. Continue with other tasks if possible

**For Human-in-Charge:**
1. Check `work/human-in-charge/` regularly (or via notification)
2. Review new items by subdirectory priority:
   - `blockers/` (highest priority - prevents progress)
   - `decision_requests/` (next - enables forward movement)
   - `problems/` (requires judgment)
   - `executive_summaries/` (periodic review)
3. Fill in resolution sections in files
4. Optionally create follow-up tasks via `work/collaboration/inbox/`
5. Commit resolution with descriptive message

**For Manager Mike:**
- Monitor HiC directory for new items
- Route agent escalations to appropriate subdirectory
- Consolidate related escalations
- Create executive summaries for complex initiatives
- Notify agents when HiC has resolved items

## Consequences

### Positive

✅ **Structured Escalation:** Clear paths for different escalation types  
✅ **Async-Friendly:** HiC reviews at convenience, no real-time coordination needed  
✅ **Traceability:** All escalations in Git history with full context  
✅ **Pattern Consistency:** Extends existing file-based collaboration patterns  
✅ **AFK Enhancement:** Makes AFK mode more practical for long autonomous sessions  
✅ **Reduced Noise:** Executive summaries consolidate complex work, reduce log scanning  
✅ **Decision Context:** Decision requests preserve full context for informed choices  
✅ **Blocker Visibility:** Blockers surfaced prominently, not buried in task status  
✅ **Discovery:** HiC can scan one directory instead of agent-specific logs  

### Negative

⚠️ **Directory Proliferation:** Another top-level directory in `work/`  
- **Mitigation:** Clear documentation on when to use, distinct from reports

⚠️ **Overlap with Reports:** Some conceptual overlap with `work/reports/exec_summaries/`  
- **Mitigation:** Clarify distinction (reports = completed work, HiC = pending review)

⚠️ **Agent Training:** All agents need guidance on when/how to use  
- **Mitigation:** New Directive 040 + updates to all agent profiles

⚠️ **Human Monitoring:** Requires HiC to check directory regularly  
- **Mitigation:** Document expected checking cadence, future automation possible

⚠️ **File Proliferation:** Could accumulate many files over time  
- **Mitigation:** Archive resolved items monthly (like `work/collaboration/archive/`)

### Risks

🔴 **Low Risk:** Additive change, no breaking modifications to existing systems  
🟡 **Medium Risk:** Requires discipline from agents to use correctly  
🟢 **Mitigated:** Directive + examples + agent profile updates provide guidance

## Alternatives Considered

### Alternative 1: Continue Using Agent-Specific Logs
**Description:** Keep current ad-hoc approach of escalations in agent logs

**Pros:**
- No new structure needed
- Familiar to current agents

**Cons:**
- HiC must scan multiple directories
- No standardized format
- Hard to discover pending items
- Doesn't solve AFK mode escalation
- Mixed with routine logs

**Rejected because:** Doesn't address core problem of discovery and structure

---

### Alternative 2: Extend `work/collaboration/` with Human Tasks
**Description:** Treat HiC as another "agent" in task system

**Pros:**
- Reuses existing task infrastructure
- Consistent with orchestration model

**Cons:**
- Overloads task system with different semantics
- HiC isn't an "agent" executing tasks
- Decision requests don't fit task YAML schema
- Executive summaries aren't "tasks"
- Blocker/problem distinction lost

**Rejected because:** Semantic mismatch, forces human workflows into agent patterns

---

### Alternative 3: Use `work/reports/` with Subdirectories
**Description:** Add `work/reports/human-review/` instead of separate top-level directory

**Pros:**
- Fewer top-level directories
- "Reports" semantically fits some use cases

**Cons:**
- "Reports" implies completed work, not pending review
- Conceptually wrong for decision requests and blockers
- Mixes outputs (reports) with inputs (decisions needed)
- Doesn't emphasize "awaiting human" aspect

**Rejected because:** Semantic confusion between outputs and pending items

---

### Alternative 4: Use Issues/PRs Instead of Files
**Description:** Use GitHub issues for escalations, PRs for decisions

**Pros:**
- Native GitHub notification system
- Comment threads for discussion
- Status tracking via labels

**Cons:**
- Breaks file-based collaboration principle
- External dependency (GitHub-specific)
- Not portable to other platforms
- Context split between files and issues
- Harder to archive/search

**Rejected because:** Violates file-based async coordination principle (ADR-008)

## Implementation Plan

**Phase 1: Core Structure** (This ADR)
- ✅ Create `work/human-in-charge/` directory
- ✅ Add subdirectories with README.md
- ✅ Add .gitkeep files
- ✅ Create template examples

**Phase 2: Doctrine Integration**
- Create Directive 040 (Human-in-Charge Escalation Protocol)
- Update AFK mode shorthand to reference HiC directory
- Update Directive 019 to mention HiC escalation

**Phase 3: Agent Integration**
- Update Manager Mike profile with HiC monitoring duties
- Update all agent profiles to reference Directive 040
- Add HiC escalation to relevant tactics

**Phase 4: Documentation**
- Update `work/README.md` with HiC directory description
- Add usage examples to HiC README
- Update orchestration documentation

**Phase 5: Future Enhancements** (out of scope)
- Automation script to notify HiC of new items
- Dashboard integration for monitoring
- Metrics on escalation frequency by type

## References

- **ADR-004:** Work Directory Structure - Defined `work/` as orchestration space
- **ADR-008:** File-Based Async Coordination - Established file-based collaboration principle
- **ADR-005:** Coordinator Agent Pattern - Manager Mike role
- **Directive 019:** File-Based Collaboration Framework
- **AFK Mode Shorthand:** `doctrine/shorthands/afk-mode.md`
- **Work Directory Orchestration Approach:** `doctrine/approaches/work-directory-orchestration.md`

## Related Work

- **Directive 040** (to be created): Human-in-Charge Escalation Protocol
- **Manager Mike Profile Update:** Add HiC monitoring responsibilities
- **Agent Profile Updates:** All agents reference Directive 040

---

**Author:** Curator Claire  
**Date:** 2026-02-14  
**Status:** Accepted ✅
