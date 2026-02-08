# Persona: Emerging Developer

**Example audience persona for technical documentation targeting early-career engineers.**

---

## Persona: Emerging Developer

### Overview

> **Purpose:** Early-career engineers (0-2 years) integrating into professional development teams.

- **Role Focus:** Feature implementation and technical skill development
- **Primary Function:** Deliver assigned work while absorbing architecture, practices, and collaboration norms
- **Environment / Context:** Cross-functional teams with mentorship available but limited; hybrid or remote work common

---

### Core Motivations

- **Professional Drivers:** Build credibility through reliable delivery; understand decision rationale; accelerate learning curve
- **Emotional or Cognitive Drivers:** Curious and cautious; seeks psychological safety to ask foundational questions without judgment
- **Systemic Positioning:** Dependent contributor with potential to become future multiplier if guided effectively

---

### Desiderata

| Category    | Expectation / Need        | Description                                                        |
|-------------|---------------------------|--------------------------------------------------------------------|
| Information | Clear, jargon-light primers| Needs concise explanations with examples mirroring real work       |
| Interaction | Structured feedback loops | Weekly check-ins, code review rituals, pairing opportunities       |
| Support     | Self-serve references     | Cheatsheets, glossaries, and templates for common deliverables     |
| Governance  | Transparent expectations  | Wants criteria for "good" pull requests, testing, documentation    |

---

### Frustrations and Constraints

- **Pain Points:** Context fragmentation—different seniors offer conflicting guidance; unclear priority between learning and delivery
- **Trade-Off Awareness:** Must balance speed of learning with delivery pressure; tension between asking questions and appearing competent
- **Environmental Constraints:** Limited ownership rights; dependent on tooling access, permissions, and approvals

---

### Behavioral Cues

| Situation            | Typical Behavior                       | Interpretation                                      |
|----------------------|----------------------------------------|------------------------------------------------------|
| Stable / Routine     | Follows checklists, documents discoveries | Building muscle memory through repetition          |
| Change / Uncertainty | Pauses, seeks clarification via chat   | Needs framing before acting; fear of breaking things |
| Under Pressure       | Tunnels on tasks, forgets to broadcast | Requires reminders to surface blockers early        |

---

### Collaboration Preferences

- **Decision Style:** Looks for precedent; prefers concrete examples over abstract principles
- **Communication Style:** Async messages plus occasional pairing; appreciates annotated code reviews with rationale
- **Feedback Expectations:** Actionable, kind, and specific; aware of growth areas but needs prioritization guidance

---

### Measures of Success

| Dimension   | Indicator                                | Type                        |
|-------------|------------------------------------------|-----------------------------|
| Performance | Stories delivered with fewer reworks     | Quantitative (rework rate)  |
| Quality     | Tests/docs included without prompting    | Qualitative (review notes)  |
| Growth      | Increased autonomy per sprint            | Developmental (scope size)  |

---

### Cross-Context Adaptation

| Domain    | Specific Focus       | Adaptation Notes                                         |
|-----------|----------------------|----------------------------------------------------------|
| Technical | Feature delivery     | Uses primers/practices to clarify architecture expectations |
| Service   | Internal upskilling  | Shares lessons with fellow juniors to reinforce learning   |

---

### Narrative Summary

A developer learning how systems and people fit together. They open documentation when a term shows up in stand-up, when preparing for design reviews, or when trying to justify a testing approach without yet having the vocabulary. They value clear examples over theory and appreciate when documentation acknowledges common mistakes without judgment.

---

### Metadata

| Field                 | Value                                           |
|-----------------------|-------------------------------------------------|
| **Persona ID**        | `emerging-developer-001`                        |
| **Created / Updated** | `2026-02-08`                                    |
| **Domain / Context**  | Generic software development (any tech stack)   |
| **Linked Artifacts**  | Python conventions, VCS hygiene, testing guides |

---

## Documentation Implications

**When writing for Emerging Developers:**

- **Tone:** Clear, neutral, patient. Avoid assuming prior knowledge; define terms inline.
- **Structure:** Step-by-step instructions with examples. Show before explaining theory.
- **Examples:** Use realistic scenarios from production work, not toy problems.
- **Depth:** Start shallow; link to deeper material for "why" questions.
- **Anti-patterns:** Highlight common mistakes explicitly (they haven't seen them yet).
- **Validation:** Provide checklists or self-assessment criteria.

**Content priorities:**
1. "How do I..." guides (high value)
2. Common pitfalls with fixes (high value)
3. Setup/configuration instructions (essential)
4. Architecture overviews (medium value - needs simplification)
5. Theoretical foundations (low value until they're ready)
