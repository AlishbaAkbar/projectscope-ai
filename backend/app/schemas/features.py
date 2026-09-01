from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.tasks import TaskResponse

PriorityLevel = Literal["low", "medium", "high", "critical"]
ComplexityLevel = Literal["low", "medium", "high"]


class FeatureBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, description="Feature identifier/name")
    description: str = Field(..., min_length=1, description="Functional summary of the feature")
    priority: str = Field(default="medium", description="Priority level: low, medium, high, critical")
    complexity: str = Field(default="medium", description="Complexity level: low, medium, high")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")


class FeatureCreate(FeatureBase):
    normalized_key: Optional[str] = None
    project_id: Optional[int] = None


class FeatureResponse(FeatureBase):
    id: int
    project_id: int
    normalized_key: str
    created_at: datetime
    tasks: List[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)
