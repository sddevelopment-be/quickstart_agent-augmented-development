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

Return Path: See AGENTS.md core for integration guidance.