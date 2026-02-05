#!/usr/bin/env bash
# Manual Visual Validation Script for Rich Terminal UI
# 
# This script demonstrates the rich terminal UI output in various modes
# for manual visual validation as per ADR-030.

set -e

echo "===================================================================="
echo "Rich Terminal UI - Manual Visual Validation"
echo "===================================================================="
echo ""
echo "This script will run CLI commands to demonstrate rich terminal UI."
echo ""

# Setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG_DIR="$ROOT_DIR/config"

echo ""
echo "===================================================================="
echo "Test 1: Normal TTY Mode (with rich formatting)"
echo "===================================================================="
echo ""

python -m llm_service.cli --config-dir "$CONFIG_DIR" config validate || true

echo ""
echo "===================================================================="
echo "Test 2: Version Command"
echo "===================================================================="
echo ""

python -m llm_service.cli version

echo ""
echo "===================================================================="
echo "Test 3: Non-TTY Mode (piped output - should be plain text)"
echo "===================================================================="
echo ""

python -m llm_service.cli --config-dir "$CONFIG_DIR" config validate | cat || true

echo ""
echo "===================================================================="
echo "Test 4: --no-color Flag (should disable colors)"
echo "===================================================================="
echo ""

python -m llm_service.cli --config-dir "$CONFIG_DIR" --no-color config validate || true

echo ""
echo "===================================================================="
echo "Visual Validation Complete!"
echo "===================================================================="
echo ""
echo "Please verify:"
echo "  ✓ Test 1: Rich formatting with panels, tables, and colors"
echo "  ✓ Test 2: Version info in formatted panel"
echo "  ✓ Test 3: Plain text output without formatting"
echo "  ✓ Test 4: No colors but structure maintained"
echo ""
