import json
from pathlib import Path
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.roles import RoleCreate, RoleResponse


class RoleService:
    """Service for managing roles"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_role(self, role_id: int) -> Optional[Role]:
        """Get role by ID"""
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get role by name"""
        return self.db.query(Role).filter(Role.name == name).first()
    
    def get_all_roles(self) -> List[Role]:
        """Get all roles"""
        return self.db.query(Role).all()
    
    def get_role_details(self, role_id: int) -> Dict:
        """Get detailed role information"""
        role = self.get_role(role_id)
        if not role:
            return {}
        
        # Get skill metadata
        skill_metadata = role.skill_metadata or {}
        
        return {
            "id": role.id,
            "name": role.name,
            "hourly_rate": role.hourly_rate,
            "description": skill_metadata.get("description", ""),
            "skills": skill_metadata.get("skills", []),
            "level": skill_metadata.get("level", "Mid"),
            "created_at": role.created_at
        }
    
    def get_role_summary(self, role_ids: List[int]) -> Dict:
        """Get summary for multiple roles"""
        summary = {}
        for role_id in set(role_ids):
            details = self.get_role_details(role_id)
            if details:
                summary[str(role_id)] = details
        return summary
    
    def initialize_roles(self) -> int:
        """Initialize roles from predefined data"""
        # Check if roles already exist
        existing_count = self.db.query(Role).count()
        if existing_count > 0:
            return 0
        
        roles_data = [
            {"id": 1, "name": "UI/UX Designer", "hourly_rate": 45.0, 
             "skill_metadata": {"description": "Designs user interfaces and user experiences", 
                               "skills": ["Figma", "Adobe XD", "Sketch", "Prototyping"], 
                               "level": "Senior"}},
            {"id": 2, "name": "Frontend Developer", "hourly_rate": 50.0,
             "skill_metadata": {"description": "Builds user-facing web interfaces",
                               "skills": ["React", "Next.js", "TypeScript", "CSS", "HTML"],
                               "level": "Senior"}},
            {"id": 3, "name": "Backend Developer", "hourly_rate": 55.0,
             "skill_metadata": {"description": "Builds server-side logic and APIs",
                               "skills": ["Python", "FastAPI", "SQL", "Docker", "Redis"],
                               "level": "Senior"}},
            {"id": 4, "name": "Full-Stack Developer", "hourly_rate": 60.0,
             "skill_metadata": {"description": "Works on both frontend and backend",
                               "skills": ["React", "Python", "TypeScript", "SQL", "Docker"],
                               "level": "Senior"}},
            {"id": 5, "name": "Mobile Developer", "hourly_rate": 55.0,
             "skill_metadata": {"description": "Builds mobile applications",
                               "skills": ["React Native", "Flutter", "Swift", "Kotlin"],
                               "level": "Senior"}},
            {"id": 6, "name": "QA Engineer", "hourly_rate": 40.0,
             "skill_metadata": {"description": "Tests and ensures quality",
                               "skills": ["Selenium", "Jest", "Postman", "Test Automation"],
                               "level": "Mid"}},
            {"id": 7, "name": "DevOps Engineer", "hourly_rate": 60.0,
             "skill_metadata": {"description": "Manages infrastructure and deployment",
                               "skills": ["AWS", "Docker", "Kubernetes", "CI/CD"],
                               "level": "Senior"}},
            {"id": 8, "name": "Security Engineer", "hourly_rate": 65.0,
             "skill_metadata": {"description": "Ensures application security",
                               "skills": ["Penetration Testing", "OWASP", "Encryption", "Auth"],
                               "level": "Senior"}},
            {"id": 9, "name": "Product Manager", "hourly_rate": 50.0,
             "skill_metadata": {"description": "Manages product requirements and roadmap",
                               "skills": ["Agile", "Jira", "Requirements", "Strategy"],
                               "level": "Senior"}},
            {"id": 10, "name": "CEO/Business Owner", "hourly_rate": 75.0,
             "skill_metadata": {"description": "Strategic decision making and business management",
                               "skills": ["Strategy", "Leadership", "Business Planning"],
                               "level": "Executive"}},
        ]
        
        created_count = 0
        for role_data in roles_data:
            # Check if role exists
            existing = self.db.query(Role).filter(Role.id == role_data["id"]).first()
            if not existing:
                role = Role(
                    id=role_data["id"],
                    name=role_data["name"],
                    hourly_rate=role_data["hourly_rate"],
                    skill_metadata=role_data["skill_metadata"]
                )
                self.db.add(role)
                created_count += 1
        
        if created_count > 0:
            self.db.commit()
        
        return created_count
    
    def format_role_for_task(self, role_id: int) -> Dict:
        """Format role information for task display"""
        details = self.get_role_details(role_id)
        if not details:
            return {
                "id": role_id,
                "name": f"Role {role_id}",
                "hourly_rate": 50.0
            }
        return details
    
    def get_role_task_summary(self, task_summary: Dict) -> Dict:
        """Enrich task summary with role details"""
        enriched = {}
        for role_id, data in task_summary.items():
            role_details = self.get_role_details(int(role_id))
            if role_details:
                enriched[role_details["name"]] = {
                    "role_id": int(role_id),
                    "hourly_rate": role_details["hourly_rate"],
                    "total_hours": data["total_hours"],
                    "num_tasks": data["num_tasks"],
                    "estimated_cost": round(data["total_hours"] * role_details["hourly_rate"], 2)
                }
            else:
                enriched[f"Role {role_id}"] = {
                    "role_id": int(role_id),
                    "hourly_rate": 50.0,
                    "total_hours": data["total_hours"],
                    "num_tasks": data["num_tasks"],
                    "estimated_cost": round(data["total_hours"] * 50.0, 2)
                }
        return enriched