# Step 4: Pattern Recognition

## When to Use

Identifying reusable patterns and anti-patterns from prompt analysis.

## Effective Pattern Identification

Look for prompt elements that:

- Reduced interpretation time
- Eliminated clarification needs
- Enabled fast execution
- Produced high-quality results
- Required minimal context loading

## Anti-Pattern Identification

Look for prompt elements that:

- Caused confusion or delays
- Required external file consultation
- Led to misaligned execution
- Produced incomplete results
- Increased token usage unnecessarily

## Pattern Categories

### By Task Type

**Meta-Analysis Prompts**

- Characteristics: Require synthesis, cross-file analysis
- Effective patterns: Clear scope boundaries, metric definitions
- Anti-patterns: Vague "review everything" requests

**Implementation Prompts**

- Characteristics: Code/file changes, specific deliverables
- Effective patterns: Exact file paths, example outputs
- Anti-patterns: Missing acceptance criteria

**Documentation Prompts**

- Characteristics: Writing, structuring information
- Effective patterns: Target audience, format examples
- Anti-patterns: Unclear voice/tone expectations

**Coordination Prompts**

- Characteristics: Multi-agent orchestration, delegation
- Effective patterns: Clear handoff points, agent capabilities
- Anti-patterns: Undefined responsibility boundaries

**Review/Audit Prompts**

- Characteristics: Validation, compliance checking
- Effective patterns: Explicit criteria, pass/fail definitions
- Anti-patterns: Subjective quality measures

### By Effectiveness Level

**High Clarity** (minimal interpretation needed)

- Specific file paths and line numbers
- Concrete examples of desired output
- Explicit success criteria with measurements
- Step-by-step process guidance
- Clear scope boundaries

**Medium Clarity** (some interpretation required)

- General file references
- Format guidelines without examples
- Implied success criteria
- High-level process description
- Reasonable scope assumptions

**Low Clarity** (significant interpretation needed)

- Vague references ("the files")
- No examples or format guidance
- Missing success criteria
- Unclear process
- Ambiguous scope

## Pattern Documentation Format

````markdown
### Pattern: [Name]

**Context:** When to use this pattern
**Problem:** What issue it addresses
**Solution:** How to structure the prompt
**Example:**
```
[Concrete example of pattern]
```
**Benefits:**
- Benefit 1
- Benefit 2

**Cautions:**
- Potential issue 1
- Mitigation approach
````

## Effective Pattern Examples

### Pattern: Metric-First Requirements

**Context:** Tasks requiring measurable outcomes
**Problem:** Subjective interpretation of success
**Solution:** Define metrics before describing work

**Example:**

```markdown
## Success Metrics
- Token count: < 1,000 words (50% reduction from current 2,000)
- Test coverage: 100% of changed lines
- Build time: < 30 seconds

## Task
Refactor the parser module to improve efficiency...
```

**Benefits:**

- Clear success definition
- Objective validation
- Reduces scope ambiguity

**Cautions:**

- Ensure metrics are measurable
- Avoid conflicting metrics

### Pattern: Example-Driven Format

**Context:** Tasks producing structured output
**Problem:** Format misalignment with expectations
**Solution:** Include complete example of desired output

**Example:**

```markdown
## Expected Output Format

```yaml
task:
  title: "Task title"
  agent: "agent-name"
  priority: "high"
  status: "new"
```

Create task descriptors following this format for...

```

**Benefits:**
- Eliminates format guesswork
- Provides validation template
- Reduces iteration cycles

## Anti-Pattern Examples

### Anti-Pattern: Vague Scope Boundaries

**Problem:**
```markdown
Update the documentation to be better.
```

**Why It Fails:**

- "Documentation" - which files?
- "Better" - by what measure?
- No success criteria
- Unlimited scope

**Better Version:**

```markdown
Update `README.md` sections 2-3 to:
1. Add installation steps for Windows
2. Include troubleshooting section
Success: Windows users can install without external help
```

### Anti-Pattern: Implicit Prerequisites

**Problem:**

```markdown
Run the analysis on the latest data.
```

**Why It Fails:**

- "Latest data" - where is it?
- "Analysis" - which analysis?
- Assumes knowledge of location/process

**Better Version:**

```markdown
Run analysis script `ops/scripts/analyze.py` on data file:
- Location: `data/metrics/2025-11-27-metrics.json`
- Output: `reports/2025-11-27-analysis.md`
Prerequisites: Python 3.11+, pandas installed
```

## Usage Guidelines

### For Agents Documenting Prompts

1. Identify 2-3 most effective patterns from the prompt
2. Identify 1-2 anti-patterns that caused issues
3. Categorize by task type and clarity level
4. Provide concrete examples, not abstractions
5. Link patterns to SWOT findings

### For Task Creators Using Documentation

1. Review prompt documentation in `work/reports/logs/prompts/`
2. Identify patterns relevant to your task type
3. Apply effective patterns to new prompts
4. Avoid documented anti-patterns
5. Reference example prompts when available

### For Framework Maintainers

1. Aggregate patterns across multiple prompt docs
2. Build pattern library by task type
3. Create prompt templates from effective patterns
4. Update task creation guidelines with anti-patterns
5. Track pattern effectiveness over time

## Integration with SWOT

Link patterns to SWOT findings:

- **Strengths** → Effective patterns to preserve
- **Weaknesses** → Anti-patterns to avoid
- **Opportunities** → Pattern improvements to apply
- **Threats** → Pattern risks to mitigate

## Next Steps

- Include pattern analysis in prompt documentation
- Reference patterns in "Recommendations" section
- Link to similar prompts using same patterns
