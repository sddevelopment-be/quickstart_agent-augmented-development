---
packaged: true
audiences: [software_engineer, automation_agent, process_architect, devops_engineer]
note: Contains CI/CD tooling and error reporting infrastructure.
---

# Tools & Scripts

This directory contains operational scripts and tooling for the repository.

## Error Reporting System

**NEW - Agent-Friendly Error Reporting**

### `generate-error-summary.py`
Python script that generates structured error reports from validation output.

**Features:**
- Parses validation errors into structured JSON
- Generates human-readable Markdown summaries
- Emits GitHub Actions annotations
- Provides actionable fix suggestions

**Usage:**
```bash
python generate-error-summary.py \
  --workflow "Validation" \
  --job "validate" \
  --validator "task-schema" \
  --input validation_output.txt \
  --output-json errors.json \
  --output-markdown errors.md \
  --emit-annotations \
  --fail-on-errors
```

**Documentation:** See [docs/error-reporting-system.md](../../docs/error-reporting-system.md)

### `generate-error-summary.sh`
Shell wrapper for `generate-error-summary.py` with sensible defaults.

**Usage:**
```bash
bash generate-error-summary.sh \
  --workflow "Validation" \
  --job "validate" \
  --validator "task-schema" \
  --input validation_output.txt
```

**Quick Reference:** See [docs/error-reporting-quick-reference.md](../../docs/error-reporting-quick-reference.md)

## Task Management Scripts

Scripts for managing task lifecycle in the orchestration system:

- `start_task.py` - Create and assign new tasks
- `complete_task.py` - Mark tasks as complete
- `freeze_task.py` - Archive completed tasks
- `list_open_tasks.py` - List pending tasks
- `validate-task.sh` - Validate task YAML files

**Documentation:** See [README_TASK_MANAGEMENT.md](README_TASK_MANAGEMENT.md)

## CI/CD & Validation Scripts

- `assemble-agent-context.sh` - Build agent context for execution
- `load_directives.sh` - Load directive files
- `template-status-checker.sh` - Check template status
- `validate-model-router.py` - Validate model routing configuration
- `validate-doctrine-dependencies.sh` - Check doctrine dependency rules
- `validate-src-dependencies.sh` - Validate source dependencies

## Deployment Scripts

- `deploy-skills.js` - Deploy agent skills
- `skills-exporter.js` - Export skills definitions

## Maintenance Scripts

See `maintenance/` subdirectory for:
- Directive manifest updates
- Repository maintenance tasks
- Cleanup utilities

## Planning Scripts

See `planning/` subdirectory for:
- Task planning utilities
- Workflow generation

## Related Directories

- **Validators:** `tools/validators/` - Validation rules and schemas
- **Actions:** `.github/actions/` - Reusable GitHub Actions
- **Workflows:** `.github/workflows/` - CI/CD workflows
- **Examples:** `examples/error-reports/` - Example error outputs

## Best Practices

### For Script Authors

1. Include docstring with purpose and usage
2. Use consistent error output format (❌, ⚠️, ❗️)
3. Return appropriate exit codes (0=success, 1=error)
4. Write to stderr for errors, stdout for output
5. Support `--help` flag

### For Workflow Integration

1. Capture both stdout and stderr: `2>&1 | tee output.txt`
2. Use `continue-on-error: true` for validation steps
3. Generate error reports for failures
4. Upload artifacts for agent access
5. Update PR comments with results

## Testing

Run integration tests:
```bash
bash tests/test_error_reporting_integration.sh
```

## Support

For questions or issues:
1. Review script documentation and examples
2. Check workflow runs for usage patterns
3. Consult [DevOps Danny](.github/agents/devops_danny.agent.md) for CI/CD questions
4. Review related documentation in `docs/`

---

*Last updated: 2025-02-11 by DevOps Danny*
