# Maintenance Scripts

Automated maintenance scripts for the agent-augmented development framework.

## Overview

This directory contains scripts that automate routine maintenance tasks, ensuring consistency and reducing manual overhead in framework management.

## Scripts

### update_directives_manifest.py

Maintains the directives manifest.json file by scanning the directives directory and ensuring all directive files are properly registered with correct metadata.

**Purpose:**
- Prevent manifest drift as new directives are added
- Detect orphaned manifest entries
- Validate metadata consistency (code, slug, filename match)
- Support both validation and auto-fix modes
- Provide CI-ready exit codes

**Usage:**

```bash
# Validate manifest (report only, exit non-zero if issues found)
python -m ops.scripts.maintenance.update_directives_manifest

# Validate with explicit dry-run mode
python -m ops.scripts.maintenance.update_directives_manifest --dry-run

# Auto-fix discrepancies
python -m ops.scripts.maintenance.update_directives_manifest --fix

# Specify custom directives directory
python -m ops.scripts.maintenance.update_directives_manifest \
  --directives-dir /path/to/directives
```

**Features:**
- ✅ Scans `.github/agents/directives/` for numbered directive files (`NNN_slug.md`)
- ✅ Validates manifest entries against actual files
- ✅ Detects missing directives (file exists, no manifest entry)
- ✅ Detects orphaned entries (manifest entry, no file)
- ✅ Validates metadata consistency (code, slug, filename match)
- ✅ `--dry-run` mode: report only, no changes
- ✅ `--fix` mode: auto-update manifest
- ✅ Exit codes: 0 for success, 1 for validation failures (CI-ready)
- ✅ Comprehensive error messages with actionable suggestions

**CI Integration:**

Add to your CI pipeline to ensure manifest stays in sync:

```yaml
- name: Validate directives manifest
  run: python -m ops.scripts.maintenance.update_directives_manifest
```

**Output Examples:**

Valid manifest:
```
🔍 Validating manifest...

✅ Manifest is valid - all directives are properly registered.
```

Issues found:
```
🔍 Validating manifest...

❌ Manifest validation failed:

📄 Missing Manifest Entries (1):
  - 024_self_observation_protocol.md (file exists but no manifest entry)

⚠️  Metadata Inconsistencies (1):
  - 012_operating_procedures.md:
    • Slug mismatch: filename has 'operating_procedures', manifest has 'common_operating_procedures'

💡 Resolution:
  Run with --fix to automatically update the manifest
```

Fixing issues:
```
🔧 Fixing manifest discrepancies...
📝 Adding 1 missing entries...
✅ Manifest updated: .github/agents/directives/manifest.json

✅ Manifest is valid - all directives are properly registered.
```

## Testing

Both unit tests and acceptance tests are provided following Directives 016 (ATDD) and 017 (TDD):

```bash
# Run all maintenance script tests
pytest validation/maintenance/

# Run unit tests only
pytest validation/maintenance/test_directives_manifest_unit.py

# Run acceptance tests only
pytest validation/maintenance/test_directives_manifest_acceptance.py

# Run with coverage
pytest validation/maintenance/ --cov=ops.scripts.maintenance --cov-report=html
```

## Development Guidelines

When creating new maintenance scripts:

1. **Follow TDD/ATDD**: Write acceptance tests first (Directive 016), then unit tests (Directive 017)
2. **Document thoroughly**: Include comprehensive docstrings and usage examples (Directive 018)
3. **Make scripts idempotent**: Safe to run multiple times without side effects
4. **Provide dry-run modes**: Allow validation without changes
5. **Return proper exit codes**: 0 for success, non-zero for failures (CI-ready)
6. **Generate clear reports**: Human-readable output with actionable suggestions
7. **Handle edge cases**: Missing files, invalid JSON, permission errors, etc.
8. **Add to this README**: Document new scripts and their usage

## Contributing

Maintenance scripts should:
- Be standalone Python modules (runnable with `python -m`)
- Include comprehensive test coverage (>90%)
- Follow project code style (black, ruff)
- Support both CLI and programmatic usage
- Be documented in this README

## Related Documentation

- [Directive 016: ATDD](/.github/agents/directives/016_acceptance_test_driven_development.md)
- [Directive 017: TDD](/.github/agents/directives/017_test_driven_development.md)
- [Directive 018: Traceable Decisions](/.github/agents/directives/018_traceable_decisions.md)
- [Directive 014: Work Log Creation](/.github/agents/directives/014_worklog_creation.md)
