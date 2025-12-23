# Manifest Maintenance Guide

## Overview

The `META/MANIFEST.yml` file is the single source of truth for the Agent-Augmented Development Framework. It catalogs all framework-managed files, their checksums, and sync modes, enabling automated installation, upgrades, and integrity validation.

**Purpose:**
- Define which files belong to the framework core
- Enable Framework Guardian to detect drift and conflicts
- Support automated install/upgrade operations
- Provide checksums for integrity verification

**Key Consumers:**
- `ops/scripts/framework_install.sh` - First-time framework installation
- `ops/scripts/framework_upgrade.sh` - Framework version upgrades
- Framework Guardian Agent - Drift detection and validation
- Distribution packaging scripts - Release bundle creation

## File Structure

```yaml
framework:
  name: "quickstart-agent-augmented-development"
  version: "0.1.0"              # Semantic version
  release_date: "2025-12-23"    # ISO date format
  
paths:                           # Directory-level entries
  - path: ".github/agents"
    mode: sync-always
    description: "..."

files:                           # Individual file entries
  - path: ".github/agents/framework-guardian.agent.md"
    checksum: "sha256:abc123..."
    mode: sync-always
    description: "..."

tooling:                         # Framework automation scripts
  - script: "ops/scripts/framework_install.sh"
    purpose: "..."
    mode: sync-always
```

## Sync Modes

### sync-always
Files that should track framework updates closely. Projects should rarely diverge from these.

**Examples:**
- `.github/agents/` - Agent profiles and directives
- `docs/templates/` - Canonical templates
- `validation/` - Validation framework
- `ops/scripts/framework_*.sh` - Install/upgrade scripts

**Upgrade behavior:** Always overwrite with framework version

### copy-once
Initial scaffold files that projects are expected to customize.

**Examples:**
- `work/README.md` - Orchestration guide (can be adapted)
- `REPO_MAP.md` - Repository structure (project-specific)

**Upgrade behavior:** Only copy if file doesn't exist; preserve existing

### reference-only
Informational documentation about the framework itself.

**Examples:**
- Framework overview documents
- Architecture decision records about framework design

**Upgrade behavior:** Available for reference but not enforced

## Generation Workflow

### Automated Generation

Generate manifest from current repository structure:

```bash
# Auto-detect version from pyproject.toml
cd /path/to/repository
ops/scripts/generate_manifest.sh

# Specify custom version
ops/scripts/generate_manifest.sh --version 1.2.0

# Preview without writing file
ops/scripts/generate_manifest.sh --dry-run

# Custom output location
ops/scripts/generate_manifest.sh --output /tmp/manifest.yml --version 1.0.0
```

### When to Regenerate

**Always regenerate when:**
1. Adding new framework files (agents, templates, directives)
2. Removing framework files
3. Moving/renaming framework files
4. Preparing a new framework release

**Do NOT regenerate for:**
- Project-specific task files in `work/`
- Temporary files in `tmp/` or `local/`
- Test outputs or build artifacts

### Pre-Release Checklist

Before creating a framework release:

1. **Update version in `pyproject.toml`**
   ```bash
   # Edit version field
   vim pyproject.toml
   ```

2. **Regenerate manifest**
   ```bash
   ops/scripts/generate_manifest.sh
   ```

3. **Validate manifest structure**
   ```bash
   # YAML validation happens automatically
   # Check output for "✅ YAML validation passed"
   ```

4. **Review changes**
   ```bash
   git diff META/MANIFEST.yml
   # Verify:
   # - New files are included
   # - Removed files are excluded
   # - Checksums updated
   # - Version bumped correctly
   ```

5. **Run tests**
   ```bash
   ops/scripts/tests/test_manifest_generation.sh
   ```

6. **Commit manifest**
   ```bash
   git add META/MANIFEST.yml
   git commit -m "chore: update manifest for v${VERSION}"
   ```

## Understanding Checksums

Checksums enable integrity verification:

```yaml
checksum: "sha256:f0e8561405510b5bdee9eeed28a16ce0a4c97ec22f65b27221a1a1c627ec09e9"
```

**Purpose:**
- Detect file corruption during distribution
- Verify successful file transfers
- Detect unauthorized modifications
- Support diff-based upgrades

**Generation:**
- Uses `sha256sum` (Linux) or `shasum -a 256` (macOS)
- Calculated during manifest generation
- Automatically updated when files change

## Customization

### Adding New Framework Paths

Edit `generate_manifest.sh` to include additional directories:

```bash
# In CORE_PATHS array
CORE_PATHS=(
    # ... existing entries ...
    "new/framework/directory:sync-always:Description of directory"
)
```

### Adding Specific Files

For files that need explicit metadata:

```bash
# In SPECIFIC_FILES array
SPECIFIC_FILES=(
    # ... existing entries ...
    "path/to/special/file.md:sync-always:Special file description"
)
```

### Excluding Paths

To prevent directories from being scanned:

```bash
# In EXCLUDE_PATTERNS array
EXCLUDE_PATTERNS=(
    # ... existing entries ...
    "new/excluded/pattern"
)
```

## Troubleshooting

### Manifest validation fails

```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('META/MANIFEST.yml'))"

# Or with yq (if installed)
yq eval '.' META/MANIFEST.yml
```

### Missing files in manifest

1. Check file exists in repository
2. Verify path not in `EXCLUDE_PATTERNS`
3. Ensure parent directory in `CORE_PATHS` or file in `SPECIFIC_FILES`
4. Regenerate manifest: `ops/scripts/generate_manifest.sh`

### Checksum mismatches

Framework Guardian may report checksum mismatches:

```
⚠️  Checksum mismatch: .github/agents/AGENTS.md
Expected: sha256:abc123...
Found:    sha256:def456...
```

**Diagnosis:**
1. File was modified locally (legitimate customization or drift)
2. Manifest is outdated (regenerate needed)
3. File corruption (rare)

**Resolution:**
- If file should match framework: restore from framework source
- If legitimate local change: document in `.framework_meta.yml` 
- If manifest outdated: regenerate manifest

### Script not executable

```bash
chmod +x ops/scripts/generate_manifest.sh
```

### Wrong version in manifest

Ensure `pyproject.toml` has correct version:

```toml
[tool.poetry]
name = "quickstart-agent-augmented-development"
version = "1.2.0"  # Update this
```

Or specify version explicitly:

```bash
ops/scripts/generate_manifest.sh --version 1.2.0
```

## Integration with Release Workflow

### Manual Release Process

1. Update version in `pyproject.toml`
2. Run `ops/scripts/generate_manifest.sh`
3. Review and commit `META/MANIFEST.yml`
4. Create git tag: `git tag -a v1.2.0 -m "Release 1.2.0"`
5. Push tag: `git push origin v1.2.0`

### Automated CI/CD Integration (Future)

```yaml
# Example GitHub Actions workflow
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    steps:
      - uses: actions/checkout@v3
      - name: Generate manifest
        run: ops/scripts/generate_manifest.sh
      - name: Validate manifest
        run: ops/scripts/tests/test_manifest_generation.sh
      - name: Create release bundle
        run: |
          mkdir -p dist
          zip -r dist/framework-${{ github.ref_name }}.zip \
            .github/agents docs/templates validation \
            ops/scripts META/MANIFEST.yml
```

## Framework Guardian Integration

The Framework Guardian Agent uses the manifest to:

1. **Detect Drift:** Compare installed files against manifest checksums
2. **Identify Conflicts:** Find local modifications to sync-always files
3. **Plan Upgrades:** Determine which files need updating
4. **Validate Integrity:** Verify no corruption or tampering

**Guardian Commands:**
```bash
# Audit current installation
/audit-framework

# Check for available upgrades
/check-upgrade

# Generate upgrade plan
/plan-upgrade --target-version 1.2.0
```

## Best Practices

1. **Always regenerate before releases** - Ensures manifest accuracy
2. **Test after regeneration** - Run test suite to verify correctness
3. **Review changes carefully** - Check git diff before committing
4. **Keep version in sync** - Match `pyproject.toml` and manifest
5. **Document custom exclusions** - Add comments to generation script
6. **Validate YAML structure** - Use Python or yq to check syntax
7. **Version control manifest** - Track changes with meaningful commits

## Related Documentation

- **ADR-013:** Zip-Based Framework Distribution
- **ADR-014:** Framework Guardian Agent
- **Technical Design:** `docs/architecture/design/distribution_of_releases_technical_design.md`
- **Install Script:** `ops/scripts/framework_install.sh`
- **Upgrade Script:** `ops/scripts/framework_upgrade.sh`
- **Test Suite:** `ops/scripts/tests/test_manifest_generation.sh`

## Version History

| Date       | Version | Changes                                |
|------------|---------|----------------------------------------|
| 2025-12-23 | 1.0.0   | Initial manifest maintenance guide     |

---

**Maintained by:** DevOps Danny (Build Automation Specialist)  
**Last updated:** 2025-12-23  
**Status:** Active
