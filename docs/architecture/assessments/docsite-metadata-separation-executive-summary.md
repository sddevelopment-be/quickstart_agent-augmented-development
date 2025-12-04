# Executive Summary: Docsite Metadata Separation Architecture

**Status:** Feasibility Analysis  
**Date:** 2025-12-04  
**Prepared by:** Architect Alphonso

## Verdict: Conditional Adoption as Advanced Profile

The proposed architecture to separate static-site metadata from markdown content is **technically feasible but operationally complex**. Given that this repository's markdown files currently contain **no front matter**, the token-economy problem this pattern aims to solve does not yet exist. However, the architecture presents a **proactive defense** against future metadata pollution.

## Key Findings

**Token Economy Impact:** Minimal immediate benefit. Current files are clean. Future prevention is the primary value. Estimated token savings: 0% today, potentially 15-25% if front matter were added to 150+ files.

**Technical Feasibility:** High complexity. Symlinks pose cross-platform challenges (Windows requires developer mode or admin rights). Hugo can consume symlinked content, but metadata lookup mechanics require custom template logic and path-keying strategies with drift risk.

**Agent Workflow Benefits:** Mixed. Content-reading agents benefit from clean files. Metadata Curator Agent adds coordination overhead. Validation tooling becomes mandatory to prevent metadata-file mismatches.

**Repository Ergonomics:** Reduced for human contributors. Metadata separated from content breaks the single-file mental model. Onboarding complexity increases. Trade-off: agent efficiency vs. human discoverability.

**Recommendation:** Adopt as **optional advanced profile** for teams with high agent workload and tolerance for operational complexity. **Not recommended as default template baseline**. Baseline should remain front-matter-optional with clean content as the norm. Advanced users opt-in via documented setup.

## Strengths

- Future-proofs against front matter bloat
- Clean content remains generator-agnostic
- Metadata centralization enables bulk operations
- Logical separation of concerns (content vs. presentation)

## Risks

- **HIGH:** Symlink failures on Windows, JetBrains IDEs, some CI environments
- **HIGH:** Metadata drift when files renamed/moved without metadata update
- **MEDIUM:** Validation tooling becomes critical dependency
- **MEDIUM:** Increased cognitive load for new contributors
- **LOW:** Hugo template complexity, keying strategy fragility

## Next Steps

If proceeding with conditional adoption:

1. Prototype Hugo setup with symlinked content and external metadata
2. Test cross-platform symlink behavior (Windows, macOS, Linux, GitHub Actions)
3. Implement validation script for metadata-file synchronization
4. Document advanced profile setup in `docs/HOW_TO_USE/advanced-docsite-setup.md`
5. Create Docsite Curator Agent profile with metadata management responsibilities
6. Establish metadata drift detection in CI workflow

**Timeline:** 3-4 weeks for full implementation. 1 week for prototype validation.

---

_Related Documentation: [Full Feasibility Study](docsite-metadata-separation-feasibility-study.md) | [ADR-022](../adrs/ADR-022-docsite-separated-metadata.md) | [Risk Assessment](docsite-metadata-separation-risks.md)_
