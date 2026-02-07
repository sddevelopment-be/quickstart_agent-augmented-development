# Bug Fixing Checklist - Agent Quick Reference

**Approach Type:** Problem-Solving Technique
**Status:** Active
**Last Updated:** 2026-02-06

**When a bug is reported or test fails, follow this checklist.**

---

## STOP First! ✋

Before you do ANYTHING, answer these questions:

- [ ] Have I read the bug report completely?
- [ ] Do I understand what SHOULD happen vs what ACTUALLY happens?
- [ ] Can I reproduce this issue in a test?

If you answered "yes" to all three, proceed to Phase 1.

If you answered "no" to any, gather more information first.

---

## Phase 1: Write a Failing Test (DO THIS FIRST)

### ❌ DO NOT:
- Run the full application
- Create side-scripts to investigate
- Make changes to production code
- Deploy and test manually
- Guess and check

### ✅ DO THIS:

1. **Choose test level:**
   ```
   [ ] Unit test (isolated component)
   [ ] Integration test (component interaction)
   [ ] Acceptance test (end-to-end behavior)
   ```

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

3. **Run the test - MUST FAIL:**
   ```
   [ ] Test fails ✅ (Good! Continue to step 4)
   [ ] Test passes ❌ (Bad! Your test doesn't reproduce the bug - try again)
   ```

4. **Verify it fails for the RIGHT reason:**
   - Change assertion to expect WRONG behavior
   - Test should now PASS
   - This confirms test accurately reproduces bug
   - **Revert assertion** back to correct behavior

5. **Save your work:**
   ```bash
   git add src/test/java/.../YourTest.java
   git commit -m "WIP: Test reproducing bug - [description]"
   ```

---

## Phase 2: Fix the Code

### Now you can fix it:

1. **Use test to guide debugging:**
   ```
   [ ] Run test in debug mode
   [ ] Step through execution
   [ ] Identify where behavior diverges
   ```

2. **Make minimal change:**
   ```
   [ ] Focus on making test pass
   [ ] Resist urge to refactor (do that later)
   [ ] Keep changes localized
   ```

3. **Run the test - should now PASS:**
   ```
   [ ] Test passes ✅ (Good! Continue to step 4)
   [ ] Test still fails ❌ (Continue investigating)
   ```

4. **Run ALL tests:**
   ```bash
   mvn test  # or appropriate test command
   ```
   ```
   [ ] All tests pass ✅ (Good! Continue to Phase 3)
   [ ] Some tests fail ❌ (Fix them or reconsider your approach)
   ```

---

## Phase 3: Verify and Ship

1. **Manual verification (if applicable):**
   ```
   [ ] Tested against actual system
   [ ] Bug is fixed in real environment
   [ ] No side effects observed
   ```

2. **Review your changes:**
   ```
   [ ] Fix is minimal and focused
   [ ] No similar issues elsewhere
   [ ] Related scenarios covered by tests
   ```

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
- ✅ Bug report updated with resolution

---

## Common Mistakes

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
| **Test-first (after guidance)** | 45 minutes | Bug fixed, test prevents recurrence |

**"But writing tests is slower!"**

No. It feels slower initially, but it's faster in total:
- No wasted deployment cycles
- No manual testing repetition
- No regression later
- No re-fixing the same bug

---

## The Golden Rule

> **Before you change production code, write a test that fails because of the bug.**

**When in doubt, ask:**

> "If I deploy this fix, how do I KNOW it works?"

If the answer is "I ran it manually," you're doing it wrong.

---

## Full Documentation

For complete guide, see: `approaches/test-first-bug-fixing.md`

For original technique, see: [LinkedIn Article](https://www.linkedin.com/pulse/example-test-first-bug-fixing-javascript-stijn-dejongh/)

---

**Status:** Recommended for all bug-fixing tasks
**Related:** Directive 028 (Bug Fixing Techniques), Directive 017 (TDD)
