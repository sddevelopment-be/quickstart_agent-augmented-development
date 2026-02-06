# Dashboard Enhancements Roadmap

**Initiative:** Dashboard Enhancements  
**Status:** Ready for Implementation  
**Total Effort:** 27-35 hours (MVP: 21-28 hours)  
**Priority:** HIGH  
**Start Date:** 2026-02-06  
**Related ADRs:** ADR-035, ADR-036, ADR-037  
**Related Specs:** specifications/llm-dashboard/

---

## Executive Summary

Three coordinated enhancements to improve dashboard usability, readability, and strategic visibility:

1. **Markdown Rendering** (9-11 hours) - Formatted task descriptions with XSS prevention
2. **Priority Editing** (7-9 hours) - In-place priority updates with in-progress protection
3. **Initiative Tracking** (11-15 hours) - Portfolio view linking specs to tasks

**Key Achievement:** Transform dashboard from read-only monitoring tool to interactive task management interface with strategic context.

---

## Implementation Phases

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
