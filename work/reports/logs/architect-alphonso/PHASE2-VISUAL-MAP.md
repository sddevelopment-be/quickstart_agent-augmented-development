# Phase 2 Cleanup - Visual Map

## File Movements

```
📁 docs/
├── ❌ DELETED: SHELL_LINTING_QUICKSTART.md (merged)
│
├── 🔀 MOVED TO docs/architecture/assessments/
│   └── SHELL_LINTING_ISSUES.md → shell-linting-issues-assessment.md
│
├── 🔀 MOVED TO docs/architecture/design/
│   └── error-reporting-system.md
│
├── 🔀 MOVED TO docs/guides/
│   ├── IMPLEMENTATION_ERROR_REPORTING.md → error-reporting-implementation.md
│   ├── error-reporting-quick-reference.md
│   └── shell-linting-guide.md (consolidated from 2 files)
│
├── 🔀 MOVED TO docs/reports/exec_summaries/
│   └── ERROR_REPORTING_EXECUTIVE_SUMMARY.md → error-reporting-executive-summary.md
│
└── 🔀 MOVED TO docs/workflows/
    └── auto-remediation-workflow.md
```

## Template Structure (Recommended)

```
✅ KEEP: doctrine/templates/           [82 files - CANONICAL]
   ├── architecture/
   ├── automation/
   ├── documentation/      [Framework only]
   ├── prompts/
   └── ... (all framework templates)

✅ KEEP: .doctrine-config/templates/   [2 files - LOCAL OVERRIDES]
   ├── README.md
   └── pr-comment-templates.md

⚠️ REMOVE: docs/templates/             [77 files - DUPLICATE]
   └── (entire directory - awaiting approval)

✅ KEEP: src/llm_service/templates/    [5 files - APPLICATION CODE]
✅ KEEP: tests/unit/templates/         [Test fixtures]
✅ KEEP: work/templates/               [Empty workspace]
```

## Decision Matrix

| Template Type | Location | Action |
|---------------|----------|--------|
| **Framework Templates** | `doctrine/templates/` | ✅ Keep (canonical) |
| **Framework Templates** | `docs/templates/` | ❌ Remove (duplicate) |
| **Local Overrides** | `.doctrine-config/templates/` | ✅ Keep (correct) |
| **Application Code** | `src/*/templates/` | ✅ Keep (correct) |
| **Test Fixtures** | `tests/*/templates/` | ✅ Keep (correct) |

## Before & After

### Before Phase 2
```
docs/
├── ERROR_REPORTING_EXECUTIVE_SUMMARY.md       [Root level, unclear purpose]
├── IMPLEMENTATION_ERROR_REPORTING.md          [Root level, unclear purpose]
├── error-reporting-system.md                  [Root level, unclear purpose]
├── error-reporting-quick-reference.md         [Root level, unclear purpose]
├── SHELL_LINTING_ISSUES.md                    [Root level, unclear purpose]
├── SHELL_LINTING_QUICKSTART.md                [Duplicate content]
├── shell-linting-guide.md                     [Incomplete]
├── auto-remediation-workflow.md               [Root level]
└── templates/                                 [77 duplicate files]
```

### After Phase 2
```
docs/
├── architecture/
│   ├── assessments/
│   │   └── shell-linting-issues-assessment.md   [Clear categorization]
│   └── design/
│       └── error-reporting-system.md            [Clear categorization]
│
├── guides/
│   ├── error-reporting-implementation.md        [Clear purpose]
│   ├── error-reporting-quick-reference.md       [Clear purpose]
│   └── shell-linting-guide.md                   [Consolidated & complete]
│
├── reports/
│   └── exec_summaries/
│       └── error-reporting-executive-summary.md [Clear categorization]
│
├── workflows/
│   └── auto-remediation-workflow.md             [Clear categorization]
│
└── templates/                                   [RECOMMEND: Remove after ref updates]
```

## Impact Summary

### ✅ Completed
- 7 files moved to canonical locations
- 2 files merged into 1 comprehensive guide
- 2 directories created (exec_summaries, workflows)
- Git history preserved for all moves

### ⚠️ Pending Approval
- Remove `docs/templates/` (77 duplicate files)
- Update 5 specification file references
- Update REPO_MAP.md

### 📊 Metrics
- **Files affected:** 8 operations
- **Lines reorganized:** 453 lines
- **Consolidation savings:** ~2KB (shell linting)
- **Duplication identified:** 77 files in docs/templates/
- **Template divergence:** 40+ files differ between locations

## Questions Answered

| Question | Answer |
|----------|--------|
| Does `docs/templates/` make sense? | ❌ NO - Remove after reference updates |
| Where do framework templates go? | ✅ `doctrine/templates/` (canonical) |
| Where do local overrides go? | ✅ `.doctrine-config/templates/` |
| What about git subtree distribution? | ✅ Templates must be in `doctrine/` |
| Is template structure correct? | ✅ YES - Just need to remove duplication |

## Next Actions

1. ✅ **Commit Phase 2 moves** (ready now)
2. ⚠️ **Update specification references** (5 files)
3. ⚠️ **Remove docs/templates/** (after #2)
4. ⚠️ **Update REPO_MAP.md** (after #3)

---

**Legend:**
- ✅ = Approved/Correct
- ⚠️ = Requires Approval
- ❌ = Remove/Incorrect
- 🔀 = Moved
- 📁 = Directory
