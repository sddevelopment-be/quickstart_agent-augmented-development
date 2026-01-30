# approach-decision-first-development

This approach describes how to systematically capture architectural decisions throughout the development lifecycle, integrating decision rationale with artifacts to preserve "why" knowledge for fut...

## Capabilities

- documentation-pattern
- operational-guide
- decision-visibility
- flow-state-respect

## Instructions

This approach describes how to systematically capture architectural decisions throughout the development lifecycle, integrating decision rationale with artifacts to preserve "why" knowledge for future contributors and AI agents. It implements the traceable decision patterns established in ADR-017.

## Core Principles

1. **Decision Visibility**: Every architectural decision should be discoverable and traceable from ideation through implementation.
2. **Flow State Respect**: Decision capture timing should adapt to individual productivity rhythms—defer when deep in creation, collaborate when iterating with agents, formalize during reflection.
3. **Bidirectional Linking**: Decisions reference affected artifacts; artifacts reference governing decisions. No orphaned rationale.
4. **Progressive Fidelity**: Start with lightweight markers, evolve to synthesis documents, formalize as ADRs when patterns stabilize.
5. **Agent Awareness**: AI agents check relevant ADRs before proposing changes and include decision references in generated artifacts.

## When to Use

- Making architectural choices that will affect multiple components
- Evaluating trade-offs between alternative implementations
- Establishing conventions or patterns for the codebase
- Working with AI agents on complex features requiring context
- Onboarding new contributors who need to understand rationale

## Example Prompts

- "Help me document an architectural decision"
- "What's the best way to capture design rationale?"
- "Explain the Decision-First Development Workflow approach"
- "When should I use Decision-First Development Workflow?"

## Metadata


