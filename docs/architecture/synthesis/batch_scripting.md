# Batch Scripting Primer – Agentic Fit Analysis
*Prepared by Architect Alphonso — 2025-11-24*

## Source Snapshot
- Reference: `tmp/reference_docs/batch-scripting.md`
- Thesis: Windows batch (.bat/.cmd) remains the lowest-common-denominator automation surface—ideal for zero-dependency orchestration but limited in structure.

## Key Forces & Trade-offs
- **Reach vs. Maintainability:** batch scripts run everywhere Windows does, yet quickly become opaque. They are best as launchers for richer tooling, not as logic containers.
- **Speed vs. Safety:** rapid automation often ignores quoting/escaping, introducing injection risks and brittle error handling.
- **Legacy constraints:** regulated or air-gapped environments may mandate batch due to policy; modernization may require staged migration paths.

## Fit to the Agentic Framework
- **Operational alignment:** supports the guideline to “prefer small, incremental changes” by providing a thin shim around deterministic tasks; agents should keep business logic elsewhere (Python, PowerShell, compiled tools).
- **Command discipline:** when invoking via `/execute` style actions, log `%errorlevel%` handling and note environmental assumptions inside `work/scripts/` readme blocks.
- **Strategic viewpoint:** treat batch automation as part of the infrastructure baseline. ADRs describing cross-platform workflows should include a compatibility matrix that highlights when batch is acceptable and when to demand PowerShell or Bash.

## Application Patterns
1. **Bootstrap launchers:** create batch files that only set environment variables and dispatch to portable tooling (`python`, `powershell`, `node`) to ensure minimal drift.
2. **Validation harnesses:** pair batch scripts with GitHub Actions / CI equivalents so local Windows flows match pipeline expectations.
3. **Migration guide entries:** document how to transform existing `.bat` logic into PowerShell modules, capturing parity tests; store future ADR seeds here for progressive replacement.

## Risks & Open Questions
- Need a directive clarifying when batch is acceptable inside repositories vs. when to enforce PowerShell for maintainability.
- Windows quoting rules remain an error source; consider supplying snippet templates or lint checks before promoting scripts to shared tooling.
- Investigate whether agentic automation (e.g., orchestrator) should emit batch variants automatically when generating ops scripts for Windows contributors.
