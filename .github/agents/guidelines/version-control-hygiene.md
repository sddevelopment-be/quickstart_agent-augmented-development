# Version Control Hygiene

**Version:** 1.0.0  
**Last Updated:** 2026-02-08  
**Status:** Active

---

## Purpose

Keep commits easy to review, search, and audit. Use consistent, scoped messages and avoid mixing unrelated changes. This guideline supports collaborative development, agent-augmented workflows, and long-term maintainability.

---

## Commit Message Format

### Conventional Commits Standard

Use a conventional, scoped prefix: `type(scope): summary`

**Examples:**
- `feat(orchestration): add timeout handling for task execution`
- `fix(tests): stabilize agent orchestrator e2e tests`
- `docs(readme): update installation instructions`
- `refactor(agents): extract common validation logic`
- `chore(deps): update black to 25.11.0`
- `architecture(adr): add ADR-NNN (caching strategy) for caching strategy`

### Type Prefixes

| Type | Usage | Examples |
|------|-------|----------|
| `feat` | New feature or capability | `feat(api): add rate limiting` |
| `fix` | Bug fix | `fix(parser): handle empty input` |
| `docs` | Documentation changes | `docs(guide): clarify setup steps` |
| `refactor` | Code restructuring (no behavior change) | `refactor(utils): extract helper functions` |
| `test` | Test additions or fixes | `test(unit): add edge case coverage` |
| `chore` | Maintenance tasks | `chore(ci): update workflow triggers` |
| `architecture` | Design decisions, ADRs | `architecture(adr): document service boundaries` |
| `restructure` | Major organizational changes | `restructure(repo): consolidate test directories` |

### Message Guidelines

**Summary Line:**
- Keep under 72 characters
- Be specific about the change, not the intent
- Use imperative mood ("add feature" not "added feature")
- Don't end with a period

**Body (Optional):**
- Separate from summary with blank line
- Explain *why* the change was made, not *what* changed
- Reference issues, ADRs, or related work
- Use bullet points for multiple points

**Examples:**

```
feat(orchestration): add configurable task timeouts

Enables users to specify per-task execution limits to prevent
runaway processes. Defaults to 30 minutes if not specified.

Related: Directive 018 (Traceable Decisions) (Traceable Decisions)
Closes: #142
```

---

## Commit Content Guidelines

### One Logical Change Per Commit

**Principle:** Each commit should represent a single, complete, logical change.

✅ **Do:**
- Fix one bug per commit
- Add one feature per commit
- Refactor one module per commit
- Update related tests in the same commit as code changes

❌ **Don't:**
- Mix feature additions with refactoring
- Combine bug fixes across unrelated modules
- Bundle formatting changes with logic changes
- Include unrelated file modifications

### Respect Existing Worktree

**Principle:** Don't stage or revert files you didn't intentionally modify.

✅ **Do:**
- Review `git status` before committing
- Use `git add -p` for selective staging
- Preserve others' uncommitted work
- Ask before touching shared configuration

❌ **Don't:**
- Stage all changes blindly (`git add .`)
- Revert files to resolve conflicts without discussion
- Modify unrelated files "while you're there"
- Delete or move others' work-in-progress

### Additive Changes Preferred

**Principle:** Favor additive, non-destructive changes unless explicitly required.

✅ **Do:**
- Add new functions alongside old ones
- Create new directories for new organization
- Deprecate before removing
- Preserve backward compatibility when reasonable

❌ **Don't:**
- Delete working code without clear justification
- Rename core APIs without migration path
- Remove features without stakeholder agreement
- Break existing integrations

### Documentation Synchronization

**Principle:** Keep documentation aligned with code changes.

**Update when:**
- Public APIs change
- Configuration formats evolve
- User-facing behavior modifies
- Architecture decisions finalize

**What to update:**
- README files
- CHANGELOG entries
- API documentation
- Architecture Decision Records
- Inline code comments (when clarification needed)

---

## Branch Hygiene

### Rebase or Merge Frequently

**Principle:** Reduce drift by staying synchronized with main branch.

✅ **Do:**
- Rebase feature branches daily (or before each push)
- Resolve conflicts locally before pushing
- Keep branches short-lived (<24 hours ideal)
- Delete merged branches promptly

❌ **Don't:**
- Let feature branches diverge for weeks
- Push conflicting changes to shared branches
- Accumulate multiple merge commits
- Keep abandoned branches indefinitely

### Focused Feature Branches

**Principle:** Each branch should have a clear, narrow scope.

✅ **Do:**
- Name branches descriptively (`feat/timeout-handling`, `fix/parser-edge-case`)
- Complete one feature per branch
- Keep branches small and reviewable
- Create new branch for unrelated work

❌ **Don't:**
- Accumulate unrelated changes in one branch
- Mix features, fixes, and refactoring
- Create generic branch names (`updates`, `fixes`, `dev`)
- Reuse branches for different purposes

---

## Reviewability

### Small, Reviewable Commits

**Principle:** Favor commits that can be reviewed in <10 minutes.

**Size Guidelines:**
- **Ideal:** 50-200 lines changed
- **Acceptable:** 200-500 lines changed
- **Large:** 500-1000 lines (needs justification)
- **Too Large:** >1000 lines (split into logical commits)

**Split large changes by:**
- Preparation (refactoring, setup)
- Implementation (core logic)
- Integration (wiring, configuration)
- Documentation (README, CHANGELOG)

### Clear Diffs

**Principle:** Make changes easy to understand through diff review.

✅ **Do:**
- Format code before logic changes (separate commits)
- Use meaningful variable/function names
- Extract complex logic into named functions
- Add comments for non-obvious decisions

❌ **Don't:**
- Mix formatting and logic in one commit
- Rename variables while changing logic
- Introduce whitespace-only changes randomly
- Obfuscate intent through clever code

### Validation Evidence

**Principle:** Include or reference evidence that changes work.

**When behavior changes:**
- Mention test additions in commit message
- Reference manual validation steps
- Link to CI/CD run showing green tests
- Note regression testing performed

**Example:**
```
fix(parser): handle empty input gracefully

Now returns empty result set instead of raising exception.

Tests: Added test_parse_empty_input() covering edge case
Validated: Manual testing with production data samples
```

---

## Safety

### Destructive Command Warnings

**Principle:** Never use destructive Git commands on shared work without explicit approval.

❌ **NEVER do (on shared branches):**
- `git reset --hard` (destroys uncommitted work)
- `git checkout -- <file>` (overwrites local changes)
- `git clean -fd` (deletes untracked files)
- `git push --force` (rewrites shared history)
- `git branch -D` (force-deletes unmerged branches)

✅ **Safe alternatives:**
- `git stash` (preserves work temporarily)
- `git stash pop` (restores stashed work)
- `git commit -m "wip"` (save work before switching)
- `git revert` (creates new commit undoing changes)
- `git merge --abort` (safely exit merge conflicts)

### Collaboration Safety

**When uncertain:**
1. Ask before modifying others' files
2. Communicate before force-pushing
3. Discuss before reverting merged commits
4. Coordinate before major restructuring

**If you must use destructive commands:**
1. Announce intent in team chat
2. Verify no conflicts with others' work
3. Create backup branch first
4. Document rationale in commit message

---

## Agent-Specific Conventions

### Agent Identity in Commits

When an agent performs work:

```
feat(orchestration): add retry logic for failed tasks

Implemented by: Agent DevOps-Danny
Reviewed by: Human reviewer (stijn)
```

### Multi-Agent Coordination

When multiple agents contribute:

```
refactor(tests): improve test readability

Contributors:
- Agent Pedro: Test structure refactoring
- Agent Benny: Assertion clarity improvements
- Human: Final review and adjustments
```

---

## References

- **Conventional Commits:** https://www.conventionalcommits.org/
- **Git Best Practices:** https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project
- **Related Guidelines:** `doctrine/guidelines/python-conventions.md`
- **Traceable Decisions:** `doctrine/directives/018_traceable_decisions.md`

---

## Version History

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.0.0   | 2026-02-08 | Extracted from saboteurs styleguides, added agent-specific conventions |

---

**Maintained by:** SDD Framework Contributors  
**Review Cycle:** Annually or when Git workflows evolve  
**Status:** Active guideline for all agent-augmented development
