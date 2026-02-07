<!-- The following information is to be interpreted literally -->

# 018 Traceable Decisions Directive

Purpose: Instruct agents on decision traceability and rationale capture to maintain architectural context throughout the development lifecycle.

## 1. Scope and Applicability

This directive is **optional** and **not safety-critical**. Load it when:

- Working on tasks with architectural implications
- Creating or modifying documentation in `${DOC_ROOT}/architecture/`
- Implementing features that establish new patterns or conventions
- Collaborating with humans on decision-heavy work
- Generating artifacts that will influence future development

## 2. Core Requirements

### 2.1 Pre-Task Decision Check

Before proposing architectural changes, agents MUST:

1. **Load ADR Index:** Read `${DOC_ROOT}/architecture/adrs/README.md` to identify relevant decisions
2. **Select Relevant ADRs:** Identify 2-3 ADRs most relevant to task scope (keyword matching)
3. **Load ADR Content:** Read full text of selected ADRs into context
4. **Flag Conflicts:** If task conflicts with established ADR, alert human before proceeding
5. **Reference in Plan:** Include ADR references when proposing approach

**Example:**

```
[Agent performing task: "Implement agent handoff protocol"]

Step 1: Load ${DOC_ROOT}/architecture/adrs/README.md
Step 2: Identify relevant: ADR-002, ADR-003, ADR-008
Step 3: Load full text of ADR-008 (File-Based Async Coordination)
Step 4: Check for conflicts: None found
Step 5: Reference in proposal: "Per ADR-008, will use file-based handoff..."
```

### 2.2 Decision Marker Generation

When making architectural choices during artifact creation, agents MUST add decision markers:

**Full Format (for significant decisions):**

```markdown
<!-- DECISION-MARKER: ADR-NNN -->
**Decision:** [Brief statement of what was decided]
**Rationale:** [Why this approach was chosen]
**Alternatives:** [Options considered and rejected with reasons]
**Consequences:** [Accepted trade-offs]
**Status:** [Implemented | Proposed | Deprecated]
**Date:** [YYYY-MM-DD]
<!-- END-DECISION-MARKER -->
```

**Minimal Format (for referencing existing decisions):**

```markdown
<!-- DECISION: ADR-NNN - [One-line rationale] -->
```

**When to Add Markers:**

- Establishing new patterns or conventions
- Choosing between alternative implementations
- Applying architectural decisions from ADRs
- Making trade-offs with known consequences
- Implementing critical design choices

**When NOT to Add Markers:**

- Trivial implementation details
- Standard patterns already well-documented
- Obvious choices requiring no justification
- Temporary experimental code

### 2.3 Commit Message Decision Rationale

When creating commits with architectural changes, agents SHOULD include decision context:

```
<type>: <subject>

Decision: [Brief decision statement]
ADR: [ADR-NNN reference if formalized]
Rationale: [One-line justification]
Context: [Link to ideation/synthesis if applicable]
```

**Example:**

```
feat: add decision rationale to task schema

Decision: Extend task YAML with decision_rationale block
ADR: ADR-014
Rationale: Enable agents to document decision context during execution
Context: See synthesis/traceable-decision-patterns-synthesis.md
```

### 2.4 Task Result Decision Documentation

For orchestrated tasks involving architectural decisions, agents MUST include `decision_rationale` block in task YAML result:

```yaml
result:
  summary: "Created coordination protocol with file-based handoffs"
  artefacts:
    - "${DOC_ROOT}/architecture/protocols/agent-handoff.md"
  decision_rationale:
    adr: "ADR-008"
    justification: "File-based coordination aligns with established pattern"
    alternatives_considered: ["API-based", "message queue"]
    chosen_because: "Git-native, no additional infrastructure, transparent state"
  completed_at: "2025-11-25T12:00:00Z"
```

### 2.5 Work Log Decision Context

Work logs MUST include decision-making context in the "Context" or "Approach" sections:

```markdown
## Context

This task required implementing agent handoff protocol per ADR-008.

**Relevant ADRs:**
- ADR-008: File-Based Async Coordination (primary guidance)
- ADR-003: Task Lifecycle State Management (handoff timing)
- ADR-014: Traceable Decision Integration (documentation requirements)

**Decision Points:**
1. Handoff trigger: Task completion vs. explicit signal
2. State transition: Move file vs. create new file
3. Context propagation: Copy all vs. selective fields
```

## 3. Linking Conventions

### 3.1 Forward Links (ADR → Artifacts)

When creating ADRs, list affected artifacts:

```markdown
## Affected Artifacts

This decision impacts:
- **Code:** `src/coordination/*.py`
- **Documentation:** `${DOC_ROOT}/architecture/protocols/handoff.md`
- **Directives:** `.github/agents/directives/012_operating_procedures.md`
- **Templates:** `templates/agent-tasks/task-base.yaml`
```

### 3.2 Backward Links (Artifacts → ADR)

When creating artifacts governed by ADRs, reference decisions in headers:

**Markdown files:**

```markdown
# Agent Handoff Protocol

**Governed by:** [ADR-008: File-Based Async Coordination](../adrs/ADR-008.md)
**Related:** [ADR-003: Task Lifecycle](../adrs/ADR-003.md)

[Document content...]
```

**Code files (Python example):**

```python
"""
Agent coordination module implementing file-based handoffs.

Architecture: ADR-008 (File-Based Async Coordination)
Related: ADR-003 (Task Lifecycle State Management)
"""
```

**YAML files:**

```yaml
# Task schema definition
# Governed by: ADR-003 (Task Lifecycle)
# Extended by: ADR-014 (Traceable Decisions)

task:
  id: string
  ...
```

### 3.3 Cross-References (Decision → Decision)

When creating ADRs that relate to existing decisions:

```markdown
**Related ADRs:**
- [ADR-001: Modular Directives](ADR-001-modular-agent-directive-system.md) — Provides directive framework
- [ADR-003: Task Lifecycle](ADR-003-task-lifecycle-state-management.md) — Defines state transitions
- Supersedes: ADR-007 (deprecated manual coordination approach)
- Superseded by: None
```

## 4. Decision Debt Tracking

### 4.1 Metric Definition

Agents SHOULD track decision debt in work log metrics:

```yaml
metrics:
  decision_debt:
    markers_added: 3           # New decision markers created this task
    markers_promoted: 1        # Markers formalized as ADRs
    adrs_referenced: 2         # Existing ADRs linked in artifacts
    debt_ratio: 0.15          # (markers_added - markers_promoted) / markers_added
```

### 4.2 Acceptable Thresholds

- **<20%** (Healthy): Normal balance, some markers are implementation details
- **20-40%** (Attention): Growing backlog, note in work log
- **>40%** (Alert): Flag for human review, suggest synthesis session

### 4.3 Reporting

If decision debt exceeds 20%, agents SHOULD include in work log "Lessons Learned":

```markdown
## Lessons Learned

**Decision Debt:** Current ratio 35% (7 markers added, 2 promoted to ADRs).
**Recommendation:** Consider synthesis session to consolidate markers related to coordination patterns.
**Affected Areas:** Agent handoff protocol, state transition logic, error handling.
```

## 5. Flow State Awareness

Agents MUST adapt decision capture behavior to human flow state:

### 5.1 Deep Creation Flow

**Detection signals:**

- Long periods without agent interaction
- Rapid code commits without pauses
- Human not requesting decision documentation

**Agent Behavior:**

- Passive: Don't interrupt for decision capture
- Defer: Note decisions for later synthesis
- Support: Answer questions without proactive suggestions

**Example:**

```
[Human commits 5 files in 10 minutes without messages]
Agent: [Silently tracks potential decision points]
Agent: [Does NOT suggest "Add decision marker here?"]
Agent: [Waits for human to initiate interaction]
```

### 5.2 Agent Collaboration Flow

**Detection signals:**

- Active back-and-forth with agent
- Human asking "should we..." or "what about..."
- Iterative refinement of approach

**Agent Behavior:**

- Active: Suggest decision markers in real-time
- Template: Offer formatted decision marker templates
- Validate: Check marker format and ADR references

**Example:**

```
Human: "Should we use file-based or API coordination?"
Agent: "Checking ADR-008... File-based coordination is established pattern.
        Shall I add decision marker referencing ADR-008?"
Human: "Yes"
Agent: [Adds formatted marker with ADR reference]
```

### 5.3 Reflection/Synthesis Flow

**Detection signals:**

- Human reviewing multiple files
- Explicit request for synthesis or documentation
- Batch updates to decision markers

**Agent Behavior:**

- Summarize: Extract decision patterns from session
- Suggest: Recommend ADR creation if 3+ related markers
- Draft: Create synthesis documents linking decisions

**Example:**

```
Agent: "Found 5 decision markers related to coordination patterns.
        Decision debt ratio: 35% (above 20% threshold).
        Recommend: Draft synthesis document consolidating these decisions.
        May I create synthesis document in ${DOC_ROOT}/architecture/synthesis/?"
```

## 6. Validation Requirements

Agents MUST validate decision traceability before completing tasks:

### 6.1 Pre-Completion Checks

- [ ] All new artifacts reference governing ADRs (header/frontmatter)
- [ ] Decision markers follow standard format (full or minimal)
- [ ] ADR references are valid (no broken links)
- [ ] Task YAML includes `decision_rationale` if architectural
- [ ] Work log documents decision-making process
- [ ] Commit messages include decision context for architectural changes

### 6.2 Link Validation

Check that:

- ADR numbers exist in `${DOC_ROOT}/architecture/adrs/`
- Cross-references between ADRs are valid
- Synthesis documents link to source ideation
- Ideation documents link to resulting ADRs (if formalized)

### 6.3 Format Validation

Decision markers MUST include:

- ADR reference (if formalized decision)
- Decision statement (what was decided)
- Rationale (why this choice)
- Date (when decided)

Optional but recommended:

- Alternatives (options rejected)
- Consequences (trade-offs accepted)
- Status (implemented/proposed/deprecated)

## 7. Discovery Support

### 7.1 Search Patterns

Agents should be able to respond to these queries:

```
"What ADRs govern authentication?"
→ Search ${DOC_ROOT}/architecture/adrs/README.md for "authentication"
→ Load relevant ADR full text
→ Summarize decision and rationale

"Why did we choose file-based coordination?"
→ Search for "DECISION-MARKER" + "coordination"
→ Load ADR-008
→ Explain rationale with context

"Show me all decisions about error handling"
→ rg "Decision.*error" ${DOC_ROOT}/architecture/
→ List ADRs and decision markers
→ Summarize common patterns
```

### 7.2 Context Loading Strategy

To manage context window efficiently:

**Always Load:**

- `${DOC_ROOT}/architecture/adrs/README.md` (ADR index)

**Load if Task-Relevant:**

- ADRs matching task keywords (top 3 by relevance)
- Synthesis documents referenced by relevant ADRs

**Load on Request:**

- Full ideation document history
- Older ADRs not referenced by recent decisions
- Decision markers from unrelated code areas

## 8. Integration with Other Directives

### 8.1 Dependencies

This directive builds on:

- **004 (Documentation & Context Files):** Defines canonical document locations
- **008 (Artifact Templates):** Provides templates for decision markers

### 8.2 Related Directives

Works with:

- **012 (Operating Procedures):** Decision capture is part of standard workflow
- **014 (Work Log Creation):** Work logs include decision context

### 8.3 Conflicts

If conflicts arise:

- **Priority 1:** Safety-critical directives (001, 002, 003, 006, 007, 009, 010, 011, 012)
- **Priority 2:** This directive (016, optional)
- **Resolution:** Flag conflict in work log, request human guidance

## 9. Examples

### Example 1: Referencing Existing ADR

```markdown
# Agent Task Assignment Protocol

**Governed by:** [ADR-003: Task Lifecycle State Management](../adrs/ADR-003.md)

## Task States

Tasks progress through well-defined states as specified in ADR-003:

<!-- DECISION: ADR-003 - Task states ensure deterministic lifecycle -->

1. **new**: Created in inbox/
2. **assigned**: Moved to assigned/<agent>/
3. **in_progress**: Agent actively working
4. **done**: Completed successfully
```

### Example 2: New Decision Marker

```markdown
# Agent Handoff Error Recovery

<!-- DECISION-MARKER: ADR-014 -->
**Decision:** Retry handoffs up to 3 times before escalating to error state
**Rationale:** Transient file system issues should not fail coordination
**Alternatives:** 
  - Immediate error (rejected: too brittle for network filesystems)
  - Infinite retry (rejected: could mask real problems)
**Consequences:** Small delay (3-5 seconds) in error detection, but improved reliability
**Status:** Implemented
**Date:** 2025-11-25
<!-- END-DECISION-MARKER -->

[Implementation code...]
```

### Example 3: Task YAML with Decision Rationale

```yaml
id: 2025-11-25T1200-architect-coordination-protocol
agent: architect
status: done
title: "Design agent handoff error recovery"

result:
  summary: "Created retry logic for handoff failures per ADR-008 resilience principles"
  artefacts:
    - "${DOC_ROOT}/architecture/protocols/handoff-error-recovery.md"
    - "src/coordination/retry.py"
  decision_rationale:
    adr: "ADR-014"
    justification: "Error recovery requires explicit decision documentation"
    alternatives_considered: 
      - "Immediate failure"
      - "Infinite retry with backoff"
    chosen_because: "3-retry limit balances reliability with failure detection"
  completed_at: "2025-11-25T12:30:00Z"
```

### Example 4: Work Log Decision Context

```markdown
# Work Log: Agent Coordination Error Recovery

**Agent:** architect
**Date:** 2025-11-25T12:30:00Z

## Context

Task required designing error recovery for agent handoffs per ADR-008.

**Relevant ADRs:**
- ADR-008: File-Based Async Coordination (primary)
- ADR-003: Task Lifecycle State Management (error states)
- ADR-014: Traceable Decision Integration (documentation requirements)

**Key Question:** How many retries before escalating to error state?

## Approach

Analyzed trade-offs between reliability and failure detection:

1. **No retry** (immediate error):
   - Pro: Fast failure detection
   - Con: Brittle for transient issues
   - Decision: Rejected

2. **Infinite retry with backoff**:
   - Pro: Eventually succeeds for transient issues
   - Con: Masks real problems indefinitely
   - Decision: Rejected

3. **Fixed retry limit (3 attempts)**:
   - Pro: Handles transient issues, detects real failures within 5 seconds
   - Con: Must choose arbitrary limit
   - Decision: **Selected** (documented in ADR-014 marker)

## Decision Marker Added

Added full decision marker to `${DOC_ROOT}/architecture/protocols/handoff-error-recovery.md`:
- References ADR-014 for traceability
- Documents alternatives and rationale
- Includes consequences (3-5 second delay in error detection)

## Metrics

```yaml
decision_debt:
  markers_added: 1
  markers_promoted: 0
  adrs_referenced: 3
  debt_ratio: 0.0  # Marker documents implementation detail, ADR not needed
```

```

## 10. Non-Compliance

This directive is **optional** (requiredInAgents: false), so non-compliance does not block task completion.

However, agents SHOULD note when decision traceability is skipped:

```markdown
## Lessons Learned

**Decision Traceability:** Not applied to this task (implementation details only, no architectural decisions).
**Justification:** Changes were mechanical refactoring without new patterns or trade-offs.
```

If architectural decisions ARE made without traceability:

```markdown
## Lessons Learned

⚠️ **Decision Traceability Gap:** Made architectural choice about error handling but didn't add decision marker.
**Recommendation:** Retroactively add marker or create follow-up task for documentation.
**Rationale:** Future contributors may not understand why 3-retry limit was chosen.
```

## 11. Maintenance

This directive should be updated when:

- ADR-014 is revised with new decision marker formats
- New decision artifact types are introduced
- Validation tooling changes requirements
- Decision debt thresholds are adjusted based on empirical data

Version history maintained in ADR-014.

---

**Directive Version:** 1.0.0  
**Status:** Active  
**Required in Agents:** false  
**Safety Critical:** false  
**Dependencies:** 004 (Documentation), 008 (Templates)  
**Related:** 012 (Operating Procedures), 014 (Work Logs)  
**Source ADR:** [ADR-014: Traceable Decision Integration](../../${DOC_ROOT}/architecture/adrs/ADR-014-traceable-decision-integration.md)
