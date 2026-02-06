# Dashboard Enhancement: Specification-Driven Initiative Tracking

## Vision

Transform the dashboard from **task-level monitoring** to **initiative-level portfolio management** by integrating the `specifications/` folder as the strategic layer above tasks.

## Current State vs. Desired State

### Current Dashboard (Task-Level View)
```
┌─────────────────────────────────────────┐
│  Dashboard: Task Execution View         │
├─────────────────────────────────────────┤
│  Inbox (3)    Assigned (2)    Done (12) │
│  [task.yaml]  [task.yaml]     [...]     │
└─────────────────────────────────────────┘
```

**Limitation:** No way to see "What feature is this task building?"

---

### Desired Dashboard (Initiative → Feature → Task Hierarchy)
```
┌─────────────────────────────────────────────────────────┐
│  Dashboard: Portfolio View                              │
├─────────────────────────────────────────────────────────┤
│  Initiatives                                            │
│  ├─ M3: Cost Optimization (60% complete)                │
│  │  └─ Features:                                        │
│  │     ├─ Telemetry Infrastructure (✅ Implemented)     │
│  │     ├─ Policy Engine (🚧 In Progress - 40%)         │
│  │     └─ Cost Dashboard (📋 Planned)                  │
│  │                                                       │
│  ├─ M4: User Experience (80% complete)                  │
│  │  └─ Features:                                        │
│  │     ├─ Rich CLI (✅ Implemented)                     │
│  │     ├─ Real-Time Dashboard (✅ Implemented)          │
│  │     └─ Template Config (🚧 In Progress - 60%)       │
│  │                                                       │
│  └─ Task Queue (click to expand)                        │
│     ├─ Inbox: 3 tasks                                   │
│     ├─ Assigned: 2 tasks                                │
│     └─ Done: 12 tasks                                   │
└─────────────────────────────────────────────────────────┘
```

---

## Proposed Architecture

### 1. Specification Metadata Format

Add frontmatter to each specification in `specifications/`:

```markdown
---
id: llm-dashboard-001
title: "Real-Time Execution Dashboard"
status: Implemented
initiative: M4-User-Experience
priority: HIGH
completion: 100%
target_personas: [software-engineer, agentic-framework-core-team]
created: 2026-02-05
updated: 2026-02-06
author: analyst-annie
epic: dashboard-integration
features:
  - kanban-board
  - cost-tracking
  - websocket-events
---

# Specification: Real-Time Execution Dashboard
...
```

### 2. Task-to-Spec Linking

Enhance YAML task files with `specification` field:

```yaml
id: 2026-02-05T1400-backend-dev-rich-terminal-ui
title: "Rich Terminal UI Implementation"
specification: llm-dashboard/real-time-execution-dashboard  # NEW FIELD
milestone: M4
feature: rich-cli
...
```

### 3. Dashboard Backend Enhancements

**New Module:** `src/llm_service/dashboard/spec_tracker.py`

```python
class SpecificationTracker:
    """Track specifications and their implementation progress."""
    
    def __init__(self, spec_dir: str = 'specifications'):
        self.spec_dir = spec_dir
        self.specs = self._load_specifications()
    
    def _load_specifications(self) -> Dict[str, Specification]:
        """Parse all .md files in specifications/ for frontmatter."""
        # Parse YAML frontmatter from each spec
        # Return dict of spec_id -> Specification object
    
    def get_spec_progress(self, spec_id: str) -> SpecProgress:
        """Calculate progress based on linked tasks."""
        # Find all tasks with specification=spec_id
        # Calculate: (done_tasks / total_tasks) * 100
    
    def get_initiatives(self) -> List[Initiative]:
        """Group specs by initiative (M3, M4, etc.)."""
        # Group by frontmatter.initiative field
        # Return hierarchical structure
```

**Integration:** Wire into `file_watcher.py` to emit spec progress events

### 4. Dashboard UI Enhancements

**New Section:** "Portfolio View" (top of dashboard)

```html
<!-- Portfolio View: Initiative Progress -->
<section class="portfolio-view">
  <h2>🎯 Initiatives & Features</h2>
  
  <div class="initiative-card" data-initiative="M3">
    <div class="initiative-header">
      <h3>M3: Cost Optimization</h3>
      <div class="progress-bar">
        <div class="progress-fill" style="width: 60%"></div>
      </div>
      <span class="progress-text">60%</span>
    </div>
    
    <div class="feature-list">
      <div class="feature completed">
        ✅ Telemetry Infrastructure (specifications/llm-dashboard/telemetry.md)
      </div>
      <div class="feature in-progress">
        🚧 Policy Engine (40% complete, 2 tasks remaining)
      </div>
      <div class="feature planned">
        📋 Cost Dashboard (Not started)
      </div>
    </div>
  </div>
</section>
```

**Interactions:**
- Click initiative → Expand/collapse feature list
- Click feature → Show linked tasks
- Click task → Show task detail modal

---

## Implementation Plan

### Phase 1: Specification Metadata (2-3 hours)
**Agent:** Analyst Annie or Writer-Editor Sam

1. Create specification frontmatter schema
2. Add frontmatter to existing spec: `specifications/llm-dashboard/real-time-execution-dashboard.md`
3. Document specification metadata format in `specifications/README.md`

**Deliverables:**
- Frontmatter schema (YAML)
- Updated spec with metadata
- Documentation update

---

### Phase 2: Task-to-Spec Linking (1-2 hours)
**Agent:** Planning Petra or Backend-dev Benny

1. Add `specification` field to task YAML schema
2. Update existing tasks with spec references
3. Update task creation templates

**Deliverables:**
- Updated task schema in `work/collaboration/inbox/INDEX.md`
- Existing tasks tagged with specs
- Template updates

---

### Phase 3: Backend Spec Tracker (4-5 hours)
**Agent:** Backend-dev Benny or Python Pedro

1. Create `spec_tracker.py` module
2. Parse specification frontmatter (YAML)
3. Calculate progress based on linked tasks
4. Integrate with file_watcher.py
5. Add WebSocket events: `spec.progress_update`
6. Unit tests (>80% coverage)

**Deliverables:**
- `src/llm_service/dashboard/spec_tracker.py`
- Integration with file watcher
- REST API endpoint: `/api/initiatives`
- WebSocket events
- Unit tests

---

### Phase 4: Dashboard UI Portfolio View (3-4 hours)
**Agent:** Frontend specialist or Backend-dev Benny

1. Add Portfolio View section to `static/index.html`
2. Update CSS for initiative cards
3. Update JS to consume `/api/initiatives`
4. Add WebSocket handlers for spec progress
5. Add expand/collapse interactions

**Deliverables:**
- Updated `static/index.html`
- Updated `static/dashboard.css`
- Updated `static/dashboard.js`
- Visual regression tests

---

### Phase 5: Integration Testing (1-2 hours)
**Agent:** Backend-dev Benny or Test Agent

1. Create test specifications
2. Create test tasks linking to specs
3. Verify dashboard displays initiatives correctly
4. Verify progress calculation accuracy
5. E2E test: spec → tasks → dashboard update

**Deliverables:**
- Integration test suite
- Test data fixtures
- E2E validation

---

## Data Flow

```
Specifications (specifications/*.md)
  ↓ (frontmatter parsing)
SpecificationTracker
  ↓ (tracks progress)
Task YAML files (work/collaboration/*.yaml)
  ↓ (file watcher events)
WebSocket events (spec.progress_update)
  ↓ (real-time push)
Dashboard UI (Portfolio View)
```

---

## Benefits

### For Users
✅ **Strategic Visibility**: See feature/initiative progress, not just tasks
✅ **Context Understanding**: Tasks linked to specifications provide "why"
✅ **Portfolio Management**: Track multiple initiatives simultaneously
✅ **Planning Insight**: Identify which features are blocked or at risk

### For Framework
✅ **Spec-First Culture**: Specifications become living documents with real-time status
✅ **Traceability**: Tasks → Specs → Initiatives → Business Goals
✅ **Agent Coordination**: Agents see which features need work next
✅ **Metrics**: Initiative-level completion tracking for reporting

---

## Example Use Cases

### Use Case 1: Morning Standup
**Scenario:** Team lead opens dashboard for daily review

**Current Dashboard:**
- "12 tasks done, 3 in inbox" ← No strategic context

**Enhanced Dashboard:**
- "M3 Cost Optimization: 60% complete (Policy Engine in progress)"
- "M4 User Experience: 80% complete (Dashboard implemented, Templates 60% done)"
- ← Clear initiative status

---

### Use Case 2: Sprint Planning
**Scenario:** Planning Petra identifies next batch

**Current Process:**
- Read NEXT_BATCH.md
- Read agent status
- Manually track feature completion

**Enhanced Process:**
- Open dashboard
- See "M3 Telemetry: Ready (all specs complete)"
- See "M4 Templates: 60% done (2 tasks remaining)"
- Make data-driven prioritization decision

---

### Use Case 3: Stakeholder Reporting
**Scenario:** Human needs to report progress

**Current:**
- "We completed 12 tasks this week" ← Not meaningful to stakeholders

**Enhanced:**
- "We completed Real-Time Dashboard feature (M4 milestone now 80% done)"
- "Next: Cost Optimization initiative (M3) starting next sprint"
- ← Business-level language

---

## Open Questions

1. **Specification Granularity:**
   - Should every task reference a spec, or only complex features?
   - **Recommendation:** Optional field, use for features spanning 3+ tasks

2. **Completion Calculation:**
   - Should we use task counts or estimated hours?
   - **Recommendation:** Task counts (simpler), optionally weight by complexity

3. **Initiative Definition:**
   - How do we define initiatives (milestones, epics, quarters)?
   - **Recommendation:** Use milestone notation (M1, M2, M3) initially

4. **Spec Status Automation:**
   - Should spec status auto-update based on tasks, or manual?
   - **Recommendation:** Hybrid - auto-calculate progress, manual status field

---

## Success Metrics

- **Adoption:** 80% of tasks link to specifications within 2 weeks
- **Visibility:** Dashboard shows 3+ initiatives with real-time progress
- **Usage:** Human opens dashboard 2+ times per day for planning
- **Feedback:** Stakeholders prefer initiative view over task list

---

## Estimated Effort

| Phase | Hours | Agent |
|-------|-------|-------|
| Phase 1: Spec Metadata | 2-3 | Analyst Annie |
| Phase 2: Task Linking | 1-2 | Planning Petra |
| Phase 3: Backend Tracker | 4-5 | Backend-dev Benny |
| Phase 4: UI Portfolio View | 3-4 | Backend-dev Benny |
| Phase 5: Integration Tests | 1-2 | Backend-dev Benny |
| **Total** | **11-16 hours** | **~2-3 days** |

---

## Recommendation

**PROCEED** with this enhancement. It aligns perfectly with:
- ✅ Spec-Driven Development approach (Directive 034)
- ✅ Traceable Decisions (Directive 018)
- ✅ Work Directory Orchestration
- ✅ Dashboard vision (ADR-032)

**Priority:** MEDIUM-HIGH (after M3.1 Telemetry, before M4.3 MCP Server)

**Next Step:** Create tasks for Phase 1-5 in `work/collaboration/inbox/`
