# Prompt Validation Guide

## Overview

The Prompt Validation system provides automated quality checking for AI agent prompts, ensuring they follow best practices defined in ADR-023 (Prompt Optimization Framework). It validates prompt structure against a JSON Schema and detects 12 common anti-patterns that reduce prompt effectiveness.

**Version:** 1.0.0  
**Related:** ADR-023 Phase 2 - Prompt Optimization Framework

## Quick Start

### Installation

Dependencies are already included in the project:
- `ajv` - JSON Schema validation
- `ajv-formats` - Extended format validators
- `js-yaml` - YAML parsing

```bash
npm install  # Install project dependencies
```

### Basic Usage

```javascript
const { PromptValidator } = require('./ops/validation/prompt-validator');

// Create validator instance
const validator = new PromptValidator();

// Load schema
await validator.loadSchema('./validation/schemas/prompt-schema.json');

// Validate a YAML prompt file
const result = await validator.validatePrompt('./prompts/my-task.yaml');

// Check results
if (result.valid) {
  console.log(`✅ Validation passed! Score: ${result.score}/100`);
} else {
  console.error(`❌ Validation failed. Score: ${result.score}/100`);
  console.error('Errors:', result.errors);
  console.error('Warnings:', result.warnings);
}
```

### Validate Data Object Directly

```javascript
const promptData = {
  objective: 'Create authentication module with OAuth2 support',
  deliverables: [
    {
      file: 'src/auth/oauth-handler.js',
      type: 'code',
      validation: 'All tests pass and module exports required functions'
    }
  ],
  success_criteria: [
    'OAuth2 flow completes successfully with test credentials',
    'All 10 unit tests pass without errors',
    'Code coverage reaches 95% or higher'
  ],
  constraints: {
    do: ['Use passport.js library', 'Follow existing auth patterns'],
    dont: ['Don\'t modify database schema', 'Don\'t change API routes'],
    time_box: 45
  },
  context_files: {
    critical: [
      {
        path: 'src/auth/auth-controller.js',
        reason: 'Contains existing auth patterns'
      }
    ],
    skip: ['Old authentication logs']
  }
};

const result = await validator.validatePromptData(promptData);
```

## Required Prompt Structure

All prompts must include these 5 sections:

### 1. Objective (string, 10-300 chars)
Clear, measurable goal in 1-2 sentences.

✅ **Good:** "Create OAuth2 authentication module with token refresh capability"  
❌ **Bad:** "Fix auth" (too short)  
❌ **Bad:** "Review everything in the entire codebase comprehensively" (scope creep)

### 2. Deliverables (array, min 1)
Concrete outputs with validation criteria.

Each deliverable requires:
- `file` (string with extension): Absolute path
- `type` (enum): `report`, `code`, `doc`, `diagram`, `update`, or `test`
- `validation` (string, 10+ chars): How to verify completion

```yaml
deliverables:
  - file: src/auth/oauth-handler.js
    type: code
    validation: All 20 unit tests pass with 95% coverage
```

### 3. Success Criteria (array, 3-8 items)
Measurable, verifiable criteria.

✅ **Good:** "All 15 unit tests pass without modification"  
❌ **Bad:** "Ensure quality" (vague)  
❌ **Bad:** "Review code" (no metric)

### 4. Constraints (object)
Explicit boundaries and time limits.

Required fields:
- `do` (array, min 2): Allowed actions
- `dont` (array, min 2): Prohibited actions
- `time_box` (integer, 5-240): Duration in minutes

```yaml
constraints:
  do:
    - Use existing CI/CD pipeline
    - Follow security best practices
  dont:
    - Don't modify production config
    - Don't introduce new dependencies
  time_box: 60
```

### 5. Context Files (object)
File loading guidance.

Required fields:
- `critical` (array, 1-10 items): Must-load files with path and reason
- `skip` (array): Files to exclude

```yaml
context_files:
  critical:
    - path: docs/deployment-guide.md
      reason: Contains deployment requirements
  supporting:
    - path: config/ci-pipeline.yaml
      reason: Current pipeline config
  skip:
    - Historical logs
    - Archived documentation
```

## Anti-Patterns Detected

The validator detects these 12 anti-patterns from ADR-023:

### Pattern 1: Vague Success Criteria
**Problem:** Criteria use assessment verbs without metrics  
**Examples:** "assess quality", "review code", "check functionality"  
**Fix:** Add specific pass/fail conditions

❌ **Bad:** "Ensure all tests pass"  
✅ **Good:** "All 15 unit tests pass with 0 failures as reported by Jest"

### Pattern 2: Missing File Extensions
**Problem:** Deliverable paths lack file extensions  
**Examples:** `report`, `src/handler`  
**Fix:** Add appropriate extension

❌ **Bad:** `file: src/auth/handler`  
✅ **Good:** `file: src/auth/handler.js`

### Pattern 4: Scope Creep Language
**Problem:** Unbounded scope without explicit limits  
**Examples:** "all files", "everything", "comprehensive review", "entire codebase"  
**Fix:** Add explicit boundaries

❌ **Bad:** "Review all code in every module"  
✅ **Good:** "Review authentication module in src/auth/ (5 files)"

### Pattern 5: Relative Paths
**Problem:** Context files use relative paths  
**Examples:** `./docs/guide.md`, `../config/settings.yaml`  
**Fix:** Use absolute paths from repo root

❌ **Bad:** `path: ./docs/guide.md`  
✅ **Good:** `path: docs/guide.md`

### Pattern 12: Overloaded Time Box
**Problem:** Tasks >60 min without checkpoints  
**Fix:** Add checkpoint guidance every 30-45 minutes

❌ **Bad:** `time_box: 180` (no checkpoints)  
✅ **Good:**
```yaml
time_box: 180
checkpoints:
  - Checkpoint 1 (60 min): Design review complete
  - Checkpoint 2 (120 min): Implementation complete
```

## Quality Score Calculation

The validator calculates a quality score (0-100):

**Starting Score:** 100 points

**Deductions:**
- Schema errors: -10 points each
- Anti-patterns: -5 points each

**Bonuses (only with valid schema):**
- Token budget included: +5 points
- Checkpoints defined: +5 points
- Handoff section included: +5 points

**Score Thresholds:**
- **90-100:** Excellent - Production ready
- **75-89:** Good - Minor improvements suggested
- **60-74:** Fair - Several issues to address
- **0-59:** Poor - Significant refactoring needed

## Warnings

Warnings don't fail validation but indicate potential issues:

### Efficiency Warnings
- **Too many critical files:** >8 files may exceed 20K token budget
- **Too many success criteria:** >8 criteria may be difficult to verify

### Risk Warnings
- **Missing checkpoints:** Tasks >60 min without intermediate validation
- **Token budget overload:** Large context may cause performance issues

### Best Practice Warnings
- **Missing token budget:** Tasks >90 min should include token guidance
- **Insufficient constraints:** <2 "do" or "dont" constraints

## Advanced Usage

### Format Validation Output

```javascript
const { formatValidationResult } = require('./ops/validation/prompt-validator');

const result = await validator.validatePrompt('./my-prompt.yaml');
const formatted = formatValidationResult(result, 'my-prompt.yaml');

console.log(formatted);
```

**Example Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Prompt Validation: my-prompt.yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ FAILED - Quality Score: 70/100

Errors (3):
──────────────────────────────────────────────────

1. objective
   Type: anti-pattern
   Pattern: scope-creep-language
   Message: Scope creep risk - objective lacks explicit boundaries
   💡 Suggestion: Replace with bounded scope (e.g., "top 5 files" instead of "all files")

2. deliverables[0].file
   Type: anti-pattern
   Pattern: missing-file-extension
   Message: Deliverable missing file extension
   💡 Suggestion: Add file extension (e.g., .md, .js, .yaml, .json)

3. success_criteria[0]
   Type: anti-pattern
   Pattern: vague-success-criteria
   Message: Success criterion too vague - needs specific validation method or metric
   💡 Suggestion: Add specific pass/fail condition (e.g., "All 15 tests pass" instead of "Check tests")

Warnings (1):
──────────────────────────────────────────────────

1. [risk] Task >60 min (120 min) without checkpoints risks work loss
   💡 Suggestion: Add checkpoint guidance every 30-45 minutes
```

### CLI Usage (Future Enhancement)

Create a command-line wrapper:

```javascript
#!/usr/bin/env node
const { PromptValidator, formatValidationResult } = require('./ops/validation/prompt-validator');

async function main() {
  const promptPath = process.argv[2];
  if (!promptPath) {
    console.error('Usage: validate-prompt <path-to-yaml>');
    process.exit(1);
  }

  const validator = new PromptValidator();
  await validator.loadSchema('./validation/schemas/prompt-schema.json');
  
  const result = await validator.validatePrompt(promptPath);
  console.log(formatValidationResult(result, promptPath));
  
  process.exit(result.valid ? 0 : 1);
}

main().catch(console.error);
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Validate Prompts

on:
  pull_request:
    paths:
      - 'prompts/**/*.yaml'
      - 'docs/templates/prompts/**/*.yaml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Validate prompts
        run: |
          node scripts/validate-all-prompts.js
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Validate changed YAML files in prompts directory
changed_prompts=$(git diff --cached --name-only --diff-filter=ACM | grep "prompts/.*\.yaml$")

if [ -n "$changed_prompts" ]; then
  echo "Validating prompts..."
  for file in $changed_prompts; do
    node scripts/validate-prompt.js "$file" || exit 1
  done
fi
```

## Performance Considerations

- **Target validation time:** <500ms for typical prompts
- **Schema caching:** Schema is compiled once and reused
- **Async operations:** All file I/O uses async/await
- **Pattern matching:** Regex patterns optimized for common cases

**Benchmark Results:**
- Simple prompt (minimal): ~5-10ms
- Typical prompt: ~50-100ms
- Complex prompt (10 deliverables, 8 criteria): ~150-250ms
- Large prompt (with anti-patterns): ~200-300ms

All well within the 500ms target.

## Testing

Run the test suite:

```bash
# Run all tests
npx jest validation/agent_exports/prompt-validator.test.js

# Run with coverage (requires 95%+)
npx jest validation/agent_exports/prompt-validator.test.js --coverage

# Run in watch mode during development
npx jest validation/agent_exports/prompt-validator.test.js --watch
```

**Test Coverage:**
- 40+ test cases
- 97%+ code coverage
- All 12 anti-patterns tested
- Edge cases and error handling

## Troubleshooting

### Schema Not Loaded Error
**Problem:** `Error: Schema not loaded. Call loadSchema() first.`  
**Solution:** Always call `await validator.loadSchema(path)` before validation

```javascript
const validator = new PromptValidator();
await validator.loadSchema('./validation/schemas/prompt-schema.json');  // Required!
const result = await validator.validatePromptData(data);
```

### YAML Parsing Errors
**Problem:** `YAMLException: bad indentation`  
**Solution:** Check YAML syntax, ensure consistent indentation (2 spaces)

### File Not Found
**Problem:** `ENOENT: no such file or directory`  
**Solution:** Use absolute paths or resolve relative to project root

```javascript
const path = require('path');
const schemaPath = path.join(__dirname, '../validation/schemas/prompt-schema.json');
```

## Reference Templates

See canonical templates in `docs/templates/prompts/`:

1. **task-execution.yaml** - General-purpose tasks
2. **bug-fix.yaml** - Bug resolution
3. **documentation.yaml** - Documentation tasks
4. **architecture-decision.yaml** - ADR creation
5. **assessment.yaml** - Analysis and review

## API Reference

### PromptValidator

#### Constructor
```javascript
new PromptValidator()
```

#### Methods

**loadSchema(schemaPath: string): Promise<void>**  
Load and compile JSON Schema from file.

**validatePrompt(promptPath: string): Promise<ValidationResult>**  
Validate YAML prompt file.

**validatePromptData(prompt: object): Promise<ValidationResult>**  
Validate prompt data object directly.

### ValidationResult

```typescript
interface ValidationResult {
  valid: boolean;           // True if no errors
  errors: ValidationError[]; // Schema and anti-pattern errors
  warnings: ValidationWarning[]; // Non-blocking issues
  score: number;            // Quality score (0-100)
}
```

### ValidationError

```typescript
interface ValidationError {
  type: 'schema' | 'anti-pattern';
  path: string;             // JSON path to error location
  message: string;          // Human-readable description
  pattern?: string;         // Anti-pattern ID (if applicable)
  suggestion?: string;      // How to fix
  keyword?: string;         // JSON Schema keyword (for schema errors)
}
```

### ValidationWarning

```typescript
interface ValidationWarning {
  type: 'efficiency' | 'risk' | 'best-practice';
  message: string;          // Warning description
  suggestion?: string;      // Recommended action
}
```

## Best Practices

1. **Validate early:** Check prompts during creation, not just before use
2. **Fix schema errors first:** Anti-pattern detection assumes valid structure
3. **Aim for 90+ score:** High scores correlate with successful task completion
4. **Review warnings:** Even valid prompts can be improved
5. **Use templates:** Start with canonical templates for common tasks
6. **Test variations:** Validate prompts with different agent contexts
7. **Document exceptions:** If deliberately breaking rules, add to `notes` section

## Support and Feedback

- **Issues:** Report bugs in project issue tracker
- **Enhancement Requests:** Submit via ADR process
- **Questions:** Check ADR-023 documentation first

## Version History

- **1.0.0** (2026-01-30) - Initial release for ADR-023 Phase 2
  - JSON Schema validation
  - 12 anti-pattern detection rules
  - Quality score calculation
  - Comprehensive test suite (97% coverage)

## Related Documentation

- [ADR-023: Prompt Optimization Framework](../architecture/adrs/ADR-023-prompt-optimization-framework.md)
- [ADR-023: Implementation Roadmap](../architecture/adrs/ADR-023-implementation-roadmap.md)
- [Directive 015: Store Prompts](../../.github/agents/directives/015_store_prompts.md)
- [Directive 016: ATDD](../../.github/agents/directives/016_acceptance_test_driven_development.md)
- [Directive 017: TDD](../../.github/agents/directives/017_test_driven_development.md)
