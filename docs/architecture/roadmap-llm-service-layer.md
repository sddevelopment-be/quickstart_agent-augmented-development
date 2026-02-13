# Roadmap: LLM Service Layer

**Project:** LLM Service Layer and Agent Control Plane
**Version:** 2.0.0
**Status:** Active — Control Plane phases added 2026-02-13
**Last Updated:** 2026-02-13

---

## Vision

Enable seamless agent-to-LLM interaction through a configuration-driven service layer that optimizes costs, provides unified interfaces, and supports extensible tool integration.

This roadmap now covers two interrelated system layers that have evolved from the same foundation:

- **Phases 0-4:** LLM Service Layer (agent-to-tool routing, cost optimization, distribution)
- **Phases 5-7:** Agent Control Plane (CQRS event architecture, async execution, run container model)

The Control Plane phases build on the LLM Service Layer's telemetry and routing infrastructure. They were approved following the Local Agent Control Plane Architecture design (`docs/architecture/design/local-agent-control-plane-architecture.md`) and are governed by ADR-047, ADR-048, and ADR-049.

---

## Milestones

### ✅ Phase 0: Architecture & Design (Complete)
**Status:** Complete  
**Duration:** Week 0 (2026-02-04)  
**Deliverables:**
- [x] Architectural prestudy (`docs/architecture/design/llm-service-layer-prestudy.md`)
- [x] Human-approved decisions (Python/Node.js, YAML, configurable budgets, claude-code+codex)
- [x] Architecture diagrams (Component, Sequence, Configuration, Deployment)
- [x] Implementation plan with task breakdown

---

### 🔄 Phase 1: Foundation (Milestone 1)
**Status:** In Progress  
**Duration:** Weeks 1-2  
**Start Date:** 2026-02-04 (Tech stack decision: Python)  
**Goal:** Establish core infrastructure and configuration management

**Key Deliverables:**
- [x] Tech stack decision (Python 3.10+ selected)
- [x] Configuration schema (YAML) with Pydantic validation
- [ ] CLI interface foundation (exec, config validate, init, version)
- [ ] Routing engine core (agent-to-tool mapping, fallback chains)
- [ ] Unit test coverage >80%

**Tasks:**
1. ✅ Config schema definition (Backend-Dev) - COMPLETED 2026-02-04
   - Created Pydantic v2 schemas for agents, tools, models, policies
   - Implemented cross-reference validation
   - Created example YAML files for MVP tools
2. 🔄 Config loader implementation (Backend-Dev) - 2-3 days - NEXT
3. 📋 CLI interface foundation (Backend-Dev) - 2-3 days
4. 📋 Routing engine core (Backend-Dev) - 3-4 days

**Dependencies:**
- ✅ Tech stack decision (Python) - RESOLVED 2026-02-04
- ✅ Sample YAML files for claude-code and codex - COMPLETED

**Progress:** 25% complete (1 of 4 tasks done)

---

### 📋 Phase 2: Tool Integration (Milestone 2)
**Status:** Planned  
**Duration:** Weeks 2-3  
**Goal:** Implement tool adapters and subprocess execution

**Key Deliverables:**
- [ ] Base adapter interface/architecture
- [ ] Claude-Code adapter (MVP tool #1)
- [ ] Codex adapter (MVP tool #2)
- [ ] Generic YAML-based adapter (extensibility)
- [ ] Integration test suite >70% coverage

**Tasks:**
5. Adapter base interface (Backend-Dev) - 2 days
6. Claude-Code adapter (Backend-Dev) - 2-3 days
7. Codex adapter (Backend-Dev) - 2-3 days
8. Generic YAML adapter (Backend-Dev) - 2 days

**Dependencies:**
- Completion of Milestone 1 (routing engine)
- Access to claude-code and codex CLIs (or mocks)

---

### 💰 Phase 3: Cost Optimization & Telemetry (Milestone 3)
**Status:** Planned  
**Duration:** Weeks 3-4  
**Goal:** Implement budget enforcement and usage tracking

**Key Deliverables:**
- [ ] SQLite telemetry database with invocation logging
- [ ] Policy engine (budget limits, cost optimization, rate limiting)
- [ ] Stats command (daily/monthly reports, per-agent breakdowns)
- [ ] Privacy controls (metadata-only vs. full logging)

**Tasks:**
9. Telemetry infrastructure (Backend-Dev) - 2-3 days
10. Policy engine (Backend-Dev) - 3-4 days
11. Stats reporting (Backend-Dev) - 2 days

**Dependencies:**
- Completion of Milestone 2 (tool adapters)
- Model cost data in models.yaml

**Human Gate:** Approval required before implementing budget enforcement (cost implications for users)

---

### ✅ Phase 4: Integration & Distribution (Milestone 4)
**Status:** Planned  
**Duration:** Week 4  
**Goal:** End-to-end testing, documentation, and packaging for release

**Key Deliverables:**
- [ ] Acceptance test suite (8 Gherkin scenarios)
- [ ] Cross-platform testing (Linux, macOS, Windows/WSL2)
- [ ] User guide and configuration reference
- [ ] Example workflows for 3 personas
- [ ] Standalone executables (PyInstaller/pkg)
- [ ] Installation scripts and GitHub Release

**Tasks:**
12. Acceptance tests (Backend-Dev) - 2-3 days
13. CI integration (Framework-Guardian) - 1 day
14. User guide (Writer-Editor) - 2 days
15. Persona workflows (Scribe) - 1 day
16. Packaging (Build-Automation) - 1-2 days
17. Installation scripts (Build-Automation) - 1 day

**Dependencies:**
- Completion of Milestones 1-3 (all core functionality)
- CI/CD pipeline supporting cross-platform matrix

**Human Gate:** Final approval before public release

---

---

### ✅ Milestone 5.1: Conceptual Alignment Foundation (COMPLETE)

**Status:** COMPLETE (code done 2026-02-12, formal closure pending Manager Mike sign-off)
**Completed:** 2026-02-12

**Delivered:**
- ADR-046: Domain Module Refactoring — 4/4 tasks, 942 tests, git history preserved
- ADR-045: Doctrine Concept Domain Model — 5/5 tasks complete
  - 6 immutable domain models, 4 markdown parsers, 3 validators
  - 195 tests passing (92% coverage), 0 production errors
  - Performance: 7ms (68x faster than 500ms target)
  - Dashboard portfolio view integration (Task 5)
- All reviews approved: Alphonso, Annie, Claire, Pedro

**Formal Closure:** Manager Mike approval required to archive milestone task files. No code work is outstanding.

---

## Control Plane Phases (Approved 2026-02-13)

These phases implement the Local Agent Control Plane architecture. They were approved following the architecture design review and are backed by ADR-047 (CQRS), ADR-048 (Run Container), and ADR-049 (Async Execution Engine).

**Governing Documents:**
- Architecture Design: `docs/architecture/design/local-agent-control-plane-architecture.md` (Approved)
- ADR-047: `docs/architecture/adrs/ADR-047-cqrs-local-agent-control-plane.md` (Proposed)
- ADR-048: `docs/architecture/adrs/ADR-048-run-container-concept.md` (Proposed)
- ADR-049: `docs/architecture/adrs/ADR-049-async-execution-engine.md` (Proposed)

**Human Gate:** ADR-047, ADR-048, and ADR-049 are currently Proposed. Architect Alphonso review at the CQRS boundary checkpoint (end of M6.1 P1b interface definition) is required before those ADRs are formally approved. Implementation can proceed for P1a; P1b gating point is the interface review.

---

### Phase 5: Control Plane Foundation — M6.1: Dashboard Query Architecture

**Status:** Ready to Start
**Milestone:** M6.1
**Effort:** 5-7 days
**Agents:** Python Pedro (backend), Frontend agent (UI)

**Goal:** Establish the CQRS event boundary and deliver dashboard initiative tracking. This phase combines the Control Plane P1 work with M4.3 (Dashboard Initiative Tracking) because both modify dashboard data access internals. Combining them avoids touching the same files twice.

**Key Deliverables:**
- [ ] JSONL event writer for run telemetry (P1a) — append-only, ADR-047 schema
- [ ] Query Service facade separating read from write path (P1b) — CQRS boundary enforced by interface
- [ ] Initiative tracking backend API — reads via Query Service
- [ ] Dashboard initiative list and status visualization (frontend)

**Tasks:**

| ID | Task | Agent | Effort | Dependency |
|----|------|-------|--------|------------|
| CP-P1a | JSONL event writer | Python Pedro | 1-2 days | None |
| CP-P1b | Query Service facade extraction | Python Pedro | 2-3 days | CP-P1a |
| M4.3-BE | Initiative tracking backend API | Python Pedro | 1-2 days | CP-P1b interface defined |
| M4.3-FE | Frontend integration and visualization | Frontend agent | 2-3 days | M4.3-BE complete |

**Existing Task Reference:** `work/collaboration/assigned/python-pedro/2026-02-06T1150-dashboard-initiative-tracking.yaml`

**Dependencies:**
- M5.1 code complete (met)
- Control Plane architecture design approved (met)
- ADR-047 formal approval: required before P1b ships to production (review checkpoint during P1b interface definition)

**Decision Checkpoints:**
1. JSONL schema review (Architect Alphonso) — before P1a implementation begins
2. CQRS interface review (Architect Alphonso) — after P1b interface is drafted, before implementation
3. M4.3 API contract review (Manager Mike) — after backend API spec is complete
4. M6.1 batch completion review (Manager Mike, Alphonso) — all workstreams done, tests green

**Human Gate:** CQRS boundary review (checkpoint 2) is a hard gate before P1b production implementation proceeds.

---

### Phase 6: Async Execution — M6.2

**Status:** Planned (begins after M6.1 complete)
**Effort:** Estimated 6-9 days
**Agents:** Python Pedro (backend), Framework Guardian (CI/infra)

**Goal:** Implement non-blocking async execution of agent runs, cancellation support, and the Direct Distributor pattern for tool dispatch.

**Key Deliverables:**
- [ ] Async execution engine (ADR-049) — non-blocking run submission and status polling
- [ ] Cancellation protocol — clean shutdown of in-flight runs
- [ ] Direct Distributor — tool dispatch without blocking the caller
- [ ] Async run state machine — submitted → running → done/cancelled/failed
- [ ] Integration tests for async lifecycle

**Tasks:**

| ID | Task | Agent | Effort | Dependency |
|----|------|-------|--------|------------|
| AE-01 | Async execution engine core | Python Pedro | 2-3 days | M6.1 complete |
| AE-02 | Run state machine | Python Pedro | 1-2 days | AE-01 |
| AE-03 | Cancellation protocol | Python Pedro | 1-2 days | AE-02 |
| AE-04 | Direct Distributor | Python Pedro | 1-2 days | AE-01 |
| AE-05 | CI async test harness | Framework Guardian | 1 day | AE-03 |

**Dependencies:**
- M6.1 complete (Query Service must exist for async runs to write events)
- ADR-049 approval (currently Proposed — approval expected during M6.1 planning horizon)

**Human Gate:** ADR-049 formal approval required before M6.2 begins.

---

### Phase 7: Run Container — M6.3

**Status:** Planned (begins after M6.2 complete)
**Effort:** Estimated 5-8 days
**Agents:** Python Pedro (backend), Frontend agent (UI)

**Goal:** Introduce the Run domain model (ADR-048), exposing run history and status in the dashboard and enabling per-run cost and performance tracking.

**Key Deliverables:**
- [ ] Run domain model and repository (ADR-048) — persistent run records
- [ ] Run list and detail views in dashboard
- [ ] Per-run cost and token telemetry surfaced in UI
- [ ] Run-level filtering and search

**Tasks:**

| ID | Task | Agent | Effort | Dependency |
|----|------|-------|--------|------------|
| RC-01 | Run domain model and repository | Python Pedro | 2-3 days | M6.2 complete |
| RC-02 | Run API endpoints | Python Pedro | 1-2 days | RC-01 |
| RC-03 | Dashboard run list view | Frontend agent | 1-2 days | RC-02 |
| RC-04 | Dashboard run detail view | Frontend agent | 1-2 days | RC-03 |

**Dependencies:**
- M6.2 complete (async engine produces run records that RC-01 persists)
- ADR-048 formal approval (currently Proposed)

**Human Gate:** ADR-048 formal approval required before M6.3 begins.

---

## Future Phases (Post-MVP)

### Optional: Advanced Features

**Status:** Not Planned
**Potential Scope:**
- [ ] Parallel tool invocation (concurrent multi-agent workflows)
- [ ] Context management (automatic conversation history tracking)
- [ ] Web UI (local dashboard for configuration and monitoring)
- [ ] Plugin system (user-defined adapters without core changes)
- [ ] Cloud sync (telemetry and config across machines)

**Trigger:** User feedback from MVP pilot deployment

---

## Task List Summary

### LLM Service Layer (Phases 0-4)

| ID | Task | Agent | Milestone | Status | Completed |
|----|------|-------|-----------|--------|-----------|
| 1 | Config schema definition | Backend-Dev | M1 | Complete | 2026-02-04 |
| 2 | Config loader implementation | Backend-Dev | M1 | Next | - |
| 3 | CLI interface foundation | Backend-Dev | M1 | Planned | - |
| 4 | Routing engine core | Backend-Dev | M1 | Planned | - |
| 5 | Adapter base interface | Backend-Dev | M2 | Planned | - |
| 6 | Claude-Code adapter | Backend-Dev | M2 | Planned | - |
| 7 | Codex adapter | Backend-Dev | M2 | Planned | - |
| 8 | Generic YAML adapter | Backend-Dev | M2 | Planned | - |
| 9 | Telemetry infrastructure | Backend-Dev | M3 | Planned | - |
| 10 | Policy engine | Backend-Dev | M3 | Planned | - |
| 11 | Stats reporting | Backend-Dev | M3 | Planned | - |
| 12 | Acceptance tests | Backend-Dev | M4 | Planned | - |
| 13 | CI integration | Framework-Guardian | M4 | Planned | - |
| 14 | User guide | Writer-Editor | M4 | Planned | - |
| 15 | Persona workflows | Scribe | M4 | Planned | - |
| 16 | Packaging | Build-Automation | M4 | Planned | - |
| 17 | Installation scripts | Build-Automation | M4 | Planned | - |

### Control Plane (Phases 5-7)

| ID | Task | Agent | Milestone | Status |
|----|------|-------|-----------|--------|
| CP-P1a | JSONL event writer | Python Pedro | M6.1 | Ready to Start |
| CP-P1b | Query Service facade | Python Pedro | M6.1 | Ready to Start (after P1a) |
| M4.3-BE | Initiative tracking backend API | Python Pedro | M6.1 | Ready to Start (after P1b interface) |
| M4.3-FE | Dashboard initiative UI | Frontend agent | M6.1 | Planned (after M4.3-BE) |
| AE-01 | Async execution engine core | Python Pedro | M6.2 | Planned |
| AE-02 | Run state machine | Python Pedro | M6.2 | Planned |
| AE-03 | Cancellation protocol | Python Pedro | M6.2 | Planned |
| AE-04 | Direct Distributor | Python Pedro | M6.2 | Planned |
| AE-05 | CI async test harness | Framework Guardian | M6.2 | Planned |
| RC-01 | Run domain model and repository | Python Pedro | M6.3 | Planned |
| RC-02 | Run API endpoints | Python Pedro | M6.3 | Planned |
| RC-03 | Dashboard run list view | Frontend agent | M6.3 | Planned |
| RC-04 | Dashboard run detail view | Frontend agent | M6.3 | Planned |

**Critical Path (Control Plane):** CP-P1a → CP-P1b → M4.3-BE → M4.3-FE → AE-01 → AE-02/AE-03 → RC-01 → RC-02 → RC-03/RC-04

---

## Success Metrics

### Technical Metrics
- **Test Coverage:** >80% unit tests, >70% integration tests
- **Performance:** CLI overhead <500ms per invocation
- **Reliability:** Tool fallback success rate >95%
- **Cross-Platform:** Pass all tests on Linux + macOS + WSL2

### Business Metrics
- **Cost Reduction:** 30-56% token cost savings (measured via telemetry)
- **User Adoption:** 10+ agents configured in first month
- **ROI:** Break-even at 13 users or 1 high-volume team
- **Feedback:** >8/10 user satisfaction score

### Operational Metrics
- **Documentation Quality:** All commands documented with examples
- **Onboarding Time:** <30 minutes from install to first successful invocation
- **Support Burden:** <2 hours/week support requests after stable release

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Tech stack indecision delays start | Medium | High | Set 1-week deadline for Python/Node.js choice |
| Tool CLI unavailability blocks testing | Medium | Medium | Use mocks for MVP, real tools for pilot |
| Cross-platform issues (WSL2) | Medium | Medium | Early CI/CD setup, test on all platforms weekly |
| Scope creep (add more tools) | High | Medium | Strict MVP focus (claude-code+codex only), defer others |
| Performance problems (latency) | Low | High | Early performance testing, optimize if >500ms |
| Budget enforcement contention | Medium | Medium | Make configurable (soft/hard), get human approval |

---

## Dependencies

### External Dependencies
- **Claude CLI:** Anthropic's claude-code command-line tool
- **Codex CLI:** OpenAI's codex command-line tool
- **CI/CD Platform:** GitHub Actions with Linux, macOS, Windows runners

### Internal Dependencies
- **Architecture Approval:** ✅ Complete (2026-02-04)
- **Tech Stack Decision:** ✅ Complete (Python 3.10+ selected 2026-02-04)
- **Team Capacity:** ⏳ Pending (1-2 developers allocated)

---

## Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-02-04 | 1.0.0 | Initial roadmap creation with 4 milestones, 17 tasks | Planning Petra |
| 2026-02-04 | 1.1.0 | Added ADR-025 reference for formal architectural decision | Architect Alphonso |
| 2026-02-04 | 1.2.0 | Updated Milestone 1 progress: Task 1 complete, Python selected, 25% done | Planning Petra |
| 2026-02-13 | 2.0.0 | Added Control Plane phases (5-7): M6.1 Dashboard Query Architecture, M6.2 Async Execution, M6.3 Run Container. Documented M5.1 as effectively complete. Linked ADR-047, ADR-048, ADR-049 and approved technical design. | Planning Petra |

---

## References

### LLM Service Layer
- **ADR-025:** `docs/architecture/adrs/ADR-025-llm-service-layer.md` — formal architectural decision record
- **Architecture Prestudy:** `docs/architecture/design/llm-service-layer-prestudy.md`
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md`
- **Diagrams:** `docs/architecture/diagrams/llm-service-layer-*.puml`

### Control Plane
- **Architecture Design (Approved):** `docs/architecture/design/local-agent-control-plane-architecture.md`
- **ADR-047 (CQRS Pattern):** `docs/architecture/adrs/ADR-047-cqrs-local-agent-control-plane.md`
- **ADR-048 (Run Container):** `docs/architecture/adrs/ADR-048-run-container-concept.md`
- **ADR-049 (Async Execution Engine):** `docs/architecture/adrs/ADR-049-async-execution-engine.md`

### Batch Coordination
- **Current Batch (M6.1):** `work/collaboration/NEXT_BATCH.md`
- **Work Directory Orchestration:** `.github/agents/approaches/work-directory-orchestration.md`
