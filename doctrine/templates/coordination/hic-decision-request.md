---
type: decision_request
agent: [agent-name]
date: YYYY-MM-DD
urgency: [low, medium, high, blocking]
context: Brief one-sentence description of decision needed
status: pending
---

# Decision Request: [Title]

## Context

[Why this decision is needed - provide full background. Explain:]
- What you're trying to accomplish
- Why this decision point was reached
- What constraints exist
- What's at stake with each choice

---

## Question

[Specific decision to be made - be precise and unambiguous]

**Example:** "Should we use REST or GraphQL for the new mobile API?"

---

## Options

### Option A: [Name]

**Description:**  
[Brief description of this option]

**Pros:**
- [Pro 1 - be specific]
- [Pro 2]
- [Pro 3]

**Cons:**
- [Con 1 - be specific]
- [Con 2]
- [Con 3]

**Implications:**
- [What changes if we choose this]
- [Impact on existing systems]
- [Effort estimate]
- [Risk assessment]
- [Long-term maintenance considerations]

---

### Option B: [Name]

**Description:**  
[Brief description of this option]

**Pros:**
- [Pro 1 - be specific]
- [Pro 2]
- [Pro 3]

**Cons:**
- [Con 1 - be specific]
- [Con 2]
- [Con 3]

**Implications:**
- [What changes if we choose this]
- [Impact on existing systems]
- [Effort estimate]
- [Risk assessment]
- [Long-term maintenance considerations]

---

### Option C: [Name] (if applicable)

**Description:**  
[Brief description of this option]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Implications:**
- [What changes]
- [Effort estimate]
- [Risks]

---

## Comparison Matrix

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| **Performance** | [Rating/notes] | [Rating/notes] | [Rating/notes] |
| **Complexity** | [Rating/notes] | [Rating/notes] | [Rating/notes] |
| **Maintenance** | [Rating/notes] | [Rating/notes] | [Rating/notes] |
| **Cost** | [Rating/notes] | [Rating/notes] | [Rating/notes] |
| **Time to implement** | [Estimate] | [Estimate] | [Estimate] |
| **Risk level** | [Low/Med/High] | [Low/Med/High] | [Low/Med/High] |

---

## Agent Recommendation

**Recommended:** Option [X]

**Rationale:**  
[Why agent recommends this option. If no strong preference, explain why options are balanced and what factors should drive the decision.]

**Confidence level:** [Low/Medium/High]

---

## Related Work

**Specifications:**
- [Link to relevant spec]

**ADRs:**
- [ADR-XXX: Related decision](link)

**Tasks:**
- [Task ID: Related task](link)

**Prior Discussions:**
- [Link to Slack thread, PR comments, etc.]

**Industry Precedent:**
- [Examples of similar decisions in other projects]

---

## Timeline

**Urgency:** [low, medium, high, blocking]

**Decision needed by:** YYYY-MM-DD

**Impact if delayed:**  
[What happens if decision is delayed - blocked work, missed deadlines, etc.]

**Current workaround:**  
[If any temporary workaround in place, describe it and its limitations]

---

## Decision

<!-- HiC fills this in -->

**Chosen:** [Option X]

**Rationale:**  
[Why this option was chosen]

**Additional guidance:**  
[Any clarifications, modifications, or additional instructions]

**Conditions/Constraints:**  
[Any conditions under which this decision applies or should be revisited]

**Date:** YYYY-MM-DD

**Follow-up required:**  
- [ ] Create implementation task
- [ ] Update specifications
- [ ] Create ADR documenting decision
- [ ] Notify stakeholders
- [ ] Other: [Specify]
