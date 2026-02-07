# Version Control Hygiene

**Purpose:** Keep commits easy to review, search, and audit. Use consistent, scoped messages and avoid mixing unrelated changes.

## Commit Message Format
- Use a conventional, scoped prefix: `type(scope): summary`
  - Examples: `chore(sally): update changelog for branch changes`, `feat(orchestration): add timeout handling`, `fix(tests): stabilize agent orchestrator e2e`, `restructure(agents): move orchestrator to orchestrator package`, `refactor(tests): improve test readability`, `docs(readme): update readme`, `architecture(feature planning): add design documents for upcoming feature <slug>`
- Keep the summary under ~72 characters; be specific about the change, not the intent.
- If representing a persona/agent, include the persona in the scope (e.g., `chore(sally): …`).

## Commit Content Guidelines
- One logical change per commit; avoid bundling unrelated edits.
- Don’t stage or revert files you didn’t touch; respect existing worktree changes.
- Prefer additive, non-destructive changes unless explicitly required.
- Ensure changelog/README/docs are updated when behavior, interfaces, or user-facing docs change.

## Branch Hygiene
- Rebase or merge frequently to reduce drift; resolve conflicts locally before pushing.
- Keep feature branches focused; avoid long-lived branches accumulating unrelated work.

## Reviewability
- Favor small, reviewable commits; split large changes into coherent steps.
- Include tests or notes on validation when behavior changes.
- Use clear diffs: avoid churn from formatting unless formatting was the goal.

## Safety
- Never use destructive git commands (`reset --hard`, `checkout --`) on shared work unless explicitly approved.
- Do not delete or move others’ uncommitted work; if in doubt, ask.
