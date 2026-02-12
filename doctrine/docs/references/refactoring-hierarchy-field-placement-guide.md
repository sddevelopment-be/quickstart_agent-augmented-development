# Refactoring Hierarchy Field Placement Guide

Purpose: Decide when fields should be pulled up or pushed down in inheritance hierarchies.

## Decision Matrix

| Signal | Preferred Move | Apply When | Risk |
|---|---|---|---|
| Same field duplicated across subclasses | Pull Up Field | Field semantics and lifecycle are identical across variants | Premature abstraction when semantics differ subtly |
| Base class contains field used by only subset of subclasses | Push Down Field | Field is variant-specific and not universally valid | Fragmented initialization logic across subclasses |
| Field appears shared but drives conditional branches by type | Consider Strategy/State before field move | Behavior variation dominates over structure | Keeping brittle hierarchy with cosmetic field moves |

## Practical Steps

1. Map field reads/writes by class.
2. Validate invariant and lifecycle consistency.
3. Choose pull-up or push-down based on semantic ownership.
4. Apply incrementally with tests for construction and behavior paths.

## Guardrails

- Do not move fields based on line-count symmetry alone.
- Avoid hierarchy churn when composition would simplify responsibility boundaries.
