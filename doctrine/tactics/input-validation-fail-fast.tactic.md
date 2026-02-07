# Tactic: Input Validation with Fail-Fast Feedback

**Invoked by:**
- (Discoverable — general best practice for external data processing)

**Related tactics:**
- (Standalone — focuses on validation patterns)

**Complements:**
- General secure coding practices
- API design and error handling patterns

---

## Intent

Validate input data comprehensively before processing to avoid wasting resources on invalid data. Provide clear, actionable feedback on errors to facilitate quick resolution while protecting system internals from exposure.

Apply when:
- Processing data is computationally expensive or time-consuming
- Invalid input mid-processing causes costly recovery or data corruption
- Clear error feedback reduces support burden
- Input data comes from external sources (users, APIs, file uploads)

## Preconditions

**Required inputs:**
- Clear specification of expected input format, structure, and constraints
- Understanding of which validations are critical vs. nice-to-have
- Logging infrastructure to capture detailed errors

**Assumed context:**
- Software designed to handle errors gracefully
- Input data specifications are stable (not changing daily)
- Team has expertise in validation implementation

**Exclusions (when NOT to use):**
- Validation checks introduce unacceptable latency (real-time systems)
- Input specifications are unclear or constantly evolving
- Errors are never monitored or acted upon (validation becomes security theater)
- Ultra-simple input with negligible processing cost

## Execution Steps

1. **Define validation categories** for input data:
   - **Presence**: Required fields exist and are not null/empty
   - **Format**: Data matches expected type/pattern (email, date, number)
   - **Range**: Values within acceptable bounds (age 0-150, quantity >0)
   - **Logical consistency**: Related fields are coherent (start_date < end_date)
   - **Uniqueness**: No duplicates when required (unique IDs, primary keys)
   - **Referential integrity**: Foreign keys reference existing records

2. **Prioritize validations by criticality**:
   - **Critical**: Would cause system crash, data corruption, or security breach
   - **Important**: Would produce incorrect results or require manual intervention
   - **Nice-to-have**: Improves user experience but system can handle gracefully

3. **Implement validation sequence** (fail-fast ordering):
   - **Step 1**: Presence checks (fastest, catch missing data immediately)
   - **Step 2**: Format/type checks (avoid type conversion errors)
   - **Step 3**: Range/constraint checks (ensure values within bounds)
   - **Step 4**: Logical consistency checks (cross-field validation)
   - **Step 5**: Uniqueness/referential checks (may require database queries—slowest)
   - **Halt at first failure** (do not continue to next step if current step fails)

4. **Design error feedback** (dual-level):
   - **User-facing message** (generic, safe):
     - Clear indication of what failed ("Email format invalid")
     - Actionable guidance ("Please provide email in format: user@domain.com")
     - **No** internal implementation details
     - **No** sensitive system information
   - **Internal log** (detailed, diagnostic):
     - Exact validation rule that failed
     - Input value that caused failure (sanitized if sensitive)
     - Context: timestamp, user ID, request ID
     - Stack trace if applicable

5. **Implement batch validation** (optional, for large datasets):
   - Collect all validation errors instead of stopping at first
   - Return comprehensive error report
   - Allow user to fix multiple issues in one iteration
   - **Trade-off**: Slightly slower validation, better UX

6. **Add security considerations**:
   - For security-sensitive errors: use generic message + reference number
   - Example: "An error occurred. Reference: 1234567890. Contact support if needed."
   - Log detailed error internally with reference number for support lookup
   - Prevents leaking system architecture or data patterns to attackers

7. **Configure monitoring and alerting**:
   - Track validation failure rates by rule
   - Alert on sudden spikes (may indicate data source issues)
   - Periodic review of common failures to improve upstream data quality

## Checks / Exit Criteria

- Validation categories defined (presence, format, range, logic, uniqueness, integrity)
- Validations prioritized by criticality
- Fail-fast sequence implemented (stops at first failure)
- Dual-level error feedback designed:
  - User messages: clear, actionable, no internals exposed
  - Internal logs: detailed, diagnostic, includes context
- Security-sensitive errors use generic messages + reference numbers
- Validation failure monitoring configured
- At least one successful validation failure test executed

## Failure Modes

- **Overly strict validation:** Rejecting valid data (false positives), frustrating users
- **Insufficient isolation:** Not stubbing external dependencies, causing slow validation
- **Exposing internals:** Detailed error messages reveal system architecture to attackers
- **No batch mode:** Forcing users to fix errors one-at-a-time in large datasets
- **Validation drift:** Rules become outdated as input specifications change
- **Performance bottleneck:** Complex validation checks slow down entire pipeline
- **Silently ignoring errors:** Logging errors but never reviewing or acting on them

## Outputs

- **Validation Module:**
  - Ordered validation checks (presence → format → range → logic → uniqueness)
  - Error code constants for each validation rule
  - User-facing message templates
  - Internal logging with context

- **Error Response Format:**
  ```json
  {
    "success": false,
    "error": {
      "code": "INVALID_EMAIL_FORMAT",
      "message": "Email format invalid. Expected format: user@domain.com",
      "field": "email",
      "reference": "20260207-054700-ABC123"
    }
  }
  ```

- **Internal Log Entry:**
  ```
  [ERROR] 2026-02-07T05:47:00Z | ref:20260207-054700-ABC123
  Validation failed: INVALID_EMAIL_FORMAT
  Field: email | Value: "user@domain" | Rule: RFC5322 email pattern
  User: user-id-456 | Request: req-789 | Source: API/upload
  ```

- **Monitoring Dashboard:**
  - Validation failure rate by rule (chart)
  - Most common validation errors (top 10 list)
  - Trend analysis (failures over time)

## Notes

**Resource efficiency:** Validating upfront prevents expensive processing of bad data. Time spent on validation < time wasted on failed processing.

**User experience balance:** Clear, helpful error messages improve UX. Overly technical messages confuse. Generic messages frustrate ("something went wrong").

**Security-first feedback:** For authentication, authorization, or data access errors, prefer generic messages to avoid information leakage. Track attempts internally for anomaly detection.

**Progressive validation:** For complex workflows, validate incrementally (validate step 1 input before showing step 2). Reduces user frustration from discovering late-stage errors.

**Validation libraries:** Leverage existing libraries (JSON Schema, Joi, Pydantic) instead of writing custom logic. Well-tested, optimized, and maintained by community.

**False positives cost:** If validation rejects too much valid data, users will route around the system or abandon usage. Balance strictness with practicality.

**Source:** Derived from "Fail Fast" practice at https://patterns.sddevelopment.be/practices/fail_fast/
