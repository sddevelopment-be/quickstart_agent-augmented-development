# ADR-002: Adopt OpenCode Specification for Agent Portability

**status**: `Accepted`  
**date**: 2025-11-22

### Context

The agent-augmented development repository aims to maximize the portability, reusability, and automation-readiness of its agent stack. Previously, agent configurations were maintained in markdown files with YAML frontmatter, which limited interoperability, validation, and integration with external tools. As the number of specialized agents grew, the need for a vendor-neutral, schema-validated, and automation-friendly configuration format became critical. This decision is made in the context of ongoing efforts to standardize agent specialization patterns ([agent_specialization_patterns.md](../patterns/agent_specialization_patterns.md)) and to support robust CI/CD workflows.

### Decision

We will adopt the OpenCode specification as the canonical format for agent configuration. All agent profiles will be converted to OpenCode-compliant JSON, and validation/conversion tooling will be integrated into the repository's automation pipeline. Markdown-based agent files will be retained for human readability but will be considered secondary to the OpenCode source of truth.

### Rationale

- **Portability:** OpenCode is a vendor-neutral, widely supported format, enabling agent configurations to be shared and reused across projects and platforms.
- **Validation:** Schema-based validation ensures configuration integrity and reduces the risk of runtime errors.
- **Automation:** JSON-based configuration is easily consumed by CI/CD pipelines, validation scripts, and external tools.
- **Extensibility:** OpenCode supports future enhancements and can accommodate new agent capabilities without breaking existing workflows.
- **Alignment:** This approach aligns with the repository's architectural vision and specialization patterns, supporting clear boundaries and handoff protocols between agents.

### Envisioned Consequences``

- **Positive:**
  - Improved agent portability and reusability
  - Automated validation and conversion in CI/CD
  - Reduced configuration errors and onboarding friction
  - Easier integration with external tools and platforms
  - Consistent, schema-driven agent definitions
- **Negative:**
  - Initial migration effort for existing agent files
  - Need to maintain both markdown and JSON representations (until full migration)
  - Potential learning curve for contributors unfamiliar with OpenCode

### Considered Alternatives

- **Continue using markdown/YAML only:**
  - Rejected due to lack of schema validation, limited automation, and poor interoperability.
- **Adopt a proprietary or less common format:**
  - Rejected due to vendor lock-in and reduced community support.
- **Manual validation and conversion:**
  - Rejected due to high maintenance burden and risk of human error.

---

_References:_
- [Agent Specialization Patterns](../patterns/agent_specialization_patterns.md)
- [OpenCode Specification Validator](../../../ops/scripts/opencode-spec-validator.py)
- [Agent to OpenCode Converter](../../../ops/scripts/convert-agents-to-opencode.py)


