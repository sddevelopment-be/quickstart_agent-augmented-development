# Quickstart Documentation Site

Welcome to the documentation site repository for the **Quickstart Agent-Augmented Development Framework**.

This directory contains the source code for the framework's public documentation website, built with Hugo and deployed to GitHub Pages.

---

## 🚀 Quick Start for Contributors

### Prerequisites

- **Hugo Extended**: v0.140.1 or later
- **Git**: For version control and theme submodules

### Installation

**macOS (Homebrew)**:
```bash
brew install hugo
```

**Linux (Debian/Ubuntu)**:
```bash
sudo apt install hugo
```

**Linux (Snap)**:
```bash
snap install hugo --channel=extended
```

**Windows (Chocolatey)**:
```bash
choco install hugo-extended
```

**Manual Download**: https://github.com/gohugoio/hugo/releases

---

## 🏗️ Local Development

### 1. Clone and Setup

```bash
# Clone repository (if not already done)
git clone https://github.com/sd-development/quickstart_agent-augmented-development.git
cd quickstart_agent-augmented-development/docs-site

# Initialize theme submodule
git submodule update --init --recursive
```

### 2. Start Local Server

```bash
# Development server with live reload
hugo server -D

# Server will start at http://localhost:1313
# Changes auto-reload in browser
```

**Options**:
- `-D`: Include draft content
- `--navigateToChanged`: Auto-navigate to changed page
- `--disableFastRender`: Disable fast render (for troubleshooting)

### 3. Create New Content

```bash
# Create new guide
hugo new content/guides/my-new-guide.md

# Create new architecture doc
hugo new content/architecture/my-adr.md

# Edit the created file with your content
```

### 4. Build for Production

```bash
# Build static site to public/
hugo --minify

# Output will be in public/ directory
```

---

## 📁 Directory Structure

```
docs-site/
├── archetypes/          # Content templates for hugo new
├── assets/              # SASS/SCSS, fonts (processed by Hugo)
├── content/             # 📝 Main documentation content (EDIT HERE)
│   ├── _index.md        # Homepage
│   ├── getting-started/ # Onboarding guides
│   ├── guides/          # How-to guides
│   ├── architecture/    # Architecture docs, ADRs
│   ├── reference/       # API reference, glossary
│   └── contributing/    # Contribution guides
├── data/                # Data files (YAML/JSON/TOML)
├── layouts/             # Custom templates (overrides theme)
├── static/              # Static assets (images, CSS, JS)
├── themes/              # Hugo themes (git submodules)
│   └── hugo-book/       # Current theme
├── hugo.toml            # ⚙️ Site configuration
├── ARCHITECTURE.md      # Architecture documentation
└── README.md            # This file
```

---

## ✍️ Content Guidelines

### Front Matter

Every content page should include front matter at the top:

```yaml
---
title: "Page Title"
description: "Brief description for SEO"
weight: 10  # Lower number = higher priority in menu
draft: false  # Set to true to hide from production
---
```

### Markdown Features

**Hugo Book theme** supports:

- **Standard Markdown**: Headings, lists, links, images, code blocks
- **Emoji**: `:smile:` → 😃 (enabled in config)
- **Syntax Highlighting**: Language-specific code blocks
- **Shortcodes**: Custom content blocks (see theme docs)

**Example Code Block**:
````markdown
```bash
# This is a bash command
hugo server -D
```
````

**Example Image**:
```markdown
![Alt text](/images/screenshot.png)
```

### Internal Links

**Link to other pages**:
```markdown
[Getting Started](/getting-started/)
[Guide Name](/guides/my-guide/)
```

**Link to GitHub files** (external):
```markdown
[View Source](https://github.com/sd-development/quickstart/blob/main/docs/VISION.md)
```

---

## 🎨 Theme Customization

### Current Theme: Hugo Book

**Repository**: https://github.com/alex-shpak/hugo-book  
**Documentation**: https://github.com/alex-shpak/hugo-book#readme

### Customization Options

1. **Configuration** (`hugo.toml`):
   - Site title, description, menus
   - Theme parameters (search, TOC, colors)

2. **Layouts** (`layouts/`):
   - Override theme templates
   - Add custom page types

3. **Styling** (`assets/`):
   - Custom SCSS/CSS
   - Theme variables override

4. **Static Assets** (`static/`):
   - Images, logos, custom JS

---

## 🚢 Deployment

### Automatic Deployment

**GitHub Actions** automatically deploys the site when changes are pushed to `main`:

1. **Trigger**: Push to `docs-site/` on `main` branch
2. **Build**: Hugo builds static site in ~1-2 seconds with dynamically configured baseURL
3. **Deploy**: Static files deployed via GitHub Pages native actions
4. **Live**: Site updates at https://sddevelopment-be.github.io/quickstart_agent-augmented-development/ in 2-3 minutes

**Note**: The workflow uses GitHub's native Pages deployment actions (`actions/configure-pages@v4`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`) for improved reliability. The `baseURL` is automatically configured from the Pages environment settings, ensuring all links work correctly regardless of repository name or location.

### Manual Deployment (if needed)

```bash
# Build production site
hugo --minify

# Deploy public/ directory to GitHub Pages
# (Automated by GitHub Actions; manual deploy rarely needed)
```

---

## 🧪 Testing and Validation

### Local Testing

```bash
# Test build (no server)
hugo

# Check for errors
hugo --verbose

# Validate links (future: automated script)
# Manual: Click through navigation, check for 404s
```

### Accessibility Testing

- **Lighthouse**: Run in Chrome DevTools (target: >90 score)
- **Keyboard Navigation**: Tab through pages, test all interactive elements
- **Screen Reader**: Test with NVDA/JAWS (basic validation)

### Mobile Testing

- **Responsive Design Mode**: Browser DevTools
- **Physical Devices**: Test on phone/tablet if available
- **Touch Targets**: Ensure buttons/links are tappable (>44px)

---

## 📚 Helpful Resources

### Hugo Documentation

- **Official Docs**: https://gohugo.io/documentation/
- **Quick Start**: https://gohugo.io/getting-started/quick-start/
- **Content Management**: https://gohugo.io/content-management/
- **Templates**: https://gohugo.io/templates/

### Hugo Book Theme

- **GitHub**: https://github.com/alex-shpak/hugo-book
- **Demo Site**: https://hugo-book-demo.netlify.app/

### Markdown Reference

- **CommonMark Spec**: https://commonmark.org/
- **Hugo Markdown**: https://gohugo.io/content-management/formats/

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `hugo: command not found`
- **Fix**: Install Hugo (see Installation section)

**Issue**: Theme not loading (blank page)
- **Fix**: Initialize theme submodule: `git submodule update --init --recursive`

**Issue**: Changes not showing in browser
- **Fix**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R), or restart server

**Issue**: Build errors
- **Fix**: Check Hugo version (`hugo version`), ensure v0.140.1+
- **Fix**: Validate markdown syntax in errored files

**Issue**: Slow build times
- **Fix**: Use `hugo --gc` to clean unused cache
- **Fix**: Check for large images (compress with `hugo gen images`)

### Getting Help

1. **Check ARCHITECTURE.md**: Comprehensive architecture documentation
2. **Search Hugo Docs**: https://gohugo.io/documentation/
3. **Hugo Community**: https://discourse.gohugo.io/
4. **GitHub Issues**: Report bugs/issues in repository

---

## 🤝 Contributing

### Contribution Workflow

1. **Fork & Clone**: Fork repository, clone locally
2. **Create Branch**: `git checkout -b docs/my-improvement`
3. **Make Changes**: Edit content in `content/` directory
4. **Test Locally**: Run `hugo server -D`, verify changes
5. **Commit**: `git commit -m "docs: improve getting started guide"`
6. **Push**: `git push origin docs/my-improvement`
7. **Pull Request**: Open PR with clear description

### Contribution Types

**Content Contributions**:
- Fix typos, grammar, clarity
- Add new guides or tutorials
- Update outdated information
- Improve code examples

**Technical Contributions**:
- Theme customization
- Layout improvements
- Search enhancements
- Build optimizations

**Style Guidelines**:
- Use clear, concise language
- Follow existing content structure
- Include code examples where helpful
- Test all links before submitting

---

## 📊 Site Metrics

### Build Performance

- **Current Build Time**: ~0.7 seconds (initial site)
- **Target**: <5 seconds for 200 pages
- **Hugo Version**: v0.140.1 Extended

### Content Status

- **Phase**: Batch 1 (Foundation)
- **Pages**: Initial homepage + section placeholders
- **Next**: Batch 2 content migration (19 HOW_TO_USE guides)

---

## 📞 Contact & Support

**Repository**: https://github.com/sd-development/quickstart_agent-augmented-development  
**Documentation Site**: https://[org].github.io/[repo] (after deployment)  
**Issues**: https://github.com/sd-development/quickstart/issues

---

## 📝 License

This documentation is part of the Quickstart Agent-Augmented Development Framework and follows the same license as the main repository.

---

**Last Updated**: 2026-01-31  
**Version**: 1.0.0 (Batch 1: Foundation)
