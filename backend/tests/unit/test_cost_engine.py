import pytest

from app.estimation.cost_engine import CostEngine


def test_project_cost_sums_role_ranges():
    result = CostEngine().calculate_project_cost({
        "UI/UX Designer": 10,
        "Backend Developer": 20,
    })

    assert result["total"]["min"] == 1240
    assert result["total"]["expected"] == 1550
    assert result["total"]["max"] == 1860
    assert result["summary"]["total_hours"] == 30


def test_unknown_role_uses_fallback_rate_and_markup():
    result = CostEngine().calculate_role_cost("Custom Role", 10, markup=1.5)

    assert result.min_cost == 600
    assert result.expected_cost == 750
    assert result.max_cost == 900


def test_empty_project_cost_is_zero():
    assert CostEngine().calculate_project_cost({})["total"] == {
        "min": 0,
        "expected": 0,
        "max": 0,
    }


@pytest.mark.parametrize("hours", [0, 1, 10])
def test_cost_calculation_is_deterministic(hours):
    result = CostEngine().calculate_role_cost("QA Engineer", hours)
    assert result.min_cost <= result.expected_cost <= result.max_cost
