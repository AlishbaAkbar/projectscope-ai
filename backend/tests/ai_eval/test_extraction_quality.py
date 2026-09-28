import json

import pytest

from app.ai.providers.mock_provider import MockLLMProvider
from app.ai.schemas import RawAnalysisResponse


@pytest.mark.asyncio
async def test_provider_output_is_validated_against_analysis_schema():
    output = await MockLLMProvider().generate(
        'Project Description:\n"""A clinic where doctors and patients book appointments."""'
    )
    result = RawAnalysisResponse.model_validate(json.loads(output))
    assert result.project_type == "healthcare"
    assert result.requirements
    assert result.features


@pytest.mark.asyncio
async def test_healthcare_precedes_ecommerce_metadata():
    output = await MockLLMProvider().generate(
        'Project Description:\n"""Doctors manage patient medical appointments."""\nCategory: e-commerce'
    )
    assert json.loads(output)["project_type"] == "healthcare"


@pytest.mark.asyncio
async def test_every_requirement_has_a_valid_confidence_and_category():
    output = await MockLLMProvider().generate(
        'Project Description:\n"""A clinic with appointment scheduling and secure patient records."""'
    )
    response = RawAnalysisResponse.model_validate(json.loads(output))
    assert all(0 <= item.confidence <= 1 and item.category for item in response.requirements)
