# Tactic: ADR Drafting Workflow

**Invoked by:**
- [Directive 018 (Traceable Decisions)](../directives/018_traceable_decisions.md) — decision documentation
- Shorthand: [`/architect-adr`](../shorthands/architect-adr.md)

**Related tactics:**
- [`premortem-risk-identification.tactic.md`](./premortem-risk-identification.tactic.md) — failure mode analysis
- [`ammerse-analysis.tactic.md`](./ammerse-analysis.tactic.md) — trade-off evaluation
- [`adversarial-testing.tactic.md`](./adversarial-testing.tactic.md) — stress-test alternatives

---

## Intent

Systematically draft Architectural Decision Records (ADRs) with comprehensive trade-off analysis, risk assessment, and stakeholder context.

**Apply when:**
- Making architectural choices affecting multiple components
- Evaluating alternatives with significant trade-offs
- Need to document rationale for future contributors
- Decision has medium-high impact and limited reversibility

---

## Preconditions

**Required inputs:**
- Decision title (brief, descriptive)
- Problem context (why this decision is needed)
- At least 2 alternatives considered
- Preferred option identified

**Optional inputs:**
- Forces/constraints, risk appetite, time horizon, NFRs

---

## Execution Steps

### 1. Validate Uniqueness
- [ ] Search existing ADRs for similar decisions
- [ ] Check if this extends/supersedes existing ADR
- [ ] Assign next ADR number

### 2. Decompose Context
- [ ] Problem statement (1-2 sentences)
- [ ] Drivers (what forces this decision now)
- [ ] Constraints (technical, organizational, timeline)

### 3. Analyze Options (Matrix)
- [ ] List all considered alternatives
- [ ] Score against impact areas (performance, maintainability, etc.)
- [ ] Qualitative assessment (Low/Medium/High)

### 4. Draft ADR Sections
- [ ] **Context:** Problem + drivers + constraints
- [ ] **Decision:** Chosen option (≤120 words)
- [ ] **Rationale:** Why this option (trade-off narrative)
- [ ] **Consequences:** Positive + negative impacts
- [ ] **Alternatives:** Rejected options with rejection rationale (1 sentence each)

### 5. Risk Assessment
- [ ] Invoke premortem-risk-identification tactic if high-risk
- [ ] Document failure modes
- [ ] Align with stated risk appetite

### 6. Success Metrics
- [ ] Define measurable acceptance criteria
- [ ] Specify validation approach

### 7. Cross-Link Updates
- [ ] Add ADR to README index
- [ ] Link related ADRs
- [ ] Reference from affected code/docs

---

## Outputs
- ADR markdown file (`docs/architecture/adrs/ADR-XXX-slug.md`)
- Option impact matrix
- Success metrics list
- Cross-reference updates

---

**Status:** ✅ Active
