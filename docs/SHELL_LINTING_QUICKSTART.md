# Shell Linting - Quick Reference

## Files Added to Your Project

### 1. Configuration
- **`.shellcheckrc`** - ShellCheck configuration (project root)
- **`.github/workflows/shell-lint.yml`** - GitHub Actions workflow

### 2. Documentation
- **`docs/shell-linting-guide.md`** - Comprehensive user guide
- **`docs/SHELL_LINTING_ISSUES.md`** - Issues found and how to fix them

### 3. npm Scripts (in package.json)
- **`npm run lint:shell`** - Validate all shell scripts
- **`npm run lint:shell:report`** - Generate JSON report
- **`npm run lint`** - Updated to include shell linting

## Quick Commands

```bash
# Check all shell scripts
npm run lint:shell

# Generate detailed JSON report
npm run lint:shell:report

# Run integrated validation (text + shell)
npm run lint
```

## Key Issues That Will Be Caught

### 1. Use `[[` instead of `[` for Conditionals

✅ **ShellCheck will catch**: All uses of `[` in conditional tests

```bash
# ❌ Current (will be flagged)
if [ "$os" = "unknown" ]; then
    exit 1
fi

# ✅ Recommended (passes)
if [[ $os == unknown ]]; then
    exit 1
fi
```

### 2. Other Common Issues

- Unquoted variables that cause word splitting
- Backticks instead of `$()`
- Using `ls` for parsing file listings
- Array assignment issues
- And 50+ other shell script issues

## Files Affected

Your project has 22 shell scripts. Key ones with issues:
- `.github/copilot/setup.sh` - Multiple `[` vs `[[` issues

## Configuration

The `.shellcheckrc` file is already configured to:
- Enable all optional checks
- Disable SC2086 (word splitting) - project allows controlled expansion
- Disable SC1091 (source file) - dynamic sourcing patterns
- Disable SC2181 (exit code) - common pattern in project

## How to Fix Issues

1. Run: `npm run lint:shell`
2. Review the output for each file
3. Update scripts according to recommendations
4. Most common fix: Replace `[ ` with `[[ ` and ` ]` with ` ]]`

## Integration

- ✅ Runs automatically on push/PR to main/develop
- ✅ Comments on PRs with results
- ✅ Stores JSON report artifacts (30 days)
- ✅ Part of `npm run lint` validation suite

## See Also

- `docs/shell-linting-guide.md` - Full guide with examples
- `docs/SHELL_LINTING_ISSUES.md` - Detailed issue documentation
- `.shellcheckrc` - Configuration file (in project root)

---

**Status**: ✅ Configuration Complete, Ready for Use  
**Date**: 2026-02-12

