# Setup Validation Environment Action

**Agent:** DevOps Danny (Build Automation Specialist)  
**Created:** 2025-12-14  
**Purpose:** Provide a reusable composite action for setting up Node.js validation environment

## Description

This composite action sets up Node.js with dependency caching optimized for Markua validation and testing workflows. It's designed to be used by all agents and CI workflows that need to run validations.

## Features

- ✅ Node.js setup with configurable version
- ✅ npm dependency caching for faster builds
- ✅ Automatic dependency installation
- ✅ Optimized cache keys based on package-lock.json
- ✅ Fallback to `npm install` if package-lock.json missing
- ✅ Idempotent and safe to re-run

## Usage

### Basic Usage

```yaml
steps:
  - uses: actions/checkout@v4
  
  - name: Setup validation environment
    uses: ./.github/actions/setup-validation-env
  
  - name: Run validations
    run: |
      npm test
      npm run lint:markua
```

### With Custom Node Version

```yaml
steps:
  - uses: actions/checkout@v4
  
  - name: Setup validation environment
    uses: ./.github/actions/setup-validation-env
    with:
      node-version: '18'
```

### Skip Dependency Installation

```yaml
steps:
  - uses: actions/checkout@v4
  
  - name: Setup validation environment
    uses: ./.github/actions/setup-validation-env
    with:
      install-dependencies: 'false'
  
  - name: Install specific dependencies
    run: npm install --production
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to use | No | `'20'` |
| `cache-key-prefix` | Prefix for cache key | No | `'npm'` |
| `install-dependencies` | Whether to install npm dependencies | No | `'true'` |

## Outputs

None. This action sets up the environment for subsequent steps.

## Cache Strategy

The action caches:
- `~/.npm` - npm global cache
- `node_modules` - installed dependencies

Cache key: `{OS}-{prefix}-{hash(package-lock.json)}`

Restore keys (in order):
1. `{OS}-{prefix}-{hash(package-lock.json)}` (exact match)
2. `{OS}-{prefix}-` (prefix match, latest)
3. `{OS}-npm-` (fallback to any npm cache)

## Integration with Existing Workflows

This action is designed to work seamlessly with:
- `.github/workflows/spell-check.yml` - Manuscript validation workflow
- Local agent validation scripts
- Manual testing workflows

### Example: Update Existing Workflow

**Before:**
```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

- name: Install dependencies
  run: npm install
```

**After:**
```yaml
- name: Setup validation environment
  uses: ./.github/actions/setup-validation-env
```

## Testing Locally

Agents can test validation setup locally:

```bash
# Setup environment
cd /path/to/saboteurs
npm install

# Run validations
npm test              # Anchor validation
npm run lint:markua   # Markua syntax validation
```

## Maintenance

- Update Node.js version in `inputs.node-version.default` as needed
- Review cache strategy if dependencies grow significantly
- Monitor cache hit rates in CI logs
- Update documentation when adding new validation tools

## Related Documentation

- `docs/references/markua-notes.md` §11 - Anchor validation conventions
- `ops/scripts/test-markua-anchors.mjs` - Test suite documentation
- `ops/scripts/remark-lint-markua.mjs` - Linter documentation
- `.github/workflows/spell-check.yml` - Main validation workflow

## Compliance

✅ **Directive 007:** Authority confirmed for shared CI infrastructure  
✅ **Directive 016/017:** ATDD/TDD principles applied to action design  
✅ **Directive 018:** Documentation at appropriate level for maintenance  
✅ **ADR-011:** Follows Primer Execution Matrix for automation scripts

## Support

For issues or questions:
1. Check workflow logs for cache hit rates and performance
2. Verify `package.json` and `package-lock.json` are up to date
3. Review related documentation links above
4. Escalate to DevOps Danny if infrastructure changes needed
