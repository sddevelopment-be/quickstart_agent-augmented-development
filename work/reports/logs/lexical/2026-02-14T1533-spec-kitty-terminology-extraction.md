# Specialist Report: Lexical

## Scope
Extract and normalize recurring domain terms from code and docs.

## Normalization Decisions
- Canonical: `work package` (`WPxx`) over ad hoc `task bundle` wording.
- Canonical: `lane` with values `planned`, `doing`, `for_review`, `done`.
- Canonical: `workspace-per-WP` model; legacy lane-directory model treated as deprecated term set.
- Canonical: `target_branch`, `base workspace`, `preflight`, `status resolver` in merge path semantics.
- Canonical: `mission`, `active mission`, `slash commands`, `agent context` for prompt/runtime context.

## High-Signal Term Families
- Spec lifecycle: `specify`, `plan`, `tasks`, `implement`, `review`, `accept`, `merge`.
- Git topology: `worktree`, `workspace`, `dependency graph`, `multi-parent merge`, `branch routing`.
- Runtime: `dashboard lifecycle`, `health check`, `diagnostics`, `event log`, `JSON output`.
- Distribution: `template source`, `migration registry`, `upgrade runner`, `manifest`.
- Hardening: `context validation`, `metadata validation`, `encoding validation`, `path validation`, `CSV schema enforcement`.
