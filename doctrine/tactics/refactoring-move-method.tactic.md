# Tactic: Refactoring.MoveMethod

**Related tactics:**
- `refactoring-extract-first-order-concept.tactic.md` — both improve class structure and responsibility alignment
- `refactoring-strangler-fig.tactic.md` — may use Move Method within new implementation for clean internal structure

**Complements:**
- [Directive 017 (Test Driven Development)](../directives/017_test_driven_development.md) — ensures safety during method relocation
- [Directive 021 (Locality of Change)](../directives/021_locality_of_change.md) — guides when and where to move methods

---

## Intent
Relocate a method from one class to another when the method uses more features (data or methods) of the target class than its current host.

Use this tactic to improve cohesion by placing behavior close to the data it operates on, reducing coupling and clarifying class responsibilities.

---

## Preconditions

**Required inputs:**
- Method exhibits "Feature Envy" code smell (more interested in another class than its own)
- Tests exist or can be added to verify current behavior
- Target class is an appropriate home for the method
- Method's responsibility naturally aligns with target class

**Assumed context:**
- Codebase supports incremental refactoring
- Tests can be run frequently to verify behavior preservation
- Target class is accessible and can be modified

**Exclusions (when NOT to use):**
- Method coordinates between multiple classes (use Extract Method first)
- Move would create circular dependencies
- Move would violate architectural layer boundaries
- Method is polymorphic and its location affects dispatch behavior
- No tests exist and cannot be created

---

## Execution Steps

1. **Examine references:** Count how many calls/field accesses the method makes to its current class versus the target class.
2. **Check polymorphism:** Verify the method is not overridden or location-dependent for dispatch.
3. **Verify tests:** Ensure tests exist that cover the method's behavior (add if missing).
4. **Copy method to target class:** Create the method in the target class without removing the original yet.
5. **Adjust method body:** Update parameter list and references (e.g., add parameter for old host if needed, adjust field access).
6. **Delegate from original:** Replace the original method body with a call to the new location.
7. **Run tests:** Verify behavior is preserved with delegation in place.
8. **Update callers incrementally:** Change call sites one by one to call the new location directly.
9. **Test after each update:** Run tests after each caller is updated.
10. **Remove old method:** Delete the delegating method once all callers are updated.
11. **Run comprehensive tests:** Execute full test suite to verify complete behavior preservation.
12. Stop.

---

## Checks / Exit Criteria
- All tests pass after each incremental step
- Method behavior is unchanged from external perspective
- Original method has been safely removed
- No callers depend on the old location
- Encapsulation is maintained or improved
- No circular dependencies introduced

---

## Failure Modes
- **Breaking encapsulation:** Moving exposes internal data that should remain private
- **Creating circular dependencies:** Target class now depends on original, creating coupling cycle
- **Moving too early:** Premature refactoring without clear evidence of Feature Envy
- **Batch moving without tests:** Changing multiple call sites simultaneously without intermediate verification
- **Ignoring inheritance:** Moving polymorphic methods breaks subclass behavior
- **Changing behavior during move:** Accidentally modifying logic instead of preserving it exactly
- **Insufficient testing:** Missing edge cases that break during relocation

---

## Outputs
- Method relocated to more appropriate class
- Updated call sites
- Passing test suite
- Improved class cohesion and responsibility alignment

---

## Notes on Use

**Feature Envy detection heuristics:**
- Method makes more calls to another class than its own
- Method uses more fields from another class
- Method name suggests it belongs elsewhere (e.g., `customer.getOrderDiscount()` → `order.getDiscount()`)
- Method requires extensive data passing from target class

**Information Expert principle (GRASP):** The object with the information should do the work. Move methods to where the data lives.

**Incremental approach:** Copy → Delegate → Update → Remove
- **Copy:** Create new method, verify compilation
- **Delegate:** Original calls new, verify tests
- **Update:** Change callers one by one, verify tests each time
- **Remove:** Delete old method only when safe

**Parameter adjustments:**
- If moved method needs access to original class, add it as a parameter
- If method uses many fields from target, consider moving those fields too
- Minimize parameter lists to maintain encapsulation

**Common scenarios:**
- **Customer/Order:** Move `getDiscount()` from Order to Customer (pricing is customer's responsibility)
- **Report/Formatter:** Move `formatAsCurrency()` from ReportController to CurrencyFormatter utility
- **Account/Transaction:** Move `calculateNewBalance()` from Transaction to Account (balance is account's concern)

**When to stop moving:**
- Method uses equal features from both classes (probably coordinating, not envious)
- No clear "information expert" exists (consider Extract Class to create one)
- Move would violate architectural boundaries (respect layer separation)

**Relationship to other refactorings:**
- Often follows **Extract Method** (extract first, then evaluate where it belongs)
- May precede **Extract Class** (moving multiple methods suggests new class needed)
- Complements **Replace Temp with Query** (methods become more moveable)

---
