from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.tasks import TaskResponse

class FeatureBase(BaseModel):
    canonical_name: str
    description: Optional[str] = None
    priority: str = "MEDIUM"
    complexity: int = 3
    confidence: float = 0.8
    dependencies: List[str] = []

class FeatureCreate(FeatureBase):
    project_id: int
    source_requirement_ids: List[int] = []

class FeatureResponse(FeatureBase):
    id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class FeatureWithTasks(FeatureResponse):
    tasks: List[TaskResponse] = []