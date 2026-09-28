import time

from app.models.project import Project


def test_querying_one_hundred_projects_is_responsive(db, organization):
    db.add_all([
        Project(
            organization_id=organization.id,
            name=f"Perf Project {index}",
            description="Performance test project",
        )
        for index in range(100)
    ])
    db.commit()

    started = time.perf_counter()
    projects = db.query(Project).filter(Project.organization_id == organization.id).all()
    elapsed = time.perf_counter() - started

    assert len(projects) == 100
    assert elapsed < 1.0
