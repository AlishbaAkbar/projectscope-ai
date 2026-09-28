from app.estimation.complexity_factors import ComplexityFactors


def test_known_feature_and_dependency_weights():
    score, breakdown = ComplexityFactors.calculate_complexity_score(
        ["PAYMENT", "AUTHENTICATION"],
        {"PAYMENT": ["AUTHENTICATION"]},
    )

    assert score == 8.5
    assert breakdown["PAYMENT"]["multiplier"] == 1.1
    assert breakdown["AUTHENTICATION"]["score"] == 3


def test_empty_features_have_zero_complexity():
    assert ComplexityFactors.calculate_complexity_score([]) == (0, {})


def test_complexity_levels_and_risk_levels():
    assert ComplexityFactors.get_complexity_level(10) == "LOW"
    assert ComplexityFactors.get_complexity_level(21) == "HIGH"
    assert ComplexityFactors.get_risk_level(14, 1) == "MEDIUM"


def test_unknown_feature_uses_default_weight():
    score, breakdown = ComplexityFactors.calculate_complexity_score(["CUSTOM_FEATURE"])
    assert score == 3
    assert breakdown["CUSTOM_FEATURE"]["base"] == 3
