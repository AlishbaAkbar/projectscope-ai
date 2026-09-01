import json
import pytest
from app.ai.analyzer import RequirementAnalyzer
from app.ai.providers.base import LLMProvider
from app.schemas.analysis import RawAIAnalysisResponse
from app.utils.error_handlers import LLMValidationException


class DummyStringProvider(LLMProvider):
    def __init__(self, response_text: str):
        self.response_text = response_text

    async def analyze(self, prompt: str, system_prompt: str = None) -> str:
        return self.response_text

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        return self.response_text


@pytest.mark.asyncio
async def test_valid_structured_response_parsing():
    valid_payload = {
        "project_type": "ecommerce",
        "users": ["buyer", "seller"],
        "requirements": [
            {"text": "Buyers can browse items", "category": "functional", "confidence": 0.95},
            {"text": "System must respond under 200ms", "category": "non_functional", "confidence": 0.90}
        ],
        "features": [
            {"name": "authentication", "description": "User login and signup", "priority": "high", "complexity": "medium", "confidence": 0.95},
            {"name": "payment", "description": "Checkout process", "priority": "critical", "complexity": "high", "confidence": 0.98}
        ],
        "missing_information": ["Target currency is not specified"],
        "assumptions": ["Cloud hosted database"]
    }

    provider = DummyStringProvider(json.dumps(valid_payload))
    analyzer = RequirementAnalyzer(provider=provider)

    result = await analyzer.analyze("Store", "An ecommerce store for selling electronics")
    assert isinstance(result, RawAIAnalysisResponse)
    assert result.project_type == "ecommerce"
    assert len(result.requirements) == 2
    assert result.requirements[0].category == "functional"
    assert result.requirements[1].category == "non_functional"
    assert len(result.features) == 2


@pytest.mark.asyncio
async def test_markdown_wrapped_json_parsing():
    valid_payload = {
        "project_type": "saas",
        "users": ["admin", "member"],
        "requirements": [{"text": "Login required", "category": "functional", "confidence": 1.0}],
        "features": [{"name": "auth", "description": "Authentication module", "priority": "high", "complexity": "medium", "confidence": 1.0}],
        "missing_information": [],
        "assumptions": []
    }

    wrapped_text = f"Here is the analysis:\n```json\n{json.dumps(valid_payload)}\n```\nHope this helps!"

    provider = DummyStringProvider(wrapped_text)
    analyzer = RequirementAnalyzer(provider=provider)

    result = await analyzer.analyze("SaaS Tool", "A dashboard SaaS tool")
    assert result.project_type == "saas"
    assert len(result.requirements) == 1


@pytest.mark.asyncio
async def test_invalid_json_raises_validation_exception():
    invalid_text = "This is not json at all, just a paragraph of text explaining the project."

    provider = DummyStringProvider(invalid_text)
    analyzer = RequirementAnalyzer(provider=provider)

    with pytest.raises(LLMValidationException):
        await analyzer.analyze("App", "Some generic project description")


@pytest.mark.asyncio
async def test_missing_required_fields_raises_validation_exception():
    # Missing 'project_type'
    incomplete_payload = {
        "users": ["student"],
        "requirements": [],
        "features": []
    }

    provider = DummyStringProvider(json.dumps(incomplete_payload))
    analyzer = RequirementAnalyzer(provider=provider)

    with pytest.raises(LLMValidationException):
        await analyzer.analyze("App", "Some generic project description")
