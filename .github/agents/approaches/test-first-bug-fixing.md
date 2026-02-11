# Approach: Test-First Bug Fixing

**Type:** Problem-Solving Technique
**Context:** Debugging production issues, fixing defects, investigating failures
**When to Use:** When a bug is reported or discovered, before attempting to fix the code
**Author:** Stijn Dejongh
**Status:** Proven - Field-tested in production environments
**Last Updated:** 2026-02-06

---

## Overview

**Test-First Bug Fixing** is a disciplined approach to resolving software defects by writing a failing test that reproduces the issue **before** modifying any production code. This technique transforms bug fixing from an ad-hoc, trial-and-error process into a systematic, verifiable procedure.

**Core Principle:**

> "Before you fix the bug, write a test that fails because of the bug. Fix the code. The test passes. You're done."

---

## Why This Works

### Traditional Bug-Fixing Approach (Anti-Pattern)

```
1. Read bug report
2. Guess where the problem is
3. Make changes to production code
4. Deploy and test manually
5. Bug still there? Go to step 2
6. Eventually it works (you think)
7. Hope you didn't break anything else
```

**Problems:**
- ❌ No proof the bug is fixed
- ❌ No proof you didn't break something else
- ❌ Wastes time on deployments/restarts
- ❌ Can't easily reproduce the issue later
- ❌ Other developers might re-introduce the bug

### Test-First Bug-Fixing Approach (Recommended)

```
1. Read bug report
2. Write a failing test that reproduces the bug
3. Verify the test fails for the RIGHT reason
4. Fix the production code
5. Test passes
6. Run all tests to ensure nothing else broke
7. Commit both test and fix
```

**Benefits:**
- ✅ Proof the bug existed
- ✅ Proof the bug is fixed
- ✅ Proof you didn't break anything else
- ✅ Fast feedback loop (no deployment needed)
- ✅ Regression prevention (bug can't come back unnoticed)
- ✅ Documentation of the issue

---

## When to Use This Approach

### Ideal Scenarios ✅

- Production bugs with clear reproduction steps
- Failures discovered during testing
- Mysterious behavior that needs investigation
- Integration issues between components
- Edge cases not covered by existing tests
- Any defect that can be reproduced programmatically

### Less Suitable Scenarios ⚠️

- UI/UX issues requiring visual inspection
- Performance problems (use profiling/benchmarking instead)
- Configuration errors (use configuration validation)
- Infrastructure failures (use monitoring/alerting)
- Security vulnerabilities (use security testing tools)

**Rule of Thumb:** If you can write a test that demonstrates the problem, use test-first bug fixing.

---

## Step-by-Step Process

### Phase 1: Understand the Bug (5-10 minutes)

1. **Read the bug report carefully**
   - What is the expected behavior?
   - What is the actual behavior?
   - What are the reproduction steps?
   - What data/context triggers the issue?

2. **Gather additional information**
   - Review error logs
   - Check related code areas
   - Identify affected components
   - Look for similar issues in git history

3. **Formulate a hypothesis**
   - What do you think is wrong?
   - Where is the problem likely located?
   - What assumptions might be incorrect?

**Output:** Clear understanding of what should happen vs what actually happens.

---

### Phase 2: Write the Failing Test (10-20 minutes)

1. **Choose the right test level**
   - Unit test: Isolated component issue
   - Integration test: Component interaction issue
   - Acceptance test: End-to-end behavior issue

2. **Write a test that reproduces the bug**
   ```java
   @Test
   @DisplayName("Bug description - should do X but does Y")
   void testBugReproduction() {
       // Arrange: Set up the scenario that triggers the bug
       var input = createBugTriggeringInput();

       // Act: Execute the code that fails
       var result = systemUnderTest.process(input);

       // Assert: Verify the CORRECT behavior (test will fail)
       assertThat(result).isEqualTo(expectedCorrectBehavior);
   }
   ```

3. **Run the test - it MUST fail**
   - If it passes, your test doesn't reproduce the bug
   - Verify the failure message matches the reported issue

4. **Verify the test fails for the RIGHT reason**
   - Temporarily change the assertion to expect the WRONG behavior
   - Test should now pass
   - This confirms your test accurately reproduces the issue
   - Revert the assertion back to correct behavior

**Output:** A failing test that proves the bug exists.

**Critical:** Do NOT proceed to fixing until you have a failing test.

---

### Phase 3: Fix the Bug (Variable time)

1. **Use the test to guide debugging**
   - Run test in debug mode
   - Step through the execution
   - Identify where behavior diverges from expectation

2. **Make the minimal change to fix the issue**
   - Resist the urge to refactor (do that later)
   - Focus on making the test pass
   - Keep changes localized

3. **Run the test - it should now pass**
   - Green test = bug fixed
   - Still red? Continue investigating

4. **Run ALL tests to ensure no regressions**
   - Full test suite must pass
   - If something else breaks, fix it or reconsider your approach

**Output:** Passing test + fixed production code.

---

### Phase 4: Verify and Clean Up (5-10 minutes)

1. **Test against the actual system (if applicable)**
   - Deploy to test environment
   - Manually verify the fix
   - "Better safe than sorry"

2. **Review your changes**
   - Is the fix minimal and focused?
   - Are there similar issues elsewhere?
   - Should you add more tests for related scenarios?

3. **Document the fix (if needed)**
   - Update ADRs if architectural assumptions changed
   - Add comments if the fix is non-obvious
   - Update bug report with resolution details

4. **Commit test and fix together**
   ```bash
   git add src/main/java/BuggyClass.java
   git add src/test/java/BuggyClassTest.java
   git commit -m "Fix: Description of bug - explain what was wrong and how you fixed it"
   ```

**Output:** Committed fix with regression test.

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: "I'll just quickly fix it first"

**Problem:** You make changes without a test, think it's fixed, but can't prove it.

**Solution:** Discipline. Write the test first, every time. It's faster in the long run.

**Quote from original article:**
> "Even though this approach might feel slower than just hacking away at the live code base and redeploying it a few times to see if you solved the issue, it usually ends up being faster."

---

### Pitfall 2: Test passes immediately

**Problem:** You wrote a test expecting it to fail, but it passes. Your test doesn't reproduce the bug.

**Solution:** Re-examine your test setup. Are you using the correct data? Are you testing the right component? Review the bug report again.

---

### Pitfall 3: Test fails for the WRONG reason

**Problem:** Test fails, but not because of the bug you're trying to fix.

**Solution:** Temporarily change the assertion to expect the WRONG behavior. If the test passes, your test is correct. If it still fails, your test setup is wrong.

**From original article:**
> "Now, to make sure our test is working correctly, we will quickly change the test to make it expect the incorrect value. [...] Yes, I am in fact testing my test. Yes, this sounds silly. And yes, failing to do this has cost me countless hours of chasing ghost bugs in the past."

---

### Pitfall 4: Test is too broad

**Problem:** Test covers too much ground, making it hard to pinpoint the issue.

**Solution:** Start with a focused unit test. Only escalate to integration/acceptance tests if the issue is truly cross-component.

---

### Pitfall 5: Can't reproduce the bug in a test

**Problem:** The bug only happens in production, can't be reproduced locally.

**Solution:**
- Extract production data for test fixtures
- Replicate production configuration
- Use property-based testing to explore edge cases
- If all else fails, add extensive logging and monitor in production

---

## Integration with Agent Workflows

### For Agents Debugging Issues

When a bug is reported or test fails:

1. **STOP** - Do not run the full application
2. **STOP** - Do not create side-scripts to investigate
3. **START** - Write a failing test that reproduces the issue
4. **VERIFY** - Run the test, ensure it fails for the right reason
5. **FIX** - Make the minimal change to pass the test
6. **VALIDATE** - Run all tests, ensure nothing broke
7. **COMMIT** - Test and fix together

### Agent Collaboration Pattern

```yaml
# ${WORKSPACE_ROOT}/collaboration/inbox/2026-XX-XX-bug-fix-task.yaml
task_id: "bug-fix-[description]"
assigned_to: "backend-benny"
priority: "high"
status: "in_progress"

approach: "test-first-bug-fixing"

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

## Comparison with Other Approaches

| Approach | Time to First Attempt | Confidence in Fix | Regression Prevention | Learning Value |
|----------|----------------------|-------------------|----------------------|----------------|
| **Test-First** | Moderate (write test first) | High (test proves it) | High (test prevents recurrence) | High (test documents issue) |
| **Trial-and-Error** | Fast (dive right in) | Low (hope it works) | None (no test) | Low (fix is magic) |
| **Side-Scripts** | Slow (build tooling) | Medium (manual verification) | Low (scripts rot) | Medium (tooling reusable) |
| **Full App Runs** | Very slow (deploy/restart) | Low (hard to isolate) | None (no test) | Low (wastes time) |

---

## Success Metrics

### How to Know This Approach Is Working

- ✅ Time from bug report to fix decreases over time
- ✅ Fewer "fixed" bugs that come back
- ✅ Higher confidence in deployments
- ✅ Test suite grows to cover real-world scenarios
- ✅ Team spends less time in firefighting mode

### Red Flags That You're Not Doing It Right

- ❌ Tests are written AFTER the fix
- ❌ Tests pass immediately (don't reproduce the bug)
- ❌ Fixes are deployed without tests
- ❌ Same bug comes back weeks later
- ❌ Team says "tests slow us down"

---

## Related Practices

### Complementary Approaches

- **TDD (Test-Driven Development):** Write tests before writing ANY code (broader than bug fixing)
- **Approval Testing:** Capture current behavior, then refactor safely
- **Snapshot Testing:** Validate complex output structures
- **Property-Based Testing:** Generate test cases to find edge cases

### When to Combine

- **Test-First + Production Data:** Extract fixtures from production to write realistic tests
- **Test-First + Debugging:** Use test to drive debugger session
- **Test-First + Refactoring:** Write characterization tests before refactoring

---

## References

### Original Articles

- **LinkedIn:** ["Example of test-first bug-fixing in JavaScript"](https://www.linkedin.com/pulse/example-test-first-bug-fixing-javascript-stijn-dejongh/) by Stijn Dejongh (2022)
- **LinkedIn:** ["Software Design Nuggets: 5 Practical Tips for Aspiring Architects"](https://www.linkedin.com/pulse/software-design-nuggets-5-practical-tips-aspiring-stijn-dejongh-sjw9e/) by Stijn Dejongh (2025)

### External Resources

- Kent Beck's Test Desiderata: [https://kentbeck.github.io/TestDesiderata/](https://kentbeck.github.io/TestDesiderata/)
- Approval Testing: [https://approvaltests.com/](https://approvaltests.com/)
- Snapshot Testing (Jest): [https://jestjs.io/docs/snapshot-testing](https://jestjs.io/docs/snapshot-testing)

---

## Quick Reference Card

### The Golden Rule

> **Before you change production code, write a test that fails because of the bug.**

### The Five-Step Pattern

1. **Understand:** Read bug report, gather context, formulate hypothesis
2. **Reproduce:** Write failing test, verify it fails for the right reason
3. **Fix:** Make minimal change to pass the test
4. **Validate:** Run all tests, ensure no regressions
5. **Ship:** Commit test + fix together

### Remember

- ✅ Test first, fix second
- ✅ Make the test fail before fixing
- ✅ Verify test fails for the RIGHT reason
- ✅ Keep the fix minimal
- ✅ Run ALL tests before committing
- ✅ Commit test and fix together

### When in Doubt

Ask yourself: "If I deploy this fix, how do I KNOW it works?"

If the answer is "I ran it manually and it looked okay," you're doing it wrong.

---

**Tags:** `#bug-fixing` `#test-first` `#tdd` `#debugging` `#regression-prevention`
**Related:** Directive 028 (Bug Fixing Techniques), Directive 017 (TDD), Directive 016 (ATDD)
