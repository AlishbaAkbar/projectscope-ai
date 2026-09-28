import json

import pytest

from app.ai.providers.mock_provider import MockLLMProvider


@pytest.mark.asyncio
async def test_vague_project_brief_returns_clarifying_question():
    payload = json.loads(await MockLLMProvider().generate(
        'Project Description:\n"""A new software project."""'
    ))
    assert payload["missing_information"]
    assert payload["requirements"] == []


@pytest.mark.asyncio
async def test_healthcare_brief_flags_unspecified_regulatory_needs():
    payload = json.loads(await MockLLMProvider().generate(
        'Project Description:\n"""A clinic app for patients to book appointments with doctors."""'
    ))
    assert any("privacy" in question.lower() or "regulatory" in question.lower()
               for question in payload["missing_information"])
