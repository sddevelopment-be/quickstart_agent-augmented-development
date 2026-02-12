# Tactic: Select Appropriate Agent for Task Assignment

**Invoked by:**
- Manager Mike during initial task assignment (inbox → assigned)
- Manager Mike during handoff processing (completed task with next_agent → check for specialist)
- Manager Mike during reassignment pass (periodic review of existing assignments)
- Any agent during delegation when unsure of best downstream agent

**Related:**
- [DDR-011 (Agent Specialization Hierarchy)](../decisions/DDR-011-agent-specialization-hierarchy.md)
- [DDR-007 (Coordinator Agent Orchestration Pattern)](../decisions/DDR-007-coordinator-agent-orchestration-pattern.md)
- [Manager Mike Profile](../agents/manager-mike.agent.md)
- [Agent Specialization Hierarchy Design](../../docs/architecture/design/agent-specialization-hierarchy.md)

**Glossary Terms:**
- Agent Specialization Hierarchy
- Parent Agent
- Child Agent / Specialist Agent
- Specialization Context
- Routing Priority
- Reassignment Pass

---

## Purpose

Determine the most appropriate agent to handle a task by analyzing task context, discovering candidate agents, calculating match scores, and applying workload and complexity adjustments. Ensures tasks are routed to the most specific qualified agent while preventing specialist overload.

**Apply when:**
- Assigning new tasks from inbox to specialists
- Processing task handoffs with generic parent agent targets
- Running periodic reassignment passes to upgrade generic assignments
- Delegating work when multiple potential agents exist
- Adding new specialist agents and reviewing existing assignments

---

## Preconditions

**Required inputs:**
- Task YAML file with:
  - `files`: List of file paths (for language/framework inference)
  - `title`: Task title (for keyword extraction)
  - `description`: Task description (for keyword and framework extraction)
  - `priority`: Task priority (critical, high, normal, low)
  - `metadata.complexity`: Optional complexity indicator (low, medium, high)

**Assumed context:**
- Agent profiles exist in `doctrine/agents/`
- Optional local agent profiles exist in `.doctrine-config/custom-agents/`
- Agent profiles include `specialization_context` fields
- Manager Mike has access to read all agent profiles
- Workload tracking available (count of active tasks per agent)

**Exclusions (when NOT to use):**
- Tasks explicitly pinned to specific agent (`task.pinned: true`)
- Tasks already in_progress (only reassign new/assigned tasks)
- Emergency/critical tasks requiring immediate routing (use manual assignment)
- Tasks with no contextual information (files, description, keywords) — fallback to Manager Mike

---

## Procedure

### Step 1: Extract Task Context

**Goal:** Infer contextual metadata from task to enable matching with agent specializations.

**Actions:**

1. **Infer language from file extensions:**
   ```python
   # Examples:
   # *.py → python
   # *.java, pom.xml → java
   # *.ts, *.tsx → typescript
   # *.rs → rust
   ```
   - Extract file extensions from `task.files`
   - Map extensions to language identifiers
   - Store as `task_context.language`

2. **Extract frameworks from description and files:**
   ```python
   # Examples from description:
   # "Add Flask endpoint" → flask
   # "Spring Boot service" → spring
   # "FastAPI validation" → fastapi

   # Examples from files:
   # requirements.txt with "flask==2.0.1" → flask
   # pom.xml with "spring-boot" → spring
   # package.json with "react" → react
   ```
   - Scan `task.description` for framework keywords
   - Optionally scan file contents for dependency declarations
   - Store as `task_context.frameworks` (list)

3. **Extract domain keywords from title and description:**
   ```python
   # Examples:
   # "API endpoint validation" → [api, validation]
   # "User guide for onboarding" → [user-guide, onboarding]
   # "Database migration script" → [database, migration]
   ```
   - Extract meaningful nouns and verbs
   - Filter out common words (the, is, and, etc.)
   - Store as `task_context.domain_keywords` (list)

4. **Determine complexity:**
   - Read explicit `task.metadata.complexity` if present
   - Otherwise infer from:
     - Description length (>500 words = high)
     - File count (>10 files = high, 3-10 = medium, <3 = low)
     - Keyword indicators ("refactor", "architecture" = high; "fix typo" = low)
   - Store as `task_context.complexity` (low, medium, high)

5. **Record priority:**
   - Copy `task.priority` to `task_context.priority`

**Checklist:**
- [ ] Language inferred from file extensions
- [ ] Frameworks extracted from description/files
- [ ] Domain keywords extracted from title/description
- [ ] Complexity determined (explicit or inferred)
- [ ] Priority recorded
- [ ] TaskContext object created

**Output:** `TaskContext` object with language, frameworks, domain_keywords, complexity, priority

---

### Step 2: Discover Candidate Agents

**Goal:** Find all agents whose specialization context matches the task context.

**Actions:**

1. **Load framework agents:**
   ```bash
   # Load all agents from doctrine/agents/
   ls doctrine/agents/*.agent.md
   ```
   - Parse YAML frontmatter from each agent profile
   - Extract `specialization_context` fields
   - Store as `framework_agents` list

2. **Load local agents:**
   ```bash
   # Load local overrides from .doctrine-config/custom-agents/
   ls .doctrine-config/custom-agents/*.agent.md
   ```
   - Parse YAML frontmatter from each local agent profile
   - Extract `specialization_context` fields
   - Apply +20 routing priority boost to local agents
   - Store as `local_agents` list

3. **Combine agent pools:**
   ```python
   all_agents = framework_agents + local_agents
   ```

4. **Filter by context match:**
   ```python
   def agent_matches_context(agent, task_context):
       # No context = generalist (always matches)
       if not agent.specialization_context:
           return True

       # Language match
       if task_context.language in agent.specialization_context.language:
           return True

       # Framework match
       if any(fw in agent.specialization_context.frameworks
              for fw in task_context.frameworks):
           return True

       # File pattern match
       if any(fnmatch(file, pattern)
              for file in task_context.files
              for pattern in agent.specialization_context.file_patterns):
           return True

       # Domain keyword match
       if any(kw in agent.specialization_context.domain_keywords
              for kw in task_context.domain_keywords):
           return True

       return False
   ```
   - Filter `all_agents` to only matching agents
   - Store as `candidates` list

5. **Include parent agents as fallbacks:**
   ```python
   for candidate in candidates:
       if candidate.specializes_from:
           parent = find_agent(candidate.specializes_from, all_agents)
           if parent and parent not in candidates:
               candidates.append(parent)
   ```

**Checklist:**
- [ ] Framework agents loaded from `doctrine/agents/`
- [ ] Local agents loaded from `.doctrine-config/custom-agents/`
- [ ] Local agents receive +20 routing priority boost
- [ ] Agents filtered by context match
- [ ] Parent agents included as fallbacks
- [ ] Candidate list created

**Output:** `candidates` list with all matching agents

---

### Step 3: Calculate Match Scores

**Goal:** Quantify how well each candidate agent matches the task context.

**Scoring Algorithm:**

```python
def calculate_match_score(agent, task_context):
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

    # Generalist fallback score (if no specific matches)
    if score == 0.0 and not agent.specializes_from:
        score = 0.50  # Generalist agents get baseline score

    return score
```

**Checklist:**
- [ ] Language match calculated (40% weight)
- [ ] Framework match calculated (20% weight)
- [ ] File pattern match calculated (20% weight)
- [ ] Domain keyword match calculated (10% weight)
- [ ] Exact match bonus applied (10% weight)
- [ ] Generalist fallback score applied if needed
- [ ] Each candidate has `match_score` between 0.0 and 1.0

**Output:** `candidates` list with `match_score` for each agent

---

### Step 4: Adjust for Workload

**Goal:** Prevent specialist overload by penalizing agents with high active task counts.

**Workload Penalty Table:**

| Active Tasks | Penalty |
|--------------|---------|
| 0-2 tasks    | 0% (no penalty) |
| 3-4 tasks    | 15% penalty |
| 5+ tasks     | 30% penalty |

**Algorithm:**

```python
def adjust_for_workload(candidates):
    for candidate in candidates:
        # Count active tasks (assigned + in_progress)
        active_tasks = count_active_tasks(candidate.name)

        # Calculate penalty
        if active_tasks <= 2:
            penalty = 0.0
        elif active_tasks <= 4:
            penalty = 0.15
        else:
            penalty = 0.30

        # Apply penalty
        candidate.workload_adjusted_score = candidate.match_score * (1 - penalty)

    return candidates
```

**Actions:**

1. **Count active tasks per agent:**
   ```bash
   # Count tasks in assigned/ and in_progress/ for each agent
   ls work/collaboration/assigned/<agent-name>/*.yaml | wc -l
   # Sum assigned + in_progress
   ```

2. **Apply workload penalty:**
   - Multiply `match_score` by `(1 - penalty)`
   - Store as `workload_adjusted_score`

**Checklist:**
- [ ] Active tasks counted for each candidate
- [ ] Penalty calculated based on workload table
- [ ] Workload penalty applied to match scores
- [ ] Each candidate has `workload_adjusted_score`

**Output:** `candidates` list with `workload_adjusted_score` for each agent

---

### Step 5: Adjust for Complexity

**Goal:** Match task complexity to agent capability breadth. High complexity tasks favor broader context (parents), low complexity tasks favor specialists.

**Complexity Adjustment Table:**

| Task Complexity | Agent Type | Adjustment |
|-----------------|------------|------------|
| Low             | Specialist | +10% boost |
| Low             | Parent     | No adjustment |
| Medium          | Any        | No adjustment |
| High            | Specialist | -10% penalty |
| High            | Parent     | +10% boost |

**Algorithm:**

```python
def adjust_for_complexity(candidates, task_complexity):
    for candidate in candidates:
        boost = 1.0  # Default: no adjustment

        # Low complexity prefers specialists
        if task_complexity == 'low' and candidate.specializes_from:
            boost = 1.10  # Specialist gets 10% boost

        # Medium complexity: neutral
        elif task_complexity == 'medium':
            boost = 1.0  # No adjustment

        # High complexity prefers parents (broader context)
        elif task_complexity == 'high':
            if candidate.specializes_from:
                boost = 0.90  # Specialist gets 10% penalty
            else:
                boost = 1.10  # Parent gets 10% boost

        # Apply boost
        candidate.complexity_adjusted_score = candidate.workload_adjusted_score * boost

    return candidates
```

**Checklist:**
- [ ] Task complexity determined (low, medium, high)
- [ ] Complexity adjustment calculated per agent
- [ ] Specialists receive boost for low complexity
- [ ] Parents receive boost for high complexity
- [ ] Each candidate has `complexity_adjusted_score`

**Output:** `candidates` list with `complexity_adjusted_score` for each agent

---

### Step 6: Resolve Ties

**Goal:** Select a single agent from candidates using a clear tiebreaker hierarchy.

**Tiebreaker Hierarchy:**

1. **Highest final score** (complexity_adjusted_score)
2. **Language match preference** (for programming tasks)
3. **Highest routing priority**
4. **Manager Mike free choice** (with logged rationale)

**Algorithm:**

```python
def resolve_ties(candidates, task_context):
    # Sort by final score (descending)
    candidates.sort(key=lambda c: c.complexity_adjusted_score, reverse=True)

    # Check for ties at top score
    top_score = candidates[0].complexity_adjusted_score
    top_candidates = [c for c in candidates if c.complexity_adjusted_score == top_score]

    # Single winner
    if len(top_candidates) == 1:
        return top_candidates[0], "highest_adjusted_score"

    # Tiebreaker 1: Language match for programming tasks
    if task_context.language:
        language_matches = [c for c in top_candidates
                           if task_context.language in c.specialization_context.get('language', [])]
        if language_matches:
            return language_matches[0], "language_match_preference"

    # Tiebreaker 2: Highest routing priority
    top_candidates.sort(key=lambda c: c.routing_priority, reverse=True)
    if top_candidates[0].routing_priority > top_candidates[1].routing_priority:
        return top_candidates[0], "highest_routing_priority"

    # Tiebreaker 3: Manager Mike free choice
    selected = top_candidates[0]
    return selected, "manager_free_choice"
```

**Checklist:**
- [ ] Candidates sorted by `complexity_adjusted_score` (descending)
- [ ] Tiebreakers applied in order: score → language → priority → free choice
- [ ] Single agent selected
- [ ] Selection rationale recorded

**Output:** Single selected agent with rationale

---

### Step 7: Return Selection

**Goal:** Package selection result with metadata for auditability and handoff.

**Selection Result Structure:**

```yaml
selection_result:
  selected_agent: "python-pedro"
  match_score: 0.85
  workload_adjusted_score: 0.85
  complexity_adjusted_score: 0.935
  rationale: "Python language match (0.40), FastAPI framework match (0.20), file pattern match (0.20). Workload acceptable (2/5 tasks). Low complexity task (+10% specialist boost)."
  fallback_agent: "backend-benny"
  decision_factors:
    - "Language: python"
    - "Framework: fastapi"
    - "File pattern: *.py"
    - "Workload: 2/5 tasks (no penalty)"
    - "Complexity: low (specialist +10%)"
  tiebreaker: null  # or "language_match_preference", "highest_routing_priority", "manager_free_choice"
  selected_at: "2026-02-12T14:30:00Z"
```

**Checklist:**
- [ ] `selected_agent` field populated
- [ ] Match scores recorded (raw, workload-adjusted, complexity-adjusted)
- [ ] Human-readable rationale written
- [ ] Fallback agent identified (parent or generalist)
- [ ] Decision factors listed
- [ ] Tiebreaker recorded (if applicable)
- [ ] Timestamp added

**Output:** `SelectionResult` object for logging and audit trail

---

## Edge Cases

### No Specialist Match

**Scenario:** Task context doesn't match any specialist agents.

**Resolution:**
- Route to generalist parent (Backend Benny, Frontend Freddy, etc.)
- Record in rationale: "No specialist match, routing to generalist parent"
- Example: Generic infrastructure task → Manager Mike or DevOps agent

### Local Override Specialist

**Scenario:** `.doctrine-config/custom-agents/` contains specialist with higher priority.

**Resolution:**
- Local agents automatically receive +20 routing priority boost
- Local specialist preferred over framework specialist at equal match scores
- Record in rationale: "Local specialist override"

**Example:**
```yaml
# Framework: python-pedro (priority 80)
# Local: custom-python-pedro (priority 80 + 20 = 100)
# Result: custom-python-pedro selected
```

### Circular Delegation

**Scenario:** Agent A delegates to Agent B, which delegates back to Agent A.

**Prevention:**
- Track delegation chain in task metadata
- Reject delegation if target agent already in chain
- Fallback to parent agent or Manager Mike
- Log warning: "Circular delegation detected, routing to parent"

### Multiple Equally-Qualified Specialists

**Scenario:** Python Pedro and Java Jenny both match (e.g., polyglot project).

**Resolution:**
- Apply tiebreaker hierarchy (Step 6)
- For programming tasks, language match is primary tiebreaker
- If still tied, use routing priority
- Final tie: Manager Mike free choice with logged rationale

**Example:**
```yaml
# Task: Refactor Python and Java integration
# Context: language: null (both present), frameworks: [flask, spring]
# Candidates: python-pedro (flask match), java-jenny (spring match)
# Resolution: Check file counts — more .py files → python-pedro
```

---

## Validation

### Post-Selection Checks

**Run after agent selection to ensure result is valid:**

1. **Agent exists and is active:**
   ```bash
   # Verify agent profile exists
   test -f doctrine/agents/<selected-agent>.agent.md || \
   test -f .doctrine-config/custom-agents/<selected-agent>.agent.md
   ```

2. **Agent not over capacity:**
   ```python
   active_tasks = count_active_tasks(selected_agent)
   max_tasks = selected_agent.max_concurrent_tasks
   assert active_tasks < max_tasks, "Agent at or over capacity"
   ```

3. **Selection rationale is human-readable:**
   - Rationale length > 20 characters
   - Contains concrete decision factors (language, framework, workload)
   - No generic placeholders ("selected for reasons")

4. **Fallback agent identified:**
   - If selected agent is specialist, fallback is parent
   - If selected agent is parent, fallback is Manager Mike
   - Fallback agent exists and is active

**Checklist:**
- [ ] Selected agent profile exists
- [ ] Selected agent not over capacity
- [ ] Rationale is human-readable and specific
- [ ] Fallback agent identified and valid

---

## Logging Requirements

**Log all selection decisions for audit trail and debugging.**

**Log Entry Structure:**

```yaml
---
timestamp: "2026-02-12T14:30:00Z"
task_id: "2026-02-12T1400-implement-endpoint"
task_context:
  language: "python"
  frameworks: ["fastapi"]
  domain_keywords: ["api", "endpoint", "validation"]
  complexity: "low"
  priority: "normal"
  files: ["src/api/users.py", "tests/test_users.py"]

candidates:
  - name: "python-pedro"
    match_score: 0.85
    workload_adjusted_score: 0.85
    complexity_adjusted_score: 0.935
    active_tasks: 2
  - name: "backend-benny"
    match_score: 0.50
    workload_adjusted_score: 0.50
    complexity_adjusted_score: 0.50
    active_tasks: 3

selection:
  selected_agent: "python-pedro"
  final_score: 0.935
  rationale: "Python language match (0.40), FastAPI framework match (0.20), file pattern match (0.20). Workload acceptable (2/5 tasks). Low complexity task (+10% specialist boost)."
  fallback_agent: "backend-benny"
  tiebreaker: null

decision_factors:
  - "Language: python (40% weight)"
  - "Framework: fastapi (20% weight)"
  - "File pattern: *.py (20% weight)"
  - "Workload: 2/5 tasks (no penalty)"
  - "Complexity: low (specialist +10%)"
---
```

**Log Location:**
- `work/reports/agent-selection/YYYY-MM-DD.log`
- Append to daily log file
- Rotate logs monthly

**Checklist:**
- [ ] Log entry created for every selection
- [ ] Timestamp in ISO8601 format with Z suffix
- [ ] Task context logged
- [ ] All candidates logged with scores
- [ ] Selection result logged with rationale
- [ ] Decision factors listed

---

## Exit Criteria

**Selection is complete when:**

- [ ] Single agent selected from candidates
- [ ] Match score, workload score, complexity score calculated
- [ ] Human-readable rationale generated
- [ ] Fallback agent identified
- [ ] Selection result validated (agent exists, not over capacity)
- [ ] Selection decision logged
- [ ] Task assigned to selected agent (file moved to `work/collaboration/assigned/<agent>/`)

**Success Metrics:**
- 90%+ of programming tasks route to language-specific specialists
- Specialist workload balanced (no agent consistently >80% capacity)
- <5% reassignments after initial routing
- Zero circular delegation incidents

---

## Failure Modes

### Algorithm Complexity Bugs

**Symptom:** Incorrect scores calculated, wrong agent selected.

**Remediation:**
- Add unit tests for score calculation (see Phase 5 in architecture design)
- Log intermediate scores at each step for debugging
- Review match score weights (language 40%, framework 20%, etc.)
- Validate with known test cases (Python task → Python Pedro)

### Performance Degradation

**Symptom:** Agent selection takes >5 seconds, blocks task routing.

**Remediation:**
- Cache agent profiles (reload only on profile changes)
- Optimize workload counting (batch queries)
- Pre-filter candidates before scoring (eliminate obvious mismatches)
- Profile algorithm with benchmarking tools

### Specialist Overload

**Symptom:** Specialist consistently maxed out, tasks queue up.

**Remediation:**
- Increase `max_concurrent_tasks` for overloaded specialist
- Add additional specialists (Python Pedro 2, Python Pedro 3)
- Route overflow tasks to parent agent
- Run reassignment pass to redistribute workload

### Local Override Conflicts

**Symptom:** Local specialist shadows framework specialist, causes unexpected routing.

**Remediation:**
- Review `.doctrine-config/custom-agents/` for conflicts
- Verify local specialist has narrower context than framework specialist
- Document local override rationale in agent profile
- Consider renaming local agent to avoid name collisions

### Circular Delegation Loops

**Symptom:** Task bounces between agents, never completes.

**Remediation:**
- Track delegation chain in task metadata: `delegation_chain: [agent1, agent2, ...]`
- Reject delegation if target agent in chain
- Escalate to Manager Mike after 3 delegation hops
- Log warning in task result: "Circular delegation detected"

### Missing Parent Agent

**Symptom:** Specialist references non-existent parent in `specializes_from`.

**Remediation:**
- Run agent hierarchy validation script: `python tools/scripts/validate-agent-hierarchy.py`
- Fix `specializes_from` reference or create missing parent profile
- Validation should run in CI/CD to prevent invalid profiles

---

## Related

- **DDR-011:** Agent Specialization Hierarchy (core decision record)
- **DDR-007:** Coordinator Agent Orchestration Pattern (Manager Mike responsibilities)
- **DDR-004:** File-Based Asynchronous Coordination Protocol (task file structure)
- **DDR-005:** Task Lifecycle State Management Protocol (task status transitions)
- **Manager Mike Profile:** `doctrine/agents/manager-mike.agent.md` (invokes this tactic)
- **Python Pedro Profile:** `doctrine/agents/python-pedro.agent.md` (example specialist)
- **Backend Benny Profile:** `doctrine/agents/backend-benny.agent.md` (example parent)
- **Glossary Terms:** Agent Specialization Hierarchy, Parent Agent, Child Agent, Specialization Context, Routing Priority

---

## Metadata

- **Version:** 1.0.0
- **Created:** 2026-02-12
- **Author:** Architect Alphonso
- **Status:** Active
- **Invocation Frequency:** Every task assignment, handoff processing, reassignment pass
- **Estimated Duration:** 2-5 seconds per selection (excluding file I/O)
- **Success Metric:** 90%+ specialist routing accuracy, <5% reassignments
