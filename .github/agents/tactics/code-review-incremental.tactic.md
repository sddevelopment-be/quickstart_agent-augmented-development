# Tactic: CodeReview.Incremental

**Invoked by:**
- [Directive 021 (Locality of Change)](../directives/021_locality_of_change.md) — reviewing changes without expanding scope

**Related tactics:**
- (Standalone — focuses on incremental review discipline)

**Complements:**
- [Directive 021 (Locality of Change)](../directives/021_locality_of_change.md)
- Approach: Trunk-Based Development

---

## Intent

Review a change set to identify correctness, structural, and architectural risks without rewriting or expanding scope.

## Preconditions

**Required inputs:**
- A concrete diff or commit range exists

**Assumed context:**
- Reviewer is not responsible for implementing fixes
- No new features are introduced during review
- Change is scoped and bounded (not massive refactor)

**Exclusions (when NOT to use):**
- Initial code contributions requiring architectural guidance
- Major refactoring where scope expansion is necessary
- Emergency hotfixes requiring immediate action without review

## Execution Steps
1. Read the commit message or change description without opening files.
2. Scan the diff to identify touched modules and files.
3. Read modified files in full, without commenting.
4. Summarize the apparent intent of the change in one paragraph.
5. Identify risks in the following order:
   - correctness
   - architectural boundaries
   - maintainability
   - unintended side effects
6. Formulate feedback as observations and questions, not instructions.
7. Stop.

## Checks / Exit Criteria
- A written intent summary exists.
- At least one risk category has been considered.
- No code changes have been made.

## Failure Modes
- Suggesting refactors unrelated to the change.
- Rewriting code mentally instead of reviewing it.
- Treating stylistic preference as correctness issues.

## Outputs

**Review summary:**
```
Change Intent: [One paragraph describing what the change attempts to accomplish]

Risks Identified:
- [Correctness] Issue description and question for author
- [Architecture] Boundary concern and potential impact
- [Maintainability] Long-term concern or suggestion

Overall Assessment: [Approve / Request Changes / Comment]
```

**Format guidelines:**
- Use observations language ("I notice...", "This appears to...")
- Frame concerns as questions ("Does this handle...", "What happens when...")
- Avoid prescriptive commands ("Change X to Y")
- Reference specific lines/files in feedback

## Notes

**Review discipline:**
- Resist urge to redesign during review
- Focus on correctness and architectural fit, not style
- Keep feedback proportional to change size
- Distinguish between blocking issues and suggestions

**Integration with Locality of Change:**
- Flag changes that expand scope beyond stated intent
- Question additions unrelated to primary change
- Verify change doesn't introduce premature optimization

**Timing:**
- 5-15 minutes for small changes (<200 lines)
- 15-30 minutes for medium changes (200-500 lines)
- Request decomposition for changes >500 lines
