# Operations Scripts

This directory contains automation scripts for repository operations and portability enhancements.

## Contents

### `scripts/`

Scripts for converting and validating agent configurations, plus lightweight context assembly helpers.

#### `assemble-agent-context.sh`

Emits a minimal or full agent context bundle (runtime sheet, aliases, specialist profile, and optional directives) to STDOUT to avoid manual copy/paste.

**Usage:**
```bash
ops/scripts/assemble-agent-context.sh --agent backend-dev --mode minimal --directives 001 006
```

**Options:**
- `--agent <name|path>` - Specialist profile basename (e.g., `backend-dev`) or explicit path.
- `--mode minimal|full` - Minimal includes runtime sheet + profile + aliases; full adds general and operational guidelines.
- `--directives <codes>` - Space-separated directive codes to inline via `.github/agents/load_directives.sh`.
- `--no-aliases` - Skip alias inclusion.

Use `--mode full` for high-stakes work that requires full governance; default `minimal` keeps tokens lean for low-risk edits.

Tip: `.github/agents/load_directives.sh --list` shows available directive codes before assembling a bundle.

#### `opencode-spec-validator.py`

Validates JSON configuration files against the OpenCode agent specification.

**Usage:**
```bash
python3 ops/scripts/opencode-spec-validator.py <config-file.json>
```

**Options:**
- `-q, --quiet` - Suppress output, only use exit code
- `--warnings-as-errors` - Treat warnings as validation errors

**Exit Codes:**
- `0` - Valid configuration
- `1` - Invalid configuration
- `2` - File error (not found, invalid JSON, etc.)

**Example:**
```bash
# Validate configuration
python3 ops/scripts/opencode-spec-validator.py opencode-config.json

# Quiet mode for scripts
python3 ops/scripts/opencode-spec-validator.py -q config.json
echo $?  # Check exit code
```

#### `convert-agents-to-opencode.py`

Converts agent markdown files from `.github/agents` to OpenCode JSON format.

**Usage:**
```bash
python3 ops/scripts/convert-agents-to-opencode.py [options]
```

**Options:**
- `-i, --input-dir PATH` - Agent files directory (default: `.github/agents`)
- `-o, --output PATH` - Output JSON file (default: `opencode-config.json`)
- `-v, --verbose` - Enable verbose logging
- `--validate` - Validate output using opencode-spec-validator.py

**Exit Codes:**
- `0` - Successful conversion
- `1` - Conversion errors occurred
- `2` - Validation failed (when `--validate` is used)

**Examples:**
```bash
# Convert with default settings
python3 ops/scripts/convert-agents-to-opencode.py

# Convert with validation and verbose output
python3 ops/scripts/convert-agents-to-opencode.py --validate --verbose

# Custom input/output paths
python3 ops/scripts/convert-agents-to-opencode.py \
  -i .github/agents \
  -o config/opencode.json \
  --validate
```

#### `github-issue-helpers.sh`

Shared Bash helpers for any workflow that needs to open GitHub issues via the `gh` CLI. Functions cover CLI discovery, CSV parsing for labels/assignees, and safe body loading from either inline text or companion files (e.g., `/work/collaboration/*.md`).

**Usage:**
```bash
#!/usr/bin/env bash
source ops/scripts/github-issue-helpers.sh

BODY="$(_github_issue::body_from_file work/collaboration/ISSUE_BODY.md)"
_github_issue::create \
  "sddevelopment-be/quickstart_agent-augmented-development" \
  "Automation request" \
  "$BODY" \
  "automation,ops" \
  "Copilot"
```

- `_github_issue::body_from_source "<fallback>" "<file>"` lets you keep a default body in the script while preferring the canonical markdown file if it exists.
- `_github_issue::create` normalizes comma-separated labels/assignees into repeated `gh --label/--assignee` arguments, warns about missing repository labels, and logs the action for observability.
- Missing labels trigger a warning recommending the forthcoming `gh label sync` helper so mismatched metadata can be resolved before retrying.

#### `create-github-issue.sh`

Thin CLI wrapper around the helpers for ad-hoc automation or CI usage.

**Usage:**
```bash
# From a local file
ops/scripts/create-github-issue.sh \
  --repo sddevelopment-be/quickstart_agent-augmented-development \
  --title "Document iteration automation" \
  --body-file work/collaboration/GITHUB_ISSUE_10_POST_IMPLEMENTATION_ANALYSIS.md \
  --label automation --label enhancement --assignee Copilot

# Or pipe a generated body via STDIN
generate_body | ops/scripts/create-github-issue.sh \
  --repo owner/repo \
  --title "Generated issue from pipeline" \
  --label pipeline
```

Flags mirror the native `gh issue create` parameters but make it easy to compose automation without repeating parsing/validation logic.

### `test-data/`

Test fixtures for validation:
- `valid-config.json` - Example of valid OpenCode configuration
- `invalid-config.json` - Example with validation errors

## OpenCode Specification

The scripts implement validation and conversion for the OpenCode agent configuration format.

### Schema Overview

```json
{
  "version": "string",
  "agents": [
    {
      "name": "string",
      "description": "string", 
      "instructions": "string (markdown content)",
      "tools": ["array", "of", "strings"]
    }
  ],
  "metadata": {
    "source": "string",
    "generated": "ISO timestamp",
    "generator": "string",
    "agent_count": 0
  }
}
```

**Required Fields:**
- Root level: `version`, `agents`
- Agent level: `name`, `description`, `instructions`

**Optional Fields:**
- Root level: `metadata`
- Agent level: `tools`, `model`, `capabilities`

### Agent File Format

Agent markdown files in `.github/agents/` must follow this structure:

```markdown
---
name: agent-identifier
description: Brief agent description
tools: ["tool1", "tool2", "tool3"]
---

# Agent Profile: Agent Name

[Markdown content with agent instructions]
```

The YAML frontmatter is parsed to extract metadata, and the markdown body becomes the agent's instructions.

## GitHub Actions Integration

The conversion process is automated via the `reusable-config-mapping` workflow.

**Workflow:** `.github/workflows/reusable-config-mapping.yml`

**Triggers:**
- Automatic: Changes to `.github/agents/**`
- Manual: Workflow dispatch with optional validation-only mode

**What it does:**
1. Detects changes to agent configuration files
2. Runs the conversion script
3. Validates the generated configuration
4. Commits changes if the configuration was updated
5. Provides summary of conversion results

**Manual Execution:**
```bash
# Via GitHub CLI
gh workflow run reusable-config-mapping.yml

# Validation only (no conversion)
gh workflow run reusable-config-mapping.yml -f validate_only=true
```

## Testing

### Test the Validator

```bash
# Valid configuration should pass
python3 ops/scripts/opencode-spec-validator.py ops/test-data/valid-config.json
# Exit code: 0

# Invalid configuration should fail with errors
python3 ops/scripts/opencode-spec-validator.py ops/test-data/invalid-config.json
# Exit code: 1
```

### Test the Converter

```bash
# Convert and validate
python3 ops/scripts/convert-agents-to-opencode.py \
  --input-dir .github/agents \
  --output /tmp/test-config.json \
  --validate \
  --verbose

# Check the output
cat /tmp/test-config.json
```

## Development

### Requirements

- Python 3.8+
- Standard library only (no external dependencies)

### Code Style

- PEP 8 compliant
- Type hints for public interfaces
- Comprehensive docstrings
- Clear error messages

### Adding New Validations

To add validation rules, edit `opencode-spec-validator.py`:

1. Update `OPENCODE_SCHEMA` dictionary
2. Add validation method to `OpenCodeValidator` class
3. Call new method from `validate()` method
4. Add test cases to `test-data/`

## Troubleshooting

### Conversion Issues

**Problem:** Agent file not converted
- Check YAML frontmatter syntax (must have `---` delimiters)
- Ensure required fields (`name`, `description`) are present
- Use `--verbose` flag to see detailed parsing logs

**Problem:** Invalid JSON output
- Check for special characters in descriptions/instructions
- Ensure frontmatter values are properly quoted

### Validation Issues

**Problem:** Validation fails after conversion
- Review error messages for specific field issues
- Check that all required fields are present
- Verify array fields (like `tools`) are properly formatted

**Problem:** Unknown field warnings
- These are informational only and don't cause validation failure
- Update `OPENCODE_SCHEMA` if new fields are part of the specification

## Portability Notes

The scripts are designed to be portable and vendor-neutral:

- **No vendor lock-in:** OpenCode format is standard across platforms
- **Pure Python:** No external dependencies beyond standard library
- **Configurable:** Easy to adapt for different agent formats
- **Extensible:** Schema can be updated as specification evolves

## Future Enhancements

Potential improvements:

- [ ] JSON Schema file for formal validation
- [ ] Support for additional metadata fields
- [ ] Multi-format export (YAML, TOML, etc.)
- [ ] Agent inheritance/composition
- [ ] Diff tool for configuration changes
- [ ] Interactive configuration editor

## Contributing

When modifying these scripts:

1. Maintain backward compatibility
2. Update test fixtures if schema changes
3. Document new features in this README
4. Test with actual agent files
5. Update workflow if script interface changes

## References

- OpenCode Specification: https://opencode.ai/config.json (when available)
- Agent Files: `.github/agents/*.agent.md`
- Workflow: `.github/workflows/reusable-config-mapping.yml`
