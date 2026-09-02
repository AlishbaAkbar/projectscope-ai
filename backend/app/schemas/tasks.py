from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_hours: float
    min_hours: Optional[float] = None
    max_hours: Optional[float] = None
    base_hours: Optional[float] = None
    complexity_factor: Optional[float] = 1.0
    priority: str = "MEDIUM"
    dependencies: List[str] = []
    confidence: float = 0.8
    is_global: bool = False

class TaskCreate(TaskBase):
    project_id: int
    feature_id: Optional[int] = None
    role_id: int

class TaskResponse(TaskBase):
    id: int
    project_id: int
    feature_id: Optional[int] = None
    role_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True