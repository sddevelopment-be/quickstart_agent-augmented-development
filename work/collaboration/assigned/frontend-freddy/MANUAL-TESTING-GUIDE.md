# Priority Editing Feature - Manual Testing Guide

**Feature:** Dashboard Task Priority In-Place Editing (ADR-035)  
**Dashboard URL:** http://localhost:8080  
**Date:** 2026-02-06  
**Tester:** _____________

---

## 🎯 Testing Objectives

Verify that users can:
1. Edit priority of editable tasks via dropdown
2. See visual protection for in-progress/done/failed tasks
3. Receive clear feedback on success/error states
4. Experience real-time synchronization across browser tabs

---

## ✅ Test Cases

### Test 1: Basic Priority Editing

**Steps:**
1. Open dashboard: http://localhost:8080
2. Locate a task in the "Inbox" or "Assigned" column
3. Find the priority dropdown (replaces the static `🏷️ MEDIUM` text)
4. Change priority from current value to a different value (e.g., MEDIUM → HIGH)

**Expected Results:**
- [ ] Dropdown appears in task card meta section
- [ ] Current priority is pre-selected in dropdown
- [ ] Upon change:
  - [ ] Dropdown is disabled immediately
  - [ ] Loading spinner (⏳) appears next to dropdown
  - [ ] After ~200ms, success checkmark (✅) appears briefly
  - [ ] Activity feed shows "Priority Updated: [task-id] → HIGH"
  - [ ] Dropdown re-enables

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 2: In-Progress Task Protection

**Steps:**
1. Identify a task with `status: in_progress` (if none exist, manually edit a task file)
2. Locate the task in the dashboard

**Expected Results:**
- [ ] Priority displays as a **badge** (not dropdown)
- [ ] Orange pulsing dot (●) appears before priority text
- [ ] Badge has visual styling indicating disabled state
- [ ] Hovering over badge shows tooltip: "Cannot edit in_progress tasks"
- [ ] Badge is not clickable/editable

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 3: Error Handling (Invalid Priority)

**Steps:**
1. Open browser developer console (F12)
2. Execute JavaScript in console:
   ```javascript
   fetch('/api/tasks/test-task-123/priority', {
     method: 'PATCH',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({priority: 'INVALID'})
   }).then(r => r.json()).then(console.log)
   ```

**Expected Results:**
- [ ] API returns 400 Bad Request
- [ ] Response contains error message about valid priorities
- [ ] If done via UI dropdown, dropdown would revert to original value
- [ ] Toast notification appears: "Priority Update Failed: [error message]"
- [ ] Activity feed shows error entry

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 4: Real-Time WebSocket Synchronization

**Steps:**
1. Open dashboard in **two separate browser tabs** (Tab A and Tab B)
2. In Tab A, change a task priority (e.g., LOW → HIGH)
3. Observe Tab B (do not refresh)

**Expected Results:**
- [ ] Tab A shows normal success flow (spinner → checkmark)
- [ ] Tab B automatically updates priority dropdown value within 1 second
- [ ] Tab B shows toast notification: "Priority updated by another user: [task-id] → HIGH"
- [ ] Both tabs show identical priority values
- [ ] Activity feed updates in both tabs

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 5: Modal Priority Editing

**Steps:**
1. Click on any task card to open the modal
2. Locate the "Priority:" field in modal
3. Change priority using the dropdown in the modal
4. Close modal
5. Reopen the same task modal

**Expected Results:**
- [ ] Priority dropdown appears in modal (same as card)
- [ ] Dropdown functions identically to card dropdown
- [ ] Loading/success states appear in modal
- [ ] After closing and reopening, priority change persists
- [ ] Card view also reflects the new priority

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 6: Error Recovery (409 Conflict)

**Steps:**
1. Manually edit a task file to set `status: in_progress`
2. Before dashboard refreshes, try to change priority via dropdown

**Expected Results:**
- [ ] API returns 409 Conflict
- [ ] Toast notification appears: "Priority Update Failed: Cannot edit task with status 'in_progress'..."
- [ ] Dropdown reverts to original value
- [ ] Activity feed shows error entry
- [ ] After dashboard refresh, task shows badge (not dropdown)

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 7: Multiple Priority Changes

**Steps:**
1. Select a task and change priority: MEDIUM → HIGH
2. Wait for success confirmation
3. Immediately change again: HIGH → CRITICAL
4. Wait for success
5. Change again: CRITICAL → LOW

**Expected Results:**
- [ ] Each change shows loading → success cycle
- [ ] No race conditions or stuck states
- [ ] Final value is LOW
- [ ] Activity feed shows 3 separate update entries
- [ ] YAML file reflects final value (check manually)

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 8: Done/Failed Task Protection

**Steps:**
1. Find or create tasks with `status: done` and `status: failed`
2. Locate these tasks in the "Done" column

**Expected Results:**
- [ ] Priority displays as badge (not dropdown)
- [ ] No pulsing dot (only for in_progress)
- [ ] Tooltip explains why editing is disabled
- [ ] Badge styling indicates non-editable state

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 9: Visual Feedback Timing

**Steps:**
1. Change a task priority
2. Use stopwatch or browser dev tools to measure timing

**Expected Results:**
- [ ] Loading spinner appears within 50ms of change
- [ ] API call completes within 500ms
- [ ] Success checkmark appears after API success
- [ ] Success checkmark auto-hides after 2 seconds
- [ ] Toast notification auto-dismisses after 5 seconds

**Pass/Fail:** ___________  
**Notes:**
```



```

---

### Test 10: Accessibility & Keyboard Navigation

**Steps:**
1. Use keyboard (Tab key) to navigate to a priority dropdown
2. Press Enter or Space to open dropdown
3. Use arrow keys to select a priority
4. Press Enter to confirm

**Expected Results:**
- [ ] Dropdown is reachable via keyboard
- [ ] Dropdown opens/closes with keyboard
- [ ] Options are selectable with arrow keys
- [ ] Selection triggers the same change flow as mouse click
- [ ] Loading/success states are perceivable without color alone

**Pass/Fail:** ___________  
**Notes:**
```



```

---

## 🐛 Bugs Found

| # | Severity | Description | Steps to Reproduce | Expected | Actual |
|---|----------|-------------|-------------------|----------|--------|
| 1 |          |             |                   |          |        |
| 2 |          |             |                   |          |        |
| 3 |          |             |                   |          |        |

---

## 💡 Usability Observations

| Observation | Impact | Suggestion |
|-------------|--------|------------|
|             |        |            |
|             |        |            |

---

## 📊 Test Summary

- **Total Test Cases:** 10
- **Passed:** _____
- **Failed:** _____
- **Blocked:** _____
- **Overall Status:** [ ] PASS / [ ] FAIL

---

## ✍️ Tester Sign-Off

**Name:** ___________________________  
**Date:** ___________________________  
**Signature:** ______________________

**Recommendation:**
- [ ] Approve for production
- [ ] Approve with minor fixes
- [ ] Reject - major issues found

**Comments:**
```




```
