# Execution Roadmap: Spec Kitty × Doctrine Unification

**Version:** 1.0.0  
**Date:** 2026-02-14  
**Owner:** Planning Petra  
**Status:** Proposed  
**Mode:** `/analysis-mode`

---

## Strategic Context

**Integration Direction:** Spec Kitty as primary platform, Doctrine as governance plugin, LLM service concerns as standalone libraries or SK extensions.

**Key Architectural Principles:**
- Spec Kitty remains authoritative for workflow/lifecycle orchestration
- Doctrine provides behavioral governance through optional extension
- Both systems continue to work independently (backward compatibility)
- Minimum 80% test coverage on all new code (TDD/ATDD required)
- Spec Kitty fork at `/media/stijnd/DATA/development/projects/forks/spec-kitty` is READ-ONLY (upstream collaboration needed for code changes)

**Foundation Documents:**
- `work/kitty/SUMMARY.md` — Analysis summary with 4-phase roadmap
- `work/kitty/proposal/spec-kitty-governance-doctrine-extension-proposal.md` — Architectural proposal
- `work/kitty/analysis/2026-02-14-control-plane-spec-kitty-coverage.md` — Gap analysis (~25% coverage overall)
- `docs/architecture/assessments/platform_next_steps.md` — Existing platform roadmap (must align)

---

## Phase Overview

| Phase | Goal | Duration | Dependencies | Value Delivered |
|-------|------|----------|--------------|-----------------|
| **0** | Foundation & Analysis | — | None | ✅ **COMPLETE** — Analysis, architecture decisions, proposal documents |
| **1** | Telemetry & Observability Library | M | Phase 0 | Standalone event log, cost tracking, SQLite materialized views usable by both systems |
| **2** | Governance Plugin Extension | L | Phase 0 | Doctrine integration into Spec Kitty via optional plugin with lifecycle hooks |
| **3** | Model Routing & Agent Bridge | L | Phase 1, Phase 2 | Pluggable routing provider, agent profile mapping, LLM service integration |
| **4** | Real-Time Dashboard & Query Service | M | Phase 1, Phase 3 | SocketIO-based dashboard with cost metrics, task state, artifact links |
| **5** | Error Reporting & CI Integration | M | Phase 1 | CI/CD error extraction, agent-friendly parsing, fix cycle automation |
| **6** | Documentation, Migration & Release | S | All prior phases | User guides, migration tooling, release pipeline, upstream collaboration plan |

**Total Effort:** ~4.5–6 person-months spread across 6 phases  
**Critical Path:** Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 6 (minimum to deliver working integration)

---

## Phase 0: Foundation & Analysis ✅ **COMPLETE**

**Goal:** Establish architectural direction, analyze integration options, document strategic decisions.

### Deliverables
- ✅ Integration feasibility analysis (`2026-02-14-doctrine-spec-kitty-integration-analysis.md`)
- ✅ Infrastructure coverage gap analysis (`2026-02-14-control-plane-spec-kitty-coverage.md`)
- ✅ Integration proposal document (`spec-kitty-governance-doctrine-extension-proposal.md`)
- ✅ Executive summary and vision documents
- ✅ Terminology mapping and glossary (`work/kitty/glossary/*`)
- ✅ PlantUML architecture diagrams (`spec-kitty-doctrine-layered-target-architecture.puml`)

### Agent Assignments
- ✅ Architect Alphonso: Architecture analysis, ADR drafting, integration options evaluation
- ✅ Curator Claire: Documentation organization, glossary creation, summary writing
- ✅ Diagram Daisy: C4 layered integration diagrams, architecture visualization

### Success Criteria
- ✅ Strategic direction confirmed: Spec Kitty-centric integration
- ✅ Gap analysis quantified: ~25% infrastructure coverage
- ✅ Integration approach selected: Option C (Doctrine as external dependency)
- ✅ Precedence contract defined
- ✅ Risk register established

### Dependencies
- None (foundation phase)

### Risk Factors
- **RESOLVED** — Initial ambiguity about architectural ownership → Clarified through analysis

---

## Phase 1: Telemetry & Observability Library

**Goal:** Build standalone telemetry infrastructure that both Spec Kitty and Doctrine can consume independently.

**Effort:** M (Medium — 3–4 weeks)  
**Value:** Addresses largest gap (~75% of observability concerns), enables CQRS read path, provides cost tracking foundation

### Deliverables

#### Code Artifacts
1. **`src/framework/telemetry/`** — Standalone telemetry library module
   - `event_log.py` — Append-only JSONL event writer with structured schema
   - `event_store.py` — SQLite materialized view layer for queries
   - `cost_tracker.py` — LLM API cost aggregation (token count → cost mapping)
   - `metrics_collector.py` — Aggregation engine (per-agent, per-task, per-day rollups)
   - `query_interface.py` — Query API for dashboards and agents
   - `schema.py` — Event schema definitions (TaskStarted, TaskCompleted, LLMInvocation, etc.)
   - `worklog_emitter.py` — EventBridge consumer that auto-generates Directive 014 work log entries from lane transitions and validation events

2. **`ops/config/telemetry.yaml`** — Configuration template
   - Storage paths (JSONL log location, SQLite DB path)
   - Retention policies (log rotation, archival)
   - Cost tracking settings (pricing tables, budget thresholds)

3. **`validation/test_telemetry_*.py`** — Comprehensive test suite
   - Event emission and persistence tests (Quad-A pattern)
   - Cost calculation accuracy tests (per Directive 017)
   - Query interface contract tests
   - Thread safety and concurrency tests (async event emission)

#### Documentation
4. **`src/framework/telemetry/README.md`** — Library usage guide
   - Integration examples for both Spec Kitty and Doctrine
   - Event schema documentation
   - Query API reference

5. **ADR-022: Telemetry Architecture** — Architecture decision record
   - Design rationale (append-only log, SQLite read models)
   - Schema versioning strategy
   - Performance considerations

### Agent Assignments

| Agent | Tasks | Artifacts |
|-------|-------|-----------|
| **Backend Benny** | Implement core telemetry library, event log, SQLite store | `telemetry/*.py` (80% of code) |
| **Python Pedro** | Write comprehensive test suite (TDD approach), 80%+ coverage | `validation/test_telemetry_*.py` |
| **Architect Alphonso** | Design event schema, write ADR-022, define query interface | ADR-022, schema design doc |
| **DevOps Danny** | Configure CI pipeline for telemetry tests, set up test fixtures | CI config, test data generators |
| **Curator Claire** | Write library documentation, integration guide, API reference | `telemetry/README.md`, integration examples |

### Dependencies
- **Upstream:** Phase 0 (architectural decisions)
- **Downstream:** Phase 3 (cost tracking), Phase 4 (dashboard queries), Phase 5 (error telemetry)

### Success Criteria
- ✅ Event emission: <10ms p99 latency for append-only writes
- ✅ Query interface: <100ms response time for standard queries (task status, cost rollup)
- ✅ Test coverage: ≥80% line coverage, all Quad-A structured
- ✅ Integration examples: Both Spec Kitty and Doctrine can emit/query events
- ✅ Schema versioned: Backward-compatible event schema evolution strategy
- ✅ CI validation: Telemetry tests pass in CI pipeline

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Performance bottleneck in SQLite queries** | Medium | High | Use indexed materialized views, benchmark early, add Redis cache if needed |
| **Schema evolution breaks existing consumers** | Medium | High | Implement schema versioning (semver), test migration paths |
| **Thread-safety issues in concurrent event emission** | Low | Medium | Use thread-safe queue, test with concurrent writers |
| **Cost calculation accuracy (LLM pricing changes)** | High | Medium | Externalize pricing table, validate against vendor APIs monthly |
| **JSONL log size growth** | Medium | Medium | Implement rotation/archival policy, compress old logs |

### Work Package Structure
```
work/kitty/phase-1-telemetry/
├── WP-001-telemetry-core.md         # Event log + SQLite store
├── WP-002-cost-tracker.md           # Cost calculation engine
├── WP-003-query-interface.md        # Query API
├── WP-004-telemetry-tests.md        # Test suite (TDD)
└── WP-005-telemetry-docs.md         # Documentation
```

---

## Phase 2: Governance Plugin Extension

**Goal:** Integrate Doctrine as optional governance layer for Spec Kitty without breaking existing workflows.

**Effort:** L (Large — 4–6 weeks)  
**Value:** Adds governance rigor, enables layered policy precedence, preserves backward compatibility

### Deliverables

#### Spec Kitty Extensions (in Doctrine repo — cannot modify upstream fork)
1. **`src/framework/governance/`** — Governance plugin module
   - `doctrine_loader.py` — Load Doctrine stack + `.doctrine-config/` overrides
   - `policy_checker.py` — Lifecycle hook executor (pre_plan, pre_tasks, pre_implement, etc.)
   - `precedence_resolver.py` — Resolve conflicts between constitution, guidelines, directives
   - `policy_result.py` — Normalized pass/warn/block output with directive references

2. **`src/framework/governance/hooks/`** — Lifecycle hook implementations
   - `pre_plan_hook.py` — Validate planning readiness (spec completeness, architecture approval)
   - `pre_implement_hook.py` — Check TDD constraints, test-first requirements
   - `pre_merge_hook.py` — Validate test coverage, code review completion

3. **`.doctrine-config/` template** — Project-local override directory (generated on bootstrap)
   - `config.yaml` — Doctrine configuration with path mappings
   - `repository-guidelines.md` — Project-specific governance rules
   - `hooks/` — Custom lifecycle hooks (optional)
   - Constitution ↔ `.doctrine-config/` sync validator (ensures narrative and structured config don't contradict)

**Design note — Unified event spine:** Governance lifecycle hooks share attachment points with the EventBridge (from Phase 1). Every governance validation is itself an event. The `GovernancePlugin.validate_pre_*()` result feeds into `EventBridge.emit_validation_event()`, and a `WorkLogEmitter` consumer (Phase 1) auto-generates Directive 014 entries. Adding new cross-cutting concerns (budget enforcement, audit trail) requires only registering a new EventBridge consumer — no additional orchestrator hook points.

**Design note — Constitution convergence:** SK Constitution and Doctrine `.doctrine-config/` are near-identical concepts (project-scoped governance overlays) in different forms. Phase 2 should treat them as two views of the same governance state — Constitution as human-readable narrative, `.doctrine-config/` as machine-parseable config. A validation check ensures they don't contradict.

4. **`ops/scripts/bootstrap-doctrine.py`** — Setup automation
   - Install/sync Doctrine stack (git subtree or clone)
   - Generate `.doctrine-config/` from template
   - Validate configuration against Spec Kitty project structure

#### Documentation
5. **`docs/integration/spec-kitty-governance-integration.md`** — Integration guide
   - How to enable/disable Doctrine governance
   - Precedence contract explanation
   - Hook customization guide

6. **ADR-023: Governance Plugin Architecture** — Architecture decision record
   - Extension point design
   - Backward compatibility strategy
   - Precedence resolution algorithm

#### Tests
7. **`validation/test_governance_*.py`** — Governance plugin test suite
   - Lifecycle hook execution tests
   - Precedence resolution tests (general/operational guidelines > constitution > directives)
   - Doctrine-enabled vs disabled mode comparison tests
   - Hook output validation (pass/warn/block format)

### Agent Assignments

| Agent | Tasks | Artifacts |
|-------|-------|-----------|
| **Architect Alphonso** | Design extension architecture, precedence contract, write ADR-023 | ADR-023, interface contracts |
| **Backend Benny** | Implement governance plugin, doctrine loader, hook executor | `governance/*.py` (70% of code) |
| **Bootstrap Bill** | Build bootstrap automation, `.doctrine-config/` generator | `bootstrap-doctrine.py`, config templates |
| **Python Pedro** | Write TDD tests for governance plugin, hook validation tests | `test_governance_*.py` (80%+ coverage) |
| **Curator Claire** | Write integration guide, precedence documentation | Integration guide, user docs |
| **DevOps Danny** | Add governance tests to CI, feature flag configuration | CI config, feature flags |

### Dependencies
- **Upstream:** Phase 0 (architectural decisions, proposal)
- **Parallel:** Phase 1 (no hard dependency, but governance hooks can emit telemetry events)
- **Downstream:** Phase 3 (routing policies can reference governance rules), Phase 6 (migration guide)

### Success Criteria
- ✅ Backward compatibility: Spec Kitty works identically with Doctrine disabled
- ✅ Deterministic governance: Same inputs → same pass/warn/block outputs
- ✅ Advisory rollout: Hooks start in warn-only mode, block mode is opt-in
- ✅ Precedence enforcement: Doctrine General/Operational Guidelines immutable; Constitution customizes within bounds
- ✅ WP schema unchanged: No modifications to Spec Kitty's frontmatter schema
- ✅ Test coverage: ≥80% on governance module
- ✅ Bootstrap automation: One-command setup for new projects

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Dual-authority confusion (Constitution vs Doctrine)** | High | High | Explicit precedence contract, command-time policy trace output |
| **Workflow regressions (governance blocks valid work)** | Medium | High | Advisory mode first, gradual rollout, feature flags |
| **Over-coupling to Doctrine internals** | Medium | Medium | Extension consumes stable outputs, not parser internals, version pinning |
| **Bootstrap complexity (config generation errors)** | Low | Medium | Comprehensive validation, dry-run mode, rollback support |
| **Hook performance impact on Spec Kitty commands** | Low | Medium | Async hook execution, timeout constraints, telemetry monitoring |

### Work Package Structure
```
work/kitty/phase-2-governance/
├── WP-006-governance-core.md         # Doctrine loader + policy checker
├── WP-007-lifecycle-hooks.md         # Hook implementations
├── WP-008-precedence-resolver.md     # Conflict resolution
├── WP-009-bootstrap-automation.md    # Setup tooling
├── WP-010-governance-tests.md        # Test suite (TDD)
└── WP-011-integration-docs.md        # User guides
```

---

## Phase 3: Model Routing & Agent Bridge

**Goal:** Enable pluggable model routing with doctrine policy provider while keeping Spec Kitty model-agnostic.

**Effort:** L (Large — 5–6 weeks)  
**Value:** Agent-to-model mapping, fallback chains, cost-aware routing, LLM service integration

### Deliverables

#### Routing Provider Interface (Doctrine repo)
1. **`src/framework/routing/`** — Routing provider module
   - `provider_interface.py` — Abstract routing provider contract
     ```python
     class RoutingProvider(ABC):
         @abstractmethod
         def route_task(self, task_context: TaskContext) -> RoutingDecision:
             pass
     ```
   - `routing_decision.py` — Output contract (agent_key, model, tool, fallback_chain, rationale)
   - `default_provider.py` — Simple default router (uses Spec Kitty agent config.yaml)
   - `doctrine_policy_provider.py` — Doctrine-based router (reads `.doctrine-config/model_router.yaml`)

2. **`src/framework/routing/strategies/`** — Routing strategies
   - `cost_aware_routing.py` — Select cheapest model meeting constraints
   - `capability_routing.py` — Route based on task complexity (context window, tool support)
   - `fallback_chain.py` — Primary model unavailable → automatic failover

3. **`.doctrine-config/model_router.yaml`** — Model routing policy template
   ```yaml
   routing_policies:
     - task_type: code_generation
       preferred_models: [gpt-4o, claude-sonnet-4]
       constraints:
         min_context_window: 16000
         requires_tool_calls: true
       cost_ceiling: 0.05  # per 1K tokens
       fallback_chain: [gpt-4o-mini, codestral]
   ```

4. **`src/llm_service/model_catalog.py`** — Centralized model registry
   - Model IDs, context windows, pricing, capability flags
   - Integration with OpenRouter, OpenCode.ai, direct APIs (OpenAI, Anthropic)
   - Pricing table loader with versioning

#### Agent Profile Bridge
5. **`src/framework/agents/`** — Agent profile integration
   - `profile_parser.py` — Parse Doctrine agent profiles (markdown → AgentProfile dataclass)
   - `config_generator.py` — Generate Spec Kitty `agent/config.yaml` from Doctrine profiles
   - `profile_mapper.py` — Map Doctrine capabilities → Spec Kitty agent settings

#### Tests
6. **`validation/test_routing_*.py`** — Routing provider test suite
   - Provider interface contract tests (substitutability)
   - Routing decision accuracy tests (correct model for task type)
   - Fallback chain execution tests (cascading failure scenarios)
   - Cost calculation integration tests (pricing table accuracy)

7. **`validation/test_agent_bridge_*.py`** — Agent bridge test suite
   - Profile parsing tests (markdown → dataclass)
   - Config generation tests (Doctrine profile → SK config.yaml)
   - Mapping accuracy tests (capability preservation)

#### Documentation
8. **`docs/routing/model-routing-guide.md`** — Routing configuration guide
   - How to define routing policies
   - Model catalog maintenance
   - Fallback chain design patterns

9. **ADR-024: Pluggable Routing Architecture** — Architecture decision record
   - Provider interface rationale
   - Cost-aware routing algorithm
   - Fallback strategy design

### Agent Assignments

| Agent | Tasks | Artifacts |
|-------|-------|-----------|
| **Architect Alphonso** | Design routing provider interface, write ADR-024 | ADR-024, interface contracts |
| **Backend Benny** | Implement routing providers, model catalog, agent bridge | `routing/*.py`, `llm_service/model_catalog.py` (60% of code) |
| **Python Pedro** | Write TDD tests for routing and agent bridge | `test_routing_*.py`, `test_agent_bridge_*.py` (80%+ coverage) |
| **DevOps Danny** | Set up model catalog automation, pricing table sync, CI integration | Pricing table updater, catalog validator, CI config |
| **Curator Claire** | Write routing guide, agent profile mapping documentation | Routing guide, profile migration docs |

### Dependencies
- **Upstream:** Phase 1 (cost tracking for cost-aware routing), Phase 2 (routing policies reference governance rules)
- **Parallel:** Can run in parallel with Phase 2, but integration requires both complete
- **Downstream:** Phase 4 (dashboard shows routing decisions), Phase 6 (migration tooling)

### Success Criteria
- ✅ Pluggable design: Routing provider can be swapped without core command rewrites
- ✅ Backward compatibility: Default provider works with existing Spec Kitty projects
- ✅ Doctrine integration: Policy provider reads `.doctrine-config/model_router.yaml`
- ✅ Fallback resilience: Automatic failover on primary model unavailability
- ✅ Cost accuracy: Pricing table validated against vendor APIs monthly
- ✅ Agent bridge: Doctrine profiles generate valid Spec Kitty config.yaml
- ✅ Test coverage: ≥80% on routing and agent bridge modules

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Model ID inconsistencies across routers (OpenRouter vs direct APIs)** | High | High | Centralized catalog with ID mapping, validation script |
| **Pricing data staleness (vendor changes rates)** | High | Medium | Monthly automated pricing sync, alerting on mismatches |
| **Fallback chain infinite loops** | Low | High | Max retry limit, circuit breaker pattern, telemetry monitoring |
| **Agent profile mapping loss of fidelity** | Medium | Medium | Bidirectional validation (profile → config → profile), manual review |
| **Router availability/latency impact** | Medium | Medium | Local caching, timeout constraints, fallback to default provider |

### Work Package Structure
```
work/kitty/phase-3-routing/
├── WP-012-routing-interface.md       # Provider interface + default implementation
├── WP-013-doctrine-provider.md       # Policy-based router
├── WP-014-model-catalog.md           # Model registry + pricing tables
├── WP-015-agent-bridge.md            # Profile parsing + config generation
├── WP-016-routing-tests.md           # Test suite (TDD)
└── WP-017-routing-docs.md            # Configuration guide
```

---

## Phase 4: Real-Time Dashboard & Query Service

**Goal:** Extend Spec Kitty dashboard with real-time task state, cost metrics, and artifact links.

**Effort:** M (Medium — 3–4 weeks)  
**Value:** Operational visibility, cost monitoring, real-time progress tracking

### Deliverables

#### Dashboard Backend (Doctrine repo)
1. **`src/llm_service/dashboard_service.py`** — SocketIO-based dashboard server
   - Real-time event streaming (task state changes, cost updates)
   - Query endpoints for task status, cost rollups, agent utilization
   - Artifact indexing and linking

2. **`src/llm_service/query_api.py`** — REST API for dashboard queries
   - `/tasks` — Task list with filtering (status, agent, date range)
   - `/costs` — Cost aggregation by agent, task, day, project
   - `/artifacts` — Artifact index with download links
   - `/metrics` — Agent utilization, throughput, success rate

3. **`src/llm_service/dashboard_aggregator.py`** — Aggregation layer
   - Consumes telemetry events (from Phase 1)
   - Generates real-time rollups (per-agent costs, task throughput)
   - Caches frequently accessed queries

#### Dashboard Frontend (Doctrine repo)
4. **`docs-site/src/dashboard/`** — Enhanced dashboard UI
   - Real-time task state visualization (kanban board, timeline)
   - Cost breakdown charts (by agent, by model, over time)
   - Agent utilization heatmap
   - Artifact browser with preview

5. **WebSocket event handlers** — Real-time updates
   - Task state transitions (spec → plan → implement → review → merge)
   - Cost threshold alerts (budget warnings)
   - Error notifications (CI failures, governance blocks)

#### Tests
6. **`validation/test_dashboard_*.py`** — Dashboard test suite
   - SocketIO event streaming tests
   - Query API response validation tests
   - Aggregation accuracy tests (cost rollups, throughput calculations)
   - Real-time update latency tests (<500ms from event to UI)

#### Documentation
7. **`docs/dashboard/dashboard-user-guide.md`** — User guide
   - How to start dashboard server
   - Feature overview (real-time updates, cost monitoring)
   - Configuration options

8. **ADR-025: Real-Time Dashboard Architecture** — Architecture decision record
   - SocketIO vs polling rationale
   - Aggregation strategy (pre-compute vs on-demand)
   - Caching policy

### Agent Assignments

| Agent | Tasks | Artifacts |
|-------|-------|-----------|
| **Backend Benny** | Implement dashboard service, query API, aggregator | `dashboard_service.py`, `query_api.py` (50% of code) |
| **Frontend Fiona** | Build dashboard UI components, WebSocket handlers | Dashboard React components (40% of code) |
| **Python Pedro** | Write backend tests (SocketIO, query API) | `test_dashboard_*.py` (80%+ coverage) |
| **QA Quincy** | Write E2E tests for dashboard features | E2E test scenarios, integration tests |
| **DevOps Danny** | Set up dashboard deployment, configure SocketIO server | Deployment scripts, server config |
| **Curator Claire** | Write user guide, dashboard documentation | User guide, feature docs |

### Dependencies
- **Upstream:** Phase 1 (telemetry events for aggregation), Phase 3 (routing decisions displayed in dashboard)
- **Downstream:** Phase 6 (dashboard integrated into release)

### Success Criteria
- ✅ Real-time updates: <500ms latency from event to UI update
- ✅ Query performance: <200ms response time for standard queries
- ✅ Cost accuracy: Dashboard costs match telemetry store (0% drift)
- ✅ Artifact linking: Click-to-download for all task outputs
- ✅ Multi-project support: Dashboard can monitor multiple Spec Kitty projects
- ✅ Test coverage: ≥80% on dashboard backend, E2E tests for key flows

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **WebSocket connection stability (disconnects, reconnects)** | Medium | Medium | Auto-reconnect logic, missed event replay, connection health checks |
| **Aggregation performance degradation (large projects)** | Medium | High | Pre-computed rollups, query optimization, pagination |
| **UI complexity (information overload)** | Medium | Low | Progressive disclosure, customizable views, drill-down patterns |
| **Multi-project data isolation** | Low | High | Per-project databases, access control, query scoping |
| **Real-time event flood (high-frequency updates)** | Low | Medium | Event batching, rate limiting, subscription filtering |

### Work Package Structure
```
work/kitty/phase-4-dashboard/
├── WP-018-dashboard-backend.md       # SocketIO service + query API
├── WP-019-dashboard-aggregator.md    # Aggregation layer
├── WP-020-dashboard-frontend.md      # UI components
├── WP-021-dashboard-tests.md         # Test suite (backend + E2E)
└── WP-022-dashboard-docs.md          # User guide
```

---

## Phase 5: Error Reporting & CI Integration

**Goal:** Extract CI/CD errors, provide agent-friendly parsing, automate fix cycles.

**Effort:** M (Medium — 3–4 weeks)  
**Value:** Reduce manual error triage, improve agent autonomy, accelerate fix cycles

### Deliverables

#### Error Reporting System (Doctrine repo)
1. **`src/framework/errors/`** — Error reporting module
   - `error_parser.py` — Abstract parser for CI/CD error formats (GitHub Actions, GitLab CI, Jenkins)
   - `github_actions_parser.py` — Parse GHA workflow errors
   - `test_failure_parser.py` — Parse pytest/jest test failures
   - `linter_parser.py` — Parse pylint/eslint/ruff output
   - `error_summarizer.py` — Generate markdown summaries for agents

2. **`src/framework/errors/extractors/`** — Error extractors
   - `artifact_downloader.py` — Download CI logs, test reports from GitHub
   - `error_classifier.py` — Classify errors (syntax, test failure, runtime, configuration)
   - `fix_suggester.py` — Suggest fix strategies based on error type

3. **GitHub Actions integration**
   - `.github/actions/extract-errors/action.yaml` — Reusable error extraction action
   - Posts structured error reports to PR comments
   - Triggers agent fix workflow (optional)

4. **`ops/scripts/error-report-generator.py`** — CLI tool
   - Parse local test/lint output
   - Generate agent-friendly error summaries
   - Upload to telemetry store

#### Tests
5. **`validation/test_errors_*.py`** — Error reporting test suite
   - Parser accuracy tests (various error formats)
   - Classifier correctness tests (error type detection)
   - Summarizer output validation tests (markdown format)
   - E2E tests (GitHub Actions integration)

#### Documentation
6. **`docs/errors/error-reporting-guide.md`** — Error reporting guide
   - How to integrate with CI/CD
   - Error format documentation
   - Fix workflow patterns

7. **ADR-026: Structured Error Reporting** — Architecture decision record
   - Parser extensibility strategy
   - Error classification taxonomy
   - Agent fix workflow design

### Agent Assignments

| Agent | Tasks | Artifacts |
|-------|-------|-----------|
| **Backend Benny** | Implement error parsers, extractors, summarizer | `errors/*.py` (60% of code) |
| **DevOps Danny** | Build GitHub Actions integration, CI automation | GHA action, CI scripts (30% of code) |
| **Python Pedro** | Write TDD tests for parsers, classifiers | `test_errors_*.py` (80%+ coverage) |
| **QA Quincy** | Write E2E tests for CI integration | E2E scenarios, integration tests |
| **Curator Claire** | Write error reporting guide, workflow documentation | Error guide, fix workflow docs |

### Dependencies
- **Upstream:** Phase 1 (error events logged to telemetry), Phase 2 (governance can block on CI failures)
- **Downstream:** Phase 6 (error reporting integrated into release)

### Success Criteria
- ✅ Parser coverage: GitHub Actions, pytest, pylint, eslint, ruff
- ✅ Extraction accuracy: ≥95% correct error classification
- ✅ Summarizer quality: Agents can understand errors without raw logs
- ✅ CI integration: Errors posted to PRs within 2 minutes of failure
- ✅ Fix workflow: Agents can download artifacts, apply fixes, re-run tests
- ✅ Test coverage: ≥80% on error reporting module

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **CI output format changes (GitHub Actions, pytest)** | Medium | High | Version-specific parsers, regex fallbacks, community parser library |
| **Parser brittleness (false positives/negatives)** | Medium | Medium | Extensive test corpus, manual review mode, parser tuning |
| **Large log files (download timeouts, storage)** | Low | Medium | Streaming parsers, log truncation, compression |
| **Privacy concerns (logs contain secrets)** | Low | High | Secret redaction, log sanitization, access control |
| **Agent fix quality (auto-fixes break things)** | Medium | High | Human review required, test-before-merge, rollback support |

### Work Package Structure
```
work/kitty/phase-5-errors/
├── WP-023-error-parsers.md           # Parser implementations
├── WP-024-error-extractors.md        # Artifact downloaders, classifiers
├── WP-025-ci-integration.md          # GitHub Actions integration
├── WP-026-error-tests.md             # Test suite (TDD)
└── WP-027-error-docs.md              # Error guide
```

---

## Phase 6: Documentation, Migration & Release

**Goal:** Provide comprehensive user guides, migration tooling, and release pipeline for unified platform.

**Effort:** S (Small — 2–3 weeks)  
**Value:** Onboard users, enable adoption, establish upstream collaboration path

### Deliverables

#### User Documentation (Doctrine repo)
1. **`docs/integration/getting-started.md`** — Getting started guide
   - Installation (Spec Kitty + Doctrine integration)
   - Quickstart tutorial (create project, enable governance, run first task)
   - Common workflows (planning, implementation, review)

2. **`docs/integration/migration-guide.md`** — Migration guide
   - Migrating existing Spec Kitty projects to Doctrine-enabled mode
   - Migrating existing Doctrine projects to use Spec Kitty orchestration
   - Data migration tooling usage

3. **`docs/integration/troubleshooting.md`** — Troubleshooting guide
   - Common issues (governance blocks, routing failures, dashboard connection)
   - Debugging techniques (telemetry inspection, log analysis)
   - Support resources

4. **`docs/architecture/integration-architecture.md`** — Architecture overview
   - High-level integration diagram (C4 context)
   - Component responsibilities (Spec Kitty vs Doctrine)
   - Extension points and customization

#### Migration Tooling
5. **`ops/scripts/migrate-to-doctrine.py`** — Migration automation
   - Analyze existing Spec Kitty project
   - Generate `.doctrine-config/` with defaults
   - Migrate agent config.yaml to Doctrine profiles (optional)
   - Validate migration completeness

6. **`ops/scripts/validate-integration.py`** — Integration validator
   - Check Spec Kitty compatibility
   - Verify Doctrine governance hooks
   - Test routing provider configuration
   - Generate integration health report

#### Release Pipeline
7. **Release process documentation** — `ops/releases/RELEASE_PROCESS.md`
   - Version numbering strategy (semantic versioning)
   - Release checklist (tests, docs, changelogs)
   - Upstream collaboration plan (contributing to Spec Kitty fork)

8. **Packaging and distribution**
   - PyPI package for Doctrine governance plugin
   - Docker images (dashboard, telemetry services)
   - GitHub releases with binaries

9. **Upstream collaboration plan** — `work/kitty/UPSTREAM_COLLABORATION.md`
   - Features to propose to Spec Kitty upstream
   - Contribution guidelines
   - Roadmap for upstreaming changes

#### Tests
10. **`validation/test_migration_*.py`** — Migration tooling tests
    - Migration script accuracy tests
    - Validation script correctness tests
    - Roundtrip tests (migrate → validate → migrate back)

#### Documentation
11. **`CHANGELOG.md`** — Comprehensive changelog
    - All phases documented (features, fixes, breaking changes)
    - Migration notes per phase
    - Upgrade path from Phase N to N+1

12. **`README.md` updates** — Updated README with integration overview
    - Unified value proposition
    - Quickstart links
    - Architecture diagram

### Agent Assignments

| Agent | Tasks | Artifacts |
|-------|-------|-----------|
| **Writer-Editor Eddy** | Write user guides, troubleshooting docs, getting-started tutorial | User documentation (70% of docs) |
| **Curator Claire** | Write architecture overview, organize documentation structure | Architecture docs, doc structure |
| **Backend Benny** | Implement migration tooling, validator scripts | Migration scripts (50% of code) |
| **Python Pedro** | Write tests for migration tooling | `test_migration_*.py` (80%+ coverage) |
| **DevOps Danny** | Set up release pipeline, packaging, Docker images | CI/CD release pipeline, packaging scripts |
| **Planning Petra** | Write upstream collaboration plan, release process docs | `UPSTREAM_COLLABORATION.md`, release docs |

### Dependencies
- **Upstream:** ALL prior phases (1–5) must be complete
- **Critical Path:** This is final phase before release

### Success Criteria
- ✅ Documentation complete: Getting started, migration, troubleshooting, architecture
- ✅ Migration tooling: ≥95% success rate on test projects
- ✅ Validation tooling: Catches common integration issues
- ✅ Release pipeline: Automated build, test, package, publish
- ✅ Upstream plan: Documented contribution strategy for Spec Kitty
- ✅ Backward compatibility: Existing Spec Kitty and Doctrine projects work unchanged
- ✅ Test coverage: ≥80% on migration tooling

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Documentation staleness (code changes faster than docs)** | High | Medium | Automated doc generation where possible, quarterly doc reviews |
| **Migration edge cases (unusual project structures)** | Medium | Medium | Dry-run mode, manual override options, rollback support |
| **Upstream rejection (Spec Kitty maintainers decline changes)** | Medium | Low | Focus on non-invasive extensions, demonstrate value, fork if needed |
| **Release pipeline complexity (multi-component release)** | Low | Medium | Phased rollout, component versioning, rollback plan |
| **User onboarding friction (steep learning curve)** | Medium | Medium | Tutorial videos, example projects, community support |

### Work Package Structure
```
work/kitty/phase-6-release/
├── WP-028-user-docs.md               # Getting started, migration, troubleshooting
├── WP-029-architecture-docs.md       # Integration architecture overview
├── WP-030-migration-tooling.md       # Migration scripts + validator
├── WP-031-release-pipeline.md        # CI/CD release automation
├── WP-032-upstream-plan.md           # Spec Kitty collaboration strategy
├── WP-033-migration-tests.md         # Test suite (TDD)
└── WP-034-changelog.md               # Comprehensive changelog
```

---

## Dependency Graph (Text-Based DAG)

```
Phase 0 (Analysis & Foundation) ✅ COMPLETE
    ├─→ Phase 1 (Telemetry Library) [M]
    │       ├─→ Phase 3 (Model Routing) [L]
    │       │       └─→ Phase 4 (Dashboard) [M]
    │       │               └─→ Phase 6 (Release) [S]
    │       └─→ Phase 5 (Error Reporting) [M]
    │               └─→ Phase 6 (Release) [S]
    └─→ Phase 2 (Governance Plugin) [L]
            └─→ Phase 3 (Model Routing) [L]
                    └─→ Phase 6 (Release) [S]

CRITICAL PATH (minimum viable integration):
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 6
(~3.5–4.5 person-months on critical path)

PARALLEL WORK OPPORTUNITIES:
- Phase 1 and Phase 2 can run in parallel (no hard dependency)
- Phase 4 and Phase 5 can run in parallel after Phase 1/3 complete
- Documentation (Phase 6) can start during Phase 4/5 (overlap 50%)
```

---

## Agent Assignment Matrix

| Agent | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 | Total Effort |
|-------|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:------------:|
| **Architect Alphonso** | ADR-022, schema | ADR-023, contracts | ADR-024, interfaces | ADR-025 | ADR-026 | Architecture docs | L |
| **Backend Benny** | Core telemetry (80%) | Governance (70%) | Routing (60%) | Dashboard backend (50%) | Error parsers (60%) | Migration scripts | XL |
| **Python Pedro** | Telemetry tests | Governance tests | Routing tests | Dashboard tests | Error tests | Migration tests | L |
| **DevOps Danny** | CI + fixtures | Feature flags | Catalog automation | Dashboard deployment | CI integration | Release pipeline | M |
| **Bootstrap Bill** | — | Bootstrap automation | — | — | — | — | S |
| **Frontend Fiona** | — | — | — | Dashboard UI (40%) | — | — | M |
| **QA Quincy** | — | — | — | E2E tests | E2E tests | — | M |
| **Curator Claire** | Library docs | Integration guide | Routing docs | Dashboard docs | Error guide | Architecture overview | M |
| **Writer-Editor Eddy** | — | — | — | — | — | User guides (70%) | M |
| **Planning Petra** | WP coordination | WP coordination | WP coordination | WP coordination | WP coordination | Upstream plan, release docs | M |
| **Diagram Daisy** | ✅ Phase 0 only | — | — | — | — | — | S |

**Total Team Effort:** ~6–8 person-months (with parallel work, calendar time ~4–5 months)

---

## Risk Register (Top 10 Risks)

| # | Risk | Phase | Likelihood | Impact | Mitigation Strategy | Owner |
|---|------|-------|------------|--------|---------------------|-------|
| **R1** | **Dual-authority confusion (Constitution vs Doctrine)** | 2 | High | High | Explicit precedence contract, policy trace output, advisory mode first | Architect Alphonso |
| **R2** | **Model pricing data staleness (vendor rate changes)** | 3 | High | Medium | Monthly automated pricing sync, alerting on mismatches, external pricing API | DevOps Danny |
| **R3** | **Performance bottleneck in SQLite telemetry queries** | 1 | Medium | High | Indexed materialized views, early benchmarking, Redis cache fallback | Backend Benny |
| **R4** | **Spec Kitty fork read-only constraint (cannot modify upstream)** | All | High | Medium | Build as external extensions, propose changes upstream incrementally | Planning Petra |
| **R5** | **Model ID inconsistencies across routers (OpenRouter vs direct)** | 3 | High | High | Centralized model catalog with ID mapping, validation scripts | Backend Benny |
| **R6** | **CI output format changes break parsers** | 5 | Medium | High | Version-specific parsers, regex fallbacks, community parser library | Backend Benny |
| **R7** | **Workflow regressions (governance blocks valid work)** | 2 | Medium | High | Advisory rollout, gradual block-mode enablement, feature flags | DevOps Danny |
| **R8** | **WebSocket connection stability in dashboard** | 4 | Medium | Medium | Auto-reconnect logic, missed event replay, connection health checks | Frontend Fiona |
| **R9** | **Schema evolution breaks existing telemetry consumers** | 1 | Medium | High | Schema versioning (semver), migration tests, backward compatibility guarantees | Architect Alphonso |
| **R10** | **Documentation staleness (code changes faster than docs)** | 6 | High | Medium | Automated doc generation, quarterly reviews, inline code examples | Curator Claire |

**Risk Response Plan:**
- **High/High risks (R1, R5):** Weekly status checks, dedicated mitigation work packages
- **High/Medium risks (R2, R4, R10):** Biweekly reviews, automated monitoring where possible
- **Medium/High risks (R3, R6, R7):** Early prototyping, gradual rollout, rollback plans
- **Medium/Medium risks (R8, R9):** Standard testing, documented mitigation strategies

---

## Work Package Structure & Tracking

### Directory Structure
```
work/kitty/
├── phase-1-telemetry/         # Phase 1 work packages (WP-001 to WP-005)
├── phase-2-governance/        # Phase 2 work packages (WP-006 to WP-011)
├── phase-3-routing/           # Phase 3 work packages (WP-012 to WP-017)
├── phase-4-dashboard/         # Phase 4 work packages (WP-018 to WP-022)
├── phase-5-errors/            # Phase 5 work packages (WP-023 to WP-027)
├── phase-6-release/           # Phase 6 work packages (WP-028 to WP-034)
├── analysis/                  # ✅ Phase 0 analysis documents (COMPLETE)
├── proposal/                  # ✅ Phase 0 proposal documents (COMPLETE)
│   └── EXECUTION_ROADMAP.md  # ← THIS FILE
└── status/
    ├── PHASE_STATUS.md        # Phase completion tracking
    ├── AGENT_ASSIGNMENTS.md   # Current agent assignments
    └── RISK_TRACKING.md       # Active risk monitoring
```

### Work Package Format (Compatible with Spec Kitty)
Each work package follows Spec Kitty's WP frontmatter format:

```yaml
---
wp_id: WP-001
title: Telemetry Core Implementation
phase: 1
status: ready  # ready → in-progress → review → complete
assigned_agent: backend-benny
dependencies: []
effort: M
acceptance_criteria:
  - Event log writes with <10ms p99 latency
  - SQLite materialized views for common queries
  - Schema versioning implemented
artifacts:
  - src/framework/telemetry/event_log.py
  - src/framework/telemetry/event_store.py
tests:
  - validation/test_telemetry_event_log.py
  - validation/test_telemetry_event_store.py
---

## Context
Build append-only JSONL event log and SQLite materialized view layer...
```

### Tracking Mechanisms

1. **`work/kitty/status/PHASE_STATUS.md`** — Phase completion tracking
   - Phase start/end dates (actual)
   - Deliverable checklists
   - Blocker identification

2. **`work/kitty/status/AGENT_ASSIGNMENTS.md`** — Current assignments
   - Active work packages per agent
   - Utilization tracking (avoid overload)
   - Hand-off protocol

3. **`work/kitty/status/RISK_TRACKING.md`** — Risk monitoring
   - Active risks from risk register
   - Mitigation action status
   - Escalation triggers

4. **`work/collaboration/AGENT_STATUS.md`** — Daily agent status updates
   - Progress reports per Directive 014
   - Blockers and questions
   - Hand-off notifications

---

## Critical Path Analysis

**Minimum Viable Integration (MVI):**
```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 6
  (✅)      (M)       (L)       (L)       (S)
         3 weeks   5 weeks   5 weeks   2 weeks
         = ~15 weeks (3.5–4 months calendar time)
```

**Full Feature Release (FFR):**
```
Phase 0 → Phase 1 ──→ Phase 3 ──→ Phase 4 ──→ Phase 6
  (✅)      (M)          (L)         (M)         (S)
              └──→ Phase 2 ──→ Phase 3 (merge)
                     (L)

Parallel:
Phase 1 ──→ Phase 5 ──→ Phase 6 (merge)
  (M)         (M)         (S)

Total calendar time with parallelization: ~18–20 weeks (4.5–5 months)
```

**Optimization Opportunities:**
- Phase 1 and Phase 2 can start simultaneously (save 3–5 weeks)
- Phase 4 and Phase 5 can run in parallel after Phase 1 complete (save 3–4 weeks)
- Documentation (Phase 6) can overlap with Phase 4/5 by 50% (save 1–2 weeks)
- **Net savings:** ~7–11 weeks → **Final estimate: 12–14 weeks (3–3.5 months)**

---

## Success Metrics (Project-Level)

### Technical Metrics
- **Test Coverage:** ≥80% on all new code (measured via pytest-cov)
- **Integration Test Pass Rate:** ≥95% (E2E scenarios, CI validation)
- **Performance:** Telemetry <10ms p99, Dashboard <500ms updates, Queries <200ms
- **Backward Compatibility:** 100% (existing Spec Kitty and Doctrine projects work unchanged)

### Adoption Metrics
- **Migration Success Rate:** ≥90% (migrate-to-doctrine.py on test projects)
- **Documentation Completeness:** All phases documented (getting started, migration, troubleshooting)
- **Upstream Engagement:** ≥1 accepted PR to Spec Kitty upstream within 6 months

### Governance Metrics
- **Policy Consistency:** 0% precedence conflicts (deterministic governance checks)
- **Hook Reliability:** <1% false positive blocks (governance hooks)
- **Routing Accuracy:** ≥95% correct model selection (routing provider)

### Risk Metrics
- **High/High Risks Mitigated:** 100% (R1, R5) before Phase 6
- **Critical Bugs:** <5 during integration testing
- **Rollback Events:** 0 (no production rollbacks required)

---

## Next Actions (Immediate)

### Week 1: Phase 1 Kickoff (Telemetry Foundation)
1. **Architect Alphonso:** Draft ADR-022 (Telemetry Architecture), design event schema
2. **Backend Benny:** Set up `src/framework/telemetry/` module structure, start event log implementation
3. **Python Pedro:** Write skeleton tests for event log (TDD approach)
4. **DevOps Danny:** Configure CI pipeline for telemetry tests, set up test fixtures
5. **Planning Petra:** Create Phase 1 work packages (WP-001 to WP-005), update `PHASE_STATUS.md`

### Week 2: Phase 2 Kickoff (Governance Plugin) — Parallel with Phase 1
1. **Architect Alphonso:** Draft ADR-023 (Governance Plugin Architecture), define extension interface
2. **Backend Benny:** Prototype doctrine loader, test precedence resolution
3. **Bootstrap Bill:** Design `.doctrine-config/` structure, start bootstrap script
4. **Python Pedro:** Write governance plugin tests (precedence, hook execution)
5. **Planning Petra:** Create Phase 2 work packages (WP-006 to WP-011)

### Week 3: Phase 1 Review & Phase 3 Planning
1. **Backend Benny:** Complete telemetry core (event log, SQLite store), code review
2. **Python Pedro:** Finalize telemetry tests (≥80% coverage), run integration tests
3. **Architect Alphonso:** Start ADR-024 (Routing Architecture), design provider interface
4. **Curator Claire:** Draft telemetry library documentation
5. **Planning Petra:** Review Phase 1 deliverables, create Phase 3 work packages (WP-012 to WP-017)

---

## Assumptions & Constraints

### Assumptions
1. **Spec Kitty fork stability:** No major breaking changes in upstream during integration (6-month window)
2. **Agent availability:** Core agents (Backend Benny, Python Pedro, Architect Alphonso) available ≥50% time
3. **Infrastructure access:** CI/CD pipelines, GitHub Actions, SocketIO hosting available
4. **LLM API access:** OpenRouter, OpenCode.ai, Anthropic, OpenAI APIs accessible with test credits
5. **Python version:** Python 3.10+ (existing Doctrine requirement)

### Constraints
1. **Read-only upstream:** Cannot modify Spec Kitty fork code directly (must build as extensions)
2. **Backward compatibility:** Existing Spec Kitty and Doctrine projects must work unchanged
3. **Test coverage:** ≥80% line coverage on all new code (non-negotiable, per Directive 017)
4. **TDD approach:** Tests must be written first, implementation second (per Directive 016)
5. **Budget:** No new paid services (use existing infrastructure, free tiers, or self-hosted)

### External Dependencies
1. **Spec Kitty upstream:** May need collaboration for extension hooks (Phases 2–3)
2. **LLM vendor APIs:** Pricing table updates, API stability (Phase 3)
3. **CI/CD platforms:** GitHub Actions, GitLab CI output format stability (Phase 5)
4. **Community parsers:** May leverage existing error parser libraries (Phase 5)

---

## Escalation & Re-Planning Triggers

### When to Re-Plan (Adaptation Points)

| Trigger | Threshold | Action |
|---------|-----------|--------|
| **Phase overrun** | >30% time/effort beyond estimate | Reassess remaining phases, consider scope reduction |
| **Critical blocker** | >2 weeks unresolved | Escalate to architect, consider alternative approach |
| **Upstream breaking change** | Spec Kitty API changes incompatible with extensions | Emergency re-architecture, engage upstream maintainers |
| **Test coverage miss** | <70% coverage on completed phase | Block next phase, backfill tests |
| **High/High risk materialized** | R1 or R5 occurs | Immediate mitigation sprint, reassess risk register |
| **Agent unavailability** | Core agent unavailable >3 weeks | Reassign work packages, adjust timelines |
| **Budget/infrastructure issue** | Critical service unavailable | Find alternatives, adjust architecture if needed |

### Escalation Path
1. **Blocker identified** → Agent reports in `AGENT_STATUS.md`
2. **Planning Petra reviews** → Assess impact on critical path
3. **If >3 days stuck** → Escalate to Architect Alphonso
4. **If architectural issue** → Emergency architecture review, update ADR
5. **If external dependency** → Engage upstream/vendor, document workaround

---

## Appendix A: Effort Estimation Legend

| Size | Person-Weeks | Person-Days | Description |
|------|--------------|-------------|-------------|
| **S** | 1–2 weeks | 5–10 days | Single agent, straightforward implementation, minimal dependencies |
| **M** | 3–4 weeks | 15–20 days | Single agent with support, moderate complexity, some integration work |
| **L** | 5–6 weeks | 25–30 days | Multiple agents coordinated, significant complexity, cross-module integration |
| **XL** | 7+ weeks | 35+ days | Team effort, high complexity, architectural changes, extensive testing |

**Note:** Estimates assume 50% agent availability (half-time on this project). Calendar time = effort × 2 for single-threaded work. Parallel work reduces calendar time proportionally.

---

## Appendix B: Related Documentation

### Analysis & Proposal Documents (Phase 0)
- `work/kitty/SUMMARY.md` — Consolidated analysis summary
- `work/kitty/analysis/2026-02-14-doctrine-spec-kitty-integration-analysis.md` — Integration feasibility
- `work/kitty/analysis/2026-02-14-control-plane-spec-kitty-coverage.md` — Gap analysis
- `work/kitty/analysis/2026-02-14-evaluation-doctrine-governance-extension.md` — Feasibility evaluation
- `work/kitty/proposal/spec-kitty-governance-doctrine-extension-proposal.md` — Architectural proposal
- `work/kitty/proposal/EXECUTIVE_SUMMARY.md` — Decision summary
- `work/kitty/proposal/VISION.md` — Strategic vision

### Architecture & Design
- `docs/architecture/assessments/platform_next_steps.md` — Existing platform roadmap (alignment)
- `docs/architecture/adrs/ADR-020-multi-tier-agentic-runtime.md` — Multi-tier architecture
- `docs/architecture/adrs/ADR-021-model-routing-strategy.md` — Model routing strategy
- `work/kitty/proposal/spec-kitty-doctrine-layered-target-architecture.puml` — Target architecture diagram

### Framework Guidelines
- `AGENTS.md` — Agent initialization and governance protocol
- `.doctrine-config/repository-guidelines.md` — Project conventions
- `.github/agents/directives/` — Directive catalog (esp. 016, 017 for TDD/ATDD)
- `.github/agents/approaches/` — Approach catalog

### Testing Standards
- `docs/styleguides/GENERIC_TESTING.md` — Core testing principles
- `docs/styleguides/FORMALIZED_CONSTRAINT_TESTING.md` — Contract testing patterns

---

## Appendix C: Glossary (Integration-Specific Terms)

| Term | Definition |
|------|------------|
| **Doctrine-enabled mode** | Spec Kitty project with governance plugin activated (`.doctrine-config/` present) |
| **Governance hook** | Lifecycle checkpoint where Doctrine policies are evaluated (e.g., pre_plan, pre_implement) |
| **Precedence contract** | Explicit ordering for resolving conflicts: General/Operational Guidelines > Constitution/.doctrine-config > Directives > Mission rules > Tactics |
| **Routing provider** | Pluggable interface for task-to-model mapping (default, doctrine policy, custom) |
| **Telemetry event** | Structured log entry (JSONL) recording task/agent/LLM activity |
| **Materialized view** | Pre-computed SQLite query result for fast dashboard/API access |
| **Work Package (WP)** | Atomic unit of work with frontmatter metadata (compatible with Spec Kitty schema) |
| **Agent bridge** | Mapping layer between Doctrine agent profiles and Spec Kitty agent config.yaml |
| **Advisory mode** | Governance hooks warn but don't block (used during rollout) |
| **Block mode** | Governance hooks prevent progression on policy violations (opt-in) |

---

**Document Status:** ✅ Ready for Review  
**Next Review:** After Phase 1 completion (update with actual timelines, lessons learned)  
**Maintained By:** Planning Petra  
**Last Updated:** 2026-02-14

---

## Declaration

```
✅ SDD Agent "Planning Petra" — Execution Roadmap Complete
**Context layers:** Operational ✓, Strategic ✓, Command ✓, Bootstrap ✓, AGENTS ✓
**Analysis input:** 6 foundation documents, 4 architecture ADRs, platform roadmap
**Output artifacts:** 6-phase roadmap, 34 work packages, dependency graph, risk register
**Agent assignments:** 11 specialist agents mapped across all phases
**Critical path:** Phase 0 → 1 → 2 → 3 → 6 (~15 weeks, optimized to 12–14 weeks with parallelization)
**Assumptions documented:** ✓  **Risks identified:** ✓  **Success criteria defined:** ✓
```

**Mode:** `/analysis-mode` (structured planning, dependency mapping, risk surfacing)  
**Alignment:** General Guidelines ✓, Operational Guidelines ✓, Directive 018 (stable documentation) ✓, Directive 034 (spec-driven) ✓

**Recommendation:** Review with Architect Alphonso for architectural validation, then proceed to Phase 1 kickoff.
