/**
 * Unit Tests: claude-code-generator.js — simplifyAgent()
 *
 * Following Directive 017 (TDD): RED phase — all tests written before implementation.
 * Following Directive 016 (ATDD): Tests define acceptance criteria from SPEC-DIST-002.
 *
 * Acceptance Criteria (AC-3):
 * - Agent files under 40 lines each
 * - Each agent retains: name, description, tools, purpose, specialization
 * - Each agent omits: directive tables, bootstrap declarations, mode protocols
 * - Tool names mapped to Claude Code PascalCase
 * - Model hint inferred from agent role
 */

const { simplifyAgent } = require('../../../tools/exporters/claude-code-generator');

// -- Fixtures: realistic IR objects matching parser.js output --

function makeArchitectIR() {
  return {
    ir_version: '1.0.0',
    frontmatter: {
      name: 'architect-alphonso',
      description: 'Clarify complex systems with contextual trade-offs.',
      tools: ['read', 'write', 'search', 'edit', 'bash', 'plantuml', 'MultiEdit', 'markdown-linter'],
      version: '1.0.0'
    },
    content: {
      purpose: 'Clarify and decompose complex socio-technical systems, surfacing trade-offs and decision rationale. Provide architecture patterns and interfaces that improve shared understanding and traceability without drifting into low-level implementation.',
      specialization: '- **Primary focus:** System decomposition, design interfaces, explicit decision records (ADRs, pattern docs).\n- **Secondary awareness:** Cultural, political, and process constraints that shape feasible architectures.\n- **Avoid:** Coding-level specifics, tool evangelism, premature optimization, speculative redesign without context.\n- **Success means:** Architectural clarity improves decision traceability, accelerates collaboration, and reduces hidden coupling.',
      collaboration_contract: '- Never override General or Operational guidelines.\n- Stay within defined specialization.\n- Always align behavior with global context and project vision.\n- Ask clarifying questions when uncertainty >30%.\n- Escalate issues before they become a problem. Ask for help when stuck.\n- Respect reasoning mode.\n- Use emojis for critical deviations.\n- Produce markdown ADRs/pattern docs; cross-link existing knowledge base entries.\n- Confirm architectural assumptions before modeling relationships.',
      success_criteria: 'Architectural clarity improves decision traceability, accelerates collaboration, and reduces hidden coupling.',
      output_artifacts: '- ADRs, architecture pattern documents, PlantUML diagrams.',
      mode_defaults: [
        { mode: '/analysis-mode', description: 'Systemic decomposition & trade-offs', use_case: 'Architecture exploration & ADR drafting' },
        { mode: '/creative-mode', description: 'Option generation & pattern shaping', use_case: 'Alternative interface sketches' },
        { mode: '/meta-mode', description: 'Rationale reflection & alignment', use_case: 'Post-decision evaluation' }
      ]
    },
    relationships: {
      directives: [
        { code: 1, code_formatted: '001', title: 'CLI & Shell Tooling', rationale: 'Repo/file discovery', required: false },
        { code: 18, code_formatted: '018', title: 'Documentation Level Framework', rationale: 'ADR levels', required: false },
        { code: 16, code_formatted: '016', title: 'ATDD', rationale: 'Test first', required: true },
        { code: 17, code_formatted: '017', title: 'TDD', rationale: 'Red-Green-Refactor', required: true }
      ],
      context_sources: [
        { type: 'Global Principles', location: 'doctrine/' },
        { type: 'General Guidelines', location: 'guidelines/general_guidelines.md' }
      ]
    },
    governance: {
      directive_requirements: { required: [16, 17], optional: [1, 18] },
      uncertainty_threshold: '>30%',
      escalation_rules: ['Ask clarifying questions when uncertainty >30%'],
      primer_required: true,
      test_first_required: true
    },
    metadata: {
      file_path: 'doctrine/agents/architect.agent.md',
      source_hash: 'abc123def456',
      parsed_at: '2026-02-10T12:00:00Z',
      file_size: 3200,
      parser_version: '1.0.0'
    }
  };
}

function makeBackendDevIR() {
  return {
    ir_version: '1.0.0',
    frontmatter: {
      name: 'backend-benny',
      description: 'Shape resilient service backends and integration surfaces with traceable decisions.',
      tools: ['read', 'write', 'search', 'edit', 'MultiEdit', 'Bash', 'Grep', 'Docker', 'Java', 'Python'],
      version: '1.0.0'
    },
    content: {
      purpose: 'Provide grounded backend architecture and implementation guidance\u2014clean service boundaries, dependable data flows, and explicit trade-offs\u2014while honoring systemic constraints.',
      specialization: '- **Primary focus:** API/service design, persistence strategy, performance budgets, failure-mode mapping.\n- **Secondary awareness:** Observability, security posture, deployment ergonomics for downstream integration.\n- **Avoid:** Front-end product decisions, speculative tech churn, uncontextualized migrations/refactors.\n- **Success means:** Documented, benchmark-aware interfaces ready for safe extension by collaborators.',
      collaboration_contract: '- Never override General or Operational guidelines.\n- Stay within defined specialization.\n- Ask clarifying questions when uncertainty >30%.',
      success_criteria: 'Documented, benchmark-aware interfaces ready for safe extension by collaborators.',
      output_artifacts: null,
      mode_defaults: [
        { mode: '/analysis-mode', description: 'Backend reasoning', use_case: 'ADRs, API contracts' }
      ]
    },
    relationships: {
      directives: [
        { code: 16, code_formatted: '016', title: 'ATDD', rationale: 'Test first', required: true },
        { code: 17, code_formatted: '017', title: 'TDD', rationale: 'Red-Green-Refactor', required: true }
      ],
      context_sources: []
    },
    governance: {
      directive_requirements: { required: [16, 17], optional: [] },
      uncertainty_threshold: '>30%',
      escalation_rules: [],
      primer_required: true,
      test_first_required: true
    },
    metadata: {
      file_path: 'doctrine/agents/backend-dev.agent.md',
      source_hash: 'def789',
      parsed_at: '2026-02-10T12:00:00Z',
      file_size: 2800,
      parser_version: '1.0.0'
    }
  };
}

function makeCuratorIR() {
  return {
    ir_version: '1.0.0',
    frontmatter: {
      name: 'curator-claire',
      description: 'Maintain structural, tonal, and metadata integrity across artifacts.',
      tools: ['read', 'write', 'search', 'edit', 'bash'],
      version: '1.0.0'
    },
    content: {
      purpose: 'Maintain the structural and tonal consistency of all repository artifacts, ensuring metadata integrity and cross-reference accuracy.',
      specialization: '- **Primary focus:** Content auditing, metadata validation, cross-reference integrity.\n- **Avoid:** Code implementation, architectural decisions.',
      collaboration_contract: '- Stay within defined specialization.\n- Ask clarifying questions when uncertainty >30%.',
      success_criteria: null,
      output_artifacts: null,
      mode_defaults: []
    },
    relationships: { directives: [], context_sources: [] },
    governance: {
      directive_requirements: { required: [], optional: [] },
      uncertainty_threshold: '>30%',
      escalation_rules: [],
      primer_required: false,
      test_first_required: false
    },
    metadata: {
      file_path: 'doctrine/agents/curator.agent.md',
      source_hash: 'ghi012',
      parsed_at: '2026-02-10T12:00:00Z',
      file_size: 1500,
      parser_version: '1.0.0'
    }
  };
}

function makeReviewerIR() {
  return {
    ir_version: '1.0.0',
    frontmatter: {
      name: 'code-reviewer-cindy',
      description: 'Ensure code quality through rigorous review processes.',
      tools: ['read', 'search', 'Grep', 'Glob'],
      version: '1.0.0'
    },
    content: {
      purpose: 'Review code changes for quality, consistency, and adherence to project standards.',
      specialization: '- **Primary focus:** Code review, quality assurance, standards compliance.\n- **Avoid:** Implementation, architecture redesign.',
      collaboration_contract: '- Stay within defined specialization.',
      success_criteria: null,
      output_artifacts: null,
      mode_defaults: []
    },
    relationships: { directives: [], context_sources: [] },
    governance: {
      directive_requirements: { required: [], optional: [] },
      uncertainty_threshold: null,
      escalation_rules: [],
      primer_required: false,
      test_first_required: false
    },
    metadata: {
      file_path: 'doctrine/agents/code-reviewer-cindy.agent.md',
      source_hash: 'jkl345',
      parsed_at: '2026-02-10T12:00:00Z',
      file_size: 1200,
      parser_version: '1.0.0'
    }
  };
}

// -- Tests --

describe('simplifyAgent', () => {

  describe('Output structure', () => {
    it('should produce valid YAML frontmatter with name, description, tools, model', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).toMatch(/^---\n/);
      expect(result).toMatch(/\n---\n/);
      expect(result).toMatch(/name:\s+architect-alphonso/);
      expect(result).toMatch(/description:\s+.+/);
      expect(result).toMatch(/tools:\s+\[/);
      expect(result).toMatch(/model:\s+\w+/);
    });

    it('should be under 40 lines', () => {
      const result = simplifyAgent(makeArchitectIR());
      const lines = result.split('\n');

      expect(lines.length).toBeLessThanOrEqual(40);
    });

    it('should be under 40 lines for backend-dev agent', () => {
      const result = simplifyAgent(makeBackendDevIR());
      const lines = result.split('\n');

      expect(lines.length).toBeLessThanOrEqual(40);
    });

    it('should be under 40 lines for curator agent', () => {
      const result = simplifyAgent(makeCuratorIR());
      const lines = result.split('\n');

      expect(lines.length).toBeLessThanOrEqual(40);
    });
  });

  describe('Content preservation', () => {
    it('should retain purpose text', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).toContain('Clarify and decompose');
    });

    it('should retain primary focus from specialization', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).toContain('System decomposition');
    });

    it('should retain avoid items from specialization', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).toMatch(/[Aa]void/);
      expect(result).toContain('Coding-level specifics');
    });

    it('should retain name and description in frontmatter', () => {
      const result = simplifyAgent(makeBackendDevIR());

      expect(result).toMatch(/name:\s+backend-benny/);
      expect(result).toMatch(/description:.*resilient service backends/);
    });
  });

  describe('Content stripping', () => {
    it('should NOT contain directive reference tables', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).not.toMatch(/\|\s*Code\s*\|/);
      expect(result).not.toMatch(/\|\s*016\s*\|/);
      expect(result).not.toContain('Directive References');
    });

    it('should NOT contain mode defaults tables', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).not.toMatch(/\|\s*Mode\s*\|.*Description/);
      expect(result).not.toContain('/analysis-mode');
      expect(result).not.toContain('Mode Defaults');
    });

    it('should NOT contain initialization declaration', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).not.toContain('initialized');
      expect(result).not.toContain('Context layers');
    });

    it('should NOT contain context sources listing', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).not.toContain('Context Sources');
      expect(result).not.toContain('Global Principles');
    });

    it('should NOT contain collaboration contract boilerplate', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).not.toContain('Never override General or Operational');
      expect(result).not.toContain('Respect reasoning mode');
    });

    it('should NOT contain governance details', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).not.toContain('Primer Requirement');
      expect(result).not.toContain('Test-First Requirement');
      expect(result).not.toContain('Bug-Fix Requirement');
    });
  });

  describe('Tool name mapping', () => {
    it('should map lowercase doctrine tools to PascalCase Claude Code tools', () => {
      const result = simplifyAgent(makeArchitectIR());

      // "read" -> "Read", "write" -> "Write", "search" -> "Grep", "edit" -> "Edit", "bash" -> "Bash"
      expect(result).toMatch(/tools:\s*\[.*Read/);
      expect(result).toMatch(/tools:\s*\[.*Write/);
      expect(result).toMatch(/tools:\s*\[.*Edit/);
      expect(result).toMatch(/tools:\s*\[.*Bash/);
      expect(result).toMatch(/tools:\s*\[.*Grep/);
    });

    it('should map non-native tools (plantuml, markdown-linter) to Bash', () => {
      const result = simplifyAgent(makeArchitectIR());

      // plantuml and markdown-linter should both map to Bash (CLI invocation)
      // They should not appear as separate tool names
      expect(result).not.toMatch(/tools:\s*\[.*plantuml/i);
      expect(result).not.toMatch(/tools:\s*\[.*markdown-linter/i);
    });

    it('should map Docker, Java, Python to Bash', () => {
      const result = simplifyAgent(makeBackendDevIR());

      expect(result).not.toMatch(/tools:\s*\[.*Docker/);
      expect(result).not.toMatch(/tools:\s*\[.*Java[,\]]/);
      expect(result).not.toMatch(/tools:\s*\[.*Python/);
      expect(result).toMatch(/tools:\s*\[.*Bash/);
    });

    it('should deduplicate mapped tools', () => {
      // architect has: read, write, search, edit, bash, plantuml, MultiEdit, markdown-linter
      // mapped: Read, Write, Grep, Edit, Bash, Bash, MultiEdit, Bash
      // deduped: Read, Write, Grep, Edit, Bash, MultiEdit
      const result = simplifyAgent(makeArchitectIR());
      const toolsMatch = result.match(/tools:\s*\[([^\]]+)\]/);

      expect(toolsMatch).toBeTruthy();
      const tools = toolsMatch[1].split(',').map(t => t.trim());
      const uniqueTools = [...new Set(tools)];
      expect(tools.length).toBe(uniqueTools.length);
    });

    it('should preserve already-PascalCase tools (Grep, Glob, MultiEdit)', () => {
      const result = simplifyAgent(makeReviewerIR());

      expect(result).toMatch(/tools:\s*\[.*Grep/);
      expect(result).toMatch(/tools:\s*\[.*Glob/);
    });
  });

  describe('Model inference', () => {
    it('should infer opus for architect agents', () => {
      const result = simplifyAgent(makeArchitectIR());

      expect(result).toMatch(/model:\s+opus/);
    });

    it('should infer opus for reviewer agents', () => {
      const result = simplifyAgent(makeReviewerIR());

      expect(result).toMatch(/model:\s+opus/);
    });

    it('should infer sonnet for backend-dev agents', () => {
      const result = simplifyAgent(makeBackendDevIR());

      expect(result).toMatch(/model:\s+sonnet/);
    });

    it('should infer sonnet for curator agents', () => {
      const result = simplifyAgent(makeCuratorIR());

      expect(result).toMatch(/model:\s+sonnet/);
    });
  });

  describe('Edge cases', () => {
    it('should handle IR with null content sections', () => {
      const ir = makeCuratorIR();
      ir.content.success_criteria = null;
      ir.content.output_artifacts = null;

      const result = simplifyAgent(ir);

      expect(result).toBeTruthy();
      expect(result.split('\n').length).toBeLessThanOrEqual(40);
    });

    it('should handle IR with empty tools array', () => {
      const ir = makeCuratorIR();
      ir.frontmatter.tools = [];

      const result = simplifyAgent(ir);

      expect(result).toMatch(/tools:\s*\[\]/);
    });

    it('should handle specialization without standard bullet format', () => {
      const ir = makeCuratorIR();
      ir.content.specialization = 'Content auditing and metadata validation.';

      const result = simplifyAgent(ir);

      expect(result).toBeTruthy();
      expect(result.split('\n').length).toBeLessThanOrEqual(40);
    });

    it('should handle null purpose gracefully', () => {
      const ir = makeCuratorIR();
      ir.content.purpose = null;

      const result = simplifyAgent(ir);

      expect(result).toBeTruthy();
      expect(result).toMatch(/name:\s+curator-claire/);
    });

    it('should handle null specialization gracefully', () => {
      const ir = makeCuratorIR();
      ir.content.specialization = null;

      const result = simplifyAgent(ir);

      expect(result).toBeTruthy();
      expect(result.split('\n').length).toBeLessThanOrEqual(40);
    });
  });
});
