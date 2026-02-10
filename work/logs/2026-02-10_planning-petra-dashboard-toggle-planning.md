# Work Log: Planning Petra - Dashboard Finished Work Toggle

**Agent:** Planning Petra  
**Date:** 2026-02-10T11:04:44.127Z  
**Task:** Create task breakdown for dashboard "hide finished work" feature  
**Bootstrap:** ✅ Completed per AGENTS.md

---

## Context

User request: Hide completed tasks by default in dashboard with expandable "Show Finished Work" toggle.

**Requirements:**
1. Dashboard page: 3 always-visible columns (Backlog/Inbox, Assigned, In Progress)
2. Done/Error tasks hidden by default, expandable via button
3. BLOCKED tasks shown in red with ⚠️ icon in their lifecycle column
4. Initiatives page: Same pattern for completed initiatives
5. Status value confirmed: `in_progress` (from TaskStatus enum)

**Plan document created:** `~/.copilot/session-state/.../plan.md`

---

## Specification Capture

### Feature: Hide Finished Work by Default (Dashboard)

**User Story:**
As a dashboard user, I want completed tasks hidden by default so I can focus on active work, with the ability to show finished tasks when I need to review them.

**Acceptance Criteria:**

**AC1: Three-Column Active View**
- GIVEN I am on the Dashboard page
- WHEN the page loads
- THEN I see exactly 3 columns: "Backlog/Inbox", "Assigned", "In Progress"
- AND "Done" and "Error" tasks are not visible

**AC2: Status-to-Column Mapping**
- GIVEN tasks with different statuses exist
- WHEN the dashboard renders
- THEN tasks appear in columns as:
  - NEW, INBOX → "Backlog/Inbox"
  - ASSIGNED → "Assigned"
  - IN_PROGRESS → "In Progress"
  - BLOCKED → respective column with ⚠️ icon and red styling
  - DONE, ERROR → hidden (collapsed section)

**AC3: Blocked Task Visual Treatment**
- GIVEN a task has status=BLOCKED
- WHEN the task is rendered
- THEN it displays ⚠️ icon at the start
- AND has bright red left border (#dc2626)
- AND has light red background (#fef2f2)
- AND appears in its lifecycle column (Inbox, Assigned, or In Progress)

**AC4: Show Finished Work Toggle**
- GIVEN I am viewing the dashboard
- WHEN I click "Show Finished Work" button
- THEN the finished work section expands below the 3 columns
- AND shows DONE tasks in one scrollable column
- AND shows ERROR tasks in another scrollable column
- AND button text changes to "Hide Finished Work"
- AND button icon changes from ▼ to ▲

**AC5: Hide Finished Work**
- GIVEN the finished work section is expanded
- WHEN I click "Hide Finished Work" button
- THEN the finished work section collapses
- AND button text changes to "Show Finished Work"
- AND button icon changes from ▲ to ▼

**AC6: Initiatives Page Pattern**
- GIVEN I am on the Initiatives & Milestones page
- WHEN the page loads
- THEN completed/deprecated initiatives are hidden
- AND a "Show Finished Work" toggle is present
- AND clicking it shows/hides completed initiatives

---

## Task Breakdown

### Task 1: Backend API - Finished Work Filtering
**Agent:** python-pedro  
**Priority:** HIGH  
**Estimated Effort:** 2 hours  

**Description:**
Update dashboard backend API to support filtering finished tasks and provide separate endpoints for active vs finished work.

**Implementation:**
1. Add `/api/tasks?include_done=false` query parameter
2. Use `task_query.load_open_tasks()` for active tasks
3. Create `/api/tasks/finished` endpoint for done/error tasks
4. Update WebSocket event handlers to include status metadata

**Tests:**
- Unit tests for query parameter handling
- Integration tests for API endpoints
- Verify filtering logic with various status combinations

**Files:**
- `src/llm_service/dashboard/app.py`
- `tests/llm_service/dashboard/test_app.py` (new)

---

### Task 2: Frontend - Kanban Board Restructure
**Agent:** frontend-freddy  
**Priority:** HIGH  
**Estimated Effort:** 3 hours  

**Description:**
Restructure dashboard kanban board HTML to add "In Progress" column and hide finished work section by default.

**Implementation:**
1. Add "In Progress" column after "Assigned"
2. Move "Done" column into collapsible section
3. Add "Error" column in collapsible section
4. Add "Show Finished Work" toggle button
5. Apply ARIA attributes for accessibility

**Tests:**
- Visual regression tests (manual)
- Accessibility audit with screen reader
- Responsive layout verification

**Files:**
- `src/llm_service/dashboard/static/index.html`
- `src/llm_service/dashboard/static/dashboard.css`

---

### Task 3: Frontend - Toggle Logic & Task Rendering
**Agent:** frontend-freddy  
**Priority:** HIGH  
**Estimated Effort:** 3 hours  

**Description:**
Implement JavaScript logic for toggling finished work visibility and update task rendering to route tasks to correct columns.

**Implementation:**
1. Add toggle state management (`showFinishedWork` boolean)
2. Implement `toggleFinishedWork()` function
3. Update `getTaskColumn()` to route IN_PROGRESS tasks
4. Add `renderBlockedTask()` for visual treatment
5. Implement `loadFinishedTasks()` for lazy loading
6. Update dashboard load to exclude finished by default

**Tests:**
- Unit tests for column routing logic
- Integration tests for toggle behavior
- WebSocket event handling tests

**Files:**
- `src/llm_service/dashboard/static/dashboard.js`

---

### Task 4: Initiatives Page - Finished Work Toggle
**Agent:** frontend-freddy  
**Priority:** MEDIUM  
**Estimated Effort:** 1.5 hours  

**Description:**
Apply same "hide finished work" pattern to Initiatives & Milestones page for completed/deprecated initiatives.

**Implementation:**
1. Add `showCompletedInitiatives` state
2. Implement `toggleCompletedInitiatives()` function
3. Update `filterPortfolioDisplay()` to hide implemented/deprecated
4. Add toggle button to initiatives page
5. Apply filter after portfolio loading

**Tests:**
- Manual testing of initiative filtering
- Verify state persistence across page switches

**Files:**
- `src/llm_service/dashboard/static/index.html`
- `src/llm_service/dashboard/static/dashboard.js`

---

## Task Creation

Creating YAML task files in `work/collaboration/inbox/`:

1. `2026-02-10T1104-python-pedro-dashboard-api-filtering.yaml`
2. `2026-02-10T1105-frontend-freddy-kanban-restructure.yaml`
3. `2026-02-10T1106-frontend-freddy-toggle-logic.yaml`
4. `2026-02-10T1107-frontend-freddy-initiatives-toggle.yaml`

**Total Estimated Effort:** 9.5 hours  
**Critical Path:** Tasks 1 → 2 → 3 → 4 (sequential dependencies)  
**Batch Size:** 4 tasks (single feature, tight integration)

---

## Execution Plan

**Phase 1: Backend (Task 1)**
- Python Pedro implements API filtering
- TDD: Write tests first, then implementation
- Duration: 2 hours

**Phase 2: Frontend Structure (Task 2)**
- Frontend Freddy restructures HTML/CSS
- Visual testing during implementation
- Duration: 3 hours

**Phase 3: Frontend Logic (Task 3)**
- Frontend Freddy implements toggle behavior
- Integration testing with backend API
- Duration: 3 hours

**Phase 4: Initiatives Toggle (Task 4)**
- Frontend Freddy applies pattern to initiatives page
- Final integration testing
- Duration: 1.5 hours

**Quality Gates:**
- ✅ All existing tests still passing
- ✅ New tests at 80%+ coverage
- ✅ Visual regression checks
- ✅ Accessibility audit (ARIA, keyboard navigation)
- ✅ Work logs created per Directive 014

---

## Dependencies

**Completed:**
✅ TaskStatus enum with IN_PROGRESS  
✅ task_query.py module  
✅ Dashboard infrastructure

**No Blockers**

---

## Next Actions

1. Create 4 task YAML files
2. Initialize as Python Pedro for Task 1
3. Execute TDD cycle (RED → GREEN → REFACTOR)
4. Move to Frontend Freddy for Tasks 2-4
5. Final integration testing
6. Create work logs
7. Update planning artifacts

---

**Status:** PLANNED  
**Agent:** Planning Petra  
**Ready for Execution:** ✅
