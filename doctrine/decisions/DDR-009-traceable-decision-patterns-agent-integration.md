# DDR-009: Traceable Decision Patterns and Agent Integration

**Status:** Active  
**Date:** 2026-02-11  
**Supersedes:** Repository-specific decision capture implementations (elevated from ADR-017)

---

## Context

Agent-augmented development workflows make architectural and operational decisions continuously. Without systematic decision capture, universal problems emerge:

### Knowledge Fragmentation

- Formal decisions documented separately from exploratory ideation
- Code changes lack links to architectural rationale
- Agent work logs capture execution but not decision-making context
- Ideation documents exist in isolation without implementation paths

### Discovery Friction

- Contributors spend significant time asking "why" questions during onboarding
- Teams revisit already-evaluated options due to lost rationale
- AI agents propose changes conflicting with established principles
- Cross-project pattern reuse is minimal due to poor knowledge capture

### Agent Coordination Gaps

- Agents lack access to decision context when generating artifacts
- No standardized way to reference governing decisions in outputs
- Decision rationale scattered across commits, issues, documentation
- No visibility into undocumented decisions ("decision debt")

The framework needs universal decision traceability patterns that:
- Preserve decision rationale for future contributors
- Enable AI agents to reference appropriate context
- Minimize disruption to individual contributor productivity
- Integrate seamlessly with existing documentation frameworks
- Provide measurable traceability and decision debt visibility

## Decision

**We establish traceable decision patterns as the framework's standard for decision capture, linking, and agent integration, with flow-aware capture strategies respecting individual productivity.**

### 1. Decision Marker Format

All architectural decisions embedded in code, documentation, or task artifacts use standardized markers:

**Inline Marker (code/documentation comments):**

```markdown
<!-- DECISION-MARKER: <decision-id> -->
**Decision:** [Brief statement of what was decided]
**Rationale:** [Why this approach was chosen]
**Alternatives:** [Options considered and rejected with reasons]
**Consequences:** [Accepted trade-offs]
**Status:** [Implemented | Proposed | Deprecated]
**Date:** [YYYY-MM-DD]
<!-- END-DECISION-MARKER -->
```

**Commit Message Annotation:**

```
<type>: <subject>

Decision: [Brief decision statement]
Reference: [DDR-XXX or ADR-XXX if formalized]
Rationale: [One-line justification]
Context: [Link to ideation/synthesis if applicable]
```

**Task YAML Schema Extension:**

```yaml
task:
  decision_context:
    reference: "DDR-XXX or ADR-XXX"
    justification: "Why this decision applies to this task"
    alternatives_considered: ["option1", "option2"]
    chosen_because: "Specific reasoning for selection"
```

### 2. Linking Conventions

All artifacts establish bidirectional traceability:

**Forward Links (Decision → Artifacts):**
- Formal decision records (DDRs/ADRs) list affected files, modules, components
- Synthesis documents reference implementing artifacts
- Ideation documents link to resulting decisions and implementations

**Backward Links (Artifacts → Decision):**
- New code files include decision references in header/frontmatter
- Documentation pages cite governing decisions in introduction
- Agent work logs reference relevant decisions in context section
- Task files include `decision_context` block

**Cross-References (Decision → Decision):**
- Decision records reference related/superseded decisions explicitly
- Synthesis documents link to source ideation and target decisions
- Framework directives cite decisions that mandate behavior

### 3. Agent Directive Requirements

Agents must be instructed to:

1. **Pre-check:** Load relevant decision records before proposing changes
2. **Context awareness:** Reference appropriate decisions when generating artifacts
3. **Marker generation:** Add decision markers during collaboration when architectural choices made
4. **Link validation:** Verify generated artifacts reference governing decisions
5. **Pattern extraction:** Identify recurring patterns for synthesis suggestions

### 4. Flow-Aware Capture Strategy

Decision documentation respects individual productivity through flow-aware timing:

| Flow State | Decision Action | Documentation Timing | Agent Behavior |
|-----------|----------------|---------------------|----------------|
| **Deep Creation** | Add lightweight markers in code | Defer to session-end | Passive, no interruptions |
| **Agent Collaboration** | Real-time decision markers with agent assistance | Immediate during iteration | Active co-creation with templates |
| **Reflection/Synthesis** | Draft formal decision records from accumulated markers | Dedicated synthesis time | Summarize patterns, suggest formalization |

### 5. Decision Debt Tracking

Work logs and metrics track decision traceability:

```yaml
metrics:
  decision_traceability:
    markers_added: 3           # New decision markers created
    markers_formalized: 1      # Markers promoted to formal decisions
    decisions_referenced: 2    # Existing decisions linked
    debt_ratio: 0.15          # (Markers - formalized) / Markers
```

**Thresholds:**
- Debt ratio <20%: Healthy (some markers are implementation details)
- Debt ratio 20-40%: Review needed (backlog requires synthesis)
- Debt ratio >40%: Red flag (dedicated formalization time required)

### 6. Validation Requirements

Automated validation checks:

- Decision record cross-references are valid (no broken links)
- New artifacts in documentation reference at least one decision or have exemption
- Work logs include decision context section
- Task files with architectural impact include `decision_context` block
- Decision markers follow standardized format

## Rationale

### Why Mandatory Decision Traceability?

**Problem severity:**
- Onboarding time significantly increased by "why" questions
- Architecture discussions frequently revisit settled decisions
- Agent suggestion acceptance improved by contextual awareness

**Alternative approaches insufficient:**
- Voluntary capture: compliance drops rapidly without enforcement
- Post-hoc documentation: rationale forgotten, quality poor
- Separate decision logs: disconnected from artifacts, rarely updated

### Why Standardized Markers?

**Enables automation:**
- Validation scripts parse and verify markers
- Decision debt becomes measurable
- Agents reliably detect and reference decisions
- Search tools find decisions by criteria

**Improves discoverability:**
- Uniform format aids visual scanning
- Required fields ensure completeness
- Clear delimiters enable automated extraction

### Why Flow-Aware Capture?

**Respects productivity:**
- Interrupting deep work reduces effectiveness significantly
- Context switching overhead is substantial
- Batch documentation in reflection improves quality

**Accommodates preferences:**
- Some contributors prefer real-time capture
- Others need uninterrupted creation time
- Framework accommodates both via flow state awareness

### Why Decision Debt Metric?

**Visibility enables management:**
- Quantifiable threshold enables prioritization
- Trend analysis identifies patterns
- Balances rigor with pragmatism

**Not every marker needs formalization:**
- Implementation details acceptable as markers only
- Threshold allows flexibility while preventing neglect
- Periodic review prevents debt explosion

### Framework-Level Pattern

This pattern applies universally because:
- All agent systems make architectural decisions
- All frameworks benefit from decision traceability
- All adopters need onboarding efficiency
- All systems require agent context awareness

## Consequences

### Positive

- ✅ **Reduced onboarding time:** Decision rationale discoverable quickly
- ✅ **Higher agent effectiveness:** AI agents reference appropriate context
- ✅ **Eliminated duplicate exploration:** Settled decisions rarely rediscussed
- ✅ **Knowledge reuse:** Patterns transferable across projects
- ✅ **Complete audit trail:** Decision lineage from ideation to implementation
- ✅ **Measurable traceability:** Decision debt ratio provides quality indicator
- ✅ **Improved collaboration:** Shared understanding reduces friction

### Negative (Accepted Trade-offs)

- ⚠️ **Initial training:** Contributors need time to learn marker conventions (~2 hours)
- ⚠️ **Ongoing discipline:** Consistent linking demands vigilance (mitigated by validation)
- ⚠️ **Context window pressure:** Agents loading more decisions (mitigated by selective loading)
- ⚠️ **Validation maintenance:** Link checkers require upkeep
- ⚠️ **Marker noise risk:** Over-documentation could reduce signal (mitigated by debt threshold)

## Implementation

Repositories adopting this framework should:

### Decision Capture Templates

**Inline Marker Template:**

Create template file for easy insertion:

```markdown
<!-- DECISION-MARKER: [ID-or-description] -->
**Decision:** 
**Rationale:** 
**Alternatives:** 
**Consequences:** 
**Status:** [Implemented | Proposed | Deprecated]
**Date:** YYYY-MM-DD
<!-- END-DECISION-MARKER -->
```

**Commit Message Template:**

```
<type>: <subject>

Decision: 
Reference: [DDR-XXX or ADR-XXX]
Rationale: 
Context: [link]
```

### Task YAML Extension

Add decision context block to task schema:

```yaml
# task-template.yaml
id: "task-identifier"
agent: "agent-name"
status: "new"
# ... standard fields ...

decision_context:
  reference: "DDR-XXX or ADR-XXX"
  justification: "Why this decision governs this task"
  alternatives_considered: []
  chosen_because: ""
```

### Agent Profile Updates

Add to all agent profiles:

```markdown
## Decision Traceability (DDR-009)

**Pre-check:**
- Load relevant decision records before proposing changes
- Search for existing decisions in domain before architecting

**Context awareness:**
- Reference appropriate decisions in generated artifacts
- Link to governing decisions in documentation

**Marker generation:**
- Add decision markers when making architectural choices
- Use standardized format (see templates/)

**Validation:**
- Verify generated artifacts link to decisions
- Include decision_context in task results
```

### Validation Scripts

**Link Validation:**

```bash
#!/bin/bash
# validate-decision-links.sh

# Check decision record references are valid
for file in $(find docs/ -name "*.md"); do
  # Extract decision references
  refs=$(grep -o 'DDR-[0-9]\+\|ADR-[0-9]\+' "$file")
  
  for ref in $refs; do
    # Check if referenced decision exists
    if ! find_decision "$ref"; then
      echo "⚠️ Broken link in $file: $ref"
    fi
  done
done
```

**Decision Debt Calculator:**

```python
# calculate-decision-debt.py

def calculate_debt(work_logs):
    total_markers = 0
    formalized = 0
    
    for log in work_logs:
        metrics = log.get('metrics', {}).get('decision_traceability', {})
        total_markers += metrics.get('markers_added', 0)
        formalized += metrics.get('markers_formalized', 0)
    
    debt_ratio = (total_markers - formalized) / total_markers if total_markers > 0 else 0
    
    return {
        'total_markers': total_markers,
        'formalized': formalized,
        'debt_ratio': debt_ratio,
        'status': get_status(debt_ratio)
    }

def get_status(ratio):
    if ratio < 0.20:
        return 'Healthy'
    elif ratio < 0.40:
        return 'Review Needed'
    else:
        return 'Action Required'
```

### Work Log Template Extension

Add decision traceability section:

```yaml
# work-log-template.yaml

context:
  decisions_referenced:
    - DDR-010: Modular directive system applies to agent structure
    - ADR-015: Local repository follows trunk-based development
  decisions_made:
    - "Chose YAML over JSON for task schema (readability)"
  
metrics:
  decision_traceability:
    markers_added: 2
    markers_formalized: 0
    decisions_referenced: 2
    debt_ratio: 1.0  # All markers still informal
```

### Phased Adoption

**Phase 1: Foundation (Week 1-2)**
- Create decision marker templates
- Update agent profiles with decision requirements
- Implement basic link validation

**Phase 2: Tooling (Week 3-4)**
- Implement decision debt calculator
- Create marker extraction tools
- Integrate validation into CI/pre-commit

**Phase 3: Agent Integration (Week 5-6)**
- Update agents with pre-check protocol
- Enable collaboration flow marker generation
- Implement synthesis suggestion logic

**Phase 4: Validation (Week 7-8)**
- Execute pilot tasks with full traceability
- Measure adoption rate and debt ratio
- Iterate based on contributor feedback

## Related

- **Doctrine:** DDR-001 (Primer Execution Matrix) - reflection mode for decision synthesis
- **Doctrine:** DDR-010 (Modular Directive System) - decision markers extend directive system
- **Approach:** Decision capture and traceability approach (framework principles)
- **Implementation:** See repository-specific ADRs for validation tooling and metrics
