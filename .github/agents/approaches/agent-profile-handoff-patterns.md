# Agent Profile Handoff Patterns Template

**Purpose:** Guide for documenting common handoff patterns in agent profiles as recommended by ADR-011.

**Last Updated:** 2025-11-24  
**Related ADR:** ADR-015 (Follow-Up Task Lookup Pattern - Rejected)

## Overview

Instead of a centralized lookup table, each agent profile documents its own observed handoff patterns. This approach:

- Preserves agent autonomy
- Requires zero implementation complexity
- Remains easy to maintain
- Provides discoverable guidance during agent initialization

## Template Structure

Add this section to each agent profile (`.github/agents/<agent-name>.agent.md`):

```markdown
## Common Handoff Patterns

### Outgoing Handoffs

*Document typical next agents for this agent's outputs based on observed practice*

**Pattern:** [Output Type] → [Next Agent]
- **When:** [Conditions/Context]
- **Purpose:** [Why this handoff makes sense]
- **Example:** [Task ID reference if available]

### Incoming Handoffs

*Document typical upstream agents that handoff to this agent*

**Pattern:** [Source Agent] → This Agent
- **When:** [Conditions/Context]  
- **Purpose:** [What this agent provides in the chain]
- **Example:** [Task ID reference if available]

### Special Cases

*Document context-dependent variations or exceptions*

- **Case:** [Description]
- **Reasoning:** [Why standard pattern doesn't apply]
```

## Agent-Specific Examples

### Architect Profile Example

```markdown
## Common Handoff Patterns

### Outgoing Handoffs

**Pattern:** ADR Creation → Diagrammer
- **When:** ADR describes complex component relationships or architectural patterns
- **Purpose:** Visual representation improves comprehension and communication
- **Example:** 2025-11-23T1738 (ADR-009 → diagram updates)

**Pattern:** ADR Creation → Writer-Editor
- **When:** ADR targets broad audience or requires polish for publication
- **Purpose:** Clarity and accessibility improvements
- **Example:** (Future - no observed instances yet)

**Pattern:** Assessment/Review → No Handoff (Terminal)
- **When:** Assessment is informational or decision-making document
- **Purpose:** Assessments typically don't require downstream transformation
- **Example:** 2025-11-23T2158 (implementation review)

### Incoming Handoffs

**Pattern:** Manager → Architect
- **When:** High-level architectural decisions needed
- **Purpose:** Decompose complex socio-technical problems, surface trade-offs
- **Example:** 2025-11-23T1846 (follow-up lookup assessment)

### Special Cases

- **Multi-output ADRs:** If ADR creates both documentation and diagrams, may handoff to synthesizer instead of individual specialists
- **Rejected ADRs:** Typically terminal - no handoff unless rejection requires alternative proposal
```

### Curator Profile Example

```markdown
## Common Handoff Patterns

### Outgoing Handoffs

**Pattern:** Documentation Creation → Writer-Editor
- **When:** Documentation targets end-users and requires polish for clarity
- **Purpose:** Writer-Editor specializes in accessibility and readability
- **Example:** 2025-11-23T0722 (orchestration guide → writer-editor polish)

**Pattern:** Structural Audit → Depends on Findings
- **When:** Audit identifies issues requiring correction
- **Purpose:** Route to specialist capable of addressing specific issue type
- **Example:** (Conditional - no observed instances yet)

**Pattern:** Quality Gate → No Handoff (Terminal)
- **When:** Curator performs final validation in a workflow chain
- **Purpose:** Quality gates are typically end-of-chain
- **Example:** (POC3 Phase 5 - not yet executed)

### Incoming Handoffs

**Pattern:** Any Agent → Curator
- **When:** Documentation, configuration, or structural artifacts need validation
- **Purpose:** Curator provides structural consistency audits and integrity checks
- **Example:** 2025-11-23T0722 (self-initiated orchestration guide)

### Special Cases

- **Self-initiated tasks:** Curator may create documentation and self-hand-off to writer-editor
- **Validation failures:** If audit finds critical issues, may hand back to original agent rather than forward
```

### Writer-Editor Profile Example

```markdown
## Common Handoff Patterns

### Outgoing Handoffs

**Pattern:** Documentation Polish → Curator (Optional)
- **When:** Polished documentation benefits from final structural audit
- **Purpose:** Curator validates consistency and completeness
- **Example:** (Rare - most writer-editor tasks are terminal)

**Pattern:** Documentation Polish → No Handoff (Terminal)
- **When:** Polish completes the documentation workflow
- **Purpose:** Writer-editor is often final step in documentation chains
- **Example:** 2025-11-23T2207 (orchestration guide polish)

### Incoming Handoffs

**Pattern:** Curator → Writer-Editor
- **When:** Documentation needs clarity and accessibility improvements
- **Purpose:** Polish rough documentation for end-user consumption
- **Example:** 2025-11-23T0722 → 2025-11-23T2207 (orchestration guide)

**Pattern:** Synthesizer → Writer-Editor
- **When:** Synthesis documents need refinement for publication
- **Purpose:** Improve narrative flow and readability
- **Example:** 2025-11-23T2117 (POC3 synthesis → writer-editor)

### Special Cases

- **Technical documentation:** May require light touch to preserve technical accuracy
- **User guides:** May require heavier editing for accessibility
```

### Diagrammer Profile Example

```markdown
## Common Handoff Patterns

### Outgoing Handoffs

**Pattern:** Diagram Creation → Synthesizer
- **When:** Diagrams are part of multi-artifact deliverable (e.g., ADR + diagrams)
- **Purpose:** Synthesizer integrates diagrams with textual artifacts
- **Example:** 2025-11-23T2100 (POC3 diagrams → synthesizer)

**Pattern:** Diagram Creation → Curator
- **When:** Diagrams require accessibility validation (alt-text)
- **Purpose:** Curator validates DESCRIPTIONS.md completeness
- **Example:** (Alternative to synthesizer handoff)

**Pattern:** Diagram Creation → No Handoff (Terminal)
- **When:** Diagram creation is standalone deliverable
- **Purpose:** Simple diagram additions don't require downstream transformation
- **Example:** (Observed in simple updates)

### Incoming Handoffs

**Pattern:** Architect → Diagrammer
- **When:** Architectural concepts benefit from visual representation
- **Purpose:** Create PlantUML diagrams for ADRs, technical designs
- **Example:** 2025-11-23T1738 (ADR-009 → diagram updates)

### Special Cases

- **Diagram updates vs. creation:** Updates may be terminal, creation often triggers synthesis
- **Rendering validation:** If rendering fails, may loop back to diagrammer for fixes
```

### Synthesizer Profile Example

```markdown
## Common Handoff Patterns

### Outgoing Handoffs

**Pattern:** Synthesis Document → Writer-Editor
- **When:** Synthesis needs clarity refinement for broader audience
- **Purpose:** Writer-editor improves narrative flow and accessibility
- **Example:** 2025-11-23T2117 (POC3 synthesis → writer-editor suggested)

**Pattern:** Synthesis Document → Curator
- **When:** Synthesis is final integration requiring quality gate
- **Purpose:** Curator validates cross-artifact consistency
- **Example:** (Alternative to writer-editor handoff)

### Incoming Handoffs

**Pattern:** Diagrammer → Synthesizer
- **When:** Multiple artifacts (diagrams + text) need integration
- **Purpose:** Synthesizer aggregates and validates consistency
- **Example:** 2025-11-23T2100 (POC3 diagrams → synthesizer)

**Pattern:** Multiple Agents → Synthesizer
- **When:** Complex workflows produce distributed artifacts
- **Purpose:** Synthesizer provides cross-artifact linkage and validation
- **Example:** (Future multi-source synthesis)

### Special Cases

- **Convergent workflows:** Synthesizer may wait for multiple upstream agents to complete
- **Validation vs. integration:** Some synthesis tasks focus on validation, others on narrative integration
```

## Usage Guidelines

### For Agent Profile Authors

1. **Start minimal:** Document only observed patterns, don't speculate
2. **Update organically:** Add patterns as you observe them in completed tasks
3. **Cite examples:** Reference actual task IDs to ground patterns in evidence
4. **Mark speculation:** Use "(Future)" or "(Not yet observed)" for hypothetical patterns
5. **Include context:** Explain *why* handoff makes sense, not just *what* handoff occurs

### For Agents Using Profiles

1. **Read during initialization:** Load handoff patterns as guidance, not rules
2. **Apply contextually:** Consider whether pattern fits current task context
3. **Deviate when appropriate:** Patterns are guidance; use judgment
4. **Document deviations:** If you deviate from pattern, note why in work log
5. **Suggest updates:** If you discover new patterns, note for profile enhancement

### For Framework Maintainers

1. **Review quarterly:** Check if documented patterns match observed practice
2. **Add missing patterns:** Update profiles when new patterns emerge
3. **Remove stale patterns:** Archive patterns that no longer apply
4. **Cross-reference:** Link to task IDs as evidence for patterns
5. **Maintain consistency:** Use similar structure across all agent profiles

## Maintenance Process

### When to Update Patterns

- After completing a sprint with multiple handoffs
- When new agent added to framework
- When agent specialization changes
- During quarterly documentation reviews
- When handoff errors occur (document correct pattern)

### Update Checklist

- [ ] Pattern observed in at least 2 task instances?
- [ ] Pattern documented with example task ID?
- [ ] Conditions/context clearly explained?
- [ ] Purpose/rationale provided?
- [ ] Special cases identified?
- [ ] Consistent with agent specialization?
- [ ] Reviewed by agent maintainer?

## Advantages Over Centralized Lookup Table

| Dimension               | Agent Profile Patterns          | Centralized Lookup Table                 |
|-------------------------|---------------------------------|------------------------------------------|
| **Implementation Cost** | Zero (markdown addition)        | High (schema, conditions, evaluation)    |
| **Maintenance**         | Update profile as observed      | Update central file, propagate to agents |
| **Autonomy**            | Full (guidance only)            | Reduced (prescriptive)                   |
| **Flexibility**         | High (agent interprets context) | Low (condition-based evaluation)         |
| **Discoverability**     | High (loaded during init)       | Requires central file lookup             |
| **Alignment**           | Organic emergence               | Premature standardization                |

## References

- **ADR-015:** Follow-Up Task Lookup Pattern (Rejected)
- **ADR-008:** File-Based Asynchronous Coordination
- **File-Based Orchestration Approach:** `.github/agents/approaches/file-based-orchestration.md`
- **Agent Profiles:** `.github/agents/*.agent.md`

---

_Maintained by: Curator Claire & Architect Alphonso_  
_For questions, see: ADR-015 or file-based-orchestration.md_
