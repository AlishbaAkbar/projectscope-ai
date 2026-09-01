import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test environment variables before importing app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["AI_PROVIDER"] = "mock"
os.environ["APP_ENV"] = "testing"

from app.database.session import Base, get_db
from app.main import app
from app.ai.providers.mock_provider import MockLLMProvider
from app.ai.analyzer import RequirementAnalyzer
from app.services.project_service import ProjectService
from app.api.routes.projects import get_project_service

# Create test in-memory SQLite engine
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden DB and ProjectService dependencies"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    mock_analyzer = RequirementAnalyzer(provider=MockLLMProvider())
    test_service = ProjectService(analyzer=mock_analyzer)

    def override_get_project_service():
        return test_service

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_project_service] = override_get_project_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
