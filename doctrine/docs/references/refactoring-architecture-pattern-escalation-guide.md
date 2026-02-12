# Refactoring Architecture Pattern Escalation Guide

Purpose: Define escalation thresholds from code-level refactoring to architecture-pattern adoption.

## Escalation Thresholds

| Refactoring Trigger | Escalate To | Apply When | Risks |
|---|---|---|---|
| Legacy/new model semantic mismatch | Anti-Corruption Layer (ACL) | Domain boundary translation is recurring and costly | Added translation complexity and latency |
| Multiple clients with divergent data/workflow needs | BFF | Single backend causes persistent client-specific branching | Backend fragmentation and duplication |
| Sequential transformations become rigid monolith | Pipes and Filters | Processing stages can be independently evolved/deployed | Ordering/idempotency errors |
| Need immutable audit/replay of state changes | Event Sourcing | History is first-class requirement and event model is stable | Major complexity increase, migration cost |
| Remote transient failures cause flakiness | Retry pattern | Failures are temporary and operation is retry-safe | Retry storms and hidden systemic faults |
| Long-running backend operation over request/response | Async Request-Reply | Caller needs immediate ack with later status retrieval | Polling load and weak completion semantics |
| Read/write model tension in same bounded context | CQRS | Scale/complexity asymmetry justifies split models | Increased cognitive and operational overhead |

## Practical Rule

Treat architecture patterns as escalation tools, not default outcomes. Exhaust low-blast-radius refactoring first.

## Preconditions for Escalation

- Repeated pain observed over multiple changes.
- Simpler local refactorings no longer resolve the issue.
- Test/observability strategy exists for transition safety.
