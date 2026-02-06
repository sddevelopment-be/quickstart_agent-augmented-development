# ADR-037: Dashboard Initiative Tracking (Portfolio View)

**Status:** Proposed  
**Date:** 2026-02-06  
**Deciders:** Architect Alphonso, Human-in-Charge  
**Related Specs:** [Initiative Tracking Specification](../../specifications/llm-dashboard/initiative-tracking.md)  
**Related ADRs:** 
- [ADR-032: Real-Time Execution Dashboard](ADR-032-real-time-execution-dashboard.md)
- [ADR-034: MCP Server Integration Strategy](ADR-034-mcp-server-integration-strategy.md) (potential future integration)

---

## Context

The dashboard currently displays tasks in a flat list grouped by status (inbox, assigned, done). When working on complex features that span multiple tasks across specifications, epics, and initiatives, users lose strategic context. There's no visibility into:

- Which initiatives are in progress
- How features map to specifications
- Progress rollup (% complete across related tasks)
- Strategic priorities vs. operational tasks

**Problem Statement:**  
Engineers need portfolio-level visibility to understand how daily tasks connect to strategic goals and track initiative progress.

**Constraints:**
- MUST leverage existing specification files (`specifications/`) as source of truth
- MUST preserve file-based orchestration (no separate database)
- MUST NOT duplicate metadata (specifications define initiatives/features)
- MUST maintain backward compatibility with existing tasks (optional `specification:` field)

---

## Decision

Implement a portfolio view that parses specification frontmatter to construct initiative/feature/task hierarchies with automated progress calculation.

### Solution Components

**1. Specification Metadata Schema**

Specifications use YAML frontmatter to define initiatives and features:

```yaml
---
id: "INIT-002"
title: "LLM Service Layer & Dashboard"
status: "in_progress"
initiative: "Execution Visibility"
priority: "HIGH"
epic: "Agent Monitoring"
target_personas: ["devops-danny", "architect-alphonso"]
features:
  - id: "FEAT-002-01"
    title: "Real-Time Task Dashboard"
    status: "done"
  - id: "FEAT-002-02"
    title: "Task Priority Editing"
    status: "in_progress"
completion: 65
created: "2026-01-15"
updated: "2026-02-05"
author: "analyst-annie"
---

# Specification Title

Rest of markdown specification...
```

**2. Task Linking to Specifications**

Tasks link to specifications via `specification:` field:

```yaml
id: "2026-02-05T1400-task-priority-edit-backend"
title: "Implement Priority Edit API Endpoint"
specification: "specifications/llm-dashboard/task-priority-editing.md"
status: "in_progress"
priority: "HIGH"
```

**3. Data Aggregation Architecture**

```
┌────────────────────────────────────────────────┐
│  Specification Parser (Python)                 │
│  - Scan specifications/ directory              │
│  - Parse YAML frontmatter                      │
│  - Extract initiative/feature metadata         │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  Task Linker                                   │
│  - Find tasks with `specification:` field      │
│  - Group tasks by specification ID             │
│  - Calculate task completion (done/total)      │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  Progress Calculator                           │
│  - Aggregate task completion by feature        │
│  - Roll up feature completion to initiative    │
│  - Calculate weighted progress percentages     │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  Portfolio Data Model                          │
│  {                                             │
│    "initiatives": [                            │
│      {                                         │
│        "id": "INIT-002",                       │
│        "title": "LLM Service Layer",           │
│        "progress": 65,                         │
│        "features": [                           │
│          {                                     │
│            "id": "FEAT-002-01",                │
│            "progress": 100,                    │
│            "tasks": [...]                      │
│          }                                     │
│        ]                                       │
│      }                                         │
│    ]                                           │
│  }                                             │
└────────────────┬───────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────┐
│  Dashboard Portfolio View                      │
│  - Hierarchical accordion UI                   │
│  - Progress bars with percentages              │
│  - Drill-down: Initiative → Feature → Task     │
└────────────────────────────────────────────────┘
```

**4. API Endpoint**

```
GET /api/portfolio
Response: {
  "initiatives": [
    {
      "id": "INIT-002",
      "title": "LLM Service Layer & Dashboard",
      "status": "in_progress",
      "priority": "HIGH",
      "progress": 65,
      "features": [
        {
          "id": "FEAT-002-02",
          "title": "Task Priority Editing",
          "specification": "specifications/llm-dashboard/task-priority-editing.md",
          "status": "in_progress",
          "progress": 40,
          "tasks": [
            {
              "id": "2026-02-05T1400-task-priority-edit-backend",
              "title": "Implement Priority Edit API Endpoint",
              "status": "in_progress"
            }
          ]
        }
      ]
    }
  ],
  "orphan_tasks": [
    // Tasks without specification links
  ]
}
```

**5. Frontend Portfolio View**

```
┌─────────────────────────────────────────────────────┐
│  Portfolio View                                     │
│                                                     │
│  📊 Initiatives (2 active, 1 completed)             │
│                                                     │
│  ▼ 🎯 LLM Service Layer & Dashboard       [65%] ▓▓▓▓░│
│     Status: In Progress | Priority: HIGH          │
│     Features:                                      │
│     ├─ ✅ Real-Time Task Dashboard        [100%]  │
│     ├─ 🔄 Task Priority Editing            [40%]  │
│     │    Tasks:                                    │
│     │    ├─ ✅ Create specification               │
│     │    ├─ 🔄 Implement backend API              │
│     │    └─ ⏳ Frontend integration               │
│     └─ ⏳ Markdown Rendering                [0%]   │
│                                                     │
│  ▼ 🎯 Telemetry Infrastructure            [30%] ▓░░░░│
│     Status: In Progress | Priority: MEDIUM        │
│     ...                                            │
│                                                     │
│  📝 Orphan Tasks (5)                                │
│     Tasks without specification links...           │
└─────────────────────────────────────────────────────┘
```

---

## Alternatives Considered

### Alternative 1: Manual Initiative YAML Files (Rejected)
**Approach:** Create separate `work/initiatives/*.yaml` files for initiatives  
**Pros:** Explicit initiative definitions, easier to parse  
**Cons:** Duplicate metadata from specs, synchronization burden, violates DRY  
**Decision:** Specifications already contain this metadata—reuse it

### Alternative 2: Database-Backed Portfolio (Rejected)
**Approach:** Import specs/tasks into SQLite, query for hierarchies  
**Pros:** Fast queries, complex aggregations easy  
**Cons:** Violates file-based orchestration, adds state synchronization complexity  
**Decision:** File system remains source of truth per ADR-032

### Alternative 3: GitHub Projects API Integration (Rejected)
**Approach:** Sync with GitHub Projects for portfolio view  
**Pros:** Leverage existing GitHub tooling  
**Cons:** External dependency, API rate limits, network latency, not local-first  
**Decision:** Local file-based solution keeps dashboard self-contained

### Alternative 4: Hardcoded Initiative List (Rejected)
**Approach:** Manually define initiatives in dashboard config file  
**Pros:** Simple, no parsing needed  
**Cons:** Rigid, requires dashboard code changes for new initiatives  
**Decision:** Dynamic parsing from specs provides flexibility

---

## Consequences

### Positive

- ✅ **Strategic Visibility:** Engineers see how tasks connect to initiatives
- ✅ **Single Source of Truth:** Specifications define initiatives/features (no duplication)
- ✅ **Automated Progress:** No manual progress updates—calculated from task status
- ✅ **Backward Compatible:** Tasks without `specification:` field still work (orphan section)
- ✅ **Specification-Driven Workflow:** Reinforces Directive 034 (write specs before tasks)

### Negative

- ⚠️ **Parsing Overhead:** Scanning all specifications on every request adds latency
- ⚠️ **Frontmatter Coupling:** Dashboard depends on spec frontmatter schema stability
- ⚠️ **Progress Accuracy:** Calculated progress may diverge from subjective assessment
- ⚠️ **Orphan Task Clutter:** Many existing tasks lack `specification:` field

### Mitigations

- **Parsing Overhead:** Cache parsed specs in memory, invalidate on file change (file watcher)
- **Frontmatter Coupling:** Define schema in `specifications/schema.json`, validate on save
- **Progress Accuracy:** Allow manual `completion:` override in spec frontmatter
- **Orphan Tasks:** Gradual migration—link tasks to specs during normal workflow

---

## Implementation Plan

### Phase 1: Specification Parser (4 hours)
- Create `SpecificationParser` class
- Parse YAML frontmatter from markdown files
- Extract initiative/feature metadata
- Unit tests: Valid/invalid frontmatter, edge cases

### Phase 2: Task Linker (3 hours)
- Find tasks with `specification:` field
- Group tasks by specification ID
- Handle missing/invalid spec references
- Unit tests: Task grouping, orphan detection

### Phase 3: Progress Calculator (2 hours)
- Implement task-to-feature rollup
- Implement feature-to-initiative rollup
- Handle mixed status scenarios (in_progress, done, blocked)
- Unit tests: Progress calculation accuracy

### Phase 4: API Endpoint (2 hours)
- Create `/api/portfolio` endpoint
- Wire parser, linker, calculator
- Add caching layer (file watcher invalidation)
- Integration tests: End-to-end data flow

### Phase 5: Frontend Portfolio View (5-8 hours)
- Create hierarchical accordion component
- Render progress bars with percentages
- Drill-down navigation
- Responsive design (mobile/desktop)
- UI tests: Interaction, visual regression

**Total Effort:**  
- **Full Implementation:** 16-19 hours  
- **MVP (Initiative List Only):** 8-10 hours (no progress calculation, no task linking)

---

## Technical Design

### Data Models

```python
# Specification Metadata (from frontmatter)
@dataclass
class SpecificationMetadata:
    id: str              # e.g., "INIT-002"
    title: str
    status: str          # "draft" | "in_progress" | "implemented" | "deprecated"
    initiative: str      # High-level grouping
    priority: str        # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    epic: Optional[str]  # Optional epic grouping
    features: List[Feature]
    completion: Optional[int]  # Manual override (0-100)
    created: str         # ISO date
    updated: str
    author: str

@dataclass
class Feature:
    id: str              # e.g., "FEAT-002-01"
    title: str
    status: str
    specification_path: str  # Path to specification file

# Task Link (from task YAML)
@dataclass
class TaskLink:
    task_id: str
    specification_id: str
    status: str
    priority: str

# Portfolio Aggregate
@dataclass
class PortfolioInitiative:
    metadata: SpecificationMetadata
    features: List[FeatureProgress]
    calculated_progress: int  # 0-100

@dataclass
class FeatureProgress:
    metadata: Feature
    tasks: List[TaskLink]
    calculated_progress: int  # % of tasks done
```

### Progress Calculation Algorithm

```python
def calculate_feature_progress(feature: Feature, tasks: List[Task]) -> int:
    """
    Calculate feature completion percentage from linked tasks.
    
    Logic:
    - done: 100% weight
    - in_progress: 50% weight
    - blocked: 25% weight
    - inbox/assigned: 0% weight
    """
    if not tasks:
        return 0
    
    weights = {"done": 1.0, "in_progress": 0.5, "blocked": 0.25}
    total_weight = sum(weights.get(t.status, 0) for t in tasks)
    return int((total_weight / len(tasks)) * 100)

def calculate_initiative_progress(initiative: Initiative) -> int:
    """
    Roll up feature progress to initiative level.
    
    If manual `completion:` field exists in spec frontmatter, use it.
    Otherwise, calculate as weighted average of feature progress.
    """
    if initiative.metadata.completion is not None:
        return initiative.metadata.completion
    
    if not initiative.features:
        return 0
    
    avg_progress = sum(f.calculated_progress for f in initiative.features) / len(initiative.features)
    return int(avg_progress)
```

### Caching Strategy

```python
class PortfolioCache:
    """
    In-memory cache invalidated by file watcher events.
    """
    def __init__(self):
        self._cache = None
        self._last_update = None
        self._spec_mtimes = {}  # {path: mtime}
    
    def get(self) -> Optional[PortfolioData]:
        if self._cache is None:
            return None
        
        # Check if any spec file modified
        for path, cached_mtime in self._spec_mtimes.items():
            current_mtime = os.path.getmtime(path)
            if current_mtime != cached_mtime:
                self._cache = None  # Invalidate
                return None
        
        return self._cache
    
    def set(self, data: PortfolioData):
        self._cache = data
        self._last_update = time.time()
        # Record mtimes for all specs
        self._spec_mtimes = {
            spec.path: os.path.getmtime(spec.path)
            for spec in data.specifications
        }
```

### File Watcher Integration

```python
# Extend existing FileWatcher to monitor specifications/
class SpecificationWatcher(FileWatcher):
    def __init__(self, specs_dir: str, portfolio_cache: PortfolioCache):
        super().__init__(specs_dir)
        self.cache = portfolio_cache
    
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            # Specification changed—invalidate cache
            self.cache.invalidate()
            # Emit WebSocket event for UI refresh
            emit('portfolio.updated', {}, namespace='/dashboard')
```

---

## Security Considerations

### Path Traversal Prevention
- Validate `specification:` field contains relative path within `specifications/`
- Reject paths with `../` or absolute paths
- Sanitize file paths before filesystem access

### YAML Injection Prevention
- Parse frontmatter with `safe_load` (no code execution)
- Validate frontmatter schema (reject unknown fields)
- Limit frontmatter size (<10KB)

### Denial of Service
- Limit specification directory depth (max 5 levels)
- Cap number of specifications scanned (<1000)
- Timeout spec parsing (5 seconds max)

---

## Performance Characteristics

### Benchmarks (Target)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Initial portfolio load | <500ms | Parse specs + aggregate |
| Cached portfolio load | <50ms | Memory read |
| Spec parsing (typical) | <10ms | YAML frontmatter only |
| Progress calculation | <20ms | Task aggregation |
| WebSocket update latency | <100ms | Cache invalidation → broadcast |

### Scalability

| Scale Factor | Performance | Notes |
|--------------|-------------|-------|
| 10 specifications | <200ms | Typical small project |
| 50 specifications | <500ms | Medium project (current target) |
| 200 specifications | <2s | Large project (may need optimization) |

**Optimization strategies for large projects:**
- Background pre-calculation (update cache on timer)
- Incremental parsing (only changed specs)
- Spec metadata index file (avoid parsing on every load)

---

## Testing Strategy

### Unit Tests
- Frontmatter parsing (valid/invalid YAML)
- Feature extraction from specs
- Task linking (valid/missing/orphan tasks)
- Progress calculation accuracy
- Cache invalidation logic

### Integration Tests
- End-to-end: Spec file → parsed metadata → API response
- File watcher triggers cache invalidation
- WebSocket events broadcast to connected clients

### Manual Tests
- Create new specification, verify appears in portfolio
- Link task to spec, verify progress updates
- Modify spec frontmatter, verify cache invalidates
- Large spec directory (100+ files) load time

---

## Migration Strategy

### Existing Tasks Without `specification:` Field

**Option 1: Gradual Migration (Recommended)**
- Display orphan tasks in separate "Unlinked Tasks" section
- As tasks are worked on, add `specification:` field
- No breaking changes, backward compatible

**Option 2: Bulk Linking Script**
- Create script to auto-link tasks based on title matching
- Manual review required (high error rate)
- One-time effort, cleaner result

**Decision:** Option 1 (gradual migration) chosen for safety and flexibility.

### Specification Frontmatter Migration

**Current state:** Some specifications lack frontmatter (pure markdown)

**Migration plan:**
1. **Phase 1:** Add minimal frontmatter (id, title, status) to existing specs
2. **Phase 2:** Add features array as features are defined
3. **Phase 3:** Link tasks to specs during normal workflow

**Tooling support:**
- Create `ops/scripts/add-spec-frontmatter.py` to bootstrap frontmatter
- Validate schema with `ops/scripts/validate-specs.py`

---

## Open Questions

✅ All resolved with stakeholder.

---

## Future Enhancements

### Near-Term (Next 6 Months)
1. **Gantt Chart View:** Timeline visualization of initiatives/features
2. **Burndown Charts:** Track velocity and completion trends
3. **Dependency Mapping:** Visualize task/feature dependencies
4. **Spec Templates:** Auto-generate spec frontmatter from templates

### Long-Term (6-12 Months)
1. **GitHub Projects Sync:** Bidirectional sync with GitHub Projects (Optional)
2. **Portfolio Analytics:** Historical progress trends, velocity metrics
3. **AI Insights:** Predict completion dates, identify blockers
4. **Multi-Repository Portfolios:** Aggregate across multiple codebases

---

## References

- **Specification:** `specifications/llm-dashboard/initiative-tracking.md`
- **Directive 034:** Spec-Driven Development
- **ADR-032:** Real-Time Execution Dashboard
- **Proposal:** `docs/planning/dashboard-spec-integration-proposal.md`
- **YAML Frontmatter Spec:** https://jekyllrb.com/docs/front-matter/
- **Python YAML Parser:** https://pyyaml.org/

---

**Author:** Architect Alphonso  
**Reviewers:** Human-in-Charge, Backend-dev Benny, Analyst Annie  
**Status:** Proposed (awaiting approval)  
**Next Steps:** 
1. Stakeholder approval
2. Create `specifications/schema.json` (frontmatter validation)
3. Create implementation tasks
4. Assign to Backend-dev Benny (parser) + Frontend (UI)
