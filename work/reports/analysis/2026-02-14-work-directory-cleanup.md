# Work Directory Cleanup & Consolidation Analysis

**Agent:** Curator Claire  
**Date:** 2026-02-14  
**Status:** ⏳ Pending Approval  
**Purpose:** Structural consistency audit and consolidation plan for `work/` directory

---

## Executive Summary

The `work/` directory currently contains **1,099 files** across **199 directories** (6.3M total size). This analysis identifies significant structural redundancies, inconsistent naming patterns, and opportunities for consolidation aligned with doctrine expectations.

### Key Findings

❗️ **Critical Issues:**
1. **Triple-redundancy in log storage:** `work/logs/`, `work/reports/logs/`, and per-agent subdirectories
2. **Coordination vs. Collaboration overlap:** `work/coordination/` (284K) duplicates `work/collaboration/` (2.5M) purposes
3. **Inconsistent agent-specific organization:** Mixed patterns across directories
4. **Loose files in work/ root:** 3 markdown files lack proper categorization
5. **Agent-specific directories outside collaboration/:** `work/synthesizer/`, `work/telemetry/`, `work/curator/`, etc.

✅ **Positive Observations:**
- `work/collaboration/` has correct task workflow structure (inbox/assigned/done/archive)
- `work/reports/` has comprehensive subdirectories for specialized reports
- No empty directories detected (all contain `.gitkeep` or files)

---

## Current State Analysis

### Directory Inventory (by size)

| Directory | Size | File Count | Purpose | Status |
|-----------|------|------------|---------|--------|
| `reports/` | 6.3M | 520+ | Agent outputs, logs, metrics | ✅ Keep (consolidate logs) |
| `collaboration/` | 2.5M | 166+ | Task orchestration | ✅ Keep (canonical) |
| `curator/` | 808K | ? | Curator work artifacts | ⚠️ Move to collaboration/assigned/curator/ |
| `logs/` | 660K | 51 | Legacy work logs | ⚠️ **Redundant** - merge to reports/logs/ |
| `notes/` | 624K | ? | Project notes | ✅ Keep |
| `planning/` | 392K | ? | Planning artifacts | ⚠️ Review for collaboration/assigned/planning/ |
| `glossary-candidates/` | 348K | ? | Glossary work | ⚠️ Move to collaboration/assigned/lexical/ |
| `coordination/` | 284K | 20 | Coordination artifacts | ⚠️ **Redundant** - merge to collaboration/ |
| `analysis/` | 220K | ? | Analysis reports | ⚠️ Merge to reports/analysis/ |
| `LEX/` | 80K | ? | Lexical analysis | ⚠️ Move to collaboration/done/lexical/ |
| `articles/` | 60K | ? | Article drafts | ⚠️ Move to reports/research/ or notes/ |
| `archive/` | 56K | ? | Archived work | ✅ Keep |
| `architect/` | 40K | ? | Architect work | ⚠️ Move to collaboration/assigned/architect/ |
| `tasks/` | 36K | ? | Task definitions | ⚠️ Review for collaboration/ |
| `prompts/` | 36K | ? | Prompt experiments | ⚠️ Move to notes/ or archive/ |
| `telemetry/` | 32K | 3 | Telemetry docs | ⚠️ Move to docs/ or collaboration/done/ |
| `validation/` | 28K | ? | Validation reports | ⚠️ Merge to reports/validation/ |
| `schemas/` | 28K | ? | Schema artifacts | ⚠️ Move to collaboration/done/ |
| `synthesizer/` | 24K | ? | Synthesizer work | ⚠️ Move to collaboration/assigned/synthesizer/ |
| `research/` | 20K | ? | Research notes | ⚠️ Merge to reports/research/ |
| `analyst/` | 20K | ? | Analyst work | ⚠️ Move to collaboration/assigned/analyst/ |
| `session-summaries/` | 12K | ? | Session logs | ⚠️ Merge to reports/logs/ |
| `status/` | 8.0K | ? | Status reports | ⚠️ Merge to reports/ |
| `templates/` | 4.0K | .gitkeep only | Templates | ✅ Keep (reserved) |

### Structural Redundancies

#### 1. **Log Storage Triple-Redundancy**

**Problem:** Work logs are stored in three locations:

```
work/logs/                          # 51 files (660K)
  ├── 2026-02-05/
  ├── architect/
  ├── build-automation/
  ├── dashboard/
  ├── diagrammer/
  ├── framework-guardian/
  ├── frontend/
  ├── manager/
  ├── planning-petra/
  ├── python-pedro/
  └── writer-editor/

work/reports/logs/                  # 274 files (embedded in 6.3M)
  ├── analyst/
  ├── analyst-annie/
  ├── architect/
  ├── architect-alphonso/
  ├── backend-benny/
  ├── [... 30+ agent subdirectories ...]
  └── writer-editor/

work/coordination/                  # 20 coordination logs mixed with status
  ├── 2026-02-11-manager-mike-work-log.md
  ├── WORKFLOW_LOG.md
  ├── AGENT_STATUS.md
  └── [... coordination artifacts ...]
```

**Recommendation:** 
- ✅ **Canonical location:** `work/reports/logs/` (comprehensive, well-organized)
- 🔀 **Migrate:** All files from `work/logs/` → `work/reports/logs/`
- 🔀 **Migrate:** Coordination logs from `work/coordination/` → `work/reports/logs/manager/`

#### 2. **Coordination vs. Collaboration Overlap**

**Problem:** Two directories serve similar purposes:

- `work/collaboration/` - Task-based workflow (inbox/assigned/done/archive) ✅
- `work/coordination/` - Coordination artifacts, status reports, work logs ❌

**Analysis:**
- `work/collaboration/` follows doctrine-specified task workflow structure
- `work/coordination/` contains 20 files that belong in either:
  - `work/collaboration/` (coordination artifacts like HANDOFFS.md)
  - `work/reports/logs/manager/` (work logs)
  - `work/reports/orchestration/` (orchestration reports)

**Recommendation:**
- 🔀 **Migrate coordination artifacts:** AGENT_STATUS.md, WORKFLOW_LOG.md, HANDOFFS.md → `work/collaboration/`
- 🔀 **Migrate work logs:** *-work-log.md → `work/reports/logs/manager/`
- 🔀 **Migrate orchestration reports:** *-orchestration-*.md → `work/reports/orchestration/`
- 🗑️ **Remove:** `work/coordination/` directory after migration

#### 3. **Agent-Specific Directories Outside Collaboration**

**Problem:** Agent work artifacts scattered across work/ root instead of collaboration structure:

```
work/
  ├── curator/           # Should be collaboration/assigned/curator/
  ├── architect/         # Should be collaboration/assigned/architect/
  ├── analyst/           # Should be collaboration/assigned/analyst/
  ├── synthesizer/       # Should be collaboration/assigned/synthesizer/
  ├── LEX/               # Should be collaboration/done/lexical/
  ├── glossary-candidates/  # Should be collaboration/assigned/lexical/
  └── telemetry/         # Should be collaboration/done/ (completed work)
```

**Recommendation:**
- 🔀 **Active work:** Move to `work/collaboration/assigned/<agent-slug>/`
- 🔀 **Completed work:** Move to `work/collaboration/done/<agent-slug>/`
- Ensures consistency with task workflow structure

#### 4. **Report Directory Inconsistencies**

**Problem:** Analysis, validation, and research reports duplicated:

- `work/analysis/` exists but `work/reports/analysis/` also exists
- `work/validation/` exists but `work/reports/validation/` also exists  
- `work/research/` exists but `work/reports/research/` also exists

**Recommendation:**
- 🔀 **Consolidate to:** `work/reports/{analysis,validation,research}/`
- Maintains canonical reports location

#### 5. **Loose Files in work/ Root**

**Files requiring categorization:**
- `work/20260212-212335-bootstrap-initialization.md` → `work/reports/logs/bootstrap-bill/`
- `work/boy_scout_sqlite_fix.md` → `work/reports/refactoring/` or `work/archive/2026-02/`
- `work/README.md` ✅ (keep - directory documentation)

---

## Proposed Consolidation Plan

### Phase 1: Canonical Structure Definition

**Expected Structure (Aligned with Doctrine):**

```
work/
├── README.md                      # ✅ Directory documentation
├── .gitkeep                       # ✅ Git tracking
│
├── collaboration/                 # ✅ CANONICAL - Task orchestration
│   ├── README.md                  # Task workflow documentation
│   ├── inbox/                     # New tasks
│   ├── assigned/<agent-slug>/     # Active tasks per agent
│   ├── done/<agent-slug>/         # Completed tasks per agent
│   ├── archive/YYYY-MM/           # Archived tasks
│   ├── fridge/                    # On-hold work
│   ├── handoffs/                  # Agent handoffs
│   ├── backups/                   # Task backups
│   ├── AGENT_STATUS.md            # ⬅️ FROM coordination/
│   ├── WORKFLOW_LOG.md            # ⬅️ FROM coordination/
│   ├── HANDOFFS.md                # ⬅️ FROM coordination/
│   ├── AGENT_TASKS.md             # ✅ Keep
│   ├── DEPENDENCIES.md            # ✅ Keep
│   └── NEXT_BATCH.md              # ✅ Keep
│
├── reports/                       # ✅ CANONICAL - All agent outputs
│   ├── README.md                  # Reports documentation
│   ├── logs/<agent-slug>/         # ⬅️ MERGE work/logs/ here
│   ├── analysis/                  # ⬅️ MERGE work/analysis/ here
│   ├── validation/                # ⬅️ MERGE work/validation/ here
│   ├── research/                  # ⬅️ MERGE work/research/ here
│   ├── orchestration/             # ⬅️ FROM coordination/
│   ├── architecture/              # ✅ Keep
│   ├── assessments/               # ✅ Keep
│   ├── benchmarks/                # ✅ Keep
│   ├── checkpoints/               # ✅ Keep
│   ├── compliance/                # ✅ Keep
│   ├── curation/                  # ✅ Keep
│   ├── dashboards/                # ✅ Keep
│   ├── exec_summaries/            # ✅ Keep (rename to executive-summaries)
│   ├── executive-summaries/       # ✅ Keep (consolidate with exec_summaries)
│   ├── metrics/                   # ✅ Keep
│   ├── planning/                  # ✅ Keep
│   ├── pr-summaries/              # ✅ Keep
│   ├── ralph-checks/              # ✅ Keep
│   ├── refactoring/               # ✅ Keep
│   ├── reflections/               # ✅ Keep
│   ├── review/                    # ✅ Keep (consolidate with reviews/)
│   ├── reviews/                   # ✅ Keep
│   ├── synthesis/                 # ✅ Keep
│   └── _archive/                  # ✅ Keep
│
├── notes/                         # ✅ CANONICAL - Persistent notes
│   ├── external_memory/           # Inter-agent context
│   └── [other notes]              # ⬅️ FROM work/prompts/, work/articles/
│
├── planning/                      # ✅ CANONICAL - Planning artifacts
│   └── [planning docs]            # Review for duplication with collaboration/
│
├── archive/                       # ✅ CANONICAL - Long-term retention
│   ├── 2026-02-14/                # Today's cleanup archive
│   └── [YYYY-MM-DD/]              # Historical archives
│
├── templates/                     # ✅ CANONICAL - Reserved
│   └── .gitkeep
│
└── schemas/                       # ⚠️ Review for move to collaboration/done/
```

**Removed/Consolidated:**
- ❌ `work/coordination/` → Merged to `collaboration/` and `reports/orchestration/`
- ❌ `work/logs/` → Merged to `reports/logs/`
- ❌ `work/analysis/` → Merged to `reports/analysis/`
- ❌ `work/validation/` → Merged to `reports/validation/`
- ❌ `work/research/` → Merged to `reports/research/`
- ❌ `work/curator/` → Moved to `collaboration/assigned/curator/`
- ❌ `work/architect/` → Moved to `collaboration/assigned/architect/`
- ❌ `work/analyst/` → Moved to `collaboration/assigned/analyst/`
- ❌ `work/synthesizer/` → Moved to `collaboration/assigned/synthesizer/`
- ❌ `work/LEX/` → Moved to `collaboration/done/lexical/`
- ❌ `work/glossary-candidates/` → Moved to `collaboration/assigned/lexical/`
- ❌ `work/telemetry/` → Moved to `collaboration/done/telemetry/`
- ❌ `work/session-summaries/` → Merged to `reports/logs/`
- ❌ `work/status/` → Merged to `reports/`
- ❌ `work/tasks/` → Review and merge to `collaboration/`
- ❌ `work/prompts/` → Move to `notes/` or `archive/`
- ❌ `work/articles/` → Move to `notes/` or `reports/research/`

---

## Detailed Migration Plan

### Phase 2: Pre-Migration Validation

**Before moving any files:**

1. ✅ **Verify no active agent processes** referencing work/ files
2. ✅ **Check for cross-references** in documentation (grep work/)
3. ✅ **Backup current state** to `work/archive/2026-02-14-pre-cleanup/`
4. ✅ **Create migration log** in `work/reports/curation/`

### Phase 3: Migration Execution

**Order of operations (sequential to avoid conflicts):**

#### Step 1: Create Archive Snapshot
```bash
# Archive current state before any changes
mkdir -p work/archive/2026-02-14-pre-cleanup
cp -r work/coordination work/archive/2026-02-14-pre-cleanup/
cp -r work/logs work/archive/2026-02-14-pre-cleanup/
# [... other directories being modified ...]
```

#### Step 2: Merge Logs (work/logs/ → work/reports/logs/)
```bash
# Migrate agent-specific logs
for dir in work/logs/*/; do
  agent=$(basename "$dir")
  mkdir -p "work/reports/logs/$agent"
  mv "$dir"/* "work/reports/logs/$agent/" 2>/dev/null || true
done

# Migrate root-level log files
mv work/logs/*.md work/reports/logs/generic/ 2>/dev/null || true

# Remove empty work/logs/
rmdir work/logs/*/
rmdir work/logs/
```

#### Step 3: Merge Coordination (work/coordination/ → work/collaboration/ + work/reports/)
```bash
# Move coordination artifacts to collaboration/
mv work/coordination/AGENT_STATUS.md work/collaboration/
mv work/coordination/WORKFLOW_LOG.md work/collaboration/
mv work/coordination/HANDOFFS.md work/collaboration/
mv work/coordination/ENHANCEMENT_SUMMARY.md work/collaboration/
mv work/coordination/ORCHESTRATION_QUICK_REFERENCE.md work/collaboration/
mv work/coordination/PROFILE_ENHANCEMENT_LOG.md work/collaboration/

# Move orchestration reports
mkdir -p work/reports/orchestration
mv work/coordination/*-orchestration-*.md work/reports/orchestration/ 2>/dev/null || true

# Move work logs to reports
mv work/coordination/*-work-log.md work/reports/logs/manager/ 2>/dev/null || true
mv work/coordination/*-execution-*.md work/reports/orchestration/ 2>/dev/null || true

# Move remaining artifacts
mv work/coordination/*.md work/reports/orchestration/ 2>/dev/null || true

# Remove empty coordination/
rmdir work/coordination/
```

#### Step 4: Consolidate Agent Directories
```bash
# Active agent work → collaboration/assigned/
mv work/curator/* work/collaboration/assigned/curator/ 2>/dev/null || true
mv work/architect/* work/collaboration/assigned/architect/ 2>/dev/null || true
mv work/analyst/* work/collaboration/assigned/analyst/ 2>/dev/null || true
mv work/synthesizer/* work/collaboration/assigned/synthesizer/ 2>/dev/null || true
mv work/glossary-candidates/* work/collaboration/assigned/lexical/glossary-candidates/ 2>/dev/null || true

# Completed work → collaboration/done/
mv work/LEX/* work/collaboration/done/lexical/LEX/ 2>/dev/null || true
mv work/telemetry/* work/collaboration/done/telemetry/ 2>/dev/null || true
mv work/schemas/* work/collaboration/done/schemas/ 2>/dev/null || true

# Remove emptied directories
rmdir work/curator work/architect work/analyst work/synthesizer
rmdir work/glossary-candidates work/LEX work/telemetry work/schemas
```

#### Step 5: Consolidate Report Directories
```bash
# Merge analysis/
mv work/analysis/* work/reports/analysis/ 2>/dev/null || true
rmdir work/analysis/

# Merge validation/
mv work/validation/* work/reports/validation/ 2>/dev/null || true
rmdir work/validation/

# Merge research/
mv work/research/* work/reports/research/ 2>/dev/null || true
rmdir work/research/

# Merge session-summaries/
mv work/session-summaries/* work/reports/logs/generic/ 2>/dev/null || true
rmdir work/session-summaries/

# Merge status/
mv work/status/* work/reports/orchestration/ 2>/dev/null || true
rmdir work/status/

# Consolidate executive summaries (exec_summaries → executive-summaries)
mv work/reports/exec_summaries/* work/reports/executive-summaries/ 2>/dev/null || true
rmdir work/reports/exec_summaries/

# Consolidate review directories
mv work/reports/review/* work/reports/reviews/ 2>/dev/null || true
rmdir work/reports/review/
```

#### Step 6: Handle Loose Files
```bash
# Categorize root-level files
mv work/20260212-212335-bootstrap-initialization.md work/reports/logs/bootstrap-bill/
mv work/boy_scout_sqlite_fix.md work/reports/refactoring/
```

#### Step 7: Review and Categorize Remaining Directories
```bash
# Planning - review for duplication
# Articles - move to notes/ or reports/research/
# Prompts - move to notes/ or archive/
# Tasks - review and merge to collaboration/

# Move prompts to notes
mkdir -p work/notes/prompts
mv work/prompts/* work/notes/prompts/ 2>/dev/null || true
rmdir work/prompts/

# Move articles to reports/research
mv work/articles/* work/reports/research/ 2>/dev/null || true
rmdir work/articles/
```

### Phase 4: Post-Migration Validation

**After migration:**

1. ✅ **Verify file counts:** Ensure no files lost (`find work/ -type f | wc -l`)
2. ✅ **Check for broken references:** `grep -r "work/logs/" docs/ .github/ README.md`
3. ✅ **Validate structure:** Compare against canonical structure
4. ✅ **Update documentation:** Fix cross-references in README files
5. ✅ **Git commit:** Clear migration commit with full summary

---

## Naming Convention Standardization

### Current Inconsistencies

1. **Date formats:**
   - ✅ ISO 8601: `2026-02-14` (preferred)
   - ❌ Compact: `20260212` 
   - ❌ With time: `2026-01-31T0638`

2. **Agent naming:**
   - ✅ Slug format: `backend-benny`, `curator-claire` (preferred)
   - ❌ Role only: `architect`, `analyst`
   - ❌ Mixed: `planning-petra` vs `planning`

3. **Directory naming:**
   - ✅ Lowercase with hyphens: `executive-summaries` (preferred)
   - ❌ Underscore: `exec_summaries`
   - ❌ Mixed: `pr-summaries` vs `session-summaries`

### Recommended Standards

**File Naming:**
```
YYYY-MM-DD-<agent-slug>-<description>.md
YYYY-MM-DD-<type>-<description>.md
```

**Directory Naming:**
```
lowercase-with-hyphens/
<agent-slug>/  (for agent-specific subdirectories)
```

**Agent Slugs (Canonical):**
- analyst-annie
- architect-alphonso
- backend-benny
- bootstrap-bill
- code-reviewer-cindy
- curator-claire
- devops-danny
- diagrammer-diana
- framework-guardian-gary
- frontend-freddy
- java-jenny
- lexical-lex
- manager-mike
- planning-petra
- python-pedro
- researcher-ralph
- scribe-sally
- synthesizer-steve
- test-terry
- translator-tony
- writer-editor-wendy

---

## Risk Assessment

### Low Risk
- ✅ Merging logs (no active dependencies)
- ✅ Consolidating reports (canonical location already exists)
- ✅ Moving completed work to collaboration/done/

### Medium Risk
- ⚠️ Removing coordination/ (verify no scripts reference it)
- ⚠️ Moving agent directories (check for active work)
- ⚠️ Renaming directories (update cross-references)

### Mitigation Strategies
1. **Full backup:** Archive current state before changes
2. **Staged execution:** Migrate in phases with validation checkpoints
3. **Documentation updates:** Fix cross-references immediately
4. **Git history:** Clear commits for easy rollback
5. **Verification scripts:** Automated checks for broken references

---

## Success Criteria

### Structural
- ✅ All logs in `work/reports/logs/<agent-slug>/`
- ✅ No duplicate directories (coordination/, analysis/, etc.)
- ✅ Agent work in `work/collaboration/assigned/` or `done/`
- ✅ Consistent naming conventions
- ✅ No loose files in work/ root (except README.md, .gitkeep)

### Functional
- ✅ No broken cross-references in documentation
- ✅ All files accounted for (no data loss)
- ✅ Git history clean and traceable
- ✅ README files updated to reflect new structure

### Compliance
- ✅ Aligned with doctrine expectations from `work/README.md`
- ✅ Follows task workflow structure (inbox/assigned/done/archive)
- ✅ Canonical locations clearly defined

---

## Approval Request

**This analysis proposes:**
1. ✅ Merging 3 redundant directories (coordination, logs, analysis/validation/research)
2. ✅ Moving 10 agent-specific directories to collaboration/
3. ✅ Consolidating 5 report subdirectories
4. ✅ Standardizing naming conventions
5. ✅ Removing ~15 empty or redundant directory structures

**Total impact:**
- **Before:** 199 directories, 1,099 files
- **After:** ~150 directories (25% reduction), 1,099 files (no loss)
- **Complexity reduction:** 40% fewer top-level directories

**Estimated execution time:** 30-45 minutes (scripted migration)

---

## Next Steps

**Awaiting approval to proceed with:**

1. **Phase 1:** Create archive snapshot
2. **Phase 2:** Execute migration script
3. **Phase 3:** Validate post-migration state
4. **Phase 4:** Update documentation and commit

**Questions for stakeholder:**
1. ❓ Should `work/planning/` be reviewed for duplication with `collaboration/assigned/planning/`?
2. ❓ Archive policy for `work/articles/` - move to `notes/` or `reports/research/`?
3. ❓ Retain `work/schemas/` separately or move to `collaboration/done/schemas/`?

---

**Report Status:** ⏳ Awaiting Approval  
**Next Action:** Execute migration upon confirmation  
**Curator:** Claire  
**Date:** 2026-02-14
