# 015 Store Prompts Directive

Purpose: Define optional practice for documenting original task prompts with SWOT analysis to help users improve prompt quality and effectiveness over time.

## 1. When to Store Prompts

Agents MAY store prompt documentation when:
- Completing complex or novel orchestration tasks
- Encountering ambiguous or unclear task requirements
- Identifying patterns in prompt quality that impact execution
- Requested explicitly by human stakeholders
- The task required significant interpretation or clarification

Agents SHOULD store prompt documentation when:
- The prompt could serve as a learning example for future task creators
- Significant improvements to the prompt structure are identified
- The task execution revealed gaps in the original prompt
- The prompt represents a new pattern or approach worth documenting

## 2. Prompt Documentation Location

All prompt documentation MUST be stored in:
```
work/logs/prompts/YYYY-MM-DDTHHMM-<agent>-<slug>-prompt.md
```

**Naming Convention:**
- `YYYY-MM-DD`: Date in ISO 8601 format
- `THHMM`: Time in 24-hour format
- `<agent>`: Agent name (lowercase, hyphenated)
- `<slug>`: Short description matching task slug (lowercase, hyphenated, max 50 chars)
- `-prompt`: Suffix to identify as prompt documentation

**Example:** `work/logs/prompts/2025-11-23T1921-synthesizer-done-work-assessment-prompt.md`

## 3. Prompt Documentation Structure

Prompt documentation MUST include the following sections:

### Required Sections

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
- etc.

### Weaknesses

What could be improved in the prompt:
- Ambiguous terminology
- Missing success criteria
- Unclear handoff expectations
- Undefined metrics
- etc.

### Opportunities

How the prompt could be enhanced:
- Add explicit deliverable list
- Include metric definitions
- Specify handoff guidance
- Provide example outputs
- etc.

### Threats

What could go wrong with this prompt pattern:
- Misinterpretation risk areas
- Scope creep potential
- Context overload
- Conflicting requirements
- etc.

---

## Suggested Improvements

### Version 2.0: Enhanced Prompt

```
<improved version of the prompt incorporating SWOT findings>
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

[Continue for all major improvements]

---

## Pattern Recognition

### Effective Prompt Elements

List elements that made this prompt effective:
1. Specific file paths reduced ambiguity
2. Step-by-step process guided execution
3. etc.

### Anti-Patterns to Avoid

List elements that caused confusion or inefficiency:
1. ❌ Vague goals without specifics
2. ❌ Missing context about importance
3. etc.

---

## Recommendations for Similar Prompts

For [task type] tasks, future prompts should:
1. Include explicit success criteria in prompt text
2. Define all custom metrics upfront
3. State handoff expectations clearly
4. etc.

---

**Documented by:** <agent-name>
**Date:** YYYY-MM-DDTHH:MM:SSZ
**Purpose:** Future reference for prompt improvement and task creation best practices
**Related:** Task <task-id> (completed)
```

### Optional Sections

- **Retrospective Analysis:** Post-execution assessment of prompt effectiveness
- **Token Efficiency Impact:** How prompt clarity affected token usage
- **Execution Comparison:** Differences between prompt intent and actual execution
- **User Feedback:** Comments or guidance from human stakeholders
- **Alternative Formulations:** Other ways the prompt could have been structured

## 4. SWOT Analysis Guidelines

### Strengths

Focus on what made the prompt effective:
- **Clarity:** Unambiguous language, specific references
- **Completeness:** All necessary information provided
- **Structure:** Logical organization and flow
- **Context:** Appropriate situational awareness
- **Actionability:** Clear steps and expected outcomes

### Weaknesses

Identify gaps or areas of confusion:
- **Ambiguity:** Terms or concepts requiring interpretation
- **Missing Information:** Gaps in requirements or context
- **Complexity:** Unnecessarily complicated structure
- **Redundancy:** Duplicated or conflicting information
- **Assumptions:** Unstated expectations or prerequisites

### Opportunities

Suggest concrete improvements:
- **Enhance Clarity:** Add definitions, examples, or specifications
- **Improve Structure:** Reorganize for better flow
- **Add Context:** Include rationale or situational awareness
- **Specify Metrics:** Define success criteria explicitly
- **Provide Examples:** Show desired output format

### Threats

Highlight risks in the current prompt pattern:
- **Misinterpretation:** Where agent might misunderstand intent
- **Scope Creep:** Vague boundaries leading to over-delivery
- **Context Overload:** Too much information reducing focus
- **Conflicting Guidance:** Contradictory requirements
- **Dependency Gaps:** Missing prerequisite information

## 5. Improvement Guidelines

### Version Numbering

- **Original:** Version 1.0 (the prompt as received)
- **Enhanced:** Version 2.0 (suggested improvements incorporated)
- **Further Iterations:** Version 2.1, 2.2, etc. for minor refinements

### Improvement Categories

**Clarity Enhancements:**
- Replace vague terms with specific definitions
- Add file paths or exact references
- Include example outputs

**Completeness Additions:**
- Explicit success criteria
- Deliverable specifications
- Metric definitions

**Structure Improvements:**
- Logical section ordering
- Clear process steps
- Visual hierarchy

**Context Enrichment:**
- Situational awareness (phase, dependencies)
- Rationale for task importance
- Audience specification

### Impact Assessment

For each improvement, specify:
- **Clarity Impact:** How much ambiguity is reduced (High/Medium/Low)
- **Efficiency Impact:** Estimated token or time savings
- **Quality Impact:** How execution quality improves
- **Reusability Impact:** How well it transfers to similar tasks

## 6. Pattern Recognition Guidelines

### Identifying Effective Patterns

Look for prompt elements that:
- Reduced interpretation time
- Eliminated back-and-forth clarification
- Enabled fast execution
- Produced high-quality results
- Required minimal context loading

### Identifying Anti-Patterns

Look for prompt elements that:
- Caused confusion or delays
- Required external file consultation
- Led to misaligned execution
- Produced incomplete results
- Increased token usage unnecessarily

### Pattern Categorization

**By Task Type:**
- Meta-analysis prompts
- Implementation prompts
- Documentation prompts
- Coordination prompts
- Review/audit prompts

**By Effectiveness:**
- High clarity (minimal interpretation needed)
- Medium clarity (some interpretation required)
- Low clarity (significant interpretation or clarification needed)

## 7. Usage Guidelines

### For Agents

**After Task Completion:**
1. If task execution revealed prompt issues, consider documenting
2. Focus on SWOT analysis over complaints
3. Provide specific, actionable improvements
4. Include concrete examples in enhanced version

**Document When:**
- Prompt required significant interpretation
- Multiple clarifications were needed
- Better structure would improve future similar tasks
- Novel pattern worth preserving as example

**Skip When:**
- Prompt was clear and complete
- Task was routine with no insights
- Time constraints prevent thorough analysis

### For Task Creators (Humans)

**Using Prompt Documentation:**
1. Review prompt documentation in `work/logs/prompts/`
2. Compare original vs enhanced versions
3. Identify patterns in effective prompts
4. Apply improvements to future task creation

**Learning from SWOT:**
- Strengths → Preserve these patterns
- Weaknesses → Avoid these patterns
- Opportunities → Apply these improvements
- Threats → Watch for these risks

### For Framework Maintainers

**Aggregate Insights:**
1. Collect prompt documentation across tasks
2. Extract common strengths and weaknesses
3. Build prompt template library
4. Update task creation guidelines

**Continuous Improvement:**
- Track prompt quality trends over time
- Identify recurring anti-patterns
- Share best practices with community
- Evolve prompt templates based on learnings

## 8. Integration with Work Logs

Prompt documentation complements but does not replace work logs:

**Work Log (Directive 014):**
- Documents what agent did and why
- Focuses on execution and outcomes
- Required for orchestrated tasks

**Prompt Documentation (Directive 015):**
- Documents what human asked and how to improve
- Focuses on request quality and clarity
- Optional but recommended for learning

Both should reference each other:
- Work log: "See prompt documentation for original request analysis"
- Prompt doc: "See work log for execution details"

## 9. Example Prompt Documentation

See: `work/logs/prompts/2025-11-23T1921-synthesizer-done-work-assessment-prompt.md` (reference implementation)

## 10. Validation

Prompt documentation SHOULD:
- Include verbatim copy of original prompt
- Provide balanced SWOT analysis (not just criticism)
- Offer concrete, actionable improvements
- Specify impact of suggested changes
- Follow naming convention
- Be committed to Git for future reference

Prompt documentation SHOULD NOT:
- Criticize the task creator personally
- Focus only on negatives
- Provide vague suggestions ("make it better")
- Duplicate work log content
- Be created for trivial or routine tasks

## 11. Benefits

### For Individual Agents

- Learn from experience
- Improve interpretation skills
- Build pattern recognition
- Reduce clarification overhead

### For Task Creators

- Improve prompt writing skills
- Understand agent perspective
- Create more effective tasks
- Reduce execution errors

### For Framework

- Build prompt template library
- Identify systemic issues
- Evolve best practices
- Improve task success rates

## 12. Non-Compliance

Since prompt documentation is optional (MAY/SHOULD):
- Agents are not penalized for skipping it
- Recommended but not enforced
- Encouraged for learning tasks
- Human reviewers can request if valuable

---

**Directive Status:** Optional (MAY/SHOULD)  
**Applies To:** All agents handling orchestrated tasks  
**Dependencies:** Directive 014 (Work Log Creation)  
**Version:** 1.0.0  
**Last Updated:** 2025-11-23
