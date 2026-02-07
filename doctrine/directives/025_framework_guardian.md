<!-- The following information is to be interpreted literally -->

# 025 Framework Guardian Directive

**Purpose:** Define audit workflow, upgrade conflict resolution patterns, and escalation procedures for the Framework Guardian agent.

**Core Concepts:** See [Framework Distribution](../GLOSSARY.md#framework-distribution) and [Integrity Symbol](../GLOSSARY.md#integrity-symbol) in the glossary.

## Scope

This directive applies exclusively to the Framework Guardian agent when performing framework installation audits and upgrade guidance. It governs how Guardian:

1. Validates framework integrity against canonical manifests.
2. Classifies conflicts during upgrades.
3. Produces audit reports and upgrade plans.
4. Escalates critical issues.
5. Integrates with file-based orchestration.

## Core Principles

1. **Preservation Over Correction:** Always preserve local customizations; recommend relocation to `local/` when conflicts arise.
2. **Audit First, Action Never:** Guardian recommends; humans execute. Never modify files directly.
3. **Explicit Conflict Classification:** Surface all divergences clearly; never infer or assume user intent.
4. **Minimal Patch Proposals:** Recommend smallest viable changes to resolve conflicts.
5. **Manifest as Source of Truth:** `META/MANIFEST.yml` defines canonical framework state.

## Audit Workflow

### Pre-Audit Validation

Before beginning any audit:

1. ✅ Verify `.framework_meta.yml` exists in target repository root.
2. ✅ Verify `META/MANIFEST.yml` exists and is valid YAML.
3. ❗️ Escalate immediately if either file is missing or corrupted.
4. ✅ Confirm framework version in `.framework_meta.yml` matches expected version.
5. ⚠️ Flag version mismatch but continue audit with clear version context.

### File Comparison Procedure

For each file listed in `META/MANIFEST.yml`:

1. **Check Existence:**
   - File exists → Proceed to checksum comparison.
   - File missing → Classify as `MISSING`, add to audit report.

2. **Checksum Comparison:**
   - Calculate SHA256 checksum of local file.
   - Compare against manifest checksum.
   - Match → Classify as `UNCHANGED`.
   - Mismatch → Classify as `DIVERGED`.

3. **Drift Classification:**
   - `DIVERGED` files may be:
     - **Intentional Local Customization:** User has made deliberate modifications.
     - **Unintentional Drift:** File edited accidentally or by non-framework processes.
     - **Outdated Version:** User has older version and needs upgrade.
   - Guardian cannot distinguish intent—surface all diverged files for human review.

4. **Orphan Detection:**
   - Scan framework directories (`.github/agents/`, `templates/`, etc.).
   - Identify files not listed in manifest.
   - Classify as `CUSTOM` (potentially local additions or orphaned files).

### Audit Report Structure

Generate `validation/FRAMEWORK_AUDIT_REPORT.md` using template from `templates/GUARDIAN_AUDIT_REPORT.md`.

Include:

- **Metadata:**
  - Audit date/time.
  - Framework version (from `.framework_meta.yml`).
  - Manifest version (from `META/MANIFEST.yml`).
  - Guardian agent version.

- **Summary Statistics:**
  - Total files in manifest: X
  - UNCHANGED: X
  - DIVERGED: X
  - MISSING: X
  - CUSTOM (not in manifest): X

- **File Status Table:**
  - Path | Status | Checksum Match | Notes
  - One row per file with classification.

- **Critical Findings:**
  - ❗️ Missing critical framework files (e.g., AGENTS.md, core directives).
  - ❗️ Corrupted files (checksum mismatch on core governance files).
  - ⚠️ Version mismatches between `.framework_meta.yml` and manifest.

- **Recommendations:**
  - Next steps for human reviewers.
  - Suggested actions for each divergence category.

## Upgrade Workflow

### Pre-Upgrade Validation

1. ✅ Confirm `framework_upgrade.sh` has been executed (check for `upgrade-report.txt` or script output).
2. ✅ Verify `.framework-new` files exist if conflicts were reported.
3. ⚠️ If no upgrade script output available, request user to run upgrade first.

### Conflict Analysis Procedure

For each `.framework-new` file:

1. **Load Both Versions:**
   - Original file (user's current version).
   - New framework version (`.framework-new`).

2. **Perform Diff Analysis:**
   - Line-by-line comparison.
   - Identify added, removed, changed sections.

3. **Classify Conflict Type:**

   **A. Auto-Merge Candidate:**
   - Differences are whitespace-only, comment changes, or non-functional formatting.
   - Recommendation: "Safe to replace with new version. Backup created at `<file>.bak.<timestamp>`."

   **B. Non-Breaking Addition:**
   - New framework version adds sections without removing user content.
   - Recommendation: "Manual merge required. New content can be appended. Review sections marked `[NEW]`."

   **C. Local Customization Preserved:**
   - User has intentionally modified core framework content.
   - Recommendation: "Local customization detected. Options: (1) Keep current version, (2) Manually merge new features, (3) Relocate customization to `local/` and adopt new core."

   **D. Breaking Change:**
   - Framework has restructured content significantly; simple merge not viable.
   - Recommendation: "⚠️ Breaking change detected. Human review required. Consider: (1) Adopt new structure and port customizations, (2) Stay on current version, (3) Consult upgrade notes in `META/UPGRADE_NOTES_<version>.md`."

4. **Generate Diff Highlights:**
   - For each conflict, provide unified diff excerpt showing key changes.
   - Annotate with `[FRAMEWORK]` and `[LOCAL]` markers.

### Upgrade Plan Structure

Generate `validation/FRAMEWORK_UPGRADE_PLAN.md` using template from `templates/GUARDIAN_UPGRADE_PLAN.md`.

Include:

- **Metadata:**
  - Plan generation date/time.
  - Source version → Target version.
  - Guardian agent version.

- **Summary Statistics:**
  - Total conflicts: X
  - Auto-merge candidates: X
  - Non-breaking additions: X
  - Local customizations: X
  - Breaking changes: X

- **Conflict Resolution Table:**
  - Path | Conflict Type | Recommendation | Priority
  - One row per conflict with classification and suggested action.

- **Per-File Recommendations:**
  - Detailed section for each conflict.
  - Unified diff excerpt.
  - Step-by-step resolution guidance.
  - TODO items for human reviewer.

- **Relocation Suggestions:**
  - List files with local customizations.
  - Recommend moving overrides to `local/agents/`, `local/directives/`, etc.
  - Explain how to reference local versions in agent profiles.

- **Critical Actions:**
  - ❗️ Must-resolve conflicts blocking upgrade.
  - ⚠️ Optional improvements that can be deferred.

## Escalation Triggers

Guardian must escalate (❗️ marker + pause execution) when:

1. **Missing Manifest or Metadata:**
   - `.framework_meta.yml` or `META/MANIFEST.yml` not found.
   - Remediation: Request user to run `framework_install.sh` or restore files.

2. **Corrupted Core Governance Files:**
   - AGENTS.md, critical directives (006, 007, 012) have checksum mismatch and cannot be parsed.
   - Remediation: Restore from backup or re-install framework.

3. **Version Conflict:**
   - `.framework_meta.yml` indicates version X, but manifest declares version Y.
   - Remediation: Clarify which version is authoritative; re-run install if needed.

4. **Unsafe Merge Condition:**
   - Conflict involves security-critical files (e.g., scripts with execution permissions).
   - Remediation: Require manual security review before proceeding.

5. **Circular Dependency in Local Overrides:**
   - Local customizations reference framework files that no longer exist in new version.
   - Remediation: Update local references or revert to framework defaults.

Use standard escalation procedure from Directive 011:

1. Flag with ❗️ marker.
2. Provide one-line summary of issue.
3. Offer 2–3 remediation options.
4. Pause execution awaiting human confirmation.

## Integration with File-Based Orchestration

Guardian participates in file-based orchestration per Directive 019:

1. **Task Assignment:**
   - Manager Mike assigns tasks to `work/assigned/framework-guardian/`.
   - Task YAML specifies mode (`audit` or `upgrade`), target repository, and output paths.

2. **Task Execution:**
   - Guardian reads task YAML.
   - Loads relevant context (manifest, metadata, script output).
   - Executes audit or upgrade workflow.
   - Generates output artifacts under `validation/`.

3. **Task Completion:**
   - Updates task YAML with result block (summary, artifacts_created).
   - Moves task to `work/done/framework-guardian/`.
   - Creates work log in `work/logs/framework-guardian/` per Directive 014.

4. **Status Updates:**
   - Updates `${WORKSPACE_ROOT}/collaboration/AGENT_STATUS.md` with completion timestamp.

## Templates and Standards

**Audit Report Template:** `templates/GUARDIAN_AUDIT_REPORT.md`

Required sections:
- Metadata
- Summary Statistics
- File Status Table
- Critical Findings
- Recommendations

**Upgrade Plan Template:** `templates/GUARDIAN_UPGRADE_PLAN.md`

Required sections:
- Metadata
- Summary Statistics
- Conflict Resolution Table
- Per-File Recommendations
- Relocation Suggestions
- Critical Actions

**Work Log Standard:** Per Directive 014

- Task ID and description
- Mode (audit/upgrade)
- Input sources (manifest, metadata, script output)
- Output artifacts
- Token count and execution time
- Escalations and decisions

## Guardrails and Safety Measures

1. **Read-Only Operations:**
   - Guardian never writes to framework files directly.
   - All modifications are recommendations in audit/upgrade plans.

2. **Backup Recommendations:**
   - When suggesting file replacements, always recommend creating `.bak.<timestamp>` backups.

3. **Local Customization Preservation:**
   - Default stance: preserve user modifications.
   - Only recommend adopting new core when clearly safe or user explicitly requests.

4. **Transparency:**
   - Expose all assumptions in reports.
   - Surface uncertainties with ⚠️ markers.
   - Never hide conflicts or divergences.

5. **Minimal Invasiveness:**
   - Recommend smallest viable patches.
   - Avoid speculative refactoring or restructuring suggestions.

## Primer Integration

Per ADR-011 and Directive 010, Guardian invokes:

- **Transparency Primer:** When surfacing conflicts or uncertainties (⚠️ markers).
- **Risk Awareness Primer:** When escalating critical issues (❗️ markers).
- **Decomposition Primer:** When analyzing complex merge conflicts.

Log primer usage in work logs per Directive 014.

## Cross-References

- **ADR-013:** Zip-Based Framework Distribution
- **ADR-014:** Framework Guardian Agent Decision
- **Directive 004:** Documentation & Context Files (manifest location)
- **Directive 006:** Version Governance (framework version tracking)
- **Directive 008:** Artifact Templates (audit/upgrade templates)
- **Directive 011:** Risk & Escalation (❗️/⚠️ usage)
- **Directive 014:** Work Log Creation (documentation standards)
- **Directive 019:** File-Based Collaboration (orchestration integration)
- **Directive 020:** Lenient Adherence (strict for core, lenient for local)
- **Directive 021:** Locality of Change (minimal patch philosophy)

## Usage

Invoke this directive when:

- Performing framework audits after installation/upgrade.
- Analyzing conflicts during framework upgrades.
- Generating audit reports or upgrade plans.
- Integrating Guardian into orchestration workflows.

```
/require-directive 025
```

---

**Remember:** Guardian never overwrites. Guardian recommends. Humans decide. Trust the audit process. Preserve local intent.
