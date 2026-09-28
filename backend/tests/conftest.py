from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.api.dependencies import get_current_user
from app.core.security import create_access_token, hash_password
from app.database.session import Base, get_db
from app.main import app
from app.models import AuditLog, Feature, LLMRequest, Organization, Project, Role, Task, User


@pytest.fixture
def engine(tmp_path):
    database_path = tmp_path / "tests.sqlite"
    test_engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={"check_same_thread": False, "timeout": 30},
    )
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def db_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db(db_factory) -> Generator[Session, None, None]:
    session = db_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_factory):
    def override_get_db():
        session = db_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    app.dependency_overrides.clear()


@pytest.fixture
def organization(db):
    organization = Organization(name="Test Organization", slug="test-organization")
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


@pytest.fixture
def user(db, organization):
    user = User(
        email="user@example.com",
        password_hash=hash_password("Password123"),
        full_name="Test User",
        organization_id=organization.id,
        role="owner",
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def token(user):
    return create_access_token(user.id, user.organization_id, user.role)


@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def authenticated_client(client, user):
    async def override_current_user():
        return user

    app.dependency_overrides[get_current_user] = override_current_user
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def seed_roles(db):
    role_names = [
        "UI/UX Designer",
        "Frontend Developer",
        "Backend Developer",
        "Full-Stack Developer",
        "Mobile Developer",
        "QA Engineer",
        "DevOps Engineer",
        "Security Engineer",
        "Product Manager",
        "CEO/Business Owner",
    ]
    for role_id, name in enumerate(role_names, start=1):
        db.add(Role(id=role_id, name=name, hourly_rate=50))
    db.commit()
