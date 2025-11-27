# Multi-Repository Orchestration Patterns Assessment

_Version: 1.0.0_  
_Date: 2025-11-27_  
_Status: Research/Assessment_  
_Author: Architect Alphonso_

## Executive Summary

This document assesses architectural patterns and infrastructure requirements for multi-repository orchestration scenarios in agent-augmented development workflows. The current implementation focuses on single-repository coordination using file-based task workflows. As teams scale, multi-repository orchestration becomes necessary for:

- **Cross-project dependencies** in microservice architectures
- **Shared framework maintenance** across multiple consuming repositories
- **Organization-wide governance** and standards enforcement
- **Template distribution** and synchronization

This assessment evaluates three primary patterns (monorepo, polyrepo, hybrid) and recommends a **gradual extension of the existing file-based coordination model** with cross-repository task references and centralized orchestration hubs.

## Context and Requirements

### Current State

The repository implements asynchronous multi-agent orchestration via:

- **File-based coordination**: YAML task files in `work/` directories (ADR-008)
- **Task lifecycle**: `inbox → assigned → in_progress → done → archive` (ADR-003)
- **Agent specialization**: Dedicated agents with clear boundaries (ADR-005)
- **Git-native audit trail**: All state changes versioned in Git commits

This model works well for **single-repository scenarios** but faces challenges when:

1. **Multiple repositories need coordination**: Template updates, shared directive changes
2. **Cross-repo dependencies exist**: Service A depends on Service B's API changes
3. **Organization-wide standards evolve**: Governance updates must propagate to all projects
4. **Distributed teams collaborate**: Different repositories owned by different teams

### Requirements Analysis

Multi-repository orchestration must support:

| Requirement | Priority | Rationale |
|------------|----------|-----------|
| **Autonomy**: Each repository retains independent workflows | Critical | Teams must maintain control over their projects |
| **Visibility**: Cross-repo task status is transparent | High | Coordination requires awareness of external dependencies |
| **Traceability**: Full audit trail across repositories | High | Compliance, debugging, and retrospectives |
| **Scalability**: Pattern works for 2-100+ repositories | Medium | Support growth without architecture redesign |
| **Simplicity**: Minimal infrastructure overhead | High | Aligns with existing file-based simplicity principle |
| **Git-native**: Leverage existing version control | High | No new infrastructure for state management |
| **Failure isolation**: One repository's issues don't cascade | Medium | Resilience and fault tolerance |

### Anti-Requirements

Explicitly **not** in scope:

- Real-time synchronization across repositories (async model sufficient)
- Centralized database for task state (conflicts with Git-native principle)
- Automated cross-repo merging without human approval (safety)
- Vendor-specific orchestration platforms (portability)

## Pattern Analysis

### Pattern 1: Monorepo

**Description**: All projects consolidated into a single Git repository with shared `work/` orchestration directory.

**Structure Example**:
```
mega-repo/
  .github/agents/           # Shared agent profiles
  work/                     # Centralized orchestration
    collaboration/
      inbox/
      assigned/
  projects/
    service-a/
    service-b/
    shared-library/
    template-repo/
```

**Pros**:
- ✅ **Simplicity**: Single orchestration directory, no cross-repo coordination needed
- ✅ **Atomic changes**: Single commit affects multiple projects simultaneously
- ✅ **Unified tooling**: One set of agents, directives, and validation scripts
- ✅ **Refactoring ease**: Cross-project changes are straightforward
- ✅ **Dependency clarity**: All dependencies visible in one place

**Cons**:
- ⚠️ **Scale limitations**: Git performance degrades with large monorepos (>10GB)
- ⚠️ **CI complexity**: Build times increase; requires sophisticated caching
- ⚠️ **Access control**: Difficult to restrict repository access per-team
- ⚠️ **Cognitive load**: Developers must navigate large directory structures
- ⚠️ **Clone times**: Initial clone and pulls slower as repo grows
- ⚠️ **Branch conflicts**: High risk of merge conflicts with many contributors
- ⚠️ **Organizational friction**: Existing polyrepo setups resist consolidation

**Infrastructure Requirements**:
- **VCS**: Git with LFS for large assets, or specialized tools (Google's Bazel, Microsoft's VFS for Git)
- **CI/CD**: Intelligent build orchestration (Bazel, Nx, Turborepo) to avoid full-repo builds
- **Access control**: Fine-grained CODEOWNERS, branch protection rules
- **Tooling**: Path-based filtering for agents, build caching infrastructure

**Use Cases**:
- Startups with <10 projects and tight integration needs
- Organizations standardizing on Google/Facebook-style monorepo culture
- Projects where cross-repo refactoring is frequent (e.g., shared type libraries)

**Risk Assessment**:
- 🔴 **High migration cost**: Consolidating existing repositories is disruptive
- 🟡 **Performance risk**: Git performance unpredictable at scale without specialized tooling
- 🟢 **Low coordination complexity**: No cross-repo orchestration needed

---

### Pattern 2: Polyrepo (Distributed Orchestration)

**Description**: Each repository maintains independent `work/` orchestration, with cross-repository tasks referencing external repositories via URLs or identifiers.

**Structure Example**:
```
service-a/
  .github/agents/           # Local agent profiles
  work/
    collaboration/
      inbox/
        2025-11-27-cross-repo-task.yaml  # References service-b

service-b/
  .github/agents/
  work/
    collaboration/
      inbox/
        2025-11-27-dependency-update.yaml
```

**Cross-Repo Task Example**:
```yaml
# service-a/work/collaboration/inbox/2025-11-27-api-change.yaml
id: 2025-11-27T1430-api-change-coordination
agent: architect
status: new
priority: high

title: "Coordinate breaking API change with consuming services"

external_dependencies:
  - repo: "org/service-b"
    task_ref: "2025-11-27T1430-update-api-client"
    status_url: "https://github.com/org/service-b/blob/main/work/collaboration/assigned/build-automation/2025-11-27T1430-update-api-client.yaml"
  - repo: "org/service-c"
    task_ref: "2025-11-27T1430-update-api-client"

blocking_on:
  - "external_dependencies[*].status == 'done'"
```

**Pros**:
- ✅ **Autonomy**: Each repository fully independent, no forced coupling
- ✅ **Scalability**: Linear scaling; no performance bottlenecks
- ✅ **Access control**: Native GitHub permissions per repository
- ✅ **Failure isolation**: Repository issues don't block others
- ✅ **Team ownership**: Clear boundaries, no cross-team merge conflicts
- ✅ **Gradual adoption**: New repositories adopt orchestration incrementally

**Cons**:
- ⚠️ **Coordination complexity**: Cross-repo task tracking requires tooling
- ⚠️ **Visibility challenges**: No single dashboard for multi-repo workflows
- ⚠️ **Duplication risk**: Directives, agents, and templates may diverge
- ⚠️ **Dependency resolution**: Must poll external repositories for status
- ⚠️ **Refactoring friction**: Cross-repo changes require multiple PRs and synchronization
- ⚠️ **Audit trail fragmentation**: Task history scattered across repositories

**Infrastructure Requirements**:
- **Cross-repo polling**: Agents must check external task status (GitHub API or file access)
- **Task references**: Schema extensions for `external_dependencies` and `blocking_on`
- **Status aggregation**: Optional dashboard aggregating task status across repositories
- **Synchronization**: Tooling to propagate directive/template updates
- **Authentication**: GitHub tokens with cross-repo read access

**Use Cases**:
- Organizations with existing polyrepo setups (most enterprises)
- Microservice architectures with clear service boundaries
- Teams with strong autonomy requirements
- Open-source projects with distributed contributors

**Risk Assessment**:
- 🟢 **Low migration cost**: Extends existing single-repo pattern naturally
- 🟡 **Medium coordination complexity**: Requires tooling for cross-repo visibility
- 🟢 **Low Git performance risk**: Each repository remains small

---

### Pattern 3: Hybrid (Hub-and-Spoke)

**Description**: Centralized orchestration hub repository coordinates cross-repo workflows, while individual repositories maintain local task workflows for internal work.

**Structure Example**:
```
orchestration-hub/
  .github/agents/           # Shared agent profiles
  work/
    collaboration/
      inbox/                # Cross-repo coordination tasks only
      assigned/
        coordinator/        # Coordinator agent manages cross-repo workflows
  managed-repos.yaml        # Registry of managed repositories
  sync/                     # Directive/template synchronization

service-a/
  .github/agents/           # Extends hub profiles
  work/
    collaboration/
      inbox/                # Local tasks only
      external/             # Tasks delegated from hub

service-b/
  .github/agents/
  work/
    collaboration/
      inbox/
      external/
```

**Managed Repos Registry Example**:
```yaml
# orchestration-hub/managed-repos.yaml
version: 1.0.0
hub_repo: "org/orchestration-hub"

managed_repos:
  - name: "service-a"
    repo: "org/service-a"
    sync_directives: true
    sync_templates: true
    contact: "team-alpha@example.com"
  
  - name: "service-b"
    repo: "org/service-b"
    sync_directives: true
    sync_templates: false
    contact: "team-beta@example.com"
```

**Cross-Repo Workflow Example**:
```yaml
# orchestration-hub/work/collaboration/inbox/2025-11-27-multi-repo-migration.yaml
id: 2025-11-27T1500-multi-repo-api-migration
agent: coordinator
status: new
priority: high

title: "Coordinate API v2 migration across services"

orchestration_plan:
  - phase: "1-update-api-definition"
    repos: ["org/api-spec"]
    tasks:
      - "Update OpenAPI spec to v2"
  
  - phase: "2-update-server"
    repos: ["org/service-a"]
    depends_on: ["1-update-api-definition"]
    tasks:
      - "Implement v2 endpoints"
      - "Add deprecation warnings to v1"
  
  - phase: "3-update-clients"
    repos: ["org/service-b", "org/service-c"]
    depends_on: ["2-update-server"]
    parallel: true
    tasks:
      - "Migrate client code to v2"
      - "Update integration tests"
```

**Pros**:
- ✅ **Centralized visibility**: Single hub shows all cross-repo workflows
- ✅ **Governance enforcement**: Hub propagates directives, templates, standards
- ✅ **Repository autonomy**: Local workflows remain independent
- ✅ **Failure isolation**: Hub issues don't block local repository work
- ✅ **Incremental adoption**: Repositories opt-in to hub coordination
- ✅ **Audit trail**: Complete cross-repo workflow history in hub

**Cons**:
- ⚠️ **Hub becomes SPOF**: Hub repository availability critical for cross-repo work
- ⚠️ **Complexity**: Two orchestration layers (hub + local) to understand
- ⚠️ **Synchronization overhead**: Keeping hub and repositories aligned requires automation
- ⚠️ **Authority ambiguity**: Unclear whether hub or repository has final say
- ⚠️ **Hub scaling**: Hub repository may grow large with coordination history

**Infrastructure Requirements**:
- **Hub repository**: Dedicated Git repository for cross-repo orchestration
- **Synchronization tooling**: Automate directive/template propagation (Git submodules, subtree, or custom scripts)
- **Cross-repo agents**: Agents with multi-repo access (GitHub App or PAT)
- **Status aggregation**: Dashboard showing hub + repository task status
- **Notification system**: Alert teams of hub-initiated tasks in their repositories

**Use Cases**:
- Organizations with 10-50 repositories needing light coordination
- Platform teams managing shared infrastructure across services
- Template repositories distributing reusable patterns
- Governance teams enforcing organization-wide standards

**Risk Assessment**:
- 🟡 **Medium migration cost**: Requires hub setup and sync automation
- 🟡 **Medium coordination complexity**: Two-layer orchestration increases cognitive load
- 🟢 **Low Git performance risk**: Hub and repositories remain small

---

## Infrastructure Requirements Comparison

| Component | Monorepo | Polyrepo | Hybrid |
|-----------|----------|----------|--------|
| **Version Control** | Git + LFS or specialized VCS | Standard Git | Standard Git |
| **Build System** | Intelligent caching (Bazel, Nx) | Per-repo CI/CD | Per-repo + hub CI/CD |
| **Access Control** | Fine-grained CODEOWNERS | Native GitHub permissions | Hub + repo permissions |
| **Orchestration Tooling** | Single-repo agent orchestrator | Cross-repo status polling | Hub orchestrator + local agents |
| **Synchronization** | N/A (single repo) | Manual or custom scripts | Automated hub sync |
| **Monitoring Dashboard** | Single dashboard | Aggregation service | Hub + repo dashboards |
| **Authentication** | Single-repo access | Multi-repo GitHub tokens | Hub + managed repo tokens |
| **Deployment Complexity** | High (monorepo tooling) | Low (standard Git) | Medium (hub + sync) |

## Recommendations

### Recommended Pattern: **Hybrid (Hub-and-Spoke)** with Gradual Adoption

**Rationale**:

1. **Aligns with existing architecture**: Extends current file-based coordination naturally
2. **Preserves repository autonomy**: Teams retain control over local workflows
3. **Enables centralized governance**: Hub propagates standards without forcing consolidation
4. **Scales incrementally**: Start with 2-3 repositories, expand gradually
5. **Low infrastructure cost**: Leverages existing Git and GitHub infrastructure
6. **Maintains simplicity**: No databases, APIs, or complex tooling

**Implementation Phases**:

#### Phase 1: Cross-Repo Task References (Low-Hanging Fruit)

Extend existing task schema to support external dependencies:

```yaml
# Add to task YAML schema
external_dependencies:
  - repo: string          # GitHub repo identifier (org/repo)
    task_ref: string      # Task ID in external repository
    status_url: string    # URL to external task file (optional)
    status: enum          # Cached status: new, in_progress, done, blocked
    last_checked: datetime

blocking_on:
  - condition: string     # E.g., "external_dependencies[0].status == 'done'"
```

**Agents** poll external task status periodically (via GitHub API or raw file access).

**Benefits**:
- No infrastructure changes required
- Works with existing polyrepo setups
- Clear visibility into cross-repo dependencies

**Effort**: 1-2 days (schema update, agent logic, documentation)

#### Phase 2: Orchestration Hub (Optional, Future)

Create dedicated hub repository when cross-repo coordination exceeds ad-hoc capacity (>5 cross-repo workflows per month).

**Hub Responsibilities**:
- Maintain `managed-repos.yaml` registry
- Execute cross-repo workflow orchestration plans
- Propagate directive/template updates to managed repositories
- Aggregate status dashboard

**Effort**: 1-2 weeks (hub setup, sync automation, coordinator agent updates)

#### Phase 3: Directive/Template Synchronization (Long-Term)

Automate synchronization of governance content from hub to repositories:

- **Git submodules**: Reference hub directives/templates (simple, Git-native)
- **Git subtree**: Embed hub content with independent history (more flexible)
- **Custom sync script**: Periodically copy files and create PRs (most control)

**Trade-offs**:
- Submodules: Simple but requires explicit updates (`git submodule update`)
- Subtree: Seamless but merge conflicts on divergence
- Custom script: Full control but maintenance overhead

**Effort**: 3-5 days (tooling implementation, testing, documentation)

### Alternative: Pure Polyrepo (If Hub Overhead Unacceptable)

If hub infrastructure is rejected, implement **Phase 1 only** (cross-repo task references) and rely on manual coordination for governance updates.

**Trade-offs**:
- ✅ Minimal infrastructure
- ⚠️ Manual governance propagation (copy-paste directives)
- ⚠️ No centralized cross-repo visibility

### Alternative: Monorepo (If Consolidation Acceptable)

Consider monorepo only if:
- Organization has <10 repositories
- Strong cultural alignment with monorepo philosophy (Google/Facebook model)
- Willingness to invest in specialized tooling (Bazel, Nx, or similar)

**Migration Path**:
1. Use Git subtree merge to consolidate repositories
2. Refactor `work/` directory to support multi-project filtering
3. Implement build orchestration with intelligent caching

**Effort**: 2-4 weeks (high disruption risk)

## Decision Criteria

Choose pattern based on organizational context:

| Criterion | Choose Monorepo | Choose Polyrepo | Choose Hybrid |
|-----------|-----------------|-----------------|---------------|
| **Repository count** | <10 repositories | >50 repositories | 10-50 repositories |
| **Cross-repo refactoring frequency** | Daily/Weekly | Rarely | Monthly |
| **Team autonomy** | Low (centralized) | High | Medium |
| **Existing setup** | Green-field or small | Established polyrepo | Established polyrepo with coordination needs |
| **Infrastructure budget** | High (specialized tooling) | Low (standard Git) | Medium (hub + sync) |
| **Risk tolerance** | High (migration disruption) | Low (incremental extension) | Medium (new hub component) |

## Security and Compliance Considerations

### Access Control

- **Monorepo**: Fine-grained CODEOWNERS per directory, branch protection rules
- **Polyrepo**: Native GitHub repository permissions, PATs with minimal scopes
- **Hybrid**: Hub requires read access to managed repositories; consider GitHub App for scoped permissions

### Audit Trail

- **Monorepo**: Single Git history; all changes traceable
- **Polyrepo**: Distributed history; cross-repo audits require aggregation
- **Hybrid**: Hub history + local repository history; cross-reference via task IDs

### Secrets Management

- **Cross-repo agents**: Store GitHub tokens in CI/CD secrets (GitHub Actions, GitLab CI)
- **Hub sync**: Use GitHub App with read/write permissions, scoped to specific repositories
- **Avoid**: Hardcoding tokens in task files or scripts

## Open Questions

1. **Hub repository ownership**: Which team owns the orchestration hub?
2. **Governance propagation**: Mandatory or opt-in for managed repositories?
3. **Failure handling**: What happens if hub is unavailable? Fallback to local-only mode?
4. **Versioning**: Should directives/templates be versioned independently per repository?
5. **Migration path**: How to migrate existing repositories to hub coordination?

## Next Steps

1. **Socialize this assessment** with stakeholders (architects, team leads, DevOps)
2. **Prototype Phase 1** (cross-repo task references) in 1-2 pilot repositories
3. **Measure coordination overhead** (time spent on cross-repo task tracking)
4. **Decide on Phase 2** (hub) based on coordination frequency metrics
5. **Draft ADR** if hub-and-spoke pattern is approved

## References

- [ADR-008: File-Based Asynchronous Agent Coordination](../adrs/ADR-008-file-based-async-coordination.md)
- [ADR-003: Task Lifecycle and State Management](../adrs/ADR-003-task-lifecycle-state-management.md)
- [Async Multi-Agent Orchestration Architecture](../design/async_multiagent_orchestration.md)
- [Orchestration Implementation Plan](../../../work/collaboration/orchestration-implementation-plan.md)
- [Google's Monorepo Practices](https://dl.acm.org/doi/10.1145/2854146)
- [Microsoft's Git Virtual File System](https://github.com/microsoft/VFSForGit)
- [Bazel Build System](https://bazel.build/)
- [Nx Monorepo Tooling](https://nx.dev/)

---

_Maintained by: Architect agents_  
_Review cycle: Quarterly or when cross-repo coordination needs change_  
_Version: 1.0.0_
