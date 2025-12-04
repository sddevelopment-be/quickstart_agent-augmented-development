# Risk Assessment: Docsite Metadata Separation Architecture

**Status:** Analysis Complete  
**Date:** 2025-12-04  
**Prepared by:** Architect Alphonso  
**Version:** 1.0.0  
**Related ADR:** [ADR-022: Docsite Separated Metadata](../adrs/ADR-022-docsite-separated-metadata.md)

## Risk Matrix Overview

This assessment evaluates risks associated with implementing separated metadata architecture as an optional advanced profile. Risks are scored on:

- **Probability:** Low (10-30%), Medium (30-60%), High (60-90%)
- **Impact:** Low (minor inconvenience), Medium (significant disruption), High (blocking issue)
- **Overall Severity:** Probability × Impact = Risk Score

**Risk Scoring:**
- **Critical (≥7):** Requires immediate mitigation; may block adoption
- **High (5-6):** Significant concern; mitigation strongly recommended
- **Medium (3-4):** Manageable with planning; monitor closely
- **Low (1-2):** Acceptable risk; document workaround

---

## Risk Register

| ID | Risk | Probability | Impact | Severity | Mitigation |
|----|------|-------------|--------|----------|------------|
| R1 | Symlink failures on Windows | High (70%) | High | **9 - CRITICAL** | Provide copy-based fallback; document Developer Mode setup |
| R2 | Metadata drift (file renamed, metadata stale) | High (60%) | High | **9 - CRITICAL** | Mandatory validation in CI; Curator agent audits; migration script |
| R3 | Missing metadata entries for new files | Medium (50%) | Medium | **6 - HIGH** | CI validation warns; template agent generates skeleton entries |
| R4 | Human confusion over metadata location | Medium (40%) | Medium | **5 - HIGH** | Clear documentation; two-location editing workflow guide |
| R5 | Hugo compatibility issues with custom templates | Medium (30%) | High | **5 - HIGH** | Test with Hugo versions 0.80+; provide fallback templates |
| R6 | Agent accidentally edits metadata file | Low (20%) | High | **4 - MEDIUM** | Directive 018 enforcement; validation checks commit history |
| R7 | Windows/IDE indexing problems | Medium (50%) | Low | **3 - MEDIUM** | Exclude `docs-site/content/` from IDE indexing; document workaround |
| R8 | CI build failures due to incorrect paths | Low (30%) | Medium | **3 - MEDIUM** | Path normalization validation; CI test on multiple runners |
| R9 | Validation tooling proves unsustainable | Low (20%) | Medium | **3 - MEDIUM** | Comprehensive test suite; versioned configuration; community support |
| R10 | Community rejects pattern as too complex | Medium (40%) | Low | **2 - LOW** | Optional adoption; standard front matter remains default |
| R11 | Metadata schema drift over time | Low (30%) | Low | **2 - LOW** | Schema versioning; migration scripts for schema changes |
| R12 | Hugo theme incompatibility | Low (20%) | Low | **1 - LOW** | Document custom template patterns; theme-agnostic approach |

---

## Detailed Risk Analysis

### R1: Symlink Failures on Windows (CRITICAL)

**Description:** Windows does not enable symlinks by default. Users without Developer Mode enabled will encounter broken symlinks, causing Hugo build failures and confusion.

**Probability:** High (70%)
- Windows 10/11 market share ~70% of desktop users
- Developer Mode not enabled by default
- Many developers unaware of symlink requirements

**Impact:** High
- Hugo build fails completely
- Users cannot preview docsite locally
- Frustration and abandonment of advanced profile
- Support burden increases

**Scenarios:**

1. **User clones repo without Developer Mode:**
   - Git converts symlinks to text files containing target path
   - Hugo reads text files as content → rendering errors
   - Build fails with cryptic error messages

2. **User enables Developer Mode after clone:**
   - Must run `git config core.symlinks true` and `git reset --hard HEAD`
   - Non-obvious recovery procedure
   - Risk of losing local changes

3. **Corporate environments with restricted Admin rights:**
   - Developer Mode requires Admin privileges in some Windows versions
   - Users cannot enable symlinks even if desired
   - Copy-based fallback becomes mandatory

**Mitigation Strategies:**

**Primary Mitigation: Copy-Based Fallback**
- Provide `sync-docs.sh` (Bash) and `sync-docs.ps1` (PowerShell) scripts
- Scripts copy `docs/` → `docs-site/content/docs/` (one-way sync)
- Optional watch mode for continuous sync during editing

**Sync Script Implementation:**
```powershell
# sync-docs.ps1
param([switch]$Watch)

$source = "docs/"
$dest = "docs-site/content/docs/"

function Sync-Docs {
    Write-Host "Syncing $source to $dest..."
    robocopy $source $dest /MIR /XD .git
}

Sync-Docs

if ($Watch) {
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $source
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true
    
    Register-ObjectEvent $watcher "Changed" -Action { Sync-Docs }
    Write-Host "Watching $source for changes... Press Ctrl+C to stop."
    
    while ($true) { Start-Sleep 1 }
}
```

**Documentation:**
- Clearly document symlink requirements in setup guide
- Provide step-by-step Developer Mode activation (with screenshots)
- Fallback procedure prominent in troubleshooting section
- Detection script to identify symlink status

**Detection Script:**
```bash
# scripts/check-symlinks.sh
if [ -L "docs-site/content/docs" ]; then
    echo "✅ Symlinks working correctly"
else
    echo "⚠️ Symlinks not working. Using copy-based fallback."
    echo "Run: scripts/sync-docs.sh"
fi
```

**CI Integration:**
- GitHub Actions: Explicitly test Windows runner behavior
- Workflow configures symlinks or falls back to copies
- Example workflow snippet:
  ```yaml
  - name: Setup symlinks (Windows)
    if: runner.os == 'Windows'
    run: |
      git config core.symlinks true
      git reset --hard HEAD
  ```

**Residual Risk:** Medium (30%)
- Users may not read documentation thoroughly
- Sync script requires manual execution
- Watch mode requires keeping script running

**Acceptance Criteria:**
- Copy-based fallback documented with clear instructions
- Sync scripts tested on Windows 10, 11, Server 2019
- Setup guide includes symlink detection script
- Troubleshooting section addresses symlink failures prominently

---

### R2: Metadata Drift (File Renamed, Metadata Stale) (CRITICAL)

**Description:** When files are renamed or moved, metadata keyed by old path becomes orphaned. New path has no metadata entry, leading to rendering with default/missing metadata.

**Probability:** High (60%)
- File renames common during refactoring
- Human error inevitable without automation
- Git mv does not trigger metadata update automatically

**Impact:** High
- Orphaned metadata clutters `docmeta.yaml`
- Renamed files render incorrectly (missing title, tags, menu placement)
- Navigation breaks (menu links point to old paths)
- Accumulation over time degrades docsite quality

**Scenarios:**

1. **Single file renamed:**
   - Developer: `git mv docs/old.md docs/new.md`
   - Metadata still keyed as `docs/old.md`
   - `docs/new.md` renders with default metadata (filename as title, no tags)

2. **Directory restructure:**
   - Developer: `git mv docs/old-section/ docs/new-section/`
   - All metadata keys under `docs/old-section/` orphaned
   - Entire section renders incorrectly

3. **File deleted without metadata cleanup:**
   - Developer: `git rm docs/obsolete.md`
   - Metadata entry remains in `docmeta.yaml`
   - Harmless but clutters metadata file over time

**Mitigation Strategies:**

**Primary Mitigation: Mandatory Validation in CI**
- CI workflow runs `validation/validate-docsite-metadata.py` on every commit
- Validation fails build if:
  - Orphaned metadata keys detected (ERROR)
  - Missing metadata for existing files (WARNING, configurable to ERROR)
- PR cannot merge until validation passes

**Validation Script Features:**
```python
# validation/validate-docsite-metadata.py

def check_file_coverage(content_dirs, metadata):
    """Check all markdown files have metadata entries."""
    files = find_markdown_files(content_dirs)
    missing = [f for f in files if f not in metadata]
    return missing

def check_metadata_validity(metadata, content_dirs):
    """Check all metadata keys reference existing files."""
    orphaned = [key for key in metadata if not file_exists(key)]
    return orphaned

def detect_rename_suggestions(orphaned, files):
    """Suggest renames based on filename similarity."""
    suggestions = []
    for old_path in orphaned:
        old_filename = os.path.basename(old_path)
        for new_path in files:
            new_filename = os.path.basename(new_path)
            if old_filename == new_filename:
                suggestions.append((old_path, new_path))
    return suggestions
```

**Curator Agent Automation:**
- Docsite Curator Agent runs weekly metadata audit
- Audit detects orphaned keys and missing entries
- Generates tasks for human review or automated fixes
- Logs drift metrics (entries added, updated, removed)

**Migration Script for Bulk Renames:**
```python
# scripts/migrate-metadata.py update-keys
# Reads git log for file renames
# Prompts user to confirm metadata key updates
# Applies updates in batch
```

**Pre-Commit Hook (Optional):**
- Detects file renames in staged commits
- Warns if metadata keys not updated
- User can abort commit to fix metadata first

**Documentation:**
- Prominently document rename workflow in setup guide
- Provide migration script usage examples
- Troubleshooting section for drift recovery

**Residual Risk:** Medium (30%)
- Bulk renames may slip through if validation disabled temporarily
- Human may override validation warnings incorrectly
- Migration script may not detect all rename patterns (e.g., content changes + rename)

**Acceptance Criteria:**
- CI validation detects 100% of orphaned keys in test scenarios
- Validation suggests likely renames based on filename matching
- Migration script successfully updates keys for bulk renames
- Curator agent audit detects drift within 7 days

---

### R3: Missing Metadata Entries for New Files (HIGH)

**Description:** Developers add new markdown files to `docs/` without creating corresponding metadata entries, resulting in files rendering with default metadata.

**Probability:** Medium (50%)
- Developers focus on content, may forget metadata
- No automatic metadata generation (requires manual entry)
- Workflow friction increases with two-location editing

**Impact:** Medium
- New files render with poor metadata (filename as title, no tags)
- Navigation incomplete (menu missing new entries)
- Search/filtering less effective (no tags)
- Cumulative issue if many files added without metadata

**Scenarios:**

1. **Quick documentation fix:**
   - Developer adds `docs/troubleshooting/fix.md` to resolve urgent issue
   - Commits immediately without metadata entry
   - File renders but missing from menu, untagged

2. **Batch content addition:**
   - Writer adds 10 new guides in `docs/tutorials/`
   - Adds 3 metadata entries, forgets remaining 7
   - Tutorials section partially navigable

3. **Generated documentation:**
   - Automated tool generates API reference files
   - Tool unaware of metadata requirement
   - All generated files missing metadata

**Mitigation Strategies:**

**Primary Mitigation: CI Validation Warnings**
- Validation script detects missing metadata entries
- CI build **warns** (not fails) on missing metadata
- Configurable to fail build if strictness desired

**Template Agent Generates Skeleton Entries:**
- Automated agent scans for new files without metadata
- Generates default metadata entries:
  ```yaml
  docs/new-file.md:
    title: "New File"  # Derived from filename
    tags: []  # Empty, requires human input
    section: "Uncategorized"  # Placeholder
    weight: 999  # Bottom of list
  ```
- Creates PR or task for human to review and enhance

**Metadata Entry Template:**
```yaml
# Template for new entry (copy-paste into docmeta.yaml)
docs/path/to/new-file.md:
  title: ""  # Required: Human-readable title
  description: ""  # Optional: SEO summary
  tags: []  # Required: List of tags
  section: ""  # Required: Section name
  weight: 10  # Optional: Ordering (lower = higher priority)
  menu:
    main:
      parent: ""  # Optional: Parent menu item
```

**Documentation:**
- Workflow guide includes metadata creation step
- Checklist for adding new files:
  - [ ] Create markdown file in `docs/`
  - [ ] Add metadata entry to `docs-site/data/docmeta.yaml`
  - [ ] Validate with `make validate-docsite`
  - [ ] Preview with Hugo dev server

**PR Review Checklist:**
- Reviewers check for metadata entries in PRs adding files
- GitHub Actions comment reminds author if missing metadata detected

**Residual Risk:** Low (20%)
- Template agent catches most missing entries
- Validation warnings visible in CI logs
- Human reviewers provide safety net

**Acceptance Criteria:**
- Validation script detects 100% of missing metadata entries
- Template agent generates skeleton entries within 24 hours
- Documentation includes clear workflow for adding files
- PR review checklist includes metadata verification

---

### R4: Human Confusion Over Metadata Location (HIGH)

**Description:** Developers accustomed to front matter in files may be confused by external metadata file. Two-location editing increases cognitive overhead.

**Probability:** Medium (40%)
- Separated metadata is non-standard pattern
- Onboarding documentation may be skipped
- Muscle memory from other projects (standard front matter)

**Impact:** Medium
- Developers edit wrong files (add front matter to content files)
- Metadata entries created in wrong location
- Support requests increase
- Frustration and reduced adoption

**Scenarios:**

1. **New contributor adds front matter:**
   - Developer familiar with Jekyll/Hugo adds YAML front matter to markdown file
   - Hugo ignores front matter (custom templates lookup metadata file)
   - File renders incorrectly, developer confused

2. **Developer edits metadata in wrong file:**
   - Developer searches for "title: Foo" in repo
   - Expects result in markdown file, doesn't find it
   - Unaware of `docmeta.yaml` location

3. **Reviewer misses metadata in PR:**
   - PR adds new file with metadata entry
   - Reviewer checks markdown file, sees no front matter
   - Approves without verifying metadata correctness

**Mitigation Strategies:**

**Primary Mitigation: Clear Documentation**
- Setup guide prominently explains separated metadata pattern
- Visual diagram showing content vs. metadata locations:
  ```
  Content Files (docs/):           Metadata File (docs-site/data/):
  ┌─────────────────────┐         ┌─────────────────────────┐
  │ # My Document       │         │ docs/my-doc.md:         │
  │                     │  ←────→ │   title: "My Document"  │
  │ Content starts...   │         │   tags: [guide]         │
  └─────────────────────┘         └─────────────────────────┘
  ```

**Two-Location Editing Workflow Guide:**
1. **Edit content:** `docs/path/to/file.md` (markdown only, no front matter)
2. **Edit metadata:** `docs-site/data/docmeta.yaml` (find entry keyed by filepath)
3. **Validate:** `make validate-docsite` (check sync)
4. **Preview:** `hugo server --source docs-site/` (see rendered output)

**Onboarding Checklist:**
- Required reading: Advanced Docsite Setup guide
- Hands-on exercise: Add new file + metadata entry
- Validation test: Run validation script, interpret output

**IDE Configuration Guide:**
- VS Code: Snippets for metadata entry creation
- JetBrains: Exclude `docs-site/content/` from indexing (avoid symlink confusion)
- Vim/Emacs: Functions to jump between file and metadata entry

**Front Matter Detection in Validation:**
- Validation script warns if markdown files contain YAML front matter
- Suggests removing front matter and migrating to `docmeta.yaml`

**Residual Risk:** Low (20%)
- Comprehensive documentation reduces confusion
- Validation catches incorrect edits
- Community support and examples reinforce pattern

**Acceptance Criteria:**
- Setup guide includes workflow diagram and step-by-step instructions
- Validation script detects and warns on front matter in content files
- IDE configuration guide tested with popular editors
- Onboarding feedback confirms understanding within 1-2 hours

---

### R5: Hugo Compatibility Issues with Custom Templates (HIGH)

**Description:** Custom Hugo templates for metadata lookup may be incompatible with future Hugo versions or specific Hugo features.

**Probability:** Medium (30%)
- Hugo evolves with breaking changes (rare but possible)
- Custom templates bypass standard Hugo mechanisms
- Symlink handling may change in future versions

**Impact:** High
- Docsite build fails after Hugo upgrade
- Custom templates require rewrite
- Users blocked until templates updated
- Maintenance burden on template maintainers

**Scenarios:**

1. **Hugo breaks `.File.Path` behavior:**
   - Hugo changes how symlinked file paths are reported
   - Templates keying metadata by `.File.Path` fail to lookup
   - Entire site renders with default metadata

2. **Hugo deprecates `followSymlinks` config:**
   - Future version removes symlink support
   - Docsite build fails to find content
   - Migration to copies required

3. **Template syntax changes:**
   - Hugo updates Go template engine with breaking changes
   - Custom metadata lookup logic invalid
   - Build fails with syntax errors

**Mitigation Strategies:**

**Primary Mitigation: Test with Multiple Hugo Versions**
- CI matrix tests Hugo 0.80.0, 0.110.0, latest stable
- Document minimum required Hugo version (e.g., 0.80.0+)
- Pin Hugo version in `netlify.toml` or CI config

**Fallback Template Patterns:**
- Provide multiple template approaches:
  1. **Primary:** Metadata lookup from `data/docmeta.yaml`
  2. **Fallback 1:** Hybrid (minimal front matter + extended metadata)
  3. **Fallback 2:** Standard front matter (full compatibility)

**Template Versioning:**
- Version custom templates (e.g., `v1.0.0`)
- Changelog tracks Hugo compatibility
- Migration guide for template updates

**Hugo Theme Agnosticism:**
- Custom templates extend `baseof.html` from any theme
- Metadata lookup in `layouts/_default/`, not theme-specific
- Tested with popular themes (Docsy, Book, Paper)

**Community Engagement:**
- Monitor Hugo release notes for breaking changes
- Participate in Hugo community discussions
- Report symlink or template issues upstream

**Documentation:**
- Explicitly document Hugo version requirements
- Troubleshooting section for Hugo upgrade issues
- Contact info for template maintainers

**Residual Risk:** Low (20%)
- Hugo rarely introduces breaking changes
- Fallback patterns provide flexibility
- Community support mitigates issues

**Acceptance Criteria:**
- Custom templates tested with Hugo 0.80+, 0.110+, latest
- Documentation specifies minimum Hugo version
- Fallback template patterns documented
- CI matrix tests multiple Hugo versions

---

### R6: Agent Accidentally Edits Metadata File (MEDIUM)

**Description:** Content-focused agents (Writer, Researcher) accidentally edit `docs-site/data/docmeta.yaml` instead of content files, corrupting metadata.

**Probability:** Low (20%)
- Agents follow directives restricting metadata access
- Validation catches corruption quickly
- Clear agent profiles reduce confusion

**Impact:** High
- Metadata corruption breaks docsite rendering
- Manual recovery required
- Trust in agent automation reduced
- Validation rollback needed

**Scenarios:**

1. **Agent instructed to "update all tags":**
   - Agent interprets as editing `docmeta.yaml`
   - Accidentally removes required fields
   - Validation fails build

2. **Agent adds front matter to markdown file:**
   - Agent unaware of separated metadata pattern
   - Adds YAML front matter thinking it's required
   - Hugo ignores front matter, rendering incomplete

3. **Agent creates duplicate metadata entries:**
   - Agent adds metadata entry without checking existing
   - Multiple entries for same file cause Hugo errors

**Mitigation Strategies:**

**Primary Mitigation: Directive Enforcement**
- Update Directive 018 (Decision Capture Protocols):
  > "Content agents MUST NOT edit `docs-site/data/docmeta.yaml`. Metadata modifications are the sole responsibility of the Docsite Curator Agent."

**Agent Profile Updates:**
- Content agent profiles (Writer, Researcher, Architect) exclude metadata file from context
- Invocation specifies context directories: `docs/**/*.md`, `.github/agents/**/*.md`
- Explicitly exclude: `docs-site/data/*`

**Validation Post-Execution:**
- Check agent work logs for file modifications
- Validate: if agent modified `docmeta.yaml` and is not Docsite Curator, flag for review
- CI check inspects commit author; warns if non-curator edited metadata

**Commit Message Convention:**
- Metadata commits include prefix: `[metadata]` or `[curator]`
- CI validation checks commits modifying `docmeta.yaml` have correct prefix
- Alerts if content agent committed metadata changes

**Rollback Mechanism:**
- Git history preserves all metadata versions
- Rollback script: `git revert <commit>` if metadata corruption detected
- Validation runs before merge, catches corruption early

**Residual Risk:** Very Low (10%)
- Directive enforcement strong
- Validation catches corruption immediately
- Git history enables easy rollback

**Acceptance Criteria:**
- Directive 018 updated with metadata restriction clause
- Content agent profiles exclude `docs-site/data/` from context
- Validation script checks commit history for unauthorized edits
- Rollback procedure documented in troubleshooting guide

---

### R7: Windows/IDE Indexing Problems (MEDIUM)

**Description:** JetBrains IDEs and Windows Explorer may handle symlinks poorly, causing indexing errors, duplicate file displays, or performance degradation.

**Probability:** Medium (50%)
- JetBrains IDEs historically poor symlink support
- Windows Explorer shows symlinks as shortcuts (confusing UI)
- Indexing may traverse symlinks, duplicating files

**Impact:** Low
- IDE performance degraded (longer indexing times)
- Duplicate file results in search
- Confusing UI (same file appears twice)
- Developer annoyance but not blocking

**Scenarios:**

1. **JetBrains IDE indexes symlinked content:**
   - IDE indexes `docs/` AND `docs-site/content/docs/` (symlink)
   - File search returns duplicate results
   - "Go to File" command shows same file twice

2. **Windows Explorer displays symlinks as shortcuts:**
   - Developer navigates to `docs-site/content/docs/`
   - Sees shortcut icon instead of directory
   - Confusion about whether content is "real" or linked

3. **Git client GUI confusion:**
   - GUI tools (GitKraken, SourceTree) show symlinks inconsistently
   - Changes in `docs/` may not reflect in `docs-site/content/docs/` view
   - Developer unsure which location to edit

**Mitigation Strategies:**

**Primary Mitigation: IDE Configuration**
- Exclude `docs-site/content/` from indexing in JetBrains IDEs
- `.idea/vcs.xml` configuration:
  ```xml
  <component name="VcsDirectoryMappings">
    <mapping directory="$PROJECT_DIR$" vcs="Git" />
    <mapping directory="$PROJECT_DIR$/docs-site/content" vcs="" />
  </component>
  ```
- VS Code `.vscode/settings.json`:
  ```json
  {
    "search.exclude": {
      "docs-site/content": true
    },
    "files.watcherExclude": {
      "docs-site/content/**": true
    }
  }
  ```

**Documentation:**
- IDE configuration guide for IntelliJ IDEA, PyCharm, WebStorm, VS Code
- Explain why `docs-site/content/` should be excluded
- Provide configuration snippets (copy-paste)

**Fallback for Windows Users:**
- Copy-based approach eliminates symlinks entirely
- Sync script keeps directories in sync
- No IDE indexing issues with copies

**Git Configuration:**
- `.gitignore` entry for `docs-site/content/` (symlinked directories ignored by default)
- Prevents accidental commits of symlink targets

**Residual Risk:** Very Low (10%)
- IDE configuration solves problem completely
- Copy-based fallback eliminates symlinks for affected users

**Acceptance Criteria:**
- IDE configuration tested with IntelliJ IDEA 2023+, VS Code 1.80+
- Documentation includes configuration steps with screenshots
- Validation: Open project in IDE, verify no duplicate files in search

---

### R8: CI Build Failures Due to Incorrect Paths (MEDIUM)

**Description:** Hugo templates fail to lookup metadata due to path mismatches (absolute vs. relative, forward vs. backslash, trailing slashes).

**Probability:** Low (30%)
- Path normalization in validation reduces risk
- Hugo uses forward slashes internally
- Manual path entry prone to errors

**Impact:** Medium
- Hugo build fails or renders pages incorrectly
- CI pipeline blocks merge
- Developer frustration debugging path issues

**Scenarios:**

1. **Windows-style paths in metadata:**
   - Developer on Windows adds metadata entry: `docs\path\file.md`
   - Hugo template expects forward slashes: `docs/path/file.md`
   - Lookup fails, file renders with default metadata

2. **Absolute paths in metadata:**
   - Developer mistakenly keys metadata with absolute path: `/home/user/repo/docs/file.md`
   - Hugo `.File.Path` returns relative path: `docs/file.md`
   - Lookup fails

3. **Trailing slashes inconsistency:**
   - Metadata key: `docs/section/` (with trailing slash)
   - File path: `docs/section` (no trailing slash)
   - Lookup fails due to mismatch

**Mitigation Strategies:**

**Primary Mitigation: Path Normalization Validation**
- Validation script checks all metadata keys for:
  - Forward slashes (not backslashes)
  - Relative paths (not absolute)
  - No trailing slashes
  - Consistent with filesystem paths

**Path Normalization Function:**
```python
def normalize_path(path):
    """Normalize path to forward slashes, relative, no trailing slash."""
    path = path.replace('\\', '/')  # Windows backslashes → forward slashes
    path = path.lstrip('/')  # Remove leading slash (absolute → relative)
    path = path.rstrip('/')  # Remove trailing slash
    return path
```

**Hugo Template Robustness:**
```go-template
{{ $relPath := strings.TrimPrefix "content/" .File.Path }}
{{ $relPath = strings.TrimSuffix "/" $relPath }}
{{ $relPath = replace $relPath "\\" "/" }}
{{ $metadata := index .Site.Data.docmeta $relPath }}
```

**CI Test on Multiple Platforms:**
- GitHub Actions matrix: ubuntu-latest, windows-latest, macos-latest
- Verify Hugo build succeeds on all platforms
- Catch platform-specific path issues early

**Documentation:**
- Metadata entry guidelines specify path format
- Examples show correct relative paths with forward slashes

**Residual Risk:** Very Low (5%)
- Validation enforces correct paths
- Template normalization provides safety net
- CI tests catch platform issues

**Acceptance Criteria:**
- Validation script rejects Windows-style paths (backslashes)
- Validation script rejects absolute paths
- Hugo templates normalize paths before lookup
- CI builds successfully on Linux, Windows, macOS

---

### R9: Validation Tooling Proves Unsustainable (MEDIUM)

**Description:** Validation script requires frequent maintenance due to changing requirements, Hugo updates, or repo structure evolution.

**Probability:** Low (20%)
- Well-designed validation tooling is stable
- Comprehensive test suite reduces breakage risk
- Configuration file allows adaptation without code changes

**Impact:** Medium
- Validation script breaks, CI pipeline fails
- Manual validation required until fix
- Maintenance burden discourages adoption
- Pattern abandoned if unsustainable

**Scenarios:**

1. **Repo structure changes:**
   - New directory added to `docs/` that should be excluded from metadata
   - Validation script not updated, reports false positives
   - CI fails on every commit

2. **Metadata schema evolves:**
   - New required field added (e.g., `audience`)
   - Validation script not updated to check field
   - Schema violations go undetected

3. **Hugo updates break assumptions:**
   - Hugo changes `.File.Path` format in new version
   - Validation script keying logic incompatible
   - Massive false positives reported

**Mitigation Strategies:**

**Primary Mitigation: Comprehensive Test Suite**
- Pytest suite for validation script with fixtures:
  - Missing metadata entries (false negatives)
  - Orphaned metadata keys (false positives)
  - Schema violations (missing fields, wrong types)
  - Path normalization (backslashes, absolute paths)
- Test coverage >90%

**Configuration-Driven Design:**
- Validation rules in `docsite-metadata-config.yaml`:
  ```yaml
  validation:
    content_directories:
      - docs/
      - .github/agents/
    exclude_patterns:
      - docs/templates/
      - docs/drafts/
    metadata_file: docs-site/data/docmeta.yaml
    required_fields:
      - title
      - tags
      - section
    optional_fields:
      - description
      - audience
      - weight
  ```
- Changes to rules require config update, not code changes

**Versioned Validation Script:**
- Semantic versioning (e.g., v1.0.0)
- Changelog documents breaking changes
- Migration guide for config updates

**Community Support Model:**
- Validation script open source (MIT license)
- Community contributions welcome
- Issue tracker for bug reports and feature requests
- Monthly review of issues by maintainer

**Monitoring Maintenance Burden:**
- Track time spent on validation script maintenance
- Threshold: >4 hours/quarter triggers reassessment
- If unsustainable, simplify or provide alternative

**Residual Risk:** Very Low (10%)
- Configuration-driven design minimizes code changes
- Test suite catches breakage early
- Community support distributes maintenance burden

**Acceptance Criteria:**
- Pytest suite with >90% coverage
- Configuration file documented with all options
- Validation script versioned with changelog
- Maintenance burden tracked quarterly

---

### R10: Community Rejects Pattern as Too Complex (LOW)

**Description:** Users find separated metadata architecture too complex for their needs, preferring standard front matter simplicity.

**Probability:** Medium (40%)
- Separated metadata is non-standard, unfamiliar
- Setup overhead significant (symlinks, validation, Hugo config)
- Value proposition unclear for small projects

**Impact:** Low
- Low adoption of advanced profile
- Wasted effort documenting pattern
- Standard front matter remains dominant
- Pattern maintained but underutilized

**Scenarios:**

1. **New user evaluates template:**
   - Sees advanced docsite setup documentation
   - Perceives as too complex for getting started
   - Chooses simpler template or standard front matter

2. **User attempts setup, encounters issues:**
   - Windows symlink problems frustrate developer
   - Gives up, reverts to standard front matter
   - Leaves negative feedback

3. **Team discusses adoption:**
   - Benefits (token savings) seem marginal
   - Costs (maintenance, onboarding) seem high
   - Decision: not worth the complexity

**Mitigation Strategies:**

**Primary Mitigation: Optional Adoption**
- Position as **advanced profile**, not default
- Standard front matter remains recommended baseline
- Clear documentation of when to use separated metadata:
  - High agent workload (>100 agent sessions/month)
  - Large documentation set (>100 files)
  - Frequent doc re-reading by agents
  - Token economy is priority

**Value Proposition Clarity:**
- Executive summary quantifies benefits (2-7% context window savings)
- Use cases documented with real-world examples
- Comparison table: standard vs. separated metadata

**Gradual Adoption Path:**
- Phase 1: Use standard front matter initially
- Phase 2: Migrate to hybrid (minimal front matter)
- Phase 3: Adopt separated metadata when benefits justify

**Community Feedback Loop:**
- Gather feedback from early adopters
- Iterate documentation based on pain points
- Feature adoption metrics (how many users opt-in)
- Sunset pattern if adoption <10% after 12 months

**Residual Risk:** Very Low (5%)
- Optional adoption eliminates pressure
- Standard front matter remains viable
- No negative impact if pattern unused

**Acceptance Criteria:**
- Documentation clearly positions pattern as optional advanced profile
- Value proposition quantified with metrics
- Feedback mechanism in place for early adopters
- Adoption tracked and reviewed quarterly

---

### R11: Metadata Schema Drift Over Time (LOW)

**Description:** As docsite evolves, metadata schema changes (new fields added, old fields deprecated), requiring migration of existing entries.

**Probability:** Low (30%)
- Schema changes infrequent (1-2 times/year)
- Backward compatibility usually maintained
- Optional fields reduce breaking changes

**Impact:** Low
- Migration script needed for schema updates
- Some manual review required
- Temporary inconsistency during migration
- Manageable with planning

**Scenarios:**

1. **New required field added:**
   - Schema update adds `audience` as required field
   - Existing 100+ entries missing field
   - Validation fails on all entries until migrated

2. **Field renamed for clarity:**
   - `tags` renamed to `categories`
   - Hugo templates updated to use new field
   - Old entries break until migrated

3. **Field type changes:**
   - `weight` was string, now integer
   - Template expects integer for sorting
   - String weights fail comparison

**Mitigation Strategies:**

**Primary Mitigation: Schema Versioning**
- Metadata file includes schema version:
  ```yaml
  schema_version: "1.0.0"
  documents:
    docs/file.md:
      title: "Title"
      # ...
  ```

**Migration Script:**
```python
# scripts/migrate-metadata.py upgrade-schema
# Reads current schema version
# Applies migrations to reach target version
# Validates result
```

**Backward Compatibility:**
- Hugo templates support both old and new field names
- Fallback logic: `{{ $metadata.tags | default $metadata.categories }}`
- Deprecated fields logged as warnings, not errors

**Deprecation Policy:**
- Announce schema changes 1 month in advance
- Provide migration script before enforcement
- Deprecated fields supported for 6 months
- Remove only after community notice

**Documentation:**
- Schema changelog documents all changes
- Migration guide for each schema version
- Automated migration script tested on real data

**Residual Risk:** Very Low (5%)
- Schema changes infrequent and planned
- Migration scripts automate updates
- Backward compatibility reduces breakage

**Acceptance Criteria:**
- Schema versioning implemented in metadata file
- Migration script handles version upgrades
- Hugo templates support deprecated fields with fallback
- Deprecation policy documented

---

### R12: Hugo Theme Incompatibility (LOW)

**Description:** Popular Hugo themes expect front matter in content files; custom metadata lookup incompatible with theme templates.

**Probability:** Low (20%)
- Many users choose standard themes for simplicity
- Custom templates override theme behavior
- Themes vary in architecture

**Impact:** Low
- Users must modify theme templates
- Limits theme ecosystem compatibility
- Increased setup complexity
- Theme updates may break customizations

**Scenarios:**

1. **User applies popular theme (Docsy):**
   - Theme templates expect front matter fields
   - Metadata lookup not integrated
   - Pages render with incomplete/incorrect metadata

2. **User updates theme:**
   - Theme update overwrites custom templates
   - Metadata lookup logic lost
   - Docsite breaks until templates restored

3. **User switches themes:**
   - New theme has different template structure
   - Metadata lookup logic must be adapted
   - Significant rework required

**Mitigation Strategies:**

**Primary Mitigation: Theme-Agnostic Templates**
- Custom templates in `layouts/_default/` override theme templates
- Metadata lookup in overrides, not theme modifications
- Theme can be changed without affecting metadata logic

**Theme Compatibility Documentation:**
- Document tested themes (Docsy, Book, Paper)
- Provide override templates for each
- Explain how to adapt pattern to new themes

**Hybrid Approach:**
- Minimal front matter (title) in content files
- Theme uses front matter title if present
- Extended metadata in `docmeta.yaml` for custom fields

**Theme Update Workflow:**
- Custom templates in version control
- Theme updates don't overwrite custom layouts
- `.gitignore` excludes theme files if using submodule

**Residual Risk:** Very Low (5%)
- Theme-agnostic design minimizes impact
- Override templates survive theme updates
- Documentation guides theme customization

**Acceptance Criteria:**
- Custom templates tested with Docsy, Book, Paper themes
- Documentation explains theme compatibility
- Override templates survive theme updates
- Hybrid approach documented as fallback

---

## Risk Mitigation Priority

**Immediate Action (Critical Risks):**
1. **R1: Symlink failures on Windows** → Implement copy-based fallback, document Developer Mode
2. **R2: Metadata drift** → Mandatory CI validation, Curator agent audits, migration script

**Phase 1 Implementation (High Risks):**
3. **R3: Missing metadata entries** → CI warnings, template agent skeleton generation
4. **R4: Human confusion** → Comprehensive documentation, workflow guide, visual diagrams
5. **R5: Hugo compatibility** → Multi-version testing, fallback templates, version pinning

**Phase 2 Monitoring (Medium Risks):**
6. **R6: Agent edits metadata** → Directive enforcement, validation post-execution
7. **R7: IDE indexing** → IDE configuration guide, exclusion rules
8. **R8: Path issues** → Path normalization validation, template robustness
9. **R9: Validation unsustainable** → Comprehensive test suite, configuration-driven design

**Ongoing Tracking (Low Risks):**
10. **R10: Community rejection** → Optional adoption, feedback loop, adoption metrics
11. **R11: Schema drift** → Schema versioning, migration scripts, backward compatibility
12. **R12: Theme incompatibility** → Theme-agnostic templates, documentation

---

## Monitoring and Review

**Quarterly Risk Review:**
- Assess actual vs. predicted probability/impact
- Update mitigation strategies based on real-world usage
- Identify new risks emerging from pattern adoption

**Metrics to Track:**
- Symlink failure rate (Windows users)
- Metadata drift incidents (orphaned keys, missing entries)
- Validation script maintenance hours/quarter
- Adoption rate (% of template users opting in)
- Support requests related to separated metadata

**Risk Escalation:**
- If any risk severity increases to Critical, halt new adoptions pending mitigation
- If maintenance burden >8 hours/quarter, reassess pattern viability
- If adoption <10% after 12 months, consider deprecation

---

_Prepared by: Architect Alphonso_  
_Related Documents: [ADR-022](../adrs/ADR-022-docsite-separated-metadata.md) | [Feasibility Study](docsite-metadata-separation-feasibility-study.md) | [Implementation Plan](../design/docsite-metadata-separation-implementation-plan.md)_  
_Version: 1.0.0_  
_Last Updated: 2025-12-04_
