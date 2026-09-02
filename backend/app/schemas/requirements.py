from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequirementBase(BaseModel):
    text: str
    category: Optional[str] = "general"
    confidence: Optional[float] = 0.8

class RequirementCreate(RequirementBase):
    project_id: int
    source: Optional[str] = "user_input"

class RequirementResponse(RequirementBase):
    id: int
    project_id: int
    source: str
    created_at: datetime
    
    class Config:
        from_attributes = True