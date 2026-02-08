# Documentation Templates

This directory contains templates for documenting concepts, patterns, and audiences.

## Available Templates

### Pattern Template (`pattern-template.md`)
**Purpose:** Document operational patterns, practices, and organizational techniques using forces-based analysis.

**Key sections:**
- Problem Statement & Intent
- Solution approach
- Contextual Forces (Enablers/Deterrents)
- Rationale & Consequences
- Mitigation strategies
- Examples & Criticism

**When to use:** Describing proven approaches with contextual trade-offs (solutions with enablers and deterrents).

**Related:** Complements ADR template (decisions) and concept template (abstract ideas).

---

### Concept Template (`concept-template.md`)
**Purpose:** Document abstract ideas, theories, principles, and conceptual frameworks.

**Key sections:**
- Definition & Key Components
- Background (Origin, Application, Comparisons)
- Significance & Examples
- Misconceptions
- Practical Implications

**When to use:** Explaining foundational ideas, mental models, or theoretical concepts that underpin practices.

**Related:** Concepts explain *what* and *why* (ideas, principles). Practices explain *how* (application). For operational patterns, use pattern template.

---

### Audience Persona Template (`audience-persona-template.md`)
**Purpose:** Document target reader profiles to guide documentation tone, depth, and structure decisions.

**Key sections:**
- Overview & Core Motivations
- Desiderata (Information/Interaction/Support/Governance needs)
- Frustrations & Constraints
- Behavioral Cues
- Collaboration Preferences
- Measures of Success
- Narrative Summary

**When to use:** Creating content for a specific audience; ensuring documentation addresses reader needs systematically.

**Related:** See `doctrine/approaches/target-audience-fit.md` for workflow guidance.

---

## Example Personas

See `doctrine/examples/personas/` for reference implementations:

- **Emerging Developer** (`emerging-developer.md`) - Early-career engineers (0-2 years)
- **Technical Lead** (`technical-lead.md`) - Experienced hands-on leaders (5+ years)

These examples demonstrate how to fill out the persona template and provide documentation implications for each audience type.

---

## Template Coverage

The documentation template collection now provides:

| Template Type | Purpose | Complementary To |
|---------------|---------|------------------|
| **ADR** (architecture/) | Architectural decisions | Pattern template (practices) |
| **Pattern** (this dir) | Operational practices with forces | ADR (decisions), Concept (ideas) |
| **Concept** (this dir) | Abstract ideas and theories | Pattern (application), ADR (decisions) |
| **Persona** (this dir) | Target audience profiles | All templates (guides tone/depth) |

This comprehensive set enables systematic documentation across decisions, practices, concepts, and audiences.

---

## Usage Workflow

### 1. Pattern Documentation
```bash
# Copy template
cp doctrine/templates/documentation/pattern-template.md docs/patterns/new-pattern.md

# Fill out sections
# - Start with Problem Statement
# - Be honest about Enablers AND Deterrents
# - Include real examples
```

### 2. Concept Documentation
```bash
# Copy template
cp doctrine/templates/documentation/concept-template.md docs/concepts/new-concept.md

# Fill out sections
# - Precise definition first
# - Comparisons to related concepts
# - Bridge to practical implications
```

### 3. Audience Persona Creation
```bash
# Copy template
cp doctrine/templates/documentation/audience-persona-template.md docs/personas/new-persona.md

# Fill out sections
# - Base on research or real user feedback
# - Include behavioral cues (observable)
# - End with narrative summary
```

### 4. Target-Audience Fit Check
Before writing documentation:
1. Identify primary persona (1-2 personas max per document)
2. Review their Desiderata table
3. Write for their Communication Style
4. Validate against their Measures of Success

See `doctrine/approaches/target-audience-fit.md` for detailed workflow.

---

## Novel Contributions

### Forces-Based Pattern Template
**Origin:** Extracted from Penguin Pragmatic Patterns editorial taxonomy  
**Innovation:** Explicit Enablers/Deterrents section captures contextual forces systematically  
**Value:** Complements decision-focused ADRs with practice-focused pattern documentation

### Audience Persona Framework
**Origin:** UX practice applied to technical documentation  
**Innovation:** Behavioral Cues and Collaboration Preferences tailored for technical writers  
**Value:** Systematic reader empathy; agents can adapt tone/depth based on persona

### Concept vs Practice Distinction
**Origin:** Penguin editorial taxonomy  
**Clarity:** Concepts (what/why) vs Practices (how/when)  
**Value:** Helps writers choose appropriate template, prevents mixing abstraction levels

---

## Integration with Agents

**Writer-Editor Agent:**
- Uses persona Desiderata to guide content structure
- Adapts tone based on Collaboration Preferences
- Validates draft against persona's Behavioral Cues

**Reviewer Agent:**
- Checks pattern completeness (Enablers AND Deterrents present?)
- Validates concept clarity (Definition precise? Comparisons clear?)
- Assesses audience fit (Does tone match persona expectations?)

**Curator Agent:**
- Ensures pattern metadata consistency
- Validates cross-references between concepts and practices
- Maintains persona catalog updates

---

## Related Documentation

- **Architecture Decision Records:** `doctrine/templates/architecture/adr-template.md`
- **Target Audience Fit:** `doctrine/approaches/target-audience-fit.md`
- **Writer-Editor Agent:** `doctrine/agents/writer-editor.agent.md`
- **Reviewer Agent:** `doctrine/agents/reviewer.agent.md`

---

**Maintained by:** SDD Framework Contributors  
**Version:** 1.0.0  
**Last Updated:** 2026-02-08
