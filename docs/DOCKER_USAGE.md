# Docker Usage Guide

This repository provides a Docker image containing the shared configuration, documentation, and framework for agent-augmented development workflows.

## Overview

The Docker image includes:
- ✅ Shared agent configurations (`.github/agents/`)
- ✅ Documentation and guidelines (`docs/`)
- ✅ Framework and operations scripts (`framework/`, `ops/`)
- ✅ Validation tooling (`validation/`)
- ✅ Python dependencies pre-installed

User-specific directories are **not** included in the image and should be mounted from your local filesystem:
- `work/` - Your progress logs, notes, and collaboration files
- `output/` - Generated artifacts for review
- `tmp/` - Temporary files and reference materials

## Quick Start

### Pull the Image

```bash
docker pull ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest
```

### Run with Volume Mounts

```bash
docker run -it --rm \
  -v $(pwd)/work:/workspace/work \
  -v $(pwd)/output:/workspace/output \
  -v $(pwd)/tmp:/workspace/tmp \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest \
  /bin/bash
```

This command:
- Mounts your local `work/`, `output/`, and `tmp/` directories
- Provides an interactive shell in the container
- Removes the container when you exit (`--rm`)

## Common Use Cases

### 1. Running Validation Tests

```bash
docker run --rm \
  -v $(pwd)/work:/workspace/work \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest \
  python -m pytest validation/
```

### 2. Running Operations Scripts

```bash
docker run --rm \
  -v $(pwd)/work:/workspace/work \
  -v $(pwd)/output:/workspace/output \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest \
  python ops/orchestration/process_task.py work/collaboration/assigned/
```

### 3. Interactive Development Session

```bash
docker run -it --rm \
  -v $(pwd)/work:/workspace/work \
  -v $(pwd)/output:/workspace/output \
  -v $(pwd)/tmp:/workspace/tmp \
  -e GITHUB_TOKEN=${GITHUB_TOKEN} \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest \
  /bin/bash
```

### 4. Docker Compose Setup

Create a `docker-compose.yml` in your project:

```yaml
version: '3.8'

services:
  agent-dev:
    image: ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest
    volumes:
      - ./work:/workspace/work
      - ./output:/workspace/output
      - ./tmp:/workspace/tmp
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    stdin_open: true
    tty: true
```

Run with:
```bash
docker-compose run agent-dev /bin/bash
```

## Building Locally

If you want to build the image locally for testing:

```bash
# Build the image
docker build -t agent-augmented-dev:local .

# Run the local image
docker run -it --rm \
  -v $(pwd)/work:/workspace/work \
  -v $(pwd)/output:/workspace/output \
  agent-augmented-dev:local \
  /bin/bash
```

## Volume Mount Details

### Required Mounts

These directories contain user-specific content and should always be mounted:

| Local Path | Container Path | Purpose |
|------------|----------------|---------|
| `./work/` | `/workspace/work/` | Progress logs, notes, collaboration files |
| `./output/` | `/workspace/output/` | Generated artifacts awaiting review |

### Optional Mounts

| Local Path | Container Path | Purpose |
|------------|----------------|---------|
| `./tmp/` | `/workspace/tmp/` | Temporary files, reference docs |

### Read-Only Mounts

For production workflows, you may want to mount work directories as read-only:

```bash
docker run --rm \
  -v $(pwd)/work:/workspace/work:ro \
  -v $(pwd)/output:/workspace/output \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest \
  python ops/orchestration/validate_structure.py
```

## Environment Variables

The container respects these environment variables:

| Variable | Purpose | Example |
|----------|---------|---------|
| `GITHUB_TOKEN` | GitHub API access | `ghp_...` |
| `PYTHONPATH` | Python module paths | `/workspace/framework:/workspace/ops` |

## Security Considerations

### Secrets Management

**Never** include secrets in the Docker image. Always:
- Use environment variables for tokens
- Mount secret files as read-only volumes
- Use Docker secrets for orchestration

```bash
# Good: Pass secrets via environment
docker run --rm \
  -e GITHUB_TOKEN=$(cat ~/.github/token) \
  -v $(pwd)/work:/workspace/work \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest
```

### User Permissions

The container runs as root by default. For production:

```bash
# Run as specific user
docker run --rm \
  --user $(id -u):$(id -g) \
  -v $(pwd)/work:/workspace/work \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest
```

## Troubleshooting

### Permission Issues

If you encounter permission errors with mounted volumes:

```bash
# Option 1: Run as your user
docker run --user $(id -u):$(id -g) ...

# Option 2: Fix permissions after container exits
docker run --rm -v $(pwd)/work:/workspace/work busybox chown -R $(id -u):$(id -g) /workspace/work
```

### Python Module Not Found

Ensure the Python path is set correctly:

```bash
docker run --rm \
  -e PYTHONPATH=/workspace/framework:/workspace/ops \
  -v $(pwd)/work:/workspace/work \
  ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest
```

### Out of Date Image

Always pull the latest image:

```bash
docker pull ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest
```

## CI/CD Integration

### GitHub Actions Example

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:latest
    steps:
      - uses: actions/checkout@v4
      - name: Run validation
        run: python -m pytest validation/
```

## Version Pinning

For reproducibility, pin to specific versions:

```bash
# Use semantic version
docker pull ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:1.0.0

# Use commit SHA (most reproducible)
docker pull ghcr.io/sddevelopment-be/quickstart_agent-augmented-development:sha-abc1234
```

## Additional Resources

- [Repository README](../README.md)
- [Agent Configuration Guide](.github/agents/QUICKSTART.md)
- [Vision Document](docs/VISION.md)
- [Workflow Documentation](docs/WORKFLOWS.md)

## Support

For issues or questions:
- Open an issue: https://github.com/sddevelopment-be/quickstart_agent-augmented-development/issues
- Review documentation: https://github.com/sddevelopment-be/quickstart_agent-augmented-development/tree/main/docs
