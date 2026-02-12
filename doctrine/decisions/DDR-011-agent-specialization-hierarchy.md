# DDR-011: Agent Specialization Hierarchy

**Status:** Accepted
**Date:** 2026-02-12
**Author:** Architect Alphonso
**Supersedes:** N/A
**Related:** DDR-007 (Coordinator Agent Orchestration Pattern)

---

## Context

Multi-agent orchestration systems assign tasks to agents based on explicit metadata or simple matching. When multiple agents could handle a task, current systems lack a principled way to select the most appropriate specialist.

**Problem Observed:**

- Python/Java tasks assigned to generic Backend Benny instead of Python Pedro / Java Jenny
- No workload awareness—specialists become overloaded
- No complexity consideration—narrow specialists given tasks requiring broader context
- Repository-specific specialists (`.doctrine-config`) not discovered automatically
- Manual handoff overhead—agents must know all downstream specialists

**Example Failure:**

```yaml
# Task: Implement FastAPI endpoint
task:
  agent: backend-benny  # Generic assignment
  files: [ "src/api/users.py" ]

# Should route to python-pedro (language + framework match)
```

**Root Cause:**
Lack of formalized specialization hierarchy where:

- Specialists inherit from parent agents
- Context-based routing selects most appropriate agent
- Workload and complexity inform selection
- Local customization supported

---

## Decision

**We establish Agent Specialization Hierarchy as a core orchestration pattern.**

### Core Concepts

1. **Parent-Child Relationships**
    - Specialist agents declare parent via `specializes_from` metadata
    - Specialists inherit parent's collaboration contract
    - Specialists operate in narrower context (language, framework, domain, style)

2. **Specialization Context**
    - Declarative conditions defining when specialist preferred:
        - `language`: Programming languages (python, java, etc.)
        - `frameworks`: Frameworks/libraries (flask, spring, etc.)
        - `file_patterns`: Glob patterns for file matching
        - `domain_keywords`: Domain/task keywords
        - `writing_style`: For writing-focused agents
        - `complexity_preference`: Preferred task complexity levels

3. **Routing Priority**
    - Numeric specificity score (0-100)
    - Parents default to 50
    - Specialists typically 60-90
    - Local specialists (+20 boost)

4. **SELECT_APPROPRIATE_AGENT Tactic**
    - Invoked by Manager Mike during:
        - Initial task assignment
        - Handoff processing
        - Reassignment pass
    - Algorithm:
        1. Extract task context (language, files, domain, complexity)
        2. Discover candidates (doctrine + .doctrine-config)
        3. Calculate match scores (language 40%, framework 20%, files 20%, keywords 10%, exact 10%)
        4. Adjust for agent workload (penalty if overloaded)
        5. Adjust for task complexity (specialists prefer low/medium, parents prefer high)
        6. Resolve ties (language match > score > priority > free choice)
        7. Return selection + rationale

5. **Handoff Enhancement**
    - Handoff to parent agent triggers specialist check
    - SELECT_APPROPRIATE_AGENT invoked to find more specific agent
    - Example: `next_agent: backend-benny` → routes to Python Pedro if Python context

6. **Reassignment Pass**
    - Manager Mike periodic review of task assignments
    - Upgrades generic assignments to specialists when available
    - Safety: Don't reassign in_progress or pinned tasks

7. **Local Specialization Override**
    - Repositories define custom specialists in `.doctrine-config/custom-agents/`
    - Local specialists receive +20 routing priority boost
    - Auto-discovered by SELECT_APPROPRIATE_AGENT

### Hierarchy Examples

```
Backend Specialist (Backend Benny) [parent, priority=50]
  ├── Python Specialist (Python Pedro) [child, priority=80]
  ├── Java Specialist (Java Jenny) [child, priority=80]
  └── Node.js Specialist [future child]

Frontend Specialist (Frontend Freddy) [parent, priority=50]
  ├── React Specialist [future child]
  └── Vue Specialist [future child]

Writer-Editor (Editor Eddy) [parent, priority=50]
  ├── User Guide Specialist (Ursula) [example local child, priority=85]
  └── API Docs Specialist [future child]
```

---

## Rationale

### Why Explicit Hierarchy?

**Clarity & Discoverability:**

- Parent-child relationships visible in profiles
- Tooling can validate and visualize hierarchy
- Humans understand specialization scope

**Intelligent Routing:**

- Context-based selection more accurate than keyword matching
- Workload awareness prevents specialist overload
- Complexity matching balances specialist vs generalist strengths

**Flexibility & Extensibility:**

- Generalizes beyond language (domain, style, framework)
- Supports local customization (`.doctrine-config` specialists)
- Backward compatible (parents remain valid fallback)

### Why Hybrid Approach (Explicit + Implicit)?

**Explicit:** Parent declared in `specializes_from` field
**Implicit:** Routing via context matching algorithm

**Advantage:** Combines discoverability (explicit) with flexibility (implicit)

### Why Context-Based Routing?

**Alternative Rejected:** Task creators specify specialist explicitly

**Problems:**

- Shifts burden to task creators (must know all specialists)
- Doesn't solve "Manager Mike favors generic agents" problem
- No automatic discovery of new specialists

**Chosen Approach:** SELECT_APPROPRIATE_AGENT tactic

**Benefits:**

- Automatic specialist discovery
- Consistent routing logic
- Transparent decision rationale
- Manager Mike handles complexity

### Why Workload Awareness?

**Problem:** Specialists become bottlenecks when overloaded

**Solution:** Workload penalty in routing algorithm

- 0-2 active tasks: No penalty
- 3-4 active tasks: 15% penalty
- 5+ active tasks: 30% penalty

**Result:** Automatic fallback to parent when specialist busy

### Why Complexity Adjustment?

**Insight:** Complex tasks may require broader context that specialists lack

**Adjustment:**

- Low complexity: Specialist +10% boost
- Medium complexity: Neutral
- High complexity: Parent +10%, Specialist -10%

**Rationale:** Parents (generalists) better suited for tasks requiring cross-domain knowledge

### Why Reassignment Pass?

**Use Case:** Gradual migration of existing tasks to specialists

**Triggers:**

- New specialist introduced
- Specialist workload decreases
- Manual invocation

**Safety:**

- Only reassign `new` / `assigned` tasks (not `in_progress`)
- Respect pinned tasks (`task.pinned: true`)
- Generate audit report

### Why Local Override?

**Use Case:** Repository-specific specialists

**Examples:**

- User Guide Ursula for product documentation style
- Payment Processing Paul for financial domain
- React 18 Rachel for specific framework version

**Mechanism:**

- Define in `.doctrine-config/custom-agents/`
- Receive +20 priority boost
- Auto-discovered by SELECT_APPROPRIATE_AGENT

---

## Consequences

### Positive

- ✅ **Accurate Routing:** Tasks assigned to most appropriate specialist
- ✅ **Workload Distribution:** Prevents specialist overload via automatic fallback
- ✅ **Complexity Matching:** Specialists handle focused tasks, parents handle complex
- ✅ **Local Customization:** Repositories can define custom specialists
- ✅ **Backward Compatible:** Existing tasks continue working, gradual migration
- ✅ **Transparency:** All routing decisions logged with rationale
- ✅ **Extensible:** Pattern generalizes beyond language (domain, style, framework)
- ✅ **Reduced Handoff Overhead:** Automatic specialist discovery in handoff chains

### Negative (Accepted Trade-Offs)

- ⚠️ **Schema Changes:** Agent profiles require new optional fields
- ⚠️ **Routing Complexity:** SELECT_APPROPRIATE_AGENT algorithm has multiple factors
- ⚠️ **Testing Burden:** Complex routing logic requires comprehensive test coverage
- ⚠️ **Migration Effort:** Existing specialist profiles need hierarchy metadata
- ⚠️ **Potential for Misconfiguration:** Invalid hierarchy (circular deps) possible

### Risks & Mitigations

| Risk                        | Mitigation                                                 |
|-----------------------------|------------------------------------------------------------|
| **Circular dependencies**   | Validation script detects cycles, profile linter           |
| **Complex routing bugs**    | Comprehensive test suite, detailed logging                 |
| **Performance degradation** | Algorithm optimization, caching, profiling                 |
| **Migration disruption**    | Gradual rollout, backward compatibility, reassignment pass |
| **Specialist overload**     | Workload monitoring, automatic fallback to parent          |

---

## Implementation

### Phase 1: Core Decision & Glossary (6-8h)

- ✅ Create DDR-011 (this document)
- Update `doctrine/GLOSSARY.md` with new terminology
- Document domain model in architecture design

### Phase 2: SELECT_APPROPRIATE_AGENT Tactic (10-12h)

- Create `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md`
- Implement routing algorithm (Python reference implementation)
- Add logging and telemetry

### Phase 3: Agent Profile Schema (8-10h)

- Update `doctrine/templates/agent-profile-template.md`
- Update Python Pedro, Java Jenny, Backend Benny profiles
- Create `tools/validators/validate-agent-hierarchy.py`

### Phase 4: Manager Mike Enhancement (10-12h)

- Update `doctrine/agents/manager.agent.md`
- Implement handoff protocol enhancement
- Implement reassignment pass

### Phase 5: Validation & Testing (12-16h)

- Write hierarchy validation script
- Create test scenarios (unit, integration, end-to-end)
- Validate with real task examples

### Phase 6: Documentation & Migration (8-10h)

- Migration guide for existing repositories
- Repository adopter guide (how to add custom specialists)
- Decision tree: "When to use which agent"

**Total Effort:** 54-68 hours

### Agent Profile Schema

**Template Enhancement:**

```yaml
---
name: agent-slug
description: Brief description
tools: [ ... ]

# Specialization Hierarchy (Optional)
specializes_from: parent-agent-slug    # Parent in hierarchy
routing_priority: 50                   # 0-100, default 50 (parents), 60-90 (specialists)
max_concurrent_tasks: 5                # Workload threshold

# Specialization Context (Optional - for specialists only)
specialization_context:
  language: [ python, java ]             # Programming languages
  frameworks: [ flask, spring, pytest ]  # Frameworks/libraries
  file_patterns: # Glob patterns
    - "**/*.py"
    - "**/pyproject.toml"
  domain_keywords: # Domain/task keywords
    - api
    - backend
  writing_style: [ technical, academic ] # For writing-focused agents
  complexity_preference: [ low, medium ] # Preferred task complexity
---
```

**Example: Python Pedro**

```yaml
---
name: python-pedro
specializes_from: backend-benny
routing_priority: 80
max_concurrent_tasks: 5
specialization_context:
  language: [ python ]
  frameworks: [ flask, fastapi, pytest, pydantic ]
  file_patterns: [ "**/*.py", "**/pyproject.toml" ]
  domain_keywords: [ python, pytest, flask ]
  complexity_preference: [ low, medium, high ]
---
```

**Example: Backend Benny (Parent)**

```yaml
---
name: backend-benny
routing_priority: 50  # Default parent priority
max_concurrent_tasks: 8  # Higher capacity as fallback
specialization_context:
  domain_keywords: [ backend, api, service, database ]
  complexity_preference: [ medium, high ]
---
```

### Validation

**Hierarchy Validation Script:**

```python
# tools/validators/validate-agent-hierarchy.py

def validate_hierarchy(agents):
    """Validate agent hierarchy configuration."""
    issues = []

    # Check 1: Circular dependencies
    for agent in agents:
        if detect_circular_parent(agent, agents):
            issues.append(f"Circular dependency: {agent.name}")

    # Check 2: Parent exists
    for agent in agents:
        if agent.specializes_from:
            if not find_agent(agent.specializes_from, agents):
                issues.append(f"Missing parent: {agent.specializes_from} for {agent.name}")

    # Check 3: Priority conflicts
    contexts = get_all_contexts(agents)
    for context in contexts:
        matching = [a for a in agents if a.matches_context(context)]
        priorities = [a.routing_priority for a in matching]
        if len(priorities) != len(set(priorities)):
            issues.append(f"Priority conflict in context: {context}")

    return issues
```

---

## Alternatives Considered

### Alternative 1: Implicit Capability-Based Routing

**Approach:** Manager Mike infers best agent from task metadata + agent capabilities (no explicit hierarchy)

**Pros:**

- No schema changes
- Flexible—new specialists auto-discovered
- Agents don't need to know their "parent"

**Cons:**

- ❌ Routing logic becomes complex heuristic
- ❌ Non-deterministic agent selection
- ❌ Hard to debug when wrong agent chosen
- ❌ No explicit hierarchy for humans to understand

**Rejected:** Lack of transparency and debuggability

### Alternative 2: Task-Driven Routing

**Approach:** Tasks declare required specialist type; fallback to generalist if unavailable

**Pros:**

- Task creator controls routing
- Simple coordinator logic (read field, route)
- Works with existing task schema

**Cons:**

- ❌ Shifts burden to task creators (must know specialist landscape)
- ❌ Doesn't solve "Manager Mike favors backend-dev" problem
- ❌ No automatic specialist discovery

**Rejected:** Doesn't solve the core problem

### Alternative 3: Flat Agent Pool (No Hierarchy)

**Approach:** All agents at same level, no parent-child relationships

**Pros:**

- Simple—no hierarchy to maintain
- No circular dependency risk
- Agents fully independent

**Cons:**

- ❌ No fallback mechanism when specialist unavailable
- ❌ No workload balancing via parent agents
- ❌ Duplicate capabilities across specialists (e.g., all need general backend skills)

**Rejected:** Doesn't leverage inheritance pattern benefits

---

## Related Decisions

- **DDR-004:** File-Based Asynchronous Coordination Protocol (task file structure)
- **DDR-005:** Task Lifecycle State Management Protocol (task states)
- **DDR-007:** Coordinator Agent Orchestration Pattern (Manager Mike role)
- **DDR-010:** Modular Agent Directive System Architecture (agent profile format)
- **DDR-011:** Agent Specialization Hierarchy (this decision)

---

## Terminology

**Agent Specialization Hierarchy:**
Parent-child relationship where specialized agents refine their parent's scope to narrower contexts. Orchestrator prefers specialists when context matches, falls back to parent when specialist unavailable or overloaded.

**Parent Agent:**
Generalist agent whose collaboration contract and capabilities are inherited and refined by specialist child agents. Serves as fallback when no specialist matches task context or specialists are overloaded.

**Child Agent / Specialist Agent:**
Agent that inherits parent's collaboration contract but operates in narrower specialization context. Declared via
`specializes_from` metadata in agent profile frontmatter.

**Specialization Context:**
Declarative conditions defining when specialist preferred over parent: language, frameworks, file patterns, domain keywords, writing style.

**Routing Priority:**
Numeric specificity score (0-100) for specialist agents. Higher priority agents preferred when multiple match context. Parent agents default to 50.

**Reassignment Pass:**
Manager Mike process that reviews existing task assignments and updates to use more specific specialist agents when available. Used for backward compatibility and after new specialists are introduced.

**SELECT_APPROPRIATE_AGENT:**
Orchestration tactic that determines most appropriate agent for a task considering specialization hierarchy, context matching, workload, and complexity.

---

## References

- **Architecture Design:** `docs/architecture/design/agent-specialization-hierarchy.md`
- **Work Log:** `work/reports/logs/architect/2026-02-12T0900-agent-specialization-hierarchy-evaluation.md`
- **Tactic:** `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md` (to be created)

---

## Approval

**Status:** Proposed
**Approval Required:** Human stakeholder
**Implementation Start:** After approval
**Expected Completion:** 6-8 weeks (54-68 hours total effort)

---

## Change Log

- **2026-02-12:** Initial decision proposal (Architect Alphonso)
