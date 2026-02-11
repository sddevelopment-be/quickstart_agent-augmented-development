# Directive 036: Boy Scout Rule

**Status:** Active  
**Applies To:** All agents (especially coding and documentation agents)  
**Priority:** HIGH - Mandatory pre-task check  
**Version:** 1.0.0  
**Last Updated:** 2026-02-09

---

## Purpose

Enforce the Boy Scout Rule: **"Leave the code/campground/repository better than you found it."**

Every task begins with a quick spot check of the surrounding area. Improvements discovered must be executed **before** starting new work to avoid enlarging technical debt or compounding existing issues.

---

## The Rule

> **Always leave the codebase cleaner than you found it.**  
> — Adapted from Robert C. Martin's "Clean Code"

This applies to:
- Code quality (formatting, naming, structure)
- Documentation accuracy (outdated comments, broken links, missing context)
- Test coverage (missing tests, flaky tests, unclear assertions)
- Technical debt markers (TODO comments, deprecated APIs, known issues)

---

## Pre-Task Spot Check Protocol

### Before Starting Any Task

**1. Scan the Working Area (2-5 minutes)**

Examine files you'll be touching plus immediate neighbors:

```bash
# Example for Python task in src/framework/orchestration/
- Review: src/framework/orchestration/*.py
- Check: Adjacent modules that import or are imported
- Scan: Related test files in tests/unit/framework/orchestration/
```

**2. Identify Quick Wins**

Look for issues that take <5 minutes to fix:

✅ **Code Quality:**
- Inconsistent formatting (run Black/Prettier)
- Unused imports
- Magic numbers without constants
- Unclear variable names
- Missing type hints

✅ **Documentation:**
- Outdated docstrings
- Broken markdown links
- Missing ADR references
- Stale TODO comments
- Incorrect file headers

✅ **Testing:**
- Missing Quad-A structure labels
- Unclear test names
- Commented-out test code
- Assertion messages missing

✅ **Structure:**
- Files in wrong directories
- Inconsistent naming conventions
- Duplicate code fragments

**3. Decision Point**

| Finding Type | Action | Timing |
|-------------|--------|--------|
| **Quick fix (<5 min)** | Fix immediately, commit separately | Before task |
| **Medium fix (5-15 min)** | Fix if time permits, commit separately | Before or during task |
| **Large fix (>15 min)** | Create task, document in work log | Defer to backlog |
| **Systemic issue** | Document, escalate to architect/planner | Create initiative |

---

## Execution Guidelines

### When to Apply

**ALWAYS before:**
- Feature implementation
- Bug fixes
- Refactoring work
- Documentation updates
- Test additions

**OPTIONAL for:**
- Emergency hotfixes (defer to follow-up)
- Trivial one-line changes
- Automated tool outputs

### How to Apply

**Step 1: Spot Check (2-5 min)**
```bash
# Example Python workflow
cd src/target/area
rg "TODO|FIXME|HACK" .  # Find technical debt markers
python -m ruff check .  # Run linter
python -m black --check .  # Check formatting
```

**Step 2: Fix Quick Issues (0-10 min)**
```bash
python -m black .  # Auto-format
python -m ruff check . --fix  # Auto-fix linting issues
# Manual fixes: rename variables, update docstrings, fix typos
```

**Step 3: Commit Separately**
```bash
git add -p  # Stage cleanup changes
git commit -m "chore: Apply Boy Scout Rule cleanup in src/target/area

- Format code with Black
- Fix ruff warnings (unused imports, etc.)
- Update stale docstrings
- Add missing type hints to public functions

Pre-task cleanup before [TASK-ID]"
```

**Step 4: Proceed with Original Task**

Now start your planned work with a clean foundation.

---

## Commit Strategy

**Critical:** Boy Scout cleanups MUST be separate commits from feature work.

### ✅ Good: Separate Commits
```
commit abc1234: chore: Boy Scout cleanup - format and fix linting
commit def5678: feat: Add status enum validation (TASK-2026-02-09-001)
```

### ❌ Bad: Mixed Commit
```
commit xyz9999: feat: Add status enum + cleanup surrounding code
```

**Rationale:**
- Reviewers can distinguish cleanup from functionality
- Git bisect works correctly
- Rollback is targeted (revert feature, keep cleanup)
- Code archaeology is clear (why did this change?)

---

## Scope Boundaries

### What Counts as "Better"?

**In Scope (Always):**
- Code formatting compliance
- Linting rule compliance
- Docstring accuracy
- Type hint completeness
- Test structure (Quad-A pattern)
- Removing commented-out code
- Fixing typos in comments/docs

**Out of Scope (Requires Approval):**
- Changing functionality or behavior
- Refactoring algorithms
- Renaming public APIs
- Restructuring modules
- Adding new features "while you're there"
- Performance optimizations

**Rule of Thumb:** If it changes observable behavior or requires regression testing, it's **not** a Boy Scout cleanup—it's a separate task.

---

## Anti-Patterns to Avoid

### ❌ Don't: Scope Creep
```python
# Started: Fix typo in docstring
# Ended: Rewrote entire module architecture
```
**Problem:** Original task delayed, new bugs introduced.  
**Solution:** Document larger issues, create follow-up tasks.

### ❌ Don't: Gold Plating
```python
# Found: One unused import
# Did: Refactored entire import strategy across 15 files
```
**Problem:** Massive diff obscures original intent.  
**Solution:** Fix the one import, document systemic issue for planning.

### ❌ Don't: Skip the Commit Boundary
```
git commit -m "feat: Add validation + fix formatting + update tests"
```
**Problem:** Reviewer can't distinguish feature from cleanup.  
**Solution:** Two commits (cleanup, then feature).

### ❌ Don't: Ignore Pre-Existing Failures
```python
# Found: 3 failing tests in module
# Did: Added new code anyway
```
**Problem:** Can't distinguish new regressions from old.  
**Solution:** Fix or document pre-existing failures first.

---

## Integration with Other Directives

### Directive 017 (TDD)
Boy Scout cleanup happens **before** Red-Green-Refactor cycle:
1. **Boy Scout:** Clean surrounding area
2. **RED:** Write failing test
3. **GREEN:** Make test pass
4. **REFACTOR:** Improve implementation

### Directive 020 (Locality of Change)
Boy Scout cleanups respect locality:
- Fix issues in files you're already touching
- Don't wander into unrelated modules
- Document systemic issues for strategic planning

### Directive 026 (Commit Protocol)
Boy Scout commits follow standard conventions:
- Prefix: `chore: Boy Scout cleanup in <area>`
- Body: Bullet list of specific fixes
- Footer: Reference to upcoming task (optional)

### Directive 028 (Bug Fixing)
When fixing bugs:
1. **Boy Scout:** Clean area around bug
2. **Write failing test:** Reproduce bug
3. **Fix bug:** Make test pass
4. **Refactor:** Improve fix quality

---

## Agent-Specific Guidance

### Python Pedro (Python Development)
**Pre-task checklist:**
```bash
python -m black <target>  # Format
python -m ruff check <target> --fix  # Lint
python -m mypy <target>  # Type check
rg "# TODO" <target>  # Find stale TODOs
```

### Backend Benny (Backend Services)
**Pre-task checklist:**
- Check for deprecated API usage
- Update dependency versions if patch available
- Fix security warnings from linters
- Update API documentation if stale

### Java Jenny (Java Development)
**Pre-task checklist:**
```bash
./gradlew spotlessApply  # Format
./gradlew checkstyleMain  # Style check
rg "@Deprecated" src/  # Find deprecated usage
rg "TODO|FIXME" src/  # Find technical debt
```

### Writer-Editor Eddy (Documentation)
**Pre-task checklist:**
- Fix broken markdown links
- Update stale dates/versions
- Fix typos and grammar
- Validate code examples still work
- Check ADR references are correct

### Curator Claire (Directory Curation)
**Pre-task checklist:**
- Remove duplicate files
- Rename inconsistently named files
- Update README.md files
- Validate directory structure
- Archive obsolete content

---

## Measurement & Accountability

### Success Metrics

Track Boy Scout activity in work logs:

```markdown
## Boy Scout Cleanup (Pre-Task)

**Time:** 5 minutes  
**Scope:** src/framework/orchestration/  
**Findings:**
- 3 files missing type hints
- 2 stale TODO comments (resolved or documented)
- 1 deprecated API usage
- Formatting drift (15 lines)

**Actions Taken:**
- Added type hints to public functions
- Removed resolved TODOs, created tasks for others
- Replaced deprecated API with current equivalent
- Ran Black formatter

**Commit:** abc1234 - chore: Boy Scout cleanup in orchestration module
```

### Quality Gates

Boy Scout cleanup should:
- Take <10% of task time (if longer, defer to separate task)
- Not introduce new test failures
- Not change observable behavior
- Be committed separately from feature work

---

## Escalation Protocol

### When Boy Scout Reveals Systemic Issues

If spot check uncovers:
- Widespread inconsistency (naming, structure, patterns)
- Missing tests across multiple modules
- Deprecated practices throughout codebase
- Architecture violations

**DO NOT fix everything.**

**Instead:**
1. Fix immediate area only (maintain locality)
2. Document systemic issue in work log
3. Create task for Planning Petra:
   ```yaml
   title: "[TECHNICAL DEBT] Systemic issue: <description>"
   priority: medium
   scope: codebase-wide
   effort: <estimate>
   rationale: "Discovered during Boy Scout check in <area>"
   ```
4. Continue with original task

**Rationale:** Systemic fixes require:
- Architecture review
- Coordinated migration strategy
- Adequate testing across affected areas
- Risk assessment

These exceed Boy Scout scope and belong in planned initiatives.

---

## Examples

### Example 1: Python Feature Addition

**Task:** Add `TaskStatus.CANCELLED` enum value

**Boy Scout Check:**
```bash
cd src/common/
python -m black types.py  # Formats file
python -m ruff check types.py  # Finds unused import
# Manual: Notice docstring outdated
```

**Boy Scout Fixes:**
```python
# Before
from typing import List, Dict  # Dict unused
class TaskStatus(str, Enum):
    """Task states (updated 2025-11-01)"""  # Stale date
    
# After
from typing import List  # Removed unused import
class TaskStatus(str, Enum):
    """Task lifecycle states (see domain model docs)"""  # Updated, added reference
```

**Commit:**
```bash
git commit -m "chore: Boy Scout cleanup in src/common/types.py

- Remove unused Dict import
- Update docstring with domain model reference
- Format with Black

Pre-task cleanup before adding CANCELLED status"
```

**Then:** Proceed with adding `CANCELLED` enum value (separate commit).

---

### Example 2: Documentation Update

**Task:** Update README.md with new installation instructions

**Boy Scout Check:**
```bash
cd docs/
# Manual review finds:
# - Broken link to architecture decision record
# - Stale "last updated" date
# - Typo: "recieve" → "receive"
```

**Boy Scout Fixes:**
```markdown
# Before
Last updated: 2025-08-15
See [ADR-001](../adrs/ADR-001.md) for details.
To recieve updates...

# After
Last updated: 2026-02-09
See [ADR-001](../architecture/adrs/ADR-001-modular-agent-directive-system.md)
To receive updates...
```

**Commit:**
```bash
git commit -m "docs: Boy Scout cleanup in docs/README.md

- Fix broken ADR link (path changed)
- Update last modified date
- Fix typo: recieve → receive

Pre-task cleanup before updating installation section"
```

---

### Example 3: Test File Addition

**Task:** Add test for new `validate_agent()` function

**Boy Scout Check:**
```bash
cd tests/unit/common/
# Find existing test_types.py has:
# - No Quad-A labels
# - Unclear test names
# - One commented-out test
```

**Boy Scout Fixes:**
```python
# Before
def test_status():
    status = TaskStatus.DONE
    assert status.is_terminal()
    
# def test_old_behavior():  # TODO: remove?
#     assert False

# After
def test_task_status_is_terminal_returns_true_for_done():
    """Test TaskStatus.is_terminal() recognizes DONE as terminal state."""
    # Arrange
    status = TaskStatus.DONE
    
    # Act
    result = status.is_terminal()
    
    # Assert
    assert result is True

# Commented-out test removed (created task to investigate if needed)
```

**Commit:**
```bash
git commit -m "test: Boy Scout cleanup in tests/unit/common/test_types.py

- Add Quad-A structure labels to existing tests
- Rename test functions for clarity (include expected behavior)
- Remove commented-out test (created TASK-2026-02-09-002 to investigate)

Pre-task cleanup before adding validate_agent() tests"
```

---

## Related Resources

- **Directive 020:** Locality of Change (scope boundaries)
- **Directive 017:** Test-Driven Development (when to apply)
- **Directive 026:** Commit Protocol (how to commit cleanups)
- **Python Conventions:** `doctrine/guidelines/python-conventions.md`
- **Version Control Hygiene:** `doctrine/guidelines/version-control-hygiene.md`

---

## Metadata

**Version:** 1.0.0  
**Status:** Active  
**Created:** 2026-02-09  
**Author:** Code-reviewer Cindy  
**Maintainers:** All development and documentation agents  
**Review Cycle:** Quarterly

---

## Appendix: Quick Reference Card

```
╔════════════════════════════════════════════════════════════╗
║            BOY SCOUT RULE - QUICK REFERENCE                ║
╠════════════════════════════════════════════════════════════╣
║ BEFORE starting ANY task:                                 ║
║                                                            ║
║ 1. SPOT CHECK (2-5 min)                                   ║
║    • Scan files you'll touch + neighbors                  ║
║    • Run linter/formatter                                 ║
║    • Look for: typos, stale docs, missing tests          ║
║                                                            ║
║ 2. FIX QUICK ISSUES (<5 min each)                        ║
║    • Format code                                          ║
║    • Remove unused imports                                ║
║    • Update stale docstrings                              ║
║    • Fix obvious typos                                    ║
║                                                            ║
║ 3. COMMIT SEPARATELY                                      ║
║    • Prefix: "chore: Boy Scout cleanup in <area>"        ║
║    • List specific fixes                                  ║
║    • Reference upcoming task                              ║
║                                                            ║
║ 4. PROCEED WITH TASK                                      ║
║    • Now on clean foundation                              ║
║    • Separate commit for feature work                     ║
║                                                            ║
║ REMEMBER:                                                  ║
║ • Fix only what you touch (locality)                      ║
║ • Don't change behavior (no refactoring)                  ║
║ • Large issues → create task, defer                       ║
║ • Cleanup commit ≠ feature commit                         ║
╚════════════════════════════════════════════════════════════╝
```
