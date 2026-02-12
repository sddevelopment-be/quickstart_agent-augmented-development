# DDR-008: Framework Distribution and Upgrade Mechanisms

**Status:** Active  
**Date:** 2026-02-11  
**Supersedes:** Repository-specific distribution implementations (elevated from ADR-013)

---

## Context

Agent-augmented development frameworks must be distributed to consuming repositories without forcing dependencies on:
- Git history rewriting or submodule complexity
- Specific hosting platforms (GitHub, GitLab, Bitbucket)
- Network availability (air-gapped environments)
- Advanced Git workflows (rebasing, cherry-picking)

Consumers span diverse environments:
- Public cloud repositories (GitHub, GitLab)
- On-premise Git installations
- File shares and USB distribution
- Environments with restricted internet access

Additionally, the framework must respect the **core vs. local boundary**:
- **Core framework:** Agent profiles, directives, guidelines, templates, validation
- **Local customizations:** Project-specific agents, repository ADRs, tooling, configurations

Upgrades must not overwrite local customizations, while still allowing adopters to receive framework improvements.

## Decision

**We establish zip-based framework distribution as the standard packaging and upgrade mechanism, with scripted installation respecting the core/local boundary.**

### Distribution Package Structure

Every framework release is packaged as: `<framework-name>-<version>.zip`

**Contents:**

```
<framework-name>-<version>.zip
│
├── framework_core/              # Curated framework files
│   ├── agents/
│   │   ├── directives/          # Core directives
│   │   ├── profiles/            # Standard agent profiles
│   │   └── guidelines/          # Framework guidelines
│   ├── templates/               # Templates for ADRs, tasks, etc.
│   ├── validation/              # Validation scripts
│   └── work/                    # Scaffolding (empty directories)
│
├── scripts/
│   ├── framework_install.sh     # Initial installation script
│   ├── framework_upgrade.sh     # Upgrade script (safe merging)
│   └── framework_validate.sh    # Post-install validation
│
└── META/
    ├── MANIFEST.yml             # File inventory with checksums
    ├── RELEASE_NOTES.md         # Version release notes
    └── UPGRADE_GUIDE.md         # Migration guidance for breaking changes
```

### Installation Protocol

**Initial installation:**

1. Unzip package anywhere
2. Run `scripts/framework_install.sh` with target repository path
3. Script copies `framework_core/` to repository (respecting `.gitignore`)
4. Creates `.framework_meta.yml` in repository root with version metadata
5. Initializes work directory structure if not present

**Upgrade:**

1. Unzip new version package
2. Run `scripts/framework_upgrade.sh` with repository path
3. Script compares installed version (from `.framework_meta.yml`) with new version
4. Copies changed files, creates `.framework-new` files for conflicts
5. Updates `.framework_meta.yml` with new version
6. Generates upgrade report

### Core vs. Local Boundary

**Framework-managed paths (safe to overwrite on upgrade):**
- `agents/directives/` (core directives)
- `agents/profiles/` (standard agent profiles)
- `agents/guidelines/` (framework guidelines)
- `templates/` (framework templates)
- `validation/` (validation scripts)

**Repository-managed paths (never overwritten):**
- `local/agents/` (custom agent profiles)
- `local/directives/` (local extensions)
- `docs/architecture/adrs/` (repository ADRs)
- `work/` (task state and outputs)
- `.framework_overrides.yml` (explicit local modifications)

**Conflict resolution:**
- If repository file differs from framework version → create `.framework-new` file
- Human or agent reviews conflict and merges manually
- Upgrade script never silently overwrites divergent files

### Metadata Tracking

**`.framework_meta.yml` (created in repository root):**

```yaml
framework:
  name: "quickstart-agent-framework"
  version: "1.2.0"
  installed_at: "2026-02-11T14:30:00Z"
  upgraded_from: "1.1.0"
  
managed_paths:
  - "agents/directives/"
  - "agents/profiles/"
  - "agents/guidelines/"
  - "templates/"
  - "validation/"

local_paths:
  - "local/"
  - "docs/architecture/adrs/"
  - "work/"

checksums:
  "agents/directives/001_example.md": "sha256:abc123..."
  "agents/profiles/architect.md": "sha256:def456..."
  # ... etc.
```

### Safety Mechanisms

1. **Conflict detection:** Compare file checksums before overwriting
2. **Backup creation:** Create `.framework-backup/` before upgrade
3. **Dry-run mode:** Preview changes without applying (`--dry-run`)
4. **Rollback script:** Restore from backup if upgrade fails
5. **Validation post-install:** Run framework validation after upgrade

## Rationale

### Why Zip Distribution?

**Portability:**
- Works on any platform (Windows, macOS, Linux)
- No special tools required (zip is universal)
- Transferable via any medium (USB, file share, email, download)
- Air-gap friendly (no network dependencies)

**Simplicity:**
- Single file contains everything
- Versioned clearly in filename
- Easy to archive and mirror
- Deterministic contents

**Deterministic:**
- Manifest provides file inventory
- Checksums enable integrity verification
- Reproducible installations
- Auditable contents

### Why Shell Scripts?

**Portability:**
- POSIX shell runs everywhere
- No runtime dependencies (Python, Node, etc.)
- Simple to inspect and modify
- Easy to debug

**Transparency:**
- Human-readable installation logic
- No black-box installers
- Easy to audit for security
- Simple to customize if needed

### Why Core/Local Boundary?

**Respects customization:**
- Projects can extend framework without fear of overwrites
- Local modifications persist through upgrades
- Framework improvements delivered without disruption

**Enables learning period:**
- Teams can evaluate framework changes before merging
- `.framework-new` files enable side-by-side comparison
- Human judgment applied to conflicts

**Predictable upgrades:**
- Clear expectations about what changes
- No surprises from automatic overwrites
- Explicit conflict resolution

### Framework-Level Pattern

This pattern applies universally because:
- All adopters need framework updates
- All repositories have local customizations
- All environments may have network restrictions
- All teams benefit from safe upgrade mechanisms

## Consequences

### Positive

- ✅ **Downstream independence:** Install/upgrade without rewriting history or Git dependencies
- ✅ **Automated drift detection:** Guardian can diff against manifest
- ✅ **Easy mirroring:** Releases simple to archive and distribute
- ✅ **Safe upgrades:** Conflicts explicit, never silent overwrites
- ✅ **Air-gap friendly:** Works without internet access
- ✅ **Platform agnostic:** Zip works everywhere
- ✅ **Transparent:** Scripts are readable and auditable

### Negative (Accepted Trade-offs)

- ⚠️ **Zip regeneration:** Must rebuild package for every release (mitigated by CI automation)
- ⚠️ **Large artifacts:** Framework size may inflate zip (mitigated by compression and selective inclusion)
- ⚠️ **Script testing:** Installation scripts need cross-platform testing (Linux, macOS, WSL)
- ⚠️ **Manual conflict resolution:** `.framework-new` files require human review (accepted for safety)

## Implementation

Repositories adopting this framework should:

### Package Creation (Framework Maintainers)

```bash
#!/bin/bash
# build-framework-package.sh

VERSION="1.2.0"
FRAMEWORK_NAME="quickstart-agent-framework"
PACKAGE_NAME="${FRAMEWORK_NAME}-${VERSION}.zip"

# Create staging directory
mkdir -p build/framework_core
mkdir -p build/scripts
mkdir -p build/META

# Copy core framework files
cp -r agents/ build/framework_core/
cp -r templates/ build/framework_core/
cp -r validation/ build/framework_core/

# Copy scripts
cp scripts/framework_install.sh build/scripts/
cp scripts/framework_upgrade.sh build/scripts/
cp scripts/framework_validate.sh build/scripts/

# Generate manifest
generate_manifest build/framework_core > build/META/MANIFEST.yml

# Generate release notes
cp RELEASE_NOTES.md build/META/
cp UPGRADE_GUIDE.md build/META/

# Create zip
cd build
zip -r "../${PACKAGE_NAME}" .
cd ..

echo "Created: ${PACKAGE_NAME}"
```

### Installation Script (Simplified Example)

```bash
#!/bin/bash
# framework_install.sh

REPO_PATH="$1"
FRAMEWORK_VERSION="1.2.0"

if [ -z "$REPO_PATH" ]; then
  echo "Usage: $0 <repository-path>"
  exit 1
fi

# Check if already installed
if [ -f "$REPO_PATH/.framework_meta.yml" ]; then
  echo "Framework already installed. Use framework_upgrade.sh instead."
  exit 1
fi

# Copy framework core
echo "Installing framework core..."
cp -r framework_core/agents "$REPO_PATH/"
cp -r framework_core/templates "$REPO_PATH/"
cp -r framework_core/validation "$REPO_PATH/"

# Initialize work directory
echo "Initializing work directory..."
mkdir -p "$REPO_PATH/work/inbox"
mkdir -p "$REPO_PATH/work/assigned"
mkdir -p "$REPO_PATH/work/done"
mkdir -p "$REPO_PATH/work/archive"

# Create metadata file
cat > "$REPO_PATH/.framework_meta.yml" <<EOF
framework:
  name: "quickstart-agent-framework"
  version: "$FRAMEWORK_VERSION"
  installed_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
EOF

echo "✅ Framework installed successfully (version $FRAMEWORK_VERSION)"
echo "Run validation: ./validation/validate_framework.sh"
```

### Upgrade Script (Simplified Example)

```bash
#!/bin/bash
# framework_upgrade.sh

REPO_PATH="$1"
NEW_VERSION="1.2.0"

if [ ! -f "$REPO_PATH/.framework_meta.yml" ]; then
  echo "Framework not installed. Use framework_install.sh instead."
  exit 1
fi

# Read current version
CURRENT_VERSION=$(grep 'version:' "$REPO_PATH/.framework_meta.yml" | cut -d'"' -f2)
echo "Upgrading from $CURRENT_VERSION to $NEW_VERSION"

# Create backup
echo "Creating backup..."
cp -r "$REPO_PATH/agents" "$REPO_PATH/.framework-backup/agents"

# Upgrade core files
for file in framework_core/agents/directives/*.md; do
  dest="$REPO_PATH/agents/directives/$(basename $file)"
  
  if [ -f "$dest" ]; then
    # Check if file has diverged
    if ! cmp -s "$file" "$dest"; then
      echo "Conflict detected: $(basename $file)"
      cp "$file" "$dest.framework-new"
      echo "  Created: $dest.framework-new (review and merge manually)"
    else
      # Identical, safe to overwrite
      cp "$file" "$dest"
    fi
  else
    # New file, safe to copy
    cp "$file" "$dest"
  fi
done

# Update metadata
sed -i "s/version: \"$CURRENT_VERSION\"/version: \"$NEW_VERSION\"/" "$REPO_PATH/.framework_meta.yml"
sed -i "/upgraded_from:/d" "$REPO_PATH/.framework_meta.yml"
sed -i "/installed_at:/a \  upgraded_from: \"$CURRENT_VERSION\"" "$REPO_PATH/.framework_meta.yml"

echo "✅ Framework upgraded to $NEW_VERSION"
echo "Review any .framework-new files for conflicts"
```

### Validation

Post-installation validation:

```bash
#!/bin/bash
# framework_validate.sh

REPO_PATH="$1"

# Check metadata exists
if [ ! -f "$REPO_PATH/.framework_meta.yml" ]; then
  echo "❌ Framework metadata not found"
  exit 1
fi

# Check required directories
required_dirs=(
  "$REPO_PATH/agents/directives"
  "$REPO_PATH/agents/profiles"
  "$REPO_PATH/templates"
  "$REPO_PATH/work/inbox"
)

for dir in "${required_dirs[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "❌ Missing required directory: $dir"
    exit 1
  fi
done

# Validate directive integrity
"$REPO_PATH/validation/validate_directives.sh"

echo "✅ Framework installation valid"
```

## Related

- **Doctrine:** DDR-002 (Framework Guardian Role) - guardian validates framework integrity
- **Doctrine:** DDR-010 (Modular Directive System) - framework structure being distributed
- **Approach:** Framework portability approach (framework principles)
- **Implementation:** See repository-specific ADRs for build and release automation
