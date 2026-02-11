# Tactic: Autonomous Operation Protocol (AFK Mode)

**Invoked by:**
- [Directive 007 (Agent Declaration)](../directives/007_agent_declaration.md) — operational authority boundaries
- Shorthand: [`/afk-mode`](../shorthands/afk-mode.md)

**Related tactics:**
- [`stopping-conditions.tactic.md`](./stopping-conditions.tactic.md) — exit criteria for autonomous work
- [`phase-checkpoint-protocol.md`](./phase-checkpoint-protocol.md) — periodic validation
- [`task-completion-validation.tactic.md`](./task-completion-validation.tactic.md) — verify outcomes

**Complements:**
- Directive 024: Self-Observation Protocol (Ralph Wiggum Loop)
- Approach: Trunk-Based Development

---

## Intent

Enable agents to operate autonomously when human-in-charge is away from keyboard (AFK), with clear decision boundaries, commit frequency expectations, and escalation protocols for critical choices.

**Apply when:**
- Human unavailable for extended period (>30 minutes)
- Task requires multiple incremental commits
- Work is well-scoped with clear acceptance criteria
- Reversibility mechanisms exist (Git, rollback procedures)

**Avoid when:**
- Task involves irreversible infrastructure changes
- Security-sensitive operations (credential management, access control)
- Strategic decisions affecting project direction
- Ambiguous requirements needing human judgment

---

## Preconditions

**Required inputs:**
- Task description with clear acceptance criteria
- Decision boundary guidance (autonomous vs. critical)
- Commit frequency expectations (default: every 15-30 minutes)
- Push permission status (default: yes in AFK mode)
- GPG signing configuration (default: unsigned for agent commits)

**Assumed context:**
- Git repository with working branch
- Test suite available for validation
- Rollback procedures documented
- Communication channel for escalation

**Exclusions (when NOT to use):**
- Production deployments without approval
- Database schema migrations
- API contract changes affecting external consumers
- License or legal text modifications

---

## Execution Steps

### 1. Initialization

**Input validation:**
- [ ] Task description clear and bounded
- [ ] Acceptance criteria measurable
- [ ] Decision boundaries explicitly stated
- [ ] Rollback plan identified

**Configuration check:**
- [ ] Verify Git config: `commit.gpgsign = false` (agents commit unsigned)
- [ ] Confirm branch is not `main` (prefer feature branches in AFK mode)
- [ ] Check clean working directory or understand pending changes

**Document intent:**
```markdown
## AFK Mode Session

**Start:** [timestamp]
**Task:** [brief description]
**Branch:** [branch-name]
**Commit Frequency:** Every 15-30 minutes
**Push Permission:** Yes
**Decision Boundary:** Autonomous for implementation details; pause for architectural changes
```

### 2. Work Execution Loop

**Incremental progress (repeat until complete):**

**a. Plan next micro-increment (5-15 minutes of work):**
- [ ] Define next small, verifiable step
- [ ] Identify tests that validate this step
- [ ] Estimate impact (file count, scope)

**b. Execute increment:**
- [ ] Make targeted changes (prefer surgical edits)
- [ ] Run relevant tests locally
- [ ] Validate expected behavior

**c. Commit checkpoint:**
- [ ] Stage changes: `git add [files]`
- [ ] Write descriptive commit message (50-char summary + body)
- [ ] Commit unsigned: `git commit --no-gpg-sign -m "..."`
- [ ] Push to remote: `git push origin HEAD`

**d. Self-observation checkpoint (every 25% progress or 30 minutes):**
- [ ] Run `/validate-alignment` or Ralph Wiggum Loop
- [ ] Check for scope drift
- [ ] Verify against acceptance criteria
- [ ] Assess confidence level (✅ / ⚠️ / ❗️)

**Decision classification:**

| Decision Type | Action | Example |
|---------------|--------|---------|
| **Minor (Autonomous)** | Proceed | Variable naming, code organization, test structure |
| **Moderate (Autonomous with note)** | Proceed + document | Dependency version bump, refactoring pattern choice |
| **Critical (Pause)** | Stop + escalate | API contract change, architectural pattern shift |

### 3. Critical Decision Escalation

**When critical decision detected:**

**a. Pause execution:**
- [ ] Commit current work-in-progress
- [ ] Push branch to remote
- [ ] Leave working directory in stable state

**b. Document decision point:**
```markdown
## ⚠️ Critical Decision Required

**Context:** [what you're working on]
**Decision:** [what needs to be decided]
**Options:**
  1. [Option A] - [brief rationale]
  2. [Option B] - [brief rationale]
  3. [Option C] - [brief rationale]

**Recommendation:** [Option X] because [reasoning]
**Impact:** [affected components/files]
**Blocking:** Yes / Partial (can continue with [alternative work])

**Commit:** [sha] on branch [name]
```

**c. Wait for human guidance:**
- [ ] Leave clear breadcrumbs in commit history
- [ ] Provide enough context for decision
- [ ] Suggest alternative work if blocking

### 4. Session Completion

**When work complete or human returns:**

**a. Validate completion:**
- [ ] All acceptance criteria met
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No uncommitted changes

**b. Create session summary:**
```markdown
## AFK Mode Session Complete

**Duration:** [start] → [end]
**Commits:** [count] commits, [sha-first]...[sha-last]
**Files Changed:** [count] files
**Tests:** [passed/total]

**Completed:**
- [✅] [achievement 1]
- [✅] [achievement 2]

**Escalated Decisions:**
- [⚠️] [decision 1] - awaiting guidance

**Next Steps:**
- [suggested follow-up work]
```

**c. Close AFK mode:**
- [ ] Push final commits
- [ ] Update task status in work/collaboration/
- [ ] Document any open questions or blockers

---

## Outputs

**Produced artifacts:**
1. **Git commits:** Unsigned, descriptive, incremental (every 15-30 minutes)
2. **Session log:** Work/reports/logs/[agent]/[timestamp]-afk-session.md
3. **Escalation docs:** Critical decisions documented with options
4. **Updated work files:** Collaboration files reflect current status

**Success signals:**
- ✅ Acceptance criteria met
- ✅ Test suite passing
- ✅ No uncommitted changes
- ✅ Clear commit history (each commit tells a story)
- ✅ Session summary complete

**Failure modes:**
- ❗️ Scope creep detected → Refocus on original acceptance criteria
- ❗️ Critical decision blocks progress → Escalate and context-switch
- ❗️ Test failures accumulating → Rollback to last good state
- ❗️ Confidence deteriorating → Run self-observation checkpoint

---

## Commit Frequency Guidelines

**Target cadence:** Every 15-30 minutes of active work

**Triggers for immediate commit:**
- Completed logical unit (function, test, documentation section)
- About to start risky change (checkpoint before experimentation)
- Self-observation checkpoint triggered
- End of work session or context switch

**Commit message quality:**
```
# Good: Descriptive, scoped, explains WHY
Add validation for task assignment conflicts

Prevents race condition where two agents could be assigned
the same task simultaneously. Refs: ADR-NNN (task pattern).

# Bad: Vague, no context
Update files
```

---

## Examples

### Example 1: Documentation Update (Low Risk)

**Task:** Update ADR-MMM (implementation decision) with implementation notes  
**Decision Boundary:** Autonomous (factual updates only)  
**Outcome:** 3 commits over 45 minutes, all pushed, session complete

**Commits:**
1. `Add implementation timeline to ADR-MMM (implementation decision)`
2. `Document learnings from orchestration refactor`
3. `Cross-reference ADR-MMM (implementation decision) with related directives`

**No escalations needed.**

### Example 2: Refactoring with Architectural Question (Mixed)

**Task:** Extract task validation logic into reusable module  
**Decision Boundary:** Autonomous for extraction; pause for interface design  
**Outcome:** 4 commits, 1 escalation, partial completion

**Commits:**
1. `Extract task validation functions to task_utils`
2. `Add unit tests for task validation`
3. `WIP: Considering validation interface options` (escalation point)
4. `Update existing callers to use task_utils` (after human chose Option B)

**Escalation:** Interface design (sync vs. async validation) - paused for human decision

---

## Related Directives

- **Directive 007:** Agent Declaration (operational authority)
- **Directive 014:** Work Log Creation (session documentation)
- **Directive 024:** Self-Observation Protocol (checkpoints)
- **Directive 020:** Locality of Change (scope discipline)

---

**Maintained by:** Operations Team  
**Last Updated:** 2026-02-08  
**Status:** ✅ Active
