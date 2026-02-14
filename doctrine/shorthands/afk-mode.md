# Shorthand: afk-mode

**Alias:** `/afk-mode`  
**Category:** Session Management  
**Purpose:** Enable autonomous operation while human is away from keyboard  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Definition

**AFK Mode** (Away From Keyboard) is a session management shorthand that grants agents extended autonomy for incremental work with specific operational boundaries.

When a user declares "afk-mode" or uses the `/afk-mode` command, it activates the following operational protocol:

---

## Operational Parameters

### 1. Commit Frequency

**Instruction:** Commit often (after each logical unit of work)

**Rationale:** 
- Preserves work incrementally
- Enables rollback if needed
- Documents progress granularly
- Allows human to review commit history upon return

**Implementation:**
- Commit after each file edit/creation
- Commit after completing each sub-task
- Commit after validation passes
- Use descriptive commit messages with agent prefix

---

### 2. Commit Signing

**Instruction:** Commit without GPG signing

**Rationale:**
- Agent commits should be distinguishable from human commits
- GPG signing requires human interaction (password prompts)
- Repository config `.doctrine-config/config.yaml` specifies `commit_signing: false`

**Implementation:**
- Ensure `git config --local commit.gpgsign false` is set
- Verify unsigned commits with `git log --show-signature`

---

### 3. Push Permission

**Instruction:** Exceptional permission to push to remote

**Rationale:**
- Makes progress visible to human
- Enables work continuation across sessions
- Allows collaboration with other agents
- Prevents work loss if local environment fails

**Implementation:**
- Push after each commit (or logical batch of commits)
- Use current branch (do not push to main/master without explicit instruction)
- Push frequency: Every 1-3 commits or every 15 minutes of work

---

### 4. Decision Authority

**Instruction:** Permission to make decisions and small inferences

**Scope - MINOR DECISIONS (Autonomous):**
- File naming conventions (follow repository patterns)
- Directory organization (align with existing structure)
- Code formatting and style (follow existing conventions)
- Error message wording
- Variable/function naming
- Comment placement and wording
- Test data selection
- Minor refactoring (extract method, rename variable)
- Documentation phrasing and structure
- Cross-reference additions
- Link corrections

**Examples:**
- ✅ "Should I name this test_feature_x or feature_x_test?" → Choose based on pattern
- ✅ "Should I put this in utils/ or helpers/?" → Follow repository convention
- ✅ "Should I add a TODO comment here?" → Yes, if uncertainty exists

---

**Scope - CRITICAL DECISIONS (Pause & Wait):**
- Architectural changes (new patterns, paradigm shifts)
- Breaking API changes
- Database schema modifications
- Security policy changes
- Dependency additions/removals
- Major refactoring (rename core concepts, restructure modules)
- Deletion of existing features
- Technology stack changes
- Performance optimization trade-offs
- User-facing behavior changes
- Pricing/licensing decisions

**Action:** Create decision request in `work/human-in-charge/decision_requests/`

**Examples:**
- ❌ "Should I switch from REST to GraphQL?" → PAUSE, create decision request
- ❌ "Should I delete this deprecated module?" → PAUSE, create decision request
- ❌ "Should I add a new database table?" → PAUSE, create decision request

---

### 5. Escalation Protocol

**When to Pause:**

1. **Ambiguous Requirements:**
   - Requirement interpretation has multiple valid options
   - User story doesn't specify edge case behavior
   - Acceptance criteria are unclear

2. **Blockers:**
   - Missing credentials or access
   - Broken dependencies that cannot be auto-fixed
   - Test failures unrelated to current work

   **Action:** Create blocker in `work/human-in-charge/blockers/`

3. **Critical Decisions:**
   - See "Critical Decisions" scope above
   - Trade-offs with significant business impact
   - Changes affecting user privacy or security

   **Action:** Create decision request in `work/human-in-charge/decision_requests/`

4. **Unexpected Results:**
   - Tests pass but behavior seems wrong
   - Implementation significantly diverges from plan
   - Discovered constraints not mentioned in requirements

   **Action:** Create problem report in `work/human-in-charge/problems/`

**How to Pause:**
1. Stop current work
2. Commit completed work (if any)
3. Create escalation file in `work/human-in-charge/`:
   - Critical decisions → `decision_requests/`
   - External blockers → `blockers/`
   - Unexpected results → `problems/`
4. Update task status to `frozen` with reference to HiC file
5. Document in work log
6. Wait for human guidance

---

## Usage

### Activation

Human says one of:
- "afk-mode"
- "/afk-mode"
- "I'm going AFK, continue working"
- "AFK mode → commit often, exception permission to push"

### Acknowledgment

Agent responds:
```
✅ AFK Mode Activated

Operational Parameters:
- Commit frequency: After each logical unit
- Commit signing: Disabled (unsigned)
- Push permission: Granted (current branch)
- Decision authority: Minor decisions autonomous, critical decisions pause

Will pause for:
- Architectural changes
- Breaking changes
- Ambiguous requirements
- Blockers

Proceeding with: [task description]
```

### Deactivation

**Automatic:**
- Human returns and sends message
- Human explicitly says "AFK mode off" or "/exit-afk"

**Manual:**
- Agent completes all assigned work
- Agent encounters critical decision and pauses

---

## Example Session

**Human:**
```
AFK mode. Please complete the following tasks:
1. Fix typos in docs/guides/
2. Update README with new guide links
3. Add tests for feature X
```

**Agent:**
```
✅ AFK Mode Activated

Proceeding with 3 tasks. Will commit often and push progress.

Task 1: Fixing typos in docs/guides/...
[work happens]
Commit: "curator-claire: Fix typos in 3 guide files"
Push: ✓

Task 2: Updating README...
[work happens]
Commit: "curator-claire: Add new guide links to README"
Push: ✓

Task 3: Adding tests for feature X...
⏸️ PAUSED - Critical Decision Required

**Decision:** Test data strategy for feature X
- Option A: Use mocked data (fast, isolated)
- Option B: Use real database (slow, realistic)
- Option C: Use fixture files (middle ground)

**Recommendation:** Option C (fixture files)
**Rationale:** Balance between speed and realism

**Created:** work/human-in-charge/decision_requests/2026-02-14-test-data-strategy.md

Awaiting your choice before proceeding with test implementation.

**Completed:** 2/3 tasks
**Commits:** 2 (pushed)
**Status:** Paused at task 3 for guidance
```

---

## Related Directives

- **Directive 014:** Work Log Creation - Document AFK work in logs
- **Directive 018:** Traceable Decisions - Document decision rationale
- **Directive 040:** Human-in-Charge Escalation Protocol - Using HiC directory
- **.doctrine-config/config.yaml:** Repository-specific commit signing policy

---

## Notes

**Token Efficiency:**
- AFK mode doesn't change context loading strategy
- Still load directives on-demand
- Still use efficient tool patterns
- Focus: Autonomy boundaries, not context usage

**Quality Assurance:**
- Commit messages must be descriptive (what + why)
- Work logs required per Directive 014
- Self-review before pushing
- Run validation/tests before committing

**Safety:**
- Never commit secrets or credentials
- Never push to protected branches without explicit instruction
- Never delete files without verification
- Always preserve Git history (use git mv, not rm + add)

---

**Status:** ✅ Active  
**Maintained by:** Manager Mike, Planning Petra  
**Version:** 1.0.0  
**Last Updated:** 2026-02-08

---

## Related

- **Tactic:** `doctrine/tactics/autonomous-operation-protocol.tactic.md`
- **Directive 007:** Agent Declaration (operational authority)
- **Directive 024:** Self-Observation Protocol (checkpoints)
- **Directive 020:** Locality of Change (scope discipline)
