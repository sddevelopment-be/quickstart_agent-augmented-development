# Copilot Custom Instructions

This file provides custom instructions for GitHub Copilot based on the agent framework.

## Available Skills

### Prompt Templates

These are reusable task-specific prompts:

- **architect-adr**: Prompt for Architect Alphonso to perform analysis and draft a Proposed ADR
- **automation-script**: Prompt for DevOps Danny to generate an automation script based on requirements or direct prompt
- **bootstrap-repo**: Prompt for Bootstrap Bill to bootstrap a cloned repository for local/project context
- **curate-directory**: Prompt for Curator Claire to audit and normalize a target directory
- **editor-revision**: Prompt for Editor Eddy to revise a draft document using lexical analysis artifacts
- **lexical-analysis**: Prompt for Lexical Larry to perform a lexical style diagnostic and minimal diff pass
- **new-agent**: Prompt to request creation of a new specialized agent (Manager Mike runs it)

### Operational Approaches

These are workflow patterns and operational guides:

- **approach-agent-profile-handoff-patterns**: Instead of a centralized lookup table, each agent profile documents its own observed handoff patterns. This approach:  - Preserves agent autonomy - Requires zero implementation complexity - Remains...
- **approach-decision-first-development**: This approach describes how to systematically capture architectural decisions throughout the development lifecycle, integrating decision rationale with artifacts to preserve "why" knowledge for fut...
- **approach-design-diagramming-incremental-detail**: The C4 model (Context, Container, Component, Code) is a lightweight hierarchical technique for structuring software architecture diagrams. It favors progressive disclosure of technical detail so st...
- **approach-file-based-orchestration**: 
- **approach-locality-of-change**: 
- **approach-style-execution-primers**: 
- **approach-target-audience-fit**: Translate the “Target Audience Personas” practice (see `work/notes/ideation/opinionated_platform/target_audience_personas.md`) into a repeatable workflow so every artifact intentionally addresses t...
- **approach-test-readability-clarity-check**: The Test Readability and Clarity Check is a dual-agent validation approach that assesses whether a test suite effectively documents system behavior by reconstructing system understanding purely fro...
- **approach-tooling-setup-best-practices**: This approach describes best practices for setting up, configuring, and maintaining development tooling to support agent-augmented development. It provides a framework for tool selection, configura...
- **approach-traceable-decisions-detailed-guide**: 
- **approach-trunk-based-development**: Trunk-based development (TBD) is a branching strategy where all developers (agents and humans) commit frequently to a single shared branch (`main`), with short-lived feature branches (<24 hours) us...
- **approach-work-directory-orchestration**: Provide a single, precise reference for the file-based asynchronous orchestration model that powers the `work/` directory. The approach keeps exploratory and operational work visible inside Git by ...

## Detailed Instructions

For detailed instructions, see the individual files in `.github/instructions/`.

## Framework Reference

This project uses the Agent-Augmented Development framework. Key references:
- Agent profiles: `.github/agents/*.agent.md`
- Directives: `.github/agents/directives/`
- Approaches: `.github/agents/approaches/`
