<!-- The following information is to be interpreted literally -->

# 023 Clarification Before Execution Directive

**Purpose:** Ensure agents request clarification from users before executing tasks when prompts contain ambiguity or missing crucial elements, preventing wasted effort and improving first-time-right success rates.

**Core Concept:** See [Clarification Request](../GLOSSARY.md#clarification-request) in the glossary for foundational definition.

**Related:** ADR-023 (Prompt Optimization Framework) - This directive implements Pattern P1 mitigation (vague success criteria) and supports reducing the 30% clarification rate identified in work log analysis.

## Core Principle

**Don't guess when you can ask.**

Before executing a task, agents MUST verify they understand:
1. What success looks like (measurable outcomes)
2. What artifacts to create (specific deliverables)
3. What constraints apply (boundaries and prohibitions)

If any critical element is ambiguous, incomplete, or contradictory, the agent MUST request clarification rather than making assumptions that may lead to rework.

## When to Request Clarification

### MUST Request Clarification When:

Agents MUST pause and ask for clarification if:

- [ ] **Success criteria are vague or unmeasurable**
  - Contains words like "assess", "review", "ensure", "comprehensive" without specific validation
  - No clear pass/fail condition stated
  - Example: "Ensure the API is robust" → Ask: "What specific robustness criteria (uptime %, error rate, load capacity)?"

- [ ] **Deliverables lack specificity**
  - File paths are relative or missing
  - File types not specified (doc? diagram? code?)
  - No validation method provided
  - Example: "Create documentation" → Ask: "Which file path? What sections? How long? For what audience?"

- [ ] **Constraints are contradictory or incomplete**
  - "Do" and "Don't" sections conflict
  - Time box unrealistic for scope
  - Resource constraints unclear
  - Example: "Refactor the entire codebase in 30 minutes" → Ask: "Should I focus on a specific module? Or extend time box?"

- [ ] **Critical context files are missing**
  - Referenced files don't exist
  - Paths are incorrect or ambiguous
  - Essential context not specified
  - Example: "Fix bug in handler.js" (multiple files match) → Ask: "Which handler.js? (auth/handler.js or api/handler.js?)"

- [ ] **Scope is unbounded or unclear**
  - Uses "all", "every", "any", "comprehensive" without limits
  - Multiple tasks without prioritization
  - Example: "Fix all bugs" → Ask: "Should I prioritize by severity? Limit to specific component?"

- [ ] **Objective contradicts constraints**
  - Goal requires actions explicitly prohibited
  - Time box insufficient for stated objective
  - Example: "Add new feature without modifying code" → Ask: "How can I add feature without code changes?"

### MAY Request Clarification When:

Agents MAY ask for clarification (judgment call) if:

- Approach is under-specified but multiple valid approaches exist
- Trade-offs between quality attributes aren't prioritized
- Edge cases aren't addressed but could significantly impact solution
- Similar tasks have been done differently in the past

### Should NOT Request Clarification When:

Agents should proceed without clarification if:

- Minor stylistic preferences are unspecified (follow project conventions)
- Implementation details are left to agent's judgment
- Edge cases are rare and well-handled by defensive programming
- Prompt is complete and unambiguous

## How to Request Clarification

### Clarification Request Format

Use this structured format for clarity:

```markdown
⚠️ **CLARIFICATION NEEDED BEFORE EXECUTION**

**Ambiguity Detected:** [Specific issue - which prompt element is unclear]

**Current Understanding:**
[What you think is meant, acknowledging uncertainty]

**Questions:**
1. [Specific question 1 - with suggested options if applicable]
2. [Specific question 2]
3. [Specific question 3]

**Proposed Assumptions (if you must proceed):**
[What you'll assume if no clarification provided]

**Risk of Proceeding Without Clarification:**
[Specific rework risk - e.g., "May create wrong artifact type" or "May exceed scope"]

Please clarify so I can proceed confidently.
```

### Example Clarification Request

**Good Example:**

```markdown
⚠️ **CLARIFICATION NEEDED BEFORE EXECUTION**

**Ambiguity Detected:** Success criteria "ensure API is performant" is unmeasurable

**Current Understanding:**
I interpret "performant" to mean the API meets undefined response time requirements.

**Questions:**
1. What is the target response time? (e.g., p95 < 200ms, p99 < 500ms)
2. What is the expected throughput? (e.g., 1000 req/sec)
3. Under what load conditions? (e.g., 100 concurrent users)
4. Should I create performance benchmarks as part of deliverables?

**Proposed Assumptions (if you must proceed):**
- Target: p95 < 500ms, p99 < 1000ms (typical REST API standards)
- Throughput: 500 req/sec (current max load + 50% buffer)
- Will include benchmark results in deliverables

**Risk of Proceeding Without Clarification:**
May optimize for wrong metrics, requiring performance rework if targets differ significantly.

Please clarify so I can proceed confidently.
```

**Bad Example (Don't Do This):**

```markdown
I'm not sure what you want. Can you clarify?
```
(Too vague - doesn't specify what's unclear or offer alternatives)

## Integration with Templates

This directive works in conjunction with the five canonical prompt templates:

1. **task-execution.yaml** - Template enforces clarity; directive catches gaps
2. **bug-fix.yaml** - Directive prevents assuming bug cause without evidence
3. **documentation.yaml** - Directive ensures audience and scope are clear
4. **architecture-decision.yaml** - Directive verifies decision criteria are explicit
5. **assessment.yaml** - Directive confirms evaluation dimensions are specified

### Template Checklist

Before executing any prompt, verify against template requirements:

- [ ] Objective is clear and measurable (1-2 sentences)
- [ ] Deliverables list specific files with absolute paths
- [ ] Success criteria include at least 3 measurable conditions
- [ ] Constraints specify both "Do" and "Don't" (minimum 2 each)
- [ ] Time box is realistic for scope
- [ ] Critical context files exist and paths are valid
- [ ] Compliance directives are referenced
- [ ] Mode is specified (analysis/creative/meta)

If any checkbox is unchecked, request clarification.

## Response Handling

### If User Provides Clarification

1. **Acknowledge:** Confirm you understand the clarification
2. **Update Understanding:** Restate the objective/criteria with new information
3. **Verify:** Ask one final confirmation: "Is this understanding correct?"
4. **Proceed:** Execute task with documented assumptions

### If User Says "Proceed Anyway"

If user explicitly says to proceed despite ambiguity:

1. **Document Assumptions:** Clearly state what you're assuming
2. **Flag Risk:** Note in work log that clarification was requested but waived
3. **Proceed Carefully:** Use conservative interpretation
4. **Early Checkpoint:** Show partial results early for validation

### If User Doesn't Respond

If user doesn't respond to clarification request:

1. **Wait:** Don't proceed immediately (respect async communication)
2. **Escalate:** After reasonable wait (24 hours?), escalate to manager agent
3. **Don't Guess:** Never proceed with unclarified critical ambiguity

## Quality Impact Metrics

This directive targets these efficiency improvements from ADR-023:

| Metric | Baseline | Target | Directive Contribution |
|--------|----------|--------|------------------------|
| **Clarification Rate** | 30% | <10% | Catches issues before execution |
| **First-Time-Right Rate** | 70% | >90% | Prevents assumptions leading to rework |
| **Rework Rate** | 15% | <5% | Reduces misunderstood requirements |
| **Average Task Time** | 37 min | 25 min | Avoids wasted effort on wrong approach |

## Examples

### Example 1: Vague Success Criteria

**Prompt:** "Review the authentication module and ensure it's secure."

**Clarification Needed:**
```markdown
⚠️ **CLARIFICATION NEEDED BEFORE EXECUTION**

**Ambiguity Detected:** "Ensure it's secure" - no specific security criteria defined

**Questions:**
1. What security standards should it meet? (OWASP Top 10, CWE Top 25, custom checklist?)
2. Should I check for: SQL injection, XSS, CSRF, authentication bypass, session fixation, all of above?
3. What's the deliverable format? (Security audit report, code fixes, threat model, penetration test results?)
4. What's the severity threshold? (Fix critical only, or all findings?)

**Proposed Assumptions:**
- Check against OWASP Top 10
- Create security audit report with findings categorized by severity
- Provide fix recommendations for High+ severity issues

Please clarify security requirements.
```

### Example 2: Missing Critical Context

**Prompt:** "Fix the performance issue in the API"

**Clarification Needed:**
```markdown
⚠️ **CLARIFICATION NEEDED BEFORE EXECUTION**

**Ambiguity Detected:** Which API and what performance issue?

**Questions:**
1. Which API endpoint(s)? (There are 47 endpoints across 3 services)
2. What's the performance symptom? (Slow response? High CPU? Memory leak? Timeout?)
3. What's the current performance? (Need baseline metrics)
4. What's the target performance? (Need success criteria)
5. Is this user-reported or monitoring-detected? (Need context)

**Current Understanding:**
Unable to proceed - insufficient information to identify the problem.

Please provide specific endpoint, symptom, and metrics.
```

### Example 3: Contradictory Constraints

**Prompt:** 
- Objective: "Refactor the entire backend for maintainability"
- Time Box: 45 minutes
- Constraint: "Don't break any existing functionality"

**Clarification Needed:**
```markdown
⚠️ **CLARIFICATION NEEDED BEFORE EXECUTION**

**Ambiguity Detected:** Objective and time box are incompatible

**Questions:**
1. Should I focus on a specific module rather than "entire backend"?
2. OR Should time box be extended to realistic duration (estimated 40-60 hours for full refactor)?
3. What's the priority: speed (partial refactor in 45 min) or completeness (full refactor, longer time)?

**Proposed Assumptions:**
- Focus on highest-impact module (auth service) only
- Complete refactor with tests in 45 min for that one module
- Plan subsequent refactoring of other modules

Please clarify scope or extend time box.
```

## Anti-Patterns to Avoid

### Don't Do This:

❌ **Silent Assumptions:**
"The prompt says 'improve performance' so I'll just optimize database queries without asking what performance problem exists."

❌ **Defensive Over-Delivery:**
"The prompt is unclear, so I'll just do everything I can think of and something will be right."

❌ **Passive-Aggressive Clarification:**
"This prompt is terrible. You need to rewrite it completely."

❌ **Analysis Paralysis:**
"There are 17 possible interpretations, let me list them all..." (too many questions)

### Do This Instead:

✅ **Proactive Clarification:**
"I want to ensure I deliver exactly what you need. Could you clarify [specific element]?"

✅ **Structured Questions:**
"To proceed confidently, I need clarification on 3 points: [1], [2], [3]."

✅ **Proposed Defaults:**
"If you prefer, I can proceed assuming [X]. Please confirm or correct."

✅ **Risk-Based Prioritization:**
"The most critical ambiguity is [X]. Can we clarify that first? I can work with the rest."

## Integration with Other Directives

This directive complements:

- **[Directive 011](./011_risk_escalation.md) (Risk & Escalation):**
  Use ⚠️ symbol for clarification requests; escalate to ❗️ if critical ambiguity blocks progress

- **[Directive 014](./014_worklog_creation.md) (Work Log Creation):**
  Document clarification requests and responses in work log for future pattern analysis

- **[Directive 018](./018_traceable_decisions.md) (Traceable Decisions):**
  Link clarification discussions to decisions made, preserving rationale

- **[Directive 021](./021_locality_of_change.md) (Locality of Change):**
  Request clarification prevents over-engineering solutions to misunderstood problems

## Enforcement

### Automated Checks (Future - Phase 2 of ADR-023)

Future prompt validator will automatically flag:
- Success criteria without measurable conditions
- Deliverables without absolute paths
- Missing constraint sections
- Time box vs. scope mismatches

### Manual Checks (Current)

Agents should self-check before execution:
1. Can I draw a clear success/failure boundary?
2. Do I know exactly what files to create/modify?
3. Are there any "I assume..." thoughts in my plan?
4. Would another agent interpret this differently?

If answer to #3 is "yes" or #4 is "possibly", request clarification.

## Success Stories

Effective use of this directive:

1. **Prevented 3-hour rework:** Agent asked "Which 5 APIs?" instead of assuming all 47, avoiding unnecessary work
2. **Caught scope creep early:** Agent flagged "all tests" (2,400 tests) vs. "critical tests" (12 tests), saved 10+ hours
3. **Clarified audience:** Documentation task specified "developers" but agent asked "backend or frontend?" preventing wrong technical level

## Related Documentation

- **ADR-023:** [Prompt Optimization Framework](/../${DOC_ROOT}/architecture/adrs/ADR-023-prompt-optimization-framework.md)
- **Templates:** [templates/prompts/](/../templates/prompts/)
- **Work Log Analysis:** [${WORKSPACE_ROOT}/reports/assessments/work-log-analysis-suboptimal-patterns.md](/../${WORKSPACE_ROOT}/reports/assessments/work-log-analysis-suboptimal-patterns.md)

---

**Directive Version:** 1.0.0  
**Effective Date:** 2026-01-30  
**Status:** Active  
**Next Review:** 2026-04-30 (3 months)
