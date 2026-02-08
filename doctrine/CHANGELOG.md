# Doctrine Changelog - SDD Agentic Framework

All notable changes to the doctrine framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Note:** Repository-specific changes (code structure, tooling) are documented in the [root CHANGELOG.md](../CHANGELOG.md).

---

## [Unreleased]

### Phase 1: Doctrine Extraction & Portability (2026-02-08)

#### Added
- **`doctrine/` directory** - Standalone, portable framework with zero external dependencies
- **`doctrine/DOCTRINE_MAP.md`** - Comprehensive navigation guide for all 201 framework files
- **`doctrine/DOCTRINE_STACK.md`** - Five-layer architecture documentation
- **`doctrine/GLOSSARY.md`** - Centralized terminology reference
- **`doctrine/templates/`** - Canonical template location (80 templates)
- **`doctrine/templates/automation/doctrine-config-template.yaml`** - Path configuration template
- **Path parameterization** - All files use `${WORKSPACE_ROOT}`, `${DOC_ROOT}`, `${SPEC_ROOT}`, `${OUTPUT_ROOT}` for portability
- **Bootstrap Bill doctrine setup** - Automatically creates `.doctrine/config.yaml` during repository initialization

#### Changed
- **BREAKING:** Agent profiles context sources now reference `doctrine/` instead of `.github/agents/`
- **Moved:** All templates from `doctrine/docs/templates/` to `doctrine/templates/` (canonical location per architecture)
- **Renamed:** `prompts/` → `doctrine/shorthands/` (clarifies purpose as reusable command aliases)
- **Updated:** All 20 agent profiles to use doctrine paths
- **Updated:** All directives, approaches, guidelines, tactics to use parameterized paths
- **Updated:** 38 files with template path references

#### Removed
- **Symlink:** `./agents` (deprecated, pointed to old `.github/agents/`)
- **External dependencies:** All outgoing references from doctrine/ eliminated

#### Migration Details

**Phase 1a: Zero-dependency content (46 files)**
- Tactics: 20 files (ready for subtree distribution)
- Clean agents: 8 files (Alphonso, Annie, Benny, etc.)
- Clean directives: 11 files
- Clean approaches: 7 files + subdirectories

**Phase 1b: Parameterized content (155 files)**
- Agents: 12 remaining profiles (all parameterized)
- Approaches: 27 files (all parameterized)
- Directives: 18 files (all parameterized)
- Guidelines: 5 files (all parameterized)
- Templates: 80 files (moved to canonical location)
- Shorthands: 3 files (renamed from prompts/)
- Reference docs: 4 comparative studies

**Validation:**
- Created `ops/scripts/validate-doctrine-dependencies.sh` (6 validation checks)
- All checks passing (excluding expected documentation references)
- Curator Claire consistency audit: Grade A- (Excellent, production-ready)

#### Documentation

**Added:**
- `doctrine/DOCTRINE_MAP.md` - Quick navigation, file catalog, path parameterization guide
- `doctrine/templates/automation/doctrine-config-template.yaml` - Configuration template for consuming repos
- Updated `specific_guidelines.md` with Glossary update requirement and bootstrap requirements

**Updated:**
- Bootstrap Bill profile with doctrine configuration responsibilities
- All agent profiles with new context source paths
- `templates/automation/README.md` with template catalog

#### Architecture

**Five-Layer Doctrine Stack:**
1. **Guidelines** (values, preferences) - Highest precedence
2. **Approaches** (mental models, philosophies)
3. **Directives** (instructions, constraints)
4. **Tactics** (procedural execution guides)
5. **Templates** (output structure contracts) - Lowest precedence

**Path Parameterization Pattern:**
```yaml
# .doctrine/config.yaml
paths:
  workspace_root: "work"           # ${WORKSPACE_ROOT}
  doc_root: "docs"                 # ${DOC_ROOT}
  spec_root: "specifications"      # ${SPEC_ROOT}
  output_root: "output"            # ${OUTPUT_ROOT}
```

#### Distribution Readiness

Doctrine is now ready for:
- **Git subtree distribution:** `git subtree split --prefix=doctrine -b doctrine-main`
- **Standalone consumption:** Zero dependencies on parent repository
- **Multi-repository deployment:** Path variables allow customization per repo
- **Tool integration:** Supports GitHub Copilot, Claude, Cursor, OpenCode

**Commits:** 26 commits from initial extraction through Phase 1 completion (up to 22b17ee)

---

## Version Strategy

**Doctrine versioning** (independent of repository):
- **Major (X.0.0):** Breaking changes to directive contracts, approach signatures, agent interfaces
- **Minor (0.X.0):** New directives, approaches, agents; backward-compatible additions
- **Patch (0.0.X):** Clarifications, typo fixes, documentation improvements

**Current Status:** Unreleased (Phase 1 complete, awaiting Phase 2 tooling)

---

## Future Phases

### Phase 2: Doctrine Tooling (Planned)
- Exporters: doctrine/ → `.github/instructions/`, `.claude/skills/`
- Update existing exporters to read from doctrine/
- Create `doctrine/README.md` with usage instructions
- Update `AGENTS.md` to reference doctrine/

### Phase 3: Multi-Repository Testing (Planned)
- Test doctrine distribution to downstream repositories
- Validate `.doctrine/config.yaml` path overrides
- Document integration patterns for consuming repositories

---

## Notes

- **Zero external dependencies:** Doctrine must never reference files outside `doctrine/`
- **Path parameterization:** All file references use `${VARIABLE}` syntax
- **Bootstrap requirement:** Bootstrap Bill MUST create `.doctrine/config.yaml` during repo setup
- **Glossary discipline:** New terms MUST be added to `doctrine/GLOSSARY.md`
- **Template canonical location:** `doctrine/templates/` (not `doctrine/docs/templates/`)
