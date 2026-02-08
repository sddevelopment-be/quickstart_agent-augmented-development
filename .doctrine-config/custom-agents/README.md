# Custom Agents

**Purpose:** Repository-specific agent extensions that don't belong in the core framework.

---

## When to Add Custom Agents

Create custom agents here for:

- **Domain-specific expertise** (e.g., financial data validation, medical records processing)
- **Legacy system integration** (e.g., mainframe connectors, proprietary formats)
- **Project-unique workflows** (e.g., compliance reporting, vendor-specific protocols)

**Do NOT add:**
- General-purpose patterns → those belong in `doctrine/agents/`
- Temporary workarounds → document as technical debt instead
- Personal preferences → those stay out of version control

---

## Custom Agent Template

```yaml
# Example: data-analyst-dana.agent.yaml
name: "Data Analyst Dana"
slug: "data-analyst-dana"
role: "domain-specific"
specialization: "CSV validation and data quality checks for financial datasets"

extends: "analyst-annie"  # Inherit from framework agent (optional)

capabilities:
  - data-validation
  - csv-schema-inference
  - financial-data-quality
  - regulatory-compliance-checks

constraints:
  - must-validate-headers
  - must-check-numeric-precision
  - must-flag-outliers

hand_off_patterns:
  receives_from:
    - Backend Developer (raw CSV files)
  hands_off_to:
    - Quality Assurance (validation reports)
    - Architect (schema recommendations)

related_directives:
  - "016_atdd"           # Test-driven validation
  - "034_spec_driven"    # Validation specifications

tools:
  - pandas
  - great-expectations
  - csv-validator

initialization:
  mode: "analysis"
  context_required:
    - "CSV schema documentation"
    - "Regulatory requirements"
    - "Business rules for validation"
```

---

## Guidelines

1. **Extend, don't duplicate** - Inherit from framework agents when possible
2. **Document specialization clearly** - What makes this agent unique?
3. **Define hand-off patterns** - Who does this agent work with?
4. **Link to directives** - Which framework rules apply?
5. **List required tools** - What dependencies exist?

---

## Current Custom Agents

_(None yet - this is the template directory)_

---

**Maintained by:** Repository maintainers  
**Review when:** Adding domain-specific functionality
