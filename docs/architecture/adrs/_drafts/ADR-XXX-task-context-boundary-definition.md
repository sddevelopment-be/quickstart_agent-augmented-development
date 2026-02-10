# ADR-XXX: Task Context Boundary Definition

**Status:** DRAFT  
**Date:** 2026-02-10  
**Deciders:** [To be assigned]  
**Related:** Strategic Linguistic Assessment (2026-02-10), ADR-042 (Shared Task Domain Model), ADR-008 (File-Based Async Coordination)

---

## Context

### Problem Statement

The term **"Task"** is used across three distinct semantic contexts without explicit translation boundaries:

1. **Orchestration Context** - YAML-based file I/O and persistence
2. **Task Domain Context** - Business logic and state machine
3. **Collaboration Context** - Human-facing workflow and agent assignment

This linguistic polysemy creates:
- **Architectural coupling** - Changes in one context ripple to others
- **Maintenance burden** - Bug fixes must be applied in multiple representations
- **Onboarding confusion** - Developers conflate distinct concepts
- **Feature fragility** - Workflow changes require orchestration changes

### Current State Analysis

**Three Representations of "Task":**

```python
# 1. Orchestration: Dictionary representation
def read_task(path: Path) -> Dict[str, Any]:
    # YAML file I/O
    
# 2. Domain: Type-safe dataclass
@dataclass
class Task:
    status: TaskStatus
    # Business logic
    
# 3. Collaboration: Implicit in file system
work/collaboration/assigned/<agent>/task.yaml
```

**Evidence from Linguistic Assessment:**
- 189 occurrences of "task" in Python code
- Multiple task I/O implementations (ADR-042 addresses duplication)
- No Anti-Corruption Layer between contexts
- Direct dictionary passing between orchestration and domain

### Architectural Signal

From Language-First Architecture approach:
> "Same term, multiple meanings → Hidden bounded context boundary → Accidental coupling"

**Hidden Bounded Contexts:**
```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  Orchestration  │   │   Task Domain   │   │  Collaboration  │
│    Context      │   │     Context     │   │     Context     │
│                 │   │                 │   │                 │
│  TaskDescriptor │──▶│  TaskAggregate  │◀──│  WorkItem       │
│  (YAML I/O)     │   │  (State Machine)│   │  (Agent Queue)  │
└─────────────────┘   └─────────────────┘   └─────────────────┘
   ACL: Parser         ACL: Hydrator         ACL: Presenter
```

---

## Decision

We will **make bounded context boundaries explicit** by:

1. **Defining distinct vocabulary** per context
2. **Creating Anti-Corruption Layers** at context boundaries
3. **Documenting ubiquitous language** in glossary
4. **Aligning module structure** with semantic boundaries

### Proposed Bounded Contexts

#### 1. Orchestration Context

**Ubiquitous Language:**
- **TaskDescriptor** (replaces raw `Dict[str, Any]`)
- **Serialize/Deserialize** (file I/O operations)
- **Persist/Load** (durability concerns)

**Responsibilities:**
- YAML file persistence
- File system coordination
- Work directory management

**Module:** `src/orchestration/`

**Anti-Corruption Layer:**
```python
# src/orchestration/translation.py
def parse_task_descriptor(yaml_dict: Dict[str, Any]) -> TaskDescriptor:
    """Parse YAML dictionary into TaskDescriptor."""
    
def serialize_task_descriptor(descriptor: TaskDescriptor) -> Dict[str, Any]:
    """Serialize TaskDescriptor to YAML-compatible dictionary."""
```

---

#### 2. Task Domain Context

**Ubiquitous Language:**
- **TaskAggregate** (replaces generic `Task`)
- **Lifecycle** (state progression)
- **Transition** (state changes with validation)
- **Invariant** (business rules)

**Responsibilities:**
- Task lifecycle state machine
- Business rule enforcement
- Transition validation

**Module:** `framework/core/task_domain/`

**Anti-Corruption Layer:**
```python
# framework/core/task_domain/hydration.py
def hydrate_from_descriptor(descriptor: TaskDescriptor) -> TaskAggregate:
    """Create TaskAggregate from orchestration TaskDescriptor."""
    
def dehydrate_to_descriptor(aggregate: TaskAggregate) -> TaskDescriptor:
    """Convert TaskAggregate to orchestration TaskDescriptor."""
```

---

#### 3. Collaboration Context

**Ubiquitous Language:**
- **WorkItem** (human-facing work unit)
- **Assignment** (agent allocation)
- **Handoff** (work transfer)
- **Queue** (agent-specific work list)

**Responsibilities:**
- Agent assignment logic
- Handoff coordination
- Workflow presentation

**Module:** `src/collaboration/`

**Anti-Corruption Layer:**
```python
# src/collaboration/presentation.py
def present_as_work_item(aggregate: TaskAggregate) -> WorkItem:
    """Present TaskAggregate as WorkItem for agent queues."""
    
def extract_aggregate_changes(work_item: WorkItem) -> TaskAggregate:
    """Extract domain changes from completed WorkItem."""
```

---

## Consequences

### Positive

✅ **Explicit Boundaries** - No more implicit coupling via shared dictionary representation  
✅ **Independent Evolution** - Each context can change vocabulary without affecting others  
✅ **Clear Ownership** - Each bounded context has explicit responsibility scope  
✅ **Onboarding Clarity** - New developers understand semantic boundaries  
✅ **Maintenance Safety** - Changes localized to single context  

### Negative

⚠️ **Translation Overhead** - Anti-Corruption Layers add code and complexity  
⚠️ **Migration Effort** - Existing code must be refactored to use new vocabulary  
⚠️ **Performance** - Conversion between representations adds overhead (minor)  

### Mitigations

- **Phased Migration** - Introduce new vocabulary incrementally, support both during transition
- **Backward Compatibility** - Keep existing dictionary interfaces until all consumers updated
- **Performance** - Profile hotpaths, optimize critical conversions if needed
- **Documentation** - Clear glossary entries for each context's ubiquitous language

---

## Implementation Strategy

### Phase 1: Define Vocabulary (Week 1)

**Deliverables:**
1. Glossary entries for TaskDescriptor, TaskAggregate, WorkItem
2. Update `.contextive/contexts/orchestration.yml`
3. Context map diagram showing relationships

**Effort:** 8 hours

---

### Phase 2: Create Anti-Corruption Layers (Week 2-3)

**Deliverables:**
1. `src/orchestration/translation.py` - Parse/serialize functions
2. `framework/core/task_domain/hydration.py` - Hydrate/dehydrate functions
3. `src/collaboration/presentation.py` - Present/extract functions
4. Unit tests for all translation functions

**Effort:** 24 hours

---

### Phase 3: Refactor Existing Code (Week 4-8)

**Deliverables:**
1. Update `agent_base.py` to use TaskAggregate instead of Dict
2. Update `agent_orchestrator.py` to use TaskDescriptor
3. Update dashboard code to use WorkItem presentation
4. Integration tests for cross-context scenarios

**Effort:** 40 hours (phased, can be distributed)

---

### Phase 4: Remove Legacy Dictionary API (Week 9+)

**Deliverables:**
1. Deprecate raw dictionary usage
2. Remove backward compatibility shims
3. Update all documentation
4. Final integration test pass

**Effort:** 8 hours

---

## Validation Criteria

### Acceptance Criteria

- [ ] Three bounded contexts have explicit vocabulary in glossary
- [ ] Anti-Corruption Layers exist at context boundaries
- [ ] No direct dictionary passing between contexts
- [ ] Context map document exists showing relationships
- [ ] All existing tests pass with new vocabulary
- [ ] Module structure reflects semantic boundaries

### Success Metrics

- **Code Locality** - Changes to orchestration don't require domain changes (and vice versa)
- **Vocabulary Consistency** - Each context uses its own ubiquitous language consistently
- **Developer Feedback** - Onboarding developers can explain context boundaries
- **Defect Rate** - Bugs from task representation ambiguity approach zero

---

## Alternatives Considered

### Alternative 1: Keep Single "Task" Concept

**Rationale:** Simpler, no migration needed

**Rejected Because:**
- Coupling already causing maintenance burden (ADR-042)
- Linguistic ambiguity confusing developers
- Violates bounded context principles
- Technical debt will compound

---

### Alternative 2: Use Type Aliases Only

**Approach:**
```python
TaskDescriptor = Dict[str, Any]
TaskAggregate = Task
WorkItem = Task
```

**Rejected Because:**
- Type aliases don't create semantic boundaries
- No enforcement of translation at boundaries
- Still allows direct coupling
- Doesn't solve underlying architectural issue

---

### Alternative 3: Monolithic Task Model

**Approach:** Single rich Task class with all concerns

**Rejected Because:**
- Violates Single Responsibility Principle
- Couples persistence, domain logic, and presentation
- Makes testing harder
- Increases cognitive load

---

## Related Decisions

- **ADR-042:** Shared Task Domain Model (addresses I/O duplication)
- **ADR-008:** File-Based Async Coordination (defines orchestration patterns)
- **ADR-004:** Work Directory Structure (defines file system layout)

---

## References

### Doctrine
- **language-first-architecture.md** - Linguistic signals as architectural decisions
- **bounded-context-linguistic-discovery.md** - Context boundary identification
- **living-glossary-practice.md** - Vocabulary maintenance

### Domain-Driven Design
- **Strategic Design** - Bounded Context, Context Map, Anti-Corruption Layer
- **Ubiquitous Language** - Context-specific vocabulary
- **Aggregate Pattern** - TaskAggregate as consistency boundary

### Assessment
- **Strategic Linguistic Assessment (2026-02-10)** - Signal 1: Task Polysemy

---

## Decision Log

- **2026-02-10:** DRAFT created based on linguistic assessment findings
- [To be updated as decision evolves]

---

## Notes

**Architect's Note:** This ADR was drafted as part of the strategic linguistic assessment. It proposes a significant refactoring but addresses a real architectural coupling risk. Recommend prioritizing based on team capacity and near-term roadmap impact.

**Risk:** If not addressed, the task representation coupling will:
1. Compound as more features are added
2. Make future microservice extraction harder
3. Increase onboarding time
4. Lead to subtle bugs from ambiguity

**Opportunity:** Implementing this creates a clearer mental model for the entire team and sets a pattern for other potential bounded contexts (Agent domain, Specification domain, etc.).

---

_ADR follows Directive 018 (Traceable Decisions) and is informed by Language-First Architecture approach._
