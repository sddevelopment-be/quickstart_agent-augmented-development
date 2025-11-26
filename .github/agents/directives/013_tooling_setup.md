<!-- The following information is to be interpreted literally -->
# 013 Tooling Setup & Fallbacks

> **Purpose:** Installation commands, version requirements, and fallback strategies for core development tools

## 1. Core Tool Suite

This directive documents installation, versioning, and fallback strategies for tools referenced in directive 001 (CLI & Shell Tooling).

### Tool Inventory

| Tool | Purpose | Minimum Version | Fallback |
|------|---------|-----------------|----------|
| `fd` | Fast file discovery | 8.0+ | `find` |
| `rg` (ripgrep) | Fast content search | 13.0+ | `grep -r` |
| `ast-grep` | AST-based code search | 0.5+ | Manual parsing with grep/sed |
| `jq` | JSON parsing/querying | 1.6+ | Manual JSON parsing (Python/Node) |
| `yq` | YAML parsing/querying | 4.0+ | Manual YAML parsing (Python) |
| `fzf` | Interactive fuzzy finder | 0.30+ | Manual file selection |

## 2. Installation

### Linux (Debian/Ubuntu)

```bash
# Update package index
sudo apt update

# Core tools
sudo apt install -y fd-find ripgrep jq

# fd-find binary may be named 'fdfind' on Debian/Ubuntu
# Create symlink if needed
sudo ln -s $(which fdfind) /usr/local/bin/fd 2>/dev/null || true

# yq (YAML processor)
VERSION=v4.35.1
BINARY=yq_linux_amd64
wget https://github.com/mikefarah/yq/releases/download/${VERSION}/${BINARY} -O /tmp/yq
sudo mv /tmp/yq /usr/local/bin/yq
sudo chmod +x /usr/local/bin/yq

# fzf (fuzzy finder)
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --all

# ast-grep (AST-based search)
VERSION=0.12.0
wget https://github.com/ast-grep/ast-grep/releases/download/${VERSION}/ast-grep-x86_64-unknown-linux-gnu.zip
unzip ast-grep-x86_64-unknown-linux-gnu.zip -d /tmp
sudo mv /tmp/ast-grep /usr/local/bin/
sudo chmod +x /usr/local/bin/ast-grep
```

### macOS (Homebrew)

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Core tools
brew install fd ripgrep jq yq fzf ast-grep

# Initialize fzf
$(brew --prefix)/opt/fzf/install --all
```

### Verification

```bash
# Verify installations
fd --version
rg --version
jq --version
yq --version
fzf --version
ast-grep --version
```

## 3. Fallback Strategies

### When `fd` is Unavailable

Use `find` with appropriate flags:

```bash
# fd equivalent: fd -t f -e md
find . -type f -name "*.md"

# fd equivalent: fd -t d src
find . -type d -name "src"

# fd equivalent: fd --hidden --no-ignore
find . -type f
```

**Note:** `find` is slower on large repositories but universally available.

### When `rg` (ripgrep) is Unavailable

Use `grep` with recursive flag:

```bash
# rg equivalent: rg "pattern"
grep -r "pattern" .

# rg equivalent: rg -i "pattern"
grep -ri "pattern" .

# rg equivalent: rg -l "pattern"
grep -rl "pattern" .

# Exclude directories (like .git):
grep -r --exclude-dir=.git "pattern" .
```

**Note:** `grep` is slower and less feature-rich but universally available.

### When `jq` is Unavailable

Use Python for JSON parsing:

```bash
# jq equivalent: jq '.version' manifest.json
python3 -c "import json; print(json.load(open('manifest.json'))['version'])"

# jq equivalent: jq -r '.directives[].code' manifest.json
python3 -c "import json; data=json.load(open('manifest.json')); print('\\n'.join([d['code'] for d in data['directives']]))"
```

Or Node.js:

```bash
# jq equivalent: jq '.version' manifest.json
node -e "console.log(require('./manifest.json').version)"
```

**Note:** Python/Node are typically available in development environments.

### When `yq` is Unavailable

Use Python with PyYAML:

```bash
# yq equivalent: yq '.key' config.yaml
python3 -c "import yaml; print(yaml.safe_load(open('config.yaml'))['key'])"

# Install PyYAML if needed
pip3 install pyyaml
```

### When `ast-grep` is Unavailable

Use language-specific parsers or manual grep patterns:

```bash
# For simple AST-like searches, use grep with appropriate patterns
# Example: Find function definitions in JavaScript
grep -rn "function\s\+\w\+" src/

# For more complex AST needs, use language-specific tools:
# - TypeScript: Use `tsc` with `--listFiles` and custom scripts
# - Python: Use `ast` module with custom scripts
# - Go: Use `go list` with `-json` flag
```

### When `fzf` is Unavailable

Use manual selection with `ls` and numbered choices:

```bash
# List files with numbers
ls -1 | nl

# Read user selection
read -p "Enter number: " NUM
FILE=$(ls -1 | sed -n "${NUM}p")
```

Or use simple grep filtering:

```bash
# Filter files by pattern
ls | grep "pattern"
```

## 4. Performance Considerations

### Large Repository Search Strategy

When working with large repositories (>100K files):

1. **Use `fd` over `find`** — 5-10x faster due to parallel execution and `.gitignore` awareness
2. **Use `rg` over `grep`** — 10-100x faster due to optimized algorithms and parallel execution
3. **Enable `.gitignore` awareness** — Skip irrelevant files (node_modules, build artifacts)
4. **Limit search scope** — Specify subdirectories instead of searching from root
5. **Use file type filters** — Reduce search space with `-t` (fd) or `-g` (rg)

Example:

```bash
# Slow: grep -r "pattern" .
# Fast: rg "pattern" src/ --type md
```

### Memory-Constrained Environments

If running in memory-limited environments (CI containers, embedded systems):

- Prefer `rg` and `fd` — More memory-efficient than alternatives
- Avoid loading entire directory trees into memory
- Use streaming/line-by-line processing
- Limit concurrent operations

## 5. Version Pinning

For reproducible environments, pin tool versions:

```dockerfile
# Dockerfile example
FROM ubuntu:22.04

ENV FD_VERSION=8.7.0 \
    RG_VERSION=13.0.0 \
    JQ_VERSION=1.6 \
    YQ_VERSION=4.35.1 \
    FZF_VERSION=0.42.0 \
    AST_GREP_VERSION=0.12.0

RUN apt-get update && apt-get install -y wget unzip git && \
    # Install specific versions...
    # (installation commands with version variables)
```

## 6. Common Issues and Solutions

### Issue: `fd` binary named `fdfind` on Debian/Ubuntu

**Solution:** Create symlink as shown in installation section.

### Issue: `yq` conflicts with Python `yq` package

**Solution:** Use full path `/usr/local/bin/yq` or ensure shell PATH prioritizes correct binary.

### Issue: `ast-grep` not in PATH

**Solution:** Verify installation and add to PATH:

```bash
export PATH="$PATH:/usr/local/bin"
```

### Issue: `fzf` keybindings not working

**Solution:** Re-run installation with `--all` flag:

```bash
~/.fzf/install --all
```

Then restart shell or source config:

```bash
source ~/.bashrc  # or ~/.zshrc
```

## 7. Agent Usage Guidelines

### Checking Tool Availability

Before using a tool, agents should verify availability:

```bash
if command -v fd &> /dev/null; then
  fd -t f -e md
else
  find . -type f -name "*.md"
fi
```

### Fallback Decision Tree

1. **Check if preferred tool exists** (`command -v <tool>`)
2. **If available:** Use preferred tool with optimized flags
3. **If unavailable:** Use fallback with equivalent functionality
4. **If fallback unavailable:** Escalate with ⚠️ marker, request manual intervention

### Error Reporting

When a tool is unavailable and no fallback succeeds:

```markdown
⚠️ Required tool `ast-grep` not available and no suitable fallback found.
Please install ast-grep version 0.5+ or provide alternative approach.
```

## 8. Continuous Integration Considerations

For CI/CD pipelines:

- **Cache tool installations** to speed up builds
- **Use official Docker images** with tools pre-installed when possible
- **Verify tool availability** in CI scripts before use
- **Provide installation fallbacks** for different OS environments

Example GitHub Actions:

```yaml
- name: Install tools
  run: |
    sudo apt-get update
    sudo apt-get install -y fd-find ripgrep jq
    # Add yq, fzf, ast-grep as needed
```

## 9. Related Directives

- **001: CLI & Shell Tooling** — Tool usage patterns and best practices
- **003: Repository Quick Reference** — Repository structure and navigation
- **011: Risk & Escalation** — How to escalate when tools are unavailable

---

_Version: 1.0.0_  
_Last Updated: 2025-11-17_
