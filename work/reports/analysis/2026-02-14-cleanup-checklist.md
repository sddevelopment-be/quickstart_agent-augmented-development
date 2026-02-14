# Work Directory Cleanup - Approval Checklist

**Agent:** Curator Claire  
**Date:** 2026-02-14  
**Related Report:** [2026-02-14-work-directory-cleanup.md](./2026-02-14-work-directory-cleanup.md)

---

## Pre-Approval Review Checklist

### 1. Analysis Validation

- [ ] Review proposed directory consolidations
- [ ] Verify no active dependencies on directories to be removed
- [ ] Check migration impact on existing workflows
- [ ] Confirm canonical locations align with doctrine expectations

### 2. Risk Assessment

- [ ] Review backup/archive strategy
- [ ] Verify no data loss in proposed migrations
- [ ] Check for cross-references in documentation
- [ ] Assess rollback plan if needed

### 3. Stakeholder Questions

**Please provide input on:**

1. **Planning directory:** Should `work/planning/` be reviewed for duplication with `collaboration/assigned/planning/`?
   - [ ] Keep separate (planning is cross-agent)
   - [ ] Merge to collaboration/assigned/planning/
   - [ ] Other: _______________________

2. **Articles directory:** Where should `work/articles/` content go?
   - [ ] Move to `notes/` (persistent reference)
   - [ ] Move to `reports/research/` (research outputs)
   - [ ] Archive to `work/archive/2026-02/` (obsolete)
   - [ ] Other: _______________________

3. **Schemas directory:** How should `work/schemas/` be handled?
   - [ ] Keep as top-level (active development)
   - [ ] Move to `collaboration/done/schemas/` (completed work)
   - [ ] Other: _______________________

---

## Approval Decision

### Option A: Approve Full Migration
```
✅ APPROVED - Proceed with full migration as proposed
```

**Execute:**
1. Run Phase 1: Archive snapshot
2. Run Phases 2-6: Execute migrations
3. Run Phase 7: Validate and document
4. Commit changes with clear migration log

### Option B: Approve with Modifications
```
⚠️ APPROVED with changes - Modify plan then proceed
```

**Modifications requested:**
- [ ] Exclude directory: _______________________
- [ ] Additional consolidation: _______________________
- [ ] Change approach for: _______________________
- [ ] Other: _______________________

### Option C: Request Additional Analysis
```
❌ NOT APPROVED - Need more information
```

**Additional information needed:**
- [ ] Impact analysis on: _______________________
- [ ] Cross-reference check for: _______________________
- [ ] Alternative proposal for: _______________________
- [ ] Other: _______________________

---

## Post-Approval Execution Plan

### Phase 1: Archive Snapshot (5 min)
```bash
mkdir -p work/archive/2026-02-14-pre-cleanup
# Copy all directories being modified
tar czf work/archive/2026-02-14-pre-cleanup/backup.tar.gz \
  work/logs work/coordination work/analysis work/validation \
  work/research work/curator work/architect work/analyst \
  work/synthesizer work/LEX work/glossary-candidates \
  work/telemetry work/session-summaries work/status \
  work/prompts work/articles
```

### Phase 2-6: Execute Migrations (20-30 min)
- [ ] Merge logs → reports/logs/
- [ ] Merge coordination → collaboration/ + reports/orchestration/
- [ ] Move agent directories → collaboration/
- [ ] Consolidate report subdirectories
- [ ] Handle loose files
- [ ] Review and categorize remaining

### Phase 7: Validation (10 min)
- [ ] Verify file counts (no loss)
- [ ] Check for broken references
- [ ] Validate directory structure
- [ ] Update documentation
- [ ] Git commit with summary

---

## Validation Commands

**Pre-migration file count:**
```bash
find work/ -type f | wc -l  # Should be: 1,099
```

**Post-migration file count:**
```bash
find work/ -type f | wc -l  # Should be: 1,099 (no loss)
```

**Check for broken references:**
```bash
grep -r "work/logs/" docs/ .github/ README.md
grep -r "work/coordination/" docs/ .github/ README.md
```

**Directory count reduction:**
```bash
find work/ -type d | wc -l  # Should be: ~150 (from 199)
```

---

## Rollback Plan (if needed)

**If issues detected post-migration:**

```bash
# Extract backup
tar xzf work/archive/2026-02-14-pre-cleanup/backup.tar.gz -C work/

# Restore Git state
git checkout HEAD -- work/

# Or revert commit
git revert <commit-hash>
```

---

## Success Metrics

**Structural:**
- ✅ All logs in `work/reports/logs/<agent-slug>/`
- ✅ No duplicate directories (coordination/, analysis/, etc.)
- ✅ Agent work in `work/collaboration/assigned/` or `done/`
- ✅ Consistent naming conventions
- ✅ No loose files in work/ root (except README.md, .gitkeep)

**Functional:**
- ✅ No broken cross-references
- ✅ All files accounted for
- ✅ Git history clean
- ✅ README files updated

**Compliance:**
- ✅ Aligned with doctrine expectations
- ✅ Follows task workflow structure
- ✅ Canonical locations clearly defined

---

## Approval Signature

**Approved by:** _______________________  
**Date:** _______________________  
**Option:** [ ] A [ ] B [ ] C  
**Notes:** _______________________

---

**Status:** ⏳ Awaiting Approval  
**Next Action:** Proceed upon signed approval
