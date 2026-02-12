# Research Report: Refactoring Patterns Analysis
**Researcher:** Ralph (SDD Research Agent)  
**Date:** 2024  
**Purpose:** Inform creation of doctrine tactic files for Move Method and Strangler Fig patterns  
**Context:** Agent-Augmented Development Framework - Doctrine Stack Enhancement

---

## Executive Summary

This research synthesizes two foundational refactoring patterns:

1. **Move Method Refactoring** — A code-level refactoring that relocates methods to classes with stronger cohesion
2. **Strangler Fig Pattern** — An architectural migration strategy for incremental legacy system replacement

Both patterns emphasize incremental change, test-driven safety, and risk mitigation. They operate at different scales (method vs. system) but share core principles of gradual transformation.

⚠️ **Research Methodology Note:** External URLs were not accessible in the execution environment. This synthesis is based on established software engineering literature, including:
- Martin Fowler's "Refactoring: Improving the Design of Existing Code" (1999, 2018)
- Kent Beck's "Smalltalk Best Practice Patterns" (1997)
- Joshua Kerievsky's "Refactoring to Patterns" (2004)
- Michael Feathers' "Working Effectively with Legacy Code" (2004)
- Sam Newman's "Building Microservices" (2015, 2021)

These patterns are well-established in the software engineering canon and widely documented across multiple authoritative sources.

---

## 1. Move Method Refactoring

**Source Authority:** Martin Fowler (Refactoring catalog), https://refactoring.guru/move-method

### Description
Move Method is a foundational refactoring technique where a method is relocated from one class to another because the method uses more features (data or methods) of the target class than its current host. This refactoring improves cohesion by placing behavior close to the data it primarily operates on, thereby reducing coupling and improving the clarity of class responsibilities.

### Key Principles and Concepts

1. **Feature Envy (Code Smell)**
   - Primary indicator: method is more interested in another class than its current host
   - Manifests as excessive use of another class's data or methods
   - Named and cataloged by Fowler as a refactoring opportunity

2. **Cohesion Over Coupling**
   - Methods should live where they have the strongest relationships
   - High cohesion: related functionality grouped together
   - Low coupling: minimal dependencies between classes

3. **Single Responsibility Principle (SOLID)**
   - Each class should have one reason to change
   - Methods should support that singular purpose
   - Misplaced methods dilute class responsibility

4. **Information Expert Pattern (GRASP)**
   - The object that has the information should perform the work
   - Reduces need for data exposure and getter chains
   - Aligns responsibility with knowledge

5. **Law of Demeter (Principle of Least Knowledge)**
   - Reduce the number of classes a method needs to communicate with
   - Avoid "train wreck" calls: `a.getB().getC().doSomething()`
   - Moving methods closer to data reduces coupling chains

### When to Use It (Preconditions)

**Positive Indicators:**
- Method makes more calls to another class than to its own class
- Method uses more fields/properties from another class than its own
- Method's logic is conceptually more aligned with another class's responsibility
- Tests exist (or can be added) to verify behavior before and after the move
- Target class is a stable, appropriate home for the functionality
- Move will not create circular dependencies or violate architectural boundaries

**Negative Indicators (Do NOT use when):**
- Method genuinely coordinates between multiple classes (consider Extract Method first)
- Moving would create inappropriate coupling or violate architectural layers (e.g., domain -> infrastructure)
- Method is overridden by subclasses in ways that depend on current location
- Behavior is truly polymorphic and location-dependent
- Move would require exposing private data to support the method

### Step-by-Step Execution Approach

1. **Examine the method** — Identify all features (fields, methods) used by the candidate method
2. **Count references** — Determine which class has more features used by the method (quantitative assessment)
3. **Check for polymorphism** — Verify method isn't overridden in subclasses, or plan how to handle overrides
4. **Verify or add tests** — Ensure current behavior is protected by tests (characterization tests if legacy)
5. **Copy the method** to the target class (don't remove from source yet — coexistence phase)
6. **Adjust the method body:**
   - Change references to source class members to use a parameter or get them from target class
   - If method needs access to source class data, pass the source object as a parameter
   - Maintain exact behavior (no feature changes during refactoring)
7. **Compile and test** the new method in isolation (unit test level)
8. **Determine the interface:**
   - Make method public if it will be called from outside the target class
   - Keep it private/protected if only used internally
   - Consider naming: method may need renaming to fit target class context
9. **Update the original method** to delegate to the new location (temporary delegation):
   ```
   public ReturnType originalMethod(params) {
       return targetObject.newMethod(this, params);
   }
   ```
10. **Find all callers** and update them to call the new location directly (one at a time or in batches)
11. **Run tests** after each caller is updated (incremental verification)
12. **Remove the old method** once all callers are updated (cleanup phase)
13. **Run final comprehensive tests** (integration and system level)
14. **Stop**

### Common Failure Modes or Pitfalls

1. **Breaking Encapsulation**
   - Exposing internal data just to support the moved method
   - Creating excessive getters/setters
   - *Prevention:* Pass objects as parameters instead of exposing internals

2. **Creating Circular Dependencies**
   - Moving methods without considering dependency direction
   - A depends on B, then moving method makes B depend on A
   - *Prevention:* Map dependencies first, consider Extract Class if circular dependency is unavoidable

3. **Moving Too Early (Premature Refactoring)**
   - Before understanding the full responsibility allocation
   - Based on incomplete understanding of domain
   - *Prevention:* Wait for duplication or clear pattern (Rule of Three)

4. **Batch Moving Without Tests**
   - Moving multiple methods at once without verification steps
   - Compounding risk
   - *Prevention:* Move one method at a time, test after each

5. **Ignoring Inheritance Hierarchies**
   - Not considering how subclasses override or extend the method
   - Breaking polymorphic behavior
   - *Prevention:* Analyze class hierarchy, test all subclasses

6. **Feature Envy Cascade**
   - Moving a method only to discover it now causes feature envy in the target class
   - Symptom of deeper design issue
   - *Prevention:* Consider Extract Class to create new abstraction

7. **Loss of Context**
   - Moving a method that genuinely coordinates between classes
   - Should be Extract Method + Move instead
   - *Prevention:* If method uses features from 3+ classes, it's a coordinator

8. **Changing Behavior During Move**
   - Accidentally modifying logic while relocating
   - Mixing refactoring with feature work
   - *Prevention:* Strict discipline, separate commits, test coverage

9. **Missing Delegation Step**
   - Removing the old method before all callers are updated
   - Breaking existing code
   - *Prevention:* Always delegate first, remove last

### Example Scenarios

**Scenario 1: Customer and Order (Responsibility Misalignment)**
```java
// BEFORE: Order class has a method that's really about customer pricing policy
class Order {
  private Customer customer;
  private List<Item> items;
  
  public double getDiscount() {
    // This logic is all about customer, not order
    if (customer.isPremium()) return 0.15;
    if (customer.getYearsActive() > 5) return 0.10;
    return 0.05;
  }
  
  public double getTotal() {
    double subtotal = items.stream().mapToDouble(Item::getPrice).sum();
    return subtotal * (1 - getDiscount());
  }
}

// AFTER: Move to Customer where the pricing policy logic belongs
class Customer {
  private boolean isPremium;
  private int yearsActive;
  
  public double getDiscountRate() {
    if (this.isPremium) return 0.15;
    if (this.yearsActive > 5) return 0.10;
    return 0.05;
  }
}

class Order {
  private Customer customer;
  private List<Item> items;
  
  public double getTotal() {
    double subtotal = items.stream().mapToDouble(Item::getPrice).sum();
    return subtotal * (1 - customer.getDiscountRate());
  }
}
```

**Analysis:** The discount logic was Feature Envy — it used customer data exclusively. Moving it to Customer improves cohesion and aligns responsibility with knowledge.

**Scenario 2: Report Generation (Utility Extraction)**
```java
// BEFORE: ReportController has formatting logic (wrong layer)
class ReportController {
  private Report report;
  
  public String formatAsCurrency(double amount) {
    return "$" + String.format("%.2f", amount);
  }
  
  public String generateSummary() {
    return "Total: " + formatAsCurrency(report.getTotal());
  }
}

// AFTER: Move to CurrencyFormatter utility (proper separation of concerns)
class CurrencyFormatter {
  public static String format(double amount) {
    return "$" + String.format("%.2f", amount);
  }
}

class ReportController {
  private Report report;
  
  public String generateSummary() {
    return "Total: " + CurrencyFormatter.format(report.getTotal());
  }
}
```

**Analysis:** Formatting is cross-cutting, not specific to reports. Extract to utility class for reusability and testability.

**Scenario 3: Account and Transaction (Information Expert)**
```java
// BEFORE: Transaction calculates account balance (wrong expert)
class Transaction {
  private Account account;
  private double amount;
  
  public double calculateNewBalance() {
    return account.getCurrentBalance() + this.amount;
  }
}

// AFTER: Move to Account (information expert for balances)
class Account {
  private double currentBalance;
  
  public double calculateBalanceAfter(Transaction transaction) {
    return this.currentBalance + transaction.getAmount();
  }
}
```

**Analysis:** Account is the information expert for balance calculations. Transaction should describe itself, not calculate account state.

---

## 2. Strangler Fig Pattern

**Source Authority:** Martin Fowler (2004), https://martinfowler.com/bliki/StranglerFigApplication.html

### Description
The Strangler Fig Pattern is an architectural migration strategy where a new system gradually replaces an old system by implementing new functionality alongside the legacy code and incrementally routing traffic to the new implementation. Named after the strangler fig vine (genus Ficus) that grows around a host tree and eventually replaces it, this pattern allows for safe, reversible, low-risk evolution of systems without requiring a risky "big bang" rewrite.

**Botanical Metaphor:** Strangler figs germinate in tree canopies, send roots to the ground, and gradually envelope the host tree. The host may eventually die and decompose, leaving a hollow fig tree structure. This mirrors how new systems grow around and eventually replace legacy systems.

### Key Principles and Concepts

1. **Incremental Replacement**
   - Replace functionality piece by piece, not all at once
   - Each increment is small enough to be reversible
   - Reduces cognitive load and testing scope per iteration

2. **Coexistence During Migration**
   - Old and new implementations run simultaneously during transition
   - Both implementations are "production" during overlap
   - Requires temporary duplication and synchronization

3. **Reversibility and Safety**
   - Each step can be rolled back if problems arise
   - Feature flags or routing changes enable instant rollback
   - De-risks migration through escape hatches

4. **Verification at Each Step**
   - Tests and monitoring confirm equivalence before proceeding
   - Behavioral parity is continuously validated
   - Metrics-driven confidence building

5. **Routing/Interception Layer**
   - Facade, proxy, API gateway, or adapter directs traffic
   - Abstracts the decision of which implementation to use
   - Enables gradual traffic shifting (canary, percentage-based)

6. **Eventual Complete Replacement**
   - Old code is safely deleted only after all traffic is rerouted
   - Temporary complexity (duplication, routing) is eliminated
   - End state is clean, not compromised

7. **Risk Mitigation Through Time**
   - Spreads deployment risk across multiple releases
   - Limits blast radius of any single change
   - Allows learning and adjustment during migration

8. **Business Continuity**
   - System remains operational throughout migration
   - No maintenance windows or "big bang" cutover
   - Users experience seamless transition

### When to Use It (Preconditions)

**Positive Indicators:**
- Large-scale refactoring or system replacement that cannot be done safely in one step
- Legacy system must remain operational during migration (zero-downtime requirement)
- Incremental deployment and testing capabilities exist (CI/CD, feature flags)
- Ability to introduce a routing/interception layer (architectural seam exists or can be created)
- Tests exist or can be created to verify behavioral equivalence
- Team has capacity for temporary code duplication and maintenance overhead
- Rollback capability is important (risk-averse environment)
- Migration timeline is measured in weeks or months, not days (sustained effort)
- Organizational commitment to completing the migration (not abandoning mid-stream)

**Negative Indicators (Do NOT use when):**
- Simple, safe single-step refactoring is possible (use simpler techniques)
- System architecture prevents coexistence (no seams, tightly coupled monolith)
- Tests cannot be created and behavioral verification is impossible (undocumented, chaotic legacy)
- Temporary duplication creates unacceptable maintenance burden (very high change rate)
- Old system can be safely shut down for complete replacement (acceptable downtime)
- Change scope is small and low-risk (overkill for simple changes)
- Team lacks discipline to finish migration (risk of permanent duplication)

### Step-by-Step Execution Approach

1. **Identify the subsystem or behavior** to be replaced
   - Define clear boundaries (API surface, module, service)
   - Document current behavior comprehensively

2. **Create or verify comprehensive tests** for existing behavior
   - Characterization tests if documentation is poor
   - Focus on external behavior, not internal structure
   - Establish baseline for equivalence verification

3. **Introduce a routing layer** (facade, adapter, proxy, API gateway)
   - Abstracts caller from implementation choice
   - Initially routes 100% to old implementation
   - Must be lightweight and reliable (don't create new single point of failure)

4. **Select the first slice** of functionality to migrate
   - Choose low-risk, high-value first (build confidence)
   - Prefer vertical slices (end-to-end functionality)
   - Keep slice small (1-2 weeks of work maximum)

5. **Implement the new version** of the selected slice alongside the old
   - Both implementations exist simultaneously
   - New implementation should pass same tests as old
   - May require data synchronization if stateful

6. **Verify equivalence**
   - Run tests against both implementations
   - Use parallel runs or shadow mode to compare outputs
   - Validate non-functional requirements (performance, security)

7. **Route a small percentage** of traffic to the new implementation
   - Start with 1-5% (canary deployment)
   - Use feature flags or percentage-based routing
   - Ensure ability to instantly revert to 0%

8. **Monitor and measure**
   - Watch for errors, exceptions, timeouts
   - Compare performance metrics (latency, throughput)
   - Collect user feedback if applicable
   - Set objective criteria for "success"

9. **Gradually increase traffic** to new implementation
   - If monitoring shows success, increase percentage (10%, 25%, 50%, 75%, 100%)
   - Pause at each level to observe
   - Rollback immediately if problems detected

10. **Iterate steps 4-9** for each additional slice of functionality
    - Repeat until entire subsystem is migrated
    - Maintain discipline and incremental approach throughout

11. **Remove routing to old implementation** for each completed slice
    - Once slice is 100% on new implementation for stability period
    - Simplify routing logic as old paths are eliminated

12. **Delete old code** once fully replaced and verified unused
    - Confirm no callers remain (static analysis, runtime monitoring)
    - Archive for reference if needed
    - Celebrate deletion (reducing code is a positive outcome)

13. **Remove or simplify routing layer** if no longer needed
    - Direct calls if no future flexibility needed
    - Keep simplified routing if useful for future migrations

14. **Run final comprehensive tests**
    - Full regression suite
    - Load and performance testing
    - Security scanning

15. **Stop**

### Common Failure Modes or Pitfalls

1. **Forgetting to Test First**
   - Starting migration without adequate test coverage
   - Leads to silent breakage and undetected regressions
   - *Prevention:* Characterization testing is mandatory before starting

2. **Big Slices (Not Incremental Enough)**
   - Trying to migrate too much at once
   - Loses the incremental risk-reduction benefit
   - *Prevention:* Enforce slice size limits (1-2 weeks maximum)

3. **Divergent Implementations**
   - Allowing old and new to evolve differently during migration
   - Creates maintenance nightmare and extends migration timeline
   - *Prevention:* Feature freeze on old implementation, or sync changes

4. **Premature Removal**
   - Deleting old code before all routing is complete
   - Breaking edge cases or hidden dependencies
   - *Prevention:* Comprehensive usage analysis, monitoring before removal

5. **No Rollback Plan**
   - Not maintaining ability to quickly switch back to old implementation
   - High risk if problems discovered in production
   - *Prevention:* Test rollback procedure, keep it simple (feature flag toggle)

6. **Monitoring Gaps**
   - Not measuring success/failure of new implementation adequately
   - Flying blind during migration
   - *Prevention:* Define metrics up front, instrument both implementations

7. **Mixing Concerns**
   - Combining refactoring with new feature development
   - Scope creep, confusion about what changed
   - *Prevention:* Strict separation, feature freeze during migration

8. **Routing Complexity Explosion**
   - Creating overly complex routing logic that becomes technical debt
   - Routing layer becomes its own legacy system
   - *Prevention:* Keep routing simple, remove logic as slices complete

9. **Incomplete Migration (Abandonment)**
   - Starting strangler pattern but never finishing
   - Permanent duplication, ongoing maintenance burden
   - *Prevention:* Executive commitment, dedicated team capacity, track progress

10. **Architecture Mismatch**
    - New implementation doesn't fit well alongside old
    - Forced coexistence creates unnatural boundaries
    - *Prevention:* Architectural design up front, proof of concept for coexistence

11. **Testing Only New Code**
    - Not verifying behavioral equivalence between old and new
    - Drift in behavior over time
    - *Prevention:* Comparison testing, parallel runs, shadow mode

12. **Ignoring Non-Functional Requirements**
    - New implementation has different performance, security, or operational characteristics
    - Surprises in production under load
    - *Prevention:* NFR testing at each percentage level, production-like environments

### Example Scenarios

**Scenario 1: E-commerce Payment Processing Migration**
```
Context: Legacy payment system uses outdated payment gateway (PCI compliance issues, 
high fees, no modern features). Need migration to modern provider (Stripe, Adyen) 
without payment disruption.

Challenges:
- Zero tolerance for payment failures (revenue impact)
- Complex retry logic and error handling in legacy system
- Historical transaction data must remain accessible

Strangler Fig Approach:

Step 1: Create PaymentService interface (routing layer)
  interface PaymentService {
    PaymentResult processPayment(PaymentRequest request);
    PaymentStatus getStatus(String transactionId);
  }

Step 2: Implement adapter for legacy gateway
  class LegacyPaymentAdapter implements PaymentService {
    // Wraps existing legacy payment code
  }

Step 3: Implement adapter for new gateway
  class ModernPaymentAdapter implements PaymentService {
    // Integrates with Stripe/Adyen API
    // Mirrors legacy retry and error handling
  }

Step 4: Route 1% of payments through new gateway with comprehensive logging
  - Select low-value transactions first (< $10)
  - Log every request/response for comparison
  - Set up alerts for failures

Step 5: Monitor for errors, payment failures, processing time
  - Success rate: 99.9%+ required to proceed
  - Latency: Must match or beat legacy (< 500ms p95)
  - Error rates: Track by error type

Step 6-10: Gradually increase to 5%, 10%, 25%, 50%, 75%, 100%
  - Pause at each level for 48 hours
  - Include high-value transactions at 50%
  - Monitor continuously

Step 11: Maintain fallback to legacy for 2 weeks after 100%
  - Keep feature flag in place
  - Monitor for delayed failures or chargebacks
  - Build confidence in new system

Step 12: Remove legacy adapter and gateway integration
  - Archive legacy code
  - Terminate legacy gateway contract
  - Simplify routing to direct call

Step 13: Simplify routing layer to direct call
  if (legacyGatewayNeeded) { // Always false now
    // Dead code, remove
  }
  return modernPaymentAdapter.processPayment(request);

Benefits Realized:
- Zero downtime during migration
- Instant rollback capability at each step
- Validated with real production traffic
- Caught performance issues early (at 10%) and optimized
- Total migration time: 6 weeks

Metrics:
- Success rate: 99.95% (improved from 99.8% on legacy)
- Average latency: 280ms (reduced from 450ms)
- Cost per transaction: Reduced 30%
```

**Scenario 2: Monolith to Microservices - User Service Extraction**
```
Context: Monolithic e-commerce application has grown to 500K LOC. Team velocity 
decreasing, deployment risk increasing. Extract user management as first microservice.

Challenges:
- User data accessed from 47 different modules in monolith
- Authentication tightly coupled to HTTP session
- User preferences scattered across multiple database tables
- Cannot afford authentication outage

Strangler Fig Approach:

Step 1: Create UserService microservice (new implementation)
  - REST API for user operations
  - Separate database (eventual consistency acceptable)
  - Authentication JWT-based

Step 2: Implement API gateway routing layer
  - Kong/Nginx sits in front of monolith
  - Routes /api/users/* to either monolith or UserService
  - Initially 100% to monolith

Step 3: Migrate user authentication to new service
  - UserService issues JWT tokens
  - Monolith validates JWT tokens (dual authentication temporarily)
  - Route POST /api/users/login to UserService

Step 4: Verify authentication works equivalently
  - Parallel run: Authenticate with both systems, compare results
  - Shadow mode for 1 week
  - Load testing with authentication traffic

Step 5: Migrate user profile management (GET/PUT /api/users/:id)
  - Read from UserService, sync writes to both systems
  - Data synchronization layer (temporary)
  - Route reads to UserService, writes to both

Step 6: Migrate user preferences (GET/PUT /api/users/:id/preferences)
  - Similar dual-write approach
  - Verify consistency daily

Step 7: Route all user-related calls to microservice
  - Gradually increase routing percentage
  - Monitor for cache invalidation issues
  - Handle distributed transactions (eventual consistency)

Step 8: Remove user code from monolith
  - Delete UserController, UserService (monolith classes)
  - Remove user-related database tables (after data validated)
  - Remove synchronization layer

Step 9: Retire direct monolith database access for user data
  - All user data flows through UserService API
  - Enforce via database permissions

Timeline: 4 months

Challenges Encountered:
- Session management migration (solved with JWT)
- Transaction boundaries (user + order creation) — used saga pattern
- Cache invalidation across services — event-driven invalidation
- Database migration (copied data, then synced, then cut over)

Benefits:
- User team can deploy independently
- Improved user service performance (optimized for read-heavy workload)
- Clearer boundaries and ownership
- Established pattern for future microservice extractions
```

**Scenario 3: Legacy Reporting System Replacement**
```
Context: Old reporting system uses custom templating engine (10 years old, no 
maintainer), migrating to modern BI platform (Tableau/PowerBI).

Challenges:
- 200+ reports in production
- Custom SQL queries embedded in templates
- Users trained on old UI
- Some reports used in automated processes (email, dashboards)

Strangler Fig Approach:

Step 1: Identify 20 most-used reports (80/20 rule)
  - Analyze usage logs
  - Interview stakeholders
  - Prioritize by business impact

Step 2: Create ReportRouter that checks report type
  class ReportRouter {
    Report getReport(String reportId) {
      if (migratedReports.contains(reportId)) {
        return modernReportingEngine.generate(reportId);
      } else {
        return legacyReportingEngine.generate(reportId);
      }
    }
  }

Step 3: Migrate top 3 reports to new platform
  - Recreate in Tableau
  - Validate data accuracy (row-by-row comparison)
  - Match formatting as closely as possible

Step 4: Route those report requests to new system
  - Add report IDs to migratedReports set
  - Monitor for user complaints

Step 5: Compare outputs side-by-side for 1 week
  - Generate same report from both systems
  - Automated diff tool
  - Investigate discrepancies

Step 6-10: Migrate next 5 reports, continue until top 20 complete (3 months)

Step 11: Assess remaining 180 reports
  - 120 unused in last 6 months — archive without migration
  - 40 rarely used — migrate on demand
  - 20 medium usage — migrate in next phase

Step 12: Deprecate and remove old reporting engine
  - Notify users 90 days in advance
  - Offer training on new platform
  - Archive old engine code

Step 13: Update documentation and user training
  - New report creation guides
  - Video tutorials
  - Office hours for questions

Timeline: 6 months for top 20, additional 3 months for remaining

Benefits:
- Avoided migrating 120 unused reports (60% savings)
- Users involved throughout (feedback loop)
- Incremental training (not overwhelming)
- Modern platform enables self-service (users create new reports)

Lessons Learned:
- Usage data is critical (don't migrate unused features)
- Side-by-side comparison builds trust
- User involvement prevents resistance
```

**Scenario 4: Framework Migration - Vue 2 to Vue 3**
```
Context: Large Vue 2 application (150 components, 80K LOC) needs migration to 
Vue 3 for Long-Term Support and performance benefits.

Challenges:
- Breaking changes in Vue 3 (Composition API, emits, removed features)
- Components tightly coupled (prop drilling, event buses)
- No component tests (only E2E tests)
- Active feature development cannot stop

Strangler Fig Approach:

Step 1: Set up Vue 3 alongside Vue 2 using @vue/compat (migration build)
  - Compatibility layer allows gradual migration
  - Both runtimes loaded initially
  - Configuration flags control Vue 2 vs. Vue 3 behavior per component

Step 2: Create routing that determines which version renders each component
  - Compatibility layer handles this automatically
  - Track migration status per component

Step 3: Migrate leaf components first (no children, minimal props)
  - Start with utility components (buttons, icons, inputs)
  - Add component tests during migration
  - Mark components as Vue 3-ready with config flag

Step 4: Verify component behavior with tests
  - Visual regression tests (Chromatic/Percy)
  - Unit tests with Testing Library
  - Interaction tests

Step 5: Gradually migrate parent components (bottom-up approach)
  - Child components already migrated
  - Update to Composition API
  - Remove deprecated patterns (filters, event bus)

Step 6: Use feature flags to control which version is active per route/component
  - A/B test routes with Vue 3 components
  - Monitor for console errors
  - Measure performance improvements

Step 7: Monitor for console errors and behavior differences
  - Automated error tracking (Sentry)
  - Performance monitoring (Web Vitals)
  - User session recordings for UX issues

Step 8: Remove Vue 2 and compat layer once migration complete
  - Delete compatibility configuration
  - Remove Vue 2 dependencies
  - Bundle size reduction

Timeline: 8 months (2 components per sprint)

Strategy: Bottom-up migration (leaf components → parents → root), 
         vertical slices (full routes), parallel to feature development

Benefits:
- Maintained feature velocity during migration
- Improved component quality (tests added)
- Performance improvements (Composition API, smaller bundles)
- Team learned Vue 3 incrementally (not overwhelming)
- No "big bang" rollout (reduced risk)

Challenges:
- Compatibility layer had bugs (required workarounds)
- Some patterns required complete rethinking (event bus → props/emits)
- Discipline required to not mix Vue 2/3 patterns
```

---

## 3. Comparison and Relationships

### Similarities
| Aspect | Move Method | Strangler Fig |
|--------|------------|---------------|
| **Incrementalism** | One method at a time | One subsystem slice at a time |
| **Test Dependence** | Requires tests to verify behavior preservation | Requires tests to verify behavioral equivalence |
| **Verification Steps** | Run tests after each caller updated | Monitor and measure after each traffic increase |
| **Risk Reduction** | Small, reversible steps | Small, reversible increments |
| **Coexistence Phase** | Temporary delegation from old to new | Extended parallel operation of old and new |
| **Cleanup** | Remove old method after all callers updated | Remove old implementation after all traffic rerouted |

### Differences
| Dimension | Move Method | Strangler Fig |
|-----------|------------|---------------|
| **Scale** | Code-level (single method, class) | System-level (subsystems, services, modules) |
| **Duration** | Minutes to hours | Weeks to months |
| **Complexity** | Low (mechanical refactoring) | High (architectural, organizational) |
| **Risk** | Low (compile-time safety, small scope) | High (runtime behavior, large scope) |
| **Coexistence** | Brief delegation phase (temporary) | Extended parallel operation (sustained) |
| **Coordination** | Individual developer | Team or multiple teams |
| **Testing** | Unit tests primarily | Integration, E2E, monitoring, shadow mode |
| **Rollback** | Version control revert | Feature flags, routing changes, deployment rollback |
| **Motivation** | Improve class cohesion, reduce coupling | Replace legacy, architectural migration, rewrite |

### When to Use Which

**Use Move Method when:**
- Working within a single codebase at code structure level
- Goal is to improve class design and responsibility allocation
- Change can be completed in minutes to hours
- Low risk, high confidence
- Compile-time safety available
- Affects small number of call sites

**Use Strangler Fig when:**
- Working at system or architectural level
- Goal is to replace legacy subsystems or migrate architectures
- Change requires weeks to months
- High risk, need gradual validation
- Runtime behavior must be verified in production
- Affects large number of integration points
- Business continuity is critical

### Combined Usage (Nested Patterns)

Strangler Fig may employ Move Method refactorings as part of implementing the new system:

**Example: Microservice Extraction**
1. **Outer Loop (Strangler Fig):** Extract OrderService from monolith
   - Create new microservice
   - Route traffic incrementally
   - Eventual remove from monolith

2. **Inner Loop (Move Method):** While building OrderService microservice
   - Move calculateDiscount() from Order to Customer (Move Method)
   - Extract calculateTax() to TaxCalculator utility (Move Method)
   - Organize new microservice with clean boundaries

**Result:** Well-structured microservice, safely extracted using Strangler Fig, with internal refactoring via Move Method

---

## 4. Integration with Agent-Augmented Development Framework

### Relationship to Existing Doctrine Elements

**Directives:**
- **Directive 017 (Test Driven Development):** Both patterns depend on test-driven safety
  - Move Method requires tests to verify behavior preservation
  - Strangler Fig requires tests to verify behavioral equivalence

**Approaches:**
- **Trunk-Based Development:** Complements Strangler Fig (short-lived branches for each slice)
- **Locality of Change:** Aligns with Move Method (surgical, minimal changes)

**Existing Tactics:**
- **refactoring-strangler-fig.tactic.md:** Already exists, should be reviewed for consistency with this research
- **refactoring-extract-first-order-concept.tactic.md:** Related to Move Method (both improve structure)
- **safe-to-fail-experiment-design.tactic.md:** Provides low-risk validation framework for Strangler Fig steps

### Proposed New Tactic

**File:** `refactoring-move-method.tactic.md`

**Structure:** Follow template at `doctrine/templates/tactic.md`

**Related Tactics:** 
- `refactoring-extract-first-order-concept.tactic.md` (complementary, both improve class design)
- `refactoring-strangler-fig.tactic.md` (different scale, similar incrementalism)

**Complements:**
- [Directive 017 (Test Driven Development)](../directives/017_test_driven_development.md)
- Approach: Locality of Change

### Key Doctrinal Principles Reinforced

1. **Incrementalism:** Both patterns embody small, safe, verifiable steps
2. **Test-Driven Safety:** No refactoring without tests
3. **Reversibility:** Changes can be undone if problems arise
4. **Verification:** Don't trust, verify (run tests, monitor)
5. **Risk Mitigation:** Spread change over time, limit blast radius

---

## 5. Research Quality and Limitations

### Source Authority
✅ Both patterns originate from Martin Fowler, a recognized authority in software refactoring and architecture
✅ Widely documented in canonical software engineering literature
✅ Established patterns with 20+ years of industry validation
✅ Cross-referenced in multiple authoritative sources

### Limitations
⚠️ External URLs were not directly accessible during research (execution environment lacks internet)
⚠️ Synthesis is based on general knowledge of well-established patterns, not real-time web content
⚠️ Specific examples from refactoring.guru and martinfowler.com could not be directly quoted

### Verification Recommendations
1. Manually verify synthesized content against source URLs when internet access is available
2. Confirm specific terminology and example code match source materials
3. Check for any recent updates or refinements to the patterns (as of 2024)
4. Validate that Fowler's Strangler Fig article aligns with this synthesis

### Confidence Assessment
- **Move Method:** High confidence (fundamental refactoring, well-established, minimal variance across sources)
- **Strangler Fig:** High confidence (Fowler's original article well-known, pattern widely adopted)
- **Examples:** Moderate confidence (synthesized from general software engineering knowledge, not source-specific)
- **Integration Notes:** High confidence (based on actual doctrine framework inspection)

---

## 6. Recommendations

### Immediate Actions
1. ✅ Create `doctrine/tactics/refactoring-move-method.tactic.md` following template
2. ✅ Review `doctrine/tactics/refactoring-strangler-fig.tactic.md` for consistency with research
3. ✅ Update tactic relationships (cross-reference in "Related tactics" sections)
4. ⚠️ Verify research against source URLs when internet-connected

### Documentation Enhancements
- Consider adding code examples to tactics (template currently doesn't include them)
- Create visual diagrams for Strangler Fig routing layer evolution
- Document combined usage patterns (nested tactics)

### Future Research
- **Extract Method Refactoring:** Complement to Move Method (extract before move)
- **Extract Class Refactoring:** When Move Method reveals need for new abstraction
- **Branch by Abstraction:** Alternative to Strangler Fig for certain scenarios
- **Parallel Change (Expand-Contract):** Related incremental migration pattern

---

## Appendices

### A. Pattern Origins and History

**Move Method:**
- First documented by Kent Beck in Smalltalk patterns (1990s)
- Popularized by Martin Fowler in "Refactoring" (1999)
- Remains unchanged in 2nd edition (2018) — foundational pattern

**Strangler Fig:**
- Introduced by Martin Fowler in 2004 blog post
- Named after strangler fig plants observed in Australian rainforest
- Gained prominence with microservices movement (2010s)
- Now standard pattern for legacy modernization

### B. Related Patterns

**Code-Level Refactoring:**
- Extract Method
- Extract Class
- Inline Method (opposite of Extract/Move)
- Move Field
- Introduce Parameter Object

**Architectural Migration:**
- Branch by Abstraction (Google's approach)
- Parallel Change (Expand-Contract pattern)
- Blue-Green Deployment (infrastructure level)
- Canary Deployment (gradual rollout)
- Feature Toggles (runtime configuration)

### C. Tool Support

**Move Method:**
- IDE automated refactoring (IntelliJ, VS Code, Eclipse)
- Static analysis tools (linters, code quality tools)
- Test frameworks (JUnit, Jest, pytest)

**Strangler Fig:**
- API Gateways (Kong, Nginx, AWS API Gateway)
- Feature flag platforms (LaunchDarkly, Unleash, Split)
- Service meshes (Istio, Linkerd) — traffic routing
- Monitoring (Datadog, New Relic, Prometheus)
- Observability (OpenTelemetry, Jaeger, Zipkin)

---

**End of Research Report**

**Status:** Ready for tactic file creation  
**Next Steps:** 
1. Create `refactoring-move-method.tactic.md`
2. Review and update `refactoring-strangler-fig.tactic.md` if needed
3. Verify against source URLs when possible
