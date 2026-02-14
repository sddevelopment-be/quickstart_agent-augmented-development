<!-- The following information is to be interpreted literally -->

# 040 Human-in-Charge Escalation Protocol

**Purpose:** Define when and how agents escalate to humans via the `work/human-in-charge/` directory structure.

**Core Concepts:** See [Escalation](../GLOSSARY.md#escalation), [Human-in-Charge](../GLOSSARY.md#human-in-charge), [Blocker](../GLOSSARY.md#blocker), and [Decision Request](../GLOSSARY.md#decision-request) in the glossary.

**Related ADR:** [ADR-047: Human-in-Charge Directory Structure](../../docs/architecture/adrs/ADR-047-human-in-charge-directory-structure.md)

## Core Principle

When agents encounter situations requiring human judgment, decisions, or external actions, they **escalate via structured files** in `work/human-in-charge/` rather than waiting for real-time human response.

This enables **asynchronous human-agent coordination** in environments like:
- GitHub Copilot Web (no persistent sessions)
- Claude Projects (async file-based interaction)
- AFK mode (human away, agent working autonomously)
- Multi-agent initiatives (periodic human checkpoint reviews)

## Directory Structure

```
work/human-in-charge/
├── README.md                  # Usage guide and conventions
├── executive_summaries/       # High-level summaries requiring HiC review
├── decision_requests/         # Explicit decisions needed from HiC
├── blockers/                  # External blockers awaiting human action
└── problems/                  # Internal problems requiring human judgment
```

## When to Escalate

### 1. Executive Summaries (`executive_summaries/`)

**Create when:**
- ✅ Multi-agent initiative completes a major phase
- ✅ Architecture change affects multiple modules
- ✅ Major refactoring with cross-cutting impact
- ✅ Periodic progress report on long-running work (weekly/bi-weekly)
- ✅ Manager Mike consolidates outputs from multiple agents

**Do NOT create for:**
- ❌ Routine single-agent tasks (use work logs instead)
- ❌ Minor bug fixes or documentation updates
- ❌ Work still in progress (wait for completion or milestone)

**Who creates:**
- **Primary:** Manager Mike (consolidates multi-agent work)
- **Secondary:** Any agent after completing complex initiative

**Example triggers:**
- "Spec → Review → Implementation cycle completed"
- "Architecture migration 60% complete, checkpoint review"
- "5 agents collaborated on feature X, summary needed"

---

### 2. Decision Requests (`decision_requests/`)

**Create when:**
- ✅ Architectural choices (REST vs GraphQL, SQL vs NoSQL)
- ✅ Breaking API changes
- ✅ Technology stack additions/changes
- ✅ Security or privacy policy decisions
- ✅ Trade-offs with business impact
- ✅ Ambiguous requirements with multiple valid interpretations
- ✅ Design conflicts between modules/specifications

**Do NOT create for:**
- ❌ Minor implementation details (file naming, variable naming)
- ❌ Code style preferences (follow existing conventions)
- ❌ Routine refactoring decisions (extract method, etc.)
- ❌ Test data selection (use reasonable defaults)

**Who creates:**
- **Any agent** when encountering decision beyond authority
- **Especially:** Architect Alphonso, Analyst Annie, Framework Guardian

**Example triggers:**
- "Should we use REST or GraphQL for new API?" (Architect)
- "Spec requires real-time updates, WebSockets or polling?" (Analyst)
- "Breaking change needed, approve before proceeding?" (Any agent)

**Reference:** AFK Mode shorthand (lines 95-111) - Critical Decisions scope

---

### 3. Blockers (`blockers/`)

**Create when:**
- ✅ Missing credentials (API keys, passwords, tokens)
- ✅ Awaiting PR reviews from humans
- ✅ External system dependencies (down services, pending access)
- ✅ Clarifications needed from product owner
- ✅ Resource provisioning (infrastructure, accounts, permissions)
- ✅ Legal/compliance review required

**Do NOT create for:**
- ❌ Internal code issues (use `problems/` instead)
- ❌ Failing tests (debug or report as problem)
- ❌ Missing documentation (write it or request via decision)
- ❌ Dependency version conflicts (resolve or escalate as problem)

**Who creates:**
- **Any agent** when external action prevents progress

**Action after creating:**
1. Create blocker file
2. Update related task to `status: frozen` with reference
3. Log blocker in work log
4. **Continue with other tasks** (don't wait idle)

**Example triggers:**
- "Need AWS credentials to test S3 integration"
- "PR #123 needs human review before merging"
- "Staging environment down, cannot deploy"

**Reference:** AFK Mode shorthand (lines 117-128) - Blocker handling

---

### 4. Problems (`problems/`)

**Create when:**
- ✅ Contradictory requirements in specifications
- ✅ Tests pass but behavior seems wrong
- ✅ Implementation diverges significantly from plan
- ✅ Discovered constraints not in requirements
- ✅ Unexpected results with unclear cause
- ✅ Design conflicts between modules
- ✅ Data inconsistencies or corruption detected

**Do NOT create for:**
- ❌ Simple bugs (fix and commit)
- ❌ Obvious typos or formatting issues (fix immediately)
- ❌ Expected test failures (fix the code)
- ❌ Missing files (create them)

**Who creates:**
- **Any agent** when discovering problems requiring human judgment

**Example triggers:**
- "Spec A requires X, Spec B requires opposite of X"
- "All tests pass but API returns wrong data structure"
- "Implementation requires breaking 10 other tests unexpectedly"

**Reference:** AFK Mode shorthand (lines 129-138) - Unexpected Results

---

## File Format Standards

### Executive Summary Template

**Filename:** `YYYY-MM-DD-[initiative-slug]-summary.md`

```yaml
---
type: executive_summary
agent: [agent-name]
initiative: [initiative-id or description]
date: YYYY-MM-DD
status: pending_review
summary: Brief one-paragraph overview
---

# Executive Summary: [Title]

## Overview
[What was done - 3-5 sentences]

## Key Decisions
- Decision 1: [Description] → [Outcome]
- Decision 2: [Description] → [Outcome]

## Impact
- **Modules affected:** [List]
- **Breaking changes:** [Yes/No - if yes, describe]
- **Tests updated:** [Count]
- **Documentation updated:** [List]

## Next Steps
1. [Next step 1]
2. [Next step 2]

## Review Required
- [ ] Approve architecture changes
- [ ] Approve breaking changes
- [ ] Approve next phase plan

## Related Artifacts
- Specifications: [Links]
- ADRs: [Links]
- Tasks: [Links]
```

---

### Decision Request Template

**Filename:** `YYYY-MM-DD-[topic-slug]-decision.md`

```yaml
---
type: decision_request
agent: [agent-name]
date: YYYY-MM-DD
urgency: [low, medium, high, blocking]
context: Brief description
status: pending
---

# Decision Request: [Title]

## Context
[Why this decision is needed - provide full background]

## Question
[Specific decision to be made - be precise]

## Options

### Option A: [Name]
**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Implications:**
- [What changes if we choose this]
- [Effort estimate]
- [Risk assessment]

### Option B: [Name]
[Same structure]

### Option C: [Name] (if applicable)
[Same structure]

## Agent Recommendation
**Recommended:** Option [X]

**Rationale:** [Why agent recommends this option, or "No strong preference" if balanced]

## Related Work
- Specifications: [Links]
- ADRs: [Links]
- Tasks: [Links]
- Prior discussions: [Links]

## Decision
<!-- HiC fills this in -->
**Chosen:** [Option X]  
**Rationale:** [Why]  
**Additional guidance:** [Any clarifications or modifications]  
**Date:** YYYY-MM-DD
```

---

### Blocker Template

**Filename:** `YYYY-MM-DD-[blocker-slug].md`

```yaml
---
type: blocker
agent: [agent-name]
task_id: [related-task-id or null]
date: YYYY-MM-DD
blocking: [task-ids or initiative names]
urgency: [low, medium, high, critical]
status: active
---

# Blocker: [Title]

## Description
[What is blocking progress - be specific]

## Impact
- **Blocked tasks:** [List task IDs or descriptions]
- **Estimated delay:** [Duration if continues]
- **Workaround available:** [Yes/No]

## What's Needed
[Specific action HiC must take - be explicit]

**Example:**
- "Provide AWS S3 access key and secret for staging bucket"
- "Review and merge PR #123"
- "Confirm if we can use GPL-licensed dependency"

## Attempted Solutions
- [Attempt 1: result]
- [Attempt 2: result]
- [Attempt 3: result]

## Workaround
[If any workaround in place, describe it and limitations]

## Resolution
<!-- HiC fills this in when resolved -->
**Action taken:** [Description]  
**Follow-up tasks:** [Task IDs created, if any]  
**Date:** YYYY-MM-DD
```

---

### Problem Template

**Filename:** `YYYY-MM-DD-[problem-slug].md`

```yaml
---
type: problem
agent: [agent-name]
date: YYYY-MM-DD
severity: [minor, moderate, major, critical]
status: open
---

# Problem: [Title]

## Description
[What problem was discovered - be detailed]

## Context
[Where/when it was discovered]
- File: [Filename or location]
- During: [What activity revealed it]
- Related: [Spec, ADR, task references]

## Evidence
- [Evidence 1: describe and provide data/logs]
- [Evidence 2: screenshots, error messages, etc.]
- [Evidence 3: reproduction steps if applicable]

## Impact
- **Severity:** [minor/moderate/major/critical]
- **Modules affected:** [List]
- **Workaround exists:** [Yes/No]

## Attempted Solutions
- [Attempt 1: what was tried, result]
- [Attempt 2: what was tried, result]

## Proposed Resolution
[Agent's proposal, if any - may be multiple options]

## Questions for HiC
1. [Question 1]
2. [Question 2]
3. [Question 3]

## Resolution
<!-- HiC fills this in -->
**Decision:** [Description of resolution]  
**Action taken:** [Implementation or task created]  
**Follow-up:** [Any follow-up needed]  
**Date:** YYYY-MM-DD
```

---

## Agent Responsibilities

### For All Agents

1. **Recognize escalation conditions** (see "When to Escalate" above)
2. **Create appropriately formatted file** in correct subdirectory
3. **Use templates** (see File Format Standards above)
4. **Update related task files** with reference to HiC file
5. **Log escalation** in your work log (`work/reports/logs/[agent]/`)
6. **Continue with other work** if possible (don't wait idle)

### For Manager Mike (Coordination Agent)

**Additional responsibilities:**

1. **Monitor `work/human-in-charge/`** for new escalations
2. **Consolidate related escalations** into executive summaries
3. **Route agent escalations** to appropriate subdirectory
4. **Create executive summaries** for multi-agent initiatives
5. **Notify agents** when HiC resolves items (via task updates or handoffs)
6. **Archive resolved items** monthly (move to `work/human-in-charge/archive/YYYY-MM/`)

---

## Human-in-Charge Responsibilities

### Checking Cadence

**Recommended:**
- **Blockers:** Check daily (high priority - prevents progress)
- **Decision Requests:** Check every 2-3 days
- **Problems:** Check weekly
- **Executive Summaries:** Check weekly or at initiative milestones

### Resolution Process

1. **Review new items** in priority order (blockers → decisions → problems → summaries)
2. **Fill in resolution section** in each file
3. **Create follow-up tasks** if needed (via `work/collaboration/inbox/`)
4. **Update file status** in frontmatter (e.g., `status: resolved`)
5. **Commit with descriptive message** (e.g., "Resolved blocker: AWS credentials provided")
6. **Optional:** Add comment in related task files or GitHub issues

### Resolution Format

All templates include a "Resolution" section at the bottom (commented out). HiC should:
- Fill in the relevant fields
- Update frontmatter status
- Commit the file

**Example (Decision Request):**
```markdown
## Decision
<!-- HiC fills this in -->
**Chosen:** Option B (GraphQL)  
**Rationale:** Better fit for mobile app needs, real-time requirements  
**Additional guidance:** Use Apollo Client, not Relay  
**Date:** 2026-02-15
```

---

## Integration with Existing Systems

### AFK Mode

When operating in AFK mode (`doctrine/shorthands/afk-mode.md`):
- **Critical decisions** → `decision_requests/` (line 95-111 reference)
- **Blockers** → `blockers/` (line 117-128 reference)
- **Unexpected results** → `problems/` (line 129-138 reference)

**AFK mode pause protocol:**
1. Stop current work
2. Commit completed work (if any)
3. Create appropriate HiC file (decision/blocker/problem)
4. Update task status to `frozen` with reference
5. Log pause in work log
6. Continue with other tasks if available

---

### Task Lifecycle

**Tasks can reference HiC files:**

```yaml
# In task YAML file
id: 2026-02-14T1200-implement-graphql-api
status: frozen
blocker_ref: work/human-in-charge/blockers/2026-02-14-api-architecture-decision.md
notes:
  - Awaiting HiC decision on GraphQL vs REST
```

**When HiC resolves:**
1. HiC updates blocker/decision file
2. HiC updates task status to `assigned` (or creates new task)
3. Agent picks up resumed task

---

### Work Logs

**Reference HiC files in work logs:**

```markdown
## 2026-02-14 14:30 - Session Log

### Completed
- Analyzed API requirements for mobile app integration

### Blocked
- Encountered architectural decision: GraphQL vs REST
- Created decision request: `work/human-in-charge/decision_requests/2026-02-14-api-architecture-decision.md`
- Paused work on task `2026-02-14T1200-implement-graphql-api`

### Next Steps
- Awaiting HiC decision
- Will continue with frontend mockup work (task `2026-02-14T1400-frontend-mockup`)
```

---

### Multi-Agent Initiatives

**Manager Mike coordinates:**

1. **Initiative starts** → Manager Mike creates coordination plan
2. **Agents execute phases** → Each agent logs work
3. **Phase completes** → Manager Mike creates executive summary in `executive_summaries/`
4. **HiC reviews** → Approves or requests changes
5. **Next phase starts** → Manager Mike routes next tasks

**Example flow:**
```
Phase 1: Specification (Analyst Annie)
  → Work log created
  
Phase 2: Architecture (Architect Alphonso)
  → Work log created
  → Decision request: Database choice
  
Phase 3: HiC Checkpoint
  → Manager Mike creates executive summary
  → Consolidates both work logs + decision request
  → HiC reviews and approves
  
Phase 4: Implementation (Python Pedro)
  → Continues based on HiC approval
```

---

## Examples

### Example 1: AFK Mode Critical Decision

**Scenario:** Agent working autonomously, encounters architectural choice

**Agent action:**
```bash
# Agent creates decision request
cat > work/human-in-charge/decision_requests/2026-02-14-database-choice.md <<'EOF'
---
type: decision_request
agent: architect-alphonso
date: 2026-02-14
urgency: high
context: Choosing database for user session management
status: pending
---

# Decision Request: Database for User Sessions

## Context
Implementing user session management for web app. Current spec doesn't specify database.

## Question
Which database should we use for session storage?

## Options

### Option A: Redis
**Pros:**
- Fast in-memory storage
- Built-in TTL for session expiration
- Wide adoption for sessions

**Cons:**
- Additional infrastructure dependency
- Data loss if Redis crashes (unless persistence enabled)

**Implications:**
- Need Redis server deployment
- Effort: 2-3 hours setup + testing

### Option B: PostgreSQL
**Pros:**
- Already using PostgreSQL for main data
- No new infrastructure
- Persistent by default

**Cons:**
- Slower than Redis
- Need cleanup job for expired sessions

**Implications:**
- Add sessions table to existing DB
- Effort: 1-2 hours + migration

## Agent Recommendation
**Recommended:** Option A (Redis)

**Rationale:** Session storage benefits from fast in-memory access. PostgreSQL query overhead would slow down every request.

## Related Work
- Spec: specifications/features/user-authentication.md
- ADR-012: PostgreSQL as primary database

## Decision
<!-- HiC fills this in -->
EOF

# Update task
yq -i '.status = "frozen"' work/collaboration/assigned/architect/2026-02-14T1200-session-management.yaml
yq -i '.blocker_ref = "work/human-in-charge/decision_requests/2026-02-14-database-choice.md"' work/collaboration/assigned/architect/2026-02-14T1200-session-management.yaml

# Log pause
echo "## 14:30 - Paused for decision request" >> work/reports/logs/architect-alphonso/2026-02-14-session.log
echo "Created decision request: work/human-in-charge/decision_requests/2026-02-14-database-choice.md" >> work/reports/logs/architect-alphonso/2026-02-14-session.log

# Continue with other work
echo "Continuing with frontend mockup work while awaiting decision..."
```

**HiC action (later):**
```bash
# Edit decision file
cat >> work/human-in-charge/decision_requests/2026-02-14-database-choice.md <<'EOF'

## Decision
**Chosen:** Option A (Redis)  
**Rationale:** Agreed - session performance is critical. Use Redis with persistence enabled.  
**Additional guidance:** Use Redis Sentinel for high availability.  
**Date:** 2026-02-15
EOF

# Update status in frontmatter
yq -i '.status = "decided"' work/human-in-charge/decision_requests/2026-02-14-database-choice.md

# Unblock task
yq -i '.status = "assigned"' work/collaboration/assigned/architect/2026-02-14T1200-session-management.yaml
yq -i 'del(.blocker_ref)' work/collaboration/assigned/architect/2026-02-14T1200-session-management.yaml

# Commit
git add work/human-in-charge/decision_requests/2026-02-14-database-choice.md work/collaboration/assigned/architect/2026-02-14T1200-session-management.yaml
git commit -m "Resolved decision request: Use Redis for sessions with Sentinel"
```

---

### Example 2: Blocker - Missing Credentials

**Scenario:** Agent needs API key to test integration

**Agent action:**
```bash
# Create blocker
cat > work/human-in-charge/blockers/2026-02-14-aws-s3-credentials.md <<'EOF'
---
type: blocker
agent: python-pedro
task_id: 2026-02-14T1500-s3-integration
date: 2026-02-14
blocking: [2026-02-14T1500-s3-integration]
urgency: high
status: active
---

# Blocker: AWS S3 Credentials for Staging

## Description
Cannot test S3 file upload integration without AWS credentials for staging bucket.

## Impact
- **Blocked tasks:** 2026-02-14T1500-s3-integration
- **Estimated delay:** 1-2 days if not resolved
- **Workaround available:** No (mocking not sufficient for integration test)

## What's Needed
Provide AWS credentials for staging S3 bucket `myapp-staging-uploads`:
- Access Key ID
- Secret Access Key
- Bucket region

**Alternatively:** Create IAM user `agent-integration-test` with S3 permissions and provide credentials.

## Attempted Solutions
- Checked documentation: No credentials documented
- Checked `.env.example`: Only production credentials listed (not usable)
- Asked in Slack: No response yet

## Workaround
None - integration test requires real S3 connection.

## Resolution
<!-- HiC fills this in when resolved -->
EOF

# Freeze task
python tools/scripts/freeze_task.py 2026-02-14T1500-s3-integration --reason "Missing AWS S3 credentials"

# Log blocker
echo "## 15:30 - Blocked on AWS credentials" >> work/reports/logs/python-pedro/2026-02-14-s3-integration.log

# Continue with other work
echo "Continuing with database migration work while awaiting credentials..."
```

**HiC action (next day):**
```bash
# Provide credentials via secure method (not in file!)
# Then update blocker file

cat >> work/human-in-charge/blockers/2026-02-14-aws-s3-credentials.md <<'EOF'

## Resolution
**Action taken:** Created IAM user `agent-integration-test` with S3 permissions. Credentials provided via 1Password shared vault.  
**Follow-up tasks:** None  
**Date:** 2026-02-15
EOF

# Update status
yq -i '.status = "resolved"' work/human-in-charge/blockers/2026-02-14-aws-s3-credentials.md

# Unfreeze task (or agent will do this when they see resolution)
# Agent will continue work when they check HiC directory

git add work/human-in-charge/blockers/2026-02-14-aws-s3-credentials.md
git commit -m "Resolved blocker: AWS S3 credentials provided via 1Password"
```

---

### Example 3: Problem - Contradictory Specs

**Scenario:** Agent discovers conflicting requirements

**Agent action:**
```bash
cat > work/human-in-charge/problems/2026-02-14-spec-contradiction-auth.md <<'EOF'
---
type: problem
agent: analyst-annie
date: 2026-02-14
severity: major
status: open
---

# Problem: Contradictory Authentication Requirements

## Description
Specifications contain contradictory requirements for user authentication flow.

## Context
- File: specifications/features/user-authentication.md
- During: Spec review phase
- Related: SPEC-AUTH-001

## Evidence
- **Spec line 45:** "Users must authenticate via OAuth2 with Google/GitHub"
- **Spec line 89:** "Users must have username/password authentication for offline access"
- **Spec line 112:** "No password storage allowed per security policy"

**Contradiction:**
- Line 45 + 89 require both OAuth AND password auth
- Line 112 forbids password storage
- Cannot implement password auth without password storage

## Impact
- **Severity:** major (blocks implementation)
- **Modules affected:** Authentication, User Management
- **Workaround exists:** No

## Attempted Solutions
- Reviewed security policy: Confirms no password storage
- Checked ADRs: No prior auth decisions documented
- Considered passwordless options: Not specified in requirements

## Proposed Resolution
**Option A:** OAuth-only authentication
- Pros: Meets security policy, modern approach
- Cons: Requires internet, no offline access

**Option B:** OAuth + Passkeys (WebAuthn)
- Pros: Meets security policy, supports offline
- Cons: Newer tech, limited browser support

**Option C:** Clarify "offline access" requirement
- Maybe offline access not actually needed?

## Questions for HiC
1. Is offline access actually required? (Line 89)
2. If yes, is Passkeys/WebAuthn acceptable alternative to passwords?
3. Should we update spec to remove contradictory line 89?

## Resolution
<!-- HiC fills this in -->
EOF

# Log problem
echo "## 16:00 - Discovered spec contradiction" >> work/reports/logs/analyst-annie/2026-02-14-auth-spec.log
echo "Created problem report: work/human-in-charge/problems/2026-02-14-spec-contradiction-auth.md" >> work/reports/logs/analyst-annie/2026-02-14-auth-spec.log
```

**HiC action:**
```bash
cat >> work/human-in-charge/problems/2026-02-14-spec-contradiction-auth.md <<'EOF'

## Resolution
**Decision:** "Offline access" requirement was mistake - copy-paste error from old spec.  
**Action taken:** 
- Remove line 89 from spec (offline access requirement)
- Add clarification: OAuth-only authentication required
- Updated SPEC-AUTH-001 frontmatter to revision 2

**Follow-up:** Analyst Annie to update spec and increment version  
**Date:** 2026-02-15
EOF

yq -i '.status = "resolved"' work/human-in-charge/problems/2026-02-14-spec-contradiction-auth.md

# Create follow-up task
cat > work/collaboration/inbox/2026-02-15T0900-analyst-update-auth-spec.yaml <<'EOF'
id: 2026-02-15T0900-analyst-update-auth-spec
agent: analyst
status: new
title: "Update authentication spec based on HiC resolution"
artefacts:
  - specifications/features/user-authentication.md
context:
  resolution: work/human-in-charge/problems/2026-02-14-spec-contradiction-auth.md
  changes:
    - Remove line 89 (offline access requirement)
    - Add OAuth-only clarification
    - Increment spec version to revision 2
created_at: "2026-02-15T09:00:00Z"
created_by: "human-stijn"
EOF

git add work/human-in-charge/problems/2026-02-14-spec-contradiction-auth.md work/collaboration/inbox/2026-02-15T0900-analyst-update-auth-spec.yaml
git commit -m "Resolved problem: Remove offline auth requirement from spec"
```

---

## Validation Checklist

Before creating HiC file, verify:

- [ ] **Correct subdirectory** chosen based on escalation type
- [ ] **Template followed** with all required sections filled
- [ ] **Frontmatter complete** with accurate metadata
- [ ] **Context provided** - HiC can understand without additional research
- [ ] **Evidence included** - data, logs, links to support escalation
- [ ] **Attempted solutions documented** - show what was tried
- [ ] **Related work linked** - specs, ADRs, tasks, prior discussions
- [ ] **Task references updated** - if blocking task, update task file
- [ ] **Work log entry created** - document escalation in your log
- [ ] **Filename follows convention** - `YYYY-MM-DD-[slug].md`

---

## Anti-Patterns (Do NOT Do)

### ❌ Wrong Subdirectory Choice
**Problem:** Blocker filed as decision request  
**Why bad:** HiC may not check decision_requests daily, delays resolution  
**Correct:** Use `blockers/` for external actions preventing progress

### ❌ Insufficient Context
**Problem:** Decision request lacks background or alternatives  
**Why bad:** HiC cannot make informed decision, must ask for clarification  
**Correct:** Provide full context, all options with pros/cons

### ❌ Waiting Instead of Continuing
**Problem:** Agent creates blocker then sits idle  
**Why bad:** Wastes time, blocks other work  
**Correct:** Create blocker, mark task frozen, **continue with other tasks**

### ❌ Escalating Trivial Decisions
**Problem:** "Should I name this variable `userId` or `user_id`?"  
**Why bad:** Clutters HiC directory, slows autonomous work  
**Correct:** Follow existing conventions, make minor decisions autonomously

### ❌ Skipping Work Logs
**Problem:** Create HiC file but don't log it  
**Why bad:** Lost traceability, hard to track what happened  
**Correct:** Always create work log entry referencing HiC file

### ❌ Not Updating Task Status
**Problem:** Create blocker but leave task status as `in_progress`  
**Why bad:** Task appears active but is actually blocked  
**Correct:** Update task to `frozen` with `blocker_ref`

### ❌ Unclear What's Needed
**Problem:** "Something is wrong with the API"  
**Why bad:** HiC doesn't know what action to take  
**Correct:** Be specific: "API returns 401, need OAuth credentials for staging"

### ❌ Missing Frontmatter
**Problem:** File lacks YAML frontmatter or incomplete metadata  
**Why bad:** Cannot filter, search, or automate processing  
**Correct:** Use templates, ensure all frontmatter fields filled

---

## Related Directives

- **Directive 019:** File-Based Collaboration Framework - Parent pattern
- **Directive 024:** Self-Observation Protocol - Checkpointing and reflection
- **Directive 018:** Traceable Decisions - Document decision rationale
- **Directive 007:** Agent Declaration - Authority boundaries

## Related Approaches

- **Work Directory Orchestration:** `doctrine/approaches/work-directory-orchestration.md`
- **AFK Mode:** `doctrine/shorthands/afk-mode.md`

## Related ADRs

- **ADR-047:** Human-in-Charge Directory Structure - Architecture decision
- **ADR-004:** Work Directory Structure - Overall work directory design
- **ADR-008:** File-Based Async Coordination - Async collaboration principle
- **ADR-005:** Coordinator Agent Pattern - Manager Mike's role

---

**Status:** ✅ Active  
**Version:** 1.0.0  
**Created:** 2026-02-14  
**Author:** Curator Claire  
**Maintained by:** Manager Mike, Planning Petra
