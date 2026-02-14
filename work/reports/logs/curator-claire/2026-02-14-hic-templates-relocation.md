# HiC Templates Relocation Report

**Date:** 2026-02-14  
**Agent:** Curator Claire (Structural & Tonal Consistency Specialist)  
**Initiative:** Relocate HiC coordination templates to canonical doctrine location  
**Status:** ✅ Complete

---

## Executive Summary

Successfully relocated 4 Human-in-Charge coordination templates from scattered `work/human-in-charge/*/TEMPLATE.md` locations to canonical `doctrine/templates/coordination/` directory. This aligns with the doctrine principle that templates should live in `doctrine/templates/` (not in `work/` subdirectories).

**Impact:**
- ✅ Templates now follow canonical location pattern
- ✅ All references updated across 5 files
- ✅ Created comprehensive coordination template index (README.md)
- ✅ Work subdirectories remain functional (kept .gitkeep files)
- ✅ Zero breaking changes (old locations removed, new locations documented)

---

## What Was Relocated

### Templates Moved

| Old Location | New Location | Size | Renamed |
|--------------|--------------|------|---------|
| `work/human-in-charge/executive_summaries/TEMPLATE.md` | `doctrine/templates/coordination/hic-executive-summary.md` | 3,167 bytes | ✅ Yes |
| `work/human-in-charge/decision_requests/TEMPLATE.md` | `doctrine/templates/coordination/hic-decision-request.md` | 3,429 bytes | ✅ Yes |
| `work/human-in-charge/blockers/TEMPLATE.md` | `doctrine/templates/coordination/hic-blocker.md` | 3,581 bytes | ✅ Yes |
| `work/human-in-charge/problems/TEMPLATE.md` | `doctrine/templates/coordination/hic-problem.md` | 4,646 bytes | ✅ Yes |

**Naming Convention:** Templates renamed from generic `TEMPLATE.md` to descriptive `hic-{type}.md` pattern for clarity.

**Total Content:** 14,823 bytes (4 templates)

---

## Directory Structure Changes

### Before Relocation

```
work/human-in-charge/
├── README.md
├── QUICK_START.md
├── executive_summaries/
│   ├── .gitkeep
│   └── TEMPLATE.md              ← Removed
├── decision_requests/
│   ├── .gitkeep
│   └── TEMPLATE.md              ← Removed
├── blockers/
│   ├── .gitkeep
│   └── TEMPLATE.md              ← Removed
└── problems/
    ├── .gitkeep
    └── TEMPLATE.md              ← Removed
```

### After Relocation

```
doctrine/templates/coordination/   ← NEW canonical location
├── README.md                      ← NEW (10,050 bytes)
├── hic-executive-summary.md       ← MOVED + RENAMED
├── hic-decision-request.md        ← MOVED + RENAMED
├── hic-blocker.md                 ← MOVED + RENAMED
└── hic-problem.md                 ← MOVED + RENAMED

work/human-in-charge/              ← Work subdirectories preserved
├── README.md                      ← UPDATED
├── QUICK_START.md                 ← UPDATED
├── executive_summaries/
│   └── .gitkeep                   ✅ Kept
├── decision_requests/
│   └── .gitkeep                   ✅ Kept
├── blockers/
│   └── .gitkeep                   ✅ Kept
└── problems/
    └── .gitkeep                   ✅ Kept
```

**Key:** Work subdirectories remain functional for storing actual escalation files (instances). Templates now sourced from canonical doctrine location.

---

## Files Updated

### 1. `work/human-in-charge/README.md`

**Changes:**
- Updated directory structure diagram to show templates in `doctrine/templates/coordination/`
- Changed 4 template references from relative paths (`executive_summaries/TEMPLATE.md`) to absolute paths (`doctrine/templates/coordination/hic-executive-summary.md`)
- Updated example command from `cp work/human-in-charge/blockers/TEMPLATE.md` to `cp doctrine/templates/coordination/hic-blocker.md`
- Rewrote "Templates" section to reference canonical location

**Lines Modified:** 6 sections updated

---

### 2. `work/human-in-charge/QUICK_START.md`

**Changes:**
- Updated "What Was Built" directory diagram to show templates in doctrine
- Updated Quick Check commands to remove `! -name "TEMPLATE.md"` filters (no longer needed)
- Updated Quick Links section to point to `doctrine/templates/coordination/`

**Lines Modified:** 3 sections updated

---

### 3. `doctrine/agents/manager.agent.md`

**Changes:**
- Updated Manager Mike's executive summary creation reference from `work/human-in-charge/executive_summaries/TEMPLATE.md` to `doctrine/templates/coordination/hic-executive-summary.md`

**Lines Modified:** 1 line updated

---

### 4. `doctrine/directives/040_human_in_charge_escalation_protocol.md`

**Changes:**
- Added "Canonical Templates" section to File Format Standards
- Added note that template content shown in directive is condensed reference (full templates in doctrine)
- Documented canonical location: `doctrine/templates/coordination/`

**Lines Modified:** 1 section added (12 lines)

---

### 5. `doctrine/templates/coordination/README.md`

**Created:** ✅ New file (10,050 bytes)

**Content:**
- Comprehensive guide to all 4 HiC coordination templates
- When to use each template (with ✅/❌ patterns)
- Who creates each escalation type
- Priority ordering (blockers daily, decisions 2-3 days, problems weekly)
- Complete usage workflow for agents and HiC
- File naming conventions with examples
- Integration with Directive 040, ADR-047, AFK Mode
- Template maintenance guidelines
- Metrics and quality standards
- Related documentation cross-references

**Sections:** 14 major sections with complete operational guidance

---

## Verification Checklist

### ✅ Directory Structure
- [x] `doctrine/templates/coordination/` directory created
- [x] 4 templates copied with descriptive names
- [x] Old TEMPLATE.md files removed from work subdirectories
- [x] .gitkeep files preserved in work subdirectories
- [x] README.md created in coordination directory

### ✅ Template Content
- [x] hic-executive-summary.md - 3,167 bytes ✓
- [x] hic-decision-request.md - 3,429 bytes ✓
- [x] hic-blocker.md - 3,581 bytes ✓
- [x] hic-problem.md - 4,646 bytes ✓
- [x] All templates retain original content (no changes)

### ✅ Reference Updates
- [x] work/human-in-charge/README.md references updated (6 locations)
- [x] work/human-in-charge/QUICK_START.md references updated (3 locations)
- [x] doctrine/agents/manager.agent.md reference updated (1 location)
- [x] doctrine/directives/040_human_in_charge_escalation_protocol.md updated (1 section)
- [x] No broken links or references remain

### ✅ Documentation Quality
- [x] Canonical location clearly documented
- [x] Usage workflow explained (copy from doctrine to work)
- [x] File naming conventions maintained
- [x] Cross-references to Directive 040, ADR-047 intact
- [x] Integration with existing systems documented

### ✅ Functional Testing
- [x] Work subdirectories still functional (can accept escalation files)
- [x] Template access path clear (`doctrine/templates/coordination/`)
- [x] No breaking changes to existing escalation workflow
- [x] .gitkeep files ensure empty directories track in git

---

## Rationale for Changes

### Why Relocate Templates?

**Problem:** Templates were scattered in work subdirectories (`work/human-in-charge/*/TEMPLATE.md`), violating the doctrine principle that templates should live in `doctrine/templates/`.

**Canonical Pattern:**
```
doctrine/templates/        ← Templates (reusable contracts)
work/                      ← Work artifacts (instances)
```

**Benefits of Relocation:**

1. **Single Source of Truth:** Templates now have one canonical location in doctrine
2. **Clear Separation:** Work directories contain instances, doctrine contains contracts
3. **Discoverable:** All templates accessible from `doctrine/templates/` (not buried in work subdirectories)
4. **Maintainable:** Template updates happen in one place, agents copy updated versions
5. **Consistent:** Follows same pattern as other templates (specifications, ADRs, etc.)

### Why Rename Templates?

**Old:** `TEMPLATE.md` (generic, unclear type)  
**New:** `hic-executive-summary.md`, `hic-decision-request.md`, etc. (descriptive, clear purpose)

**Benefits:**
- **Clarity:** File name indicates template type without opening file
- **Searchable:** `hic-*` prefix groups all HiC templates together
- **Namespace:** Avoids collision with other template types
- **Descriptive:** Name conveys purpose (executive-summary vs decision-request)

---

## Impact Assessment

### Breaking Changes

**None.** This is a pure relocation with reference updates. No functionality changed.

### Agent Workflow Changes

**Before:**
```bash
cp work/human-in-charge/blockers/TEMPLATE.md \
   work/human-in-charge/blockers/2026-02-14-aws-credentials.md
```

**After:**
```bash
cp doctrine/templates/coordination/hic-blocker.md \
   work/human-in-charge/blockers/2026-02-14-aws-credentials.md
```

**Impact:** Source path changed, destination unchanged. Simple adjustment.

### Documentation Changes

**Updated:** 4 documentation files (README.md, QUICK_START.md, manager.agent.md, directive 040)  
**Created:** 1 new comprehensive index (coordination/README.md)  
**Total documentation:** 5 files updated/created

---

## Cross-References

### Updated Documents
- [work/human-in-charge/README.md](../../../work/human-in-charge/README.md) - Main HiC directory guide
- [work/human-in-charge/QUICK_START.md](../../../work/human-in-charge/QUICK_START.md) - Quick reference for HiC
- [doctrine/agents/manager.agent.md](../../../doctrine/agents/manager.agent.md) - Manager Mike profile
- [doctrine/directives/040_human_in_charge_escalation_protocol.md](../../../doctrine/directives/040_human_in_charge_escalation_protocol.md) - Complete escalation protocol

### Related Documentation
- [doctrine/templates/coordination/README.md](../../../doctrine/templates/coordination/README.md) - NEW canonical template index
- [docs/architecture/adrs/ADR-047-human-in-charge-directory-structure.md](../../../docs/architecture/adrs/ADR-047-human-in-charge-directory-structure.md) - Architecture decision
- [work/reports/logs/curator-claire/2026-02-14-hic-directory-implementation.md](./2026-02-14-hic-directory-implementation.md) - Original HiC implementation

---

## Migration Notes for Agents

### What Changed

**Old pattern:**
- Templates lived in `work/human-in-charge/*/TEMPLATE.md`
- Agents copied from same subdirectory where they'd save escalation

**New pattern:**
- Templates live in `doctrine/templates/coordination/hic-*.md`
- Agents copy from doctrine to work subdirectory

### No Action Required

✅ **Existing escalation files:** Unaffected (they're instances, not templates)  
✅ **Work subdirectories:** Still function exactly the same  
✅ **Escalation workflow:** Same process, just different source path for templates  
✅ **HiC review process:** Unchanged (still checks same subdirectories)

### For Future Escalations

**When creating new escalation:**
1. Identify escalation type (blocker, decision, problem, summary)
2. Copy template from `doctrine/templates/coordination/hic-{type}.md`
3. Save to `work/human-in-charge/{type}s/YYYY-MM-DD-[slug].md`
4. Fill all sections as before

**Example:**
```bash
# Old way (now deprecated)
# cp work/human-in-charge/blockers/TEMPLATE.md work/human-in-charge/blockers/2026-02-14-blocker.md

# New way (current)
cp doctrine/templates/coordination/hic-blocker.md \
   work/human-in-charge/blockers/2026-02-14-blocker.md
```

---

## Quality Metrics

### Structural Consistency

- ✅ **Canonical location:** Templates now in `doctrine/templates/` (correct layer)
- ✅ **Naming convention:** Descriptive `hic-{type}.md` pattern (clear, searchable)
- ✅ **Documentation completeness:** 10KB comprehensive README.md created
- ✅ **Cross-references:** All 4 documentation files updated with new paths
- ✅ **Zero broken links:** All references validated and updated

### Tonal Consistency

- ✅ **Terminology alignment:** "HiC coordination templates" used consistently
- ✅ **Directive integration:** Coordination templates explicitly linked to Directive 040
- ✅ **Approach alignment:** Follows file-based async coordination approach
- ✅ **Glossary compliance:** Terms like "canonical," "doctrine," "work directory" used correctly

### Operational Integrity

- ✅ **Zero breaking changes:** Old files removed only after new location documented
- ✅ **Work directories functional:** .gitkeep files preserved
- ✅ **Agent workflow clear:** README.md explains copy-from-doctrine pattern
- ✅ **HiC workflow unchanged:** Still checks same work subdirectories
- ✅ **Version control ready:** All changes git-trackable

---

## Lessons Learned

### What Went Well

1. **Clear rationale:** HiC request aligned with doctrine principles (templates in doctrine)
2. **Systematic approach:** Phased execution (create, move, update, verify, report)
3. **Documentation-first:** Created comprehensive README.md for coordination templates
4. **Reference integrity:** Found and updated all 10 template references across 5 files
5. **Zero breakage:** Work subdirectories remain functional throughout

### Template Location Best Practices

**Doctrine principle confirmed:**
- **Templates (reusable contracts):** `doctrine/templates/`
- **Instances (work artifacts):** `work/*/`
- **Agents copy templates to work directories when creating instances**

**Why this matters:**
- Single source of truth for template updates
- Clear separation of contracts vs. work artifacts
- Discoverable template library in doctrine
- Version-controlled template evolution

### Naming Convention Insights

**Generic names (`TEMPLATE.md`):**
- ❌ Unclear type without context
- ❌ Hard to search/grep
- ❌ Collision risk with other templates

**Descriptive names (`hic-blocker.md`):**
- ✅ Self-documenting purpose
- ✅ Searchable with `hic-*` pattern
- ✅ Namespace prevents collisions
- ✅ Alphabetically grouped

---

## Recommendations

### For Future Template Creation

When adding new templates to the system:

1. **Location:** Always create in `doctrine/templates/{category}/`
   - Use `{category}` to group related templates (coordination, specifications, etc.)
   - Never place templates in `work/` subdirectories

2. **Naming:** Use descriptive, prefixed names
   - Pattern: `{system}-{type}.md` (e.g., `hic-blocker.md`, `spec-feature.md`)
   - Avoid generic names like `TEMPLATE.md`

3. **Documentation:** Create category README.md
   - When to use each template
   - Usage workflow (copy → fill → save)
   - Integration with related directives/approaches

4. **Cross-references:** Update all related documents
   - Agent profiles that use templates
   - Directives that reference templates
   - Approach documents explaining workflow

### For Template Maintenance

**Version Control:**
- Templates evolve with doctrine version
- Agents copy current version when creating instances
- Old instances retain their template version (not retroactively updated)

**Update Process:**
1. Edit template in `doctrine/templates/{category}/`
2. Document change in category README.md changelog
3. Update related directives if format changes significantly
4. Notify agents via directive update or changelog

**Quality Standards:**
- Templates should be self-documenting (inline comments explaining sections)
- Include YAML frontmatter with all required metadata fields
- Provide examples of filled sections in comments or README
- Cross-reference to directives/approaches explaining usage

---

## Completion Checklist

### ✅ Phase 1: Directory Structure
- [x] Created `doctrine/templates/coordination/` directory
- [x] Verified directory in correct location

### ✅ Phase 2: Template Relocation
- [x] Copied 4 templates to new location
- [x] Renamed templates with descriptive names
- [x] Removed old TEMPLATE.md files from work subdirectories
- [x] Preserved .gitkeep files in work subdirectories

### ✅ Phase 3: Coordination Index
- [x] Created comprehensive README.md (10,050 bytes)
- [x] Documented all 4 templates with usage guidance
- [x] Explained when to use each template
- [x] Provided complete usage workflow
- [x] Cross-referenced related documentation

### ✅ Phase 4: Reference Updates
- [x] Updated work/human-in-charge/README.md (6 locations)
- [x] Updated work/human-in-charge/QUICK_START.md (3 locations)
- [x] Updated doctrine/agents/manager.agent.md (1 location)
- [x] Updated doctrine/directives/040_human_in_charge_escalation_protocol.md (1 section)
- [x] Verified no broken references remain

### ✅ Phase 5: Verification
- [x] All templates accessible at new location
- [x] All references point to new location
- [x] Work subdirectories functional
- [x] Documentation complete and accurate
- [x] Zero breaking changes

### ✅ Phase 6: Reporting
- [x] Created relocation report (this document)
- [x] Documented all changes and rationale
- [x] Provided migration notes for agents
- [x] Included lessons learned and recommendations

---

## Summary Statistics

**Files Created:** 5
- 4 templates relocated (hic-executive-summary.md, hic-decision-request.md, hic-blocker.md, hic-problem.md)
- 1 coordination index (README.md)

**Files Updated:** 4
- work/human-in-charge/README.md
- work/human-in-charge/QUICK_START.md
- doctrine/agents/manager.agent.md
- doctrine/directives/040_human_in_charge_escalation_protocol.md

**Files Removed:** 4
- work/human-in-charge/executive_summaries/TEMPLATE.md
- work/human-in-charge/decision_requests/TEMPLATE.md
- work/human-in-charge/blockers/TEMPLATE.md
- work/human-in-charge/problems/TEMPLATE.md

**Total Documentation:** 24,873 bytes
- Templates: 14,823 bytes (4 files)
- README.md: 10,050 bytes (1 file)

**References Updated:** 10 locations across 4 files

**Breaking Changes:** 0

**Time Investment:** ~2 hours (systematic relocation + comprehensive documentation)

---

## Status

**Phase:** ✅ Complete  
**Date Completed:** 2026-02-14  
**Agent:** Curator Claire  
**Verification:** All templates relocated, references updated, documentation complete  
**Next Steps:** None required - relocation complete and verified

---

## Appendix: File Paths Reference

### New Canonical Template Locations

```
doctrine/templates/coordination/
├── README.md                      # Coordination template index
├── hic-executive-summary.md       # Executive summary template
├── hic-decision-request.md        # Decision request template
├── hic-blocker.md                 # Blocker template
└── hic-problem.md                 # Problem template
```

### Work Directory Structure (Unchanged)

```
work/human-in-charge/
├── README.md                      # HiC directory guide
├── QUICK_START.md                 # Quick reference for HiC
├── executive_summaries/           # Instances saved here
│   └── .gitkeep
├── decision_requests/             # Instances saved here
│   └── .gitkeep
├── blockers/                      # Instances saved here
│   └── .gitkeep
└── problems/                      # Instances saved here
    └── .gitkeep
```

### Updated Documentation References

- `doctrine/directives/040_human_in_charge_escalation_protocol.md` - Line 152 (File Format Standards section)
- `doctrine/agents/manager.agent.md` - Line 178 (Executive Summary creation)
- `work/human-in-charge/README.md` - Lines 26-40 (directory structure), 71, 91, 117, 139, 162, 373-379 (templates section)
- `work/human-in-charge/QUICK_START.md` - Lines 13-28 (directory structure), 45-49 (commands), 108 (quick links)

---

**Report Author:** Curator Claire  
**Report Date:** 2026-02-14  
**Report Status:** ✅ Final  
**Related Initiative:** HiC Directory Structure & Coordination Templates
