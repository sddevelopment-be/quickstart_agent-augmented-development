# Human-in-Charge Directory

**Purpose:** Structured escalation path for agents to request human decisions, report blockers, and surface problems requiring judgment.

**Version:** 1.0.0  
**Created:** 2026-02-14  
**Related:** [ADR-047](../../docs/architecture/adrs/ADR-047-human-in-charge-directory-structure.md), [Directive 040](../../doctrine/directives/040_human_in_charge_escalation_protocol.md)

---

## Overview

This directory enables **asynchronous agent-human coordination** for:
- Async environments (GitHub Copilot Web, Claude Projects)
- AFK mode (agent working autonomously while human away)
- Multi-agent initiatives (periodic checkpoint reviews)
- Blocker management (external dependencies preventing progress)

**Key Principle:** Agents escalate via structured files instead of waiting for real-time human response.

---

## Directory Structure

```
work/human-in-charge/
├── README.md                    # This file
├── executive_summaries/         # High-level summaries requiring HiC review
│   ├── .gitkeep
│   └── TEMPLATE.md             # Template for executive summaries
├── decision_requests/           # Explicit decisions needed from HiC
│   ├── .gitkeep
│   └── TEMPLATE.md             # Template for decision requests
├── blockers/                    # External blockers awaiting human action
│   ├── .gitkeep
│   └── TEMPLATE.md             # Template for blocker reports
└── problems/                    # Internal problems requiring human judgment
    ├── .gitkeep
    └── TEMPLATE.md             # Template for problem reports
```

---

## Quick Reference: When to Use Each Subdirectory

| Subdirectory | Use When | Priority | Who Creates | Example |
|--------------|----------|----------|-------------|---------|
| **executive_summaries/** | Complex multi-phase work completes | Low (weekly review) | Manager Mike, Any agent | "Spec → Review → Impl cycle done" |
| **decision_requests/** | Architectural/policy decisions needed | Medium (2-3 days) | Any agent | "REST vs GraphQL?" |
| **blockers/** | External action prevents progress | **High (daily check)** | Any agent | "Need AWS credentials" |
| **problems/** | Internal issues need judgment | Medium (weekly) | Any agent | "Contradictory specs found" |

---

## Subdirectory Details

### `executive_summaries/` - Checkpoint Reviews

**Purpose:** Consolidate complex multi-agent work for human review at milestones.

**When to use:**
- ✅ Multi-agent initiative completes major phase
- ✅ Architecture changes affect multiple modules
- ✅ Major refactoring with cross-cutting impact
- ✅ Periodic progress reports (weekly/bi-weekly)

**Who creates:**
- **Primary:** Manager Mike (consolidates multi-agent outputs)
- **Secondary:** Any agent after completing complex initiative

**Format:** See `executive_summaries/TEMPLATE.md`

**Example filename:** `2026-02-14-authentication-system-migration-summary.md`

---

### `decision_requests/` - Critical Choices

**Purpose:** Request explicit decisions that agents cannot make autonomously.

**When to use:**
- ✅ Architectural choices (REST vs GraphQL, SQL vs NoSQL)
- ✅ Breaking API changes
- ✅ Technology stack additions/changes
- ✅ Security or privacy policy decisions
- ✅ Trade-offs with business impact
- ✅ Ambiguous requirements with multiple interpretations

**Who creates:** Any agent encountering decision beyond authority

**Format:** See `decision_requests/TEMPLATE.md`

**Example filename:** `2026-02-14-database-choice-sessions.md`

**Related:** AFK Mode shorthand (Critical Decisions scope)

---

### `blockers/` - External Dependencies

**Purpose:** Report external blockers preventing agent progress.

**When to use:**
- ✅ Missing credentials (API keys, passwords)
- ✅ Awaiting PR reviews from humans
- ✅ External system dependencies (down services, access requests)
- ✅ Clarifications needed from product owner
- ✅ Resource provisioning (infrastructure, accounts)

**Who creates:** Any agent when external action prevents progress

**Action after creating:**
1. Create blocker file
2. Update related task to `status: frozen`
3. **Continue with other tasks** (don't wait idle)

**Format:** See `blockers/TEMPLATE.md`

**Example filename:** `2026-02-14-aws-s3-credentials.md`

**Priority:** ⚠️ **Highest - Check daily**

---

### `problems/` - Internal Issues

**Purpose:** Report internal problems requiring human judgment.

**When to use:**
- ✅ Contradictory requirements in specifications
- ✅ Tests pass but behavior seems wrong
- ✅ Implementation diverges significantly from plan
- ✅ Discovered constraints not in requirements
- ✅ Unexpected results with unclear cause
- ✅ Design conflicts between modules

**Who creates:** Any agent discovering problems requiring judgment

**Format:** See `problems/TEMPLATE.md`

**Example filename:** `2026-02-14-spec-contradiction-auth.md`

---

## Agent Workflow

### Creating Escalation File

1. **Recognize escalation condition** (see Quick Reference above)
2. **Choose correct subdirectory** based on escalation type
3. **Copy template** from subdirectory (`TEMPLATE.md`)
4. **Fill all sections** with complete information
5. **Save with proper filename** (`YYYY-MM-DD-[slug].md`)
6. **Update related task** (if blocking) with reference
7. **Log escalation** in your work log
8. **Continue with other work** if possible

### Example (Creating Blocker)

```bash
# 1. Copy template
cp work/human-in-charge/blockers/TEMPLATE.md work/human-in-charge/blockers/2026-02-14-aws-credentials.md

# 2. Edit file with details (use your editor)

# 3. Update task status
yq -i '.status = "frozen"' work/collaboration/assigned/python-pedro/2026-02-14T1500-s3-integration.yaml
yq -i '.blocker_ref = "work/human-in-charge/blockers/2026-02-14-aws-credentials.md"' work/collaboration/assigned/python-pedro/2026-02-14T1500-s3-integration.yaml

# 4. Log in work log
echo "## 15:30 - Created blocker for AWS credentials" >> work/reports/logs/python-pedro/2026-02-14.log

# 5. Continue with other work
echo "Continuing with database migration work..."
```

---

## Human-in-Charge Workflow

### Checking Cadence

**Recommended:**
- **Blockers:** Daily (prevents agent progress)
- **Decision Requests:** Every 2-3 days
- **Problems:** Weekly
- **Executive Summaries:** Weekly or at milestones

### Resolution Process

1. **Scan subdirectories** in priority order (blockers → decisions → problems → summaries)
2. **Review new items** (check frontmatter `status: pending`, `status: active`, etc.)
3. **Fill resolution section** at bottom of file
4. **Update frontmatter status** (e.g., `status: resolved`)
5. **Create follow-up tasks** if needed (via `work/collaboration/inbox/`)
6. **Commit with descriptive message**

### Resolution Example

```bash
# Edit decision request file
vim work/human-in-charge/decision_requests/2026-02-14-database-choice.md

# Add resolution section (at bottom):
## Decision
**Chosen:** Option A (Redis)  
**Rationale:** Session performance is critical. Use Redis with persistence.  
**Additional guidance:** Use Redis Sentinel for HA.  
**Date:** 2026-02-15

# Update frontmatter
yq -i '.status = "decided"' work/human-in-charge/decision_requests/2026-02-14-database-choice.md

# Commit
git add work/human-in-charge/decision_requests/2026-02-14-database-choice.md
git commit -m "Resolved decision: Use Redis for sessions with Sentinel"
```

---

## Manager Mike Responsibilities

**Additional coordination duties:**

1. **Monitor `work/human-in-charge/`** for new escalations
2. **Consolidate related escalations** into executive summaries
3. **Route agent escalations** to appropriate subdirectory
4. **Create executive summaries** for multi-agent initiatives
5. **Notify agents** when HiC resolves items
6. **Archive resolved items** monthly (move to `archive/YYYY-MM/`)

---

## Integration with Existing Systems

### AFK Mode

When operating in AFK mode (`doctrine/shorthands/afk-mode.md`):
- Critical decisions → `decision_requests/`
- External blockers → `blockers/`
- Unexpected results → `problems/`

**Pause protocol:**
1. Stop current work
2. Commit completed work
3. Create appropriate HiC file
4. Update task status to `frozen`
5. Continue with other tasks

---

### Task Lifecycle

**Tasks reference HiC files:**

```yaml
# In work/collaboration/assigned/agent/task.yaml
id: 2026-02-14T1500-s3-integration
status: frozen
blocker_ref: work/human-in-charge/blockers/2026-02-14-aws-credentials.md
notes:
  - Awaiting AWS credentials from HiC
```

**When HiC resolves:**
- HiC updates HiC file with resolution
- HiC updates task status to `assigned`
- Agent resumes work

---

### Work Logs

**Reference HiC files in logs:**

```markdown
## 2026-02-14 15:30 - Session Log

### Blocked
- Encountered missing AWS credentials for S3 integration
- Created blocker: `work/human-in-charge/blockers/2026-02-14-aws-credentials.md`
- Frozen task: `2026-02-14T1500-s3-integration`

### Next Steps
- Awaiting HiC credentials
- Continuing with database migration work
```

---

## Best Practices

### ✅ Do

- **Provide full context** - HiC should understand without additional research
- **Include evidence** - logs, error messages, screenshots
- **Document attempted solutions** - show what was tried
- **Link related work** - specs, ADRs, tasks, discussions
- **Use templates** - ensures consistency and completeness
- **Continue other work** - don't wait idle on blockers
- **Update task status** - mark tasks as `frozen` when blocked
- **Log escalations** - document in your work log

### ❌ Don't

- **Wrong subdirectory** - blocker filed as decision request
- **Insufficient context** - missing background or alternatives
- **Wait instead of continue** - sitting idle after creating blocker
- **Escalate trivial decisions** - follow conventions autonomously
- **Skip work logs** - always log escalations
- **Unclear requests** - "something is wrong" vs "API returns 401"
- **Missing frontmatter** - use templates for complete metadata

---

## File Naming Conventions

**Format:** `YYYY-MM-DD-[descriptive-slug].md`

**Good examples:**
- ✅ `2026-02-14-aws-s3-credentials.md`
- ✅ `2026-02-14-database-choice-sessions.md`
- ✅ `2026-02-14-spec-contradiction-auth.md`
- ✅ `2026-02-14-authentication-migration-summary.md`

**Bad examples:**
- ❌ `blocker.md` (not descriptive, no date)
- ❌ `2026-02-14.md` (no description)
- ❌ `decision-request-1.md` (sequential numbering, no date)
- ❌ `AWS_CREDENTIALS.md` (uppercase, no date)

---

## Maintenance

### Archiving

**Monthly:** Move resolved items to `archive/YYYY-MM/`

```bash
# Create archive directory
mkdir -p work/human-in-charge/archive/2026-02

# Move resolved items (older than 30 days)
find work/human-in-charge/{blockers,decision_requests,problems} -name "*.md" -mtime +30 -type f | while read file; do
  if grep -q "status: resolved\|status: decided\|status: resolved" "$file"; then
    mv "$file" work/human-in-charge/archive/2026-02/
  fi
done

# Commit
git add work/human-in-charge/archive/
git commit -m "Archive resolved HiC items from January 2026"
```

**Note:** Executive summaries typically not archived (serve as long-term reference).

---

## Related Documentation

- **ADR-047:** Human-in-Charge Directory Structure - Architecture decision
- **Directive 040:** Human-in-Charge Escalation Protocol - Complete usage guide
- **ADR-004:** Work Directory Structure - Overall work directory design
- **ADR-008:** File-Based Async Coordination - Async collaboration principle
- **AFK Mode:** `doctrine/shorthands/afk-mode.md` - Autonomous operation protocol
- **Work Directory Orchestration:** `doctrine/approaches/work-directory-orchestration.md`

---

## Templates

Each subdirectory contains a `TEMPLATE.md` file:
- `executive_summaries/TEMPLATE.md`
- `decision_requests/TEMPLATE.md`
- `blockers/TEMPLATE.md`
- `problems/TEMPLATE.md`

**To use:** Copy template, rename to `YYYY-MM-DD-[slug].md`, fill all sections.

---

## Status

**Version:** 1.0.0  
**Created:** 2026-02-14  
**Author:** Curator Claire  
**Maintained by:** Manager Mike, Planning Petra  
**Status:** ✅ Active
