# Tactic: Refactoring.RetryPatternHardening

## Intent
Introduce or refactor retry behavior for transient-failure operations to improve resilience without masking persistent faults.

Use this tactic when existing retry logic is missing, duplicated, or inconsistent in integration boundaries.

---

## Preconditions
- Operation failures are known to be transient and retry-safe.
- Idempotency or compensation strategy is defined.
- Tests or simulations exist for retry success and exhaustion behavior.

Do not use this tactic when:
- Failures are deterministic or business-rule violations.
- Retrying can cause harmful side effects.

---

## Execution Steps
1. Identify target operation and transient failure modes.
2. Define retry policy (attempts, backoff, jitter, termination conditions).
3. Add or verify tests for success-after-retry and max-attempt exhaustion.
4. Encapsulate retry behavior in a single reusable component.
5. Replace duplicated ad-hoc retry blocks with the shared policy component.
6. Add logging/metrics hooks for attempts and terminal failure.
7. Run tests and targeted fault-injection checks.
8. Stop.

---

## Checks / Exit Criteria
- Retry behavior is centralized and policy-driven.
- Terminal failures surface clearly after policy exhaustion.
- No duplicate retry implementations remain in target scope.
- Tests pass for retry and non-retry paths.

---

## Failure Modes
- Retrying non-transient failures and increasing outage pressure.
- Missing jitter/backoff causing synchronized retry storms.
- Swallowing terminal errors after retries are exhausted.

---

## Outputs
- Shared retry policy implementation.
- Updated call sites using policy component.
- Passing resilience tests for retry scenarios.
