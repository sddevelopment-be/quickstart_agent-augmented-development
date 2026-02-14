# Next Batch: Current Execution Focus

**Last Updated**: 2026-02-13 (Control Plane Architecture Approved — M6.1 Batch Defined)
**Updated By**: Planning Petra (standing in for Jenny)
**Status**: M5.1 EFFECTIVELY COMPLETE — Next Batch is M6.1: Dashboard Query Architecture

---

## Executive Summary

**M5.1 Status:** Code complete. ADR-045 Task 5 (Dashboard Integration) is done. Formal milestone closure is pending Manager Mike sign-off and archiving of task files. No blocking work remains.

**Next Batch: M6.1 — Dashboard Query Architecture**

This batch combines two workstreams that both modify dashboard internals. Separating them would require touching the same files twice. Combining them into a single batch reduces integration risk and review overhead.

**Workstreams in M6.1:**
- M4.3: Dashboard Initiative Tracking (existing task, previously blocked by M5.1)
- Control Plane P1b: Query Service facade extraction (new, from ADR-047 CQRS Pattern)
- Control Plane P1a: JSONL event writer for telemetry (new, from ADR-047)

**Estimated Effort:** 5-7 days total
**Primary Agents:** Python Pedro (backend), Frontend agent (UI)

---

## M5.1 Closure: Status

**Overall Status:** EFFECTIVELY COMPLETE (code done, formal closure pending)

| Component | Status | Notes |
|---|---|---|
| ADR-046: Domain Module Refactoring | COMPLETE | 4/4 tasks, 942 tests passing |
| ADR-045 Tasks 1-4 | COMPLETE | All approved by Alphonso, Annie, Claire |
| ADR-045 Task 5: Dashboard Integration | CODE DONE | Pending formal milestone sign-off |
| M5.1 Milestone Closure | PENDING | Manager Mike approval required |

**Action Required (non-blocking for M6.1):** Manager Mike to formally close M5.1 milestone and archive task files. This is an administrative step; no code work is outstanding.

**Achievements from M5.1:**
- 195 tests passing (92% coverage)
- 0 production errors in validation
- Performance exceeds targets by 68x (7ms vs 500ms target)
- Production-ready domain models, parsers, and validators
- All reviews approved (Pedro, Alphonso, Annie, Claire)

---

## Current Batch: M6.1 — Dashboard Query Architecture

### Rationale for Combining M4.3 and Control Plane P1

M4.3 (Dashboard Initiative Tracking) and Control Plane P1b (Query Service extraction) both modify dashboard data access internals. Executing them sequentially would require two rounds of touching the same files, increasing merge risk and requiring reviewers to context-switch twice. Combining them into a single coordinated batch avoids this.

Control Plane P1a (JSONL event writer) is included because it is a prerequisite for P1b and is self-contained on the backend.

**Technical References:**
- Technical Design: `docs/architecture/design/local-agent-control-plane-architecture.md` (Approved)
- ADR-047: CQRS Pattern — `docs/architecture/adrs/ADR-047-cqrs-local-agent-control-plane.md` (Accepted)
- ADR-048: Run Container — `docs/architecture/adrs/ADR-048-run-container-concept.md` (Accepted)
- ADR-049: Async Execution Engine — `docs/architecture/adrs/ADR-049-async-execution-engine.md` (Accepted)
- Existing Task: `work/collaboration/assigned/python-pedro/2026-02-06T1150-dashboard-initiative-tracking.yaml`

---

### Workstream 1: Control Plane P1a — JSONL Event Writer

**Owner:** Python Pedro
**Effort:** 1-2 days
**Source:** ADR-047 (CQRS Pattern), Control Plane Architecture
**Status:** ✅ COMPLETE (2026-02-14)

**Deliverables:**
- JSONL append-only event writer for run telemetry
- Writer integrated at tool invocation boundaries
- Unit tests with >90% coverage
- Work log per Directive 014

**Acceptance Criteria:**
1. Events written in JSONL format with schema conforming to ADR-047
2. Writer is append-only (no mutation of existing records)
3. File rotation handled gracefully (no data loss on rotation boundary)
4. Tests cover write, rotation, and error paths

**Dependencies:** None (self-contained backend component)

---

### Workstream 2: Control Plane P1b — Query Service Facade Extraction

**Owner:** Python Pedro
**Effort:** 2-3 days
**Source:** ADR-047 (CQRS Pattern)
**Status:** Depends on P1a (JSONL writer must exist to have something to query)

**Deliverables:**
- Query Service facade separating read path from write path
- CQRS boundary enforced at the service layer (reads never touch write path)
- Dashboard data access refactored to route through Query Service
- Integration tests confirming read/write path separation

**Acceptance Criteria:**
1. All dashboard reads go through Query Service (no direct event log access from UI layer)
2. CQRS boundary is enforced by interface, not convention
3. Existing dashboard functionality is not regressed (all current tests pass)
4. Query Service is independently testable in isolation

**Dependencies:** P1a complete (JSONL writer is the read source for the Query Service)

---

### Workstream 3: M4.3 — Dashboard Initiative Tracking

**Owner:** Python Pedro (backend API), Frontend agent (UI)
**Effort:** Backend 1-2 days, Frontend 2-3 days (parallelisable after backend API is done)
**Source:** Existing task `2026-02-06T1150-dashboard-initiative-tracking`
**Status:** Unblocked (M5.1 code complete)

**Deliverables:**
- Initiative tracking backend API (Python Pedro)
- Frontend integration: initiative list and status display (Frontend agent)
- Status dashboard visualization (Frontend agent)

**Acceptance Criteria:**
1. Initiatives visible in dashboard with current status
2. API follows Query Service pattern (reads via facade from P1b)
3. Status visualization renders without errors on all supported viewport sizes
4. Performance: <100ms page load for initiative list

**Dependencies:**
- M5.1 formal closure (administrative only, not a code dependency)
- P1b Query Service facade (initiative tracking reads route through it)

---

## Sequencing Within M6.1

```
P1a (JSONL writer)        [Pedro, day 1-2]
     |
     v
P1b (Query Service)       [Pedro, day 2-4]
     |
     +---> M4.3 backend   [Pedro, day 3-5]
                |
                v
          M4.3 frontend   [Frontend agent, day 4-7]
```

P1a and the start of P1b can overlap. M4.3 backend work can begin once the Query Service interface is defined (implementation of P1b does not need to be complete, only the interface contract). Frontend work begins after the M4.3 backend API is available.

---

## Decision Checkpoints

| Checkpoint | Trigger | Reviewers |
|---|---|---|
| P1a schema review | JSONL schema drafted | Architect Alphonso |
| CQRS boundary review | P1b interface defined (before implementation) | Architect Alphonso |
| M4.3 API contract review | Backend API spec complete | Manager Mike |
| M6.1 batch completion | All workstreams done, tests green | Manager Mike, Alphonso |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| ADR-047 still Proposed (not Approved) | Medium | Medium | Proceed with P1a/P1b; architect review at CQRS boundary checkpoint gates further work |
| M4.3 frontend scope expands | Medium | Low | M4.3 frontend is scoped to existing design; escalate any scope additions |
| P1b touches same files as M4.3 backend | Low | Medium | Combined batch structure avoids this by design; Pedro to coordinate sequencing |

---

## Inbox Tasks Pending (Not in M6.1)

The following approved inbox tasks exist but are not scheduled in this batch. They should be addressed in M6.2 planning:

- `2026-02-12T1101`: Planning Petra — roadmap integration for Agent Specialization Hierarchy
- `2026-02-12T1102`: Manager Mike — task assignment for Agent Specialization Hierarchy

---

## Change Log

**2026-02-13 (Planning Petra):**
- Declared M5.1 effectively complete (code done, formal closure pending)
- Defined M6.1: Dashboard Query Architecture (combined M4.3 + Control Plane P1a + P1b)
- Documented rationale for combining workstreams
- Added sequencing diagram and decision checkpoints
- Linked approved technical design and proposed ADRs

**2026-02-12 (Planning Petra):**
- Updated M5.1 progress: 80% complete (4/5 tasks)
- Marked ADR-045 Tasks 1-4 as COMPLETE
- Updated dependencies: Task 5 ready, M4.3 blocked
- Added success metrics and timeline
- Documented retrospective insights

**2026-01-31 (Planning Petra):**
- Initial batch definition (Iteration 2)
- 5 tasks selected across 3 agents
- Dependencies mapped

---

**Related Documents:**
- Technical Design: `docs/architecture/design/local-agent-control-plane-architecture.md`
- ADR-047 (CQRS): `docs/architecture/adrs/ADR-047-cqrs-local-agent-control-plane.md`
- ADR-048 (Run Container): `docs/architecture/adrs/ADR-048-run-container-concept.md`
- ADR-049 (Async Engine): `docs/architecture/adrs/ADR-049-async-execution-engine.md`
- Milestone Checkpoint: `work/coordination/adr045-tasks-1-4-checkpoint.md`
- Architecture Review: `work/reports/architecture/2026-02-12-adr045-final-review.md`
- Dependencies: `work/collaboration/DEPENDENCIES.md`
- Agent Status: `work/collaboration/AGENT_STATUS.md`
