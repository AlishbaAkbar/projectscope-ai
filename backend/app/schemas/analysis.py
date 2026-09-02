from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.schemas.tasks import TaskResponse
from app.schemas.features import FeatureResponse
from app.schemas.project import ProjectResponse


class RawAIAnalysisResponse(BaseModel):
    project_type: str
    description: str
    features: List[Dict[str, Any]] = []
    users: List[str] = []
    technologies: List[str] = []
    integrations: List[str] = []
    estimated_complexity: str = "MEDIUM"
    confidence: float = 0.7


class AnalysisRequest(BaseModel):
    project_id: int
    description: str
    budget: Optional[float] = None
    target_platform: Optional[str] = None
    constraints: Optional[List[str]] = None


class AnalysisResponse(BaseModel):
    project_id: int
    status: str
    features: List[FeatureResponse] = []
    tasks: List[TaskResponse] = []
    estimated_hours: Optional[float] = None
    confidence: Optional[float] = None
    message: Optional[str] = None
    created_at: datetime


class ProjectAnalysisResult(BaseModel):
    project_id: int
    features: List[FeatureResponse]
    tasks: List[TaskResponse]
    roles: List[str]
    total_estimated_hours: float
    complexity_score: int
    risk_level: str
    summary: dict