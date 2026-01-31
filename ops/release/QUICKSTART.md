# Release Packaging - Quick Start

## 🚀 Quick Commands

### Build a Release Locally

```bash
# Simple build
python ops/release/build_release_artifact.py --version 1.0.0

# Dry-run (validation only)
python ops/release/build_release_artifact.py --version 1.0.0 --dry-run

# Custom output location
python ops/release/build_release_artifact.py \
    --version 1.0.0 \
    --output-dir ./my-releases
```

### Trigger CI/CD Build

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# Or use GitHub Actions manual dispatch
# Go to: Actions → Release Packaging → Run workflow
```

### Verify a Release

```bash
cd output/releases

# Verify checksum
sha256sum -c checksums.txt

# List contents
unzip -l quickstart-framework-1.0.0.zip

# Extract and inspect
unzip quickstart-framework-1.0.0.zip
cat quickstart-framework-1.0.0/META/metadata.json
```

## 📋 What Gets Packaged

```
quickstart-framework-X.Y.Z.zip
├── framework_core/
│   ├── .github/agents/       ← Agent profiles, directives, guidelines
│   ├── docs/                 ← Architecture, templates
│   ├── framework/            ← Python framework code
│   ├── validation/           ← Validation scripts
│   ├── AGENTS.md
│   └── README.md
├── scripts/                  ← Install/upgrade helpers
└── META/
    ├── MANIFEST.yml          ← File inventory with checksums
    ├── metadata.json         ← Build metadata
    └── RELEASE_NOTES.md      ← Release documentation
```

## ✅ What's Excluded

- `.git/` - Version control data
- `tmp/`, `output/` - Temporary files
- `work/logs/`, `work/reports/` - Work outputs
- `local/` - Project-specific customizations
- `__pycache__/`, `*.pyc` - Python cache
- `.vscode/`, `.idea/` - IDE files

## 🔍 Validation

The build automatically validates:
- ✅ Semantic version format (X.Y.Z[-prerelease][+build])
- ✅ Repository structure (required directories exist)
- ✅ File checksums (SHA256 for all files)
- ✅ Manifest completeness (all files listed)
- ✅ Metadata accuracy (version, git info)

## 📖 Full Documentation

- **Complete Guide**: See [ops/release/README.md](README.md)
- **Architecture**: [docs/architecture/adrs/ADR-013-zip-distribution.md](../../docs/architecture/adrs/ADR-013-zip-distribution.md)
- **Guardian Integration**: [docs/architecture/adrs/ADR-014-framework-guardian-agent.md](../../docs/architecture/adrs/ADR-014-framework-guardian-agent.md)

## 🐛 Troubleshooting

### "Invalid version format"
Remove 'v' prefix: use `1.0.0` not `v1.0.0`

### "Invalid repository structure"
Run from repository root, ensure required directories exist

### Files missing from artifact
Check if they match exclusion patterns in `EXCLUDE_PATTERNS`

## 🧪 Testing

```bash
# Run all tests
pytest validation/release/ -v

# Run integration tests only
pytest validation/release/test_integration.py -v
```

## 💡 Tips

- Use `--dry-run` to preview what will be packaged
- Check `output/releases/` for built artifacts
- Verify checksums before distributing
- Review `META/MANIFEST.yml` for file inventory
- Test extraction in a clean directory

## 🔗 Related Tasks

- **Install Scripts**: Task `2025-12-05T1012` (framework_install.sh)
- **Upgrade Scripts**: Task `2025-12-05T1012` (framework_upgrade.sh)
- **Framework Guardian**: Planned implementation for audit/upgrade modes
