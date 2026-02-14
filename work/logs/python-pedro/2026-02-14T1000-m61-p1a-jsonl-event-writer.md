# Work Log: M6.1 P1a — JSONL Event Writer

**Date:** 2026-02-14
**Agent:** Python Pedro
**Task:** 2026-02-13T1000-m61-jsonl-event-writer
**Batch:** M6.1
**Status:** Complete ✅

## Summary

Implemented the append-only JSONL event writer for lifecycle and execution telemetry per ADR-047. This is the foundation for the Control Plane telemetry architecture.

## Deliverables

| File | Type | Description |
|------|------|-------------|
| `src/llm_service/telemetry/event_schema.py` | NEW | EventType enum (6 types) + frozen Event dataclass with JSON serialization |
| `src/llm_service/telemetry/event_writer.py` | NEW | EventWriter: append-only JSONL with fsync, optional rotation, crash-safe reads |
| `src/llm_service/telemetry/__init__.py` | MODIFIED | Added Event, EventType, EventWriter to public API |
| `tests/unit/telemetry/test_event_schema.py` | NEW | 12 tests: enum coverage, immutability, JSON roundtrip, schema conformance |
| `tests/unit/telemetry/test_event_writer.py` | NEW | 19 tests: write/read, crash-safety, rotation, concurrency, compatibility |

## Metrics

- **Tests:** 31 new (12 schema + 19 writer), 64 total telemetry tests passing
- **Coverage:** 100% on new modules (79 statements, 0 missed)
- **Existing tests:** 33 unchanged, all passing
- **Breaking changes:** None — existing TelemetryLogger/InvocationRecord unaffected

## Acceptance Criteria Status

- [x] EventType enum covers lifecycle + execution events (6 types)
- [x] Event dataclass with all ADR-047 fields (ts, run_id, task_id, phase, agent_role, tool, mode, event, status, log_paths, summary)
- [x] EventWriter.emit() appends JSON line + fsync
- [x] File rotation (configurable max_size_bytes, single backup)
- [x] JSONL valid (one JSON object per line, parseable)
- [x] Crash-safe (corrupt/incomplete lines skipped on read)
- [x] Unit tests: schema validation, write/read roundtrip, concurrent writes
- [x] 100% coverage (exceeds 80% requirement)
- [x] Compatible with existing telemetry/logger.py

## Design Decisions

- **Frozen dataclass** for Event: immutability aligns with ADR-046 patterns
- **os.open + os.fsync** instead of Python file API: guarantees write-ahead semantics
- **Single-backup rotation**: simple `.1` suffix; sufficient for local-first use case
- **Lenient read**: corrupt lines are silently skipped (crash-safety over strictness)

## Next Steps

- P1b (Query Service Facade) can now proceed — it reads from this JSONL writer
- Architecture/design alignment work continues on this branch
