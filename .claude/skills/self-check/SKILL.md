---
name: "self-check"
description: "Mid-execution self-monitoring checkpoint (Ralph Wiggum Loop): Detect warning signs (drift, confusion, gold-plating), course-correct before completion. Mandatory at 25% progress and before delegation."
version: "1.0.0"
type: "quality-gate"
category: "self-monitoring"
---

# Self-Check: Self-Observation Protocol

Invoke mid-execution checkpoint to detect warning signs and course-correct. Prevents drift, confusion, and wasted effort through systematic self-observation.

## Instructions

**When to Invoke (Mandatory):**
- 25% task completion (early warning)
- Before delegating tasks to other agents
- After loading 5+ directives or large documents
- When 3+ ⚠️ symbols appear within 10 minutes
- Before marking task complete (final alignment check)

**Optional Invocations:**
- Every 15-20 minutes during long tasks
- When detecting internal confusion
- When switching reasoning modes frequently
- Before requesting human guidance

---

## Checkpoint Protocol

### Step 1: Enter Meta-Mode

```markdown
[mode: current-mode → meta]
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

```markdown
## Self-Observation Checklist

### Execution State
- **Current task:** [one-line description]
- **Original goal:** [from initial prompt or task file]
- **Progress:** [steps completed / total steps]
- **Time budget:** [elapsed / estimated]

### Warning Signs (Mark all that apply)
- [ ] Repetitive patterns: Am I doing the same thing multiple times?
- [ ] Goal drift: Have I lost sight of the original objective?
- [ ] Speculation: Am I guessing instead of validating?
- [ ] Verbosity: Are outputs becoming unclear or too long?
- [ ] Scope creep: Am I adding work not requested?
- [ ] Directive violations: Am I ignoring established protocols?
- [ ] Confusion: Do I understand what I'm doing next?
- [ ] Mode misuse: Is my reasoning mode appropriate?

### Integrity Symbols
- ❗️ Critical issues: [list or "none detected"]
- ⚠️ Warning signs: [list or "none detected"]
- ✅ Alignment status: [confirmed/uncertain/violated]
```

### Step 4: Pattern Recognition

**If warnings detected, identify pattern:**

| Pattern | Symptoms | Required Action |
|---------|----------|-----------------|
| **Drift** | Scope creep, added features | Revert to original scope |
| **Confusion** | Multiple ⚠️, uncertainty | Stop and request clarification |
| **Gold-plating** | Over-engineering, future features | Remove unnecessary work |
| **Mode misuse** | Wrong reasoning mode | Switch to appropriate mode |
| **Repetition** | Same actions multiple times | Change approach |
| **Speculation** | Guessing without validation | Validate assumptions |

### Step 5: Course Correction

**If ✅ Aligned:**
- Resume previous mode
- Continue execution
- Document alignment confirmation

**If ⚠️ Warnings:**
- Apply corrections from pattern recognition table
- Document corrective actions
- Resume with adjusted approach

**If ❗️ Critical:**
- STOP execution immediately
- Request human guidance
- Document issue clearly

### Step 6: Exit Meta-Mode

```markdown
[mode: meta → previous-mode]

**Checkpoint Result:** ✅ Aligned / ⚠️ Corrected / ❗️ Blocked

**Corrective Actions Taken:** [List or "none needed"]

**Resuming:** [Next specific action]
```

---

## Example Checkpoint

```markdown
🔄 **Ralph Wiggum Loop Checkpoint**

[Timestamp: 2026-02-06T14:30:00Z]
[Current Mode: /analysis-mode]
[Task Progress: 25% complete, Step 3 of 12]
[Elapsed Time: 45 minutes]

## Self-Observation Checklist

### Execution State
- **Current task:** Implement GenericYAMLAdapter with ENV support
- **Original goal:** Create adapter that reads tool config from YAML
- **Progress:** 3/12 steps (base class done, env expansion pending)
- **Time budget:** 45min elapsed / 5h estimated (18% time used)

### Warning Signs
- [x] Scope creep: Added caching mechanism not in requirements
- [ ] Repetitive patterns: No
- [ ] Goal drift: No
- [ ] Speculation: No
- [ ] Verbosity: No
- [ ] Directive violations: No
- [ ] Confusion: No
- [ ] Mode misuse: No

### Integrity Symbols
- ❗️ Critical issues: none detected
- ⚠️ Warning signs: Scope creep detected (caching not requested)
- ✅ Alignment status: UNCERTAIN

---

**Pattern Identified:** Gold-plating
- **Symptom:** Added caching for "future performance"
- **Root cause:** Anticipated need without validation

**Corrective Action:**
1. Remove caching code (not in requirements)
2. Add TODO comment if needed later
3. Focus on core adapter functionality only
4. Follow Directive 020 (Locality of Change)

**Result:** ⚠️ Corrected

---

[mode: meta → analysis]

**Checkpoint Result:** ⚠️ Corrected - Removed gold-plating

**Corrective Actions Taken:**
- Deleted 45 lines of caching code
- Simplified to core requirements only
- Added TODO for future consideration

**Resuming:** Implement ENV variable expansion (Step 4)
```

---

## Warning Pattern Guide

### 1. Goal Drift
**Symptoms:**
- Original goal unclear or forgotten
- Working on tangentially related items
- "While I'm here..." changes

**Correction:**
- Re-read original task description
- Compare current work to acceptance criteria
- Remove work not in scope

### 2. Confusion
**Symptoms:**
- Multiple ⚠️ markers accumulating
- Uncertainty about next steps
- Conflicting constraints

**Correction:**
- STOP immediately
- Request clarification
- Do NOT proceed on assumptions

### 3. Gold-Plating
**Symptoms:**
- Adding features "for future use"
- Over-engineering solutions
- Implementing before needed

**Correction:**
- Remove extra features
- Focus on current requirements
- Add TODO if truly valuable later

### 4. Repetition
**Symptoms:**
- Attempting same approach multiple times
- Not learning from failures
- No progress despite effort

**Correction:**
- Change approach completely
- Request help or guidance
- Consider different tool/technique

### 5. Speculation
**Symptoms:**
- Guessing without validation
- "Probably" or "should work" language
- No verification of assumptions

**Correction:**
- Validate every assumption
- Write test to verify behavior
- Use tools to check facts

### 6. Mode Misuse
**Symptoms:**
- Creative mode for technical analysis
- Analysis mode for writing/brainstorming
- Unclear which mode is active

**Correction:**
- Switch to appropriate mode
- Document mode transition
- Stay in mode until natural boundary

---

## Integration with Workflow

### During /iterate

```
Agent (Backend-Dev):
  Step 1-3: Implement feature...

  [At 25% completion]
  🔄 Self-Check Checkpoint
    ✅ Aligned - Continue

  Step 4-6: Continue implementation...

  [Before delegating to Frontend]
  🔄 Self-Check Checkpoint
    ⚠️ Warning: Scope creep detected
    Corrective action: Removed extra validation
    ✅ Corrected - Ready to delegate

  Step 7: Delegate UI task...
```

### Before Major Decisions

```
Agent: About to make significant architectural change...

🔄 Self-Check Checkpoint
  ❗️ CRITICAL: Change not aligned with ADR-025
  Action: STOP - Request architect review
  Status: BLOCKED pending review
```

### Final Alignment Check

```
Agent: Feature implementation complete...

🔄 Final Self-Check Checkpoint
  ✅ All requirements met
  ✅ No scope creep
  ✅ Tests passing
  ✅ Work log created
  Status: ALIGNED - Ready to complete
```

---

## Benefits

**Prevents Wasted Effort:**
- Catches drift early (25% checkpoint)
- Corrects course before major investment
- Avoids "throw away and restart" scenarios

**Maintains Quality:**
- Detects directive violations
- Ensures alignment with requirements
- Prevents over-engineering

**Improves Communication:**
- Documents decision points
- Makes reasoning visible
- Creates audit trail

**Reduces Rework:**
- Catches issues before completion
- Validates assumptions early
- Prevents late-stage corrections

---

## Common Patterns

### Healthy Checkpoint (✅)
```
🔄 Checkpoint at 25%
  ✅ On track, aligned
  Resume: Continue Step 4
```

### Warning Detected (⚠️)
```
🔄 Checkpoint at 50%
  ⚠️ Scope creep detected
  Corrective action: Removed feature X
  Resume: Refocus on core requirements
```

### Critical Issue (❗️)
```
🔄 Checkpoint at pre-delegation
  ❗️ Violates ADR-029
  Action: STOP - Request architect review
  Status: BLOCKED
```

---

## Anti-Patterns

❌ **Skipping mandatory checkpoints:**
- "I'm almost done, no need to check"
- Results in wasted effort on wrong path

❌ **Ignoring warnings:**
- "I'll fix it later"
- Compounds problems, harder to correct

❌ **Superficial checks:**
- "Everything looks fine"
- Defeats purpose of systematic observation

❌ **Over-checking:**
- Checkpoint every 5 minutes
- Wastes time, disrupts flow

✅ **Correct usage:**
- Follow mandatory checkpoint schedule
- Take warnings seriously
- Course-correct immediately
- Resume work promptly after alignment

---

## Related Skills

- `/iterate` - Uses self-check at batch milestones
- `/review` - Similar systematic evaluation
- `/status` - Planning-level health check

## References

- **Directive 024:** `.github/agents/directives/024_self_observation_protocol.md`
- **Approach:** `.github/agents/approaches/ralph-wiggum-loop.md` (detailed pattern)
- **Directive 020:** `.github/agents/directives/021_locality_of_change.md` (Scope management)
