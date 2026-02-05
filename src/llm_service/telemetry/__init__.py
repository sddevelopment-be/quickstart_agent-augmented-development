"""
Telemetry module for LLM Service Layer.

Provides cost tracking, performance monitoring, and invocation logging
for all LLM service requests.

Key Components:
- TelemetryLogger: Main logging interface
- InvocationRecord: Data structure for invocation metadata
- SQLite backend for persistent storage
"""

from .logger import TelemetryLogger, InvocationRecord

__all__ = ['TelemetryLogger', 'InvocationRecord']
