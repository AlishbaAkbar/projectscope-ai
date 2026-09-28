import pytest

from app.ai.providers.mock_provider import MockLLMProvider
import app.api.routes.projects as projects_route


@pytest.mark.parametrize(
    "description",
    [
        "Patients book clinic appointments with doctors.",
        "Students track bus routes and arrival times.",
    ],
)
def test_analysis_tasks_have_estimates_and_roles(
    authenticated_client,
    auth_headers,
    monkeypatch,
    seed_roles,
    description,
):
    monkeypatch.setattr(projects_route, "get_provider", MockLLMProvider)
    created = authenticated_client.post(
        "/api/v1/projects",
        headers=auth_headers,
        json={"name": "Task Quality Project", "description": description},
    )
    assert created.status_code == 201, created.text
    response = authenticated_client.post(
        f"/api/v1/projects/{created.json()['id']}/analyze",
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    assert all(
        task["estimated_hours"] > 0 and task["role_id"] > 0
        for task in response.json()["tasks"]
    )
