#!/bin/bash
# Verification Script - Shell Linting Integration
# Run this to verify all components are in place

echo "════════════════════════════════════════════════════════════"
echo "  Shell Linting Integration Verification"
echo "════════════════════════════════════════════════════════════"
echo ""

# Check configuration file
echo "1️⃣  Configuration Files:"
if [ -f .shellcheckrc ]; then
    echo "   ✅ .shellcheckrc exists"
    echo "      Size: $(wc -c < .shellcheckrc) bytes"
else
    echo "   ❌ .shellcheckrc NOT FOUND"
fi

if [ -f .github/workflows/shell-lint.yml ]; then
    echo "   ✅ .github/workflows/shell-lint.yml exists"
    echo "      Size: $(wc -c < .github/workflows/shell-lint.yml) bytes"
else
    echo "   ❌ .github/workflows/shell-lint.yml NOT FOUND"
fi

# Check documentation
echo ""
echo "2️⃣  Documentation Files:"
docs=(
    "docs/shell-linting-guide.md"
    "docs/SHELL_LINTING_ISSUES.md"
    "docs/SHELL_LINTING_QUICKSTART.md"
)

for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "   ✅ $doc exists ($(wc -l < "$doc") lines)"
    else
        echo "   ❌ $doc NOT FOUND"
    fi
done

# Check npm scripts
echo ""
echo "3️⃣  npm Scripts:"
if grep -q '"lint:shell"' package.json; then
    echo "   ✅ npm run lint:shell configured"
else
    echo "   ❌ npm run lint:shell NOT FOUND"
fi

if grep -q '"lint:shell:report"' package.json; then
    echo "   ✅ npm run lint:shell:report configured"
else
    echo "   ❌ npm run lint:shell:report NOT FOUND"
fi

if grep -q '"lint".*lint:shell' package.json; then
    echo "   ✅ npm run lint updated with shell linting"
else
    echo "   ⚠️  npm run lint may not include shell linting"
fi

# Summary
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  Quick Start Commands"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Validate all shell scripts:"
echo "  $ npm run lint:shell"
echo ""
echo "Generate JSON report:"
echo "  $ npm run lint:shell:report"
echo ""
echo "Run integrated validation (text + shell):"
echo "  $ npm run lint"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "See documentation:"
echo "  • docs/SHELL_LINTING_QUICKSTART.md - Quick reference"
echo "  • docs/SHELL_LINTING_ISSUES.md - Issues and fixes"
echo "  • docs/shell-linting-guide.md - Comprehensive guide"
echo ""

