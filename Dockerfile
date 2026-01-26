# Multi-stage Dockerfile for Agent-Augmented Development Repository
# Purpose: Provide a portable environment with shared configs and docs
# while allowing user-specific files to be mounted at runtime

FROM python:3.10-slim AS base

# Metadata
LABEL org.opencontainers.image.title="Agent-Augmented Development Quickstart"
LABEL org.opencontainers.image.description="Portable environment for agent-augmented development workflows"
LABEL org.opencontainers.image.source="https://github.com/sddevelopment-be/quickstart_agent-augmented-development"
LABEL org.opencontainers.image.documentation="https://github.com/sddevelopment-be/quickstart_agent-augmented-development/blob/main/README.md"

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies first for layer caching
COPY requirements.txt requirements-dev.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt

# Copy shared configuration and documentation
# These are the files that should be standardized across all users
COPY .github/ .github/
COPY docs/ docs/
COPY agents/ agents/
COPY framework/ framework/
COPY ops/ ops/
COPY validation/ validation/
COPY AGENTS.md LICENSE README.md REPO_MAP.md ./

# Create mount points for user-specific directories
# These should be mounted from the user's local filesystem
RUN mkdir -p /workspace/work /workspace/output /workspace/tmp

# Set up volume mount points
VOLUME ["/workspace/work", "/workspace/output", "/workspace/tmp"]

# Default command: show usage information
CMD ["python", "-c", "print('Agent-Augmented Development Environment\\n\\nShared configs loaded from image.\\nMount your local directories:\\n  - work/\\n  - output/\\n  - tmp/\\n\\nExample:\\n  docker run -v $(pwd)/work:/workspace/work -v $(pwd)/output:/workspace/output agent-augmented-dev\\n')"]
