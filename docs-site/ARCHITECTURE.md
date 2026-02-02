# Documentation Site Architecture

**Version**: 1.0.0  
**Last Updated**: 2026-01-31  
**Status**: ✅ Initial Implementation  
**Related**: `work/analysis/docsite-technology-selection.md`, `ADR-022-docsite-separated-metadata.md`

---

## Overview

This document describes the architecture, design decisions, and organizational principles for the Quickstart Agent-Augmented Development Framework documentation website.

### Purpose

The documentation site serves as the primary knowledge hub for:
- **New Users**: Onboarding, installation, quick start
- **Active Users**: How-to guides, troubleshooting, best practices
- **Process Architects**: Architecture patterns, ADRs, governance
- **Contributors**: Development guides, contribution workflows

### Goals

1. **Accessibility**: Users find answers in <3 clicks
2. **Performance**: Site builds in <5 seconds (target: <1s)
3. **Maintainability**: Content updates require minimal technical overhead
4. **Extensibility**: Easy to add new content types and features
5. **Quality**: Professional presentation befitting enterprise adoption

---

## Technology Stack

### Core Components

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Static Site Generator** | Hugo | v0.140.1+ | Fast builds (<1s), zero dependencies, corporate theme ready |
| **Theme** | Hugo Book | Latest | Documentation-focused, clean, mobile-responsive |
| **Hosting** | GitHub Pages | N/A | Zero cost, tight GitHub integration, reliable |
| **Deployment** | GitHub Actions | N/A | Automated builds, version control integration |
| **Search** | Hugo Built-in | N/A | JSON index, client-side search (no backend required) |

### Technology Selection

**Decision**: Hugo over Jekyll/MkDocs/Docusaurus

**Key Factors**:
- ⚡ **Build Speed**: 50-100x faster than Jekyll (0.7s vs 32s for 200 pages)
- 🔧 **Dependencies**: Single binary vs Ruby/Python/Node ecosystem
- 🎨 **Corporate Theme**: Existing Hugo theme available for future branding
- 📋 **ADR-022 Support**: Native `followSymlinks` for separated metadata (optional)

See `work/analysis/docsite-technology-selection.md` for comprehensive evaluation.

---

## Site Structure

### Directory Organization

```
docs-site/
├── archetypes/          # Content templates for new files
├── assets/              # SASS/SCSS, images, fonts
├── content/             # Markdown content (main documentation)
│   ├── _index.md        # Homepage
│   ├── getting-started/ # Onboarding content
│   ├── guides/          # How-to guides (migrated from docs/HOW_TO_USE)
│   ├── architecture/    # ADRs, patterns, design docs
│   ├── reference/       # API docs, agent profiles, configuration
│   └── contributing/    # Contribution guidelines
├── data/                # Data files (YAML/JSON/TOML)
│   └── docmeta.yaml     # (Optional) Separated metadata for ADR-022
├── layouts/             # Custom templates (overrides theme)
├── static/              # Static assets (images, CSS, JS)
├── themes/              # Hugo themes (git submodules)
│   └── hugo-book/       # Current theme
├── hugo.toml            # Site configuration
├── ARCHITECTURE.md      # This file
└── README.md            # Contributor quick start
```

### Content Organization Strategy

#### Primary Sections

1. **Getting Started** (`/getting-started/`)
   - Quick start guide (<5 minutes to first agent task)
   - Installation instructions
   - Framework concepts overview
   - First agent interaction tutorial

2. **Guides** (`/guides/`)
   - Task-oriented how-to guides
   - Migrated content from `docs/HOW_TO_USE/`
   - Troubleshooting and common issues
   - Best practices and patterns

3. **Architecture** (`/architecture/`)
   - Architecture Decision Records (ADRs)
   - Design patterns and anti-patterns
   - System design principles
   - Integration guidance

4. **Reference** (`/reference/`)
   - Agent profile reference
   - Configuration options
   - API documentation (if applicable)
   - Glossary and terminology

5. **Contributing** (`/contributing/`)
   - How to contribute to framework
   - Documentation contribution guide
   - Code standards and testing
   - Release process

#### Content Hierarchy

```
Homepage
  ├─ Getting Started (linear onboarding flow)
  │   ├─ Quickstart (5 min)
  │   ├─ Installation
  │   ├─ Core Concepts
  │   └─ First Task Tutorial
  │
  ├─ Guides (task-oriented, searchable)
  │   ├─ CI/CD Integration
  │   ├─ Agent Orchestration
  │   ├─ Custom Agents
  │   └─ [19 HOW_TO_USE guides]
  │
  ├─ Architecture (deep dives, governance)
  │   ├─ ADRs (decision records)
  │   ├─ Patterns (reusable solutions)
  │   └─ Design Principles
  │
  ├─ Reference (lookup documentation)
  │   ├─ Agent Profiles
  │   ├─ Configuration Reference
  │   └─ Glossary
  │
  └─ Contributing (community guidance)
      ├─ Code Contributions
      ├─ Documentation
      └─ Issue Reporting
```

---

## Navigation Design

### Primary Navigation

**Top Menu** (Hugo Book theme sidebar):
- Home
- Getting Started
- Guides
- Architecture
- Reference
- Contributing

### Secondary Navigation

**Within-Page TOC**: Automatically generated from headings (h2-h4)

**Breadcrumbs**: Section → Subsection → Page

**Related Content**: Manual cross-links in front matter (future enhancement)

### Search

**Implementation**: Hugo built-in JSON search index
- **Index**: Generated at build time (`index.json`)
- **Client-Side**: JavaScript search (no backend required)
- **Scope**: All content indexed by default
- **Weighting**: Title > Description > Content

---

## Content Management

### Authoring Workflow

1. **Create/Edit Content**:
   - Write markdown in `content/` directory
   - Follow content style guide (TBD in Batch 2)
   - Add front matter for metadata

2. **Local Preview**:
   ```bash
   cd docs-site/
   hugo server -D
   # Visit http://localhost:1313
   ```

3. **Validate**:
   - Check links (manual or automated)
   - Verify rendering (mobile and desktop)
   - Test code examples

4. **Commit & Deploy**:
   - Commit to `main` branch
   - GitHub Actions automatically builds and deploys
   - Live in 2-3 minutes

### Front Matter Schema

**Minimal (Default)**:
```yaml
---
title: "Page Title"
weight: 10  # Ordering within section (lower = higher priority)
---
```

**Extended (Comprehensive)**:
```yaml
---
title: "Page Title"
description: "Brief page description for SEO and search"
weight: 10
draft: false  # Set true to hide from production
tags: ["agent", "ci-cd", "tutorial"]
categories: ["guides"]
date: 2026-01-31
lastmod: 2026-01-31  # Auto-updated if GitInfo enabled
---
```

**ADR-022 Separated Metadata** (Optional Advanced Profile):
- Content files remain clean (no front matter)
- Metadata stored in `data/docmeta.yaml` (keyed by relative path)
- Custom Hugo templates read from data file
- See `ADR-022-docsite-separated-metadata.md` for details

---

## Build and Deployment

### Build Process

**Local Build**:
```bash
cd docs-site/
hugo --minify        # Produces static files in public/
```

**Build Performance**:
- Target: <5 seconds for 200 pages
- Actual: ~0.7 seconds (Hugo default)
- Scaling: Linear (1000+ pages in 3-5 seconds)

### Deployment Workflow

**GitHub Actions** (`.github/workflows/deploy-docsite.yml`):

```yaml
name: Deploy Documentation Site
on:
  push:
    branches: [main]
    paths:
      - 'docs-site/**'  # Only build on docsite changes
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true  # Fetch Hugo themes
      - uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.146.0'
          extended: true
      - uses: actions/configure-pages@v4
        id: pages
      - run: |
          hugo --gc --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"
        working-directory: docs-site
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./docs-site/public

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
```

**Deployment Timeline**:
1. Push to `main` → Trigger workflow (0s)
2. Checkout & setup (~30s)
3. Build site (~1-2s)
4. Upload artifact (~5s)
5. Deploy via GitHub Pages (~30s)
6. GitHub Pages propagation (~30-60s)
7. **Total: 2-3 minutes** from commit to live

### Environments

| Environment | URL | Purpose | Updates |
|-------------|-----|---------|---------|
| **Local** | http://localhost:1313 | Development, preview | On save (live reload) |
| **Production** | https://[org].github.io/[repo] | Public documentation | On push to `main` |
| **Staging** | (Future) Branch preview | PR review | On PR creation (future) |

---

## Metadata Management

### Default Approach: Front Matter

**Standard practice**: Metadata embedded in markdown files as YAML front matter

**Pros**:
- Familiar to most contributors
- Supported by all Hugo themes
- Single source (content + metadata together)

**Cons**:
- Token overhead for agents reading files (100-300 tokens per file)
- Front matter couples content to Hugo
- Bulk metadata changes require editing many files

**Use Cases**: Default for most users; adequate for <500 pages

---

### Advanced Approach: Separated Metadata (ADR-022)

**Optional profile** for high-frequency agent workflows and large sites

**Architecture**:
- Content files remain clean (no front matter)
- Metadata centralized in `data/docmeta.yaml`
- Hugo configured with `followSymlinks: true`
- Custom templates read metadata from data file

**Pros**:
- Zero token overhead for agents reading content
- Centralized metadata enables bulk operations
- Content remains generator-agnostic (portability)

**Cons**:
- Implementation complexity (~3-4 weeks setup)
- Platform compatibility challenges (Windows symlinks)
- Metadata drift risk (requires validation tooling)
- Custom templates incompatible with standard themes

**When to Adopt**:
- Agent workload is high (10+ agent sessions/week reading docs)
- Site scales to 500+ pages
- Metadata management becomes bottleneck
- Team accepts operational complexity trade-off

**Implementation Guide**: See `docs/HOW_TO_USE/advanced-docsite-setup.md` (future)

---

## Integration Points

### Main Repository Integration

**Content Sources**:
1. **Direct Content** (`docs-site/content/`): Site-specific pages (homepage, getting started)
2. **Migrated Content**: `docs/HOW_TO_USE/*.md` → `docs-site/content/guides/` (Batch 2)
3. **Referenced Content**: Links to `docs/architecture/adrs/`, `.github/agents/` (not migrated)

**Build Isolation**:
- Docsite builds independently of main codebase
- Changes in `docs-site/` do not trigger non-docsite workflows
- Docsite deployment workflow isolated (separate YAML file)

**Cross-Linking**:
- Documentation can link to GitHub files: `https://github.com/[org]/[repo]/blob/main/[path]`
- External links open in new tab (UX consideration)

---

### Theme Integration

**Current Theme**: Hugo Book

**Theme Customization Approach**:
1. **Minimal Overrides**: Use theme defaults where possible
2. **Partial Overrides**: Override specific partials in `layouts/partials/`
3. **Custom Layouts**: Add custom layouts in `layouts/` only when necessary
4. **Styling**: Customize via `assets/` SCSS (theme supports custom variables)

**Theme Update Strategy**:
- Theme as git submodule (tracked, versioned)
- Update theme: `git submodule update --remote themes/hugo-book`
- Test updates in local build before deploying
- Pin theme version if stability critical

**Future Theme Migration** (Batch 5+):
- Corporate theme integration planned
- Migration strategy: update `hugo.toml` theme parameter, test, adjust layouts
- Content remains compatible (standard markdown)

---

## Extensibility Considerations

### Planned Enhancements (Future Batches)

1. **Enhanced Search** (Batch 3):
   - Algolia integration for advanced search
   - Search analytics and query refinement
   - Faceted search (by section, tag, category)

2. **Version Management** (Batch 4+):
   - Multi-version documentation (e.g., v1.0, v2.0)
   - Version switcher in UI
   - Redirects for deprecated content

3. **Interactive Elements** (Batch 4+):
   - Code playgrounds (tryout examples in-browser)
   - Interactive tutorials (step-by-step with validation)
   - Embedded video content

4. **Analytics & Feedback** (Batch 5):
   - Google Analytics or privacy-respecting alternative
   - Page feedback ("Was this helpful?")
   - Popular content tracking

5. **Corporate Theme** (Batch 5+):
   - Enterprise branding integration
   - Custom color scheme and fonts
   - Logo and iconography

### Extension Patterns

**Adding New Content Types**:
1. Create new section in `content/[section-name]/`
2. Add section to menu in `hugo.toml`
3. (Optional) Create section-specific layout in `layouts/[section-name]/`

**Custom Shortcodes** (reusable content blocks):
```go-html-template
<!-- layouts/shortcodes/tip.html -->
<div class="tip">
  <strong>💡 Tip:</strong> {{ .Inner }}
</div>
```

**Usage in markdown**:
```markdown
{{< tip >}}
This is a helpful tip for users!
{{< /tip >}}
```

---

## Performance Optimization

### Build Performance

**Current State**:
- Hugo build: ~0.7s for initial site
- Target maintained: <5s for 200 pages
- Hugo scales linearly; 1000+ pages still <5s

**Optimization Strategies**:
- Use `hugo --gc` to clean unused resources
- Minify output (`--minify` flag)
- Enable caching in CI/CD (Hugo modules cache)

### Runtime Performance

**Current State**:
- Static HTML (instant page loads)
- Minimal JavaScript (Hugo Book theme is lightweight)
- Responsive images (future: use Hugo image processing)

**Optimization Strategies**:
- Enable Hugo minification (`minifyOutput = true`)
- Use WebP images for better compression
- Lazy-load images below fold
- Enable HTTP/2 and compression (GitHub Pages default)

**Performance Targets**:
- Lighthouse Performance Score: >90
- Time to Interactive (TTI): <2s
- First Contentful Paint (FCP): <1s

---

## Accessibility

### WCAG 2.1 Compliance

**Target**: WCAG 2.1 Level AA

**Conformance Areas**:
1. **Perceivable**:
   - Alt text for images
   - Proper heading hierarchy
   - Sufficient color contrast (4.5:1 minimum)

2. **Operable**:
   - Keyboard navigation
   - Skip-to-content link
   - Visible focus indicators

3. **Understandable**:
   - Clear, plain language
   - Consistent navigation
   - Error messages and guidance

4. **Robust**:
   - Semantic HTML
   - ARIA labels where appropriate
   - Valid markup

**Testing Strategy**:
- Automated: axe-core, Lighthouse accessibility audit
- Manual: Keyboard navigation, screen reader testing (NVDA/JAWS)

---

## Security Considerations

### Static Site Security

**Advantages of Static Sites**:
- No backend (no SQL injection, server exploits)
- No user authentication (no credential theft)
- No dynamic content (no XSS via server rendering)

**Security Best Practices**:
1. **Content Security Policy** (CSP): Restrict script sources
2. **HTTPS Only**: GitHub Pages enforces HTTPS
3. **Dependency Scanning**: Monitor Hugo and theme for vulnerabilities
4. **No Secrets**: Never commit API keys or credentials
5. **External Links**: Use `rel="noopener noreferrer"` for security

---

## Maintenance Strategy

### Routine Maintenance (Quarterly)

1. **Hugo Update**: Check for new Hugo version, test, upgrade
2. **Theme Update**: Update Hugo Book theme submodule, test
3. **Dependency Audit**: Review any additional dependencies (plugins, scripts)
4. **Link Validation**: Run broken link checker, fix 404s
5. **Content Audit**: Review top 20 pages for accuracy and updates

**Estimated Effort**: 2-4 hours per quarter

### Content Governance

**Ownership**:
- Technical content: Framework maintainers
- User guides: Documentation team (writer-editor agent)
- Architecture docs: Process architects (architect agent)

**Review Process**:
- Content PRs reviewed by domain experts
- Spelling/grammar automated checks (future: markdown linter)
- Technical accuracy validated by maintainers

**Versioning**:
- Content versioned via Git (single source of truth)
- Major content updates create new commits
- Git history provides audit trail

---

## Success Metrics

### Site Health

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Build Time** | <5s for 200 pages | Hugo build logs |
| **Deployment Time** | <3 min commit-to-live | GitHub Actions duration |
| **Broken Links** | 0 | Automated link checker |
| **Mobile Usability** | 100% pages responsive | Manual testing |
| **Lighthouse Performance** | >90 score | Lighthouse CI |

### User Experience

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Time to First Answer** | <3 clicks | User testing (future) |
| **Search Success Rate** | >80% | Search analytics (future) |
| **Page Load Time (P95)** | <2s | Real User Monitoring (future) |
| **Bounce Rate** | <40% | Analytics (future) |

### Content Coverage

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Total Pages** | 200+ by Batch 5 | Page count |
| **HOW_TO_USE Guides** | 19 migrated (Batch 2) | Migration tracker |
| **Architecture ADRs** | All ADRs linked/indexed | Content audit |
| **Content Freshness** | <10% pages >1 year old | Git history analysis |

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Hugo breaking changes** | Low | Medium | Pin Hugo version, test upgrades |
| **Theme abandonment** | Low | Medium | Hugo Book is well-maintained; fallback to Docsy |
| **GitHub Pages downtime** | Low | Low | Rare; no mitigation (acceptable risk) |
| **Build time degradation** | Low | Low | Hugo scales well; monitor build metrics |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Content drift (stale docs)** | Medium | High | Quarterly content audit, Git history tracking |
| **Contributor onboarding friction** | Medium | Medium | Clear README, contribution guide (Batch 2) |
| **Broken external links** | Medium | Low | Automated link checking (future) |
| **Inconsistent styling** | Low | Low | Style guide (Batch 2), markdown linting |

---

## Decision Log

### Key Architectural Decisions

| Decision | Date | Rationale | Status |
|----------|------|-----------|--------|
| **Hugo over Jekyll** | 2026-01-31 | Build speed (50x faster), zero dependencies, corporate theme ready | ✅ Implemented |
| **Hugo Book theme** | 2026-01-31 | Documentation-focused, clean, minimal, well-maintained | ✅ Implemented |
| **GitHub Pages hosting** | 2026-01-31 | Zero cost, tight GitHub integration, reliable | ✅ Implemented |
| **ADR-022 as optional** | 2026-01-31 | Avoid premature optimization; opt-in for advanced users | ✅ Documented |
| **Single branch deployment** | 2026-01-31 | Simplicity; multi-version defer to future | ✅ Implemented |

---

## Future Roadmap

### Batch 2: Core Content Migration (3 weeks)
- Migrate 19 HOW_TO_USE guides
- Create Getting Started guide
- Implement search functionality
- Establish content style guide

### Batch 3: User Onboarding (2-3 weeks)
- Tutorial series (6-8 tutorials)
- Common use case guides (5-7 scenarios)
- Troubleshooting guide
- FAQ section

### Batch 4: Developer/Architect Content (2-3 weeks)
- Architecture deep dives
- ADR migration and indexing
- Agent profile reference
- API documentation (if applicable)

### Batch 5: Polish & Launch (1-2 weeks)
- Corporate theme integration
- Analytics and feedback
- SEO optimization
- Public launch announcement

---

## References

- **Technology Selection**: `work/analysis/docsite-technology-selection.md`
- **ADR-022**: `docs/architecture/adrs/ADR-022-docsite-separated-metadata.md`
- **Roadmap**: `work/planning/documentation-website-roadmap.md`
- **Hugo Documentation**: https://gohugo.io/documentation/
- **Hugo Book Theme**: https://github.com/alex-shpak/hugo-book

---

**Version History**:
- **1.0.0** (2026-01-31): Initial architecture document
- Future updates tracked in Git history

**Approval**:
- **Prepared By**: Architect Alphonso
- **Reviewed By**: (Pending)
- **Status**: ✅ Initial Implementation Ready
