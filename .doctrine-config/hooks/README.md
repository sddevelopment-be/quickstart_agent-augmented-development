# Git Hooks and Automation

**Purpose:** Repository-specific git hooks and automation scripts for enforcing doctrine compliance.

---

## Available Hooks

### Pre-Commit Hooks

**Location:** Place executable scripts in this directory, symlink from `.git/hooks/`

Example hooks:

1. **check-phase-declaration.sh** - Verify commit messages include phase declarations (Directive 034)
2. **validate-work-logs.sh** - Ensure work logs exist for completed tasks (Directive 014)
3. **check-doctrine-consistency.sh** - Verify doctrine exports match source files
4. **prevent-distribution-edits.sh** - Block manual edits to generated files (.github/, .claude/, .opencode/)

### Post-Commit Hooks

1. **update-work-index.sh** - Regenerate work/ directory index after commits
2. **trigger-export.sh** - Auto-run exporters when doctrine/ files change

### Pre-Push Hooks

1. **verify-tests-passing.sh** - Block push if tests fail
2. **check-review-approval.sh** - Verify Phase 6 reviews exist for specs

---

## Installation

```bash
# Link hooks to git
ln -sf ../../.doctrine-config/hooks/pre-commit .git/hooks/pre-commit
ln -sf ../../.doctrine-config/hooks/pre-push .git/hooks/pre-push
chmod +x .doctrine-config/hooks/*
```

---

## Hook Template

```bash
#!/bin/bash
# Hook: check-phase-declaration
# Purpose: Verify commit messages follow phase declaration format

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Check if this is a phase-related commit
if echo "$COMMIT_MSG" | grep -qE "Phase [1-6]"; then
    # Verify format: "agent-slug: Phase N - description"
    if ! echo "$COMMIT_MSG" | grep -qE "^[a-z-]+: Phase [1-6]"; then
        echo "❌ ERROR: Phase commits must follow format:"
        echo "   agent-slug: Phase N - description"
        echo ""
        echo "See: .doctrine-config/repository-guidelines.md"
        exit 1
    fi
fi

exit 0
```

---

## Current Hooks

_(None yet - this is the template directory)_

To enable enforcement:
1. Create hook scripts in this directory
2. Make them executable (`chmod +x`)
3. Symlink from `.git/hooks/`
4. Test with `git commit --dry-run`

---

**Maintained by:** Repository maintainers  
**Enable when:** Process enforcement needed
