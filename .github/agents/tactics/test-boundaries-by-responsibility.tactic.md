# Tactic: Define Test Boundaries by Functional Responsibility

**Invoked by:**
- [Directive 016 (ATDD)](../directives/016_acceptance_test_driven_development.md) — defining acceptance test scope
- [Directive 017 (TDD)](../directives/017_test_driven_development.md) — defining unit test boundaries

**Related tactics:**
- [`ATDD_adversarial-acceptance.tactic.md`](./ATDD_adversarial-acceptance.tactic.md) — adversarial acceptance test definition

**Complements:**
- [Directive 016 (ATDD workflow)](../directives/016_acceptance_test_driven_development.md)
- [Directive 017 (TDD workflow)](../directives/017_test_driven_development.md)

---

## Intent

Determine appropriate scope for a unit test by identifying which components are directly responsible for the functionality being validated, rather than strictly following structural boundaries (layers, modules). Reduces brittle tests while ensuring meaningful validation.

Apply when:
- Writing unit tests for features spanning multiple components
- Tests break frequently due to changes in unrelated layers
- Unclear whether to mock/stub a dependency
- Team debates "what is a unit?" in unit testing

## Preconditions

**Required inputs:**
- Specific functionality to be tested (user story, feature requirement)
- Understanding of system architecture and component responsibilities
- Access to stubbing/mocking tools

**Assumed context:**
- System has modular, structured architecture (not monolithic)
- Components have clear, defined responsibilities
- Team has basic understanding of test doubles (stubs, mocks)

**Exclusions (when NOT to use):**
- Unstructured/monolithic systems with unclear boundaries
- Features with no internal logic (pure pass-through to external services)
- When structural testing conventions are mandated by organization
- Legacy systems where responsibility boundaries are impossible to determine

## Execution Steps

1. **Identify functionality to validate**
   - Write 1-sentence description of feature being tested
   - Example: "User registration validates email format and creates account record"

2. **Map responsibility boundaries**:
   - List all components involved in delivering the functionality
   - For each component, ask: "Does this directly implement logic for this feature?"
   - Mark components as:
     - **Inside boundary:** Directly responsible for feature logic
     - **Outside boundary:** Supporting infrastructure, external dependencies

3. **Classify dependencies**:
   - **Inside boundary (do NOT mock):**
     - Business logic classes/functions implementing the feature
     - Value objects, domain models used by the feature
     - Validation rules specific to the feature
   - **Outside boundary (DO mock/stub):**
     - Database access layers
     - External APIs/services
     - File system operations
     - Network calls
     - Time/date providers
     - Other services outside the current module

4. **Define test scope statement**:
   - Write: "This test validates [functionality] by exercising [inside boundary components] while stubbing [outside boundary components]"
   - Example: "This test validates user registration by exercising UserRegistrationService and EmailValidator while stubbing UserRepository and EmailDeliveryService"

5. **Create focused test**:
   - Instantiate all inside-boundary components (real implementations)
   - Stub/mock all outside-boundary components
   - Write assertions against behavior of inside-boundary components
   - Do NOT assert on stubbed component interactions unless necessary for the functionality

6. **Verify boundary correctness**:
   - Ask: "If I refactor inside-boundary components without changing functionality, should this test still pass?" (Answer: Yes)
   - Ask: "If outside-boundary implementations change, should this test be affected?" (Answer: No, because they're stubbed)

## Checks / Exit Criteria

- Functionality to test identified and described (1 sentence)
- All components classified as inside or outside boundary
- Test scope statement written
- Test created with:
  - Real implementations for inside-boundary components
  - Stubs/mocks for outside-boundary components
  - Assertions focus on functionality, not implementation details
- Boundary verification questions answered correctly

## Failure Modes

- **Excessive mocking:** Stubbing components that are part of the functional slice (leads to testing test doubles instead of real logic)
- **Insufficient isolation:** Not stubbing external dependencies (leads to slow, fragile tests)
- **Structural bias:** Defining boundaries based on layers (e.g., "must mock service layer") instead of responsibilities
- **Over-assertion:** Verifying internal implementation details instead of functional outcomes
- **Unclear responsibilities:** Unable to determine which components are responsible for functionality (indicates architectural issue)
- **Monolithic testing:** Including too many components inside boundary (test becomes integration test)

## Outputs

- **Test Boundary Document** (for complex features):
  - Functionality description
  - Inside-boundary components (list)
  - Outside-boundary components (list)
  - Test scope statement
  - Rationale for boundary decisions

- **Unit Test** with:
  - Clear test name describing functionality
  - Setup section showing real vs. mocked components
  - Assertions on functional behavior
  - Comments explaining non-obvious boundary decisions (optional)

## Notes

**Goal of testing:** Validate functionality, not implementation structure. Tests should assert behavior visible to outside components (public API), not internal mechanics.

**Refactoring protection:** Well-defined boundaries allow refactoring inside-boundary components without breaking tests, as long as functionality remains unchanged.

**When to use integration tests:** If functionality has minimal internal logic and mostly coordinates external services, prefer integration tests over unit tests with extensive mocking.

**Team adoption:** This approach requires shared understanding of system responsibilities. Initial investment in boundary discussions pays off through reduced test brittleness.

**Migration from layer testing:** Teams accustomed to testing each layer in isolation may resist this approach. Start with small examples demonstrating reduced brittleness.

**Source:** Derived from "Define Test Boundaries" practice at https://patterns.sddevelopment.be/practices/define_test_boundaries/
