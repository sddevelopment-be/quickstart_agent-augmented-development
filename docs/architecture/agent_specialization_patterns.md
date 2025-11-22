# Agent Specialization Patterns

**Version:** 1.0.0  
**Last Updated:** 2025-11-17  
**Type:** Architecture Pattern Guide

---

## Purpose

This document describes **architectural patterns for agent specialization** in the agent-augmented development repository. It provides guidance for creating, configuring, and coordinating specialized agents to maximize efficiency, maintain quality, and ensure consistent collaboration.

## Pattern Overview

Agent specialization follows a **bounded context** pattern where each agent:
- Operates within a clearly defined domain
- Loads only relevant directives for its role
- Collaborates via explicit handoff protocols
- Escalates when operating outside its boundaries

## Core Specialization Patterns

### 1. Architect Pattern

**Purpose:** System decomposition, design interfaces, explicit decision records.

**Specialization Boundaries:**
- ✅ ADRs, architecture pattern documents, PlantUML diagrams
- ✅ Trade-off analysis, decision rationale, interface design
- ✅ Cross-cutting concerns, quality attributes, extension points
- ❌ Low-level implementation details, code optimization, tool evangelism

**Key Directives:**
- 003: Repository Quick Reference
- 004: Documentation & Context Files
- 006: Version Governance
- 007: Agent Declaration
- 008: Artifact Templates

**Output Artifacts:**
- ADRs following `docs/templates/architecture/adr.md`
- Architecture vision documents
- System decomposition diagrams
- Pattern guides and recommendations

**Collaboration Model:**
- Consumes: Vision, functional requirements, technical constraints
- Produces: Architecture decisions, design patterns, system boundaries
- Hands off to: Developers (implementation), Curators (validation)

### 2. Curator Pattern

**Purpose:** Validation, consistency checks, integrity assurance, metadata maintenance.

**Specialization Boundaries:**
- ✅ Structural validation, orphan detection, manifest synchronization
- ✅ Cross-reference integrity, template conformity, version tracking
- ✅ Assessment reports, enhancement recommendations
- ❌ Content creation, implementation work, strategic decisions

**Key Directives:**
- 001: CLI & Shell Tooling
- 004: Documentation & Context Files
- 006: Version Governance
- 011: Risk & Escalation
- 012: Common Operating Procedures

**Output Artifacts:**
- Validation reports (structural, semantic, integrity)
- Consistency assessments
- Enhancement roadmaps
- Manifest updates

**Collaboration Model:**
- Consumes: All repository artifacts (for validation)
- Produces: Quality reports, improvement recommendations
- Hands off to: Architects (for governance changes), Developers (for fixes)

### 3. Developer Pattern (Backend/Frontend)

**Purpose:** Code implementation, testing, debugging, refactoring.

**Specialization Boundaries:**
- ✅ Code generation, test writing, debugging, performance optimization
- ✅ API implementation, database schema, integration logic
- ✅ Build configuration, dependency management
- ❌ Architecture decisions, UX design, documentation strategy

**Key Directives:**
- 001: CLI & Shell Tooling
- 003: Repository Quick Reference
- 004: Documentation & Context Files
- 009: Role Capabilities

**Output Artifacts:**
- Source code, test suites, build scripts
- Technical implementation notes
- Debug logs, performance profiling
- Refactoring documentation

**Collaboration Model:**
- Consumes: ADRs, technical designs, functional requirements
- Produces: Working code, tests, implementation notes
- Hands off to: Writers (documentation), Curators (validation)

### 4. Writer/Editor Pattern

**Purpose:** Content creation, documentation, technical writing, editing.

**Specialization Boundaries:**
- ✅ User guides, API documentation, tutorials, style refinement
- ✅ Markdown formatting, cross-referencing, content structure
- ✅ Terminology consistency, readability improvements
- ❌ Code implementation, architecture decisions, infrastructure changes

**Key Directives:**
- 004: Documentation & Context Files
- 008: Artifact Templates
- 010: Mode Protocol (creative mode usage)

**Output Artifacts:**
- User-facing documentation
- API reference materials
- Tutorials and guides
- Style guide updates

**Collaboration Model:**
- Consumes: Technical specifications, architecture decisions, code
- Produces: Human-readable documentation
- Hands off to: Curators (review), Translators (localization)

### 5. Lexical (LEX) Pattern

**Purpose:** Linguistic consistency, terminology governance, style enforcement.

**Specialization Boundaries:**
- ✅ Glossary maintenance, term normalization, style rule creation
- ✅ Language pattern detection, inconsistency reporting
- ✅ Cross-repository terminology audits
- ❌ Content authoring, technical implementation, architecture design

**Key Directives:**
- 001: CLI & Shell Tooling (for grep/search operations)
- 004: Documentation & Context Files
- 008: Artifact Templates (LEX templates)

**Output Artifacts:**
- LEX reports (style violations, inconsistencies)
- LEX deltas (proposed terminology changes)
- Style rule documentation
- Glossary updates

**Collaboration Model:**
- Consumes: All written content (for analysis)
- Produces: Consistency reports, style recommendations
- Hands off to: Writers (corrections), Curators (validation)

### 6. Build/Automation Pattern

**Purpose:** CI/CD configuration, automation scripts, infrastructure as code.

**Specialization Boundaries:**
- ✅ Workflow files, build scripts, deployment automation
- ✅ Test automation, linting configuration, validation tooling
- ✅ Infrastructure provisioning, environment setup
- ❌ Business logic, UI implementation, content creation

**Key Directives:**
- 001: CLI & Shell Tooling
- 003: Repository Quick Reference
- 009: Role Capabilities

**Output Artifacts:**
- CI/CD workflows
- Automation scripts
- Infrastructure configurations
- Validation tooling

**Collaboration Model:**
- Consumes: Build requirements, quality standards, deployment specs
- Produces: Automation infrastructure, validation tooling
- Hands off to: Developers (integration), Curators (validation)

### 7. Researcher Pattern

**Purpose:** Information gathering, technology evaluation, feasibility analysis.

**Specialization Boundaries:**
- ✅ Market research, technology comparisons, best practice surveys
- ✅ Dependency analysis, security advisories, ecosystem trends
- ✅ Proof-of-concept evaluation, migration path analysis
- ❌ Final decisions, implementation, production changes

**Key Directives:**
- 004: Documentation & Context Files
- 006: Version Governance
- 010: Mode Protocol (analysis mode)

**Output Artifacts:**
- Research reports
- Technology comparison matrices
- Feasibility assessments
- Recommendation summaries

**Collaboration Model:**
- Consumes: Research questions, evaluation criteria
- Produces: Findings, recommendations, risk analysis
- Hands off to: Architects (decisions), Developers (implementation)

## Collaboration Patterns

### Pattern 1: Sequential Handoff

**Use Case:** Linear workflow where each agent completes its phase before the next begins.

**Example Flow:**
1. Architect produces ADR
2. Developer implements based on ADR
3. Writer documents implementation
4. Curator validates consistency

**Coordination Mechanism:**
- Status flags in `work/collaboration/`
- Explicit completion markers (✅)
- Next-agent tagging in progress logs

### Pattern 2: Parallel Execution

**Use Case:** Independent agents work on different aspects simultaneously.

**Example Flow:**
- Backend Developer works on API
- Frontend Developer works on UI
- Writer prepares user documentation
- All coordinate via shared progress logs

**Coordination Mechanism:**
- Role-specific directories in `work/`
- Shared context files (REPO_MAP, SURFACES)
- Daily sync summary in `work/collaboration/`

### Pattern 3: Iterative Refinement

**Use Case:** Agent produces initial output, curator validates, agent refines based on feedback.

**Example Flow:**
1. Writer creates documentation
2. Curator identifies inconsistencies
3. Writer updates based on LEX report
4. Curator re-validates

**Coordination Mechanism:**
- Draft markers (`FIRST PASS`)
- Validation reports with line-item feedback
- Version increments on refinement cycles

### Pattern 4: Expert Consultation

**Use Case:** Generalist agent encounters specialized question and defers to expert.

**Example Flow:**
1. Manager agent identifies architecture question
2. Manager requests Architect input via `work/collaboration/`
3. Architect provides ADR or recommendation
4. Manager incorporates guidance and proceeds

**Coordination Mechanism:**
- Explicit consultation requests with context
- Response files in `work/<consultant-role>/`
- Acknowledgment and integration confirmation

## Anti-Patterns to Avoid

### ❌ Boundary Violation

**Problem:** Agent operates outside its specialization area without escalation.

**Example:** Writer agent modifies build scripts, Developer agent creates ADRs.

**Impact:** Inconsistent quality, missed collaboration opportunities, unclear ownership.

**Mitigation:** Explicit escalation with ⚠️ marker, defer to appropriate specialist.

### ❌ Context Overload

**Problem:** Agent loads all directives "just in case" instead of selective loading.

**Example:** Writer agent loads tooling, versioning, and role capability directives when only needing templates.

**Impact:** Token waste, slower initialization, unnecessary cognitive overhead.

**Mitigation:** Load only directives listed in agent profile's reference table.

### ❌ Implicit Dependencies

**Problem:** Agents assume knowledge or outputs from other agents without explicit verification.

**Example:** Developer assumes architecture decisions exist without checking ADRs.

**Impact:** Misalignment, rework, inconsistent implementation.

**Mitigation:** Reference specific ADRs or design docs, escalate if missing.

### ❌ Silent Failure

**Problem:** Agent encounters issue but proceeds without reporting uncertainty.

**Example:** Curator finds validation issue but doesn't flag with ❗️.

**Impact:** Quality degradation, human reviewers unaware of risks.

**Mitigation:** Always use integrity markers (⚠️ ❗️) for uncertainties and errors.

### ❌ Template Divergence

**Problem:** Agent creates output format inconsistent with repository templates.

**Example:** Architect produces ADR without "Considered Alternatives" section.

**Impact:** Reduced maintainability, confusion for future readers, validation failures.

**Mitigation:** Always reference and follow templates from `docs/templates/`.

## Extending Specializations

### Creating a New Agent Profile

**Prerequisites:**
1. Identified need not covered by existing agents
2. Clear specialization boundary definition
3. Template selection from `docs/templates/automation/`

**Steps:**
1. **Define Purpose and Boundaries**
   - Primary focus areas
   - Secondary awareness areas
   - Explicit "avoid" list

2. **Identify Directive Dependencies**
   - Review manifest for relevant directives
   - Select minimal set needed for specialization
   - Document rationale for each selection

3. **Specify Output Artifacts**
   - Link to templates from `docs/templates/`
   - Define naming conventions
   - Specify validation criteria

4. **Establish Collaboration Contract**
   - What this agent consumes from others
   - What this agent produces for others
   - Handoff protocols and coordination mechanisms

5. **Set Mode Defaults**
   - Default reasoning mode (`/analysis-mode`, `/creative-mode`, etc.)
   - Mode transition triggers
   - Output labeling requirements

6. **Create Profile File**
   - Use `docs/templates/automation/NEW_SPECIALIST.agent.md`
   - Place in `.github/agents/<role>.agent.md`
   - Update `directives/005_agent_profiles.md`

7. **Validate Integration**
   - Test directive loading
   - Run validation script
   - Verify template references

## Success Metrics

Agent specialization patterns are effective when:

- ✅ Agents stay within defined boundaries >90% of the time
- ✅ Escalations are explicit and actionable
- ✅ Token usage remains within budget for each agent type
- ✅ Human review cycles are efficient (minimal rework)
- ✅ Handoffs between agents are smooth and well-documented
- ✅ Quality remains consistent across agent outputs

## Related Documentation

- Core Specification: [`AGENTS.md`](/AGENTS.md)
- Agent Profiles Directive: [`.github/agents/directives/005_agent_profiles.md`](/.github/agents/directives/005_agent_profiles.md)
- Role Capabilities Directive: [`.github/agents/directives/009_role_capabilities.md`](/.github/agents/directives/009_role_capabilities.md)
- Agent Audience Documentation: [`docs/audience/automation_agent.md`](/docs/audience/automation_agent.md)
- Architectural Vision: [`docs/architecture/architectural_vision.md`](architectural_vision.md)
- ADR-001 Modular Directive System: [`docs/architecture/ADR-001-modular-agent-directive-system.md`](adrs/ADR-001-modular-agent-directive-system.md)

---

_Prepared by: Architect Alphonso_  
_Mode: `/analysis-mode`_  
_Version: 1.0.0_
