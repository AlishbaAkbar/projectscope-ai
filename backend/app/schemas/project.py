from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the software project")
    description: str = Field(..., min_length=5, description="Natural language description of project idea or requirements")
    platform: str = Field(default="Web", description="Target platform (Web, Mobile, Full-stack, API, etc.)")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=5)
    platform: Optional[str] = None
    project_type: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    project_type: Optional[str] = None
    target_users: List[str] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
