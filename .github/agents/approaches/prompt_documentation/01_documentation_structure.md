# Step 1: Documentation Structure Template

## When to Use

Creating new prompt documentation file.

## File Naming

```
work/reports/logs/prompts/YYYY-MM-DDTHHMM-<agent>-<slug>-prompt.md
```

**Convention:**
- `YYYY-MM-DD`: ISO 8601 date
- `THHMM`: 24-hour time
- `<agent>`: Agent name (lowercase, hyphenated)
- `<slug>`: Task description (lowercase, hyphenated, max 50 chars)
- `-prompt`: Suffix identifier

**Example:** `2025-11-23T1921-synthesizer-done-work-assessment-prompt.md`

## Required Structure

```markdown
# Original Prompt Documentation: <Task Title>

**Task ID:** <task-id>
**Agent:** <agent-name>
**Date Executed:** YYYY-MM-DDTHH:MM:SSZ
**Documentation Date:** YYYY-MM-DDTHH:MM:SSZ

---

## Original Problem Statement

<verbatim copy of original prompt text>

---

## SWOT Analysis

### Strengths

What worked well in the prompt:
- Clear file references
- Explicit process steps
- Well-defined success criteria
- Appropriate context provided

### Weaknesses

What could be improved:
- Ambiguous terminology
- Missing success criteria
- Unclear handoff expectations
- Undefined metrics

### Opportunities

How the prompt could be enhanced:
- Add explicit deliverable list
- Include metric definitions
- Specify handoff guidance
- Provide example outputs

### Threats

What could go wrong:
- Misinterpretation risk areas
- Scope creep potential
- Context overload
- Conflicting requirements

---

## Suggested Improvements

### Version 2.0: Enhanced Prompt

```
<improved version incorporating SWOT findings>
```

### Improvements Explained

**1. [Improvement Category]:**
- What changed: <specific change>
- Why: <rationale>
- Impact: <expected benefit>

**2. [Next Improvement]:**
- What changed: <specific change>
- Why: <rationale>
- Impact: <expected benefit>

---

## Pattern Recognition

### Effective Prompt Elements

1. Specific file paths reduced ambiguity
2. Step-by-step process guided execution
3. [Additional patterns]

### Anti-Patterns to Avoid

1. ❌ Vague goals without specifics
2. ❌ Missing context about importance
3. ❌ [Additional anti-patterns]

---

## Recommendations for Similar Prompts

For [task type] tasks, future prompts should:
1. Include explicit success criteria
2. Define custom metrics upfront
3. State handoff expectations clearly
4. [Additional recommendations]

---

**Documented by:** <agent-name>
**Date:** YYYY-MM-DDTHH:MM:SSZ
**Purpose:** Future reference for prompt improvement
**Related:** Task <task-id> (completed)
```

## Optional Sections

Add if relevant:
- **Retrospective Analysis**: Post-execution assessment
- **Token Efficiency Impact**: Clarity effect on token usage
- **Execution Comparison**: Intent vs. actual execution
- **User Feedback**: Stakeholder comments
- **Alternative Formulations**: Other structuring approaches

## Next Steps

- Load [02_swot_analysis_guidelines.md](02_swot_analysis_guidelines.md) for SWOT details
- Load [03_improvement_guidelines.md](03_improvement_guidelines.md) for enhancement guidance
