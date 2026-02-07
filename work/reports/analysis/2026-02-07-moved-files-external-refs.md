# External References in Recently Moved Files

**Date:** 2026-02-07T15:15:00Z
**Context:** Analysis of directives and shorthands moved to doctrine/

## Summary

### Files Analyzed
- directive 003_repository_quick_reference.md ✅ Framework content with examples
- directive 004_documentation_context_files.md ✅ Framework content with examples
- directive 034_spec_driven_development.md ⚠️ Repository-specific paths
- directive 035_specification_frontmatter_standards.md ⚠️ Repository-specific paths
- shorthands/README.md (aliases.md) ✅ Clean
- shorthands/iteration-orchestration.md ⚠️ Repository-specific examples
- shorthands/SKILLS_CREATED.md ⚠️ Repository-specific examples

## Detailed Analysis

### 003_repository_quick_reference.md
**Status:** ✅ Framework content - References are **examples**

**References found:**
- `work/` paths (8 references) - Directory structure examples
- `docs/` paths (7 references) - Documentation structure examples

**Nature:** This directive describes **generic patterns** for repository structure.
The work/ and docs/ paths are **illustrative examples**, not dependencies.

**Action:** Needs light abstraction - parameterize examples or mark as "typical structure"

---

### 004_documentation_context_files.md
**Status:** ✅ Framework content - References are **canonical file patterns**

**References found:**
- `docs/VISION.md` - Generic pattern
- `docs/SURFACES.md` - Generic pattern
- `docs/WORKFLOWS.md` - Generic pattern
- `docs/planning/`, `docs/architecture/` - Generic patterns

**Nature:** Describes **framework expectations** for documentation structure.
References are patterns, not specific implementations.

**Action:** Already framework-appropriate. May benefit from noting these are "recommended patterns"

---

### 034_spec_driven_development.md
**Status:** ⚠️ Mixed - Has **repository-specific implementation details**

**References found:**
- `docs/specifications/` (5 references) - Local convention
- `docs/architecture/design/comparative_study/` (3 references) - **Specific repository files**
- Links to comparative analysis docs

**Nature:** 
- **Framework concept:** Spec-driven development methodology ✅
- **Repository-specific:** Paths to THIS repository's spec-kitty analysis ❌

**Action Required:**
1. **Abstract framework concept** → Keep in doctrine/
2. **Extract repository specifics** → Move to local docs/ or comment as "implementation example"
3. Parameterize paths: `${SPEC_ROOT}/features/` instead of `docs/specifications/features/`

**Critical issue:** Lines 325, 353-354 reference **specific files** in this repository's docs/

---

### 035_specification_frontmatter_standards.md
**Status:** ⚠️ Repository-specific conventions

**References found:**
- `specifications/` (28 references) - **This repository's structure**
- `docs/templates/specifications/` (2 references)
- `docs/audience/` (1 reference)
- Specific file examples: `specifications/llm-dashboard/orphan-task-assignment.md`

**Nature:** This directive defines **metadata standards for THIS repository's specification files**.
Heavily tied to local implementation (llm-dashboard examples, local directory structure).

**Action Required:** ⚠️ **Core Decision Needed**

**Option A:** Keep in doctrine/ as "example implementation"
- Mark all paths as parameterizable: `${SPEC_ROOT}/`
- Note that llm-dashboard is an example initiative

**Option B:** Move to repository-specific docs/
- This is a local convention, not universal framework
- Other repositories may have different spec structures

**Recommendation:** Move to `docs/conventions/specification-frontmatter.md`
- Too tied to this repository's initiative structure
- Frontmatter standards are implementation detail, not framework principle

---

### shorthands/README.md (aliases.md)
**Status:** ✅ Clean - No external references

**Action:** None needed

---

### shorthands/iteration-orchestration.md
**Status:** ⚠️ Has repository-specific paths in examples

**References found:**
- `work/collaboration/` (9 references)
- `docs/architecture/` (4 references)
- Specific files: `work/reports/reviews/`, `work/reports/logs/`

**Nature:** Orchestration workflow with **concrete examples** from this repository.

**Action:** Light abstraction
- Parameterize: `${WORKSPACE_ROOT}/collaboration/`
- Mark examples as "typical implementation"

---

### shorthands/SKILLS_CREATED.md
**Status:** ⚠️ Has repository-specific implementation details

**References found:**
- `work/collaboration/` (2 references)
- `work/reports/reviews/` (1 reference)
- `specifications/` (3 references)
- Specific example: `specifications/llm-dashboard/real-time-execution-dashboard.md`

**Nature:** Skills catalog with examples tied to this repository's structure.

**Action:** Abstract examples or mark as "reference implementation"

---

## Recommendations

### Immediate Actions

**1. Keep as-is (Framework appropriate):**
- ✅ 003_repository_quick_reference.md (examples are generic)
- ✅ 004_documentation_context_files.md (patterns, not specifics)
- ✅ shorthands/README.md (clean)

**2. Light abstraction needed:**
- ⚠️ shorthands/iteration-orchestration.md (parameterize work/ paths)
- ⚠️ shorthands/SKILLS_CREATED.md (parameterize examples)

**3. Moderate abstraction needed:**
- ⚠️ 034_spec_driven_development.md
  - Remove lines 325, 353-354 (specific file links)
  - Parameterize `docs/specifications/` → `${SPEC_ROOT}/`
  - Mark comparative-study as "example analysis location"

### Core Decision Required

**❓ 035_specification_frontmatter_standards.md:**

**Should this directive stay in doctrine/ or move to repository-specific docs/?**

**Arguments for keeping in doctrine/:**
- Frontmatter standards are useful pattern for any spec-driven repo
- Can be abstracted with parameterization
- Provides reusable convention

**Arguments for moving to local docs/:**
- Heavily tied to llm-dashboard initiative structure
- 28 references to local `specifications/` directory
- Specific examples (orphan-task-assignment, markdown-rendering)
- May not apply to repositories without initiative structure

**Recommendation:** 
Move to `docs/conventions/specification-frontmatter.md` as **repository-specific implementation** of spec-driven development concepts from directive 034.

---

## Path Parameterization Strategy

For files staying in doctrine/, use variable patterns:

```markdown
<!-- Before -->
Location: work/reports/logs/<agent>/

<!-- After -->
Location: ${WORKSPACE_ROOT}/reports/logs/<agent>/

<!-- With defaults in .doctrine/config.yaml -->
workspace_root: "work"
spec_root: "specifications"
doc_root: "docs"
```

---

## Next Steps

1. **Await human decision** on directive 035 location
2. Abstract directive 034 (remove specific file links)
3. Parameterize shorthands examples
4. Create `.doctrine/config.yaml` template
5. Document abstraction patterns

