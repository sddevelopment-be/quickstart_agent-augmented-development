# Agent-Friendly Error Reporting System

**Owner:** DevOps Danny  
**Status:** Active  
**Version:** 1.0.0  
**Last Updated:** 2025-02-11

## Overview

The Agent-Friendly Error Reporting System provides structured, machine-readable error summaries from GitHub Actions workflows, making it easy for Copilot agents to:
- Parse validation errors programmatically
- Understand error context and location
- Access actionable fix suggestions
- Retrieve errors via workflow artifacts

## Architecture

```
┌─────────────────────┐
│  Workflow Step      │
│  (Validator)        │
└──────────┬──────────┘
           │ Raw output
           ▼
┌─────────────────────┐
│ Error Summary       │
│ Generator           │
│ (Python)            │
└──────────┬──────────┘
           │
           ├────────────┐
           │            │
           ▼            ▼
┌──────────────┐  ┌──────────────┐
│ JSON Report  │  │ MD Summary   │
│ (Structured) │  │ (Human)      │
└──────────────┘  └──────────────┘
           │            │
           └─────┬──────┘
                 ▼
      ┌────────────────────┐
      │ GitHub Artifacts   │
      │ + PR Comments      │
      │ + Annotations      │
      └────────────────────┘
```

## Components

### 1. Core Script: `generate-error-summary.py`

**Location:** `tools/scripts/generate-error-summary.py`

**Purpose:** Parse validation output and generate structured error reports.

**Features:**
- Structured error model with location, severity, suggestions
- JSON output for programmatic access
- Markdown output for human readability
- GitHub Actions annotations for inline feedback
- Extensible error parsing for different validators

**Usage:**
```bash
# Direct usage
python tools/scripts/generate-error-summary.py \
  --workflow "Work Validation" \
  --job "validate" \
  --validator "task-schema" \
  --input validation_output.txt \
  --output-json errors.json \
  --output-markdown errors.md \
  --emit-annotations \
  --fail-on-errors

# Via stdin
python validate-task-schema.py file.yaml 2>&1 | \
  python generate-error-summary.py \
    --workflow "..." \
    --job "..." \
    --validator "..."
```

### 2. Shell Wrapper: `generate-error-summary.sh`

**Location:** `tools/scripts/generate-error-summary.sh`

**Purpose:** Bash-friendly wrapper with sensible defaults.

**Usage:**
```bash
bash generate-error-summary.sh \
  --workflow "Work Validation" \
  --job "validate" \
  --validator "task-schema" \
  --input validation_output.txt \
  --emit-annotations \
  --fail-on-errors
```

### 3. Reusable Action: `error-summary`

**Location:** `.github/actions/error-summary/action.yml`

**Purpose:** Drop-in GitHub Action for workflows.

**Usage:**
```yaml
- name: Generate error report
  if: failure()
  uses: ./.github/actions/error-summary
  with:
    workflow-name: "Work Directory Validation"
    job-name: "validate"
    validator-name: "task-schema"
    input-file: output/validation.txt
    fail-on-errors: 'true'
    emit-annotations: 'true'
    upload-artifact: 'true'
```

## Error Format

### JSON Structure

```json
{
  "workflow": "Work Directory Validation",
  "job": "validate",
  "run_id": "12345",
  "run_url": "https://github.com/org/repo/actions/runs/12345",
  "timestamp": "2025-02-11T20:00:00Z",
  "summary": {
    "total_errors": 3,
    "total_warnings": 1,
    "total_issues": 4
  },
  "errors": [
    {
      "error_id": "task-schema_1234",
      "error_type": "validation_failure",
      "severity": "error",
      "message": "work/agent/done/task.yaml: invalid status 'foo', expected one of ['done', 'error', 'assigned']",
      "validator": "task-schema",
      "timestamp": "2025-02-11T20:00:00Z",
      "location": {
        "file_path": "work/agent/done/task.yaml",
        "line_number": 5,
        "column_number": null,
        "context_lines": []
      },
      "suggestions": [
        {
          "description": "Update status field to one of: done, assigned, in_progress, error",
          "diff": null,
          "command": null
        }
      ],
      "raw_output": "❌ work/agent/done/task.yaml: invalid status 'foo', expected one of ['done', 'error']",
      "documentation_url": null
    }
  ]
}
```

### Markdown Format

```markdown
# 🔍 Error Summary: Work Directory Validation

**Job:** validate
**Timestamp:** 2025-02-11T20:00:00Z
**Run:** [View Full Logs](https://github.com/.../runs/12345)

## Summary

- ❌ **Errors:** 3
- ⚠️ **Warnings:** 1
- 📊 **Total Issues:** 4

## Issues by Validator

### task-schema
*3 errors, 1 warnings*

❌ **validation_failure**: invalid status 'foo', expected one of ['done', 'error']
  - 📁 `work/agent/done/task.yaml`, Line 5

  **Suggested fixes:**
  1. Update status field to one of: done, assigned, in_progress, error
```

## Integration Patterns

### Pattern 1: Capture and Report on Failure

```yaml
- name: Run validator
  id: validate
  run: |
    set +e
    OUTPUT_FILE="output/validation.txt"
    mkdir -p output
    
    python tools/validators/validate-task-schema.py file.yaml 2>&1 | tee "$OUTPUT_FILE"
    EXIT_CODE=${PIPESTATUS[0]}
    
    echo "exit_code=$EXIT_CODE" >> $GITHUB_OUTPUT
    echo "output_file=$OUTPUT_FILE" >> $GITHUB_OUTPUT
  continue-on-error: true

- name: Generate error report
  if: steps.validate.outputs.exit_code != '0'
  uses: ./.github/actions/error-summary
  with:
    workflow-name: ${{ github.workflow }}
    job-name: ${{ github.job }}
    validator-name: "task-schema"
    input-file: ${{ steps.validate.outputs.output_file }}
```

### Pattern 2: Aggregate Multiple Validators

```yaml
- name: Run all validators
  id: validate_all
  run: |
    set +e
    EXIT_CODE=0
    
    # Structure
    bash tools/validators/validate-work-structure.sh 2>&1 | tee output/structure.txt
    [ ${PIPESTATUS[0]} -ne 0 ] && EXIT_CODE=1
    
    # Schema
    python tools/validators/validate-task-schema.py file.yaml 2>&1 | tee output/schema.txt
    [ ${PIPESTATUS[0]} -ne 0 ] && EXIT_CODE=1
    
    echo "exit_code=$EXIT_CODE" >> $GITHUB_OUTPUT
  continue-on-error: true

- name: Generate structure error report
  if: always()
  uses: ./.github/actions/error-summary
  with:
    workflow-name: ${{ github.workflow }}
    job-name: ${{ github.job }}
    validator-name: "work-structure"
    input-file: output/structure.txt
    fail-on-errors: 'false'

- name: Generate schema error report
  if: always()
  uses: ./.github/actions/error-summary
  with:
    workflow-name: ${{ github.workflow }}
    job-name: ${{ github.job }}
    validator-name: "task-schema"
    input-file: output/schema.txt
    fail-on-errors: 'false'
```

## Agent Access Guide

### For Copilot Agents

**Step 1: Identify Failed Workflow Run**
- Look for PR comment with validation results
- Note the run ID (e.g., `12345`)

**Step 2: Download Error Artifacts**
```bash
# Using GitHub CLI
gh run download 12345 --name error-summary-task-schema-12345

# Or via API
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/org/repo/actions/runs/12345/artifacts
```

**Step 3: Parse JSON Errors**
```python
import json

with open("errors_*.json") as f:
    report = json.load(f)

for error in report["errors"]:
    print(f"Error: {error['message']}")
    print(f"File: {error['location']['file_path']}")
    print(f"Line: {error['location']['line_number']}")
    
    for suggestion in error["suggestions"]:
        print(f"Fix: {suggestion['description']}")
        if suggestion['command']:
            print(f"  Run: {suggestion['command']}")
```

**Step 4: Apply Fixes**
- Use error location to navigate to specific files
- Review suggestions for actionable fixes
- Execute suggested commands where applicable
- Re-run validation locally before pushing

### Example Agent Workflow

```markdown
1. Agent detects PR validation failure
2. Agent downloads error-summary artifact
3. Agent parses JSON to extract:
   - File paths with errors
   - Line numbers for precise location
   - Error types and severities
   - Fix suggestions
4. Agent applies fixes:
   - For schema errors: Update YAML fields
   - For structure errors: Create missing directories
   - For naming errors: Rename files
5. Agent commits fixes
6. Validation re-runs automatically
```

## Adding New Validators

### Step 1: Ensure Structured Output

Validators should output errors in a parseable format:

```bash
# Good: Structured with markers
echo "❌ path/to/file.yaml: invalid status 'foo'"

# Better: Include line numbers
echo "❌ path/to/file.yaml:5: invalid status 'foo'"

# Best: Use consistent format
echo "ERROR: path/to/file.yaml:5:10: invalid status 'foo', expected one of ['done', 'error']"
```

### Step 2: Integrate Error Reporting

```yaml
- name: Run new validator
  id: new_validator
  run: |
    set +e
    OUTPUT_FILE="output/new_validator.txt"
    mkdir -p output
    
    bash tools/validators/new-validator.sh 2>&1 | tee "$OUTPUT_FILE"
    EXIT_CODE=${PIPESTATUS[0]}
    
    echo "exit_code=$EXIT_CODE" >> $GITHUB_OUTPUT
    echo "output_file=$OUTPUT_FILE" >> $GITHUB_OUTPUT
  continue-on-error: true

- name: Generate error report
  if: steps.new_validator.outputs.exit_code != '0'
  uses: ./.github/actions/error-summary
  with:
    workflow-name: ${{ github.workflow }}
    job-name: ${{ github.job }}
    validator-name: "new-validator"
    input-file: ${{ steps.new_validator.outputs.output_file }}
```

### Step 3: Extend Error Parser (Optional)

For custom error formats, extend `ErrorParser` class:

```python
@staticmethod
def parse_custom_validator_output(output: str, validator: str) -> list[ValidationError]:
    """Parse custom validator format."""
    errors = []
    
    for line in output.split("\n"):
        # Custom parsing logic
        if "CUSTOM_ERROR:" in line:
            # Extract details
            error = ValidationError(
                error_id=f"{validator}_{hash(line)}",
                error_type="custom_error",
                severity="error",
                message=line,
                validator=validator,
                timestamp=datetime.utcnow().isoformat() + "Z",
            )
            errors.append(error)
    
    return errors
```

## Testing

### Test Script Locally

```bash
# Create test validation output
echo "❌ work/test.yaml: invalid status 'foo'" > test_output.txt
echo "⚠️ Missing required directory: work/collaboration" >> test_output.txt

# Generate report
python tools/scripts/generate-error-summary.py \
  --workflow "Test" \
  --job "test" \
  --validator "test" \
  --input test_output.txt \
  --output-json test_errors.json \
  --output-markdown test_errors.md

# Verify JSON structure
python -m json.tool test_errors.json

# Verify markdown format
cat test_errors.md
```

### Test in Workflow

See example test workflow in `.github/workflows/test-error-reporting.yml`

## Best Practices

### For Validator Authors

1. **Use consistent error markers:** `❌` for errors, `⚠️` for warnings
2. **Include file paths:** Always specify which file has issues
3. **Add line numbers:** When possible, include exact location
4. **Provide context:** Explain what's wrong and why
5. **Suggest fixes:** Include actionable remediation steps

### For Workflow Authors

1. **Capture all output:** Use `2>&1 | tee` to capture both stdout and stderr
2. **Continue on error:** Use `continue-on-error: true` to allow reporting
3. **Upload artifacts:** Always upload error summaries for agent access
4. **Update PR comments:** Keep PRs updated with latest validation status
5. **Emit annotations:** Use GitHub annotations for inline feedback

### For Agent Developers

1. **Download artifacts:** Always fetch structured JSON reports
2. **Parse systematically:** Use the error model structure
3. **Apply fixes incrementally:** Fix one error type at a time
4. **Verify locally:** Test fixes before committing
5. **Document changes:** Reference error IDs in commit messages

## Troubleshooting

### Error: "No such file or directory: generate-error-summary.py"

**Solution:** Ensure you're running from repository root:
```bash
cd /path/to/repo
python tools/scripts/generate-error-summary.py ...
```

### Error: "Python module not found"

**Solution:** Install required dependencies:
```bash
pip install pyyaml
```

### No errors captured in artifact

**Solution:** Verify output is being captured:
```yaml
- name: Run validator
  run: |
    # Ensure output is written to file
    bash validator.sh 2>&1 | tee output/validation.txt
    # Check file was created
    ls -la output/validation.txt
```

### Artifacts not uploading

**Solution:** Check artifact path matches output file:
```yaml
- uses: ./.github/actions/error-summary
  with:
    input-file: output/validation.txt  # Must match actual file path
```

## Future Enhancements

- [ ] Auto-suggest diff patches for common fixes
- [ ] Integration with GitHub Code Scanning
- [ ] Error trend analysis across runs
- [ ] Automated fix PR generation
- [ ] Custom error rules configuration
- [ ] Multi-language validator support

## References

- **ADR-028:** Bug Fixing Techniques (test-first approach)
- **Directive 001:** CLI & Shell Tooling
- **Directive 018:** Documentation Level Framework
- **GitHub Actions Annotations:** https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions

## Support

For issues or questions:
1. Check existing workflow runs for examples
2. Review this documentation
3. Test locally with sample data
4. Consult DevOps Danny (agent profile)

---

*Last updated: 2025-02-11 by DevOps Danny*
