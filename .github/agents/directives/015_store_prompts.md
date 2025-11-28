<!-- The following information is to be interpreted literally -->

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

All prompt documentation MUST be stored in [`work/report/logs/prompts`](/work/reports/logs/prompts) following the naming convention:

```
work/reports/logs/prompts/YYYY-MM-DDTHHMM-<agent>-<slug>-prompt.md
```

**Naming Convention:**

- `YYYY-MM-DD`: Date in ISO 8601 format
- `THHMM`: Time in 24-hour format
- `<agent>`: Agent name (lowercase, hyphenated)
- `<slug>`: Short description matching task slug (lowercase, hyphenated, max 50 chars)
- `-prompt`: Suffix to identify as prompt documentation

**Example:** `work/reports/logs/prompts/2025-11-23T1921-synthesizer-done-work-assessment-prompt.md`

## 3. Approach Reference

**CRITICAL:** Load only the step relevant to your current documentation phase to maintain token discipline.

See `.github/agents/approaches/prompt_documentation/README.md` for:

- Complete documentation structure template
- SWOT analysis guidelines
- Improvement suggestion framework
- Pattern recognition methodology

## 4. Quick Procedure

1. Decide if prompt documentation is warranted (see section 1)
2. Load `.github/agents/approaches/prompt_documentation/01_documentation_structure.md` for template
3. Load `.github/agents/approaches/prompt_documentation/02_swot_analysis_guidelines.md` for analysis
4. Load `.github/agents/approaches/prompt_documentation/03_improvement_guidelines.md` for enhancements
5. Load `.github/agents/approaches/prompt_documentation/04_pattern_recognition.md` for patterns
6. Create documentation file in `work/reports/logs/prompts/`
7. Commit to Git for future reference

## 5. Integration with Work Logs

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
- If the Reflection Loop or Transparency primers (ADR-011) surfaced prompt-quality issues, note the primer invocation in the SWOT analysis for traceability.

## 6. Benefits

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

## 7. Example Reference

See: `work/reports/logs/prompts/2025-11-23T1921-synthesizer-done-work-assessment-prompt.md` (reference implementation)

## 8. Validation Criteria

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

## 9. Non-Compliance

Since prompt documentation is optional (MAY/SHOULD):

- Agents are not penalized for skipping it
- Recommended but not enforced
- Encouraged for learning tasks
- Human reviewers can request if valuable

---

**Directive Status:** Optional (MAY/SHOULD)  
**Applies To:** All agents handling orchestrated tasks  
**Dependencies:** Directive 014 (Work Log Creation)  
**Version:** 1.1.0  
**Last Updated:** 2025-11-27
