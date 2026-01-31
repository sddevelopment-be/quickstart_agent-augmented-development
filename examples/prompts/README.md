# Example Prompts

This directory contains example prompt files that demonstrate the structure and quality requirements defined in [ADR-023 Prompt Optimization Framework](../../docs/architecture/adrs/ADR-023-prompt-optimization-framework.md).

## Purpose

These example prompts serve as:
1. **Reference implementations** showing correct prompt structure
2. **Test fixtures** for the prompt validation CI/CD pipeline
3. **Learning resources** for creating high-quality agent prompts

## Files

### Valid Prompts

- **`valid-deployment-task.yaml`** - Example of a well-structured deployment automation task
  - Score: 100/100
  - Demonstrates all required fields with proper formatting
  - Includes optional best-practice fields (checkpoints, token_budget)
  - No anti-patterns detected

### Invalid Prompts (for testing)

- **`invalid-bug-fix.yaml`** - Example showing common anti-patterns
  - Score: 15/100
  - Demonstrates validation errors:
    - Vague success criteria
    - Missing file extensions
    - Relative paths
    - Insufficient constraints
  - Used to test CI failure scenarios

## Validation

To validate prompts in this directory:

```bash
# Run validation
npm run validate:prompts

# Verbose output with detailed errors
npm run validate:prompts:verbose

# Strict mode (threshold 85)
npm run validate:prompts:strict

# JSON output
npm run validate:prompts:json
```

## Schema Compliance

All prompts in this directory should conform to the schema defined in:
- **Schema:** `validation/schemas/prompt-schema.json`
- **Validator:** `ops/validation/prompt-validator.js`
- **Anti-patterns:** Defined in ADR-023

## Required Fields

Every valid prompt must include:
- `objective` - Clear, measurable goal (10-300 chars)
- `deliverables` - Array of concrete outputs with validation
- `success_criteria` - 3-8 measurable criteria
- `constraints` - do/dont/time_box
- `context_files` - critical/skip file guidance

## Optional Fields (Recommended)

- `checkpoints` - Required for tasks >60 min
- `token_budget` - Recommended for large tasks
- `handoff` - For multi-agent workflows
- `compliance` - Directive/ADR references

## Creating New Examples

To add a new example prompt:

1. Create a `.yaml` file in this directory
2. Follow the structure in `valid-deployment-task.yaml`
3. Run validation: `npm run validate:prompts:verbose`
4. Fix any errors until score >= 70
5. Commit the file

## CI Integration

The GitHub Actions workflow `.github/workflows/validate-prompts.yml` automatically:
- Validates all `.yaml` files in this directory on every PR
- Posts quality report as PR comment
- Fails CI if any prompt scores < 70
- Uploads validation artifacts for review

## Related Documentation

- [ADR-023: Prompt Optimization Framework](../../docs/architecture/adrs/ADR-023-prompt-optimization-framework.md)
- [CI Validation Guide](../../docs/HOW_TO_USE/ci-validation-guide.md)
- [Prompt Templates](../../docs/templates/prompts/) - Markdown template documentation
- [Validator Implementation](../../ops/validation/prompt-validator.js)

## Quality Thresholds

- **Minimum (CI Pass):** 70/100
- **Good:** 80-89/100
- **Excellent:** 90-99/100
- **Perfect:** 100/100

## Common Anti-Patterns to Avoid

1. **Vague success criteria** - Use specific metrics, not "ensure quality"
2. **Missing file extensions** - All deliverable paths need extensions
3. **Relative paths** - Use absolute paths from repo root
4. **Scope creep** - Avoid "all", "every", "comprehensive"
5. **Weak constraints** - Need at least 2 do's and 2 don'ts
6. **No checkpoints** - Required for tasks >60 minutes

See [CI Validation Guide](../../docs/HOW_TO_USE/ci-validation-guide.md) for detailed fixes.

---

**Maintained by:** DevOps Danny (Build Automation)  
**Last Updated:** 2026-01-31  
**Related ADR:** ADR-023
