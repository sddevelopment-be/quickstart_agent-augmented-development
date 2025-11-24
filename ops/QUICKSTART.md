# Quick Start Guide: OpenCode Configuration Mapping

## What This Does

Automatically converts agent markdown files from `.github/agents/` to OpenCode JSON format for vendor-neutral portability.

## Files Overview

| File | Purpose |
|------|---------|
| `ops/scripts/opencode-spec-validator.py` | Validates OpenCode JSON configs |
| `ops/scripts/convert-agents-to-opencode.py` | Converts agent markdown to JSON |
| `ops/scripts/github-issue-helpers.sh` | Common Bash helpers for `gh issue create` |
| `ops/scripts/create-github-issue.sh` | CLI wrapper for reusable issue creation |
| `.github/workflows/reusable-config-mapping.yml` | Automates conversion on changes |
| `opencode-config.json` | Generated OpenCode configuration |

## Quick Usage

### Validate Configuration
```bash
python3 ops/scripts/opencode-spec-validator.py opencode-config.json
```

### Convert Agents
```bash
# Basic conversion
python3 ops/scripts/convert-agents-to-opencode.py

# With validation
python3 ops/scripts/convert-agents-to-opencode.py --validate --verbose
```

### Manual Workflow Trigger
```bash
# Using GitHub CLI
gh workflow run reusable-config-mapping.yml

# Validation only (no conversion)
gh workflow run reusable-config-mapping.yml -f validate_only=true
```

## Automatic Behavior

The workflow automatically runs when:
- Any file in `.github/agents/` is modified
- You manually trigger it via GitHub UI or CLI

It will:
1. Convert all agent markdown files to OpenCode JSON
2. Validate the generated configuration
3. Commit changes if the configuration was updated
4. Skip commit if no changes detected (idempotent)

## Testing

```bash
# Test validator with valid config
python3 ops/scripts/opencode-spec-validator.py ops/test-data/valid-config.json
# Exit: 0 ✅

# Test validator with invalid config
python3 ops/scripts/opencode-spec-validator.py ops/test-data/invalid-config.json
# Exit: 1 ❌ (5 errors reported)

# Test full conversion
python3 ops/scripts/convert-agents-to-opencode.py --validate
# Should convert 15 agents and pass validation
```

## GitHub Issue Automation

The operations toolbox also exposes reusable GitHub issue helpers that power `work/scripts/create-follow-up-issues.sh` and any bespoke automation.

### Create from Markdown
```bash
ops/scripts/create-github-issue.sh \
  --repo sddevelopment-be/quickstart_agent-augmented-development \
  --title "Documentation & Tooling Enhancements (Issue #8 Follow-Up)" \
  --body-file work/collaboration/GITHUB_ISSUE_9_DOCUMENTATION_TOOLING.md \
  --label documentation --label tooling --assignee Copilot
```

### Pipe Generated Content
```bash
cat <<'EOF' | ops/scripts/create-github-issue.sh \
  --repo owner/repo \
  --title "Automated follow-up" \
  --label automation --label enhancement
Please triage the follow-up work that dropped out of the last iteration.
EOF
```

Both examples lean on `ops/scripts/github-issue-helpers.sh` for dependency checks, CSV parsing for labels/assignees, and consistent logging before calling `gh issue create`.
If any requested labels are missing from the repository, the helper warns and suggests running the upcoming `gh label sync` utility before retrying.

## Current Status

✅ **15 agents** successfully converted to OpenCode format
✅ **Validation passing** - configuration is syntactically correct
✅ **Workflow ready** - will execute on next agent file change

## Troubleshooting

**Problem:** Validation fails after conversion
```bash
# Run with verbose output to see details
python3 ops/scripts/convert-agents-to-opencode.py --validate --verbose
```

**Problem:** Agent file not converted
- Check YAML frontmatter has `---` delimiters
- Ensure `name` and `description` fields are present
- View logs with `--verbose` flag

**Problem:** Workflow doesn't trigger
- Ensure changes are in `.github/agents/` directory
- Check workflow file permissions in GitHub UI
- View workflow runs in Actions tab

## For More Information

See `ops/README.md` for comprehensive documentation including:
- Detailed script options
- OpenCode schema specification
- Agent file format requirements
- Development guidelines
- Security considerations

## Next Steps

After merging this PR:
1. Any changes to agent files will automatically update `opencode-config.json`
2. The OpenCode config can be used by any compatible tooling
3. No vendor lock-in - configuration is portable across platforms

---

**Agent:** DevOps Danny (Build Automation Specialist)  
**Version:** 1.0.0  
**Date:** 2025-11-16
