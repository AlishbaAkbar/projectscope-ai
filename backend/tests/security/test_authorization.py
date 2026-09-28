from app.models.project import Organization, Project


def test_user_cannot_access_other_tenant_project(
    authenticated_client,
    auth_headers,
    db,
):
    other = Organization(name="Confidential Tenant", slug="confidential-tenant")
    db.add(other)
    db.flush()
    project = Project(
        organization_id=other.id,
        name="Secret Project",
        description="Private project description",
    )
    db.add(project)
    db.commit()

    assert authenticated_client.get(
        f"/api/v1/projects/{project.id}",
        headers=auth_headers,
    ).status_code == 404
    assert authenticated_client.post(
        f"/api/v1/projects/{project.id}/analyze",
        headers=auth_headers,
    ).status_code == 404
    assert authenticated_client.put(
        f"/api/v1/projects/{project.id}",
        headers=auth_headers,
        json={"name": "Tampered project"},
    ).status_code == 404
