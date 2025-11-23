# Validation Recommendations for the Agentic Framework

## Purpose
Outline a pragmatic validation approach to prove that the guardrails, directives, and operational flows actually improve safety, efficiency, and output quality for agent-assisted work in this repository.

## Validation Principles
- **Evidence over intention:** prefer measurable signals (latency, tokens, defect rates) to subjective impressions.
- **Comparative baselines:** test both the current governance pack and the proposed small-footprint path to highlight deltas.
- **Task stratification:** validate across low-, medium-, and high-stakes tasks to ensure guidance scales.
- **Fast feedback:** prioritize checks that can run per-PR and in short manual dry-runs.

## KPIs and How to Measure Them
- **Token efficiency:** average and p95 prompt+completion tokens for key flows (bootstrap, analysis, edit, summary). Collect via model telemetry or proxy logs.
- **Turn count:** median turns to complete scoped tasks (bugfix, doc edit, refactor). Measure in scripted harness runs.
- **Execution overhead:** number of mandatory steps (files opened, commands run) per task; aim to reduce redundant reads.
- **Defect rate:** ratio of PRs needing rework after review; proxied via CI failures or reviewer re-request counts.
- **Guideline adherence:** percentage of runs that follow required directives (e.g., safety notes, summary format). Spot-check via log parsing or automated lint rules.
- **Context relevance:** fraction of injected context that is actually referenced in outputs (citation/use rate). Sample transcripts and compute reference hits.
- **User effort:** time a human spends staging context for the agent (manual copy/paste vs. scripted assembly). Capture during dry-run sessions.

## Validation Activities
- **A/B harness runs:** replay a fixed task suite through (a) full governance pack and (b) small-footprint bootstrap. Compare KPIs above.
- **Red-team drills:** craft adversarial prompts to test guardrail enforcement (e.g., skip safety steps, request off-scope actions) and record responses.
- **Transcript linting:** add CI checks that detect missing summaries, integrity symbols, or absent citations in produced work logs.
- **Token budget audits:** periodically run `load_directives.sh` + new runtime sheet to measure injected tokens; block merges when above thresholds.
- **Shadow reviews:** have a second agent (or human) review outputs for alignment against directives; log discrepancies and remediation steps.

## Acceptance Criteria for “Effective”
- **Efficiency:** ≥15% reduction in tokens and at least 1 fewer interaction turn on low-risk tasks compared to the current baseline.
- **Compliance:** ≥95% adherence to required directives in sampled runs; zero critical guardrail escapes in red-team drills.
- **Quality:** No increase in defect/rework rate; ideally a measurable drop for routine fixes.
- **Operability:** Setup time for agents (human or automated) under 1 minute using the scripted context assembly.

## Reporting
- Maintain a lightweight dashboard (or markdown log) summarizing KPI trends per release cycle.
- Include a “guardrail effectiveness” note in PR templates for agent-generated work until KPIs stabilize.
