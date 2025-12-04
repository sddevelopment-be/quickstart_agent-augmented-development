# ADR-022: Docsite Separated Metadata Architecture

**status**: `Accepted`  
**date**: 2025-12-04  
**supersedes**: None  
**related**: ADR-001 (Modular Directives), ADR-008 (File-Based Coordination), ADR-017 (Traceable Decisions)

## Context

### The Documentation Rendering Challenge

This repository serves as a quickstart template for agent-augmented development workflows. As the documentation grows (currently 124 files in `docs/`, 72 in `.github/agents/`), the need for a professional documentation website (docsite) becomes apparent for improved discoverability, navigation, and presentation.

Static site generators (Hugo, Jekyll, MkDocs) typically require **front matter** (YAML/TOML metadata blocks) at the beginning of each markdown file to control:
- Page title and description
- Tags and categories
- Navigation weight and menu placement
- Section and hierarchy
- Custom rendering parameters

### Current State: Clean Markdown Files

**Critical observation:** The repository's markdown files **currently contain no front matter**. Files are clean, semantic content only—no YAML blocks, no metadata pollution. This aligns well with the repository's emphasis on token economy (ADR-001) and agent readability.

### The Token Economy Dilemma

Front matter introduces token overhead when agents read documentation:

**Hypothetical scenario if front matter were added:**
- Typical front matter: 5-15 lines (~100-300 tokens)
- 196 total markdown files × 200 tokens average = **~39,200 tokens**
- Agents re-reading files: Curator (~30 files/session), Architect (~15 files/session), Writer (~10 files/session)
- Token cost per session:
  - Curator: 6,000 tokens (~5-7% of 100K context window)
  - Architect: 3,000 tokens (~3%)
  - Writer: 2,000 tokens (~2%)

While not catastrophic, this represents **cumulative overhead** that compounds over hundreds of agent interactions.

### The Portability and Maintainability Concern

Front matter couples content to specific static site generators:
- **Hugo:** TOML or YAML front matter with Hugo-specific fields
- **Jekyll:** YAML front matter with Jekyll-specific fields
- **MkDocs:** No front matter; uses `mkdocs.yml` navigation structure
- **Docusaurus:** JS-based sidebar configuration

Metadata changes (retagging, reorganization) require editing dozens of files. This creates maintenance friction and increases risk of inconsistency.

### The Agent Specialization Opportunity

The repository's multi-agent architecture (ADR-001, ADR-008) creates an opportunity:
- **Content-reading agents** (Architect, Writer, Researcher) benefit from clean markdown
- **Metadata-managing agents** (Docsite Curator) can operate on centralized metadata
- **Separation of concerns** aligns with agent specialization pattern

### Problem Statement

**Should we adopt a separated metadata architecture proactively, preventing front matter pollution before a docsite is implemented, or should we accept standard front matter when/if a docsite is added?**

Forces to balance:
1. **Token economy:** Minimize agent context overhead
2. **Maintainability:** Centralize metadata for bulk operations
3. **Portability:** Keep content generator-agnostic
4. **Human ergonomics:** Preserve familiar patterns for human contributors
5. **Operational complexity:** Avoid premature optimization
6. **Template mission:** Keep quickstart simple and approachable

## Decision

**We will adopt separated metadata architecture as an OPTIONAL ADVANCED PROFILE, not as the default template baseline.**

Specifically:

### 1. Default Template Behavior

- Markdown files in `docs/` and `.github/agents/` **remain clean** (no front matter)
- No docsite configuration included in base template
- Users who add a docsite may choose standard front matter OR separated metadata

### 2. Advanced Profile: Separated Metadata

For teams with **high agent workload** and **tolerance for operational complexity**, provide documented advanced setup:

**Architecture:**
- Clean markdown files in `docs/` and `.github/agents/` (no changes to source)
- Centralized metadata in `docs-site/data/docmeta.yaml` (keyed by relative file path)
- Symlinks (or copies on Windows) from source directories into `docs-site/content/`
- Hugo configured with `followSymlinks: true` and custom templates for metadata lookup
- Validation script (`validation/validate-docsite-metadata.py`) to detect metadata drift
- **Docsite Curator Agent** profile to manage metadata integrity

**Keying Strategy:**
```yaml
# docs-site/data/docmeta.yaml
docs/architecture/adrs/ADR-022-docsite-separated-metadata.md:
  title: "ADR-022: Docsite Separated Metadata"
  tags: ["architecture", "decision", "docsite"]
  weight: 22
  section: "ADRs"
  menu:
    main:
      parent: "architecture"
```

**Hugo Template Pattern:**
```go-template
{{ $relPath := strings.TrimPrefix "content/" .File.Path }}
{{ $metadata := index .Site.Data.docmeta $relPath }}
<h1>{{ $metadata.title | default .Title }}</h1>
```

### 3. Implementation Scope

**Included in base template:**
- Documentation explaining both standard and separated approaches
- Reference implementation guide in `docs/HOW_TO_USE/advanced-docsite-setup.md`
- Link to example repository demonstrating separated metadata pattern

**NOT included in base template:**
- No pre-configured Hugo setup
- No `docs-site/` directory structure
- No `docmeta.yaml` file
- No Docsite Curator Agent (provided as optional profile)

**Rationale for opt-in approach:**
- Preserves template simplicity for new users
- Avoids premature optimization (many users may not add docsite)
- Advanced users can adopt pattern when benefits justify complexity
- Documentation ensures pattern is accessible without making it mandatory

## Rationale

### Why Optional, Not Mandatory?

**Problem severity is LOW today:**
- Current markdown files contain no front matter
- Token economy problem is hypothetical, not actual
- No immediate pain to solve

**Operational complexity is HIGH:**
- Symlinks fail on Windows without Developer Mode
- Metadata drift requires validation tooling
- Custom Hugo templates incompatible with standard themes
- Cognitive overhead for new contributors

**Template mission favors simplicity:**
- Base template should be approachable for newcomers
- Advanced patterns should be opt-in, not default
- Complexity justified only when benefits realized

**Verdict:** Making separated metadata the default would be **premature optimization** that increases onboarding friction without addressing a current problem.

### Why Provide It at All?

**Future-proofing value:**
- Teams adopting this template may eventually add docsite
- Separated metadata prevents front matter pollution proactively
- Pattern documented and validated once, reusable by many

**Agent workflow benefits are REAL for high-frequency use:**
- Content-reading agents benefit from clean files
- Metadata Curator Agent enables specialized management
- Token savings modest but meaningful over time (2-7% per session)

**Aligns with existing architecture:**
- Separation of concerns (content vs. metadata) matches agent specialization (ADR-001)
- File-based coordination (ADR-008) extends to metadata management
- Traceable decisions (ADR-017) apply to metadata governance

**Verdict:** Pattern has legitimate value for subset of users; documentation ensures accessibility.

### Why Relative Path Keying?

**Alternatives considered:**
1. **Filename only:** Risk of collisions (same filename in different directories)
2. **Unique IDs:** Opaque, requires ID registry, poor human readability
3. **Content hashes:** Breaks on content changes, extremely opaque

**Relative path keying chosen because:**
- Intuitive and human-readable
- Matches filesystem structure
- Easy to maintain with validation tooling
- Drift detectable via automated checks

**Trade-off accepted:** File renames break keying, but validation script detects and validation/migration script can fix in bulk.

### Why Symlinks Instead of Copies?

**Symlinks preferred:**
- Changes to source files immediately reflected in docsite content
- No sync overhead or script needed
- Git tracks single source of truth

**Copies as fallback (Windows):**
- Windows symlink support unreliable without Developer Mode
- Provide `sync-docs.sh` script for one-way sync
- Document as platform-specific workaround

**Trade-off accepted:** Windows users have degraded experience; fallback available.

### Why Hugo as Reference Implementation?

**Alternatives considered:**
- **Jekyll:** Ruby dependency, slower builds, declining popularity
- **MkDocs:** Python-based, simple but limited customization
- **Docusaurus:** Modern, React-based, but heavy and opinionated

**Hugo chosen because:**
- Single binary, no runtime dependencies
- Fast builds (seconds for hundreds of pages)
- Flexible templating with Go templates
- Active community, extensive themes
- Supports `followSymlinks` configuration

**Trade-off accepted:** Go template syntax has learning curve; alternatives viable with pattern adaptation.

## Envisioned Consequences

### Positive

- ✅ **Prevents future token overhead:** Proactive defense against front matter pollution (15-25% savings if baseline were front matter)
- ✅ **Preserves content portability:** Markdown files remain generator-agnostic
- ✅ **Enables centralized metadata management:** Bulk operations (retagging, reorganization) simplified
- ✅ **Aligns with agent specialization:** Content agents read clean files; curator manages metadata
- ✅ **Optional adoption reduces risk:** Advanced users opt-in; newcomers unaffected
- ✅ **Documented pattern reusable:** Other projects can adopt with guidance
- ✅ **Maintains template simplicity:** Base template remains approachable

### Negative (Accepted Trade-Offs)

- ⚠️ **Implementation complexity for adopters:** Symlinks, custom templates, validation tooling required (~3-4 weeks setup)
- ⚠️ **Platform compatibility challenges:** Windows users need fallback to copies; JetBrains IDEs need configuration
- ⚠️ **Metadata drift risk:** File renames break keying without validation; tooling becomes mandatory dependency
- ⚠️ **Two-location editing overhead:** Humans edit content in `docs/`, metadata in `docs-site/data/docmeta.yaml`
- ⚠️ **Hugo theme incompatibility:** Standard themes require modification; limits theme ecosystem
- ⚠️ **Validation maintenance burden:** Metadata validation script requires ongoing maintenance (~4 hours/quarter)
- ⚠️ **Learning curve for new contributors:** Non-standard pattern requires explanation (~1-2 hours training)

### Neutral

- ↔️ **Docsite adoption remains optional:** Users can choose standard front matter, separated metadata, or no docsite
- ↔️ **Pattern applicability varies:** High value for agent-heavy workflows; marginal for human-centric repos
- ↔️ **Documentation maintenance:** Advanced setup guide requires upkeep but benefits many users

## Considered Alternatives

### Alternative 1: Mandatory Separated Metadata in Base Template

**Description:** Include `docs-site/` directory with separated metadata in base template; all users adopt by default.

**Rejected because:**
- Increases template complexity significantly
- Many users may never add docsite (wasted setup)
- Premature optimization—problem doesn't exist today
- Onboarding friction discourages adoption
- Violates "keep it simple" template design principle

**When to revisit:** If 80%+ of template users report adding docsite AND suffering from front matter overhead.

### Alternative 2: Standard Front Matter (Status Quo)

**Description:** When docsite added, use traditional front matter in markdown files; accept token overhead.

**Rejected because:**
- Tokens overhead is cumulative and permanent
- Front matter pollution reduces content portability
- Metadata maintenance overhead high (edit many files)
- Misses opportunity to align with agent specialization

**Accepted for default:** Remains viable option for users who choose simplicity over optimization.

### Alternative 3: Hybrid Front Matter (Minimal in Files, Extended in Metadata)

**Description:** Add minimal front matter (title only) to markdown files; extended metadata in `docmeta.yaml`.

**Partially adopted:**
- Documented as middle-ground option in advanced setup guide
- Title in file provides human-readable context
- Extended metadata (tags, weight, menu) centralized
- 75% token savings vs. full front matter

**Trade-off:** Still requires front matter parsing by agents; metadata drift risk remains.

### Alternative 4: External Metadata Service (JSON/YAML, Build-Time Injection)

**Description:** Store metadata in `registry.json`; inject front matter into copied files during build.

**Rejected because:**
- Extreme complexity—build scripts, injection logic, two-stage builds
- Debugging difficulty (source doesn't match rendered)
- Opaque build process confusing to contributors
- Overkill for current scale

**When to revisit:** If metadata management becomes bottleneck requiring database-like capabilities (unlikely).

### Alternative 5: No Docsite (Documentation in README and Wiki)

**Description:** Forego static site; rely on GitHub's markdown rendering in repo and wiki.

**Partially valid:**
- Acceptable for small projects or early-stage templates
- Current state of this repository (no docsite today)
- Users can choose to remain docsite-free

**Limitation:** Professional documentation site improves discoverability, branding, SEO for mature projects.

## Implementation Notes

### Phase 1: Documentation (Week 1)

**Deliverables:**
1. **Advanced Setup Guide:** `docs/HOW_TO_USE/advanced-docsite-setup.md`
   - Explanation of separated metadata architecture
   - Step-by-step setup instructions (Hugo, symlinks, metadata file)
   - Windows fallback procedure (copies, sync script)
   - Validation tooling setup
   
2. **Docsite Curator Agent Profile:** `.github/agents/docsite-curator.agent.md`
   - Responsibilities: maintain `docmeta.yaml`, validate entries, detect drift
   - Capabilities: YAML editing, path normalization, bulk operations
   - Integration: task routing, orchestration rules

3. **Reference Implementation Repository:**
   - Public example repo demonstrating separated metadata
   - Includes sample Hugo configuration, templates, validation script
   - Link from quickstart template for easy reference

### Phase 2: Tooling (Week 2)

**Deliverables:**
1. **Validation Script:** `validation/validate-docsite-metadata.py`
   - File coverage check (all docs have metadata)
   - Metadata validity check (all keys reference existing files)
   - Schema validation (required fields present, types correct)
   - Path normalization check (forward slashes, relative paths)
   
2. **Sync Script (Windows):** `docs-site/scripts/sync-docs.sh` / `sync-docs.ps1`
   - One-way sync from `docs/` → `docs-site/content/docs/`
   - Optional watch mode for continuous sync
   - PowerShell equivalent for Windows users

3. **Metadata Schema:** `docs-site/schemas/docmeta.schema.json`
   - JSON Schema for `docmeta.yaml` structure
   - Validation hook for pre-commit or CI

### Phase 3: Example Repository (Week 3)

**Deliverables:**
1. **Sample Hugo Configuration:** `config.toml` with `followSymlinks: true`
2. **Custom Templates:**
   - `layouts/_default/single.html` (metadata lookup for single pages)
   - `layouts/_default/list.html` (metadata lookup for lists)
   - `layouts/partials/menu.html` (menu generation from metadata)
3. **Sample Metadata File:** `data/docmeta.yaml` with entries for key documents
4. **CI Workflow:** `.github/workflows/docsite-validation.yml` (runs validation script)

### Phase 4: Integration Testing (Week 4)

**Test Cases:**
1. **Cross-platform symlink test:** Verify symlinks work on Linux, macOS; fallback on Windows
2. **Metadata drift detection:** Rename file, verify validation script catches orphaned metadata
3. **Hugo build test:** Ensure custom templates correctly lookup and render metadata
4. **Agent workflow test:** Curator agent edits metadata; content agent reads clean file
5. **Validation script test:** Verify all checks (coverage, validity, schema) function correctly

### Acceptance Criteria

This ADR is successfully implemented when:

- ✅ `docs/HOW_TO_USE/advanced-docsite-setup.md` exists with comprehensive setup guide
- ✅ Docsite Curator Agent profile created in `.github/agents/docsite-curator.agent.md`
- ✅ Reference implementation repository created and linked from template
- ✅ Validation script (`validate-docsite-metadata.py`) functional with all checks
- ✅ Windows sync script (`sync-docs.sh`/`.ps1`) tested on Windows 10+
- ✅ Example Hugo configuration, templates, and metadata file documented
- ✅ Cross-platform testing completed (Linux, macOS, Windows)
- ✅ ADR README updated to include ADR-022

**Current Status:** Proposed—awaiting review and approval.

**Next Steps:**
1. Review ADR with stakeholders (architecture team, template maintainers)
2. Approve or request modifications
3. If approved, begin Phase 1 (documentation)
4. Pilot implementation in reference repository
5. Gather feedback from early adopters
6. Iterate based on real-world usage

## Related Documentation

- **Feasibility Study:** [Docsite Metadata Separation Feasibility Study](../assessments/docsite-metadata-separation-feasibility-study.md)
- **Risk Assessment:** [Docsite Metadata Separation Risks](../assessments/docsite-metadata-separation-risks.md)
- **Implementation Plan:** [Docsite Metadata Separation Implementation Plan](../design/docsite-metadata-separation-implementation-plan.md)
- **Executive Summary:** [Docsite Metadata Separation Executive Summary](../assessments/docsite-metadata-separation-executive-summary.md)
- **Related ADRs:**
  - [ADR-001: Modular Agent Directive System](ADR-001-modular-agent-directive-system.md) (Token economy motivation)
  - [ADR-008: File-Based Async Coordination](ADR-008-file-based-async-coordination.md) (Agent coordination pattern)
  - [ADR-017: Traceable Decision Integration](ADR-017-traceable-decision-integration.md) (Decision capture)

## Sunset/Revisit Conditions

**Revisit this ADR if:**

1. **80%+ of template users adopt docsite AND report front matter friction** → Consider making separated metadata the default
2. **Hugo symlink handling changes significantly** → Re-evaluate technical feasibility
3. **Windows symlink support improves dramatically** (e.g., enabled by default) → Remove fallback complexity
4. **Alternative pattern emerges with better ergonomics** (e.g., generator-native support for external metadata) → Evaluate replacement
5. **Token costs drop dramatically** (e.g., context windows reach 1M+ tokens, making overhead negligible) → Reconsider necessity
6. **Validation tooling proves unsustainable** (>8 hours/quarter maintenance burden) → Simplify or abandon pattern

**Sunset this ADR if:**
- Pattern unused by community (no adoption within 12 months)
- Maintenance burden exceeds benefits (validation tooling breaks repeatedly)
- Standard front matter becomes consensus (community feedback overwhelmingly prefers traditional approach)

---

_Prepared by: Architect Alphonso_  
_Reviewed by: Core Team_  
_Version: 1.0.0_  
_Last Updated: 2025-12-04_
