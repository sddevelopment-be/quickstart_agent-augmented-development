#!/bin/bash
# Doctrine Dependency Direction Validator
# Ensures framework artifacts do not reference repository-specific ADRs
# 
# Usage: ./validate-dependencies.sh
# Exit code: 0 = no violations, 1 = violations found

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCTRINE_DIR="${SCRIPT_DIR}/../../doctrine"

echo "🔍 Doctrine Dependency Direction Validator"
echo "=========================================="
echo ""
echo "Checking: ${DOCTRINE_DIR}"
echo ""

# Search for ADR-NNN references in doctrine/
# Exclude:
# - ${DOC_ROOT} templated paths (intentional for portability)
# - spec-kitty ADR references (external project analysis)
# - Example/comment lines
# - Backup files
# - CHANGELOG entries
# - Directive 003 (Repository Quick Reference - legitimate exception)

violations=$(grep -rn "ADR-[0-9]" "${DOCTRINE_DIR}/" \
  | grep -v '${DOC_ROOT}' \
  | grep -v 'spec-kitty ADR' \
  | grep -v 'spec-kitty:.*ADR' \
  | grep -v '# Example:' \
  | grep -v 'CHANGELOG' \
  | grep -v '.backup' \
  | grep -v 'directives/003_repository_quick_reference.md' \
  | grep -v 'docs/references/comparative_studies' \
  || true)

if [[ -n "${violations}" ]]; then
  echo "❌ VIOLATIONS FOUND"
  echo ""
  echo "Framework artifacts in doctrine/ reference repository-specific ADRs:"
  echo ""
  echo "${violations}"
  echo ""
  echo "═══════════════════════════════════════════════════════════════"
  echo "DEPENDENCY DIRECTION RULE VIOLATION"
  echo "═══════════════════════════════════════════════════════════════"
  echo ""
  echo "Correct dependency flow:"
  echo "  ✅ Local (docs/architecture/adrs/) → Framework (doctrine/)"
  echo "  ❌ Framework (doctrine/) → Local (docs/architecture/adrs/)"
  echo ""
  echo "Framework artifacts must remain portable across repositories."
  echo ""
  echo "See: doctrine/docs/dependency-direction-rules.md"
  echo ""
  exit 1
else
  echo "✅ No dependency direction violations found"
  echo ""
  echo "All framework artifacts properly abstracted from local ADRs."
  echo ""
  exit 0
fi
