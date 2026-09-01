from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.schemas.project import ProjectResponse
from app.schemas.requirements import RequirementResponse
from app.schemas.features import FeatureResponse
from app.schemas.tasks import TaskResponse


# --- Raw AI Validation Schemas ---

class RawRequirement(BaseModel):
    text: str = Field(..., min_length=3, description="Requirement statement")
    category: str = Field(default="functional", description="Requirement category: functional, non_functional, technical, business")
    confidence: float = Field(default=0.9, ge=0.0, le=1.0, description="Confidence level (0.0 to 1.0)")

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        if not isinstance(v, str):
            return "functional"
        v_clean = v.strip().lower().replace("-", "_").replace(" ", "_")
        if v_clean in ["functional", "non_functional", "nonfunctional", "technical", "business", "security", "performance"]:
            return "non_functional" if v_clean == "nonfunctional" else v_clean
        return "functional"


class RawFeature(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Name or identifier of the feature")
    description: str = Field(..., min_length=5, description="Clear description of feature capability")
    priority: str = Field(default="medium", description="Priority: low, medium, high, critical")
    complexity: str = Field(default="medium", description="Complexity: low, medium, high")
    confidence: float = Field(default=0.9, ge=0.0, le=1.0, description="Confidence level (0.0 to 1.0)")

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, v: str) -> str:
        if not isinstance(v, str):
            return "medium"
        v_clean = v.strip().lower()
        if v_clean in ["low", "medium", "high", "critical", "urgent"]:
            return "critical" if v_clean == "urgent" else v_clean
        return "medium"

    @field_validator("complexity", mode="before")
    @classmethod
    def normalize_complexity(cls, v: str) -> str:
        if not isinstance(v, str):
            return "medium"
        v_clean = v.strip().lower()
        if v_clean in ["low", "medium", "high", "very high", "complex", "simple"]:
            if v_clean in ["very high", "complex"]:
                return "high"
            if v_clean == "simple":
                return "low"
            return v_clean
        return "medium"


class RawAIAnalysisResponse(BaseModel):
    project_type: str = Field(..., min_length=2, description="Categorization or domain of the project")
    users: List[str] = Field(default_factory=list, description="Target user roles or personas")
    requirements: List[RawRequirement] = Field(default_factory=list, description="Extracted requirements")
    features: List[RawFeature] = Field(default_factory=list, description="Identified features")
    missing_information: List[str] = Field(default_factory=list, description="Ambiguities or unstated requirements")
    assumptions: List[str] = Field(default_factory=list, description="Working assumptions made for this project")


# --- Final Unified Analysis Result Schema ---

class ProjectAnalysisResult(BaseModel):
    project: ProjectResponse
    project_type: str
    users: List[str]
    requirements: List[RequirementResponse]
    features: List[FeatureResponse]
    missing_information: List[str]
    assumptions: List[str]
    total_tasks_count: int
    total_estimated_hours: float
