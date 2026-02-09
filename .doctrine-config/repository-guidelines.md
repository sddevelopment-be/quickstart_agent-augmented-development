# Project-Specific Guidelines

**Version:** 1.1.0
**Last Updated:** 2026-02-09
**Status:** Active

This document contains project-specific conventions and guidelines that supplement the core agent framework directives. All agents and contributors should follow these guidelines when working in this repository.

---

## Domain Rules

- Never use production credentials.
- Respect privacy / anonymisation requirements.
- **Planning/documenting future work is NOT completion.** Only mark tasks complete after implementation, testing, and validation. Documenting next steps or creating follow-up tasks does not constitute completion of current work.
- **Distinguish clearly between "foundation complete" and "work complete"** - partial implementations should be documented as such with remaining work identified

---

## Commit Message Guidelines

### Format

```
<agent-slug>: Epic/Task name or description - Specific comment

<optional body with details>
```

### Examples

```
backend-benny: Phase 4 Validation - Implement ExposureClassPredicate

Added predicate to compare exposure class types between OSX and ABACUS
records. Includes unit tests for matching, mismatching, and edge cases.
```

```
architect-alphonso: Review Gate 3 - Approve Phase 4 implementation

Code review completed. All architecture constraints satisfied.
See work/reports/reviews/2026-02-02-phase4-code-review.md
```

```
planning-petra: Roadmap update - Mark Phase 4 complete

Updated PLAN_OVERVIEW.md and NEXT_BATCH.md to reflect Phase 4 completion.
Phase 5 (Reporting) now ready to start.
```

### Header Components

| Component | Description | Example |
|-----------|-------------|---------|
| `<agent-slug>` | Agent identifier (lowercase, hyphenated) | `backend-benny` |
| Epic/Task | High-level work item | `Phase 4 Validation` |
| Specific comment | What this commit does | `Implement ExposureClassPredicate` |

---

## Agent Commit Signing

### Policy: Unsigned Commits for Agents

Commits made by agents **must be unsigned** to:

1. **Avoid password prompts** — GPG signing requires the human-in-charge's passphrase
2. **Clarify authorship** — Unsigned commits clearly indicate automated/agent work
3. **Maintain workflow** — Agents can commit without human intervention

### Implementation

When committing as an agent, ensure GPG signing is disabled:

```bash
git commit --no-gpg-sign -m "agent-slug: Description"
```

Or configure locally for this repository:

```bash
git config commit.gpgsign false
```

### Human Commits

Human-authored commits may be signed per normal workflow. The distinction helps identify:
- **Signed commits** → Human-authored, manually verified
- **Unsigned commits** → Agent-authored, automated workflow

---

## Testing Standards

All implementation work **must adhere** to the following testing styleguides:

| Document | Purpose |
|----------|---------|
| `docs/styleguides/GENERIC_TESTING.md` | Core testing principles, test structure, minimization |
| `docs/styleguides/FORMALIZED_CONSTRAINT_TESTING.md` | Contract-based testing patterns (equals, hashCode, serialization) |

### Key Principles

- Follow **Quadruple-A structure**: Arrange → Assumption → Act → Assert
- Prefer **contract tests** over spot-checks
- Avoid **logical duplication** (code overlap is allowed)
- Apply **"just enough" testing** — remove tests that no longer add value
- Include **positive and negative** cases for every contract
- **Minimum 80% coverage** on new code, all tests passing before completion
- Use **TDD approach** (Directive 017): Write tests first, implement to pass, refactor

### Technical Constraints

- Target language: Python 3.10+, JavaScript/Node.js for tooling
- Preferred frameworks: pytest for testing, Flask for services
- Follow ADR-documented architectural decisions

### Output Expectations

- Code style: Follow existing patterns, use type hints
- Documentation: Update ADRs for architectural decisions, maintain work logs per Directive 014
- File formats: YAML for configuration, Markdown for documentation

---

## File and Directory Naming Conventions

### Directory Names

- **Preference:** Use lowercase with underscores for multi-word directory names
- **Examples:**
  - ✅ `ready_for_dev/`, `spec_validation_reports/`, `data/base_in/`
  - ❌ `Ready for Dev/`, `ReadyForDev/`, `ready-for-dev/`
- **Rationale:**
  - Consistent with Unix/Linux conventions
  - Avoids issues with case-sensitive filesystems
  - Easier to type in CLI environments
  - Prevents confusion with spaces in directory names

### File Names

- **Java files:** Follow Java naming conventions (PascalCase for classes)
- **Configuration files:** lowercase with underscores or hyphens
  - Examples: `example.txt`, `application-test.properties`, `pom.xml`
- **Documentation files:** UPPERCASE for root-level docs (e.g., `README.md`, `AGENTS.md`)
  - Subdirectory docs may use lowercase or mixed case as appropriate

---

## Terminology and Concept Management

### Glossary Updates Required

When introducing **new concepts, terminology, or framework elements**, agents and contributors **must update** the framework Glossary:

- **Location:** `doctrine/GLOSSARY.md` (or `.github/agents/GLOSSARY.md` during migration)
- **Trigger events:**
  - Defining new agent roles, capabilities, or patterns
  - Introducing framework concepts (e.g., "doctrine stack layer", "handoff pattern")
  - Creating domain-specific terminology used across multiple files
  - Establishing acronyms or shorthand notation
- **Update process:**
  1. Add term with precise definition
  2. Include context about where/how it's used
  3. Link related concepts
  4. Maintain alphabetical order within sections

### Example Glossary Entry

```markdown
## Shorthand

**Definition:** A reusable command alias or prompt template that allows quick invocation of complex agent workflows through simple keywords.

**Context:** Stored in `doctrine/shorthands/`. Originally tracked in `aliases.md`.

**Related:** Command aliases, prompt templates, orchestration patterns
```

**Rationale:** Maintaining a canonical Glossary ensures:
- Consistent terminology across the framework
- Clear onboarding path for new contributors
- Reduced ambiguity in multi-agent coordination
- Documentation discoverability

---

## Repository Bootstrap Requirements

### Doctrine Configuration

**When bootstrapping a repository** that uses the SDD Agentic Framework:

1. **Bootstrap Bill must create** `.doctrine-config/` directory in repository root
2. **Generate `config.yaml`** from `doctrine/templates/automation/doctrine-config-template.yaml`
3. **Configure path variables** to match the repository structure:
   - `workspace_root` (default: `work`) — Task orchestration workspace
   - `doc_root` (default: `docs`) — Documentation root
   - `spec_root` (default: `specifications`) — Specification files
   - `output_root` (default: `output`) — Generated artifacts
4. **Set repository metadata** (name, description, version)
5. **Enable tool integrations** based on detected tooling

**Rationale:** The `.doctrine/config.yaml` file provides local path overrides for the parameterized doctrine framework, enabling portability across repositories with different directory structures.

**Reference:** See `doctrine/DOCTRINE_MAP.md` for variable usage throughout framework files.

---

## Related Documentation

**Framework Guidelines:**
- [AGENTS.md](AGENTS.md) - Agent initialization and governance protocol
- [.github/agents/directives/](../.github/agents/directives/) - Directive catalog
- [.github/agents/approaches/](../.github/agents/approaches/) - Approach catalog

**Testing Guidelines:**
- [docs/styleguides/GENERIC_TESTING.md](docs/styleguides/GENERIC_TESTING.md) - General testing principles
- [docs/styleguides/FORMALIZED_CONSTRAINT_TESTING.md](docs/styleguides/FORMALIZED_CONSTRAINT_TESTING.md) - Contract testing patterns

**Workflow Documentation:**
- [work/collaboration/README.md](work/collaboration/README.md) - File-based orchestration
- [specifications/README.md](specifications/README.md) - Specification-driven development

---

**Maintained by:** Agentic Framework Core Team
**Review Cycle:** Quarterly or as needed
**Next Review:** 2026-05-01
