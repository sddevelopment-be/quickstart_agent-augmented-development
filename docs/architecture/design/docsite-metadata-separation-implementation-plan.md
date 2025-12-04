# Implementation Plan: Docsite Metadata Separation Architecture

**Status:** Proposed  
**Date:** 2025-12-04  
**Prepared by:** Architect Alphonso  
**Version:** 1.0.0  
**Related ADR:** [ADR-022: Docsite Separated Metadata](../adrs/ADR-022-docsite-separated-metadata.md)

## Overview

This document outlines a phased implementation plan for the separated metadata architecture as an **optional advanced profile** for the quickstart template. The plan balances feasibility validation, documentation quality, and sustainable rollout.

**Implementation Approach:** Prototype → Integrate → Template Rollout

**Total Timeline:** 4-6 weeks (condensed to 3-4 weeks if resources dedicated)

**Key Principle:** Validate technical feasibility early (Phase 1); invest in tooling and documentation only after prototype proves viable.

---

## Phase 1: Prototype & Validation (Week 1-2)

**Goal:** Prove technical feasibility of separated metadata architecture with minimal investment. Identify blockers early.

### 1.1 Create Reference Repository

**Task:** Set up standalone example repository demonstrating separated metadata pattern.

**Steps:**
1. Initialize new repo: `quickstart-docsite-separated-metadata-example`
2. Create minimal documentation structure:
   ```
   docs/
   ├── README.md
   ├── guides/
   │   ├── getting-started.md
   │   └── advanced.md
   └── reference/
       └── api.md
   ```
3. Set up Hugo docsite structure:
   ```
   docs-site/
   ├── config.toml
   ├── content/
   │   └── docs -> ../../docs/  # Symlink
   ├── data/
   │   └── docmeta.yaml
   └── layouts/
       ├── _default/
       │   ├── baseof.html
       │   ├── single.html
       │   └── list.html
       └── partials/
           └── menu.html
   ```

**Deliverables:**
- ✅ Working Hugo site with symlinked content
- ✅ `docmeta.yaml` with entries for all documentation files
- ✅ Custom templates performing metadata lookup by path
- ✅ Hugo build succeeds and renders pages correctly

**Success Criteria:**
- Hugo build completes without errors
- Metadata (title, tags, weight) correctly displayed in rendered pages
- Symlinks work on Linux/macOS
- Manual test on Windows (with Developer Mode) or copy fallback documented

**Estimated Effort:** 8-12 hours

### 1.2 Test Cross-Platform Symlink Behavior

**Task:** Validate symlink handling on Linux, macOS, Windows, GitHub Actions.

**Test Matrix:**

| Platform | Configuration | Expected Behavior |
|----------|--------------|------------------|
| Linux (Ubuntu 22.04) | Native symlinks | ✅ Works |
| macOS (latest) | Native symlinks | ✅ Works |
| Windows 10+ (Developer Mode ON) | `git config core.symlinks true` | ✅ Works |
| Windows 10+ (Developer Mode OFF) | Git converts symlinks to text files | ❌ Fails → Use copy fallback |
| GitHub Actions (ubuntu-latest) | Native symlinks | ✅ Works |
| GitHub Actions (windows-latest) | `git config core.symlinks true` | Test needed |

**Steps:**
1. Test symlink creation and Hugo build on each platform
2. Document fallback procedure for Windows without Developer Mode
3. Create `sync-docs.sh` and `sync-docs.ps1` scripts for copy-based fallback

**Deliverables:**
- ✅ Cross-platform test results documented
- ✅ Sync scripts for Windows fallback
- ✅ CI workflow demonstrating build on Linux and Windows runners

**Success Criteria:**
- Symlinks work on Linux/macOS without configuration
- Windows fallback procedure documented and tested
- GitHub Actions workflow builds successfully on both Linux and Windows runners

**Estimated Effort:** 4-6 hours

### 1.3 Implement Minimal Validation Script

**Task:** Create Python script to detect metadata drift (missing entries, orphaned keys).

**Script:** `validation/validate-docsite-metadata.py`

**Functionality:**
1. **File Coverage Check:**
   - List all `.md` files in configured directories (`docs/`, `.github/agents/`)
   - Check each file has entry in `docmeta.yaml`
   - Report missing entries with severity WARNING

2. **Metadata Validity Check:**
   - List all keys in `docmeta.yaml`
   - Check each key references existing file
   - Report orphaned keys with severity ERROR

3. **Basic Schema Validation:**
   - Verify required fields present (title, tags, section)
   - Validate field types (tags is list, weight is integer)
   - Report schema violations with severity ERROR

**Configuration:** `validation/docsite-metadata-config.yaml`
```yaml
validation:
  content_directories:
    - docs/
    - .github/agents/
  metadata_file: docs-site/data/docmeta.yaml
  required_fields:
    - title
    - tags
    - section
  warn_on_missing: true
  fail_on_orphaned: true
```

**Deliverables:**
- ✅ `validate-docsite-metadata.py` script with coverage, validity, schema checks
- ✅ Configuration file for customizable validation rules
- ✅ Test suite for validation script (pytest)

**Success Criteria:**
- Script detects missing metadata entries (false negative test)
- Script detects orphaned metadata keys (false positive test)
- Script validates schema (required fields, correct types)
- Exit codes: 0 (pass), 1 (warnings), 2 (errors)

**Estimated Effort:** 8-10 hours

### 1.4 Pilot Test with Realistic Content

**Task:** Copy 10-15 markdown files from main repository into reference repo; add metadata; validate workflow.

**Steps:**
1. Copy sample files from `docs/architecture/adrs/` (5 files), `docs/HOW_TO_USE/` (5 files), `.github/agents/` (3 profiles)
2. Create metadata entries in `docmeta.yaml` for all files
3. Build Hugo site and verify rendering
4. Intentionally rename a file without updating metadata; verify validation script detects drift
5. Add new file without metadata; verify validation script reports missing entry

**Deliverables:**
- ✅ Reference repository with realistic content (15+ files)
- ✅ Metadata entries correctly keyed by relative path
- ✅ Validation script successfully detects drift scenarios

**Success Criteria:**
- All 15 files render correctly with metadata
- Drift detection works (renamed file, missing entry)
- Hugo build time acceptable (<5 seconds for 15 files)

**Estimated Effort:** 4-6 hours

### Phase 1 Exit Criteria

- ✅ Reference repository demonstrates working separated metadata architecture
- ✅ Cross-platform symlink behavior documented with fallback procedures
- ✅ Validation script detects metadata drift reliably
- ✅ No technical blockers identified
- ⚠️ If blockers found, halt and reassess ADR before proceeding to Phase 2

**Total Phase 1 Effort:** 24-34 hours (1.5-2 weeks part-time)

---

## Phase 2: Integration & Tooling (Week 3-4)

**Goal:** Create production-quality tooling and agent integration for separated metadata pattern.

### 2.1 Introduce Docsite Curator Agent

**Task:** Create agent profile and integrate with orchestration workflow.

**Agent Profile:** `.github/agents/docsite-curator.agent.md`

**Responsibilities:**
- Maintain `docs-site/data/docmeta.yaml` integrity
- Add metadata entries for new documentation files
- Update metadata entries when files renamed
- Prune orphaned metadata entries
- Validate metadata schema compliance
- Perform periodic metadata audits

**Capabilities:**
- Read and edit YAML files
- Execute validation script
- Report metadata drift to orchestrator
- Generate bulk metadata updates (retagging, weight adjustment)

**Integration Points:**
1. **Task Routing:** Orchestrator routes metadata tasks to Docsite Curator
2. **Validation Trigger:** CI failure on metadata drift creates curator task
3. **Content Agent Handoff:** Content agents create metadata tasks when adding new files

**Task Template:** `work/templates/docsite-curator-task.yaml`
```yaml
task:
  id: "docsite-curator-{{ timestamp }}"
  type: "metadata-maintenance"
  status: "pending"
  agent: "docsite-curator"
  priority: "medium"
  description: "{{ action }}: {{ files }}"
  context:
    action: "add-entry | update-entry | prune-orphaned | audit"
    files:
      - "{{ file_path }}"
    validation_script: "validation/validate-docsite-metadata.py"
  result: null
  metrics:
    entries_added: 0
    entries_updated: 0
    entries_removed: 0
    drift_detected: false
```

**Deliverables:**
- ✅ Docsite Curator agent profile created
- ✅ Task template for metadata operations
- ✅ Orchestrator rules for routing metadata tasks
- ✅ Integration test: curator adds metadata entry for new file

**Success Criteria:**
- Curator agent successfully adds metadata entry via task
- Validation script confirms entry added correctly
- Orchestrator routes metadata tasks to curator (not content agents)

**Estimated Effort:** 8-12 hours

### 2.2 Add Metadata-Update Tasks to Task Queues

**Task:** Enable automated metadata task creation when content changes.

**Triggers:**

1. **New File Added:**
   - Content agent creates file in `docs/` or `.github/agents/`
   - Post-commit hook or CI check detects missing metadata
   - Orchestrator creates curator task: "Add metadata entry for `{{ file_path }}`"

2. **File Renamed:**
   - Content agent renames file (git mv)
   - Validation script detects orphaned metadata key
   - Orchestrator creates curator task: "Update metadata key from `{{ old_path }}` to `{{ new_path }}`"

3. **File Deleted:**
   - Content agent deletes file (git rm)
   - Validation script detects orphaned metadata key
   - Orchestrator creates curator task: "Remove orphaned metadata entry for `{{ old_path }}`"

**Automation Script:** `scripts/create-metadata-tasks.py`
```python
# Parse validation script output
# For each missing entry: create add-entry task
# For each orphaned key: create update-entry or prune task
# Write tasks to work/tasks/docsite-curator/
```

**Deliverables:**
- ✅ Automation script to generate curator tasks from validation results
- ✅ CI workflow integration (run validation → create tasks on failure)
- ✅ Task queue in `work/tasks/docsite-curator/`

**Success Criteria:**
- New file added → curator task created automatically
- File renamed → curator task identifies old/new paths
- File deleted → curator task prunes orphaned entry

**Estimated Effort:** 6-8 hours

### 2.3 Update Orchestrator Rules

**Task:** Configure orchestrator to recognize metadata tasks and route to curator.

**Orchestrator Rule:** `framework/orchestration/rules/docsite-curator-routing.yaml`
```yaml
routing_rule:
  name: "Route metadata tasks to Docsite Curator"
  condition:
    task_type: "metadata-maintenance"
  action:
    assign_to: "docsite-curator"
    priority: "medium"
  dependencies:
    - validation_script: "validation/validate-docsite-metadata.py"
    - metadata_file: "docs-site/data/docmeta.yaml"
```

**Orchestrator Behavior:**
1. Scan `work/tasks/` for new tasks
2. Match `task_type: metadata-maintenance`
3. Move task to `work/tasks/docsite-curator/` (assigned state)
4. Curator agent polls directory, processes tasks
5. Curator updates task YAML with result and metrics

**Deliverables:**
- ✅ Routing rule for metadata tasks
- ✅ Orchestrator configuration updated
- ✅ Integration test: orchestrator routes metadata task correctly

**Success Criteria:**
- Metadata task placed in `work/tasks/` is routed to curator
- Curator processes task and updates result
- Orchestrator marks task as completed

**Estimated Effort:** 4-6 hours

### 2.4 Expand Metadata Structure

**Task:** Define comprehensive metadata schema with all fields for rich docsite.

**Enhanced Schema:** `docs-site/schemas/docmeta.schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "patternProperties": {
    "^.*\\.md$": {
      "type": "object",
      "required": ["title", "tags", "section"],
      "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "section": {"type": "string"},
        "weight": {"type": "integer", "minimum": 0},
        "draft": {"type": "boolean"},
        "menu": {
          "type": "object",
          "properties": {
            "main": {
              "type": "object",
              "properties": {
                "parent": {"type": "string"},
                "weight": {"type": "integer"}
              }
            }
          }
        },
        "audience": {"type": "array", "items": {"type": "string"}},
        "related": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

**Optional Fields:**
- `description`: Short summary for SEO
- `draft`: Hide from production build
- `audience`: Target personas (from `docs/audience/`)
- `related`: Links to related documents

**Deliverables:**
- ✅ JSON Schema for comprehensive metadata structure
- ✅ Updated validation script to validate against schema
- ✅ Documentation of optional vs. required fields

**Success Criteria:**
- Schema validation passes for well-formed metadata
- Schema validation fails for malformed metadata (wrong types, missing required)

**Estimated Effort:** 4-6 hours

### 2.5 Add Validation for Metadata Drift

**Task:** Enhance validation script with advanced drift detection.

**Enhanced Checks:**

1. **Path Normalization:**
   - Check keys use forward slashes (not backslashes)
   - Check keys are relative to repo root (not absolute paths)
   - Warn on inconsistent path format

2. **Duplicate Title Detection:**
   - Check if multiple entries have identical titles
   - Warn (may be intentional, e.g., different sections)

3. **Orphaned Key Analysis:**
   - Detect if key matches pattern of recently renamed file (git log)
   - Suggest automated migration

4. **Missing Field Warnings:**
   - Report entries missing optional fields (description, audience)
   - Suggest fields to add for richer metadata

**Deliverables:**
- ✅ Enhanced validation script with advanced checks
- ✅ Validation report includes warnings and suggestions
- ✅ CI integration with configurable strictness (fail on error, warn only)

**Success Criteria:**
- Path normalization check detects Windows-style paths
- Duplicate title check warns on collisions
- Missing field warnings suggest improvements

**Estimated Effort:** 6-8 hours

### 2.6 Improve Hugo Layouts

**Task:** Create polished Hugo templates showcasing metadata capabilities.

**Templates to Enhance:**

1. **Single Page Template (`layouts/_default/single.html`):**
   - Display title from metadata
   - Render tags as clickable links
   - Show audience personas (if specified)
   - Display related documents section

2. **List Template (`layouts/_default/list.html`):**
   - Sort by weight (ascending)
   - Filter by tags or section
   - Show summaries from metadata description

3. **Menu Template (`layouts/partials/menu.html`):**
   - Build hierarchical menu from metadata `menu.main.parent`
   - Highlight current page
   - Show section badges

4. **Tags Page (`layouts/tags/list.html`):**
   - List all tags with document counts
   - Filter documents by selected tag

**Deliverables:**
- ✅ Enhanced Hugo templates with metadata-driven features
- ✅ Example CSS styling for tags, menus, audiences
- ✅ Documentation of template customization points

**Success Criteria:**
- Rendered site displays all metadata fields correctly
- Tags page lists all tags with counts
- Menu builds hierarchy from metadata

**Estimated Effort:** 8-12 hours

### Phase 2 Exit Criteria

- ✅ Docsite Curator Agent integrated with orchestration workflow
- ✅ Metadata tasks automatically created and routed
- ✅ Validation script detects advanced drift scenarios
- ✅ Hugo templates showcase rich metadata capabilities
- ✅ Reference repository demonstrates full pattern with 30+ files

**Total Phase 2 Effort:** 36-52 hours (2-3 weeks part-time)

---

## Phase 3: Template Rollout (Week 5-6)

**Goal:** Integrate separated metadata pattern into main quickstart template as optional advanced profile.

### 3.1 Integrate into Template Repository

**Task:** Add documentation and tooling to main quickstart template (opt-in, not default).

**Files to Add:**

1. **Advanced Setup Guide:** `docs/HOW_TO_USE/advanced-docsite-setup.md`
   - Explanation of separated metadata architecture
   - Benefits and trade-offs
   - Step-by-step setup instructions
   - Troubleshooting guide

2. **Docsite Curator Agent Profile:** `.github/agents/docsite-curator.agent.md`
   - Copy from reference repository
   - Customize for template context

3. **Validation Script:** `validation/validate-docsite-metadata.py`
   - Copy from reference repository
   - Add to validation suite

4. **Example Configuration Files:**
   - `docs/templates/docsite/config.toml.example` (Hugo config)
   - `docs/templates/docsite/docmeta.yaml.example` (Metadata template)
   - `docs/templates/docsite/single.html.example` (Custom template)

5. **Sync Scripts:** `scripts/sync-docs.sh` and `scripts/sync-docs.ps1`
   - For Windows users without symlink support

**Deliverables:**
- ✅ All documentation and tooling added to template
- ✅ Files clearly marked as optional/advanced
- ✅ README.md updated with link to advanced setup guide

**Success Criteria:**
- Template users can find advanced setup guide easily
- Setup guide is comprehensive and tested
- Example files work out-of-box with minimal customization

**Estimated Effort:** 8-12 hours

### 3.2 Add Section to `agents/QUICKSTART.md`

**Task:** Update quickstart guide to mention optional docsite setup.

**Section to Add:**

```markdown
## Optional: Documentation Site Setup

This template supports two approaches for documentation sites:

### Standard Approach (Recommended for Most Users)

Use traditional front matter in markdown files. Hugo, Jekyll, and most static site generators work out-of-box.

### Advanced Approach: Separated Metadata (Opt-In)

For teams with high agent workload and token economy concerns:
- Keep markdown files clean (no front matter)
- Centralize metadata in `docs-site/data/docmeta.yaml`
- Symlink content into Hugo's `content/` directory
- Use Docsite Curator Agent to maintain metadata

**When to use:** Agent-heavy workflows, frequent doc re-reading, >100 markdown files.

**Setup Guide:** See [Advanced Docsite Setup](../docs/HOW_TO_USE/advanced-docsite-setup.md)
```

**Deliverables:**
- ✅ Quickstart guide updated with docsite section
- ✅ Link to advanced setup guide

**Success Criteria:**
- Section clearly explains both approaches
- Guidance on when to use separated metadata
- Link to comprehensive setup guide

**Estimated Effort:** 2-3 hours

### 3.3 Provide Docs for Customizing Metadata

**Task:** Document how to customize metadata schema and Hugo templates.

**Documentation:** `docs/HOW_TO_USE/docsite-metadata-customization.md`

**Topics:**

1. **Adding Custom Metadata Fields:**
   - Extend `docmeta.yaml` schema
   - Update JSON Schema validation
   - Modify Hugo templates to display custom fields

2. **Changing Keying Strategy:**
   - Switch from relative path to filename or ID-based
   - Update validation script
   - Migrate existing metadata

3. **Hugo Theme Integration:**
   - Adapt separated metadata to work with existing Hugo themes
   - Override theme templates with metadata lookup logic
   - Fallback to standard front matter for missing metadata

4. **Metadata Defaults and Inheritance:**
   - Define default metadata for directory subtrees
   - Implement merge logic in Hugo templates
   - Reduce repetition in metadata file

5. **Validation Customization:**
   - Configure required vs. optional fields
   - Set validation strictness (warnings vs. errors)
   - Add custom validation rules

**Deliverables:**
- ✅ Comprehensive customization guide
- ✅ Code examples for each customization scenario
- ✅ Troubleshooting section

**Success Criteria:**
- Users can extend metadata schema independently
- Hugo template customization examples work
- Validation configuration documented

**Estimated Effort:** 6-8 hours

### 3.4 Provide Issue Templates

**Task:** Create GitHub issue templates for docsite-related tasks.

**Templates:**

1. **Metadata Drift Detected:** `.github/ISSUE_TEMPLATE/metadata-drift.md`
   ```markdown
   ---
   name: Metadata Drift Detected
   about: Validation script found mismatched metadata
   labels: docsite, metadata, bug
   ---

   **Validation Output:**
   ```
   [Paste validation script output]
   ```

   **Expected Behavior:**
   All files should have corresponding metadata entries; all metadata keys should reference existing files.

   **Action Needed:**
   - [ ] Add metadata entries for missing files
   - [ ] Update metadata keys for renamed files
   - [ ] Remove orphaned metadata entries
   ```

2. **Request Metadata Update:** `.github/ISSUE_TEMPLATE/metadata-update.md`
   ```markdown
   ---
   name: Request Metadata Update
   about: Request changes to document metadata (tags, weight, menu)
   labels: docsite, metadata, enhancement
   ---

   **Files Affected:**
   - `docs/path/to/file.md`

   **Requested Changes:**
   - Tags: [current] → [proposed]
   - Weight: [current] → [proposed]
   - Menu: [current] → [proposed]

   **Rationale:**
   [Explain why this metadata change improves navigation or discoverability]
   ```

**Deliverables:**
- ✅ Issue templates for metadata tasks
- ✅ Templates include validation output placeholders
- ✅ Labels configured for automated triage

**Success Criteria:**
- Issue templates appear in "New Issue" menu
- Templates guide users to provide necessary information

**Estimated Effort:** 2-3 hours

### 3.5 Add Migration Notes

**Task:** Document migration path from standard front matter to separated metadata (and vice versa).

**Documentation:** `docs/HOW_TO_USE/docsite-metadata-migration.md`

**Scenarios:**

1. **Migrate from Front Matter to Separated Metadata:**
   - Script to extract front matter from all markdown files
   - Generate `docmeta.yaml` from extracted metadata
   - Remove front matter from markdown files
   - Validate migration completeness

2. **Migrate from Separated Metadata to Front Matter:**
   - Script to inject metadata from `docmeta.yaml` into markdown files
   - Validate front matter format (YAML/TOML)
   - Test Hugo build with traditional front matter

3. **Bulk Rename with Metadata Update:**
   - Git operations to rename files
   - Script to update metadata keys accordingly
   - Validation to confirm sync

**Migration Script:** `scripts/migrate-metadata.py`
```python
# Subcommands:
# - extract: Extract front matter to docmeta.yaml
# - inject: Inject metadata from docmeta.yaml to front matter
# - update-keys: Update metadata keys after bulk rename
```

**Deliverables:**
- ✅ Migration documentation with step-by-step instructions
- ✅ Migration script with extract, inject, update-keys subcommands
- ✅ Test suite for migration script

**Success Criteria:**
- Migration script successfully extracts front matter to `docmeta.yaml`
- Migration script successfully injects metadata as front matter
- Bulk rename migration updates all metadata keys correctly

**Estimated Effort:** 8-12 hours

### Phase 3 Exit Criteria

- ✅ Advanced setup guide integrated into template
- ✅ Docsite Curator Agent available in template
- ✅ Validation and sync scripts included
- ✅ Example configurations and templates provided
- ✅ Customization and migration documentation complete
- ✅ Issue templates for metadata tasks available
- ✅ Template README links to separated metadata option

**Total Phase 3 Effort:** 26-38 hours (1.5-2 weeks part-time)

---

## Total Implementation Timeline

| Phase | Duration | Effort (Hours) | Key Deliverables |
|-------|----------|----------------|------------------|
| **Phase 1: Prototype** | Week 1-2 | 24-34 | Reference repo, validation script, cross-platform tests |
| **Phase 2: Integration** | Week 3-4 | 36-52 | Curator agent, metadata tasks, enhanced validation |
| **Phase 3: Rollout** | Week 5-6 | 26-38 | Template integration, documentation, migration tools |
| **Total** | 4-6 weeks | **86-124 hours** | Fully documented optional advanced profile |

**Resource Allocation (Recommended):**
- **Architect:** 30-40 hours (design, validation, documentation)
- **Developer:** 40-60 hours (scripts, Hugo templates, CI integration)
- **Curator:** 10-15 hours (agent profile, metadata examples, testing)
- **Tester:** 6-9 hours (cross-platform validation, migration testing)

**Condensed Timeline (Aggressive):**
- Phase 1: 1 week (full-time dedication)
- Phase 2: 1.5 weeks (full-time dedication)
- Phase 3: 1 week (full-time dedication)
- **Total: 3.5-4 weeks** (with dedicated resources)

---

## Success Metrics

### Technical Metrics

- **Validation script accuracy:** 100% detection of missing/orphaned metadata
- **Cross-platform compatibility:** Hugo build succeeds on Linux, macOS, Windows (with fallback)
- **Build performance:** Hugo build completes in <5 seconds for 100 files
- **Metadata drift incidents:** <5% of commits require manual metadata correction
- **Agent token savings:** 2-7% context window savings confirmed in pilot

### Adoption Metrics

- **Documentation quality:** Setup guide comprehension tested with 3+ early adopters
- **Setup time:** Advanced profile setup completes in <2 hours for new user
- **Issue template usage:** 80%+ of metadata issues use provided templates
- **Community feedback:** Net positive sentiment on separated metadata option

### Sustainability Metrics

- **Validation maintenance:** <4 hours/quarter for script updates
- **Template maintenance:** <2 hours/quarter for documentation updates
- **Support burden:** <1 issue/month requiring maintainer intervention
- **Migration success rate:** 90%+ of migrations complete without data loss

---

## Risk Mitigation Plan

### Risk: Windows Symlink Failures

**Mitigation:**
- Provide `sync-docs.sh`/`.ps1` as fallback
- Document Developer Mode setup clearly
- Test on Windows in Phase 1 before investing in Phase 2

### Risk: Metadata Drift Becomes Unmanageable

**Mitigation:**
- Make validation script mandatory in CI (fail build on drift)
- Curator agent performs weekly audits
- Migration script automates bulk renames

### Risk: Community Rejects Pattern as Too Complex

**Mitigation:**
- Position as optional advanced profile (not default)
- Provide standard front matter as recommended baseline
- Gather feedback from pilot users before template rollout

### Risk: Hugo Theme Incompatibility

**Mitigation:**
- Document custom template patterns clearly
- Provide examples for popular themes (Docsy, Book)
- Fallback to standard front matter if theme modification infeasible

### Risk: Validation Script Breaks with Repo Changes

**Mitigation:**
- Comprehensive test suite for validation script (pytest)
- Configuration file for easy adaptation
- Versioned validation script (semantic versioning)

---

## Rollback Plan

If separated metadata pattern proves unsustainable:

1. **Phase 1 Rollback:** Delete reference repository; document reasons in ADR-022 amendment
2. **Phase 2 Rollback:** Archive curator agent and validation script; revert orchestrator rules
3. **Phase 3 Rollback:** Remove advanced setup guide from template; update README to mark as deprecated

**Criteria for Rollback:**
- Validation script maintenance exceeds 8 hours/quarter
- Metadata drift incidents exceed 10% of commits
- Community feedback overwhelmingly negative (>70% negative sentiment)
- Cross-platform issues prove insurmountable (Windows compatibility <50%)

---

## Next Steps

1. **Review this implementation plan** with stakeholders (Architect, Curator, Template Maintainer)
2. **Approve or modify** based on feedback
3. **Assign resources** for Phase 1 (prototype)
4. **Execute Phase 1** (Week 1-2)
5. **Gate decision:** Evaluate Phase 1 results; proceed to Phase 2 only if no blockers
6. **Execute Phase 2** (Week 3-4)
7. **Execute Phase 3** (Week 5-6)
8. **Pilot test** with 3-5 early adopters
9. **Iterate** based on pilot feedback
10. **Announce** optional advanced profile in template release notes

---

_Prepared by: Architect Alphonso_  
_Related Documents: [ADR-022](../adrs/ADR-022-docsite-separated-metadata.md) | [Feasibility Study](../assessments/docsite-metadata-separation-feasibility-study.md) | [Risk Assessment](../assessments/docsite-metadata-separation-risks.md)_  
_Version: 1.0.0_  
_Last Updated: 2025-12-04_
