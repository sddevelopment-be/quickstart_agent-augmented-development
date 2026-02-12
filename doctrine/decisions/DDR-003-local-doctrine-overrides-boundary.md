# DDR-003: Local Doctrine Overrides and Stack Boundary Enforcement

**Status:** Accepted  
**Date:** 2026-02-12  
**Scope:** Doctrine framework initialization and dependency guardrails

## Context

The doctrine stack must stay portable while still supporting repository-specific customization. We need a consistent localization technique for project-specific guidance and extensions without allowing local configuration to weaken core governance.

Prior references to a docs-root specific-guidelines path also created ambiguity about where local constraints should live.

## Decision

1. Repository-local doctrine customization is expected under `.doctrine-config/` and loaded only after the main `doctrine/` stack.
2. Expected local constraints entry point is:
   - `.doctrine-config/specific_guidelines.md`
   - or `${LOCAL_DOCTRINE_ROOT}/specific_guidelines.md` when using placeholders.
3. Local overrides may tweak, enhance, or extend lower-priority layers (custom agents, extra directives/instructions, tactics, approaches).
4. Local overrides MUST NOT override or weaken:
   - `doctrine/guidelines/general_guidelines.md`
   - `doctrine/guidelines/operational_guidelines.md`
5. Dependency checks must enforce doctrine stack boundary rules:
   - no direct cross-directory references from `doctrine/DOCTRINE_STACK.md` to non-doctrine project directories,
   - except expected local override locations/placeholders.

## Consequences

### Positive

- Keeps doctrine portable and self-contained.
- Standardizes local extension discovery across repositories.
- Prevents local customization from bypassing core behavioral guardrails.
- Makes validation enforceable in CI.

### Trade-offs

- Requires migration of legacy docs-root specific-guidelines references.
- Adds one more path variable (`LOCAL_DOCTRINE_ROOT`) to governance checks.

## Implementation Notes

- Update doctrine governance docs to reference `.doctrine-config` / `${LOCAL_DOCTRINE_ROOT}`.
- Update dependency validators to allow expected local override paths while rejecting broader cross-directory coupling.
