from datetime import datetime

from app.estimation.timeline_engine import TimelineEngine


def test_critical_path_uses_longest_dependency_chain():
    engine = TimelineEngine(start_date=datetime(2025, 1, 6, 9))
    engine.add_tasks_from_list([
        {"id": "design", "title": "Design", "estimated_hours": 8, "role_id": 1},
        {"id": "build", "title": "Build", "estimated_hours": 16, "role_id": 2, "dependencies": ["design"]},
        {"id": "test", "title": "Test", "estimated_hours": 8, "role_id": 3, "dependencies": ["build"]},
        {"id": "docs", "title": "Docs", "estimated_hours": 4, "role_id": 4},
    ])

    result = engine.get_formatted_timeline()
    assert result["critical_path"] == ["design", "build", "test"]
    assert result["total_working_days"] >= 4


def test_empty_timeline_has_no_tasks_or_duration():
    result = TimelineEngine().get_formatted_timeline()
    assert result["critical_path"] == []
    assert result["total_days"] == 0


def test_dependency_cycle_is_rejected():
    engine = TimelineEngine()
    engine.add_tasks_from_list([
        {"id": "first", "estimated_hours": 1, "dependencies": ["second"]},
        {"id": "second", "estimated_hours": 1, "dependencies": ["first"]},
    ])
    try:
        engine.get_formatted_timeline()
    except Exception as exc:
        assert "cycle" in str(exc).lower() or "dag" in str(exc).lower()
    else:
        raise AssertionError("A cyclic task graph must not produce a valid timeline")
