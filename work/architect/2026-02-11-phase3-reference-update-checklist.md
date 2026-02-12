# Phase 3 Reference Update Checklist

**Task:** Update doctrine files to reference new DDRs instead of repository ADRs  
**Estimated Time:** 3.5-4.5 hours  
**Status:** Ready to execute

---

## Reference Update Mapping

| Old Reference | New Reference | Description |
|--------------|---------------|-------------|
| `../../docs/architecture/adrs/ADR-001-*` | `./decisions/DDR-010-*` | Modular directive system |
| `../../docs/architecture/adrs/ADR-003-*` | `./decisions/DDR-005-*` | Task lifecycle |
| `../../docs/architecture/adrs/ADR-004-*` | `./decisions/DDR-006-*` | Work directory structure |
| `../../docs/architecture/adrs/ADR-005-*` | `./decisions/DDR-007-*` | Coordinator pattern |
| `../../docs/architecture/adrs/ADR-008-*` | `./decisions/DDR-004-*` | File-based coordination |
| `../../docs/architecture/adrs/ADR-013-*` | `./decisions/DDR-008-*` | Framework distribution |
| `../../docs/architecture/adrs/ADR-017-*` | `./decisions/DDR-009-*` | Traceable decisions |

**Note:** File name mapping (ADR-008 → DDR-004, etc.) is intentional due to DDR numbering sequence.

---

## Files Requiring Updates (17 total)

### Agent Profiles (9 files)

**High Priority (Multiple ADR references):**

- [ ] `doctrine/agents/architect.md`
  - Expected references: ADR-001, ADR-017
  - Update to: DDR-010, DDR-009

- [ ] `doctrine/agents/coordinator.md`
  - Expected references: ADR-003, ADR-004, ADR-005, ADR-008
  - Update to: DDR-005, DDR-006, DDR-007, DDR-004

- [ ] `doctrine/agents/curator.md`
  - Expected references: ADR-001
  - Update to: DDR-010

**Medium Priority (Single ADR references):**

- [ ] `doctrine/agents/developer.md`
  - Expected references: ADR-001
  - Update to: DDR-010

- [ ] `doctrine/agents/lexical.md`
  - Expected references: ADR-001
  - Update to: DDR-010

- [ ] `doctrine/agents/planning.md`
  - Expected references: ADR-017
  - Update to: DDR-009

- [ ] `doctrine/agents/structural.md`
  - Expected references: ADR-001
  - Update to: DDR-010

- [ ] `doctrine/agents/synthesizer.md`
  - Expected references: ADR-001
  - Update to: DDR-010

- [ ] `doctrine/agents/writer-editor.md`
  - Expected references: ADR-001
  - Update to: DDR-010

---

### Core Documents (1 file)

- [ ] `doctrine/core_specification.md`
  - Expected references: ADR-001, ADR-003, ADR-005
  - Update to: DDR-010, DDR-005, DDR-007

---

### Directives (3 files)

- [ ] `doctrine/directives/002_context_notes.md`
  - Expected references: ADR-001
  - Update to: DDR-010

- [ ] `doctrine/directives/004_documentation_context_files.md`
  - Expected references: ADR-001
  - Update to: DDR-010

- [ ] `doctrine/directives/018_documentation_level_framework.md`
  - Expected references: ADR-017
  - Update to: DDR-009

---

### Guidelines (3 files)

- [ ] `doctrine/guidelines/bootstrap.md`
  - Expected references: ADR-001, ADR-003
  - Update to: DDR-010, DDR-005

- [ ] `doctrine/guidelines/general_guidelines.md`
  - Expected references: ADR-001
  - Update to: DDR-010

- [ ] `doctrine/guidelines/operational_guidelines.md`
  - Expected references: ADR-001, ADR-003, ADR-004, ADR-005
  - Update to: DDR-010, DDR-005, DDR-006, DDR-007

---

### Tactical Documents (1 file)

- [ ] `doctrine/tactical/file-based-orchestration.md`
  - Expected references: ADR-004, ADR-005, ADR-008
  - Update to: DDR-006, DDR-007, DDR-004

---

## ADR Deprecation Notices (7 files)

Add deprecation notice to each elevated ADR:

```markdown
> **⚠️ ELEVATED TO DOCTRINE**
> This ADR has been elevated to framework-level guidance.
> See: [DDR-XXX](../../../doctrine/decisions/DDR-XXX-title.md)
> 
> This repository-specific implementation reference is maintained for historical context.
```

### Files and Notices:

- [ ] `docs/architecture/adrs/ADR-001-modular-agent-directive-system.md`
  ```markdown
  > **⚠️ ELEVATED TO DOCTRINE**
  > This ADR has been elevated to framework-level guidance.
  > See: [DDR-010: Modular Agent Directive System Architecture](../../../doctrine/decisions/DDR-010-modular-agent-directive-system-architecture.md)
  > 
  > This repository-specific implementation reference is maintained for historical context.
  ```

- [ ] `docs/architecture/adrs/ADR-003-task-lifecycle-state-management.md`
  ```markdown
  > **⚠️ ELEVATED TO DOCTRINE**
  > This ADR has been elevated to framework-level guidance.
  > See: [DDR-005: Task Lifecycle and State Management Protocol](../../../doctrine/decisions/DDR-005-task-lifecycle-state-management-protocol.md)
  > 
  > This repository-specific implementation reference is maintained for historical context.
  ```

- [ ] `docs/architecture/adrs/ADR-004-work-directory-structure.md`
  ```markdown
  > **⚠️ ELEVATED TO DOCTRINE**
  > This ADR has been elevated to framework-level guidance.
  > See: [DDR-006: Work Directory Structure and Naming Conventions](../../../doctrine/decisions/DDR-006-work-directory-structure-naming-conventions.md)
  > 
  > This repository-specific implementation reference is maintained for historical context.
  ```

- [ ] `docs/architecture/adrs/ADR-005-coordinator-agent-pattern.md`
  ```markdown
  > **⚠️ ELEVATED TO DOCTRINE**
  > This ADR has been elevated to framework-level guidance.
  > See: [DDR-007: Coordinator Agent Orchestration Pattern](../../../doctrine/decisions/DDR-007-coordinator-agent-orchestration-pattern.md)
  > 
  > This repository-specific implementation reference is maintained for historical context.
  ```

- [ ] `docs/architecture/adrs/ADR-008-file-based-async-coordination.md`
  ```markdown
  > **⚠️ ELEVATED TO DOCTRINE**
  > This ADR has been elevated to framework-level guidance.
  > See: [DDR-004: File-Based Asynchronous Coordination Protocol](../../../doctrine/decisions/DDR-004-file-based-asynchronous-coordination-protocol.md)
  > 
  > This repository-specific implementation reference is maintained for historical context.
  ```

- [ ] `docs/architecture/adrs/ADR-013-zip-distribution.md`
  ```markdown
  > **⚠️ ELEVATED TO DOCTRINE**
  > This ADR has been elevated to framework-level guidance.
  > See: [DDR-008: Framework Distribution and Upgrade Mechanisms](../../../doctrine/decisions/DDR-008-framework-distribution-upgrade-mechanisms.md)
  > 
  > This repository-specific implementation reference is maintained for historical context.
  ```

- [ ] `docs/architecture/adrs/ADR-017-traceable-decision-integration.md`
  ```markdown
  > **⚠️ ELEVATED TO DOCTRINE**
  > This ADR has been elevated to framework-level guidance.
  > See: [DDR-009: Traceable Decision Patterns and Agent Integration](../../../doctrine/decisions/DDR-009-traceable-decision-patterns-agent-integration.md)
  > 
  > This repository-specific implementation reference is maintained for historical context.
  ```

---

## Validation Checklist

After completing updates:

- [ ] No broken links in doctrine/ files
- [ ] All DDR references resolve correctly
- [ ] All ADR deprecation notices added
- [ ] Git commit with clear message
- [ ] Framework Guardian validation passes
- [ ] Spot-check: Load 2-3 agent profiles to verify references work

---

## Execution Strategy

### Recommended Approach

**Phase 3a: Doctrine Reference Updates (2-3 hours)**

1. Use find/replace with caution:
   ```bash
   # Example (verify before executing):
   find doctrine/ -name "*.md" -exec sed -i \
     's|../../docs/architecture/adrs/ADR-001-modular-agent-directive-system.md|./decisions/DDR-010-modular-agent-directive-system-architecture.md|g' {} \;
   ```

2. Manually verify high-priority files (coordinator, architect, core_specification)

3. Test loading agent profiles to ensure references resolve

**Phase 3b: ADR Deprecation Notices (1 hour)**

1. Add notice at top of each ADR (after title, before Context)
2. Use exact notice format from this checklist
3. Verify links resolve to new DDRs

**Phase 3c: Final Validation (0.5 hours)**

1. Run markdown link checker
2. Grep for remaining ADR references in doctrine/
3. Spot-check 5-6 doctrine files manually
4. Git commit with descriptive message

---

## Success Criteria

- ✅ 0 doctrine files reference repository ADRs
- ✅ All doctrine files reference appropriate DDRs
- ✅ All 7 elevated ADRs have deprecation notices
- ✅ No broken links in doctrine/
- ✅ Framework Guardian validation passes
- ✅ Git history shows clear phase progression

---

## Notes

**Path Differences:**
- Old: `../../docs/architecture/adrs/ADR-XXX-*.md` (relative from doctrine/)
- New: `./decisions/DDR-XXX-*.md` (relative from doctrine/)
- Deprecation: `../../../doctrine/decisions/DDR-XXX-*.md` (relative from ADR)

**Number Mapping (be careful!):**
- ADR-001 → DDR-010
- ADR-003 → DDR-005
- ADR-004 → DDR-006
- ADR-005 → DDR-007
- ADR-008 → DDR-004 ⚠️ (crosses sequence!)
- ADR-013 → DDR-008
- ADR-017 → DDR-009

**Context Preservation:**
- ADRs remain in repository for historical reference
- Deprecation notices link both directions
- Repository-specific implementation details preserved

---

**Prepared by:** Architect Alphonso  
**Date:** 2026-02-11  
**For Phase:** 3 (Reference Updates)  
**Parent Task:** Doctrine Violation Remediation
