import json

from app.ai.providers.mock_provider import MockLLMProvider
from app.models.llm_request import LLMRequest
from app.models.project import Requirement
import app.api.routes.projects as projects_route


def test_mock_provider_analysis_persists_extracted_results(
    authenticated_client,
    auth_headers,
    db,
    monkeypatch,
):
    monkeypatch.setattr(projects_route, "get_provider", MockLLMProvider)
    created = authenticated_client.post(
        "/api/v1/projects",
        headers=auth_headers,
        json={
            "name": "Clinic Scheduling",
            "type": "healthcare",
            "description": "Doctors and patients schedule clinic appointments and manage medical records.",
        },
    )
    assert created.status_code == 201, created.text
    project_id = created.json()["id"]

    analysis = authenticated_client.post(
        f"/api/v1/projects/{project_id}/analyze",
        headers=auth_headers,
    )
    assert analysis.status_code == 200, analysis.text

    requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()
    assert requirements
    assert all(item.source == "ai_generated" for item in requirements)
    assert not any("shopping cart" in item.text.lower() for item in requirements)
    assert db.query(LLMRequest).filter(LLMRequest.project_id == project_id).count() == 1

    features = authenticated_client.get(f"/api/v1/projects/{project_id}/features")
    assert features.status_code == 200
    names = {feature["canonical_name"] for feature in features.json()}
    assert "BOOKING" in names
    assert "CART" not in names


def test_mock_provider_does_not_invent_features_for_vague_brief():
    provider = MockLLMProvider()
    payload = provider.analyze_requirements('Project Description:\n"""A project."""\n')
    assert payload["requirements"] == []
    assert payload["features"] == []
    assert payload["users"] == []


def test_llm_failure_and_retry_are_audited(db):
    from app.ai.analyzer import RequirementAnalyzer
    from app.ai.providers.base import LLMProvider
    from app.utils.error_handlers import LLMProviderException

    class FailedProvider(LLMProvider):
        async def analyze(self, prompt, system_prompt=None):
            raise LLMProviderException("unavailable", provider="test")

        async def generate(self, prompt, system_prompt=None):
            return await self.analyze(prompt, system_prompt)

    import asyncio

    result = asyncio.run(RequirementAnalyzer(
        provider=FailedProvider(),
        db=db,
        project_id=None,
    ).analyze("Clinic", "A clinic for doctors and patients to book appointments."))

    assert result.project_type == "healthcare"
    requests = db.query(LLMRequest).all()
    assert [request.status for request in requests] == ["failure", "success"]
    assert requests[0].error_message


def test_invalid_llm_output_retries_once_with_error_feedback_then_falls_back():
    import asyncio
    from app.ai.analyzer import RequirementAnalyzer
    from app.ai.providers.base import LLMProvider

    class InvalidThenValidProvider(LLMProvider):
        def __init__(self):
            self.prompts = []

        async def analyze(self, prompt, system_prompt=None):
            self.prompts.append(prompt)
            if len(self.prompts) == 1:
                return "not JSON"
            return json.dumps({
                "project_type": "healthcare",
                "users": ["doctor"],
                "requirements": [{"text": "Doctors can manage appointments", "confidence": 0.9}],
                "features": [{"name": "appointment scheduling", "complexity": "medium"}],
                "missing_information": [],
                "assumptions": [],
            })

        async def generate(self, prompt, system_prompt=None):
            return await self.analyze(prompt, system_prompt)

    provider = InvalidThenValidProvider()
    result = asyncio.run(RequirementAnalyzer(provider=provider).analyze(
        "Clinic",
        "Doctors manage patient appointments at a clinic.",
    ))
    assert result.project_type == "healthcare"
    assert len(provider.prompts) == 2
    assert "failed validation" in provider.prompts[1]


def test_two_invalid_llm_responses_fall_back_to_mock():
    import asyncio
    from app.ai.analyzer import RequirementAnalyzer
    from app.ai.providers.base import LLMProvider

    class AlwaysInvalidProvider(LLMProvider):
        async def analyze(self, prompt, system_prompt=None):
            return "invalid JSON"

        async def generate(self, prompt, system_prompt=None):
            return await self.analyze(prompt, system_prompt)

    result = asyncio.run(RequirementAnalyzer(provider=AlwaysInvalidProvider()).analyze(
        "Clinic",
        "Doctors and patients schedule clinic appointments.",
    ))
    assert result.project_type == "healthcare"


def test_ai_endpoint_populates_features_and_tasks(
    authenticated_client,
    auth_headers,
    monkeypatch,
    seed_roles,
):
    monkeypatch.setattr(projects_route, "get_provider", MockLLMProvider)
    created = authenticated_client.post(
        "/api/v1/projects",
        headers=auth_headers,
        json={
            "name": "Transit Tracker",
            "description": "Students track bus routes and live arrival times.",
        },
    )
    project_id = created.json()["id"]
    response = authenticated_client.post(
        f"/api/v1/projects/{project_id}/analyze",
        headers=auth_headers,
    )
    assert response.status_code == 200, response.text
    assert response.json()["features"]
    assert response.json()["tasks"]
