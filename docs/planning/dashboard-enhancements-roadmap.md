# Dashboard Enhancements Roadmap

**Initiative:** Dashboard Enhancements  
**Status:** Batch 1 COMPLETE (3/3 features) + Batch 1.1 Specification Ready  
**Total Effort:**
- Batch 1 (Complete): 26.33h actual vs 27-35h estimated
- Batch 1.1 (Orphan Assignment - Ready): 6-8 hours estimated
- Batch 2 (Pending): 48-63 hours (MVP: 37-48 hours)
- **Combined Total: 80-107 hours (MVP: 69-91 hours)**  
**Priority:** HIGH  
**Start Date:** 2026-02-06  
**Related ADRs:** ADR-035, ADR-036, ADR-037 (Batch 1) + ADR-038, ADR-039, ADR-040 (Batch 2)  
**Related Specs:** specifications/llm-dashboard/

---

## Executive Summary

Seven coordinated enhancements across three implementation batches to transform dashboard from read-only monitoring to interactive management platform:

### Batch 1: Core Interactivity (COMPLETE - 26.33 hours)
1. ✅ **Markdown Rendering** (6h actual vs 9-11h) - Formatted task descriptions with XSS prevention
2. ✅ **Priority Editing** (5.83h actual vs 7-9h) - In-place priority updates with in-progress protection
3. ✅ **Initiative Tracking** (14.5h actual vs 11-15h) - Portfolio view linking specs to tasks

### Batch 1.1: Task Organization (SPECIFICATION READY - 6-8 hours)
4. **Orphan Task Assignment** (6-8h estimated) - Feature-level task linking via modal UI

### Batch 2: Productivity & Automation (48-63 hours)
5. **Docsite Integration** (9-12h) - Context-aware documentation links + help toolbar
6. **Repository Initialization** (16-21h) - Bootstrap Bill web UI with progress streaming
7. **Configuration Management** (23-30h) - Schema-validated config editing interface

**Key Achievement (Batch 1):** Delivered 3/3 core features 25% under estimate with production quality (63-85% test coverage, <100ms latency).

**Next Milestone (Batch 1.1):** Orphan task assignment enables users to organize unlinked work into initiative hierarchy via feature-level modal selector.

---

## Batch 1: Core Interactivity (COMPLETE ✅)

### Implementation Phases

### Phase 1: Markdown Rendering (Week 1)
**Effort:** 9-11 hours  
**Agent:** Frontend Specialist  
**Task:** `2026-02-06T1148-dashboard-markdown-rendering`  
**Priority:** HIGH  
**Dependencies:** None

**Deliverables:**
- ✅ marked.js + DOMPurify integration
- ✅ GFM extensions (tables, task lists, autolinks)
- ✅ Selective rendering (markdown vs. technical fields)
- ✅ XSS prevention with sanitization
- ✅ CSS styling for markdown elements
- ✅ Security testing (OWASP XSS payloads)

**Success Criteria:**
- Task descriptions render with proper formatting
- Code blocks, tables, and lists display correctly
- XSS test suite passing (10+ payloads)
- Performance: <50ms typical, <200ms P95
- Cross-browser compatibility (Chrome, Firefox, Safari)

---

### Phase 2: Priority Editing (Week 1-2)
**Effort:** 7-9 hours  
**Agent:** Backend-dev Benny  
**Task:** `2026-02-06T1149-dashboard-priority-editing`  
**Priority:** HIGH  
**Dependencies:** None (can run parallel to Phase 1)

**Deliverables:**
- ✅ PATCH /api/tasks/:id/priority endpoint
- ✅ YAML file writer with comment preservation (ruamel.yaml)
- ✅ Priority + status validation
- ✅ In-progress task indicator (pulsing dot + badge)
- ✅ Priority dropdown with disabled states
- ✅ Real-time WebSocket updates

**Success Criteria:**
- Priority changes save to YAML without losing comments
- In-progress tasks cannot be edited (409 Conflict)
- All connected clients see priority changes instantly
- Performance: <500ms P95 end-to-end
- Optimistic locking prevents concurrent edit conflicts

---

### Phase 3: Initiative Tracking (Week 2-3)
**Effort:** 11-15 hours (MVP: 6-8 hours)  
**Agent:** Backend-dev Benny + Frontend Specialist  
**Task:** `2026-02-06T1150-dashboard-initiative-tracking`  
**Priority:** MEDIUM  
**Dependencies:**
- Markdown rendering (for formatted descriptions in portfolio)
- Priority editing (for priority dropdown in portfolio)

**Deliverables:**
- ✅ Specification frontmatter parser
- ✅ Task linking via `specification:` field
- ✅ Progress rollup calculator (task → feature → initiative)
- ✅ GET /api/portfolio endpoint
- ✅ Portfolio view UI (hierarchical accordion)
- ✅ Orphan tasks handling

**Success Criteria:**
- Initiative hierarchy displays correctly
- Progress bars reflect actual task completion
- Drill-down navigation works (initiative → feature → task)
- Portfolio loads fast (cached: <50ms, uncached: <500ms)
- Real-time updates when tasks/specs change

**MVP Option (If Time-Constrained):**
- Simple list view (no accordion)
- Manual progress only (skip calculation)
- Reduced effort: 6-8 hours

---

## Batch 1.1: Task Organization Enhancement

### Phase 4: Orphan Task Assignment (NEW - Week 4)
**Effort:** 6-8 hours  
**Agent:** Python Pedro (Backend + Frontend)  
**Task:** TBD - `2026-02-06T1530-dashboard-orphan-assignment`  
**Priority:** MEDIUM  
**Dependencies:** Initiative Tracking (Phase 3) ✅  
**Specification:** [Orphan Task Assignment (SPEC-DASH-007)](../../specifications/llm-dashboard/orphan-task-assignment.md)

**Context:**
Initiative Tracking delivered orphan task visibility, but users cannot assign them to specifications without manual YAML editing. This feature completes the workflow by enabling feature-level task linking via intuitive modal UI.

**Deliverables:**
- [ ] `GET /api/initiatives` endpoint (feature hierarchy for modal)
- [ ] `PATCH /api/tasks/:id/assignment` endpoint (update spec + feature)
- [ ] `task.assigned` WebSocket event
- [ ] Assignment modal UI (initiative → feature tree, expandable)
- [ ] Search/filter for large initiative lists
- [ ] Task context display in modal (title, agent, priority)
- [ ] Bulk assignment support (multi-select orphans)
- [ ] Real-time portfolio refresh after assignment
- [ ] YAML comment preservation during write
- [ ] Path traversal validation + optimistic locking

**Success Criteria:**
- Modal loads in <500ms (P95)
- Specification frontmatter parsing <200ms per spec
- YAML write completes in <300ms (P95)
- Search/filter returns results in <100ms (50 initiatives)
- Orphan task moves to correct portfolio section immediately
- All connected clients see update via WebSocket
- Comments and field order preserved in task YAML
- In-progress tasks cannot be assigned (UI disabled)

**Test Coverage:**
- Unit: 15+ tests (assignment handler, spec registry, validation)
- Integration: 8+ tests (API endpoints, WebSocket events)
- Functional: 5+ acceptance tests (end-to-end workflows)
- Manual: Keyboard navigation, mobile responsive, multi-browser sync

**Technical Highlights:**
- Reuses `task_priority_updater.py` YAML writing patterns
- Caches parsed frontmatter (invalidate on file watcher events)
- Feature-level precision (not just spec-level assignment)
- AI suggestion capability (SHOULD-have: keyword matching)

**Non-Functional:**
- Security: Path traversal prevention, XSS sanitization, optimistic locking
- Performance: <500ms modal load, <200ms frontmatter parsing, <300ms write
- Accessibility: WCAG 2.1 AA, keyboard navigation, screen reader support
- Usability: Error messages non-technical, mobile responsive

**Specification Breakdown:**
- MUST: 10 critical requirements (FR-M1 through FR-M10)
- SHOULD: 7 usability enhancements (FR-S1 through FR-S7)
- COULD: 4 nice-to-have features (FR-C1 through FR-C4)
- WON'T: 3 explicitly excluded (reassignment, spec modification, custom metadata)

**User Workflows Covered:**
1. Basic assignment: Orphan task → Modal → Select feature → Assigned
2. Bulk assignment: Multi-select orphans → Single modal → All to same feature
3. AI-suggested: 1-click assignment based on task metadata (SHOULD-have)

---

## Milestone Timeline

### M4 Batch 4.3 - Dashboard Enhancements (Weeks 1-3)

**Week 1:**
- Day 1-2: Markdown Rendering (Phase 1) ✓
- Day 3-4: Priority Editing Backend (Phase 2 Part A) ✓
- Day 5: Priority Editing Frontend (Phase 2 Part B) ✓

**Week 2:**
- Day 1-2: Initiative Tracking Backend (Phase 3 Part A)
- Day 3: Initiative Tracking Frontend (Phase 3 Part B)
- Day 4-5: Integration Testing + Polish

**Week 3:**
- Day 1: Security audit (XSS, YAML injection, path traversal)
- Day 2: Performance optimization + load testing
- Day 3: Documentation updates (user guide, API docs)
- Day 4: Stakeholder demo + feedback
- Day 5: Bug fixes + final polish

---

## Technical Architecture

### Component Dependencies

```
┌─────────────────────────────────────────────┐
│         Dashboard Frontend                   │
│  ┌─────────────┐  ┌──────────────────────┐ │
│  │ Task Detail │  │ Portfolio View       │ │
│  │ Modal       │  │                      │ │
│  │             │  │ ┌────────────────┐   │ │
│  │ Markdown    │  │ │ Initiative List│   │ │
│  │ Renderer ───┼──┼─► (uses markdown) │   │ │
│  │             │  │ │                │   │ │
│  │ Priority    │  │ │ Priority       │   │ │
│  │ Dropdown ───┼──┼─► Dropdown       │   │ │
│  └─────────────┘  │ │ (uses dropdown)│   │ │
│                   │ └────────────────┘   │ │
│                   └──────────────────────┘ │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│         Dashboard Backend                    │
│  ┌─────────────────┐  ┌─────────────────┐  │
│  │ Priority API    │  │ Portfolio API   │  │
│  │ (YAML writer)   │  │ (Spec parser)   │  │
│  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────┘
```

### Data Flow

1. **Markdown Rendering:** Task data → marked.parse() → DOMPurify → DOM
2. **Priority Editing:** Dropdown → PATCH API → YAML write → File watcher → WebSocket
3. **Portfolio View:** Specs → Parser → Task linker → Progress calc → API → UI

---

## Risk Management

### High-Priority Risks

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| XSS vulnerability in markdown | CRITICAL | DOMPurify sanitization + CSP headers | Addressed in ADR-036 |
| YAML corruption on concurrent edits | HIGH | Optimistic locking + atomic writes | Addressed in ADR-035 |
| Slow portfolio load (100+ specs) | MEDIUM | Caching + file watcher invalidation | Addressed in ADR-037 |
| Frontend complexity explosion | MEDIUM | MVP scope, vanilla JS (no React) | Scoped appropriately |

### Medium-Priority Risks

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Spec frontmatter migration effort | MEDIUM | Automation script provided | Tooling ready |
| Browser compatibility issues | MEDIUM | Cross-browser testing plan | Testing defined |
| Performance regression | MEDIUM | Benchmark targets defined | SLOs established |

---

## Success Metrics

### Usability Metrics
- **Context switching reduction:** 80% (no more leaving dashboard to edit tasks)
- **Task comprehension time:** 50% faster (formatted markdown vs. raw text)
- **Strategic visibility:** 100% improvement (no portfolio view → full initiative tracking)

### Technical Metrics
- **Markdown render time:** <50ms typical, <200ms P95
- **Priority update latency:** <500ms P95 end-to-end
- **Portfolio load time:** <50ms cached, <500ms uncached
- **Test coverage:** 80%+ for all new code
- **Security: **0 XSS vulnerabilities, 0 YAML injection vulnerabilities

### Adoption Metrics (Post-Launch)
- **Dashboard usage frequency:** Track daily active sessions
- **Priority edits per week:** Measure feature adoption
- **Portfolio view engagement:** Track time spent in portfolio view

---

## Documentation Requirements

### User Documentation
- [ ] Markdown syntax guide for task descriptions
- [ ] Priority editing user guide
- [ ] Portfolio view navigation guide
- [ ] Update DASHBOARD_QUICKSTART.md

### Technical Documentation
- [ ] API documentation (/api/tasks/:id/priority, /api/portfolio)
- [ ] WebSocket event protocol
- [ ] Specification frontmatter schema (JSON Schema)
- [ ] Security best practices guide

### Maintenance Documentation
- [ ] Troubleshooting guide (common issues + solutions)
- [ ] Performance tuning guide
- [ ] Backup and recovery procedures

---

## Post-Implementation Review

### Review Criteria
- All acceptance criteria met (from specifications)
- ADR compliance verified (ADR-035, ADR-036, ADR-037)
- Security audit passed (XSS, YAML injection, path traversal)
- Performance benchmarks met (SLOs satisfied)
- User feedback collected and addressed

### Review Participants
- **Architect Alphonso:** Technical design compliance
- **Backend-dev Benny:** Implementation quality
- **Frontend Specialist:** UI/UX polish
- **Human-in-Charge:** Stakeholder acceptance

### Review Schedule
- **Target Date:** 3 weeks from implementation start
- **Format:** Live demo + documentation review + code walkthrough
- **Deliverables:** Review report with approval/conditional approval/revision needed

---

## Batch 2: Productivity & Automation

### Implementation Phases

### Phase 4: Docsite Integration (Week 4)
**Effort:** 9-12 hours  
**Agent:** Frontend Specialist  
**Task:** `2026-02-06T1220-dashboard-docsite-integration`  
**Priority:** MEDIUM  
**Dependencies:** None

**Deliverables:**
- ✅ Pattern-based link resolver (dashboard-doc-links.js)
- ✅ /api/config/docsite configuration endpoint
- ✅ Auto-linkification (agent names → profiles, ADR-XXX → docs)
- ✅ Help toolbar UI (bottom-right, toggle menu)
- ✅ CSS styling for doc links (external icon, hover states)
- ✅ Accessibility testing (keyboard nav, ARIA labels)

**Success Criteria:**
- Agent names clickable, open profile pages in new tab
- ADR references auto-linkify (regex: ADR-\d{3})
- Help toolbar visible with 5+ documentation shortcuts
- Broken links gracefully handled (404 acceptable)
- Performance: Link resolution <1ms, config fetch <50ms

---

### Phase 5: Repository Initialization (Week 5)
**Effort:** 16-21 hours (MVP: 14-18 hours with polling fallback)  
**Agent:** Backend-dev Benny  
**Task:** `2026-02-06T1221-dashboard-repository-initialization`  
**Priority:** MEDIUM  
**Dependencies:** None

**Deliverables:**
- ✅ Initialization modal with form (vision, constraints, guidelines)
- ✅ /api/init/check endpoint (re-bootstrap detection)
- ✅ /api/init/execute endpoint (Bootstrap Bill subprocess)
- ✅ Progress streaming (WebSocket or polling fallback)
- ✅ Re-bootstrap warning dialog
- ✅ Error handling and timeout protection (10 minutes)

**Success Criteria:**
- Form validates vision length (50-5000 chars)
- Re-bootstrap warning shows if repository initialized
- Bootstrap Bill executes successfully (2-5 minutes)
- Progress log displays real-time output
- Subprocess hangs killed after timeout
- Dashboard reloads after successful initialization

**MVP Option:** Use polling fallback (4-5h Phase 3) instead of WebSocket streaming (6-8h)
- Simpler implementation, acceptable 2s latency
- Upgrade to WebSocket in future iteration if needed

---

### Phase 6: Configuration Management (Week 6-7)
**Effort:** 23-30 hours (MVP: 14-18 hours without rich markdown editor)  
**Agent:** Backend-dev Benny + Frontend Specialist  
**Task:** `2026-02-06T1222-dashboard-configuration-management`  
**Priority:** HIGH  
**Dependencies:** None

**Deliverables:**
- ✅ Tabbed config viewer (LLM Service, Agent Stack, Agent Profiles)
- ✅ Inline editing for agent-model mappings
- ✅ Schema validation (jsonschema library)
- ✅ File writers with comment preservation (ruamel.yaml)
- ✅ Agent profile editor (frontmatter form + markdown textarea)
- ✅ Optimistic locking (mtime checks)
- ✅ Security validation (path traversal, YAML injection prevention)

**Success Criteria:**
- Config viewer loads all three tabs (<200ms)
- Agent-model mappings editable inline (dropdown)
- Validation errors display before file writes
- YAML comments preserved after edits
- Agent profiles editable (frontmatter + markdown)
- Concurrent edits detected (409 Conflict on mtime mismatch)
- Performance: <500ms P95 for config updates

**MVP Option:** Simple textarea for markdown (Phase 1-3 only)
- No rich editor (EasyMDE/SimpleMDE)
- No live preview panel
- Sufficient for most editing tasks
- Defer rich editor to Phase 2 if needed (adds 9-12h)

---

## Batch 2: Milestone Timeline

### Week 4: Docsite Integration
**Duration:** 2-3 days (9-12 hours)

| Day | Focus | Hours |
|-----|-------|-------|
| 1-2 | Link resolver + auto-linkification | 7-8h |
| 3   | Help toolbar + testing | 2-4h |

**Milestone Completion Criteria:**
- ✅ Agent links and ADR refs clickable
- ✅ Help toolbar functional
- ✅ Accessibility tests passing

---

### Week 5: Repository Initialization
**Duration:** 3-4 days (14-21 hours)

| Day | Focus | Hours |
|-----|-------|-------|
| 1   | UI form + validation | 4-5h |
| 2-3 | Bootstrap Bill integration | 6-8h |
| 4   | Progress streaming (polling or WebSocket) | 4-8h |

**Milestone Completion Criteria:**
- ✅ Initialization modal functional
- ✅ Bootstrap Bill subprocess executes
- ✅ Progress feedback working
- ✅ Re-bootstrap warning prevents accidents

---

### Week 6-7: Configuration Management
**Duration:** 5-6 days (14-30 hours depending on MVP vs full)

| Day | Focus | Hours |
|-----|-------|-------|
| 1-2 | Config viewer (tabbed UI) | 6-8h |
| 3-4 | Inline editing + validation | 8-10h |
| 5-6 | Agent profile editor | 6-12h (MVP) or 15-24h (full) |

**Milestone Completion Criteria:**
- ✅ All config tabs render correctly
- ✅ Inline editing saves to files
- ✅ Schema validation prevents errors
- ✅ Agent profiles editable
- ✅ Security tests passing

---

## Batch 2: Risk Management

### Risk Matrix

| Risk | Likelihood | Impact | Mitigation Strategy | Owner |
|------|------------|--------|---------------------|-------|
| Bootstrap Bill subprocess hangs | MEDIUM | HIGH | 10-minute timeout + kill signal | Backend-dev |
| Configuration validation too strict | MEDIUM | MEDIUM | Provide clear error messages, allow overrides | Backend-dev |
| Concurrent config edits cause conflicts | LOW | MEDIUM | Optimistic locking with mtime checks | Backend-dev |
| Documentation links break after docsite restructure | MEDIUM | LOW | Pattern-based URLs, easy to update | Frontend |
| WebSocket streaming adds complexity | MEDIUM | LOW | Use polling fallback for MVP | Backend-dev |

---

## Batch 2: Success Metrics

### Usability Metrics
- **Docsite Integration:** Documentation link clicks per session >2
- **Repository Initialization:** Initialization completion rate >90%
- **Configuration Management:** Config edit error rate <5%

### Technical Metrics
- **Docsite:** Link resolution <1ms, config fetch <50ms
- **Initialization:** Bootstrap Bill execution 2-5 minutes (unchanged)
- **Config Management:** Update latency <500ms P95

### Adoption Metrics
- **Docsite:** Percentage of sessions with doc link clicks >50%
- **Initialization:** New repositories initialized via dashboard >50%
- **Config Management:** Config edits via dashboard >30% of total

---

## Combined Batch 1 + Batch 2: Documentation Requirements

### User Documentation (Batch 2 Additions)
- [ ] Docsite integration user guide
- [ ] Repository initialization tutorial
- [ ] Configuration management guide
- [ ] Update DASHBOARD_QUICKSTART.md with new features

### Technical Documentation (Batch 2 Additions)
- [ ] /api/config/docsite, /api/init/*, /api/config/* API documentation
- [ ] Link resolution patterns and URL templates
- [ ] Bootstrap Bill integration architecture
- [ ] Configuration schema documentation
- [ ] Security validation rules

---

## Post-Implementation Review (Updated for Both Batches)

### Review Criteria
- **Batch 1:** Markdown rendering, priority editing, initiative tracking
- **Batch 2:** Docsite integration, repository initialization, config management
- All acceptance criteria met (from 6 specifications)
- ADR compliance verified (ADR-035 through ADR-040)
- Security audit passed (XSS, YAML injection, path traversal, subprocess injection)
- Performance benchmarks met (all SLOs satisfied)
- User feedback collected and addressed

### Review Participants
- **Architect Alphonso:** Technical design compliance (6 ADRs)
- **Backend-dev Benny:** Implementation quality (4 of 6 features)
- **Frontend Specialist:** UI/UX polish (2 of 6 features)
- **Human-in-Charge:** Stakeholder acceptance

### Review Schedule
- **Batch 1 Review:** 3 weeks from start (Week 3)
- **Batch 2 Review:** 7 weeks from start (Week 7)
- **Format:** Live demo + documentation review + code walkthrough
- **Deliverables:** Review report with approval/conditional approval/revision needed


---

## Future Enhancements (Deferred)

### Near-Term (3-6 months)
- Gantt chart timeline view for initiatives
- Burndown charts for tracking velocity
- Dependency visualization (task → task, feature → feature)
- Keyboard shortcuts for power users

### Long-Term (6-12 months)
- GitHub Projects bidirectional sync (optional)
- Multi-repository portfolio aggregation
- AI-powered insights (completion predictions, blocker detection)
- Mobile-responsive portfolio view

---

## References

- **ADRs:** ADR-035 (Priority), ADR-036 (Markdown), ADR-037 (Portfolio)
- **Specifications:** specifications/llm-dashboard/*.md
- **Technical Design:** docs/architecture/design/dashboard-enhancements-technical-design.md
- **Tasks:** work/collaboration/inbox/2026-02-06T11*-dashboard-*.yaml

---

**Document Owner:** Planning Petra  
**Last Updated:** 2026-02-06  
**Status:** ✅ **APPROVED** - Ready for implementation  
**Next Review:** After Phase 3 completion (estimated 3 weeks)
