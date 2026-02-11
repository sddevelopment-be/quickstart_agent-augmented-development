# Directive 039: Refactoring Techniques

**Status:** Active
**Applies To:** All development agents (Backend-Dev Benny, Frontend-Dev, Python Pedro, Java Jenny, etc.)
**Priority:** MEDIUM-HIGH - Recommended for code quality improvements
**Version:** 1.0.0
**Last Updated:** 2026-02-11

---

## Purpose

Standardize refactoring practices across all development agents to ensure:
- Safe, incremental improvements to code structure
- Behavior preservation during structural changes
- Clear decision-making about when and how to refactor
- Reduced technical debt accumulation
- Improved maintainability and readability

---

## The Golden Rule

> **Refactoring changes structure, not behavior. Always verify behavior is preserved.**

---

## Quick Reference: Refactoring Tactics

### 1. Move Method
**When:** Method exhibits "Feature Envy" (uses more features of another class than its own)
**Intent:** Relocate behavior closer to the data it operates on
**Safety:** Copy → Delegate → Update callers → Remove old method
**Details:** `doctrine/tactics/refactoring-move-method.tactic.md`

### 2. Strangler Fig
**When:** Large-scale refactoring that cannot be done safely in one step
**Intent:** Incrementally replace old implementation by building new alongside it
**Safety:** New implementation coexists → Gradual rerouting → Remove old when safe
**Details:** `doctrine/tactics/refactoring-strangler-fig.tactic.md`

### 3. Extract First-Order Concept
**When:** Logic is duplicated, implicit, or conceptually important but hidden
**Intent:** Make implicit patterns explicit by extracting named abstractions
**Safety:** Identify responsibility → Extract → Update callers → Verify tests
**Details:** `doctrine/tactics/refactoring-extract-first-order-concept.tactic.md`

---

## When to Apply Refactoring

### Code Smell Indicators

Refactor when you encounter these signals:

#### ✅ Strong Indicators (High Priority)
- **Duplicated logic** in 3+ locations (Rule of Three)
- **Feature Envy** - method uses more features of another class than its own
- **Long methods** (>20 lines) that do multiple things
- **Large classes** (>300 lines) with multiple responsibilities
- **Primitive obsession** - using primitives instead of domain objects
- **Data clumps** - same group of parameters passed together repeatedly
- **Dead code** - unused methods, classes, or variables
- **Shotgun surgery** - single change requires updates in many places

#### ⚠️ Moderate Indicators (Context-Dependent)
- **Long parameter lists** (>4 parameters)
- **Divergent change** - class changes for multiple reasons
- **Complex conditionals** that represent business rules
- **Comments explaining complex logic** (extract method with descriptive name instead)
- **Temporary fields** - instance variables used only in certain cases

#### 🔍 Weak Indicators (Investigate First)
- **Speculative generality** - "maybe we'll need this someday"
- **Middle man** - class that only delegates to another
- **Message chains** - `a.getB().getC().getD()`
- **Refused bequest** - subclass doesn't use inherited behavior

---

## Test-First Safety Protocol

### Before You Refactor

1. **Verify test coverage exists:**
   - Run tests to confirm current behavior is protected
   - If tests are missing, ADD THEM FIRST (see Directive 017)
   - Tests should pass before refactoring begins

2. **Confirm behavior preservation:**
   - Refactoring ONLY changes structure
   - If behavior changes, it's NOT refactoring - it's a feature change
   - Keep refactoring and feature changes in separate commits

3. **Check test quality:**
   ```bash
   # Run tests
   npm test  # or pytest, mvn test, etc.
   
   # Verify tests are meaningful
   # - Do they test behavior, not implementation?
   # - Would they catch accidental behavior changes?
   ```

### During Refactoring

1. **Work in small steps:**
   - Make one structural change at a time
   - Run tests after EACH step
   - Commit frequently (green-to-green)

2. **Follow the Red-Green-Refactor cycle:**
   ```
   ✅ GREEN: All tests pass
   ↓
   🔨 REFACTOR: Improve structure
   ↓
   ▶️ RUN TESTS: Verify behavior preserved
   ↓
   ✅ GREEN: All tests still pass
   ↓
   💾 COMMIT: Save safe state
   ```

3. **Stop if tests fail:**
   - Revert the change
   - Understand why tests failed
   - Make smaller incremental change

### After Refactoring

1. **Verify all tests pass:**
   ```bash
   # Run full test suite
   npm test -- --coverage
   
   # Ensure no regressions
   git diff --stat  # Review changes
   ```

2. **Check for side effects:**
   - Review performance implications
   - Verify no accidental API changes
   - Ensure encapsulation maintained

3. **Commit with clear message:**
   ```bash
   git add .
   git commit -m "refactor: extract UserValidator from UserService
   
   - Moved validation logic to dedicated class
   - Improves cohesion and testability
   - No behavior changes"
   ```

---

## Incremental Approach

### The Safety Pattern

**Never attempt big-bang refactoring.** Break down large structural changes into safe incremental steps.

#### ❌ DON'T DO THIS:
```
1. Rewrite entire module at once
2. Change multiple classes simultaneously
3. Mix refactoring with feature changes
4. Skip test verification between steps
5. Make structural changes without tests
```

#### ✅ DO THIS INSTEAD:
```
1. Identify ONE structural improvement
2. Verify tests protect current behavior
3. Make SMALL change (5-10 lines)
4. Run tests → should pass
5. Commit
6. Repeat steps 1-5
```

### Example: Safe Method Extraction

**Bad approach (risky):**
```java
// Extract 5 methods at once, change parameter lists, reorder calls
public void processOrder(Order order) {
    // All changed at once - high risk
}
```

**Good approach (incremental):**
```java
// Step 1: Extract one method, keep same behavior
public void processOrder(Order order) {
    validateOrder(order);  // ← Extracted, test passes
    calculateTotal(order);
    applyDiscount(order);
    chargePayment(order);
}

// Step 2: Extract second method (new commit)
// Step 3: Extract third method (new commit)
// etc.
```

---

## Decision Framework

### When to Refactor NOW

Refactor immediately if:
- ✅ You're already touching the code for another reason (Boy Scout Rule - see Directive 036)
- ✅ Code smell is HIGH severity (duplicated critical logic, security issue)
- ✅ Refactoring takes <15 minutes and has low risk
- ✅ You have complete test coverage for the area
- ✅ Refactoring unblocks current work

### When to Defer Refactoring

Consider deferring if:
- ⚠️ Tests don't exist and would take >1 hour to write
- ⚠️ Code is in rarely-changed legacy area (low ROI)
- ⚠️ Refactoring requires >2 hours (create separate task)
- ⚠️ You're in the middle of urgent bug fix
- ⚠️ Area is scheduled for replacement/removal soon

**When deferring:** Create technical debt ticket with:
- Specific code smell identified
- Estimated effort to address
- Business impact of NOT addressing
- Suggested approach

### When NOT to Refactor

Don't refactor if:
- ❌ No clear improvement identified (avoid "just because" refactoring)
- ❌ Code works and meets requirements (no smell detected)
- ❌ Speculative ("we might need this flexibility someday")
- ❌ Personal style preference without objective benefit
- ❌ Tests cannot be written or are impractical

---

## Refactoring Anti-Patterns

### Mistake 1: Refactoring Without Tests

**Problem:** No safety net to verify behavior preservation.

**Solution:** 
```yaml
1. Stop refactoring
2. Write tests first (see Directive 017)
3. Verify tests pass
4. THEN refactor with confidence
```

---

### Mistake 2: Mixing Refactoring with Feature Changes

**Problem:** Impossible to determine if behavior change was intentional.

**Solution:**
```bash
# Wrong: Mixed commit
git commit -m "Add discount logic and refactor validator"

# Right: Separate commits
git commit -m "refactor: extract DiscountValidator"
git commit -m "feat: add seasonal discount logic"
```

**Rule:** One commit should do ONE thing - either refactor OR change behavior, never both.

---

### Mistake 3: Over-Engineering

**Problem:** Creating abstractions that add complexity without clear benefit.

**Solution:**
- Follow **Rule of Three** - don't extract until pattern appears 3 times
- Ask: "Does this abstraction make the code easier to understand?"
- Avoid speculative generality ("we might need this flexibility")
- **YAGNI principle:** You Aren't Gonna Need It

---

### Mistake 4: Breaking Encapsulation

**Problem:** Moving method exposes internal data or creates circular dependencies.

**Solution:**
```java
// Bad: Breaks encapsulation
order.getCustomer().setInternalState()  // Customer internals exposed

// Good: Tell, don't ask
order.applyCustomerDiscount()  // Encapsulation maintained
```

---

### Mistake 5: Big-Bang Refactoring

**Problem:** Large structural changes fail because they're too risky.

**Solution:**
- Use **Strangler Fig pattern** for large refactorings
- Break down into 15-minute incremental steps
- Commit after each safe state
- Always maintain working code (trunk-based development)

---

## Collaboration Pattern

When planning refactoring work:

```yaml
# ${WORKSPACE_ROOT}/work/refactoring-task.yaml
task_id: "refactor-[description]"
assigned_to: "[agent-name]"
technique: "move-method"  # or strangler-fig, extract-concept

safety_checks:
  - test_coverage: "verified"
  - behavior_risk: "low"
  - estimated_time: "30 minutes"
  
steps:
  - phase: "verify_tests"
    status: "complete"
    output: "87% coverage, all tests pass"
  
  - phase: "refactor_step_1"
    status: "complete"
    output: "Extracted validateInput method, tests pass"
    commit: "abc123"
  
  - phase: "refactor_step_2"
    status: "in_progress"
    output: "Moving method to appropriate class"
```

---

## Code Review Checklist

Refactoring pull requests SHOULD include:

- [ ] All tests pass before and after refactoring
- [ ] No behavior changes (confirmed by passing tests)
- [ ] Incremental commits showing safe progression
- [ ] Clear commit messages explaining structural changes
- [ ] No mixed refactoring/feature commits
- [ ] Code smells addressed (documented in PR description)
- [ ] Encapsulation maintained or improved
- [ ] No new dependencies introduced unnecessarily

**Note:** Large refactorings should use Strangler Fig pattern with multiple PRs.

---

## Success Criteria

You've successfully refactored when:

- ✅ All tests pass (behavior preserved)
- ✅ Code structure is measurably improved (less duplication, better cohesion)
- ✅ Code smell has been eliminated or reduced
- ✅ Changes are committed incrementally with clear messages
- ✅ No accidental behavior changes introduced
- ✅ Future changes will be easier in the affected area
- ✅ Team understands the structural improvement

---

## Relationship to Other Directives

### Must Follow Simultaneously

- **Directive 017 (TDD):** Tests verify behavior preservation during refactoring
- **Directive 021 (Locality of Change):** Guides where to make structural improvements
- **Directive 036 (Boy Scout Rule):** Opportunistic refactoring when touching code

### Related Guidance

- **Directive 016 (ATDD):** Integration tests provide safety net for larger refactorings
- **Directive 018 (Traceable Decisions):** Document significant architectural refactorings
- **Directive 020 (Lenient Adherence):** Balance refactoring perfectionism with pragmatism
- **Directive 028 (Bug Fixing):** Use test-first approach when refactoring reveals bugs

---

## Additional Resources

### Tactics Documentation

- `tactics/refactoring-move-method.tactic.md` - Relocate methods to appropriate classes
- `tactics/refactoring-strangler-fig.tactic.md` - Incremental replacement pattern
- `tactics/refactoring-extract-first-order-concept.tactic.md` - Make implicit concepts explicit

### External References

- **Martin Fowler's Refactoring Catalog:** [refactoring.com/catalog](https://refactoring.com/catalog)
- **Book:** "Refactoring: Improving the Design of Existing Code" by Martin Fowler
- **Book:** "Working Effectively with Legacy Code" by Michael Feathers

---

## Quick Decision Tree

```
                 Is code hard to work with?
                        ↓
                    YES → Identify code smell
                        ↓
              Do tests cover this area?
                    ↓         ↓
                  YES        NO → Write tests first (D017)
                    ↓
          Is refactoring <15 minutes?
                ↓         ↓
              YES        NO → Create separate task
                ↓
         Will it unblock current work?
                ↓         ↓
              YES        NO → Apply Boy Scout Rule (D036)
                ↓
           Refactor incrementally
                ↓
          Test after each step
                ↓
            Commit green-to-green
```

---

## Summary

**The Four Principles:**

1. **Behavior Preservation:** Refactoring changes structure, not behavior. Tests prove this.
2. **Incremental Safety:** Small steps, frequent testing, regular commits.
3. **Test-First Protection:** Never refactor without test coverage.
4. **Clear Intent:** One commit does one thing - refactor OR change behavior, not both.

**Remember:**

> "Make the change easy (refactor), then make the easy change (feature)."
> 
> — Kent Beck

**When in doubt:**
- Is there a code smell? → Choose appropriate technique
- Do tests exist? → If no, write them first
- Is change <15 min? → Do it now
- Is change risky? → Break into smaller steps or use Strangler Fig

---

**Status:** Active and recommended for all development agents
**Effective:** Immediately
**Review:** Quarterly or after significant refactoring lessons learned
