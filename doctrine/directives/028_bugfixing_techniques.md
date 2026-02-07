# Directive 028: Bug Fixing Techniques

**Status:** Active
**Applies To:** All development agents (Backend-Dev Benny, Frontend-Dev, Database Danny, etc.)
**Priority:** HIGH - Recommended for all bug-fixing tasks
**Version:** 1.0.0
**Last Updated:** 2026-02-06

---

## Purpose

Standardize bug-fixing approach across all development agents to ensure:
- Systematic problem reproduction
- Verifiable fixes
- Regression prevention
- Efficient debugging (no wasted time on trial-and-error)

---

## The Golden Rule

> **Before you change production code, write a test that fails because of the bug.**

---

## Quick Reference: Test-First Bug Fixing

### Phase 1: Write a Failing Test (DO THIS FIRST)

#### ❌ DO NOT:
- Run the full application
- Create side-scripts to investigate
- Make changes to production code
- Deploy and test manually
- Guess and check

#### ✅ DO THIS:

1. **Choose test level:**
   - Unit test (isolated component)
   - Integration test (component interaction)
   - Acceptance test (end-to-end behavior)

2. **Write test that reproduces the bug:**
   ```java
   @Test
   @DisplayName("Bug: [describe what's wrong]")
   void reproduceBug() {
       // Arrange: Set up scenario that triggers bug
       var input = createBugTriggeringInput();

       // Act: Execute the failing code
       var result = systemUnderTest.process(input);

       // Assert: What SHOULD happen (test will fail)
       assertThat(result).isEqualTo(expectedCorrectBehavior);
   }
   ```

3. **Run the test - MUST FAIL**
   - If it passes, your test doesn't reproduce the bug

4. **Verify it fails for the RIGHT reason:**
   - Change assertion to expect WRONG behavior
   - Test should now PASS
   - Revert assertion back to correct behavior

5. **Commit your test:**
   ```bash
   git add src/test/java/.../ReproductionTest.java
   git commit -m "WIP: Test reproducing bug - [description]"
   ```

---

### Phase 2: Fix the Code

1. **Use test to guide debugging**
2. **Make minimal change** to pass the test
3. **Run the test** - should now PASS
4. **Run ALL tests** - ensure no regressions

---

### Phase 3: Verify and Ship

1. **Manual verification** (if applicable)
2. **Review changes** for minimalism and focus
3. **Commit test and fix together:**
   ```bash
   git add src/main/java/.../FixedClass.java
   git add src/test/java/.../ReproductionTest.java
   git commit -m "Fix: [bug description] - [explanation]"
   ```

---

## Success Criteria

You're done when:

- ✅ Failing test existed that proved the bug
- ✅ Production code changed to fix bug
- ✅ Previously failing test now passes
- ✅ All other tests still pass
- ✅ Test and fix committed together

---

## Common Mistakes and Solutions

### Mistake 1: "I'll just quickly fix it first"

**Problem:** No proof the bug existed or that you fixed it.

**Solution:** Discipline. Test first, every single time.

---

### Mistake 2: Test passes immediately

**Problem:** Your test doesn't reproduce the bug.

**Solution:** Re-examine test setup. Are you using correct data? Testing right component?

---

### Mistake 3: Running full application to investigate

**Problem:** Slow feedback loop, hard to isolate issue, no regression prevention.

**Solution:** Write a focused test instead. It's faster and creates permanent value.

---

### Mistake 4: Creating side-scripts

**Problem:** Scripts become throwaway code, no permanent regression test.

**Solution:** Convert investigation logic into a proper test. Same effort, permanent benefit.

---

## Time Investment Comparison

**Real-world example:**

| Approach | Time Spent | Outcome |
|----------|-----------|---------|
| **Running full app + side-scripts** | Hours | Still broken, confused |
| **Test-first (proper guidance)** | 45 minutes | Bug fixed, test prevents recurrence |

**"But writing tests is slower!"**

No. It feels slower initially, but it's faster in total:
- No wasted deployment cycles
- No manual testing repetition
- No regression later
- No re-fixing the same bug

---

## When to Apply This Directive

### Always Use Test-First For:

- ✅ Production bugs with clear reproduction steps
- ✅ Failures discovered during testing
- ✅ Mysterious behavior that needs investigation
- ✅ Integration issues between components
- ✅ Edge cases not covered by existing tests
- ✅ Any defect that can be reproduced programmatically

### Other Techniques For:

- ⚠️ UI/UX issues (use visual inspection)
- ⚠️ Performance problems (use profiling/benchmarking)
- ⚠️ Configuration errors (use configuration validation)
- ⚠️ Infrastructure failures (use monitoring/alerting)

---

## Agent Collaboration Pattern

When working on a bug fix task:

```yaml
# ${WORKSPACE_ROOT}/collaboration/inbox/YYYY-MM-DD-bug-fix-task.yaml
task_id: "bug-fix-[description]"
assigned_to: "[agent-name]"
approach: "test-first-bug-fixing"  # ← RECOMMENDED

steps:
  - phase: "understand"
    status: "complete"
    output: "Hypothesis: [what you think is wrong]"

  - phase: "write_test"
    status: "complete"
    output: "[TestClass.java] created, test fails as expected"

  - phase: "fix"
    status: "in_progress"
    output: "Implementing fix in [ProductionClass.java]"

  - phase: "verify"
    status: "pending"
```

---

## Code Review Checklist

Bug fixes SHOULD include:

- [ ] Test that reproduces the bug
- [ ] Test failed before fix
- [ ] Test passes after fix
- [ ] All other tests still pass
- [ ] Test and fix committed together

**Note:** If test is not feasible, document why in commit message or work log.

---

## Red Flags

Watch for these anti-patterns:

❌ **"Let me just quickly fix it..."**
✅ **"Let me first write a test that reproduces the issue..."**

❌ **"I'll run the full app to see what's wrong..."**
✅ **"I'll write a focused test to isolate the problem..."**

❌ **"Let me create a side-script to investigate..."**
✅ **"Let me write a test that proves the bug exists..."**

---

## Additional Resources

### Full Documentation

- **Detailed Approach:** `.github/agents/approaches/test-first-bug-fixing.md`
- **Checklist:** `.github/agents/approaches/bug-fixing-checklist.md`

### External References

- **LinkedIn Article:** [Example of test-first bug-fixing in JavaScript](https://www.linkedin.com/pulse/example-test-first-bug-fixing-javascript-stijn-dejongh/)
- **Software Design Nuggets:** [5 Practical Tips for Aspiring Architects](https://www.linkedin.com/pulse/software-design-nuggets-5-practical-tips-aspiring-stijn-dejongh-sjw9e/)

### Related Directives

- **Directive 016:** Acceptance Test Driven Development (ATDD)
- **Directive 017:** Test Driven Development (TDD)

---

## Summary

**The Five-Step Pattern:**

1. **Understand:** Read bug report, gather context, formulate hypothesis
2. **Reproduce:** Write failing test, verify it fails for the right reason
3. **Fix:** Make minimal change to pass the test
4. **Validate:** Run all tests, ensure no regressions
5. **Ship:** Commit test + fix together

**Remember:**

> "If I deploy this fix, how do I KNOW it works?"
>
> If the answer is "I ran it manually and it looked okay," you might be missing an opportunity for regression prevention.

---

**Status:** Recommended for all development agents
**Effective:** Immediately
**Review:** Quarterly or after significant learning moments
