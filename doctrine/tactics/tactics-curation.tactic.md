# Tactic: Tactics Curation and Maintenance

**Invoked by:**
- (Meta-tactic — used by curators maintaining the tactics layer)

**Related tactics:**
- (Standalone — focuses on tactic lifecycle management)

**Complements:**
- [Directive 009 (Role Capabilities)](../directives/009_role_capabilities.md) — curator responsibilities
- [Tactics Catalog](./README.md) — tactics catalog

---

## Intent

Maintain structural, tonal, and metadata integrity across the tactics layer by following systematic procedures for adding, updating, and retiring tactics. Ensures consistency, discoverability, and alignment with directives and approaches.

Apply when:
- Adding a new tactic to the doctrine stack
- Updating an existing tactic's scope or invocation context
- Identifying tactics that need refinement or retirement
- Performing periodic curation reviews of tactics catalog

## Preconditions

**Required inputs:**
- Understanding of doctrine stack structure (Directives → Tactics → Templates)
- Access to `.github/agents/tactics/` directory
- Curator role or explicit permission to modify tactics

**Assumed context:**
- Tactic template exists at `docs/templates/tactic.md`
- Tactics README exists at `./README.md` (tactics catalog)
- Version control is in place (git)

**Exclusions (when NOT to use):**
- Quick edits to fix typos (use direct editing)
- Emergency hotfixes (follow expedited review process)
- Content changes that don't affect structure or metadata

## Execution Steps

### When Adding New Tactics

1. **Create tactic file**:
   - Use template from `docs/templates/tactic.md`
   - Place in `.github/agents/tactics/` directory
   - Name: `kebab-case-description.tactic.md`
   - Include metadata header with:
     - **Invoked by:** List directives that mandate this tactic
     - **Related tactics:** List complementary tactics with relative links
     - **Complements:** List approaches and directives this supports

2. **Add entry to tactics catalog**:
   - Open `./README.md` (tactics catalog)
   - Add entry to appropriate category table in "Available Tactics" section
   - Include: Name, File, Intent, Invoke When, Invoked By, Notes
   - Maintain alphabetical or logical order within category

3. **Update relevant directives** (if applicable):
   - Identify directives that should mandate this tactic
   - Add explicit invocation statement in workflow section
   - Use format: `Invoke tactics/<tactic-name>.tactic.md`
   - Document in directive's "Related Resources" section

4. **Update tactics count**:
   - Increment count in README.md "Version" section
   - Update "Last Updated" date

5. **Commit with standard message**:
   - Format: `claire: add <tactic-name> - <one-line intent>`
   - Example: `claire: add input-validation-fail-fast - comprehensive validation with clear feedback`

### When Updating Existing Tactics

1. **Edit tactic file**:
   - Modify content while preserving structure
   - Update metadata header if invocation contexts change
   - Ensure related tactics links remain accurate

2. **Update README if needed**:
   - Modify entry in "Available Tactics" table if intent/invocation changes
   - Update "Tactic Selection Guidance" section if context changes
   - Update "Cross-References" section if relationships change

3. **Update directives if needed**:
   - Modify invocation statements if workflow integration changes
   - Update directive metadata if tactic relationships change

4. **Update version metadata**:
   - Increment README version if structural changes occur
   - Update "Last Updated" date

5. **Commit with standard message**:
   - Format: `claire: update <tactic-name> - <change-summary>`
   - Example: `claire: update stopping-conditions - add resource exhaustion exit criteria`

### Periodic Curation Review

1. **Check metadata consistency**:
   - Verify all tactics have complete metadata headers
   - Ensure "Invoked by" references exist in directives
   - Validate "Related tactics" links are not broken

2. **Check catalog accuracy**:
   - Verify README.md table entries match tactic files
   - Ensure tactics count is accurate
   - Validate categories are logical and balanced

3. **Check directive alignment**:
   - Confirm directives reference tactics correctly
   - Ensure tactics support directive workflows appropriately
   - Identify missing invocation opportunities

4. **Check template compliance**:
   - Verify tactics follow template structure
   - Ensure required sections are present
   - Validate tone and style consistency

5. **Document findings**:
   - Create work log entry with discrepancies found
   - Prioritize fixes by impact (broken links > style issues)
   - Plan remediation batch

## Checks / Exit Criteria

**For adding new tactics:**
- [ ] Tactic file exists in tactics directory
- [ ] Tactic follows template structure from `docs/templates/tactic.md`
- [ ] Metadata header is complete (Invoked by, Related tactics, Complements)
- [ ] Entry added to README.md "Available Tactics" table
- [ ] Tactics count incremented in README.md
- [ ] Related directives updated (if applicable)
- [ ] All relative links resolve correctly
- [ ] Commit message follows standard format

**For updating tactics:**
- [ ] Tactic content updated with changes
- [ ] Metadata header reflects current relationships
- [ ] README.md updated if invocation context changed
- [ ] Directives updated if workflow integration changed
- [ ] Version metadata updated appropriately
- [ ] Commit message follows standard format

**For curation review:**
- [ ] All tactics have complete metadata
- [ ] README.md catalog is accurate
- [ ] Directive invocations are consistent
- [ ] Template compliance verified
- [ ] Findings documented in work log

## Failure Modes

**Common misuse:**
- Adding tactics without updating README.md catalog (creates orphaned tactics)
- Forgetting to update directives when adding directive-invoked tactics
- Using inconsistent naming conventions (breaks discoverability)
- Breaking relative links when moving files
- Skipping metadata headers (loses relationships)

**Typical shortcuts that undermine intent:**
- Direct commits without following standard message format
- Updating one layer (tactic) without updating others (README, directive)
- Adding tactics that duplicate existing ones (check catalog first)
- Creating tactics for one-time use (tactics should be reusable procedures)

**Silent failures:**
- Broken relative links (tactics still function but relationships lost)
- Outdated "Invoked by" metadata (creates confusion about authority)
- Stale tactics count (minor but indicates lack of maintenance)
- Missing tactic entries in README (tactic exists but not discoverable)

## Outputs

**For adding new tactics:**
- New tactic file in tactics directory
- Updated `./README.md` with new entry
- Updated directives with invocation statements (if applicable)
- Git commit with standard format

**For updating tactics:**
- Modified tactic file with updated content
- Updated `./README.md` (if needed)
- Updated directives (if needed)
- Git commit with standard format

**For curation review:**
- Work log entry documenting findings
- Remediation plan for identified issues
- (Optional) Batch commits fixing discrepancies

## Notes

**Commit message conventions:**
- Always prefix with `claire:` to indicate curator role
- Use present tense, imperative mood
- Keep one-line summary under 72 characters
- Multi-line commits: blank line, then details

**Relationship tracking:**
- "Invoked by" = directive mandates this tactic (authority)
- "Related tactics" = complementary procedures (peer relationship)
- "Complements" = philosophical grounding (approaches) or governance (directives)

**Version policy:**
- Increment README version for structural changes (categories, organization)
- Update "Last Updated" date for all changes (individual tactic updates, README modifications)
- Don't increment version for content-only updates to individual tactics
- Tactics themselves don't have individual version numbers
- Tactics count reflects active tactics only (exclude retired ones)

---
