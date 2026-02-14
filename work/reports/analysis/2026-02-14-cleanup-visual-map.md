# Work Directory Cleanup - Visual Migration Map

**Agent:** Curator Claire  
**Date:** 2026-02-14  
**Purpose:** Visual representation of proposed directory consolidation

---

## Current State → Target State

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CURRENT STATE (199 dirs)                        │
└─────────────────────────────────────────────────────────────────────────┘

work/
├── 📂 collaboration/ (2.5M) ✅ CANONICAL - Task workflow
│   ├── inbox/
│   ├── assigned/<agent>/
│   ├── done/<agent>/
│   └── archive/
│
├── 📂 reports/ (6.3M) ✅ CANONICAL - All outputs
│   ├── logs/<agent>/
│   ├── analysis/
│   ├── validation/
│   └── [... 20+ subdirs ...]
│
├── ❗️ logs/ (660K) ⚠️ REDUNDANT - Duplicate of reports/logs/
│   ├── architect/
│   ├── python-pedro/
│   └── [... agent subdirs ...]
│
├── ❗️ coordination/ (284K) ⚠️ REDUNDANT - Overlaps collaboration/
│   ├── AGENT_STATUS.md
│   ├── WORKFLOW_LOG.md
│   └── [... coordination files ...]
│
├── ❗️ curator/ (808K) ⚠️ MISPLACED - Should be in collaboration/
├── ❗️ architect/ (40K) ⚠️ MISPLACED
├── ❗️ analyst/ (20K) ⚠️ MISPLACED
├── ❗️ synthesizer/ (24K) ⚠️ MISPLACED
├── ❗️ LEX/ (80K) ⚠️ MISPLACED - Completed work
├── ❗️ glossary-candidates/ (348K) ⚠️ MISPLACED
├── ❗️ telemetry/ (32K) ⚠️ MISPLACED - Completed work
├── ❗️ schemas/ (28K) ⚠️ MISPLACED - Completed work
│
├── ❗️ analysis/ (220K) ⚠️ REDUNDANT - Duplicate of reports/analysis/
├── ❗️ validation/ (28K) ⚠️ REDUNDANT - Duplicate of reports/validation/
├── ❗️ research/ (20K) ⚠️ REDUNDANT - Duplicate of reports/research/
├── ❗️ session-summaries/ (12K) ⚠️ REDUNDANT - Belongs in reports/logs/
├── ❗️ status/ (8.0K) ⚠️ REDUNDANT - Belongs in reports/
│
├── ❓ planning/ (392K) ⚠️ REVIEW - May overlap collaboration/
├── ❓ prompts/ (36K) ⚠️ REVIEW - Archive or move to notes/
├── ❓ articles/ (60K) ⚠️ REVIEW - Move to notes/ or research/
├── ❓ tasks/ (36K) ⚠️ REVIEW - Merge to collaboration/
│
├── 📂 notes/ (624K) ✅ KEEP - Persistent notes
├── 📂 archive/ (56K) ✅ KEEP - Long-term retention
└── 📂 templates/ (4.0K) ✅ KEEP - Reserved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────────────┐
│                         TARGET STATE (150 dirs)                         │
└─────────────────────────────────────────────────────────────────────────┘

work/
├── 📂 collaboration/ ✅ CANONICAL - Task workflow
│   ├── inbox/
│   ├── assigned/
│   │   ├── curator/         ⬅️ FROM work/curator/
│   │   ├── architect/       ⬅️ FROM work/architect/
│   │   ├── analyst/         ⬅️ FROM work/analyst/
│   │   ├── synthesizer/     ⬅️ FROM work/synthesizer/
│   │   ├── lexical/
│   │   │   └── glossary-candidates/ ⬅️ FROM work/glossary-candidates/
│   │   └── [... other agents ...]
│   ├── done/
│   │   ├── lexical/
│   │   │   └── LEX/         ⬅️ FROM work/LEX/
│   │   ├── telemetry/       ⬅️ FROM work/telemetry/
│   │   ├── schemas/         ⬅️ FROM work/schemas/
│   │   └── [... other agents ...]
│   ├── archive/
│   ├── AGENT_STATUS.md      ⬅️ FROM work/coordination/
│   ├── WORKFLOW_LOG.md      ⬅️ FROM work/coordination/
│   ├── HANDOFFS.md          ⬅️ FROM work/coordination/
│   └── [... other tracking ...]
│
├── 📂 reports/ ✅ CANONICAL - All outputs
│   ├── logs/
│   │   ├── <agent>/         ⬅️ MERGED FROM work/logs/<agent>/
│   │   ├── generic/         ⬅️ FROM work/session-summaries/
│   │   └── manager/         ⬅️ FROM work/coordination/*-log.md
│   ├── analysis/            ⬅️ MERGED FROM work/analysis/
│   ├── validation/          ⬅️ MERGED FROM work/validation/
│   ├── research/            ⬅️ MERGED FROM work/research/
│   ├── orchestration/       ⬅️ FROM work/coordination/*-orchestration-*
│   ├── executive-summaries/ ⬅️ MERGED FROM exec_summaries/
│   ├── reviews/             ⬅️ MERGED FROM review/
│   └── [... other reports ...]
│
├── 📂 notes/ ✅ KEEP
│   ├── external_memory/
│   └── prompts/             ⬅️ FROM work/prompts/
│
├── 📂 planning/ ✅ KEEP (review for duplication)
├── 📂 archive/ ✅ KEEP
│   └── 2026-02-14-pre-cleanup/ ⬅️ BACKUP before changes
└── 📂 templates/ ✅ KEEP

REMOVED:
  ❌ work/logs/               → Merged to reports/logs/
  ❌ work/coordination/       → Merged to collaboration/ + reports/orchestration/
  ❌ work/curator/            → Moved to collaboration/assigned/curator/
  ❌ work/architect/          → Moved to collaboration/assigned/architect/
  ❌ work/analyst/            → Moved to collaboration/assigned/analyst/
  ❌ work/synthesizer/        → Moved to collaboration/assigned/synthesizer/
  ❌ work/LEX/                → Moved to collaboration/done/lexical/
  ❌ work/glossary-candidates/ → Moved to collaboration/assigned/lexical/
  ❌ work/telemetry/          → Moved to collaboration/done/telemetry/
  ❌ work/schemas/            → Moved to collaboration/done/schemas/
  ❌ work/analysis/           → Merged to reports/analysis/
  ❌ work/validation/         → Merged to reports/validation/
  ❌ work/research/           → Merged to reports/research/
  ❌ work/session-summaries/  → Merged to reports/logs/generic/
  ❌ work/status/             → Merged to reports/orchestration/
  ❌ work/prompts/            → Moved to notes/prompts/
  ❌ work/articles/           → [Decision pending]
  ❌ work/tasks/              → [Review for collaboration/]
```

---

## Migration Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           MIGRATION PHASES                              │
└─────────────────────────────────────────────────────────────────────────┘

PHASE 1: Archive Snapshot (Backup)
┌─────────────────────────────────────────┐
│ work/archive/2026-02-14-pre-cleanup/    │
│   ├── logs/                             │
│   ├── coordination/                     │
│   ├── curator/                          │
│   └── [... all modified dirs ...]      │
└─────────────────────────────────────────┘
            ↓
            ↓ (Backup complete)
            ↓
PHASE 2: Merge Logs
┌──────────────────┐     ┌──────────────────────────┐
│   work/logs/     │────→│ work/reports/logs/       │
│   (51 files)     │     │   ├── architect/         │
│                  │     │   ├── python-pedro/      │
│                  │     │   └── [... merged ...]   │
└──────────────────┘     └──────────────────────────┘
            ↓
            ↓ (Logs consolidated)
            ↓
PHASE 3: Merge Coordination
┌─────────────────────────┐     ┌──────────────────────────────┐
│  work/coordination/     │────→│ work/collaboration/          │
│   ├── AGENT_STATUS.md   │     │   ├── AGENT_STATUS.md ←─┐   │
│   ├── WORKFLOW_LOG.md   │     │   ├── WORKFLOW_LOG.md ←─┤   │
│   ├── HANDOFFS.md       │     │   └── HANDOFFS.md ←─────┤   │
│   └── [... files ...]   │     └──────────────────────────┼───┘
└─────────────────────────┘                                │
            │                   ┌──────────────────────────┘
            └──────────────────→│ work/reports/orchestration/
                                │   ├── *-orchestration-*.md
                                │   └── *-execution-*.md
                                └─────────────────────────────
            ↓
            ↓ (Coordination consolidated)
            ↓
PHASE 4: Move Agent Directories
┌──────────────────┐     ┌────────────────────────────────────┐
│ work/curator/    │────→│ work/collaboration/assigned/curator/│
│ work/architect/  │────→│ work/collaboration/assigned/architect/│
│ work/analyst/    │────→│ work/collaboration/assigned/analyst/│
│ work/LEX/        │────→│ work/collaboration/done/lexical/   │
│ work/telemetry/  │────→│ work/collaboration/done/telemetry/ │
└──────────────────┘     └────────────────────────────────────┘
            ↓
            ↓ (Agent work organized)
            ↓
PHASE 5: Consolidate Report Subdirs
┌──────────────────┐     ┌──────────────────────────┐
│ work/analysis/   │────→│ work/reports/analysis/   │
│ work/validation/ │────→│ work/reports/validation/ │
│ work/research/   │────→│ work/reports/research/   │
└──────────────────┘     └──────────────────────────┘
            ↓
            ↓ (Reports consolidated)
            ↓
PHASE 6: Handle Loose Files
┌────────────────────────────────────┐
│ work/20260212-*-bootstrap-*.md     │────→ reports/logs/bootstrap-bill/
│ work/boy_scout_sqlite_fix.md      │────→ reports/refactoring/
└────────────────────────────────────┘
            ↓
            ↓ (All files categorized)
            ↓
PHASE 7: Validation & Documentation
┌────────────────────────────────────┐
│ ✅ Verify file counts (1,099)     │
│ ✅ Check for broken references     │
│ ✅ Validate directory structure    │
│ ✅ Update README files             │
│ ✅ Git commit with summary         │
└────────────────────────────────────┘
            ↓
            ↓ (Cleanup complete)
            ↓
        ✅ DONE
```

---

## Impact Summary

### Directory Count Reduction
```
┌─────────────┬────────┬────────┬─────────┐
│  Metric     │ Before │ After  │ Change  │
├─────────────┼────────┼────────┼─────────┤
│ Directories │  199   │  150   │  -25%   │
│ Files       │ 1,099  │ 1,099  │   0%    │
│ Top-level   │   24   │   10   │  -58%   │
└─────────────┴────────┴────────┴─────────┘
```

### Canonical Locations Established
```
✅ work/collaboration/  - Task workflow (inbox/assigned/done/archive)
✅ work/reports/        - All agent outputs, logs, and metrics
✅ work/notes/          - Persistent project notes
✅ work/planning/       - Planning artifacts
✅ work/archive/        - Long-term retention
✅ work/templates/      - Reserved for templates
```

### Redundancies Eliminated
```
❌ Removed: 15 redundant/duplicate directories
❌ Removed: 3 overlapping log storage locations
❌ Removed: 10 misplaced agent-specific directories
```

---

## Validation Checkpoints

### Pre-Migration
- [ ] File count: `find work/ -type f | wc -l` = 1,099
- [ ] Directory count: `find work/ -type d | wc -l` = 199
- [ ] Top-level dirs: `ls -d work/*/ | wc -l` = 24

### Post-Migration
- [ ] File count: `find work/ -type f | wc -l` = 1,099 ✅ (no loss)
- [ ] Directory count: `find work/ -type d | wc -l` ≈ 150 ✅ (-25%)
- [ ] Top-level dirs: `ls -d work/*/ | wc -l` ≈ 10 ✅ (-58%)
- [ ] Broken refs: `grep -r "work/logs/" docs/ .github/` = 0 ✅
- [ ] Broken refs: `grep -r "work/coordination/" docs/ .github/` = 0 ✅

---

**Status:** ⏳ Awaiting Approval  
**Related Documents:**
- [Full Analysis Report](./2026-02-14-work-directory-cleanup.md)
- [Approval Checklist](./2026-02-14-cleanup-checklist.md)
