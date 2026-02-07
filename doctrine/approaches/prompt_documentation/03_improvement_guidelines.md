# Step 3: Improvement Guidelines

## When to Use

Creating enhanced prompt version with improvements.

## Version Numbering

- **Original:** Version 1.0 (prompt as received)
- **Enhanced:** Version 2.0 (suggested improvements)
- **Iterations:** Version 2.1, 2.2 for minor refinements

## Improvement Categories

### Clarity Enhancements

**Replace vague terms:**

- Before: "Update the files"
- After: "Update .github/agents/directives/012_operating_procedures.md"

**Add exact references:**

- Before: "Look at the approach"
- After: "See agents/approaches/file_based_collaboration/03_process_tasks.md"

**Include examples:**

- Before: "Follow the pattern"
- After: "Follow the pattern: `YYYY-MM-DDTHHMM-agent-slug.md`"

### Completeness Additions

**Explicit success criteria:**

```markdown
## Success Criteria
- [ ] Token count reduced by 50%+
- [ ] All references remain valid
- [ ] Tests pass
```

**Deliverable specifications:**

```markdown
## Deliverables
1. Updated directive file with references
2. New approach files in agents/approaches/
3. Refactoring notes documenting changes
```

**Metric definitions:**

```markdown
## Metrics
- Current token count: 1,954 words
- Target: < 977 words (50% reduction)
- Measure: `wc -w <file>`
```

### Structure Improvements

**Logical section ordering:**

1. Context and goals first
2. Approach/method next
3. Deliverables and success criteria
4. References and related work last

**Clear process steps:**

```markdown
## Process
1. Analyze current structure
2. Extract verbose sections
3. Create approach files
4. Update directive with references
5. Validate token reduction
```

**Visual hierarchy:**

- Use heading levels consistently
- Bullet points for lists
- Code blocks for examples
- Tables for structured data

### Context Enrichment

**Situational awareness:**

```markdown
## Context
- Parent Epic: Housekeeping and Refactoring
- Related: Directive 019 refactoring (completed)
- Priority: High
- Timeline: Week 1
```

**Rationale for importance:**

```markdown
## Why This Matters
Token efficiency directly impacts:
- Agent context window usage
- Response generation speed
- Cost per interaction
```

**Audience specification:**

```markdown
## Target Audience
- Agent: Curator Claire (refactoring specialist)
- Reviewer: Framework maintainer
- Stakeholder: Development team
```

## Impact Assessment

For each improvement, specify:

**Clarity Impact** (High/Medium/Low)

- How much ambiguity reduced
- Understanding improvement

**Efficiency Impact**

- Token savings estimate
- Time savings estimate

**Quality Impact**

- Execution accuracy improvement
- Error reduction

**Reusability Impact**

- Transfer to similar tasks
- Template potential

## Implementation Example

**Before:**

```markdown
Refactor the directive to be more efficient.
```

**After:**

```markdown
Refactor `.github/agents/directives/012_operating_procedures.md`:
1. Extract verbose content (sections 2-3) to `agents/approaches/operating_procedures/`
2. Replace with cross-references using pattern from Directive 019
3. Target: 50%+ token reduction (< 228 words)
4. Validate: `wc -w` before/after comparison

Success criteria:
- [ ] Token count < 228 words
- [ ] All references valid
- [ ] Behavioral norms preserved
```

**Improvements:**

1. **Clarity:** Specific file path, exact sections, concrete pattern reference
2. **Completeness:** Step-by-step process, metric definition, validation method
3. **Structure:** Numbered steps, checklist format
4. **Context:** Success criteria explicit

**Impact:**

- Clarity: High (eliminates guesswork)
- Efficiency: High (reduces clarification needs)
- Quality: High (precise execution)
- Reusability: High (transferable pattern)

## Next Steps

- Load [04_pattern_recognition.md](04_pattern_recognition.md) to identify broader patterns
- Document improvements in prompt documentation file
