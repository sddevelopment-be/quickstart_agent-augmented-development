# Architecture Specification: Spec Kitty × Doctrine Integration

**Status:** Proposed  
**Date:** 2026-02-14  
**Author:** Architect Alphonso  
**Supersedes:** `spec-kitty-governance-doctrine-extension-proposal.md`  
**Related:** ADR-045 (Domain Model), ADR-046 (Bounded Contexts), ADR-048 (Run Container)

---

## Context

### Problem Statement

Two systems with complementary capabilities exist in parallel:

1. **Spec Kitty**: Production-quality workflow orchestrator managing the spec-driven development lifecycle (`spec → plan → tasks → implement → review → accept → merge`). Strong in mission adaptation, worktree isolation, multi-agent coordination, and quality gates.

2. **Doctrine Framework**: Behavioral governance stack (Guidelines → Approaches → Directives → Tactics → Templates) with agent profiles, file-based collaboration, and precedence-driven constraint systems. Strong in policy enforcement, decision traceability, and cross-cutting behavioral quality.

**Current state:** Both systems independently address agent-augmented development but overlap in agent configuration, project initialization, coordination mechanisms, and governance models. Using both creates friction:

- **Dual authority problem**: Constitution vs. Guidelines both claim top-level behavioral authority
- **Parallel coordination**: WP frontmatter lanes vs. `work/collaboration/` YAML tasks
- **Agent identity gap**: Flat agent config keys vs. rich agent profiles with capabilities
- **Token budget pressure**: Loading both contexts simultaneously risks exhausting agent context windows

**Business value at risk:** Teams want Spec Kitty's workflow polish with Doctrine's governance depth, but integration friction blocks adoption.

### Coverage Analysis Summary

From `2026-02-14-control-plane-spec-kitty-coverage.md`:

| System Component | Spec Kitty Coverage | Gap |
|---|:---:|---|
| CLI/TUI Interface | ✅ 100% | Production Typer + Rich + StepTracker |
| Task Lifecycle Management | ✅ 95% | WP frontmatter lanes, kanban workflow |
| Agent Coordination | 🟡 60% | Multi-agent orchestrator present; lacks CQRS events |
| Quality Gates | ✅ 90% | Merge preflight, conflict forecasting, validators |
| **Telemetry & Observability** | ❌ 5% | No JSONL event log, no materialized views, no cost tracking |
| **LLM Model Routing** | ❌ 0% | Model-agnostic by design; no agent-to-model mapping |
| **Budget Enforcement** | ❌ 0% | No financial awareness |
| **CQRS Event Architecture** | ❌ 10% | Implicit command/query separation; no event sourcing |
| **Structured Error Reporting** | ❌ 5% | No CI/CD error extraction |
| **Async Execution & Cancellation** | ❌ 0% | Synchronous only; no signal escalation |

**Weighted average infrastructure coverage: ~25%**

### Strategic Decision

**This proposal adopts Option C from the integration analysis**: **Spec Kitty as primary product platform, Doctrine as governance plugin layer.**

**Rationale:**
1. Spec Kitty already provides production CLI, mission system, worktree isolation, and orchestration engine — 75% of needed capability
2. Doctrine provides governance depth, constraint systems, and precedence rules that Spec Kitty lacks
3. Building missing infrastructure (telemetry, routing, events) as shared libraries benefits both systems
4. Git subtree distribution mechanism already works; requires zero changes to Spec Kitty core
5. Preserves both systems' independence and avoids forced migration

---

## Decision

### High-Level Architecture

**We will implement a five-layer architecture where Spec Kitty owns orchestration and Doctrine provides governance as an optional plugin:**

```
Layer 1: Governance Plugin (Doctrine + .doctrine-config/)
         ↓ (policy constraints, directive loading)
Layer 2: Specification Domain (Spec Kitty kitty-specs/ + missions/)
         ↓ (work package definition, domain context)
Layer 3: Orchestration (Spec Kitty workflow engine, worktree, dependency scheduling)
         ↓ (lifecycle transitions, agent coordination)
Layer 4: Routing (RoutingProvider interface, model/tool selection)
         ↓ (agent-to-LLM mapping, fallback chains)
Layer 5: Execution (LLM vendor adapters, telemetry, artifact capture)
```

### Interface Contracts

#### 1. GovernancePlugin Interface

**Purpose:** Enable Doctrine to hook into Spec Kitty lifecycle without modifying core.

**Contract:**
```python
class GovernancePlugin(ABC):
    """Pluggable governance layer for Spec Kitty workflows."""
    
    @abstractmethod
    def validate_pre_plan(self, spec_context: SpecContext) -> ValidationResult:
        """Check spec against governance rules before planning."""
        pass
    
    @abstractmethod
    def validate_pre_implement(self, task_context: TaskContext) -> ValidationResult:
        """Check task assignment and agent capabilities before implementation."""
        pass
    
    @abstractmethod
    def validate_pre_review(self, work_package: WorkPackage) -> ValidationResult:
        """Check work products against quality gates before review."""
        pass
    
    @abstractmethod
    def validate_pre_accept(self, review_context: ReviewContext) -> ValidationResult:
        """Check acceptance criteria and decision documentation before accept."""
        pass

@dataclass(frozen=True)
class ValidationResult:
    """Normalized governance check output."""
    status: ValidationStatus  # pass | warn | block
    reasons: list[str]
    directive_refs: list[int]
    suggested_actions: list[str]
```

**Input contracts:**
- `SpecContext`: Spec content, target mission, feature scope
- `TaskContext`: Task metadata, assigned agent, acceptance criteria
- `WorkPackage`: Implementation artifacts, test results, commit references
- `ReviewContext`: Review comments, approval state, merge conflicts

**Output contract:**
- `pass`: Allow workflow transition
- `warn`: Log concern but allow progression (advisory mode)
- `block`: Halt workflow with actionable remediation steps

**Implementation:** `DoctrineGovernancePlugin` reads `doctrine/` artifacts, loads relevant directives, evaluates constraints, returns validation result.

#### 2. RoutingProvider Interface

**Purpose:** Abstract model/tool/agent routing decisions from Spec Kitty core.

**Contract:**
```python
class RoutingProvider(ABC):
    """Pluggable routing strategy for task-to-model assignment."""
    
    @abstractmethod
    def route_task(self, task_context: TaskContext) -> RoutingDecision:
        """Determine which agent, model, and tools to use for a task."""
        pass
    
    @abstractmethod
    def get_fallback_chain(self, primary_model: str) -> list[ModelEndpoint]:
        """Return ordered fallback models if primary unavailable."""
        pass

@dataclass(frozen=True)
class RoutingDecision:
    """Task routing outcome."""
    agent_key: str  # Maps to Spec Kitty agent config key
    agent_profile_path: Optional[Path]  # Doctrine agent profile if available
    model: str  # LLM model identifier
    tool: str  # CLI tool or SDK
    fallback_chain: list[ModelEndpoint]
    routing_rationale: str  # Why this routing decision was made

@dataclass(frozen=True)
class ModelEndpoint:
    """LLM endpoint configuration."""
    model: str
    provider: str  # anthropic | openai | cohere
    endpoint: str
    max_tokens: int
    cost_per_1k_input: float
    cost_per_1k_output: float
```

**Implementation strategies:**

1. **DefaultRoutingProvider**: Simple mapping from agent config YAML
2. **DoctrineRoutingProvider**: Reads agent profiles, applies directives, considers task complexity
3. **CostOptimizedRoutingProvider**: Selects cheapest model meeting task requirements
4. **AvailabilityAwareRoutingProvider**: Queries model availability before selection

**Integration point:** Spec Kitty's orchestrator calls `routing_provider.route_task()` before work package execution.

#### 3. EventBridge Interface

**Purpose:** Normalize workflow transition events for telemetry and governance.

**Contract:**
```python
class EventBridge(ABC):
    """Emit structured events from Spec Kitty lifecycle transitions."""
    
    @abstractmethod
    def emit_lane_transition(self, event: LaneTransitionEvent) -> None:
        """Emit when work package moves between lanes."""
        pass
    
    @abstractmethod
    def emit_validation_event(self, event: ValidationEvent) -> None:
        """Emit when governance validation runs."""
        pass
    
    @abstractmethod
    def emit_execution_event(self, event: ExecutionEvent) -> None:
        """Emit when agent executes work."""
        pass

@dataclass(frozen=True)
class LaneTransitionEvent:
    """Work package lane change."""
    timestamp: datetime
    work_package_id: str
    from_lane: str
    to_lane: str
    agent: Optional[str]
    commit_sha: Optional[str]

@dataclass(frozen=True)
class ValidationEvent:
    """Governance check result."""
    timestamp: datetime
    validation_type: str  # pre_plan | pre_implement | pre_review | pre_accept
    status: ValidationStatus
    directive_refs: list[int]
    duration_ms: int

@dataclass(frozen=True)
class ExecutionEvent:
    """Agent work execution."""
    timestamp: datetime
    work_package_id: str
    agent: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    duration_ms: int
    success: bool
    error: Optional[str]
```

**Consumers:**
- Telemetry Store (JSONL append-only log)
- Dashboard (real-time UI updates)
- Cost tracker (budget enforcement)
- Governance reporter (compliance metrics)

**Implementation:** Spec Kitty orchestrator calls `event_bridge.emit_*()` at key workflow points. EventBridge fan-out to registered listeners.

---

## Architecture Layers (Detailed)

### Layer 1: Governance Plugin

**Components:**
- `doctrine/` (git subtree at project root)
- `.doctrine-config/` (project-local overrides)
- `DoctrineGovernancePlugin` implementation

**Responsibilities:**
- Load doctrine stack on demand (lazy loading to minimize token cost)
- Evaluate directives against work package state
- Return pass/warn/block decisions with actionable remediation
- Provide governance telemetry (which directives applied, compliance rate)

**Precedence hierarchy (when Doctrine enabled):**
1. Constitution (project-level principles) — authoritative for project-specific rules
2. Doctrine Guidelines (enduring values) — framework defaults
3. Doctrine Directives (explicit constraints) — must-follow unless Constitution overrides
4. Mission guidance (workflow context) — domain-specific behavior
5. Doctrine Tactics/Templates (execution patterns) — how-to guidance

⚠️ **Assumption:** Constitution includes precedence declaration block generated by `spec-kitty init --doctrine`.

**Token budget optimization:**
- Load only directives relevant to current phase (`pre_plan` → load spec/planning directives)
- Cache loaded directives for session duration
- Provide `--skip-governance` flag for fast iteration when needed

### Layer 2: Specification Domain

**Components:**
- `kitty-specs/` (work packages, specs, plans, tasks)
- `missions/` (software-dev, research, documentation adapters)
- Domain model from ADR-045

**Responsibilities:**
- Define work packages with acceptance criteria
- Decompose features into implementable tasks
- Map domain context (mission) to workflow phases
- Validate spec/plan/task structure

**Integration with Doctrine:**
- Work packages reference applicable directives in frontmatter
- Domain model `Specification` and `Feature` dataclasses map to Spec Kitty specs
- Mission adapters load approach-specific context from `doctrine/approaches/`

**Migration strategy for existing domain model:**
- `src/domain/specifications/` (existing) maps to Spec Kitty's spec artifacts
- No code changes needed — domain model already compatible
- Add optional `doctrine_directives: list[int]` field to `Specification` dataclass

### Layer 3: Orchestration

**Components:**
- `src/specify_cli/orchestrator/` (multi-agent coordinator)
- `src/specify_cli/core/worktree.py` (git worktree isolation)
- `src/specify_cli/core/dependency_graph.py` (task scheduling)
- `EventBridge` integration points

**Responsibilities:**
- Execute workflow lifecycle (spec → plan → ... → merge)
- Coordinate parallel agent work with worktree isolation
- Enforce dependency ordering (tasks → implement only after all dependencies done)
- Emit lifecycle events via EventBridge

**Changes required:**
1. **Governance hook integration** (16h):
   ```python
   # In orchestrator before phase transition
   if governance_plugin:
       result = governance_plugin.validate_pre_plan(spec_context)
       if result.status == ValidationStatus.BLOCK:
           raise GovernanceBlockError(result.reasons, result.directive_refs)
   ```

2. **Event emission** (12h):
   ```python
   # After lane transition
   event_bridge.emit_lane_transition(
       LaneTransitionEvent(
           timestamp=now(),
           work_package_id=wp.id,
           from_lane=old_lane,
           to_lane=new_lane,
           agent=wp.assigned_agent,
           commit_sha=wp.commit
       )
   )
   ```

3. **Routing provider integration** (8h):
   ```python
   # Before agent invocation
   routing = routing_provider.route_task(task_context)
   agent_context = load_agent_context(routing.agent_key)
   if routing.agent_profile_path:
       agent_context.merge(load_doctrine_profile(routing.agent_profile_path))
   ```

### Layer 4: Routing

**Components:**
- `src/llm_service/routing.py` (existing stub)
- `RoutingProvider` implementations
- Agent profile loader

**Responsibilities:**
- Map tasks to appropriate models based on complexity, cost, availability
- Load agent profiles (Spec Kitty config + Doctrine profiles)
- Provide fallback chains for resilience
- Record routing decisions for telemetry

**Implementation priority:**

**Phase 1** (16h): `DefaultRoutingProvider`
- Read `config.yaml` agent mappings
- Return hardcoded model assignments
- No fallback chain
- Sufficient for initial integration

**Phase 2** (32h): `DoctrineRoutingProvider`
- Parse agent profiles from `doctrine/agents/`
- Match task characteristics to agent capabilities
- Apply directive constraints (e.g., "use gpt-4 for architecture tasks")
- Generate fallback chains based on model tier

**Phase 3** (40h): Advanced routing
- Cost-aware routing with budget constraints
- Availability checks before assignment
- Load-balancing across rate-limited models
- Routing metrics dashboard

### Layer 5: Execution

**Components:**
- `src/llm_service/adapters/` (vendor adapters)
- `src/llm_service/telemetry/` (execution telemetry)
- Artifact capture (worktree outputs)

**Responsibilities:**
- Execute LLM calls via vendor SDKs or CLI tools
- Capture stdout/stderr, artifacts, and exit codes
- Record token usage and cost
- Emit execution events

**Critical gaps to build:**

1. **Telemetry Store** (24h):
   ```python
   class TelemetryStore:
       """Append-only event log with SQLite materialized views."""
       
       def append_event(self, event: Event) -> None:
           """Append to JSONL log and update materialized views."""
           
       def query_costs(self, filters: CostQuery) -> CostReport:
           """Query aggregated costs from materialized view."""
           
       def query_executions(self, filters: ExecutionQuery) -> list[ExecutionEvent]:
           """Query execution history."""
   ```
   
   - JSONL append-only log at `telemetry.jsonl`
   - SQLite materialized views at `telemetry.db`
   - Indexes on `timestamp`, `agent`, `work_package_id`, `model`

2. **Vendor Adapters** (32h):
   ```python
   class VendorAdapter(ABC):
       """Abstract LLM vendor integration."""
       
       @abstractmethod
       def execute(self, prompt: str, model: str, config: dict) -> ExecutionResult:
           """Execute LLM call and capture telemetry."""
   ```
   
   Implementations:
   - `AnthropicAdapter` (Claude API)
   - `OpenAIAdapter` (GPT-4, GPT-3.5)
   - `CLIAdapter` (Shell out to vendor CLI tools)

3. **Budget Enforcer** (16h):
   ```python
   class BudgetEnforcer:
       """Enforce spending limits."""
       
       def check_budget(self, agent: str, estimated_cost: float) -> BudgetCheck:
           """Return ok | warn | block based on budget state."""
           
       def record_spend(self, agent: str, actual_cost: float) -> None:
           """Update budget tracking."""
   ```

---

## Open Questions — Resolved

### Q1: Where should doctrine artifacts live?

**Decision:** `doctrine/` at project root.

**Rationale:**
- Doctrine is a governance framework that transcends any single tool
- Placing at root signals cross-cutting authority
- Consistent with non-Spec-Kitty projects (no special-casing)
- Git subtree path remains standard
- `.kittify/` contains Spec Kitty-specific config; Doctrine is broader

### Q2: How to handle "two-masters" precedence problem?

**Decision:** Constitution is authoritative; Doctrine extends it.

**Implementation:**
- Constitution template includes precedence declaration:
  ```markdown
  ## Governance Framework
  
  This project follows Agentic Doctrine governance.
  See `doctrine/DOCTRINE_STACK.md` for the behavioral governance framework.
  
  ### Precedence
  1. This Constitution (project-level principles)
  2. Doctrine Guidelines (enduring values)
  3. Doctrine Directives (explicit constraints)
  4. Mission-specific workflow guidance
  5. Doctrine Tactics and Templates (execution)
  
  When Constitution and Doctrine conflict, Constitution wins.
  When in doubt, consult the Constitution first.
  ```

- `DoctrineGovernancePlugin.validate_*()` checks Constitution before applying directives
- Agents receive Constitution + relevant directives (not full stack)

### Q3: How does domain model map to Spec Kitty concepts?

**Mapping:**

| ADR-045 Domain Model | Spec Kitty Concept | Alignment |
|---|---|:---:|
| `Specification` | Spec file (`spec.md`) | ✅ Direct |
| `Feature` | Work Package | ✅ Direct |
| `Batch` | WP with multiple tasks | 🟡 Conceptual |
| `Iteration` | Not present (SK is continuous) | ❌ Gap |
| `Cycle` | Mission phases | 🟡 Related |
| `AgentProfile` | Agent config key + profile file | ✅ Bridged |
| `Directive` | Referenced in WP frontmatter | ✅ Integrated |

**Inverse mapping (Spec Kitty → Doctrine):**

| Spec Kitty Concept | ADR-045 Domain Model | Alignment | Notes |
|---|---|:---:|---|
| Feature Spec (`spec.md`) | `Specification` | ✅ Direct | Spec Kitty specs are change deltas; Doctrine specs are persistent |
| Work Package (WP) | `Feature` | ✅ Direct | WP is independently deliverable; Feature is a capability unit |
| Lane (`planned` → `done`) | Task lifecycle (`new` → `done`) | 🟡 Related | Different state names, same progression concept (see crosswalk below) |
| Mission | No direct equivalent | ❌ Gap | Doctrine uses Approaches + Directives, not domain-scoped mission profiles |
| Constitution | Guidelines (Layer 1) | 🟡 Conceptual | Constitution is a single document; Guidelines is a layered stack |
| Worktree / Workspace | Run Container (ADR-048) | ✅ Direct | Both isolate work execution; worktrees are the implementation of Run Containers |
| Agent config key | `AgentProfile` | ✅ Bridged | SK flat key maps to Doctrine rich profile via `doctrine_profiles` config |
| Merge Preflight | Governance Validator | 🟡 Related | SK validates merge readiness; Doctrine validates behavioral compliance |
| Slash Commands | Shorthands / Tactics | 🟡 Related | Both provide agent-facing command vocabulary at different abstraction levels |
| Dashboard / Scanner | Query Service | 🟡 Related | SK has diagnostics focus; Doctrine design targets CQRS read models |
| Event Log | Telemetry Store (JSONL) | ❌ Gap | SK concept exists but implementation is thin; Doctrine design is unbuilt |

⚠️ **On `Iteration` vs `Cycle`:** These terms are related but not synonymous in Doctrine usage. *Iteration* refers to a discrete execution batch (planning → agent work → review), while *Cycle* refers to a complete structured workflow (e.g., TDD RED→GREEN→REFACTOR, or the Six-Phase SDD Cycle). Spec Kitty has neither concept explicitly — its lifecycle is continuous lane progression per WP, not batch-grouped.

**Actions:**
- Extend `Specification` dataclass with optional `doctrine_directives: list[int]`
- Map `Feature` to WP metadata (no code change needed)
- `Batch` concept unused (SK WPs are already batch-like)
- `Iteration`/`Cycle` remain Doctrine-specific (not forced into SK)
- Add Mission → Approach/Directive crosswalk in Phase 2 adapter layer

### Q4: Token budget impact?

**Measurement needed:** Empirical testing in Phase 2.

**Mitigation strategies:**
1. **Lazy loading**: Load only directives for current phase
   - Pre-plan: Load ~3 directives (~2K tokens)
   - Pre-implement: Load ~5 directives (~4K tokens)
   - Pre-review: Load ~4 directives (~3K tokens)
   
2. **Directive summarization**: Provide one-sentence summaries for quick checks
   ```yaml
   directive_summary:
     17: "Follow TDD: write tests before implementation"
     18: "Document decisions in ADR format"
   ```

3. **Session caching**: Load once per session, reuse for all WPs

4. **Skip flag**: `--skip-governance` for tight iteration cycles

**Estimated token budget:**
- Constitution: ~1K tokens
- Relevant directives: ~4K tokens per phase
- Agent profile: ~1K tokens
- Total governance overhead: **~6K tokens** (vs. 200K context window = 3%)

---

## Migration Strategy

### Existing `src/framework/` Code

**Status:** Partial overlap with Spec Kitty functionality.

**Migration plan:**

| Component | Decision | Rationale |
|---|---|---|
| `src/framework/config/` | **Deprecate** | Spec Kitty config management is superior |
| `src/framework/context/` | **Extend** | Context loaders useful for loading doctrine artifacts |
| `src/framework/orchestration/` | **Absorb into SK extensions** | SK orchestrator is more mature; migrate concepts |
| `src/framework/schemas/` | **Keep** | Domain model validation still needed |

**Actions:**
1. Tag current `src/framework/` as `v0.9-pre-kitty` (backup)
2. Migrate `context/loaders/` to `src/integrations/doctrine/loaders/`
3. Deprecate `orchestration/` (mark as "superseded by Spec Kitty")
4. Keep `schemas/` for domain model validation

### Existing `src/llm_service/` Code

**Status:** Mostly stubs and design sketches.

**Migration plan:**

| Component | Decision | Rationale |
|---|---|---|
| `src/llm_service/routing.py` | **Implement** | Build out `RoutingProvider` interface |
| `src/llm_service/adapters/` | **Implement** | Build vendor adapters per Layer 5 spec |
| `src/llm_service/telemetry/` | **Implement** | Highest-priority gap (Phase 1) |
| `src/llm_service/dashboard/` | **Extend SK dashboard** | SK has better UI foundation |
| `src/llm_service/config/` | **Merge into SK config** | Avoid dual config systems |

**Actions:**
1. Implement `TelemetryStore` as standalone library (no SK dependency)
2. Implement `RoutingProvider` interface and default implementation
3. Build `VendorAdapter` ABC and Claude/OpenAI implementations
4. Extend SK dashboard with cost/telemetry views

### Existing `doctrine/` Stack

**Status:** Mature and stable.

**Migration plan:** **No changes needed.**

**Integration approach:**
1. Distribute via git subtree (existing mechanism)
2. Projects run `git subtree add --prefix=doctrine/ <doctrine-repo> main`
3. `.doctrine-config/` for local overrides (existing pattern)
4. Spec Kitty Constitution references doctrine via template

**Versioning:**
- Doctrine versioned independently (semantic versioning)
- Projects pin to specific doctrine version via subtree commit
- Updates via `git subtree pull`

---

## Key Decisions

### Decision 1: Spec Kitty as Primary, Doctrine as Plugin

**Alternatives considered:**
- **A. Doctrine as SK mission type**: Rejected (abstraction mismatch, distorts both systems)
- **B. Doctrine as file-based plugin**: Rejected (fragile, no enforcement)
- **C. Doctrine as external dependency** ✅ **Selected**
- **D. Bidirectional integration**: Deferred (premature; Phase 4 target)

**Trade-offs accepted:**
- ✅ Preserves both systems' independence
- ✅ Minimal code changes required
- ✅ Leverages existing git subtree distribution
- ❌ Not as "native" as built-in integration
- ❌ Requires manual setup (until `--doctrine` flag implemented)

### Decision 2: Layer Architecture (5 layers)

**Rationale:** Separation of concerns at different abstraction levels.

**Trade-offs:**
- ✅ Clear boundaries between governance, orchestration, routing, execution
- ✅ Easier to test (mock layer interfaces)
- ✅ Enables swapping implementations (e.g., different routing strategies)
- ❌ More boilerplate (interface definitions, adapter code)
- ❌ Learning curve for contributors

### Decision 3: Governance as Advisory First, Blocking Later

**Rationale:** Reduce rollout risk; gather real-world usage data.

**Phasing:**
- **Phase 1-2**: `warn` status only (log governance violations, don't block)
- **Phase 3**: Opt-in `block` mode (`--enforce-governance` flag)
- **Phase 4**: Block mode default (opt-out via `--skip-governance`)

**Trade-offs:**
- ✅ Safe rollout path
- ✅ Time to validate directive applicability
- ❌ Delayed enforcement value
- ❌ Risk of teams ignoring warnings

### Decision 4: Telemetry as Standalone Library

**Rationale:** Largest gap, benefits both systems.

**Trade-offs:**
- ✅ Reusable across Spec Kitty and Doctrine framework
- ✅ Can be developed in parallel with integration work
- ✅ No dependency on Spec Kitty specifics
- ❌ Additional library to maintain
- ❌ Must define stable API upfront

### Decision 5: Routing Provider Interface

**Alternatives considered:**
- **A. Hard-code routing in SK orchestrator**: Rejected (vendor lock-in)
- **B. Provider interface** ✅ **Selected**
- **C. External routing service**: Rejected (over-engineering for current scale)

**Trade-offs:**
- ✅ Extensible (add new providers without core changes)
- ✅ Testable (mock provider for tests)
- ❌ Additional abstraction complexity
- ❌ Requires all routing logic to fit interface

---

## Acceptance Criteria

### AC-1: Doctrine Optional and Backward Compatible

**Testable statements:**
- [ ] `spec-kitty init` works without `--doctrine` flag (no doctrine references)
- [ ] Existing Spec Kitty projects work unchanged with new codebase
- [ ] `--skip-governance` flag bypasses all doctrine checks
- [ ] No doctrine artifacts → no governance validation runs

### AC-2: Governance Lifecycle Hooks

**Testable statements:**
- [ ] `DoctrineGovernancePlugin.validate_pre_plan()` called before planning phase
- [ ] `validate_pre_implement()` called before work package execution
- [ ] `validate_pre_review()` called before review lane transition
- [ ] `validate_pre_accept()` called before accept command
- [ ] Validation results include `status`, `reasons`, `directive_refs`, `suggested_actions`

### AC-3: Routing Provider Swappable

**Testable statements:**
- [ ] `DefaultRoutingProvider` works with zero configuration
- [ ] `DoctrineRoutingProvider` works when `doctrine/agents/` present
- [ ] Custom routing provider can be registered via config
- [ ] Routing decision includes agent key, model, tool, fallback chain
- [ ] No hardcoded vendor strings in orchestrator core

### AC-4: Event Bridge Functional

**Testable statements:**
- [ ] Lane transitions emit `LaneTransitionEvent`
- [ ] Governance checks emit `ValidationEvent`
- [ ] Agent executions emit `ExecutionEvent`
- [ ] Multiple listeners can register for events
- [ ] Events serializable to JSONL

### AC-5: Telemetry Store Operational

**Testable statements:**
- [ ] Events append to `telemetry.jsonl` without loss
- [ ] SQLite materialized views update on event append
- [ ] Cost queries return aggregated spend by agent/model/timeframe
- [ ] Execution queries return filtered event history
- [ ] Telemetry store handles concurrent writes

### AC-6: Token Budget Stays Under 10% of Context Window

**Testable statements:**
- [ ] Constitution + governance context < 20K tokens (10% of 200K window)
- [ ] Lazy loading reduces per-phase overhead to <6K tokens
- [ ] Session caching prevents redundant directive loading
- [ ] Directive summaries available for quick checks

### AC-7: Domain Model Compatibility

**Testable statements:**
- [ ] `Specification` dataclass maps to Spec Kitty spec files
- [ ] `AgentProfile` dataclass loads from `doctrine/agents/`
- [ ] `Directive` dataclass loads from `doctrine/directives/`
- [ ] Domain objects include `source_file` traceability
- [ ] No circular dependencies between domain model and SK core

### AC-8: Migration Non-Disruptive

**Testable statements:**
- [ ] Existing `src/framework/` code marked deprecated with migration guide
- [ ] `src/llm_service/` stubs replaced with functional implementations
- [ ] `doctrine/` unchanged (zero breaking changes)
- [ ] Doctrine version pinned via git subtree commit
- [ ] Rollback path documented and tested

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2, 56h)

**Goal:** Build standalone telemetry library and define interfaces.

**Deliverables:**
1. **TelemetryStore** (24h)
   - JSONL append-only log
   - SQLite materialized views (costs, executions)
   - Query API
   - Unit tests (95% coverage)

2. **Interface definitions** (16h)
   - `GovernancePlugin` ABC
   - `RoutingProvider` ABC
   - `EventBridge` ABC
   - Event dataclasses
   - Documentation with examples

3. **Domain model extensions** (16h)
   - Add `doctrine_directives` to `Specification`
   - Implement `AgentProfile.from_file()`
   - Implement `Directive.from_file()`
   - Update ADR-045 with changes

**Success criteria:**
- [ ] Telemetry store passes acceptance tests
- [ ] Interfaces documented and approved
- [ ] Domain model loads doctrine artifacts

### Phase 2: Integration (Weeks 3-5, 80h)

**Goal:** Integrate interfaces into Spec Kitty orchestrator.

**Deliverables:**
1. **Orchestrator changes** (32h)
   - Add governance hook callsites
   - Add event emission callsites
   - Add routing provider integration
   - Backward compatibility tests

2. **DoctrineGovernancePlugin** (24h)
   - Implement `validate_pre_*()` methods
   - Load doctrine artifacts on demand
   - Return validation results
   - Unit tests

3. **DefaultRoutingProvider** (16h)
   - Read agent config YAML
   - Return routing decisions
   - Unit tests

4. **EventBridge implementation** (8h)
   - Fan-out to telemetry store
   - Register/unregister listeners
   - Unit tests

**Success criteria:**
- [ ] Governance checks run at correct lifecycle points
- [ ] Events flow to telemetry store
- [ ] Routing provider selects agents
- [ ] Backward compatibility maintained

### Phase 3: Vendor Adapters (Weeks 6-7, 64h)

**Goal:** Build LLM vendor execution layer.

**Deliverables:**
1. **VendorAdapter ABC** (8h)
   - Interface definition
   - Telemetry capture hooks
   - Error handling

2. **AnthropicAdapter** (24h)
   - Claude API integration
   - Token/cost tracking
   - Retry logic
   - Tests with mocked API

3. **OpenAIAdapter** (24h)
   - GPT-4/3.5 integration
   - Token/cost tracking
   - Retry logic
   - Tests with mocked API

4. **CLIAdapter** (8h)
   - Shell out to vendor tools
   - Capture stdout/stderr
   - Parse responses
   - Tests

**Success criteria:**
- [ ] Adapters execute LLM calls
- [ ] Telemetry captured accurately
- [ ] Errors handled gracefully
- [ ] Fallback chains work

### Phase 4: Advanced Routing (Weeks 8-9, 64h)

**Goal:** Implement Doctrine-aware routing and budget enforcement.

**Deliverables:**
1. **DoctrineRoutingProvider** (32h)
   - Parse agent profiles
   - Match tasks to capabilities
   - Apply directive constraints
   - Generate fallback chains
   - Tests

2. **BudgetEnforcer** (16h)
   - Track spend by agent/project
   - Warn at 80% budget
   - Block at 100% budget
   - Tests

3. **Routing metrics** (16h)
   - Dashboard view for routing decisions
   - Cost projections
   - Model availability status
   - Tests

**Success criteria:**
- [ ] Doctrine routing selects appropriate models
- [ ] Budget enforcement prevents overspend
- [ ] Routing decisions visible in dashboard

### Phase 5: Polish & Documentation (Week 10, 40h)

**Goal:** Production readiness and user onboarding.

**Deliverables:**
1. **Documentation** (16h)
   - Integration guide
   - Constitution template with precedence
   - Directive reference for SK workflows
   - Troubleshooting guide

2. **CLI enhancements** (16h)
   - `spec-kitty init --doctrine` flag
   - `spec-kitty governance status` command
   - `spec-kitty routing info` command
   - Help text updates

3. **Performance optimization** (8h)
   - Profile governance loading
   - Optimize directive caching
   - Benchmark token usage
   - Document findings

**Success criteria:**
- [ ] Users can integrate Doctrine in <15 minutes
- [ ] Documentation complete and accurate
- [ ] Performance acceptable (governance overhead <500ms)

---

## Risks and Mitigations

| Risk | Severity | Likelihood | Mitigation |
|---|:---:|:---:|---|
| **Constitution-Directive conflicts** | High | Medium | Precedence declaration in Constitution; plugin checks Constitution first |
| **Token budget exceeded** | Medium | High | Lazy loading, caching, summaries; empirical measurement in Phase 2 |
| **Routing provider inadequate** | Medium | Medium | Start with simple default provider; iterate based on real usage |
| **Telemetry performance bottleneck** | Medium | Low | Async append to JSONL; batch SQLite updates; benchmark early |
| **Spec Kitty maintainer rejection** | Low | Medium | Option C requires zero SK changes; all work in extensions/plugins |
| **Agent confusion from dual contexts** | Medium | Medium | Constitution precedence; phase-specific directive loading; clear documentation |
| **Budget enforcement too strict** | Low | Medium | Warn mode first; configurable thresholds; override flag |
| **Migration breaks existing workflows** | High | Low | Comprehensive backward compatibility tests; rollback plan |

---

## Success Metrics

### Technical Metrics

- **Test coverage**: ≥90% for new code
- **Governance check latency**: <500ms per validation
- **Telemetry overhead**: <50ms per event
- **Token budget**: <10% of context window
- **Backward compatibility**: 100% of existing SK commands work unchanged

### User Experience Metrics

- **Time to integrate Doctrine**: <15 minutes
- **Governance false positive rate**: <5%
- **Routing accuracy**: >90% (agent has required capabilities)
- **Cost tracking accuracy**: ±2% of actual spend

### Business Metrics

- **Adoption rate**: >30% of SK users enable Doctrine within 3 months
- **Governance compliance**: >80% of work packages pass all checks
- **Cost reduction**: >15% from optimized routing (vs. always using GPT-4)

---

## References

### Internal Documents

- `work/kitty/SUMMARY.md` — Analysis summary
- `work/kitty/proposal/spec-kitty-governance-doctrine-extension-proposal.md` — Initial proposal
- `work/kitty/proposal/VISION.md` — Vision statement
- `work/kitty/analysis/2026-02-14-doctrine-spec-kitty-integration-analysis.md` — Integration feasibility
- `work/kitty/analysis/2026-02-14-control-plane-spec-kitty-coverage.md` — Infrastructure gaps
- `work/kitty/analysis/2026-02-14-evaluation-doctrine-governance-extension.md` — Evaluation decision
- `work/kitty/analysis/spec-kitty-vs-quickstart-terminology-comparison.md` — Terminology crosswalk
- `docs/architecture/adrs/ADR-045-doctrine-concept-domain-model.md` — Domain model
- `docs/architecture/adrs/ADR-046-domain-module-refactoring.md` — Bounded contexts
- `docs/architecture/adrs/ADR-048-run-container-concept.md` — Run container model

### External References

- Spec Kitty repository: `https://github.com/Priivacy-ai/spec-kitty`
- Spec Kitty source: `/media/stijnd/DATA/development/projects/forks/spec-kitty/src/specify_cli/`

---

## Appendix A: Terminology Crosswalk

| Doctrine Term | Spec Kitty Term | Notes |
|---|---|---|
| Specification | Spec file (`spec.md`) | Direct mapping |
| Feature | Work Package | Direct mapping |
| Task | Task in WP | Direct mapping |
| Agent Profile | Agent config key + profile file | Bridged via routing provider |
| Directive | Referenced in WP frontmatter | Loaded on demand |
| Tactic | Mission phase guidance | Related but different granularity |
| Approach | Mission philosophy | Conceptual alignment |
| Collaboration task | WP lane state | Parallel coordination (use SK lanes for feature work) |
| Batch | WP with multiple tasks | Conceptual overlap |
| Iteration | Not present | Doctrine-specific (not forced into SK) |
| Cycle | Mission phases | Related pattern |
| Work log | Activity log in WP frontmatter | Different format, same purpose |

---

## Appendix B: Sample Constitution with Precedence

```markdown
# Constitution: [Project Name]

## Governance Framework

This project follows Agentic Doctrine governance.
See `doctrine/DOCTRINE_STACK.md` for the behavioral governance framework.

### Precedence

When multiple governance sources apply, resolve conflicts in this order:

1. **This Constitution** — Project-level principles and overrides
2. **Doctrine Guidelines** — Enduring values from the framework
3. **Doctrine Directives** — Explicit constraints and requirements
4. **Mission-specific guidance** — Workflow context from active mission
5. **Doctrine Tactics and Templates** — Execution patterns and output contracts

**When Constitution and Doctrine conflict, Constitution wins.**

**When in doubt, consult the Constitution first, then relevant directives.**

### Relevant Directives

This project prioritizes:
- **Directive 016**: Acceptance Test-Driven Development (ATDD)
- **Directive 017**: Test-Driven Development (TDD)
- **Directive 018**: Traceable Decisions (ADRs)
- **Directive 020**: Lenient Adherence (stylistic flexibility)
- **Directive 026**: Commit Protocol (conventional commits)
- **Directive 034**: Spec-Driven Development (SDD)

## Project Principles

[... project-specific rules ...]
```

---

**Status:** Ready for review  
**Next Actions:**
1. Human review of architecture decisions
2. Approval to proceed with Phase 1 implementation
3. Create Phase 1 work packages in Spec Kitty format
