# Tactic: Lexical Style Diagnostic

**Invoked by:**
- [Directive 015 (Store Prompts)](../directives/015_store_prompts.md)
- Shorthand: [`/lexical-analysis`](../shorthands/lexical-analysis.md)

---

## Intent

Perform lexical analysis on documentation to identify style inconsistencies, readability issues, and tone misalignments.

**Apply when:**
- Documentation feels inconsistent in voice/tone
- Readability improvements needed
- Preparing content for external audience
- Before major documentation release

---

## Execution Steps

### 1. Sentence Structure Analysis
- [ ] Identify overly complex sentences (>30 words)
- [ ] Check for passive voice overuse
- [ ] Detect excessive subordinate clauses

### 2. Tone Consistency Check
- [ ] Verify voice alignment with target audience
- [ ] Identify informal/formal mixing
- [ ] Check jargon appropriateness

### 3. Readability Scoring
- [ ] Calculate Flesch-Kincaid grade level
- [ ] Assess paragraph length distribution
- [ ] Check heading hierarchy consistency

### 4. Style Issue Identification
- [ ] Flag unclear pronouns (it, this, that without antecedent)
- [ ] Identify redundant phrases
- [ ] Check parallel structure in lists

### 5. Generate Recommendations
- [ ] Create minimal diff proposals
- [ ] Prioritize high-impact changes
- [ ] Preserve author's voice

---

## Outputs
- Lexical analysis report
- Style issues with recommendations
- Minimal diff proposals
- Readability metrics

---

**Status:** ✅ Active
