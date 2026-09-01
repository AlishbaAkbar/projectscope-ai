from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field

RequirementCategory = Literal["functional", "non_functional", "technical", "business"]


class RequirementBase(BaseModel):
    category: str = Field(default="functional", description="Requirement category: functional, non_functional, technical, business")
    text: str = Field(..., min_length=1, description="Requirement statement")
    source: str = Field(default="llm_analysis", description="Source origin of requirement")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")


class RequirementCreate(RequirementBase):
    project_id: Optional[int] = None


class RequirementResponse(RequirementBase):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
