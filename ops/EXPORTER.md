# Agent Framework Export Tools

This directory contains conversion and export tools for transforming the agent framework into various standard formats.

## Available Tools

### opencode-exporter.js

Converts agent profiles to OpenCode standard format (https://opencode.ai).

**Features:**
- Parses YAML frontmatter from agent markdown files
- Generates OpenCode discovery files (`.opencode.json`)
- Generates OpenCode definition files (`.definition.yaml`)
- Creates tool registry
- Creates manifest file
- Preserves markdown as single source of truth

**Usage:**
```bash
# Export all agents
node tools/opencode-exporter.js

# Export specific agent
node tools/opencode-exporter.js --agent architect

# Custom output directory
node tools/opencode-exporter.js --output dist/custom
```

**Output Structure:**
```
dist/opencode/
├── agents/
│   ├── architect-alphonso.opencode.json
│   ├── architect-alphonso.definition.yaml
│   ├── backend-benny.opencode.json
│   └── backend-benny.definition.yaml
├── tools.opencode.json
└── manifest.opencode.json
```

**Requirements:**
- Node.js 14+
- `js-yaml` package (install with `npm install js-yaml`)

## Planned Tools

### copilot-exporter.js (Coming Soon)
Export to GitHub Copilot Skills format.

### mcp-exporter.js (Coming Soon)
Export to Model Context Protocol format.

### profile-validator.js (Coming Soon)
Validate agent profile frontmatter and structure.

### manifest-generator.js (Coming Soon)
Generate agent catalog manifest from profiles.

## Development

### Adding a New Exporter

1. Create a new file following the naming pattern `{format}-exporter.js`
2. Implement the core export logic
3. Support CLI arguments for filtering and output control
4. Add tests in `tools/tests/`
5. Update this README

### Testing

Run tests (when implemented):
```bash
npm test -- tools/
```

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Generate Exports
on: [push]
jobs:
  export:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install js-yaml
      - run: node tools/opencode-exporter.js
      - uses: actions/upload-artifact@v3
        with:
          name: opencode-exports
          path: dist/opencode/
```

## License

Same as parent repository.
