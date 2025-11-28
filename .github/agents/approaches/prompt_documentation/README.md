# Prompt Documentation Approach

## Overview

Optional practice for documenting task prompts with SWOT analysis to improve prompt quality and effectiveness over time.

## When to Document Prompts

Agents **MAY** document prompts when:
- Completing complex or novel orchestration tasks
- Encountering ambiguous task requirements
- Identifying patterns in prompt quality
- Requested explicitly by stakeholders

Agents **SHOULD** document prompts when:
- Prompt could serve as learning example
- Significant improvements identified
- Task execution revealed gaps in prompt
- Represents new pattern worth preserving

## Approach Steps

Load only the step relevant to your current need:

| Step | File | When to Load |
|------|------|--------------|
| 1. Structure Template | [01_documentation_structure.md](01_documentation_structure.md) | Creating new prompt documentation |
| 2. SWOT Analysis | [02_swot_analysis_guidelines.md](02_swot_analysis_guidelines.md) | Analyzing prompt effectiveness |
| 3. Improvements | [03_improvement_guidelines.md](03_improvement_guidelines.md) | Suggesting prompt enhancements |
| 4. Pattern Recognition | [04_pattern_recognition.md](04_pattern_recognition.md) | Identifying reusable patterns |

## Location

All prompt documentation in: `work/reports/logs/prompts/YYYY-MM-DDTHHMM-<agent>-<slug>-prompt.md`

## Integration

Complements **Directive 014** (Work Logs):
- Work log: Documents execution and outcomes
- Prompt doc: Documents request quality and improvements

## Benefits

- **Agents**: Learn from experience, improve interpretation
- **Task Creators**: Improve prompt writing, understand agent perspective
- **Framework**: Build template library, evolve best practices

## Status

**Directive Status:** Optional (MAY/SHOULD)  
**Applies To:** All agents handling orchestrated tasks  
**Dependencies:** Directive 014 (Work Log Creation)
