# Agent-Friendly Error Reporting - Quick Reference

**Version:** 1.0.0  
**Last Updated:** 2025-02-11

## Quick Start

### For Workflow Authors

Add error reporting to any validation step:

```yaml
- name: Run validator
  id: validate
  run: |
    set +e
    OUTPUT_FILE="output/validation.txt"
    mkdir -p output
    
    bash tools/validators/your-validator.sh 2>&1 | tee "$OUTPUT_FILE"
    echo "output_file=$OUTPUT_FILE" >> $GITHUB_OUTPUT
  continue-on-error: true

- name: Generate error report
  if: failure()
  uses: ./.github/actions/error-summary
  with:
    workflow-name: ${{ github.workflow }}
    job-name: ${{ github.job }}
    validator-name: "your-validator"
    input-file: ${{ steps.validate.outputs.output_file }}
```

### For Copilot Agents

**Step 1:** Find the error artifact
```bash
# List artifacts from a workflow run
gh run view RUN_ID --json artifacts

# Download error summary
gh run download RUN_ID --name error-summary-VALIDATOR-RUN_ID
```

**Step 2:** Parse the JSON
```python
import json

with open("errors_*.json") as f:
    report = json.load(f)

# Access structured error data
for error in report["errors"]:
    print(f"File: {error['location']['file_path']}")
    print(f"Line: {error['location']['line_number']}")
    print(f"Error: {error['message']}")
    
    # Get fix suggestions
    for suggestion in error["suggestions"]:
        print(f"Fix: {suggestion['description']}")
        if suggestion['command']:
            print(f"Run: {suggestion['command']}")
```

**Step 3:** Apply fixes systematically
```bash
# Navigate to error location
vim +LINE_NUMBER FILE_PATH

# Or apply automated fixes
for suggestion in suggestions:
    if suggestion.command:
        eval $suggestion.command
```

## Error Format Reference

### JSON Structure
```json
{
  "workflow": "...",
  "job": "...",
  "summary": {
    "total_errors": N,
    "total_warnings": N
  },
  "errors": [
    {
      "error_id": "unique-id",
      "error_type": "validation_failure",
      "severity": "error",
      "message": "...",
      "validator": "...",
      "location": {
        "file_path": "...",
        "line_number": N
      },
      "suggestions": [
        {
          "description": "...",
          "command": "..."
        }
      ]
    }
  ]
}
```

### Severity Levels
- **error**: Must be fixed (blocks merge)
- **warning**: Should be reviewed (doesn't block)
- **info**: Informational (FYI only)

### Common Error Types
- `validation_failure`: Validation rule violation
- `schema_error`: YAML/JSON schema mismatch
- `syntax_error`: Parse error
- `missing_file`: Required file not found
- `missing_field`: Required field not present

## Command Reference

### Python Script
```bash
python tools/scripts/generate-error-summary.py \
  --workflow "NAME" \
  --job "NAME" \
  --validator "NAME" \
  --input file.txt \
  --output-json errors.json \
  --output-markdown errors.md \
  --emit-annotations \
  --fail-on-errors
```

### Shell Wrapper
```bash
bash tools/scripts/generate-error-summary.sh \
  --workflow "NAME" \
  --job "NAME" \
  --validator "NAME" \
  --input file.txt
```

### GitHub Action
```yaml
- uses: ./.github/actions/error-summary
  with:
    workflow-name: "Workflow Name"
    job-name: "job-name"
    validator-name: "validator-name"
    input-file: "path/to/output.txt"
    fail-on-errors: 'true'
    emit-annotations: 'true'
    upload-artifact: 'true'
```

## Integration Patterns

### Pattern 1: Single Validator
```yaml
- name: Validate
  id: validate
  run: bash tools/validators/validate.sh 2>&1 | tee output/validate.txt
  continue-on-error: true

- name: Report errors
  if: steps.validate.outcome == 'failure'
  uses: ./.github/actions/error-summary
  with:
    workflow-name: ${{ github.workflow }}
    job-name: ${{ github.job }}
    validator-name: "validator"
    input-file: output/validate.txt
```

### Pattern 2: Multiple Validators
```yaml
- name: Run all validators
  run: |
    bash tools/validators/structure.sh 2>&1 | tee output/structure.txt || true
    python tools/validators/schema.py 2>&1 | tee output/schema.txt || true
  continue-on-error: true

- name: Report structure errors
  uses: ./.github/actions/error-summary
  with:
    validator-name: "structure"
    input-file: output/structure.txt
    ...

- name: Report schema errors
  uses: ./.github/actions/error-summary
  with:
    validator-name: "schema"
    input-file: output/schema.txt
    ...
```

### Pattern 3: Aggregate & Comment
```yaml
- name: Generate all reports
  if: always()
  run: |
    # Reports generated in previous steps
    ls -la output/*.json

- name: Comment on PR
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const reports = fs.readdirSync('output')
        .filter(f => f.endsWith('.json'))
        .map(f => JSON.parse(fs.readFileSync(`output/${f}`)));
      
      let body = '## Validation Results\n\n';
      for (const report of reports) {
        body += `### ${report.validator}\n`;
        body += `- Errors: ${report.summary.total_errors}\n`;
        body += `- Warnings: ${report.summary.total_warnings}\n\n`;
      }
      
      github.rest.issues.createComment({...});
```

## Troubleshooting

### No errors captured
- Verify `2>&1 | tee` captures both stdout and stderr
- Check output file exists: `ls -la output/validation.txt`
- Ensure validators write to stdout/stderr (not just return codes)

### JSON parse error
- Verify input file is text (not binary)
- Check for valid UTF-8 encoding
- Ensure validators use consistent format

### Artifacts not uploading
- Check artifact name is unique per validator
- Verify output files exist before upload step
- Check retention-days doesn't exceed repo limits

### Annotations not showing
- Verify `emit-annotations: 'true'` is set
- Check file paths are relative to repo root
- Ensure line numbers are valid

## Best Practices

### For Validator Authors
1. Use consistent error markers: `❌`, `⚠️`, `❗️`
2. Always include file paths when applicable
3. Add line numbers for precision
4. Write actionable error messages
5. Suggest fixes where possible

### For Workflow Authors
1. Capture all output: `2>&1 | tee`
2. Continue on error: `continue-on-error: true`
3. Upload artifacts: `upload-artifact: 'true'`
4. Update PR comments with results
5. Emit annotations for inline feedback

### For Agent Developers
1. Always download JSON artifacts
2. Parse errors systematically
3. Apply fixes one type at a time
4. Verify fixes locally first
5. Reference error IDs in commits

## Examples

### Example 1: Schema Validation Error
```json
{
  "error_id": "schema_1234",
  "error_type": "validation_failure",
  "severity": "error",
  "message": "invalid status 'foo', expected one of ['done', 'error']",
  "location": {
    "file_path": "work/task.yaml",
    "line_number": 5
  },
  "suggestions": [
    {
      "description": "Update status field to 'done' or 'error'",
      "command": null
    }
  ]
}
```

**Agent Fix:**
```python
# Read YAML
with open("work/task.yaml") as f:
    task = yaml.safe_load(f)

# Apply fix
task["status"] = "done"

# Write back
with open("work/task.yaml", "w") as f:
    yaml.dump(task, f)
```

### Example 2: Missing Directory Error
```json
{
  "error_id": "structure_5678",
  "error_type": "validation_failure",
  "severity": "error",
  "message": "Missing required directory: work/reports",
  "suggestions": [
    {
      "description": "Create missing directory",
      "command": "mkdir -p work/reports"
    }
  ]
}
```

**Agent Fix:**
```bash
mkdir -p work/reports
```

## Resources

- **Full Documentation:** [docs/error-reporting-system.md](error-reporting-system.md)
- **Source Code:** `tools/scripts/generate-error-summary.py`
- **Action:** `.github/actions/error-summary/action.yml`
- **Tests:** `tests/test_error_reporting_integration.sh`

## Support

Questions? Issues?
1. Review full documentation
2. Check existing workflow runs for examples
3. Test locally with sample data
4. Consult DevOps Danny agent

---

*Generated by DevOps Danny - Agent-Friendly CI/CD*
