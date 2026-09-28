import asyncio

import pytest

from app.ai.analyzer import RequirementAnalyzer
from app.ai.providers.mock_provider import MockLLMProvider


@pytest.mark.asyncio
async def test_five_parallel_analyses_complete_without_shared_state_leaks():
    descriptions = [
        "A clinic app for doctors and patients to book appointments.",
        "Students track bus routes and driver arrival times.",
        "A restaurant app lets customers order meals for delivery.",
        "A shop lets buyers search product inventory and checkout carts.",
        "A course platform helps teachers manage lessons and students.",
    ]
    results = await asyncio.gather(*[
        RequirementAnalyzer(provider=MockLLMProvider()).analyze(
            f"Parallel project {index}",
            description,
        )
        for index, description in enumerate(descriptions)
    ])
    assert [result.project_type for result in results] == [
        "healthcare",
        "transportation",
        "food_delivery",
        "e-commerce",
        "saas",
    ]
