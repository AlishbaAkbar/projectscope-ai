import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "project_name,description,expected_type,expected_users,expected_feature",
    [
        (
            "University Transport App",
            "I want to build a university transport app where students can view buses, track their bus live, receive notifications and report transport issues.",
            "transportation",
            "student",
            "live_tracking"
        ),
        (
            "Modern E-Commerce Store",
            "An online store where customers can browse catalog, add items to cart, checkout with Stripe, and track orders.",
            "e-commerce",
            "customer",
            "payment"
        ),
        (
            "QuickBite Food Delivery",
            "A food delivery application where users can discover local restaurants, order food, and track courier on a live GPS map.",
            "food_delivery",
            "customer",
            "live_tracking"
        ),
        (
            "MediCare Clinic Scheduler",
            "A healthcare appointment system where patients can search doctors, book consultation slots, and review medical history.",
            "healthcare",
            "patient",
            "booking"
        ),
    ]
)
def test_e2e_project_scenarios(
    client: TestClient,
    project_name: str,
    description: str,
    expected_type: str,
    expected_users: str,
    expected_feature: str
):
    # 1. Create project
    create_res = client.post(
        "/api/v1/projects",
        json={
            "name": project_name,
            "description": description,
            "platform": "Web"
        }
    )
    assert create_res.status_code == 201
    project_data = create_res.json()
    project_id = project_data["id"]

    # 2. Run analysis
    analysis_res = client.post(f"/api/v1/projects/{project_id}/analyze")
    assert analysis_res.status_code == 200
    analysis = analysis_res.json()

    # 3. Assert correct domain extraction
    assert analysis["project_type"] == expected_type
    assert any(expected_users in u.lower() for u in analysis["users"])

    # 4. Assert non-empty requirements with confidence scores
    assert len(analysis["requirements"]) > 0
    for req in analysis["requirements"]:
        assert req["text"]
        assert req["category"] in ["functional", "non_functional", "technical", "business"]
        assert 0.0 <= req["confidence"] <= 1.0

    # 5. Assert features and normalized keys
    assert len(analysis["features"]) > 0
    feature_names = [f["name"].lower() for f in analysis["features"]]
    assert expected_feature in feature_names

    # 6. Assert tasks decomposition exists with estimated hours
    assert analysis["total_tasks_count"] > 0
    assert analysis["total_estimated_hours"] > 0
    for feat in analysis["features"]:
        assert len(feat["tasks"]) > 0
        for task in feat["tasks"]:
            assert task["title"]
            assert task["category"] in ["Frontend", "Backend", "Database", "QA", "Integration", "DevOps"]

    # 7. Assert missing info and assumptions
    assert len(analysis["missing_information"]) > 0
    assert len(analysis["assumptions"]) > 0
