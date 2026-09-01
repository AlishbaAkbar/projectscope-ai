import pytest
from app.services.task_service import TaskService


def test_authentication_task_generation():
    tasks = TaskService.generate_tasks_for_feature(
        normalized_key="AUTHENTICATION",
        feature_name="authentication",
        description="User login and registration"
    )
    assert len(tasks) >= 4
    categories = {t.category for t in tasks}
    assert "Frontend" in categories
    assert "Backend" in categories
    assert "Database" in categories
    assert "QA" in categories

    for t in tasks:
        assert t.title
        assert t.description
        assert t.estimated_hours is not None
        assert t.estimated_hours > 0


def test_live_tracking_task_generation():
    tasks = TaskService.generate_tasks_for_feature(
        normalized_key="LIVE_TRACKING",
        feature_name="live_tracking",
        description="Real-time GPS vehicle location tracking"
    )
    assert len(tasks) >= 4
    categories = {t.category for t in tasks}
    assert "Frontend" in categories
    assert "Backend" in categories
    assert "Database" in categories
    assert "QA" in categories
    assert "Integration" in categories


def test_custom_feature_task_generation():
    tasks = TaskService.generate_tasks_for_feature(
        normalized_key="AI_VOICE_ASSISTANT",
        feature_name="ai_voice_assistant",
        description="Voice interaction engine"
    )
    assert len(tasks) == 4
    categories = {t.category for t in tasks}
    assert "Frontend" in categories
    assert "Backend" in categories
    assert "Database" in categories
    assert "QA" in categories
    assert any("Ai Voice Assistant" in t.title for t in tasks)
