from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from app.schemas.tasks import TaskResponse
from app.schemas.features import FeatureResponse
from app.schemas.project import ProjectResponse


class AIRequirement(BaseModel):
    text: str = Field(min_length=1)
    category: str = "functional"
    confidence: float = Field(default=0.8, ge=0, le=1)


class AIFeature(BaseModel):
    name: Optional[str] = None
    canonical_name: Optional[str] = None
    description: str = ""
    priority: str = "MEDIUM"
    complexity: Union[int, str] = 3
    confidence: float = Field(default=0.8, ge=0, le=1)

    @model_validator(mode="after")
    def require_name(self):
        if not (self.canonical_name or self.name):
            raise ValueError("Feature must include a name or canonical_name")
        return self


class RawAIAnalysisResponse(BaseModel):
    project_type: str
    description: str = ""
    requirements: List[AIRequirement] = Field(min_length=1)
    features: List[AIFeature] = Field(min_length=1)
    users: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    integrations: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
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
    features: List[FeatureResponse] = []
    tasks: List[TaskResponse] = []
    roles: List[str] = []
    total_estimated_hours: float = 0
    complexity_score: float = 0
    risk_level: str = "LOW"
    summary: Dict[str, Any] = {}
    timeline: Optional[Dict[str, Any]] = None
    cost: Optional[Dict[str, Any]] = None
    risks: Optional[Dict[str, Any]] = None
    hybrid_estimate: Optional[Dict[str, Any]] = None
    explanation: Optional[ExplanationResponse] = None

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


class ExplanationResponse(BaseModel):
    summary: str
    explanations: Dict[str, str]
    detailed_explanations: List[Dict[str, Any]]
    assumptions: List[str]
    limitations: List[str]
    knowledge_used: Optional[List[Dict[str, Any]]] = []


class ChatMessageRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []


class ChatMessageResponse(BaseModel):
    reply: str
    citations: Optional[List[Dict[str, Any]]] = []
    suggested_actions: Optional[List[str]] = []


class FeedbackRequest(BaseModel):
    rating: int
    category: Optional[str] = "general"
    comments: Optional[str] = None
    tags: Optional[List[str]] = []


class FeedbackResponse(BaseModel):
    status: str
    message: str
    recorded_at: datetime


class TechRecommendationItem(BaseModel):
    name: str
    category: str
    role: str
    rationale: str
    pros: List[str] = []
    alternatives: List[str] = []


class TechStackResponse(BaseModel):
    project_id: int
    platform: str
    recommendations: List[TechRecommendationItem]
    architectural_notes: List[str] = []