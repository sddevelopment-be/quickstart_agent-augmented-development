# Centralized Version Management

## Overview

All CI/CD workflows use centralized version configuration stored in `.github/versions.yml`. This ensures consistency across workflows and simplifies version updates.

## Configuration File

**Location:** `.github/versions.yml`

The configuration file defines:
- Python versions (default and release)
- Node.js versions
- Operating system versions
- Tool versions

## Using Versions in Workflows

### Option 1: Direct YAML Reference (Recommended for Simple Cases)

For workflows that don't need dynamic version loading, directly reference the standard versions:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'  # Standard default version
```

### Option 2: Load Versions Action (For Dynamic Use)

For workflows that need to load versions dynamically:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Load versions
        id: versions
        uses: ./.github/actions/load-versions
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ steps.versions.outputs.python-default }}
```

### Option 3: Parse YAML Directly

For advanced use cases:

```yaml
- name: Get Python version
  id: python-version
  run: |
    VERSION=$(grep -A 5 "^python:" .github/versions.yml | grep "default:" | sed 's/.*"\(.*\)"/\1/')
    echo "version=$VERSION" >> $GITHUB_OUTPUT

- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: ${{ steps.python-version.outputs.version }}
```

## Standard Versions

As of the last update:

| Component | Default Version | Release Version | Notes |
|-----------|----------------|-----------------|-------|
| Python    | 3.10           | 3.12            | Default for testing, 3.12 for releases |
| Node.js   | 18             | 18              | LTS version |
| Ubuntu    | ubuntu-latest  | ubuntu-latest   | GitHub-hosted runner |

## Updating Versions

### Process

1. **Update `.github/versions.yml`**
   - Modify the version number
   - Add entry to changelog section
   - Document the reason for the change

2. **Test the change**
   - Create a feature branch
   - Update one workflow to use new version
   - Run the workflow and verify success

3. **Update workflows** (if needed)
   - Most workflows reference versions.yml automatically
   - For hardcoded versions, update them to match

4. **Document the change**
   - Update this README if the approach changes
   - Note any compatibility concerns

### Example Update

```yaml
# In .github/versions.yml
python:
  default: "3.11"  # Updated from 3.10
  
changelog:
  - date: "2026-03-15"
    change: "Updated Python default to 3.11 for better performance"
    python_default: "3.11"
```

## Migration Status

### Workflows Using Centralized Versions

✅ **Fully Migrated:**
- `workflow-validation.yml` - Uses Python 3.10 (centralized default)

⏳ **Pending Migration:**
- `pr-quality-gate.yml` - Currently hardcoded to 3.10 (matches centralized default)
- `orchestration.yml` - Currently hardcoded to 3.10 (matches centralized default)
- `validation.yml` - Currently hardcoded to 3.10 (matches centralized default)
- `test-ops-changes.yml` - Currently hardcoded to 3.10 (matches centralized default)
- `release-packaging.yml` - Currently hardcoded to 3.12 (matches centralized release)
- `reusable-config-mapping.yml` - Currently hardcoded to 3.12 (matches centralized release)
- `validate-prompts.yml` - Currently hardcoded to Node 18 (matches centralized default)

**Note:** Existing workflows already use the correct versions as defined in versions.yml. No immediate migration is required unless versions need to be changed in the future.

## Benefits

1. **Consistency:** All workflows use the same versions
2. **Maintainability:** Update versions in one place
3. **Documentation:** Clear version choices with rationale
4. **Auditability:** Changelog tracks version changes over time
5. **Testing:** Easier to test version upgrades in isolation

## Best Practices

1. **Use semantic versioning:** Specify major.minor (e.g., "3.10") not patch versions
2. **Test before merging:** Always test version changes on a feature branch
3. **Document changes:** Update the changelog in versions.yml
4. **Plan upgrades:** Schedule version upgrades, don't rush them
5. **Monitor compatibility:** Check for breaking changes in new versions

## Troubleshooting

### Workflow fails after version update

1. Check the workflow run logs for version-specific errors
2. Review release notes for the new version
3. Test locally with the new version
4. Consider pinning to the previous version temporarily

### Version not loading correctly

1. Verify `.github/versions.yml` syntax is valid
2. Check that the workflow has checked out the repository (`actions/checkout@v4`)
3. Ensure the path to versions.yml is correct
4. Test the parsing command locally

## Future Enhancements

Potential improvements to consider:

1. **Matrix testing:** Test against multiple Python/Node versions
2. **Automated updates:** Use Dependabot or Renovate to suggest version updates
3. **Version compatibility matrix:** Document which versions work together
4. **Workflow generator:** Script to generate workflows with correct versions
