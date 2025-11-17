 # Agentic Setup Reassessment Report
Role: Curator Claire  
Date: 2025-11-17  
Scope: Core AGENTS.md, external directives (001–012), agent profiles, manifest, validation script

---
## 1. Executive Summary
The agentic configuration has successfully modularized governance and operational detail into a lean core plus a directive suite. Safety signaling, behavioral redundancy, and structural indexing are sound. Integrity and extensibility gaps remain around per‑directive versioning, hashing, and dynamic dependency loading. Validation coverage is good but can be extended to semantic and orphan checks. Tooling guidance is lightweight and needs install/fallback detail.

---
## 2. Structural Separation & Clarity
Strengths:
- Core `AGENTS.md` now minimal (12 sections) with Extended Directives Index.
- Directives numerically ordered (`001`–`012`) enabling deterministic load sequences.
- Agent profiles reference only relevant directives, reducing extraneous context.

Gaps:
- No composite meta-version (core + directive set) to track synchronized state.
- No explicit recovery flow if a directive becomes unavailable mid-session.

Recommendations:
- Introduce `core_version` and `directive_set_version` header in `AGENTS.md`.
- Add directive `014_integrity_checksums.md` documenting rehydration + mismatch remediation.

---
## 3. Consistency & Referencing
Strengths:
- Consistent zero-padded numbering; headings start with `# <code>` validated.
- Extended Directives Index mirrors manifest content.

Issues:
- Hard-coded `generated_at` timestamp in manifest risks staleness.
- Mixed hyphen/en-dash usage; unify style (ASCII hyphen for lists, en-dash for numeric ranges only).

Actions:
- Automate manifest regeneration (script) to refresh timestamp.
- Run a style normalization pass on directive prose.

---
## 4. Safety & Behavioral Guardrails
Strengths:
- Integrity markers (❗️ ⚠️ ✅) standardized and present in risk directive (011).
- Clarifying line redundancy preserved across agents plus COP directive (012).

Missing:
- Explicit maximum output size guidance to prevent token overflow.
- Fallback protocol if alignment validation cannot complete (e.g., tool failure).

Recommendation:
- Add size guardrails (suggest: soft cap ~800 tokens per single reasoning block, encourage chunking) in COP directive.
- Extend validation script to simulate alignment check placeholder.

---
## 5. Redundancy Justification
Current State:
- Clarifying line (“Ask clarifying questions when uncertainty >30%.”) purposely duplicated.
- Directive 012 lists duplication policy but lacks rationale.

Add:
- Paragraph in 012 explaining cognitive priming and defense against partial context loss.

---
## 6. Manifest Completeness
Strengths:
- Fields: code, slug, title, purpose, dependencies, requiredInAgents, safetyCritical.

Gaps:
- No per-directive version numbers.
- No checksum/hash for tamper detection.
- No deprecated/replaces semantics for future evolution.
- Dependencies logical but naive (no directionality validation).

Enhancements:
- Add `directive_version`, `checksum_sha256`, `status` (active|deprecated|pending), `replaces`.
- Provide generation script computing hashes and updating manifest.

---
## 7. Validation Tooling Coverage
Strengths:
- Sequencing, heading conformity, dependency file existence, index presence, clarifying line presence.
- Works with or without `jq`.

Limitations:
- No check for Purpose section existence.
- Does not detect orphan directives (never referenced by agents or index).
- Does not verify index ordering matches ascending code sequence.
- Hard-coded required clarifying line (fragile to punctuation change).

Extension Plan:
- Add regex check: `^# [0-9]{3}` + search for `Purpose:` substring.
- Orphan detection: grep directive codes across agent files / index.
- Compare index table line order with numeric ascending list.
- Externalize required behavior lines into manifest array `requiredLines`.

---
## 8. Tooling Instructions Adequacy (Directive 001)
Strengths:
- Lists core discovery and parsing tools (fd, rg, ast-grep, jq, yq, fzf).

Deficiencies:
- No install commands or version pins.
- No operational fallback (e.g., grep when rg absent, manual JSON parsing when jq absent).
- No performance guidelines (large repo search strategy).

Proposed Directive 013 (`tooling_setup.md`):
- Include install commands for Linux/macOS.
- Provide fallback tool matrix.
- Add minimal version recommendations.

---
## 9. Loading & Dependency Resolution
Current Loader:
- `load_directives.sh` concatenates specified directives; no dependency awareness.

Risks:
- Manual error if dependency omitted.
- Repeated loads could duplicate content silently.

Improvements:
- Add `--with-deps` flag that queries manifest (jq) to auto-append dependencies.
- Deduplicate loaded codes using a visited set.
- Option to output summary header listing loaded directives + versions + checksums.

---
## 10. Fragmentation & Resilience
Considerations:
- Multi-agent sessions rely on stable directive availability.
- Missing directive risk currently leads to validation fail (good) but not an operational fallback.

Mitigation:
- Add fallback directive mechanism: if directive missing, mark with ❗️ and load COP + Risk directives automatically.
- Document fallback in integrity checks directive (future 014).

---
## 11. Priority Recommendations
Critical (implement next):
1. Extend manifest: add per-directive version + checksum.
2. Add loader dependency resolution and deduplication.
3. Create tooling setup directive (013) with install/fallback guidance.

High:
4. Enhance validation: Purpose check, orphan detection, index order verification.
5. Output JSON validation report for CI integration (`validate_directives --json`).

Medium:
6. Add directive 014 for integrity & recovery protocol.
7. Add meta-version fields in `AGENTS.md` header (e.g., `Directive-Set-Version:`).
8. Add redundancy rationale subsection to 012.

Low:
9. Normalize dash usage & punctuation style.
10. Add alias mapping directive (015) with recommended shell functions.
11. Add linter for directive prose (e.g., no trailing whitespace, max line length).

---
## 12. Incremental Roadmap
Phase 1 (Integrity) – Critical items 1–3.  
Phase 2 (Validation) – Items 4–5.  
Phase 3 (Governance) – Items 6–8.  
Phase 4 (Polish) – Items 9–11.  
Phase 5 (Continuous Improvement) – Add CI integration, automated regeneration job.

---
## 13. Discrepancy Summary Table
| Area | Current | Gap | Recommendation |
|------|---------|-----|----------------|
| Manifest | Basic metadata | No version/checksum | Add version + SHA256 per directive |
| Loader | Manual list | No deps/dedup | Implement `--with-deps` + unique set |
| Validation | Structural basics | No Purpose/orphan/index order checks | Extend script with semantic checks |
| Tooling | Usage list | No install/fallback | Add directive 013 with install matrix |
| Safety | Markers present | No max output guidance | Add output size guidance to 012 |
| Recovery | Basic rehydration | No directive fallback | Add recovery flows in 014 |
| Redundancy | Clarifying line kept | No rationale doc | Add redundancy justification to 012 |
| Integrity | Single manifest version | No per-file versioning | Add directive_version & composite meta-version |

---
## 14. Sample Implementation Snippets (Future)
Manifest checksum sample field:
```
{
  "code": "001",
  "directive_version": "1.0.0",
  "checksum_sha256": "<hash>",
  ...
}
```
Loader enhancement pseudo-code:
```
codes=("$@")
if [[ $WITH_DEPS == 1 ]]; then
  for c in "${codes[@]}"; do
    deps=$(jq -r --arg c "$c" '.directives[]|select(.code==$c)|.dependencies[]?' manifest.json)
    codes+=("$deps")
  done
fi
# Deduplicate
unique=($(printf '%s
' "${codes[@]}" | sort -u))
```
Validation extension (orphan check):
```
for code in ${unique_codes}; do
  grep -R "require-directive ${code}" .github/agents || warn "Possible orphan: ${code}";
Done
```

---
## 15. Acceptance Criteria for Next Iteration
- Manifest includes directive_version & checksum for all entries.
- Validation script passes new semantic checks and emits JSON summary.
- Loader supports `--with-deps` and prevents duplicate loads.
- Tooling setup directive (013) created and indexed.
- Redundancy justification added to 012.

---
## 16. Final Notes
The current architecture is a strong foundation; proposed refinements focus on integrity, resilience, and developer ergonomics. Prioritizing manifest enrichment and loader intelligence will yield immediate reliability gains while keeping cognitive load low.

Prepared by: Curator Claire

