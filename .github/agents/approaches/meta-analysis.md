# meta-analysis

Periodic analysis of work logs and prompt assessments to identify framework improvements

## Capabilities
- framework-improvement
- operational-guide

## Purpose

Review accumulated work logs, prompt assessments, and operational patterns to surface systemic improvements. This approach treats the agent framework itself as an evolving system that benefits from empirical observation and continuous refinement.

## When to Use

- Monthly operational reviews
- After major feature additions or structural changes
- When patterns of confusion or inefficiency emerge
- Before quarterly planning cycles
- On explicit request: `/meta-analysis`

## Instructions

### 1. Collection Phase

Gather artifacts from recent operational periods (default: last 30 days):

```bash
# Work logs
`${WORKSPACE_ROOT}/reports/logs/*.md

# Prompt assessments
`${WORKSPACE_ROOT}/prompts/*.md

# Decision records (if relevant)
`${DOC_ROOT}/decisions/*.md

# Error logs or anomaly reports
`${WORKSPACE_ROOT}/reports/errors/ (if present)
```

**Collection criteria:**
- Prioritize recent material (last 30 days)
- Include edge cases and error conditions
- Note frequency of similar issues
- Capture both successes and failures

### 2. Analysis Phase

#### What to Look For

**A. Common Mistakes & Anti-Patterns**
- Repeated misunderstandings of directives
- Scope creep beyond stated capabilities
- Inefficient tool usage (e.g., sequential instead of parallel calls)
- Missing context or incomplete handoffs
- Assumption failures (e.g., path errors, missing files)

**B. Token Efficiency Issues**
- Verbose logs where concise ones would suffice
- Redundant context loading
- Unnecessary re-reading of files
- Over-explanation where brevity is appropriate
- Primer misapplication (wrong detail level)

**C. Clarity & Communication Gaps**
- Ambiguous directives causing confusion
- Missing guidance for edge cases
- Unclear agent boundaries or responsibilities
- Inadequate examples in approaches
- Documentation drift (stated vs. actual behavior)

**D. Structural Problems**
- Missing capabilities that are frequently improvised
- Approach files that are too abstract or too prescriptive
- Directive conflicts or overlaps
- Inadequate cross-referencing between documents

**E. Workflow Bottlenecks**
- Tasks requiring multiple back-and-forth clarifications
- Frequent escalations that could be handled with better guidance
- Repeated requests for the same type of information
- Manual processes that could be automated

#### Analysis Technique

For each log or prompt assessment:

1. **Identify the core task**: What was requested?
2. **Evaluate execution quality**: Was it completed effectively?
3. **Note deviations**: Where did behavior diverge from expectations?
4. **Extract learnings**: What does this reveal about framework gaps?
5. **Assess recurrence**: Is this a one-off or pattern?

### 3. Categorization Phase

Group findings into actionable categories:

**Category 1: Anti-Patterns**
- Behaviors to actively discourage
- Common traps or failure modes
- Misapplications of existing guidance

**Category 2: Efficiency Opportunities**
- Token usage optimizations
- Tool call improvements
- Process streamlining

**Category 3: Quality Enhancements**
- Clarity improvements
- Better examples
- Refined directives

**Category 4: Missing Capabilities**
- Gaps requiring new approaches
- Underspecified domains
- Cross-cutting concerns without guidance

**Category 5: Documentation Debt**
- Outdated or incorrect documents
- Missing cross-references
- Ambiguous language

### 4. Prioritization Phase

Rank findings using impact × frequency matrix:

| Priority | Criteria |
|----------|----------|
| **Critical** | High frequency + High impact (affects multiple agents/tasks) |
| **High** | High frequency OR High impact |
| **Medium** | Moderate frequency + Moderate impact |
| **Low** | One-off issues or minimal impact |

**Impact factors:**
- Number of agents affected
- Severity of errors or inefficiency
- User experience degradation
- Maintenance burden

**Frequency factors:**
- Occurrences in review period
- Across how many different contexts
- Trend direction (increasing/stable/decreasing)

### 5. Recommendation Phase

For each high-priority finding, propose concrete improvements:

**Recommendation format:**

```markdown
### [Category]: [Brief Description]

**Problem**: Clear statement of the issue
**Evidence**: References to specific logs/assessments
**Impact**: Who/what is affected
**Proposal**: Specific, actionable change
**Effort**: Estimated complexity (Low/Medium/High)
**Owner**: Suggested responsible party (if applicable)
```

**Types of recommendations:**
- New or revised directive language
- Additional approach files
- Improved examples or templates
- Tool usage guidelines
- Process refinements
- Documentation updates

### 6. Documentation Phase

Write assessment report to `work/reports/assessments/`:

**Filename convention**: `meta-YYYY-MM-DD.md`

**Report structure:**

```markdown
# Meta-Analysis: [Date Range]

**Analysis Date**: YYYY-MM-DD
**Review Period**: [Start Date] to [End Date]
**Logs Reviewed**: [Count]
**Assessments Reviewed**: [Count]

## Executive Summary

[2-3 paragraph overview of key findings and recommendations]

## Collection Summary

- Total artifacts reviewed: X
- Date range: [dates]
- Agents covered: [list]
- Task types analyzed: [categories]

## Key Findings

### Critical Issues
[Prioritized list with evidence]

### Opportunities for Improvement
[Prioritized list with evidence]

### Positive Patterns
[What's working well - preserve these]

## Detailed Analysis

[For each category, provide deeper analysis with references]

## Recommendations

[Prioritized list of actionable improvements]

## Appendices

### A. Reference Logs
[Links to specific logs supporting findings]

### B. Metrics
[Quantitative data if available]

### C. Follow-Up Actions
[Tracking items for implementation]
```

## Output Expectations

**Characteristics of a good meta-analysis:**

- **Empirical**: Grounded in actual logs, not speculation
- **Specific**: References concrete examples
- **Actionable**: Recommendations are implementable
- **Balanced**: Notes both problems and successes
- **Prioritized**: Clear guidance on what matters most
- **Concise**: Respects reader attention (aim for 1500-3000 words)

**Avoid:**
- Vague generalizations without evidence
- Recommendations without clear ownership or effort estimates
- Over-focusing on trivial issues while missing systemic problems
- Pure criticism without constructive proposals
- Analysis paralysis (don't let perfect be enemy of good)

## Integration with Existing Framework

**Cross-references:**
- Uses Directive 018 (Documentation Levels) to calibrate detail
- Applies Directive 022 (Audience Orientation) for report writing
- Follows DDR-001 (Primer Execution Matrix) and Directive 010 for appropriate depth
- Logs analysis per Directive 014 (Work Logging)
- May surface items for architectural decision process (Directive 005)

**Collaboration:**
- Share findings with relevant specialists
- Coordinate with DocMaster Dan for documentation updates
- Escalate systemic issues requiring architectural decisions

## Example Prompts

- "Run meta-analysis on recent work logs"
- "/meta-analysis"
- "Analyze the last month of operational logs for improvement opportunities"
- "Review prompt assessments and identify recurring confusion"
- "What patterns emerge from recent work logs?"

## Success Indicators

- Recommendations are implemented and improve operations
- Reduction in recurring errors or confusion
- Improved token efficiency in subsequent logs
- Fewer escalations for previously common issues
- Documentation becomes clearer and more actionable

## Metadata

**Approach Type**: analytical, periodic  
**Typical Duration**: 1-3 hours depending on scope  
**Output**: Written assessment report  
**Frequency**: Monthly or on-demand  
**Dependencies**: Requires existing work logs and assessments
