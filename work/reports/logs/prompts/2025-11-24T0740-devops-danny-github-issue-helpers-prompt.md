# Original Prompt Documentation: Extract GitHub Issue Automation Helpers

**Task ID:** github-issue-helpers
**Agent:** DevOps Danny
**Date Executed:** 2025-11-24T07:40:29Z
**Documentation Date:** 2025-11-24T07:40:29Z

---

## Original Problem Statement

Initialize yourself according to the primary SDD agent reference in `/media/stijnd/DATA/development/projects/libraries/sd-templates/agents`. Start from the `AGENTS.md` file there, before proceeding to checking the current directory for an `AGENTS.md` file or `.agents` directory. If the current directory is a git repository, scan the `.github` directory for AGENT directives.

When initialized, bootstrap as Devops Danny. review the script `work/scripts/create-follow-up-issues.sh`, and extract helper functions/shell scripts to create github issues. Store these under the `ops/scripts` directory, and update the README.md and QUICKSTART.md files in that directory. Ensure you adhere to Devops Danny's directives, and directive 015. Update the main changelog with a condensed description of the new utility scripts. Commit often!

---

## SWOT Analysis

### Strengths
- Provided exact source script path (`work/scripts/create-follow-up-issues.sh`)
- Named target directory (`ops/scripts`) and docs to update (`README.md`, `QUICKSTART.md`)
- Explicitly referenced directive 015 plus agent profile, preventing guesswork on governance
- Requested changelog entry and commit cadence, clarifying delivery expectations

### Weaknesses
- No guidance on desired CLI interface for the extracted helpers
- Did not clarify whether helpers should be libraries, standalone scripts, or both
- Documentation scope ambiguous (ops docs mainly focus on OpenCode tooling, so tone/structure alignment required interpretation)
- “Commit often” lacks target granularity (per feature, per file, etc.)

### Opportunities
- Suggest referencing GitHub CLI requirements and example invocations in docs
- Offer both a helper library and CLI wrapper to satisfy multiple automation styles
- Capture request quality via Directive 015 to strengthen future prompt iterations
- Recommend explicit success criteria (tests, validations) for scripts touching GitHub APIs

### Threats
- Without defining CLI expectations, helper design might miss downstream integration needs
- Ambiguous documentation focus could cause mismatched tone with existing OpenCode sections
- Lack of body source guidance might create drift between script heredocs and canonical markdown issue files
- Vague commit cadence instruction could lead to over/under-committing

---

## Suggested Improvements

### Version 2.0: Enhanced Prompt

```
Bootstrap using the primary SDD agent reference under /media/stijnd/DATA/development/projects/libraries/sd-templates/agents (load repo AGENTS afterward, scan .github). Run as DevOps Danny.

Task: refactor work/scripts/create-follow-up-issues.sh so all GitHub issue creation logic lives in reusable ops/scripts utilities.

Deliverables:
1. ops/scripts/github-issue-helpers.sh (Bash library): exposes functions to load issue bodies from files/fallback text and wrap `gh issue create`, handling labels/assignees. Include basic logging + CLI presence checks.
2. ops/scripts/create-github-issue.sh (executable): accepts --repo/--title/--body[(-file)]/--label/--assignee/--milestone/--draft arguments and pipes content into the helper.
3. work/scripts/create-follow-up-issues.sh updated to source the helper rather than calling `gh` directly.
4. ops/README.md and ops/QUICKSTART.md updated with usage instructions + examples for both new scripts (mention gh dependency).
5. CHANGELOG.md `[Unreleased]` gains a concise note about the new GitHub issue automation utilities.
6. Directive 015 prompt documentation stored under `work/logs/prompts/` with SWOT + improved prompt.

Acceptance:
- Shellcheck passes on new scripts.
- Scripts remain ASCII + executable.
- At least two commits (scripts, then docs/changelog/prompt) on copilot/review-issue-8-final-iteration.
```

### Improvements Explained

**1. Deliverable granularity:**
- What changed: Broke requirements into numbered artifacts (library, CLI, refactor, docs, changelog, prompt doc).
- Why: Removes ambiguity about expected outputs and helps scope reviews.
- Impact: Easier verification + reduces risk of missing a file.

**2. Interface specification:**
- What changed: Defined CLI arguments + helper behavior.
- Why: Prevents misaligned implementations and mismatched downstream usage.
- Impact: Consumers can rely on a stable interface without reading source first.

**3. Acceptance gates:**
- What changed: Added shellcheck, ASCII, and commit count expectations.
- Why: The original “commit often” was vague; this provides measurable checks.
- Impact: Encourages disciplined delivery and reduces follow-up clarifications.

**4. Directive compliance reminder:**
- What changed: Called out Directive 015 deliverable explicitly.
- Why: The original prompt cited the directive but not the expected artifact.
- Impact: Ensures documentation isn’t skipped under time pressure.

---

## Pattern Recognition

### Effective Prompt Elements
+ Precise file paths minimized search overhead.
+ Mentioning directives up front aligned the work with governance requirements.
+ Multi-step instruction order (initialize, bootstrap, edit, update docs, commit) set a high-level workflow.

### Improvement Targets
+ Future prompts benefit from enumerated deliverables and acceptance criteria.
+ Include interface sketches for new scripts/utilities to reduce assumption-driven work.
+ State exact commit strategy (e.g., “Commit scripts, then docs”).

### Observed Risks
+ Commands referencing GitHub could require auth; prompts should clarify whether to run them or mock.
+ Mixing infrastructure tasks (helper extraction) with documentation updates without priority hints can cause scope creep.
+ Without examples, doc updates risk tonal drift from existing content.

---

## Suggested Follow-Up Actions

1. Maintain a lightweight template for scripting prompts that captures deliverables, acceptance checks, and governance references.
2. Share this prompt documentation with other task authors to reinforce Directive 015 adoption.
3. Consider linking existing doc focus areas (OpenCode vs Ops automation) so future prompts specify which section to expand.

---

**References:** Directive 015 (Store Prompts) compliance log.
