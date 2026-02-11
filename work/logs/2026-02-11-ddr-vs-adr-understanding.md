# Understanding: DDR vs ADR Distinction

**Date:** 2026-02-11  
**Context:** Clarifying terminology per Human In Charge feedback

---

## Decision Hierarchy Clarification

### Doctrine Decision Records (DDR-NNN)

**Purpose:** Framework-level decisions that ship with `doctrine/`

**Characteristics:**
- Universal patterns applicable across repositories
- Part of doctrine framework itself
- Portable with doctrine when distributed
- Examples: Primer execution pattern, Guardian agent pattern, Doctrine stack layers

**Location:** `doctrine/decisions/DDR-NNN-*.md`

**Scope:** ONLY decisions about doctrine framework concepts, patterns, and governance

---

### Architecture Decision Records (ADR-NNN)

**Purpose:** Repository-specific implementation decisions

**Characteristics:**
- Specific to this repository's architecture
- Include: tools, applications, distribution mechanisms, local implementations
- NOT portable with doctrine framework
- Examples: Distribution tooling, export formats, CI pipeline, local module structure

**Location:** `docs/architecture/adrs/ADR-NNN-*.md`

**Scope:** Decisions about THIS repository's implementation, including how doctrine is packaged/distributed

---

## Key Distinction (Human In Charge Clarification)

> "Distribution of the doctrine is not an integral part of the doctrine itself, so it should be captured in the ADRs of this repository (which is scoped to contain the `doctrine` as well as supporting tools/applications/flows)."

**Interpretation:**
- **Doctrine content** (directives, approaches, tactics) = DDRs
- **Tooling around doctrine** (how we export, distribute, package) = ADRs
- **This repository** contains BOTH doctrine AND supporting tools

**Example:**
- ❌ WRONG: "How to zip doctrine for distribution" → DDR (NO - this is tooling)
- ✅ CORRECT: "How to zip doctrine for distribution" → ADR (YES - this is about distribution tooling)
- ✅ CORRECT: "Framework Guardian role definition" → DDR (YES - this is about doctrine pattern)

---

## Violations from Claire's Audit

**Previously suggested as DDRs (Framework Decisions):**
- ADR-011 (Primer Execution) → Could be DDR-001
- ADR-013 (Zip Distribution) → **STAYS as ADR** (distribution is tooling, not doctrine)
- ADR-014 (Framework Guardian) → Could be DDR-002

**Corrected Understanding:**
- ADR-013 MUST stay as ADR (distribution mechanism is repository tooling)
- Only move decisions about doctrine CONCEPTS to DDRs
- Distribution, export, CI, tooling → Always ADRs

---

## Impact on Remediation

**Claire's report suggested:**
> "Some ADRs are framework-level (ADR-011, ADR-013, ADR-014), creating circular dependencies"

**Correction:**
- ADR-011 (Primer Execution) → Could move to DDR-001 (doctrine concept)
- ADR-013 (Zip Distribution) → STAYS as ADR-013 (tooling/distribution)
- ADR-014 (Framework Guardian) → Could move to DDR-002 (doctrine role pattern)

**Action:**
- Create DDR structure for doctrine concepts ONLY
- Keep all distribution/tooling decisions as ADRs
- Update directives to reference DDRs for concepts, ADRs for implementation

---

## Validation Criteria

**Is this a DDR?**
- ✅ Defines a doctrine concept, pattern, or governance principle
- ✅ Applies universally across any repository using doctrine
- ✅ Would ship with doctrine framework
- ❌ NOT about how we build/distribute/package/export

**Is this an ADR?**
- ✅ Specific to this repository's implementation
- ✅ About tooling, CI, distribution, local architecture
- ✅ Includes module structure decisions (src/domain, etc.)
- ✅ Technology choices for repository infrastructure

---

**Status:** Understanding confirmed, ready to implement DDR structure with correct scope
