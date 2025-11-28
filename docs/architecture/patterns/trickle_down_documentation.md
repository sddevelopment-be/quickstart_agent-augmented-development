# Trickle-Down Documentation Pattern

**Pattern Type:** Documentation Structure  
**Context:** Technical documentation, agent directives, architectural documents  
**Version:** 1.0.0  
**Last Updated:** 2025-11-28

---

## Intent

Organize structured documents so that general overview information appears at the beginning (top-level headings), with increasingly detailed information revealed as the reader progresses through the document or descends into deeper heading levels.

## Motivation

Technical documentation often needs to serve multiple audiences with varying needs:
- Quick scanners who need high-level understanding
- Implementers who need specific procedural details
- Researchers who need comprehensive background

The trickle-down pattern ensures that:
1. Documents remain scannable for quick reference
2. Details are available but don't overwhelm initial comprehension
3. Information architecture mirrors the natural reading and discovery process
4. Navigation is intuitive (general → specific, abstract → concrete)

## Structure

```
# Title (H1)
  Brief purpose statement
  
  ## High-Level Concept (H2)
    General principle or overview
    
    ### Implementation Detail (H3)
      Specific guidance or example
      
      #### Edge Cases (H4)
        Nuanced considerations
```

## Application Rules

### Heading Hierarchy
- **H1 (Title):** Document name and immediate purpose
- **H2 (Sections):** Major conceptual divisions, broad topics
- **H3 (Subsections):** Specific implementations, detailed guidance
- **H4+ (Details):** Edge cases, technical notes, implementation specifics

### Content Organization
1. **Start general:** Begin each section with the broadest applicable concept
2. **Progress to specific:** Add detail progressively as headings descend
3. **Preserve context:** Each level should be understandable in isolation
4. **Avoid premature detail:** Don't explain implementation at overview level

### Example Pattern

```markdown
## Authentication System (H2 - General)
The system uses token-based authentication to secure endpoints.

### Token Generation (H3 - Specific)
Tokens are JWT-based with 24-hour expiration:
1. User credentials validated
2. Claims assembled
3. Token signed with HS256

#### Token Refresh Strategy (H4 - Detail)
Refresh tokens use a sliding window approach with...
```

## Anti-Patterns

### Depth Without Breadth
❌ **Bad:**
```markdown
## Authentication
### JWT Token Configuration
#### Signing Algorithm Selection
##### HMAC vs RSA Trade-offs
```

✅ **Good:**
```markdown
## Authentication
Brief overview of auth strategy

### Token-Based Approach
Why we chose tokens

### JWT Configuration
Implementation details
```

### Detail Before Context
❌ **Bad:**
```markdown
## Database
Configure connection string in appsettings.json with format:
"Server=...;Database=...;User Id=...;Password=..."
```

✅ **Good:**
```markdown
## Database
Uses PostgreSQL for persistent storage.

### Connection Configuration
Connection string format: "Server=...;Database=..."
Located in appsettings.json
```

### Flat Structure
❌ **Bad:** All content at same heading level, no hierarchical organization

✅ **Good:** Clear H2 → H3 → H4 progression with increasing detail

## Integration with Directives

When creating or updating agent directives:
1. Lead with purpose and core concept (H2)
2. Follow with quick decision tools or checklists (H2)
3. Descend into application guidance (H2 → H3)
4. End with integration notes and references (H2)

Example: See [Directive 020](../../.github/agents/directives/020_locality_of_change.md) for proper trickle-down structure.

## Benefits

- **Improved Scanability:** Readers can quickly assess relevance
- **Progressive Disclosure:** Information revealed at appropriate detail level
- **Better Navigation:** Clear hierarchy enables jump-to-section workflows
- **Reduced Cognitive Load:** Readers not overwhelmed by premature detail
- **Tool-Friendly:** IDEs and refactoring tools work better with clear structure

## Related Patterns

- **Progressive Enhancement:** Similar concept applied to user interfaces
- **Inverted Pyramid:** Journalism pattern (most important information first)
- **Information Architecture:** Broader discipline of content organization

---

**References:**
- Applied in: Agent directives, ADR templates, approach documents
- Related: [Agent Specialization Patterns](./agent_specialization_patterns.md)
