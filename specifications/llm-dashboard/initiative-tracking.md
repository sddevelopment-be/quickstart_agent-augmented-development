---
id: "SPEC-DASH-003"
title: "Initiative Tracking and Portfolio View"
status: "implemented"
initiative: "Dashboard Enhancements"
priority: "HIGH"
epic: "Dashboard Core Features"
target_personas: ["project-manager", "software-engineer", "architect-alphonso"]
features:
  - id: "FEAT-DASH-003-01"
    title: "Specification Parser with Frontmatter Extraction"
    status: "done"
  - id: "FEAT-DASH-003-02"
    title: "Task-to-Spec Linking and Progress Calculator"
    status: "done"
  - id: "FEAT-DASH-003-03"
    title: "Portfolio API Endpoint"
    status: "done"
  - id: "FEAT-DASH-003-04"
    title: "Hierarchical Portfolio UI"
    status: "done"
completion: 100
created: "2026-02-06"
updated: "2026-02-06"
author: "analyst-annie"
---

# Specification: Initiative Tracking and Portfolio View

**Status:** Implemented ✅  
**Created:** 2026-02-06  
**Last Updated:** 2026-02-06  
**Author:** Analyst Annie  
**Stakeholders:** Human-in-Charge, Software Engineers, Project Managers, Agentic Framework Core Team

---

## User Story

**As a** Project Manager or Software Engineer  
**I want** to see tasks organized by initiatives and features (not just a flat list)  
**So that** I understand strategic progress toward business goals, not just operational task completion

**Alternative: Acceptance Criterion Format**  
**Given** I open the dashboard  
**When** I view the Portfolio section  
**Then** I see initiatives (M1, M2, M3) with features grouped underneath, showing progress percentages  
**And** Clicking a feature expands to show related tasks  
**Unless** no specifications exist (fallback to task-only view)

**Target Personas:**
- Project Manager (Primary) - Needs strategic visibility and portfolio management
- Software Engineer (Primary) - Needs to understand how tasks contribute to larger goals
- Agentic Framework Core Team (Primary) - Needs initiative-level planning and tracking
- Line Manager (Secondary) - Needs executive-level progress reporting

---

## Overview

Initiative Tracking transforms the dashboard from a task-centric view to a strategic portfolio view by linking tasks → features → initiatives through the `specifications/` directory. This solves the "tactical blindness" problem where users see individual tasks completing but lack context on strategic progress toward business goals.

**Context:**
- **Problem Solved:** Flat task lists provide no strategic context—"12 tasks done" is meaningless without knowing which features/initiatives progressed
- **Why Needed Now:** Specification-Driven Development (Directive 034) establishes `specifications/` as strategic layer; dashboard should surface this
- **Constraints:**
  - MUST preserve file-based orchestration (specifications are markdown files, not database)
  - MUST work with optional specification coverage (not all tasks have specs)
  - MUST calculate progress dynamically from task states (no manual progress tracking)
  - MUST support incremental adoption (works with 0 specs, improves as specs added)

**Related Documentation:**
- Related ADRs:
  - [ADR-032: Real-Time Execution Dashboard](../../docs/architecture/adrs/ADR-032-real-time-execution-dashboard.md)
  - Pending: ADR-035 Specification-Driven Initiative Tracking
- Related Specifications: [Real-Time Execution Dashboard](real-time-execution-dashboard.md)
- Directives:
  - [Directive 034: Specification-Driven Development](../../.github/agents/directives/034_spec_driven_development.md)
- Background:
  - [Dashboard Spec Integration Proposal](../../docs/planning/dashboard-spec-integration-proposal.md) (11-16 hour estimate)

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** System MUST parse specification frontmatter metadata from `specifications/` directory
- **Rationale:** Specifications contain initiative, status, and feature metadata required for portfolio view
- **Personas Affected:** All personas
- **Success Criteria:** YAML frontmatter parsed from specification markdown files; fields: `id`, `title`, `status`, `initiative`, `epic`, `priority`

**FR-M2:** System MUST link tasks to specifications via `specification` field in YAML
- **Rationale:** Traceability—tasks reference their governing specification
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** Task YAML field `specification: llm-dashboard/real-time-execution-dashboard` links task to spec file

**FR-M3:** System MUST calculate feature progress based on linked task completion
- **Rationale:** Dynamic progress—no manual tracking required
- **Personas Affected:** Project Manager
- **Success Criteria:** Feature progress = (done_tasks / total_tasks) * 100; updates in real-time via WebSocket

**FR-M4:** System MUST group features by initiative (milestone)
- **Rationale:** Strategic hierarchy—initiatives contain features, features contain tasks
- **Personas Affected:** Project Manager, Line Manager
- **Success Criteria:** Portfolio view shows: Initiative → Features → Tasks hierarchy

**FR-M5:** System MUST display portfolio view prominently on dashboard
- **Rationale:** Strategic visibility—portfolio view is primary interface, not hidden
- **Personas Affected:** All personas
- **Success Criteria:** Portfolio view appears above task Kanban board, collapsible section

**FR-M6:** System MUST handle tasks without specifications gracefully
- **Rationale:** Incremental adoption—not all tasks have specs initially
- **Personas Affected:** All personas
- **Success Criteria:** Unlinked tasks appear in "Unspecified Tasks" section; no errors or missing data

### SHOULD Have (Important - Feature degraded without these)

**FR-S1:** System SHOULD show initiative completion percentage
- **Rationale:** Executive summary—high-level progress at a glance
- **Personas Affected:** Project Manager, Line Manager
- **Success Criteria:** Initiative card shows: "M3: Cost Optimization - 60% complete (3/5 features done)"
- **Workaround if omitted:** Users manually count completed features

**FR-S2:** System SHOULD allow expand/collapse of initiative sections
- **Rationale:** Information density—show only relevant initiatives
- **Personas Affected:** Software Engineer
- **Success Criteria:** Click initiative header → Toggle feature list visibility
- **Workaround if omitted:** All initiatives always expanded (scroll fatigue)

**FR-S3:** System SHOULD display feature status badges
- **Rationale:** Visual status—quick scan of feature health
- **Personas Affected:** Software Engineer, Project Manager
- **Success Criteria:** Features show: ✅ Implemented, 🚧 In Progress (40%), 📋 Planned, ❌ Blocked
- **Workaround if omitted:** Text-only status

**FR-S4:** System SHOULD link feature cards to specification files
- **Rationale:** Discoverability—users can read full specification
- **Personas Affected:** Software Engineer
- **Success Criteria:** Click feature title → Open specification markdown in modal or new tab
- **Workaround if omitted:** Users manually navigate file system

**FR-S5:** System SHOULD show task count per feature
- **Rationale:** Scope understanding—how much work is a feature?
- **Personas Affected:** Project Manager
- **Success Criteria:** Feature card shows: "5 tasks (3 done, 1 in progress, 1 pending)"
- **Workaround if omitted:** Users count tasks manually

### COULD Have (Nice to have - Enhances experience)

**FR-C1:** System COULD display initiative timeline/roadmap
- **Rationale:** Planning visibility—when will initiatives complete?
- **Personas Affected:** Project Manager, Line Manager
- **Success Criteria:** Gantt chart or timeline view with initiative milestones
- **If omitted:** No temporal visualization

**FR-C2:** System COULD support custom initiative groupings (beyond milestones)
- **Rationale:** Flexibility—organize by quarter, team, customer, etc.
- **Personas Affected:** Project Manager
- **Success Criteria:** Filter/group by: milestone, epic, quarter, team
- **If omitted:** Milestone grouping only

**FR-C3:** System COULD show velocity metrics per initiative
- **Rationale:** Predictability—estimate completion dates
- **Personas Affected:** Project Manager
- **Success Criteria:** "M3 velocity: 2.5 tasks/week, estimated completion: 2026-02-20"
- **If omitted:** No predictive analytics

**FR-C4:** System COULD support specification dependency visualization
- **Rationale:** Dependency management—understand blockers
- **Personas Affected:** Architect Alphonso, Project Manager
- **Success Criteria:** Mermaid diagram showing: Spec A → Spec B → Spec C dependency chain
- **If omitted:** Manual dependency tracking

### WON'T Have (Explicitly out of scope)

**FR-W1:** System will NOT support manual progress overrides
- **Rationale:** Progress is calculated from tasks (source of truth), not manually set
- **Future Consideration:** Could add "adjusted progress" field for exceptions

**FR-W2:** System will NOT support initiative budget tracking
- **Rationale:** Cost tracking is separate concern (M3 Telemetry)
- **Future Consideration:** Integrate with telemetry cost data later

**FR-W3:** System will NOT support multi-repository portfolio aggregation
- **Rationale:** Single-repo tool; multi-repo requires API federation
- **Future Consideration:** Multi-repo orchestration (ADR-018) future work

---

## Scenarios and Behavior

### Scenario 1: Happy Path - View Portfolio with Initiatives

**Given** I open the dashboard  
**And** Specifications exist with frontmatter: `initiative: M3`, `initiative: M4`  
**And** Tasks are linked to specifications via `specification:` field  
**When** The portfolio view renders  
**Then** I see two initiative cards: "M3: Cost Optimization" and "M4: User Experience"  
**And** Each card shows completion percentage (e.g., "M3: 60% complete")  
**And** Each card lists features grouped underneath  
**And** Each feature shows status badge (✅, 🚧, 📋) and task count

### Scenario 2: Expand/Collapse Initiative

**Given** I am viewing the portfolio with initiative "M3: Cost Optimization"  
**And** The initiative is collapsed (features hidden)  
**When** I click the initiative header  
**Then** The feature list expands smoothly (CSS animation)  
**And** Features are displayed: "Telemetry Infrastructure", "Policy Engine", "Cost Dashboard"  
**When** I click the header again  
**Then** The feature list collapses

### Scenario 3: Drill Down - Feature to Tasks

**Given** I am viewing expanded initiative "M3"  
**And** Feature "Telemetry Infrastructure" shows "🚧 In Progress - 40% (2/5 tasks done)"  
**When** I click the feature card  
**Then** The task list filters to show only tasks linked to that feature  
**And** The task Kanban board highlights: 2 done, 1 in progress, 2 pending  
**When** I click "Show All Tasks" button  
**Then** The filter is cleared

### Scenario 4: Specification Linking

**Given** I am viewing feature "Real-Time Execution Dashboard"  
**When** I click the feature title (hyperlink styled)  
**Then** A modal opens displaying the specification markdown (rendered per Spec B)  
**Or** (Alternative) The specification file opens in a new browser tab

### Scenario 5: Real-Time Progress Update

**Given** I am viewing the portfolio  
**And** Initiative "M3" shows "40% complete (2/5 features)"  
**When** An agent completes a task linked to M3 feature  
**And** The task YAML status changes to "done"  
**And** A WebSocket `task.completed` event is emitted  
**Then** The backend recalculates M3 progress: now 50% (2.5/5 features)  
**And** The portfolio view updates in real-time via WebSocket  
**And** The initiative card animates the progress bar change

### Scenario 6: Unspecified Tasks Fallback

**Given** I have 10 tasks in the inbox  
**And** Only 5 tasks have `specification:` field set  
**When** The portfolio view renders  
**Then** 5 tasks appear under their respective features  
**And** 5 tasks appear in "Unspecified Tasks" section at bottom  
**And** A badge shows: "5 tasks not linked to specifications"  
**And** Clicking the badge expands the unspecified task list

### Scenario 7: Empty State - No Specifications

**Given** The `specifications/` directory is empty or has no frontmatter  
**When** The portfolio view attempts to render  
**Then** A friendly empty state appears: "No initiatives found. Add specifications to track progress."  
**And** A "Learn More" link points to Directive 034 documentation  
**And** The task Kanban board remains functional (fallback to task-only view)

### Scenario 8: Specification Status Filter

**Given** I am viewing the portfolio with 10 features  
**And** Features have status: 3 Implemented, 4 In Progress, 2 Planned, 1 Blocked  
**When** I click filter: "In Progress Only"  
**Then** The view shows only 4 in-progress features  
**When** I click "Show All"  
**Then** All 10 features are visible again

---

## Data Model

### Specification Frontmatter (YAML)
```yaml
---
id: llm-dashboard-001
title: "Real-Time Execution Dashboard"
status: Implemented
initiative: M4-User-Experience
epic: dashboard-integration
priority: HIGH
completion: 100%
target_personas: [software-engineer, agentic-framework-core-team]
created: 2026-02-05
updated: 2026-02-06
author: analyst-annie
features:
  - kanban-board
  - cost-tracking
  - websocket-events
---

# Specification: Real-Time Execution Dashboard
...
```

### Task YAML Linking
```yaml
id: 2026-02-05T1400-backend-dev-rich-terminal-ui
title: "Rich Terminal UI Implementation"
agent: backend-dev
priority: HIGH
status: done
specification: llm-dashboard/real-time-execution-dashboard  # NEW FIELD
milestone: M4
feature: rich-cli
...
```

### Initiative Progress Calculation
```python
# Pseudocode
initiative_progress = sum(feature_progress for feature in initiative.features) / len(initiative.features)

feature_progress = len(done_tasks) / len(all_tasks) * 100

# Example:
# M3 has 3 features:
# - Feature A: 5/5 tasks done = 100%
# - Feature B: 2/5 tasks done = 40%
# - Feature C: 0/3 tasks done = 0%
# M3 progress = (100 + 40 + 0) / 3 = 46.67%
```

---

## UI/UX Specifications

### Portfolio View Layout

**Position:** Top section of dashboard, above task Kanban board  
**Default State:** Expanded (can be collapsed to save space)  
**Responsive:** Stacks initiative cards vertically on mobile

### Initiative Card Design

**Structure:**
```
┌─────────────────────────────────────────────────┐
│ M3: Cost Optimization              [Collapse] │
│ ████████░░░░░░░░░░░░░ 40% (2/5 features)     │
│                                                 │
│ Features:                                       │
│   ✅ Telemetry Infrastructure (5/5 tasks)    │
│   🚧 Policy Engine (2/5 tasks) - 40%         │
│   📋 Cost Dashboard (0/3 tasks) - Planned    │
│                                                 │
│ Unspecified: 3 tasks                           │
└─────────────────────────────────────────────────┘
```

**Color Coding:**
- Initiative header: Dark blue (#1e3a8a)
- Progress bar fill: Gradient (blue → green as completion approaches 100%)
- Feature status:
  - ✅ Implemented: Green (#10b981)
  - 🚧 In Progress: Blue (#3b82f6)
  - 📋 Planned: Gray (#6b7280)
  - ❌ Blocked: Red (#ef4444)

### Interactions

- **Hover Initiative Header:** Show tooltip with metadata (created date, author, total tasks)
- **Click Initiative Header:** Expand/collapse feature list
- **Click Feature Card:** Filter task Kanban to show only that feature's tasks
- **Click Feature Title:** Open specification modal/tab
- **Click Progress Bar:** Show task breakdown modal

---

## Acceptance Criteria

### Definition of Done

- [ ] Specification frontmatter parser reads YAML from `specifications/**/*.md`
- [ ] Task YAML field `specification:` links tasks to spec files
- [ ] Initiative cards display with completion percentages
- [ ] Feature cards display with status badges and task counts
- [ ] Expand/collapse interactions work smoothly
- [ ] Clicking feature filters task Kanban board
- [ ] Clicking feature title opens specification (rendered markdown)
- [ ] Real-time progress updates via WebSocket when tasks complete
- [ ] Unspecified tasks section shows tasks without spec links
- [ ] Empty state displays when no specifications exist
- [ ] Specification status filter (Implemented/In Progress/Planned/Blocked) works
- [ ] Unit tests: Frontmatter parsing, progress calculation
- [ ] Integration tests: End-to-end portfolio view with real specs/tasks
- [ ] Manual test: Add new spec → Create linked tasks → Verify progress updates
- [ ] Documentation: User guide + specification authoring guide

---

## Implementation Approach Recommendation

### Incremental Rollout (3 Phases)

**Phase 1: Metadata Foundation (3-4 hours)**
- Add frontmatter parser (parse YAML from markdown files)
- Add `specification:` field to task YAML schema
- Manually tag 5-10 existing tasks with spec references
- Create specification examples with frontmatter
- Unit tests for parsing and linking

**Phase 2: Backend Progress Calculation (4-5 hours)**
- Create `SpecificationTracker` class (calculates progress dynamically)
- Integrate with file watcher to detect spec changes
- Add REST endpoint: `GET /api/initiatives` (returns hierarchy)
- Add WebSocket event: `initiative.progress_update`
- Integration tests

**Phase 3: Frontend Portfolio View (4-6 hours)**
- Create Initiative Card component
- Create Feature Card component
- Wire to `/api/initiatives` endpoint
- Add expand/collapse interactions
- Add feature filtering (click feature → filter tasks)
- Add specification modal (click feature title → show rendered spec)
- CSS styling for dark theme

**Total Estimated Effort:** 11-15 hours

### Alternative: MVP-First (Single Phase, 6-8 hours)

**Simplified Scope:**
- Display initiatives without expand/collapse (always expanded)
- Show features with task counts only (no status badges)
- Manual progress calculation (no real-time updates)
- Link to spec files (open in new tab, not modal)

**Trade-off:** Faster delivery, limited UX; enhance later

**Recommendation:** Use incremental approach (3 phases) for better UX and maintainability.

---

## Technical Design Considerations

### Specification Frontmatter Parser

**Library:** Use `gray-matter` (JS) or `python-frontmatter` (Python)  
**Caching:** Cache parsed frontmatter in memory, refresh when files change  
**Validation:** Warn if required fields missing (id, title, status, initiative)

### Progress Calculation Strategy

**Option A: Aggregate on Read (Simple)**
- Calculate progress dynamically when `/api/initiatives` called
- Pro: Always accurate, no state management
- Con: Slower for large repos (100+ specs)

**Option B: Cache with Invalidation (Optimized)**
- Calculate once, cache result, invalidate when task status changes
- Pro: Fast reads, scales better
- Con: More complexity, cache invalidation logic

**Recommendation:** Start with Option A (simpler), optimize to Option B if performance issues arise.

### Specification Discovery

**File Pattern:** `specifications/**/*.md`  
**Frontmatter Detection:** Check first 50 lines for `---\n...\n---` delimiter  
**Error Handling:** Skip files with parse errors, log warning

---

## Open Questions

None—implementation approach left flexible per user preference (see FR requirement).

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Low Spec Adoption | HIGH | MEDIUM | Graceful fallback to task-only view; documentation to encourage spec authoring |
| Performance (100+ Specs) | MEDIUM | LOW | Cache parsed frontmatter; pagination for large portfolios |
| Spec/Task Linking Errors | MEDIUM | MEDIUM | Validation warnings; "Unspecified Tasks" section catches orphans |
| Complex Progress Calculation | LOW | LOW | Unit tests with edge cases; simple initial algorithm |

---

## Success Metrics

- **Adoption:** 60% of tasks link to specifications within 1 month
- **Usage:** Portfolio view opened 3x more frequently than task-only view
- **Satisfaction:** Positive feedback on strategic visibility (survey)
- **Performance:** Portfolio view loads <200ms (95th percentile)

---

## References

- **Directive 034:** Specification-Driven Development
- **Specifications Directory:** `specifications/README.md`
- **Dashboard Proposal:** `docs/planning/dashboard-spec-integration-proposal.md`
- **File Watcher:** `src/llm_service/dashboard/file_watcher.py`

---

**Prepared by:** Analyst Annie  
**Date:** 2026-02-06  
**Status:** Draft (ready for Architect Alphonso technical design review)
