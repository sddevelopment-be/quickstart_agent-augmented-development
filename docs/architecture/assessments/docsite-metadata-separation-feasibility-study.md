# Feasibility Study: Docsite Metadata Separation Architecture

**Status:** Analysis Complete  
**Date:** 2025-12-04  
**Prepared by:** Architect Alphonso  
**Version:** 1.0.0

## 1. Problem Restatement

### 1.1 Core Challenge

Static site generators (Hugo, Jekyll, Gatsby) typically require **front matter** in markdown files—YAML or TOML metadata blocks at the beginning of each document. This metadata (title, tags, weight, menu placement, section) controls rendering and navigation but creates friction in agent-augmented workflows:

1. **Token Economy Concern:** Agents reading documentation files repeatedly (context loading, analysis, citation) consume tokens processing metadata irrelevant to content comprehension.
2. **Content Pollution:** Front matter intermingles presentation logic with semantic content, reducing markdown portability.
3. **Generator Lock-in:** Front matter syntax ties content to specific static site tooling.
4. **Maintenance Overhead:** Metadata changes (reorganization, tagging strategy) require editing dozens of content files.

### 1.2 Current State of This Repository

**Critical observation:** This repository's markdown files **do not currently contain front matter**. The 124 files in `docs/` and 72 files in `.github/agents/` are **clean markdown** with no YAML/TOML blocks.

**Implication:** The problem this architecture solves **does not yet exist**. The proposal is **preventative**, not remedial. The question is whether to proactively adopt this pattern to avoid future front matter pollution when/if a docsite is added.

### 1.3 Proposed Solution

**Architecture:** Separate metadata from content by:

- Keeping markdown files in `docs/` and `.github/agents/` clean (no front matter)
- Creating `docs-site/data/docmeta.yaml` to hold all metadata
- Symlinking `docs/` → `docs-site/content/docs/` and `.github/agents/` → `docs-site/content/agents/`
- Configuring Hugo to lookup metadata by file path
- Optionally introducing a **Docsite Curator Agent** to maintain metadata integrity

**Goal:** Agents operate on clean markdown; Hugo renders using separated metadata.

## 2. Contextual Forces

### 2.1 Technical Forces

**Force: Cross-Platform Symlink Compatibility**
- **Linux/macOS:** Symlinks work natively, widely supported
- **Windows:** Requires Developer Mode (Win10+) or Admin rights; some tools (IDEs, indexers) handle symlinks poorly
- **Git:** Symlinks stored as special objects; behavior varies by platform on checkout
- **Implication:** Windows users may encounter broken symlinks, requiring fallback to directory copies

**Force: Hugo Symlink Handling**
- **Hugo behavior:** Hugo can follow symlinks in `content/` directories (configurable via `followSymlinks: true`)
- **Template complexity:** Custom templates required to lookup metadata from `data/docmeta.yaml` by filepath
- **Implication:** Standard Hugo themes incompatible without modification; custom lookup logic required

**Force: Static Site Generator Agnosticism**
- **Benefit:** Clean markdown files can be consumed by any generator (Hugo, MkDocs, Docusaurus, Sphinx)
- **Trade-off:** External metadata pattern uncommon; switching generators requires new lookup implementation
- **Implication:** Generator-agnostic goal achieved, but migration effort remains significant

**Force: Metadata Drift Risk**
- **Scenario:** File renamed `docs/foo.md` → `docs/bar.md`, metadata keyed by old path remains
- **Detection:** Requires validation script to compare filesystem paths with metadata keys
- **Implication:** Validation becomes mandatory CI step; human error prone without automation

### 2.2 Agentic/LLM Forces

**Force: Token Economy at Scale**
- **Current state:** 124 docs + 72 agent files = 196 markdown files, no front matter
- **Front matter size:** Typical front matter 5-15 lines (~100-300 tokens per file)
- **Potential cost:** If front matter added, 196 × 200 tokens = **~39,200 tokens** consumed per full-repo context load
- **Agent reading patterns:** Curator agent reads ~20-30 files per analysis; Architect agent reads ~10-15 ADRs; Writer agent reads ~5-10 guides
- **Actual token savings:** Curator: ~6,000 tokens/session; Architect: ~3,000 tokens/session; Writer: ~2,000 tokens/session
- **Implication:** Savings meaningful (5-10% of context window) only if agents frequently reload documents. For single-read tasks, benefit negligible.

**Force: Agent Specialization Alignment**
- **Content-reading agents** (Architect, Writer, Researcher): Benefit significantly from clean files
- **Metadata-managing agents** (Docsite Curator): Require access to `docmeta.yaml` but not content files
- **Coordination agents** (Orchestrator): Unaffected, operate on task YAML files
- **Implication:** Separation aligns well with agent responsibilities; clear boundaries reduce cognitive load

**Force: Metadata Modification Discipline**
- **Risk:** Non-curator agents accidentally editing metadata if location unclear
- **Mitigation:** Directive 018 (Decision Capture) can mandate: "Content agents MUST NOT edit `docs-site/data/docmeta.yaml`"
- **Implication:** Agent profiles must be updated to restrict metadata access; validation tooling verifies compliance

### 2.3 Human Developer Forces

**Force: Cognitive Model of "A Document"**
- **Traditional model:** One file = content + metadata
- **Separated model:** Content in `docs/`, metadata in `docs-site/data/docmeta.yaml`
- **Onboarding friction:** New contributors expect metadata alongside content; external metadata breaks mental model
- **Implication:** Documentation must explicitly explain pattern; training overhead increases ~1-2 hours

**Force: Editing Workflow Complexity**
- **Traditional:** Edit file, add front matter, preview locally
- **Separated:** Edit file in `docs/`, add metadata entry to `docmeta.yaml` (keyed by path), rebuild Hugo
- **Preview dependency:** Cannot preview single file rendering without Hugo build
- **Implication:** Local development ergonomics degraded; Hugo dev server becomes mandatory for preview

**Force: Discoverability of Metadata**
- **Traditional:** Metadata at top of file, immediately visible
- **Separated:** Metadata in separate file, requires lookup by path
- **Impact:** Bulk metadata operations (retagging, weight adjustment) easier; single-file context harder
- **Implication:** Trade-off favors centralized maintenance over point-of-need visibility

### 2.4 Repository Evolution Forces

**Force: Docsite Adoption Timing**
- **Current state:** No Hugo/Jekyll configuration exists
- **Adoption scenarios:**
  1. Never adopt docsite → pattern unnecessary, pure overhead
  2. Adopt docsite in 3-6 months → proactive pattern prevents front matter pollution
  3. Adopt docsite immediately → pattern justifies implementation effort
- **Implication:** Decision timing critical; premature optimization if docsite not planned within 6 months

**Force: Template Repository Mission**
- **Purpose:** Provide quickstart template for agent-augmented workflows
- **Tension:** Advanced patterns (separated metadata) increase template complexity
- **Baseline expectation:** Simple, approachable setup for new users
- **Implication:** Advanced patterns should be **opt-in profiles**, not default baseline

**Force: Maintenance Burden Over Time**
- **Validation tooling:** Metadata-file sync checker requires ongoing maintenance
- **Hugo template updates:** Custom lookup logic incompatible with standard theme updates
- **Docsite Curator Agent:** Additional agent to maintain, test, coordinate
- **Implication:** Long-term cost exceeds initial implementation; requires commitment to sustain

### 2.5 Build & CI Constraints

**Force: Symlink Behavior in GitHub Actions**
- **Linux runners:** Symlinks work natively
- **Windows runners:** May require `git config core.symlinks true`, Admin mode unavailable
- **Workaround:** Use directory copies instead of symlinks on Windows runners
- **Implication:** CI scripts must detect platform and adapt symlink strategy

**Force: Hugo Build Complexity**
- **Standard build:** `hugo --source docs-site/`
- **Metadata lookup:** Custom templates in `docs-site/layouts/` required
- **Dependency:** Hugo extended version may be needed for advanced templating
- **Implication:** CI/CD pipeline adds Hugo build step; build time increases ~5-15 seconds

**Force: Deployment Artifact Size**
- **Without docsite:** No static build artifacts
- **With docsite:** HTML/CSS/JS output in `docs-site/public/`, ~5-20MB depending on content size
- **Implication:** Repository size increases; GitHub Pages or external hosting required

### 2.6 Cross-Platform Constraints

**Force: Windows Developer Experience**
- **Symlink issues:** Broken symlinks without Developer Mode; IDE indexers may not follow symlinks
- **Fallback strategy:** Provide `sync-docs.sh` script to copy `docs/` → `docs-site/content/docs/` instead of symlinking
- **Implication:** Windows users have degraded experience; manual sync required after content edits

**Force: JetBrains IDE Symlink Handling**
- **IntelliJ IDEA, PyCharm, WebStorm:** Historically poor symlink indexing; may show duplicate files or indexing errors
- **Workaround:** Exclude `docs-site/content/` from indexing in `.idea/` settings
- **Implication:** Additional IDE configuration required; documented in setup guide

### 2.7 Long-Term Maintainability

**Force: Metadata Schema Evolution**
- **Initial schema:** title, tags, weight, menu, section
- **Future additions:** author, last_updated, related_docs, audience
- **Migration risk:** Schema changes require updating all metadata entries and Hugo templates
- **Implication:** Schema versioning and migration scripts needed for sustainability

**Force: Knowledge Transfer**
- **Team turnover:** New maintainers must understand non-standard pattern
- **Documentation debt:** Setup guide, metadata conventions, troubleshooting must be maintained
- **Implication:** Pattern sustainability depends on comprehensive documentation and team buy-in

### 2.8 Ergonomics for Repository Users

**Force: Cloning and Setup**
- **Standard repo:** `git clone` → edit files → commit
- **Separated metadata:** `git clone` → configure symlinks/copies → edit files + metadata → commit both → rebuild docsite
- **Friction points:** Additional setup steps; two-location editing; build dependency
- **Implication:** User experience degraded for casual contributors; better for high-frequency agent workflows

**Force: Search and Navigation**
- **Content search:** `grep -r "pattern" docs/` works as expected
- **Metadata search:** `grep -r "tag: foo" docs-site/data/docmeta.yaml` centralized
- **Trade-off:** Content search unaffected; metadata search different but simpler (one file vs. many)
- **Implication:** Documentation must explain both search patterns

### 2.9 Future-Proofing (Switching Generators)

**Force: Generator Migration Effort**
- **Hugo → MkDocs:** Requires rewriting metadata lookup logic in Jinja2 templates
- **Hugo → Docusaurus:** Requires converting `docmeta.yaml` to JS-based sidebar configuration
- **Hugo → Sphinx:** Requires mapping to `conf.py` toctree configuration
- **Implication:** Generator-agnostic goal partially achieved (content portable), but metadata integration is generator-specific

**Force: Metadata Format Portability**
- **YAML format:** Widely supported, human-readable
- **Alternative formats:** JSON (less human-friendly), TOML (Hugo-native but less common)
- **Implication:** YAML is good choice; conversion scripts feasible if format change needed

## 3. Options to Compare

### Option A: Standard Front Matter in Content Files

**Description:** Traditional approach—add YAML front matter blocks to each markdown file in `docs/` and `.github/agents/`.

**Implementation:**
```markdown
---
title: "Agent Orchestration Guide"
tags: ["agents", "workflow", "automation"]
weight: 10
section: "HOW_TO_USE"
menu:
  main:
    parent: "guides"
---

# Agent Orchestration Guide

Content starts here...
```

**Pros:**
- Industry standard, well-understood pattern
- Single-file mental model (content + metadata together)
- Hugo themes work out-of-box, no custom templates
- Local preview simple (edit → save → Hugo reload)
- No symlink complexity
- No validation tooling needed for metadata drift

**Cons:**
- Token overhead: ~200 tokens/file × 196 files = 39,200 tokens
- Content pollution: presentation logic intermixed with semantic content
- Generator lock-in: front matter syntax varies by generator
- Maintenance: metadata changes require editing many files
- Agent cognitive load: must parse front matter to find content

**Agent Impact:**
- Agents must skip front matter when reading content
- Token budget consumed by irrelevant metadata
- LLMs handle front matter well (common pattern in training data)

**Complexity:** Low—standard Hugo setup

**Token Cost:** High—cumulative overhead across all files

**Build Implications:** Standard Hugo build, no customization needed

**UX/Onboarding:** Excellent—familiar to most developers, tutorials abundant

### Option B: Docsite-Separated Metadata (Proposed Approach)

**Description:** Keep markdown files clean; centralize metadata in `docs-site/data/docmeta.yaml`; symlink content into Hugo's `content/` directory.

**Implementation:**

**Clean markdown file (`docs/HOW_TO_USE/multi-agent-orchestration.md`):**
```markdown
# Multi-Agent Orchestration

This guide explains how to coordinate...
```

**Metadata file (`docs-site/data/docmeta.yaml`):**
```yaml
docs/HOW_TO_USE/multi-agent-orchestration.md:
  title: "Multi-Agent Orchestration Guide"
  tags: ["agents", "workflow", "automation"]
  weight: 10
  section: "HOW_TO_USE"
  menu:
    main:
      parent: "guides"
```

**Hugo template snippet (`docs-site/layouts/_default/single.html`):**
```go-template
{{ $path := .File.Path }}
{{ $metadata := index .Site.Data.docmeta $path }}
<h1>{{ $metadata.title | default .Title }}</h1>
<div class="tags">
  {{ range $metadata.tags }}
    <span class="tag">{{ . }}</span>
  {{ end }}
</div>
```

**Symlink setup:**
```bash
ln -s ../../docs docs-site/content/docs
ln -s ../../../.github/agents docs-site/content/agents
```

**Pros:**
- Clean content files: zero token overhead for agents reading docs
- Generator-agnostic content: markdown portable to any system
- Centralized metadata: bulk operations simple (retag all "agents" files)
- Agent specialization: content agents never see metadata; curator manages metadata
- Future-proof: prevents front matter pollution

**Cons:**
- High complexity: symlinks, custom templates, validation tooling required
- Platform issues: Windows symlink problems, IDE indexing issues
- Cognitive overhead: two-location editing, mental model shift
- Metadata drift risk: file renames break keying without validation
- Hugo theme incompatibility: standard themes require modification
- Maintenance burden: validation scripts, curator agent, custom templates

**Agent Impact:**
- Content-reading agents benefit significantly (clean files)
- Docsite Curator Agent added for metadata management
- Validation agent must check metadata-file synchronization

**Complexity:** High—custom Hugo setup, symlink management, validation tooling

**Token Cost:** Zero for content agents; metadata separate

**Build Implications:** Custom Hugo templates, symlink configuration, validation scripts

**UX/Onboarding:** Poor—non-standard pattern, multi-location editing, setup complexity

### Option C: Hybrid Front Matter (Minimal in Files, Heavy in Site)

**Description:** Minimal front matter in markdown files (only title); extended metadata in `docs-site/data/docmeta.yaml`.

**Implementation:**

**Markdown file (`docs/HOW_TO_USE/multi-agent-orchestration.md`):**
```markdown
---
title: "Multi-Agent Orchestration"
---

# Multi-Agent Orchestration

This guide explains how to coordinate...
```

**Metadata file (`docs-site/data/docmeta.yaml`):**
```yaml
docs/HOW_TO_USE/multi-agent-orchestration.md:
  tags: ["agents", "workflow", "automation"]
  weight: 10
  section: "HOW_TO_USE"
  menu:
    main:
      parent: "guides"
```

**Pros:**
- Balanced trade-off: title visible in file, metadata centralized
- Reduced token overhead: ~50 tokens/file vs. 200 (75% reduction)
- Better human ergonomics: title at top aids quick identification
- Partial generator compatibility: minimal front matter widely supported
- Simpler templates: Hugo can use file front matter title as fallback

**Cons:**
- Still requires custom Hugo templates for metadata lookup
- Title duplication possible (front matter vs. first heading)
- Metadata drift risk remains (keying by path)
- Agents still parse front matter (reduced but not eliminated)

**Agent Impact:**
- Token savings moderate: ~75% reduction vs. Option A
- Agents must still skip front matter block
- Curator agent manages extended metadata in `docmeta.yaml`

**Complexity:** Medium—custom templates, partial validation

**Token Cost:** Low—minimal front matter overhead

**Build Implications:** Custom Hugo templates for extended metadata

**UX/Onboarding:** Good—familiar front matter pattern, centralized metadata for advanced needs

### Option D: External Metadata Service (JSON/YAML Indexed by Path, Hugo-Independent)

**Description:** Metadata stored in structured format (JSON/YAML) indexed by filepath; consumed by build scripts (not Hugo-native). Supports multiple generators via adapter scripts.

**Implementation:**

**Metadata file (`docs-site/metadata/registry.json`):**
```json
{
  "version": "1.0",
  "documents": [
    {
      "path": "docs/HOW_TO_USE/multi-agent-orchestration.md",
      "title": "Multi-Agent Orchestration Guide",
      "tags": ["agents", "workflow", "automation"],
      "weight": 10,
      "section": "HOW_TO_USE",
      "menu": {"main": {"parent": "guides"}}
    }
  ]
}
```

**Build script (`docs-site/scripts/inject-metadata.js`):**
```javascript
// Read registry.json, inject front matter into copied markdown files
// Generate Hugo-compatible front matter in docs-site/content/
```

**Pros:**
- Clean source markdown files (zero front matter)
- Generator-agnostic metadata format
- Structured, versioned metadata registry
- Build-time injection: source files remain pristine
- Schema-validatable JSON format

**Cons:**
- Extreme complexity: build scripts, injection logic, adapter maintenance
- Two-step build: inject metadata → run Hugo
- Duplication: source files + generated files with injected metadata
- Debugging difficulty: source doesn't match rendered (injected metadata invisible)
- Fragile keying: filepath changes break registry without validation

**Agent Impact:**
- Source files completely clean: maximum token savings
- Curator agent manages JSON registry (structured format)
- Validation complexity high: schema validation + drift detection

**Complexity:** Very High—custom build tooling, multi-stage pipeline

**Token Cost:** Zero for source files

**Build Implications:** Two-stage build, custom injection scripts, generated file management

**UX/Onboarding:** Poor—opaque build process, unfamiliar pattern, debugging challenges

## 4. Technical Feasibility Analysis

### 4.1 Symlink Behavior on Different Platforms

**Linux:**
- Native symlink support via `ln -s target link`
- Git stores symlinks as special objects (mode `120000`)
- Hugo follows symlinks with `followSymlinks: true` in `config.toml`
- **Verdict:** Fully compatible, no issues expected

**macOS:**
- Identical to Linux (POSIX-compliant symlinks)
- **Verdict:** Fully compatible

**Windows:**
- **Without Developer Mode:** Symlinks disabled; `git clone` converts symlinks to text files containing target path
- **With Developer Mode (Win10+):** Symlinks enabled via `git config core.symlinks true`
- **Admin Rights:** `mklink` requires Admin privileges in older Windows versions
- **Fallback:** Directory copies via `robocopy` or PowerShell `Copy-Item -Recurse`
- **Verdict:** Partially compatible; requires Developer Mode or fallback to copies

**GitHub Actions:**
- Linux runners: Symlinks work natively
- Windows runners: Require `git config core.symlinks true` in workflow; Admin mode unavailable
- macOS runners: Symlinks work natively
- **Verdict:** Linux/macOS compatible; Windows runners need explicit configuration or fallback

**Recommendation:** Provide dual-mode setup:
- **Default:** Symlinks for Linux/macOS
- **Windows:** Setup script to copy directories (with watch script for auto-sync)

### 4.2 Hugo Behavior with Symlinked Content

**Configuration:**
```toml
# docs-site/config.toml
followSymlinks = true
```

**Behavior:**
- Hugo resolves symlinks and treats targets as regular content
- File paths relative to `content/` directory, not symlink target
- `.File.Path` in templates returns symlinked path, not original

**Metadata Lookup Strategy:**
```go-template
{{ $path := .File.Path }}
{{ $metadata := index .Site.Data.docmeta $path }}
```

**Issue:** `.File.Path` returns `docs/HOW_TO_USE/multi-agent-orchestration.md` (symlinked path), but metadata keyed by `docs/HOW_TO_USE/multi-agent-orchestration.md` (source path).

**Resolution:** Normalize paths in metadata file to match symlinked paths, OR use relative paths.

**Verdict:** Feasible with careful path normalization; requires testing.

### 4.3 Template Patterns Required

**Single Page Template (`layouts/_default/single.html`):**
```go-template
{{ $relPath := strings.TrimPrefix "content/" .File.Path }}
{{ $metadata := index .Site.Data.docmeta $relPath }}

<article>
  <h1>{{ $metadata.title | default .Title }}</h1>
  
  {{ if $metadata.tags }}
  <div class="tags">
    {{ range $metadata.tags }}
      <a href="/tags/{{ . | urlize }}">{{ . }}</a>
    {{ end }}
  </div>
  {{ end }}
  
  {{ .Content }}
</article>
```

**List Template (`layouts/_default/list.html`):**
```go-template
{{ range .Pages }}
  {{ $relPath := strings.TrimPrefix "content/" .File.Path }}
  {{ $metadata := index $.Site.Data.docmeta $relPath }}
  
  <div class="list-item">
    <h2><a href="{{ .RelPermalink }}">{{ $metadata.title | default .Title }}</a></h2>
    <p>{{ .Summary }}</p>
  </div>
{{ end }}
```

**Menu Generation (`layouts/partials/menu.html`):**
```go-template
{{ $docmeta := .Site.Data.docmeta }}
{{ range $path, $meta := $docmeta }}
  {{ if $meta.menu }}
    {{ if $meta.menu.main }}
      <li>
        <a href="/{{ $path | replaceRE "\\.md$" "" }}">{{ $meta.title }}</a>
      </li>
    {{ end }}
  {{ end }}
{{ end }}
```

**Complexity Assessment:** Medium—custom templates required, but patterns are straightforward once established. Standard themes cannot be used without modification.

### 4.4 Metadata Lookup Mechanics

**Keying Strategy Options:**

1. **By Relative Path (Recommended):**
   ```yaml
   docs/HOW_TO_USE/multi-agent-orchestration.md:
     title: "Multi-Agent Orchestration"
   ```
   - **Pros:** Intuitive, matches filesystem, human-readable
   - **Cons:** Breaks on file rename/move without metadata update

2. **By Filename Only:**
   ```yaml
   multi-agent-orchestration.md:
     title: "Multi-Agent Orchestration"
   ```
   - **Pros:** Survives directory moves
   - **Cons:** Name collisions possible (same filename in different dirs)

3. **By Unique ID:**
   ```yaml
   doc-001:
     path: docs/HOW_TO_USE/multi-agent-orchestration.md
     title: "Multi-Agent Orchestration"
   ```
   - **Pros:** Survives renames/moves, no collisions
   - **Cons:** Opaque, requires ID tracking, human readability poor

4. **By Content Hash (SHA256):**
   ```yaml
   a3f5b8c9d2e1...:
     title: "Multi-Agent Orchestration"
   ```
   - **Pros:** Survives renames, collision-proof
   - **Cons:** Extremely opaque, hash changes on content edits, impractical

**Recommendation:** Use **relative path keying** with mandatory validation to detect drift. Provide migration script for bulk renames.

### 4.5 Implementation Complexity

**Components Required:**

1. **Hugo Configuration:**
   - `config.toml` with `followSymlinks = true`
   - Content directory symlinks or copies

2. **Metadata File:**
   - `docs-site/data/docmeta.yaml` with structured entries

3. **Custom Templates:**
   - Single page template with metadata lookup
   - List template with metadata lookup
   - Menu generation logic

4. **Validation Script:**
   ```python
   # validation/validate-docsite-metadata.py
   # - Check all files in docs/ have metadata entries
   # - Check all metadata keys reference existing files
   # - Warn on missing title, tags, etc.
   ```

5. **Sync Script (Windows Fallback):**
   ```bash
   # docs-site/scripts/sync-docs.sh
   rsync -av --delete docs/ docs-site/content/docs/
   rsync -av --delete .github/agents/ docs-site/content/agents/
   ```

6. **Docsite Curator Agent Profile:**
   - Responsibilities: maintain `docmeta.yaml`, validate entries, detect drift
   - Capabilities: YAML editing, path normalization, bulk operations

**Complexity Rating:** 7/10 (High)—requires multiple custom components, ongoing validation, specialized agent.

### 4.6 Risks with Metadata Drift

**Scenario 1: File Renamed**
- Action: `git mv docs/foo.md docs/bar.md`
- Metadata: Still keyed as `docs/foo.md`
- Result: Metadata orphaned; `docs/bar.md` renders with default/missing metadata

**Detection:**
- Validation script compares filesystem files with metadata keys
- Reports orphaned keys and missing keys

**Mitigation:**
- CI validation fails on drift
- Pre-commit hook warns on file moves
- Curator agent audits metadata weekly

**Scenario 2: File Deleted**
- Action: `git rm docs/obsolete.md`
- Metadata: Entry remains in `docmeta.yaml`
- Result: Orphaned metadata entry (harmless but clutters)

**Detection:**
- Validation script reports orphaned keys

**Mitigation:**
- Curator agent prunes orphaned entries monthly

**Scenario 3: New File Added**
- Action: `touch docs/newguide.md`, commit without metadata
- Metadata: No entry for `docs/newguide.md`
- Result: File renders with default metadata (title from filename, no tags)

**Detection:**
- Validation script reports files missing metadata

**Mitigation:**
- CI validation warns on missing metadata
- Template agent adds default metadata entry skeleton

**Risk Level:** HIGH—metadata drift is inevitable without rigorous validation and discipline.

### 4.7 Required Validation Tooling

**Script: `validation/validate-docsite-metadata.py`**

**Functions:**
1. **File Coverage Check:**
   - List all `.md` files in `docs/` and `.github/agents/`
   - Check each file has corresponding metadata key
   - Report missing metadata entries

2. **Metadata Validity Check:**
   - List all keys in `docmeta.yaml`
   - Check each key references existing file
   - Report orphaned metadata entries

3. **Schema Validation:**
   - Verify required fields present (title, tags, section)
   - Validate field types (tags is list, weight is number)
   - Warn on unusual values (weight < 0, empty title)

4. **Path Normalization Check:**
   - Ensure keys use consistent path format (forward slashes, relative to repo root)
   - Warn on Windows-style backslashes

5. **Duplicate Detection:**
   - Check for multiple metadata entries with same title
   - Warn on potential collisions

**Integration:**
- Run as CI check (GitHub Actions)
- Run as pre-commit hook (optional)
- Run manually via `make validate-docsite`

**Exit Codes:**
- 0: All checks passed
- 1: Warnings (missing metadata)
- 2: Errors (orphaned metadata, schema invalid)

**Complexity:** Medium—Python script, YAML parsing, filesystem traversal, ~200-300 lines.

### 4.8 Metadata Inheritance/Defaults Support

**Use Case:** All files in `docs/architecture/adrs/` share common tags `["architecture", "decision"]` and section `"ADRs"`.

**Option 1: Explicit in Metadata File**
```yaml
docs/architecture/adrs/ADR-001.md:
  title: "ADR-001: Modular Directives"
  tags: ["architecture", "decision", "directives"]
  section: "ADRs"
docs/architecture/adrs/ADR-002.md:
  title: "ADR-002: Example"
  tags: ["architecture", "decision"]
  section: "ADRs"
```
- **Pros:** Explicit, easy to override
- **Cons:** Repetitive, maintenance burden

**Option 2: Defaults Section**
```yaml
defaults:
  docs/architecture/adrs/*:
    tags: ["architecture", "decision"]
    section: "ADRs"
    
docs/architecture/adrs/ADR-001.md:
  title: "ADR-001: Modular Directives"
  tags: ["directives"]  # Merges with defaults
```
- **Pros:** DRY, easier maintenance
- **Cons:** Requires merge logic in Hugo templates (complex)

**Recommendation:** Start with explicit entries; add defaults support in Phase 2 if maintenance burden becomes high.

### 4.9 Compatibility: Windows, JetBrains IDEs, GitHub CI Runners

**Windows Compatibility:**
- **Symlinks:** Require Developer Mode or Admin rights; not default
- **Fallback:** Directory copies via PowerShell script
- **Watch script:** Auto-sync `docs/` → `docs-site/content/docs/` on file changes
- **Verdict:** Workable with fallback; additional setup steps required

**JetBrains IDEs (IntelliJ, PyCharm, WebStorm):**
- **Symlink indexing:** Historically poor; may show duplicate files or errors
- **Workaround:** Exclude `docs-site/content/` from indexing in `.idea/vcs.xml`
- **Configuration:**
  ```xml
  <component name="VcsDirectoryMappings">
    <mapping directory="$PROJECT_DIR$" vcs="Git" />
    <mapping directory="$PROJECT_DIR$/docs-site/content" vcs="" />
  </component>
  ```
- **Verdict:** Workable with IDE configuration; documented in setup guide

**GitHub Actions:**
- **Linux runners:** Symlinks work natively
- **Windows runners:** Require `git config core.symlinks true` in workflow
- **Example workflow step:**
  ```yaml
  - name: Setup symlinks (Windows)
    if: runner.os == 'Windows'
    run: |
      git config core.symlinks true
      git reset --hard HEAD
  ```
- **Verdict:** Workable with workflow configuration

## 5. Agent Workflow Implications

### 5.1 Token Savings Expectations

**Current State (No Front Matter):**
- 196 markdown files, zero tokens consumed by metadata
- **Savings vs. Baseline:** 0% (no problem to solve)

**Hypothetical (If Front Matter Added):**
- 196 files × 200 tokens/file = 39,200 tokens
- Agents re-reading files: Curator (~30 files/session), Architect (~15 files/session), Writer (~10 files/session)
- **Curator savings:** 30 × 200 = 6,000 tokens/session (~5-7% of 100K context window)
- **Architect savings:** 15 × 200 = 3,000 tokens/session (~3% of context window)
- **Writer savings:** 10 × 200 = 2,000 tokens/session (~2% of context window)

**Verdict:** Savings are **modest** (2-7% context window) and **only meaningful if front matter would be added**. Since files are currently clean, benefit is **preventative**, not remedial.

### 5.2 Which Specialists Benefit Most

**High Benefit:**
- **Curator Claire:** Reads 20-30 docs per analysis; clean files reduce noise
- **Researcher Riley:** Scans many files for patterns; metadata irrelevant to content analysis
- **Writer Willow:** Reviews 10-15 guides; clean content improves focus

**Medium Benefit:**
- **Architect Alphonso:** Reads 10-15 ADRs; token savings modest but appreciated
- **Lexical Agent:** Parses glossary and terminology; clean files simplify parsing

**Low/No Benefit:**
- **Docsite Curator (New):** Operates on metadata file, not content files
- **Orchestrator:** Works with task YAML files, not documentation
- **Bootstrap Bill:** Reads agent profiles, which could remain in `.github/agents/` (symlinked)

**Verdict:** Content-reading generalists benefit most; metadata-focused specialists unaffected or negatively impacted (additional coordination).

### 5.3 Which Agents Should/Shouldn't Read Metadata

**Should Read Metadata:**
- **Docsite Curator:** Primary responsibility—maintain `docmeta.yaml`
- **Architect Alphonso:** May reference metadata structure when designing docsite architecture
- **Validator Agent:** Checks metadata-file synchronization

**Should NOT Read Metadata:**
- **Content-focused agents (Writer, Researcher, Lexical):** Metadata irrelevant to content analysis
- **Orchestrator:** Operates on task YAML, not docsite metadata
- **Build Automation:** May consume metadata during Hugo build but doesn't edit

**Enforcement:**
- Directive 018 update: "Content agents MUST NOT edit `docs-site/data/docmeta.yaml`"
- Agent profiles: Exclude metadata file from context unless explicitly curator role

**Verdict:** Clear separation aligns with agent specialization; reduces cognitive load and accidental edits.

### 5.4 Whether Metadata Modification Restricted to Curator Agent

**Proposal:** Designate **Docsite Curator Agent** as sole authority for metadata editing.

**Rationale:**
- Prevents accidental corruption by content-focused agents
- Centralizes metadata governance
- Enables specialized validation and drift detection

**Enforcement Mechanisms:**
1. **Agent Directives:** Explicitly forbid non-curator agents from editing `docmeta.yaml`
2. **Validation Script:** Check commit history; warn if non-curator edited metadata
3. **PR Review Checklist:** Verify metadata changes made by curator or approved by human

**Trade-off:**
- **Pro:** Reduces error risk, clear responsibility
- **Con:** Coordinator overhead—content agents must request metadata changes from curator

**Verdict:** Recommended for Phase 2; Phase 1 can allow human-supervised metadata edits.

### 5.5 Safeguards to Prevent Metadata Corruption

**Risk Vectors:**
1. Non-curator agent accidentally edits `docmeta.yaml`
2. Human manually edits and introduces YAML syntax errors
3. File renamed without metadata update
4. Metadata entry added with incorrect path key

**Safeguards:**

**1. Schema Validation:**
- JSON Schema for `docmeta.yaml`
- Pre-commit hook validates YAML syntax and schema
- CI check fails on invalid metadata

**2. Drift Detection:**
- `validate-docsite-metadata.py` runs in CI
- Reports missing metadata, orphaned metadata, schema violations
- Fails build on errors; warns on missing metadata

**3. Agent Directive Enforcement:**
- Directive 018: "Content agents MUST NOT edit metadata file"
- Agent profiles: Exclude metadata from context for non-curator agents

**4. Path Normalization:**
- Validation script checks paths use forward slashes
- Warns on absolute paths (should be relative to repo root)

**5. Automated Metadata Skeleton:**
- Template agent generates default metadata entry for new files
- Curator reviews and enhances skeleton entries

**Verdict:** Multi-layered safeguards essential; without them, metadata drift becomes unmanageable.

### 5.6 How to Enforce Only Content Files Processed by Content Agents

**Mechanism 1: Directory-Based Context Loading**
- Content agents receive context: `docs/**/*.md` and `.github/agents/**/*.md`
- Exclude: `docs-site/data/*` from context
- Implementation: Agent invocation specifies context directories

**Mechanism 2: Directive-Based Restrictions**
- Directive 018: "When operating on documentation, agents MUST read files from `docs/` or `.github/agents/`, NOT from `docs-site/data/`"
- Agent profiles: Include directive in pre-check instructions

**Mechanism 3: Validation Post-Execution**
- Check agent work logs: if metadata file edited by non-curator, flag for review
- CI check: inspect git commits from agent accounts, warn on metadata edits

**Mechanism 4: File Path Filtering in Agent Tools**
- If agent framework supports path filters, exclude `docs-site/` from content agent file operations
- Not always feasible depending on LLM toolchain

**Verdict:** Directive-based enforcement most practical; validation provides safety net.

## 6. Repository Structure Impact

### 6.1 Detailed Changes to `docs/`

**Current Structure:**
```
docs/
├── VISION.md
├── CHANGELOG.md
├── HOW_TO_USE/
│   ├── QUICKSTART.md
│   ├── multi-agent-orchestration.md
│   └── ...
├── architecture/
│   ├── adrs/
│   ├── patterns/
│   └── ...
└── ...
```

**No Changes Required:**
- Files remain in place
- No front matter added
- Content unchanged

**Impact:** Zero—separation preserves existing structure.

### 6.2 Changes to `.github/agents/`

**Current Structure:**
```
.github/agents/
├── AGENTS.md
├── architect.agent.md
├── curator.agent.md
├── directives/
│   ├── 001_cli_shell_tooling.md
│   └── ...
└── ...
```

**Symlink Addition:**
```
docs-site/content/agents -> ../../../.github/agents/
```

**Impact:** Minimal—symlink created; files unchanged. Symlink may need `.gitignore` entry to avoid confusion.

### 6.3 New `docs-site/` Directory Structure

**Proposed Structure:**
```
docs-site/
├── config.toml               # Hugo configuration
├── content/
│   ├── docs -> ../../docs/   # Symlink to docs/
│   └── agents -> ../../../.github/agents/  # Symlink to agents/
├── data/
│   └── docmeta.yaml          # Centralized metadata
├── layouts/
│   ├── _default/
│   │   ├── baseof.html       # Base template
│   │   ├── single.html       # Single page template
│   │   └── list.html         # List template
│   └── partials/
│       ├── header.html
│       ├── footer.html
│       └── menu.html
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── main.js
├── scripts/
│   ├── sync-docs.sh          # Windows fallback sync
│   └── validate-metadata.py # Metadata validation
└── public/                   # Generated site (gitignored)
```

**Files to Create:**
- `config.toml`: Hugo configuration with symlink support
- `docmeta.yaml`: Initial metadata file with entries for key documents
- Custom templates: `single.html`, `list.html`, `menu.html`
- Validation script: `validate-metadata.py`
- Sync script: `sync-docs.sh` (Windows fallback)

### 6.4 Changes to `work/` (Task Logs, Metadata Tasks)

**New Subdirectory:**
```
work/tasks/docsite-curator/
├── metadata-audit-2025-12-04.yaml
├── metadata-sync-2025-12-05.yaml
└── ...
```

**Task Template for Metadata Operations:**
```yaml
task:
  id: "docsite-curator-audit-20251204"
  type: "metadata-audit"
  status: "pending"
  agent: "docsite-curator"
  description: "Audit docmeta.yaml for missing entries and orphaned keys"
  context:
    files:
      - docs-site/data/docmeta.yaml
    validation_script: validation/validate-docsite-metadata.py
  result: null
```

**Impact:** New task category for metadata operations; orchestrator must route to curator agent.

### 6.5 Changes to Validation Scripts

**New Script: `validation/validate-docsite-metadata.py`**

**Responsibilities:**
- File coverage check
- Metadata validity check
- Schema validation
- Path normalization check

**Integration:**
- CI workflow: `.github/workflows/docsite-validation.yml`
- Pre-commit hook (optional): `.git/hooks/pre-commit`
- Manual: `make validate-docsite` or `python validation/validate-docsite-metadata.py`

**Exit Codes:**
- 0: All checks passed
- 1: Warnings (missing metadata, suggest additions)
- 2: Errors (orphaned metadata, schema violations)

**Configuration File: `validation/docsite-metadata-config.yaml`**
```yaml
validation:
  content_directories:
    - docs/
    - .github/agents/
  metadata_file: docs-site/data/docmeta.yaml
  required_fields:
    - title
    - tags
    - section
  warn_on_missing: true
  fail_on_orphaned: true
```

---

_Continued in Part 2..._
