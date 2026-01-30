---
status: assigned
agent: devops-danny
priority: high
estimated_duration: 3-4 hours
created_at: 2026-01-30T11:15:00Z
assigned_by: github-copilot
context_files:
  - ops/skills-exporter.js
  - ops/opencode-exporter.js
  - package.json
  - work/reports/assessments/export-module-implementation-review.md
---

# Task: Create Export Workflow with Artifact Packaging

## Objective

Create a GitHub Actions workflow that runs the export scripts (without deploying) and packages the output as a downloadable zip file.

## Context

The repository has two export scripts that generate agent profiles and skills in multiple formats:
1. `node ops/skills-exporter.js` - Exports prompt templates and approaches
2. `node ops/opencode-exporter.js` - Exports agent profiles to OpenCode format

Both scripts write to `dist/` directory and should be run on every commit to ensure exports stay in sync with source files.

## Requirements

### Workflow Trigger
- Run on: 
  - Push to `main` branch
  - Pull requests to `main`
  - Manual workflow dispatch (for testing)

### Workflow Steps
1. **Setup:**
   - Checkout repository
   - Setup Node.js (v18 or v20)
   - Install dependencies: `npm install`

2. **Export Execution:**
   - Run: `npm run export:all` (runs both exporters)
   - Capture: Exit codes, stdout, stderr
   - Validate: Both exports succeed (exit code 0)

3. **Artifact Packaging:**
   - Create: `agent-exports.zip` containing entire `dist/` directory
   - Include: All generated files (skills, agents, manifests)
   - Upload: As GitHub Actions artifact

4. **Validation:**
   - Check: All expected directories exist
   - Verify: Manifest files are valid JSON
   - Count: Files generated (should be ~81 files based on review)

### Acceptance Criteria

✅ **Must Have:**
- Workflow file at `.github/workflows/export-agents.yml`
- Completes in <5 minutes (current export takes <2 seconds)
- Produces downloadable `agent-exports.zip` artifact
- Fails workflow if any export fails
- Clear error messages on failure

✅ **Nice to Have:**
- Artifact retention: 30 days
- Export summary in workflow output (files count, size)
- Diff comparison showing what changed

❌ **Not Required:**
- No deployment to any external system
- No publishing to npm/GitHub packages
- No automatic releases

## Technical Details

### Package.json Scripts
```json
{
  "export:agents": "node ops/opencode-exporter.js",
  "export:skills": "node ops/skills-exporter.js",
  "export:all": "npm run export:agents && npm run export:skills"
}
```

### Expected Output Structure
```
dist/
├── opencode/
│   ├── agents/          (30 files: .opencode.json + .definition.yaml)
│   ├── manifest.opencode.json
│   └── tools.opencode.json
└── skills/
    ├── claude-code/     (19 files)
    ├── copilot/         (19 files)
    ├── opencode/        (19 files)
    ├── approach-skills-manifest.json
    └── prompt-skills-manifest.json
```

### Success Indicators
- Exit code: 0 for both exporters
- Console output contains:
  - "✨ Skills Export Complete!"
  - "✨ OpenCode export complete!"
- File count: ~81 files total

### Error Scenarios to Handle
1. Parse error in source files → Show which file failed
2. Missing dependencies → Clear npm install instructions
3. Write permission error → Check dist/ directory
4. Validation failure → Show validation errors

## Constraints

- **No External Dependencies:** Use only GitHub Actions and standard Node.js
- **No Secrets Required:** All operations are read/write to repo
- **No Deployment:** Just package, don't deploy anywhere
- **Fast Execution:** Complete in <5 minutes

## Deliverables

1. **Workflow File:** `.github/workflows/export-agents.yml`
2. **Documentation:** Update README or add comment in workflow file
3. **Test Run:** Successfully execute workflow and verify artifact

## Testing Checklist

- [ ] Workflow runs successfully on push to main
- [ ] Workflow runs successfully on PR
- [ ] Workflow can be triggered manually
- [ ] Artifact is created and downloadable
- [ ] Artifact contains all expected files
- [ ] Workflow fails if export script fails
- [ ] Error messages are clear and actionable

## References

- **Export Review:** `work/reports/assessments/export-module-implementation-review.md`
- **Skills Exporter:** `ops/skills-exporter.js`
- **OpenCode Exporter:** `ops/opencode-exporter.js`
- **Package.json:** `package.json` (see scripts section)
- **GitHub Actions Docs:** https://docs.github.com/en/actions

## Notes

This task is part of the export module review (branch: `copilot/review-export-module-implementation`). The workflow will help ensure exports stay in sync with source files and make it easy to download agent definitions for distribution.

---

**Priority:** High  
**Estimated Effort:** 3-4 hours  
**Assigned To:** DevOps Danny  
**Due Date:** Within current sprint  
**Status:** Assigned
