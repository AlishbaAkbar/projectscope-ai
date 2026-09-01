from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.schemas.features import FeatureResponse
from app.schemas.tasks import TaskResponse
from app.schemas.analysis import ProjectAnalysisResult
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


def get_project_service() -> ProjectService:
    return ProjectService()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project with a name, description, and platform.
    """
    project = service.create_project(db=db, project_in=project_in)
    return project


@router.get("", response_model=List[ProjectResponse])
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    """
    List all created projects with pagination.
    """
    projects = service.get_all_projects(db=db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    """
    Get project details by ID.
    """
    project = service.get_project_by_id(db=db, project_id=project_id)
    return project


@router.post("/{project_id}/analyze", response_model=ProjectAnalysisResult)
async def analyze_project(
    project_id: int,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    """
    Execute AI requirement analysis on a project:
    1. Sends project description to LLM Requirement Analyzer.
    2. Validates structured JSON using Pydantic.
    3. Normalizes features to canonical domain keys.
    4. Generates baseline engineering development tasks.
    5. Stores requirements, features, and tasks in database.
    6. Returns complete structured analysis result.
    """
    result = await service.analyze_project(db=db, project_id=project_id)
    return result


@router.get("/{project_id}/features", response_model=List[FeatureResponse])
def get_project_features(
    project_id: int,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    """
    Get all features (with nested tasks) for a project.
    """
    features = service.get_features_by_project_id(db=db, project_id=project_id)
    return features


@router.get("/{project_id}/tasks", response_model=List[TaskResponse])
def get_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    service: ProjectService = Depends(get_project_service)
):
    """
    Get all development tasks for a project.
    """
    tasks = service.get_tasks_by_project_id(db=db, project_id=project_id)
    return tasks
