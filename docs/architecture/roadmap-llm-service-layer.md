# Roadmap: LLM Service Layer

**Project:** LLM Service Layer for Agent-Tool Orchestration  
**Version:** 1.0.0  
**Status:** In Planning  
**Last Updated:** 2026-02-04

---

## Vision

Enable seamless agent-to-LLM interaction through a configuration-driven service layer that optimizes costs, provides unified interfaces, and supports extensible tool integration.

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
**Status:** Planned  
**Duration:** Weeks 1-2  
**Start Date:** TBD (pending tech stack decision)  
**Goal:** Establish core infrastructure and configuration management

**Key Deliverables:**
- [ ] Configuration schema (YAML) with validation
- [ ] CLI interface foundation (exec, config validate, init, version)
- [ ] Routing engine core (agent-to-tool mapping, fallback chains)
- [ ] Unit test coverage >80%

**Tasks:**
1. Config schema definition (Backend-Dev) - 3-4 days
2. Config loader implementation (Backend-Dev) - 2-3 days
3. CLI interface foundation (Backend-Dev) - 2-3 days
4. Routing engine core (Backend-Dev) - 3-4 days

**Dependencies:**
- Tech stack decision (Python vs. Node.js) required before start
- Sample YAML files for claude-code and codex

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

## Future Phases (Post-MVP)

### Phase 5: Advanced Features (Optional)
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

| ID | Task | Agent | Milestone | Status |
|----|------|-------|-----------|--------|
| 1 | Config schema definition | Backend-Dev | M1 | 📋 Planned |
| 2 | Config loader implementation | Backend-Dev | M1 | 📋 Planned |
| 3 | CLI interface foundation | Backend-Dev | M1 | 📋 Planned |
| 4 | Routing engine core | Backend-Dev | M1 | 📋 Planned |
| 5 | Adapter base interface | Backend-Dev | M2 | 📋 Planned |
| 6 | Claude-Code adapter | Backend-Dev | M2 | 📋 Planned |
| 7 | Codex adapter | Backend-Dev | M2 | 📋 Planned |
| 8 | Generic YAML adapter | Backend-Dev | M2 | 📋 Planned |
| 9 | Telemetry infrastructure | Backend-Dev | M3 | 📋 Planned |
| 10 | Policy engine | Backend-Dev | M3 | 📋 Planned |
| 11 | Stats reporting | Backend-Dev | M3 | 📋 Planned |
| 12 | Acceptance tests | Backend-Dev | M4 | 📋 Planned |
| 13 | CI integration | Framework-Guardian | M4 | 📋 Planned |
| 14 | User guide | Writer-Editor | M4 | 📋 Planned |
| 15 | Persona workflows | Scribe | M4 | 📋 Planned |
| 16 | Packaging | Build-Automation | M4 | 📋 Planned |
| 17 | Installation scripts | Build-Automation | M4 | 📋 Planned |

**Total Tasks:** 17  
**Estimated Duration:** 4 weeks (assuming 1-2 developers)  
**Critical Path:** Tasks 1→2→3→4→5→6/7→9→10→12→16/17

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
- **Tech Stack Decision:** ⏳ Pending (Python vs. Node.js)
- **Team Capacity:** ⏳ Pending (1-2 developers allocated)

---

## Change Log

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-02-04 | 1.0.0 | Initial roadmap creation with 4 milestones, 17 tasks | Planning Petra |

---

## References

- **Architecture Prestudy:** `docs/architecture/design/llm-service-layer-prestudy.md`
- **Implementation Plan:** `docs/planning/llm-service-layer-implementation-plan.md`
- **Diagrams:** `docs/architecture/diagrams/llm-service-layer-*.puml`
- **Work Directory Orchestration:** `.github/agents/approaches/work-directory-orchestration.md`
