from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    hourly_rate: float
    skill_metadata: Optional[dict] = {}


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RoleDetailResponse(RoleResponse):
    description: Optional[str] = ""
    skills: List[str] = []
    level: str = "Mid"


class RoleSummary(BaseModel):
    role_id: int
    name: str
    hourly_rate: float
    total_hours: float
    num_tasks: int
    estimated_cost: float