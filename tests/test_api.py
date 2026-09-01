import pytest
from fastapi.testclient import TestClient


def test_create_project_success(client: TestClient):
    payload = {
        "name": "Campus Ride Tracker",
        "description": "A bus tracking application for university students and drivers.",
        "platform": "Mobile"
    }
    response = client.post("/api/v1/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["platform"] == "Mobile"
    assert "id" in data
    assert "created_at" in data


def test_create_project_invalid_payload(client: TestClient):
    # Empty name
    response = client.post("/api/v1/projects", json={"name": "", "description": "Some description"})
    assert response.status_code == 422

    # Description too short
    response = client.post("/api/v1/projects", json={"name": "Test", "description": "abc"})
    assert response.status_code == 422


def test_list_and_get_project(client: TestClient):
    # Create two projects
    p1 = client.post("/api/v1/projects", json={"name": "P1", "description": "First project description"}).json()
    p2 = client.post("/api/v1/projects", json={"name": "P2", "description": "Second project description"}).json()

    # List
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 2

    # Get single
    response = client.get(f"/api/v1/projects/{p1['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == p1["id"]

    # Get non-existent
    response = client.get("/api/v1/projects/99999")
    assert response.status_code == 404
    assert response.json()["error"] is True


def test_analyze_project_e2e_flow(client: TestClient):
    # 1. Create project
    create_res = client.post(
        "/api/v1/projects",
        json={
            "name": "UniTransport",
            "description": "I want to build a university transport app where students can view buses, track their bus live, receive notifications and report transport issues.",
            "platform": "Web"
        }
    )
    assert create_res.status_code == 201
    project_id = create_res.json()["id"]

    # 2. Analyze project
    analyze_res = client.post(f"/api/v1/projects/{project_id}/analyze")
    assert analyze_res.status_code == 200
    data = analyze_res.json()

    # Verify structured analysis output
    assert data["project"]["id"] == project_id
    assert data["project_type"] == "transportation"
    assert "student" in data["users"]
    assert len(data["requirements"]) > 0
    assert len(data["features"]) > 0
    assert len(data["missing_information"]) > 0
    assert len(data["assumptions"]) > 0
    assert data["total_tasks_count"] > 0
    assert data["total_estimated_hours"] > 0

    # Verify features and nested tasks
    feature_names = [f["name"] for f in data["features"]]
    assert "authentication" in feature_names or "live_tracking" in feature_names

    # 3. Query features endpoint
    feat_res = client.get(f"/api/v1/projects/{project_id}/features")
    assert feat_res.status_code == 200
    features_list = feat_res.json()
    assert len(features_list) == len(data["features"])
    assert len(features_list[0]["tasks"]) > 0

    # 4. Query tasks endpoint
    tasks_res = client.get(f"/api/v1/projects/{project_id}/tasks")
    assert tasks_res.status_code == 200
    tasks_list = tasks_res.json()
    assert len(tasks_list) == data["total_tasks_count"]
