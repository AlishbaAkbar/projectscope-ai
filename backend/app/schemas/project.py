from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    organization_id: Optional[int] = 1  # ✅ Made optional with default


class ProjectCreate(ProjectBase):
    platform: Optional[str] = "Web"  # ✅ Added for frontend
    industry: Optional[str] = None  # ✅ Added for frontend
    budget: Optional[float] = None  # ✅ Added for frontend
    timeline: Optional[str] = None  # ✅ Added for frontend
    target_users: Optional[list] = []  # ✅ Added for frontend
    constraints: Optional[list] = []  # ✅ Added for frontend


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    platform: Optional[str] = None
    industry: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    status: str
    platform: Optional[str] = "Web"
    industry: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    target_users: Optional[list] = []
    constraints: Optional[list] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
