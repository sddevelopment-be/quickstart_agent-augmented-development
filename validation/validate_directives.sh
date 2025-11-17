#!/usr/bin/env bash
# validation/validate_directives.sh
# Lightweight validation for agent directive manifest & profile compliance.
# Exits non-zero on any failed check.

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR_DIR="$ROOT_DIR/.github/agents/directives"
MANIFEST="$DIR_DIR/manifest.json"
AGENTS_MD="$ROOT_DIR/AGENTS.md"
AGENTS_DIR="$ROOT_DIR/.github/agents"

fail() { echo "[FAIL] $*" >&2; exit 1; }
warn() { echo "[WARN] $*" >&2; }
pass() { echo "[PASS] $*"; }

if [[ ! -f "$MANIFEST" ]]; then
  fail "Manifest file missing: $MANIFEST"
fi

# Basic JSON validation (jq optional)
if command -v jq >/dev/null 2>&1; then
  jq . "$MANIFEST" >/dev/null || fail "Manifest JSON invalid"
  COUNT_MANIFEST=$(jq '.directives | length' "$MANIFEST")
else
  # Fallback: naive count of '"code":' occurrences
  COUNT_MANIFEST=$(grep -c '"code"' "$MANIFEST")
  warn "jq not found; used fallback counting method"
fi

# Count directive markdown files
COUNT_FILES=$(find "$DIR_DIR" -maxdepth 1 -type f -name '*_[a-z]*.md' -printf '%f\n' | wc -l | tr -d ' ')
[[ "$COUNT_MANIFEST" -eq "$COUNT_FILES" ]] || fail "Manifest directive count ($COUNT_MANIFEST) != file count ($COUNT_FILES)"
pass "Directive count matches ($COUNT_FILES)"

# Ensure sequential codes
CODES=$(find "$DIR_DIR" -maxdepth 1 -type f -name '*_[a-z]*.md' -printf '%f\n' | sort)
EXPECTED_SEQ=$(printf '%03d\n' $(seq 1 $COUNT_FILES))
ACTUAL_SEQ=$(echo "$CODES" | sed -E 's/^([0-9]{3}).*/\1/' )
if [[ "$EXPECTED_SEQ" != "$ACTUAL_SEQ" ]]; then
  echo "Expected sequence:" >&2
  echo "$EXPECTED_SEQ" >&2
  echo "Actual sequence:" >&2
  echo "$ACTUAL_SEQ" >&2
  fail "Directive numbering sequence mismatch"
fi
pass "Directive numbering contiguous"

# Verify each directive file heading matches code & dependency resolution
while IFS= read -r file; do
  CODE=${file:0:3}
  FIRST_LINE=$(grep -m1 '^# ' "$DIR_DIR/$file" || true)
  [[ "$FIRST_LINE" == "# $CODE"* ]] || fail "Heading mismatch in $file (got: $FIRST_LINE)"
  pass "Heading ok: $file"
  if command -v jq >/dev/null 2>&1; then
    jq -e --arg c "$CODE" '.directives[] | select(.code==$c)' "$MANIFEST" >/dev/null || fail "Manifest entry missing for code $CODE"
  else
    grep -q "\"code\": \"$CODE\"" "$MANIFEST" || fail "Manifest entry missing (fallback) for code $CODE"
  fi
  pass "Manifest entry exists: $CODE"
  if command -v jq >/dev/null 2>&1; then
    DEPS=$(jq -r --arg c "$CODE" '.directives[] | select(.code==$c) | .dependencies[]?' "$MANIFEST" || true)
    for d in $DEPS; do
      if ! find "$DIR_DIR" -maxdepth 1 -type f -name "${d}_*.md" | grep -q .; then
        fail "Dependency directive file for $d referenced by $CODE not found"
      fi
    done
  fi
done < <(echo "$CODES")

# Validate Extended Directives Index in AGENTS.md
for code in $(printf '%03d ' $(seq 1 $COUNT_FILES)); do
  grep -q "| $code" "$AGENTS_MD" || fail "AGENTS.md missing directive code $code in index"
  pass "AGENTS.md lists code $code"
done

# Collaboration contract clarifying line presence (robust null handling)
REQUIRED_LINE="Ask clarifying questions when uncertainty >30%"
find "$AGENTS_DIR" -maxdepth 1 -type f -name '*agent.md' -print0 | while IFS= read -r -d '' profile_path; do
  profile=$(basename "$profile_path")
  if ! grep -q "$REQUIRED_LINE" "$profile_path"; then
    fail "Missing required clarifying line in $profile"
  fi
  pass "Clarifying line present in $profile"
DoneMarker="1"
  # continue
:; done

pass "All validations succeeded"
exit 0
