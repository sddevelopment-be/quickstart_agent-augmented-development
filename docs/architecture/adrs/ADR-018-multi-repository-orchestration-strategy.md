# ADR-018: Multi-Repository Orchestration Strategy

**status**: `Proposed`  
**date**: 2025-11-27

### Context

The current file-based asynchronous orchestration system (ADR-008) works effectively for single-repository scenarios. As organizations adopt this framework across multiple repositories, cross-repository coordination becomes necessary for:

- **Template distribution**: This quickstart repository serves as a template; consuming repositories need updates
- **Shared governance**: Directive and agent profile synchronization across projects
- **Cross-project dependencies**: Service A depends on Service B's API changes in microservice architectures
- **Organization-wide standards**: Policy updates must propagate to all managed repositories

Without explicit multi-repository support, teams face:

1. **Manual duplication**: Copy-paste directives and templates between repositories
2. **Drift**: Governance content diverges as repositories evolve independently
3. **Coordination overhead**: Cross-repo dependencies tracked via ad-hoc communication (Slack, email)
4. **Audit fragmentation**: No unified view of cross-repository workflows

We must extend the orchestration model to support multi-repository scenarios while preserving:

- **Simplicity**: No databases, APIs, or complex infrastructure
- **Autonomy**: Each repository retains independent workflows
- **Git-native**: Leverage existing version control for audit trail
- **Portability**: No vendor lock-in

### Decision

**We will adopt a hybrid "hub-and-spoke" orchestration pattern with phased implementation.**

Specifically:

1. **Phase 1 (Immediate)**: Extend task schema with `external_dependencies` field for cross-repository task references
2. **Phase 2 (Future)**: Establish optional orchestration hub repository for organizations with >5 cross-repo workflows per month
3. **Phase 3 (Long-term)**: Automate directive/template synchronization from hub to managed repositories

**Phase 1** is approved and should be implemented immediately. **Phase 2 and 3** are deferred pending operational evidence of coordination overhead.

### Rationale

**Why hybrid over monorepo?**

- **Migration cost**: Consolidating existing repositories into a monorepo is disruptive and resisted by teams
- **Scalability**: Monorepos require specialized tooling (Bazel, Nx) at scale, increasing infrastructure complexity
- **Autonomy**: Teams value repository independence; monorepo centralizes control

**Why hybrid over pure polyrepo?**

- **Governance enforcement**: Pure polyrepo requires manual directive synchronization, leading to drift
- **Visibility**: No centralized view of cross-repo workflows in pure polyrepo
- **Coordination efficiency**: Hub reduces coordination overhead for frequent cross-repo dependencies

**Why phased approach?**

- **Validate assumptions**: Phase 1 validates cross-repo coordination patterns before committing to hub infrastructure
- **Risk mitigation**: Incremental deployment reduces disruption
- **Resource efficiency**: Defer Phase 2/3 investment until proven necessary

**Phase 1: Cross-Repo Task References**

Extends task YAML schema with `external_dependencies`:

```yaml
id: 2025-11-27T1430-api-change
agent: architect
status: in_progress
priority: high

title: "Breaking API change in service-a"

external_dependencies:
  - repo: "org/service-b"
    task_ref: "2025-11-27T1430-update-api-client"
    status_url: "https://github.com/org/service-b/blob/main/work/collaboration/assigned/build-automation/2025-11-27T1430-update-api-client.yaml"
    status: "in_progress"
    last_checked: "2025-11-27T15:00:00Z"

blocking_on:
  - "external_dependencies[0].status == 'done'"
```

**Agents** poll external task status via GitHub API or raw file access. No infrastructure changes required.

**Phase 2: Orchestration Hub (Deferred)**

Create dedicated hub repository when coordination frequency justifies infrastructure:

```
orchestration-hub/
  .github/agents/           # Shared agent profiles
  work/collaboration/       # Cross-repo tasks only
  managed-repos.yaml        # Registry of managed repositories
  sync/                     # Directive/template synchronization tooling
```

**Phase 3: Sync Automation (Deferred)**

Automate directive/template propagation via Git submodules, subtree, or custom sync scripts.

**Trade-offs accepted:**

- **Two orchestration layers**: Hub + local repositories increase cognitive load (mitigated by clear boundaries)
- **Hub SPOF risk**: Hub unavailability blocks cross-repo coordination (mitigated by local-only fallback mode)
- **Synchronization complexity**: Keeping hub and repositories aligned requires automation (deferred until proven necessary)

### Envisioned Consequences

**Positive:**

- ✅ **Incremental adoption**: Phase 1 works with existing polyrepo setups; no forced migration
- ✅ **Visibility**: External dependencies explicitly declared in task files
- ✅ **Autonomy preservation**: Repositories remain independent; hub is optional
- ✅ **Git-native**: Task references leverage existing GitHub URLs and API
- ✅ **Low infrastructure cost**: Phase 1 requires only schema and agent logic updates
- ✅ **Validation path**: Phase 1 provides operational data to inform Phase 2 decision

**Negative:**

- ⚠️ **Polling latency**: Cross-repo task status may be stale (acceptable for async workflows)
- ⚠️ **Coordination overhead**: Phase 1 alone doesn't reduce manual coordination significantly
- ⚠️ **Deferred governance sync**: Phase 1 doesn't address directive/template drift
- ⚠️ **Hub complexity**: Phase 2 introduces new infrastructure component

**Risks:**

- **Phase 1 insufficient**: If coordination overhead remains high, Phase 2 delay causes frustration → Mitigate with clear escalation criteria (>5 cross-repo workflows/month)
- **Hub adoption resistance**: Teams may reject hub coordination → Mitigate by making hub opt-in
- **Sync conflicts**: Automated directive propagation may conflict with local customizations → Mitigate with branch-based sync and PR review

**Dependencies:**

- Task schema validation must support `external_dependencies` field
- Agents need GitHub API access (read-only) for cross-repo status polling
- Documentation updates for cross-repo task authoring

### Considered Alternatives

**1. Monorepo Consolidation**

- **Pros**: Single orchestration directory, no cross-repo coordination needed
- **Cons**: High migration cost, Git performance issues at scale, team resistance
- **Reason rejected**: Disruptive and culturally incompatible with polyrepo organizations

**2. Pure Polyrepo (No Hub)**

- **Pros**: Minimal infrastructure, maximum autonomy
- **Cons**: Manual governance propagation, no cross-repo visibility, high coordination overhead
- **Reason rejected**: Doesn't solve governance drift or coordination pain points

**3. GitHub Issues/Projects for Coordination**

- **Pros**: Native GitHub integration, existing UI
- **Cons**: API rate limits, not suitable for high-frequency updates, opaque to local development
- **Reason rejected**: Breaks Git-native principle, adds external dependency

**4. Event Bus (Redis/Kafka) for Cross-Repo Coordination**

- **Pros**: Real-time updates, scalable
- **Cons**: Requires running services, not Git-native, infrastructure complexity
- **Reason rejected**: Violates simplicity principle, not portable

---

**Related ADRs:**

- [ADR-008: File-Based Asynchronous Agent Coordination](ADR-008-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle and State Management](ADR-003-task-lifecycle-state-management.md)
- [ADR-004: Work Directory Structure](ADR-004-work-directory-structure.md)

**References:**

- [Multi-Repository Orchestration Patterns Assessment](../assessments/multi-repository-orchestration-patterns.md)
- [Async Multi-Agent Orchestration Architecture](../design/async_multiagent_orchestration.md)

**Next Steps:**

1. Update task YAML schema with `external_dependencies` and `blocking_on` fields
2. Update validation scripts to support new schema fields
3. Extend agent logic to poll external task status via GitHub API
4. Document cross-repo task authoring in `docs/guides/`
5. Measure cross-repo coordination frequency over 2-4 weeks
6. Decide on Phase 2 (hub) implementation based on metrics
