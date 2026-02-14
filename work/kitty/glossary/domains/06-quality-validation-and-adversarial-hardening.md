# Domain 06: Quality, Validation, and Adversarial Hardening

## Conceptual Focus
Terminology that defines correctness gates, invariants, and security/robustness defenses.

## Canonical Terms
- `context validation`
- `task metadata validation`
- `plan validation`
- `encoding validation`
- `path validation`
- `adversarial test suite`
- `CSV schema enforcement`
- `release readiness`

## Domain Semantics
- Validation is multi-layered: lifecycle correctness, file metadata integrity, runtime resilience, and security controls.
- Adversarial language is explicit and threat-model oriented (traversal, symlink, malformed payloads).
- Release language ties validations to operational gates and rollout safety.

## Evidence Anchors
- `src/specify_cli/plan_validation.py`
- `src/specify_cli/task_metadata_validation.py`
- `src/specify_cli/scripts/validate_encoding.py`
- `tests/adversarial/test_path_validation.py`
- `tests/adversarial/test_csv_attacks.py`
- `RELEASE_CHECKLIST.md`
