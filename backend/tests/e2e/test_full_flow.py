from app.ai.providers.mock_provider import MockLLMProvider
from app.reports.report_service import ReportService
import app.api.routes.projects as projects_route


def test_register_login_create_analyze_report_and_delete(
    client,
    monkeypatch,
    seed_roles,
    tmp_path,
):
    monkeypatch.setattr(projects_route, "get_provider", MockLLMProvider)

    registered = client.post(
        "/api/v1/auth/register",
        json={
            "email": "e2e@example.com",
            "password": "Password123",
            "full_name": "E2E User",
            "organization_name": "E2E Organization",
        },
    )
    assert registered.status_code == 201, registered.text

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "e2e@example.com", "password": "Password123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    created = client.post(
        "/api/v1/projects",
        headers=headers,
        json={
            "name": "Clinic Appointment App",
            "type": "healthcare",
            "description": "Patients book appointments with doctors at a clinic.",
        },
    )
    assert created.status_code == 201, created.text
    project_id = created.json()["id"]

    analysis = client.post(f"/api/v1/projects/{project_id}/analyze", headers=headers)
    assert analysis.status_code == 200, analysis.text

    features = client.get(f"/api/v1/projects/{project_id}/features")
    tasks = client.get(f"/api/v1/projects/{project_id}/tasks")
    assert features.status_code == 200 and features.json()
    assert tasks.status_code == 200 and tasks.json()
    assert all(task["estimated_hours"] > 0 and task["role_id"] for task in tasks.json())

    def generate_pdf(service, report_project_id, report_analysis):
        report_path = tmp_path / "project-report.pdf"
        report_path.write_bytes(b"%PDF-1.4 test report")
        return str(report_path)

    monkeypatch.setattr(ReportService, "generate_pdf", generate_pdf)
    report = client.get(f"/api/v1/projects/{project_id}/report/pdf", headers=headers)
    assert report.status_code == 200, report.text
    assert report.headers["content-type"].startswith("application/pdf")
    assert report.content.startswith(b"%PDF")

    deleted = client.delete(f"/api/v1/projects/{project_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/projects/{project_id}", headers=headers).status_code == 404
