---
id: "SPEC-DASH-008"
title: "Dashboard Orphan Task Assignment"
status: "ready_for_review"
version: "1.0.0"
initiative: "Dashboard Enhancements"
priority: "MEDIUM"
epic: "Dashboard Core Features"
target_personas: ["software-engineer", "project-manager"]
features:
  - id: "FEAT-DASH-008-01"
    title: "Orphan Task Detection and Display"
    status: "draft"
  - id: "FEAT-DASH-008-02"
    title: "Interactive Specification/Feature Selector"
    status: "draft"
  - id: "FEAT-DASH-008-03"
    title: "YAML File Update with Comment Preservation"
    status: "draft"
completion: 0
created: "2026-02-06"
updated: "2026-02-09"
author: "analyst-annie"
reviewer: "architect-alphonso"
---

# Specification: Dashboard Orphan Task Assignment (Feature-Level)

**Status:** Ready for Review  
**Version:** 1.0.0  
**Created:** 2026-02-06  
**Last Updated:** 2026-02-09  
**Author:** Analyst Annie  
**Reviewer:** Architect Alphonso  
**Stakeholders:** Human-in-Charge, Software Engineers, Agentic Framework Core Team

---

## User Story

**As a** Software Engineer managing multi-agent workflows  
**I want** to assign orphan tasks to specific features within specifications  
**So that** I can organize unlinked work into the proper initiative hierarchy without manually editing YAML files

**Alternative: Acceptance Criterion Format**  
**Given** I have orphan tasks displayed in the dashboard  
**When** I click "Assign" and select a specification and feature from the hierarchy  
**Then** the task is linked to that feature and appears in the correct initiative section  
**Unless** the specification file doesn't exist or the task is already being worked on

**Target Personas:**
- Software Engineer (Primary) - Needs to organize incoming tasks and link them to active initiatives
- Agentic Framework Core Team (Primary) - Needs clear task-to-feature-to-initiative traceability
- Project Manager (Secondary) - Needs accurate portfolio view with all work properly categorized

---

## Overview

Orphan task assignment enables users to link tasks without a `specification:` field (or with invalid paths) to specific features within specifications, moving them from the "Orphan Tasks" section into the structured initiative hierarchy. This solves the "categorization problem" where new tasks arrive in the inbox without clear initiative context.

**Context:**
- **Problem Solved:** Manual categorization burden—users must open YAML files, look up specification paths, and manually add `specification:` field
- **Why Needed Now:** Initiative Tracking feature (ADR-037) delivered; orphan tasks are now visible but not actionable
- **Constraints:**
  - MUST preserve YAML file format and comments
  - MUST respect file-based orchestration (no database-only state)
  - MUST validate specification file existence before linking
  - MUST allow feature-level granularity (not just specification-level)
  - MUST handle specification frontmatter to extract feature structure

**Related Documentation:**
- Related ADRs: 
  - [ADR-037: Dashboard Initiative Tracking](../../docs/architecture/adrs/ADR-037-dashboard-initiative-tracking.md)
  - [ADR-035: Task Priority Editing](../../docs/architecture/adrs/ADR-035-dashboard-task-priority-editing.md) (YAML writing patterns)
- Related Specifications: 
  - [Initiative Tracking](initiative-tracking.md) (Parent feature)
  - [Task Priority Editing](task-priority-editing.md) (YAML update patterns)
- Background:
  - [File-Based Orchestration Approach](../../.github/agents/approaches/work-directory-orchestration.md)
  - [Specification-Driven Development (Directive 034)](../../.github/agents/directives/034_specification_driven_development.md)

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** System MUST allow users to assign orphan tasks to features via dashboard UI
- **Rationale:** Core feature purpose—enable task-to-feature linking without leaving dashboard
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** Click "Assign" on orphan task → Select initiative/feature from modal → Task linked and moved to portfolio section

**FR-M2:** System MUST display initiative → feature hierarchy in assignment modal
- **Rationale:** Users need to see structure to make informed assignment decisions (feature-level precision)
- **Personas Affected:** Software Engineer, Project Manager
- **Success Criteria:** Modal shows expandable tree: Initiative > Feature > (Select this feature) button

**FR-M3:** System MUST update task YAML file with `specification:` and `feature:` fields
- **Rationale:** Preserve file-based orchestration—YAML remains source of truth with feature granularity
- **Personas Affected:** All personas (Git audit trail, multi-agent coordination)
- **Success Criteria:** 
  - `specification: specifications/llm-dashboard/markdown-rendering.md` added to task YAML
  - `feature: Feature 2: Selective Field Rendering` added to task YAML (if feature specified)

**FR-M4:** System MUST validate specification file existence before assignment
- **Rationale:** Prevent broken links—task assigned to non-existent spec breaks portfolio view
- **Personas Affected:** Software Engineer (debugging broken links)
- **Success Criteria:** 400 Bad Request if specification path doesn't exist; user-facing error message in UI

**FR-M5:** System MUST preserve YAML file structure and comments during assignment
- **Rationale:** Manual editing coexists with dashboard editing—don't lose user annotations
- **Personas Affected:** Software Engineer (hand-edits YAML for complex changes)
- **Success Criteria:** Comments, blank lines, and field order preserved after assignment

**FR-M6:** System MUST emit WebSocket event after task assignment
- **Rationale:** Real-time synchronization—orphan task disappears from orphan section, appears in initiative section immediately
- **Personas Affected:** Software Engineer (multi-browser scenarios), Agentic Framework Core Team
- **Success Criteria:** `task.updated` event emitted within 100ms of file write; all clients refresh portfolio

**FR-M7:** System MUST prevent assignment of in-progress or completed tasks
- **Rationale:** Changing specification mid-execution could confuse agents; completed tasks should remain immutable
- **Personas Affected:** Agentic Framework Core Team (execution integrity)
- **Success Criteria:** Assign button disabled for `status: in_progress`, `done`, `failed` tasks; tooltip explains why

**FR-M8:** System MUST parse specification frontmatter to extract feature list
- **Rationale:** Feature hierarchy comes from spec YAML frontmatter—must be dynamically loaded
- **Personas Affected:** Software Engineer (sees accurate feature list)
- **Success Criteria:** Features listed in modal match `features:` array in specification frontmatter

**FR-M9:** System MUST handle specifications without feature structure gracefully
- **Rationale:** Some specifications may not define features (specification-level only)
- **Personas Affected:** Software Engineer (assigns to spec root)
- **Success Criteria:** If no features defined, modal shows "Assign to [Spec Name] (Root)" option

**FR-M10:** System MUST provide search/filter capability for large initiative lists
- **Rationale:** As project grows (10+ initiatives), scrolling becomes inefficient
- **Personas Affected:** Software Engineer (quick assignment)
- **Success Criteria:** Search input filters initiatives and features by name; fuzzy match supported

### SHOULD Have (Important - Enhances usability significantly)

**FR-S1:** System SHOULD display task context in assignment modal
- **Rationale:** Users need to see task details to make informed assignment decisions
- **Personas Affected:** Software Engineer, Project Manager
- **Success Criteria:** Modal shows task title, description (first 200 chars), agent, priority

**FR-S2:** System SHOULD suggest relevant specifications based on task metadata
- **Rationale:** AI-assisted categorization reduces cognitive load
- **Personas Affected:** Software Engineer (faster workflow)
- **Success Criteria:** 
  - If task title contains "dashboard", suggest dashboard-related specs first
  - If task assigned to `python-pedro`, suggest backend specs first
  - Suggestions appear at top of initiative list with "Suggested" badge

**FR-S3:** System SHOULD allow bulk assignment of multiple orphan tasks
- **Rationale:** Batch operations save time when triaging multiple tasks
- **Personas Affected:** Software Engineer (weekly triage sessions)
- **Success Criteria:** Checkbox selection → "Assign Selected" button → Single modal assigns all to same feature

**FR-S4:** System SHOULD show preview of task in portfolio context before confirming
- **Rationale:** Visual confirmation reduces assignment errors
- **Personas Affected:** Software Engineer (quality assurance)
- **Success Criteria:** After selecting feature, modal shows "Task will appear under: [Initiative] > [Feature] > [Task Title]" preview

**FR-S5:** System SHOULD track assignment history for undo capability
- **Rationale:** Mistakes happen—allow quick rollback without manual YAML editing
- **Personas Affected:** Software Engineer (error recovery)
- **Success Criteria:** "Undo Last Assignment" button available for 30 seconds after assignment

**FR-S6:** System SHOULD display orphan task count badge
- **Rationale:** Visual indicator encourages triage (empty inbox methodology)
- **Personas Affected:** Software Engineer, Project Manager
- **Success Criteria:** Badge shows orphan count (e.g., "🔗 12 Orphan Tasks"); updates in real-time

**FR-S7:** System SHOULD persist feature selections for repeated assignments
- **Rationale:** Users often assign multiple tasks to the same feature in sequence
- **Personas Affected:** Software Engineer (reduced clicks)
- **Success Criteria:** "Assign another task to [Last Feature]" quick-action button; resets after 5 minutes

### COULD Have (Nice-to-have - Low priority enhancements)

**FR-C1:** System COULD support drag-and-drop assignment from orphan section to portfolio
- **Rationale:** Most intuitive UX for power users
- **Personas Affected:** Software Engineer (frequent users)
- **Success Criteria:** Drag orphan task card → Drop on feature section → Task assigned

**FR-C2:** System COULD generate AI-powered assignment recommendations
- **Rationale:** LLM analysis of task description suggests best-fit feature
- **Personas Affected:** Software Engineer (AI augmentation)
- **Success Criteria:** "AI Suggests: [Feature Name] (85% confidence)" shown in modal

**FR-C3:** System COULD allow inline creation of new features during assignment
- **Rationale:** Orphan task may reveal gap in feature structure
- **Personas Affected:** Project Manager (adaptive planning)
- **Success Criteria:** "+ Create New Feature" button in modal → Inline form → Updates spec frontmatter + assigns task

**FR-C4:** System COULD display related tasks when assigning (e.g., same agent, similar title)
- **Rationale:** Batch assignment of related work improves organization
- **Personas Affected:** Software Engineer (contextual awareness)
- **Success Criteria:** "Related orphan tasks: [Task A], [Task B]" shown in modal with quick-add checkboxes

### WON'T Have (Explicitly excluded from this version)

**FR-W1:** System WON'T support task reassignment between features
- **Rationale:** Scope creep—reassignment is separate feature (v2 enhancement)
- **Alternative:** Manual YAML editing for now; separate spec later

**FR-W2:** System WON'T modify specification frontmatter automatically
- **Rationale:** Specifications are authoritative documents requiring human review
- **Alternative:** Task links to spec via `specification:` field; spec remains static

**FR-W3:** System WON'T support custom metadata fields during assignment
- **Rationale:** Assignment is singular purpose—additional fields require task editing modal (separate feature)
- **Alternative:** Assign first, then use task detail modal to add metadata

---

## Non-Functional Requirements

### Performance Requirements

**NFR-P1:** Assignment modal MUST load in <500ms (P95)
- **Rationale:** Interactive UX—perceived lag breaks flow
- **Measurement:** Time from "Assign" button click to modal fully rendered
- **Trade-offs:** Caching specification list acceptable if refresh latency <1s

**NFR-P2:** Specification frontmatter parsing MUST complete in <200ms per spec
- **Rationale:** Modal displays all initiatives; slow parsing blocks UI
- **Measurement:** Backend timer from file read to parsed feature list
- **Trade-offs:** Cache parsed frontmatter; invalidate on file change (via file watcher)

**NFR-P3:** YAML file write operation MUST complete in <300ms (P95)
- **Rationale:** Real-time feel—user expects instant feedback
- **Measurement:** Time from API request received to file written + WebSocket event emitted
- **Trade-offs:** Atomic writes (temp file → rename) acceptable overhead

**NFR-P4:** Search/filter MUST return results in <100ms for up to 50 initiatives
- **Rationale:** Instant feedback for typeahead search
- **Measurement:** Time from keypress to filtered list rendered
- **Trade-offs:** Client-side filtering acceptable (no backend round-trip)

### Reliability Requirements

**NFR-R1:** System MUST handle concurrent assignment attempts with conflict resolution
- **Rationale:** Multiple users may assign same orphan task simultaneously
- **Measurement:** Last-write-wins with notification, or optimistic locking (HTTP 409)
- **Trade-offs:** Optimistic locking preferred (safer) but requires retry UX

**NFR-R2:** System MUST gracefully degrade if specification file is malformed
- **Rationale:** Bad YAML in spec shouldn't break assignment feature entirely
- **Measurement:** Invalid spec skipped in initiative list; error logged; user sees "1 spec unavailable" notice
- **Trade-offs:** Silent skip vs user notification (choose notification for transparency)

**NFR-R3:** System MUST validate YAML integrity after write operation
- **Rationale:** Prevent corrupted task files from breaking orchestration
- **Measurement:** YAML round-trip test (write → read → compare) before WebSocket emit
- **Trade-offs:** 50ms validation overhead acceptable for data integrity

### Usability Requirements

**NFR-U1:** Assignment modal MUST be accessible (WCAG 2.1 AA)
- **Rationale:** Keyboard navigation, screen reader support required
- **Measurement:** Tab navigation works; Esc closes modal; Enter confirms; ARIA labels present
- **Trade-offs:** Vanilla JS accessible patterns acceptable (no framework needed)

**NFR-U2:** Error messages MUST be actionable and non-technical
- **Rationale:** User-facing errors should guide resolution, not expose internals
- **Examples:**
  - ❌ "IOError: [Errno 2] No such file or directory: 'spec.md'"
  - ✅ "That specification no longer exists. Please refresh the page and try again."
- **Trade-offs:** Log technical details server-side; show friendly message client-side

**NFR-U3:** Modal MUST be responsive (mobile, tablet, desktop)
- **Rationale:** Dashboard used on various devices
- **Measurement:** 
  - Mobile (<768px): Single-column layout, full-screen modal
  - Tablet (768-1024px): 80% width modal, scrollable list
  - Desktop (>1024px): 600px fixed-width modal, nested expand/collapse
- **Trade-offs:** Touch-friendly targets (44px min) on mobile

### Security Requirements

**NFR-SEC1:** System MUST validate specification path to prevent directory traversal
- **Rationale:** Malicious input: `specification: ../../../etc/passwd`
- **Measurement:** Path validation regex; reject paths outside `specifications/` directory
- **Trade-offs:** Whitelist approach (only allow `specifications/**/*.md`)

**NFR-SEC2:** System MUST sanitize task data displayed in modal (XSS prevention)
- **Rationale:** Task description may contain user-generated markdown with malicious scripts
- **Measurement:** DOMPurify sanitization before rendering; CSP headers enforced
- **Trade-offs:** Same security layers as markdown rendering feature (ADR-036)

---

## User Workflows

### Workflow 1: Basic Orphan Task Assignment

**Actors:** Software Engineer

**Preconditions:**
- Dashboard loaded and connected
- At least one orphan task exists in "Orphan Tasks" section
- At least one specification exists with defined features

**Main Flow:**
1. User views "Orphan Tasks" section in dashboard
2. User identifies task to assign: "Add telemetry collection to track tool usage patterns"
3. User clicks **"📎 Assign"** button on task card
4. System opens **Assignment Modal** displaying:
   - Task preview (title, agent, priority)
   - Initiative hierarchy (collapsed)
   - Search bar at top
5. User expands **"Dashboard Enhancements"** initiative (click)
6. System reveals features under initiative:
   - Feature 1: Markdown Rendering
   - Feature 2: Priority Editing
   - Feature 3: Initiative Tracking
   - Feature 4: Docsite Integration
7. User clicks **"Assign to Feature 3: Initiative Tracking"** button
8. System validates specification file exists
9. System updates task YAML:
   ```yaml
   specification: specifications/llm-dashboard/initiative-tracking.md
   feature: "Feature 3: Initiative Tracking"
   ```
10. System emits WebSocket `task.updated` event
11. System shows success toast: **"Task assigned to Initiative Tracking"**
12. System closes modal
13. Task disappears from "Orphan Tasks" section
14. Task appears under **Dashboard Enhancements > Initiative Tracking** in portfolio

**Postconditions:**
- Task YAML file updated with `specification:` and `feature:` fields
- Task visible in correct initiative hierarchy
- All connected clients see updated portfolio
- Git shows atomic commit (if auto-commit enabled)

**Alternative Flows:**

**A1: Specification File Not Found**
- At step 8, system detects specification file missing
- System shows error: **"Specification file not found. The file may have been moved or deleted. Please refresh and try again."**
- Modal remains open; assignment cancelled
- User can select different feature or close modal

**A2: Task Status is In Progress**
- At step 3, system detects task status is `in_progress`
- System disables **"Assign"** button
- Tooltip on hover: **"Cannot assign tasks that are currently being worked on"**
- User must wait for task completion or cancel agent execution

**A3: Concurrent Assignment Conflict**
- At step 9, system detects task file modified since modal opened
- System shows conflict dialog: **"This task was modified by another user. Refresh and try again?"**
- User clicks **"Refresh"** → Modal reloads with latest data
- User repeats assignment flow

---

### Workflow 2: Bulk Assignment of Multiple Orphan Tasks

**Actors:** Software Engineer

**Preconditions:**
- Multiple orphan tasks exist (e.g., weekly inbox triage)
- Multiple tasks are related to same feature

**Main Flow:**
1. User views "Orphan Tasks" section with 8 orphan tasks
2. User hovers over orphan task cards → Checkboxes appear
3. User selects 3 tasks related to dashboard markdown rendering:
   - "Add syntax highlighting for code blocks"
   - "Support mermaid diagram rendering"
   - "Add copy-to-clipboard button for code blocks"
4. System shows **"Assign Selected (3)"** button at top of orphan section
5. User clicks **"Assign Selected (3)"**
6. System opens **Bulk Assignment Modal** showing:
   - List of 3 selected tasks (collapsed, titles visible)
   - Initiative hierarchy (same as single assignment)
   - Note: "All 3 tasks will be assigned to the same feature"
7. User expands **"Dashboard Enhancements"** initiative
8. User clicks **"Assign to Feature 1: Markdown Rendering"**
9. System updates all 3 task YAML files in sequence
10. System emits 3 `task.updated` WebSocket events
11. System shows success toast: **"3 tasks assigned to Markdown Rendering"**
12. Modal closes; all 3 tasks disappear from orphan section
13. All 3 tasks appear under **Dashboard Enhancements > Markdown Rendering** in portfolio

**Postconditions:**
- 3 task YAML files updated atomically
- Portfolio section shows 3 new tasks under correct feature
- Orphan task count badge decrements by 3

---

### Workflow 3: AI-Suggested Assignment (Accelerated)

**Actors:** Software Engineer

**Preconditions:**
- AI suggestion feature enabled (SHOULD-have requirement)
- Task metadata allows inference (e.g., keywords in title/description)

**Main Flow:**
1. User clicks **"Assign"** on orphan task: "Implement WebSocket reconnection logic"
2. System opens modal with **AI suggestion badge** at top:
   - **"🤖 Suggested: Dashboard Enhancements > Real-Time Updates (85% confidence)"**
3. User reviews suggestion context:
   - Task title contains "WebSocket" → matched with feature keywords
   - Task assigned to `frontend-freddy` → matched with feature agent pattern
4. User trusts suggestion and clicks **"✓ Use AI Suggestion"** quick button
5. System assigns task to suggested feature (skips manual navigation)
6. System updates YAML, emits WebSocket event, shows success toast
7. Modal closes; task appears in correct portfolio section

**Postconditions:**
- Task assigned in 2 clicks (vs 4+ clicks for manual selection)
- User learns AI suggestion patterns (improves future confidence)

**Alternative Flows:**

**A1: User Rejects AI Suggestion**
- At step 4, user clicks **"✗ Choose Manually"**
- System collapses AI suggestion; shows full initiative hierarchy
- User proceeds with standard assignment flow (Workflow 1)

---

## Acceptance Criteria (Given/When/Then)

### AC1: Assign Orphan Task to Feature via Modal

**Given** I have an orphan task "Implement rate limiting for API endpoints" in the orphan section  
**And** I have a specification "specifications/llm-service/api-hardening.md" with feature "Rate Limiting"  
**When** I click the "Assign" button on the orphan task  
**And** I expand the "API Hardening" initiative in the modal  
**And** I click "Assign to Rate Limiting" button  
**Then** the task YAML file is updated with:
```yaml
specification: specifications/llm-service/api-hardening.md
feature: "Rate Limiting"
```
**And** the task disappears from the orphan section within 500ms  
**And** the task appears under "API Hardening > Rate Limiting" in the portfolio  
**And** all other connected dashboard clients see the updated portfolio

---

### AC2: Prevent Assignment of In-Progress Tasks

**Given** I have an orphan task with `status: in_progress`  
**When** I view the orphan task card in the dashboard  
**Then** the "Assign" button is disabled (grayed out)  
**And** hovering over the button shows tooltip: "Cannot assign tasks that are currently being worked on"  
**And** clicking the button has no effect (modal does not open)

---

### AC3: Display Initiative → Feature Hierarchy in Modal

**Given** I have two specifications:
  - "specifications/llm-dashboard/markdown-rendering.md" with 3 features
  - "specifications/llm-service/telemetry.md" with 2 features  
**When** I click "Assign" on an orphan task  
**Then** the modal displays:
  - **Dashboard Enhancements** (collapsed, arrow icon)
    - (Hidden until expanded)
  - **LLM Service Telemetry** (collapsed, arrow icon)
    - (Hidden until expanded)  
**When** I click the "Dashboard Enhancements" header  
**Then** the section expands to show:
  - Feature 1: Core Markdown Parser
  - Feature 2: Selective Field Rendering
  - Feature 3: Security Hardening  
**And** each feature has an "Assign to..." button

---

### AC4: Validate Specification File Existence

**Given** I have an orphan task  
**And** I click "Assign" and select "Dashboard Enhancements > Priority Editing"  
**And** the specification file "specifications/llm-dashboard/task-priority-editing.md" does not exist (deleted or moved)  
**When** I confirm the assignment  
**Then** the system shows error message: "Specification file not found. The file may have been moved or deleted. Please refresh and try again."  
**And** the modal remains open (assignment cancelled)  
**And** the task remains in the orphan section

---

### AC5: Preserve YAML Comments During Assignment

**Given** I have an orphan task YAML file with inline comments:
```yaml
id: 2026-02-06T1430-implement-caching
title: Implement Redis caching layer
agent: backend-dev
priority: HIGH  # Critical for performance milestone
status: inbox
# TODO: Consider memcached as alternative
```
**When** I assign the task to a specification  
**Then** the updated YAML file contains:
```yaml
id: 2026-02-06T1430-implement-caching
title: Implement Redis caching layer
agent: backend-dev
priority: HIGH  # Critical for performance milestone
status: inbox
specification: specifications/llm-service/caching.md
feature: "Redis Integration"
# TODO: Consider memcached as alternative
```
**And** all comments are preserved verbatim  
**And** field order is unchanged (new fields appended logically)

---

### AC6: Real-Time Synchronization via WebSocket

**Given** I have two browser windows open with the dashboard  
**And** both show the same orphan task "Add documentation for CLI flags"  
**When** I assign the task to a feature in Window A  
**Then** within 500ms, Window B receives a `task.updated` WebSocket event  
**And** Window B's orphan section updates to remove the task  
**And** Window B's portfolio section updates to show the task under the assigned feature  
**And** no manual page refresh is required

---

### AC7: Search/Filter Initiatives by Name

**Given** I have 15 initiatives in the system  
**And** I open the assignment modal  
**When** I type "dashboard" into the search box  
**Then** the initiative list filters to show only:
  - "Dashboard Enhancements"
  - "Dashboard Docsite Integration"  
**And** all other initiatives are hidden  
**And** features under visible initiatives remain accessible  
**When** I clear the search box  
**Then** all 15 initiatives reappear

---

### AC8: Display Task Context in Assignment Modal

**Given** I have an orphan task with:
  - Title: "Implement authentication middleware"
  - Description: "Add JWT-based authentication to protect admin endpoints. Must support token refresh and role-based access control."
  - Agent: backend-dev
  - Priority: HIGH  
**When** I click "Assign" on the task  
**Then** the modal displays at the top:
  - **Task Title:** "Implement authentication middleware"
  - **Description:** "Add JWT-based authentication to protect admin endpoints. Must support..." (truncated to 200 chars with "..." if longer)
  - **Agent:** backend-dev (with agent icon/badge)
  - **Priority:** HIGH (with color-coded badge)

---

### AC9: Handle Specifications Without Features Gracefully

**Given** I have a specification "specifications/architecture/system-overview.md" with no `features:` field in frontmatter  
**When** I open the assignment modal  
**Then** the "System Overview" initiative appears in the list  
**When** I expand "System Overview"  
**Then** the section shows:
  - **"Assign to System Overview (Root)"** button  
  - No sub-features listed  
**When** I click "Assign to System Overview (Root)"  
**Then** the task YAML is updated with:
```yaml
specification: specifications/architecture/system-overview.md
# No feature: field added (specification-level assignment)
```

---

### AC10: Bulk Assignment of Multiple Tasks

**Given** I have 4 orphan tasks in the orphan section  
**When** I hover over orphan task cards  
**Then** checkboxes appear in the top-right corner of each card  
**When** I select 3 tasks (checkbox checked)  
**Then** a "Assign Selected (3)" button appears at the top of the orphan section  
**When** I click "Assign Selected (3)"  
**Then** the bulk assignment modal opens showing:
  - "Assigning 3 tasks:" followed by collapsed task titles
  - Initiative hierarchy (same as single assignment)
  - Note: "All selected tasks will be assigned to the same feature"  
**When** I select a feature and confirm  
**Then** all 3 task YAML files are updated with the same `specification:` and `feature:` fields  
**And** all 3 tasks disappear from orphan section  
**And** all 3 tasks appear under the selected feature in portfolio

---

## Data Model

### Task YAML Schema Extension

**Before Assignment (Orphan Task):**
```yaml
id: 2026-02-06T1430-implement-rate-limiting
title: Implement rate limiting for API endpoints
agent: backend-dev
priority: HIGH
status: inbox
description: |
  Add rate limiting middleware to prevent API abuse.
  Target: 100 requests/minute per IP.
```

**After Assignment (Linked Task):**
```yaml
id: 2026-02-06T1430-implement-rate-limiting
title: Implement rate limiting for API endpoints
agent: backend-dev
priority: HIGH
status: inbox
specification: specifications/llm-service/api-hardening.md
feature: "Rate Limiting"
description: |
  Add rate limiting middleware to prevent API abuse.
  Target: 100 requests/minute per IP.
```

**New Fields:**
- `specification` (string, required): Relative path from repository root to specification markdown file
- `feature` (string, optional): Feature name as defined in specification frontmatter; omitted if assigned to specification root

---

### Specification Frontmatter Schema (Reference)

**Example: specifications/llm-service/api-hardening.md**
```yaml
---
id: SPEC-LLM-003
title: API Hardening
initiative: llm-service-security
priority: HIGH
status: active
features:
  - name: "Rate Limiting"
    description: "Prevent API abuse via request throttling"
    priority: HIGH
  - name: "Input Validation"
    description: "Sanitize and validate all API inputs"
    priority: CRITICAL
  - name: "Authentication Middleware"
    description: "JWT-based authentication for protected endpoints"
    priority: HIGH
---
```

**Parsed Structure for Modal:**
```
Initiative: API Hardening
  ├─ Feature 1: Rate Limiting
  ├─ Feature 2: Input Validation
  └─ Feature 3: Authentication Middleware
```

---

## API Specification

### Endpoint: PATCH /api/tasks/:task_id/assignment

**Purpose:** Assign an orphan task to a specification and feature

**Request:**
```http
PATCH /api/tasks/2026-02-06T1430-implement-rate-limiting/assignment HTTP/1.1
Content-Type: application/json

{
  "specification": "specifications/llm-service/api-hardening.md",
  "feature": "Rate Limiting"
}
```

**Response 200 (Success):**
```json
{
  "success": true,
  "task": {
    "id": "2026-02-06T1430-implement-rate-limiting",
    "title": "Implement rate limiting for API endpoints",
    "specification": "specifications/llm-service/api-hardening.md",
    "feature": "Rate Limiting",
    "status": "inbox",
    "updated_at": "2026-02-06T15:30:45Z"
  }
}
```

**Response 400 (Bad Request - Invalid Specification):**
```json
{
  "error": "Specification file not found",
  "detail": "The file 'specifications/llm-service/api-hardening.md' does not exist",
  "code": "SPEC_NOT_FOUND"
}
```

**Response 404 (Task Not Found):**
```json
{
  "error": "Task not found",
  "detail": "No task with ID '2026-02-06T1430-invalid-task'",
  "code": "TASK_NOT_FOUND"
}
```

**Response 409 (Conflict - Task In Progress):**
```json
{
  "error": "Cannot assign in-progress task",
  "detail": "Task '2026-02-06T1200-active-task' has status 'in_progress' and cannot be modified",
  "code": "TASK_LOCKED"
}
```

**Response 409 (Conflict - Concurrent Modification):**
```json
{
  "error": "Task was modified by another user",
  "detail": "The task file was updated since you opened the assignment modal. Please refresh and try again.",
  "code": "OPTIMISTIC_LOCK_FAILURE",
  "last_modified": "2026-02-06T15:29:30Z"
}
```

---

### Endpoint: GET /api/initiatives (New)

**Purpose:** Retrieve initiative hierarchy for assignment modal

**Request:**
```http
GET /api/initiatives HTTP/1.1
```

**Response 200:**
```json
{
  "initiatives": [
    {
      "id": "dashboard-enhancements",
      "title": "Dashboard Enhancements",
      "specification": "specifications/llm-dashboard/markdown-rendering.md",
      "features": [
        {
          "name": "Core Markdown Parser",
          "description": "Parse markdown with GFM support",
          "priority": "HIGH"
        },
        {
          "name": "Selective Field Rendering",
          "description": "Render specific fields as markdown",
          "priority": "MEDIUM"
        }
      ]
    },
    {
      "id": "llm-service-security",
      "title": "API Hardening",
      "specification": "specifications/llm-service/api-hardening.md",
      "features": [
        {
          "name": "Rate Limiting",
          "priority": "HIGH"
        }
      ]
    }
  ],
  "count": 2,
  "cached": true,
  "cache_expires_at": "2026-02-06T15:35:00Z"
}
```

**Response 200 (Partial Success with Errors):**
```json
{
  "initiatives": [
    {
      "id": "dashboard-enhancements",
      "title": "Dashboard Enhancements",
      "specification": "specifications/llm-dashboard/markdown-rendering.md",
      "features": [...]
    }
  ],
  "count": 1,
  "errors": [
    {
      "specification": "specifications/invalid-spec.md",
      "error": "YAML parsing failed: invalid frontmatter"
    }
  ]
}
```

---

### WebSocket Event: task.assigned

**Emitted When:** Task is successfully assigned to a specification/feature

**Payload:**
```json
{
  "event": "task.assigned",
  "task_id": "2026-02-06T1430-implement-rate-limiting",
  "specification": "specifications/llm-service/api-hardening.md",
  "feature": "Rate Limiting",
  "timestamp": "2026-02-06T15:30:45Z"
}
```

**Client Behavior:**
- Remove task from orphan section
- Refresh portfolio hierarchy to show task under correct feature
- Show toast notification: "Task assigned to [Feature Name]"

---

## UI/UX Design Notes

### Assignment Modal Layout

```
┌─────────────────────────────────────────────────────────┐
│  Assign Task to Feature                             [×] │
├─────────────────────────────────────────────────────────┤
│  📋 Task: Implement rate limiting for API endpoints     │
│  👤 Agent: backend-dev  ⬆️ Priority: HIGH               │
│                                                         │
│  🔍 Search initiatives and features...                  │
│  ┌───────────────────────────────────────────────────┐ │
│  │                                                   │ │
│  │  ▶ Dashboard Enhancements           [3 features] │ │
│  │  ▼ LLM Service Security             [2 features] │ │
│  │    ├─ Rate Limiting        [Assign to Feature ➔] │ │
│  │    └─ Input Validation     [Assign to Feature ➔] │ │
│  │  ▶ Documentation Updates            [4 features] │ │
│  │                                                   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│                             [Cancel]  [Assign to Root] │
└─────────────────────────────────────────────────────────┘
```

**Design Principles:**
- **Task context at top:** Users see what they're assigning (no mental juggling)
- **Search-first:** Large lists need instant filtering (avoid scroll fatigue)
- **Expand/collapse:** Progressive disclosure (don't overwhelm with all features at once)
- **One-click assign:** Each feature has direct "Assign" button (no extra confirmation step)
- **Keyboard navigation:** Tab/Enter/Escape work as expected (accessibility baseline)

---

### Orphan Task Card (Before Assignment)

```
┌──────────────────────────────────────────────┐
│  ☐ (checkbox for bulk selection)            │
│  📋 Implement rate limiting for API          │
│  👤 backend-dev  ⬆️ HIGH  📅 2026-02-06      │
│  "Add rate limiting middleware to..."        │
│                                              │
│  [📎 Assign to Specification]  [👁️ View]   │
└──────────────────────────────────────────────┘
```

**Interactive States:**
- **Hover:** Checkbox fades in; card border glows
- **In-Progress Task:** "Assign" button disabled; lock icon shown; tooltip explains
- **Selected (bulk):** Blue border; checkbox checked; "Assign Selected (N)" button appears above section

---

### Bulk Assignment Flow

```
Step 1: Select Multiple Tasks
┌──────────────────────────────────────────────┐
│ Orphan Tasks (5)      [Assign Selected (3)] │
├──────────────────────────────────────────────┤
│ ☑ Task A - Implement caching                │
│ ☐ Task B - Add logging                      │
│ ☑ Task C - Refactor database layer          │
│ ☐ Task D - Update documentation             │
│ ☑ Task E - Fix memory leak                  │
└──────────────────────────────────────────────┘

Step 2: Bulk Assignment Modal
┌─────────────────────────────────────────────────────────┐
│  Assign 3 Tasks to Feature                          [×] │
├─────────────────────────────────────────────────────────┤
│  Selected Tasks (click to expand):                      │
│  ▶ Task A - Implement caching                           │
│  ▶ Task C - Refactor database layer                     │
│  ▶ Task E - Fix memory leak                             │
│                                                         │
│  ⚠️ All tasks will be assigned to the same feature     │
│                                                         │
│  🔍 Search initiatives...                               │
│  ▼ LLM Service Performance                              │
│    ├─ Caching Layer        [Assign All 3 Tasks ➔]      │
│    └─ Database Optimization [Assign All 3 Tasks ➔]     │
│                                                         │
│                             [Cancel]  [Back to Select] │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Notes

### Backend Implementation Strategy

**Files to Create:**
1. `src/llm_service/dashboard/task_assignment_handler.py`
   - `assign_task_to_feature(task_id, specification, feature)` function
   - YAML file writing (reuse `task_priority_updater.py` patterns)
   - Specification validation
   - Optimistic locking checks

2. `src/llm_service/dashboard/spec_registry.py`
   - Parse all specification frontmatter on startup
   - Cache parsed feature lists
   - Invalidate cache on file watcher events
   - `get_all_initiatives()` function for API endpoint

**Files to Modify:**
1. `src/llm_service/dashboard/app.py`
   - Add `PATCH /api/tasks/:task_id/assignment` endpoint
   - Add `GET /api/initiatives` endpoint (may reuse/extend existing portfolio endpoint)
   - Add `task.assigned` WebSocket event emission

2. `src/llm_service/dashboard/file_watcher.py`
   - Add specification file change detection
   - Invalidate `spec_registry` cache on spec file modification

**Dependencies:**
- `ruamel.yaml` (already in use for priority editing)
- No new dependencies required

---

### Frontend Implementation Strategy

**Files to Create:**
1. `src/llm_service/dashboard/static/assignment-modal.js`
   - Modal lifecycle management (open, close, escape key)
   - Initiative tree rendering (expand/collapse)
   - Search/filter logic (client-side)
   - API integration (`PATCH /api/tasks/:id/assignment`)
   - Bulk assignment state management

**Files to Modify:**
1. `src/llm_service/dashboard/static/dashboard.js`
   - Add "Assign" button to orphan task cards
   - Add checkbox logic for bulk selection
   - Add `showAssignmentModal(taskId)` function
   - Add `assignTask(taskId, specification, feature)` API call
   - Add WebSocket handler for `task.assigned` event

2. `src/llm_service/dashboard/static/dashboard.css`
   - Modal styling (overlay, content, responsive)
   - Initiative tree styling (expand arrows, indentation)
   - Search box styling
   - Bulk selection checkbox styling
   - Loading/success/error state animations

3. `src/llm_service/dashboard/static/index.html`
   - Add modal container (hidden by default)
   - Add "Assign Selected" button container (hidden until tasks selected)

**Dependencies:**
- No new JS libraries required (vanilla JS)
- Reuse existing modal patterns from task detail modal

---

### Testing Strategy

**Unit Tests (Backend):**
- `test_task_assignment_handler.py`:
  - `test_assign_task_updates_yaml_file()`
  - `test_assign_task_preserves_comments()`
  - `test_assign_task_validates_specification_exists()`
  - `test_assign_task_rejects_in_progress_tasks()`
  - `test_assign_task_handles_concurrent_modification()`
  - `test_assign_task_handles_missing_feature_gracefully()`

- `test_spec_registry.py`:
  - `test_parse_specification_frontmatter()`
  - `test_cache_invalidation_on_file_change()`
  - `test_handle_malformed_specification_gracefully()`
  - `test_get_all_initiatives_returns_sorted_list()`

**Integration Tests:**
- `test_assignment_api.py`:
  - `test_patch_assignment_endpoint_success()`
  - `test_patch_assignment_endpoint_invalid_spec_returns_400()`
  - `test_patch_assignment_endpoint_task_not_found_returns_404()`
  - `test_patch_assignment_endpoint_in_progress_task_returns_409()`
  - `test_get_initiatives_endpoint_returns_hierarchy()`

**Functional Tests:**
- `test_assignment_acceptance.py`:
  - `test_orphan_task_assigned_to_feature_appears_in_portfolio()`
  - `test_orphan_task_assignment_emits_websocket_event()`
  - `test_bulk_assignment_updates_multiple_tasks()`

**Manual Tests:**
- `tests/manual/dashboard-assignment-test-cases.md`:
  - Modal keyboard navigation (Tab, Enter, Escape)
  - Search/filter performance (50+ initiatives)
  - Mobile responsive layout
  - WebSocket real-time sync (multi-browser)
  - Bulk assignment UX flow

**Coverage Target:** >80% for backend code, manual coverage for frontend (no JS test framework)

---

## Security Considerations

### Path Traversal Prevention

**Attack Vector:**
```http
PATCH /api/tasks/valid-task-id/assignment
{
  "specification": "../../etc/passwd"
}
```

**Mitigation:**
1. Validate specification path matches pattern: `^specifications/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+\.md$`
2. Resolve absolute path and verify it starts with `<repo_root>/specifications/`
3. Verify file exists within specifications directory before assignment
4. Reject any path containing `..` or absolute paths (`/`)

**Implementation:**
```python
def validate_specification_path(spec_path: str) -> bool:
    import re
    from pathlib import Path
    
    # Pattern check
    if not re.match(r'^specifications/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+\.md$', spec_path):
        return False
    
    # Resolve to absolute and verify within repo
    repo_root = Path(__file__).parent.parent.parent
    spec_abs = (repo_root / spec_path).resolve()
    specs_dir = (repo_root / "specifications").resolve()
    
    if not str(spec_abs).startswith(str(specs_dir)):
        return False
    
    if not spec_abs.exists():
        return False
    
    return True
```

---

### Cross-Site Scripting (XSS) Prevention

**Attack Vector:**
- Task title/description contains malicious HTML/JavaScript
- Assignment modal renders unsanitized task data

**Mitigation:**
1. Reuse DOMPurify sanitization from markdown rendering feature (ADR-036)
2. Use `.textContent` instead of `.innerHTML` for plain-text fields
3. Enforce CSP headers (already in place)

**Implementation:**
```javascript
// SAFE: Renders task title as plain text
modalTitle.textContent = task.title;

// SAFE: Renders task description as sanitized markdown
modalDescription.innerHTML = DOMPurify.sanitize(marked.parse(task.description));
```

---

### Optimistic Locking for Concurrent Writes

**Race Condition:**
1. User A opens assignment modal (reads task YAML)
2. User B assigns task to Feature X (writes task YAML)
3. User A assigns same task to Feature Y (overwrites User B's change)
4. Result: User B's assignment lost (silent data loss)

**Mitigation:**
1. Track `last_modified` timestamp in API response
2. Include `last_modified` in PATCH request
3. Backend verifies file timestamp matches before writing
4. If mismatch, return 409 Conflict with latest data
5. Frontend prompts user to refresh and retry

**Implementation:**
```http
PATCH /api/tasks/:task_id/assignment
{
  "specification": "...",
  "feature": "...",
  "last_modified": "2026-02-06T15:29:00Z"  # Timestamp from modal open
}

# Backend pseudo-code
file_mtime = os.path.getmtime(task_file_path)
request_mtime = parse_iso8601(request.json['last_modified'])

if file_mtime > request_mtime:
    return 409, {"error": "Task was modified by another user"}
```

---

## Open Questions & Risks

### Open Questions (Require Decision)

**Q1:** Should feature assignment be mandatory or optional?
- **Option A:** Require feature selection (enforce structure)
- **Option B:** Allow specification-level assignment (more flexibility)
- **Recommendation:** Option B with UI nudge toward feature selection ("Assign to Root" button less prominent)

**Q2:** Should we support task reassignment (moving between features)?
- **Scope:** Currently out-of-scope (FR-W1)
- **Decision:** Defer to v2; manual YAML editing for now
- **Risk:** Users may expect reassignment as natural extension of assignment feature

**Q3:** How to handle orphan tasks with invalid `specification:` field (malformed path)?
- **Option A:** Treat as orphan (ignore invalid path)
- **Option B:** Show warning badge "⚠️ Invalid Spec" but don't allow assignment until fixed
- **Recommendation:** Option A (auto-heal by re-assigning)

**Q4:** Should AI suggestions use LLM API or local heuristics?
- **Option A:** LLM API call (more accurate, higher cost, latency)
- **Option B:** Keyword matching + agent patterns (fast, free, less accurate)
- **Recommendation:** Option B for MVP; LLM integration in v2 if user feedback positive

---

### Risks & Mitigations

**R1: Specification Frontmatter Schema Drift**
- **Risk:** Specifications may not follow consistent `features:` schema
- **Impact:** Modal shows inconsistent or missing feature lists
- **Mitigation:** 
  - Document frontmatter schema in specification template
  - Graceful degradation: Show "Assign to Root" if features missing
  - Validation script: `ops/scripts/validate-spec-frontmatter.py` (future)

**R2: Performance Degradation with 100+ Specifications**
- **Risk:** Parsing 100+ spec files on every modal open causes UI lag
- **Impact:** Assignment modal takes >2s to load (frustrates users)
- **Mitigation:**
  - Cache parsed frontmatter in memory (invalidate on file change)
  - Lazy-load features (expand initiative → fetch features on demand)
  - Target: <500ms modal load for 50 specs, <1s for 100 specs

**R3: User Confusion Between Assignment and Task Editing**
- **Risk:** Users expect assignment modal to allow editing other task fields
- **Impact:** Feature requests for "Edit task while assigning" (scope creep)
- **Mitigation:**
  - Clear modal title: "Assign Task to Feature" (not "Edit Task")
  - Separate "Edit Task" button in orphan card (distinct from "Assign")
  - Tooltip: "To edit task details, click 'View' then 'Edit'"

**R4: Bulk Assignment Errors Leave Partial State**
- **Risk:** Bulk assign 5 tasks → 3 succeed, 2 fail → inconsistent state
- **Impact:** User unsure which tasks were assigned; must verify manually
- **Mitigation:**
  - Transactional batch operation: All-or-nothing semantics
  - If any task fails, rollback all assignments
  - Show detailed error: "Bulk assignment failed: Task C invalid spec. No tasks were assigned."

---

## Future Enhancements (Post-MVP)

### v2.0 Features (Deferred)

**FE1:** Task Reassignment Between Features
- Move task from Feature A to Feature B via drag-and-drop or "Reassign" button
- Update `specification:` and `feature:` fields in YAML
- Estimated effort: 4-6 hours

**FE2:** AI-Powered Assignment Recommendations (LLM-based)
- Send task title/description to LLM
- Return suggested feature with confidence score
- Estimated effort: 8-12 hours (includes LLM service integration)

**FE3:** Inline Feature Creation During Assignment
- "+ Create New Feature" button in modal
- Inline form: Feature name, description, priority
- Updates specification frontmatter + assigns task
- Estimated effort: 10-15 hours (includes spec file modification)

**FE4:** Assignment History and Undo
- Track last 10 assignments in local storage
- "Undo Last Assignment" button (30-second window)
- Visual timeline: "Task X assigned to Feature Y at 3:45 PM"
- Estimated effort: 5-7 hours

**FE5:** Drag-and-Drop Assignment
- Drag orphan task card → Drop on initiative/feature in portfolio
- Visual feedback: Drop zones highlight on drag start
- Accessibility challenge: Keyboard-only alternative required
- Estimated effort: 12-18 hours

---

## Success Metrics

### Quantitative Metrics (Track Post-Launch)

**M1:** Assignment Modal Load Time
- **Target:** <500ms P95
- **Measurement:** Browser performance.now() from button click to modal render

**M2:** Average Time to Assign Task
- **Target:** <15 seconds (from click "Assign" to task appears in portfolio)
- **Measurement:** Telemetry tracking (click timestamp → API response timestamp)

**M3:** Orphan Task Reduction Rate
- **Target:** 80% of orphan tasks assigned within 48 hours of creation
- **Measurement:** Daily snapshot of orphan task count; trend analysis

**M4:** Feature Usage Adoption
- **Target:** 70% of task assignments use assignment modal (vs manual YAML editing)
- **Measurement:** API endpoint hit count vs Git commit count with manual spec changes

**M5:** Error Rate
- **Target:** <2% of assignment attempts result in 4xx/5xx errors
- **Measurement:** API endpoint error responses / total requests

### Qualitative Metrics (User Feedback)

**M6:** User Satisfaction
- **Target:** 4.5/5 stars on "How easy was it to assign tasks?" survey
- **Measurement:** In-app survey after 5 assignment operations

**M7:** Feature Discoverability
- **Target:** 90% of users discover assignment feature within first session
- **Measurement:** Telemetry: Users who click "Assign" button / total unique users

**M8:** Perceived Performance
- **Target:** Users report modal feels "instant" (qualitative feedback)
- **Measurement:** User interviews; free-text feedback analysis

---

## Appendix

### Glossary

- **Orphan Task:** Task YAML file without `specification:` field, or with invalid specification path
- **Initiative:** Top-level project grouping (e.g., "Dashboard Enhancements"); corresponds to specification file
- **Feature:** Sub-component of initiative (e.g., "Markdown Rendering"); defined in specification frontmatter
- **Specification:** Markdown file in `specifications/` directory with YAML frontmatter defining initiative/features
- **Assignment:** Act of linking orphan task to specification and (optionally) feature via UI
- **Bulk Assignment:** Assigning multiple orphan tasks to the same feature in single operation
- **Feature-Level Assignment:** Linking task to specific feature within initiative (vs specification-level)

---

### Related Documentation

- **ADR-037:** [Dashboard Initiative Tracking](../../docs/architecture/adrs/ADR-037-dashboard-initiative-tracking.md) - Parent feature
- **ADR-035:** [Task Priority Editing](../../docs/architecture/adrs/ADR-035-dashboard-task-priority-editing.md) - YAML writing patterns
- **ADR-036:** [Markdown Rendering](../../docs/architecture/adrs/ADR-036-dashboard-markdown-rendering.md) - Security patterns (XSS prevention)
- **Directive 034:** [Specification-Driven Development](../../.github/agents/directives/034_specification_driven_development.md) - Spec frontmatter standards
- **Directive 019:** [File-Based Collaboration](../../.github/agents/directives/019_file_based_collaboration.md) - YAML file orchestration

---

### Revision History

| Version | Date       | Author         | Changes                          |
|---------|------------|----------------|----------------------------------|
| 1.0     | 2026-02-06 | Analyst Annie  | Initial draft (Option 2: Feature-Level Assignment) |

---

**End of Specification**
