from app.models.project import Project


def test_project_crud_persists_through_api(authenticated_client, auth_headers, db, organization):
    response = authenticated_client.post(
        "/api/v1/projects",
        headers=auth_headers,
        json={
            "name": "Clinic Portal",
            "description": "A portal for clinics and patients",
            "type": "healthcare",
        },
    )
    assert response.status_code == 201, response.text
    project_id = response.json()["id"]

    stored = db.query(Project).filter(Project.id == project_id).one()
    assert stored.organization_id == organization.id
    assert stored.name == "Clinic Portal"

    fetched = authenticated_client.get(f"/api/v1/projects/{project_id}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["description"] == stored.description

    updated = authenticated_client.put(
        f"/api/v1/projects/{project_id}",
        headers=auth_headers,
        json={"name": "Clinic Portal v2"},
    )
    assert updated.status_code == 200
    db.expire_all()
    assert db.query(Project).filter(Project.id == project_id).one().name == "Clinic Portal v2"

    deleted = authenticated_client.delete(f"/api/v1/projects/{project_id}", headers=auth_headers)
    assert deleted.status_code == 204
    assert db.query(Project).filter(Project.id == project_id).first() is None


def test_tenant_cannot_read_another_organizations_project(
    authenticated_client,
    auth_headers,
    db,
):
    from app.models.project import Organization

    other_org = Organization(name="Other Org", slug="other-org")
    db.add(other_org)
    db.flush()
    project = Project(
        organization_id=other_org.id,
        name="Private project",
        description="A private project brief",
    )
    db.add(project)
    db.commit()

    response = authenticated_client.get(f"/api/v1/projects/{project.id}", headers=auth_headers)
    assert response.status_code == 404


def test_project_listing_is_tenant_scoped(authenticated_client, auth_headers, db, organization):
    from app.models.project import Organization

    db.add(Project(organization_id=organization.id, name="Mine", description="My project"))
    other_org = Organization(name="Different Org", slug="different-org")
    db.add(other_org)
    db.flush()
    db.add(Project(organization_id=other_org.id, name="Not mine", description="Other project"))
    db.commit()

    response = authenticated_client.get("/api/v1/projects", headers=auth_headers)
    assert response.status_code == 200
    assert [project["name"] for project in response.json()] == ["Mine"]
