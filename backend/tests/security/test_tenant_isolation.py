from app.models.project import Organization, Project


def test_project_create_cannot_select_another_tenant(
    authenticated_client,
    auth_headers,
    db,
    organization,
):
    other = Organization(name="Another Tenant", slug="another-tenant")
    db.add(other)
    db.commit()

    response = authenticated_client.post(
        "/api/v1/projects",
        headers=auth_headers,
        json={
            "name": "Tenant Safe Project",
            "description": "A project owned by the authenticated organization.",
            "organization_id": other.id,
        },
    )
    assert response.status_code == 201, response.text
    project = db.query(Project).filter(Project.id == response.json()["id"]).one()
    assert project.organization_id == organization.id
