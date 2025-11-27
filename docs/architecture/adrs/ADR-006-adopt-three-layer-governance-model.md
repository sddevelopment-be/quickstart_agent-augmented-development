# ADR-006: Adopt Three-Layer Governance Model

> **Date:** 2025-11-22  
> **Status:** Accepted  
> **Date Accepted:** 2025-11-22  
> **Authors:** Architect Alphonso  
> **Supersedes:** None  
> **Depends On:** [ADR-001](./ADR-001-modular-agent-directive-system.md), [ADR-002](./ADR-002-portability-enhancement-opencode.md)  
> **Tags:** governance, layering, directives, portability

---
## 1. Context
Growth in agent specialization and directive complexity has introduced coupling between strategic vision artifacts, operational guidelines, and execution-level directives. ADR-001 established modular directives; ADR-002 emphasized portability. Without a stratified governance model, change control and version integrity are at risk, increasing semantic drift and reducing portability reliability.

## 2. Decision
Adopt a formal Three-Layer Governance Model:
1. **Strategic Layer:** Vision artifacts, high-stability principles, version governance, cross-cutting direction.
2. **Operational Layer:** Patterns, guidelines, reusable templates, specialization schemata.
3. **Execution Layer:** Concrete directives, agent capability manifests, validation rules.

All governed artifacts will include a mandatory metadata header:
```yaml
---
layer: strategic|operational|execution
version: <semantic or date-based>
status: active|deprecated|draft
owner: <role/persona>
review_cycle: <interval or event>
related_adrs: [ADR-001, ADR-007, ...]
portability: stable|guarded|internal
---
```
Logical (metadata) classification is adopted instead of physical directory restructuring (see ADR-008 rejection).

## 3. Rationale
- Clarifies authority boundaries (strategic changes require ADR; operational via review; execution via PR).
- Isolates higher-churn content (execution) from stability-critical artifacts (strategic).
- Enables differentiated validation rules and metrics (e.g., execution churn tolerance).
- Strengthens traceability: directives and profiles reference strategic intent explicitly.
- Facilitates portability by constraining unstable evolution points.

## 4. Options Considered
| Option | Description | Pros | Cons | Reason |
|--------|-------------|------|------|--------|
| Flat model (status quo) | Mixed artifacts in shared paths | Zero migration | Drift, unclear authority | Fails scaling needs |
| Two-layer model | Merge operational + execution | Simpler taxonomy | Blurs procedure vs directive | Insufficient separation |
| Tag-only approach | Metadata tags without formal layer semantics | Low effort | Discoverability issues, misuse risk | Lower clarity |
| Domain segmentation | Split by agent domain | Domain focus | Fragmented governance | Doesn’t address coupling |
| Three-layer model (chosen) | Distinct logical partitions + metadata | High clarity, traceability | Migration effort | Balanced trade-offs |

## 5. Implications
- Validation tooling extended to enforce layer-specific rules.
- Strategic artifacts gain stricter review and version bump requirements.
- Operational layer becomes home for reusable patterns and templates (no runtime directives).
- Execution layer changes expected to dominate churn metrics (>70% of edits).
- Documentation and onboarding updated to explain layers.

## 6. Trade-Off Analysis
| Aspect | Benefit | Cost | Net |
|--------|---------|------|-----|
| Governance rigor | Clear escalation & approval flow | Added metadata overhead | Positive |
| Portability | Stable strategic core | Added classification step | Positive |
| Scalability | Reduced coupling at scale | Initial contributor learning | Positive |
| DX (Developer Experience) | Predictable change surfaces | Extra header maintenance | Neutral/Positive |
| Review efficiency | Faster scope isolation | Transition period slowdown | Positive |

## 7. Risks
| Risk | Impact | Mitigation | Signal |
|------|--------|-----------|--------|
| Over-segmentation | Process fatigue | Keep only 3 layers; reject physical split (ADR-008) | Feedback volume |
| Metadata drift | Inaccurate layer tagging | Add validation script & CI gate | Validation failure rate |
| Contributor friction | Slower adoption | Provide Quickstart + examples | Onboarding time |
| Tooling complexity | False positives in CI | Phased rollout (warn → enforce) | CI noise metrics |
| Ambiguous ownership | Unapproved strategic edits | Require ADR reference for strategic changes | Commit message checks |
| Portability misalignment | Execution instability leaks upward | Churn monitoring & guardrails | Churn distribution reports |

## 8. Implementation Outline
1. Approve ADR-006; acknowledge ADR-008 rejection of physical restructure.
2. Add metadata headers (layer, version, status, owner) to existing governed artifacts.
3. Extend validation scripts: layer presence, allowed transitions, strategic-change ADR citation.
4. Update `AGENTS.md` and `docs/architecture/README.md` with layer mapping.
5. Generate logical layer classification index (report-only, not structural moves).
6. Pilot for 2 weeks; collect churn & validation signals.

## 9. Success Metrics
- 100% governed artifacts tagged with metadata header (layer + version) within 1 week.
- >70% of churn localized to execution layer by week 2.
- Strategic artifact review cycle time reduced vs baseline after first month.
- Zero untagged new artifacts merged after enforcement date.
- Validation false positive rate <5% after initial calibration.

## 10. Open Questions
1. Should agent profiles partially belong to operational layer when acting as templates?
2. Do we maintain a unified version ledger or per-layer ledgers?
3. Criteria for introducing a fourth “experimental” layer?
4. Standard review cycle interval for strategic layer (monthly vs quarterly)?
5. How to encode portability stability tiers (stable|guarded|internal) in CI decisions?

## 11. Alternatives for Future Revisit
- Introduce optional “experimental” layer if execution churn exceeds threshold.
- Adopt partial physical restructuring if logical tagging proves insufficient.
- Add per-layer semantic validation (e.g., strategic artifact dependency graph).

## 12. Status Change Protocol
- **Strategic layer change:** Requires new or updated ADR + version increment.
- **Operational change:** Standard PR review; may trigger minor version change.
- **Execution change:** Fast-path merge if validation passes; patch version increment optional.
- Deprecation: set `status: deprecated`, add `related_adrs` referencing replacement, archive after grace period.

## 13. References
- [`architectural_vision.md`](../architectural_vision.md)
- [`directive_system_architecture.md`](../design/directive_system_architecture.md)
- [ADR-001](./ADR-001-modular-agent-directive-system.md)
- [ADR-007](./ADR-007-portability-enhancement-opencode.md)
- [ADR-008](ADR-007-repository-restructuring-layer-separation.md) (Rejected physical restructuring)

---
Status: Accepted on 2025-11-22. Implementation proceeds with logical (metadata) classification; no physical directory changes.
