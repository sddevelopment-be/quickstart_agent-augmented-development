# Tactics: Procedural Execution Guides

Tactics are step-by-step procedures for executing specific activities within the agentic development framework. They provide concrete, ordered instructions that agents can follow to accomplish well-defined objectives.

**Location:** `tactics/`  
**Purpose:** Procedural execution (the "how")  
**Invoked by:** Directives (explicit) or discoverable exploration (with Human approval)

---

## What Tactics Are

Tactics sit in the **fourth layer** of the doctrine stack, between Directives (which select what to do) and Templates (which define output shape).

**Characteristics:**
- **Procedural:** Step-by-step instructions, not advisory guidance
- **Bounded:** Clear preconditions, execution steps, and exit criteria
- **Verifiable:** Concrete outputs and measurable completion signals
- **Failure-aware:** Explicit failure modes to prevent silent errors

**Not Tactics:**
- Philosophical frameworks (those are Approaches)
- Compliance rules (those are Directives)
- Output formats (those are Templates)
- Strategic guidance (those are Guidelines)

---

## How to Use Tactics

### Directive-Driven Invocation (Primary Path)

When a Directive explicitly references a tactic:

1. Directive mandates tactic invocation at specific workflow step
2. Agent loads tactic file and follows execution steps
3. Agent documents tactic invocation and results in work log
4. Agent proceeds with workflow

**Example:**
```markdown
## Directive 018 (Traceable Decisions)

When creating an ADR for a high-risk decision:
- Invoke tactic: `./premortem-risk-identification.tactic.md`
- Document failure scenarios in ADR "Risks" section
```

### Exploratory Discovery (Secondary Path)

When context suggests a tactic might apply but no Directive mandates it:

1. Agent searches this README for relevant tactic
2. Agent proposes tactic to Human with rationale
3. Human approves or rejects invocation
4. If approved, agent loads tactic and follows execution steps
5. Agent documents approval and results in work log

---

## Available Tactics

### Decision-Making & Risk

| Tactic | File | Intent | Invoke When | Invoked By | Notes |
|--------|------|--------|-------------|------------|-------|
| **Stopping Conditions** | [`stopping-conditions.tactic.md`](./stopping-conditions.tactic.md) | Define exit criteria to prevent indefinite effort, scope creep, and resource exhaustion | Long-running tasks (>30 min), unbounded exploration, resource-intensive operations | [Directive 024](../directives/024_self_observation_protocol.md) (Self-Observation Protocol), [Directive 011](../directives/011_risk_escalation.md) (Risk & Escalation) | |
| **Premortem Risk Identification** | [`premortem-risk-identification.tactic.md`](./premortem-risk-identification.tactic.md) | Identify potential failure modes before project start by imagining catastrophic failure and working backward | ADR creation, architecture decisions, high-risk/low-reversibility choices | [Directive 018](../directives/018_traceable_decisions.md) (Traceable Decisions) | |
| **Analysis.AdversarialTesting** | [`adversarial-testing.tactic.md`](./adversarial-testing.tactic.md) | Stress-test proposals, designs, or practices by deliberately attempting to make them fail | Evaluating practices/proposals with broad impact, need for intellectual honesty before commitment | [Directive 018](../directives/018_traceable_decisions.md) (Traceable Decisions) | Broader scope (proposals, practices) vs. project-specific failure scenarios. Complementary to Premortem, not redundant |
| **Analysis.AMMERSE** | [`ammerse-analysis.tactic.md`](./ammerse-analysis.tactic.md) | Evaluate decisions using AMMERSE framework (Agile, Minimal, Maintainable, Environmental, Reachable, Solvable, Extensible) with qualitative trade-off analysis | Architectural decisions, practice evaluation, need transparent rationale for value-driven choices | (Discoverable — architectural trade-off reasoning, Human decision) | Qualitative approach (Low/Medium/High weights) preferred over quantitative formulas to avoid false precision |

### Experimentation & Validation

| Tactic | File | Intent | Invoke When | Invoked By | Notes |
|--------|------|--------|-------------|------------|-------|
| **Safe-to-Fail Experiment Design** | [`safe-to-fail-experiment-design.tactic.md`](./safe-to-fail-experiment-design.tactic.md) | Structure exploratory work as small, reversible experiments with explicit success/failure criteria | High uncertainty about best approach, learning prioritized over optimization, rollback mechanisms exist | [Directive 021](../directives/021_locality_of_change.md) (Locality of Change) | Transform uncertainty from paralysis ("what if I'm wrong?") to progress ("what will I learn?") |

### Testing & Quality

| Tactic | File | Intent | Invoke When | Invoked By | Notes |
|--------|------|--------|-------------|------------|-------|
| **ATDD.AdversarialAcceptance** | [`ATDD_adversarial-acceptance.tactic.md`](./ATDD_adversarial-acceptance.tactic.md) | Strengthen ATDD acceptance criteria by exploring adversarial failure scenarios and converting them to acceptance tests | Defining ATDD acceptance boundaries, exploring edge cases and misuse scenarios | [Directive 016](../directives/016_acceptance_test_driven_development.md) (ATDD) | Specialized for ATDD practitioners. Combines adversarial thinking with acceptance test definition |
| **Test Boundaries by Functional Responsibility** | [`test-boundaries-by-responsibility.tactic.md`](./test-boundaries-by-responsibility.tactic.md) | Determine appropriate test scope by identifying which components are directly responsible for functionality being validated | Writing unit/integration tests, unclear whether to mock a dependency, team debates "what is a unit?" | [Directive 016](../directives/016_acceptance_test_driven_development.md) (ATDD), [Directive 017](../directives/017_test_driven_development.md) (TDD) | Responsibility-based boundaries (what implements the feature logic) vs. structural boundaries (layers, modules) |

### Code Quality & Security

| Tactic | File | Intent | Invoke When | Invoked By | Notes |
|--------|------|--------|-------------|------------|-------|
| **Input Validation with Fail-Fast Feedback** | [`input-validation-fail-fast.tactic.md`](./input-validation-fail-fast.tactic.md) | Validate input data comprehensively before processing, provide clear error feedback while protecting system internals | Processing external data (APIs, file uploads, user input), expensive computation, security-sensitive contexts | (Discoverable — general best practice) | Dual-level feedback (user-facing: clear/actionable, internal logs: detailed/diagnostic) |

### Code Review & Maintenance

| Tactic | File | Intent | Invoke When | Invoked By | Notes |
|--------|------|--------|-------------|------------|-------|
| **CodeReview.Incremental** | [`code-review-incremental.tactic.md`](./code-review-incremental.tactic.md) | Review change sets for correctness, structural, and architectural risks without expanding scope | PR review, commit analysis, change assessment | [Directive 021](../directives/021_locality_of_change.md) (Locality of Change) | Observations and questions, not prescriptive commands. Resist urge to redesign during review |

### Refactoring

| Tactic | File | Intent | Invoke When | Invoked By | Notes |
|--------|------|--------|-------------|------------|-------|
| **Refactoring.MoveMethod** | [`refactoring-move-method.tactic.md`](./refactoring-move-method.tactic.md) | Relocate a method from one class to another when the method exhibits "Feature Envy" (uses more features of another class than its own) | Method uses more features of target class, needs to improve cohesion, aligning behavior with data | [Directive 039](../directives/039_refactoring_techniques.md) (Refactoring Techniques), [Directive 021](../directives/021_locality_of_change.md) (Locality of Change) | Incremental approach: Copy → Delegate → Update → Remove. Emphasizes test-first safety and Information Expert principle |
| **Refactoring.StranglerFig** | [`refactoring-strangler-fig.tactic.md`](./refactoring-strangler-fig.tactic.md) | Incrementally replace existing functionality by building new implementation alongside old and gradually rerouting behavior | Large-scale refactoring that cannot be done safely in one step, zero-downtime migration required | [Directive 039](../directives/039_refactoring_techniques.md) (Refactoring Techniques), [Directive 017](../directives/017_test_driven_development.md) (TDD) | Architectural pattern for safe system evolution. Coexistence → Rerouting → Removal. Uses feature flags or routing layers |
| **Refactoring.ExtractFirstOrderConcept** | [`refactoring-extract-first-order-concept.tactic.md`](./refactoring-extract-first-order-concept.tactic.md) | Extract implicit or duplicated logic into an explicit first-order concept with clear responsibility | Logic duplicated in 3+ places (Rule of Three), implicit patterns need to be made explicit | [Directive 039](../directives/039_refactoring_techniques.md) (Refactoring Techniques), [Directive 017](../directives/017_test_driven_development.md) (TDD) | Creates named abstractions. Identifies responsibility → Extracts → Updates callers → Verifies tests |
| **Refactoring.GuardClausesBeforePolymorphism** | [`refactoring-guard-clauses-before-polymorphism.tactic.md`](./refactoring-guard-clauses-before-polymorphism.tactic.md) | Flatten nested conditionals into explicit guard clauses before introducing polymorphism | Branch pyramids hide variant boundaries and block safe extraction | [Directive 039](../directives/039_refactoring_techniques.md) (Refactoring Techniques), [Directive 017](../directives/017_test_driven_development.md) (TDD) | Creates an ordered, testable branch surface so polymorphic extraction can happen with lower risk |
| **Refactoring.ExtractClassByResponsibilitySplit** | [`refactoring-extract-class-by-responsibility-split.tactic.md`](./refactoring-extract-class-by-responsibility-split.tactic.md) | Split a large mixed-responsibility class into cohesive class boundaries | Class changes for multiple reasons, behavior clusters are separable | [Directive 039](../directives/039_refactoring_techniques.md) (Refactoring Techniques), [Directive 021](../directives/021_locality_of_change.md) (Locality of Change) | Moves one responsibility cluster at a time with delegation to preserve behavior during migration |
| **Refactoring.ReplaceMagicNumberWithSymbolicConstant** | [`refactoring-replace-magic-number-with-symbolic-constant.tactic.md`](./refactoring-replace-magic-number-with-symbolic-constant.tactic.md) | Replace opaque numeric literals with semantic constants | Business thresholds/policy values are encoded as unnamed literals | [Directive 039](../directives/039_refactoring_techniques.md) (Refactoring Techniques), [Directive 017](../directives/017_test_driven_development.md) (TDD) | Improves readability and change safety while preserving behavior via test-backed replacement |

---

## Tactic Selection Guidance

### By Context

**Starting a new task or experiment:**
- `stopping-conditions.tactic.md` (define exit criteria first)

**Making architectural decisions:**
- `premortem-risk-identification.tactic.md` (project-specific risks)
- `adversarial-testing.tactic.md` (stress-test proposal/practice)
- `ammerse-analysis.tactic.md` (trade-off analysis)

**Defining tests:**
- `ATDD_adversarial-acceptance.tactic.md` (acceptance boundaries with adversarial thinking)
- `test-boundaries-by-responsibility.tactic.md` (scope clarity)

**Exploring under uncertainty:**
- `safe-to-fail-experiment-design.tactic.md` (structured experiments)
- `stopping-conditions.tactic.md` (exit criteria for exploration)

**Building robust systems:**
- `input-validation-fail-fast.tactic.md` (validation patterns)

**Reviewing changes:**
- `code-review-incremental.tactic.md` (scope-preserving review)

**Refactoring code:**
- `refactoring-move-method.tactic.md` (relocate methods with Feature Envy)
- `refactoring-extract-first-order-concept.tactic.md` (eliminate duplication, make patterns explicit)
- `refactoring-strangler-fig.tactic.md` (large-scale incremental replacement)
- `refactoring-guard-clauses-before-polymorphism.tactic.md` (flatten branch pyramids before polymorphic extraction)
- `refactoring-extract-class-by-responsibility-split.tactic.md` (split mixed classes by cohesive responsibility)
- `refactoring-replace-magic-number-with-symbolic-constant.tactic.md` (replace numeric literals with semantic constants)

---

## Cross-References

### Risk Discovery Triad
- `stopping-conditions.tactic.md` ↔ `premortem-risk-identification.tactic.md` (exit criteria based on risks)
- `premortem-risk-identification.tactic.md` ↔ `adversarial-testing.tactic.md` (project vs. proposal scope)
- `adversarial-testing.tactic.md` ↔ `ammerse-analysis.tactic.md` (stress-testing then trade-off analysis)

### ATDD Workflow
- `ATDD_adversarial-acceptance.tactic.md` → `adversarial-testing.tactic.md` (builds on broader adversarial thinking)
- `ATDD_adversarial-acceptance.tactic.md` ↔ `test-boundaries-by-responsibility.tactic.md` (boundary definition)

### Experimentation Pair
- `safe-to-fail-experiment-design.tactic.md` ↔ `stopping-conditions.tactic.md` (experiments need exit criteria)

### Refactoring Set
- `refactoring-move-method.tactic.md` ↔ `refactoring-extract-first-order-concept.tactic.md` (both improve class structure)
- `refactoring-strangler-fig.tactic.md` → may use `refactoring-move-method.tactic.md` within new implementation
- `refactoring-guard-clauses-before-polymorphism.tactic.md` → precedes polymorphism-oriented extraction tactics
- `refactoring-extract-class-by-responsibility-split.tactic.md` ↔ complements `refactoring-move-method.tactic.md`
- `refactoring-replace-magic-number-with-symbolic-constant.tactic.md` → clarifies domain policy before rule extraction
- All refactoring tactics reference [Directive 017](../directives/017_test_driven_development.md) for test-first safety

---

## Maintenance

**For tactic lifecycle management** (adding, updating, curating), see [`tactics-curation.tactic.md`](./tactics-curation.tactic.md).

---

## Version

**README Version:** 1.2.0  
**Last Updated:** 2026-02-12  
**Tactic Files (.tactic.md):** 40
