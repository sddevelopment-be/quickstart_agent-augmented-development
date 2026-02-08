# Directives Index

**Version:** 1.0.0  
**Last Updated:** 2026-02-08  
**Curator:** Claire

---

## Purpose

Directives are explicit instructions and constraints for agent behavior. Each directive is numbered (001-035+) for load-on-demand efficiency and prescribes what must or must not be done in specific situations.

---

## Active Directives

| Code | Directive | Purpose |
|------|-----------|---------|
| 001  | [CLI & Shell Tooling](./001_cli_shell_tooling.md) | Tool usage patterns (fd/rg/ast-grep/jq/yq/fzf) |
| 002  | [Context Notes](./002_context_notes.md) | Profile precedence & shorthand caution |
| 003  | [Repository Quick Reference](./003_repository_quick_reference.md) | Directory roles and structure |
| 004  | [Documentation & Context Files](./004_documentation_context_files.md) | Canonical file locations |
| 005  | [Agent Profiles](./005_agent_profiles.md) | Role specialization catalog |
| 006  | [Version Governance](./006_version_governance.md) | Versioned layer table & update rules |
| 007  | [Agent Declaration](./007_agent_declaration.md) | Operational authority affirmation |
| 008  | [Artifact Templates](./008_artifact_templates.md) | Template locations & usage rules |
| 009  | [Role Capabilities](./009_role_capabilities.md) | Allowed operational verbs & conflict prevention |
| 010  | [Mode Protocol](./010_mode_protocol.md) | Standardized mode transitions |
| 011  | [Risk & Escalation](./011_risk_escalation.md) | Markers, triggers, remediation procedures |
| 012  | [Common Operating Procedures](./012_operating_procedures.md) | Centralized behavioral norms |
| 013  | [Tooling Setup & Fallbacks](./013_tooling_setup.md) | Installation, version requirements, fallbacks |
| 014  | [Work Log Creation](./014_worklog_creation.md) | Standards for work logs with metrics |
| 015  | [Store Prompts](./015_store_prompts.md) | Prompt documentation with SWOT analysis |
| 016  | [Acceptance Test Driven Development](./016_acceptance_test_driven_development.md) | ATDD workflow and requirements |
| 017  | [Test Driven Development](./017_test_driven_development.md) | TDD workflow and unit test requirements |
| 018  | [Traceable Decisions](./018_traceable_decisions.md) | Decision capture protocols and traceability |
| 019  | [File-Based Collaboration](./019_file_based_collaboration.md) | Multi-agent orchestration via YAML tasks |
| 020  | [Lenient Adherence](./020_lenient_adherence.md) | Appropriate strictness levels |
| 021  | [Locality of Change](./021_locality_of_change.md) | Problem severity measurement |
| 022  | [Audience-Oriented Writing](./022_audience_oriented_writing.md) | Target audience adaptation |
| 023  | [Clarification Before Execution](./023_clarification_before_execution.md) | Uncertainty handling protocol |
| 024  | [Self-Observation Protocol](./024_self_observation_protocol.md) | Mid-execution self-checks (Ralph Wiggum loop) |
| 025  | [Framework Guardian](./025_framework_guardian.md) | Framework upgrade and audit procedures |
| 026  | [Commit Protocol](./026_commit_protocol.md) | Commit message format and workflow |
| 028  | [Bugfixing Techniques](./028_bugfixing_techniques.md) | Systematic bug resolution strategies |
| 034  | [Spec-Driven Development](./034_spec_driven_development.md) | Specification-first methodology |
| 035  | [Specification Frontmatter Standards](./035_specification_frontmatter_standards.md) | Metadata requirements for specs |

---

## Reserved Numbers

The following directive numbers are **reserved for future use**:

| Code | Status | Notes |
|------|--------|-------|
| 027  | Reserved | Number gap in sequence |
| 029  | Reserved | Number gap in sequence |
| 030  | Reserved | Number gap in sequence |
| 031  | Reserved | Number gap in sequence |
| 032  | Reserved | Number gap in sequence |
| 033  | Reserved | Number gap in sequence |

**Rationale:** These numbers were skipped during framework evolution, likely due to removed or unimplemented directives. They are reserved to maintain numerical stability and avoid confusion.

**Policy:** Do not reuse these numbers unless formally deprecating and replacing an existing directive.

---

## Usage Patterns

### Loading Directives

Directives are loaded on-demand using the pattern:

```
/require-directive 001
/require-directive 014
```

### Directive Precedence

Per DOCTRINE_STACK.md:
1. **Guidelines** override all other layers (highest precedence)
2. **Directives** override Tactics and Templates
3. **Approaches** provide rationale but don't override directives
4. **Tactics** are invoked by directives (procedural execution)
5. **Templates** shape directive outputs (lowest precedence)

### Creating New Directives

When adding a new directive:

1. **Choose next available number** in sequence (036+)
2. **Follow naming convention:** `XXX_descriptive_name.md`
3. **Include required sections:**
   - Purpose statement
   - Scope and context
   - Explicit instructions or constraints
   - Related directives/approaches/tactics
4. **Update this index** with new entry
5. **Cross-reference** from relevant agent profiles

---

## Related Documentation

- **[DOCTRINE_STACK.md](../DOCTRINE_STACK.md)** — Layer architecture and precedence rules
- **[DOCTRINE_MAP.md](../../docs/architecture/design/DOCTRINE_MAP.md)** — Framework structure overview
- **[Tactics Index](../tactics/README.md)** — Procedural execution guides invoked by directives
- **[Agent Profiles](../agents/)** — Role-specific directive usage patterns

---

## Maintenance

**Owner:** Curator Claire  
**Review Cycle:** Annual or when 5+ directives added/changed  
**Change Protocol:** Submit proposals via `${WORKSPACE_ROOT}/collaboration/inbox/`

---

**Last Reviewed:** 2026-02-08  
**Next Review:** 2027-02-08
