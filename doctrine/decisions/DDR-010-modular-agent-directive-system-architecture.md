# DDR-010: Modular Agent Directive System Architecture

**Status:** Active  
**Date:** 2026-02-11  
**Supersedes:** Repository-specific directive implementations (elevated from ADR-001)

---

## Context

Agent-augmented development frameworks require operational guidance, behavioral norms, safety protocols, and role-specific instructions. Early implementations often consolidate all guidance into monolithic specification files, creating several universal challenges:

1. **Token inefficiency:** Agents load entire specifications, including irrelevant guidance, consuming significant context window space
2. **Maintenance overhead:** Updates require editing large files with intermingled concerns
3. **Portability barriers:** Monolithic structures resist reuse across projects or LLM toolchains
4. **Cognitive load:** Human reviewers face difficulty navigating sprawling specifications
5. **Versioning friction:** No granular control over different aspects of governance

These challenges are inherent to agent coordination systems, not specific to any single repository's tooling or technology choices.

## Decision

We establish a **modular agent directive system** as the framework's core architecture pattern, consisting of:

### 1. Lean Core Specification

A root specification file (e.g., `AGENTS.md`) providing:
- Essential sections defining initialization, runtime behavior, safety, and integration
- Directive index referencing external modular guidance
- Version metadata and update timestamp
- **No role-specific or tool-specific operational detail**

### 2. External Directive Suite

Numerically ordered directives in a designated directory structure:
- **Sequential numbering:** Zero-padded identifiers (001, 002, etc.) for deterministic loading
- **Single concern:** Each directive addresses one aspect of governance
- **Manifest metadata:** Machine-readable inventory with dependencies and safety flags
- **Load-on-demand pattern:** Agents reference directives as needed via explicit commands

### 3. Specialized Agent Profiles

Role-specific profiles that:
- Reference only relevant directives needed for that specialization
- Define clear boundaries and collaboration contracts
- Avoid duplicating directive content
- Inherit behavioral patterns from referenced directives

### 4. Supporting Infrastructure

Supporting mechanisms that repositories should implement:
- **Directive loader:** Script or function for concatenated context assembly
- **Validation tooling:** Integrity checks for directive structure and completeness
- **Bootstrap protocol:** Agent initialization and context loading procedures
- **Rehydration protocol:** Recovery procedures for interrupted workflows

## Rationale

### Universal Benefits

**Token Efficiency:**
- Lazy loading: Agents load only task-relevant directives
- Deduplication: Each directive loaded once per session
- Selective context: Core specification remains minimal; full suite loaded on-demand
- **Estimated gains:** 40-60% reduction in initialization context versus monolithic approach

**Maintainability:**
- Separation of concerns: One directive per governance aspect
- Clear ownership: Manifest indicates safety-critical vs. advisory content
- Predictable structure: Consistent numbering and format
- Human-readable: Each directive understandable independently

**Portability:**
- **Markdown-first:** Platform-agnostic `.md` format, no vendor lock-in
- **Standardized metadata:** JSON/YAML manifest for machine discovery
- **Cross-toolchain compatibility:** Works with any LLM system supporting markdown context
- **Reusability:** Directives transferable across repositories with minimal adaptation

**Extensibility:**
- **Directive-level versioning:** Independent evolution of governance aspects
- **Dependency tracking:** Manifest captures interdependencies
- **Safe deprecation:** Status field (`active|deprecated|pending`) for lifecycle management
- **Integrity validation:** Automated checks for structural conformity

### Framework-Level Pattern

This pattern applies universally because:
- All agent systems face token budget constraints
- All frameworks benefit from separation of concerns
- All adopters need portability across toolchains
- All systems require versioning and governance evolution

## Consequences

### Positive

- ✅ **Reduced token costs:** Agents consume 40-60% less context on initialization
- ✅ **Faster iteration:** Updates to specific directives without touching core specification
- ✅ **Better collaboration:** Concurrent agent work without context conflicts
- ✅ **Clearer responsibilities:** Explicit purpose and dependencies per directive
- ✅ **Improved discoverability:** Manifest provides searchable metadata
- ✅ **Easier onboarding:** Agents reference only necessary directives
- ✅ **Quality assurance:** Validation tooling catches structural issues
- ✅ **Portable framework:** Adoptable by new repositories with minimal changes

### Negative (Accepted Trade-offs)

- ⚠️ **Increased file count:** Multiple directive files vs. single specification (accepted for maintainability)
- ⚠️ **Load coordination overhead:** Agents must explicitly load directives (mitigated by loader tooling)
- ⚠️ **Potential for drift:** Directives could become inconsistent (mitigated by validation)
- ⚠️ **Learning curve:** Contributors must understand directive system (mitigated by documentation)
- ⚠️ **Manifest synchronization:** Manifest must stay current with directive files (automation recommended)

## Implementation

Repositories adopting this framework should:

### Directive Structure

```
<framework-root>/
  agents/               # or .github/agents/, .agents/, etc.
    directives/
      manifest.json     # Directive inventory
      001_<name>.md     # Sequential directives
      002_<name>.md
      ...
    profiles/           # Agent role definitions
      <agent-name>.md
    AGENTS.md           # Core specification
```

### Manifest Schema

```json
{
  "directives": [
    {
      "code": "001",
      "slug": "directive-identifier",
      "title": "Human-readable name",
      "file": "directives/001_name.md",
      "purpose": "One-line description",
      "dependencies": ["002", "005"],
      "requiredInAgents": false,
      "safetyCritical": true,
      "version": "1.0.0",
      "status": "active"
    }
  ]
}
```

### Directive Format

Each directive file should:
- Start with heading `# <code>: <title>`
- Include Purpose, Decision, Rationale, Consequences sections
- Document dependencies on other directives
- Specify target audience (all agents, specific roles, coordinators)
- Provide implementation examples without repository-specific code

### Load-on-Demand Pattern

Agents should support explicit directive loading:
- Command: `/require-directive <code>` or equivalent
- Loader concatenates requested directives with core specification
- Dependency resolution: Automatically include prerequisite directives
- Deduplication: Load each directive only once per session

### Validation Requirements

Repositories should validate:
- Directive sequencing (ascending numerical order)
- Heading conformity (matches manifest)
- Dependency file existence
- Manifest completeness (all files listed)
- Status field validity (`active|deprecated|pending`)
- No orphaned directives (present in filesystem but not manifest)

## Related

- **Doctrine:** DDR-002 (Framework Guardian Role) - guardian validates directive integrity
- **Approach:** Modular documentation approach (framework principles)
- **Implementation:** See repository-specific ADRs for tooling and directory structures
