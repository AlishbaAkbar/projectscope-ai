from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field

TaskCategory = Literal["Frontend", "Backend", "Database", "QA", "Integration", "DevOps", "General"]


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Brief title of the task")
    description: str = Field(..., min_length=1, description="Detailed actionable task description")
    category: str = Field(default="Backend", description="Discipline/category of the task")
    estimated_hours: Optional[float] = Field(default=None, ge=0, description="Baseline estimated effort in hours")


class TaskCreate(TaskBase):
    feature_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    feature_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
