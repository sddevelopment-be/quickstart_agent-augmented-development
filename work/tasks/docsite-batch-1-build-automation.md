# Task: Documentation Site Deployment Automation

**Task ID**: `2026-01-31T1030-docsite-deploy-automation`  
**Assignee**: Build Automation Agent (Build Buddy)  
**Priority**: HIGH  
**Estimated Effort**: 4-6 hours  
**Depends On**: Architect Alphonso (docs-site foundation - ✅ COMPLETE)  
**Related**: `work/planning/docsite-batch-1-implementation-plan.md`

---

## Objective

Create and deploy GitHub Actions workflow to automatically build and deploy the Hugo documentation site to GitHub Pages.

---

## Context

The documentation site foundation has been established by Architect Alphonso:
- ✅ Hugo site initialized in `docs-site/`
- ✅ Hugo Book theme configured as git submodule
- ✅ Initial content created (homepage, section placeholders)
- ✅ Build tested locally (85ms build time, 18 pages, 94 files)
- ✅ Configuration validated (`docs-site/hugo.toml`)

**Your task**: Automate the build and deployment process via GitHub Actions.

---

## Deliverables

### 1. GitHub Actions Workflow

**File**: `.github/workflows/deploy-docsite.yml`

**Requirements**:
- **Trigger**: Push to `main` branch with changes in `docs-site/**` path
- **Hugo Version**: 0.146.0 extended (minimum; can use latest)
- **Build Command**: `hugo --minify` (from `docs-site/` directory)
- **Deploy Target**: GitHub Pages (via `gh-pages` branch)
- **Submodules**: Must checkout git submodules (Hugo Book theme)

**Workflow Steps**:
1. Checkout repository (with submodules)
2. Setup Hugo (extended version)
3. Build site (`cd docs-site && hugo --minify`)
4. Deploy to GitHub Pages

---

### 2. Workflow Validation

**Test Steps**:
1. Create test branch with workflow
2. Push test changes to `docs-site/content/`
3. Verify workflow triggers
4. Check build logs
5. Verify deployment to `gh-pages` branch
6. Confirm site accessible at GitHub Pages URL

**Expected Results**:
- Workflow completes successfully
- Deployment time: <3 minutes total
- Site renders correctly

---

### 3. Documentation Updates

- Add build status badge to `docs-site/README.md`
- Update `docs-site/ARCHITECTURE.md` with deployment details
- Add docsite link to main `README.md`

---

## Success Criteria

- ✅ Workflow builds docsite on push to `main`
- ✅ Deployment completes in <3 minutes
- ✅ Site accessible at GitHub Pages URL
- ✅ Build failures reported clearly
- ✅ Status badge displays correctly
- ✅ Documentation updated

---

## Reference

- **Hugo + GitHub Pages**: https://gohugo.io/hosting-and-deployment/hosting-on-github/
- **Hugo Action**: https://github.com/peaceiris/actions-hugo
- **Deploy Action**: https://github.com/peaceiris/actions-gh-pages
- **Current config**: `docs-site/hugo.toml`

---

**Created**: 2026-01-31  
**Status**: 🟡 Ready to Start
