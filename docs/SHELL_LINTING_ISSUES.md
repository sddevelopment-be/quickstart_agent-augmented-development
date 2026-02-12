# Shell Linting Issues Detected in Your Project

## Issues That ShellCheck Will Catch

### 1. **Use `[[` instead of `[` for conditional tests**

ShellCheck recommends using `[[` (bash conditional construct) instead of `[` (POSIX test command) because `[[` is safer and more feature-rich.

**Location**: `.github/copilot/setup.sh` (multiple occurrences)

**Issues Found**:
- Line 85: `if [ ! -f "$file_path" ]; then`
- Line 103: `if [ "$actual_checksum" = "$expected_checksum" ]; then`
- Line 111: `if [ -n "$version_check" ]; then`
- Line 127: `if [ -n "$install_cmd" ]; then`
- Line 142: `if [ "$os" = "unknown" ]; then`
- Line 149: `if [ "$os" = "linux" ]; then`
- And more throughout the file

**Why Use `[[`?**
- ✅ No word splitting or pathname expansion
- ✅ Safer string comparisons
- ✅ Supports regex matching with `=~`
- ✅ Supports pattern matching with `*`
- ✅ More readable and intuitive
- ✅ Logical operators: `&&`, `||` instead of `-a`, `-o`

**Example Fix**:
```bash
# ❌ Old style (with [)
if [ ! -f "$file_path" ]; then
    echo "File not found"
fi

# ✅ New style (with [[)
if [[ ! -f $file_path ]]; then
    echo "File not found"
fi
```

### 2. **Unquoted Variables (SC2086)**

**Status**: Disabled in `.shellcheckrc` (project allows controlled expansion)

Some instances of unquoted variables in the setup.sh script that could cause word splitting:
- Line 129: `$($version_check 2>/dev/null || echo "unknown")`
- Line 169: `eval "$install_cmd"`

**Note**: These are in controlled contexts and would be caught by SC2086 if enabled.

### 3. **Exit Code Comparison (SC2181)**

**Status**: Disabled in `.shellcheckrc` (common pattern in project)

Example:
```bash
if eval "$install_cmd"; then
    # This is pattern SC2181 checks for
```

**Note**: This pattern is acceptable and disabled in configuration.

## How to Run the Linting

### Locally

```bash
# Check all shell scripts
npm run lint:shell

# Generate detailed JSON report
npm run lint:shell:report

# Integrated validation (text + shell)
npm run lint
```

### On GitHub

The `.github/workflows/shell-lint.yml` workflow will automatically:
- Run on push/PR to main/develop with `*.sh` changes
- Comment on PRs with results
- Upload JSON artifact
- Fail the check if issues found

## Recommended Fixes for setup.sh

### Fix 1: Replace `[` with `[[`

Change all instances of `[ condition ]` to `[[ condition ]]` throughout the script.

**Example**:
```bash
# Line 85
# Before:
if [ ! -f "$file_path" ]; then

# After:
if [[ ! -f $file_path ]]; then
```

**Pattern to replace**:
- `[ ` → `[[ `
- ` ]` → ` ]]`

But be careful with:
- `[ -a` and `[ -o` become `[[` with `&&` and `||`
- String quoting can often be removed in `[[`

### Fix 2: Add ShellCheck Directive (Optional)

If you want to suppress the `[[` warning for specific sections, add:

```bash
# shellcheck disable=SC2039
if [ "$os" = "linux" ]; then
```

But it's better to fix the code than to suppress the check.

## Configuration Summary

Your ShellCheck configuration (`.shellcheckrc`) has:
- ✅ All optional checks enabled
- ✅ SC2086 disabled (allows controlled word splitting)
- ✅ SC1091 disabled (dynamic sourcing allowed)
- ✅ SC2181 disabled (exit code patterns allowed)

This means the `[[` vs `[` issue WILL be caught and reported.

## Next Steps

1. **Run baseline linting**: `npm run lint:shell`
2. **Review output**: Check the issues reported
3. **Fix setup.sh first**: Replace `[` with `[[` 
4. **Test locally**: `npm run lint:shell` should pass
5. **Create PR**: Workflow will verify automatically

## Helpful Resources

- **ShellCheck Wiki**: https://www.shellcheck.net/wiki/
- **Bash Guide**: https://mywiki.wooledge.org/BashGuide
- **Best Practices**: https://www.shellcheck.net/wiki/SC2006

## Quick Reference: `[` vs `[[`

| Feature | `[` | `[[` |
|---------|-----|------|
| Word splitting | ❌ Unsafe | ✅ Safe |
| Pathname expansion | ❌ Unsafe | ✅ Safe |
| String comparison | ⚠️ Fragile | ✅ Robust |
| Regex matching | ❌ Not supported | ✅ `=~` operator |
| Pattern matching | ❌ Not supported | ✅ `*` wildcards |
| POSIX compatible | ✅ Yes | ❌ Bash only |

---

**Configuration Date**: 2026-02-12  
**ShellCheck Version**: Latest (via apt)  
**Linting Framework**: Agent-Augmented Development

