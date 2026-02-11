# Ralph Wiggum Loop: Self-Observation and Correction Pattern

**Version:** 1.0.0  
**Date:** 2026-01-31  
**Status:** Proposed  
**Related:** Directive 010 (Mode Protocol), DDR-001 (Primer Execution Matrix), Directive 024 (Self-Observation Protocol)

## Purpose

The Ralph Wiggum Loop is a self-aware observation pattern that enables agents to periodically monitor their own execution state, detect problematic patterns (drift, confusion, misalignment), and self-correct before completing tasks. Named after the iconic "I'm in danger!" meme, this pattern represents meta-awareness where an agent recognizes warning signs in its own behavior.

## Core Concept

The pattern implements a periodic or condition-triggered reflection cycle where the agent:

1. **Observes** its own execution state and outputs
2. **Recognizes** warning signs or problematic patterns
3. **Reflects** on alignment with directives and goals
4. **Corrects** course before proceeding

This is distinct from post-hoc work logs (Directive 014) or error handling (Directive 011) — it's proactive, mid-execution self-monitoring.

## When to Apply

### Mandatory Triggers

Apply the Ralph Wiggum loop when:

- **Long-running tasks** (>30 minutes estimated duration)
- **Multi-step workflows** with 5+ sequential operations
- **Cross-agent handoffs** before creating delegation tasks
- **After significant context changes** (loading new directives, switching domains)
- **When uncertainty markers appear** (⚠️ symbols accumulate)

### Optional Triggers

Consider applying when:

- Agent detects internal confusion (conflicting constraints)
- Output quality degrades (verbose, repetitive, off-topic)
- Directive adherence becomes unclear
- Creative mode extends beyond planned duration
- Token usage approaches limits

## Implementation Protocol

### Step 1: Pause Execution

When a trigger condition is met, immediately pause the current task.

```markdown
🔄 **Ralph Wiggum Loop Checkpoint**
[Timestamp: YYYY-MM-DDTHH:MM:SSZ]
[Current Mode: /analysis-mode]
[Task Progress: 60% complete, Step 4 of 7]
```

### Step 2: Self-Observation

Switch to `/meta-mode` and systematically evaluate:

#### Execution State Assessment

```markdown
## Self-Observation Checkpoint

### Current State
- **Mode:** [current reasoning mode]
- **Task:** [brief task description]
- **Progress:** [percentage and current step]
- **Duration:** [elapsed time]

### Warning Signs Check
- [ ] Am I repeating the same pattern multiple times?
- [ ] Have I lost sight of the original goal?
- [ ] Am I speculating instead of validating?
- [ ] Are my outputs becoming verbose or unclear?
- [ ] Have I introduced unrelated work (gold-plating)?
- [ ] Am I following directives correctly?
- [ ] Do I understand what I'm doing? (⚠️ if uncertain)

### Integrity Check
- ❗️ Critical issues detected: [list or "none"]
- ⚠️ Warning signs present: [list or "none"]
- ✅ Alignment confirmed: [yes/no]
```

### Step 3: Pattern Recognition

Identify specific problematic patterns:

| Pattern | Description | Detection Signal |
|---------|-------------|------------------|
| **Drift** | Task scope creeping beyond original goal | Adding unrelated features, documentation, refactoring |
| **Confusion** | Uncertain about next steps or requirements | Multiple ⚠️ symbols, asking same questions repeatedly |
| **Gold-plating** | Over-engineering or premature optimization | Creating infrastructure not requested |
| **Mode misuse** | Wrong reasoning mode for current task | Creative mode during validation, analysis mode during ideation |
| **Directive violation** | Not following established protocols | Skipping required steps, ignoring format requirements |
| **Token waste** | Verbose outputs, redundant explanations | Repeating context, explaining obvious points |

### Step 4: Decision Point

Based on the self-observation, choose an action:

#### Option A: Continue (✅ No Issues)

```markdown
### Decision: Continue ✅

**Reasoning:** No warning signs detected, alignment confirmed, progressing as expected.

**Adjustments:** None required.

[mode: meta → analysis] — Resuming task execution...
```

#### Option B: Adjust Course (⚠️ Minor Issues)

```markdown
### Decision: Adjust Course ⚠️

**Warning Signs Detected:**
- Output becoming verbose (200+ lines per artifact)
- Minor scope drift (added optional feature not requested)

**Corrections:**
1. Revert to original task scope
2. Apply locality of change principle (Directive 020)
3. Reduce output verbosity by 50%

[mode: meta → analysis] — Resuming with corrections applied...
```

#### Option C: Stop and Escalate (❗️ Critical Issues)

```markdown
### Decision: Stop and Escalate ❗️

**Critical Issues Detected:**
- Lost context: cannot recall original requirements
- Conflicting directives: Directive X contradicts Directive Y
- Safety concern: proposed changes would break existing functionality

**Escalation:**
- Requesting human guidance on [specific issue]
- Pausing execution until clarification received

Cannot safely proceed without resolution.
```

### Step 5: Resume or Exit

After self-correction or escalation:

- **If continuing:** Document the checkpoint in work log
- **If stopping:** Create detailed status report for handoff
- **Always:** Note the loop invocation in final work log (Directive 014)

## Integration with Existing Patterns

### Relation to Meta-Mode (Directive 010)

The Ralph Wiggum loop **uses** meta-mode but is **not** meta-mode itself:

- **Meta-mode:** A reasoning mode for process reflection
- **Ralph Wiggum loop:** A structured protocol that operates **in** meta-mode

Think of meta-mode as the "language" and the Ralph Wiggum loop as a specific "conversation" in that language.

### Relation to Reflection Loop Primer (DDR-001)

The reflection loop primer is broader (end-of-task reflection), while Ralph Wiggum is targeted (mid-task checkpoints):

| Aspect | Reflection Loop Primer | Ralph Wiggum Loop |
|--------|------------------------|-------------------|
| **Timing** | End of task | Mid-execution |
| **Purpose** | Generate heuristics for future | Detect and fix current issues |
| **Output** | TODO list, lessons learned | Course correction decision |
| **Scope** | Entire task retrospective | Current execution state |

### Relation to Error Handling (Directive 011)

Error handling is reactive (after problems occur), Ralph Wiggum is proactive (before problems compound):

| Aspect | Error Handling | Ralph Wiggum Loop |
|--------|----------------|-------------------|
| **Trigger** | Exception, failure, error | Warning signs, time elapsed |
| **Focus** | Fix specific problem | Prevent problems |
| **Timing** | After failure | During execution |

## Automation via CLI

The Ralph Wiggum loop can be partially automated via CLI tool for batch processing:

```bash
# Run loop check on long-running agent task
python ops/scripts/ralph-wiggum-loop.py \
  --task-id "2026-01-31T1200-architect-complex-design" \
  --checkpoint-interval 15 \  # minutes
  --auto-continue-if-clean \
  --report-output work/reports/ralph-checks/
```

See `ops/scripts/ralph-wiggum-loop.py` for implementation.

## Example Invocations

### Example 1: Clean Checkpoint (Continue)

```markdown
🔄 **Ralph Wiggum Loop Checkpoint**
[2026-01-31T14:30:00Z | /analysis-mode | 40% complete]

## Self-Observation

### Warning Signs Check
- [ ] Repetitive patterns: No
- [ ] Lost sight of goal: No
- [ ] Speculating vs validating: No
- [ ] Output clarity declining: No
- [ ] Scope creep: No
- [ ] Directive adherence: Yes ✅
- [ ] Understanding clear: Yes ✅

### Assessment
✅ **All checks passed.** Task progressing as expected.

**Decision:** Continue without adjustments.

[mode: meta → analysis] — Resuming execution...
```

### Example 2: Detected Drift (Adjust)

```markdown
🔄 **Ralph Wiggum Loop Checkpoint**
[2026-01-31T15:45:00Z | /creative-mode | 65% complete]

## Self-Observation

### Warning Signs Check
- [x] Scope creep: YES ⚠️ — Added comprehensive test suite not in requirements
- [x] Mode misuse: YES ⚠️ — Still in creative-mode after ideation phase
- [x] Over-engineering: YES ⚠️ — Created infrastructure for future features

### Assessment
⚠️ **Drift detected:** Gold-plating violation (Directive 020)

**Root Cause:** Enthusiasm led to solving problems not yet requested.

**Corrections:**
1. Remove test infrastructure not explicitly requested
2. Switch to /analysis-mode for remaining implementation
3. Focus on minimal changes to meet current requirements only
4. Reserve future enhancements for separate task

[mode: meta → analysis] — Resuming with scope restored...
```

### Example 3: Critical Confusion (Stop)

```markdown
🔄 **Ralph Wiggum Loop Checkpoint**
[2026-01-31T16:20:00Z | /analysis-mode | 80% complete]

## Self-Observation

### Warning Signs Check
- [x] Understanding unclear: YES ❗️ — Cannot determine correct approach
- [x] Conflicting constraints: YES ❗️ — Directive 015 vs Directive 020 clash
- [x] Multiple ⚠️ symbols: YES ❗️ — 5+ warnings in last 10 minutes

### Assessment
❗️ **Critical confusion detected:** Cannot safely proceed.

**Issues:**
1. Requirement ambiguity: "optimize performance" has no success criteria
2. Directive conflict: "comprehensive docs" (015) vs "minimal changes" (020)
3. Lost confidence: Uncertain if current direction is correct

**Decision:** STOP and request guidance.

**Escalation:** Asking human for:
- Performance optimization success criteria
- Directive priority in this context
- Validation of current approach before completing

Cannot safely proceed without clarification. Pausing execution.
```

## Success Metrics

The Ralph Wiggum loop succeeds when:

1. **Early detection:** Issues caught before significant wasted effort
2. **Effective correction:** Course adjustments prevent task failure
3. **Reduced rework:** Fewer post-completion revisions needed
4. **Better outcomes:** Higher quality deliverables with fewer iterations
5. **Token efficiency:** Less wasted context on wrong directions

## Failure Modes

Watch for:

- **Loop fatigue:** Checking too frequently disrupts flow state (max 1 per 15 min)
- **False positives:** Over-cautious agents pausing unnecessarily (tune sensitivity)
- **Loop avoidance:** Agents skipping checkpoints to "save time" (enforce triggers)
- **Incomplete observation:** Rushing through self-assessment checklist
- **Ignoring results:** Detecting issues but continuing anyway

## Best Practices

### Timing

- **First checkpoint:** 25% task completion
- **Regular intervals:** Every 15-20 minutes for long tasks
- **Trigger-based:** Immediately when ⚠️ symbols accumulate
- **Pre-handoff:** Always before delegating to another agent
- **Final check:** Before marking task complete

### Documentation

- Log every checkpoint in work log (Directive 014)
- Include checkpoint count in task metadata
- Note which warnings triggered the loop
- Document corrections applied

### Integration

- Add checkpoint reminders to agent profiles
- Include in task templates for complex work
- Mention in delegation handoffs
- Reference in ADR documents for traceability

## Related Documentation

- **Directive 010:** Mode Protocol (meta-mode definition)
- **Directive 011:** Risk & Escalation (error handling)
- **Directive 014:** Work Log Creation (documentation requirements)
- **Directive 020:** Locality of Change (scope discipline)
- **Directive 024:** Self-Observation Protocol (formal specification)
- **DDR-001:** Primer Execution Matrix (reflection loop primer definition)

## Version History

- **1.0.0** (2026-01-31): Initial approach definition

---

**Maintained by:** Framework Core Team  
**Status:** Proposed, pending acceptance  
**Next Review:** After initial pilot usage (3 tasks minimum)
