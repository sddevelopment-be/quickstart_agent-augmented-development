+++
title = "Markdown Primer"
subtitle = "Lightweight markup for readable, version-controllable documentation"
aliases = ["markdown-primer", "markup-and-diagramming/markdown"]
author = "Stijn Dejongh"
outputs = ['html', 'rss', 'json']
date = "2025-11-13T22:00:00+00:00"
tags = ["documentation", "markdown", "primer", "reference", "markup"]
summary = """
Markdown is a plain-text formatting syntax designed for readability in both raw and rendered form. 
It enables version-controlled documentation, README files, and static site content without requiring 
specialized editors or complex markup languages.
"""
further_exploration = [
    { type = "raw", author = "Gruber, John", year = "2004", title = "Original Markdown Syntax", site = "Daring Fireball", link = "https://daringfireball.net/projects/markdown/syntax" },
    { type = "raw", author = "CommonMark", year = "2024", title = "CommonMark Specification", site = "commonmark.org", link = "https://commonmark.org/" },
    { type = "raw", author = "GitHub", year = "2024", title = "GitHub Flavored Markdown Spec", site = "GitHub", link = "https://github.github.com/gfm/" },
    { type = "raw", author = "Google", year = "2024", title = "Markdown Style Guide", site = "Google Developer Documentation Style Guide", link = "https://google.github.io/styleguide/docguide/style.html" },
    { type = "raw", author = "Markdown Guide", year = "2024", title = "Markdown Guide: Comprehensive Reference", site = "markdownguide.org", link = "https://www.markdownguide.org/" }
]
image = "primers/markdown_logo"
+++

## 1. Purpose and Philosophy

> Simplicity and readability over feature completeness.

Markdown was created by [John Gruber](https://daringfireball.net/projects/markdown/syntax#philosophy) in 2004 with a clear goal: enable writers to **create formatted documents using plain text that remains readable in its source form**. It prioritizes simplicity and accessibility over feature completeness.

**Strengths:**

- **Human-readable source:** Raw markdown is as legible as rendered output
- **Version control friendly:** Plain text diffs cleanly in Git
- **Universal adoption:** GitHub, GitLab, static site generators, documentation tools
- **Minimal syntax:** Learn the basics in minutes
- **Tool independence:** Edit with any text editor; render with countless tools (VS Code, Typora, static site generators, git hosting platforms)
- **Extensible:** HTML embedding for advanced needs; many flavors/extensions ([GFM](https://github.github.com/gfm/), [MultiMarkdown](https://fletcherpenney.net/multimarkdown/), [Markua](https://markua.com/))

**Limitations:**

- **Inconsistent implementations:** CommonMark, GitHub Flavored Markdown (GFM), and others have variations that can lead to rendering differences (especially with tables, task lists, images, and extensions)
- **Limited semantic structure:** No native support for complex layouts or interactive elements
- **Extensibility via HTML:** Power users embed HTML, breaking portability and reading in pure markdown renderers
- **Table complexity:** Advanced tables require extensions or workarounds

**Use Markdown for:**

- README files, CONTRIBUTING guides, changelogs
- Static site content (Hugo, Jekyll, MkDocs)
- Inline documentation in code repositories
- Personal notes, Zettelkasten systems, wikis

**Avoid Markdown for:**

- Print-quality documents (use LaTeX, word processors, or HTML/CSS) unless converted, parsed through specialized tools
- Complex layouts with precise formatting requirements
- Interactive or dynamic content (unless combined with frameworks)

**Authoritative References:**

- [CommonMark Specification](https://commonmark.org/) — Standardized Markdown syntax
- [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/) — GitHub's extended syntax
- [Markdown Guide](https://www.markdownguide.org/) — Comprehensive reference and best practices
- [Original Markdown Syntax by John Gruber](https://daringfireball.net/projects/markdown/syntax)

## 2. Getting Started

Writing markdown requires nothing more than a text editor. To get started quickly, choose an editor that suits your workflow:

**For beginners:**
- **[Notepad++](https://notepad-plus-plus.org/)** (Windows) — Lightweight, syntax highlighting, free
- **TextEdit** (macOS) — Built-in, switch to plain text mode (Format → Make Plain Text)
- **gedit** (Linux) — Simple, comes pre-installed on many distributions

**For enhanced productivity:**
- **[VS Code](https://code.visualstudio.com/)** — Live preview, extensions for linting and formatting, cross-platform
- **[Typora](https://typora.io/)** — WYSIWYG markdown editor with instant preview
- **[Obsidian](https://obsidian.md/)** — Note-taking with linking and graph views

**Quick setup with VS Code:**
1. Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install recommended extensions:
   - "Markdown All in One" for shortcuts and preview
   - "markdownlint" for style checking
3. Open a `.md` file and press `Ctrl+K V` (or `Cmd+K V` on macOS) for side-by-side preview
4. Start writing—autocomplete and syntax highlighting work out of the box

Once you have an editor, create a file named `README.md`, write a few headings and lists following the syntax below, and preview the results. Most modern platforms (GitHub, GitLab, static site generators) will render markdown automatically.

## 3. Core Syntax

**Minimal cheatsheet:**

### Headings
```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```

### Text Formatting
```markdown
**Bold text**
*Italic text*
***Bold and italic***
~~Strikethrough~~ (GFM extension)
`Inline code`
```

### Lists
```markdown
Unordered list:
- Item 1
- Item 2
  - Nested item

Ordered list:
1. First item
2. Second item
   1. Nested item
```

### Links and Images
```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Optional title")

![Alt text for image](path/to/image.png)
![Image with title](image.png "Optional title")
```

### Code Blocks

Fenced code blocks use triple backticks with an optional language identifier for syntax highlighting:

{{< highlight markdown >}}
```python
def hello():
    print("Hello, world!")
```
{{< /highlight >}}

### Blockquotes
```markdown
> This is a blockquote.
> It can span multiple lines.
>
> — Attribution
```

### Horizontal Rule
```markdown
---
```

### Tables (GFM)
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

Alignment:
| Left | Center | Right |
|:-----|:------:|------:|
| A    |   B    |     C |
```

### Task Lists (GFM Extension)
```markdown
- [x] Completed task
- [ ] Pending task
```

## 4. Patterns and Idioms

Here are some common usage patterns for using markdown effectively in documentation and READMEs.

### README Structure
Most README files follow a consistent pattern:

{{< highlight markdown >}}
# Project Name

Brief one-sentence description.

## Installation

```bash
npm install project-name
```

## Usage

```javascript
const project = require('project-name');
project.doSomething();
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License

{{< /highlight >}}

### Documentation Organization
```markdown
# Feature Name

## Overview
High-level description

## Motivation
Why this exists

## Usage
How to use it with examples

## API Reference
Detailed function/class descriptions

## Further Reading
Links to related docs
```

### Linking Within Repository
```markdown
Relative links to other markdown files:
[See the guide](docs/guide.md)

Linking to specific headings:
[Jump to Installation](#installation)

Cross-file heading links:
[See Setup in Guide](docs/guide.md#setup)
```

### Embedding Code Snippets

When documenting code in a repository, you can reference source files directly or include inline snippets with syntax highlighting. This helps readers understand implementation details without leaving the documentation.

{{< highlight markdown >}}
Reference code in repository:
See [example.py](src/example.py) for implementation.

Inline snippet with highlighting:
```python
# File: src/example.py
def process_data(items):
    return [item.upper() for item in items]
```
{{< /highlight >}}

### Embedding ASCI DIagrams

Wrapping Ascii diagrams in code blocks for proper rendering:

```markdown
  +---------+
  |  Start  |
  +---------+
       |
       v
  +---------+
  | Process |
  +---------+
       |
       v
  +---------+
  |   End   |
  +---------+
```

## 5. Tooling and Rendering

Beyond basic text editors, markdown benefits from specialized tools that provide validation, transformation, and publishing capabilities. These tools help maintain consistency and streamline documentation workflows.

### Editors
- [VS Code](https://code.visualstudio.com/) with Markdown extensions (preview, linting)
- [Typora](https://typora.io/) — WYSIWYG markdown editor
- [Obsidian](https://obsidian.md/) — Note-taking with markdown and linking
- [Zettlr](https://www.zettlr.com/) — Academic markdown editor

### Linters and Formatters

Automated tools catch style inconsistencies and formatting errors before they reach production. Running these in pre-commit hooks or CI pipelines ensures documentation quality.

- [markdownlint](https://github.com/DavidAnson/markdownlint) — Style checker and linter
- [Prettier](https://prettier.io/) — Auto-formatter for markdown
- [Remark](https://remark.js.org/) — Markdown processor with plugins

### Static Site Generators

These tools transform markdown files into complete websites, handling navigation, theming, and asset management automatically.

- [Hugo](https://gohugo.io/) — Fast static site generator (used by this site)
- [Jekyll](https://jekyllrb.com/) — GitHub Pages default generator
- [MkDocs](https://www.mkdocs.org/) — Documentation-focused generator
- [Docusaurus](https://docusaurus.io/) — React-based documentation sites
- [Docsify](https://docsify.js.org/) — Dynamic documentation site without static build step
- [reveal.js](https://revealjs.com/) — Markdown-based presentation framework for creating HTML slideshows

### Rendering Libraries

When building custom documentation tools or integrating markdown into applications, these libraries parse and convert markdown to HTML.

- [marked](https://github.com/markedjs/marked) — JavaScript markdown parser
- [markdown-it](https://github.com/markdown-it/markdown-it) — Extensible markdown parser
- [Python-Markdown](https://python-markdown.github.io/) — Python implementation
- [CommonMark](https://commonmark.org/help/) — Reference implementation

## 6. Integration

Markdown's plain-text nature makes it ideal for integration with development workflows. Version control, automated builds, and documentation-as-code practices all benefit from treating docs like source code.

### Version Control
```bash
# All markdown files are plain text, perfect for Git
git add README.md
git commit -m "Update installation instructions"
git diff HEAD~1 README.md  # Clean, readable diffs
```

### CI/CD Documentation Builds
```yaml
# GitHub Actions example
name: Build Docs
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build with Hugo
        run: |
          hugo --minify
      - name: Lint markdown
        run: |
          npm install -g markdownlint-cli
          markdownlint '**/*.md'
```

### Auto-Generated Documentation

Example usage of badges and links to generated docs in a README.md file:

```markdown
<!-- Embed badges -->
![Build Status](https://github.com/user/repo/workflows/CI/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

<!-- Link to auto-generated API docs -->
See [API Documentation](https://user.github.io/repo/api/)
```

### Documentation as Code
```markdown
Store documentation alongside source:
project/
├── src/
├── docs/
│   ├── architecture.md
│   ├── api-reference.md
│   └── guides/
│       ├── quickstart.md
│       └── advanced.md
└── README.md
```

## 7. Accessibility and Review

### Accessibility Practices
- **Alt text for images:** Always provide meaningful descriptions
  ```markdown
  ![Architecture diagram showing three-layer separation](diagrams/architecture.png)
  ```
- **Descriptive link text:** Avoid "click here"
  ```markdown
  Bad:  [Click here](https://example.com)
  Good: [Read the installation guide](https://example.com/install)
  ```
- **Heading hierarchy:** Use headings in order (don't skip levels)
- **Table headers:** Ensure tables have proper header rows for screen readers

### Review and Versioning
- **Preview before committing:** Use editor preview or local site build
- **Lint for consistency:** Run markdownlint in pre-commit hooks
- **Track changes with Git:** Markdown diffs are human-readable
- **Version documentation with code:** Tag releases include corresponding docs

### Common Pitfalls
- **Inconsistent spacing:** Blank lines around headings, code blocks vary by renderer
- **HTML fallback abuse:** Embedding complex HTML reduces portability
- **Broken relative links:** Test links in rendered context, not just source
- **Forgotten fenced code blocks:** Backticks must match (three for blocks)

## 8. Example and Reference

**Complete working example: Project README**

{{< highlight markdown >}}
# Task Manager

A simple command-line task management tool written in Python.

## Features

- Add, list, and complete tasks
- Persistent storage in JSON format
- Filter by status and priority

## Installation

```bash
pip install task-manager
```

## Usage

```bash
# Add a task
task add "Write documentation"

# List all tasks
task list

# Complete a task
task complete 1

# Filter by status
task list --status pending
```

## Configuration

Create `~/.taskrc`:

```json
{
  "default_priority": "medium",
  "storage_path": "~/.tasks.json"
}
```

## Development

```bash
# Clone repository
git clone https://github.com/user/task-manager

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Lint code
flake8 src/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — see [LICENSE](LICENSE) for details.

## References

- [Task Management Best Practices](https://example.com)
- [CLI Design Patterns](https://example.com)
{{< /highlight >}}

**Best practices demonstrated:**
- Clear hierarchy of headings
- Code blocks with language hints
- Working examples with explanations
- Relative links to repository files
- Consistent formatting throughout

