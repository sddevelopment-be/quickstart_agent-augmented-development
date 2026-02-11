# Refactoring Patterns Research Summary
**Quick Reference Guide for Tactic Creation**

---

## 1. Move Method Refactoring

### Description (2-3 sentences)
Move Method is a code-level refactoring that relocates a method from one class to another when the method uses more features (data or methods) of the target class than its current host. This improves cohesion by placing behavior close to the data it operates on, reducing coupling and clarifying class responsibilities. The pattern follows a safe, incremental approach: copy → delegate → update callers → remove old method.

### Key Principles
- **Feature Envy:** Method is more interested in another class than its own
- **Information Expert (GRASP):** Object with information should do the work
- **Single Responsibility:** Each class has one reason to change
- **Law of Demeter:** Minimize coupling chains
- **Test-Driven Safety:** Verify behavior before and after move

### When to Use (Preconditions)
✅ **Use when:**
- Method makes more calls to another class than its own
- Method uses more fields from another class
- Tests exist or can be added
- Target class is appropriate home

❌ **Do NOT use when:**
- Method coordinates between multiple classes (use Extract Method first)
- Would create circular dependencies
- Would violate architectural layers
- Method is polymorphic and location-dependent

### Execution Steps (Simplified)
1. Examine and count references
2. Check for polymorphism
3. Verify/add tests
4. **Copy** method to target class
5. Adjust method body (parameters, references)
6. **Delegate** from original to new location
7. Update callers one by one
8. Test after each update
9. **Remove** old method
10. Final comprehensive tests

### Common Failure Modes
- Breaking encapsulation (exposing internal data)
- Creating circular dependencies
- Moving too early (premature refactoring)
- Batch moving without tests
- Ignoring inheritance hierarchies
- Changing behavior during move

### Example Scenarios
- **Customer/Order:** Move getDiscount() from Order to Customer (pricing is customer's responsibility)
- **Report/Formatter:** Move formatAsCurrency() from ReportController to CurrencyFormatter utility
- **Account/Transaction:** Move calculateNewBalance() from Transaction to Account (balance is account's concern)

---

## 2. Strangler Fig Pattern

### Description (2-3 sentences)
Strangler Fig is an architectural migration strategy where a new system gradually replaces an old system by implementing new functionality alongside legacy code and incrementally routing traffic to the new implementation. Named after the strangler fig vine that grows around and eventually replaces a host tree, this pattern enables safe, reversible, low-risk system evolution without a "big bang" rewrite. A routing layer (facade, proxy, API gateway) controls which implementation handles each request, allowing gradual traffic shifting with instant rollback capability.

### Key Principles
- **Incremental Replacement:** Replace piece by piece, not all at once
- **Coexistence:** Old and new run simultaneously during migration
- **Reversibility:** Each step can be rolled back (feature flags, routing)
- **Verification at Each Step:** Tests and monitoring confirm equivalence
- **Routing Layer:** Facade/proxy directs traffic (canary, percentage-based)
- **Eventual Complete Replacement:** Old code deleted only after full migration
- **Business Continuity:** System stays operational throughout

### When to Use (Preconditions)
✅ **Use when:**
- Large-scale refactoring cannot be done safely in one step
- Legacy system must stay operational (zero-downtime requirement)
- Incremental deployment capability exists (CI/CD, feature flags)
- Can introduce routing layer (architectural seams exist/can be created)
- Tests exist or can be created
- Team has capacity for temporary duplication
- Migration timeline is weeks/months (sustained effort)
- Organizational commitment to complete migration

❌ **Do NOT use when:**
- Simple single-step refactoring is possible
- Architecture prevents coexistence (no seams, tight coupling)
- Tests cannot be created
- Temporary duplication creates unacceptable burden
- Old system can be shut down for complete replacement
- Change scope is small and low-risk
- Team lacks discipline to finish (risk of permanent duplication)

### Execution Steps (Simplified)
1. Identify subsystem to replace
2. Create/verify comprehensive tests
3. **Introduce routing layer** (initially 100% to old)
4. Select first slice (small, low-risk, high-value)
5. **Implement new version** alongside old
6. Verify equivalence (tests, parallel runs, shadow mode)
7. **Route small percentage** to new (1-5% canary)
8. **Monitor and measure** (errors, performance, behavior)
9. **Gradually increase traffic** (10%, 25%, 50%, 75%, 100%)
10. **Iterate** for each slice (repeat 4-9)
11. Remove routing to old for completed slices
12. **Delete old code** when fully replaced
13. Simplify/remove routing layer
14. Final comprehensive tests

### Common Failure Modes
- Forgetting to test first (silent breakage)
- Big slices (not incremental enough)
- Divergent implementations (old and new evolve differently)
- Premature removal (delete before routing complete)
- No rollback plan
- Monitoring gaps (flying blind)
- Mixing concerns (refactoring + new features)
- Routing complexity explosion (technical debt)
- Incomplete migration (abandonment)
- Testing only new code (equivalence not verified)

### Example Scenarios
- **Payment Gateway Migration:** Replace legacy payment provider with modern one (Stripe/Adyen), route 1% → 100% over 6 weeks
- **Microservice Extraction:** Extract UserService from monolith, API gateway routes incrementally, 4 months
- **Reporting System Replacement:** Migrate 200 reports from custom engine to Tableau, prioritize top 20 (80/20 rule), 6 months
- **Framework Migration:** Vue 2 → Vue 3 using @vue/compat, bottom-up component migration, 8 months

---

## 3. Comparison

| Dimension | Move Method | Strangler Fig |
|-----------|-------------|---------------|
| **Scale** | Code (method/class) | System (subsystem/service) |
| **Duration** | Minutes to hours | Weeks to months |
| **Risk** | Low | High |
| **Coordination** | Individual developer | Team/multiple teams |
| **Testing** | Unit tests | Integration, E2E, monitoring |
| **Coexistence** | Brief delegation | Extended parallel operation |
| **Motivation** | Improve class design | Replace legacy systems |

**Combined Usage:** Strangler Fig at architectural level may use Move Method within new implementation for clean internal structure.

---

## 4. Doctrine Integration

### Related Directives
- **Directive 017 (Test Driven Development):** Both patterns require tests for safety

### Related Tactics
- **refactoring-extract-first-order-concept.tactic.md:** Related to Move Method (both improve structure)
- **refactoring-strangler-fig.tactic.md:** Already exists (review for consistency)
- **safe-to-fail-experiment-design.tactic.md:** Supports Strangler Fig validation steps

### Key Principles Reinforced
1. **Incrementalism:** Small, safe, verifiable steps
2. **Test-Driven Safety:** No refactoring without tests
3. **Reversibility:** Changes can be undone
4. **Verification:** Run tests, monitor metrics
5. **Risk Mitigation:** Spread change over time

---

## 5. Next Steps

### Immediate Actions
1. Create `doctrine/tactics/refactoring-move-method.tactic.md`
2. Review `doctrine/tactics/refactoring-strangler-fig.tactic.md` for consistency
3. Update cross-references in related tactics
4. ⚠️ Verify against source URLs when internet-connected

### Research Limitations
⚠️ External URLs not accessible during research
- Synthesis based on established software engineering literature
- Patterns are well-documented across multiple authoritative sources
- Recommend manual verification against source URLs

---

## Sources

**Primary Authorities:**
- Martin Fowler: "Refactoring" (1999, 2018), Strangler Fig article (2004)
- Kent Beck: "Smalltalk Best Practice Patterns" (1997)
- Refactoring catalog: https://refactoring.guru/move-method
- Martin Fowler's bliki: https://martinfowler.com/bliki/StranglerFigApplication.html

**Supporting Literature:**
- Joshua Kerievsky: "Refactoring to Patterns" (2004)
- Michael Feathers: "Working Effectively with Legacy Code" (2004)
- Sam Newman: "Building Microservices" (2015, 2021)
