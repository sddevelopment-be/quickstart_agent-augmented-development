# Framework Guardian Usage Guide

> **Agent:** Framework Guardian  
> **Purpose:** Framework audit and upgrade orchestration  
> **Version:** 1.0.0  
> **Last Updated:** 2025-12-23

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use the Framework Guardian](#when-to-use-the-framework-guardian)
3. [Audit Mode Workflow](#audit-mode-workflow)
4. [Upgrade Mode Workflow](#upgrade-mode-workflow)
5. [Understanding Conflict Classifications](#understanding-conflict-classifications)
6. [Reading Audit Reports](#reading-audit-reports)
7. [Reading Upgrade Plans](#reading-upgrade-plans)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Examples](#examples)

---

## Overview

The **Framework Guardian** is a specialized agent that helps maintain framework consistency across your project. It operates in two modes:

- **Audit Mode:** Compares your installation against the canonical framework specification
- **Upgrade Mode:** Analyzes upgrade conflicts and proposes safe merge strategies

**Key Principle:** The Guardian NEVER automatically modifies files. It produces detailed reports and recommendations for human review and approval.

---

## When to Use the Framework Guardian

### Audit Mode Scenarios

Use Audit Mode when you want to:

1. **Verify framework compliance** after initial installation
2. **Detect drift** from canonical framework over time
3. **Identify missing files** that should be present per the framework specification
4. **Review local overrides** and ensure they're properly organized
5. **Prepare for an upgrade** by understanding current state
6. **Investigate issues** related to framework configuration

**Recommended Frequency:** Monthly, or after significant local modifications to framework files.

### Upgrade Mode Scenarios

Use Upgrade Mode when:

1. **After running `framework_upgrade.sh`** to analyze the generated conflicts
2. **Planning a framework version upgrade** to understand impact
3. **Resolving `.framework-new` files** created during upgrades
4. **Deciding which changes to accept** from a new framework version
5. **Documenting merge strategies** for team review

**Trigger:** Immediately after `framework_upgrade.sh` reports conflicts.

---

## Audit Mode Workflow

### Step 1: Ensure Prerequisites

Before running an audit, verify:

```bash
# Check that framework metadata exists
cat .framework_meta.yml

# Check that manifest is present (if framework includes it)
cat META/MANIFEST.yml

# Verify core directories exist
ls -la .github/agents/
ls -la docs/templates/
```

### Step 2: Invoke the Framework Guardian

Create a task YAML in `work/collaboration/inbox/`:

```yaml
# work/collaboration/inbox/YYYY-MM-DDTHHMM-framework-audit.yaml
id: YYYY-MM-DDTHHMM-framework-audit
agent: framework-guardian
status: new
priority: medium
urgency: medium
mode: /analysis-mode
title: Conduct framework compliance audit

description: |
  Execute Audit Mode to compare installed framework against canonical
  specification. Identify drift, missing files, and local overrides.
  
  Focus areas:
  - Core agent profiles
  - Templates and directives
  - Task orchestration structure
  - Local override organization

artefacts:
  - validation/FRAMEWORK_AUDIT_REPORT.md

context:
  audit_scope: full  # or: agents-only, templates-only, directives-only
  
requirements:
  - Follow Audit Mode procedure in agent profile
  - Use framework-audit-report-template.md
  - Include actionable recommendations
  - Classify all framework-managed files
```

### Step 3: Review the Audit Report

The Guardian will produce `validation/FRAMEWORK_AUDIT_REPORT.md` containing:

- **Summary:** Overall status (OK / DRIFT / OUTDATED / PARTIAL)
- **Core vs Local Overview:** File classifications and counts
- **Divergence Details:** Specific modified files with analysis
- **Missing Files:** Expected but absent framework files
- **Recommendations:** Prioritized by risk level

### Step 4: Act on Recommendations

**Low-Risk Improvements** (Section 5.1): Safe to implement immediately
- Adding missing framework files
- Updating outdated templates
- Organizing files into proper directories

**Suggested Refactors** (Section 5.2): Require planning
- Moving modified core files to `local/` overrides
- Reconciling conflicting directives
- Updating agent profiles to match framework patterns

**Optional Enhancements** (Section 5.3): Consider for future iterations
- Adopting new framework features
- Restructuring local overrides for clarity

---

## Upgrade Mode Workflow

### Step 1: Run the Upgrade Script

```bash
# Download and extract new framework version
unzip quickstart-framework-X.Y.Z.zip -d /tmp/framework-new

# Run upgrade script
bash /tmp/framework-new/scripts/framework_upgrade.sh

# Check upgrade report
cat upgrade-report.txt
```

The script will:
- Copy unchanged files
- Add new files
- Create `.framework-new` files for conflicts
- Generate `upgrade-report.txt`

### Step 2: Invoke Framework Guardian for Upgrade Analysis

Create upgrade task:

```yaml
# work/collaboration/inbox/YYYY-MM-DDTHHMM-framework-upgrade-plan.yaml
id: YYYY-MM-DDTHHMM-framework-upgrade-plan
agent: framework-guardian
status: new
priority: high
urgency: high
mode: /analysis-mode
title: Analyze framework upgrade conflicts

description: |
  Execute Upgrade Mode to classify conflicts from framework_upgrade.sh.
  Propose merge strategies and identify safe auto-merge candidates.
  
  Upgrade details:
  - Previous version: [from .framework_meta.yml]
  - Target version: [from new MANIFEST.yml]
  - Conflicts detected: [from upgrade-report.txt]

artefacts:
  - validation/FRAMEWORK_UPGRADE_PLAN.md

context:
  upgrade_report: upgrade-report.txt
  framework_new_files: present
  
requirements:
  - Follow Upgrade Mode procedure in agent profile
  - Use framework-upgrade-plan-template.md
  - Classify all conflicts using taxonomy
  - Provide minimal-diff patches where possible
  - Recommend files to move to local/
```

### Step 3: Review the Upgrade Plan

The Guardian produces `validation/FRAMEWORK_UPGRADE_PLAN.md` with:

- **Summary Assessment:** Version gap, conflict counts, readiness status
- **Upgrade Items Overview:** Table of all touched files with status
- **Detailed Conflict Analysis:** Per-file merge strategies
- **Auto-Merge Items:** Safe to apply list
- **Post-Upgrade Checklist:** Verification steps

### Step 4: Execute Approved Changes

**For Auto-Merge Items (Section 4):**

```bash
# Review auto-merge list
grep "Auto-Merge" validation/FRAMEWORK_UPGRADE_PLAN.md

# If approved, apply changes
for file in $(list_from_plan); do
  cp "$file.framework-new" "$file"
  rm "$file.framework-new"
done
```

**For Manual Merge Items (Section 3):**

Use the Guardian's minimal-diff patches:

```bash
# Review suggested patch for each conflict
vim validation/FRAMEWORK_UPGRADE_PLAN.md

# Apply patch manually or with guidance
# Example: merge tool usage
git diff --no-index file.local file.framework-new
# Then edit file.local to incorporate approved changes
rm file.framework-new
```

**For Local Override Recommendations:**

```bash
# Move customized files to local/ as recommended
mkdir -p local/agents/
mv .github/agents/custom-agent.agent.md local/agents/
cp /tmp/framework-new/.github/agents/custom-agent.agent.md .github/agents/
```

### Step 5: Verify and Update Metadata

```bash
# Run post-upgrade checks from plan Section 8
ls -la .framework-new  # Should be empty

# Update framework metadata
vim .framework_meta.yml
# Update version, install_checksum, installed_at

# Run another audit to verify
# (Create new audit task as in Audit Mode workflow)
```

---

## Understanding Conflict Classifications

The Guardian uses a three-tier taxonomy:

### Tier 1: Auto-Merge Candidates

**Characteristics:**
- Formatting changes only (whitespace, line endings)
- Non-overlapping edits (framework and local touch different sections)
- Additive content (new sections that don't alter existing)
- Comment additions with no logic changes

**Guardian Indication:** Listed in Section 4 of upgrade plan with note "Safe to apply"

**Your Action:** Review list, then batch-apply if approved

### Tier 2: Manual Review Required

**Characteristics:**
- Logic changes in customized sections
- Structural reorganization (moved/renamed sections)
- Directive updates affecting local overrides
- Ambiguous intent (unclear if local change is customization or drift)

**Guardian Indication:** Listed in Section 3 with detailed conflict analysis, diff summary, and suggested patches

**Your Action:** Review each conflict individually, use provided patches as guidance, make informed merge decisions

### Tier 3: Local Customization to Preserve

**Characteristics:**
- Heavily customized agent profiles
- Project-specific guidelines/directives
- Custom templates tailored to project
- Integration configurations (CI/CD, tooling)

**Guardian Indication:** Flagged with recommendation to move to `local/` and keep core file at framework version

**Your Action:** Follow Guardian's reorganization advice, document overrides, maintain separate local versions

---

## Reading Audit Reports

### Section 1: Summary
Quick health check — your starting point.

**OK:** Framework is current, no drift → Routine maintenance only  
**DRIFT:** Some files diverged → Review Section 3  
**OUTDATED:** Missing updates → Consider upgrade  
**PARTIAL:** Incomplete installation → Review Section 2.1 for missing files

### Section 2: Core vs Local Overview
Understand what files the framework manages vs your customizations.

**Key Questions:**
- Are missing files critical? (Check descriptions)
- Do unknown files belong in `local/`?
- Are local overrides intentional?

### Section 3: Divergence Details
The meat of the audit — file-by-file analysis.

**Table Columns:**
- **File:** Path to diverged file
- **Status:** modified / outdated / missing
- **Notes:** Guardian's interpretation

**For each modified file:**
- **What changed?** — Specific differences
- **Is it intentional?** — Guardian's assessment
- **Should it move to local/?** — Reorganization suggestion

### Section 5: Recommendations
Prioritized action items.

**5.1 Safe, Low-Risk:** Do these first  
**5.2 Suggested Refactors:** Requires planning  
**5.3 Optional Enhancements:** Future improvements

---

## Reading Upgrade Plans

### Section 1: Summary
Upgrade complexity assessment.

**READY:** Few conflicts, mostly auto-merge → Safe to proceed  
**NEEDS-MANUAL-MERGE:** Several Tier 2 conflicts → Plan review time  
**BLOCKED:** Critical issues detected → Resolve before continuing

### Section 2: Upgrade Items Overview
Master table of all changes.

**Status Types:**
- **NEW:** Framework added this file → Review and accept
- **UNCHANGED:** No changes needed → Ignore
- **UPDATED:** Framework changed, no conflict → Accept update
- **CONFLICT:** Local modifications diverge → See Section 3
- **LOCAL-ONLY:** Not managed by framework → Ignore

**Resolution Required Column:**
- **auto:** Safe to batch-apply
- **manual merge:** Needs individual attention
- **copy:** Just add the file
- **preserve:** Keep local version, ignore framework

### Section 3: Detailed Conflict Analysis
Your detailed merge guide for each conflict.

**Per-File Structure:**
1. **Diff Summary:** Natural language explanation
2. **Recommended Merge Strategy:** Guardian's advice
3. **Suggested Patch:** Minimal-diff changes (when possible)
4. **Follow-up Action:** Reorganization recommendations

**How to Use:**
1. Read diff summary to understand what changed
2. Evaluate Guardian's strategy against your project needs
3. Apply suggested patch or adapt as needed
4. Consider follow-up actions (moving to local/)

### Section 8: Post-Upgrade Checklist
Verification steps to ensure success.

**Execute each checkbox:**
- [ ] Framework version updated in `.framework_meta.yml`
- [ ] No unmerged `.framework-new` files remain
- [ ] Orchestration structure intact
- [ ] Agent definitions load correctly
- [ ] Documentation references consistent

---

## Best Practices

### Audit Mode Best Practices

1. **Audit regularly** — Monthly or after major local changes
2. **Address drift promptly** — Small fixes are easier than accumulated drift
3. **Document intentional divergences** — Add notes in local override files explaining why
4. **Use local/ directories** — Keep customizations separate from core framework
5. **Review before upgrades** — Clean audit state makes upgrades smoother

### Upgrade Mode Best Practices

1. **Read the entire plan first** — Understand full scope before starting
2. **Start with auto-merge items** — Build confidence with easy wins
3. **Handle Tier 2 conflicts carefully** — These need your expertise
4. **Test after each major merge** — Don't accumulate untested changes
5. **Update metadata promptly** — Keep `.framework_meta.yml` current
6. **Run post-upgrade audit** — Verify upgrade success with fresh audit

### General Best Practices

1. **Never ignore Guardian escalations** — ❗️ markers indicate serious issues
2. **Trust the classification taxonomy** — Guardian is conservative (safe bias)
3. **Preserve local intent** — When in doubt, keep your customization
4. **Document your decisions** — Add comments explaining merge choices
5. **Provide feedback** — If Guardian classifications are wrong, note it for improvement

---

## Troubleshooting

### Problem: Audit fails with missing `.framework_meta.yml`

**Cause:** Framework was not installed via `framework_install.sh`, or metadata was deleted.

**Solution:**
```bash
# Manually create metadata file
cat > .framework_meta.yml << EOF
framework_version: "unknown"
installed_at: "$(date -Iseconds)"
source_release: "manual-install"
install_checksum: "none"
EOF

# Then run audit to establish baseline
```

### Problem: Upgrade plan says "BLOCKED"

**Cause:** Critical issues detected (missing MANIFEST, corrupted meta, security conflicts).

**Solution:**
1. Read escalation details in plan Section 1
2. Resolve critical issues (usually: restore missing files, fix corrupted metadata)
3. Regenerate upgrade plan
4. If stuck, request human assistance (escalate to architect or devops)

### Problem: Guardian classifies conflict incorrectly

**Cause:** Guardian's heuristics don't capture your specific context.

**Solution:**
1. Note the misclassification in the upgrade plan
2. Make informed decision based on your project knowledge
3. Document your reasoning for future reference
4. Consider providing feedback to improve Guardian taxonomy

### Problem: Too many manual merge conflicts

**Cause:** Large framework version gap, or excessive local modifications to core files.

**Solution:**
1. Break upgrade into smaller steps (upgrade one minor version at a time)
2. Move heavily customized files to `local/` before upgrading
3. Restore core files to framework version where possible
4. Request assistance if conflicts exceed your time budget

### Problem: Post-upgrade audit shows new drift

**Cause:** Manual merges introduced inconsistencies, or `.framework-new` files not fully resolved.

**Solution:**
```bash
# Check for leftover framework-new files
find . -name "*.framework-new"

# Remove or resolve them
# Then re-run audit to verify
```

### Problem: Guardian takes too long / times out

**Cause:** Very large repository, or complex conflict analysis.

**Solution:**
1. Narrow audit scope: use `audit_scope: agents-only` or similar in task YAML
2. Run upgrade mode on subsets of conflicts
3. Increase agent timeout settings if available
4. Consider splitting into multiple smaller tasks

---

## Examples

### Example 1: Routine Monthly Audit

**Scenario:** You want to verify framework compliance as part of regular maintenance.

**Task YAML:**
```yaml
id: 2025-12-23T0900-framework-routine-audit
agent: framework-guardian
status: new
priority: low
urgency: low
mode: /analysis-mode
title: Monthly framework compliance audit

description: |
  Routine audit to detect drift and verify framework health.
  No recent major changes, expect mostly OK status.

artefacts:
  - validation/FRAMEWORK_AUDIT_REPORT.md

context:
  audit_type: routine
  last_audit: 2025-11-23
```

**Expected Outcome:** Report with "OK" status, possibly minor drift in comments or formatting.

**Action:** Review recommendations, apply low-risk improvements if any.

---

### Example 2: Pre-Upgrade Audit

**Scenario:** A new framework version is available, you want to understand current state before upgrading.

**Task YAML:**
```yaml
id: 2025-12-23T1000-framework-pre-upgrade-audit
agent: framework-guardian
status: new
priority: high
urgency: medium
mode: /analysis-mode
title: Pre-upgrade audit before v2.0 adoption

description: |
  Audit current installation before upgrading from v1.2 to v2.0.
  Goal: identify drift and local overrides that may conflict with upgrade.
  
  Prepare project for smooth upgrade by cleaning up drift first.

artefacts:
  - validation/FRAMEWORK_AUDIT_REPORT.md

context:
  audit_type: pre-upgrade
  current_version: "1.2.0"
  target_version: "2.0.0"
  focus: identify-local-overrides
```

**Expected Outcome:** Report highlighting modified core files and suggesting moves to `local/`.

**Action:** Address divergence (move to local/, restore core files) before running upgrade script.

---

### Example 3: Post-Upgrade Conflict Resolution

**Scenario:** You ran `framework_upgrade.sh` and got 12 conflicts. Need Guardian to classify them.

**Task YAML:**
```yaml
id: 2025-12-23T1100-framework-upgrade-v2-plan
agent: framework-guardian
status: new
priority: critical
urgency: high
mode: /analysis-mode
title: Analyze v1.2 → v2.0 upgrade conflicts

description: |
  framework_upgrade.sh completed with 12 CONFLICT files.
  Need classification and merge strategies for each.
  
  Upgrade report shows:
  - 45 UNCHANGED files
  - 8 NEW files
  - 12 CONFLICT files (.framework-new created)
  
  Focus: Provide minimal-diff patches for Tier 2 conflicts.

artefacts:
  - validation/FRAMEWORK_UPGRADE_PLAN.md

context:
  previous_version: "1.2.0"
  target_version: "2.0.0"
  upgrade_report: upgrade-report.txt
  conflict_count: 12
  
requirements:
  - Classify all 12 conflicts using taxonomy
  - Provide patches for auto-merge and Tier 2 items
  - Identify Tier 3 files to move to local/
  - Include post-upgrade checklist
```

**Expected Outcome:** Upgrade plan with:
- 5 auto-merge candidates
- 4 manual review conflicts with patches
- 3 files recommended for local/ override

**Action:** Apply auto-merge batch, manually resolve 4 Tier 2 conflicts using patches, reorganize 3 files to local/.

---

### Example 4: Investigating Framework Drift

**Scenario:** Agents are behaving inconsistently; you suspect framework drift is the cause.

**Task YAML:**
```yaml
id: 2025-12-23T1400-framework-drift-investigation
agent: framework-guardian
status: new
priority: high
urgency: high
mode: /analysis-mode
title: Investigate suspected framework drift

description: |
  Agents not loading directives correctly. Possible causes:
  - Modified core agent files
  - Missing directive files
  - Conflicting local overrides
  
  Request comprehensive audit with focus on agent profiles and directives.

artefacts:
  - validation/FRAMEWORK_AUDIT_REPORT.md

context:
  audit_type: investigation
  symptoms: "agents-ignoring-directives"
  audit_scope: agents-and-directives
```

**Expected Outcome:** Report identifying specific modified agent files and missing/conflicting directives.

**Action:** Restore modified core files or properly organize local overrides, add missing directives.

---

## Quick Reference Card

### Audit Mode
**When:** Monthly, pre-upgrade, investigating issues  
**Input:** MANIFEST.yml, .framework_meta.yml, project files  
**Output:** validation/FRAMEWORK_AUDIT_REPORT.md  
**Key Section:** Section 3 (Divergence Details)

### Upgrade Mode
**When:** After framework_upgrade.sh creates conflicts  
**Input:** upgrade-report.txt, .framework-new files  
**Output:** validation/FRAMEWORK_UPGRADE_PLAN.md  
**Key Section:** Section 3 (Detailed Conflict Analysis)

### Conflict Tiers
**Tier 1 (Auto-merge):** Formatting, comments, non-overlapping → Batch apply  
**Tier 2 (Manual):** Logic changes, restructuring → Review and merge  
**Tier 3 (Preserve):** Heavy customization → Move to local/

### Escalation Markers
**❗️ Critical:** Stop and escalate immediately  
**⚠️ Warning:** Proceed with caution  
**✅ Aligned:** Good to go

### File Organization
**Core:** `.github/agents/`, `docs/templates/`, `docs/directives/` (framework-managed)  
**Local:** `local/`, `local_agents/`, `local_guidelines/` (project-specific)  
**Validation:** `validation/` (audit/upgrade reports)

---

**Questions or Issues?**

If the Framework Guardian produces unexpected results or you need clarification on recommendations:

1. Check the troubleshooting section above
2. Review the agent profile (`.github/agents/framework-guardian.agent.md`)
3. Consult ADR-014 (Framework Guardian Agent) for design rationale
4. Escalate to DevOps Danny (build automation) or Architect Alphonso (system design)

**Version:** 1.0.0  
**Last Updated:** 2025-12-23  
**Maintained By:** Architect Alphonso
