# Quarterly Tool Review Checklist

**Version:** 1.0.0  
**Last Updated:** {{YYYY-MM-DD}}  
**Reviewer:** {{name}}  
**Quarter:** {{Q1/Q2/Q3/Q4}} {{YYYY}}

---

## Purpose

This checklist ensures systematic review of tooling infrastructure to maintain security, performance, and alignment with project needs. Conduct this review at the end of each quarter or when significant framework updates are released.

---

## 1. Version Update Checks

### Core CLI Tools

- [ ] **ripgrep (rg)** - Current version: _____ | Latest: _____ | Action needed: _____
- [ ] **fd** - Current version: _____ | Latest: _____ | Action needed: _____
- [ ] **ast-grep** - Current version: _____ | Latest: _____ | Action needed: _____
- [ ] **jq** - Current version: _____ | Latest: _____ | Action needed: _____
- [ ] **yq** (mikefarah/yq) - Current version: _____ | Latest: _____ | Action needed: _____
- [ ] **fzf** - Current version: _____ | Latest: _____ | Action needed: _____

### Framework Components

- [ ] **Agent profiles** - Current: _____ | Target: _____ | Drift detected: Y/N
- [ ] **Directives** - Current: _____ | Target: _____ | Missing files: _____
- [ ] **Templates** - Current: _____ | Target: _____ | Local customizations: _____
- [ ] **Validation scripts** - Current: _____ | Target: _____ | Updates needed: _____

### Dependencies

- [ ] **Python requirements** - Check `requirements.txt` for outdated packages
- [ ] **GitHub Actions** - Review workflow versions and deprecated actions
- [ ] **Pre-commit hooks** - Verify hook versions and configurations

---

## 2. Security Audit

### Tool Sources & Integrity

- [ ] All tools installed from official/trusted sources
- [ ] Download URLs use HTTPS exclusively
- [ ] Tool versions are pinned in setup scripts
- [ ] No credentials or secrets in configuration files
- [ ] Installation paths follow security best practices

### Vulnerability Scanning

- [ ] Run `pip list --outdated` and check for known CVEs
- [ ] Review GitHub Dependabot alerts (if enabled)
- [ ] Check tool changelogs for security-related updates
- [ ] Verify no deprecated or EOL tools in use

### Access Control

- [ ] Setup scripts use minimal required privileges
- [ ] No hardcoded tokens or API keys in repository
- [ ] Secrets management follows documented procedures
- [ ] Agent access boundaries remain appropriate

---

## 3. Performance Validation

### Tool Performance

- [ ] **Setup script duration** - Target: <2 min | Actual: _____ | Status: Pass/Fail
- [ ] **ripgrep search speed** - Baseline test: _____ | Current: _____ | Trend: _____
- [ ] **fd file discovery** - Baseline test: _____ | Current: _____ | Trend: _____
- [ ] **ast-grep pattern matching** - Baseline test: _____ | Current: _____ | Trend: _____

### Agent Execution

- [ ] Average task completion time compared to previous quarter
- [ ] Number of tool installation failures/retries
- [ ] Context window usage efficiency (token metrics if available)
- [ ] Orchestration system responsiveness

### CI/CD Pipeline

- [ ] Workflow execution times within acceptable range
- [ ] No frequent timeout or resource exhaustion issues
- [ ] Caching strategies effective and up-to-date

---

## 4. Documentation Updates

### User-Facing Documentation

- [ ] `docs/HOW_TO_USE/copilot-tooling-setup.md` - Accurate and current
- [ ] `docs/HOW_TO_USE/multi-agent-orchestration.md` - Reflects current practices
- [ ] `docs/HOW_TO_USE/creating-agents.md` - Examples working as documented
- [ ] `README.md` - Quick start instructions valid

### Agent Documentation

- [ ] `.github/agents/AGENTS.md` - Version numbers current
- [ ] `.github/agents/directives/` - All directives reviewed for accuracy
- [ ] Agent profiles - Specializations clearly defined
- [ ] `GLOSSARY.md` - Terms aligned with current usage

### Templates

- [ ] All templates in `docs/templates/` tested and functional
- [ ] Template examples updated with recent artifacts
- [ ] Template README files accurate and helpful

---

## 5. Roadmap Planning

### Upcoming Priorities

- [ ] Review framework roadmap from upstream (if applicable)
- [ ] Identify gaps between current state and vision
- [ ] Prioritize technical debt items for next quarter
- [ ] Plan major version upgrades or migrations

### Deprecation Planning

- [ ] Identify tools/features planned for deprecation
- [ ] Document migration paths for deprecated items
- [ ] Set target dates for removal
- [ ] Communicate deprecations to stakeholders

### Feature Requests

- [ ] Review filed issues for feature requests
- [ ] Assess feasibility and value of proposed enhancements
- [ ] Update issue labels and milestones
- [ ] Add high-value items to roadmap

---

## 6. Quality Metrics

### Artifact Consistency

- [ ] ADRs follow template structure
- [ ] Work logs contain required sections
- [ ] Agent coordination files properly formatted
- [ ] Cross-references between documents valid

### Traceability

- [ ] Decision traceability chain intact (ADRs → Requirements → Implementation)
- [ ] Agent task completion tracked in work logs
- [ ] Change history documented in CHANGELOG
- [ ] Links between related artifacts functional

---

## 7. Derivative Repository Assessment

### Portability

- [ ] Framework elements clearly separated from project-specific content
- [ ] Local customizations documented and justified
- [ ] No vendor lock-in for critical functionality
- [ ] Setup scripts work across supported platforms

### Adoption Feedback

- [ ] Gather feedback from derivative projects (if any)
- [ ] Document common customization patterns
- [ ] Identify barriers to adoption
- [ ] Update quickstart guides based on learnings

---

## 8. Action Items

Document all identified issues and action items:

| Priority | Item | Owner | Target Date | Status |
|----------|------|-------|-------------|--------|
| High     |      |       |             |        |
| Medium   |      |       |             |        |
| Low      |      |       |             |        |

---

## 9. Review Completion

- [ ] All sections completed
- [ ] Action items assigned and tracked
- [ ] Review results shared with team
- [ ] Next review scheduled for: _____
- [ ] Archive this completed checklist to: `work/reports/maintenance/YYYY-QX-tool-review.md`

**Review completed by:** _____  
**Date:** _____  
**Sign-off:** _____

---

## Related Documentation

- **Tooling Setup:** `docs/HOW_TO_USE/copilot-tooling-setup.md`
- **Directive 001:** `.github/agents/directives/001_cli_shell_tooling.md`
- **Framework Audit:** Use `docs/templates/automation/framework-audit-report-template.md` for detailed audits
- **Work Directory:** `work/README.md` for orchestration system health

---

**Template maintained by:** Build Automation & Curator agents  
**Next review:** End of {{next quarter}}
