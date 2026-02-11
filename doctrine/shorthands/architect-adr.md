# Shorthand: architect-adr

**Alias:** `/architect-adr`  
**Category:** Architecture  
**Agent:** Architect Alphonso  
**Complexity:** High  
**Version:** 1.0.0  
**Created:** 2026-02-08

---

## Purpose

Quick command to bootstrap Architect Alphonso and draft a Proposed ADR (Architectural Decision Record) with trade-off analysis and impact assessment.

---

## Usage

```
/architect-adr
```

Or with parameters:
```
/architect-adr TITLE="WebSocket Technology Choice" \
  CONTEXT="Need real-time communication for dashboard" \
  OPTIONS="Flask-SocketIO, Native WebSockets, Server-Sent Events"
```

---

## Process

1. Clear context
2. Bootstrap as Architect Alphonso
3. Execute architectural analysis
4. Draft Proposed ADR with:
   - Context & problem statement
   - Decision rationale
   - Options analysis (trade-off matrix)
   - Envisioned consequences
   - Considered alternatives
   - Success metrics

---

## Required Inputs

- **Decision Title:** Brief, descriptive name
- **Problem Context:** Paragraph explaining the situation
- **Forces/Constraints:** Key factors influencing decision
- **Options:** Alternative approaches considered
- **Preferred Option:** Recommended choice

---

## Optional Inputs

- **Impact Areas:** performance, portability, maintainability, etc.
- **Related Artifacts:** paths to affected files/docs
- **Existing ADR References:** list of related ADRs
- **Risk Appetite:** low | medium | high
- **Time Horizon:** short | medium | long
- **Non-Functional Requirements:** security, scalability, etc.

---

## Output

- **ADR markdown file:** `docs/architecture/adrs/ADR-XXX-{slug}.md`
- **Option Impact Matrix:** Qualitative scores per option
- **Success Metrics:** Measurable acceptance criteria
- **Diff plan:** Cross-link updates for README index

---

## Constraints

- Decision section ≤ 120 words
- Each alternative: one sentence rejection reason
- Avoid speculative implementation details
- Ask clarifying questions if ambiguous

---

## Example

```
/architect-adr

Decision Title: WebSocket Technology Choice for Real-Time Dashboard
Problem Context: Dashboard requires real-time task updates. Need low-latency 
  bidirectional communication between server and browser clients.
Forces: Minimal setup overhead, CORS support, Python ecosystem
Options: Flask-SocketIO, Native WebSockets, Server-Sent Events
Preferred: Flask-SocketIO
Risk Appetite: medium
Time Horizon: medium (6-12 months)
```

**Output:** `ADR-NNN (technology choice)-websocket-technology-choice.md`

---

## Related

- **Tactic:** `doctrine/tactics/adr-drafting-workflow.tactic.md`
- **Template:** `doctrine/templates/prompts/ARCHITECT_ADR.prompt.md`
- **Directive 018:** Traceable Decisions
- **Agent Profile:** `doctrine/agents/architect.agent.md`

---

**Status:** ✅ Active  
**Maintained by:** Architect Alphonso  
**Last Updated:** 2026-02-08
