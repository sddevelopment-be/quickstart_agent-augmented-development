# Framework Guardian Guide

The Framework Guardian is a specialized agent that audits framework installations and guides upgrades without automatically overwriting files.

## Purpose

The Guardian helps maintain framework integrity by:
- **Auditing** installations to detect drift, missing files, or modifications
- **Guiding** upgrades by analyzing conflicts and proposing resolutions
- **Protecting** local customizations from accidental overwrites
- **Ensuring** core/local separation is maintained

See [ADR-014](../architecture/adrs/ADR-014-framework-guardian-agent.md) for architectural rationale.

## When to Use

### Run Audit Mode When:
- After installing the framework
- Before committing framework changes
- Periodically (monthly recommended)
- After team members modify framework files
- When troubleshooting installation issues
- Before upgrading to a new version

### Run Upgrade Mode When:
- After running `framework_upgrade.sh`
- When `.framework-new` files are present
- To get guidance on resolving upgrade conflicts
- Before committing upgrade changes

## Operating Modes

### Audit Mode

Compares your installation against the framework manifest to detect:
- Missing core files
- Modified core files (checksum mismatches)
- Misplaced files (should be in core or local)
- Outdated version
- Configuration issues

**Output:** `validation/FRAMEWORK_AUDIT_REPORT.md`

### Upgrade Mode

Analyzes upgrade conflicts and proposes resolution strategy:
- Classifies conflicts (auto-merge, manual review, relocate)
- Shows framework vs local changes
- Recommends resolution approach
- Provides step-by-step execution plan
- Identifies customizations to move to `local/`

**Output:** `validation/FRAMEWORK_UPGRADE_PLAN.md`

## Usage

### Command Line (when implementation available)

```bash
# Audit current installation
python3 work/scripts/framework_guardian.py --mode audit --target .

# Review audit report
cat validation/FRAMEWORK_AUDIT_REPORT.md

# After upgrade, analyze conflicts
python3 work/scripts/framework_guardian.py --mode upgrade --target . --release 1.1.0

# Review upgrade plan
cat validation/FRAMEWORK_UPGRADE_PLAN.md
```

### Via Task System

Create task in `work/inbox/`:

```yaml
id: "2025-11-24T2000-guardian-audit"
agent: "framework-guardian"
status: "new"
title: "Audit framework installation"
artefacts:
  - "validation/FRAMEWORK_AUDIT_REPORT.md"
context:
  notes:
    - "Post-installation integrity check"
  mode: "audit"
  target_directory: "."
```

## Typical Workflows

### Workflow 1: Post-Installation Audit

```bash
# 1. Install framework
./scripts/framework_install.sh .

# 2. Run audit
python3 work/scripts/framework_guardian.py --mode audit --target .

# 3. Review report
cat validation/FRAMEWORK_AUDIT_REPORT.md

# 4. Address any issues
# [Follow recommendations in report]

# 5. Commit if clean
git add .
git commit -m "Install framework v1.0.0 - audit passed"
```

### Workflow 2: Upgrade with Guardian Assistance

```bash
# 1. Download new version
unzip quickstart-framework-1.1.0.zip
cd quickstart-framework-1.1.0

# 2. Dry-run upgrade
./scripts/framework_upgrade.sh --dry-run /path/to/repo

# 3. Review what would change
cat /path/to/repo/framework-upgrade-report.txt

# 4. Apply upgrade
./scripts/framework_upgrade.sh /path/to/repo

# 5. Generate upgrade plan
cd /path/to/repo
python3 work/scripts/framework_guardian.py --mode upgrade --target . --release 1.1.0

# 6. Review plan
cat validation/FRAMEWORK_UPGRADE_PLAN.md

# 7. Execute plan step-by-step
# [Follow Phase 1-6 in upgrade plan]

# 8. Verify completion
python3 work/scripts/framework_guardian.py --mode audit --target .

# 9. Commit
git add .
git commit -m "Upgrade framework to v1.1.0"
```

### Workflow 3: Regular Maintenance Audit

```bash
# Monthly or quarterly
python3 work/scripts/framework_guardian.py --mode audit --target .

# Check for:
# - New version available
# - Unintended modifications
# - Missing files
# - Drift from canonical state

# Address findings and re-audit
```

## Understanding Reports

### Audit Report Sections

1. **Executive Summary** - Quick status overview
2. **Version Information** - Installed vs available versions
3. **Detailed Findings** - File-by-file issues
4. **Recommendations** - Prioritized action items
5. **Compliance Status** - Pass/fail criteria
6. **Next Steps** - What to do

### Upgrade Plan Sections

1. **Executive Summary** - Conflict count and complexity
2. **Conflict Analysis** - Categorized by resolution type
3. **Breaking Changes** - API/structure changes
4. **Step-by-Step Plan** - Phases 1-6 execution
5. **Rollback Procedure** - If things go wrong
6. **Risk Assessment** - Potential issues

### Status Indicators

- ✅ **Compliant/OK** - No action needed
- ⚠️ **Warning** - Review recommended
- ❗️ **Critical** - Action required

## Guardian Guardrails

The Guardian will NEVER:
- Overwrite files automatically
- Modify local customizations in `local/**`
- Apply patches without approval
- Delete framework files
- Change metadata without explicit upgrade

The Guardian will ALWAYS:
- Generate reports for human review
- Propose minimal, surgical changes
- Preserve local customizations
- Note whether changes are framework-aligned or local
- Provide clear reasoning for recommendations

## Customization Management

### When Guardian Recommends Relocation

If audit or upgrade finds customized framework files, Guardian suggests moving them to `local/`:

```bash
# Example: Customized agent profile
mkdir -p local/agents
cp .github/agents/custom-agent.agent.md local/agents/
# Then restore framework version
```

**Why?**
- Separates core framework from customizations
- Prevents upgrade conflicts
- Makes customizations explicit
- Protects from accidental overwrites

### Local Directory Structure

```
local/
├── agents/           # Custom agent profiles
├── directives/       # Project-specific directives
├── guidelines/       # Custom guidelines
└── templates/        # Custom templates
```

## Troubleshooting

### Guardian Not Found

**Problem:** `framework_guardian.py not found`

**Solution:** Guardian implementation is part of Task 1958. If not yet implemented, use manual audit:
1. Check `.framework_meta.yml` exists
2. Compare installed files with `META/MANIFEST.yml`
3. Look for `.framework-new` files
4. Review framework-install-report.txt

### Report Not Generated

**Problem:** Script runs but no report created

**Solution:**
1. Check permissions on `validation/` directory
2. Verify `META/MANIFEST.yml` exists
3. Check `.framework_meta.yml` is valid
4. Review script output for errors

### Conflicting Recommendations

**Problem:** Report recommends conflicting actions

**Solution:**
1. Follow numbered sequence in report
2. Address ❗️ Critical items first
3. Then ⚠️ Warnings
4. Then ✅ Suggested improvements
5. Re-audit after each phase

## Best Practices

1. **Audit After Installation** - Always run audit post-install
2. **Audit Before Upgrade** - Ensure clean state before upgrading
3. **Review Reports Fully** - Don't skip sections
4. **Execute Plans Sequentially** - Follow phase order
5. **Backup Before Upgrade** - Create backup branch
6. **Test After Changes** - Verify nothing breaks
7. **Re-Audit Post-Fix** - Confirm issues resolved
8. **Schedule Regular Audits** - Monthly minimum
9. **Preserve Customizations** - Use `local/` directory
10. **Document Decisions** - Note why you deviated from recommendations

## Integration with CI/CD

### Automated Audit in CI

```yaml
# .github/workflows/framework-audit.yml
name: Framework Audit
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Framework Audit
        run: |
          python3 work/scripts/framework_guardian.py --mode audit --target .
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: validation/FRAMEWORK_AUDIT_REPORT.md
```

## Related Documentation

- [ADR-013: Zip-Based Distribution](../architecture/adrs/ADR-013-zip-distribution.md)
- [ADR-014: Framework Guardian Agent](../architecture/adrs/ADR-014-framework-guardian-agent.md)
- [Framework Installation Guide](framework-installation.md)
- [Framework Upgrade Guide](framework-upgrades.md)
- [Technical Design: Distribution Workflow](../architecture/design/distribution_of_releases_technical_design.md)

## Support

For issues with the Guardian:
1. Check this documentation
2. Review generated reports for details
3. Consult ADR-014 for design rationale
4. Open issue with `framework-guardian` label

---

**Note:** The Guardian implementation (Task 1958) provides the Python script. This guide describes usage patterns and workflows.
