# Repository Roadmap

**Version:** 2.0.0
**Last Updated:** 2026-02-12
**Owner:** Planning Petra
**Status:** Active

---

## Strategic Vision

This repository serves as a quickstart template and reference implementation for agent-augmented development workflows. Our roadmap focuses on three strategic pillars:

1. **Orchestration Intelligence** - Enable smarter task routing and workload distribution
2. **Framework Maturity** - Strengthen governance, validation, and portability
3. **Adoption Enablement** - Reduce friction for new teams adopting the framework

---

## Active Initiatives

### 1. Agent Specialization Hierarchy (NEW)

**Epic:** Orchestration Intelligence
**Priority:** HIGH
**Status:** Approved - Implementation Pending
**Total Effort:** 54-68 hours
**Owner:** Architect Alphonso

**Problem:** Orchestration system favors generic agents over context-appropriate specialists, leading to suboptimal routing and specialist underutilization.

**Solution:** Formalize parent-child agent relationships with context-based routing, workload awareness, and automatic fallback chains.

**Strategic Value:**
- Improved task routing accuracy (90%+ specialist selection when available)
- Better workload distribution across agent pool
- Support for repository-specific specialists via `.doctrine-config`
- Reduced manual handoff overhead

**Architecture References:**
- DDR-011: Agent Specialization Hierarchy
- Architecture Design: `docs/architecture/design/agent-specialization-hierarchy.md`
- Specification: `specifications/initiatives/agent-specialization-hierarchy/agent-specialization-hierarchy.md`

**Phase Breakdown:**

#### Phase 1: Core Decision & Glossary (6-8h) - PARTIALLY COMPLETE
- Status: DDR-011 completed ✅, GLOSSARY.md updates pending
- Deliverables:
  - ✅ DDR-011 (Agent Specialization Hierarchy decision)
  - Update `doctrine/GLOSSARY.md` with hierarchy terminology
  - Document domain model in architecture design ✅
- Dependencies: None
- Risk: Low - foundational documentation phase

#### Phase 2: SELECT_APPROPRIATE_AGENT Tactic (10-12h)
- Status: Not Started
- Deliverables:
  - Create `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md`
  - Python reference implementation of routing algorithm
  - Logging and telemetry integration
- Dependencies: Phase 1 complete
- Assigned: Architect Alphonso (tactic doc), Python Pedro (implementation)
- Risk: Medium - complex routing logic requires comprehensive testing

#### Phase 3: Agent Profile Schema Enhancement (8-10h)
- Status: Not Started
- Deliverables:
  - Update `doctrine/templates/agent-profile-template.md`
  - Update Python Pedro, Java Jenny, Backend Benny profiles with hierarchy metadata
  - Create `tools/validators/validate-agent-hierarchy.py`
- Dependencies: Phase 1 complete
- Assigned: Curator Claire (template), Python Pedro (profiles)
- Risk: Low - additive schema changes, backward compatible

#### Phase 4: Manager Mike Enhancement (10-12h)
- Status: Not Started
- Deliverables:
  - Update `doctrine/agents/manager.agent.md` profile
  - Implement handoff protocol enhancement (specialist override)
  - Implement reassignment pass script
- Dependencies: Phase 2, Phase 3 complete
- Assigned: Python Pedro (handoff logic), Backend Benny (reassignment script)
- Risk: Medium - handoff override must preserve task context integrity

#### Phase 5: Validation & Testing (12-16h)
- Status: Not Started
- Deliverables:
  - Unit tests for routing algorithm (context extraction, scoring, penalties)
  - Integration tests (end-to-end routing, handoff override, reassignment)
  - Test scenarios (specialist selection, overload fallback, local specialist discovery)
- Dependencies: Phase 2, 3, 4 complete
- Assigned: Python Pedro (unit tests), Backend Benny (integration tests)
- Risk: High - inadequate testing risks production routing failures

#### Phase 6: Documentation & Migration (8-10h)
- Status: Not Started
- Deliverables:
  - Migration guide for existing repositories
  - Repository adopter guide (how to add custom specialists)
  - Decision tree: "When to use which agent"
- Dependencies: Phase 5 complete
- Assigned: Scribe Sally (guides), Curator Claire (migration doc)
- Risk: Low - documentation phase, no code changes

**Success Criteria:**
- All 6 phases complete
- Routing accuracy >90% for tasks with available specialists
- Specialist workload never exceeds capacity by >1 task (race condition tolerance)
- Handoff override rate >70% for eligible handoffs
- Zero circular dependency errors in validation
- All agents (new and existing) load without errors

**Timeline Estimate:**
- Sequential execution with validation gates: 8-10 weeks
- Aggressive parallel execution: 6-7 weeks
- Recommended: Sequential with gates (higher quality, lower risk)

**Key Milestones:**
- M1 (End Week 2): Phase 1 complete - Glossary and DDR approved
- M2 (End Week 4): Phase 2 complete - Routing algorithm functional
- M3 (End Week 6): Phase 3 complete - Agent profiles updated
- M4 (End Week 8): Phase 4 complete - Manager Mike integration
- M5 (End Week 10): Phase 5 complete - All tests passing
- M6 (End Week 10): Phase 6 complete - Documentation published

---

### 2. Dashboard Enhancements

**Epic:** Orchestration Intelligence
**Priority:** CRITICAL
**Status:** M4 Batch 4.3 In Progress
**Owner:** Frontend Freddy, Python Pedro

**Current Focus:**
- Initiative-level tracking
- Portfolio view with progress metrics
- Real-time task status updates

**Completion Target:** February 2026 (Week 3)

---

### 3. Framework Distribution

**Epic:** Framework Maturity
**Priority:** HIGH
**Status:** Partially Complete
**Owner:** DevOps Danny, Backend Benny

**Recent Completions:**
- ✅ Multi-format export (Claude Code, GitHub Copilot, OpenCode)
- ✅ Agent generator simplification
- ✅ Rules file generation
- ✅ CLAUDE.md generation

**Pending Work:**
- Validation scripts
- Distribution packaging
- Adopter onboarding documentation

---

### 4. Quickstart & Onboarding

**Epic:** Adoption Enablement
**Priority:** HIGH
**Status:** Specifications Complete
**Owner:** Bootstrap Bill, Python Pedro

**Focus:**
- `init-repository.sh` core script (automated mode)
- Interactive wizard (Python TUI)
- Agent-assisted initialization

**Start Target:** March 2026 (after Agent Specialization Hierarchy Phase 1)

---

### 5. Terminology Alignment & Refactoring

**Epic:** Framework Maturity
**Priority:** HIGH
**Status:** Specification Ready for Review
**Owner:** Backend Benny, Code Reviewer Cindy

**Total Effort:** 120 hours (phased)

**Phase 1 Focus (Next Batch):**
- Directive updates for naming enforcement (4h)
- Top 5 generic class refactors (31h)
- Terminology standardization (6h)

**Future Phases:**
- Task context boundary implementation (40h)
- CQRS research (8h)
- Remaining generic class refactors (52h)

**Start Target:** Parallel with Agent Specialization Hierarchy

---

### 6. Conceptual Alignment Initiative

**Epic:** Framework Maturity
**Priority:** MEDIUM
**Status:** Specification Proposed
**Owner:** Analyst Annie

**Focus:**
- Expand `doctrine/GLOSSARY.md` with 40+ DDD terms
- Contextive IDE integration
- Visual concept mapping
- Terminology validation automation

**Start Target:** Q2 2026

---

## Phasing Strategy

### Current Quarter (2026 Q1)

**February (Weeks 2-4):**
- Week 2: Agent Specialization Hierarchy - Phase 1 complete
- Week 3: Dashboard enhancements M4 4.3 complete
- Week 4: Agent Specialization Hierarchy - Phase 2 complete

**March:**
- Week 1-2: Agent Specialization Hierarchy - Phases 3-4
- Week 3-4: Agent Specialization Hierarchy - Phases 5-6 + Quickstart Batch 1

### Next Quarter (2026 Q2)

**April:**
- Quickstart & Onboarding (Batches 2-4)
- Terminology Alignment Phase 1 (parallel)

**May-June:**
- Conceptual Alignment Initiative
- Terminology Alignment Phase 2-3

---

## Dependencies & Critical Path

### Sequential Dependencies

**CRITICAL PATH:**
```
Agent Specialization Hierarchy Phase 1
  → Phase 2 (routing algorithm)
  → Phase 3 (profiles)
  → Phase 4 (Manager Mike integration)
  → Phase 5 (testing)
  → Phase 6 (documentation)
```

**PARALLEL TRACKS:**
- Dashboard Enhancements (independent, completing soon)
- Terminology Alignment Phase 1 (can parallel with ASH Phases 2-6)
- Framework Distribution packaging (independent)

### Blocking Relationships

1. **Agent Specialization Hierarchy Phase 2 blocks Phase 4**
   - Routing algorithm must exist before Manager Mike integration
   - Mitigation: Strong specification and test coverage in Phase 2

2. **Dashboard M4 4.3 blocks team capacity**
   - Frontend Freddy, Python Pedro at capacity until completion
   - Mitigation: Start ASH Phase 1 (documentation-heavy) immediately

3. **ASH Phase 5 blocks production deployment**
   - No Manager Mike enhancement without comprehensive testing
   - Mitigation: Dedicated testing phase, no shortcuts

---

## Capacity Planning

### Agent Utilization (Current)

| Agent | Current Load | Capacity | Utilization | Availability for ASH |
|-------|-------------|----------|-------------|---------------------|
| Architect Alphonso | 4 tasks | 5 | 80% | Limited (20%) |
| Python Pedro | 6 tasks | 5 | 120% | ⚠️ Overloaded |
| Backend Benny | 6 tasks | 8 | 75% | Moderate (25%) |
| Frontend Freddy | 2 tasks | 5 | 40% | High (60%) after dashboard |
| DevOps Danny | 4 tasks | 5 | 80% | Limited (20%) |
| Curator Claire | 1 task | 5 | 20% | High (80%) |
| Scribe Sally | 2 tasks | 5 | 40% | High (60%) |
| Analyst Annie | 0 tasks | 5 | 0% | Full (100%) |

### Capacity Constraints

**CRITICAL:** Python Pedro overloaded (120% utilization)
- Risk: Phase 2 and Phase 3 both assign work to Pedro
- Mitigation: Reassign Phase 3 profile updates to Backend Benny or defer to Phase 5

**OPPORTUNITY:** Analyst Annie, Curator Claire, Scribe Sally underutilized
- Phase 1: Leverage Curator Claire for GLOSSARY updates
- Phase 6: Leverage Scribe Sally + Curator Claire for documentation

### Recommended Sequencing

**Batch 1 (Phase 1 + Phase 2 start) - 2 weeks:**
- Curator Claire: GLOSSARY.md updates (Phase 1)
- Architect Alphonso: SELECT_APPROPRIATE_AGENT tactic spec (Phase 2 prep)
- Total: ~10 hours

**Batch 2 (Phase 2 complete) - 2 weeks:**
- Architect Alphonso: Tactic document finalization (4h)
- Python Pedro: Routing algorithm implementation (6h) - AFTER dashboard complete
- Python Pedro: Unit tests (2h)
- Total: ~12 hours

**Batch 3 (Phase 3 + Phase 4 start) - 2 weeks:**
- Backend Benny: Agent profile updates (6h) - REASSIGNED from Pedro
- Curator Claire: Template updates (2h)
- Python Pedro: Validation script (2h)
- Total: ~10 hours

**Batch 4 (Phase 4 complete) - 2 weeks:**
- Python Pedro: Handoff protocol enhancement (5h)
- Backend Benny: Reassignment pass script (5h)
- Manager Mike profile update (2h)
- Total: ~12 hours

**Batch 5 (Phase 5 complete) - 2-3 weeks:**
- Python Pedro: Unit tests (6h)
- Backend Benny: Integration tests (6h)
- Analyst Annie: Test scenario validation (4h)
- Total: ~16 hours

**Batch 6 (Phase 6 complete) - 1 week:**
- Scribe Sally: Migration guide, adopter guide (5h)
- Curator Claire: Decision tree, documentation updates (3h)
- Total: ~8 hours

---

## Risk Management

### High Risks

**RISK-001: Python Pedro Overload**
- Impact: Phase 2, 3, 4, 5 all depend on Pedro
- Probability: HIGH (already at 120% capacity)
- Mitigation:
  - Reassign Phase 3 profile updates to Backend Benny
  - Defer Phase 2 start until dashboard complete (week 3)
  - Spread Phase 5 testing across Pedro + Benny + Annie
- Owner: Planning Petra

**RISK-002: Routing Algorithm Complexity**
- Impact: Phase 2 implementation could take 2x estimated effort
- Probability: MEDIUM (complex scoring, workload tracking, tie resolution)
- Mitigation:
  - Strong technical design in Phase 2 tactic document
  - Architect Alphonso review before implementation
  - Incremental implementation (scoring → workload → complexity → ties)
- Owner: Architect Alphonso

**RISK-003: Testing Coverage Inadequate**
- Impact: Production routing failures, task assignment errors
- Probability: MEDIUM (complex state machine, edge cases)
- Mitigation:
  - Dedicated Phase 5 with 12-16 hour allocation
  - Comprehensive test scenarios in specification
  - Integration tests covering end-to-end workflows
- Owner: Python Pedro, Backend Benny

### Medium Risks

**RISK-004: Manager Mike Integration Breaks Existing Workflows**
- Impact: Current task assignment stops working
- Probability: LOW-MEDIUM (backward compatibility design goal)
- Mitigation:
  - Extensive integration testing in Phase 5
  - Gradual rollout (opt-in flag initially)
  - Rollback plan documented
- Owner: Backend Benny

**RISK-005: Terminology Alignment Conflicts**
- Impact: Parallel work on terminology could conflict with ASH glossary updates
- Probability: LOW (different focus areas)
- Mitigation:
  - Coordinate Phase 1 GLOSSARY updates with Terminology spec
  - Single source of truth: `doctrine/GLOSSARY.md`
- Owner: Curator Claire

---

## Success Metrics

### Initiative-Level Metrics

**Agent Specialization Hierarchy:**
- Routing accuracy: >90% specialist selection when available
- Specialist utilization: 60-90% (balanced, not overloaded)
- Handoff override rate: >70% for eligible handoffs
- Zero validation errors (circular dependencies, missing parents)

**Quickstart & Onboarding:**
- Setup time: <15 minutes (from hours)
- User satisfaction: >80%
- Adoption: 20+ repos in first 3 months

**Terminology Alignment:**
- Generic class names: 19 → 0 (100% elimination)
- Glossary coverage: 100+ terms (from ~60)
- Validation passing: 100% of doctrine files

---

## Change Log

| Date | Author | Change | Reason |
|------|--------|--------|--------|
| 2026-02-12 | Planning Petra | Added Agent Specialization Hierarchy initiative | DDR-011 approved, specification complete |
| 2026-02-12 | Planning Petra | Initial roadmap document created | Consolidate strategic planning view |

---

## Approval

**Planning Petra:** Submitted for review - 2026-02-12
**Architect Alphonso:** Pending
**Manager Mike:** Pending
**Human-in-Charge:** Pending

---

**Version:** 2.0.0
**Status:** Active
**Next Review:** 2026-03-01 or after Agent Specialization Hierarchy Phase 2 completion
