# Doctrine Decision Records (DDR)

Framework-level decisions that define doctrine concepts, patterns, and governance.

## DDR vs ADR Distinction

**DDRs (doctrine/decisions/):**
- Universal patterns applicable across repositories
- Part of doctrine framework itself
- Ship with doctrine when distributed
- Examples: Primer execution patterns, agent role definitions

**ADRs (docs/architecture/adrs/):**
- Repository-specific implementation decisions
- Tooling, distribution mechanisms, local architecture
- NOT part of doctrine framework
- Examples: Export formats, CI pipelines, module structures

## Key Principle

> "Distribution of the doctrine is not an integral part of the doctrine itself, so it should be captured in the ADRs of this repository (which is scoped to contain the `doctrine` as well as supporting tools/applications/flows)."
>
> — Human In Charge Decision, 2026-02-11

## DDR Index

| DDR | Title | Status | Date |
|-----|-------|--------|------|
| [DDR-001](DDR-001-primer-execution-matrix.md) | Primer Execution Matrix | Accepted | 2026-02-11 |
| [DDR-002](DDR-002-framework-guardian-role.md) | Framework Guardian Agent Role | Accepted | 2026-02-11 |

## Usage in Profiles and Directives

**When to reference DDRs:**
- Conceptual patterns that apply universally (e.g., primer execution, agent role patterns)
- Behavioral contracts that define "how agents should operate" across any repository

**When to reference repository ADRs:**
- Implementation specifics (e.g., "see your repository's ADRs for distribution mechanisms")
- Tooling choices, CI pipelines, module structures
- Examples of how doctrine concepts are implemented locally

**When to use generic descriptions:**
- If the pattern is simple enough not to warrant a DDR
- If the reference is purely illustrative and not normative
