#!/usr/bin/env python3
"""
Verification script for ADR-045 Task 5: Dashboard Integration.

This script demonstrates that the agent portfolio integration works correctly:
1. Loads agents using domain model (AgentParser)
2. Extracts capabilities and compliance
3. Provides data via API endpoint
4. Meets performance requirements

Usage:
    python verify_agent_portfolio.py
"""

import sys
from pathlib import Path
from time import perf_counter

# Add src to path for imports
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))


def test_service_direct():
    """Test 1: Direct service usage (Python API)."""
    print("=" * 70)
    print("TEST 1: Direct Service Usage (Python API)")
    print("=" * 70)

    from src.llm_service.dashboard.agent_portfolio import AgentPortfolioService

    # Create service
    service = AgentPortfolioService()
    print(f"✅ Service created: {service}")

    # Load agents
    start_time = perf_counter()
    agents = service.get_agents()
    load_time = (perf_counter() - start_time) * 1000

    print(f"✅ Loaded {len(agents)} agents in {load_time:.2f}ms")

    # Verify agents are domain objects
    if agents:
        agent = agents[0]
        print(f"✅ Sample agent: {agent.name} ({agent.id})")
        print(f"   Specialization: {agent.specialization}")
        print(f"   Required directives: {len(agent.required_directives)}")
        print(f"   Source: {agent.source_file.name}")

    # Get portfolio data
    portfolio = service.get_portfolio_data()
    print(
        f"✅ Portfolio data: {portfolio['metadata']['total_agents']} agents, "
        f"{portfolio['metadata']['load_time_ms']:.2f}ms"
    )

    # Verify structure
    assert "agents" in portfolio, "Portfolio should have 'agents' key"
    assert "metadata" in portfolio, "Portfolio should have 'metadata' key"
    assert (
        portfolio["metadata"]["load_time_ms"] < 100
    ), f"Load time should be <100ms, got {portfolio['metadata']['load_time_ms']}ms"

    print("✅ All assertions passed!\n")
    return True


def test_api_endpoint():
    """Test 2: API endpoint (REST API)."""
    print("=" * 70)
    print("TEST 2: API Endpoint (REST API)")
    print("=" * 70)

    from src.llm_service.dashboard.app import create_app

    # Create Flask app
    app_tuple = create_app()
    app = app_tuple[0]  # Extract Flask app
    print(f"✅ Flask app created")

    # Test client
    client = app.test_client()
    print(f"✅ Test client created")

    # Call API endpoint
    start_time = perf_counter()
    response = client.get("/api/agents/portfolio")
    api_time = (perf_counter() - start_time) * 1000

    print(f"✅ API response: {response.status_code} (took {api_time:.2f}ms)")

    # Verify response
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.get_json()
    print(f"✅ JSON data parsed: {data['metadata']['total_agents']} agents")

    # Verify structure
    assert "agents" in data, "Response should have 'agents' key"
    assert "metadata" in data, "Response should have 'metadata' key"
    assert "timestamp" in data, "Response should have 'timestamp' key"

    # Verify agent structure
    if data["agents"]:
        agent = data["agents"][0]
        required_fields = [
            "id",
            "name",
            "specialization",
            "capability_descriptions",
            "directive_compliance",
            "source_file",
            "source_hash",
        ]
        for field in required_fields:
            assert field in agent, f"Agent should have '{field}' field"
        print(f"✅ Agent data structure validated ({len(required_fields)} fields)")

    print("✅ All assertions passed!\n")
    return True


def test_performance():
    """Test 3: Performance validation."""
    print("=" * 70)
    print("TEST 3: Performance Validation")
    print("=" * 70)

    from src.llm_service.dashboard.agent_portfolio import AgentPortfolioService

    service = AgentPortfolioService()

    # Warm-up (load into cache)
    _ = service.get_agents()
    print("✅ Warm-up: agents loaded into cache")

    # Measure cached performance
    trials = 10
    times = []

    for i in range(trials):
        start_time = perf_counter()
        _ = service.get_portfolio_data()
        elapsed = (perf_counter() - start_time) * 1000
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"✅ Performance over {trials} trials:")
    print(f"   Average: {avg_time:.2f}ms")
    print(f"   Min: {min_time:.2f}ms")
    print(f"   Max: {max_time:.2f}ms")

    # Verify all under target
    target = 100  # ms
    assert max_time < target, f"Max time {max_time:.2f}ms exceeds target {target}ms"
    print(f"✅ All trials under {target}ms target!")

    # Calculate margin
    margin = ((target - avg_time) / target) * 100
    print(f"✅ Performance margin: {margin:.1f}% faster than target\n")

    return True


def test_domain_model_integration():
    """Test 4: Domain model integration."""
    print("=" * 70)
    print("TEST 4: Domain Model Integration")
    print("=" * 70)

    from src.domain.doctrine.models import Agent
    from src.domain.doctrine.parsers import AgentParser
    from src.llm_service.dashboard.agent_portfolio import AgentPortfolioService

    # Verify AgentParser is used (not raw YAML)
    service = AgentPortfolioService()
    print(f"✅ Service uses AgentParser: {hasattr(service, '_parser')}")

    # Verify agents are domain objects
    agents = service.get_agents()
    if agents:
        agent = agents[0]
        assert isinstance(agent, Agent), f"Agent should be Agent instance, got {type(agent)}"
        print(f"✅ Agent is domain object: {type(agent).__name__}")

        # Verify domain attributes
        domain_attrs = [
            "id",
            "name",
            "specialization",
            "capabilities",
            "required_directives",
            "primers",
            "source_file",
            "source_hash",
            "capability_descriptions",
        ]
        for attr in domain_attrs:
            assert hasattr(agent, attr), f"Agent should have '{attr}' attribute"
        print(f"✅ Domain attributes validated ({len(domain_attrs)} attributes)")

    print("✅ All assertions passed!\n")
    return True


def run_all_tests():
    """Run all verification tests."""
    print("\n")
    print("🚀 ADR-045 TASK 5 VERIFICATION SCRIPT")
    print("=" * 70)
    print("Verifying: Dashboard Integration (Portfolio View)")
    print("=" * 70)
    print()

    tests = [
        ("Direct Service Usage", test_service_direct),
        ("API Endpoint", test_api_endpoint),
        ("Performance Validation", test_performance),
        ("Domain Model Integration", test_domain_model_integration),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success, None))
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}\n")
            results.append((test_name, False, str(e)))

    # Summary
    print("=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    for test_name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if error:
            print(f"       Error: {error}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ ALL TESTS PASSED - READY FOR PRODUCTION!")
        return 0
    else:
        print("❌ SOME TESTS FAILED - REVIEW REQUIRED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
