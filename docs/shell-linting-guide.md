# Shell Linting Integration Guide

## Overview

This project uses **ShellCheck** for static analysis of shell scripts. The project contains 22 shell scripts across various directories.

## Configuration

### `.shellcheckrc` (Project Root)

The ShellCheck configuration file defines:

- **Enabled checks**: All optional checks are enabled by default
- **Disabled checks**:
  - `SC1091`: Source file not found (dynamic sourcing patterns)
  - `SC2086`: Double quote word splitting (allows controlled expansion)
  - `SC2181`: Check exit code directly (common pattern in scripts)

- **Severity**: Warning level (includes errors, warnings, info, style)
- **Shell dialect**: Bash (primary)
- **Format**: GCC (for CI/CD integration)

**View configuration:**
```bash
cat .shellcheckrc
```

## Local Usage

### Check Shell Scripts

Run ShellCheck on all project shell scripts:

```bash
npm run lint:shell
```

This finds all `*.sh` files (excluding `node_modules` and `.git`) and validates them against the configuration.

### Generate Report

Create a JSON report of all issues:

```bash
npm run lint:shell:report
```

Output: `shellcheck-report.json` (machine-readable format for analysis and trend tracking)

### Integrated Validation

Run all project validation (text + shell):

```bash
npm run lint
```

This runs:
1. Spell checking (`npm run spell`)
2. Markdown linting (`npm run lint:markua`)
3. Shell linting (`npm run lint:shell`)

## GitHub Actions Integration

### Workflow: `.github/workflows/shell-lint.yml`

**Trigger conditions:**
- Push to `main` or `develop` branches with changes to `*.sh` files
- Pull requests targeting `main` or `develop` with shell script changes
- Manual trigger via `workflow_dispatch`

**Job: ShellCheck Linting**

- **Environment**: Ubuntu Latest
- **Steps**:
  1. Checkout code
  2. Install ShellCheck from apt
  3. Verify installation (version check)
  4. Run linting with `.shellcheckrc` configuration
  5. Generate JSON report (always)
  6. Upload artifact (if report exists)
  7. Comment PR with results (if PR)

**Permissions:**
- `contents: read` - Read repository
- `checks: write` - Write check results
- `pull-requests: write` - Comment on PRs

### PR Comment Integration

When linting runs on a PR:
- ✅ **Pass**: "All shell scripts passed ShellCheck linting"
- ⚠️ **Fail**: Lists up to 50 issues with file:line:column references
- Suggests running `npm run lint:shell` locally

### Artifacts

ShellCheck reports are uploaded as GitHub artifacts:
- Name: `shellcheck-report`
- Format: JSON
- Retention: 30 days
- Available for download on workflow page

## Common ShellCheck Issues

### SC1004: Only one '/' is needed

**Issue**: Using `//` in regex or path where one `/` is sufficient

**Example**:
```bash
# ❌ Wrong
sed 's//old//new/g'

# ✅ Correct
sed 's/old/new/g'
```

### SC2006: Use `$()` instead of backticks

**Issue**: Backticks are deprecated in favor of `$()`

**Example**:
```bash
# ❌ Wrong (backticks)
result=`command`

# ✅ Correct (command substitution)
result=$(command)
```

### SC2012: Use `find` instead of `ls` for parsing file listings

**Issue**: `ls` output is not reliable for scripting

**Example**:
```bash
# ❌ Wrong
for file in $(ls *.txt); do
  echo "$file"
done

# ✅ Correct
find . -name '*.txt' -print0 | while IFS= read -r -d '' file; do
  echo "$file"
done
```

### SC2207: Array assignment with command substitution may lose elements

**Issue**: Word splitting in array assignments

**Example**:
```bash
# ❌ Wrong (loses elements with spaces)
array=($(find . -name '*.sh'))

# ✅ Correct (preserves elements)
mapfile -t array < <(find . -name '*.sh')
```

### SC2076: Don't quote `$var` in `[[ $var == pattern ]]`

**Issue**: Quoting prevents pattern matching in `[[` tests

**Example**:
```bash
# ❌ Wrong (treats as literal string)
[[ "$var" == *.txt ]]

# ✅ Correct (pattern matching works)
[[ $var == *.txt ]]
```

### SC2046: Quote this to prevent word splitting/globbing

**Issue**: Unquoted variable expansion causes word splitting

**Example**:
```bash
# ❌ Wrong (splits on spaces)
files=$var
rm $files

# ✅ Correct (preserves spaces)
files=$var
rm "$files"
```

### SC2181: Check exit code of `test` by inspecting its output

**Note**: This check is disabled by default in `.shellcheckrc` as the pattern is common in the project.

### Using `[[` vs `[`

**Recommendation**: Use `[[` instead of `[` for conditional tests

**Benefits of `[[`:**
- No word splitting or pathname expansion
- Safer and more intuitive
- Supports regex matching with `=~`
- Supports pattern matching
- Logical operators: `&&`, `||` instead of `-a`, `-o`

**Example**:
```bash
# ❌ Old style (unsafe)
if [ -n "$var" ] && [ "$var" = "test" ]; then
  echo "OK"
fi

# ✅ New style (safer)
if [[ -n $var && $var == test ]]; then
  echo "OK"
fi
```

## Per-Script Configuration

To disable a check for a specific script:

```bash
#!/bin/bash
# shellcheck disable=SC2086,SC1091

# script content
```

To set shell dialect for a script:

```bash
#!/bin/bash
# shellcheck shell=bash

# script content
```

To disable a check for a single line:

```bash
# shellcheck disable=SC2076
[[ "$var" == *.txt ]]
```

## IDE Integration

### VS Code

Install the "ShellCheck" extension:
- Automatically uses `.shellcheckrc`
- Real-time linting as you type
- Quick fixes for common issues

### IntelliJ IDEs (PhpStorm, WebStorm, GoLand, etc.)

Built-in ShellCheck support:
1. Settings → Languages & Frameworks → Shell Script
2. Enable ShellCheck
3. Point to `.shellcheckrc` in project root

### Vim/Neovim

Use with ALE or Syntastic plugins:
- ALE automatically respects `.shellcheckrc`
- Syntastic: Configure shellcheck path

## Workflow

### Pre-Commit (Local)

```bash
# 1. Run linting before commit
npm run lint:shell

# 2. Review output
# 3. Fix issues in scripts

# 4. Verify fixes
npm run lint:shell

# 5. Commit when passing
```

### CI/CD (Automated)

1. **Push/PR**: Workflow triggers automatically
2. **Linting**: ShellCheck runs with configuration
3. **Report**: JSON artifact generated and linked
4. **Comment**: PR gets automated comment with results
5. **Status**: Check passes/fails based on issues found

## Installation (If Needed)

### macOS
```bash
brew install shellcheck
```

### Ubuntu/Debian
```bash
sudo apt-get install shellcheck
```

### Docker
```bash
docker run --rm -v "$PWD:/workspace" -w /workspace \
  koalaman/shellcheck-alpine:latest *.sh
```

## Troubleshooting

### ShellCheck not found

**Error**: `shellcheck: command not found`

**Solution**:
```bash
# Check if installed
which shellcheck

# Install if missing
sudo apt-get install shellcheck  # Linux
brew install shellcheck          # macOS
```

### Configuration not applied

**Ensure**:
1. `.shellcheckrc` is in project root
2. Scripts use correct command: `shellcheck --config=.shellcheckrc`
3. Reload shell/IDE after creating config

### Too many false positives

1. Review disabled checks in `.shellcheckrc`
2. Add per-script overrides if needed: `# shellcheck disable=SC####`
3. Consider if script needs specific shell dialect

## References

- [ShellCheck GitHub](https://www.shellcheck.net/)
- [ShellCheck Wiki](https://www.shellcheck.net/wiki/)
- [ShellCheck SC Code Reference](https://www.shellcheck.net/wiki/)
- [Bash Guide](https://mywiki.wooledge.org/BashGuide)

## Next Steps

1. ✅ Configuration created
2. Run baseline linting: `npm run lint:shell`
3. Review and fix issues by priority
4. Implement per-script overrides as needed
5. Verify CI/CD passing on PRs

---

**Last Updated**: 2026-02-12  
**Configuration Version**: 1.0.0  
**Project**: Agent-Augmented Development Framework

