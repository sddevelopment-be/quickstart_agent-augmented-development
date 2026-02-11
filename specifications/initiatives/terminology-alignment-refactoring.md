---
id: "SPEC-TERM-001"
title: "Terminology Alignment and Code Refactoring Initiative"
status: "draft"
initiative: "Conceptual Alignment"
priority: "HIGH"
epic: "Language-First Architecture Maturation"
target_personas: ["backend-developer", "architect", "code-reviewer", "project-manager"]
features:
  - id: "FEAT-TERM-001-01"
    title: "Directive Updates for Naming Enforcement"
    status: "draft"
    description: "Update directives to enforce collaboration scripts as ONLY way to manipulate work artifacts and avoid generic naming anti-patterns"
  - id: "FEAT-TERM-001-02"
    title: "Top 5 Generic Class Name Refactoring"
    status: "draft"
    description: "Rename highest-impact classes from Manager/Handler/Processor to domain-specific names"
  - id: "FEAT-TERM-001-03"
    title: "Terminology Standardization"
    status: "draft"
    description: "Resolve State/Status, Load/read, Persist/write terminology conflicts"
  - id: "FEAT-TERM-001-04"
    title: "Task Context Boundary Implementation"
    status: "draft"
    description: "Implement ADR-XXX task context boundary definition with Anti-Corruption Layers"
  - id: "FEAT-TERM-001-05"
    title: "CQRS Research and Pattern Evaluation"
    status: "draft"
    description: "Research CQRS pattern applicability and create doctrine reference"
  - id: "FEAT-TERM-001-06"
    title: "Full Generic Class Refactoring"
    status: "draft"
    description: "Complete remaining 14 generic class name refactors opportunistically"
  - id: "FEAT-TERM-001-07"
    title: "Glossary Automation"
    status: "draft"
    description: "Automate glossary term usage validation in CI pipeline"
completion: null
created: "2026-02-11"
updated: "2026-02-11"
author: "analyst-annie"
---

# Initiative Specification: Terminology Alignment and Code Refactoring

**Status:** Draft  
**Created:** 2026-02-11  
**Last Updated:** 2026-02-11  
**Author:** Analyst Annie  
**Stakeholders:** Architect Alphonso, Backend Developers, Code Reviewers, Planning Petra

---

## Executive Summary

This initiative addresses critical terminology fragmentation and code quality issues identified in the **Conceptual Alignment Assessment** (2026-02-10). By systematically refactoring generic class names, standardizing vocabulary, and implementing explicit bounded context boundaries, we reduce future maintenance costs and accelerate onboarding.

### Critical Priority Rationale

**ROI Analysis:**
- **Current cost:** 189 "task" references across 3 contexts = 15-20% maintenance overhead per feature
- **Prevention value:** Addressing now prevents ~40 hours/quarter of debugging and refactoring
- **Strategic alignment:** Enables language-first architecture approach (doctrine foundation)
- **Team velocity:** Reduces onboarding time from 2 weeks to 1 week (terminology clarity)

**Connection to Language-First Architecture:**
> "Same term, multiple meanings → Hidden bounded context boundary → Accidental coupling"  
> — Language-First Architecture Approach (doctrine/approaches/language-first-architecture.md)

This initiative operationalizes the language-first approach by making linguistic boundaries explicit and enforcing vocabulary consistency.

### Investment Summary

| Timeframe | Effort | Deliverables | Impact |
|-----------|--------|--------------|--------|
| Week 1    | 7 hours | Directive updates, quick wins | Prevent future violations |
| Weeks 2-4 | 31 hours | Top 5 refactors, terminology standardization | Immediate clarity improvement |
| Month 2-3 | 52 hours | ADR implementation, remaining refactors | Architectural health |
| Ongoing   | 30 min/week | Living glossary maintenance | Continuous alignment |
| **Total** | **~120 hours** | **Sustainable linguistic health** | **65% → 85% health score** |

---

## Problem Statement

### Current State Issues

**1. Task Polysemy (HIGH SEVERITY)**
- The term "task" is used across 3 distinct semantic contexts without translation layers:
  1. **Orchestration Tasks** - YAML-based file I/O and persistence
  2. **Task Domain** - Business logic and state machine
  3. **Collaboration Tasks** - Human-facing workflow and agent assignment
- **Impact:** Architectural coupling, maintenance burden (bug fixes in multiple places), onboarding confusion
- **Evidence:** 189 occurrences, no Anti-Corruption Layers (ACLs), direct dictionary passing between contexts

**2. Generic Naming Anti-Patterns (MEDIUM SEVERITY)**
- 19 classes use generic technical suffixes (Manager/Handler/Processor) in domain code:
  - `ModelConfigurationManager` (should be `ModelRouter`)
  - `TemplateManager` (should be `TemplateRenderer`)
  - `TaskAssignmentHandler` (should be `TaskAssignmentService`)
  - `OrchestrationConfigLoader` (needs domain name)
  - `AgentSpecRegistry` (needs domain name)
- **Impact:** Reduces code readability, obscures domain concepts, increases cognitive load
- **Pattern:** "Generic Technical Jargon Dominates" anti-pattern from language-first architecture

**3. Terminology Conflicts (MEDIUM SEVERITY)**
- 3 terminology pairs used inconsistently:
  - State/Status → no clear usage pattern
  - Load/read → confusing for YAML operations
  - Persist/write → ambiguous intent
- **Impact:** Code reviews require clarification, PRs have terminology debates, glossary underutilized

**4. Glossary-Code Misalignment (LOW SEVERITY)**
- 75% of glossary terms unused (34/44 terms)
- Aspirational DDD terms not operationalized
- **Impact:** False expectations about team's DDD maturity, glossary not trusted as source of truth

### Impact on Maintainability

**Current Costs:**
- **Onboarding:** 2 weeks to understand "task" contexts (vs. 1 week target)
- **Code Review:** 20% of review time spent on terminology clarification
- **Debugging:** 15% maintenance overhead from context confusion
- **Refactoring:** Every orchestration change risks breaking domain logic

### Risk of Continued Drift

**If Not Addressed:**
1. Coupling compounds as features grow → 40 hours/quarter rework
2. Microservice extraction becomes impossible → architectural lock-in
3. Team velocity decreases as terminology debt accumulates
4. New developers struggle with ambiguous vocabulary → turnover risk

---

## Target Personas

### Primary Personas

**1. Backend Developer (Backend Benny, Python Pedro)**
- **Needs:** Clear naming conventions, unambiguous terminology, refactoring guidance
- **Benefits:** Less confusion, faster feature development, confident code reviews
- **Success Metric:** Can rename a class without breaking orchestration (decoupled)

**2. Code Reviewer (Code Reviewer Cindy)**
- **Needs:** Enforcement guidelines, PR comment templates, escalation criteria
- **Benefits:** Consistent feedback, reduced review time, clear standards
- **Success Metric:** Zero terminology debates in PRs

### Secondary Personas

**3. Architect (Architect Alphonso)**
- **Needs:** Strategic decisions documented, ADR implementation tracked, bounded context clarity
- **Benefits:** Architectural vision operationalized, Conway's Law alignment visible
- **Success Metric:** Context boundaries explicit in code structure

**4. Planning Lead (Planning Petra)**
- **Needs:** Work phasing strategy, task breakdown guidance, ROI tracking
- **Benefits:** Clear initiative roadmap, predictable delivery timeline
- **Success Metric:** 90% on-time feature completion (reduced rework)

---

## Requirements (MoSCoW)

### MUST Have (Critical - Initiative fails without these)

#### FR-M1: Directive Updates for Workflow Enforcement
**Requirement:** Update `.github/agents/directives/` to enforce:
- "Use collaboration scripts/API as ONLY way to manipulate work artifacts"
- "Avoid generic naming in domain code (Manager/Handler/Processor)"
- Document exceptions and leniency guidelines

**Rationale:** Prevent future violations at source (enforcement > cleanup)  
**Personas Affected:** All agents, code reviewers  
**Success Criteria:**
- Given a PR with direct file manipulation
- When code reviewer evaluates
- Then directive violation is flagged with specific guidance

**Acceptance Tests:**
```gherkin
Scenario: Direct file manipulation detected
  Given a PR modifies task YAML directly (not via scripts)
  When Code Reviewer Cindy reviews
  Then comment references Directive [X] and suggests correct script
  
Scenario: Generic class name in domain code
  Given a new class named "TaskManager" in domain code
  When Code Reviewer Cindy reviews
  Then comment references Directive [Y] and suggests domain-specific name
```

---

#### FR-M2: Top 5 Generic Class Name Refactoring
**Requirement:** Rename 5 highest-impact classes to domain-specific names:
1. `ModelConfigurationManager` → `ModelRouter`
2. `TemplateManager` → `TemplateRenderer`
3. `TaskAssignmentHandler` → `TaskAssignmentService`
4. `OrchestrationConfigLoader` → [TBD with team]
5. `AgentSpecRegistry` → [TBD with team]

**Rationale:** Immediate clarity improvement, demonstrates naming standard  
**Personas Affected:** Backend developers, new contributors  
**Success Criteria:**
- Given a developer reads `ModelRouter` code
- When they need to understand routing logic
- Then class name accurately describes responsibility

**Acceptance Tests:**
```gherkin
Scenario: Renamed class maintains functionality
  Given ModelConfigurationManager renamed to ModelRouter
  When all tests run
  Then 100% tests pass (backward compatibility preserved)
  
Scenario: Import paths updated consistently
  Given ModelRouter replaces ModelConfigurationManager
  When developer searches for old name in codebase
  Then zero occurrences found (complete migration)
```

---

#### FR-M3: Terminology Standardization
**Requirement:** Resolve 3 terminology conflicts:
- **State/Status:** Standardize on "Status" for task lifecycle (per ADR-043)
- **Load/read:** Use "load" for YAML deserialization, "read" for generic file I/O
- **Persist/write:** Use "persist" for intentional storage, "write" for low-level I/O

**Rationale:** Eliminates code review debates, aligns with glossary  
**Personas Affected:** All developers, code reviewers  
**Success Criteria:**
- Given a developer writes YAML deserialization code
- When they choose terminology
- Then glossary provides unambiguous guidance

**Acceptance Tests:**
```gherkin
Scenario: Status terminology enforced
  Given a new class for task lifecycle
  When developer names field
  Then "status" used (not "state")
  And glossary reference included in docstring
  
Scenario: Load vs read clarity
  Given YAML file deserialization function
  When developer names function
  Then "load_task_from_yaml()" used (not "read_task()")
```

---

### SHOULD Have (Important - Initiative degraded without these)

#### FR-S1: Task Context Boundary Implementation
**Requirement:** Implement ADR-XXX task context boundary definition:
- Define distinct vocabulary per context (TaskDescriptor, TaskAggregate, WorkItem)
- Create Anti-Corruption Layers at context boundaries
- Document ubiquitous language in glossary
- Align module structure with semantic boundaries

**Rationale:** Addresses root cause of task polysemy, enables independent evolution  
**Personas Affected:** Backend developers, architects  
**Success Criteria:**
- Given a change to orchestration TaskDescriptor
- When task domain logic is evaluated
- Then zero breaking changes (ACL isolates contexts)

**Workaround if omitted:** Continue with shared dictionary representation (accept coupling risk)

**Acceptance Tests:**
```gherkin
Scenario: Context isolation verified
  Given TaskDescriptor schema changes
  When TaskAggregate uses descriptor
  Then ACL translation function handles conversion
  And domain logic unaffected
  
Scenario: Vocabulary clarity enforced
  Given developer reads orchestration code
  When they see "TaskDescriptor"
  Then glossary explains YAML-specific semantics
  And distinguishes from TaskAggregate (domain)
```

---

#### FR-S2: CQRS Research and Pattern Evaluation
**Requirement:** 
- Researcher Ralph: Create CQRS primer for `doctrine/docs/references/`
- Architect Alphonso: Evaluate CQRS applicability to task context boundaries
- Decision: Document whether to implement or defer

**Rationale:** PR feedback requested CQRS consideration, need informed decision  
**Personas Affected:** Architect, backend developers  
**Success Criteria:**
- Given CQRS pattern research complete
- When Architect evaluates task context boundaries
- Then decision documented with rationale (implement/defer/reject)

**Workaround if omitted:** Proceed with simpler ACL approach (ADR-XXX current proposal)

**Acceptance Tests:**
```gherkin
Scenario: Research deliverable validated
  Given CQRS primer document created
  When Architect reviews
  Then primer covers: commands, queries, event sourcing, applicability criteria
  
Scenario: Decision documented
  Given CQRS pattern evaluated
  When team reviews ADR-XXX
  Then decision section explains CQRS consideration and rationale
```

---

#### FR-S3: Full Generic Class Refactoring
**Requirement:** Complete remaining 14 generic class name refactors opportunistically during normal maintenance

**Rationale:** Incremental improvement without blocking initiative completion  
**Personas Affected:** Backend developers  
**Success Criteria:**
- Given a developer touches a class with generic name
- When they complete their feature work
- Then they apply Boy Scout rule (rename if low-risk)

**Workaround if omitted:** Accept generic names until natural refactoring opportunity

**Acceptance Tests:**
```gherkin
Scenario: Opportunistic refactoring tracked
  Given generic class refactored during feature work
  When PR submitted
  Then refactoring documented in commit message
  And total remaining generic classes decremented in tracking doc
```

---

### COULD Have (Nice to have - Enhances experience)

#### FR-C1: Glossary Automation
**Requirement:** Automate glossary term usage validation in CI pipeline:
- Scan code for glossary term references
- Verify docstrings include glossary links
- Alert on undefined terms used in domain code

**Rationale:** Continuous enforcement, reduces manual code review burden  
**Personas Affected:** All developers, CI/CD pipeline  
**Success Criteria:**
- Given a PR introduces new domain term
- When CI runs
- Then validation warns if term not in glossary

**If omitted:** Manual code review continues (acceptable, scales with team size)

**Acceptance Tests:**
```gherkin
Scenario: Missing glossary term detected
  Given PR introduces "AgentPool" term in code
  When glossary validation runs
  Then CI warns: "AgentPool not in glossary, consider adding"
  
Scenario: Glossary link verified
  Given domain class references "TaskAggregate"
  When docstring validation runs
  Then link to glossary confirmed present
```

---

#### FR-C2: Module Restructuring
**Requirement:** Restructure module hierarchy to align with bounded contexts:
- `src/orchestration/` - Orchestration Context
- `src/framework/core/task_domain/` - Task Domain Context
- `src/collaboration/` - Collaboration Context

**Rationale:** Physical structure mirrors semantic boundaries (Conway's Law alignment)  
**Personas Affected:** All developers, architects  
**Success Criteria:**
- Given a developer navigates codebase
- When they look for task lifecycle logic
- Then module structure reflects bounded context separation

**If omitted:** Accept module structure misalignment (documentation compensates)

---

### WON'T Have (Explicitly out of scope)

#### FR-W1: Database Introduction
**Reason:** File-system simplicity is architectural constraint (ADR-008), not negotiable for this initiative  
**Future Consideration:** Could revisit in microservice extraction initiative (2027+)

#### FR-W2: Over-Engineering DDD Patterns
**Reason:** Pragmatic DDD application, not textbook implementation. Avoid:
- Domain events for single-process operations
- Repository pattern for file I/O (overkill)
- Aggregate complexity beyond state machine
**Future Consideration:** Introduce patterns incrementally as complexity demands

#### FR-W3: Legacy Code Rewrite
**Reason:** Opportunistic refactoring only (Boy Scout rule). No "big bang" rewrites.  
**Note:** Preserve file-system orchestration patterns (working well)

---

## Scenarios and Behavior

### Scenario 1: Developer Renames Generic Class (Happy Path)

**Context:** Backend Benny refactoring `ModelConfigurationManager` during routing feature work

**Given:** `ModelConfigurationManager` exists with 12 references across codebase  
**And:** Directive [Y] specifies domain naming enforcement  
**When:** Benny renames to `ModelRouter` and updates all imports  
**Then:** All 52 unit tests pass (functionality preserved)  
**And:** Code reviewer approves with "✅ Follows naming directive"  
**And:** Glossary updated with `ModelRouter` definition  

**Personas:** Backend Benny (implementer), Code Reviewer Cindy (approver)  
**Priority:** MUST

---

### Scenario 2: Code Reviewer Flags Generic Naming (Enforcement Path)

**Context:** New PR introduces `DataProcessor` class in domain code

**Given:** PR adds `DataProcessor` class with 8 methods  
**And:** Directive [Y] prohibits generic naming in domain code  
**When:** Code Reviewer Cindy reviews PR  
**Then:** Comment posted: "⚠️ Generic name 'Processor' detected. Directive [Y] suggests domain-specific name. What does this process? Consider: `TaskTransformer`, `TaskValidator`, etc."  
**And:** PR marked as "changes requested"  
**And:** Developer revises to `TaskValidator` and re-submits  

**Personas:** Code Reviewer Cindy (enforcer), Backend Developer (reviser)  
**Priority:** MUST

---

### Scenario 3: Task Context Boundary Translation (Architectural Path)

**Context:** Orchestration layer needs to pass task to domain logic

**Given:** Orchestration has `TaskDescriptor` (YAML dictionary)  
**And:** Domain expects `TaskAggregate` (typed dataclass)  
**When:** Orchestration calls domain service  
**Then:** ACL translation function `hydrate_from_descriptor()` converts representation  
**And:** Domain logic operates on `TaskAggregate` (no dictionary access)  
**And:** Result translated back via `dehydrate_to_descriptor()`  
**And:** Orchestration persists updated `TaskDescriptor` to YAML  

**Personas:** Orchestration (caller), Domain Logic (callee), ACL (translator)  
**Priority:** SHOULD

---

### Scenario 4: Terminology Conflict Resolution (Error Case)

**Context:** Developer unsure whether to use "state" or "status" for task lifecycle

**Given:** Developer writing task query function  
**And:** Function needs to filter by task lifecycle stage  
**When:** Developer checks glossary for guidance  
**Then:** Glossary entry for "TaskStatus" found with definition  
**And:** Reference to ADR-043 (Status Enumeration Standard)  
**And:** Developer uses `status` field (not `state`)  
**And:** Code review has zero terminology debate  

**Personas:** Backend Developer (uncertain), Glossary (guide), Code Reviewer (validator)  
**Priority:** MUST

---

### Scenario 5: CQRS Evaluation Deferred (Alternative Path)

**Context:** Architect Alphonso evaluating CQRS for task context boundaries

**Given:** CQRS primer completed by Researcher Ralph  
**And:** Task context boundary implementation underway  
**When:** Architect reviews CQRS complexity vs. benefit  
**Then:** Decision: Defer CQRS (overkill for file-based coordination)  
**And:** ADR-XXX updated with rationale: "CQRS more suited for event-driven microservices. Current ACL approach sufficient for file-based orchestration."  
**And:** CQRS primer archived in `doctrine/docs/references/` for future consideration  

**Personas:** Architect Alphonso (decider), Researcher Ralph (educator)  
**Priority:** SHOULD

---

### Scenario 6: Opportunistic Refactoring Tracked (Boy Scout Path)

**Context:** Python Pedro implementing feature, encounters `ConfigHandler` class

**Given:** `ConfigHandler` class has 3 methods, low test coverage risk  
**And:** Feature work touches this class  
**When:** Pedro applies Boy Scout rule (leave code better)  
**Then:** Renames to `ConfigurationLoader` (domain-specific)  
**And:** Updates imports (4 files affected)  
**And:** Commits with message: "refactor: Rename ConfigHandler → ConfigurationLoader (Boy Scout)"  
**And:** Tracking doc updated: 14 → 13 remaining generic classes  

**Personas:** Python Pedro (implementer), Tracking Doc (metric)  
**Priority:** SHOULD

---

### Scenario 7: Glossary Automation Warns (Edge Case)

**Context:** CI pipeline validates glossary term usage

**Given:** PR introduces "TaskPool" term in docstring  
**And:** "TaskPool" not defined in glossary  
**When:** Glossary validation runs in CI  
**Then:** Warning posted: "⚠️ New term 'TaskPool' detected. Consider adding to glossary: `.contextive/contexts/task-domain.yml`"  
**And:** PR not blocked (advisory enforcement)  
**And:** Developer adds glossary entry in follow-up commit  

**Personas:** CI Pipeline (validator), Developer (responder), Curator Claire (glossary maintainer)  
**Priority:** COULD

---

## Constraints and Business Rules

### Business Rules

**BR1: Backward Compatibility Preserved**
- **Applies to:** All refactoring scenarios (FR-M2, FR-S3)
- **Enforcement:** 100% test pass rate required before merge

**BR2: No Breaking Changes to Collaboration Workflow**
- **Applies to:** Task context boundary implementation (FR-S1)
- **Enforcement:** Collaboration scripts API unchanged (internal refactoring only)

**BR3: Opportunistic Refactoring Only**
- **Applies to:** Full generic class refactoring (FR-S3)
- **Enforcement:** No dedicated "refactoring sprints", only during feature work

**BR4: Glossary as Source of Truth**
- **Applies to:** Terminology standardization (FR-M3)
- **Enforcement:** Code review references glossary, not individual opinion

---

### Technical Constraints

**TC1: File-System Simplicity Preserved**
- **Measurement:** No database dependencies introduced
- **Rationale:** ADR-008 (File-Based Async Coordination) is foundational

**TC2: Test Coverage Maintained**
- **Measurement:** Code coverage ≥85% after refactoring
- **Rationale:** Refactoring without tests = high regression risk

**TC3: Incremental Migration Supported**
- **Measurement:** Old and new names coexist during transition (deprecation warnings)
- **Rationale:** Phased rollout prevents "big bang" failures

---

### Non-Functional Requirements (MoSCoW)

**NFR-M1 (MUST): Onboarding Time Reduction**
- **Target:** 2 weeks → 1 week for new developers to understand task contexts
- **Measurement:** Developer feedback survey after onboarding
- **Verification:** Track time-to-first-PR metric

**NFR-S1 (SHOULD): Code Review Time Reduction**
- **Target:** 20% reduction in terminology clarification time
- **Measurement:** PR review duration (baseline vs. post-initiative)
- **Verification:** Code Reviewer Cindy feedback

**NFR-C1 (COULD): Glossary Adoption Rate**
- **Target:** 50% of domain classes reference glossary terms in docstrings
- **Measurement:** Automated scan of docstrings for glossary links
- **Verification:** CI pipeline metric

---

### Edge Cases and Limits

- **Maximum refactoring scope per PR:** 5 files affected (avoid mega-PRs)
- **Minimum glossary term usage:** 2+ occurrences before adding to glossary (avoid noise)
- **Invalid inputs:** Generic names acceptable in framework/infrastructure code (not domain)
- **Timeouts:** If ADR-XXX blocked >4 weeks, proceed with simpler ACL approach
- **Fallbacks:** If terminology debates persist, escalate to Architect for binding decision

---

## Dependencies and Constraints

### Prerequisites (Must Complete First)

✅ **Boy Scout Fixes (Complete 2026-02-10)**
- Glossary term fixes applied
- File reorganization complete
- New glossaries created (task-domain.yml, portfolio-domain.yml)
- **Status:** Delivered by Curator Claire

⚠️ **ADR-042 Implementation (In Progress)**
- Shared task domain model (`src/common/task_schema.py`)
- Eliminates task I/O duplication
- **Status:** Assigned to Python Pedro, ~9 hours remaining
- **Blocker:** Task context boundaries depend on this foundation

---

### External Dependencies

**Researcher Ralph:**
- CQRS primer for `doctrine/docs/references/` (8 hours)
- Timeline: Week 2 (parallel with top 5 refactoring)

**Architect Alphonso:**
- Finalize ADR-XXX with team input (4 hours)
- Approve task context boundary design (2 hours)
- Timeline: Week 1 (critical path)

**Code Reviewer Cindy:**
- Review and approve directive updates (2 hours)
- Timeline: Week 1 (enables enforcement)

**Curator Claire:**
- Maintain glossary updates as terms added (30 min/week ongoing)
- Timeline: Throughout initiative

---

### Architectural Constraints

**1. Preserve File-System Orchestration (ADR-008)**
- No database introduction
- No event-driven architecture
- Maintain YAML-based coordination

**2. Single Responsibility Principle**
- Each bounded context has clear ownership
- No shared mutable state across contexts

**3. Conway's Law Alignment**
- Module structure reflects team organization
- Agent specialization maps to bounded contexts

---

### Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking changes during refactoring | Medium | High | Comprehensive test coverage, incremental migration |
| Scope creep (too many classes) | High | Medium | MoSCoW strict, top 5 first, rest opportunistic |
| Team capacity shortage | Medium | Medium | Distributed work, Boy Scout approach, no dedicated sprints |
| ADR-XXX blocked by disagreement | Low | High | Architect binding decision, escalation path defined |
| Glossary maintenance neglected | Medium | Low | Curator Claire ownership, 30 min/week commitment |

---

## Phasing Strategy

### Phase 1: Foundation (Week 1) - 7 hours

**Goal:** Enable enforcement and prevent future violations

**Deliverables:**
1. **Directive Updates** (4 hours)
   - Update workflow enforcement directive
   - Update generic naming anti-pattern directive
   - Document exceptions and leniency guidelines
   - Review and approve with Code Reviewer Cindy

2. **Quick Win Refactoring** (2 hours)
   - Rename `ModelConfigurationManager` → `ModelRouter` (lowest risk)
   - Update imports and tests
   - Demonstrate refactoring pattern

3. **Glossary Approval** (1 hour)
   - Finalize `orchestration.yml` glossary (from _proposed/)
   - Approve new terms with Architect Alphonso

**Success Metric:** Zero directive violations in new PRs

---

### Phase 2: High-Impact Refactoring (Weeks 2-4) - 31 hours

**Goal:** Improve code clarity and resolve terminology conflicts

**Deliverables:**
1. **Top 5 Class Refactoring** (16 hours)
   - Week 2: `TemplateManager` → `TemplateRenderer` (4 hours)
   - Week 3: `TaskAssignmentHandler` → `TaskAssignmentService` (4 hours)
   - Week 4: `OrchestrationConfigLoader` → [Team Decision] (4 hours)
   - Week 4: `AgentSpecRegistry` → [Team Decision] (4 hours)

2. **Terminology Standardization** (8 hours)
   - Status/State: Update code to use "status" consistently (3 hours)
   - Load/read: Refactor YAML functions to use "load" (3 hours)
   - Persist/write: Document usage patterns in glossary (2 hours)

3. **CQRS Research** (8 hours - parallel)
   - Researcher Ralph: Create CQRS primer (8 hours)
   - Architect Alphonso: Evaluate applicability (included in Phase 3)

**Success Metric:** 5 classes renamed, 3 terminology conflicts resolved, 78% → 82% code clarity score

---

### Phase 3: Architectural Refactoring (Month 2-3) - 52 hours

**Goal:** Implement bounded context boundaries

**Deliverables:**
1. **ADR-XXX Finalization** (4 hours)
   - Incorporate CQRS evaluation
   - Address PR feedback (from_yaml/to_yaml vs Parser)
   - Simplify proposed architecture
   - Publish final ADR

2. **Task Context Boundaries - Phase 3a** (16 hours)
   - Define distinct vocabulary (TaskDescriptor, TaskAggregate, WorkItem)
   - Create ACL translation functions
   - Unit tests for all translations

3. **Task Context Boundaries - Phase 3b** (20 hours)
   - Refactor `agent_base.py` to use `TaskAggregate`
   - Update `agent_orchestrator.py` to use `TaskDescriptor`
   - Update dashboard to use `WorkItem` presentation
   - Integration tests for cross-context scenarios

4. **Task Context Boundaries - Phase 3c** (8 hours)
   - Remove legacy dictionary API
   - Update documentation
   - Final integration test pass

5. **Remaining Generic Classes** (4 hours - opportunistic)
   - Track refactoring during normal feature work
   - Boy Scout rule application

**Success Metric:** Task contexts decoupled, orchestration changes don't break domain logic

---

### Phase 4: Continuous Improvement (Ongoing) - 30 min/week

**Goal:** Maintain glossary and monitor adoption

**Deliverables:**
1. **Living Glossary Maintenance** (Curator Claire)
   - Add new terms as domain evolves
   - Update definitions based on usage
   - Review glossary coverage monthly

2. **Adoption Monitoring** (Manager Mike)
   - Track generic class refactoring progress (14 remaining)
   - Monitor code review terminology debates (target: zero)
   - Survey developer satisfaction with terminology clarity

3. **Automation Exploration** (COULD have)
   - Investigate CI glossary validation tools
   - Evaluate Contextive IDE plugin effectiveness

**Success Metric:** 65% → 85% linguistic health score (sustained)

---

## Traceability

### Derives From (Strategic)

**Strategic Assessment:**
- **Strategic Linguistic Assessment** - Architect Alphonso (2026-02-10)
  - Signal 1: Task Polysemy (HIGH priority)
  - Signal 2: Agent Identity as Technical Jargon (LOW priority)
  - Signal 3: Workflow Vocabulary Gap (MEDIUM priority)
  - Signal 4: DDD Theory-Practice Gap (MEDIUM priority)

**Validation Reports:**
- **Terminology Validation Report** - Code Reviewer Cindy (2026-02-10)
  - 19 generic anti-pattern classes identified
  - 11/44 glossary terms in active use
  - 21 domain concepts as glossary candidates

**Lexical Analysis:**
- **Lexical Analysis Report** - Lexical Larry (2026-02-10)
  - Linguistic health score: 72/100
  - Naming convention consistency: 78/100
  - Documentation clarity: 75/100

**PR Feedback:**
- @stijn-dejongh comment 2791393298 (2026-02-10)
  - Request for initiative specification
  - Phased implementation approach
  - Boy Scout fixes prerequisite

**Related Documents:**
- `work/conceptual-alignment-assessment-synthesis.md` - Multi-agent synthesis report
- `docs/architecture/assessments/strategic-linguistic-assessment-EXECUTIVE-SUMMARY.md`
- `work/terminology-validation-report.md`
- `work/LEX/LEXICAL_ANALYSIS.md`

---

### Feeds Into (Tactical)

**ADRs:**
- **ADR-042: Shared Task Domain Model** - Foundation for task context boundaries
- **ADR-XXX: Task Context Boundary Definition** (DRAFT) - Core architectural refactoring
- **ADR-043: Status Enumeration Standard** - Terminology standardization reference

**Directives:**
- Directive [X]: Workflow Manipulation Enforcement (to be updated)
- Directive [Y]: Generic Naming Anti-Patterns (to be updated)

**Glossaries:**
- `.contextive/contexts/orchestration.yml` (to be promoted from _proposed/)
- `.contextive/contexts/task-domain.yml` (active, needs expansion)
- `.contextive/contexts/portfolio-domain.yml` (active)

**Implementation Tasks:**
- Will be created by Planning Petra based on phasing strategy
- Location: `work/collaboration/inbox/`
- Task linking: `specification: "specifications/initiatives/terminology-alignment-refactoring.md"`

---

### Cross-References

**Doctrine:**
- `doctrine/approaches/language-first-architecture.md` - Core philosophy
- `doctrine/approaches/living-glossary-practice.md` - Maintenance approach
- `doctrine/approaches/bounded-context-linguistic-discovery.md` - Context identification
- `doctrine/tactics/terminology-extraction-mapping.tactic.md` - Operational guidance

**Templates:**
- `.doctrine-config/templates/pr-comment-templates.md` - Enforcement templates
- `.doctrine-config/tactics/terminology-validation-checklist.tactic.md` - Review checklist

**Style Guides:**
- `.doctrine-config/styleguides/python-naming-conventions.md` - Repository-specific
- `doctrine/docs/styleguides/domain-driven-naming.md` - Universal patterns

---

## Success Metrics

### Baseline (Pre-Initiative)

| Metric | Current Value | Target Value | Measurement Method |
|--------|---------------|--------------|-------------------|
| Linguistic Health Score | 65/100 | 85/100 | Strategic assessment criteria |
| Generic Classes | 19 | 5 | Code scan for Manager/Handler/Processor |
| Glossary Adoption | 25% (11/44) | 60% (operational focus) | Term usage analysis |
| Onboarding Time | 2 weeks | 1 week | Developer feedback survey |
| Code Review Terminology Debates | 20% of PRs | 0% | PR comment analysis |
| Task Context Coupling | High (189 refs) | Low (ACL isolated) | Import graph analysis |

---

### Phase-Specific Metrics

**Phase 1 (Week 1):**
- ✅ Directives updated and approved
- ✅ 1 class refactored (proof of concept)
- ✅ Zero new directive violations in PRs

**Phase 2 (Weeks 2-4):**
- ✅ 5 classes refactored (top priority)
- ✅ 3 terminology conflicts resolved
- ✅ Code clarity score: 78% → 82%

**Phase 3 (Month 2-3):**
- ✅ Task contexts decoupled (ACLs implemented)
- ✅ 14 → 10 generic classes remaining (opportunistic)
- ✅ Zero orchestration-domain coupling defects

**Phase 4 (Ongoing):**
- ✅ 30 min/week glossary maintenance sustained
- ✅ 60% glossary adoption rate achieved
- ✅ Developer satisfaction score: 4.5/5

---

### Exit Criteria (Initiative Complete)

**MUST Criteria:**
- [ ] All Phase 1-2 deliverables complete (38 hours)
- [ ] 5 top-priority classes renamed with tests passing
- [ ] 3 terminology conflicts resolved and documented
- [ ] Directives updated and enforced in code review
- [ ] Zero breaking changes to collaboration workflow

**SHOULD Criteria:**
- [ ] Task context boundaries implemented (ADR-XXX)
- [ ] CQRS pattern evaluated and decision documented
- [ ] 10-14 generic classes refactored opportunistically
- [ ] Linguistic health score ≥80/100

**COULD Criteria:**
- [ ] Glossary automation in CI pipeline
- [ ] Module restructuring aligned with contexts
- [ ] Developer onboarding time reduced to 1 week

---

## Common Misunderstandings

### ❌ "This is a big bang rewrite"
**Reality:** Incremental, phased approach. Most work opportunistic (Boy Scout rule).

### ❌ "We need perfect DDD implementation"
**Reality:** Pragmatic DDD. Bounded contexts ≠ full tactical patterns. Just clear boundaries.

### ❌ "Refactoring will break everything"
**Reality:** Comprehensive test coverage required. Backward compatibility preserved. Incremental migration supported.

### ❌ "Glossary will be ignored"
**Reality:** Enforced via directives in code review. Living document, not static artifact.

### ❌ "This delays feature work"
**Reality:** Prevents future delays. Refactoring happens during normal feature work (not separate sprints).

---

## Open Questions

### Unresolved Requirements
- [ ] **Q1:** Final names for `OrchestrationConfigLoader` and `AgentSpecRegistry`?
  - **Assigned to:** Architect Alphonso + Team
  - **Target Date:** 2026-02-18 (Week 1)
  - **Blocking:** Phase 2 weeks 3-4

- [ ] **Q2:** CQRS implementation decision?
  - **Assigned to:** Architect Alphonso (after Researcher Ralph completes primer)
  - **Target Date:** 2026-02-25 (Week 2)
  - **Blocking:** ADR-XXX finalization

### Design Decisions Needed
- [ ] **D1:** Prefer from_yaml()/to_yaml() methods vs. separate Parser class?
  - **Options:** 
    1. Dataclass methods (simpler)
    2. Separate Parser class (more extensible)
  - **Decision Maker:** Architect Alphonso
  - **Context:** PR feedback requested simplification

- [ ] **D2:** Module restructuring in Phase 3 or defer to future?
  - **Options:**
    1. Include in Phase 3 (architectural consistency)
    2. Defer to separate initiative (reduce scope)
  - **Decision Maker:** Planning Petra + Architect Alphonso
  - **Context:** Module restructuring is COULD have, may be deferred

### Clarifications Required
- [ ] **C1:** What is acceptable "leniency" for generic naming in infrastructure code?
  - **Who to ask:** Code Reviewer Cindy + Backend Developers
  - **Why it matters:** Need clear guidelines to avoid false positives in directive enforcement

- [ ] **C2:** Should glossary automation be CI warning or hard failure?
  - **Who to ask:** Manager Mike + Team
  - **Why it matters:** Enforcement level affects adoption vs. friction balance

---

## Out of Scope

**Explicitly NOT included in this initiative:**

1. **Database Introduction**
   - **Reason:** File-system simplicity is architectural constraint (ADR-008)
   - **Future:** Revisit in microservice extraction (2027+)

2. **Event-Driven Architecture**
   - **Reason:** Overkill for current file-based coordination
   - **Future:** Consider if real-time requirements emerge

3. **Full DDD Tactical Patterns**
   - **Reason:** Pragmatic application, not textbook implementation
   - **Future:** Introduce incrementally as complexity demands (Domain Events, Repository, etc.)

4. **Legacy Code Complete Rewrite**
   - **Reason:** Opportunistic refactoring only (Boy Scout rule)
   - **Note:** Preserve working orchestration patterns

5. **Agent Identity Refactoring**
   - **Reason:** Low priority (Signal 2), minimal impact
   - **Future:** Consider during agent framework v2 design

6. **Comprehensive Module Restructuring**
   - **Reason:** COULD have, may be deferred based on capacity
   - **Future:** Separate initiative if architectural misalignment grows

---

## Acceptance Criteria Summary

**This initiative is DONE when:**

- [ ] All MUST requirements (FR-M1, FR-M2, FR-M3) implemented
- [ ] All SHOULD requirements (FR-S1, FR-S2, FR-S3) implemented OR deferral documented with rationale
- [ ] All MUST scenarios pass acceptance tests
- [ ] All business rules (BR*) enforced in code review
- [ ] All technical constraints (TC*) validated
- [ ] Open questions resolved and documented
- [ ] Directives updated and approved
- [ ] Glossaries expanded and promoted to canonical status
- [ ] ADR-XXX finalized and published
- [ ] Success metrics tracked and exit criteria met
- [ ] Developer onboarding time reduced to 1 week (measured)
- [ ] Zero terminology debates in code review (4-week rolling window)

---

## Risks and Mitigations

### Risk 1: Breaking Changes During Refactoring
**Probability:** Medium  
**Impact:** High  
**Mitigation:**
- Comprehensive test coverage (≥85%) required before refactoring
- Incremental migration with backward compatibility shims
- Code review scrutiny on import changes
- Integration tests for cross-context scenarios

---

### Risk 2: Scope Creep (Too Many Classes)
**Probability:** High  
**Impact:** Medium  
**Mitigation:**
- MoSCoW prioritization strict (5 MUST, rest SHOULD/COULD)
- Top 5 classes only in Phase 2
- Remaining classes opportunistic (Boy Scout rule)
- No dedicated "refactoring sprints"

---

### Risk 3: Team Capacity Shortage
**Probability:** Medium  
**Impact:** Medium  
**Mitigation:**
- Distributed work across team (not single-threaded)
- Opportunistic approach (during feature work)
- Phase 3 can be extended to Month 4 if needed
- COULD features deferrable without failure

---

### Risk 4: ADR-XXX Blocked by Disagreement
**Probability:** Low  
**Impact:** High  
**Mitigation:**
- Architect Alphonso has binding decision authority
- Escalation path: Draft → Team Review → Decision (1 week max)
- Fallback: Simpler ACL approach (current proposal)
- CQRS evaluation separate (can defer if contentious)

---

### Risk 5: Glossary Maintenance Neglected
**Probability:** Medium  
**Impact:** Low  
**Mitigation:**
- Curator Claire ownership (30 min/week commitment)
- Living Glossary Practice (doctrine) provides structure
- Monthly review in team sync
- CI validation (COULD have) reduces manual burden

---

## Change Log

Track significant changes to this specification:

| Date | Author | Change | Reason |
|------|--------|--------|--------|
| 2026-02-11 | Analyst Annie | Initial draft created | PR feedback from @stijn-dejongh |

---

## Approval

### Reviewers

| Role | Name | Date | Status | Comments |
|------|------|------|--------|----------|
| Architect | Architect Alphonso | - | ⏳ Pending | Strategic validation needed |
| Planning Lead | Planning Petra | - | ⏳ Pending | Phasing and estimation review |
| Code Reviewer | Code Reviewer Cindy | - | ⏳ Pending | Directive updates and enforcement |
| Backend Developer | Backend Benny | - | ⏳ Pending | Implementability review |
| Stakeholder | @stijn-dejongh | - | ⏳ Pending | Feedback provider validation |

### Sign-Off

**Final Approval:**
- **Date:** [Pending]
- **Approved By:** [Pending]
- **Status:** Draft (ready for review)

---

## Metadata

**Tags:** `#initiative-spec` `#terminology` `#refactoring` `#language-first-architecture` `#bounded-context` `#ddd`

**Related Files:**
- Template: `docs/templates/specifications/feature-spec-template.md`
- Assessment: `work/conceptual-alignment-assessment-synthesis.md`
- ADR: `docs/architecture/adrs/_drafts/ADR-XXX-task-context-boundary-definition.md`
- ADR: `docs/architecture/adrs/ADR-042-shared-task-domain-model.md`
- ADR: `docs/architecture/adrs/ADR-043-status-enumeration-standard.md`
- Directive: `.github/agents/directives/034_spec_driven_development.md`
- Directive: `.github/agents/directives/035_specification_frontmatter_standards.md`

**Navigation:**
- Related Initiative: `specifications/initiatives/conceptual-alignment/initiative.md`
- Parent Context: Language-First Architecture Maturation Epic

---

## Validation Evidence

⚠️ **Pre-Implementation Validation**

This specification was created following Analyst Annie's operating procedure:

### ✅ 1. Clarify Requirements
- **Evidence:** Multi-agent assessment reports reviewed (Architect, Code Reviewer, Lexical)
- **Assumptions:** Documented in Open Questions section
- **Ambiguity Resolution:** PR feedback from @stijn-dejongh incorporated

### ✅ 2. Explore Representative Data
- **Evidence:** 
  - 189 "task" occurrences analyzed
  - 19 generic classes identified with examples
  - 163 Python files scanned for terminology patterns
- **Edge Cases:** Generic naming acceptable in framework/infrastructure (documented)

### ✅ 3. Author Spec
- **Template:** Feature spec template adapted for initiative scope
- **Structure:** MoSCoW requirements, Given/When/Then scenarios, Common Misunderstandings
- **Frontmatter:** Directive 035 YAML format with 7 features defined

### ⚠️ 4. Validate (Pending)
- **Next Steps:**
  - Architect Alphonso review (strategic alignment)
  - Planning Petra review (phasing and estimation)
  - Team review (implementability and naming decisions)
- **Validation Script:** Not applicable (requirement validation, not data validation)

### 5. Handoff (After Approval)
- **Planning Petra:** Create phased tasks per strategy
- **Backend Developers:** Implement refactoring per acceptance criteria
- **Code Reviewer Cindy:** Enforce directives with templates

---

## Notes for Implementers

**When executing this initiative:**

1. **Start with Phase 1** - Foundation (directives) prevents future violations
2. **Prioritize backward compatibility** - Tests must pass at each step
3. **Use Boy Scout rule** - Most refactoring during normal feature work
4. **Reference glossary** - Single source of truth for terminology
5. **Escalate ambiguity early** - Open questions section guides decision-making
6. **Track opportunistic progress** - Update feature status as work completes
7. **Celebrate incremental wins** - Linguistic health score progress visible

**Success pattern:**
> "Not a big bang rewrite, but continuous improvement. Each PR leaves the codebase clearer than before."

---

**✅ Specification complete. Ready for stakeholder review.**

---

_Prepared by Analyst Annie following Spec-Driven Development (Directive 034) and Language-First Architecture approach._
