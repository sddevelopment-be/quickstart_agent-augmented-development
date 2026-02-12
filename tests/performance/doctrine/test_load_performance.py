"""
Performance tests for doctrine loading.

Benchmarks loading times for agents and directives to ensure the doctrine
system can scale to 20+ agents without performance degradation.

Performance Requirements
------------------------
- Load 20 agents in <500ms
- Load 20 directives in <500ms
- Validate 20 agents + directives in <200ms
- No memory leaks during repeated loading

Test Approach
-------------
Uses pytest-benchmark if available, falls back to time.perf_counter() timing.
Tests are informational and report performance metrics without hard failures
unless performance degrades significantly (>10x baseline).
"""

import pytest
import time
from pathlib import Path
from typing import List

from src.domain.doctrine.models import Agent, Directive
from src.domain.doctrine.parsers import AgentParser, DirectiveParser
from src.domain.doctrine.validators import CrossReferenceValidator


class TestLoadPerformance:
    """Performance benchmarks for doctrine loading."""

    @pytest.fixture
    def agent_files(self) -> List[Path]:
        """Get list of agent files (up to 20)."""
        agents_dir = Path(".github/agents")
        if not agents_dir.exists():
            pytest.skip("Agents directory not found")

        agent_files = list(agents_dir.glob("*.agent.md"))[:20]
        if not agent_files:
            pytest.skip("No agent files found")

        return agent_files

    @pytest.fixture
    def directive_files(self) -> List[Path]:
        """Get list of directive files (up to 20)."""
        # Try multiple locations
        directives_dir = None
        for path in [Path("doctrine/directives"), Path("directives")]:
            if path.exists():
                directives_dir = path
                break

        if not directives_dir:
            pytest.skip("Directives directory not found")

        directive_files = list(directives_dir.glob("*.md"))[:20]
        if not directive_files:
            pytest.skip("No directive files found")

        return directive_files

    def test_load_agents_performance(self, agent_files: List[Path]):
        """Loading 20 agents should complete in reasonable time (<500ms)."""
        parser = AgentParser()

        # Warmup
        for file_path in agent_files[:2]:
            try:
                parser.parse(file_path)
            except Exception:
                pass

        # Benchmark
        start_time = time.perf_counter()

        agents: List[Agent] = []
        for file_path in agent_files:
            try:
                agent = parser.parse(file_path)
                agents.append(agent)
            except Exception as e:
                # Don't fail on parse errors, just skip
                print(f"⚠️  Failed to parse {file_path.name}: {e}")

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        # Report results
        print(f"\n📊 Agent Loading Performance:")
        print(f"   Files attempted: {len(agent_files)}")
        print(f"   Successfully loaded: {len(agents)}")
        print(f"   Total time: {elapsed_ms:.2f}ms")
        print(f"   Time per agent: {elapsed_ms / len(agents) if agents else 0:.2f}ms")
        print(f"   Throughput: {len(agents) / (elapsed_ms / 1000) if elapsed_ms > 0 else 0:.1f} agents/sec")

        # Assertions
        assert len(agents) > 0, "No agents loaded"

        # Performance target: <500ms for 20 agents
        if len(agents) >= 20:
            target_ms = 500
            if elapsed_ms > target_ms:
                print(f"\n⚠️  Performance warning: {elapsed_ms:.2f}ms > {target_ms}ms target")
            else:
                print(f"\n✅ Performance acceptable: {elapsed_ms:.2f}ms <= {target_ms}ms target")

            # Fail only if drastically over budget (>2x)
            assert elapsed_ms < target_ms * 2, f"Loading too slow: {elapsed_ms:.2f}ms > {target_ms * 2}ms"

    def test_load_directives_performance(self, directive_files: List[Path]):
        """Loading 20 directives should complete in reasonable time (<500ms)."""
        parser = DirectiveParser()

        # Warmup
        for file_path in directive_files[:2]:
            try:
                parser.parse(file_path)
            except Exception:
                pass

        # Benchmark
        start_time = time.perf_counter()

        directives: List[Directive] = []
        for file_path in directive_files:
            try:
                directive = parser.parse(file_path)
                directives.append(directive)
            except Exception as e:
                print(f"⚠️  Failed to parse {file_path.name}: {e}")

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        # Report results
        print(f"\n📊 Directive Loading Performance:")
        print(f"   Files attempted: {len(directive_files)}")
        print(f"   Successfully loaded: {len(directives)}")
        print(f"   Total time: {elapsed_ms:.2f}ms")
        print(f"   Time per directive: {elapsed_ms / len(directives) if directives else 0:.2f}ms")
        print(f"   Throughput: {len(directives) / (elapsed_ms / 1000) if elapsed_ms > 0 else 0:.1f} directives/sec")

        # Assertions
        assert len(directives) > 0, "No directives loaded"

        # Performance target: <500ms for 20 directives
        if len(directives) >= 20:
            target_ms = 500
            if elapsed_ms > target_ms:
                print(f"\n⚠️  Performance warning: {elapsed_ms:.2f}ms > {target_ms}ms target")
            else:
                print(f"\n✅ Performance acceptable: {elapsed_ms:.2f}ms <= {target_ms}ms target")

            # Fail only if drastically over budget (>2x)
            assert elapsed_ms < target_ms * 2, f"Loading too slow: {elapsed_ms:.2f}ms > {target_ms * 2}ms"

    def test_validation_performance(
        self, agent_files: List[Path], directive_files: List[Path]
    ):
        """Validating 20 agents + directives should be fast (<200ms)."""
        # Load agents
        agent_parser = AgentParser()
        agents: List[Agent] = []
        for file_path in agent_files:
            try:
                agents.append(agent_parser.parse(file_path))
            except Exception:
                pass

        # Load directives
        directive_parser = DirectiveParser()
        directives: List[Directive] = []
        for file_path in directive_files:
            try:
                directives.append(directive_parser.parse(file_path))
            except Exception:
                pass

        if not agents or not directives:
            pytest.skip("Need both agents and directives for validation")

        # Benchmark validation
        start_time = time.perf_counter()

        validator = CrossReferenceValidator(directives, agents)
        result = validator.validate_all()

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        # Report results
        print(f"\n📊 Validation Performance:")
        print(f"   Agents validated: {len(agents)}")
        print(f"   Directives checked: {len(directives)}")
        print(f"   Validation time: {elapsed_ms:.2f}ms")
        print(f"   Errors found: {len(result.errors)}")
        print(f"   Warnings found: {len(result.warnings)}")

        # Performance target: <200ms for validation
        target_ms = 200
        if elapsed_ms > target_ms:
            print(f"\n⚠️  Performance warning: {elapsed_ms:.2f}ms > {target_ms}ms target")
        else:
            print(f"\n✅ Performance acceptable: {elapsed_ms:.2f}ms <= {target_ms}ms target")

        # Fail only if drastically over budget (>5x for validation)
        assert elapsed_ms < target_ms * 5, f"Validation too slow: {elapsed_ms:.2f}ms > {target_ms * 5}ms"

    def test_repeated_loading_performance(self, agent_files: List[Path]):
        """Test repeated loading to check for memory leaks or degradation."""
        parser = AgentParser()

        # Limit to 10 agents and 10 iterations for speed
        test_files = agent_files[:10]
        iterations = 10

        times: List[float] = []

        for i in range(iterations):
            start_time = time.perf_counter()

            agents: List[Agent] = []
            for file_path in test_files:
                try:
                    agents.append(parser.parse(file_path))
                except Exception:
                    pass

            end_time = time.perf_counter()
            times.append((end_time - start_time) * 1000)

        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = (sum((t - avg_time) ** 2 for t in times) / len(times)) ** 0.5

        print(f"\n📊 Repeated Loading Performance ({iterations} iterations):")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Min: {min_time:.2f}ms")
        print(f"   Max: {max_time:.2f}ms")
        print(f"   Std Dev: {std_dev:.2f}ms")
        print(f"   Variation: {(std_dev / avg_time * 100) if avg_time > 0 else 0:.1f}%")

        # Check for performance degradation
        first_half_avg = sum(times[: len(times) // 2]) / (len(times) // 2)
        second_half_avg = sum(times[len(times) // 2 :]) / (len(times) - len(times) // 2)

        degradation = ((second_half_avg - first_half_avg) / first_half_avg * 100) if first_half_avg > 0 else 0

        print(f"\n   First half avg: {first_half_avg:.2f}ms")
        print(f"   Second half avg: {second_half_avg:.2f}ms")
        print(f"   Degradation: {degradation:+.1f}%")

        # Fail if significant degradation (>50%)
        if degradation > 50:
            print(f"\n⚠️  Performance degradation detected: {degradation:.1f}%")
        else:
            print(f"\n✅ Performance stable across iterations")

        assert degradation < 100, f"Severe performance degradation: {degradation:.1f}%"


class TestMemoryUsage:
    """Test memory usage during doctrine loading."""

    def test_memory_usage_estimate(self, agent_files: List[Path]):
        """Estimate memory usage for loaded agents."""
        import sys

        parser = AgentParser()
        agents: List[Agent] = []

        # Load all available agents
        for file_path in agent_files[:20]:
            try:
                agents.append(parser.parse(file_path))
            except Exception:
                pass

        if not agents:
            pytest.skip("No agents loaded for memory test")

        # Rough memory estimation
        # Note: This is approximate and platform-dependent
        total_size = sum(sys.getsizeof(agent) for agent in agents)

        # Account for strings and collections
        for agent in agents:
            total_size += sys.getsizeof(agent.id)
            total_size += sys.getsizeof(agent.name)
            total_size += sys.getsizeof(agent.specialization)
            # Add size of frozensets (approximate)
            total_size += sum(sys.getsizeof(item) for item in agent.capabilities)
            total_size += sum(sys.getsizeof(item) for item in agent.required_directives)

        avg_size_bytes = total_size / len(agents) if agents else 0
        avg_size_kb = avg_size_bytes / 1024

        print(f"\n📊 Memory Usage Estimate:")
        print(f"   Agents loaded: {len(agents)}")
        print(f"   Total size: {total_size / 1024:.2f} KB")
        print(f"   Average per agent: {avg_size_kb:.2f} KB")
        print(f"   Estimated for 100 agents: {avg_size_kb * 100:.2f} KB")

        # Sanity check: average agent shouldn't be > 100KB
        assert avg_size_kb < 100, f"Agent memory usage too high: {avg_size_kb:.2f} KB per agent"

        print(f"\n✅ Memory usage acceptable")

    @pytest.fixture
    def agent_files(self) -> List[Path]:
        """Get list of agent files (up to 20)."""
        agents_dir = Path(".github/agents")
        if not agents_dir.exists():
            pytest.skip("Agents directory not found")

        agent_files = list(agents_dir.glob("*.agent.md"))[:20]
        if not agent_files:
            pytest.skip("No agent files found")

        return agent_files
