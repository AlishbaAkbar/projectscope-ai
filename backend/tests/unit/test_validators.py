import pytest
from pydantic import ValidationError

from app.ai.schemas import RawAnalysisResponse, RawFeature, RawRequirement
from app.schemas.auth import UserRegisterRequest


def test_raw_analysis_schema_accepts_complete_response():
    result = RawAnalysisResponse.model_validate({
        "project_type": " healthcare ",
        "users": [" patient "],
        "requirements": [{"text": " Book a visit ", "confidence": 0.9}],
        "features": [{"name": "appointments", "complexity": "medium"}],
        "missing_information": [" Which time zone? "],
        "assumptions": [],
    })
    assert result.project_type == "healthcare"
    assert result.requirements[0].text == "Book a visit"
    assert result.features[0].complexity == "medium"


@pytest.mark.parametrize(
    "payload",
    [
        {"text": " ", "confidence": 0.8},
        {"text": "x" * 2001, "confidence": 0.8},
        {"text": "valid text", "confidence": 1.1},
        {"text": "valid text", "category": " "},
    ],
)
def test_invalid_requirement_values_are_rejected(payload):
    with pytest.raises(ValidationError):
        RawRequirement.model_validate(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {"name": ""},
        {"name": "feature", "confidence": -0.01},
        {"name": "feature", "complexity": "extreme"},
        {"name": "feature", "complexity": 6},
        {"name": "x" * 101},
    ],
)
def test_invalid_feature_values_are_rejected(payload):
    with pytest.raises(ValidationError):
        RawFeature.model_validate(payload)


def test_short_or_empty_description_cannot_fabricate_features():
    result = RawAnalysisResponse.model_validate({
        "project_type": "saas",
        "users": [],
        "requirements": [],
        "features": [],
        "missing_information": ["What should the system do?"],
        "assumptions": [],
    })
    assert result.features == []
    assert result.requirements == []


def test_registration_password_policy_is_enforced():
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            email="valid@example.com",
            password="alllowercase",
            full_name="Test",
        )
