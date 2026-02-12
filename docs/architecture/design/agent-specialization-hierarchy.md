# Agent Specialization Hierarchy: Architecture Design

**Version:** 1.0.0
**Date:** 2026-02-12
**Status:** APPROVED
**Author:** Architect Alphonso
**Reviewers:** TBD

---

## Executive Summary

This document defines the **Agent Specialization Hierarchy** pattern for multi-agent orchestration systems. It formalizes the concept of parent-child relationships between agents, where specialized agents inherit and refine their parent's collaboration contract for narrower contexts (language, framework, domain, writing style).

**Problem:** Orchestration systems favor generic agents (Backend Benny) over more specialized agents (Python Pedro, Java Jenny) when context-appropriate specialists exist.

**Solution:** Explicit specialization hierarchy with context-based routing via `SELECT_APPROPRIATE_AGENT` tactic, considering workload, complexity, and local customization.

**Impact:** Improved task routing accuracy, better workload distribution, support for repository-specific specialists via `.doctrine-config` overrides.

---

## Table of Contents

1. [Context & Problem Statement](#context--problem-statement)
2. [Design Goals](#design-goals)
3. [Conceptual Model](#conceptual-model)
4. [Domain Model](#domain-model)
5. [Routing Algorithm](#routing-algorithm)
6. [Agent Profile Schema](#agent-profile-schema)
7. [SELECT_APPROPRIATE_AGENT Tactic](#select_appropriate_agent-tactic)
8. [Handoff Protocol Enhancement](#handoff-protocol-enhancement)
9. [Reassignment Pass](#reassignment-pass)
10. [Local Specialization Override](#local-specialization-override)
11. [Implementation Phases](#implementation-phases)
12. [Testing Strategy](#testing-strategy)
13. [Migration Path](#migration-path)
14. [Trade-Offs & Risks](#trade-offs--risks)
15. [Related Decisions](#related-decisions)

---

## Context & Problem Statement

### Current State

Multi-agent orchestration systems (Manager Mike) assign tasks to agents based on explicit `agent` field in task metadata or simple keyword matching. When multiple agents could handle a task, the system lacks a principled way to select the most appropriate specialist.

**Observed Issues:**

1. **Suboptimal Routing:** Python-specific tasks assigned to Backend Benny instead of Python Pedro
2. **No Workload Awareness:** Overloaded specialists not detected, tasks pile up
3. **No Complexity Consideration:** Complex tasks given to narrow specialists who lack broader context
4. **No Local Customization:** Repository-specific specialists (`.doctrine-config`) not automatically discovered
5. **Manual Handoff Overhead:** Agents must explicitly know all downstream specialists

**Example Failure:**
```yaml
# Task: Implement FastAPI endpoint
task:
  agent: backend-benny  # Generic assignment
  files: ["src/api/users.py"]

# Should route to python-pedro:
# - Language: Python
# - Framework: FastAPI
# - Files: *.py
```

### Desired State

**Intelligent Routing:**
- Python tasks → Python Pedro (if available and not overloaded)
- Java tasks → Java Jenny (if available and not overloaded)
- Generic backend tasks → Backend Benny (fallback)
- User guide tasks → User Guide Ursula (if defined in `.doctrine-config`)

**Automatic Fallback:**
- Specialist overloaded → route to parent
- No specialist match → route to generalist parent

**Handoff Enhancement:**
- Handoff to "backend-benny" automatically checks for Python Pedro / Java Jenny
- Local specialists in `.doctrine-config` discovered and preferred

---

## Design Goals

1. **Specialization Precision:** Route tasks to most specific qualified agent
2. **Workload Distribution:** Prevent specialist overload, balance across agents
3. **Complexity Awareness:** Match task complexity to agent capability breadth
4. **Local Customization:** Support repository-specific specialists via `.doctrine-config`
5. **Backward Compatibility:** Existing tasks continue to work, gradual migration
6. **Transparency:** All routing decisions logged with rationale
7. **Simplicity:** Minimal schema changes, reuse existing patterns
8. **Generalizability:** Support language, framework, domain, style specializations

---

## Conceptual Model

### Inheritance Hierarchy

```
Agent (Abstract)
  │
  ├── Coordinator (Manager Mike)
  │
  └── Specialist Agents
        │
        ├── Backend Specialist (Backend Benny) [parent]
        │     ├── Python Specialist (Python Pedro) [child]
        │     ├── Java Specialist (Java Jenny) [child]
        │     └── Node.js Specialist [future child]
        │
        ├── Frontend Specialist (Frontend Freddy) [parent]
        │     ├── React Specialist [future child]
        │     └── Vue Specialist [future child]
        │
        ├── Writer-Editor (Editor Eddy) [parent]
        │     ├── User Guide Specialist (Ursula) [local child]
        │     └── API Docs Specialist [future child]
        │
        └── Other Specialists (Architect, Analyst, etc.)
```

### Key Relationships

| Relationship | Example | Meaning |
|--------------|---------|---------|
| **Parent** | Backend Benny | Generalist with broad collaboration contract |
| **Child** | Python Pedro | Specialist inheriting parent contract, narrower context |
| **Sibling** | Java Jenny ↔ Python Pedro | Peer specialists with same parent |
| **Specializes** | Pedro specializes Benny | Child refines parent's scope |
| **Falls back to** | Pedro → Benny | Child delegates to parent when out of scope |

---

## Domain Model

### Core Entities

#### Agent
```yaml
Agent:
  name: string                    # Unique identifier (e.g., "python-pedro")
  description: string             # Brief purpose statement
  specializes_from: string?       # Parent agent name (optional)
  routing_priority: int           # 0-100, default 50 (parents), 60-90 (specialists)
  max_concurrent_tasks: int       # Workload threshold
  specialization_context:         # When to prefer this agent
    language: string[]?
    frameworks: string[]?
    file_patterns: string[]?
    domain_keywords: string[]?
    writing_style: string[]?
    complexity_preference: string[]?
```

#### Specialization Context
```yaml
SpecializationContext:
  language:               # Programming languages
    - python
    - java
  frameworks:             # Frameworks/libraries
    - flask
    - spring
  file_patterns:          # Glob patterns
    - "**/*.py"
    - "**/pom.xml"
  domain_keywords:        # Domain/task keywords
    - api
    - validation
  writing_style:          # For writing-focused agents
    - technical
    - instructional
  complexity_preference:  # Preferred task complexity
    - low
    - medium
    - high
```

#### Task Context (Inferred)
```yaml
TaskContext:
  files: string[]                # File paths from task
  language: string?              # Inferred from extensions
  frameworks: string[]           # Inferred from imports/deps
  domain_keywords: string[]      # Extracted from description
  complexity: enum               # low | medium | high
  priority: enum                 # low | normal | high | critical
```

#### Agent Selection Result
```yaml
SelectionResult:
  selected_agent: string
  match_score: float             # 0.0-1.0
  workload_adjusted_score: float
  complexity_adjusted_score: float
  rationale: string
  fallback_agent: string?
  decision_factors: string[]
```

---

## Routing Algorithm

### High-Level Flow

```
Task → Extract Context → Discover Candidates → Calculate Scores
  → Adjust for Workload → Adjust for Complexity → Resolve Ties
  → Return Selection
```

### Detailed Steps

#### Step 1: Extract Task Context

**Input:** Task YAML
**Output:** TaskContext object

```python
def extract_task_context(task):
    """Extract context from task for agent matching."""
    context = TaskContext()

    # Infer language from file extensions
    context.language = infer_language(task.files)

    # Extract frameworks from task description or file contents
    context.frameworks = extract_frameworks(task.description, task.files)

    # Extract domain keywords from title and description
    context.domain_keywords = extract_keywords(task.title, task.description)

    # Read explicit complexity (or infer from description length/scope)
    context.complexity = task.metadata.get('complexity', infer_complexity(task))

    # Read priority
    context.priority = task.priority

    return context
```

#### Step 2: Discover Candidate Agents

**Input:** TaskContext
**Output:** List of candidate agents

```python
def discover_candidates(task_context):
    """Find agents whose context matches task."""
    candidates = []

    # Load agents from doctrine/agents/
    doctrine_agents = load_agents('doctrine/agents/')

    # Load local agents from .doctrine-config/custom-agents/
    local_agents = load_agents('.doctrine-config/custom-agents/')

    # Combine and filter
    all_agents = doctrine_agents + local_agents

    for agent in all_agents:
        if agent_matches_context(agent, task_context):
            candidates.append(agent)

            # Also add parent as fallback
            if agent.specializes_from:
                parent = find_agent(agent.specializes_from, all_agents)
                if parent and parent not in candidates:
                    candidates.append(parent)

    return candidates
```

**Matching Logic:**
```python
def agent_matches_context(agent, task_context):
    """Check if agent's specialization matches task context."""

    # No context = generalist (always matches)
    if not agent.specialization_context:
        return True

    # Language match
    if task_context.language:
        if agent.specialization_context.language:
            if task_context.language in agent.specialization_context.language:
                return True

    # Framework match
    if task_context.frameworks:
        if agent.specialization_context.frameworks:
            overlap = set(task_context.frameworks) & set(agent.specialization_context.frameworks)
            if overlap:
                return True

    # File pattern match
    if task_context.files:
        if agent.specialization_context.file_patterns:
            for file in task_context.files:
                for pattern in agent.specialization_context.file_patterns:
                    if fnmatch(file, pattern):
                        return True

    # Domain keyword match
    if task_context.domain_keywords:
        if agent.specialization_context.domain_keywords:
            overlap = set(task_context.domain_keywords) & set(agent.specialization_context.domain_keywords)
            if overlap:
                return True

    # No match
    return False
```

#### Step 3: Calculate Match Scores

**Input:** Candidates + TaskContext
**Output:** Scored candidates

```python
def calculate_match_score(agent, task_context):
    """Calculate how well agent matches task context."""
    score = 0.0

    # Language match (40% weight for programming tasks)
    if task_context.language and agent.specialization_context.language:
        if task_context.language in agent.specialization_context.language:
            score += 0.40

    # Framework match (20% weight)
    if task_context.frameworks and agent.specialization_context.frameworks:
        overlap = set(task_context.frameworks) & set(agent.specialization_context.frameworks)
        framework_score = len(overlap) / max(len(task_context.frameworks), 1)
        score += 0.20 * framework_score

    # File pattern match (20% weight)
    if task_context.files and agent.specialization_context.file_patterns:
        matching_files = count_matching_files(task_context.files, agent.file_patterns)
        pattern_score = matching_files / max(len(task_context.files), 1)
        score += 0.20 * pattern_score

    # Domain keyword match (10% weight)
    if task_context.domain_keywords and agent.specialization_context.domain_keywords:
        overlap = set(task_context.domain_keywords) & set(agent.domain_keywords)
        keyword_score = len(overlap) / max(len(task_context.domain_keywords), 1)
        score += 0.10 * keyword_score

    # Exact match bonus (10% weight)
    if is_exact_match(agent.specialization_context, task_context):
        score += 0.10

    # Generalist penalty (if no specific matches)
    if score == 0.0 and not agent.specializes_from:
        score = 0.50  # Generalist fallback score

    return score
```

#### Step 4: Adjust for Workload

**Input:** Scored candidates
**Output:** Workload-adjusted scores

```python
def adjust_for_workload(candidates):
    """Apply workload penalty to overloaded agents."""

    for candidate in candidates:
        # Count active tasks
        active_tasks = count_active_tasks(candidate.name)

        # Calculate penalty
        if active_tasks <= 2:
            penalty = 0.0  # No penalty
        elif active_tasks <= 4:
            penalty = 0.15  # 15% penalty
        else:
            penalty = 0.30  # 30% penalty

        # Apply penalty
        candidate.workload_adjusted_score = candidate.match_score * (1 - penalty)

    return candidates
```

#### Step 5: Adjust for Complexity

**Input:** Workload-adjusted candidates + task complexity
**Output:** Complexity-adjusted scores

```python
def adjust_for_complexity(candidates, task_complexity):
    """Adjust scores based on task complexity and agent preference."""

    for candidate in candidates:
        # Check if agent prefers this complexity
        if candidate.specialization_context.complexity_preference:
            if task_complexity in candidate.complexity_preference:
                boost = 1.10  # 10% boost for preferred complexity
            elif candidate.specializes_from:
                # Specialist handling non-preferred complexity
                boost = 0.95  # 5% penalty
            else:
                boost = 1.0  # Generalist, no adjustment
        else:
            boost = 1.0  # No preference, no adjustment

        # Special case: high complexity prefers parents
        if task_complexity == 'high' and candidate.specializes_from:
            boost *= 0.90  # Additional 10% penalty for high complexity

        candidate.complexity_adjusted_score = candidate.workload_adjusted_score * boost

    return candidates
```

#### Step 6: Resolve Ties

**Input:** Complexity-adjusted candidates
**Output:** Single selected agent

```python
def resolve_ties(candidates, task_context):
    """Select single agent from candidates."""

    # Sort by final score (descending)
    candidates.sort(key=lambda c: c.complexity_adjusted_score, reverse=True)

    # Check if top candidates have same score
    top_score = candidates[0].complexity_adjusted_score
    top_candidates = [c for c in candidates if c.complexity_adjusted_score == top_score]

    if len(top_candidates) == 1:
        return top_candidates[0], "highest_adjusted_score"

    # Tie resolution: prefer language match for programming tasks
    if task_context.language:
        language_matches = [c for c in top_candidates
                           if task_context.language in c.specialization_context.get('language', [])]
        if language_matches:
            return language_matches[0], "language_match_preference"

    # Tie resolution: prefer higher routing priority
    top_candidates.sort(key=lambda c: c.routing_priority, reverse=True)
    if top_candidates[0].routing_priority > top_candidates[1].routing_priority:
        return top_candidates[0], "highest_routing_priority"

    # Tie resolution: Manager Mike free choice
    # Log decision and select first candidate
    selected = top_candidates[0]
    logger.info(f"Tie between {[c.name for c in top_candidates]}, selecting {selected.name} (free choice)")
    return selected, "manager_free_choice"
```

---

## Agent Profile Schema

### Parent Agent Example (Backend Benny)

```yaml
---
name: backend-benny
description: Backend development generalist
tools: [read, write, search, edit, MultiEdit, Bash, Grep, Docker, Java, Python]

# No specializes_from (this is a parent)
routing_priority: 50  # Default parent priority
max_concurrent_tasks: 8  # Higher capacity as fallback

# Broad specialization context
specialization_context:
  domain_keywords:
    - backend
    - api
    - service
    - integration
    - database
    - persistence
  complexity_preference:
    - medium
    - high
---
```

### Child Agent Example (Python Pedro)

```yaml
---
name: python-pedro
description: Python development specialist applying ATDD + TDD
tools: [read, write, edit, MultiEdit, Bash, Grep, Python, pytest, ruff, mypy, black]

specializes_from: backend-benny  # Parent agent
routing_priority: 80              # Higher than parent
max_concurrent_tasks: 5

specialization_context:
  language:
    - python
  frameworks:
    - flask
    - fastapi
    - pytest
    - pydantic
    - sqlalchemy
  file_patterns:
    - "**/*.py"
    - "**/pyproject.toml"
    - "**/requirements.txt"
    - "**/setup.py"
  domain_keywords:
    - python
    - pytest
    - flask
    - fastapi
    - pydantic
  complexity_preference:
    - low
    - medium
    - high
---
```

### Local Specialist Example (User Guide Ursula)

**File:** `.doctrine-config/custom-agents/user-guide-ursula.agent.md`

```yaml
---
name: user-guide-ursula
description: User guide specialist for repository-specific documentation
tools: [read, write, edit, Bash, Grep]

specializes_from: writer-editor  # Inherits from Editor Eddy
routing_priority: 85              # Higher than parent (local override)
max_concurrent_tasks: 3

specialization_context:
  domain_keywords:
    - user-guide
    - tutorial
    - onboarding
    - quickstart
  writing_style:
    - instructional
    - beginner-friendly
  file_patterns:
    - "docs/guides/**/*.md"
    - "docs/tutorials/**/*.md"
  complexity_preference:
    - low
    - medium
---
```

---

## SELECT_APPROPRIATE_AGENT Tactic

**Location:** `doctrine/tactics/SELECT_APPROPRIATE_AGENT.tactic.md`

**Purpose:** Determine most appropriate agent for a task considering specialization hierarchy, context matching, workload, and complexity.

**Invoked By:**
- Manager Mike during initial task assignment
- Manager Mike during handoff processing
- Manager Mike during reassignment pass

**See Full Tactic:** [Implementation Roadmap - Phase 2](#phase-2-select_appropriate_agent-tactic)

---

## Handoff Protocol Enhancement

### Current Handoff

```yaml
# Task result from Python Pedro
result:
  status: completed
  next_agent: backend-benny  # Explicit handoff to parent
  next_task_title: "Deploy API to staging"
  next_artefacts: ["src/api/users.py"]
```

### Enhanced Handoff

Manager Mike processes handoff:

```python
def process_handoff(completed_task):
    """Process task handoff with specialist awareness."""
    result = completed_task.result
    next_agent = result.next_agent

    # Check if next_agent is a parent agent
    parent_agents = get_parent_agents()

    if next_agent in parent_agents:
        # Invoke SELECT_APPROPRIATE_AGENT to find specialist
        task_context = extract_context_from_handoff(result)
        selection = select_appropriate_agent(task_context)

        if selection.selected_agent != next_agent:
            # Override with specialist
            logger.info(f"Handoff override: {next_agent} → {selection.selected_agent}")
            logger.info(f"Rationale: {selection.rationale}")
            next_agent = selection.selected_agent

    # Create handoff task
    create_task(agent=next_agent, ...)
```

**Example:**
```yaml
# Original handoff to backend-benny
next_agent: backend-benny
next_artefacts: ["src/api/new_feature.py"]

# Manager Mike detects Python context
# Invokes SELECT_APPROPRIATE_AGENT
# Routes to python-pedro instead

# Final task assignment
task:
  agent: python-pedro  # Overridden
  context:
    original_handoff: backend-benny
    routing_override: true
    selection_rationale: "Python context detected (*.py files), specialist available, workload acceptable"
```

---

## Reassignment Pass

### Purpose

Periodic review of task assignments to upgrade generic assignments to specialists when:
- New specialists introduced
- Specialist workload decreases
- Task context becomes clearer

### Trigger

- Manual: Human invokes `python tools/scripts/reassignment_pass.py`
- Automatic: Weekly cron job (configurable)
- Event-driven: After new agent profile added

### Procedure

```python
def reassignment_pass():
    """Review and upgrade task assignments to specialists."""

    # Scan for eligible tasks
    tasks = []
    for agent_dir in glob('work/assigned/*/'):
        for task_file in glob(f'{agent_dir}/*.yaml'):
            task = read_yaml(task_file)
            # Only reassign new/assigned (not in_progress)
            if task.status in ['new', 'assigned']:
                # Don't reassign pinned tasks
                if not task.get('pinned', False):
                    tasks.append(task)

    reassignments = []

    for task in tasks:
        current_agent = task.agent

        # Invoke SELECT_APPROPRIATE_AGENT
        task_context = extract_task_context(task)
        selection = select_appropriate_agent(task_context)

        if selection.selected_agent != current_agent:
            # Reassign
            move_task(task, current_agent, selection.selected_agent)
            reassignments.append({
                'task_id': task.id,
                'from': current_agent,
                'to': selection.selected_agent,
                'reason': selection.rationale
            })

    # Generate report
    generate_reassignment_report(reassignments)

    return reassignments
```

### Safety Constraints

- ❌ Do NOT reassign `in_progress` tasks
- ❌ Do NOT reassign pinned tasks (`task.pinned: true`)
- ❌ Do NOT create loops (A → B, later B → A)
- ✅ Log all reassignments
- ✅ Generate audit report
- ✅ Commit changes atomically

### Report Example

```markdown
# Reassignment Pass Report
**Date:** 2026-02-12T10:30:00Z
**Duration:** 2.3 seconds
**Tasks Reviewed:** 47
**Reassignments:** 12

## Summary
- Specialist upgrades: 10
- Parent fallbacks: 2 (specialist overload)

## Reassignments

| Task ID | From | To | Reason |
|---------|------|-----|--------|
| T-001 | backend-benny | python-pedro | Python language match (score 0.95) |
| T-002 | backend-benny | java-jenny | Java language match (score 0.93) |
| T-003 | python-pedro | backend-benny | Specialist overloaded (6/5 tasks) |
| T-004 | writer-editor | user-guide-ursula | Local specialist match (user guide) |

## Agent Workload After Reassignment

| Agent | Active Tasks | Capacity | Utilization |
|-------|-------------|----------|-------------|
| python-pedro | 5 | 5 | 100% |
| java-jenny | 3 | 5 | 60% |
| backend-benny | 4 | 8 | 50% |
| user-guide-ursula | 1 | 3 | 33% |
```

---

## Local Specialization Override

### Mechanism

Repositories can define custom specialists in `.doctrine-config/custom-agents/` that:
1. Inherit from doctrine framework agents
2. Override routing for specific contexts
3. Automatically discovered by SELECT_APPROPRIATE_AGENT

### Priority Boost

Local specialists receive +20 routing priority boost to ensure they're preferred over framework agents.

```python
def load_all_agents():
    """Load agents with local override priority."""
    agents = []

    # Load framework agents
    framework_agents = load_agents('doctrine/agents/')
    agents.extend(framework_agents)

    # Load local agents with priority boost
    local_agents = load_agents('.doctrine-config/custom-agents/')
    for agent in local_agents:
        agent.routing_priority += 20  # Local override boost
        agent.is_local = True
    agents.extend(local_agents)

    return agents
```

### Use Cases

1. **Repository-Specific Styles:** User Guide Ursula for product documentation
2. **Domain Specialists:** Payment Processing Paul for financial domain
3. **Framework Variants:** React 18 Rachel vs React 17 Robin
4. **Team Preferences:** Preferred coding style or testing approach

---

## Implementation Phases

### Phase 1: Core Decision & Glossary (6-8 hours)
- Create DDR-011 (Agent Specialization Hierarchy)
- Update GLOSSARY.md with new terminology
- Document domain model

### Phase 2: SELECT_APPROPRIATE_AGENT Tactic (10-12 hours)
- Write complete tactic document
- Implement routing algorithm (Python)
- Add logging and telemetry

### Phase 3: Agent Profile Schema (8-10 hours)
- Update agent profile template
- Update Python Pedro, Java Jenny, Backend Benny profiles
- Create validation script

### Phase 4: Manager Mike Enhancement (10-12 hours)
- Update Manager Mike profile
- Implement handoff protocol enhancement
- Implement reassignment pass

### Phase 5: Validation & Testing (12-16 hours)
- Write hierarchy validation script
- Create test scenarios
- Integration testing

### Phase 6: Documentation (8-10 hours)
- Migration guide
- Repository adopter guide
- Decision tree ("When to use which agent")

**Total:** 54-68 hours

---

## Testing Strategy

### Unit Tests

```python
# Test context extraction
def test_extract_python_context():
    task = {
        'files': ['src/api.py', 'tests/test_api.py'],
        'description': 'Add Flask endpoint'
    }
    context = extract_task_context(task)
    assert context.language == 'python'
    assert 'flask' in context.frameworks

# Test match scoring
def test_python_specialist_scores_higher():
    task_context = TaskContext(language='python', files=['api.py'])
    pedro_score = calculate_match_score(python_pedro, task_context)
    benny_score = calculate_match_score(backend_benny, task_context)
    assert pedro_score > benny_score

# Test workload penalty
def test_overloaded_specialist_penalized():
    set_agent_workload('python-pedro', 6)  # Over max
    candidates = [python_pedro, backend_benny]
    adjusted = adjust_for_workload(candidates)
    # Benny should score higher after workload adjustment
    assert adjusted[1].workload_adjusted_score > adjusted[0].workload_adjusted_score
```

### Integration Tests

```python
# Test end-to-end routing
def test_python_task_routes_to_pedro():
    task = create_task(files=['src/api.py'], description='Add endpoint')
    selected = select_appropriate_agent(extract_task_context(task))
    assert selected.selected_agent == 'python-pedro'

# Test local specialist override
def test_local_specialist_preferred():
    # Create local agent
    create_local_agent('user-guide-ursula', parent='writer-editor')
    task = create_task(files=['docs/guides/intro.md'], domain=['user-guide'])
    selected = select_appropriate_agent(extract_task_context(task))
    assert selected.selected_agent == 'user-guide-ursula'

# Test handoff override
def test_handoff_to_parent_routes_to_specialist():
    task_result = {
        'next_agent': 'backend-benny',
        'next_artefacts': ['src/service.py']
    }
    handoff_task = process_handoff(task_result)
    assert handoff_task.agent == 'python-pedro'  # Overridden
```

### Validation Tests

```python
# Test circular dependency detection
def test_circular_dependency_detected():
    agents = [
        Agent(name='A', specializes_from='B'),
        Agent(name='B', specializes_from='A')
    ]
    issues = validate_hierarchy(agents)
    assert any('Circular' in issue for issue in issues)

# Test missing parent detection
def test_missing_parent_detected():
    agents = [Agent(name='child', specializes_from='nonexistent')]
    issues = validate_hierarchy(agents)
    assert any('Missing parent' in issue for issue in issues)
```

---

## Migration Path

### Step 1: Introduce Schema (Non-Breaking)
- Add optional fields to agent profiles
- Existing agents continue working without changes

### Step 2: Update Specialist Profiles
- Add hierarchy metadata to Python Pedro, Java Jenny
- Test routing with updated profiles

### Step 3: Deploy SELECT_APPROPRIATE_AGENT
- Manager Mike starts using tactic for new tasks
- Existing tasks unchanged

### Step 4: Run Reassignment Pass
- Review existing tasks
- Upgrade assignments where beneficial
- Monitor for issues

### Step 5: Enable Handoff Override
- Manager Mike applies specialist routing to handoffs
- Monitor handoff chains

### Step 6: Documentation & Rollout
- Publish migration guide
- Train repository adopters
- Collect feedback

---

## Trade-Offs & Risks

### Trade-Offs

| Decision | Pro | Con |
|----------|-----|-----|
| **Explicit hierarchy** | Clear relationships, toolable | Requires schema changes |
| **Context-based routing** | Intelligent selection | Complex algorithm |
| **Workload awareness** | Prevents overload | Adds computational overhead |
| **Local override** | Customization power | Discovery complexity |
| **Reassignment pass** | Gradual migration | Potential churn |

### Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Circular dependencies** | Medium | Validation script, profile linter |
| **Complex routing bugs** | High | Comprehensive test suite, logging |
| **Performance degradation** | Low | Algorithm optimization, caching |
| **Migration disruption** | Medium | Gradual rollout, backward compatibility |
| **Specialist overload** | Medium | Workload monitoring, parent fallback |

---

## Related Decisions

- **DDR-004:** File-Based Asynchronous Coordination Protocol
- **DDR-005:** Task Lifecycle State Management Protocol
- **DDR-007:** Coordinator Agent Orchestration Pattern
- **DDR-011:** Agent Specialization Hierarchy (this document)

---

## Appendices

### Appendix A: Glossary Terms

See `doctrine/GLOSSARY.md` for:
- Agent Specialization Hierarchy
- Parent Agent
- Child Agent / Specialist Agent
- Specialization Context
- Routing Priority
- Reassignment Pass

### Appendix B: Reference Implementation

See `tools/orchestration/agent_selector.py` for Python reference implementation.

### Appendix C: Decision Tree

```
Task arrives
  │
  ├─ Extract context (language, files, domain)
  │
  ├─ Discover candidates (doctrine + .doctrine-config)
  │
  ├─ Calculate match scores
  │   ├─ Language match? +40%
  │   ├─ Framework match? +20%
  │   ├─ File pattern match? +20%
  │   ├─ Domain keyword match? +10%
  │   └─ Exact match? +10%
  │
  ├─ Adjust for workload
  │   ├─ 0-2 tasks? No penalty
  │   ├─ 3-4 tasks? -15%
  │   └─ 5+ tasks? -30%
  │
  ├─ Adjust for complexity
  │   ├─ Low complexity? Specialist +10%
  │   ├─ Medium? Neutral
  │   └─ High? Parent +10%, Specialist -10%
  │
  ├─ Resolve ties
  │   ├─ Highest score? Select
  │   ├─ Language match for code? Prefer
  │   ├─ Highest priority? Prefer
  │   └─ Else: Manager Mike free choice
  │
  └─ Assign task
```

---

**Document Status:** APPROVED
**Next Review:** 2026-05-01 or after 3 months of implementation
**Change Log:**
- 2026-02-12: Initial version (Architect Alphonso)
