#!/usr/bin/env bash
# validate-doctrine-dependencies.sh
# 
# Validates that the doctrine/ directory maintains zero outgoing dependencies
# to ensure portability and self-containment.
#
# Usage:
#   ./validate-doctrine-dependencies.sh [--strict]
#
# Options:
#   --strict    Fail on warnings (template examples with .github/agents)
#
# Exit codes:
#   0 - All validations passed
#   1 - Critical violations found
#   2 - Warnings found (only in --strict mode)

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0
STRICT_MODE=false

# Parse arguments
if [[ "${1:-}" == "--strict" ]]; then
    STRICT_MODE=true
fi

# Find repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DOCTRINE_DIR="$REPO_ROOT/doctrine"

echo -e "${BLUE}=== Doctrine Dependency Validation ===${NC}"
echo "Repository: $REPO_ROOT"
echo "Doctrine: $DOCTRINE_DIR"
echo ""

# Check 1: Unparameterized paths to work/
echo -e "${BLUE}[1/8] Checking for unparameterized 'work/' references...${NC}"
UNPARAMETERIZED_WORK=$(grep -rn "['\"\`]work/" "$DOCTRINE_DIR" --include="*.md" --include="*.yaml" --include="*.yml" \
    | grep -v '\${WORKSPACE_ROOT}' \
    | grep -v '# Example:\|For example:\|e.g.\|Usage:\|File:\|Path:\|Directory:' \
    | grep -v 'workflow\|network\|framework\|rework\|homework\|worklog' \
    | grep -v 'task templates\|template\|comment\|example' \
    || true)

if [[ -n "$UNPARAMETERIZED_WORK" ]]; then
    echo -e "${RED}❌ FAIL: Found unparameterized 'work/' references${NC}"
    echo "$UNPARAMETERIZED_WORK"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ PASS: No unparameterized 'work/' references${NC}"
fi
echo ""

# Check 2: Unparameterized paths to docs/
echo -e "${BLUE}[2/8] Checking for unparameterized 'docs/' references...${NC}"
UNPARAMETERIZED_DOCS=$(grep -rn "docs/" "$DOCTRINE_DIR" --include="*.md" --include="*.yaml" --include="*.yml" \
    | grep -v '\${DOC_ROOT}' \
    | grep -v '# Example:\|For example:\|e.g.' \
    | grep -v 'documents\|documented' \
    || true)

if [[ -n "$UNPARAMETERIZED_DOCS" ]]; then
    echo -e "${RED}❌ FAIL: Found unparameterized 'docs/' references${NC}"
    echo "$UNPARAMETERIZED_DOCS"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ PASS: No unparameterized 'docs/' references${NC}"
fi
echo ""

# Check 3: Unparameterized paths to specifications/
echo -e "${BLUE}[3/8] Checking for unparameterized 'specifications/' references...${NC}"
UNPARAMETERIZED_SPECS=$(grep -rn "specifications/" "$DOCTRINE_DIR" --include="*.md" --include="*.yaml" --include="*.yml" \
    | grep -v '\${SPEC_ROOT}' \
    | grep -v '# Example:\|For example:\|e.g.' \
    || true)

if [[ -n "$UNPARAMETERIZED_SPECS" ]]; then
    echo -e "${RED}❌ FAIL: Found unparameterized 'specifications/' references${NC}"
    echo "$UNPARAMETERIZED_SPECS"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ PASS: No unparameterized 'specifications/' references${NC}"
fi
echo ""

# Check 4: Tool-specific directory references
echo -e "${BLUE}[4/8] Checking for tool-specific directory references...${NC}"
TOOL_REFS=$(grep -rn "\.github/\|\.claude/\|\.cursor/" "$DOCTRINE_DIR" --include="*.md" --include="*.yaml" --include="*.yml" \
    | grep -v "\.github/agents" \
    | grep -v '# Example:\|For example:\|e.g.\|Template example' \
    | grep -v 'GUARDIAN_\|framework-audit\|framework-upgrade' \
    || true)

if [[ -n "$TOOL_REFS" ]]; then
    echo -e "${RED}❌ FAIL: Found tool-specific directory references${NC}"
    echo "$TOOL_REFS"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ PASS: No tool-specific directory references${NC}"
fi
echo ""

# Check 5: Invalid variable usage
echo -e "${BLUE}[5/8] Checking for invalid path variables...${NC}"
VALID_VARS=('WORKSPACE_ROOT' 'DOC_ROOT' 'SPEC_ROOT' 'OUTPUT_ROOT' 'LOCAL_DOCTRINE_ROOT')
INVALID_VARS=$(grep -rn '\${[A-Z_]*}' "$DOCTRINE_DIR" --include="*.md" --include="*.yaml" --include="*.yml" \
    | grep -v '\${WORKSPACE_ROOT}\|\${DOC_ROOT}\|\${SPEC_ROOT}\|\${OUTPUT_ROOT}\|\${LOCAL_DOCTRINE_ROOT}' \
    | grep -v 'variable\|placeholder\|example' \
    || true)

if [[ -n "$INVALID_VARS" ]]; then
    echo -e "${YELLOW}⚠️  WARNING: Found potentially invalid path variables${NC}"
    echo "$INVALID_VARS"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✅ PASS: All path variables are valid${NC}"
fi
echo ""

# Check 6: Legacy specific_guidelines paths
echo -e "${BLUE}[6/8] Checking for legacy specific_guidelines paths...${NC}"
LEGACY_SPECIFIC_GUIDELINES=$(grep -rn '\${DOC_ROOT}/specific_guidelines\.md\|docs/specific_guidelines\.md' "$DOCTRINE_DIR" \
    --include="*.md" --include="*.yaml" --include="*.yml" \
    || true)

if [[ -n "$LEGACY_SPECIFIC_GUIDELINES" ]]; then
    echo -e "${RED}❌ FAIL: Found legacy specific_guidelines path references${NC}"
    echo "$LEGACY_SPECIFIC_GUIDELINES"
    echo "Expected: .doctrine-config/specific_guidelines.md or \${LOCAL_DOCTRINE_ROOT}/specific_guidelines.md"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ PASS: No legacy specific_guidelines path references${NC}"
fi
echo ""

# Check 7: Doctrine stack cross-directory boundary
echo -e "${BLUE}[7/8] Checking doctrine stack cross-directory references...${NC}"
STACK_FILE="$DOCTRINE_DIR/DOCTRINE_STACK.md"
STACK_FORBIDDEN_REFS=$(grep -nE '(src/|tools/|tests/|fixtures/|work/|output/|collaboration/|ops/|specifications/|docs/|\\./\\./|\\.\\./)' "$STACK_FILE" \
    | grep -v '\.doctrine-config/' \
    | grep -v '\${' \
    || true)

if [[ -n "$STACK_FORBIDDEN_REFS" ]]; then
    echo -e "${RED}❌ FAIL: Found forbidden cross-directory references in DOCTRINE_STACK.md${NC}"
    echo "$STACK_FORBIDDEN_REFS"
    echo "Allowed references are doctrine-local paths, expected local override locations (.doctrine-config), and placeholders."
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ PASS: DOCTRINE_STACK.md respects cross-directory boundary rules${NC}"
fi
echo ""

# Check 8: Template examples with .github/agents (warnings only)
echo -e "${BLUE}[8/8] Checking template examples...${NC}"
TEMPLATE_EXAMPLES=$(grep -rn "\.github/agents" "$DOCTRINE_DIR/templates" --include="*.md" 2>/dev/null || true)
TEMPLATE_COUNT=$(echo "$TEMPLATE_EXAMPLES" | grep -c "\.github/agents" || true)

if [[ $TEMPLATE_COUNT -gt 0 ]]; then
    echo -e "${YELLOW}⚠️  INFO: Found $TEMPLATE_COUNT .github/agents references in templates (examples)${NC}"
    if [[ "$STRICT_MODE" == true ]]; then
        echo "$TEMPLATE_EXAMPLES"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "These are template examples and may be acceptable in context."
    fi
else
    echo -e "${GREEN}✅ PASS: No .github/agents references in templates${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}=== Validation Summary ===${NC}"
echo "Directory: $DOCTRINE_DIR"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}❌ VALIDATION FAILED: $ERRORS critical violation(s) found${NC}"
    exit 1
elif [[ $WARNINGS -gt 0 ]] && [[ "$STRICT_MODE" == true ]]; then
    echo -e "${YELLOW}⚠️  VALIDATION WARNING: $WARNINGS warning(s) found (strict mode)${NC}"
    exit 2
else
    echo -e "${GREEN}✅ VALIDATION PASSED: doctrine/ is portable with zero dependencies${NC}"
    exit 0
fi
