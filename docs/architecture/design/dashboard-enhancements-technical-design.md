# Dashboard Enhancements: Technical Design Document

**Version:** 1.0.0  
**Date:** 2026-02-06  
**Author:** Architect Alphonso  
**Status:** Proposed  
**Related ADRs:** ADR-035, ADR-036, ADR-037  
**Related Specifications:** `specifications/llm-dashboard/`

---

## Executive Summary

This document provides a unified technical design for three dashboard enhancements that improve task management, readability, and strategic visibility:

1. **Task Priority Editing** (ADR-035): In-place priority updates with in-progress protection
2. **Markdown Rendering** (ADR-036): Formatted display of task descriptions and context
3. **Initiative Tracking** (ADR-037): Portfolio view linking specifications to tasks

**Combined Effort:** 27-35 hours (MVP: 21-28 hours)  
**Implementation Order:** ADR-036 → ADR-035 → ADR-037 (dependency-based)

---

## System Architecture

### High-Level Component Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                   Dashboard Frontend (Browser)                  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Task List    │  │ Task Detail  │  │ Portfolio View       │ │
│  │ (Status View)│  │ Modal        │  │ (Initiative Hierarchy)│ │
│  │              │  │              │  │                      │ │
│  │ - Priority   │  │ - Markdown   │  │ - Initiative Cards   │ │
│  │   Dropdown   │  │   Rendering  │  │ - Feature Accordion  │ │
│  │ - In-Progress│  │   (marked.js)│  │ - Progress Bars      │ │
│  │   Indicator  │  │ - DOMPurify  │  │ - Task Drill-Down    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────────┘ │
│         │                 │                  │                  │
└─────────┼─────────────────┼──────────────────┼──────────────────┘
          │                 │                  │
          │ PATCH priority  │ Task data        │ GET portfolio
          │                 │                  │
          ▼                 ▼                  ▼
┌────────────────────────────────────────────────────────────────┐
│                    Flask Dashboard Server                       │
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────────────┐   │
│  │ REST API Endpoints   │  │ WebSocket Event Handlers     │   │
│  │                      │  │                              │   │
│  │ - PATCH /api/tasks/  │  │ - task.priority_changed      │   │
│  │   :id/priority       │  │ - task.updated               │   │
│  │ - GET /api/portfolio │  │ - portfolio.updated          │   │
│  └──────┬───────────────┘  └──────────────────────────────┘   │
│         │                                                       │
│  ┌──────▼──────────────────────────────────────────────────┐  │
│  │           Core Services                                  │  │
│  │                                                          │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌───────────┐ │  │
│  │  │ YAML File      │  │ Specification  │  │ Portfolio │ │  │
│  │  │ Writer         │  │ Parser         │  │ Aggregator│ │  │
│  │  │ (ruamel.yaml)  │  │ (frontmatter)  │  │ (cache)   │ │  │
│  │  └────────┬───────┘  └────────┬───────┘  └─────┬─────┘ │  │
│  └───────────┼──────────────────┼─────────────────┼────────┘  │
│              │                  │                 │            │
│  ┌───────────▼──────────────────▼─────────────────▼─────────┐ │
│  │              File Watcher (watchdog)                      │ │
│  │  - Monitors work/collaboration/*.yaml                     │ │
│  │  - Monitors specifications/**/*.md                        │ │
│  │  - Triggers WebSocket events on changes                   │ │
│  └───────────────────────────────┬───────────────────────────┘ │
└────────────────────────────────────┼───────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────┐
│                      File System                                │
│                                                                  │
│  ┌──────────────────────────┐  ┌──────────────────────────┐   │
│  │ work/collaboration/       │  │ specifications/          │   │
│  │ - inbox/*.yaml            │  │ - **/*.md (frontmatter)  │   │
│  │ - assigned/*.yaml         │  │ - schema.json            │   │
│  │ - done/*.yaml             │  │                          │   │
│  └───────────────────────────┘  └──────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. Priority Editing Flow (ADR-035)

```
User clicks priority dropdown → Selects "HIGH"
                │
                ▼
┌─────────────────────────────────────────────┐
│ Frontend validates task not in-progress     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼ HTTP PATCH /api/tasks/123/priority
┌─────────────────────────────────────────────┐
│ Backend validates:                          │
│ - Priority value in enum                    │
│ - Task status != "in_progress"              │
│ - File exists and writable                  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ YAML File Writer (ruamel.yaml):             │
│ 1. Parse existing YAML (preserve comments)  │
│ 2. Update priority field                    │
│ 3. Atomic write (temp file → rename)        │
└─────────────────┬───────────────────────────┘
                  │
                  ▼ File modified
┌─────────────────────────────────────────────┐
│ File Watcher detects change                 │
└─────────────────┬───────────────────────────┘
                  │
                  ▼ WebSocket emit
┌─────────────────────────────────────────────┐
│ All connected clients receive:              │
│ task.priority_changed event                 │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ Frontend updates priority badge             │
│ (no page reload needed)                     │
└─────────────────────────────────────────────┘
```

### 2. Markdown Rendering Flow (ADR-036)

```
User opens task detail modal
                │
                ▼
┌─────────────────────────────────────────────┐
│ Frontend receives task data (JSON)          │
└─────────────────┬───────────────────────────┘
                  │
          ┌───────┴──────────┐
          │                  │
          ▼                  ▼
┌─────────────────┐  ┌──────────────────┐
│ Technical Fields│  │ Markdown Fields  │
│ (id, agent,     │  │ (description,    │
│  status, etc.)  │  │  context, etc.)  │
└────────┬────────┘  └────────┬─────────┘
         │                    │
         │                    ▼
         │          ┌─────────────────────┐
         │          │ marked.parse()      │
         │          │ (Markdown → HTML)   │
         │          └─────────┬───────────┘
         │                    │
         │                    ▼
         │          ┌─────────────────────┐
         │          │ DOMPurify.sanitize()│
         │          │ (XSS prevention)    │
         │          └─────────┬───────────┘
         │                    │
         ▼                    ▼
┌──────────────────────────────────────────┐
│ DOM Insertion:                           │
│ - Technical: .textContent (plain text)   │
│ - Markdown: .innerHTML (safe HTML)       │
└──────────────────────────────────────────┘
```

### 3. Portfolio View Loading Flow (ADR-037)

```
User navigates to Portfolio tab
                │
                ▼ GET /api/portfolio
┌─────────────────────────────────────────────┐
│ Check PortfolioCache                        │
└─────────────────┬───────────────────────────┘
                  │
      ┌───────────┴────────────┐
      │                        │
      ▼ Cache hit              ▼ Cache miss
┌─────────────────┐  ┌─────────────────────────┐
│ Return cached   │  │ Scan specifications/    │
│ portfolio data  │  │ directory               │
│ (<50ms)         │  └─────────┬───────────────┘
└─────────────────┘            │
                               ▼
                     ┌──────────────────────────┐
                     │ Parse each *.md file:    │
                     │ - Extract YAML frontmatter│
                     │ - Build initiative/feature│
                     │   hierarchy              │
                     └─────────┬────────────────┘
                               │
                               ▼
                     ┌──────────────────────────┐
                     │ Find linked tasks:       │
                     │ - Match task.specification│
                     │   to spec file path      │
                     │ - Group tasks by feature │
                     └─────────┬────────────────┘
                               │
                               ▼
                     ┌──────────────────────────┐
                     │ Calculate progress:      │
                     │ - Task status → weights  │
                     │ - Roll up to features    │
                     │ - Roll up to initiatives │
                     └─────────┬────────────────┘
                               │
                               ▼
                     ┌──────────────────────────┐
                     │ Cache result             │
                     │ (invalidate on file mod) │
                     └─────────┬────────────────┘
                               │
                ┌──────────────┴─────────┐
                ▼                        ▼
      Return portfolio JSON    WebSocket emit
                               portfolio.loaded
```

---

## Database Schema (File-Based)

### Task YAML Schema (Enhanced)

```yaml
# work/collaboration/assigned/2026-02-05T1400-example.yaml
id: "2026-02-05T1400-example"
title: "Implement Priority Edit API"
agent: "backend-dev-benny"
status: "in_progress"        # NEW: Used for in-progress check
priority: "HIGH"              # UPDATED: Editable via API
created: "2026-02-05T14:00:00Z"
updated: "2026-02-06T10:30:00Z"
estimated_hours: 3

# NEW: Link to specification
specification: "specifications/llm-dashboard/task-priority-editing.md"

description: |
  # Task Description (Markdown supported)
  
  Implement the `PATCH /api/tasks/:id/priority` endpoint.
  
  ## Requirements
  - Validate priority enum
  - Check task status
  - Atomic YAML writes

context: |
  Part of ADR-035 implementation.

acceptance_criteria: |
  - [ ] API returns 200 on valid priority
  - [ ] API returns 409 if task in-progress
  - [ ] YAML comments preserved

notes: |
  Use `ruamel.yaml` for comment preservation.
```

### Specification Frontmatter Schema (New)

```yaml
# specifications/llm-dashboard/task-priority-editing.md
---
id: "SPEC-DASH-001"
title: "Task Priority Editing"
status: "in_progress"        # draft | in_progress | implemented | deprecated
initiative: "Dashboard Enhancements"
priority: "HIGH"
epic: "Task Management"
target_personas: ["devops-danny", "backend-dev-benny"]

# NEW: Features array
features:
  - id: "FEAT-DASH-001-01"
    title: "Backend Priority API"
    status: "in_progress"
  - id: "FEAT-DASH-001-02"
    title: "Frontend Priority Dropdown"
    status: "inbox"

# NEW: Manual progress override (optional)
completion: 40               # 0-100, overrides calculated progress

created: "2026-02-05"
updated: "2026-02-06"
author: "analyst-annie"
---

# Specification content follows...
```

---

## API Specification

### 1. Priority Update Endpoint

```
PATCH /api/tasks/:id/priority
Content-Type: application/json

Request Body:
{
  "priority": "HIGH",
  "last_modified": "2026-02-06T10:00:00Z"  // Optimistic locking
}

Success Response (200 OK):
{
  "success": true,
  "task": {
    "id": "2026-02-05T1400-example",
    "title": "Implement Priority Edit API",
    "priority": "HIGH",
    "status": "in_progress",
    "updated": "2026-02-06T10:30:15Z"
  }
}

Error Responses:
400 Bad Request:
{
  "error": "Invalid priority value",
  "valid_values": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "normal"]
}

409 Conflict (In-Progress):
{
  "error": "Cannot change priority while task is in progress",
  "task_status": "in_progress",
  "agent": "backend-dev-benny"
}

409 Conflict (Concurrent Edit):
{
  "error": "Task was modified by another user",
  "current_modified": "2026-02-06T10:30:00Z",
  "your_modified": "2026-02-06T10:00:00Z"
}

404 Not Found:
{
  "error": "Task not found",
  "task_id": "2026-02-05T1400-example"
}
```

### 2. Portfolio Endpoint

```
GET /api/portfolio
Content-Type: application/json

Response (200 OK):
{
  "initiatives": [
    {
      "id": "SPEC-DASH-001",
      "title": "Dashboard Enhancements",
      "status": "in_progress",
      "priority": "HIGH",
      "progress": 65,           // Calculated or manual override
      "features": [
        {
          "id": "FEAT-DASH-001-01",
          "title": "Backend Priority API",
          "status": "in_progress",
          "progress": 60,       // From task completion
          "tasks": [
            {
              "id": "2026-02-05T1400-example",
              "title": "Implement Priority Edit API",
              "status": "in_progress",
              "priority": "HIGH"
            }
          ]
        }
      ],
      "specification_path": "specifications/llm-dashboard/task-priority-editing.md",
      "created": "2026-02-05",
      "updated": "2026-02-06"
    }
  ],
  "orphan_tasks": [
    // Tasks without specification links
    {
      "id": "2026-01-15T1000-legacy",
      "title": "Legacy Task Without Spec",
      "status": "inbox",
      "priority": "LOW"
    }
  ],
  "statistics": {
    "total_initiatives": 3,
    "active_initiatives": 2,
    "total_tasks": 47,
    "linked_tasks": 32,
    "orphan_tasks": 15
  }
}
```

### 3. WebSocket Events

```javascript
// Namespace: /dashboard

// Event: task.priority_changed
{
  "event": "task.priority_changed",
  "data": {
    "task_id": "2026-02-05T1400-example",
    "old_priority": "MEDIUM",
    "new_priority": "HIGH",
    "updated_by": "user@example.com",  // Future: multi-user support
    "timestamp": "2026-02-06T10:30:15Z"
  }
}

// Event: portfolio.updated
{
  "event": "portfolio.updated",
  "data": {
    "reason": "specification_modified",
    "spec_path": "specifications/llm-dashboard/task-priority-editing.md",
    "timestamp": "2026-02-06T10:35:00Z"
  }
}
```

---

## Security Architecture

### 1. XSS Prevention (ADR-036)

**Attack Surface:** Markdown rendering converts user input to HTML.

**Mitigations:**
1. **DOMPurify Sanitization:** Remove `<script>`, event handlers, `javascript:` URLs
2. **CSP Headers:** Block inline scripts, restrict script sources
3. **Limited HTML Whitelist:** Only allow safe tags (headings, lists, tables, links)
4. **URL Protocol Validation:** Only `http://` and `https://` allowed in links

**Test Coverage:**
- OWASP XSS filter evasion cheat sheet
- Unicode normalization attacks
- Malformed HTML edge cases

### 2. YAML Injection Prevention (ADR-035)

**Attack Surface:** Priority field written to YAML file.

**Mitigations:**
1. **Enum Validation:** Only allow whitelisted priority values
2. **Safe YAML Parser:** Use `yaml.safe_load()` (no code execution)
3. **File Path Validation:** Prevent `../` traversal, restrict to `work/` directory

**Test Coverage:**
- Attempt to inject YAML code execution payloads
- Path traversal attempts (`../../etc/passwd`)
- Invalid enum values

### 3. Path Traversal Prevention (ADR-037)

**Attack Surface:** Specification file paths from task `specification:` field.

**Mitigations:**
1. **Path Normalization:** Resolve to absolute path, check within `specifications/`
2. **Regex Validation:** Only alphanumeric, hyphens, slashes
3. **Symlink Detection:** Reject symlinks pointing outside allowed directories

**Test Coverage:**
- `specification: "../../../etc/passwd"`
- `specification: "/absolute/path"`
- Symlink attacks

---

## Performance Optimization

### 1. Caching Strategy

| Component | Cache Type | Invalidation Trigger | TTL |
|-----------|------------|----------------------|-----|
| Portfolio data | In-memory dict | File watcher event | None (event-driven) |
| Parsed specs | In-memory dict | Spec file modified | None (event-driven) |
| Rendered markdown | Browser cache | Task updated | 1 hour |

### 2. Lazy Loading

- **Marked.js/DOMPurify:** Load only when task modal first opened
- **Portfolio View:** Render only visible initiatives (virtual scrolling)
- **Task Details:** Fetch on-demand, not with initial task list

### 3. Benchmarks & SLOs

| Operation | P50 Target | P95 Target | P99 Target |
|-----------|------------|------------|------------|
| Priority update (end-to-end) | 150ms | 500ms | 1s |
| Markdown rendering (typical) | 20ms | 50ms | 200ms |
| Portfolio load (cached) | 30ms | 50ms | 100ms |
| Portfolio load (uncached, 50 specs) | 300ms | 500ms | 1s |

---

## Implementation Roadmap

### Phase 1: Markdown Rendering (ADR-036)
**Effort:** 9-11 hours  
**Priority:** Highest (no dependencies)

1. Integrate marked.js + DOMPurify (2h)
2. Implement selective rendering (3h)
3. Security hardening (2h)
4. Visual polish + testing (2-4h)

**Deliverables:**
- Markdown rendering in task modals
- XSS test suite passing
- Documentation updated

---

### Phase 2: Priority Editing (ADR-035)
**Effort:** 7-9 hours  
**Dependencies:** None (can run parallel to Phase 1)

1. Backend priority API (2-3h)
2. Frontend dropdown component (2-3h)
3. In-progress indicator (2h)
4. Integration testing (1h)

**Deliverables:**
- Editable priority dropdown
- In-progress task protection
- Real-time WebSocket updates

---

### Phase 3: Portfolio View (ADR-037)
**Effort:** 11-15 hours  
**Dependencies:** Requires Phases 1 & 2 complete (uses markdown + status indicators)

1. Specification parser (4h)
2. Task linker (3h)
3. Progress calculator (2h)
4. Portfolio API endpoint (2h)
5. Frontend portfolio view (5-8h)

**Deliverables:**
- Portfolio view with initiative hierarchy
- Progress rollup calculations
- Orphan task handling

**Optional MVP (Faster Launch):**
- Skip progress calculation (manual `completion:` only)
- Simple list view instead of accordion
- **Reduced effort:** 6-8 hours

---

## Testing Strategy

### Unit Tests

| Component | Test Coverage | Tools |
|-----------|---------------|-------|
| Priority validation | Valid/invalid enum values | pytest |
| YAML file operations | Comment preservation, atomic writes | pytest |
| Markdown parsing | Headings, lists, tables, code blocks | Jest |
| HTML sanitization | OWASP XSS payloads | Jest |
| Progress calculation | Various task status combinations | pytest |
| Spec frontmatter parsing | Valid/malformed YAML | pytest |

### Integration Tests

| Scenario | Validation | Tools |
|----------|------------|-------|
| Priority update E2E | PATCH → YAML updated → WebSocket received | Playwright |
| Markdown XSS prevention | Malicious markdown → sanitized HTML | Playwright |
| Portfolio load | Spec files → parsed → API response | pytest + requests |
| File watcher triggers | File change → cache invalidated → UI refreshed | pytest |

### Security Tests

| Attack Vector | Test | Expected Result |
|---------------|------|-----------------|
| XSS in markdown | `<script>alert(1)</script>` | Stripped by DOMPurify |
| YAML injection | `priority: "!!python/object/apply:os.system ['rm -rf /']"` | Rejected by validator |
| Path traversal | `specification: "../../../etc/passwd"` | 400 Bad Request |
| Concurrent edits | Two users update priority simultaneously | Optimistic locking prevents race |

---

## Rollout Plan

### Stage 1: Internal Testing (Week 1)
- Deploy to localhost
- Manual testing by human-in-charge
- Performance profiling
- Security testing

### Stage 2: Documentation (Week 1-2)
- Update dashboard quickstart guide
- Add specification writing guide
- Create video demo (optional)

### Stage 3: Production Deploy (Week 2)
- Merge to main branch
- Update `run_dashboard.py` if needed
- Announcement in project README

---

## Monitoring & Observability

### Metrics to Track

```python
# Priority editing
priority_updates_total              # Counter: Total priority changes
priority_update_errors_total        # Counter: Failed updates (by error type)
priority_update_duration_seconds    # Histogram: API latency

# Markdown rendering
markdown_render_duration_seconds    # Histogram: Render time
markdown_xss_blocked_total          # Counter: Sanitizer caught attack

# Portfolio
portfolio_load_duration_seconds     # Histogram: Load time
portfolio_cache_hit_ratio           # Gauge: Cache efficiency
portfolio_specs_parsed_total        # Counter: Specs parsed per request
```

### Logging

```python
# Priority update
logger.info("Priority updated", extra={
    "task_id": task_id,
    "old_priority": old_priority,
    "new_priority": new_priority,
    "user": user_id,
    "duration_ms": duration
})

# Security events
logger.warning("XSS attempt blocked", extra={
    "task_id": task_id,
    "field": field_name,
    "payload_snippet": payload[:100]
})

# Performance
logger.warning("Slow portfolio load", extra={
    "duration_ms": duration,
    "num_specs": num_specs,
    "cache_hit": cache_hit
})
```

---

## Migration & Backward Compatibility

### Existing Tasks
- ✅ **No breaking changes:** Tasks without `specification:` field continue working
- ✅ **Gradual migration:** Add `specification:` field during normal workflow
- ✅ **Orphan handling:** Unlinked tasks shown in separate portfolio section

### Existing Specifications
- ⚠️ **Requires frontmatter addition:** Existing specs lack frontmatter
- ✅ **Tooling support:** `ops/scripts/add-spec-frontmatter.py` automates migration
- ✅ **Validation:** `ops/scripts/validate-specs.py` checks schema compliance

### Dashboard Code
- ✅ **Backward compatible:** New features added, no existing features removed
- ✅ **Progressive enhancement:** Markdown rendering gracefully degrades to plain text
- ✅ **Feature detection:** Frontend checks API capabilities before using new endpoints

---

## Open Questions & Decisions

### Resolved

✅ **Q:** Should priority editing be allowed for `done` tasks?  
**A:** No, only `inbox` and `assigned` tasks are editable. (Stakeholder decision)

✅ **Q:** Which markdown library should we use?  
**A:** marked.js (best size/performance/features balance)

✅ **Q:** Should portfolio progress be manual or calculated?  
**A:** Calculated from tasks by default, manual override via `completion:` field

✅ **Q:** How to handle concurrent priority edits?  
**A:** Optimistic locking with `last_modified` timestamp check

### Pending

⚠️ **Q:** Should we add user authentication for multi-user support?  
**A:** Deferred to future enhancement (single-user local dashboard for now)

⚠️ **Q:** Should we support nested initiatives (hierarchy depth >2)?  
**A:** Deferred to future enhancement (single level: Initiative → Feature → Task)

---

## References

### ADRs
- [ADR-032: Real-Time Execution Dashboard](../adrs/ADR-032-real-time-execution-dashboard.md)
- [ADR-035: Dashboard Task Priority Editing](../adrs/ADR-035-dashboard-task-priority-editing.md)
- [ADR-036: Dashboard Markdown Rendering](../adrs/ADR-036-dashboard-markdown-rendering.md)
- [ADR-037: Dashboard Initiative Tracking](../adrs/ADR-037-dashboard-initiative-tracking.md)

### Specifications
- [Task Priority Editing Spec](../../specifications/llm-dashboard/task-priority-editing.md)
- [Markdown Rendering Spec](../../specifications/llm-dashboard/markdown-rendering.md)
- [Initiative Tracking Spec](../../specifications/llm-dashboard/initiative-tracking.md)

### External Documentation
- **marked.js:** https://marked.js.org/
- **DOMPurify:** https://github.com/cure53/DOMPurify
- **ruamel.yaml:** https://yaml.readthedocs.io/
- **OWASP XSS Prevention:** https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- **CommonMark Spec:** https://commonmark.org/
- **GitHub Flavored Markdown:** https://github.github.com/gfm/

---

**Document Owner:** Architect Alphonso  
**Review Cycle:** Quarterly  
**Next Review:** 2026-05-06  
**Change Log:**
- 2026-02-06: Initial version (v1.0.0)
