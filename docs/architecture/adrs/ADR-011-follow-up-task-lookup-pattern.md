# ADR-011: Follow-Up Task Lookup Pattern

**status**: `Rejected`  
**date**: 2025-11-24  
**supersedes**: None  
**related**: ADR-002 (File-Based Async Coordination), ADR-008 (File-Based Async Coordination), ADR-009 (Orchestration Metrics)

## Context

The file-based orchestration framework (delivered in Issue #8) uses manual handoffs where agents independently decide downstream steps via `result.next_agent` fields in task YAML files. After successful POC validations (POC1-Curator, POC2-Diagrammer, POC3 multi-agent chain), we conducted an exploratory assessment to determine whether a centralized "Follow-Up Task Lookup Table" would improve workflow consistency and reduce cognitive overhead.

### Current Handoff Approach

**Mechanism:**
- Agents complete tasks and optionally specify `result.next_agent` 
- Orchestrator creates follow-up task based on `next_task_title`, `next_artefacts`, `next_task_notes`
- Each agent determines appropriate handoffs based on task context and specialization knowledge
- Handoff patterns emerge organically through practice

**Observed Performance:**
- 100% task completion rate across 20+ orchestrated tasks
- Zero manual corrections required
- Successful 5-agent chain (POC3) without coordination failures
- Framework assessed as production-ready (98.9% alignment per ADR review)

### Proposed Lookup Table Pattern

A centralized YAML file mapping `(agent_name, task_type, context_conditions) → suggested_follow_ups` that would:
- Provide standardized handoff recommendations
- Reduce agent decision-making cognitive load
- Establish explicit workflow conventions
- Guide new agents on typical patterns

**Example Schema:**
```yaml
follow_up_patterns:
  - agent: curator
    task_type: documentation_creation
    conditions:
      audience: end_users
    suggested_handoffs:
      - agent: writer-editor
        priority: high
        task_template: "Review and polish {artifact_path}"
```

### Problem Analysis

**Pattern Extraction from Completed Tasks:**
- Total tasks analyzed: 20+
- Tasks with handoffs: 4 (20%)
- Tasks terminating naturally: 16 (80%)
- Observed handoff patterns:
  - Documentation → writer-editor (polish) - 2 occurrences
  - Architecture → diagrammer (visualization) - 1 occurrence
  - Diagrams → synthesizer (integration) - 1 occurrence

**Key Finding:** Handoffs are **context-dependent and relatively rare** (~20% of tasks), suggesting low baseline need for standardized lookup.

### Feasibility Challenges

**Task Type Categorization:**
- Task types overlap significantly (ADR creation spans architecture, documentation, design domains)
- Self-classification requires cognitive overhead potentially exceeding manual handoff decision
- Context matters more than category: "Create ADR" may handoff to diagrammer, writer-editor, or neither

**Condition Evaluation Complexity:**
- Conditions like "complexity: high" or "length: >300 lines" require programmatic evaluation
- Agents would need to implement condition-checking logic
- Template interpolation adds implementation burden
- Maintenance cost increases as patterns evolve

**Architectural Tension:**
- Lookup table introduces **prescriptive coordination** 
- Framework designed for **emergent coordination**
- Core principle (ADR-002): "Complex workflows emerge naturally from simple handoffs"
- Shifts paradigm from "emerge naturally" to "follow prescribed patterns"

## Decision

**We REJECT the Follow-Up Task Lookup Table Pattern.**

The pattern introduces unwarranted complexity that contradicts core orchestration principles without evidence of solving an actual problem. Current handoff approach is working exceptionally well (100% success rate, production-ready status).

## Rationale

### 1. Low Observed Need
- Only 4 handoffs in 20 tasks (20% handoff rate)
- Zero handoff errors or missed valuable follow-ups
- Current approach achieving 100% task completion rate
- No evidence of cognitive load issues for agents

### 2. Architectural Misalignment

**Conflicts with Core Principles (ADR-002, ADR-008):**

| Principle | Current Approach | Lookup Table | Assessment |
|-----------|-----------------|--------------|------------|
| **Simplicity** | Single `next_agent` field | Schema, conditions, templates, evaluation logic | ❗️ Violates simplicity |
| **Autonomy** | Agent decides handoffs | Centralized prescriptive logic | ❗️ Reduces autonomy |
| **Emergence** | Patterns discovered via practice | Patterns prescribed pre-emptively | ❗️ Prevents emergence |
| **Transparency** | Handoff visible in task YAML | Adds indirection layer | ⚠️ Reduces directness |

From ADR-008 implementation-progress-review:
> "Framework simplicity maintained — No hidden state, complex queues, or opaque protocols introduced"

Lookup table with condition evaluation and template interpolation would introduce "complex protocols" contrary to this design achievement.

### 3. High Implementation Cost
- New YAML schema design and validation
- Condition evaluation logic in agents or orchestrator
- Template interpolation mechanism
- Pattern maintenance as framework evolves
- Override mechanism for exceptions
- Testing and documentation overhead

**Cost-Benefit Analysis:** Implementation cost exceeds value delivered given low handoff frequency and current high success rate.

### 4. Premature Optimization
- Framework is production-ready without this pattern
- Patterns still emerging organically (only 3 POC iterations completed)
- Risk of locking in sub-optimal workflows before sufficient data collected
- POC3 demonstrated successful 5-agent chain emerged without prescriptive guidance

### 5. Simpler Alternatives Exist
Enhanced agent profiles can provide lightweight guidance without implementation complexity (see Alternatives section).

## Considered Alternatives

### Alternative 1: Enhanced Agent Profiles (RECOMMENDED)

**Approach:** Add "Common Handoff Patterns" section to each agent profile documenting observed patterns as guidance.

**Example:**
```markdown
## Common Handoff Patterns

### Outgoing Handoffs
- Documentation creation → writer-editor (for polish and clarity)
- Complex architectural concepts → diagrammer (for visualization)
- Multiple related artifacts → synthesizer (for integration)

### Incoming Handoffs
- From curator: Documentation requiring structural review
- From writer-editor: Polished content for final validation
```

**Advantages:**
- ✅ Zero implementation complexity
- ✅ Preserves full agent autonomy
- ✅ Easy to maintain (update profiles as patterns observed)
- ✅ Discoverable (agents load their profiles during initialization)
- ✅ Flexible (guidance, not prescription)
- ✅ Aligns with existing profile structure

**Disadvantages:**
- Decentralized (each profile documents its own patterns)
- Not programmatically enforceable

**Decision:** This alternative achieves 80% of lookup table benefits at <5% of implementation cost.

### Alternative 2: Workflow Pattern Documentation

**Approach:** Create `docs/workflows/common-patterns.md` documenting observed multi-agent workflows.

**Example:**
```markdown
## Documentation Polish Workflow
1. Creator (any agent) produces documentation
2. Handoff: writer-editor for clarity and accessibility improvements  
3. Handoff: curator for final structural validation

## Architecture Visualization Workflow
1. Architect produces ADR or technical design
2. Handoff: diagrammer for visual representation
3. Handoff: curator for alt-text validation
```

**Advantages:**
- Centralizes workflow knowledge
- Educational for human coordinators and new agents
- Low maintenance burden

**Disadvantages:**
- Static documentation may drift from practice
- Not directly actionable by agents without implementation

**Decision:** Valuable as supplementary documentation, but insufficient as primary solution.

### Alternative 3: Orchestrator Suggestion System

**Approach:** Orchestrator analyzes completed task attributes and suggests potential follow-ups to human coordinator.

**Advantages:**
- Preserves human oversight
- Reduces cognitive load on humans, not agents
- Simple heuristics (e.g., "undocumented API → suggest writer-editor")

**Disadvantages:**
- Requires orchestrator enhancement
- Assumes human in the loop
- Still needs pattern definition

**Decision:** Deferred - may be valuable if framework scales to human coordination bottleneck.

### Alternative 4: Do Nothing

**Approach:** Continue with current organic handoff approach.

**Advantages:**
- Zero cost
- Framework is working exceptionally well
- Allows patterns to mature before standardization

**Disadvantages:**
- Onboarding friction for new agents (mitigated by Alternative 1)

**Decision:** Current baseline is strong; no urgent need for change.

## Envisioned Consequences

### Positive Consequences of Rejection

**Preserved Simplicity:**
- Framework remains lightweight and easy to understand
- No additional schemas, condition logic, or evaluation mechanisms
- Onboarding complexity stays low

**Preserved Autonomy:**
- Agents retain full decision-making authority for handoffs
- Enables discovery of innovative coordination patterns
- Supports context-sensitive decision-making

**Reduced Maintenance Burden:**
- No lookup table to update as framework evolves
- Patterns documented organically in agent profiles as observed
- Avoids brittleness from prescriptive rules

**Architectural Integrity:**
- Maintains alignment with core principles (simplicity, emergence, autonomy)
- Prevents architectural drift toward complex orchestration frameworks
- Protects production-ready status achieved in current implementation

### Negative Consequences of Rejection

**Potential Inconsistency:**
- Handoff patterns may vary across similar task types
- **Mitigation:** Alternative 1 (agent profile patterns) provides guidance without prescription

**Onboarding Friction:**
- New agents lack explicit handoff guidance
- **Mitigation:** Alternative 1 (agent profiles) and Alternative 2 (workflow docs) address this

**Missed Optimizations:**
- Future workflow improvements may not be systematically captured
- **Mitigation:** Organic documentation in profiles as patterns observed; revisit decision if error rate increases

### Conditions for Revisiting This Decision

We will reconsider the lookup table pattern if:

1. **Handoff error rate exceeds 10%** (currently 0%)
2. **Measurable missed follow-up problem emerges** (currently no evidence)
3. **Framework scales beyond 10 agents** and coordination complexity increases
4. **Specific compliance/quality requirements** mandate workflow enforcement
5. **Pattern standardization becomes necessary** for tool integration or automation

## Implementation Guidance

### Immediate Actions (Next Sprint)

**Enhance Agent Profiles with Handoff Patterns:**

1. Add "Common Handoff Patterns" section to each agent profile
2. Document observed outgoing and incoming handoffs
3. Update as patterns emerge from future POCs

**Profile Template:**
```markdown
## Common Handoff Patterns

### Outgoing Handoffs
*List typical next agents for this agent's outputs*

### Incoming Handoffs  
*List typical upstream agents that handoff to this agent*

### Special Cases
*Document context-dependent variations*
```

**Priority Agents for Enhancement:**
- architect.agent.md (diverse outputs: ADRs, assessments, reviews)
- curator.agent.md (quality gate, often final step)
- writer-editor.agent.md (polish specialist, mid-chain position)

### Supplementary Documentation

**Create Workflow Pattern Guide:**
- Location: `docs/workflows/common-patterns.md`
- Content: Multi-agent workflow sequences observed in POCs
- Audience: Human coordinators, new agents, framework maintainers

### Monitoring and Metrics

**Track Handoff Effectiveness:**
- Monitor handoff error rate (target: <5%)
- Identify missed valuable follow-ups via retrospectives
- Document new patterns in agent profiles as observed
- Quarterly review of pattern documentation currency

**Trigger Points for Reassessment:**
- Handoff error rate >10% sustained for 1 month
- 3+ identified missed follow-ups in single sprint
- Agent onboarding feedback indicates pattern guidance deficit

## Open Questions

None. Decision is clear based on current evidence and architectural principles.

## References

- **ADR-002:** Portability Enhancement (OpenCode)
- **ADR-008:** File-Based Async Coordination (Core Principles)
- **ADR-009:** Orchestration Metrics Standard
- **File-Based Orchestration Approach:** `.github/agents/approaches/file-based-orchestration.md`
- **Implementation Review:** `docs/architecture/assessments/implementation-progress-review.md`
- **Work Log:** `work/logs/architect/2025-11-24T1210-follow-up-lookup-assessment.md`

---

_Author: Architect Alphonso_  
_Review Status: Completed_  
_Next Review: 2026-Q1 (or triggered by conditions listed above)_
