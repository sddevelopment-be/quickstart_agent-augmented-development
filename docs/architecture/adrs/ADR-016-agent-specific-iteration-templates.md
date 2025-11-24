# ADR-016: Agent-Specific Iteration Templates

**status**: `Rejected`  
**date**: 2025-11-24  
**supersedes**: None  
**related**: ADR-003 (Task Lifecycle), ADR-004 (Work Directory Structure), ADR-005 (Coordinator Agent Pattern), ADR-008 (File-Based Async Coordination)

## Context

The file-based orchestration framework uses generic task templates (`docs/templates/agent-tasks/`) that provide a universal structure for all agent task types. Following successful iteration tracking via GitHub issue templates (see `work/logs/build-automation/2025-11-23T2204-run-iteration-issue-template.md`, line 243), a follow-up question emerged: Should we create specialized iteration templates tailored to specific agent workflows?

### Current Template Approach

**Mechanism:**
- Generic task templates in `docs/templates/agent-tasks/`:
  - `task-base.yaml` - Required fields only
  - `task-context.yaml` - Optional context fields
  - `task-examples.yaml` - Working examples across multiple agent types
- Templates are agent-agnostic and support all 15+ agent types
- Agents adapt generic templates to their specialization during execution
- Context is provided via `context.notes` field for agent-specific guidance

**Observed Performance:**
- 100% task completion rate across 20+ orchestrated tasks
- Templates successfully used by: curator, diagrammer, synthesizer, architect, manager, build-automation
- Zero template-related blocking issues reported
- Framework assessed as production-ready (98.9% alignment per ADR reviews)

### Proposed Specialized Templates

**Examples of Agent-Specific Templates:**
1. **Documentation Sprint Template** (curator, writer-editor)
   - Pre-defined checklist of common documentation tasks
   - Quality gate criteria specific to documentation
   - Standard handoff patterns for polish workflows

2. **Test Automation Cycle Template** (backend-dev, frontend)
   - Test coverage targets
   - Test type categorization (unit, integration, e2e)
   - CI/CD integration checkpoints

3. **Refactoring Cycle Template** (backend-dev, frontend)
   - Code smell checklist
   - Refactoring safety criteria
   - Regression test requirements

4. **Architecture Review Template** (architect)
   - Trade-off analysis structure
   - Stakeholder consideration matrix
   - Decision documentation requirements

5. **Visual Design Sprint Template** (diagrammer)
   - Diagram type selection guide
   - Accessibility validation checklist
   - Format and tooling requirements

### Problem Analysis

**Pattern Extraction from Completed Tasks:**
- Total tasks analyzed: 20+
- Agent types represented: 8+ (curator, architect, diagrammer, manager, synthesizer, build-automation, structural, writer-editor)
- Task type diversity: ADRs, diagrams, documentation, orchestration, assessment, synthesis
- Template-related failures: 0 (0%)

**Key Finding:** Generic templates are **successfully supporting diverse agent workflows** without specialization, suggesting low baseline need for agent-specific variants.

### Feasibility Challenges

**Template Maintenance Overhead:**
- 15+ agent types × 2-3 common workflow patterns = 30-45 specialized templates
- Each template requires:
  - Initial design and validation
  - Documentation and examples
  - Ongoing maintenance as agent capabilities evolve
  - Version synchronization with generic template improvements
- Current maintenance burden: 5 generic templates (manageable)
- Proposed maintenance burden: 40+ templates (significant increase)

**Template Selection Complexity:**
- Agents must decide which template to use for each task
- Decision logic adds cognitive overhead: "Is this a documentation sprint or a single-document task?"
- Template boundaries may blur (e.g., "Create ADR with diagram" spans architect + diagrammer domains)
- Risk of template proliferation: "Sprint templates" → "Mini-sprint templates" → "Ad-hoc task templates"

**Workflow Rigidity:**
- Specialized templates may encode current practices prematurely
- Framework still emerging (only 3 POC iterations completed)
- Risk of locking in sub-optimal workflows before sufficient data collected
- May inhibit discovery of innovative coordination patterns

**Architectural Tension:**
- Generic templates support **emergent workflows**
- Specialized templates impose **prescriptive workflows**
- Core principle (ADR-008): "Complex workflows emerge naturally from simple coordination"
- Shifts paradigm from "emerge naturally" to "follow prescribed patterns"

## Decision

**We REJECT agent-specific iteration templates.**

The framework's generic task templates are successfully supporting diverse agent workflows without specialization. Introducing agent-specific templates would add significant maintenance overhead and workflow rigidity without evidence of solving an actual problem.

## Rationale

### 1. Generic Templates Are Working Exceptionally Well

**Evidence:**
- 100% task completion rate (20+ tasks)
- Zero template-related failures
- Successfully used by 8+ agent types across diverse task domains
- No agent feedback indicating template inadequacy
- Framework assessed as production-ready

**Why Generic Works:**
- `task-base.yaml` provides minimal required structure
- `task-context.yaml` enables agent-specific customization via notes
- `task-examples.yaml` demonstrates adaptation across domains
- Agents have full autonomy to interpret and extend templates

**Current Success Metrics:**
| Metric | Target | Actual | Assessment |
|--------|--------|--------|------------|
| Task completion rate | >90% | 100% | ✅ Exceeding |
| Template-related failures | <5% | 0% | ✅ Exceeding |
| Agent adoption | All agents | 8+ agents | ✅ Universal |
| Maintenance burden | Low | 5 templates | ✅ Manageable |

### 2. High Maintenance Cost vs. Low Value Delivered

**Cost Analysis:**

| Cost Category | Generic Templates | Specialized Templates | Delta |
|--------------|-------------------|----------------------|-------|
| Initial design | 5 templates | 40+ templates | +700% |
| Documentation | 1 README | 1 README + 40 guides | +800% |
| Version sync | 5 files | 45 files | +800% |
| Testing | 5 validation checks | 45 validation checks | +800% |
| Onboarding complexity | Low (5 examples) | High (select from 40) | +700% |

**Value Analysis:**
- Potential benefit: Slightly reduced cognitive load for template selection
- Actual need: **Zero observed failures with generic approach**
- Cost-benefit ratio: **High cost, negligible value**

### 3. Architectural Misalignment

**Conflicts with Core Principles (ADR-008, ADR-005):**

| Principle | Generic Templates | Specialized Templates | Assessment |
|-----------|-------------------|----------------------|------------|
| **Simplicity** | 5 universal templates | 40+ specialized templates | ❗️ Violates simplicity |
| **Autonomy** | Agent adapts template | Template prescribes workflow | ❗️ Reduces autonomy |
| **Emergence** | Patterns discovered | Patterns prescribed | ❗️ Prevents emergence |
| **Flexibility** | Any task fits base structure | Must match predefined types | ⚠️ Reduces flexibility |
| **Maintainability** | Low template count | High template count | ❗️ Increases burden |

From ADR-008:
> "Framework simplicity maintained — No hidden state, complex queues, or opaque protocols introduced"

Specialized templates with rigid workflow structures contradict this design achievement.

### 4. Premature Optimization

**Framework Maturity Assessment:**
- Framework delivery: Completed (Issue #8)
- Production validation: POC1-POC3 completed successfully
- Pattern observation period: ~1 week (insufficient for standardization)
- Agent workflow diversity: Still expanding as new agents onboard

**Risk of Premature Specialization:**
- Curator workflow may evolve as framework scales
- Test automation patterns still being discovered
- Architecture review templates may constrain innovative ADR formats
- Current patterns reflect initial POC experiences, not long-term practice

**Recommended Maturity Threshold:**
- Observe patterns for 3-6 months of production use
- Collect 100+ completed tasks per agent type
- Identify recurring pain points with generic templates
- Measure template-related failure rates
- **Current status:** Too early for specialization

### 5. Template Selection Overhead

**Decision Tree Complexity:**
```
Task arrives → Agent must decide:
  - Is this a sprint or single task?
  - If sprint, which type? (documentation, test, refactor, design)
  - Does it span multiple workflows?
  - Should I use specialized or generic template?
  - If specialized, which variant?
```

**Comparison:**
- **Generic approach:** Use `task-base.yaml`, add context via notes
- **Specialized approach:** Navigate 40+ templates, select best fit, risk wrong choice

**Cognitive Load:**
- Generic: Low (one decision point: base vs. context-enriched)
- Specialized: High (multi-level decision tree with fuzzy boundaries)

### 6. Simpler Alternatives Exist

Enhanced agent profiles and workflow documentation can provide lightweight guidance without template proliferation (see Alternatives section).

## Considered Alternatives

### Alternative 1: Enhanced Agent Profile Guidance (RECOMMENDED)

**Approach:** Add "Common Workflow Patterns" section to each agent profile documenting typical iteration structures.

**Example (curator.agent.md):**
```markdown
## Common Workflow Patterns

### Documentation Sprint (Multiple Files)
1. Load glossary and style guide
2. For each file:
   - Check structural consistency
   - Validate metadata
   - Cross-reference links
3. Generate discrepancy report
4. Handoff: writer-editor (if polish needed)

### Single Document Review
1. Load relevant templates
2. Structural validation
3. Tonal consistency check
4. Generate recommendations
5. Apply approved corrections
```

**Advantages:**
- ✅ Zero template maintenance overhead
- ✅ Preserves full agent autonomy
- ✅ Easy to maintain (update profiles as patterns observed)
- ✅ Discoverable (agents load profiles during initialization)
- ✅ Flexible (guidance, not prescription)
- ✅ Aligns with existing agent profile structure
- ✅ No template selection complexity

**Disadvantages:**
- Not directly actionable without agent interpretation
- Patterns may vary across agents

**Decision:** This alternative achieves 90% of specialized template benefits at <5% of implementation cost.

### Alternative 2: Workflow Pattern Documentation

**Approach:** Create `docs/workflows/agent-patterns.md` documenting common iteration patterns per agent type.

**Example:**
```markdown
## Test Automation Cycle (backend-dev, frontend)

**Typical Structure:**
1. Scope: Identify untested code paths
2. Design: Select test types (unit, integration, e2e)
3. Implement: Write tests following conventions
4. Validate: Verify coverage targets met
5. Integrate: Add to CI/CD pipeline
6. Document: Update test documentation

**Common Handoffs:**
- To devops: CI/CD integration assistance
- To curator: Documentation consistency validation
```

**Advantages:**
- Centralizes workflow knowledge
- Educational for human coordinators and new agents
- Low maintenance burden
- Does not constrain agent autonomy

**Disadvantages:**
- Static documentation may drift from practice
- Not directly actionable by agents

**Decision:** Valuable as supplementary documentation alongside Alternative 1.

### Alternative 3: Task Context Enrichment

**Approach:** Expand `task-context.yaml` template with optional workflow guidance fields.

**Example:**
```yaml
context:
  workflow_type: documentation_sprint | test_cycle | refactor_cycle | architecture_review
  workflow_checklist:
    - "Load relevant templates and guidelines"
    - "Validate against quality criteria"
    - "Generate artifacts"
    - "Consider handoff if polish needed"
```

**Advantages:**
- Single template with optional enrichment
- Agents can ignore workflow fields if not applicable
- Maintains generic template simplicity
- No template proliferation

**Disadvantages:**
- Workflow checklists may become prescriptive
- Requires agents to implement checklist logic
- Still requires maintenance of embedded workflow patterns

**Decision:** Possible future enhancement if Alternative 1 proves insufficient, but currently unnecessary.

### Alternative 4: Agent-Specific Task Examples

**Approach:** Expand `task-examples.yaml` with more examples per agent type.

**Example:**
```yaml
# Example 6: Curator Documentation Sprint
id: "2025-11-24T1000-curator-doc-sprint"
agent: "curator"
status: "new"
title: "Documentation consistency sprint (Q4 2025)"
artefacts:
  - "work/curator/sprint-report.md"
context:
  notes:
    - "Review all files in docs/ for structural consistency"
    - "Check metadata completeness across all markdown files"
    - "Validate cross-references and broken links"
    - "Generate consolidated discrepancy report"
  workflow_guidance:
    - "This is a sprint (multiple files), not single-document review"
    - "Use batch processing approach"
    - "Prioritize high-impact inconsistencies"
```

**Advantages:**
- Extends existing `task-examples.yaml` structure
- Provides concrete patterns without new templates
- Low maintenance (add examples as patterns emerge)
- Preserves generic template simplicity

**Disadvantages:**
- Examples may not cover all scenarios
- Agents must infer patterns from examples

**Decision:** Immediate action - add 5-10 agent-specific examples to `task-examples.yaml`.

### Alternative 5: Do Nothing

**Approach:** Continue with current generic template approach.

**Advantages:**
- Zero cost
- Framework is working exceptionally well
- Allows patterns to mature before standardization

**Disadvantages:**
- Onboarding friction for new agents (mitigated by Alternative 1)

**Decision:** Viable baseline if no alternatives implemented, but Alternative 1 provides low-cost improvement.

## Envisioned Consequences

### Positive Consequences of Rejection

**Preserved Simplicity:**
- Framework remains lightweight with 5 universal templates
- No complex template selection logic needed
- Onboarding complexity stays low
- Clear documentation structure maintained

**Preserved Autonomy:**
- Agents retain full decision-making authority for workflow structure
- Enables discovery of innovative coordination patterns
- Supports context-sensitive adaptations
- No artificial constraints on task types

**Reduced Maintenance Burden:**
- 5 templates to maintain vs. 40+
- Single source of truth for template structure
- Version sync complexity remains low
- Testing and validation remains manageable

**Architectural Integrity:**
- Maintains alignment with core principles (simplicity, emergence, autonomy)
- Prevents architectural drift toward rigid workflow frameworks
- Protects production-ready status achieved in current implementation
- Supports framework evolution without template lock-in

**Flexibility:**
- Agents can invent new workflow patterns without template updates
- Cross-domain tasks (e.g., "ADR with diagrams") fit naturally
- Framework adapts to new agent types without template redesign

### Negative Consequences of Rejection

**Potential Onboarding Friction:**
- New agents lack explicit workflow guidance in templates
- **Mitigation:** Alternative 1 (agent profile patterns) + Alternative 4 (expanded examples)

**Potential Workflow Inconsistency:**
- Same task type may be approached differently by same agent over time
- **Mitigation:** Alternative 2 (workflow documentation) provides guidance without prescription
- **Counter-argument:** Some inconsistency is healthy (enables experimentation and improvement)

**Potential Missed Optimizations:**
- Efficient workflow patterns may not be systematically captured
- **Mitigation:** Work logs (Directive 014) capture patterns; synthesize into profile guidance
- **Monitoring:** Track task duration and success rate; identify optimization opportunities

**Potential Cognitive Load:**
- Agents must decide workflow structure for each task
- **Mitigation:** Alternative 1 provides guidance without removing autonomy
- **Counter-argument:** This decision-making is core to agent intelligence and specialization

### Conditions for Revisiting This Decision

We will reconsider agent-specific iteration templates if:

1. **Template-related failure rate exceeds 5%** (currently 0%)
2. **Agent feedback indicates template inadequacy** (collect via retrospectives)
3. **Framework scales to 25+ agents** and workflow diversity becomes unmanageable
4. **Pattern maturity reached:** 100+ tasks per agent type completed, clear recurring patterns identified
5. **Specific compliance requirements** mandate standardized workflow documentation
6. **Generic template becomes overloaded** with agent-specific annotations (complexity threshold)

**Monitoring Metrics:**
- Task completion rate per agent type
- Template-related issues logged in work logs
- Time-to-completion variance (indicates workflow inefficiency)
- Agent profile "Common Workflow Patterns" section growth (indicates need for formalization)

**Trigger Threshold:**
- 3+ agents report template inadequacy in consecutive sprints
- Template-related failure rate >5% sustained for 1 month
- 5+ workflow patterns documented per agent (suggests need for template consolidation)

## Implementation Guidance

### Immediate Actions (This Sprint)

**1. Enhance Agent Profiles with Workflow Patterns (Alternative 1):**

Add "Common Workflow Patterns" section to each agent profile following this template:

```markdown
## Common Workflow Patterns

### Pattern 1: [Pattern Name]
**When to use:** [Trigger conditions]
**Structure:**
1. Step 1
2. Step 2
3. ...
**Common handoffs:** [Next agents]

### Pattern 2: [Pattern Name]
...
```

**Priority agents for enhancement:**
- `curator.agent.md` (documentation sprints, consistency audits)
- `architect.agent.md` (ADR creation, architecture reviews)
- `backend-dev.agent.md` (test cycles, refactoring sprints)
- `diagrammer.agent.md` (diagram creation workflows)
- `manager.agent.md` (orchestration cycles)

**2. Expand Task Examples (Alternative 4):**

Add 5-10 agent-specific examples to `docs/templates/agent-tasks/task-examples.yaml`:
- Curator: Documentation sprint (multiple files)
- Architect: ADR with diagram handoff
- Backend-dev: Test automation cycle
- Diagrammer: Multi-diagram visualization workflow
- Manager: Orchestration iteration cycle

**3. Create Workflow Pattern Documentation (Alternative 2):**

Create `docs/workflows/agent-patterns.md` documenting common multi-step workflows:
- Structure: Agent type → Common patterns → Typical handoffs
- Audience: Human coordinators, new agents, framework maintainers
- Maintenance: Update quarterly based on work log analysis

### Short-Term Actions (Next 1-2 Sprints)

**Monitor and Iterate:**
1. Collect agent feedback on profile guidance effectiveness
2. Analyze work logs for emerging patterns not yet documented
3. Update agent profiles as patterns observed
4. Add examples to `task-examples.yaml` as patterns solidify

**Metrics to Track:**
- Task completion rate by agent type (baseline: 100%)
- Template-related issues logged (baseline: 0)
- Time-to-completion variance (establish baseline)
- Agent profile section usage (via work log mentions)

### Long-Term Strategy (3-6 Months)

**Pattern Maturity Assessment:**
1. Analyze 100+ tasks per agent type
2. Identify highly recurring patterns (>10 occurrences)
3. Assess whether generic template + profile guidance remains sufficient
4. Re-evaluate this ADR if conditions for revisiting are met

**Framework Evolution:**
- Continue observing emergent patterns without premature standardization
- Let workflows mature organically through practice
- Document successful patterns in agent profiles and workflow guides
- Defer template specialization until clear, validated need emerges

## Open Questions

None. Decision is clear based on current evidence and architectural principles.

If future evidence challenges this decision, the conditions for revisiting provide clear trigger points.

## References

- **ADR-003:** Task Lifecycle and State Management
- **ADR-004:** Work Directory Structure
- **ADR-005:** Coordinator Agent Pattern
- **ADR-008:** File-Based Async Coordination (Core Principles)
- **ADR-015:** Follow-Up Task Lookup Pattern (similar rejection rationale)
- **Directive 014:** Work Log Creation (pattern capture mechanism)
- **Source Reference:** `work/logs/build-automation/2025-11-23T2204-run-iteration-issue-template.md` (line 243)
- **Task Templates:** `docs/templates/agent-tasks/task-templates-README.md`

---

_Author: Architect Alphonso_  
_Review Status: Completed_  
_Next Review: 2026-Q1 (or triggered by conditions listed above)_
