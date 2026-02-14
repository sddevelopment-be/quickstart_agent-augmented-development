# Human-in-Charge Coordination Templates

**Purpose:** Canonical templates for agent-to-human escalation via the `work/human-in-charge/` directory structure.

**Version:** 1.0.0  
**Created:** 2026-02-14  
**Related:** [Directive 040](../../directives/040_human_in_charge_escalation_protocol.md), [ADR-047](../../../docs/architecture/adrs/ADR-047-human-in-charge-directory-structure.md)

---

## Overview

These templates standardize how agents escalate decisions, blockers, and problems to the Human-in-Charge (HiC). They ensure complete context, consistent formatting, and structured resolution workflows.

**Key Principle:** Templates live in `doctrine/templates/coordination/` (canonical source), agents copy them to `work/human-in-charge/*/` when creating escalations.

---

## Templates

### 1. `hic-executive-summary.md`

**Purpose:** High-level summaries of complex multi-agent initiatives requiring HiC review.

**When to use:**
- ✅ Multi-agent initiative completes major phase
- ✅ Architecture changes affect multiple modules
- ✅ Major refactoring with cross-cutting impact
- ✅ Periodic progress reports (weekly/bi-weekly)

**Who creates:**
- **Primary:** Manager Mike (consolidates multi-agent outputs)
- **Secondary:** Any agent after completing complex initiative

**Output location:** `work/human-in-charge/executive_summaries/YYYY-MM-DD-[slug].md`

**Example:**
```bash
cp doctrine/templates/coordination/hic-executive-summary.md \
   work/human-in-charge/executive_summaries/2026-02-14-authentication-migration-summary.md
```

---

### 2. `hic-decision-request.md`

**Purpose:** Request explicit decisions that agents cannot make autonomously.

**When to use:**
- ✅ Architectural choices (REST vs GraphQL, SQL vs NoSQL)
- ✅ Breaking API changes
- ✅ Technology stack additions/changes
- ✅ Security or privacy policy decisions
- ✅ Trade-offs with business impact
- ✅ Ambiguous requirements with multiple interpretations

**Who creates:** Any agent encountering decision beyond authority

**Output location:** `work/human-in-charge/decision_requests/YYYY-MM-DD-[slug].md`

**Priority:** Medium (check every 2-3 days)

**Example:**
```bash
cp doctrine/templates/coordination/hic-decision-request.md \
   work/human-in-charge/decision_requests/2026-02-14-database-choice-sessions.md
```

---

### 3. `hic-blocker.md`

**Purpose:** Report external blockers preventing agent progress.

**When to use:**
- ✅ Missing credentials (API keys, passwords)
- ✅ Awaiting PR reviews from humans
- ✅ External system dependencies (down services, access requests)
- ✅ Clarifications needed from product owner
- ✅ Resource provisioning (infrastructure, accounts)

**Who creates:** Any agent when external action prevents progress

**Output location:** `work/human-in-charge/blockers/YYYY-MM-DD-[slug].md`

**Priority:** ⚠️ **Highest - Check daily**

**Action after creating:**
1. Create blocker file
2. Update related task to `status: frozen`
3. **Continue with other tasks** (don't wait idle)

**Example:**
```bash
cp doctrine/templates/coordination/hic-blocker.md \
   work/human-in-charge/blockers/2026-02-14-aws-s3-credentials.md
```

---

### 4. `hic-problem.md`

**Purpose:** Report internal problems requiring human judgment.

**When to use:**
- ✅ Contradictory requirements in specifications
- ✅ Tests pass but behavior seems wrong
- ✅ Implementation diverges significantly from plan
- ✅ Discovered constraints not in requirements
- ✅ Unexpected results with unclear cause
- ✅ Design conflicts between modules

**Who creates:** Any agent discovering problems requiring judgment

**Output location:** `work/human-in-charge/problems/YYYY-MM-DD-[slug].md`

**Priority:** Medium (check weekly)

**Example:**
```bash
cp doctrine/templates/coordination/hic-problem.md \
   work/human-in-charge/problems/2026-02-14-spec-contradiction-auth.md
```

---

## Template Structure

All templates include:

1. **YAML Frontmatter**
   - `type:` escalation type (executive_summary, decision_request, blocker, problem)
   - `agent:` agent name creating escalation
   - `date:` creation date (YYYY-MM-DD)
   - `urgency:` urgency level (low, medium, high, critical)
   - `status:` current status (pending, active, resolved, decided)
   - Additional type-specific metadata

2. **Context Section**
   - Full background explaining situation
   - Why escalation is needed
   - Related work references

3. **Core Content**
   - Type-specific sections (options, evidence, impact, etc.)
   - Structured data for HiC review
   - Agent recommendation (when applicable)

4. **Resolution Section** (bottom)
   - HiC fills this in when resolving
   - Documents decision/action taken
   - Follow-up tasks created
   - Status update trigger

---

## Usage Workflow

### For Agents

1. **Recognize escalation condition** (see "When to use" above)
2. **Choose correct template** based on escalation type
3. **Copy template** from `doctrine/templates/coordination/`
4. **Rename** to `YYYY-MM-DD-[descriptive-slug].md`
5. **Place in** appropriate `work/human-in-charge/*/` subdirectory
6. **Fill all sections** with complete information
7. **Update related task** (if blocking) with reference
8. **Log escalation** in your work log
9. **Continue with other work** if possible

### For Human-in-Charge

1. **Check subdirectories** in priority order:
   - Daily: `blockers/`
   - Every 2-3 days: `decision_requests/`
   - Weekly: `problems/`, `executive_summaries/`

2. **Review escalation file** - all context should be present

3. **Fill "Resolution" section** at bottom of file

4. **Update frontmatter status** (e.g., `status: resolved`)

5. **Commit with descriptive message**

6. **Create follow-up tasks** if needed

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

## Integration with HiC Escalation Protocol

**Canonical Documentation:** [Directive 040](../../directives/040_human_in_charge_escalation_protocol.md)

These templates implement the file format standards defined in Directive 040. Key integration points:

1. **AFK Mode:** When operating autonomously, agents escalate via these templates instead of waiting for real-time human response

2. **Task Lifecycle:** Tasks reference HiC files via `blocker_ref` field when frozen

3. **Work Logs:** Agents log escalations with links to HiC files

4. **Manager Mike:** Monitors `work/human-in-charge/` and consolidates multi-agent escalations into executive summaries

5. **File-Based Async Coordination:** Git-versioned escalations enable async agent-human collaboration

---

## Template Maintenance

**Source of Truth:** `doctrine/templates/coordination/` (this directory)

**Distribution Points:**
- Agents copy from here to `work/human-in-charge/*/`
- Do NOT edit templates in work directories - always edit source

**Version Control:**
- Templates are versioned with doctrine
- Changes propagate via agents copying updated templates
- Old escalation files retain their template version (not retroactively updated)

**Update Process:**
1. Edit template in `doctrine/templates/coordination/`
2. Document change in template changelog (if major)
3. Notify agents via directive update
4. Agents use new template for new escalations

---

## Metrics & Quality

**Template Completeness:** Each template ensures agents provide:
- Full context (no additional research needed by HiC)
- Evidence (logs, error messages, screenshots)
- Attempted solutions (what was tried and why it didn't work)
- Clear question/request (unambiguous action needed)
- Related work links (specs, ADRs, tasks, discussions)

**Resolution Speed:** Priority ordering helps HiC triage:
- Blockers (daily) → fastest resolution path
- Decisions (2-3 days) → adequate time for review
- Problems (weekly) → batch review efficiency
- Summaries (weekly) → milestone alignment

**Agent Autonomy:** Templates enable agents to:
- Continue other work while waiting
- Provide complete context asynchronously
- Document decision rationale (for future reference)
- Learn from past escalations (via git history)

---

## Related Documentation

### Complete System Documentation
- **Directive 040:** [Human-in-Charge Escalation Protocol](../../directives/040_human_in_charge_escalation_protocol.md) - Complete usage guide
- **ADR-047:** [Human-in-Charge Directory Structure](../../../docs/architecture/adrs/ADR-047-human-in-charge-directory-structure.md) - Architecture decision
- **HiC Directory README:** [work/human-in-charge/README.md](../../../work/human-in-charge/README.md) - Quick reference

### Integration Points
- **AFK Mode:** [doctrine/shorthands/afk-mode.md](../../shorthands/afk-mode.md) - Autonomous operation protocol
- **Work Directory Orchestration:** [doctrine/approaches/work-directory-orchestration.md](../../approaches/work-directory-orchestration.md)
- **Manager Mike Profile:** [doctrine/agents/manager.agent.md](../../agents/manager.agent.md) - HiC monitoring duties
- **ADR-004:** Work Directory Structure - Overall work directory design
- **ADR-008:** File-Based Async Coordination - Async collaboration principle

---

## Examples

Complete examples of filled templates are provided in [Directive 040](../../directives/040_human_in_charge_escalation_protocol.md):

1. **Decision Request Example:** Database choice for session storage (Redis vs PostgreSQL)
2. **Blocker Example:** Missing AWS S3 credentials blocking integration
3. **Problem Example:** Contradictory specifications in authentication flow

---

## Status

**Version:** 1.0.0  
**Created:** 2026-02-14  
**Author:** Curator Claire  
**Maintained by:** Curator Claire, Manager Mike  
**Status:** ✅ Active - Canonical Template Source
