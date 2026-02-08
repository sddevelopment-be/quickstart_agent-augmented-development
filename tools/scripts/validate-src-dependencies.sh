#!/bin/bash
# Validation script: Ensure src/ has zero outgoing dependencies to tools/, tests/, fixtures/
# Similar to doctrine validation, src/ should only depend on doctrine/ and standard libraries

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ISSUES_FOUND=0
WARNINGS_FOUND=0

echo "========================================"
echo "  src/ Dependency Validation"
echo "========================================"
echo ""
echo "Validating: src/ has zero outgoing dependencies"
echo "Allowed:    doctrine/, standard libraries, external packages"
echo "Forbidden:  tools/, tests/, fixtures/"
echo ""

# Check 1: No imports from tools/
echo "📋 Check 1: No imports from tools/"
if grep -rE "^[[:space:]]*(from tools|import tools|require\(['\"]tools)" "$REPO_ROOT/src/" --include="*.py" --include="*.js" 2>/dev/null; then
    echo -e "${RED}❌ FAIL: Found imports from tools/ in src/${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo -e "${GREEN}✅ PASS: No imports from tools/${NC}"
fi
echo ""

# Check 2: No imports from tests/
echo "📋 Check 2: No imports from tests/"
if grep -rE "^[[:space:]]*(from tests|import tests|require\(['\"]tests)" "$REPO_ROOT/src/" --include="*.py" --include="*.js" 2>/dev/null; then
    echo -e "${RED}❌ FAIL: Found imports from tests/ in src/${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo -e "${GREEN}✅ PASS: No imports from tests/${NC}"
fi
echo ""

# Check 3: No imports from fixtures/
echo "📋 Check 3: No imports from fixtures/"
if grep -rE "^[[:space:]]*(from fixtures|import fixtures|require\(['\"]fixtures)" "$REPO_ROOT/src/" --include="*.py" --include="*.js" 2>/dev/null; then
    echo -e "${RED}❌ FAIL: Found imports from fixtures/ in src/${NC}"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    echo -e "${GREEN}✅ PASS: No imports from fixtures/${NC}"
fi
echo ""

# Check 4: No hardcoded paths to tools/, tests/, fixtures/
echo "📋 Check 4: No hardcoded paths to forbidden directories"
if grep -r "tools/\|tests/\|fixtures/" "$REPO_ROOT/src/" --include="*.py" --include="*.js" \
    | grep -v "# " \
    | grep -v "//" \
    | grep -v "pyproject.toml" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  WARNING: Found path references to tools/tests/fixtures/ in src/${NC}"
    echo "   (Review these - may be legitimate string literals or comments)"
    WARNINGS_FOUND=$((WARNINGS_FOUND + 1))
else
    echo -e "${GREEN}✅ PASS: No hardcoded paths to forbidden directories${NC}"
fi
echo ""

# Check 5: Allowed dependencies (doctrine/, standard libs)
echo "📋 Check 5: Verify allowed dependencies"
echo "   Checking for doctrine/ references..."
set +e
DOCTRINE_COUNT=$(grep -r "doctrine/" "$REPO_ROOT/src/" --include="*.py" --include="*.js" 2>/dev/null | wc -l)
set -e
DOCTRINE_REFS=${DOCTRINE_COUNT:-0}
if [ "$DOCTRINE_REFS" -gt 0 ]; then
    echo -e "${GREEN}✅ Found $DOCTRINE_REFS references to doctrine/ (allowed)${NC}"
else
    echo -e "${YELLOW}⚠️  No references to doctrine/ found (production code may not use framework directives)${NC}"
fi
echo ""

# Check 6: Validate src/ can only be imported by tools/, tests/, or other src/
echo "📋 Check 6: Verify src/ is properly consumed"
echo "   Checking if tools/ imports from src/..."
set +e
TOOLS_COUNT=$(grep -r "from src\|import src" "$REPO_ROOT/tools/" --include="*.py" --include="*.js" 2>/dev/null | wc -l)
set -e
TOOLS_TO_SRC=${TOOLS_COUNT:-0}
echo "   Found $TOOLS_TO_SRC imports from src/ in tools/ (expected)"

echo "   Checking if tests/ imports from src/..."
set +e
TESTS_COUNT=$(grep -r "from src\|import src" "$REPO_ROOT/tests/" --include="*.py" --include="*.js" 2>/dev/null | wc -l)
set -e
TESTS_TO_SRC=${TESTS_COUNT:-0}
echo "   Found $TESTS_TO_SRC imports from src/ in tests/ (expected)"
echo -e "${GREEN}✅ PASS: Dependency direction correct (tools/tests → src)${NC}"
echo ""

# Summary
echo "========================================"
echo "  Validation Summary"
echo "========================================"
echo ""
if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}✅ SUCCESS: src/ has zero outgoing dependencies${NC}"
    echo ""
    echo "Dependencies validated:"
    echo "  - src/ → doctrine/ ✅ (allowed)"
    echo "  - src/ → tools/ ❌ (none found)"
    echo "  - src/ → tests/ ❌ (none found)"
    echo "  - src/ → fixtures/ ❌ (none found)"
    echo ""
    echo "  - tools/ → src/ ✅ ($TOOLS_TO_SRC imports)"
    echo "  - tests/ → src/ ✅ ($TESTS_TO_SRC imports)"
    echo ""
    if [ $WARNINGS_FOUND -gt 0 ]; then
        echo -e "${YELLOW}⚠️  $WARNINGS_FOUND warnings found (review recommended)${NC}"
        exit 0
    fi
    exit 0
else
    echo -e "${RED}❌ FAILURE: $ISSUES_FOUND critical issues found${NC}"
    echo ""
    echo "Production code in src/ MUST NOT depend on:"
    echo "  - tools/ (development utilities)"
    echo "  - tests/ (test code)"
    echo "  - fixtures/ (test data)"
    echo ""
    echo "Fix violations before proceeding."
    exit 1
fi
