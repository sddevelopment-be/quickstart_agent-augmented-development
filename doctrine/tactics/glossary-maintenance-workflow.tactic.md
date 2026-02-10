# Tactic: Glossary Maintenance Workflow

**Version:** 1.0.0  
**Date:** 2026-02-10  
**Status:** Active  
**Source:** Extracted from Living Glossary Practice Approach

---

## Purpose

Provide step-by-step procedures for maintaining a living glossary through continuous capture, regular triage, and periodic governance reviews.

---

## When to Use

Use this tactic when implementing or operating a living glossary system. Follow these procedures after initial glossary setup (see [Terminology Extraction and Mapping](terminology-extraction-mapping.tactic.md)) to maintain glossary quality over time.

**Prerequisites:**
- Glossary infrastructure exists (`.contextive/contexts/` or equivalent)
- Context owners identified and assigned
- Enforcement tiers defined (advisory, acknowledgment, hard failure)
- Agent observation system configured (optional but recommended)

---

## Procedure

### Step 1: Continuous Capture (Ongoing)

**Frequency:** Ongoing, automated observation

**Activities:**
1. **Configure agent observation:**
   - Set up automated monitoring of code commits, documentation changes, PRs
   - Optional: Meeting transcription and terminology extraction
   - Optional: Slack/Teams channel monitoring for domain terms

2. **Pattern detection:**
   - Identify new domain terms appearing in artifacts
   - Detect terminology conflicts (same term, different definitions)
   - Flag deprecated terms still in use
   - Identify terms lacking glossary definitions

3. **Generate candidates:**
   - Create proposed glossary entries with:
     - Term name
     - Preliminary definition (extracted from context)
     - Source references (file, line, author, date)
     - Suggested bounded context assignment
     - Confidence level (high/medium/low)

4. **Queue for review:**
   - Add candidates to triage backlog
   - Group related terms together
   - Prioritize by usage frequency and conflict severity

**Output:** Glossary candidates queue (e.g., `work/glossary-candidates/pending/`)

**Responsible:** Automated agents (Lexical Larry, Curator Claire) + observability tooling

---

### Step 2: Weekly Triage (Weekly 30-minute session)

**Frequency:** Weekly, scheduled meeting

**Participants:**
- Context owners (mandatory)
- Architects (recommended)
- Domain experts (as needed)
- Agent coordinators (optional)

**Agenda:**

**2.1 Review Candidate Queue (15 min)**
1. **Examine agent-generated proposals:**
   - Review term name, proposed definition, sources
   - Check for conflicts with existing terms
   - Validate context assignment

2. **Make decisions for each candidate:**
   - **Approve:** Add to glossary as-is or with edits
   - **Reject:** Not a domain term, too technical, out of scope
   - **Defer:** Needs more research, stakeholder input, or usage data
   - **Merge:** Consolidate with existing term

**2.2 Assign Enforcement Tiers (10 min)**
For approved terms, assign tier:
- **Advisory:** New terms, style preferences, emerging patterns
- **Acknowledgment Required:** Deprecated terms, cross-context usage, known conflicts
- **Hard Failure:** Banned terms, critical violations, security risks

**2.3 Update Glossary (5 min)**
1. **Commit changes:**
   - Add new entries to appropriate context file (`.contextive/contexts/[context].yml`)
   - Include decision rationale in commit message
   - Tag with decision date and approver

2. **Update decision history:**
   - Document alternatives considered
   - Record owner approval
   - Note enforcement tier justification

**Output:** Updated glossary files, decision log

**Responsible:** Context owners (decision authority), Curator Claire (facilitation)

---

### Step 3: Quarterly Health Check (Quarterly 2-hour workshop)

**Frequency:** Quarterly (every 3 months)

**Participants:**
- All context owners (mandatory)
- Architects (mandatory)
- Domain experts (recommended)
- Development team leads (recommended)

**Agenda:**

**3.1 Staleness Audit (30 min)**
1. **Identify outdated definitions:**
   - Review terms unchanged in >6 months
   - Check if definitions match current implementation
   - Validate with recent code/docs

2. **Update or deprecate:**
   - Revise definitions to match reality
   - Mark deprecated if term no longer used
   - Add "superseded by" links if replaced

**3.2 Coverage Assessment (30 min)**
1. **Missing domain terms analysis:**
   - Review recent PRs for undocumented terms
   - Survey developers: "What terms confuse you?"
   - Compare codebase terminology to glossary

2. **Gap closure plan:**
   - Prioritize missing terms by usage frequency
   - Assign owners to define high-priority terms
   - Set target: Add X terms before next check

**3.3 Conflict Resolution (30 min)**
1. **Address ambiguities:**
   - Review terms with multiple definitions
   - Identify cross-context collisions
   - Facilitate disambiguation discussion

2. **Define translation rules:**
   - Document term mappings at context boundaries
   - Create Anti-Corruption Layer (ACL) specifications
   - Update context map with relationships

**3.4 Enforcement Review (30 min)**
1. **Assess tier appropriateness:**
   - Review hard failure justifications: Still necessary?
   - Check acknowledgment patterns: Too many suppressions?
   - Evaluate advisory effectiveness: Helping or noise?

2. **Adjust enforcement:**
   - Promote terms to higher tier if critical
   - Demote terms if causing friction
   - Remove deprecated terms from checks

**Output:** Glossary refinement plan, enforcement adjustments, coverage metrics

**Responsible:** Architect Alphonso (facilitation), Context owners (decisions)

---

### Step 4: Annual Governance Retrospective (Annual half-day session)

**Frequency:** Annual (once per year)

**Participants:**
- Context owners (mandatory)
- Senior architects (mandatory)
- Engineering leadership (recommended)
- Product leadership (recommended)

**Agenda:**

**4.1 Hard Failure Justification Review (60 min)**
1. **Review each hard failure rule:**
   - Why was it created?
   - How often was it triggered?
   - Were exceptions justified?
   - Still necessary?

2. **Policy updates:**
   - Remove obsolete hard failures
   - Document rationale for keeping remaining rules
   - Establish criteria for adding new hard failures

**4.2 False Positive Analysis (60 min)**
1. **Agent accuracy assessment:**
   - Calculate false positive rate (incorrect flagging)
   - Identify patterns in agent mistakes
   - Review suppression frequency per developer

2. **Improve detection quality:**
   - Tune confidence thresholds
   - Add register variation awareness (technical vs. user-facing)
   - Update agent prompts/instructions

**4.3 Organizational Alignment (60 min)**
1. **Conway's Law validation:**
   - Map current team structure to context boundaries
   - Identify misalignments (teams split across contexts, contexts split across teams)
   - Discuss organizational changes

2. **Boundary adjustment plan:**
   - Propose context mergers/splits to align with teams
   - Define transition timeline
   - Assign migration ownership

**4.4 Tooling Evolution (60 min)**
1. **Retrospective discussion:**
   - What worked well this year?
   - What caused friction?
   - What would improve workflow?

2. **Improvement backlog:**
   - Prioritize tooling enhancements
   - Evaluate new glossary technologies
   - Plan training or process changes

**Output:** Governance policy updates, process improvements, tooling roadmap

**Responsible:** Manager Mike (facilitation), Engineering leadership (approval)

---

## Success Criteria

✅ **Workflow is effective when:**
- Weekly triage completes in <30 minutes consistently
- Candidate backlog never exceeds 20 items
- Quarterly health checks identify <10% stale definitions
- Annual retrospectives produce <5 high-priority action items
- Developer surveys show >75% find process helpful (not burdensome)

---

## Common Pitfalls

### Pitfall 1: Skipping Weekly Triage
**Symptom:** Candidate backlog grows to 50+ items, becomes overwhelming  
**Solution:** Protect 30-minute timeslot, cancel other meetings first. If consistently overrunning, increase frequency to 2x/week temporarily.

### Pitfall 2: No Clear Ownership
**Symptom:** Triage discussions become debates without decisions  
**Solution:** Assign single "decider" per bounded context. Others advise, but owner has final authority.

### Pitfall 3: Enforcement Creep
**Symptom:** Too many hard failures, developers resent glossary  
**Solution:** Reserve hard failures for security/compliance only. Default to advisory. Review justifications quarterly.

### Pitfall 4: Tooling Obsession
**Symptom:** Spending more time on tools than glossary content  
**Solution:** Start simple (YAML files + grep). Add tooling only when manual process scales poorly.

---

## Related Documentation

### Related Approaches
- **[Living Glossary Practice](../approaches/living-glossary-practice.md)** - Strategic rationale (WHY)
- **[Language-First Architecture](../approaches/language-first-architecture.md)** - Architectural context

### Related Tactics
- **[Terminology Extraction and Mapping](terminology-extraction-mapping.tactic.md)** - Initial glossary creation
- **[Context Boundary Inference](context-boundary-inference.tactic.md)** - Organizational analysis

### Related Directives
- **[Directive 038: Ensure Conceptual Alignment](../directives/038_ensure_conceptual_alignment.md)** - Term confirmation protocol

---

## Version History

- **1.0.0** (2026-02-10): Initial version extracted from Living Glossary Practice approach

---

**Curation Status:** ✅ Claire Approved (Doctrine Stack Compliant - Procedural content properly placed in Tactics layer)
