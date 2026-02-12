# Shell Script Style Guide

**Framework**: Agent-Augmented Development  
**Last Updated**: February 12, 2026  
**Status**: Active  
**Enforcement**: Automated via ShellCheck

---

## ⚠️ MANDATORY: Variable Bracing Convention

**All variable references MUST use braces: `${VAR}` not `$VAR`**

**ShellCheck Code**: SC2250 (ENFORCED - not optional)  
**Severity**: HIGH  
**Applies To**: ALL variable references in shell scripts

This is not a style preference—it is a **required safety practice** that prevents:
- Word splitting bugs
- Pathname expansion errors
- Edge cases with adjacent characters
- Unintended variable boundary issues

---

## Overview

This styleguide establishes best practices for shell scripts in the agent-augmented development framework. All shell scripts must comply with these standards as enforced by ShellCheck linting.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Conditional Expressions](#conditional-expressions)
3. [Variable Usage](#variable-usage)
4. [Quoting and Escaping](#quoting-and-escaping)
5. [Command Substitution](#command-substitution)
6. [Common Errors & Fixes](#common-errors--fixes)
7. [Best Practices](#best-practices)
8. [Validation](#validation)

---

## Core Principles

### 1. Use Modern Bash Syntax
- Target bash 3.0+ (introduced in 2004)
- Use modern constructs over deprecated POSIX equivalents
- Prioritize safety and clarity over brevity

### 2. Defensive Programming
- Always quote variables: `"${VAR}"` not `$VAR`
- Always brace variables: `${VAR}` for parameter expansion
- Always use `set -euo pipefail` at script start

### 3. Clarity Over Cleverness
- Write scripts that are easy to understand
- Explicit is better than implicit
- Comments should explain "why," not "what"

---

## Conditional Expressions

### Use `[[` Instead of `[`

**Rule**: Use bash conditional expression `[[...]]` instead of the POSIX test command `[...]` for arithmetic and string comparisons.

#### ❌ Incorrect (Old POSIX Style)
```bash
if [ $? -eq 0 ]; then
    echo "Success"
fi

if [ "$var" = "test" ]; then
    echo "Match"
fi

if [ -n $file ]; then
    echo "File set"
fi
```

#### ✅ Correct (Modern Bash Style)
```bash
if [[ $? -eq 0 ]]; then
    echo "Success"
fi

if [[ $var == test ]]; then
    echo "Match"
fi

if [[ -n ${file} ]]; then
    echo "File set"
fi
```

### Why Use `[[`?

| Feature | `[` | `[[` |
|---------|-----|------|
| Word splitting | ❌ Unsafe | ✅ Safe |
| Pathname expansion | ❌ Unsafe | ✅ Safe |
| Arithmetic operators | ⚠️ Limited | ✅ Full support |
| String comparison | ⚠️ Fragile | ✅ Robust |
| Regex matching (`=~`) | ❌ Not supported | ✅ Supported |
| Pattern matching | ❌ Not supported | ✅ Supported |

### Error SC2292 - This Issue Was Fixed

**ShellCheck Code**: SC2292  
**Message**: "Prefer [[ ]] over [ ] for tests in Bash/Ksh"  
**Impact**: HIGH - can cause unexpected behavior

**Example from project fix**:
```bash
# Line 17 - BEFORE (WRONG)
if [ $? -eq 0 ]; then

# Line 17 - AFTER (CORRECT)
if [[ $? -eq 0 ]]; then
```

---

## Variable Usage

### Always Use Braces Around Variables

**Rule**: Always use `${VAR}` syntax, not `$VAR`, for variable expansion.

#### ❌ Incorrect
```bash
# Word splitting risk
files=$var
rm $files

# Unclear boundaries
echo "Processing $file.txt"

# Numeric comparison
if [ $count -eq 0 ]; then

# In command substitution
result=$(cd "$SCRIPT_DIR/../.." && pwd)
```

#### ✅ Correct
```bash
# Protected from word splitting
files=${var}
rm ${files}

# Clear variable boundaries
echo "Processing ${file}.txt"

# Numeric comparison with braces
if [[ ${count} -eq 0 ]]; then

# In command substitution
result=$(cd "${SCRIPT_DIR}/../.." && pwd)
```

### Why Use Braces?

1. **Word Splitting Protection**: Prevents unexpected word splitting with spaces
2. **Boundary Clarity**: Makes variable boundaries explicit in complex strings
3. **Edge Case Prevention**: Eliminates entire class of parameter expansion bugs
4. **Consistency**: Uniform approach throughout codebase
5. **Maintainability**: Easier to read and modify

### Error SC2250 - This Issue Was Fixed

**ShellCheck Code**: SC2250  
**Message**: "Prefer putting braces around variable references even when not strictly required"  
**Impact**: MEDIUM - potential issues with spaces or special characters

**Example from project fix**:
```bash
# Line 21 - BEFORE (WRONG)
shellcheck $FILES 2>&1

# Line 21 - AFTER (CORRECT)
shellcheck ${FILES} 2>&1

# Line 28 - BEFORE (WRONG)
if [[ -n $file ]]; then

# Line 28 - AFTER (CORRECT)
if [[ -n ${file} ]]; then
```

---

## Quoting and Escaping

### Quote All Variable Expansions

**Rule**: Always quote variable expansions: `"${VAR}"` not `${VAR}` (unless you specifically want word splitting).

#### ❌ Incorrect
```bash
# Could split on spaces
for file in $files; do
    process $file
done

# Pathname expansion
echo $directory/*

# Command substitution result might split
result=$(find . -name "*.sh")
for script in $result; do
    lint $script
done
```

#### ✅ Correct
```bash
# Protected from word splitting
for file in ${files}; do
    process "${file}"
done

# Escaped pathname expansion
echo "${directory}"/*

# Command substitution properly quoted
mapfile -t scripts < <(find . -name "*.sh")
for script in "${scripts[@]}"; do
    lint "${script}"
done
```

### String Comparison in `[[`

In `[[` expressions, you can compare unquoted variables:

```bash
# This is safe in [[ ]]
if [[ ${var} == test ]]; then
    # ...
fi

# String with spaces is fine
if [[ ${name} == John Doe ]]; then
    # ...
fi
```

---

## Command Substitution

### Use `$()` Instead of Backticks

**Rule**: Always use `$()` for command substitution, never backticks.

#### ❌ Incorrect (Deprecated Backticks)
```bash
version=`git --version`
scripts=`find . -name "*.sh"`
result=`echo "test" | sed 's/test/passed/'`
```

#### ✅ Correct (Modern `$()`)
```bash
version=$(git --version)
scripts=$(find . -name "*.sh")
result=$(echo "test" | sed 's/test/passed/')
```

### Why Use `$()`?

1. **Nesting**: Can nest multiple command substitutions easily: `$(cmd1 $(cmd2))`
2. **Readability**: Clearer where substitution starts and ends
3. **Consistency**: Matches modern shell standards
4. **Escaping**: Easier to escape special characters

---

## Common Errors & Fixes

### Error 1: Using `[` for Arithmetic Comparisons

**ShellCheck**: SC2292  
**Severity**: HIGH

```bash
# ❌ WRONG
if [ $exit_code -eq 0 ]; then
    echo "Success"
fi

# ✅ CORRECT
if [[ ${exit_code} -eq 0 ]]; then
    echo "Success"
fi
```

### Error 2: Unbraced Variables

**ShellCheck**: SC2250  
**Severity**: MEDIUM

```bash
# ❌ WRONG
mkdir -p $output_dir
cat $input_file >> $tmp_dir/temp.txt
grep "pattern" $file

# ✅ CORRECT
mkdir -p "${output_dir}"
cat "${input_file}" >> "${tmp_dir}/temp.txt"
grep "pattern" "${file}"
```

### Error 3: Unquoted Variables in Word Contexts

**ShellCheck**: SC2086  
**Severity**: HIGH (disabled in this project for specific patterns)

```bash
# ❌ WRONG (word splitting)
for item in $list; do
    process $item
done

# ✅ CORRECT (properly quoted)
for item in ${list}; do
    process "${item}"
done
```

### Error 4: Backticks Instead of `$()`

**ShellCheck**: SC2006  
**Severity**: MEDIUM

```bash
# ❌ WRONG
version=`command --version`

# ✅ CORRECT
version=$(command --version)
```

### Error 5: Using `echo` for Escape Sequences

**ShellCheck**: SC2028  
**Severity**: LOW (informational)

```bash
# ❌ WRONG (may not expand \n)
echo "Line 1\nLine 2"

# ✅ CORRECT (printf guaranteed to work)
printf "Line 1\nLine 2\n"

# ✅ ALSO OK (with -e flag, but less portable)
echo -e "Line 1\nLine 2"
```

### Error 6: Using `ls` for Parsing File Lists

**ShellCheck**: SC2012  
**Severity**: MEDIUM

```bash
# ❌ WRONG (unreliable parsing)
for file in $(ls *.txt); do
    process "$file"
done

# ✅ CORRECT (safe parsing)
for file in *.txt; do
    process "$file"
done

# ✅ ALSO CORRECT (for recursive)
find . -name "*.txt" -print0 | while IFS= read -r -d '' file; do
    process "$file"
done
```

---

## Best Practices

### Script Header

Every shell script should start with:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Script description
# Purpose: What this script does
# Usage: How to run it
# Author: Who wrote it (optional)
```

**Explanation**:
- `#!/usr/bin/env bash`: Portable bash shebang
- `set -e`: Exit on error
- `set -u`: Exit on undefined variable
- `set -o pipefail`: Exit if any pipe command fails

### Function Definitions

```bash
# Good function structure
log_info() {
    local message="$1"
    echo "[INFO] ${message}"
}

process_file() {
    local filepath="$1"
    local output="$2"
    
    if [[ ! -f "${filepath}" ]]; then
        echo "Error: File not found: ${filepath}" >&2
        return 1
    fi
    
    # Process the file
    cat "${filepath}" >> "${output}"
}
```

### Error Handling

```bash
# Good error handling pattern
if ! command --option; then
    echo "Error: command failed" >&2
    exit 1
fi

# Or with explicit error message
local result
if ! result=$(some_command); then
    echo "Error: Failed to execute: ${result}" >&2
    return 1
fi
```

### Logging

```bash
# Structured logging
log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [INFO] $*" >&2
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [ERROR] $*" >&2
}

log_info "Starting process"
log_error "Something went wrong"
```

---

## Validation

### Running ShellCheck Locally

```bash
# Check single script
shellcheck script.sh

# Check all scripts
npm run lint:shell

# Generate detailed report
npm run lint:shell:report

# Check with specific format
shellcheck --format=json *.sh
```

### ShellCheck Configuration

This project uses `.shellcheckrc` to configure ShellCheck. Key settings:

```ini
enable=all                      # Enable all optional checks
disable=SC1091,SC2086,SC2181   # Disable specific rules for project patterns
format=gcc                      # GCC-compatible output format
severity=warning                # Include all severity levels
shell=bash                      # Target bash dialect
```

### CI/CD Integration

ShellCheck is integrated into the build pipeline:

```bash
# Automated on push/PR
.github/workflows/shell-lint.yml

# Run locally before committing
npm run lint:shell
```

---

## Project-Specific Decisions

### Why SC2086 is Disabled

**Rule**: SC2086 - Double quote to prevent globbing and word splitting

This rule is disabled in `.shellcheckrc` because the project uses controlled variable expansion in specific contexts where word splitting is intentional or managed.

**Override if needed**:
```bash
# Disable for specific line
# shellcheck disable=SC2086
for file in $list; do
    # ...
done
```

### Why SC1091 is Disabled

**Rule**: SC1091 - Not following sourced file

This rule is disabled because the project uses dynamic sourcing patterns where the sourced file path cannot be determined statically.

### Why SC2181 is Disabled

**Rule**: SC2181 - Check exit code directly with success/failure of last command

This rule is disabled because the project uses common patterns like:
```bash
if command; then
    # Process success
fi
```

---

## Summary of Key Rules

| Issue | Code | Severity | Solution |
|-------|------|----------|----------|
| Use `[[ ]]` for conditionals | SC2292 | HIGH | Replace `[ ]` with `[[ ]]` |
| Add variable braces | SC2250 | MEDIUM | Use `${VAR}` not `$VAR` |
| Unquoted variables | SC2086 | HIGH | Quote: `"${VAR}"` |
| Use `$()` not backticks | SC2006 | MEDIUM | Replace backticks with `$()` |
| Use `printf` not `echo` | SC2028 | LOW | Use `printf` for escape sequences |
| Don't parse `ls` output | SC2012 | MEDIUM | Use glob patterns or `find` |

---

## References

- [ShellCheck Official](https://www.shellcheck.net/)
- [ShellCheck Wiki](https://www.shellcheck.net/wiki/)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Community Shell Scripting Standards](https://mywiki.wooledge.org/BashGuide)

---

## Changelog

### Version 1.0.0 (February 12, 2026)

**Initial Release**
- Established baseline shell script standards
- Documented common errors and fixes
- Included project-specific configurations
- Added validation procedures
- Integrated with ShellCheck linting

**Errors Documented**:
- SC2292: Use `[[` instead of `[` (2 instances fixed)
- SC2250: Add variable braces (5+ instances fixed)
- SC2006: Use `$()` instead of backticks
- SC2012: Don't parse `ls` output
- SC2028: Use `printf` instead of `echo`
- SC2086: Quote variables (project-specific override)

---

**Document Version**: 1.0.0  
**Framework**: Agent-Augmented Development  
**Maintained By**: DevOps Specialist (DevOps Danny)  
**Enforcement**: Automated via ShellCheck in CI/CD pipeline

