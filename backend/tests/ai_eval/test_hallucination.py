import json

import pytest

from app.ai.providers.mock_provider import MockLLMProvider
from app.ai.schemas import RawAnalysisResponse


@pytest.mark.asyncio
async def test_short_non_specific_description_does_not_create_features_or_requirements():
    payload = json.loads(await MockLLMProvider().generate(
        'Project Description:\n"""A small project."""'
    ))
    response = RawAnalysisResponse.model_validate(payload)
    assert response.features == []
    assert response.requirements == []
    assert response.missing_information
