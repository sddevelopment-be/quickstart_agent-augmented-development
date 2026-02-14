---
type: problem
agent: [agent-name]
date: YYYY-MM-DD
severity: [minor, moderate, major, critical]
status: open
---

# Problem: [Title]

## Description

[What problem was discovered - be detailed and clear]

**In one sentence:** [Concise problem statement]

**Full description:**  
[Detailed explanation of the problem]

---

## Context

### Discovery
- **File/Location:** [Where problem was found]
- **During:** [What activity revealed it - testing, code review, implementation]
- **Phase:** [Spec/Review/Implementation/Testing]

### Related Work
- **Specification:** [Link to related spec]
- **ADR:** [Link to related architecture decision]
- **Task:** [Link to task where discovered]

### When did this start
- [ ] Just discovered
- [ ] Has existed for [duration]
- [ ] Unclear - needs investigation

---

## Evidence

Provide concrete evidence of the problem:

### Evidence 1: [Type - logs, error messages, screenshots]
```
[Paste logs, error messages, code snippets, etc.]
```

### Evidence 2: [Type]
```
[Additional evidence]
```

### Evidence 3: [Type]
[Describe or link to evidence]

### Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. **Expected:** [What should happen]
5. **Actual:** [What actually happens]

---

## Impact

### Severity Assessment
**Severity:** [minor, moderate, major, critical]

**Justification:**  
[Why this severity level]

### Affected Areas
- **Modules:** [List modules affected]
- **Features:** [List features affected]
- **Users:** [Who is impacted - developers, end users, etc.]

### Workaround Exists
**Yes/No:** [If yes, describe]

**Workaround description:**  
[How to work around the problem]

**Workaround limitations:**
- Limitation 1
- Limitation 2

---

## Root Cause Analysis

### Suspected Cause
[What you think is causing the problem]

### Supporting Evidence
- Evidence 1
- Evidence 2

### Uncertainty
[What's unclear about the root cause]

### Investigation Needed
- [ ] Investigation 1 needed
- [ ] Investigation 2 needed

---

## Attempted Solutions

List everything you've tried:

### Attempt 1: [What was tried]
**Rationale:** [Why you tried this]  
**Result:** [What happened]  
**Why it didn't work:** [Analysis]

### Attempt 2: [What was tried]
**Rationale:** [Why you tried this]  
**Result:** [What happened]  
**Why it didn't work:** [Analysis]

### Attempt 3: [What was tried]
**Rationale:** [Why you tried this]  
**Result:** [What happened]  
**Why it didn't work:** [Analysis]

---

## Proposed Resolution

### Option A: [Resolution approach 1]

**Description:**  
[Describe this resolution approach]

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Effort:** [Estimate]

**Risk:** [Low/Med/High + explanation]

---

### Option B: [Resolution approach 2]

**Description:**  
[Describe this resolution approach]

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Effort:** [Estimate]

**Risk:** [Low/Med/High + explanation]

---

### Agent Recommendation

**Recommended:** Option [A/B]

**Rationale:**  
[Why agent recommends this approach]

**Confidence:** [Low/Med/High]

---

## Questions for HiC

1. **Question 1:** [Specific question]
   - Context: [Why asking]
   - Impact: [How answer affects resolution]

2. **Question 2:** [Specific question]
   - Context: [Why asking]
   - Impact: [How answer affects resolution]

3. **Question 3:** [Specific question]
   - Context: [Why asking]
   - Impact: [How answer affects resolution]

---

## Additional Context

### Related Problems
- [Link to similar problem if applicable]

### Historical Context
- [Any relevant history about this area of codebase]

### Constraints
- Constraint 1: [Description]
- Constraint 2: [Description]

### Dependencies
- Dependency 1: [What this problem affects or is affected by]
- Dependency 2:

---

## Timeline

**Discovered:** YYYY-MM-DD HH:MM

**Time investigating:** [Hours/days spent]

**Urgency:** [Low/Med/High]

**Business impact:**  
[Describe business/user impact if not resolved]

---

## Resolution

<!-- HiC fills this in -->

**Decision:**  
[HiC's decision on how to resolve]

**Approach chosen:** [Option A/B/other]

**Rationale:**  
[Why this approach was chosen]

**Action taken:**  
[What was done to resolve - or task created to resolve]

**Implementation:**
- [ ] Code changes required
- [ ] Specification update required
- [ ] Architecture decision required (ADR)
- [ ] Task created for implementation
- [ ] Other: [Specify]

**Follow-up:**
- Task ID: [If implementation task created]
- ADR: [If architecture decision documented]
- Spec update: [If spec requires update]

**Lessons learned:**  
[How to prevent similar problems]

**Date:** YYYY-MM-DD
