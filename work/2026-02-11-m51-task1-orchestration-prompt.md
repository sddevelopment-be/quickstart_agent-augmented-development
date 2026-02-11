# Manager Mike Orchestration Prompt: M5.1 Task 1 Execution

**Date:** 2026-02-11  
**Requestor:** Human In Charge  
**Priority:** ⭐⭐⭐⭐⭐ CRITICAL  
**Batch:** M5.1 Task 1 - Domain Structure Creation (ADR-046)

---

## Instruction to Manager Mike

Bootstrap as **Manager Mike** and execute the following iteration:

### Mission
Launch M5.1 Task 1 execution using file-based orchestration (Directive 019). This batch addresses the **critical task polysemy finding** from conceptual alignment assessment and unblocks 49-58 hours of downstream M5.1 work.

### Context
- **Branch:** copilot/validate-conceptual-alignment
- **Authorization:** AUTH-M5.1-20260211 (Architect Alphonso GREEN LIGHT)
- **Strategic Value:** Establishes bounded contexts for language-first architecture
- **Critical Path:** Blocks ADR-045 (domain model) and SPEC-TERM-001 (terminology)
- **Parallel Work:** Python Pedro continuing M4.3 initiative tracking backend (6-8h)

### Task to Execute

**Primary Task:**
```
File: work/collaboration/assigned/python-pedro/2026-02-11T0900-adr046-task1-domain-structure.yaml
Agent: Python Pedro (Python Development Specialist)
Duration: 1-2 hours
Priority: CRITICAL
Goal: Create src/domain/ directory structure with bounded context modules
```

**Task Summary:**
- Create `src/domain/` with subdirectories: collaboration/, doctrine/, specifications/, common/
- Preserve existing `src/common/` during migration
- Document module boundaries and responsibilities
- Create __init__.py files with docstrings
- Success criteria: Clean structure, documentation updated

### Orchestration Instructions

Using **file-based orchestration approach** (Directive 019):

1. **Status Check** (5 min)
   - Review `work/coordination/AGENT_STATUS.md`
   - Confirm Python Pedro availability
   - Check for blockers or conflicts

2. **Task Delegation** (5 min)
   - Assign task file to Python Pedro
   - Notify agent via coordination channel
   - Set expected completion: 1-2 hours

3. **Monitoring** (during execution)
   - Track progress via work logs in `work/collaboration/assigned/python-pedro/`
   - Monitor for blockers or questions
   - Available for escalation (SLA: <2h critical)

4. **Verification** (post-completion)
   - Review Python Pedro work log
   - Verify success criteria met:
     - ✅ `src/domain/` structure created
     - ✅ Bounded context modules documented
     - ✅ Architecture docs updated
   - Move task file to `work/collaboration/done/python-pedro/`

5. **Handoff Preparation** (10 min)
   - Identify next task: ADR-046 Task 2 (file migration)
   - Update `work/coordination/AGENT_STATUS.md`
   - Update `work/coordination/WORKFLOW_LOG.md`
   - Report completion to Human In Charge

6. **Status Report** (10 min)
   - Create execution summary in `work/coordination/`
   - Update M5.1 progress metrics
   - Recommend next batch action

### Success Criteria

**Iteration Complete When:**
- ✅ Python Pedro completes task (1-2h)
- ✅ Work log created with metrics
- ✅ Task file moved to done/
- ✅ AGENT_STATUS.md updated
- ✅ Completion report delivered

**Quality Gates:**
- ✅ Domain structure follows ADR-046 specification
- ✅ Documentation complete
- ✅ No regressions (existing tests pass)
- ✅ Next task ready for handoff

### Notes

- **Parallel Safety:** Python Pedro working M4.3 backend (no conflict expected)
- **Checkpoint:** This is Phase 1 of 4-phase ADR-046 implementation
- **Next Up:** ADR-046 Task 2 (file migration, 2-3h) after this completes
- **Human Approval:** Not required for Task 1 (approved in kickoff)

---

## Expected Output

Manager Mike should:
1. Confirm orchestration mode active
2. Execute 6-phase iteration cycle
3. Delegate to Python Pedro
4. Monitor progress
5. Report completion with metrics
6. Recommend next action

---

**End of Orchestration Prompt**
