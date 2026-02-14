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

[What is blocking progress - be specific and clear]

**In one sentence:** [Concise description of the blocker]

**Details:**  
[More detailed explanation of what's needed and why]

---

## Impact

### Blocked Tasks
- Task ID: [Task 1 description]
- Task ID: [Task 2 description]
- Initiative: [If blocking entire initiative]

### Estimated Delay
**If not resolved:** [Duration - hours/days/weeks]

**Impact severity:**
- [ ] Critical - Blocks all progress
- [ ] High - Blocks major work stream
- [ ] Medium - Blocks one task, others can proceed
- [ ] Low - Minor inconvenience, workaround exists

### Workaround Available
**Yes/No:** [If yes, describe workaround and limitations]

---

## What's Needed

[Specific action HiC must take - be explicit and actionable]

**Examples:**
- "Provide AWS S3 access key and secret for staging bucket `myapp-staging-uploads`"
- "Review and merge PR #123"
- "Confirm if we can use GPL-licensed dependency X"
- "Grant database access to staging environment"

**Acceptance criteria:**
[How will we know the blocker is resolved?]

---

## Context

**Why is this needed:**  
[Explain why this external resource/action is necessary]

**How we got here:**  
[Brief history - what led to this blocker]

**Dependencies:**  
[What other work depends on this]

---

## Attempted Solutions

List everything you've tried to resolve this:

1. **Attempt 1:** [What was tried]
   - **Result:** [What happened]
   - **Why it didn't work:** [Explanation]

2. **Attempt 2:** [What was tried]
   - **Result:** [What happened]
   - **Why it didn't work:** [Explanation]

3. **Attempt 3:** [What was tried]
   - **Result:** [What happened]
   - **Why it didn't work:** [Explanation]

---

## Workaround

**Status:** [In place / Not available / Partial]

**Description:**  
[If any workaround is in place, describe it]

**Limitations:**
- Limitation 1
- Limitation 2

**Risks of workaround:**
- Risk 1
- Risk 2

**When to remove workaround:**  
[Criteria for when workaround should be removed]

---

## Timeline

**Blocker created:** YYYY-MM-DD HH:MM

**Blocking since:** [How long has this been blocking work]

**Urgency justification:**  
[Why this urgency level - what's the business/technical impact]

**SLA/Deadline:**  
[If any deadline or SLA applies]

---

## Related Work

**Task files:**
- [Link to blocked task YAML]

**Specifications:**
- [Link to relevant spec]

**ADRs:**
- [Link to relevant architecture decision]

**Prior blockers:**
- [Link to similar blocker if this is recurring]

---

## Agent Status

**Current status:** [Describe what agent is doing while blocked]

**Alternatives being pursued:**  
[Other tasks agent is working on while waiting]

**Will resume when:**  
[Criteria for resuming blocked work]

---

## Resolution

<!-- HiC fills this in when resolved -->

**Action taken:**  
[Description of what HiC did to resolve blocker]

**Resolution details:**
- Date: YYYY-MM-DD
- Method: [How blocker was resolved]
- Resources provided: [What was provided to agent]
- Access granted: [If applicable]
- Documentation: [If credentials/access, where documented]

**Verification:**
- [ ] Agent notified
- [ ] Task unfrozen
- [ ] Blocker tested and confirmed resolved
- [ ] Documentation updated

**Follow-up tasks:**  
[Task IDs created, if any]

**Lessons learned:**  
[How to prevent similar blockers in future]
