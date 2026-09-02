from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.project import Project, Requirement
from app.models.feature import Feature
from app.models.task import Task
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_project(self, project_data: ProjectCreate) -> Project:
        project = Project(
            name=project_data.name,
            description=project_data.description,
            type=project_data.type,
            organization_id=project_data.organization_id,
            status="draft"
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_project(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_projects(self) -> List[Project]:
        return self.db.query(Project).all()
    
    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        project = self.get_project(project_id)
        if not project:
            return None
        
        update_data = project_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)
        
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def delete_project(self, project_id: int) -> bool:
        project = self.get_project(project_id)
        if not project:
            return False
        
        self.db.delete(project)
        self.db.commit()
        return True
    
    def add_requirement(self, project_id: int, text: str, category: str = "general") -> Requirement:
        requirement = Requirement(
            project_id=project_id,
            text=text,
            category=category,
            source="user_input"
        )
        self.db.add(requirement)
        self.db.commit()
        self.db.refresh(requirement)
        return requirement
    
    def get_requirements(self, project_id: int) -> List[Requirement]:
        return self.db.query(Requirement).filter(Requirement.project_id == project_id).all()
    
    def get_features(self, project_id: int) -> List[Feature]:
        return self.db.query(Feature).filter(Feature.project_id == project_id).all()
    
    def get_tasks(self, project_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()