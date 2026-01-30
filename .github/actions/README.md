# GitHub Actions - Reusable Actions

**Maintained by:** DevOps Danny (Build Automation Specialist)  
**Purpose:** Provide composable, reusable actions for CI/CD and agent workflows

## Available Actions

### 1. setup-validation-env

**Location:** `.github/actions/setup-validation-env/`  
**Purpose:** Setup Node.js environment for Markua validation and testing

**Quick Start:**
```yaml
- uses: ./.github/actions/setup-validation-env
```

**Documentation:** [setup-validation-env/README.md](./setup-validation-env/README.md)

### 2. setup-python-env

**Location:** `.github/actions/setup-python-env/`  
**Purpose:** Setup Python environment for orchestration and validation scripts

**Quick Start:**
```yaml
- uses: ./.github/actions/setup-python-env
```

## Usage for Agents

### Running Validations Locally

Before committing changes, agents should run validations locally:

```bash
# Setup environment (first time only)
npm install

# Run all validations
npm test              # Anchor validation (checks crosslinks across entire manuscript)
npm run lint:markua   # Syntax validation (per-file Markua syntax check)
npm run spell         # Spell check (all files)

# Run targeted validations
npm run spell:manuscript  # Spell check manuscript only
npm run test:anchors      # Anchor validation only
```

### Understanding Validation Tools

| Tool | What It Validates | Scope | Use When |
|------|-------------------|-------|----------|
| `npm test` | Crosslink anchors exist | All files | Before committing manuscript changes |
| `npm run lint:markua` | Markua syntax | Per file | Checking syntax errors |
| `npm run spell` | Spelling | All files | Before committing any text |

**Key Difference:** 
- `npm test` validates that anchor targets exist (e.g. `[#t](#crisis_over_prevention)` links to a file with `{#crisis_over_prevention}`)
- `npm run lint:markua` validates syntax only (e.g. proper token usage, link format)

### CI/CD Workflows

The repository includes automated workflows:

1. **validate-manuscript.yml** - Runs on PR/push, validates anchors and syntax
2. **spell-check.yml** - Runs on PR, validates spelling and Markua syntax

Both workflows use the `setup-validation-env` action for consistency.

## Creating New Actions

When creating new reusable actions:

1. Create directory: `.github/actions/your-action-name/`
2. Add `action.yml` with proper inputs/outputs
3. Add `README.md` with usage documentation
4. Test locally before committing
5. Update this index

### Action Template

```yaml
name: 'Your Action Name'
description: 'Brief description'
inputs:
  your-input:
    description: 'Input description'
    required: false
    default: 'default-value'

runs:
  using: 'composite'
  steps:
    - name: Step name
      shell: bash
      run: |
        echo "Your script here"
```

## Best Practices

### For Action Authors (DevOps Danny)

- ✅ Make actions idempotent (safe to re-run)
- ✅ Provide sensible defaults
- ✅ Document all inputs and outputs
- ✅ Use composite actions for multi-step setups
- ✅ Cache dependencies appropriately
- ✅ Include error handling and logging
- ✅ Test with different Node.js/Python versions
- ✅ Follow SDD Agentic Framework directives

### For Action Users (All Agents)

- ✅ Always run validations before committing
- ✅ Check workflow logs when CI fails
- ✅ Use the same Node.js version locally as CI (v20)
- ✅ Report infrastructure issues to DevOps Danny
- ✅ Suggest improvements via PRs

## Troubleshooting

### Validation Failures

**Problem:** `npm test` fails with broken crosslinks  
**Solution:** 
1. Run `npm test` locally to see which anchors are missing
2. Check if the anchor exists in the target file
3. Update reference to use correct anchor ID
4. See `docs/references/markua-notes.md` §11 for conventions

**Problem:** `npm run lint:markua` shows warnings  
**Solution:**
1. Run locally to see specific line numbers
2. Check Markua syntax (tokens, format, etc.)
3. Ensure smart crosslinks use proper tokens (`#t`, `#n`, etc.)

**Problem:** Cache not working in CI  
**Solution:**
1. Check if `package-lock.json` is committed
2. Verify cache keys in action logs
3. Contact DevOps Danny if persistent issues

### Permission Errors

Actions run with repository permissions. If you encounter permission errors:
1. Verify action is in `.github/actions/` directory
2. Check workflow file uses correct relative path
3. Ensure composite action has proper `shell: bash` directives

## Related Documentation

- `docs/references/markua-notes.md` - Markua conventions and crosslink rules
- `ops/scripts/README.md` - Validation script documentation (if exists)
- `.github/workflows/README.md` - Workflow documentation (if exists)

## Maintenance

Actions should be reviewed:
- When Node.js/Python versions are updated
- When new validation tools are added
- When dependency management changes
- Quarterly for security updates

**Current versions:**
- Node.js: 20
- Python: 3.10
- npm: (managed by Node.js)

## Support

For issues with actions or workflows:
1. Check workflow logs in GitHub Actions tab
2. Test locally with same environment
3. Review action README files
4. Contact DevOps Danny for infrastructure help
5. Create issue with `ci-cd` label if needed

---

**Last updated:** 2026-01-29 by DevOps Danny  
**Compliance:** Directive 007 ✓, ADR-011 ✓, ADR-012 ✓
