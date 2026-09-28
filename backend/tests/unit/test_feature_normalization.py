import pytest

from app.services.feature_service import FeatureService


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("login", "AUTHENTICATION"),
        ("Sign up", "AUTHENTICATION"),
        ("checkout", "PAYMENT"),
        ("patient profile", "USER_PROFILE"),
        ("a bespoke module", "A_BESPOKE_MODULE"),
    ],
)
def test_feature_names_normalize_to_canonical_keys(raw, expected):
    assert FeatureService.normalize_name(raw) == expected


def test_blank_feature_name_gets_safe_fallback():
    assert FeatureService.normalize_name("") == "GENERAL_FEATURE"
