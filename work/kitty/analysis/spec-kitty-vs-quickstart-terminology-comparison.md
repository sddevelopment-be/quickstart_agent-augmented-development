# Lexical Comparison: Spec Kitty vs Quickstart Doctrine Terminology

- Analyst role used: `lexical`
- Date: 2026-02-14
- Inputs:
  - Spec Kitty terminology: `work/kitty/glossary/core-terminology.md`
  - This repo terminology baseline: `doctrine/GLOSSARY.md`

## Summary
The two vocabularies overlap strongly at the **conceptual level** (workflow governance, validation, orchestration), but diverge in **operational surface language**.

- Spec Kitty is product/runtime oriented (WP lanes, worktrees, dashboard lifecycle, migration registry).
- This repository is doctrine/orchestration oriented (directives, tactics, agent roles, mode protocols, HiC governance).

## Overlaps
1. **Spec-driven workflow philosophy**
- Spec Kitty: `Spec-Driven Development (SDD)`
- This repo: `Specification-Driven Development`, `6-Phase Spec-Driven Implementation Flow`

2. **Validation and hardening discipline**
- Spec Kitty: `Context Validation`, `Path Validation`, `Encoding Validation`, `Plan Validation`, `Adversarial Suite`
- This repo: `Fail-Fast Validation`, `Adversarial Testing`, `Adversarial Acceptance Testing`, `Acceptance Boundary`, `Coverage Threshold`

3. **Multi-agent coordination semantics**
- Spec Kitty: `Agent Context`, `Supported Agents`, `Workflow Commands`, `Slash Commands`
- This repo: `Agent Assignment`, `Agent Profile`, `Agent Specialization Hierarchy`, `AGENT_STATUS`, `HANDOFFS`

4. **Configuration/metadata contract thinking**
- Spec Kitty: `Manifest`, `Metadata Validation`
- This repo: `Manifest`, `Metadata Header`, `Doctrine Configuration`

## Discrepancies
1. **Lifecycle state model mismatch**
- Spec Kitty has explicit WP lane semantics (`planned`, `doing`, `for_review`, `done`) and CLI transitions (`finalize-tasks`, `accept`, `merge preflight`).
- This repo glossary does not use lane-state vocabulary as a core control model.

2. **Workspace semantics differ**
- Spec Kitty: `workspace`/`worktree` means git-isolated WP execution context.
- This repo: `workspace_root`/`work/` means collaboration artifact space and orchestration logs.

3. **Governance abstraction level differs**
- Spec Kitty emphasizes runtime and release mechanics (`dashboard lifecycle`, `migration registry`, `upgrade runner`).
- This repo emphasizes doctrine governance (`directives`, `tactics`, `approaches`, mode protocol symbols).

4. **Command vocabulary differs in intent**
- Spec Kitty commands are product lifecycle commands (`/spec-kitty.plan`, `agent workflow ...`).
- This repo command aliases are reasoning/process controls (`/analysis-mode`, `/meta-mode`, `/validate-alignment`).

5. **Domain scoping differs**
- Spec Kitty uses `mission` and `active mission` as domain-profile selectors.
- This repo does not center terminology around mission selection; it centers around agent specialization and doctrine layering.

## Potential Normalization Opportunities
1. Add a crosswalk table for shared terms with different meanings (`workspace`, `review`, `accept`, `manifest`).
2. Introduce explicit mapping between Spec Kitty lifecycle phases and this repo’s doctrine phase language.
3. Add Spec Kitty-specific terms (`lane`, `finalize-tasks`, `merge preflight`) to a local extension glossary if this integration continues.

## Quick Crosswalk (Suggested)
| Concept | Spec Kitty term | This repo term |
|---|---|---|
| Spec-first delivery | Spec-Driven Development (SDD) | Specification-Driven Development |
| Work unit | Work Package (WP) | Task / Initiative Task |
| State progression | Lane (`planned` -> `done`) | Task lifecycle (`new` -> `done`) |
| Operational context | Workspace / Worktree | `work/` collaboration workspace |
| Orchestration ledger | Event Log / Dashboard status | `AGENT_STATUS` / `WORKFLOW_LOG` |
| Validation gate | Plan/Metadata/Path validation | Fail-Fast / Acceptance / Validation directives |

## Note on Matching Method
Exact string matching found very few direct matches; findings above are based on semantic alignment across glossary definitions and usage context.
