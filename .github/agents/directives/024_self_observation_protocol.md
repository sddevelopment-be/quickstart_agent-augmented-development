<!-- The following information is to be interpreted literally -->

# 024 Self-Observation Protocol Directive

**Purpose:** Define standards for mid-execution self-monitoring and course correction during agent tasks.

**Core Concept:** See [Ralph Wiggum Loop](../approaches/ralph-wiggum-loop.md) for the complete operational pattern. This directive formalizes the requirements.

## 1. Scope

This directive applies to:

- Tasks with estimated duration >30 minutes
- Multi-step workflows (5+ sequential operations)
- Cross-agent collaborations requiring handoffs
- Any task where uncertainty markers (⚠️) accumulate

Agents MAY apply this directive to shorter tasks when they detect warning signs.

## 2. Checkpoint Requirements

### Mandatory Checkpoints

Agents MUST invoke a Ralph Wiggum loop checkpoint at:

1. **25% task completion** — Early warning system
2. **Task initialization** — Define stopping conditions: Invoke `tactics/stopping-conditions.tactic.md` before starting long-running tasks
3. **Pre-delegation** — Before creating tasks for other agents
4. **After major context load** — When loading 5+ new directives or large documents
5. **Warning accumulation** — When 3+ ⚠️ symbols appear within 10 minutes
6. **Before task completion** — Final alignment verification

### Optional Checkpoints

Agents MAY invoke checkpoints:

- Every 15-20 minutes during long tasks
- When switching between reasoning modes multiple times
- When detecting internal confusion or conflicting constraints
- When output quality appears to be degrading
- Before requesting human guidance

## 3. Checkpoint Protocol

### Step 1: Enter Meta-Mode

Switch from current mode to `/meta-mode` using transition annotation:

```markdown
[mode: analysis → meta]
```

### Step 2: Document Checkpoint Header

```markdown
🔄 **Ralph Wiggum Loop Checkpoint**
[Timestamp: YYYY-MM-DDTHH:MM:SSZ]
[Current Mode: /previous-mode]
[Task Progress: XX% complete, Step N of M]
[Elapsed Time: XX minutes]
```

### Step 3: Run Self-Observation Checklist

Evaluate ALL items systematically:

```markdown
## Self-Observation Checklist

### Execution State
- **Current task:** [one-line description]
- **Original goal:** [from task descriptor or initial prompt]
- **Progress:** [steps completed / total steps]
- **Time budget:** [elapsed / estimated]

### Warning Signs (Mark all that apply)
- [ ] Repetitive patterns: Am I doing the same thing multiple times?
- [ ] Goal drift: Have I lost sight of the original objective?
- [ ] Speculation: Am I guessing instead of validating?
- [ ] Verbosity: Are outputs becoming unclear or too long?
- [ ] Scope creep: Am I adding work not requested?
- [ ] Directive violations: Am I ignoring established protocols?
- [ ] Confusion: Do I understand what I'm doing next? (⚠️ if no)
- [ ] Mode misuse: Is my reasoning mode appropriate for current task?

### Integrity Symbols
- ❗️ Critical issues: [list or "none detected"]
- ⚠️ Warning signs: [list or "none detected"]
- ✅ Alignment status: [confirmed/uncertain/violated]
```

### Step 4: Pattern Recognition

If any warnings detected, identify the pattern:

| Pattern | Symptoms | Required Action |
|---------|----------|-----------------|
| **Drift** | Scope creep, added features | Revert to original scope, apply Directive 020 |
| **Confusion** | Multiple ⚠️, uncertainty | Stop and request clarification |
| **Gold-plating** | Over-engineering, future features | Remove unnecessary work |
| **Mode misuse** | Wrong reasoning mode | Switch to appropriate mode |
| **Directive violation** | Skipping protocols | Review and comply with directive |
| **Token waste** | Verbose, repetitive outputs | Simplify, reduce verbosity |

### Step 5: Make Decision

Choose ONE action:

#### Option A: Continue ✅

Requirements:
- Zero critical issues (❗️)
- Fewer than 2 warning signs (⚠️)
- Alignment confirmed
- Clear understanding of next steps

```markdown
### Decision: Continue ✅
**Reasoning:** [why safe to continue]
**Adjustments:** [any minor tweaks, or "none"]

[mode: meta → previous-mode] — Resuming execution...
```

#### Option B: Adjust Course ⚠️

Requirements:
- 2-4 warning signs detected
- Issues are correctable
- Root cause identified

```markdown
### Decision: Adjust Course ⚠️

**Warning Signs:**
1. [specific warning with evidence]
2. [specific warning with evidence]

**Root Cause:** [why warnings occurred]

**Corrections:**
1. [specific action to fix warning 1]
2. [specific action to fix warning 2]

**Success Criteria:** [how to know corrections worked]

[mode: meta → adjusted-mode] — Resuming with corrections...
```

#### Option C: Stop and Escalate ❗️

Requirements:
- 5+ warning signs OR any critical issue (❗️)
- Cannot safely continue without guidance
- Risk of wasted effort or incorrect output

```markdown
### Decision: Stop and Escalate ❗️

**Critical Issues:**
1. [specific issue]
2. [specific issue]

**Why Cannot Continue:**
[clear explanation of blocking issues]

**Guidance Needed:**
1. [specific question or clarification needed]
2. [specific question or clarification needed]

**Current Status:** [what is complete, what is blocked]

[mode: meta → paused] — Awaiting guidance before resuming.
```

### Step 6: Exit Meta-Mode

After decision, transition back to appropriate mode:

```markdown
[mode: meta → analysis]  # or other appropriate mode
```

## 4. Documentation Requirements

### In Work Logs (Directive 014)

Include checkpoint section:

```markdown
## Ralph Wiggum Loop Checkpoints

**Total Checkpoints:** 3
**Adjustments Made:** 1
**Escalations:** 0

### Checkpoint 1 (25% complete)
- **Time:** 2026-01-31T14:30:00Z
- **Outcome:** Continue ✅
- **Notes:** All checks passed

### Checkpoint 2 (50% complete)
- **Time:** 2026-01-31T15:15:00Z
- **Outcome:** Adjust Course ⚠️
- **Corrections:** Removed gold-plating, restored scope
- **Notes:** Detected scope creep, corrected successfully

### Checkpoint 3 (Pre-completion)
- **Time:** 2026-01-31T16:00:00Z
- **Outcome:** Continue ✅
- **Notes:** Final alignment confirmed
```

### In Task Descriptors

Add checkpoint metadata:

```yaml
checkpoints:
  - timestamp: "2026-01-31T14:30:00Z"
    progress: "25%"
    outcome: "continue"
    warnings: 0
  - timestamp: "2026-01-31T15:15:00Z"
    progress: "50%"
    outcome: "adjusted"
    warnings: 2
    corrections:
      - "Removed scope creep"
      - "Applied Directive 020"
```

## 5. Automation Support

Agents working with CLI automation SHOULD support:

```bash
# Manual checkpoint invocation
ralph-wiggum-loop check --task-id <task-id>

# Automatic checkpoints
ralph-wiggum-loop watch \
  --task-id <task-id> \
  --interval 15 \  # minutes
  --auto-continue-if-clean
```

See `ops/scripts/ralph-wiggum-loop.py` for implementation reference.

## 6. Success Criteria

The self-observation protocol succeeds when:

1. **Detection rate:** Warning signs caught before significant wasted effort (>80% of issues)
2. **Correction effectiveness:** Course adjustments prevent task failure (>90% success)
3. **False positive rate:** Unnecessary pauses <10% of checkpoints
4. **Time efficiency:** Checkpoints add <5% overhead to total task duration
5. **Quality improvement:** Measurable reduction in post-completion revisions

## 7. Common Pitfalls

### Pitfall 1: Checkpoint Fatigue

**Problem:** Checking too frequently disrupts flow state.

**Solution:** 
- Maximum 1 checkpoint per 15 minutes
- Skip optional checkpoints during high-confidence phases
- Trust mandatory checkpoints are sufficient

### Pitfall 2: Incomplete Assessment

**Problem:** Rushing through checklist to "save time."

**Solution:**
- Each checklist item requires 10-30 seconds of genuine reflection
- Cannot skip items or mark all as "no" without evidence
- Checkpoint quality more important than checkpoint speed

### Pitfall 3: Ignoring Results

**Problem:** Detecting issues but continuing anyway.

**Solution:**
- If decision is "Adjust," MUST apply corrections before continuing
- If decision is "Escalate," MUST stop and request guidance
- Cannot override checkpoint decision without human approval

### Pitfall 4: Over-Sensitivity

**Problem:** Treating minor style variations as critical issues.

**Solution:**
- Focus on substantive problems (scope, direction, safety)
- Distinguish ⚠️ (adjust) from ❗️ (stop) appropriately
- Not every imperfection requires a checkpoint

## 8. Integration with Existing Directives

### Relation to Directive 010 (Mode Protocol)

- Ralph Wiggum checkpoints operate IN meta-mode
- Mode transitions must be annotated per Directive 010
- Reflection Loop primer integrates with this protocol

### Relation to Directive 011 (Risk & Escalation)

- Use risk markers (❗️⚠️) consistently
- Escalation follows existing procedures
- Self-observation is proactive; error handling is reactive

### Relation to Directive 014 (Work Log Creation)

- Document all checkpoints in work log
- Include checkpoint summary in metadata
- Note corrections and escalations

### Relation to Directive 020 (Locality of Change)

- Scope creep is primary warning sign
- Gold-plating triggers checkpoints
- Course corrections often apply this directive

## 9. Exceptions

Agents MAY skip checkpoints when:

- **Trivial tasks:** <5 minutes estimated duration, single-step operations
- **Emergency fixes:** Critical production issues requiring immediate action
- **Read-only operations:** Pure analysis/observation with no modifications
- **Explicit override:** Human explicitly instructs "skip checkpoints for this task"

Document exception rationale in work log:

```markdown
**Checkpoint Exception:** Task too brief (<3 min, read-only analysis)
**Rationale:** Single-step grep operation, no risk of drift
```

## 10. Training & Adoption

### For New Agents

1. Read approach document: `.github/agents/approaches/ralph-wiggum-loop.md`
2. Review 3 example checkpoints from experienced agents
3. Practice on supervised tasks before autonomous use
4. Request human review of first 5 checkpoints

### For Experienced Agents

1. Integrate checkpoints into existing workflows
2. Tune checkpoint frequency based on task complexity
3. Share effective patterns with other agents
4. Contribute improvements to approach document

## 11. Validation

This directive complies when work logs show:

- [ ] Mandatory checkpoints executed at required milestones
- [ ] Self-observation checklist completed for each checkpoint
- [ ] Decision rationale documented with integrity symbols
- [ ] Course corrections applied when warnings detected
- [ ] Escalations include clear guidance requests
- [ ] Checkpoint metadata included in task artifacts

## 12. Version History

- **1.0.0** (2026-01-31): Initial directive specification

---

**Directive Status:** Proposed  
**Applies To:** All agents during task execution  
**Dependencies:** Directive 010 (Mode Protocol), Directive 014 (Work Log Creation)  
**Version:** 1.0.0  
**Last Updated:** 2026-01-31
