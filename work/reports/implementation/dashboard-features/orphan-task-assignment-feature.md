# Feature Request: Orphan Task Assignment to Specifications

**Date:** 2026-02-06  
**Requestor:** User  
**Context:** Dashboard Initiative Tracking feature delivered, need ability to link orphan tasks to specifications

---

## Problem Statement

Currently, orphan tasks (tasks without a `specification:` field or with invalid specification path) are displayed in a separate section but cannot be assigned to specifications through the dashboard UI. Users must manually edit YAML files to add the `specification:` field.

**User Need:** Ability to assign orphan tasks to specifications directly from the dashboard UI.

---

## Proposed Solution Options

### Option 1: Simple Dropdown Assignment (Recommended - 3-4 hours)

**UX:**
- Add "Assign to Spec" button next to each orphan task
- Click button → dropdown appears with list of available specifications
- Select specification → task updated, moved to appropriate initiative

**Pros:**
- Simple implementation
- Fast development time
- Minimal backend changes

**Cons:**
- No validation of feature-level assignment
- Assigns to specification root (not specific feature)

**Estimated Effort:** 3-4 hours
- Backend: 1-2h (PATCH endpoint to update specification field)
- Frontend: 2h (dropdown UI, API integration)

---

### Option 2: Feature-Level Assignment (Advanced - 6-8 hours)

**UX:**
- Click "Assign" on orphan task
- Modal opens showing initiative → feature hierarchy
- User selects specific feature to assign task to
- Task updated with specification path

**Pros:**
- More precise assignment (feature-level)
- Better UX (visual hierarchy)
- Aligns with portfolio structure

**Cons:**
- More complex implementation
- Requires specification frontmatter update to link task to feature
- Longer development time

**Estimated Effort:** 6-8 hours
- Backend: 3-4h (specification frontmatter update, feature linking)
- Frontend: 3-4h (modal UI, hierarchy picker)

---

### Option 3: Drag-and-Drop (Future Enhancement - 10-15 hours)

**UX:**
- Drag orphan task from orphan section
- Drop onto initiative or feature in portfolio view
- Task automatically assigned

**Pros:**
- Best UX (intuitive, visual)
- No intermediate modals
- Professional feel

**Cons:**
- Complex drag-and-drop implementation
- Accessibility concerns
- Much longer development time

**Estimated Effort:** 10-15 hours (not recommended for MVP)

---

## Recommended Implementation: Option 1

**Why:**
- Fastest time to value (3-4h vs 6-8h or 10-15h)
- Meets core user need (link orphan to spec)
- Can enhance later (upgrade to Option 2 or 3)
- Low risk, simple code

---

## Implementation Plan (Option 1)

### Backend (1-2 hours)

**Endpoint:**
```python
PATCH /api/tasks/:task_id/specification

Request:
{
  "specification": "specifications/llm-dashboard/task-priority-editing.md"
}

Response 200:
{
  "success": true,
  "task": { ... }
}

Errors:
- 400: Invalid specification path
- 404: Task or specification not found
- 409: Task in_progress (optional protection)
```

**Implementation:**
- Validate specification file exists
- Update task YAML file (preserve comments with ruamel.yaml)
- Trigger WebSocket event for portfolio refresh
- Atomic file write (temp → rename)

**Files:**
- Modify: `src/llm_service/dashboard/app.py`
- Reuse: `src/llm_service/dashboard/task_priority_updater.py` (YAML writing logic)

**Tests:**
- Unit tests: specification path validation
- Integration tests: end-to-end assignment
- Target: 10-15 tests, >80% coverage

---

### Frontend (2 hours)

**UI Changes:**
```html
<!-- Orphan task card with assign button -->
<div class="orphan-task-card">
  <div class="task-info">
    <h4>Task Title</h4>
    <span class="badge">inbox</span>
  </div>
  <button onclick="assignOrphanTask('task-id')" class="btn-assign">
    📎 Assign to Spec
  </button>
</div>

<!-- Dropdown that appears -->
<select id="spec-selector-task-id" class="spec-selector">
  <option value="">-- Select Specification --</option>
  <option value="specifications/llm-dashboard/markdown-rendering.md">
    Markdown Rendering (SPEC-DASH-002)
  </option>
  <!-- ... more options -->
</select>
```

**JavaScript:**
```javascript
async function assignOrphanTask(taskId) {
  // Show dropdown (or fetch specs first if needed)
  // On select, call API
  const specPath = dropdown.value;
  
  const response = await fetch(`/api/tasks/${taskId}/specification`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ specification: specPath })
  });
  
  if (response.ok) {
    showSuccessToast('Task assigned!');
    loadPortfolio(); // Refresh
  } else {
    showErrorToast('Failed to assign task');
  }
}
```

**CSS:**
- Style assign button (subtle, secondary style)
- Style dropdown (match existing theme)
- Add loading state

---

## Task Creation

**To implement this feature:**

1. **Create specification** (recommended):
   ```bash
   # Create new spec file
   specifications/llm-dashboard/orphan-task-assignment.md
   
   # Frontmatter:
   ---
   id: SPEC-DASH-007
   title: Orphan Task Assignment
   initiative: dashboard-enhancements
   priority: MEDIUM
   status: draft
   ---
   ```

2. **Create ADR** (if architectural decision needed):
   - Decide on specification field format
   - Decide on validation rules
   - Document trade-offs

3. **Create implementation task**:
   ```yaml
   id: 2026-02-06T1500-dashboard-orphan-assignment
   title: Dashboard Orphan Task Assignment
   agent: python-pedro  # Backend + Frontend
   priority: MEDIUM
   estimated_hours: 4
   specification: specifications/llm-dashboard/orphan-task-assignment.md
   
   description: |
     Enable users to assign orphan tasks to specifications via dashboard UI.
     
     Backend: PATCH /api/tasks/:id/specification endpoint
     Frontend: Dropdown selector with specification list
     
     Success criteria:
     - Orphan task can be assigned to specification
     - Task moves from orphan section to appropriate initiative
     - Real-time update via WebSocket
     - YAML comments preserved
   ```

---

## Alternative: Quick Manual Process

**If immediate need without development:**

1. Open task file in editor: `work/collaboration/inbox/TASK_ID.yaml`
2. Add `specification:` field:
   ```yaml
   specification: specifications/llm-dashboard/markdown-rendering.md
   ```
3. Save file
4. Dashboard will auto-refresh (via file watcher)
5. Task appears in appropriate initiative

**Pros:** Zero development time  
**Cons:** Manual editing, error-prone, not scalable

---

## Decision Required

**Which approach do you prefer?**

- ✅ **Option 1: Simple Dropdown (3-4h)** - Fastest, meets core need
- ⏳ **Option 2: Feature-Level Assignment (6-8h)** - More precise
- ⏸️ **Option 3: Drag-and-Drop (10-15h)** - Best UX, future enhancement
- 📝 **Manual editing** - No development, temporary solution

**Recommendation:** Implement Option 1 now, consider Option 3 as future enhancement after user feedback.

---

## References

- **Current Feature:** Dashboard Initiative Tracking (ADR-037)
- **Related:** Task Priority Editing (ADR-035) - YAML writing patterns
- **Portfolio API:** `/api/portfolio` - lists specifications
- **Task API Pattern:** `/api/tasks/:id/priority` - similar endpoint structure
