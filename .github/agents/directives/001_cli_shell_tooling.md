<!-- The following information is to be interpreted literally -->
# 001 CLI and Shell Tooling Directive

Use this rubric for shell operations:
- Find files: `fd`
- Find text: `rg` (ripgrep)
- AST/code structure (TS/TSX): `ast-grep`
    - `.ts`: `ast-grep --lang ts -p '<pattern>'`
    - `.tsx`: `ast-grep --lang tsx -p '<pattern>'`
    - Other languages: set `--lang` (e.g., `--lang rust`)
- Interactive selection: pipe matches to `fzf`
- JSON: `jq`
- YAML/XML: `yq`

Preference: If `ast-grep` is available, use it for structural queries; otherwise fall back to `rg` for plain‑text scanning.

## Dealing with Unreliable Tooling

Terminal interaction can be unreliable in agent-based workflows. When you suspect flaky terminal behavior:

**Remediation Technique:**
1. Create a shell script in `tmp/remediation/` at the repository root
2. Pipe terminal output to files in the same directory
3. Execute the script and capture results from the output files
4. Clean up created files after completion
5. **Document the remediation** in your report/answer: "Applied remediation technique for flaky terminal interaction"

**Example:**
```bash
mkdir -p tmp/remediation
cat > tmp/remediation/fix_interaction.sh << 'EOF'
#!/bin/bash
command_output > tmp/remediation/output.txt 2>&1
EOF
chmod +x tmp/remediation/fix_interaction.sh
./tmp/remediation/fix_interaction.sh
cat tmp/remediation/output.txt
rm -rf tmp/remediation
```

Return Path: See AGENTS.md core for integration guidance.