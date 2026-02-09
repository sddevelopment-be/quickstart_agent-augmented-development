# Repository-Specific Guidelines

_Version: 1.1.0_  
_Last updated: 2026-02-09_
_Format: Markdown protocol for agent initialization and governance_

---

These rules override any generic behaviour if there is a conflict.

## Domain Rules

- Never use production credentials.
- Respect privacy / anonymisation requirements.
- **Planning/documenting future work is NOT completion.** Only mark tasks complete after implementation, testing, and validation. Documenting next steps or creating follow-up tasks does not constitute completion of current work.

## Technical Constraints

- Target language: Python 3.10+, JavaScript/Node.js for tooling
- Preferred frameworks: pytest for testing, Flask for services
- Use TDD approach (Directive 017): Write tests first, implement to pass, refactor
- Follow ADR-documented architectural decisions

## Output Expectations

- Code style: Follow existing patterns, use type hints
- Documentation: Update ADRs for architectural decisions, maintain work logs per Directive 014
- Testing: Minimum 80% coverage on new code, all tests passing before completion
- File formats: YAML for configuration, Markdown for documentation
- **Distinguish clearly between "foundation complete" and "work complete"** - partial implementations should be documented as such with remaining work identified
