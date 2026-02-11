# Next Steps: Doctrine Code Representations Implementation

**Date:** 2026-02-11  
**Source:** `work/reports/architecture/architectural-analysis-doctrine-code-representations.md`  
**Status:** Action Items Ready

---

## Summary

Architect Alphonso has created the comprehensive architectural analysis for **doctrine code representations** that was referenced as approved by @stijn-dejongh. The analysis defines:

1. **Domain model** for doctrine concepts (Agent, Directive, Tactic, Approach, StyleGuide, Template)
2. **Orchestration concepts** (Batch, Iteration, Cycle)
3. **Module refactoring** strategy (`src/common/` → `src/domain/`)
4. **Implementation phases** (7 weeks, 120 hours estimated)
5. **ACL/adapter strategy** for vendor tool distribution

---

## Immediate Action Items

### 1. ADR Creation (Backend Benny + Architect Alphonso)

**Create ADR-045: Doctrine Code Representations**
- **Location:** `docs/architecture/adrs/ADR-045-doctrine-code-representations.md`
- **Content:** Document decision to create Python dataclasses for doctrine concepts
- **Key Sections:**
  - Context: Why we need code representations
  - Decision: Use dataclasses with validation
  - Consequences: Type safety, UI inspection, vendor export capability
  - Implementation: Reference §2 of architectural analysis
- **Status:** Draft → Review → Accepted
- **Estimated:** 2 hours

**Create ADR-046: Domain Layer Refactoring**
- **Location:** `docs/architecture/adrs/ADR-046-domain-layer-refactoring.md`
- **Content:** Document decision to refactor `src/common/` → `src/domain/`
- **Key Sections:**
  - Context: Current `src/common/` mixes utilities with domain concepts
  - Decision: Create `src/domain/{collaboration,doctrine,specifications,common}/`
  - Consequences: Clear domain boundaries, better organization
  - Migration: Reference §3 of architectural analysis
- **Status:** Draft → Review → Accepted
- **Estimated:** 2 hours

**Template:** Use `docs/templates/architecture/adr.md`

---

### 2. Architectural Overview Update (Architect Alphonso)

**Update:** `docs/architecture/README.md`

**Add Section: "Domain Layer Architecture"**

```markdown
## Domain Layer Architecture

The domain layer (`src/domain/`) represents core business concepts and provides type-safe abstractions for:

- **Collaboration Domain** (`collaboration/`) - Agents, tasks, batches, iterations
- **Doctrine Domain** (`doctrine/`) - Directives, tactics, approaches, style guides
- **Specifications Domain** (`specifications/`) - Specs, features, initiatives
- **Common Domain** (`common/`) - Shared types and exceptions

### Dependency Direction

```
Configuration (doctrine/, work/) 
    ↓ (read by)
Domain Layer (src/domain/) 
    ↓ (used by)
Framework Layer (src/framework/) 
    ↓ (used by)
Application Layer (tools/, dashboard/)
```

### Design Principles

1. **Domain objects are immutable** (dataclasses with `frozen=True`)
2. **Validation at boundaries** (fail fast on invalid config)
3. **No circular dependencies** (strict layering)
4. **Single source of truth** (doctrine configs → domain objects)

See: `work/reports/architecture/architectural-analysis-doctrine-code-representations.md`
```

**Estimated:** 1 hour

---

### 3. REPO_MAP.md Update (Curator Claire)

**Update:** `REPO_MAP.md`

**Add `src/domain/` Structure:**

```markdown
## Source Code Structure

### Domain Layer (NEW)

```
src/domain/
├── collaboration/      # Agent coordination & orchestration
│   ├── agent.py        # AgentProfile domain object
│   ├── task.py         # Task domain object
│   ├── batch.py        # Batch orchestration concept
│   ├── iteration.py    # Iteration planning cycle
│   └── cycle.py        # Recurring process cycles
├── doctrine/           # Doctrine framework artifacts
│   ├── directive.py    # Directive domain object
│   ├── tactic.py       # Tactic + TacticStep
│   ├── approach.py     # Strategic approaches
│   ├── style_guide.py  # StyleGuide + StyleRule
│   └── template.py     # Template + TemplateSection
├── specifications/     # Specification tracking
│   ├── specification.py  # Spec domain object
│   └── feature.py        # Feature tracking
└── common/             # Shared utilities
    ├── types.py        # Enums (TaskStatus, etc.)
    └── exceptions.py   # Shared exceptions
```

**Status:**
- ⚠️ Migration in progress (see ADR-046)
- Old `src/common/` deprecated, will be removed in Phase 6
```

**Mark `src/common/` as Deprecated:**

```markdown
### Common Utilities (DEPRECATED - Migration to src/domain/)

> **Note:** This directory is being refactored into `src/domain/` per ADR-046.
> See: `work/reports/architecture/architectural-analysis-doctrine-code-representations.md`

Current files:
- `types.py` → Moving to `src/domain/common/types.py`
- `task_schema.py` → Moving to `src/domain/collaboration/task.py`
- `agent_loader.py` → Moving to `src/domain/collaboration/agent.py`
```

**Estimated:** 1 hour

---

### 4. Dependency Direction Check (Curator Claire)

**Task:** Check `doctrine/` artifacts for references to repository-specific ADRs

**Rationale (from architectural analysis §4.2):**
> **Rule 1: Domain Layer NEVER Depends on Repository-Specific Artifacts**
> - ✅ `src/domain/doctrine/directive.py` loads `doctrine/directives/*.md`
> - ❌ `src/domain/doctrine/directive.py` does NOT load `docs/architecture/adrs/*.md`
> - **Rationale:** ADRs are repository-specific; directives are framework-level

**Action:**
```bash
# Search for ADR references in doctrine/
grep -r "ADR-[0-9]" doctrine/

# If found, assess:
# 1. Is the reference necessary? (likely NOT - directives should be self-contained)
# 2. Can it be rephrased as a general principle?
# 3. Should it reference a Tactic or Approach instead?
```

**Report Findings:**
- Create: `work/reports/curation/2026-02-11-doctrine-adr-dependency-check.md`
- Document:
  - Files with ADR references
  - Assessment of each reference
  - Recommended fixes (if needed)

**Estimated:** 2 hours

---

### 5. Orchestration Agent Role Assessment (Manager Mike)

**Task:** Assess if batch/iteration/cycle orchestration fits Manager Mike's role

**Context (from architectural analysis §2.2.2):**
The domain model includes:
- **Batch** - Grouped tasks for execution
- **Iteration** - Planning cycle with phases
- **Cycle** - Recurring process with rhythm

**Question:** Should Manager Mike take on orchestration responsibilities?

**Current Manager Mike Profile:**
- Specialization: Project management, task prioritization, agent coordination
- Does NOT explicitly include: Batch planning, iteration management, cycle automation

**Options:**

**Option 1: Extend Manager Mike's Profile ✅ RECOMMENDED**
- Add to `doctrine/agents/manager-mike.agent.md`:
  - Primary focus: "Batch planning and iteration management"
  - Output artifacts: Add "Batch plans", "Iteration retrospectives"
  - Required directives: Add directive for orchestration (if it exists)

**Option 2: Create New "Orchestrator Otto" Agent ⚠️ COMPLEX**
- Separate orchestration concerns from project management
- Pros: Clear separation of concerns
- Cons: More agents to maintain, overlap with Manager Mike

**Option 3: Keep Orchestration in Scripts ❌ NOT RECOMMENDED**
- Leave batch/iteration logic in `run_dashboard.py`, `tools/cycle_orchestrator.sh`
- Cons: No agent ownership, harder to track responsibility

**Recommendation:** Option 1 (extend Manager Mike's profile)

**Action:**
- Create: `work/reports/assessments/2026-02-11-manager-mike-orchestration-role.md`
- Document:
  - Current role analysis
  - Proposed extensions
  - Trade-offs
  - Decision recommendation

**Estimated:** 2 hours

---

### 6. Initiative Creation (Planning Petra)

**Create Initiative:**
- **Location:** `specifications/initiatives/doctrine-code-representations-implementation.md`
- **Status:** Planned
- **Duration:** 7 weeks (120 hours estimated)
- **Phases:** 6 implementation phases (see architectural analysis §6)

**Initiative Structure:**

```markdown
# Initiative: Doctrine Code Representations Implementation

**Status:** Planned  
**Priority:** HIGH (blocking vendor tool distribution)  
**Estimated Duration:** 7 weeks (120 hours)  
**Dependencies:** ADR-042 (Shared Task Domain Model)

## Objective

Implement Python domain objects for doctrine concepts and orchestration abstractions to enable:
1. UI inspection (dashboard, CLI)
2. Vendor tool distribution (OpenCode, Cursor, Cody)
3. Type-safe domain modeling

## Phases

### Phase 1: Core Domain Objects (Week 1, 16 hours)
- Create src/domain/ structure
- Implement doctrine domain objects (Directive, Tactic, Approach, StyleGuide, Template)
- Write unit tests

**Tasks:**
- TASK-DOMAIN-001: Create src/domain/ package structure
- TASK-DOMAIN-002: Implement Directive domain object + loader
- TASK-DOMAIN-003: Implement Tactic domain object + loader
- TASK-DOMAIN-004: Implement Approach domain object + loader
- TASK-DOMAIN-005: Implement StyleGuide domain object + loader
- TASK-DOMAIN-006: Implement Template domain object + loader
- TASK-DOMAIN-007: Write unit tests for doctrine domain

### Phase 2: Collaboration Domain (Week 2, 20 hours)
- Migrate agent_loader.py → src/domain/collaboration/agent.py
- Enhance task_schema.py → src/domain/collaboration/task.py
- Implement Batch, Iteration, Cycle concepts

**Tasks:**
- TASK-DOMAIN-008: Migrate agent_loader to domain layer
- TASK-DOMAIN-009: Enhance task schema with Task domain object
- TASK-DOMAIN-010: Implement Batch domain object
- TASK-DOMAIN-011: Implement Iteration domain object
- TASK-DOMAIN-012: Implement Cycle domain object
- TASK-DOMAIN-013: Update framework orchestration to use domain objects

### Phase 3: File Loaders & Parsers (Week 3, 24 hours)
- Implement robust YAML/Markdown parsers
- Add caching layer
- Handle edge cases

**Tasks:**
- TASK-DOMAIN-014: Implement directive loader
- TASK-DOMAIN-015: Implement tactic loader
- TASK-DOMAIN-016: Implement approach loader
- TASK-DOMAIN-017: Implement style guide loader
- TASK-DOMAIN-018: Implement template loader
- TASK-DOMAIN-019: Add caching layer
- TASK-DOMAIN-020: Write loader tests

### Phase 4: Validation Logic (Week 4, 16 hours)
- Implement validation rules
- Cross-reference validation
- CLI validation command

**Tasks:**
- TASK-DOMAIN-021: Implement AgentProfile validation
- TASK-DOMAIN-022: Implement Directive validation
- TASK-DOMAIN-023: Implement Tactic validation
- TASK-DOMAIN-024: Implement cross-reference validation
- TASK-DOMAIN-025: Create CLI validation command
- TASK-DOMAIN-026: Write validation tests

### Phase 5: UI/Export Integrations (Week 5-6, 32 hours)
- Dashboard pages for doctrine inspection
- CLI inspection commands
- Adapter layer for vendor tools

**Tasks:**
- TASK-DOMAIN-027: Create dashboard agents page
- TASK-DOMAIN-028: Create dashboard directives page
- TASK-DOMAIN-029: Create dashboard doctrine stack page
- TASK-DOMAIN-030: Implement CLI show agents command
- TASK-DOMAIN-031: Implement CLI show directives command
- TASK-DOMAIN-032: Implement CLI inspect stack command
- TASK-DOMAIN-033: Implement CLI check compliance command
- TASK-DOMAIN-034: Implement adapter base interface
- TASK-DOMAIN-035: Implement OpenCode adapter
- TASK-DOMAIN-036: Implement Cursor adapter
- TASK-DOMAIN-037: Implement CLI export command
- TASK-DOMAIN-038: Write integration tests

### Phase 6: Migration & Cleanup (Week 7, 12 hours)
- Update all import paths
- Remove old src/common/ files
- Update documentation

**Tasks:**
- TASK-DOMAIN-039: Update framework imports
- TASK-DOMAIN-040: Update dashboard imports
- TASK-DOMAIN-041: Update tools imports
- TASK-DOMAIN-042: Update scripts imports
- TASK-DOMAIN-043: Remove old src/common/ files
- TASK-DOMAIN-044: Update architectural documentation
- TASK-DOMAIN-045: Run full test suite
- TASK-DOMAIN-046: Create ADR-045 and ADR-046

## Success Criteria

- ✅ All doctrine/*.md files parse into domain objects
- ✅ Dashboard displays doctrine artifacts
- ✅ CLI inspection commands work
- ✅ Export to 2+ vendor tools (OpenCode, Cursor)
- ✅ Test coverage >80% (domain layer >90%)
- ✅ No circular dependencies

## References

- Architectural Analysis: `work/reports/architecture/architectural-analysis-doctrine-code-representations.md`
- ADR-042: Shared Task Domain Model
- ADR-045: Doctrine Code Representations (to be created)
- ADR-046: Domain Layer Refactoring (to be created)
```

**Create Tasks:**
- Use template: `doctrine/templates/task.md`
- Create 46 tasks (TASK-DOMAIN-001 through TASK-DOMAIN-046)
- Location: `work/collaboration/tasks/`
- Assign phases to iterations

**Estimated:** 4 hours (initiative + tasks)

---

### 7. Cross-Reference Updates (Planning Petra)

**Update Existing Initiatives:**

**SPEC-DIST-001: Vendor Tool Distribution**
- Location: `specifications/features/SPEC-DIST-001-vendor-tool-distribution.md`
- Add reference to adapter layer (§5.2 of architectural analysis)
- Update technical design to reference `src/adapters/` module

**SPEC-DASH-008: Dashboard Configuration Management**
- Location: `specifications/features/SPEC-DASH-008-dashboard-configuration-management.md`
- Add reference to domain objects for UI inspection (§5.3 of architectural analysis)
- Update implementation to use `src/domain/` objects

**Estimated:** 1 hour

---

## Timeline Summary

| Phase | Duration | Assigned To | Status |
|-------|----------|-------------|--------|
| ADR Creation | 4 hours | Backend Benny + Alphonso | Ready |
| Documentation Updates | 3 hours | Alphonso + Claire | Ready |
| Dependency Check | 2 hours | Claire | Ready |
| Orchestration Assessment | 2 hours | Mike | Ready |
| Initiative Creation | 5 hours | Petra | Ready |
| **Total Immediate** | **16 hours** | | |
| Phase 1-6 Implementation | 120 hours | Backend Benny (primary) | Pending |
| **Grand Total** | **136 hours** | | |

---

## Approval Chain

1. ✅ **Architectural Analysis Approved** - @stijn-dejongh, 2026-02-11
2. ⏳ **ADR-045 Draft Review** - Pending (Backend Benny creates, Alphonso reviews)
3. ⏳ **ADR-046 Draft Review** - Pending (Backend Benny creates, Alphonso reviews)
4. ⏳ **Initiative Creation** - Pending (Petra creates, Mike approves)
5. ⏳ **Implementation Start** - Pending (Mike assigns tasks)

---

## Questions for Team

**For Curator Claire:**
1. Findings from doctrine→ADR dependency check?
2. Any violations of dependency direction rules?

**For Manager Mike:**
1. Should Manager Mike own orchestration (Batch/Iteration/Cycle)?
2. Or create separate "Orchestrator Otto" agent?
3. How to prioritize 46 tasks across 7 weeks?

**For Backend Benny:**
1. Available for Phase 1 implementation (16 hours)?
2. Preferred test framework (pytest, unittest)?
3. Any concerns with dataclass approach vs. Pydantic?

**For Planning Petra:**
1. How to integrate 7-week timeline with current iteration schedule?
2. Should we create tasks all at once or phase-by-phase?

---

## Related Documents

- **Architectural Analysis:** `work/reports/architecture/architectural-analysis-doctrine-code-representations.md`
- **Work Log (Backend Benny):** `work/logs/2026-02-11T0604-doctrine-code-representations-implementation.md`
- **ADR-042:** Shared Task Domain Model (pattern reference)
- **ADR-044:** Agent Identity Type Safety (pattern reference)

---

**Status:** ACTION ITEMS READY ✅  
**Next Review:** After ADR-045/046 draft completion  
**Blocked By:** None  
**Blocking:** SPEC-DIST-001 (vendor tool export), SPEC-DASH-008 (doctrine UI)
