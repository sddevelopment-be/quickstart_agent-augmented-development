---
id: "SPEC-ASH-001"
title: "Agent Specialization Hierarchy"
status: "implemented"
initiative: "Agent Specialization Hierarchy"
priority: "HIGH"
epic: "Orchestration Intelligence"
target_personas: ["agentic-framework-core-team", "software_engineer", "process_architect", "automation_agent"]
features:
  - id: "FEAT-ASH-001-01"
    title: "Context-Based Agent Routing (SELECT_APPROPRIATE_AGENT)"
    status: "implemented"
    description: "Tactic and algorithm that selects the most appropriate agent for a task based on specialization context, workload, and complexity"
  - id: "FEAT-ASH-001-02"
    title: "Agent Profile Schema Enhancement"
    status: "implemented"
    description: "Extended agent profile frontmatter with hierarchy metadata (specializes_from, routing_priority, specialization_context)"
  - id: "FEAT-ASH-001-03"
    title: "Handoff Protocol Enhancement"
    status: "implemented"
    description: "Automatic specialist discovery during task handoff processing"
  - id: "FEAT-ASH-001-04"
    title: "Reassignment Pass"
    status: "implemented"
    description: "Periodic review and upgrade of generic task assignments to specialist agents"
  - id: "FEAT-ASH-001-05"
    title: "Local Specialist Discovery"
    status: "implemented"
    description: "Automatic discovery and priority boosting of repository-specific specialists defined in .doctrine-config"
  - id: "FEAT-ASH-001-06"
    title: "Hierarchy Validation"
    status: "implemented"
    description: "Validation script detecting circular dependencies, missing parents, and priority conflicts"
completion: "2026-02-12"
created: "2026-02-12"
updated: "2026-02-12"
author: "analyst-annie"
---

# Specification: Agent Specialization Hierarchy

**Status:** Draft
**Created:** 2026-02-12
**Last Updated:** 2026-02-12
**Author:** Analyst Annie
**Stakeholders:** Human-in-Charge, Architect Alphonso, Planning Petra, Manager Mike

---

## User Story

**As a** Coordinator Agent (Manager Mike)
**I want** to automatically route tasks to the most contextually appropriate specialist agent
**So that** tasks are handled by agents with the deepest relevant expertise, improving output quality and reducing manual routing overhead

**Alternative: Acceptance Criterion Format**
**Given** a task with Python-specific files and description arrives for assignment
**When** Manager Mike invokes the agent selection process
**Then** the task is assigned to Python Pedro (not the generic Backend Benny)
**And** the selection rationale is logged for traceability
**Unless** Python Pedro is overloaded, in which case the task falls back to Backend Benny

**Target Personas:**
- Agentic Framework Core Team (Primary) - Link: `docs/audience/agentic-framework-core-team.md`
- Software Engineer / Platform Engineer (Primary) - Link: `docs/audience/software_engineer.md`
- Process Architect (Secondary) - Link: `docs/audience/process_architect.md`
- Automation Agent (Secondary) - Link: `docs/audience/automation_agent.md`

---

## Overview

The Agent Specialization Hierarchy formalizes parent-child relationships between agents, where specialized agents inherit and refine their parent's collaboration contract for narrower contexts (language, framework, domain, writing style). This specification defines the functional requirements for context-based routing, workload-aware fallback, handoff enhancement, periodic reassignment, and local specialist discovery.

**Context:**
- **Problem Solved:** The orchestration system (Manager Mike) currently assigns tasks using explicit `agent` fields or simple keyword matching. When multiple agents could handle a task, no principled mechanism exists to select the most appropriate specialist. This leads to suboptimal routing (Python tasks assigned to Backend Benny instead of Python Pedro), no workload awareness (specialists become overloaded), and no automatic discovery of repository-specific specialists.
- **Why Needed Now:** The agent roster has grown to include language-specific specialists (Python Pedro, Java Jenny) that are underutilized because the coordinator lacks awareness of their specialization boundaries. Manual handoff overhead increases with each new specialist added.
- **Constraints:**
  - MUST preserve backward compatibility with existing task assignments and agent profiles
  - MUST work with file-based orchestration (no external services or databases)
  - MUST support gradual adoption (existing agents continue to function without hierarchy metadata)
  - MUST remain LLM-provider-agnostic (routing logic must not depend on specific model capabilities)

**Related Documentation:**
- Architecture Design: [`docs/architecture/design/agent-specialization-hierarchy.md`](../../../docs/architecture/design/agent-specialization-hierarchy.md)
- DDR-011: [`doctrine/decisions/DDR-011-agent-specialization-hierarchy.md`](../../../doctrine/decisions/DDR-011-agent-specialization-hierarchy.md)
- DDR-007: Coordinator Agent Orchestration Pattern
- DDR-004: File-Based Asynchronous Coordination Protocol
- DDR-005: Task Lifecycle State Management Protocol
- Architect Work Log: [`work/reports/logs/architect/2026-02-12T0900-agent-specialization-hierarchy-evaluation.md`](../../../work/reports/logs/architect/2026-02-12T0900-agent-specialization-hierarchy-evaluation.md)

---

## Problem Statement

### Current State

Multi-agent orchestration assigns tasks through one of two mechanisms:

1. **Explicit assignment:** The task YAML contains an `agent` field set by the task creator (human or Manager Mike).
2. **Simple keyword matching:** Manager Mike selects an agent based on task title/description keywords.

Both mechanisms treat agents as a flat pool. No hierarchy, context matching, or workload awareness exists.

### Observed Failures

| Failure Mode | Example | Impact |
|---|---|---|
| **Suboptimal routing** | Python FastAPI task assigned to Backend Benny instead of Python Pedro | Lower output quality; specialist expertise unused |
| **Specialist overload** | All Python tasks routed to Python Pedro regardless of workload | Tasks pile up; throughput degrades |
| **No complexity matching** | Complex cross-domain task given to narrow specialist | Specialist lacks broader context; rework needed |
| **Missing local specialists** | User guide task not routed to User Guide Ursula (defined in `.doctrine-config`) | Repository-specific expertise unused |
| **Manual handoff burden** | Agents must explicitly name every downstream specialist in handoff | New specialists require updating every handoff source |

### Business Value

- **Improved task quality:** Tasks handled by agents with the deepest relevant expertise
- **Better throughput:** Workload-aware routing prevents bottlenecks at specialist agents
- **Reduced coordination overhead:** Automatic specialist discovery eliminates manual routing decisions
- **Repository customization:** Teams can define project-specific specialists without modifying the core framework
- **Scalable agent roster:** Adding new specialists does not require updating every existing agent or task template

---

## Target Personas

### Persona 1: Agentic Framework Core Team (Primary)

**Needs from this feature:**
- Formalized hierarchy model that is toolable and validatable
- Transparent routing decisions with logged rationale
- Extensible pattern that generalizes beyond programming languages (domain, style, framework)
- Validation tooling to detect misconfiguration (circular dependencies, missing parents)

**Success looks like:** Routing accuracy above 90% for tasks where a specialist exists, with every routing decision logged and traceable.

### Persona 2: Software Engineer / Platform Engineer (Primary)

**Needs from this feature:**
- Repository-specific specialists defined in `.doctrine-config` that are automatically discovered
- Clear documentation on how to add custom specialists
- Backward-compatible adoption path (existing tasks continue working)
- Visible routing rationale (why was this agent selected?)

**Success looks like:** Adding a new specialist agent requires only creating a profile file; no other changes needed for automatic discovery.

### Persona 3: Process Architect (Secondary)

**Needs from this feature:**
- Documented hierarchy model with clear parent-child relationship semantics
- Workload distribution visibility (utilization per agent)
- Reassignment audit trails for governance
- Pattern documentation usable as a reference for other orchestration systems

**Success looks like:** Reassignment pass reports show workload rebalancing across agents with full audit trail.

### Persona 4: Automation Agent (Secondary)

**Needs from this feature:**
- Extended agent profile schema that is parseable from YAML frontmatter
- Deterministic routing behavior (same inputs produce same outputs)
- Clear fallback chain (specialist overloaded leads to parent, not random agent)
- Specialization context that is machine-readable and validatable

**Success looks like:** Agent profiles with hierarchy metadata pass validation without errors; routing produces deterministic results.

---

## Scenarios and Behavior

### Scenario 1: Python Task Routing to Specialist

**Context:** Manager Mike receives a new task involving Python files and must decide which agent to assign.

**Given:** A task arrives with the following characteristics:
- Files: `["src/api/users.py", "tests/test_users.py"]`
- Description: "Implement FastAPI user authentication endpoint"
- Priority: HIGH
**And:** Python Pedro is available with 2 active tasks (below capacity of 5)
**And:** Backend Benny is available with 3 active tasks (below capacity of 8)
**When:** Manager Mike invokes SELECT_APPROPRIATE_AGENT for this task
**Then:** Python Pedro is selected as the assigned agent
**And:** The selection rationale includes: language match (Python), framework match (FastAPI), file pattern match (*.py)
**And:** The match score for Python Pedro is higher than for Backend Benny
**And:** The routing decision is logged with all scoring factors

**Personas:** Agentic Framework Core Team, Automation Agent
**Priority:** MUST

### Scenario 2: Specialist Overload with Parent Fallback

**Context:** Python Pedro has reached capacity. A new Python task arrives and must fall back to the parent agent.

**Given:** A task arrives with Python-specific context (language: Python, files: *.py)
**And:** Python Pedro has 5 active tasks (at maximum capacity of 5)
**And:** Backend Benny has 3 active tasks (below capacity of 8)
**When:** Manager Mike invokes SELECT_APPROPRIATE_AGENT for this task
**Then:** Backend Benny is selected as the assigned agent
**And:** The selection rationale states: "Specialist python-pedro at capacity (5/5); falling back to parent backend-benny"
**And:** The routing decision log shows the workload penalty applied to Python Pedro's score

**Personas:** Agentic Framework Core Team, Process Architect
**Priority:** MUST

### Scenario 3: Local Specialist Discovery

**Context:** A repository has defined a custom specialist (User Guide Ursula) in `.doctrine-config/custom-agents/`. A user guide task arrives.

**Given:** A task arrives with the following characteristics:
- Files: `["docs/guides/getting-started.md"]`
- Description: "Write quickstart tutorial for new users"
- Domain keywords: user-guide, tutorial, onboarding
**And:** User Guide Ursula is defined in `.doctrine-config/custom-agents/user-guide-ursula.agent.md`
**And:** User Guide Ursula declares `specializes_from: writer-editor`
**And:** Editor Eddy (writer-editor) is also available
**When:** Manager Mike invokes SELECT_APPROPRIATE_AGENT for this task
**Then:** User Guide Ursula is selected as the assigned agent
**And:** The selection rationale includes: "Local specialist match (user guide), domain keyword match, +20 local priority boost"
**And:** User Guide Ursula's effective routing priority is her declared priority plus 20

**Personas:** Software Engineer, Agentic Framework Core Team
**Priority:** MUST

### Scenario 4: Handoff Enhancement (Parent to Specialist Override)

**Context:** An agent completes a task and hands off to Backend Benny. Manager Mike detects that the handoff target has a more appropriate specialist.

**Given:** A completed task produces a handoff result:
- `next_agent: backend-benny`
- `next_artefacts: ["src/api/new_feature.py"]`
- `next_task_title: "Implement validation logic for new feature"`
**And:** Python Pedro is available with 2 active tasks
**When:** Manager Mike processes the handoff
**Then:** Manager Mike invokes SELECT_APPROPRIATE_AGENT on the handoff context
**And:** Python Pedro is selected instead of Backend Benny
**And:** The created task records the routing override:
- `agent: python-pedro`
- `context.original_handoff: backend-benny`
- `context.routing_override: true`
- `context.selection_rationale: "Python context detected (*.py files), specialist available, workload acceptable"`

**Personas:** Automation Agent, Agentic Framework Core Team
**Priority:** MUST

### Scenario 5: Reassignment Pass

**Context:** New specialists have been introduced or specialist workload has decreased. Manager Mike reviews existing task assignments to upgrade from generic agents to specialists.

**Given:** The following tasks exist in `work/collaboration/assigned/`:
- Task A: assigned to `backend-benny`, files: `["src/api/auth.py"]`, status: `assigned`
- Task B: assigned to `backend-benny`, files: `["src/models/user.py"]`, status: `assigned`
- Task C: assigned to `backend-benny`, files: `["src/api/payments.java"]`, status: `assigned`
- Task D: assigned to `python-pedro`, files: `["src/config.py"]`, status: `in_progress`
- Task E: assigned to `backend-benny`, files: `["src/api/health.py"]`, status: `assigned`, pinned: `true`
**And:** Python Pedro has 1 active task (well below capacity)
**And:** Java Jenny has 0 active tasks
**When:** Manager Mike runs the reassignment pass
**Then:** Task A is reassigned from `backend-benny` to `python-pedro` (Python match)
**And:** Task B is reassigned from `backend-benny` to `python-pedro` (Python match)
**And:** Task C is reassigned from `backend-benny` to `java-jenny` (Java match)
**And:** Task D is NOT reassigned (status is `in_progress`)
**And:** Task E is NOT reassigned (pinned: true)
**And:** A reassignment report is generated listing all changes with rationale
**And:** The report includes post-reassignment workload distribution per agent

**Personas:** Process Architect, Agentic Framework Core Team
**Priority:** MUST

### Scenario 6: No Specialist Available (Generalist Fallback)

**Context:** A task arrives in a language or domain for which no specialist exists.

**Given:** A task arrives with Rust-specific context (language: Rust, files: *.rs)
**And:** No Rust specialist agent exists in doctrine or `.doctrine-config`
**And:** Backend Benny is available
**When:** Manager Mike invokes SELECT_APPROPRIATE_AGENT for this task
**Then:** Backend Benny is selected as the assigned agent (generalist fallback)
**And:** The selection rationale states: "No specialist match for language 'rust'; assigning to generalist backend-benny"
**And:** No error is raised (graceful degradation)

**Personas:** Agentic Framework Core Team, Automation Agent
**Priority:** MUST

### Scenario 7: High-Complexity Task Prefers Parent

**Context:** A highly complex cross-domain task arrives. Specialists prefer narrower scope; parents are better suited for broad context work.

**Given:** A task arrives with the following characteristics:
- Files: `["src/api/users.py", "src/api/auth.py", "src/services/email.py", "src/models/user.py"]`
- Description: "Refactor user authentication to support multi-tenant architecture"
- Complexity: HIGH
**And:** Python Pedro is available with 1 active task
**And:** Backend Benny is available with 2 active tasks
**When:** Manager Mike invokes SELECT_APPROPRIATE_AGENT for this task
**Then:** The complexity adjustment penalizes the specialist score and boosts the parent score
**And:** If Backend Benny's adjusted score exceeds Python Pedro's adjusted score, Backend Benny is selected
**And:** The selection rationale references the complexity factor in the decision

**Personas:** Agentic Framework Core Team, Process Architect
**Priority:** SHOULD

### Scenario 8: Hierarchy Validation Detects Circular Dependency

**Context:** A configuration error introduces a circular parent-child relationship.

**Given:** Agent profiles define:
- Agent A with `specializes_from: agent-b`
- Agent B with `specializes_from: agent-a`
**When:** The hierarchy validation script runs
**Then:** The script reports: "Circular dependency detected: agent-a -> agent-b -> agent-a"
**And:** The validation exits with a non-zero status code
**And:** No tasks are assigned using the invalid hierarchy

**Personas:** Agentic Framework Core Team, Software Engineer
**Priority:** MUST

---

## Functional Requirements (MoSCoW)

### MUST Have (Critical - Feature unusable without these)

**FR-M1:** The system SHALL select the most contextually appropriate agent for a task based on specialization context matching (language, frameworks, file patterns, domain keywords).
- **Rationale:** Core value proposition of the hierarchy. Without context matching, routing remains suboptimal.
- **Personas Affected:** All target personas
- **Success Criteria:** For tasks where a specialist exists and is available, the specialist is selected at least 90% of the time in test scenarios.

**FR-M2:** The system SHALL apply a workload penalty to agents approaching or exceeding their `max_concurrent_tasks` threshold, causing fallback to parent agents when specialists are overloaded.
- **Rationale:** Prevents specialist bottlenecks that degrade throughput.
- **Personas Affected:** Agentic Framework Core Team, Process Architect
- **Success Criteria:** When a specialist is at capacity, the parent agent is selected instead.

**FR-M3:** The system SHALL support a `specializes_from` field in agent profile frontmatter that declares the parent agent.
- **Rationale:** Explicit hierarchy required for fallback chains and routing priority.
- **Personas Affected:** All target personas
- **Success Criteria:** Agent profiles with `specializes_from` are parsed correctly; parent-child relationship is discoverable by tooling.

**FR-M4:** The system SHALL support a `specialization_context` block in agent profile frontmatter containing at least: `language`, `frameworks`, `file_patterns`, and `domain_keywords`.
- **Rationale:** Machine-readable context conditions are required for automated routing.
- **Personas Affected:** All target personas
- **Success Criteria:** Context fields are parseable from YAML; matching logic correctly evaluates each field type.

**FR-M5:** The system SHALL support a `routing_priority` field (integer 0-100) in agent profile frontmatter to influence selection order.
- **Rationale:** Numeric priority enables deterministic tie resolution and explicit preference ordering.
- **Personas Affected:** All target personas
- **Success Criteria:** Higher priority agents are preferred when match scores are equal.

**FR-M6:** The system SHALL log every routing decision with the selected agent, match score, workload factors, and textual rationale.
- **Rationale:** Transparency is a core design goal; debugging routing decisions requires audit trail.
- **Personas Affected:** Agentic Framework Core Team, Process Architect
- **Success Criteria:** Every invocation of SELECT_APPROPRIATE_AGENT produces a structured log entry containing agent name, score breakdown, and rationale string.

**FR-M7:** The system SHALL intercept handoffs to parent agents and invoke SELECT_APPROPRIATE_AGENT to determine if a specialist should be assigned instead.
- **Rationale:** Reduces manual handoff overhead; agents do not need to know all downstream specialists.
- **Personas Affected:** Automation Agent, Agentic Framework Core Team
- **Success Criteria:** Handoff to `backend-benny` with Python context results in assignment to `python-pedro` (if available).

**FR-M8:** The system SHALL provide a reassignment pass that reviews tasks with status `new` or `assigned` and upgrades generic assignments to specialists when a better match exists.
- **Rationale:** Enables gradual migration and handles the case where specialists are introduced after tasks are created.
- **Personas Affected:** Process Architect, Agentic Framework Core Team
- **Success Criteria:** Reassignment pass correctly identifies and moves eligible tasks; produces an audit report.

**FR-M9:** The reassignment pass SHALL NOT reassign tasks with status `in_progress` or tasks marked as `pinned: true`.
- **Rationale:** Safety constraint to avoid disrupting active work or overriding explicit human decisions.
- **Personas Affected:** Process Architect, Agentic Framework Core Team
- **Success Criteria:** In-progress and pinned tasks remain unchanged after reassignment pass.

**FR-M10:** The system SHALL discover local specialist agents defined in `.doctrine-config/custom-agents/` and include them in routing candidate evaluation.
- **Rationale:** Repository customization is a key design goal; local specialists should be automatically available.
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** An agent defined only in `.doctrine-config/custom-agents/` is selected when its context matches a task.

**FR-M11:** The system SHALL validate agent hierarchy configuration, detecting and reporting: circular dependencies, missing parent references, and duplicate agent names.
- **Rationale:** Configuration errors in hierarchy can cause routing failures or infinite loops.
- **Personas Affected:** All target personas
- **Success Criteria:** Validation script exits non-zero and reports all detected issues.

**FR-M12:** The system SHALL maintain backward compatibility: agent profiles without hierarchy metadata MUST continue to function as before, treated as standalone agents with default routing priority.
- **Rationale:** Gradual adoption requires that existing profiles work without modification.
- **Personas Affected:** All target personas
- **Success Criteria:** Existing agent profiles without `specializes_from` or `specialization_context` fields are loaded without errors and participate in routing as generalists.

### SHOULD Have (Important - Feature degraded without these)

**FR-S1:** The system SHOULD adjust routing scores based on task complexity, preferring parent (generalist) agents for HIGH complexity tasks that require broader context.
- **Rationale:** Narrow specialists may lack cross-domain awareness needed for complex tasks.
- **Personas Affected:** Agentic Framework Core Team, Process Architect
- **Success Criteria:** HIGH complexity tasks show a measurable score boost for parent agents and penalty for specialists.
- **Workaround if omitted:** All tasks routed by context match alone; complex tasks may need manual reassignment.

**FR-S2:** Local specialist agents defined in `.doctrine-config/custom-agents/` SHOULD receive a +20 routing priority boost over framework-defined agents.
- **Rationale:** Repository-specific specialists should be preferred over generic framework agents for domain-appropriate tasks.
- **Personas Affected:** Software Engineer, Agentic Framework Core Team
- **Success Criteria:** A local specialist with declared priority 65 is treated as priority 85 during routing.
- **Workaround if omitted:** Users manually set higher routing_priority values in local agent profiles.

**FR-S3:** The system SHOULD support a `writing_style` field in specialization context for writing-focused agents.
- **Rationale:** Generalizes the hierarchy beyond programming to documentation and content creation.
- **Personas Affected:** Agentic Framework Core Team, Process Architect
- **Success Criteria:** Writing style matching correctly routes documentation tasks to appropriate writing specialists.
- **Workaround if omitted:** Writing specialists matched only by domain_keywords and file_patterns.

**FR-S4:** The system SHOULD support a `complexity_preference` field in specialization context, indicating which complexity levels an agent is suited for.
- **Rationale:** Enables the complexity adjustment algorithm to make informed decisions.
- **Personas Affected:** Agentic Framework Core Team
- **Success Criteria:** Agents with `complexity_preference: [low, medium]` receive a score penalty for HIGH complexity tasks.
- **Workaround if omitted:** Complexity adjustment uses only the parent/child relationship (specialists penalized for all high-complexity tasks).

**FR-S5:** The reassignment pass SHOULD generate a structured report listing all reassignments with: task ID, source agent, target agent, rationale, and post-reassignment workload per agent.
- **Rationale:** Audit trail and workload visibility needed for governance.
- **Personas Affected:** Process Architect, Agentic Framework Core Team
- **Success Criteria:** Report is generated in Markdown format and includes all specified fields.
- **Workaround if omitted:** Reassignment actions are logged individually but no consolidated report is produced.

**FR-S6:** The system SHOULD detect and prevent reassignment loops (A reassigns to B, later B reassigns back to A).
- **Rationale:** Prevents infinite reassignment churn between agents.
- **Personas Affected:** Agentic Framework Core Team
- **Success Criteria:** A task that was previously reassigned from agent X to agent Y is not reassigned back to agent X in a subsequent pass.
- **Workaround if omitted:** Manual review of reassignment reports to detect loops.

### COULD Have (Enhances experience)

**FR-C1:** The system COULD support automatic reassignment triggers (event-driven when a new agent profile is added, or scheduled periodically).
- **Rationale:** Reduces manual intervention for reassignment.
- **Personas Affected:** Agentic Framework Core Team
- **Success Criteria:** Reassignment pass runs automatically after a new `.agent.md` file is committed.
- **If omitted:** Reassignment pass must be invoked manually.

**FR-C2:** The system COULD cache routing decisions for repeated identical task contexts to improve performance.
- **Rationale:** Reduces computational overhead for large task sets.
- **Personas Affected:** Automation Agent
- **Success Criteria:** Cached decisions are returned for identical task contexts; cache is invalidated when agent profiles change.
- **If omitted:** Every routing decision is computed from scratch (acceptable for typical task volumes).

**FR-C3:** The system COULD provide a visualization of the agent hierarchy (tree diagram) generated from agent profile metadata.
- **Rationale:** Improves discoverability and understanding of hierarchy relationships.
- **Personas Affected:** Software Engineer, Process Architect
- **Success Criteria:** A script generates a textual or graphical hierarchy tree from agent profiles.
- **If omitted:** Users inspect individual agent profiles to understand hierarchy.

**FR-C4:** The system COULD support multi-level specialization (grandchild agents, such as FastAPI-specific specialist under Python Pedro).
- **Rationale:** Some domains may benefit from deeper specialization trees.
- **Personas Affected:** Agentic Framework Core Team
- **Success Criteria:** Three-level hierarchy (grandparent -> parent -> child) routes correctly with cascading fallback.
- **If omitted:** Hierarchy is limited to two levels (parent -> child), which covers the primary use cases.

### WON'T Have (Explicitly out of scope for this iteration)

**FR-W1:** The system will NOT implement real-time workload monitoring via external metrics services.
- **Rationale:** File-based orchestration principle prohibits external service dependencies. Workload is computed from task file counts in the collaboration directory.
- **Future Consideration:** Could be added if dashboard integration provides live workload APIs.

**FR-W2:** The system will NOT support dynamic agent profile modification at runtime (hot-reload of hierarchy changes).
- **Rationale:** Agent profiles are static documents loaded at session initialization. Changes require a new session or explicit reload.
- **Future Consideration:** Could be added with file watcher integration in a future iteration.

**FR-W3:** The system will NOT implement machine learning-based routing optimization.
- **Rationale:** Deterministic, rule-based routing is preferred for transparency and debuggability.
- **Future Consideration:** Could be explored once sufficient routing decision data is collected for training.

**FR-W4:** The system will NOT implement cross-repository agent sharing or federation.
- **Rationale:** Scope is limited to single-repository orchestration.
- **Future Consideration:** Federation could be explored as a separate initiative.

---

## Constraints and Business Rules

### Business Rules

**BR1:** An agent may have at most one parent (single inheritance).
- **Applies to:** Agent profile schema, hierarchy validation
- **Enforcement:** Validation script rejects profiles declaring multiple parents

**BR2:** Parent agents MUST exist and be loadable at routing time.
- **Applies to:** Hierarchy validation, routing algorithm
- **Enforcement:** Validation script detects missing parent references; routing algorithm falls back to generalist pool if parent not found

**BR3:** Workload penalty thresholds are: 0-2 active tasks = no penalty; 3-4 = 15% penalty; 5+ = 30% penalty.
- **Applies to:** Routing algorithm (workload adjustment step)
- **Enforcement:** Routing logic applies tiered penalty based on active task count vs. max_concurrent_tasks

**BR4:** Local specialists (`.doctrine-config/custom-agents/`) receive a +20 routing priority boost over identically-scoped framework agents.
- **Applies to:** Agent discovery, priority calculation
- **Enforcement:** Routing algorithm applies boost during candidate scoring

**BR5:** Pinned tasks (`pinned: true`) are exempt from reassignment regardless of routing score.
- **Applies to:** Reassignment pass
- **Enforcement:** Reassignment pass skips pinned tasks unconditionally

### Technical Constraints

**TC1:** Routing algorithm execution time SHOULD remain under 500ms for a pool of up to 50 agents and 200 candidate tasks.
- **Measurement:** Wall-clock time for full routing pass
- **Rationale:** Routing is invoked during task assignment; delays affect orchestration throughput

**TC2:** Agent profile schema changes MUST be backward-compatible (all new fields optional).
- **Measurement:** Existing profiles load without errors
- **Rationale:** Gradual adoption is a core design goal

**TC3:** All hierarchy and routing logic MUST be implementable in Python 3.9+ without external service dependencies.
- **Measurement:** No network calls, database connections, or external API usage in routing path
- **Rationale:** File-based orchestration principle

### Non-Functional Requirements (MoSCoW)

**NFR-M1 (MUST):** Every routing decision SHALL produce a machine-readable log entry containing: timestamp, task ID, selected agent, match score, workload-adjusted score, and rationale string.
- **Measurement:** Log entries parseable by standard JSON or YAML parsers
- **Verification:** Log parsing test validates all required fields present

**NFR-M2 (MUST):** Hierarchy validation SHALL complete within 5 seconds for up to 100 agent profiles.
- **Measurement:** Wall-clock time for validation script
- **Verification:** Performance test with 100 synthetic profiles

**NFR-S1 (SHOULD):** Routing decisions for identical inputs SHOULD produce identical outputs (deterministic behavior).
- **Measurement:** Same task context + same agent pool + same workload state = same selected agent
- **Verification:** Repeated routing tests with fixed inputs

**NFR-S2 (SHOULD):** Reassignment pass reports SHOULD be human-readable Markdown suitable for inclusion in work logs.
- **Measurement:** Report renders correctly in standard Markdown viewers
- **Verification:** Manual review of generated reports

### Edge Cases and Limits

- **Maximum hierarchy depth:** 2 levels (parent -> child) in this iteration; deeper hierarchies are out of scope (FR-C4)
- **Maximum concurrent agents:** Routing algorithm designed for up to 50 agents; behavior above this untested
- **Empty candidate pool:** If no agent matches task context, the system SHALL fall back to the agent explicitly named in the task YAML (if any), or report an error if no agent is specified
- **Tie resolution order:** (1) Highest adjusted score, (2) Language match preference for programming tasks, (3) Highest routing priority, (4) Manager Mike free choice (first candidate)
- **Invalid specialization context:** If an agent profile contains unparseable specialization_context, the agent is treated as a generalist (no context match) and a validation warning is logged

---

## Success Metrics

### Routing Accuracy

| Metric | Target | Measurement Method |
|---|---|---|
| Specialist selected when available and not overloaded | >= 90% | Routing decision logs for tasks where a specialist context match exists |
| Correct parent fallback when specialist overloaded | 100% | Test scenarios with specialist at capacity |
| Local specialist selected when context matches | >= 95% | Routing tests with `.doctrine-config` agents present |

### Workload Distribution

| Metric | Target | Measurement Method |
|---|---|---|
| No specialist exceeds max_concurrent_tasks by more than 1 (race condition tolerance) | >= 95% of routing cycles | Workload snapshot after each routing decision |
| Parent agent utilization increases when specialists are at capacity | Measurable increase | Pre/post comparison of parent task counts |

### Operational Efficiency

| Metric | Target | Measurement Method |
|---|---|---|
| Reassignment pass reduces generic assignments | >= 50% of eligible tasks upgraded | Reassignment pass report |
| Handoff override rate (parent to specialist) | >= 70% of eligible handoffs | Handoff decision logs |
| Routing decision log completeness | 100% of decisions logged | Audit of routing log entries |

---

## Open Questions

### Unresolved Requirements

- [ ] **Q1:** Should the workload penalty thresholds (0-2/3-4/5+) be configurable per repository or fixed in the framework?
  - **Assigned to:** Architect Alphonso
  - **Target Date:** 2026-02-19
  - **Blocking:** FR-M2 implementation details (routing algorithm constants)

- [ ] **Q2:** Should the reassignment pass commit changes atomically (all-or-nothing) or individually per task?
  - **Assigned to:** Architect Alphonso
  - **Target Date:** 2026-02-19
  - **Blocking:** FR-M8 implementation details (reassignment script behavior)

### Design Decisions Needed

- [ ] **D1:** Match score weight distribution (language 40%, framework 20%, files 20%, keywords 10%, exact 10%) -- should these weights be configurable?
  - **Options:** (a) Fixed weights in framework, (b) Configurable via `.doctrine-config`, (c) Per-agent weight overrides
  - **Decision Maker:** Architect Alphonso
  - **Context:** Repositories with non-programming focus (documentation-heavy) may need different weight distributions

- [ ] **D2:** Should the `max_concurrent_tasks` field be mandatory or optional with a sensible default?
  - **Options:** (a) Required field, validation enforces presence, (b) Optional, default to 5
  - **Decision Maker:** Architect Alphonso
  - **Context:** Affects backward compatibility (FR-M12); mandatory field would break existing profiles

### Clarifications Required

- [ ] **C1:** What is the expected behavior when a local specialist declares `specializes_from` referencing a parent not present in the framework agents?
  - **Who to ask:** Architect Alphonso
  - **Why it matters:** Could occur if repository defines a completely custom hierarchy independent of framework agents

---

## Out of Scope

**Explicitly NOT included in this specification:**

1. **Real-time workload monitoring via external services**
   - **Reason:** Violates file-based orchestration principle; workload derived from task file counts
   - **Future:** Could integrate with dashboard APIs if built

2. **Machine learning-based routing optimization**
   - **Reason:** Deterministic routing preferred for transparency and debuggability
   - **Future:** Possible after routing decision data is collected at scale

3. **Cross-repository agent federation**
   - **Reason:** Single-repository scope for this iteration
   - **Future:** Could be a separate initiative

4. **Agent profile hot-reload**
   - **Reason:** Profiles are static documents per session
   - **Future:** File watcher integration could enable this

5. **Implementation details (code structure, class design, library selection)**
   - **Reason:** Implementation is left to developers following this spec
   - **Note:** See architecture design document for reference implementation pseudocode

---

## Acceptance Criteria Summary

**This feature is DONE when:**

- [ ] All MUST requirements (FR-M1 through FR-M12) are implemented
- [ ] All SHOULD requirements (FR-S1 through FR-S6) are implemented OR documented workarounds exist
- [ ] All 5 key scenarios (Scenarios 1-5) pass acceptance tests
- [ ] Scenarios 6-8 pass acceptance tests
- [ ] All business rules (BR1 through BR5) are enforced
- [ ] All technical constraints (TC1 through TC3) are met
- [ ] Hierarchy validation script detects circular dependencies, missing parents, and duplicate names
- [ ] Routing decision logs contain all required fields (NFR-M1)
- [ ] Open questions Q1, Q2, D1, D2, C1 are resolved
- [ ] Reassignment pass generates structured audit report
- [ ] Existing agent profiles without hierarchy metadata continue to function (backward compatibility)
- [ ] Documentation updated: migration guide, repository adopter guide, decision tree
- [ ] Target personas have validated the feature meets their needs

---

## Traceability

### Derives From (Strategic)

- **Architecture Design:** [`docs/architecture/design/agent-specialization-hierarchy.md`](../../../docs/architecture/design/agent-specialization-hierarchy.md) -- APPROVED 2026-02-12
- **Decision Record:** [`doctrine/decisions/DDR-011-agent-specialization-hierarchy.md`](../../../doctrine/decisions/DDR-011-agent-specialization-hierarchy.md) -- Proposed 2026-02-12
- **Related Decisions:** DDR-004 (File-Based Coordination), DDR-005 (Task Lifecycle), DDR-007 (Coordinator Pattern)
- **Architect Evaluation:** [`work/reports/logs/architect/2026-02-12T0900-agent-specialization-hierarchy-evaluation.md`](../../../work/reports/logs/architect/2026-02-12T0900-agent-specialization-hierarchy-evaluation.md)

### Feeds Into (Tactical)

- **Acceptance Tests:** To be created in `tests/acceptance/features/agent-specialization-hierarchy.feature`
- **Implementation Tasks:** To be created by Planning Petra after specification approval
- **Tactic Document:** `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md` (to be created)
- **Agent Profile Updates:** Python Pedro, Java Jenny, Backend Benny profiles to be updated
- **Validation Script:** `tools/validators/validate-agent-hierarchy.py` (to be created)

### Related Specifications

- **Dependencies:** None (this is a foundational orchestration feature)
- **Dependents:** Future specifications for agent dashboard integration, multi-level hierarchy support
- **Cross-References:** Specification-Driven Development (Directive 034), ATDD (Directive 016)

---

## Change Log

| Date | Author | Change | Reason |
|------|--------|--------|--------|
| 2026-02-12 | Analyst Annie | Initial draft created | Architecture design and DDR-011 completed; specification bridges intent to implementation |

---

## Approval

### Reviewers

| Role | Name | Date | Status | Comments |
|------|------|------|--------|----------|
| Architect | Architect Alphonso | - | Pending | Architecture design author; validate spec alignment |
| Planner | Planning Petra | - | Pending | Next agent; validate task breakdown feasibility |
| Coordinator | Manager Mike | - | Pending | Primary consumer; validate routing scenarios |
| Stakeholder | Human-in-Charge | - | Pending | Strategic alignment review |

### Sign-Off

**Final Approval:**
- **Date:** Pending
- **Approved By:** Pending
- **Status:** DRAFT -- ready for review

---

## Metadata

**Tags:** `#feature-spec` `#orchestration` `#agent-hierarchy` `#routing` `#specialization`

**Related Files:**
- Template: `doctrine/templates/specifications/feature-spec-template.md`
- Personas: `docs/audience/agentic-framework-core-team.md`, `docs/audience/software_engineer.md`, `docs/audience/process_architect.md`, `docs/audience/automation_agent.md`
- DDR: `doctrine/decisions/DDR-011-agent-specialization-hierarchy.md`
- Architecture: `docs/architecture/design/agent-specialization-hierarchy.md`
- Tasks: To be created by Planning Petra

**Navigation:**
- Parent Initiative: Agent Specialization Hierarchy
- Next Agent: Planning Petra (roadmap integration after approval)
