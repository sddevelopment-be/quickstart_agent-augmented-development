# Example Error Reports

This directory contains example error report outputs from the agent-friendly error reporting system.

## Files

### `example-validation-errors.json`
Complete JSON error report showing:
- Multiple error types (schema validation, structure validation)
- Error severities (error, warning)
- Location information (file paths, line numbers)
- Actionable fix suggestions
- Metadata (workflow, job, timestamps)

**Use this as reference for:**
- Understanding JSON structure
- Parsing errors programmatically
- Building agent automation

### `example-validation-errors.md`
Human-readable Markdown version of the same errors.

**Use this as reference for:**
- Understanding error format
- Writing PR comments
- Creating summaries

### `README.md`
This file - explains the examples.

## Using These Examples

### For Agent Developers

Parse the JSON to understand the structure:

```python
import json

with open("examples/error-reports/example-validation-errors.json") as f:
    report = json.load(f)

# Access summary
print(f"Total errors: {report['summary']['total_errors']}")

# Iterate through errors
for error in report["errors"]:
    print(f"\nError ID: {error['error_id']}")
    print(f"Type: {error['error_type']}")
    print(f"Severity: {error['severity']}")
    print(f"Message: {error['message']}")
    
    # Location (if available)
    if error['location'] and error['location']['file_path']:
        print(f"File: {error['location']['file_path']}")
        if error['location']['line_number']:
            print(f"Line: {error['location']['line_number']}")
    
    # Suggestions
    for suggestion in error['suggestions']:
        print(f"Fix: {suggestion['description']}")
        if suggestion['command']:
            print(f"Command: {suggestion['command']}")
```

### For Workflow Authors

Reference these examples when:
- Testing new validators
- Verifying error report format
- Creating documentation
- Training agents

### For Humans

Review the Markdown file to understand:
- How errors are presented
- What information is available
- How to interpret suggestions
- Where to find more details

## Generating Your Own Examples

Use the test script:

```bash
# Create sample error output
cat > test_errors.txt << 'EOF'
❌ path/to/file.yaml: error message
⚠️ path/to/other.yaml: warning message
EOF

# Generate reports
python tools/scripts/generate-error-summary.py \
  --workflow "Test" \
  --job "test" \
  --validator "test" \
  --input test_errors.txt \
  --output-json my-errors.json \
  --output-markdown my-errors.md
```

## Error Format Evolution

As the system evolves, these examples will be updated to reflect:
- New error types
- Additional fields
- Enhanced suggestions
- Improved location tracking

Check git history for changes:
```bash
git log --follow examples/error-reports/
```

## Related Documentation

- **Full Docs:** [docs/error-reporting-system.md](../../docs/error-reporting-system.md)
- **Quick Reference:** [docs/error-reporting-quick-reference.md](../../docs/error-reporting-quick-reference.md)
- **Source Code:** [tools/scripts/generate-error-summary.py](../../tools/scripts/generate-error-summary.py)

---

*Examples maintained by DevOps Danny*
