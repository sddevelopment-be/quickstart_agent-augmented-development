# Tactic: Agent Profile Creation

**Invoked by:**
- [Directive 005 (Agent Profiles)](../directives/005_agent_profiles.md)
- Shorthand: [`/new-agent`](../shorthands/new-agent.md)

---

## Intent

Systematically create new specialized agent profile with capabilities, collaboration patterns, and tooling requirements.

**Apply when:**
- Identifying gap in agent specialization coverage
- Need consistent expertise for recurring task type
- Formalizing ad-hoc agent roles

---

## Execution Steps

### 1. Define Agent Identity
- [ ] Name and persona (e.g., "Security Auditor Sally")
- [ ] Core specialization (1-2 sentences)
- [ ] Primary responsibilities

### 2. Specify Capabilities
- [ ] List operational verbs (analyze, create, validate, etc.)
- [ ] Define expertise boundaries
- [ ] Identify required skills

### 3. Document Collaboration Patterns
- [ ] Typical handoffs FROM this agent
- [ ] Typical handoffs TO this agent
- [ ] Collaboration contract with other agents

### 4. Tooling Requirements
- [ ] Required CLI tools
- [ ] Optional enhancement tools
- [ ] Fallback strategies

### 5. Create Profile File
- [ ] Use template: `doctrine/templates/agent-profile-template.md`
- [ ] Save to: `doctrine/agents/{name}.agent.md`
- [ ] Add to agents index

### 6. Integration
- [ ] Update agent catalog in Directive 005
- [ ] Add to bootstrap options if appropriate
- [ ] Document in repository README if public-facing

---

## Outputs
- Agent profile file
- Capability documentation
- Collaboration contract
- Tooling requirements

---

**Status:** ✅ Active
