# Domain Map (Spec Kitty Terminology)

## Domains
1. **Specification Lifecycle and Work Package Management**
Core terms: `specify`, `plan`, `tasks`, `work package`, `lane`, `finalize-tasks`, `review`, `accept`.

2. **Workspace and Branch Topology**
Core terms: `worktree`, `workspace`, `base workspace`, `target branch`, `dependency graph`, `merge preflight`.

3. **Agent and Mission Orchestration**
Core terms: `agent context`, `supported agents`, `mission`, `active mission`, `slash commands`, `workflow commands`.

4. **Dashboard and Runtime Observability**
Core terms: `dashboard lifecycle`, `health check`, `diagnostics`, `scanner`, `event log`, `status reporting`.

5. **Template, Migration, and Upgrade Distribution**
Core terms: `template source`, `command templates`, `migration registry`, `upgrade`, `manifest`, `packaging safety`.

6. **Quality, Validation, and Adversarial Hardening**
Core terms: `context validation`, `metadata validation`, `plan validation`, `encoding validation`, `path validation`, `CSV schema`.

## Key Boundaries
- `lane` semantics belong to lifecycle domain, while merge semantics belong to topology domain.
- `mission` semantics belong to orchestration domain, while template propagation belongs to distribution domain.
- `dashboard` terms express runtime state, but validation terms enforce correctness across lifecycle and distribution.

## Cross-Domain Translation Seams
- `tasks.md` dependencies -> worktree/workspace creation rules.
- `for_review`/`done` lanes -> merge preflight and branch routing decisions.
- mission + agent configuration -> generated template and command behavior.
- dashboard diagnostics/event logs -> release and acceptance validation gates.
