# Doctrine Decision Records

## DDR-001: Primer Execution Matrix

**status**: Accepted  
**date**: 2026-02-11  
**supersedes**: ADR-011 (content extracted and elevated to doctrine)

### Context

The *Agentic Solutioning Primer* defines five execution primers (Context Check, Progressive Refinement, Trade-Off Navigation, Transparency & Error Signaling, Reflection Loop). Each relies on explicit command aliases (`/validate-alignment`, `/fast-draft`, `/precision-pass`, `/analysis-mode`, `/meta-mode`, etc.) to anchor behavior. 

For the framework to work universally across repositories, agents must interpret these primers and their associated commands consistently. Without formalized primer-to-command mapping, agent behavior drifts, collaboration becomes unpredictable, and the reflective practices envisioned by the framework cannot be reliably enforced.

### Decision

We formalize the mapping between solutioning primers and command aliases as a first-class doctrine pattern:

1. **Command Alias Obligation**: Each primer maps to specific command aliases with defined entry/exit markers and validation checkpoints.
2. **Directive Integration**: Primer-specific directives (e.g., Directive 010: Mode Protocol) codify the execution requirements for each primer.
3. **Profile Inheritance**: All specialist agent definitions reference primer directives to ensure consistent interpretation of commands.

### Primer-Command Matrix

| Primer | Primary Commands | Required Markers | Validation |
|--------|-----------------|------------------|------------|
| Context Check | `/validate-alignment` | ✅ alignment confirmed | Pre-execution audit |
| Progressive Refinement | `/fast-draft`, `/precision-pass` | 🎯 draft complete, ✅ precision pass | Iteration tracking |
| Trade-Off Navigation | `/analysis-mode` | ⚖️ trade-offs evaluated | Decision documentation |
| Transparency & Error Signaling | Status markers (✅, ⚠️, ❗️) | Explicit severity indicators | Error escalation |
| Reflection Loop | `/meta-mode` | 🔄 reflection initiated | Process improvement |

### Rationale

- **Consistency**: Agents interpret commands uniformly, reducing drift and making multi-agent collaboration predictable.
- **Traceability**: Primer alignment becomes auditable; logs and decisions can reference primer obligations rather than ad-hoc descriptions.
- **Safety**: Embedding command obligations in doctrine reinforces guardrails and makes silent deviations less likely.
- **Onboarding Efficiency**: New specialist profiles gain ready-made behavioral contracts without re-describing primer mechanics.

### Consequences

**Positive**
- ✅ Clear linkage between behavior primers and operational commands improves reviewability of agent outputs.
- ✅ Specialist profiles become lighter because directive references replace duplicated prose.
- ✅ Validation tooling can lint for missing primer markers, improving observability.

**Watch-outs**
- ⚠️ Maintenance overhead: changes to primers require synchronized edits across directives and profiles.
- ⚠️ Risk of ceremony fatigue for trivial tasks unless exceptions are documented.

### Implementation

**In Agent Profiles:**
```markdown
**Primer Requirement:** Follow the Primer Execution Matrix (DDR-001) defined in Directive 010 (Mode Protocol) and log primer usage per Directive 014.
```

**In Directives:**
- Directive 010 (Mode Protocol) defines operational semantics
- Directive 014 (Work Log Creation) mandates primer usage tracking
- Directive 015 (Store Prompts) ensures primer context is preserved

### Considered Alternatives

1. **Leave mapping inside synthesis notes only**: Rejected because it keeps expectations informal and hard to enforce.
2. **Embed primer instructions directly in every specialist profile**: Rejected due to duplication and heightened risk of divergence.
3. **Introduce tooling-only enforcement without doctrine updates**: Rejected because governance should precede automation.

### Related

- **Doctrine**: Directive 010 (Mode Protocol), Directive 014 (Work Log Creation)
- **Implementation**: See repository-specific ADRs for how primers are operationalized in tooling
