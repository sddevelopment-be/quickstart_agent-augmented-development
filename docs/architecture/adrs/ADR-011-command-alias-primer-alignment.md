# Architecture Decision Records

## ADR-011: Formalize Primer → Command Alias Alignment

**status**: Accepted  
**date**: 2025-11-24

### Context

The *Agentic Solutioning Primer* (`docs/architecture/synthesis/solutioning_primer.md`) defines five execution primers (Context Check, Progressive Refinement, Trade-Off Navigation, Transparency & Error Signaling, Reflection Loop). Each relies on explicit command aliases (`/validate-alignment`, `/fast-draft`, `/precision-pass`, `/analysis-mode`, `/meta-mode`, etc.) to anchor behavior. Today, the alias file (`agents/aliases.md`) and specialist profiles describe these commands individually but do not codify their primer-specific obligations. This gap causes inconsistent agent behavior, complicates training, and makes it difficult to enforce the reflections envisioned by AGENTS.md.

### Decision

We will formalize the mapping between solutioning primers and command aliases as a first-class directive set:

1. Update the aliases overview to embed primer-specific usage notes, including required entry/exit markers and validation checkpoints.
2. Introduce directive text clarifying how each primer must be executed (alias invocation order, minimum logging requirements, integrity symbols).
3. Require specialist agent definitions to reference the relevant primer directives, ensuring role descriptions inherit the canonical mapping.

### Rationale

- **Consistency:** Agents will interpret `/fast-draft`, `/precision-pass`, `/analysis-mode`, and `/meta-mode` uniformly, reducing drift and making multi-agent collaboration predictable.
- **Traceability:** Primer alignment becomes auditable; logs and ADRs can reference directive IDs rather than ad-hoc descriptions.
- **Safety:** Embedding alias obligations in directives reinforces the guardrails already prescribed by AGENTS.md, making silent deviations less likely.
- **Onboarding Efficiency:** New specialist profiles gain ready-made behavioral contracts without re-describing the primer mechanics.

### Envisioned Consequences

**Positive**
- ✅ Clear linkage between behavior primers and operational commands improves reviewability of agent outputs.
- ✅ Specialist updates become lighter because directive references replace duplicated prose.
- ✅ Validation tooling can lint for missing primer markers, improving observability.

**Negative / Watch-outs**
- ⚠️ Additional maintenance overhead: changes to primers now require synchronized edits across aliases, directives, and profiles.
- ⚠️ Risk of ceremony fatigue for trivial tasks unless we document exceptions or heuristics in the directive text.

### Considered Alternatives

1. **Leave mapping inside the synthesis note only.** Rejected because it keeps expectations informal and hard to enforce.
2. **Embed primer instructions directly in every specialist profile.** Rejected due to duplication and heightened risk of divergence.
3. **Introduce tooling-only enforcement (linters) without directive updates.** Rejected because governance should precede automation; directives provide the normative baseline.
