# tools/ - Development Utilities

**Purpose:** Development-time tooling for building, testing, validating, and deploying the framework.

## Directory Structure

```
tools/
├── exporters/          # Export framework to tool-specific formats
│   ├── copilot/       # GitHub Copilot skill exporters
│   ├── claude/        # Claude skill exporters
│   └── opencode/      # OpenCode format exporters
├── validators/         # CI/CD validation scripts
│   ├── validate_task_schema.py
│   ├── validate_directives.sh
│   ├── validate_work_structure.sh
│   └── validate_task_naming.sh
├── scripts/            # Utility scripts & shell wrappers
│   ├── assemble-agent-context.sh
│   ├── load_directives.sh
│   └── template-status-checker.sh
├── dashboards/         # Development dashboards & monitoring
├── release/            # Release automation & packaging
└── README.md          # This file
```

## What Belongs Here

**Development-time utilities** - code that supports development but doesn't run in production:
- **Exporters:** Convert framework definitions to tool-specific formats (Copilot, Claude, Cursor)
- **Validators:** Schema validation, linting, structure checks for CI/CD
- **Scripts:** Build automation, convenience wrappers, deployment helpers
- **Dashboards:** Development-time monitoring and metrics visualization
- **Release tooling:** Packaging, versioning, distribution automation

## What Does NOT Belong Here

- **Production code** → `src/` (runtime orchestration, framework core)
- **Tests** → `tests/` (unit tests, integration tests)
- **Test fixtures** → `fixtures/` (example data for tests)
- **Framework definitions** → `doctrine/` (agents, directives, approaches)
- **Documentation** → `docs/` or `doctrine/docs/`

## Key Principle

> **If it only runs during development, testing, or deployment (not in production), it belongs in `tools/`.**  
> **If production code imports it, it belongs in `src/`.**

## Examples

✅ **Belongs in tools/**
- `tools/exporters/copilot/copilot-exporter.py` - Generates Copilot skill files
- `tools/validators/validate_task_schema.py` - Validates YAML during CI
- `tools/scripts/assemble-agent-context.sh` - Convenience wrapper for context assembly
- `tools/release/bump-version.sh` - Automates version bumping

❌ **Does NOT belong in tools/**
- Runtime orchestration logic → `src/framework/orchestration/`
- Framework abstractions → `src/framework/core/`
- Test suites → `tests/`
- Agent profiles → `doctrine/agents/`

## Usage Patterns

### Exporters
```bash
# Generate Copilot skills from doctrine/
python tools/exporters/copilot/copilot-exporter.py

# Export to Claude format
node tools/exporters/claude/claude-exporter.js
```

### Validators
```bash
# Validate task YAML schema
python tools/validators/validate_task_schema.py work/collaboration/**/*.yaml

# Check work directory structure
bash tools/validators/validate_work_structure.sh
```

### Scripts
```bash
# Assemble agent context (shell wrapper)
bash tools/scripts/assemble-agent-context.sh architect-alphonso

# Check template status
bash tools/scripts/template-status-checker.sh
```

## Import Guidelines

Tools may:
- Import from `src/` (read production code, generate exports)
- Import from `doctrine/` (read framework definitions)
- Import from `fixtures/` (for testing validators)
- Import from `tests/` (for test utilities, though rare)

Tools typically:
- Run as standalone scripts (not imported by production code)
- Execute via CLI, npm scripts, or CI pipelines
- Generate artifacts consumed by external tools

## CI/CD Integration

Tools are invoked by CI/CD pipelines:
```yaml
# .github/workflows/validate.yml
- name: Validate schemas
  run: python tools/validators/validate_task_schema.py work/**/*.yaml

- name: Export Copilot skills
  run: node tools/exporters/copilot/export-all.js
```

## Related Documentation

- Production code: `src/README.md`
- Framework definitions: `doctrine/DOCTRINE_MAP.md`
- CI/CD workflows: `.github/workflows/`
