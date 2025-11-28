# Style Execution Primers (Agents)

Concise, action-ready guidance for agents working in Markdown, Python, Perl, or PlantUML. Audience: agents executing tasks with these tools; keep outputs diff-friendly and template-aligned.

## Markdown (docs, READMEs, reports)
- Use CommonMark/GFM only; avoid embedded HTML unless required by template.
- Enforce semantic headings; keep one `h1` per file, ordered `h2+`.
- Lists and tables: keep rows short; prefer descriptive column headers; wrap long cells manually.
- Code fences: always set language; prefer `text` when no syntax applies.
- Links: relative paths within repo; include alt text for images; avoid bare URLs.
- Validation: run `markdownlint`/lints if available; reflow to ~80–100 cols where consistent with repo norms.

## Python (scripts, orchestration, tests)
- Env: prefer `pyproject.toml` + `poetry`; otherwise `venv` + `requirements.txt`. Never rely on system Python.
- Tooling: format with `black`, lint with `ruff`/`flake8`; type-hint public functions; use f-strings.
- Structure: keep modules `snake_case`; functions small and pure when possible; push I/O to edges.
- Tests: `pytest -q` by default; add fixtures/parametrize over inheritance; sample command: `poetry run pytest tests`.
- Packaging: respect existing layout (`src/` vs. flat); do not mix installers (pip + poetry) in the same change.

## Perl (legacy automation, text processing)
- Env: use `perlbrew`/`plenv` + `cpanm`; pin deps with `cpanfile` + `Carton` (`carton install`).
- Safety: always `use strict; use warnings; use v5.30;`; run `perl -c file.pl` before commit.
- Style: enable `Perl::Tidy`/`Perl::Critic` defaults; keep sigils correct; avoid clever context tricks in shared code.
- Tests: run `prove -l t/` or `carton exec prove -l t/`; keep TAP output clean.
- Packaging: respect existing build system (`Makefile.PL` vs. `Build.PL`); don’t switch systems in the same PR.

## PlantUML (diagrams-as-code)
- Render path: VS Code PlantUML preview or `plantuml diagram.puml`; ensure Graphviz installed when needed.
- Layout: prefer C4-PlantUML for architecture; use aliases for readability; limit line length; group with packages.
- Accessibility: add captions/alt text where embedded; export SVG when possible.
- Hygiene: start/end tags (`@startuml`/`@enduml`); keep includes local; avoid inline styling unless required.
- Validation: regenerate outputs if repo stores renders; ensure diagrams reference current file names/agents.

## Cross-cutting
- Templates first: reuse repo templates in `docs/templates/**`; do not handcraft new formats.
- Logs (Directive 014): record commands and key decisions in `work/reports/logs/<agent>/...`.
- Prompts (Directive 015): store prompt transcripts only when requested or material to the output.
- Audience fit (Directive 022): keep language concise, non-hyped; add 1–2 sentence intent notes when ambiguity risk is high.
