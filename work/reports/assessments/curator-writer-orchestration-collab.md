# Curator-Writer Collaboration: Orchestration User Guide

_Created: 2025-11-23_  
_Status: Pending_  
_Task IDs: 2025-11-23T0722-curator-orchestration-guide → writer-editor follow-up_

## Objective

Create a comprehensive, accessible user guide for the multi-agent orchestration system in `docs/HOW_TO_USE/multi-agent-orchestration.md`.

## Target Audience

**End-users** who want to:
- Understand how the orchestration system works
- Create and submit tasks for agents
- Monitor task progress
- Troubleshoot common issues
- Integrate orchestration into their workflow

**Not for:** System administrators, agent developers, or architecture discussions (those have separate docs).

## Workflow

### Phase 1: Curator Claire (Initial Draft)
**Task:** 2025-11-23T0722-curator-orchestration-guide

**Responsibilities:**
- Structure the guide with clear sections
- Distill technical documentation into user-friendly content
- Create practical examples and use cases
- Ensure accuracy and consistency with existing documentation
- Draft comprehensive but accessible content

**Source Materials:**
- `work/README.md` - Technical overview and quick start
- `docs/templates/task-descriptor.yaml` - Task structure and examples
- `docs/architecture/design/async_multiagent_orchestration.md` - Architecture details
- `work/collaboration/orchestration-implementation-plan.md` - Implementation context

**Deliverable:**
- Complete draft in `docs/HOW_TO_USE/multi-agent-orchestration.md`
- Structured, accurate, with examples
- Ready for editorial polish

### Phase 2: Writer-Editor (Polish & Refinement)
**Task:** Auto-generated follow-up from curator task

**Responsibilities:**
- Review for clarity and readability
- Ensure consistent voice and tone
- Verify examples are easy to follow
- Check consistency with other HOW_TO_USE guides
- Add practical tips and best practices
- Final polish for publication

**Verification Points:**
- [ ] Language is accessible to non-technical users
- [ ] Examples are complete and functional
- [ ] Navigation is intuitive
- [ ] Cross-references are accurate
- [ ] Formatting is consistent with repository style

## Suggested Guide Structure

### 1. Introduction
- What is the orchestration system?
- Why use it?
- Who is it for?

### 2. Core Concepts
- Tasks and task lifecycle
- Agents and specializations
- The Agent Orchestrator
- Work directory structure

### 3. Getting Started
- Prerequisites
- Creating your first task
- Understanding task status
- Monitoring progress

### 4. Task Creation Guide
- Task file structure (simplified from template)
- Naming conventions
- Required vs optional fields
- Common task patterns

### 5. Working with Agents
- Available agents and their specializations
- When to use which agent
- Agent handoffs and workflows
- Multi-step task chains

### 6. Monitoring and Tracking
- Agent status dashboard
- Workflow logs
- Handoff logs
- Understanding task states

### 7. Common Use Cases
- Documentation generation
- Architecture analysis
- Code review coordination
- Multi-phase projects

### 8. Troubleshooting
- Task not getting picked up
- Task stuck in progress
- Error states and recovery
- Getting help

### 9. Best Practices
- Task granularity
- Context provision
- Artifact specification
- Dependency management

### 10. Reference
- Quick command reference
- Task template
- Links to technical docs

## Key Messages to Convey

1. **Simplicity**: The system is file-based and transparent
2. **Visibility**: All state changes are in Git
3. **Collaboration**: Agents work together through handoffs
4. **Flexibility**: Manual override always possible
5. **Traceability**: Complete audit trail maintained

## Tone and Style

- **Friendly but professional**: Encourage usage without being overly casual
- **Action-oriented**: Focus on what users can do
- **Example-driven**: Show, don't just tell
- **Practical**: Address real workflow needs
- **Encouraging**: Build confidence in using the system

## Cross-References

Ensure proper linking to:
- Technical architecture docs (for deep dives)
- Agent profiles (for specialization details)
- Task template (for reference)
- ADRs (for decision rationale)
- Other HOW_TO_USE guides (for consistency)

## Success Criteria

The guide is successful if a new user can:
1. Understand what the orchestration system is and why to use it
2. Create a valid task file without errors
3. Submit a task and monitor its progress
4. Understand task lifecycle and states
5. Troubleshoot common issues independently
6. Apply the system to their own use cases

## Notes for Both Agents

- **Accuracy is critical**: Users will rely on this as authoritative
- **Examples must work**: Test any code/task examples provided
- **Accessibility matters**: Avoid jargon where possible, explain when necessary
- **Keep it updated**: Mark version and last-updated date
- **Link generously**: Help users find related information

## Collaboration Tips

### For Curator Claire:
- Focus on correctness and completeness first
- Don't worry about perfect prose in draft
- Include TODO markers for areas needing editor input
- Highlight any technical uncertainties

### For Writer-Editor:
- Preserve technical accuracy while improving readability
- Suggest structural changes if needed
- Add practical tips from user perspective
- Ensure consistent voice throughout

## Timeline

- **Curator phase**: 2-3 hours (draft creation)
- **Writer-Editor phase**: 1-2 hours (polish and refinement)
- **Total**: ~4-5 hours

## Questions or Issues?

If either agent encounters:
- Missing information in source materials
- Conflicting guidance between documents
- Uncertainty about technical details
- Scope questions

**Action:** Document in task YAML error/notes section and escalate to Architect or human stakeholder.

---

_Prepared by: Architect Alphonso_  
_For task coordination questions: See work/collaboration/HANDOFFS.md_
