# Agent-Enhanced Test Validation for Coaches and Engineers

**Audience:** Technical coaches, process architects, software engineers  
**Purpose:** Teach a repeatable way to check whether tests double as accurate documentation.  
**Based on:** Dual-agent experiment (92% accuracy from tests alone, 65 minutes, 66 tests across 3 files)

## Why This Matters
- Tests are often the freshest description of behavior, but we rarely verify their readability or completeness.
- A fast dual-agent pass tells you if tests explain the system well enough for onboarding and change risk assessment.
- The method surfaced architectural blind spots (rationale, operations, security) even when behavioral coverage was excellent.

## The Approach (Dual-Agent Loop)
1. **Researcher Ralph (tests-only):** Reads specified test files, reconstructs system behavior, data, and workflows. No docs, no comments. Output: system analysis with confidence levels.
2. **Architect Alphonso (full-context):** Compares Ralph’s understanding to source + ADRs, scores accuracy, and lists blind spots and fixes.
3. **Wrap-up:** Work log + prompt storage (Directives 014, 015) keep the run auditable and repeatable.

## What We Learned in the Pilot
- **Behavioral clarity:** Tests documented workflows, edge cases, and data structures so well that Ralph hit **92% overall accuracy** without docs.
- **Gaps:** Rationale (file-based, single-orchestrator), operations (cron cadence, agent lifecycle), security boundaries, and performance envelope were invisible.
- **Recommendations that worked:** Add ADR links in docstrings for intent-heavy areas, add deployment/operational scenarios, add performance/security probes, and document the single-orchestrator constraint.

## How to Run It on Your Codebase
- **Scope it:** Pick a module or feature with ~50-100 tests; avoid sprawling suites for the first run.
- **Prep:** Use the prompt template at `docs/templates/prompts/TEST_READABILITY_CHECK.prompt.md`; set time boxes (30m Ralph, 20m Alphonso).
- **Execute:** Enforce “tests only” for Ralph. Alphonso must read ADRs or design notes to spot rationale gaps.
- **Score:** Separate behavioral vs. architectural vs. operational accuracy. Keep the rubric simple (High/Medium/Low with one-line evidence).
- **Track:** Save outputs under `work/notes/` and work logs under `work/reports/logs/` for trend comparisons.

## Benefits for Engineering Teams
- **Onboarding shortcut:** A new dev can get a trustworthy system map in under an hour by reading the tests plus Alphonso’s deltas.
- **Change safety:** Highlights where tests stop documenting intent, which is often where regressions hide.
- **Refactoring guide:** Alphonso’s blind spots translate directly into a test-improvement backlog.
- **Process agility:** Repeat quarterly or before releases to keep test documentation quality visible.

## Tradeoffs and Mitigations
- **Time cost (~65 minutes):** Limit to milestones; keep scope tight. Automate test discovery to save setup time.
- **Subjectivity in scoring:** Use a tiny rubric and require evidence lines for every rating.
- **Staleness risk:** Date-stamp outputs and rerun after significant test changes.
- **Token/compute load:** Keep prompts lean; avoid running on entire monorepos.

## Quick Start Checklist
- [ ] Scope defined (which test files, which module)  
- [ ] Time boxes set (30m + 20m)  
- [ ] Prompt filled (`TEST_READABILITY_CHECK.prompt.md`)  
- [ ] Ralph output saved to `work/notes/`  
- [ ] Alphonso review saved with accuracy scores and recommendations  
- [ ] Work log and prompt storage captured  

**Next:** Pilot this on one critical module. If accuracy <85% or blind spots block onboarding, prioritize the recommended test additions.
