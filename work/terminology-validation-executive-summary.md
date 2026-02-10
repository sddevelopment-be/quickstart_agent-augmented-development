# Terminology Validation - Executive Summary

**Reviewer:** Code-reviewer Cindy  
**Date:** 2026-02-10  
**Full Report:** work/terminology-validation-report.md

---

## TL;DR

⚠️ **PARTIAL ALIGNMENT (25%)** - Codebase has strong domain concepts but most are missing from glossary.

**Key Stats:**
- 163 files analyzed across src/, tools/, tests/
- 11/44 glossary terms found in code (25% usage)
- 21 domain concepts found in code but missing from glossary
- 19 generic anti-pattern classes identified (Manager/Handler/Processor)

---

## Critical Findings

### ✅ Strengths
1. **Core orchestration terms well-established:** Agent (87 files), Task, Orchestrator
2. **Excellent type safety:** TaskStatus, FeatureStatus enums with state machines
3. **Rich dashboard domain:** Specification, Initiative, Feature concepts (not in glossary)

### ❌ Critical Gaps
1. **75% of glossary terms unused** - DDD glossary is aspirational, not operational
2. **Entire domains missing from glossary** - Portfolio, Task Status, Configuration
3. **Generic naming prevalent** - 19 classes with Manager/Handler/Processor suffixes
4. **Terminology conflicts** - "Status" vs. "State", "Load" vs. "read_task", "Persist" vs. "write_task"

---

## Priority Recommendations

### Immediate (This Sprint - 10 hours)

1. **Create Task Domain Glossary** - Add TaskStatus, FeatureStatus, TaskPriority, TaskMode, AgentIdentity
2. **Create Portfolio Domain Glossary** - Add Specification, Initiative, Feature, Portfolio View
3. **Fix 2-3 Generic Names** - Rename TemplateManager → TemplateRenderer, TaskAssignmentHandler → TaskAssignmentService

### Short-Term (Next Sprint - 14 hours)

4. **Resolve TaskDescriptor Decision** - Either implement TypedDict or remove from glossary
5. **Align State/Status Terminology** - Update glossary to match code ("Status" not "State")
6. **Add Infrastructure Terms** - Configuration, Template, Telemetry, Dashboard
7. **Document DDD Applicability** - Mark strategic terms as "conceptual"

### Long-Term (Future Sprints - 40+ hours)

8. **Bounded Context Documentation** - Create context map, document boundaries
9. **Glossary Enforcement Automation** - PR checks, IDE integration
10. **Quarterly Health Checks** - Staleness audit, coverage assessment

---

## Issues by Severity

### Advisory (80% of issues) ℹ️
- Inconsistent naming (Task File, Work Directory)
- Missing domain documentation (dashboard, configuration)
- Generic technical terms where domain language clearer

### Acknowledgment Required (18%) ⚠️
- Generic anti-pattern naming (Manager, Handler in domain classes)
- TaskDescriptor type vs. Dict[str, Any] trade-off
- Status vs. State terminology mismatch

### Hard Failure (2%) ❌
- None identified - codebase is functional

---

## Proposed Glossary Additions

### High Priority (Create New Contexts)

**Task Domain Context:**
- TaskStatus (enum)
- FeatureStatus (enum)
- TaskPriority (enum)
- TaskMode (enum)
- AgentIdentity (type)

**Portfolio Domain Context:**
- Specification
- Initiative
- Feature
- Portfolio View

### Medium Priority (Extend Existing)

**Software Design Context:**
- Configuration
- Template
- Telemetry
- Dashboard

---

## Module-Specific Assessment

| Module | Alignment | Dominant Terms | Action |
|--------|-----------|----------------|--------|
| `src/framework/orchestration/` | 30% | Agent, Task, Orchestrator | **PILOT MODULE** - Best for glossary enforcement |
| `src/llm_service/dashboard/` | 15% | Specification, Initiative, Feature | Create Portfolio Domain glossary |
| `src/common/` | 40% | TaskStatus, FeatureStatus, AgentIdentity | Add all enums to glossary |
| `src/llm_service/config/` | 10% | Configuration, Schema, Template | Add infrastructure terms |
| `tools/scripts/` | 15% | Task, Agent, Script | Low priority - operational code |
| `tests/` | 25% | Test, Given/When/Then | BDD-style, acceptable |

---

## Strategic Approach

**Incremental Alignment with Pilot Module**

1. **Phase 1: Orchestration Pilot** (1 sprint)
   - Add missing terms (TaskStatus, etc.)
   - Resolve TaskDescriptor decision
   - Standardize directory naming
   - Implement advisory-level enforcement

2. **Phase 2: Dashboard Domain** (1 sprint)
   - Create Portfolio Domain glossary
   - Document bounded context
   - Refactor generic names

3. **Phase 3: DDD Cleanup** (1 sprint)
   - Mark strategic terms as "conceptual"
   - Document WHERE DDD applies
   - Remove aspirational patterns

4. **Phase 4: Automation** (2 sprints)
   - PR-level glossary validation
   - IDE integration (Contextive)
   - Quarterly audit process

---

## Success Metrics

### Coverage Targets

| Metric | Current | 3 Months | 6 Months |
|--------|---------|----------|----------|
| Glossary term usage | 25% | 45% | 70% |
| Domain concepts documented | 0/21 | 13/21 | 19/21 |
| Generic anti-patterns | 19 | 12 | 5 |

### Quality Targets

- **Staleness:** <10% outdated definitions
- **Conflicts:** 0 terminology conflicts (currently 3)
- **Suppression rate:** <10% PRs overriding checks
- **Contribution:** >50% team-initiated updates

---

## Next Steps

### This Week
- [ ] Review with Architect Alphonso and Curator Claire
- [ ] Approve Task Domain and Portfolio Domain glossaries
- [ ] Create ADR for TaskDescriptor decision

### Next Sprint
- [ ] Implement glossary additions (task-domain.yml, portfolio-domain.yml)
- [ ] Refactor 2-3 generic class names
- [ ] Add ADR ↔ Glossary traceability links

### Next Quarter
- [ ] Set up Contextive IDE integration
- [ ] Implement PR-level validation
- [ ] Conduct first quarterly health check

---

## Enforcement Philosophy

**Start Permissive, Increase Gradually**

1. **Phase 1:** Advisory-only (suggestions, no blocking)
2. **Phase 2:** Acknowledgment required (warning, explicit override)
3. **Phase 3:** Hard failure (rare, critical violations only)

**Goal:** Build adoption through value, not coercion.

---

## References

- **Full Report:** work/terminology-validation-report.md
- **Living Glossary Practice:** doctrine/approaches/living-glossary-practice.md
- **Existing Glossaries:** .contextive/contexts/*.yml
- **Related ADRs:** ADR-042, ADR-043, ADR-044, ADR-037, ADR-031

---

**Status:** ✅ Complete - Ready for review  
**Confidence:** High - Based on comprehensive code scan (163 files)  
**Next Owner:** Architect Alphonso + Curator Claire

---

*"The glossary we need is already in the code; we just need to write it down."*  
— Code-reviewer Cindy
