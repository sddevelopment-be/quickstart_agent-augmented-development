# ADR-035: Dashboard Task Priority Editing

**Status:** Proposed  
**Date:** 2026-02-06  
**Deciders:** Architect Alphonso, Human-in-Charge  
**Related Specs:** [Task Priority Editing Specification](../../specifications/llm-dashboard/task-priority-editing.md)  
**Related ADRs:** [ADR-032: Real-Time Execution Dashboard](ADR-032-real-time-execution-dashboard.md)

---

## Context

The dashboard currently displays tasks in read-only mode. Users must leave the dashboard, open a text editor, find the YAML file, edit the `priority` field, save, and return to the dashboard to reprioritize work. This context-switching friction slows down dynamic task management during active development.

**Problem Statement:**  
Engineers need real-time priority adjustment capability without leaving the dashboard monitoring session.

**Constraints:**
- MUST preserve file-based orchestration (YAML files remain source of truth)
- MUST prevent priority changes on in-progress tasks (avoid disrupting agent workflows)
- MUST maintain Git audit trail
- MUST support all priority values from task schema (CRITICAL, HIGH, MEDIUM, LOW, normal)

---

## Decision

Implement in-place priority editing in the dashboard UI with the following architecture:

### Solution Components

**1. Backend API Endpoint**
```
PATCH /api/tasks/:id/priority
Body: { "priority": "HIGH", "last_modified": "2026-02-06T10:00:00Z" }
Response: { "success": true, "task": {...} }
```

**2. YAML File Updates**
- Use `ruamel.yaml` (Python) to preserve comments and formatting
- Implement atomic writes (temp file → rename) to prevent corruption
- Validate new priority value against schema before writing
- Check task status—reject edits if `status: in_progress`

**3. Frontend Priority Dropdown**
- Replace static priority badge with interactive dropdown
- Disable dropdown for `status: in_progress` and `status: done`
- Show visual feedback: spinner → checkmark/error
- Emit WebSocket event after successful save

**4. Real-Time Synchronization**
- File watcher detects YAML change
- Emit `task.priority_changed` WebSocket event
- All connected clients update priority display

**5. In-Progress Task Indicator**
- Pulsing blue dot animation (CSS) for active tasks
- "In Progress" badge with agent name
- Priority dropdown disabled with tooltip: "Cannot change priority while task is in progress"

---

## Alternatives Considered

### Alternative 1: Event-Based Priority Change (Rejected)
**Approach:** Emit priority change request event; separate service processes it  
**Pros:** Clean separation, scales better  
**Cons:** Complexity overkill for single-user tool; latency increased  
**Decision:** Direct file writes simpler and sufficient

### Alternative 2: Temporary UI State Only (Rejected)
**Approach:** Change priority in UI only, don't persist to file  
**Pros:** Fast, no file write complexity  
**Cons:** Loses file-based orchestration principle; state lost on refresh  
**Decision:** File must remain source of truth per ADR-032

### Alternative 3: Priority Change Queue (Rejected)
**Approach:** Queue changes, batch-write to files periodically  
**Pros:** Reduces I/O, optimizes performance  
**Cons:** Delayed persistence confusing to users; complicates error handling  
**Decision:** Immediate writes provide better UX

---

## Consequences

### Positive

- ✅ **Reduced Context Switching:** Users stay in dashboard for priority adjustments
- ✅ **Real-Time Feedback:** WebSocket updates ensure all clients see changes immediately
- ✅ **Preserves Orchestration:** YAML files remain source of truth, Git audit trail intact
- ✅ **Safe Edits:** In-progress tasks protected from disruptive changes

### Negative

- ⚠️ **File Write Complexity:** YAML comment preservation requires careful library choice (`ruamel.yaml`)
- ⚠️ **Concurrency Risk:** Multiple users/agents editing same file simultaneously needs handling
- ⚠️ **Increased Attack Surface:** UI now has write permissions; requires input validation

### Mitigations

- **Comment Preservation:** Use `ruamel.yaml` library (tested for comment preservation)
- **Concurrency:** Implement optimistic locking with `last_modified` timestamp check
- **Security:** Validate priority enum before writes; sanitize file paths to prevent traversal

---

## Implementation Plan

### Phase 1: Backend (2-3 hours)
- Create `PATCH /api/tasks/:id/priority` endpoint
- Integrate `ruamel.yaml` for file updates
- Add status validation (reject if `in_progress`)
- Unit tests: YAML operations, validation, error cases

### Phase 2: Frontend (2-3 hours)
- Replace priority badge with dropdown component
- Wire to PATCH endpoint
- Handle loading/success/error states
- WebSocket event handling

### Phase 3: In-Progress Indicator (2 hours)
- Add pulsing dot animation (CSS)
- Add "In Progress" badge component
- Wire to task status field
- Hide/show based on status transitions

### Phase 4: Testing (1 hour)
- Integration test: End-to-end priority change
- Security test: XSS/path traversal attempts
- Concurrent edit scenario testing

**Total Effort:** 7-9 hours

---

## Technical Design

### Component Architecture

```
┌─────────────────────────────────────────────────────┐
│             Dashboard UI (Browser)                   │
│  ┌──────────────┐        ┌───────────────────────┐ │
│  │ Priority     │◄──────►│ WebSocket Client      │ │
│  │ Dropdown     │        │ (/dashboard namespace)│ │
│  └──────┬───────┘        └───────────────────────┘ │
└─────────┼────────────────────────────────────────────┘
          │ HTTP PATCH
          ▼
┌─────────────────────────────────────────────────────┐
│          Flask Dashboard Server                      │
│  ┌──────────────────┐    ┌───────────────────────┐ │
│  │ Priority API     │───►│ YAML File Writer      │ │
│  │ (validation,     │    │ (ruamel.yaml)         │ │
│  │  status check)   │    └───────────────────────┘ │
│  └──────────────────┘                               │
│           │                                          │
│           ▼                                          │
│  ┌──────────────────┐    ┌───────────────────────┐ │
│  │ File Watcher     │───►│ WebSocket Emitter     │ │
│  │ (detects change) │    │ (broadcasts update)   │ │
│  └──────────────────┘    └───────────────────────┘ │
└─────────────────────────────────────────────────────┘
          │
          ▼ (atomic write)
┌─────────────────────────────────────────────────────┐
│       File System (YAML task files)                  │
│       work/collaboration/{inbox,assigned,done}/      │
└─────────────────────────────────────────────────────┘
```

### Data Flow

1. User selects new priority from dropdown
2. Frontend sends `PATCH /api/tasks/123/priority` with new value
3. Backend validates:
   - Priority value is valid enum (CRITICAL, HIGH, MEDIUM, LOW, normal)
   - Task status != `in_progress`
   - File exists and is writable
4. Backend atomically writes YAML file (preserving comments)
5. File watcher detects change
6. WebSocket event emitted: `task.priority_changed`
7. All connected clients update UI

### Error Handling

| Error Condition | HTTP Status | User Message | Recovery |
|-----------------|-------------|--------------|----------|
| Invalid priority | 400 | "Must be CRITICAL, HIGH, MEDIUM, LOW, or normal" | Show error toast |
| Task in progress | 409 | "Cannot change priority while task is in progress" | Disabled dropdown |
| File not found | 404 | "Task no longer exists" | Remove from UI |
| Concurrent edit | 409 | "Task was modified by another user. Reload?" | Reload button |
| Write failed | 500 | "Save failed. Check permissions." | Retry button |

---

## Security Considerations

### XSS Prevention
- Validate priority value against whitelist enum
- No user-provided strings written to YAML (only enum values)

### Path Traversal Prevention
- Validate task ID format (alphanumeric + dashes only)
- Reject paths containing `../` or absolute paths
- Restrict file writes to `work/collaboration/` directory

### CSRF Protection
- Use SameSite cookies for authentication (if auth added later)
- Validate origin header matches dashboard domain

---

## Performance Characteristics

- **Write Latency:** <200ms (YAML parse + write + file sync)
- **WebSocket Broadcast:** <100ms to all clients
- **Optimistic UI:** Dropdown updates immediately, rollback on error

---

## Testing Strategy

### Unit Tests
- YAML parsing with comment preservation
- Priority validation (valid/invalid values)
- Status checking (allow/reject based on status)
- Atomic file write operations

### Integration Tests
- End-to-end: Select priority → YAML updated → WebSocket received
- Concurrent edit detection and recovery
- In-progress task rejection

### Manual Tests
- Multi-browser real-time sync
- Network failure recovery
- Large task files (>100KB YAML)

---

## Open Questions

✅ None—all resolved with stakeholder.

---

## References

- **Specification:** `specifications/llm-dashboard/task-priority-editing.md`
- **ADR-032:** Real-Time Execution Dashboard
- **File Watcher Implementation:** `src/llm_service/dashboard/file_watcher.py`
- **ruamel.yaml Documentation:** https://yaml.readthedocs.io/

---

**Author:** Architect Alphonso  
**Reviewers:** Human-in-Charge, Backend-dev Benny  
**Status:** Proposed (awaiting approval)  
**Next Steps:** Approval → Create implementation tasks → Assign to Backend-dev
