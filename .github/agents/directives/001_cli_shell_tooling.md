<!-- The following information is to be interpreted literally -->

# 001 CLI and Shell Tooling Directive

**BYPASS CHECK:** FIRST, check whether a [
`work/notes/LOCAL_ENV.md`](/work/notes/LOCAL_ENV.md) file exists in the repository root. If it does, read its contents and follow any specific instructions or constraints outlined there regarding CLI and shell tooling usage. If no such file exists, or it is empty, proceed with the standard directives below.

---

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

**IMPORTANT:**
Terminal interaction can be unreliable in agent-based workflows. When you suspect flaky terminal behavior:

**Confirmation steps:**

1. create a new file in the repository's [`work/notes/tmp`](/work/notes/tmp) directory
2. attempt to interact with that file via the terminal
3. if interaction fails or is inconsistent, proceed with the remediation technique below and attempt to interact with the file again
4. if interaction is successful, continue with your task using the remediation technique
5. when the current micro task is complete, make note of the issue in the [
   `work/notes/LOCAL_ENV.md`](/work/notes/LOCAL_ENV.md) file for future reference. If the file does not exist, create it as per [/docs/templates/automation/TEMPLATE-LOCAL_ENV.md](/docs/templates/automation/TEMPLATE-LOCAL_ENV.md) and document the observed behavior

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