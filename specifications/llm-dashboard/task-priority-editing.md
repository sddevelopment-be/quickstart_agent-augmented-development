# Specification: Dashboard Task Priority Editing

**Status:** Draft  
**Created:** 2026-02-06  
**Last Updated:** 2026-02-06  
**Author:** Analyst Annie  
**Stakeholders:** Human-in-Charge, Software Engineers, Agentic Framework Core Team

---

## User Story

**As a** Software Engineer managing multi-agent workflows  
**I want** to change task priority directly from the dashboard UI  
**So that** I can reprioritize work in real-time without manually editing YAML files

**Alternative: Acceptance Criterion Format**  
**Given** I am viewing tasks in the dashboard  
**When** I click a task priority indicator and select a new priority level  
**Then** the YAML file is updated immediately and all connected clients see the change  
**Unless** the file is locked or the dashboard has insufficient write permissions

**Target Personas:**
- Software Engineer (Primary) - Needs rapid workflow adjustment without CLI context switching
- Agentic Framework Core Team (Primary) - Needs efficient task management during orchestration cycles
- Project Manager (Secondary) - Needs visibility and control over task prioritization

---

## Overview

Task priority editing enables users to modify task priority directly from the dashboard UI without switching contexts to a text editor or CLI. This solves the "friction problem" where developers must interrupt their dashboard monitoring session to manually edit YAML files when priorities change.

**Context:**
- **Problem Solved:** Context switching friction—users leave dashboard → open editor → find YAML → edit → save → return to dashboard
- **Why Needed Now:** Dashboard is primary monitoring interface (ADR-032); task reprioritization is frequent during active development
- **Constraints:**
  - MUST preserve YAML file format and comments
  - MUST respect file-based orchestration (no database-only state)
  - MUST validate priority values against task schema
  - MUST handle concurrent file access gracefully

**Related Documentation:**
- Related ADRs: [ADR-032: Real-Time Execution Dashboard](../../docs/architecture/adrs/ADR-032-real-time-execution-dashboard.md)
- Related Specifications: [Real-Time Execution Dashboard](real-time-execution-dashboard.md)
- Background:
  - [File-Based Orchestration Approach](../../.github/agents/approaches/work-directory-orchestration.md)
  - [Task YAML Schema](../../work/collaboration/inbox/INDEX.md)

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** System MUST allow users to change task priority from dashboard UI
- **Rationale:** Core feature purpose—enable priority editing without leaving dashboard
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** Click priority dropdown → Select new value → YAML file updated within 500ms

**FR-M2:** System MUST update the YAML file with new priority value
- **Rationale:** Preserve file-based orchestration—YAML remains source of truth
- **Personas Affected:** All personas (Git audit trail integrity)
- **Success Criteria:** `priority:` field in YAML file matches UI selection after save

**FR-M3:** System MUST support all priority values defined in task schema
- **Rationale:** Allow full range of prioritization per existing standards
- **Personas Affected:** Software Engineer, Project Manager
- **Success Criteria:** UI displays: CRITICAL, HIGH, MEDIUM, LOW, normal (case-insensitive mapping)

**FR-M4:** System MUST emit WebSocket event after priority change
- **Rationale:** Real-time synchronization—all connected clients see change immediately
- **Personas Affected:** Software Engineer (multi-browser scenarios), Agentic Framework Core Team
- **Success Criteria:** `task.updated` event emitted with new priority within 100ms of file write

**FR-M5:** System MUST validate priority value before saving
- **Rationale:** Prevent invalid YAML files that break orchestration
- **Personas Affected:** All personas (data integrity)
- **Success Criteria:** Invalid priority values rejected with user-facing error message

**FR-M6:** System MUST preserve YAML file structure and comments
- **Rationale:** Manual editing coexists with dashboard editing—don't lose user annotations
- **Personas Affected:** Software Engineer (hand-edits YAML for complex changes)
- **Success Criteria:** Comments, blank lines, and field order preserved after priority change

**FR-M7:** System MUST handle concurrent file access gracefully
- **Rationale:** Multiple users or agents may edit same file simultaneously
- **Personas Affected:** Agentic Framework Core Team (multi-agent scenarios)
- **Success Criteria:** Last-write-wins with notification, or optimistic locking with retry prompt

**FR-M8:** System MUST prevent priority changes for tasks that are actively in progress
- **Rationale:** Changing priority mid-execution could disrupt agent workflow and cause confusion
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** Priority dropdown disabled for tasks with `status: in_progress` or similar active states

**FR-M9:** System MUST display visual indicator for tasks actively being worked on
- **Rationale:** Users need to see which tasks agents are currently executing
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** Active tasks show animated indicator (e.g., pulsing dot, "In Progress" badge) distinct from pending/done states

### SHOULD Have (Important - Feature degraded without these)

**FR-S1:** System SHOULD indicate which tasks are editable vs. read-only
- **Rationale:** Read-only tasks (completed or in-progress) shouldn't show editable controls
- **Personas Affected:** Software Engineer
- **Success Criteria:** Priority dropdown disabled and grayed out for completed and in-progress tasks; tooltip explains why
- **Workaround if omitted:** All tasks show edit control; errors on save for read-only files

**FR-S2:** System SHOULD show visual feedback during save
- **Rationale:** User confirmation that action succeeded
- **Personas Affected:** Software Engineer
- **Success Criteria:** Spinner icon or toast notification "Priority updated to HIGH"
- **Workaround if omitted:** User uncertain if change persisted

**FR-S3:** System SHOULD support keyboard navigation for priority changes
- **Rationale:** Accessibility and power-user efficiency
- **Personas Affected:** Software Engineer (keyboard-first workflows)
- **Success Criteria:** Tab to priority → Arrow keys to select → Enter to save
- **Workaround if omitted:** Mouse-only interaction

**FR-S4:** System SHOULD log priority changes to activity log
- **Rationale:** Audit trail for understanding why tasks were reprioritized
- **Personas Affected:** Project Manager, Agentic Framework Core Team
- **Success Criteria:** Activity log entry: "Task X priority changed from MEDIUM to HIGH by user@example.com"
- **Workaround if omitted:** Rely on Git history (less user-friendly)

### COULD Have (Nice to have - Enhances experience)

**FR-C1:** System COULD support bulk priority changes
- **Rationale:** Efficiency when reprioritizing multiple tasks
- **Personas Affected:** Project Manager, Software Engineer
- **Success Criteria:** Select multiple tasks → "Set Priority" → Apply to all
- **If omitted:** Users change tasks one by one (tedious for large batches)

**FR-C2:** System COULD show priority change history in task detail modal
- **Rationale:** Understanding task lifecycle and decision rationale
- **Personas Affected:** Project Manager
- **Success Criteria:** "Priority History" section shows: "2026-02-06 10:00 - Changed HIGH → CRITICAL by user@example.com"
- **If omitted:** Manual Git log inspection required

**FR-C3:** System COULD support drag-and-drop priority ranking
- **Rationale:** Intuitive visual prioritization
- **Personas Affected:** Project Manager
- **Success Criteria:** Drag task to top of inbox → Auto-set to CRITICAL
- **If omitted:** Manual dropdown selection per task

**FR-C4:** System COULD suggest priority based on task metadata
- **Rationale:** AI-assisted prioritization
- **Personas Affected:** Project Manager
- **Success Criteria:** Badge: "Suggested: HIGH (due to milestone deadline)"
- **If omitted:** Manual prioritization only

### WON'T Have (Explicitly out of scope)

**FR-W1:** System will NOT support custom priority levels beyond schema
- **Rationale:** YAML schema standardization across framework
- **Future Consideration:** ADR required to extend priority enum

**FR-W2:** System will NOT support priority presets or templates
- **Rationale:** Simple feature first; templates add complexity
- **Future Consideration:** Could add "Urgent Batch" preset in future

**FR-W3:** System will NOT implement approval workflow for priority changes
- **Rationale:** Single-user tool currently; approval adds governance complexity
- **Future Consideration:** Multi-user deployments may need this

---

## Scenarios and Behavior

### Scenario 1: Happy Path - Change Task Priority

**Given** I am viewing the dashboard with tasks displayed  
**And** Task "Implement Telemetry Database" has priority "MEDIUM"  
**When** I click the priority dropdown for that task  
**And** Select "HIGH" from the dropdown  
**Then** The YAML file `work/collaboration/inbox/2026-02-06-telemetry-db.yaml` is updated with `priority: HIGH`  
**And** A `task.updated` WebSocket event is emitted  
**And** All connected dashboard clients show the task with priority "HIGH"  
**And** A toast notification appears: "Priority updated to HIGH"

### Scenario 2: Validation Error - Invalid Priority

**Given** I am viewing the dashboard  
**When** I somehow submit an invalid priority value "SUPER-URGENT" (edge case: browser dev tools)  
**Then** The system rejects the change with error: "Invalid priority. Must be one of: CRITICAL, HIGH, MEDIUM, LOW, normal"  
**And** The YAML file is NOT modified  
**And** The UI shows an error toast  
**And** The task retains its original priority

### Scenario 3: Concurrent Edit Detection

**Given** I am viewing the dashboard  
**And** Another user or agent modifies the same task file  
**When** I attempt to change the task priority  
**Then** The system detects the file has changed since last read  
**And** Shows notification: "Task was modified by another user. Reload and try again?"  
**And** Provides "Reload" button to refresh task state  
**Or** (Alternative: Last-write-wins) My change overwrites previous change with warning

### Scenario 4: Read-Only Task (Completed)

**Given** I am viewing a task in the "Done" column  
**When** I view the task detail modal  
**Then** The priority field is displayed as read-only text (not a dropdown)  
**And** A tooltip explains: "Cannot edit completed tasks"

### Scenario 7: Read-Only Task (In Progress)

**Given** I am viewing a task with status "in_progress"  
**And** The task shows a pulsing "In Progress" indicator  
**When** I hover over the priority dropdown  
**Then** The dropdown is disabled (grayed out, not clickable)  
**And** A tooltip appears: "Cannot change priority while task is in progress"  
**When** The agent completes the task (status changes to "done")  
**Then** The "In Progress" indicator disappears  
**And** The priority dropdown remains disabled (now because task is completed)

### Scenario 8: Active Task Indicator

**Given** I am viewing the dashboard  
**When** An agent starts working on task "Implement Telemetry Database"  
**And** The task status changes from "pending" to "in_progress"  
**Then** The task card displays a pulsing blue dot indicator  
**And** A badge shows "In Progress" with agent name: "Backend-dev Benny"  
**And** The priority dropdown becomes disabled  
**When** I hover over the indicator  
**Then** A tooltip shows: "Started by backend-dev at 2026-02-06 11:30 UTC"

### Scenario 5: Keyboard Navigation

**Given** I am viewing the dashboard  
**When** I press Tab to focus on a task priority dropdown  
**And** Press Down Arrow twice to highlight "LOW"  
**And** Press Enter to confirm  
**Then** The task priority updates to "LOW"  
**And** Focus returns to the task card

### Scenario 6: Multi-Client Real-Time Sync

**Given** I have the dashboard open in Browser A  
**And** My colleague has the dashboard open in Browser B  
**When** I change task priority from MEDIUM to HIGH in Browser A  
**Then** Browser A shows "HIGH" immediately  
**And** Browser B receives `task.updated` WebSocket event within 100ms  
**And** Browser B updates the task display to show "HIGH"

---

## Data Model

### YAML File Format (Before)
```yaml
id: 2026-02-06T1500-backend-dev-telemetry-db
title: "Implement Telemetry Database"
agent: backend-dev
priority: MEDIUM  # <-- Field to modify
status: pending
created_at: "2026-02-06T15:00:00Z"
```

### YAML File Format (After)
```yaml
id: 2026-02-06T1500-backend-dev-telemetry-db
title: "Implement Telemetry Database"
agent: backend-dev
priority: HIGH  # <-- Updated value
status: pending
created_at: "2026-02-06T15:00:00Z"
```

### WebSocket Event
```json
{
  "event": "task.updated",
  "timestamp": "2026-02-06T11:30:00.000Z",
  "data": {
    "task_id": "2026-02-06T1500-backend-dev-telemetry-db",
    "field": "priority",
    "old_value": "MEDIUM",
    "new_value": "HIGH",
    "changed_by": "user@example.com"
  }
}
```

---

## Constraints and Edge Cases

### Technical Constraints

1. **YAML Parsing:** Must preserve comments and formatting (use YAML library with comment preservation)
2. **File Locking:** No OS-level file locks (Linux environments may not support); use application-level optimistic locking
3. **WebSocket Reliability:** Handle reconnections—queue priority changes if offline, sync on reconnect
4. **Performance:** YAML write operations must complete <200ms to maintain UI responsiveness

### Edge Cases

1. **Task File Deleted During Edit:** Handle gracefully—show error "Task no longer exists"
2. **Invalid YAML After Manual Edit:** Detect parse errors—show warning "Task file corrupted, cannot edit"
3. **Permission Denied:** Dashboard user lacks write permissions—show error with sudo instructions
4. **Very Long File Write (Network FS):** Show spinner beyond 500ms threshold, timeout after 5s

### Security Considerations

1. **Path Traversal:** Validate task file paths—reject `../../etc/passwd`
2. **YAML Injection:** Sanitize priority values—reject multiline or special characters
3. **XSS in Toast Messages:** Escape user-provided values in notifications

---

## UI/UX Specifications

### Priority Dropdown Component

**Visual States:**
- Default (Editable): Badge with current priority + dropdown chevron
- Hover (Editable): Highlight border, show tooltip "Click to change priority"
- Open: Dropdown menu with 5 options (CRITICAL, HIGH, MEDIUM, LOW, normal)
- Saving: Spinner icon, dropdown disabled
- Success: Green checkmark flash (500ms), then return to default
- Error: Red X flash + error toast
- Disabled (In Progress): Badge grayed out, no chevron, tooltip "Cannot change priority while task is in progress"
- Disabled (Completed): Badge grayed out, no chevron, tooltip "Cannot edit completed tasks"

### Active Task Indicator

**Visual Design:**
- Pulsing blue dot (CSS animation, 2s cycle) next to task title
- "In Progress" badge: Blue background (#3b82f6), white text
- Agent name displayed: "Backend-dev" with avatar icon (optional)
- Timestamp: "Started 5 minutes ago" (human-readable relative time)

**Behavior:**
- Appears when task status changes to "in_progress"
- Disappears when task status changes to "done" or "failed"
- Updates in real-time via WebSocket events
- Clicking indicator shows task detail modal with execution logs (if available)

**Color Coding:**
- CRITICAL: Red background (#ef4444), white text
- HIGH: Orange background (#f97316), white text
- MEDIUM: Yellow background (#eab308), dark text
- LOW: Blue background (#3b82f6), white text
- normal: Gray background (#6b7280), white text

**Accessibility:**
- ARIA labels: "Priority: Medium. Click to change."
- Keyboard navigable (Tab, Arrow keys, Enter, Escape)
- Screen reader announces: "Priority changed to High"

### Error Messages

| Error Type | Message | Action |
|------------|---------|--------|
| Invalid Value | "Invalid priority. Must be CRITICAL, HIGH, MEDIUM, LOW, or normal." | Revert to previous value |
| File Not Found | "Task file no longer exists." | Remove task from UI |
| Permission Denied | "Cannot save: insufficient file permissions." | Show sudo instructions |
| Concurrent Edit | "Task was modified by another user. Reload?" | Show Reload button |
| Timeout | "Save operation timed out. Check network connection." | Retry button |
| Task In Progress | "Cannot change priority: task is currently being worked on." | Disable dropdown, show tooltip |

---

## Acceptance Criteria

### Definition of Done

- [ ] User can click priority dropdown on any editable task card (status: pending, assigned)
- [ ] Dropdown shows all 5 priority levels from task schema
- [ ] Selecting new priority updates YAML file within 500ms
- [ ] YAML file preserves comments, formatting, and field order
- [ ] WebSocket `task.updated` event emitted to all clients
- [ ] Visual feedback (spinner → success checkmark) shown
- [ ] Invalid priorities rejected with error message
- [ ] Completed tasks show read-only priority (no dropdown, grayed out)
- [ ] In-progress tasks show disabled priority dropdown with tooltip explanation
- [ ] Active tasks display pulsing indicator + "In Progress" badge with agent name
- [ ] Active task indicator appears/disappears based on task status changes via WebSocket
- [ ] Keyboard navigation works (Tab, Arrow, Enter) for editable tasks only
- [ ] Unit tests: YAML parsing, validation, file write, status checks
- [ ] Integration tests: End-to-end priority change with WebSocket verification
- [ ] Integration tests: In-progress task rejection scenario
- [ ] Manual test: Multi-browser real-time sync verified
- [ ] Manual test: Active task indicator appears when agent starts work
- [ ] Documentation: User guide section added

---

## Implementation Notes

### Recommended Approach

**Phase 1: Backend API (2-3 hours)**
1. Add REST endpoint: `PATCH /api/tasks/:id/priority`
2. Validate priority value against schema
3. Check task status—reject if `in_progress`
4. Update YAML file using PyYAML with comment preservation
5. Emit WebSocket event
6. Unit tests for YAML operations and status validation

**Phase 2: Frontend UI - Priority Editing (2-3 hours)**
1. Replace priority badge with dropdown component
2. Wire dropdown to PATCH endpoint
3. Conditionally disable dropdown based on task status (in_progress, done)
4. Handle loading/success/error states
5. Add toast notifications
6. Update WebSocket handler to refresh UI on `task.updated`

**Phase 3: Frontend UI - Active Task Indicator (2 hours)**
1. Add pulsing indicator component (CSS animation)
2. Add "In Progress" badge with agent name
3. Wire indicator to task status field
4. Subscribe to WebSocket `task.status_changed` events
5. Hide/show indicator based on status transitions

**Phase 4: Polish (1 hour)**
1. Keyboard navigation support (editable tasks only)
2. Tooltip explanations for disabled states
3. Activity log integration
4. Manual testing scenarios 1-8

**Total Estimated Effort:** 7-9 hours

### Technical Design Considerations

- **YAML Library:** Use `ruamel.yaml` (Python) for comment preservation, not `pyyaml`
- **Status Validation:** Check `status` field before allowing priority changes; valid editable states: `pending`, `assigned`
- **Optimistic Locking:** Include `last_modified` timestamp in API request; reject stale updates
- **WebSocket Namespace:** Reuse `/dashboard` namespace; add `task.priority_changed` and `task.status_changed` event subtypes
- **File Write Strategy:** Atomic write (write to temp file → rename) to prevent corruption
- **Rollback:** Cache previous YAML content; restore on write failure
- **Active Task Detection:** Monitor `status` field for transitions: `pending` → `in_progress` → `done`

---

## Open Questions

None—all clarifications obtained from stakeholder.

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| YAML Comment Loss | HIGH | MEDIUM | Use `ruamel.yaml`, add integration tests |
| Concurrent Write Conflicts | MEDIUM | MEDIUM | Implement optimistic locking with retry prompt |
| WebSocket Lag | LOW | LOW | 100ms target well within capabilities |
| File Permission Issues | MEDIUM | LOW | Clear error messages + documentation |

---

## Success Metrics

- **Adoption:** 80% of priority changes happen via dashboard (vs. manual YAML edits) within 2 weeks
- **Performance:** 95th percentile save time <500ms
- **Reliability:** <1% error rate on priority change operations
- **User Satisfaction:** Positive feedback on ease of use (survey or dogfooding feedback)

---

## References

- **Task YAML Schema:** `work/collaboration/inbox/INDEX.md`
- **Dashboard Architecture:** `docs/architecture/adrs/ADR-032-real-time-execution-dashboard.md`
- **File Watcher Implementation:** `src/llm_service/dashboard/file_watcher.py`
- **WebSocket Protocol:** `src/llm_service/dashboard/app.py`

---

**Prepared by:** Analyst Annie  
**Date:** 2026-02-06  
**Status:** Draft (ready for Architect Alphonso technical design review)
