# Manual Testing Guide: Orphan Task Assignment Modal

**Feature:** SPEC-DASH-008 - Orphan Task Assignment  
**Component:** Frontend Modal UI  
**Test Date:** 2026-02-09  
**Tester:** Frontend Freddy

## Pre-requisites

1. Dashboard server running: `python run_dashboard.py`
2. Browser opened to: `http://localhost:8080`
3. Navigate to "Initiatives & Milestones" tab
4. Ensure there are orphan tasks visible (tasks without specification)

## Test Scenarios

### ✅ AC1: Open Assignment Modal

**Steps:**
1. Locate an orphan task in the "Orphan Tasks" section
2. Click the "Assign" button on the task card
3. Observe modal opening animation

**Expected Results:**
- ✅ Modal opens within 500ms (check browser console for timing)
- ✅ Modal displays task preview with:
  - Task title
  - Agent badge
  - Priority badge
- ✅ Search bar is visible at top
- ✅ Initiative list is populated (collapsed by default)
- ✅ Search input has focus for immediate keyboard use

**Performance Check:**
- Browser console should log: `✅ Modal loaded in Xms`
- Value should be < 500ms

---

### ✅ AC2: Expand Initiative and Select Feature

**Steps:**
1. With modal open, click on an initiative header (e.g., "Dashboard Enhancements")
2. Observe the expansion animation
3. Review the list of specifications (features)

**Expected Results:**
- ✅ Initiative expands to show specifications
- ✅ Expand icon changes from ▶ to ▼
- ✅ Each specification shows:
  - 📄 Icon
  - Specification title
  - Status badge
  - "Assign to [Title]" button
- ✅ Can collapse/expand by clicking header again

---

### ✅ AC3: Assign Task to Feature

**Steps:**
1. Expand an initiative
2. Click "Assign to [Feature Name]" button
3. Observe loading state
4. Wait for success response

**Expected Results:**
- ✅ Loading overlay appears with spinner
- ✅ Loading message: "Assigning task..."
- ✅ Success toast notification appears: "Task assigned to [Feature]"
- ✅ Modal closes automatically
- ✅ Task disappears from orphan section
- ✅ Task appears in the correct initiative/specification hierarchy
- ✅ Portfolio view refreshes

**Backend Interaction:**
- Browser Network tab shows: `PATCH /api/tasks/:id/specification`
- Request body contains:
  ```json
  {
    "specification": "specifications/...",
    "feature": "Feature Title"
  }
  ```
- Response: 200 OK

---

### ✅ AC4: Handle Assignment Conflict (409)

**Steps:**
1. Open assignment modal for an orphan task
2. In a separate terminal, manually edit the task YAML file to simulate concurrent modification
3. Click "Assign to [Feature]" in the modal

**Expected Results:**
- ✅ Conflict dialog appears over the modal
- ✅ Error message: "This task was modified by another user."
- ✅ Two buttons visible: "Refresh" and "Cancel"
- ✅ Clicking "Cancel" closes conflict dialog, modal remains open
- ✅ Clicking "Refresh" closes modal and shows toast: "Data refreshed. Please try assigning again."
- ✅ Original modal remains open (or can be reopened)

**Backend Interaction:**
- Response: 409 Conflict

---

### ✅ AC5: Search/Filter Initiatives

**Steps:**
1. Open assignment modal
2. Type "dashboard" in the search bar (case-insensitive)
3. Observe filtering behavior
4. Clear search to see all initiatives again

**Expected Results:**
- ✅ Only initiatives/features matching "dashboard" are displayed
- ✅ Filtering completes in < 100ms (check console: `🔍 Filter completed in Xms`)
- ✅ Filtering is client-side (no network requests in Browser Network tab)
- ✅ Clearing search shows all initiatives again

**Performance Check:**
- Console log should show filter time < 100ms

---

### ✅ AC6: Keyboard Navigation

**Steps:**
1. Open assignment modal
2. Press Tab key multiple times
3. Press Escape key
4. Re-open modal
5. Tab to an "Assign" button
6. Press Enter

**Expected Results:**
- ✅ Tab key moves focus through:
  - Search input (focused by default)
  - Initiative headers
  - Assign buttons
  - Close button
- ✅ Escape key closes the modal
- ✅ Enter key on "Assign" button triggers assignment
- ✅ Focus indicators visible (blue outline)
- ✅ Modal traps focus (Tab doesn't leave modal)

---

## Error Scenarios

### Invalid Specification Path

**Steps:**
1. Open browser DevTools console
2. Run: `openAssignmentModal('test-task-id', {id: 'test', title: 'Test', agent: 'test', priority: 'HIGH'})`
3. Manually trigger assignment with invalid path using DevTools:
   ```javascript
   fetch('/api/tasks/test-task-id/specification', {
     method: 'PATCH',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({specification: '../../../etc/passwd'})
   })
   ```

**Expected Results:**
- ✅ Error toast: "Invalid specification path" or similar
- ✅ Modal remains open
- ✅ User can retry with valid path

---

### Missing Specification File

**Steps:**
1. Attempt to assign to a specification that doesn't exist
2. Observe error handling

**Expected Results:**
- ✅ Error toast: "Specification file not found" or similar
- ✅ Modal remains open

---

## Accessibility Checks

### Screen Reader Support

**Steps:**
1. Enable screen reader (VoiceOver on Mac, NVDA on Windows)
2. Open modal
3. Navigate using keyboard only

**Expected Results:**
- ✅ Modal announces itself when opened
- ✅ Task preview information is readable
- ✅ Initiative/specification hierarchy is navigable
- ✅ Buttons have descriptive labels
- ✅ Close button has aria-label: "Close modal"

### Focus Management

**Expected Results:**
- ✅ Focus moves to search input when modal opens
- ✅ Focus returns to "Assign" button when modal closes
- ✅ Focus is trapped inside modal (can't tab to background)

---

## Performance Validation

### Modal Load Time

**Tool:** Browser DevTools Console

**Benchmark:** < 500ms (P95)

**Measurement:**
- Console log: `✅ Modal loaded in Xms`
- If > 500ms, console shows: `⚠️ Modal load time exceeded 500ms: Xms`

### Search Filter Time

**Tool:** Browser DevTools Console

**Benchmark:** < 100ms (client-side)

**Measurement:**
- Console log: `🔍 Filter completed in Xms`
- If > 100ms, console shows: `⚠️ Filter time exceeded 100ms: Xms`

---

## Browser Compatibility

Test in:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)

---

## WebSocket Real-Time Updates

**Steps:**
1. Open dashboard in two browser tabs
2. In Tab 1, assign an orphan task
3. Observe Tab 2

**Expected Results:**
- ✅ Tab 2 receives WebSocket event: `task.assigned`
- ✅ Tab 2 portfolio view updates automatically
- ✅ Orphan task moves to correct specification in both tabs

---

## Summary Checklist

- [ ] AC1: Open Assignment Modal (< 500ms)
- [ ] AC2: Expand Initiative and Select Feature
- [ ] AC3: Assign Task to Feature (success flow)
- [ ] AC4: Handle Assignment Conflict (409)
- [ ] AC5: Search/Filter Initiatives (< 100ms)
- [ ] AC6: Keyboard Navigation (Tab, Escape, Enter)
- [ ] Error handling (invalid paths, missing files)
- [ ] Accessibility (screen reader, focus management)
- [ ] Performance benchmarks met
- [ ] Cross-browser compatibility
- [ ] WebSocket real-time updates

---

## Notes

- All performance metrics are logged to browser console
- Modal component follows ADR-035 patterns (consistent with priority editing modal)
- Client-side filtering requires no backend round-trips
- Conflict resolution preserves user's work (modal stays open)
