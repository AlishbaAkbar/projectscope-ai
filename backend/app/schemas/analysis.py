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

class RiskResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    probability: str
    impact: str
    risk_level: str
    mitigation: str
    contingency: str
    owner: str
    score: float


class RiskSummaryResponse(BaseModel):
    total_risks: int
    risk_score: float
    risk_level: str
    summary: Dict[str, Any]
    risks_by_level: Dict[str, int]
    top_risks: List[RiskResponse]
    recommendations: List[str]

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
    timeline: Optional[TimelineResponse] = None  # ✅ NEW
    cost: Optional[Dict] = None  # ✅ NEW
    risks: Optional[RiskSummaryResponse] = None  # ✅ NEW
    hybrid_estimate: Optional[HybridEstimateResponse] = None  # ✅ NEW

class MilestoneResponse(BaseModel):
    name: str
    date: datetime
    description: str


class TimelineResponse(BaseModel):
    start_date: datetime
    end_date: datetime
    total_days: int
    total_working_days: int
    critical_path: List[str]
    milestones: List[MilestoneResponse]
    weekly_breakdown: Dict[str, float]
    parallelization_opportunities: List[Dict]
    bottlenecks: List[Dict]

class HybridEstimateResponse(BaseModel):
    final_estimate: float
    range: Dict[str, float]
    confidence: float
    reconciliation_method: str
    version: str
    timestamp: str
    breakdown: Dict[str, float]
    weights_used: Dict[str, float]