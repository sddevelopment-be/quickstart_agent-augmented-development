# Tactic: Documentation Curation Audit

**Invoked by:**
- [Directive 014 (Work Log Creation)](../directives/014_work_log_creation.md)
- Shorthand: [`/curate-directory`](../shorthands/curate-directory.md)

---

## Intent

Systematically audit a directory for structural consistency, naming conventions, cross-reference integrity, and metadata completeness.

**Apply when:**
- Documentation structure feels inconsistent
- After major reorganization
- Preparing for release (quality gate)
- Quarterly maintenance reviews

---

## Execution Steps

### 1. Structural Analysis
- [ ] Verify directory follows documented structure
- [ ] Check depth consistency (no >4 levels without reason)
- [ ] Identify orphaned files (no parent README reference)

### 2. Naming Convention Audit
- [ ] Apply consistent naming (kebab-case, snake_case, etc.)
- [ ] Rename SCREAMING_SNAKE_CASE if inappropriate
- [ ] Verify file extensions match content type

### 3. Cross-Reference Integrity
- [ ] Scan for broken links (grep for `]\(` patterns)
- [ ] Validate relative path references
- [ ] Check ADR/directive references exist

### 4. Metadata Completeness
- [ ] Verify frontmatter in structured docs
- [ ] Check version tags, dates, status fields
- [ ] Validate author/maintainer attribution

### 5. Discrepancy Report
- [ ] Generate findings list with severity (critical/high/medium/low)
- [ ] Recommend corrective actions
- [ ] Prioritize by impact

### 6. Apply Corrections
- [ ] Execute approved changes
- [ ] Validate corrections
- [ ] Document changes in work log

---

## Outputs
- Discrepancy report
- Corrective action recommendations
- Validation summary post-corrections

---

**Status:** ✅ Active
