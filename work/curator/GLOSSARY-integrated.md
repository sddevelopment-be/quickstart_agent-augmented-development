# Agent Framework Glossary

**Version:** 1.2.0  
**Last Updated:** 2026-02-10  
**Purpose:** Centralized definitions of common terminology used across agent profiles, directives, and documentation.

---

## Overview

This glossary provides standardized definitions for terms used throughout the SDD Agent Framework. These definitions ensure consistent understanding and communication across all agents, directives, and collaborative workflows.

For context on how to use this framework, see:

- [AGENTS.md](../AGENTS.md) - Core agent specification document
- [directives/](./directives/) - Extended directive set
- Agent profiles (e.g., [curator.agent.md](./curator.agent.md), [synthesizer.agent.md](./synthesizer.agent.md))

---

## Terms

### /analysis-mode

Reasoning mode focusing on systematic decomposition, structural analysis, and diagnostic evaluation; default mode for most agents

**Context:** Agent Modes - Reasoning  
**Source:** All agent profiles  
**Related:** /creative-mode, /meta-mode, Mode Protocol

### /creative-mode

Reasoning mode focusing on option generation, pattern shaping, alternative exploration, and narrative construction

**Context:** Agent Modes - Reasoning  
**Source:** All agent profiles  
**Related:** /analysis-mode, /meta-mode, Mode Protocol

### /meta-mode

Reasoning mode focusing on process reflection, alignment validation, governance review, and methodology evaluation

**Context:** Agent Modes - Reasoning  
**Source:** All agent profiles  
**Related:** /analysis-mode, /creative-mode, Mode Protocol

### 6-Phase Spec-Driven Implementation Flow

Complete workflow sequence through all six phases of Spec-Driven Development from analysis through review with explicit phase authority and handoff protocols

**Context:** Workflows - Spec-Driven Development  
**Source:** analyst-annie.agent.md, architect.agent.md, project-planner.agent.md  
**Related:** Spec-Driven Development, Phase Authority, Hand-off Protocol, Phase Checkpoint Protocol

### Acceptance Boundary

Explicit specification of when a system refuses, constrains, or safely degrades rather than accepting input

**Context:** System behavior specification  
**Source:** ATDD_adversarial-acceptance.tactic.md  
**Related:** Adversarial Acceptance Testing, Contract Decision

### Acceptance Criteria

Explicit, testable conditions that must be satisfied for a feature or requirement to be considered complete and acceptable

**Context:** Testing - Requirements  
**Source:** analyst-annie.agent.md, python-pedro.agent.md  
**Related:** ATDD, Phase 1 (Analysis), Executable Test, Specification

### Accuracy Score

Quantitative metric (percentage) measuring how accurately tests document system across three dimensions: Behavioral (WHAT), Architectural (WHY), Operational (HOW runs)

**Context:** Quality Validation / Metrics  
**Source:** reverse-speccing.md  
**Related:** Reverse Speccing, Behavioral Accuracy, Architectural Accuracy

### Adoption Rate

Percentage of domain terms in code/docs that use glossary terminology; target >80% for effective ubiquitous language

**Context:** Architecture - DDD / Metrics  
**Source:** living-glossary-practice.md  
**Related:** Living Glossary, Ubiquitous Language

### ADR Drafting Workflow

Systematic process for creating Architecture Decision Records with trade-off analysis and risk assessment

**Context:** Decision documentation  
**Source:** adr-drafting-workflow.tactic.md  
**Related:** Trade-off Analysis, Option Impact Matrix

### Adversarial Acceptance Testing

ATDD practice of deliberately exploring failure scenarios to define acceptance boundaries for misuse, edge cases, and unsafe defaults

**Context:** Testing methodology  
**Source:** ATDD_adversarial-acceptance.tactic.md  
**Related:** Acceptance Boundary, Adversarial Testing, Contract Decision

### Adversarial Testing

Stress-testing technique that deliberately attempts to make a proposal, design, or decision fail to surface weaknesses and blind spots

**Context:** Decision validation  
**Source:** adversarial-testing.tactic.md  
**Related:** Failure Scenario, Premortem Risk Identification

### AFK Mode

Autonomous operation protocol where agents work independently when human is away from keyboard, with clear decision boundaries and commit frequency expectations

**Context:** Agent autonomy  
**Source:** autonomous-operation-protocol.tactic.md  
**Related:** Decision Boundary, Commit Checkpoint, Escalation Protocol

### Agent Assignment

Process of selecting and routing specific tasks to the most appropriate specialized agent based on task type, required capabilities, and phase authority

**Context:** Orchestration - Task Routing  
**Source:** manager.agent.md  
**Related:** Manager Mike, Hand-off Protocol, Phase Authority, AGENT_STATUS

### Agent Profile

A specialized configuration file (
`.agent.md`) that defines an agent's purpose, specialization, collaboration contract, mode defaults, and directive usage. Profiles extend the base AGENTS.md specification with role-specific competencies.

**Location:** agent profile files  
**Reference:** Directive 005  
**Related:** Specialization, Collaboration Contract
### Agent Profile Handoff Patterns

Documentation in agent profiles of common handoff patterns observed in practice (outgoing, incoming, special cases) providing guidance without prescriptive rules

**Context:** Orchestration / Agent Coordination  
**Source:** agent-profile-handoff-patterns.md  
**Related:** Handoff Pattern, Organic Emergence

### AGENT_STATUS

Coordination artifact maintained by Manager Mike documenting which agent did what, when, and current workflow state

**Context:** Artifacts - Orchestration  
**Source:** manager.agent.md  
**Related:** Manager Mike, WORKFLOW_LOG, HANDOFFS, Agent Assignment

### Agentic Enablement

Capability shift where AI agents make previously labor-intensive practices tractable (continuous capture, multi-source pattern detection, incremental maintenance)

**Context:** Meta-Pattern / Technology Impact  
**Source:** language-first-architecture.md, living-glossary-practice.md  
**Related:** Feasibility Shift, Continuous Capture

### AMMERSE Analysis

Decision-making framework evaluating practices across seven dimensions: Agile, Minimal, Maintainable, Environmental, Reachable, Solvable, Extensible

**Context:** Trade-off analysis  
**Source:** ammerse-analysis.tactic.md  
**Related:** Trade-off Analysis, Contextual Fit

### AMMERSE Dimensions

Seven evaluation criteria for practices: Agile, Minimal, Maintainable, Environmental, Reachable, Solvable, Extensible

**Context:** Decision framework  
**Source:** ammerse-analysis.tactic.md  
**Related:** AMMERSE Analysis

### Analysis Paralysis

Endless validation or research without delivery due to perfectionism or risk aversion

**Context:** Process anti-pattern  
**Source:** requirements-validation-workflow.tactic.md  
**Related:** Time-boxing, Evidence-Based Requirements

### Analyst Annie

Requirements and validation specialist agent focused on producing testable, data-backed specifications with validated acceptance criteria

**Context:** Agent Roles - Requirements Analysis  
**Source:** analyst-annie.agent.md  
**Related:** Requirements Specialist, Specification-Driven Development, Phase 1 (Analysis), Validation Script

### Anti-Pattern Identification

Systematic extraction of behaviors to actively discourage, common traps, or misapplications of guidance from operational logs

**Context:** Framework Improvement / Quality Assurance  
**Source:** meta-analysis.md  
**Related:** Meta-Analysis, Pattern Detection

### API Contract

Explicit specification of API endpoints, request/response formats, error handling, versioning, and behavioral guarantees

**Context:** Backend Architecture - Interface Definition  
**Source:** backend-dev.agent.md  
**Related:** Backend Benny, Service Design, Integration Surface

### Architect Alphonso

Architecture specialist agent who clarifies complex systems with contextual trade-offs, creates ADRs, and provides system decomposition with explicit decision rationale

**Context:** Agent Roles - Architecture  
**Source:** architect.agent.md  
**Related:** Architecture Specialist, ADR, System Decomposition, Phase 2 (Architecture), Trade-off Analysis

### Architecture Blind Spot

Aspect of system design (rationale, deployment, operations, security) that tests naturally miss and must be documented elsewhere (typically ADRs)

**Context:** Quality Validation / Documentation Gap  
**Source:** reverse-speccing.md, test-readability-clarity-check.md  
**Related:** Reverse Speccing, Test-as-Documentation

### Architecture Specialist

Agent specialization focused on system decomposition, design interfaces, explicit decision records (ADRs), and trade-off analysis for complex systems

**Context:** Agent Specializations  
**Source:** architect.agent.md  
**Related:** Architect Alphonso, ADR, System Decomposition, Trade-off Analysis

### Audit Report

Structured document produced by Framework Guardian comparing installed framework state against canonical manifest, classifying files as MISSING, UNCHANGED, DIVERGED, or CUSTOM

**Context:** Artifacts - Framework Maintenance  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Manifest, Drift Detection, Framework Integrity

### Authorial Voice

Distinctive writing style, tone, rhythm, and personality of the original author that must be preserved during editing, translation, or curation

**Context:** Content Quality - Voice Preservation  
**Source:** lexical.agent.md, translator.agent.md, writer-editor.agent.md  
**Related:** Voice Fidelity, Tonal Integrity, Tone Preservation

### Backend Benny

Backend developer specialist agent focused on resilient service backends, integration surfaces, API design, and persistence strategy with traceable decisions

**Context:** Agent Roles - Backend Development  
**Source:** backend-dev.agent.md  
**Related:** Backend Developer Specialist, Service Design, API Contract, Persistence Strategy, Integration Surface

### Backend Developer Specialist

Agent specialization focused on API/service design, persistence strategy, performance budgets, failure-mode mapping, and backend architecture

**Context:** Agent Specializations  
**Source:** backend-dev.agent.md  
**Related:** Backend Benny, Service Design, Persistence Strategy, Performance Budget

### Baseline Option

"Do nothing" alternative that must be evaluated in trade-off analysis; current state may be acceptable, or organic emergence may solve issue naturally

**Context:** Development Methodology / Decision Framework  
**Source:** locality-of-change.md  
**Related:** Problem Assessment Protocol, Organic Emergence

### Batch Planning

Planning approach that breaks work into small, time-boxed batches (typically 1-2 weeks) rather than fixed-date commitments, enabling adaptive execution

**Context:** Planning - Execution Strategy  
**Source:** project-planner.agent.md  
**Related:** Planning Petra, NEXT_BATCH, Milestone Definition

### BDD Scenario

Behavior specification in Given/When/Then format describing observable outcomes in business-relevant language

**Context:** Behavior-driven development  
**Source:** development-bdd.tactic.md  
**Related:** Given-When-Then, Executable Specification

### Bidirectional Linking

Practice of maintaining links both forward (requirements → tests → code) and backward (code → tests → requirements) to enable navigation in both directions

**Context:** Development Methodology / Documentation  
**Source:** traceability-chain-pattern.md  
**Related:** Traceability Chain, Forward Link, Backward Link

### black

Opinionated Python code formatter ensuring consistent code style with PEP 8 compliance

**Context:** Python Development - Code Formatting  
**Source:** python-pedro.agent.md  
**Related:** Python Pedro, ruff, Code Quality

### Blast Radius

Scope of potential impact from experiment failure, deliberately contained through boundaries

**Context:** Risk containment  
**Source:** safe-to-fail-experiment-design.tactic.md  
**Related:** Experiment Boundary, Safe-to-Fail Experiment

### Bootstrap Bill

Repository scaffolding specialist agent who maps repository topology, generates structural artifacts (REPO_MAP, SURFACES, WORKFLOWS), and creates doctrine configuration for efficient multi-agent collaboration

**Context:** Agent Roles - Repository Initialization  
**Source:** bootstrap-bill.agent.md  
**Related:** Repository Scaffolding, Doctrine Configuration, REPO_MAP, Topology Mapping, Structural Artifact

### Boundary Signal

Indicator of context boundaries: event clusters that separate naturally, different actors, vocabulary divergence, or team responsibility shifts

**Context:** Context boundary detection  
**Source:** event-storming-discovery.tactic.md  
**Related:** Event Cluster, Context Boundary

### Bounded Context Linguistic Discovery

Technique for identifying hidden context boundaries by analyzing terminology patterns, communication structures, and semantic conflicts in existing systems

**Context:** Architecture - DDD  
**Source:** bounded-context-linguistic-discovery.md  
**Related:** Bounded Context, Semantic Conflict, Conway's Law Applied

### Branch Age Warning

Automated alert when feature branch exceeds age threshold (8h warning, 24h maximum) to enforce short-lived branch discipline

**Context:** Version Control / Automation  
**Source:** trunk-based-development.md  
**Related:** Short-Lived Branch, Trunk-Based Development

### Build Automation Specialist

Agent specialization focused on build graph modeling, CI/CD flow design, caching strategy, dependency integrity, and reproducible pipelines

**Context:** Agent Specializations  
**Source:** build-automation.agent.md  
**Related:** DevOps Danny, CI/CD Pipeline, Reproducible Build, Build Graph

### Build Graph

Directed acyclic graph representing build dependencies, execution order, caching boundaries, and artifact relationships in CI/CD pipeline

**Context:** Build Automation - Dependency Management  
**Source:** build-automation.agent.md  
**Related:** DevOps Danny, CI/CD Pipeline, Reproducible Build

### Bypass Check

Pre-execution verification that checks for LOCAL_ENV.md file containing environment-specific constraints or instructions before proceeding with standard directives

**Context:** Framework - Environment Configuration  
**Source:** Directive 001 (CLI and Shell Tooling)  
**Related:** LOCAL_ENV.md, Remediation Technique

### C4 Model

Lightweight hierarchical technique for structuring software architecture diagrams: Context (system+users), Container (deployable units), Component (internal modules), Code (implementation)

**Context:** Architecture / Diagramming  
**Source:** design_diagramming-incremental_detail.md  
**Related:** Incremental Detail Design, Progressive Disclosure

### Capability Boundary

Explicit definition of agent expertise boundaries - what they can and cannot do

**Context:** Agent specialization  
**Source:** agent-profile-creation.tactic.md  
**Related:** Agent Profile, Specialization

### Cherry-Picking Evidence

Ignoring claims that contradict preferences, undermining intellectual honesty

**Context:** Research anti-pattern  
**Source:** requirements-validation-workflow.tactic.md  
**Related:** Claim Inventory, Confirmation Bias

### Claim Classification

System for categorizing requirement claims by evidence type: Empirical (quantitative data), Observational (qualitative patterns), Theoretical (conceptual models), Prescriptive (best practices)

**Context:** Requirements Engineering  
**Source:** evidence-based-requirements.md  
**Related:** Evidence-Based Requirements, Testability Assessment

### Claim Inventory

Systematic catalog of verifiable assertions from research sources with evidence classification enabling testable requirements

**Context:** Evidence-based requirements  
**Source:** claim-inventory-development.tactic.md  
**Related:** Evidence Type, Testability Assessment, Traceability Chain

### Claim Relationship

Connections between claims: Supporting, Contradicting, Prerequisite, or Alternative explanations

**Context:** Knowledge modeling  
**Source:** claim-inventory-development.tactic.md  
**Related:** Claim Inventory, Claim Map

### Co-occurrence Analysis

Technique for clustering terminology by analyzing which terms appear together in the same files or contexts

**Context:** Linguistic analysis  
**Source:** code-documentation-analysis.tactic.md  
**Related:** Semantic Clustering, Terminology Extraction

### Code Reviewer Cindy

Review specialist agent focused on code quality, standards compliance, and traceability validation without making direct code modifications

**Context:** Agent Roles - Code Review  
**Source:** code-reviewer-cindy.agent.md  
**Related:** Review Specialist, Code Quality, Standards Compliance, Traceability Check

### Cognitive Complexity Budget

Implicit constraint that humans can internalize ~50-100 precise domain terms effectively; bounded contexts manage this complexity

**Context:** Architecture - DDD / Cognitive Science  
**Source:** bounded-context-linguistic-discovery.md  
**Related:** Bounded Context, Vocabulary Fragmentation

### Collaboration Contract

A section within each agent profile that specifies behavioral commitments, boundaries, escalation protocols, and interaction patterns with other agents and humans. Defines what the agent will and won't do.

**Related:** Agent Profile, Escalation
### Commit Checkpoint

Regular commit cadence (every 15-30 minutes) in autonomous work to create reversible progress points

**Context:** Version control practice  
**Source:** autonomous-operation-protocol.tactic.md  
**Related:** AFK Mode, Self-Observation Checkpoint

### Communication Frequency

Classification of team interaction cadence: Daily, Weekly, Monthly, or Rarely

**Context:** Organizational patterns  
**Source:** team-interaction-mapping.tactic.md  
**Related:** Team Interaction Mapping, Shared Artifact

### Complexity Creep

Cumulative effect where each small addition seems reasonable in isolation but together degrades system simplicity, making it harder to understand and maintain

**Context:** Development Methodology / Anti-Pattern  
**Source:** locality-of-change.md  
**Related:** Gold Plating, Premature Abstraction, Simplicity Preservation

### Component Patterns

Reusable UI component designs with established structure, behavior, styling, and composition rules for consistent interface development

**Context:** Frontend Architecture - Reusability  
**Source:** frontend.agent.md  
**Related:** Frontend Freddy, UI Architecture, Design System

### Concept Extraction

Refactoring that makes implicit or duplicated logic explicit by extracting it into a named abstraction

**Context:** Code improvement  
**Source:** refactoring-extract-first-order-concept.tactic.md  
**Related:** First-Order Concept, Rule of Three

### Confidence Threshold

Minimum confidence level required before acting on automated detection results to balance automation benefits against false positive risks

**Context:** Quality Assurance / Automation  
**Source:** living-glossary-practice.md  
**Related:** False Positives, Human Review Loop

### Conflict Classification

Process of categorizing upgrade conflicts as auto-merge candidates, local customizations to preserve, or breaking changes requiring manual review

**Context:** Agent Capabilities - Framework Maintenance  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Upgrade Plan, Core/Local Boundary

### Conflict Lead Time

Time from linguistic conflict detection to architectural issue manifestation; target <2 weeks (50% improvement over baseline)

**Context:** Architecture - DDD / Metrics  
**Source:** language-first-architecture.md  
**Related:** Linguistic Signal, Semantic Conflict

### Conflict Resolution Time

Metric measuring days from semantic conflict detection to resolution; target <7 days to prevent architectural drift

**Context:** Architecture - DDD / Metrics  
**Source:** language-first-architecture.md  
**Related:** Semantic Conflict, Linguistic Signal

### Confounding Variable

Alternative explanation for observed results that must be controlled in validation experiments

**Context:** Experimental design  
**Source:** requirements-validation-workflow.tactic.md  
**Related:** Validation Experiment, Multivariate Analysis

### Context Boundary Inference

Systematic detection of bounded context boundaries from team structure and terminology conflicts using Conway's Law principles

**Context:** DDD architectural analysis  
**Source:** context-boundary-inference.tactic.md  
**Related:** Conway's Law, Vocabulary Ownership, Semantic Boundary

### Context Carry-over

Undesired influence of previous iteration results on subsequent runs, introducing bias

**Context:** Execution quality issue  
**Source:** execution-fresh-context-iteration.tactic.md  
**Related:** Fresh Context Iteration

### Context Drift

Unacknowledged change in task goals, constraints, or assumptions during execution leading to scope creep

**Context:** Scope violation  
**Source:** context-establish-and-freeze.tactic.md  
**Related:** Frozen Context, Scope Creep

### Context Mapping

Practice of defining relationships between bounded contexts (Upstream/Downstream, Shared Kernel, Published Language, Conformist) with explicit terminology translation rules

**Context:** Architecture - DDD  
**Source:** bounded-context-linguistic-discovery.md  
**Related:** Bounded Context, Translation Layer

### Contextual Fit

Degree to which a solution aligns with organizational culture, constraints, and environmental factors

**Context:** Decision analysis  
**Source:** ammerse-analysis.tactic.md  
**Related:** AMMERSE Analysis, Environmental Dimension

### Continuous Capture

Automated observation and recording of terminology, decisions, or patterns in real-time as work happens, replacing big-bang manual efforts

**Context:** Meta-Pattern / Practice  
**Source:** living-glossary-practice.md  
**Related:** Agentic Enablement, Incremental Maintenance

### Contract Decision

Explicit determination of intended outcome for a failure scenario: prevent, reject, degrade, or tolerate

**Context:** Requirements specification  
**Source:** ATDD_adversarial-acceptance.tactic.md  
**Related:** Acceptance Boundary, Failure Scenario

### Contribution Rate

Percentage of glossary entries initiated by team members (not automation); target >50% indicating healthy ownership and engagement

**Context:** Architecture - DDD / Metrics  
**Source:** living-glossary-practice.md  
**Related:** Glossary Ownership, Living Glossary

### Conway's Law Applied

Application of Conway's Law to semantics—organizational communication structure predicts vocabulary structure; teams with infrequent communication develop different vocabularies

**Context:** Architecture - DDD / Organizational  
**Source:** bounded-context-linguistic-discovery.md  
**Related:** Bounded Context, Vocabulary Fragmentation

### Conway's Law Prediction

Hypothesis that semantic boundaries align with low-frequency communication boundaries between teams

**Context:** Organizational architecture  
**Source:** context-boundary-inference.tactic.md  
**Related:** Context Boundary, Team Communication Matrix

### Core/Local Boundary

Architectural separation between framework core files (managed by framework) and local customizations (managed by repository owner) to prevent silent overwrites

**Context:** Framework Architecture  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Conflict Classification, Local Customization

### Corrective Action Set

Minimal change proposals produced by Curator Claire to align artifacts without overhauling original content, preserving authorial voice

**Context:** Curation - Change Management  
**Source:** curator.agent.md  
**Related:** Curator Claire, Discrepancy Report, Minimal Change

### Coverage Assessment

Quarterly analysis of missing domain terms by comparing codebase terminology to glossary entries

**Context:** Glossary completeness  
**Source:** glossary-maintenance-workflow.tactic.md  
**Related:** Glossary Maintenance Workflow, Gap Closure Plan

### Coverage Threshold

Minimum percentage of code covered by tests required before code can be accepted; typically ≥80% for production code

**Context:** Quality Gates - Testing  
**Source:** python-pedro.agent.md, java-jenny.agent.md  
**Related:** Self-Review Protocol, Test Coverage, pytest, Quality Gate

### Cross-Reference Integrity

Validation that all internal links resolve correctly and referenced documents exist

**Context:** Documentation quality  
**Source:** documentation-curation-audit.tactic.md  
**Related:** Orphaned File, Documentation Curation Audit

### Curator Claire

Structural and tonal consistency specialist agent who maintains cross-document integrity, enforces doctrine stack boundaries, and prevents drift through systematic audits

**Context:** Agent Roles - Content Curation  
**Source:** curator.agent.md  
**Related:** Curator, Structural Consistency, Tonal Integrity, Doctrine Stack, Discrepancy Report, Source vs Distribution

### Decision Boundary

Classification of decision types as Minor (autonomous), Moderate (autonomous with note), or Critical (pause and escalate)

**Context:** Agent autonomy governance  
**Source:** autonomous-operation-protocol.tactic.md  
**Related:** AFK Mode, Escalation Protocol

### Decision Debt

Ratio of decision markers not yet promoted to formal ADRs; acceptable <20%, requires action >40%

**Context:** Development Methodology / Metrics  
**Source:** decision-first-development.md  
**Related:** Decision Marker, ADR Promotion

### Decision Marker

Structured inline annotation in code or documentation capturing architectural decision (what was decided, rationale, alternatives, consequences) with ADR reference

**Context:** Development Methodology / Documentation  
**Source:** decision-first-development.md  
**Related:** Decision-First Development, Traceable Decisions

### Decision Rule

Pre-defined interpretation logic for experiment results determining proceed, pivot, or abandon actions

**Context:** Experiment analysis  
**Source:** safe-to-fail-experiment-design.tactic.md  
**Related:** Success Criteria, Failure Criteria

### Decision-First Development

Development workflow where architectural decisions are captured systematically throughout the lifecycle, integrating decision rationale with artifacts to preserve "why" knowledge

**Context:** Development Methodology / Documentation  
**Source:** decision-first-development.md  
**Related:** Decision Marker, Decision Debt, Traceable Decisions

### Deep Creation Flow

Uninterrupted focus state with high cognitive load from problem-solving where agents stay passive and defer decision capture to session-end

**Context:** Development Methodology / Human-Agent Interaction  
**Source:** decision-first-development.md  
**Related:** Flow State Awareness, Decision Marker

### Definition Conflict Detection

Analysis process identifying same terms with different meanings across codebases or contexts

**Context:** Linguistic analysis  
**Source:** code-documentation-analysis.tactic.md  
**Related:** Semantic Conflict, Context Boundary

### Dependency Mapping

Process of identifying and documenting prerequisite relationships between tasks, ensuring correct execution sequence and preventing blockers

**Context:** Planning - Work Sequencing  
**Source:** project-planner.agent.md  
**Related:** Planning Petra, Task Breakdown, DEPENDENCIES

### Design System

Collection of reusable components, patterns, guidelines, and assets enabling consistent, scalable UI development

**Context:** Frontend Architecture - Consistency  
**Source:** frontend.agent.md  
**Related:** Frontend Freddy, Component Patterns, UI Architecture

### DevOps Danny

Build automation specialist agent who designs reproducible build, test, and release pipelines with documented runbooks and traceable deployment flows

**Context:** Agent Roles - Build Automation  
**Source:** build-automation.agent.md  
**Related:** Build Automation Specialist, CI/CD Pipeline, Reproducible Build, Deployment Pipeline, Release Automation

### Diagram Daisy

Diagramming specialist agent who transforms conceptual and architectural structures into semantically aligned diagram-as-code artifacts (Mermaid, PlantUML, Graphviz)

**Context:** Agent Roles - Visualization  
**Source:** diagrammer.agent.md  
**Related:** Diagramming Specialist, Diagram-as-Code, Semantic Fidelity, Visual Representation

### Diagram-as-Code

Practice of creating diagrams using text-based formats (Mermaid, PlantUML, Graphviz) for version control, reproducibility, and semantic fidelity

**Context:** Agent Capabilities - Visualization  
**Source:** diagrammer.agent.md  
**Related:** Diagram Daisy, Semantic Fidelity, Mermaid, PlantUML

### Dictionary DDD

Anti-pattern where teams create glossary document, consider DDD "done," never update it; glossary becomes stale immediately with no ownership

**Context:** Architecture - DDD / Anti-Pattern  
**Source:** living-glossary-practice.md  
**Related:** Living Glossary, Glossary Ownership

### Directive Adherence Lapse

Skipping required procedures because documentation feels like overhead

**Context:** Process violation  
**Source:** phase-checkpoint-protocol.md  
**Related:** Phase Checkpoint Protocol

### Discrepancy Report

Artifact produced by Curator Claire outlining detected inconsistencies across documents, their locations, and recommended corrective actions

**Context:** Artifacts - Curation  
**Source:** curator.agent.md  
**Related:** Curator Claire, Corrective Action Set, Structural Consistency

### doc_root

Path variable in doctrine configuration pointing to documentation root directory (default 'docs') where architectural docs, guides, and reference materials reside

**Context:** Configuration - Path Variables  
**Source:** bootstrap-bill.agent.md  
**Related:** Doctrine Configuration, workspace_root, spec_root, output_root

### Doctrine Configuration

YAML configuration file (.doctrine/config.yaml) that defines path variables (workspace_root, doc_root, spec_root, output_root) and repository metadata for doctrine framework integration

**Context:** Artifacts - Repository Configuration  
**Source:** bootstrap-bill.agent.md  
**Related:** Bootstrap Bill, Path Variable, workspace_root, doc_root, spec_root

### Documentation Curation Audit

Systematic audit of directory structure, naming conventions, cross-references, and metadata completeness

**Context:** Documentation quality  
**Source:** documentation-curation-audit.tactic.md  
**Related:** Structural Consistency, Cross-Reference Integrity

### Domain Event

Business-significant state change named in past tense (e.g., OrderPlaced, PaymentReceived, ShipmentCompleted)

**Context:** Event-driven design  
**Source:** event-storming-discovery.tactic.md  
**Related:** Event Storming, Event Cluster

### Drift Detection

Process of identifying divergence between installed framework files and canonical manifest through checksum comparison and file classification

**Context:** Agent Capabilities - Framework Maintenance  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Manifest, Audit Report, Framework Integrity

### Dual-Level Error Feedback

Error reporting pattern providing generic user-facing messages and detailed internal diagnostic logs

**Context:** Error communication  
**Source:** input-validation-fail-fast.tactic.md  
**Related:** Fail-Fast Validation, Reference Number

### Dual-Trunk Model

Low-trust variant where agents commit to agent-trunk branch, humans review PRs to main, providing safety net during agent adoption phase

**Context:** Version Control / Trust Model  
**Source:** trunk-based-development.md  
**Related:** Trunk-Based Development, Human Review Gate

### Economic Feasibility

Analysis of whether practice is economically viable given current costs (labor, tooling, time) versus benefits delivered

**Context:** Meta-Pattern / Decision Framework  
**Source:** living-glossary-practice.md  
**Related:** Feasibility Shift, ROI Threshold

### Editor Eddy

Writer and editor specialist agent who revises existing content for tone, clarity, and alignment while preserving factual integrity and authorial rhythm

**Context:** Agent Roles - Editorial  
**Source:** writer-editor.agent.md  
**Related:** Writer-Editor, Editorial Specialist, Paragraph-Level Refinement, Voice Alignment, Boy Scout Rule

### Editorial Review

Review dimension focused on clarity, readability, style consistency, grammar, terminology alignment, and appropriate tone

**Context:** Quality Assurance - Review Types  
**Source:** reviewer.agent.md  
**Related:** Review Dimensions, Style Consistency, Terminology, Glossary

### Enforcement Tier

Graduated enforcement levels for glossary terms: Advisory (suggest), Acknowledgment Required (warn), Hard Failure (block), chosen per term based on criticality

**Context:** Architecture - DDD / Governance  
**Source:** living-glossary-practice.md  
**Related:** Living Glossary, Glossary Ownership

### Escalation

The process of flagging issues, uncertainties, or conflicts that require human intervention or inter-agent coordination. Escalation uses integrity markers (❗️, ⚠️) and follows protocols defined in Directive 011.

**Reference:** Directive 011  
**Related:** Integrity Symbol, Risk
### Escalation Protocol

Procedure for pausing autonomous work and documenting critical decisions requiring human guidance

**Context:** Agent autonomy governance  
**Source:** autonomous-operation-protocol.tactic.md  
**Related:** Decision Boundary, AFK Mode

### Establish and Freeze Context

Tactic requiring explicit context clarification before work begins, then freezing that context for task duration to prevent scope drift

**Context:** Work initiation discipline  
**Source:** context-establish-and-freeze.tactic.md  
**Related:** Frozen Context, Context Drift, Goals and Non-Goals

### Event Cluster

Natural grouping of related domain events indicating potential bounded context boundaries

**Context:** DDD discovery  
**Source:** event-storming-discovery.tactic.md  
**Related:** Domain Event, Event Storming

### Event Storming

Collaborative workshop technique using sticky notes to discover domain events, processes, and bounded context boundaries

**Context:** DDD discovery methodology  
**Source:** event-storming-discovery.tactic.md  
**Related:** Domain Event, Event Cluster, Boundary Signal

### Event Storming Sticky Colors

Color-coding system: Orange=events, Blue=actors, Purple=policies, Light Blue=commands

**Context:** Workshop visualization  
**Source:** event-storming-discovery.tactic.md  
**Related:** Event Storming

### Evidence Theater

Collecting evidence to justify pre-decided requirements rather than genuinely testing hypotheses

**Context:** Research anti-pattern  
**Source:** requirements-validation-workflow.tactic.md  
**Related:** Claim Inventory, Intellectual Honesty

### Evidence Type

Classification of claim support: Empirical (quantitative), Observational (qualitative), Theoretical (conceptual), or Prescriptive (best practices)

**Context:** Research methodology  
**Source:** claim-inventory-development.tactic.md  
**Related:** Claim Inventory, Confidence Level

### Evidence-Based Requirements

Requirements analysis approach grounding all claims in verifiable evidence with classified evidence types (Empirical, Observational, Theoretical, Prescriptive)

**Context:** Requirements Engineering / Research Method  
**Source:** evidence-based-requirements.md  
**Related:** Claim Classification, Testability Assessment, Requirements Validation

### Executable Test

Automated test that validates acceptance criteria through code execution, providing verifiable evidence of requirement satisfaction

**Context:** Testing - Automation  
**Source:** python-pedro.agent.md, backend-dev.agent.md  
**Related:** ATDD, Acceptance Criteria, Phase 4 (Acceptance Tests)

### Experiment Boundary

Explicit scope, duration, resource, and audience limits containing risk of experimentation

**Context:** Experiment design  
**Source:** safe-to-fail-experiment-design.tactic.md  
**Related:** Safe-to-Fail Experiment, Blast Radius

### Expert Review (Testing)

Second phase of reverse speccing where Agent B validates reconstruction against ground truth with full context access

**Context:** Test validation procedure  
**Source:** test-to-system-reconstruction.tactic.md  
**Related:** Naive Reconstruction, Accuracy Assessment

### Export Pipeline

Automated process (npm run export:all, npm run deploy:all) that transforms doctrine/ source content into tool-specific distribution formats with semantic preservation

**Context:** Doctrine Stack - Distribution  
**Source:** curator.agent.md  
**Related:** Source vs Distribution, Format Transformation, Semantic Preservation

### External Aggregation

Result consolidation performed outside execution loop to maintain iteration independence

**Context:** Data processing pattern  
**Source:** execution-fresh-context-iteration.tactic.md  
**Related:** Fresh Context Iteration

### External Memory

Storage location (work/notes/external_memory/) for offloaded task-specific details, allowing agents to swap context in/out while maintaining core behavioral norms

**Context:** Framework - Context Management  
**Source:** Directive 002 (Context Notes), Directive 003 (Repository Structure)  
**Related:** Token Discipline, Context Layer

### Extract Before Interpret

Analysis discipline that separates observable fact extraction from meaning assignment to prevent premature interpretation bias

**Context:** Analysis methodology  
**Source:** analysis-extract-before-interpret.tactic.md  
**Related:** Extraction Phase, Interpretation Phase

### Extraction Phase

First step of analysis where observable elements are extracted verbatim without judgment or conclusions

**Context:** Analysis procedure  
**Source:** analysis-extract-before-interpret.tactic.md  
**Related:** Extract Before Interpret, Interpretation Phase

### Fail-Fast Validation

Input validation strategy halting at first failure rather than continuing through all checks

**Context:** Error handling pattern  
**Source:** input-validation-fail-fast.tactic.md  
**Related:** Validation Sequence, Dual-Level Error Feedback

### Failure Scenario

Concrete description of how a feature could fail, including trigger, manifestation, and likely cause

**Context:** Risk analysis  
**Source:** ATDD_adversarial-acceptance.tactic.md  
**Related:** Adversarial Testing, Premortem Analysis

### Fallback Strategy

Alternative approach when preferred tooling (fd, rg, ast-grep, etc.) is unavailable, using universally available alternatives (find, grep) with equivalent functionality

**Context:** Framework - Tooling  
**Source:** Directive 013 (Tooling Setup & Fallbacks)  
**Related:** Tool Suite, Escalation

### False Boundaries

Context boundaries that cut across natural process flows due to organizational politics or technical convenience rather than semantic divisions

**Context:** Architecture - DDD / Failure Mode  
**Source:** bounded-context-linguistic-discovery.md  
**Related:** Bounded Context, Event Storming Validation

### False Positives

Failure mode where automated detection produces low-quality outputs (overaggressive, poor context awareness), damaging trust in tooling

**Context:** Quality Assurance / Failure Mode  
**Source:** living-glossary-practice.md, language-first-architecture.md  
**Related:** Confidence Threshold, Human Review Loop

### Falsifiable Hypothesis

Testable prediction restated from a claim in If-Then-Because format with measurable outcomes

**Context:** Scientific method application  
**Source:** requirements-validation-workflow.tactic.md  
**Related:** Validation Experiment, Success Criteria

### Feasibility Shift

Transformation where previously infeasible practice becomes operationally viable due to technological change (e.g., agentic systems enabling continuous linguistic monitoring)

**Context:** Meta-Pattern / Technology Impact  
**Source:** language-first-architecture.md, living-glossary-practice.md  
**Related:** Economic Feasibility, Agentic Enablement

### File-Based Orchestration

Coordination pattern using YAML task files and Git commits to enable asynchronous multi-agent workflows without queues, servers, or network dependencies

**Context:** Orchestration / Coordination Pattern  
**Source:** file-based-orchestration.md, work-directory-orchestration.md  
**Related:** Task Lifecycle, Work Directory Model, Asynchronous Coordination

### Finding Summary

Executive summary component of review report highlighting critical issues, key findings, and top recommendations for quick stakeholder assessment

**Context:** Quality Assurance - Reporting  
**Source:** reviewer.agent.md  
**Related:** Reviewer, Review Report, Review Dimensions

### First-Order Concept

Extracted abstraction representing a clear domain or technical concept with single, well-defined responsibility

**Context:** Refactoring pattern  
**Source:** refactoring-extract-first-order-concept.tactic.md  
**Related:** Concept Extraction, Single Responsibility

### Flaky Terminal Behavior

Unreliable or inconsistent terminal/shell interactions in agent-based workflows that require remediation techniques to ensure reliable command execution

**Context:** Framework - Terminal Operations  
**Source:** Directive 001 (CLI and Shell Tooling)  
**Related:** Remediation Technique

### Flow State Awareness

Practice of adapting decision capture behavior to human productivity rhythms: Deep Creation (defer), Agent Collaboration (real-time), Reflection/Synthesis (batch)

**Context:** Development Methodology / Human-Agent Interaction  
**Source:** decision-first-development.md  
**Related:** Decision-First Development, Deep Creation Flow

### Framework Guardian

Framework integrity specialist agent who audits framework installations against canonical manifests, detects drift, and guides safe upgrades while preserving local customizations

**Context:** Agent Roles - Framework Maintenance  
**Source:** framework-guardian.agent.md  
**Related:** Framework Integrity, Manifest Audit, Drift Detection, Upgrade Plan, Core/Local Boundary

### Framework Integrity

State where installed framework files match canonical manifest specifications without unauthorized modifications or drift

**Context:** Framework Maintenance - Quality  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Manifest, Drift Detection, Audit Report

### Fresh Context Iteration

Execution pattern running single instruction repeatedly in fresh context with no memory between runs

**Context:** Deterministic execution  
**Source:** execution-fresh-context-iteration.tactic.md  
**Related:** Context Carry-over, External Aggregation

### Frontend Freddy

Front-end specialist agent integrating design, technical architecture, and usability reasoning for coherent UI systems with maintainable component patterns

**Context:** Agent Roles - Frontend Development  
**Source:** frontend.agent.md  
**Related:** Frontend Specialist, UI Architecture, Component Patterns, State Boundaries, Design System

### Frozen Context

Agreed-upon goals, constraints, and assumptions that remain fixed during task execution unless explicitly renegotiated

**Context:** Scope management  
**Source:** context-establish-and-freeze.tactic.md  
**Related:** Establish and Freeze Context, Context Drift

### Given-When-Then

BDD scenario structure: Given (context), When (action), Then (expected outcome)

**Context:** Specification format  
**Source:** development-bdd.tactic.md  
**Related:** BDD Scenario, Observable Behavior

### Glossary as Executable Artifact

Mental model treating glossary not as documentation but as living infrastructure with continuous updates, clear ownership, workflow integration, and tiered enforcement

**Context:** Architecture - DDD / Mental Model  
**Source:** living-glossary-practice.md  
**Related:** Living Glossary, Enforcement Tier, Glossary Ownership

### Glossary as Power Tool

Failure mode where centralized control over terminology becomes organizational power lever rather than tool for shared understanding

**Context:** Organizational / Failure Mode  
**Source:** living-glossary-practice.md  
**Related:** Linguistic Policing, Weaponized Standards

### Glossary Maintenance Workflow

Four-cycle process: Continuous Capture → Weekly Triage → Quarterly Health Check → Annual Governance Retrospective

**Context:** Living glossary operations  
**Source:** glossary-maintenance-workflow.tactic.md  
**Related:** Glossary Triage, Staleness Audit, Coverage Assessment

### Glossary Ownership

Assignment of responsibility for terminology decisions to specific context owners (team leads, domain experts, architects) per bounded context

**Context:** Architecture - DDD / Governance  
**Source:** living-glossary-practice.md  
**Related:** Living Glossary, Bounded Context, Human in Charge

### Glossary Triage

Weekly 30-minute session reviewing agent-generated candidates and making approve/reject/defer/merge decisions

**Context:** Glossary workflow  
**Source:** glossary-maintenance-workflow.tactic.md  
**Related:** Glossary Maintenance Workflow, Context Owner

### Goals and Non-Goals

Explicit declaration of what a task is expected to achieve AND what is deliberately out of scope

**Context:** Task scoping  
**Source:** context-establish-and-freeze.tactic.md  
**Related:** Establish and Freeze Context

### Gold Plating

Anti-pattern of adding features, abstractions, or optimizations "just in case" or "for completeness" without evidence of actual need

**Context:** Development Methodology / Anti-Pattern  
**Source:** locality-of-change.md  
**Related:** Locality of Change, Premature Abstraction, Complexity Creep

### Gold-plating

Anti-pattern of opportunistic improvements beyond stated goal (while-I'm-here syndrome)

**Context:** Scope violation  
**Source:** change-apply-smallest-viable-diff.tactic.md  
**Related:** Scope Creep, Smallest Viable Diff

### Graceful Degradation

Principle of providing fallback strategies for every tool to ensure agents can operate even when preferred tools unavailable

**Context:** Development Environment / Resilience  
**Source:** tooling-setup-best-practices.md  
**Related:** Tool Selection Rigor, Fallback Strategy

### GREEN Phase

TDD/ATDD workflow state where tests pass after implementation, validating correct behavior

**Context:** Test-driven development  
**Source:** 6-phase-spec-driven-implementation-flow.md  
**Related:** RED Phase, Implementation Phase

### Hand-off

Explicit transfer of responsibility from one agent to another at phase boundaries, documented in commit messages

**Context:** SDD workflow coordination  
**Source:** 6-phase-spec-driven-implementation-flow.md  
**Related:** Phase Checkpoint Protocol, Phase Declaration

### Hand-off Protocol

Structured process for transferring work between agents in a multi-agent workflow, specifying what artifacts are ready, which agent receives them, and validation criteria

**Context:** Agent Collaboration  
**Source:** analyst-annie.agent.md, architect.agent.md, project-planner.agent.md  
**Related:** Phase Authority, Spec-Driven Development, Agent Assignment, HANDOFFS.md

### Handoff Pattern

Workflow where completing agent encodes follow-up work via result.next_agent block, orchestrator creates new task, copies context/artefacts for seamless continuation

**Context:** Orchestration / Workflow  
**Source:** work-directory-orchestration.md, agent-profile-handoff-patterns.md  
**Related:** File-Based Orchestration, Agent Coordination, Task Chain

### HANDOFFS

Coordination artifact documenting which work products are ready for which next agent in the workflow

**Context:** Artifacts - Orchestration  
**Source:** manager.agent.md  
**Related:** Manager Mike, Hand-off Protocol, Agent Assignment

### Hard Limit

Concrete resource boundary (financial, time, physical, mental, moral, social) triggering immediate stop

**Context:** Boundary enforcement  
**Source:** stopping-conditions.tactic.md  
**Related:** Stopping Condition, Trigger Declaration

### High-Value Feedback

Review feedback that is specific, categorized by severity, and respectful of author context

**Context:** Review quality  
**Source:** review-intent-and-risk-first.tactic.md  
**Related:** Intent-First Review, Low-Noise Feedback

### Human in Charge

A governance principle emphasizing that humans retain ultimate responsibility, authority, and decision-making power in agent-augmented workflows. Distinct from "human in the loop" (which focuses on oversight/approval), "human in charge" explicitly centers human accountability and intervention rights. The human in charge bears responsibility for work outcomes and maintains authority to override, redirect, or halt agentic operations at any point.

**Key distinctions from "human in the loop":**
- **Responsibility:** Human bears accountability for outcomes, not just oversight
- **Authority:** Power to make significant decisions and interventions
- **Control:** Ability to halt, redirect, or override agent operations
- **Ownership:** Ultimate arbiter of quality, direction, and delivery

**Practical implications:**
- Agents request permission for high-impact changes
- Humans retain approval authority over critical decisions
- Agents escalate uncertainty or risk immediately
- Human judgment overrides agent recommendations when conflicting

**Reference:** Directive 026 (Commit Protocol), Directive 011 (Risk & Escalation)  
**Related:** Escalation, Alignment, Collaboration Contract
### Human Review Loop

Process where automated detection surfaces candidates but humans make final decisions, maintaining accountability and avoiding automation bias

**Context:** Quality Assurance / Governance  
**Source:** living-glossary-practice.md  
**Related:** Human in Charge, Confidence Threshold

### Impact Analysis

Process of identifying affected artifacts (tests, code, documentation) when requirements change, enabled by traceability chain links

**Context:** Development Methodology / Change Management  
**Source:** traceability-chain-pattern.md  
**Related:** Traceability Chain, Bidirectional Linking

### Incremental Detail Design

C4 model approach using hierarchical abstraction layers (Context, Container, Component, Code) for progressive disclosure of technical detail

**Context:** Architecture / Diagramming  
**Source:** design_diagramming-incremental_detail.md  
**Related:** C4 Model, Progressive Disclosure, Abstraction Layer

### Incremental Maintenance

Practice of making small, frequent updates to living artifacts (glossaries, ADRs, specs) rather than periodic big-bang efforts

**Context:** Meta-Pattern / Practice  
**Source:** living-glossary-practice.md  
**Related:** Continuous Capture, Living Glossary

### Incremental Review

Code review practice examining changes without expanding scope or rewriting implementation

**Context:** Review discipline  
**Source:** code-review-incremental.tactic.md  
**Related:** Review Boundary, Locality of Change

### Inside Boundary (Testing)

Components directly responsible for feature logic that should NOT be mocked in tests

**Context:** Unit testing scope  
**Source:** test-boundaries-by-responsibility.tactic.md  
**Related:** Outside Boundary, Test Boundary

### Integration Surface

Set of APIs, protocols, data formats, and contracts through which a system interacts with external systems or services

**Context:** Backend Architecture - External Integration  
**Source:** backend-dev.agent.md, bootstrap-bill.agent.md  
**Related:** Backend Benny, Bootstrap Bill, API Contract, SURFACES

### Intent-First Review

Review discipline summarizing apparent intent before identifying risks or suggesting changes

**Context:** Code review methodology  
**Source:** review-intent-and-risk-first.tactic.md  
**Related:** Risk Categorization, High-Value Feedback

### Interpretation Phase

Second step of analysis where meaning is assigned to previously extracted facts as a separate, explicit activity

**Context:** Analysis procedure  
**Source:** analysis-extract-before-interpret.tactic.md  
**Related:** Extraction Phase, Extract Before Interpret

### Java Jenny

Java development specialist agent focused on code quality, style enforcement, and testing standards using Maven and Java ecosystem tooling

**Context:** Agent Roles - Java Development  
**Source:** java-jenny.agent.md  
**Related:** Java Specialist, Code Quality, Maven, JVM Ecosystem, Test-First Development

### Knowledge Encoding

Documentation of lessons in discoverable locations (tactics, directives, templates, guidelines)

**Context:** Organizational learning  
**Source:** reflection-post-action-learning-loop.tactic.md  
**Related:** Lesson Extraction, Post-Action Learning Loop

### Language-First Architecture

Architectural approach treating language drift as an early signal of deeper architectural problems, recognizing that linguistic fragmentation predicts system issues

**Context:** Architecture - DDD / Ubiquitous Language  
**Source:** language-first-architecture.md  
**Related:** Linguistic Signal, Bounded Context, Ubiquitous Language

### Layer Boundary

Separation between doctrine stack layers (Guidelines, Approaches, Directives, Tactics, Templates) that must be respected to prevent content type mixing

**Context:** Doctrine Stack - Architecture  
**Source:** curator.agent.md  
**Related:** Doctrine Stack, Curator Claire, Guideline, Approach, Directive, Tactic

### Lesson Extraction

Identification of 1-3 concrete, actionable insights from completed work

**Context:** Learning practice  
**Source:** reflection-post-action-learning-loop.tactic.md  
**Related:** Post-Action Learning Loop, Knowledge Encoding

### LEX_DELTAS

Minimal diff artifact produced by Lexical Larry showing suggested edits grouped by rule violated, ready for patch application

**Context:** Artifacts - Style Analysis  
**Source:** lexical.agent.md  
**Related:** Lexical Larry, LEX_REPORT, Minimal Diff, Rule Violation

### LEX_REPORT

Lexical analysis artifact documenting per-file style compliance (tone, rhythm, markdown hygiene) with rule violation annotations

**Context:** Artifacts - Style Analysis  
**Source:** lexical.agent.md  
**Related:** Lexical Larry, LEX_DELTAS, LEX_TONE_MAP, Style Compliance

### LEX_TONE_MAP

Medium detection artifact showing which writing medium (Pattern, Podcast, LinkedIn, Essay) applies to each file with confidence scores

**Context:** Artifacts - Style Analysis  
**Source:** lexical.agent.md  
**Related:** Lexical Larry, Medium Detection, Tone Fidelity

### Lexical Larry

Lexical analyst specialist agent who evaluates writing style compliance (tone, rhythm, formatting) while preserving authorial voice through minimal, rule-grounded edits

**Context:** Agent Roles - Style Analysis  
**Source:** lexical.agent.md  
**Related:** Lexical Analyst, Style Compliance, Tone Fidelity, Authorial Voice, LEX_REPORT

### Lexical Style Diagnostic

Analysis of documentation for style inconsistencies, readability issues, and tone misalignments

**Context:** Writing quality  
**Source:** lexical-style-diagnostic.tactic.md  
**Related:** Readability Scoring, Tone Consistency, Minimal Diff

### Linguistic Policing

Failure mode where glossary enforcement becomes compliance regime instead of shared understanding, often due to punitive enforcement or centralized authority

**Context:** Architecture - DDD / Failure Mode  
**Source:** living-glossary-practice.md, language-first-architecture.md  
**Related:** Enforcement Tier, Glossary as Power Tool

### Linguistic Signal

Observable pattern in terminology usage that indicates potential architectural problems before they manifest in code or process failures

**Context:** Architecture - DDD  
**Source:** language-first-architecture.md  
**Related:** Language-First Architecture, Vocabulary Fragmentation, Semantic Conflict

### Living Glossary

Continuously updated, executable glossary treated as infrastructure rather than static documentation, evolving with code and domain understanding

**Context:** Architecture - DDD / Documentation Practice  
**Source:** living-glossary-practice.md  
**Related:** Ubiquitous Language, Bounded Context, Glossary as Executable Artifact

### Living Specification

Specification that evolves during development as understanding grows, then freezes when feature complete to become reference documentation

**Context:** Development Methodology - SDD  
**Source:** spec-driven-development.md  
**Related:** Specification-Driven Development, Specification Lifecycle

### Local Customization

Repository-specific modifications to framework files or addition of custom files that must be preserved during framework upgrades

**Context:** Framework Maintenance - Customization  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Core/Local Boundary, Conflict Classification

### Locality of Change

A design principle emphasizing that changes should be measured against actual problems, not hypothetical concerns. Agents must verify problem existence, quantify severity, and prefer simple solutions over architectural enhancements. Discourages gold plating, premature abstraction, and complexity creep.

**Reference:** Directive 020, `approaches/locality-of-change.md`  
**Related:** Risk, Escalation, Alignment
### Manager Mike

Coordination specialist agent who routes tasks to appropriate agents, maintains workflow status maps, and prevents conflicting edits through file-based orchestration

**Context:** Agent Roles - Orchestration  
**Source:** manager.agent.md  
**Related:** Coordinator, Task Router, Workflow Status, Hand-off Tracking, AGENT_STATUS

### Manifest

Canonical list of framework files with checksums and metadata defining expected installation state for drift detection

**Context:** Framework Maintenance - Source of Truth  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Framework Integrity, Drift Detection

### Medium Detection

Process of identifying which writing medium (Pattern, Podcast, LinkedIn, Essay) applies to content based on style patterns and tone markers

**Context:** Agent Capabilities - Style Analysis  
**Source:** lexical.agent.md  
**Related:** Lexical Larry, LEX_TONE_MAP, Tone Fidelity

### Meta-Analysis

Periodic analysis of work logs, prompt assessments, and operational patterns to surface systemic framework improvements and identify recurring issues

**Context:** Framework Improvement / Operational Practice  
**Source:** meta-analysis.md  
**Related:** Pattern Detection, Anti-Pattern Identification, Framework Evolution

### Meta-Awareness

Agent capability to observe and reason about its own execution state, recognize problematic patterns, and make course corrections before completing tasks

**Context:** Agent Behavior / Self-Observation  
**Source:** ralph-wiggum-loop.md  
**Related:** Ralph Wiggum Loop, Meta-Mode

### Metadata Header

Structured front matter in tactic files: Invoked By, Related Tactics, Complements

**Context:** Tactic documentation  
**Source:** tactics-curation.tactic.md  
**Related:** Tactics Curation, Relationship Tracking

### Milestone Definition

Planning artifact that establishes significant checkpoints with goals, themes, decision gates, and validation hooks while remaining resilient to change

**Context:** Planning - Goal Setting  
**Source:** project-planner.agent.md  
**Related:** Planning Petra, PLAN_OVERVIEW, Batch Planning

### Minimal Patch

Smallest possible code or configuration change required to resolve an issue, upgrade conflict, or implement a fix without unnecessary modifications

**Context:** Development - Change Management  
**Source:** framework-guardian.agent.md, python-pedro.agent.md  
**Related:** Framework Guardian, Locality of Change, Upgrade Plan

### Mitigation Strategy

Concrete plan defining prevention actions, detection signals, and response procedures for a failure scenario

**Context:** Risk management  
**Source:** premortem-risk-identification.tactic.md  
**Related:** Premortem Risk Identification, Failure Scenario

### Momentum Bias

Failure mode where agents skip phases or roles blur due to pressure to keep moving forward without proper validation or hand-off

**Context:** Development Methodology - Anti-Pattern  
**Source:** spec-driven-6-phase-cycle.md  
**Related:** Six-Phase Cycle, Role Confusion

### Momentum Bias Trap

Tendency to continue work into next phase without proper checkpoint due to task momentum

**Context:** Workflow violation  
**Source:** phase-checkpoint-protocol.md  
**Related:** Phase Skipping, Phase Checkpoint Protocol

### mypy

Static type checker for Python that validates type hints and detects type-related errors before runtime

**Context:** Python Development - Type Safety  
**Source:** python-pedro.agent.md  
**Related:** Python Pedro, Type Hints, Type Checking

### Naive Reconstruction

Phase where analyst with NO external context reads only tests to infer system behavior, data structures, workflows, and edge cases

**Context:** Quality Validation / Testing  
**Source:** reverse-speccing.md  
**Related:** Reverse Speccing, Test-as-Documentation

### NEXT_BATCH

Planning artifact containing small batch of concrete, ready-to-run tasks for immediate execution (typically 1-2 weeks of work)

**Context:** Artifacts - Planning  
**Source:** project-planner.agent.md  
**Related:** Planning Petra, PLAN_OVERVIEW, Batch Planning, Task Breakdown

### Observable Behavior

System outcomes verifiable without knowledge of implementation details

**Context:** Testing principle  
**Source:** development-bdd.tactic.md  
**Related:** BDD Scenario, Behavioral Contract

### Offloading

The act of moving detailed context (notes, enumerations, specifics) from active agent memory into external files to conserve token budget while maintaining reference capability

**Context:** Framework - Context Management  
**Source:** Directive 002 (Context Notes)  
**Related:** Token Discipline, External Memory

### Option Impact Matrix

Qualitative scoring of alternatives against impact areas (performance, maintainability, etc.)

**Context:** Decision analysis  
**Source:** adr-drafting-workflow.tactic.md  
**Related:** ADR Drafting Workflow, Trade-off Analysis

### Organic Emergence

Principle of letting patterns emerge naturally from observed practice before codifying them, rather than prescribing patterns prematurely

**Context:** Meta-Pattern / Design Principle  
**Source:** agent-profile-handoff-patterns.md, locality-of-change.md  
**Related:** Pattern Before Prescription, Premature Abstraction

### Orphaned Artifact

Code, test, or documentation with no traceable link to requirements, specifications, or architectural decisions, making purpose and validity unclear

**Context:** Development Methodology / Anti-Pattern  
**Source:** traceability-chain-pattern.md  
**Related:** Traceability Chain, Documentation Debt

### Orphaned File

Document with no parent README reference or incoming links, reducing discoverability

**Context:** Documentation structure  
**Source:** documentation-curation-audit.tactic.md  
**Related:** Cross-Reference Integrity, Structural Consistency

### output_root

Path variable in doctrine configuration pointing to generated artifacts directory (default 'output') for build products, reports, and exports

**Context:** Configuration - Path Variables  
**Source:** bootstrap-bill.agent.md  
**Related:** Doctrine Configuration, workspace_root, doc_root, Build Artifact

### Outside Boundary (Testing)

Supporting infrastructure and external dependencies that SHOULD be mocked/stubbed in tests

**Context:** Unit testing scope  
**Source:** test-boundaries-by-responsibility.tactic.md  
**Related:** Inside Boundary, Test Boundary

### Over-Decomposition

Failure mode of creating too many tiny bounded contexts, resulting in excessive translation overhead without cognitive load benefits

**Context:** Architecture - DDD / Failure Mode  
**Source:** bounded-context-linguistic-discovery.md  
**Related:** Bounded Context, Translation Layer

### Pattern Before Prescription

Discipline requiring pattern analysis across multiple instances before standardizing, ensuring patterns based on real usage not anticipated usage

**Context:** Meta-Pattern / Design Principle  
**Source:** locality-of-change.md, agent-profile-handoff-patterns.md  
**Related:** Organic Emergence, Evidence-Based Requirements

### Pattern Detection

Analysis technique identifying recurring themes, common mistakes, or successful approaches across multiple work logs to inform framework improvements

**Context:** Framework Improvement / Analysis  
**Source:** meta-analysis.md  
**Related:** Meta-Analysis, Anti-Pattern Identification

### Performance Budget

Explicit constraints on response time, throughput, resource usage, or latency that backend services must satisfy

**Context:** Backend Architecture - Quality Attributes  
**Source:** backend-dev.agent.md  
**Related:** Backend Benny, Persistence Strategy, Service Design

### Persistence Strategy

Architectural decision defining how data is stored, retrieved, updated, and maintained including database choice, schema design, and transaction boundaries

**Context:** Backend Architecture - Data Management  
**Source:** backend-dev.agent.md  
**Related:** Backend Benny, Service Design, Performance Budget

### Persona-Driven Writing

Writing approach filtering content through specific persona goals, frustrations, and engagement style to ensure artifact addresses their stated pain points

**Context:** Documentation / Communication  
**Source:** target-audience-fit.md  
**Related:** Target-Audience Fit, Audience Segmentation

### Phase 1 (Analysis)

First phase of Spec-Driven Development where requirements are elicited, specifications are authored, and acceptance criteria are defined; Analyst Annie has PRIMARY authority

**Context:** Spec-Driven Development Phases  
**Source:** analyst-annie.agent.md  
**Related:** Analyst Annie, Phase Authority, Specification, Acceptance Criteria

### Phase 2 (Architecture)

Second phase of Spec-Driven Development where solutions are evaluated, trade-off analysis performed, and architectural design approved; Architect Alphonso has PRIMARY authority

**Context:** Spec-Driven Development Phases  
**Source:** architect.agent.md  
**Related:** Architect Alphonso, Phase Authority, Trade-off Analysis, ADR

### Phase 3 (Planning)

Third phase of Spec-Driven Development where task breakdown, dependency analysis, and agent assignment occur; Planning Petra has PRIMARY authority

**Context:** Spec-Driven Development Phases  
**Source:** project-planner.agent.md  
**Related:** Planning Petra, Phase Authority, Task Breakdown, Dependency Mapping, YAML Task File

### Phase 4 (Acceptance Tests)

Fourth phase of Spec-Driven Development where acceptance criteria are implemented as executable tests before code implementation begins

**Context:** Spec-Driven Development Phases  
**Source:** analyst-annie.agent.md, backend-dev.agent.md  
**Related:** ATDD, Acceptance Criteria, Executable Test, Phase Authority

### Phase 5 (Implementation)

Fifth phase of Spec-Driven Development where production code is written to satisfy acceptance tests using TDD cycle

**Context:** Spec-Driven Development Phases  
**Source:** backend-dev.agent.md, python-pedro.agent.md  
**Related:** TDD, RED-GREEN-REFACTOR, Phase Authority

### Phase 6 (Review)

Sixth phase of Spec-Driven Development where multiple review types occur - architecture compliance (Architect), acceptance criteria validation (Analyst), code quality (Reviewer)

**Context:** Spec-Driven Development Phases  
**Source:** analyst-annie.agent.md, architect.agent.md, reviewer.agent.md  
**Related:** Review, Architecture Compliance, Acceptance Criteria, Code Quality

### Phase Authority

Designation of which agent has PRIMARY, CONSULT, or NO authority during each phase of the Spec-Driven Development workflow

**Context:** Agent Collaboration - Spec-Driven Development  
**Source:** analyst-annie.agent.md, architect.agent.md, project-planner.agent.md  
**Related:** Spec-Driven Development, Phase Checkpoint Protocol, Hand-off Protocol, Phase 1 (Analysis), Phase 2 (Architecture), Phase 3 (Planning)

### Phase Checkpoint Protocol

Self-observation procedure executed at the end of each phase to verify completion, assess authority for next phase, and ensure proper hand-off

**Context:** Development Methodology - SDD  
**Source:** spec-driven-6-phase-cycle.md  
**Related:** Six-Phase Cycle, Ralph Wiggum Loop

### Phase Declaration

Commit message annotation indicating which phase of the 6-phase cycle a commit belongs to

**Context:** SDD commit practices  
**Source:** 6-phase-spec-driven-implementation-flow.md  
**Related:** Hand-off, Phase Checkpoint Protocol

### Phase Skipping

Workflow violation where an agent bypasses required intermediate phases (e.g., jumping from Analysis directly to Implementation)

**Context:** SDD workflow violations  
**Source:** phase-checkpoint-protocol.md  
**Related:** Phase Checkpoint Protocol, Role Overstepping

### PLAN_OVERVIEW

Planning artifact documenting current goals, themes, and focus areas for project execution

**Context:** Artifacts - Planning  
**Source:** project-planner.agent.md  
**Related:** Planning Petra, NEXT_BATCH, Milestone Definition

### Planning Petra

Project planning specialist agent who translates strategic intent into executable, assumption-aware plans with milestone definitions and dependency mapping

**Context:** Agent Roles - Project Planning  
**Source:** project-planner.agent.md  
**Related:** Planning Specialist, Milestone Definition, Dependency Mapping, Batch Planning, PLAN_OVERVIEW

### Post-Action Learning Loop

Reflection tactic capturing concrete lessons after task completion to inform future work

**Context:** Continuous improvement  
**Source:** reflection-post-action-learning-loop.tactic.md  
**Related:** Lesson Extraction, Knowledge Encoding

### Premature Abstraction

Anti-pattern of creating frameworks, lookup tables, or automation before patterns stabilize or use cases mature, adding maintenance burden without proportional value

**Context:** Development Methodology / Anti-Pattern  
**Source:** locality-of-change.md  
**Related:** Gold Plating, Complexity Creep

### Premortem Risk Identification

Proactive failure analysis that assumes a proposal has already failed and identifies critical failure modes before execution

**Context:** Risk management  
**Source:** premortem-risk-identification.tactic.md  
**Related:** Failure Scenario, Mitigation Strategy, Risk Matrix

### Problem Assessment Protocol

Four-step analysis (Evidence Collection, Severity Measurement, Baseline Option, Simple Alternatives First) required before proposing solutions to verify problem exists and justify complexity

**Context:** Development Methodology / Decision Framework  
**Source:** locality-of-change.md  
**Related:** Locality of Change, Evidence-Based Requirements

### Progressive Disclosure

Principle of revealing system complexity gradually through hierarchical views, allowing stakeholders to consume exactly the abstraction level they need

**Context:** Architecture / Communication  
**Source:** design_diagramming-incremental_detail.md  
**Related:** Incremental Detail Design, C4 Model, Audience Alignment

### pytest

Python testing framework used for unit tests, integration tests, and acceptance tests with fixtures, parametrization, and coverage reporting

**Context:** Python Development - Testing  
**Source:** python-pedro.agent.md  
**Related:** Python Pedro, Test-First Development, Coverage Threshold

### Python Pedro

Python development specialist agent applying ATDD + TDD with type safety, idiomatic Python 3.9+ patterns, and comprehensive testing using pytest ecosystem

**Context:** Agent Roles - Python Development  
**Source:** python-pedro.agent.md  
**Related:** Python Specialist, Type Hints, pytest, Coverage Threshold, Self-Review Protocol

### Ralph Wiggum Loop

Self-aware observation pattern where agents periodically monitor their own execution state, detect problematic patterns (drift, confusion, misalignment), and self-correct mid-task

**Context:** Agent Behavior / Self-Observation  
**Source:** ralph-wiggum-loop.md  
**Related:** Self-Observation Checkpoint, Meta-Awareness, Course Correction

### Readability Scoring

Quantitative assessment using metrics like Flesch-Kincaid grade level and paragraph length distribution

**Context:** Writing analysis  
**Source:** lexical-style-diagnostic.tactic.md  
**Related:** Lexical Style Diagnostic

### RED Phase

ATDD workflow state where acceptance tests have been written but fail, proving tests work before implementation

**Context:** Test-driven development  
**Source:** 6-phase-spec-driven-implementation-flow.md  
**Related:** GREEN Phase, Acceptance Test Implementation

### RED-GREEN-REFACTOR

TDD cycle where tests are written first and fail (RED), minimal code makes them pass (GREEN), then code is improved while keeping tests green (REFACTOR)

**Context:** Development Practices - TDD  
**Source:** python-pedro.agent.md, backend-dev.agent.md, java-jenny.agent.md  
**Related:** TDD, Test-First Development, Directive 017

### Register Variation Awareness

Understanding that same concept may have different names in different registers (technical vs. user-facing, internal vs. external) without indicating semantic conflict

**Context:** Architecture - DDD / Nuance  
**Source:** living-glossary-practice.md  
**Related:** Semantic Conflict, False Positives

### Regression Prevention

Benefit of test-first bug fixing where failing-then-passing test becomes permanent guard preventing bug from returning unnoticed

**Context:** Development Methodology / Testing  
**Source:** test-first-bug-fixing.md  
**Related:** Test-First Bug Fixing, Test Validates Fix

### Rejection Rationale

One-sentence explanation for each alternative not selected, documenting why it was rejected

**Context:** Decision transparency  
**Source:** adr-drafting-workflow.tactic.md  
**Related:** ADR Drafting Workflow, Alternatives Considered

### Remediation Technique

Fallback workflow for handling unreliable terminal interactions by creating shell scripts, piping output to files, and capturing results from files instead of direct terminal interaction

**Context:** Framework - Terminal Operations  
**Source:** Directive 001 (CLI and Shell Tooling)  
**Related:** Bypass Check, Flaky Terminal Behavior

### REPO_MAP

Structural artifact generated by Bootstrap Bill that documents repository topology, directory roles, key files, and navigation paths for multi-agent orientation

**Context:** Artifacts - Repository Structure  
**Source:** bootstrap-bill.agent.md  
**Related:** Bootstrap Bill, Repository Scaffolding, Topology Mapping, SURFACES, WORKFLOWS

### Repository Initialization

Bootstrap procedure creating standard directory structure, configuration files, and initial documentation per SDD framework

**Context:** Project setup  
**Source:** repository-initialization.tactic.md  
**Related:** Directory Structure, Configuration Files

### Repository Scaffolding

Process of mapping repository topology and generating structural artifacts (REPO_MAP, SURFACES, WORKFLOWS) to enable multi-agent collaboration

**Context:** Agent Specializations  
**Source:** bootstrap-bill.agent.md  
**Related:** Bootstrap Bill, REPO_MAP, Topology Mapping, Structural Artifact

### Representative Data

Real-world or production-like data samples used during requirements analysis to capture actual patterns, edge cases, and validation scenarios

**Context:** Testing - Data Quality  
**Source:** analyst-annie.agent.md  
**Related:** Analyst Annie, Validation Script, Data Validation

### Reproducible Build

Build process that produces identical artifacts from the same source inputs across different environments and time periods

**Context:** Build Automation - Reliability  
**Source:** build-automation.agent.md  
**Related:** DevOps Danny, Build Graph, CI/CD Pipeline

### Requirements Specialist

Agent specialization focused on requirements elicitation, specification authoring, data validation, and production-data alignment to reduce ambiguity

**Context:** Agent Specializations  
**Source:** analyst-annie.agent.md  
**Related:** Analyst Annie, Specification, Validation Script, Data Quality

### Requirements Validation Cycle

Five-phase process (Research & Claim Extraction, Prioritization, Experiment Design, Validation Execution, Requirements Synthesis) transforming assumptions into validated knowledge

**Context:** Requirements Engineering  
**Source:** evidence-based-requirements.md  
**Related:** Evidence-Based Requirements, Testability Assessment

### Rerouting

Incremental process of shifting calls from old to new implementation one call site or module at a time

**Context:** Strangler fig execution  
**Source:** refactoring-strangler-fig.tactic.md  
**Related:** Strangler Fig Pattern, Coexistence Period

### Researcher Ralph

Research and corroboration specialist agent who gathers, synthesizes, and contextualizes information with source-grounded summaries for systemic reasoning

**Context:** Agent Roles - Research  
**Source:** researcher.agent.md  
**Related:** Research Specialist, Literature Synthesis, Comparative Analysis, Source Grounding, Verifiable Knowledge

### Reverse Speccing

Dual-agent validation technique reconstructing system understanding purely from test code to measure how effectively tests serve as executable specifications

**Context:** Quality Validation / Testing  
**Source:** reverse-speccing.md  
**Related:** Test-as-Documentation, Naive Reconstruction, Architecture Blind Spot

### Reversibility Mechanism

Pre-implemented rollback capability using version control, feature flags, or parallel deployment

**Context:** Risk mitigation  
**Source:** safe-to-fail-experiment-design.tactic.md  
**Related:** Safe-to-Fail Experiment, Feature Flag

### Review Dimensions

Multiple perspectives applied during systematic quality review - structural (organization), editorial (clarity), technical (accuracy), standards compliance

**Context:** Quality Assurance - Review  
**Source:** reviewer.agent.md  
**Related:** Reviewer, Structural Review, Editorial Review, Technical Review, Standards Compliance Review

### Review Report

Comprehensive quality assurance artifact documenting findings across multiple review dimensions (structural, editorial, technical, standards) with prioritized recommendations

**Context:** Artifacts - Quality Assurance  
**Source:** reviewer.agent.md  
**Related:** Reviewer, Review Dimensions, Finding Summary, Validation Checklist

### Reviewer

Quality assurance specialist agent conducting systematic multi-dimensional reviews (structural, editorial, technical, standards compliance) without making direct changes

**Context:** Agent Roles - Quality Assurance  
**Source:** reviewer.agent.md  
**Related:** Quality Assurance, Review Dimensions, Finding Summary, Review Report, Validation Checklist

### Risk Categorization

Classification of review concerns by type: Correctness, Maintainability, Impact, Misuse

**Context:** Review analysis  
**Source:** review-intent-and-risk-first.tactic.md  
**Related:** Intent-First Review, Impact Assessment

### Risk Matrix

2x2 grid plotting failure scenarios by impact (vertical) and likelihood (horizontal) for prioritization

**Context:** Risk prioritization  
**Source:** premortem-risk-identification.tactic.md  
**Related:** Premortem Risk Identification, Impact Rating

### Role Confusion

Failure mode where specialists perform work outside their authority (e.g., analysts making architectural decisions, architects implementing code)

**Context:** Development Methodology - Anti-Pattern  
**Source:** spec-driven-6-phase-cycle.md  
**Related:** Momentum Bias, Role Separation

### Role Overstepping

Violation where an agent performs work outside their designated authority level (PRIMARY, CONSULT, or NO)

**Context:** Agent authority boundaries  
**Source:** phase-checkpoint-protocol.md  
**Related:** Phase Skipping, Role Boundaries Table

### Role Separation

Design principle ensuring each phase has a distinct primary owner with explicit authority boundaries to prevent role confusion and maintain accountability

**Context:** Development Methodology - SDD  
**Source:** spec-driven-6-phase-cycle.md  
**Related:** Six-Phase Cycle, Role Confusion

### ruff

Fast Python linter replacing flake8, isort, pydocstyle for code quality checks and style enforcement

**Context:** Python Development - Code Quality  
**Source:** python-pedro.agent.md  
**Related:** Python Pedro, black, Code Quality

### Rule of Three

Heuristic to consider extraction when duplication appears in three locations, not two, to avoid premature abstraction

**Context:** Refactoring timing  
**Source:** refactoring-extract-first-order-concept.tactic.md  
**Related:** Concept Extraction, Premature Abstraction

### Safe-to-Fail Experiment

Bounded exploration with reversibility mechanisms, explicit success/failure criteria, and acceptable loss limits

**Context:** Innovation practice  
**Source:** safe-to-fail-experiment-design.tactic.md  
**Related:** Experiment Boundary, Reversibility Mechanism, Blast Radius

### Scenario-Driven Design

Design approach using concrete Given/When/Then scenarios to clarify requirements and drive implementation decisions

**Context:** Development Methodology - SDD  
**Source:** spec-driven-development.md  
**Related:** Specification-Driven Development, User Scenario

### Schema Validation

Automated verification that YAML task files comply with defined structure before marking tasks complete

**Context:** File-based orchestration quality  
**Source:** task-completion-validation.tactic.md  
**Related:** Task Schema, Validation Gate

### Scribe Sally

Documentation and transcription specialist agent who maintains traceable, neutral documentation integrity through structured summaries and meeting notes

**Context:** Agent Roles - Documentation  
**Source:** scribe.agent.md  
**Related:** Documentation Specialist, Meeting Notes, Structured Summary, Neutral Tone, Timestamp

### Self-Observation Checkpoint

Structured protocol executed at trigger points (time elapsed, warning signs) where agent switches to meta-mode to assess execution state and decide continue/adjust/escalate

**Context:** Agent Behavior / Self-Observation  
**Source:** ralph-wiggum-loop.md  
**Related:** Ralph Wiggum Loop, Meta-Mode, Warning Sign Detection

### Self-Review Protocol

Systematic quality checklist executed by development agents before marking work complete, including test execution, type checking, linting, coverage validation, and ADR compliance

**Context:** Quality Gates - Development  
**Source:** python-pedro.agent.md  
**Related:** Coverage Threshold, Type Checking, Lint Results, ADR Compliance

### Semantic Clustering

Grouping of related domain terms based on co-occurrence patterns and semantic similarity

**Context:** Linguistic analysis  
**Source:** code-documentation-analysis.tactic.md  
**Related:** Co-occurrence Analysis, Vocabulary Domain

### Semantic Conflict

Situation where the same term has different meanings in different contexts, indicating a hidden bounded context boundary requiring explicit management

**Context:** Architecture - DDD  
**Source:** language-first-architecture.md, bounded-context-linguistic-discovery.md  
**Related:** Linguistic Signal, Bounded Context Boundary, Translation Layer

### Semantic Fidelity

Quality measure of how accurately a diagram or visualization represents the underlying conceptual, architectural, or organizational relationships

**Context:** Agent Capabilities - Visualization  
**Source:** diagrammer.agent.md  
**Related:** Diagram Daisy, Diagram-as-Code, Visual Representation

### Semantic Heading

Markdown heading structure using single h1 per file with ordered h2+ hierarchy to convey document structure semantically

**Context:** Documentation / Markdown  
**Source:** style-execution-primers.md  
**Related:** Style Execution Primer, CommonMark Compliance

### Service Design

Architectural process defining service boundaries, API contracts, integration patterns, and failure modes for backend systems

**Context:** Backend Architecture - System Design  
**Source:** backend-dev.agent.md  
**Related:** Backend Benny, API Contract, Integration Surface, Persistence Strategy

### Shadow Mode

Safety mechanism running old and new implementations in parallel to compare outputs before full rerouting

**Context:** Migration validation  
**Source:** refactoring-strangler-fig.tactic.md  
**Related:** Strangler Fig Pattern, Feature Flag

### Shared Artifact

Resources multiple teams contribute to: repositories, documentation, meetings

**Context:** Collaboration indicator  
**Source:** team-interaction-mapping.tactic.md  
**Related:** Team Interaction Mapping, Communication Frequency

### Ship/Show/Ask Pattern

Flexible review pattern for trunk-based development: Ship (commit directly), Show (commit + notify for async review), Ask (branch + pre-merge review)

**Context:** Version Control / Review Pattern  
**Source:** trunk-based-development.md  
**Related:** Trunk-Based Development, Code Review Discipline

### Short-Lived Branch

Feature branch with maximum lifetime of 24 hours (target 4-8h) to minimize integration risk and maintain trunk stability

**Context:** Version Control / Pattern  
**Source:** trunk-based-development.md  
**Related:** Trunk-Based Development, Branch Age Warning

### Signposted Section

Labeled portion of document indicating which persona it serves (e.g., "For Jordan—getting started") to reduce cognitive load when serving multiple audiences

**Context:** Documentation / Structure  
**Source:** target-audience-fit.md  
**Related:** Target-Audience Fit, Persona-Driven Writing

### Simplicity Preservation

Active practice of maintaining architectural simplicity over time by resisting complexity creep, validating problem severity before adding solutions, and favoring 80/20 approaches

**Context:** Development Methodology / Design Principle  
**Source:** locality-of-change.md  
**Related:** Locality of Change, Complexity Creep

### Six-Phase Cycle

Structured specification-driven workflow with distinct phases (Analysis, Architecture, Planning, Acceptance Test, Implementation, Review), each with a primary owner and explicit hand-offs

**Context:** Development Methodology - SDD  
**Source:** spec-driven-6-phase-cycle.md  
**Related:** Phase Checkpoint Protocol, Momentum Bias Prevention, Role Separation

### Smallest Viable Diff

Principle of introducing changes using minimal modification that achieves stated goal, avoiding unintended side effects

**Context:** Change discipline  
**Source:** change-apply-smallest-viable-diff.tactic.md  
**Related:** Surgical Modification, Gold-plating, Locality of Change

### Source vs Distribution

Architectural distinction where doctrine/ contains canonical source content and tool-specific directories (.github/, .claude/, .opencode/) contain generated distribution artifacts

**Context:** Doctrine Stack - Architecture  
**Source:** curator.agent.md  
**Related:** Curator Claire, Export Pipeline, Doctrine Stack, Tool-Specific Distribution

### spec_root

Path variable in doctrine configuration pointing to specification files directory (default 'specifications') where functional and technical specs are stored

**Context:** Configuration - Path Variables  
**Source:** bootstrap-bill.agent.md  
**Related:** Doctrine Configuration, workspace_root, doc_root, Specification

### Specialization Boundary

Explicit limits on agent capabilities defining what each agent will and won't do to prevent scope creep and role confusion

**Context:** Agent Collaboration - Role Definition  
**Source:** All agent profiles  
**Related:** Collaboration Contract, Hand-off Protocol, Escalation

### Specification Lifecycle

Progression of specification states: DRAFT → APPROVED → IMPLEMENTED, with status changes marking phase transitions

**Context:** Development Methodology - SDD  
**Source:** spec-driven-6-phase-cycle.md  
**Related:** Living Specification, Specification Stub

### Specification Stub

Initial draft specification with structure and metadata created during analysis phase before detailed requirements are fully documented

**Context:** Development Methodology - SDD  
**Source:** spec-driven-development.md, spec-driven-6-phase-cycle.md  
**Related:** Phase 1 Analysis, Specification Lifecycle

### Specification-Driven Development

Development methodology where specifications serve as primary artifacts bridging strategic intent and implementation, remaining independent of tests or architectural decisions

**Context:** Development Methodology - SDD  
**Source:** spec-driven-development.md  
**Related:** Living Specification, Scenario-Driven Design, Specification Stub

### Staleness Audit

Quarterly review identifying outdated definitions (>6 months unchanged) and validating against current implementation

**Context:** Glossary quality  
**Source:** glossary-maintenance-workflow.tactic.md  
**Related:** Glossary Maintenance Workflow, Coverage Assessment

### Staleness Rate

Percentage of glossary definitions that are outdated; target <10% to maintain glossary value as living reference

**Context:** Architecture - DDD / Metrics  
**Source:** living-glossary-practice.md  
**Related:** Living Glossary, Incremental Maintenance

### Standards Compliance Review

Review dimension focused on adherence to style guides, templates, directives, ADRs, file naming conventions, and required metadata

**Context:** Quality Assurance - Review Types  
**Source:** reviewer.agent.md  
**Related:** Review Dimensions, Style Guide, Template Compliance, Directive Compliance

### State Boundaries

Explicit divisions defining where application state is owned, how it flows between components, and mutation responsibilities

**Context:** Frontend Architecture - State Management  
**Source:** frontend.agent.md  
**Related:** Frontend Freddy, UI Architecture, Data Flow

### Stopping Condition

Clear, measurable threshold defining when to stop pursuing a goal based on acceptable loss limits

**Context:** Commitment management  
**Source:** stopping-conditions.tactic.md  
**Related:** Hard Limit, Warning Signal, Trigger Declaration

### Strangler Fig Pattern

Incremental refactoring pattern introducing new implementation alongside old, gradually rerouting behavior, then removing old code

**Context:** Large-scale refactoring  
**Source:** refactoring-strangler-fig.tactic.md  
**Related:** Rerouting, Coexistence Period, Shadow Mode

### Structural Artifact

Generated documentation or code that describes repository organization, workflows, or architectural patterns for orientation and navigation

**Context:** Artifacts - Repository Documentation  
**Source:** bootstrap-bill.agent.md  
**Related:** Bootstrap Bill, REPO_MAP, SURFACES, WORKFLOWS

### Structural Review

Review dimension focused on organization, flow, completeness, template compliance, cross-reference validity, and heading hierarchy

**Context:** Quality Assurance - Review Types  
**Source:** reviewer.agent.md  
**Related:** Review Dimensions, Template Compliance, Cross-Reference

### Style Execution Primer

Concise, action-ready guidance for agents working in specific formats (Markdown, Python, Perl, PlantUML) focusing on diff-friendliness and template alignment

**Context:** Documentation / Coding Standards  
**Source:** style-execution-primers.md  
**Related:** Template-First Approach, Semantic Heading, Cross-Cutting Concern

### Sunk-Cost Fallacy Override

Continuing past stopping conditions by rationalizing invested effort rather than acknowledging limits

**Context:** Decision bias  
**Source:** stopping-conditions.tactic.md  
**Related:** Stopping Condition, Hard Limit

### Suppression Pattern

Metric tracking how often developers override glossary checks; >10% indicates enforcement too strict or checks producing false positives

**Context:** Quality Assurance / Metrics  
**Source:** living-glossary-practice.md  
**Related:** Enforcement Tier, False Positives

### SURFACES

Artifact documenting integration points, APIs, config files, and external dependencies discovered during repository bootstrapping

**Context:** Artifacts - Repository Structure  
**Source:** bootstrap-bill.agent.md  
**Related:** Bootstrap Bill, REPO_MAP, Integration Surface, API Contract

### Surgical Modification

Precise, minimal code changes targeting only files and sections necessary to achieve goal

**Context:** Refactoring practice  
**Source:** change-apply-smallest-viable-diff.tactic.md  
**Related:** Smallest Viable Diff, Reviewable Change

### Synthesizer Sam

Multi-agent integration specialist who merges insights from multiple agents into coherent narratives and conceptual models while preserving source integrity

**Context:** Agent Roles - Integration  
**Source:** synthesizer.agent.md  
**Related:** Integration Specialist, Pattern Synthesis, Coherence Articulation, Cross-Agent Integration

### System Decomposition

Architectural artifact that breaks down complex systems into components, interfaces, and relationships with explicit trade-offs and decision rationale

**Context:** Artifacts - Architecture  
**Source:** architect.agent.md  
**Related:** Architect Alphonso, ADR, Component Diagram, Interface Design

### Tactics Catalog

README.md in tactics directory listing all available tactics with intent and invocation context

**Context:** Doctrine navigation  
**Source:** tactics-curation.tactic.md  
**Related:** Tactics Curation, Discoverability

### Tactics Curation

Meta-tactic maintaining structural, tonal, and metadata integrity across the tactics layer

**Context:** Doctrine maintenance  
**Source:** tactics-curation.tactic.md  
**Related:** Metadata Header, Tactics Catalog, Template Compliance

### Target-Audience Fit

Communication pattern ensuring every artifact intentionally addresses specific reader personas with appropriate tone, depth, and structure

**Context:** Documentation / Communication  
**Source:** target-audience-fit.md  
**Related:** Persona-Driven Writing, Audience Segmentation, Signposted Section

### Task Artifact Declaration

Explicit listing of files a task will modify in YAML artefacts field, enabling pre-commit conflict detection and coordination between agents

**Context:** Orchestration / Conflict Avoidance  
**Source:** work-directory-orchestration.md, trunk-based-development.md  
**Related:** File-Based Orchestration, Artifact Conflict Detection

### Task Breakdown

Process of decomposing specifications into concrete, executable tasks with clear dependencies, acceptance criteria, and agent assignments

**Context:** Planning - Work Decomposition  
**Source:** project-planner.agent.md  
**Related:** Planning Petra, Phase 3 (Planning), YAML Task File, Dependency Mapping

### Task Lifecycle

The standardized progression of orchestrated tasks through states: **new** (unassigned work), **assigned** (routed to specific agent), **in_progress
** (actively being worked), **done** (completed with results), **archive
** (historical record). Task state transitions are tracked through file-based coordination.

**Reference:** Directive 019, ADR-003  
**Related:** Orchestration, Work Log
### Team Communication Matrix

Documentation of communication frequency and artifact sharing patterns between organizational teams

**Context:** Organizational analysis  
**Source:** context-boundary-inference.tactic.md  
**Related:** Conway's Law, Team Interaction Mapping

### Team Interaction Mapping

Documentation of organizational communication patterns to identify vocabulary clusters and predict semantic boundaries

**Context:** Organizational analysis  
**Source:** team-interaction-mapping.tactic.md  
**Related:** Communication Frequency, Vocabulary Cluster, Conway's Law

### Technical Review

Review dimension focused on accuracy verification, example correctness, reference citations, code functionality, and version currency

**Context:** Quality Assurance - Review Types  
**Source:** reviewer.agent.md  
**Related:** Review Dimensions, Technical Accuracy, Code Correctness

### Template Compliance

Validation that tactics follow standardized structure from doctrine/templates/tactic.md

**Context:** Quality assurance  
**Source:** tactics-curation.tactic.md  
**Related:** Tactics Curation, Structural Consistency

### Template-First Approach

Practice of reusing repository templates before handcrafting new formats to ensure consistency and avoid format proliferation

**Context:** Documentation / Standards  
**Source:** style-execution-primers.md  
**Related:** Style Execution Primer, Configuration Consistency

### Term Candidate

Proposed glossary entry with preliminary definition, source references, and confidence level awaiting triage

**Context:** Glossary workflow  
**Source:** glossary-maintenance-workflow.tactic.md  
**Related:** Glossary Triage, Continuous Capture

### Test Boundary

Scope of components included in a test based on functional responsibility rather than structural layers

**Context:** Unit testing strategy  
**Source:** test-boundaries-by-responsibility.tactic.md  
**Related:** Inside Boundary, Outside Boundary, Functional Responsibility

### Test Validates Fix

Verification step ensuring test fails for the RIGHT reason (reproduces bug) by temporarily inverting assertion to expect wrong behavior, confirming test accuracy

**Context:** Development Methodology / Testing  
**Source:** test-first-bug-fixing.md  
**Related:** Test-First Bug Fixing, Regression Prevention

### Test-as-Documentation

Principle that well-written tests should comprehensively document system behavior so reading tests alone enables understanding "what" and "how" without external docs

**Context:** Quality Validation / Testing Philosophy  
**Source:** reverse-speccing.md, test-readability-clarity-check.md  
**Related:** Reverse Speccing, Living Specification

### Test-First Bug Fixing

Disciplined debugging approach requiring a failing test that reproduces the bug BEFORE modifying production code, transforming trial-and-error into systematic verification

**Context:** Development Methodology / Testing  
**Source:** test-first-bug-fixing.md  
**Related:** Red-Green-Refactor, Regression Prevention, Test Validates Fix

### Testability Assessment

Evaluation of whether a requirement claim can be validated: Fully Testable (concrete experiment), Partially Testable (proxy metrics), Not Testable (subjective/unfalsifiable)

**Context:** Requirements Engineering  
**Source:** evidence-based-requirements.md  
**Related:** Evidence-Based Requirements, Claim Classification

### Token Discipline

Practice of maintaining essential governance layers in active memory while offloading task-specific details to external files, optimizing context window usage without losing behavioral guardrails

**Context:** Framework - Context Management  
**Source:** Directive 002 (Context Notes)  
**Related:** External Memory, Context Layer, Offloading

### Tonal Integrity

Preservation of consistent voice, rhythm, and authorial personality across documents while preventing style drift or flattening

**Context:** Content Quality - Voice Preservation  
**Source:** curator.agent.md, lexical.agent.md, writer-editor.agent.md  
**Related:** Curator Claire, Lexical Larry, Editor Eddy, Authorial Voice, Voice Fidelity

### Tone Consistency

Alignment of voice with target audience, avoiding informal/formal mixing

**Context:** Writing quality  
**Source:** lexical-style-diagnostic.tactic.md  
**Related:** Lexical Style Diagnostic, Voice Preservation

### Tone Preservation

Active maintenance of original tone and emotional register during content transformation (translation, editing, summarization)

**Context:** Content Quality - Voice Preservation  
**Source:** translator.agent.md, writer-editor.agent.md  
**Related:** Authorial Voice, Voice Fidelity, Tonal Integrity

### Tool Selection Rigor

Disciplined framework for choosing tools based on measurable criteria (usage frequency, performance improvement, maintenance activity, security posture)

**Context:** Development Environment / Best Practice  
**Source:** tooling-setup-best-practices.md  
**Related:** Tooling Necessity Check, Tooling Quality Assessment, Graceful Degradation

### Tool-Specific Distribution

Generated content formatted for specific development tools (GitHub Copilot, Claude Desktop, OpenCode, Cursor) deployed to tool-specific directories

**Context:** Doctrine Stack - Distribution  
**Source:** curator.agent.md  
**Related:** Source vs Distribution, Export Pipeline, .github/, .claude/, .opencode/

### Topology Mapping

Process of scanning and documenting repository structure, identifying directory roles, key files, configuration locations, and navigation paths

**Context:** Agent Capabilities - Repository Analysis  
**Source:** bootstrap-bill.agent.md  
**Related:** Bootstrap Bill, REPO_MAP, Repository Scaffolding

### Traceability Chain

Bidirectional link pattern connecting artifacts throughout development lifecycle (Strategic Goal → Specification → Tests → ADRs → Implementation → Work Logs)

**Context:** Development Methodology / Quality Assurance  
**Source:** traceability-chain-pattern.md  
**Related:** Bidirectional Linking, Impact Analysis, Orphaned Artifact

### Trade-off Analysis

Architectural reasoning process that explicitly documents alternatives considered, evaluation criteria, and rationale for chosen approach

**Context:** Architecture - Decision Making  
**Source:** architect.agent.md  
**Related:** Architect Alphonso, ADR, Phase 2 (Architecture), System Decomposition

### Translation Layer

Explicit mapping mechanism protecting downstream contexts from upstream changes by transforming terminology at bounded context boundaries (Anti-Corruption Layer pattern)

**Context:** Architecture - DDD  
**Source:** bounded-context-linguistic-discovery.md  
**Related:** Anti-Corruption Layer, Bounded Context, Semantic Conflict

### Translation Rule

Explicit mapping defining how terminology changes when crossing bounded context boundaries

**Context:** Context integration  
**Source:** context-boundary-inference.tactic.md  
**Related:** Anti-Corruption Layer, Context Boundary

### Translator Tanya

Contextual interpreter specialist agent who preserves authorial tone and rhythm during accurate cross-language translation using voice fidelity techniques

**Context:** Agent Roles - Translation  
**Source:** translator.agent.md  
**Related:** Translation Specialist, Voice Fidelity, Tone Preservation, Contextual Pass, VOICE_DIFF

### Trigger Declaration

Pre-commitment statement in 'When X happens, then I will stop' format conditioning behavior

**Context:** Behavioral conditioning  
**Source:** stopping-conditions.tactic.md  
**Related:** Stopping Condition, Hard Limit

### Trunk Health Dashboard

Monitoring visualization showing key trunk metrics (commit frequency, revert rate, test pass rate, time-to-fix) for stability assessment

**Context:** Version Control / Monitoring  
**Source:** trunk-based-development.md  
**Related:** Trunk Stability, Trunk-Based Development

### Trunk Stability

Measure of main branch health (>95% test pass rate, <5% revert rate, <15 min time-to-fix) indicating system readiness for continuous deployment

**Context:** Version Control / Metrics  
**Source:** trunk-based-development.md  
**Related:** Trunk-Based Development, Trunk Health Dashboard

### Trunk-Based Development

Branching strategy where all developers commit frequently to single shared branch (main), using short-lived feature branches (<24h) only for coordinated changes

**Context:** Version Control / Collaboration Pattern  
**Source:** trunk-based-development.md  
**Related:** Short-Lived Branch, Trunk Stability, Branch Age Warning

### Type Checking

Static analysis validation using mypy (Python) or similar tools to ensure type safety before code acceptance

**Context:** Quality Gates - Code Quality  
**Source:** python-pedro.agent.md  
**Related:** Self-Review Protocol, mypy, Type Hints, Type Safety

### Type Hints

Python 3.9+ annotations specifying expected types for function parameters, return values, and variables to enable static analysis

**Context:** Python Development - Type Safety  
**Source:** python-pedro.agent.md  
**Related:** Python Pedro, mypy, Type Checking, Type Safety

### UI Architecture

Structural design of user interface including component hierarchies, state boundaries, data flow patterns, and interaction flows

**Context:** Frontend Architecture  
**Source:** frontend.agent.md  
**Related:** Frontend Freddy, Component Patterns, State Boundaries, Design System

### Upgrade Plan

Detailed document produced by Framework Guardian classifying upgrade conflicts and proposing minimal patches while preserving local customizations

**Context:** Artifacts - Framework Maintenance  
**Source:** framework-guardian.agent.md  
**Related:** Framework Guardian, Conflict Classification, Core/Local Boundary, Minimal Patch

### Validation Category

Classification of validation types: Presence, Format, Range, Logical Consistency, Uniqueness, Referential Integrity

**Context:** Input validation  
**Source:** input-validation-fail-fast.tactic.md  
**Related:** Validation Sequence

### Validation Checklist

Systematic checklist confirming all review criteria were applied, evidence collected, recommendations prioritized, and quality standards met

**Context:** Quality Assurance - Verification  
**Source:** reviewer.agent.md  
**Related:** Reviewer, Review Report, Quality Standard

### Validation Experiment

Rigorous test designed to accept or reject a claim hypothesis with clear success criteria and confound controls

**Context:** Evidence-based validation  
**Source:** claim-inventory-development.tactic.md  
**Related:** Testability Assessment, Falsifiable Hypothesis

### Validation Script

Executable script or SQL query that validates requirements against real production data, capturing pass rates and edge cases for specification quality assurance

**Context:** Artifacts - Requirements Analysis  
**Source:** analyst-annie.agent.md  
**Related:** Analyst Annie, Data Validation, Specification, Representative Data

### Validation Sequence

Ordered validation checks: Presence → Format → Range → Logical Consistency → Uniqueness

**Context:** Input processing  
**Source:** input-validation-fail-fast.tactic.md  
**Related:** Fail-Fast Validation, Validation Category

### Version Pinning Strategy

Tiered approach balancing stability with updates (Pinned Versions for API-sensitive tools, Package Manager for stable tools, Latest Stable for rapidly evolving tools)

**Context:** Development Environment / Configuration  
**Source:** tooling-setup-best-practices.md  
**Related:** Configuration Consistency, Tool Selection Rigor

### Vocabulary Cluster

Set of domain terms consistently used by a specific team, indicating ownership and expertise

**Context:** Linguistic patterns  
**Source:** team-interaction-mapping.tactic.md  
**Related:** Vocabulary Ownership, Team Interaction Mapping

### Vocabulary Fragmentation

Condition where different parts of a system or organization use inconsistent or conflicting terminology for domain concepts, signaling hidden architectural boundaries

**Context:** Architecture - DDD  
**Source:** language-first-architecture.md, bounded-context-linguistic-discovery.md  
**Related:** Linguistic Signal, Bounded Context

### Vocabulary Ownership

Assignment of terminology domains to specific teams based on code authorship and documentation patterns

**Context:** Linguistic governance  
**Source:** context-boundary-inference.tactic.md  
**Related:** Context Boundary, Semantic Clustering

### Voice Fidelity

Quality measure of how well translated or edited content preserves the original author's distinctive tone, rhythm, and cadence

**Context:** Agent Capabilities - Translation/Editing  
**Source:** translator.agent.md, writer-editor.agent.md  
**Related:** Translator Tanya, Editor Eddy, Authorial Voice, Tone Preservation

### Warning Sign Detection

Agent's ability to recognize internal signals indicating problems (repetitive patterns, lost goal, speculation, verbose output, scope creep, directive violation)

**Context:** Agent Behavior / Self-Observation  
**Source:** ralph-wiggum-loop.md  
**Related:** Ralph Wiggum Loop, Self-Observation Checkpoint

### Warning Signal

Observable red flag indicating trouble requiring attention or reassessment

**Context:** Early detection  
**Source:** stopping-conditions.tactic.md  
**Related:** Stopping Condition, Hard Limit

### Weaponized Standards

Organizational anti-pattern where glossary, coding standards, or architectural guidelines used as tool in politics rather than shared understanding

**Context:** Organizational / Anti-Pattern  
**Source:** living-glossary-practice.md  
**Related:** Linguistic Policing, Glossary as Power Tool

### Work Directory Model

Directory structure encoding orchestration state: collaboration/ (routing), reports/ (logs, metrics), external_memory/ (scratch), notes/ (ideation), planning/ (aids), schemas/ (validators)

**Context:** Orchestration / Structure  
**Source:** work-directory-orchestration.md  
**Related:** File-Based Orchestration, Task Lifecycle

### WORKFLOW_LOG

Chronological log of multi-agent workflow execution maintained by Manager Mike for traceability and coordination

**Context:** Artifacts - Orchestration  
**Source:** manager.agent.md  
**Related:** Manager Mike, AGENT_STATUS, Hand-off Tracking

### WORKFLOWS

Artifact documenting build, test, CI/CD, and deployment workflows discovered during repository bootstrapping

**Context:** Artifacts - Repository Structure  
**Source:** bootstrap-bill.agent.md  
**Related:** Bootstrap Bill, REPO_MAP, CI/CD Pipeline, Build Graph

### workspace_root

Path variable in doctrine configuration pointing to task orchestration workspace directory (default 'work') where agents create work logs, coordination artifacts, and intermediate outputs

**Context:** Configuration - Path Variables  
**Source:** bootstrap-bill.agent.md  
**Related:** Doctrine Configuration, doc_root, spec_root, output_root

### YAML Task File

Structured task definition file used in file-based orchestration containing task metadata, dependencies, acceptance criteria, and agent assignment

**Context:** Orchestration - Task Definition  
**Source:** project-planner.agent.md, manager.agent.md  
**Related:** Planning Petra, Manager Mike, File-Based Orchestration, Task Breakdown


---

## Usage Guidelines

### For Agents

- Reference glossary terms when explaining decisions or documenting work
- Use consistent terminology across all artifacts and communications
- When encountering ambiguous terms, consult this glossary first
- Suggest new terms or clarifications via work logs when gaps are identified

### For Humans

- Use glossary terms when providing instructions to agents
- Reference specific terms when clarity is needed
- Propose term additions or refinements through pull requests
- Review glossary during agent framework onboarding

### Cross-Referencing

When directives or agent profiles reference glossary terms, use this format:

```markdown
See [Term Name](./GLOSSARY.md#term-name) for definition.
```

---

## Maintenance

This glossary is a living document. Updates follow Version Governance (Directive 006):

- **Minor updates** (clarifications, examples): Update version patch number
- **New terms** (additions): Update version minor number
- **Structural changes** (reorganization): Update version major number

All changes require review by Curator agent for consistency and alignment with existing framework documentation.

**Maintained by:** Curator Claire  
**Review cycle:** Quarterly or when 5+ new terms are identified  
**Change requests:** Submit via ${WORKSPACE_ROOT}/collaboration/inbox/ task file

---

## Related Documentation

- [AGENTS.md](../AGENTS.md) - Core agent specification
- [directives/](./directives/) - Extended directive set (001-019)
- [Agent Profiles](.) - Role-specific configurations
- [Version Governance](./directives/006_version_governance.md) - Version tracking system
- [Work Log Creation](./directives/014_worklog_creation.md) - Documentation standards
