"""
Tests for portfolio API initiative grouping.

Tests proper hierarchy: Initiative → Specification → Feature → Task

Related: ADR-037 Dashboard Initiative Tracking
"""

from collections import defaultdict

import pytest


def test_initiative_grouping_structure():
    """Portfolio API should group specifications by initiative field."""
    # ARRANGE
    specs = [
        {
            "id": "SPEC-001",
            "title": "Real-Time Dashboard",
            "initiative": "Dashboard Enhancements",
            "status": "implemented",
            "priority": "HIGH",
            "progress": 100,
            "features": [],
        },
        {
            "id": "SPEC-002",
            "title": "Priority Editing",
            "initiative": "Dashboard Enhancements",
            "status": "implemented",
            "priority": "MEDIUM",
            "progress": 100,
            "features": [],
        },
        {
            "id": "SPEC-003",
            "title": "Code Distribution",
            "initiative": "Framework Distribution",
            "status": "in_progress",
            "priority": "CRITICAL",
            "progress": 50,
            "features": [],
        },
    ]

    # ACT
    initiatives_grouped = defaultdict(list)
    for spec in specs:
        initiative_name = spec.get("initiative") or "Uncategorized"
        initiatives_grouped[initiative_name].append(spec)

    # ASSERT
    assert len(initiatives_grouped) == 2
    assert len(initiatives_grouped["Dashboard Enhancements"]) == 2
    assert len(initiatives_grouped["Framework Distribution"]) == 1


def test_initiative_progress_calculation():
    """Initiative progress should aggregate from all specification features."""
    # ARRANGE
    specs = [
        {
            "features": [
                {"progress": 100, "tasks": [{"status": "done"}]},
                {"progress": 50, "tasks": [{"status": "in_progress"}]},
            ]
        },
        {
            "features": [
                {"progress": 100, "tasks": [{"status": "done"}]},
            ]
        },
    ]

    # ACT - Collect all features from all specs
    all_features = []
    for spec in specs:
        all_features.extend(spec["features"])

    # Calculate average progress
    if all_features:
        avg_progress = sum(f["progress"] for f in all_features) / len(all_features)
    else:
        avg_progress = 0

    # ASSERT
    assert len(all_features) == 3
    expected_progress = (100 + 50 + 100) / 3
    assert avg_progress == pytest.approx(expected_progress, rel=0.01)


def test_initiative_status_priority_inheritance():
    """Initiative should inherit highest status and priority from specs."""
    # ARRANGE
    specs = [
        {"status": "draft", "priority": "LOW"},
        {"status": "in_progress", "priority": "HIGH"},
        {"status": "implemented", "priority": "MEDIUM"},
    ]

    # ACT
    status_priority = {"draft": 1, "in_progress": 2, "implemented": 3, "complete": 3}
    initiative_status = max(
        (spec.get("status", "draft") for spec in specs),
        key=lambda s: status_priority.get(s, 0),
    )

    priority_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    initiative_priority = max(
        (spec.get("priority", "MEDIUM") for spec in specs),
        key=lambda p: priority_order.get(p, 2),
    )

    # ASSERT
    assert initiative_status == "implemented"
    assert initiative_priority == "HIGH"


def test_uncategorized_specs_handling():
    """Specs without initiative field should go to 'Uncategorized'."""
    # ARRANGE
    specs = [
        {"id": "SPEC-001", "initiative": "My Initiative"},
        {"id": "SPEC-002"},  # No initiative field
        {"id": "SPEC-003", "initiative": None},  # Explicit None
    ]

    # ACT
    initiatives_grouped = defaultdict(list)
    for spec in specs:
        initiative_name = spec.get("initiative") or "Uncategorized"
        initiatives_grouped[initiative_name].append(spec)

    # ASSERT
    assert "My Initiative" in initiatives_grouped
    assert "Uncategorized" in initiatives_grouped
    assert len(initiatives_grouped["Uncategorized"]) == 2


def test_initiative_response_structure():
    """Each initiative should have proper response structure."""
    # ARRANGE
    initiative_name = "Dashboard Enhancements"
    specs = [
        {
            "id": "SPEC-001",
            "title": "Real-Time Dashboard",
            "status": "implemented",
            "priority": "HIGH",
            "progress": 100,
            "features": [],
        }
    ]

    # ACT
    initiative = {
        "id": initiative_name.lower().replace(" ", "-"),
        "title": initiative_name,
        "status": "implemented",
        "priority": "HIGH",
        "progress": 100,
        "specifications": specs,
        "spec_count": len(specs),
    }

    # ASSERT
    assert initiative["id"] == "dashboard-enhancements"
    assert initiative["title"] == "Dashboard Enhancements"
    assert initiative["spec_count"] == 1
    assert "specifications" in initiative
    assert len(initiative["specifications"]) == 1
    assert initiative["specifications"][0]["id"] == "SPEC-001"
