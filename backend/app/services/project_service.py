import logging
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.project import Project, Requirement, Feature, Task, MissingInformation, Assumption
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.requirements import RequirementResponse
from app.schemas.features import FeatureResponse
from app.schemas.tasks import TaskResponse
from app.schemas.analysis import ProjectAnalysisResult
from app.services.feature_service import FeatureService
from app.services.task_service import TaskService
from app.ai.analyzer import RequirementAnalyzer
from app.utils.error_handlers import EntityNotFoundException, InvalidInputException

logger = logging.getLogger(__name__)


class ProjectService:
    """Core domain service for managing projects and running requirement analysis"""

    def __init__(self, analyzer: Optional[RequirementAnalyzer] = None):
        self.analyzer = analyzer or RequirementAnalyzer()

    def create_project(self, db: Session, project_in: ProjectCreate) -> Project:
        """Create a new project record"""
        if not project_in.name or not project_in.name.strip():
            raise InvalidInputException("Project name is required.")
        if not project_in.description or len(project_in.description.strip()) < 5:
            raise InvalidInputException("Project description must be at least 5 characters long.")

        project = Project(
            name=project_in.name.strip(),
            description=project_in.description.strip(),
            platform=project_in.platform.strip() if project_in.platform else "Web",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        logger.info(f"Created project ID={project.id} ('{project.name}')")
        return project

    def get_project_by_id(self, db: Session, project_id: int) -> Project:
        """Retrieve project by ID or raise EntityNotFoundException"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise EntityNotFoundException("Project", project_id)
        return project

    def get_all_projects(self, db: Session, skip: int = 0, limit: int = 50) -> List[Project]:
        """List projects with pagination"""
        return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()

    def get_features_by_project_id(self, db: Session, project_id: int) -> List[Feature]:
        """Get all features (with nested tasks) for a given project"""
        self.get_project_by_id(db, project_id)  # Validate existence
        return (
            db.query(Feature)
            .filter(Feature.project_id == project_id)
            .options(joinedload(Feature.tasks))
            .all()
        )

    def get_tasks_by_project_id(self, db: Session, project_id: int) -> List[Task]:
        """Get all tasks across all features for a given project"""
        self.get_project_by_id(db, project_id)  # Validate existence
        return (
            db.query(Task)
            .join(Feature, Task.feature_id == Feature.id)
            .filter(Feature.project_id == project_id)
            .all()
        )

    async def analyze_project(self, db: Session, project_id: int) -> ProjectAnalysisResult:
        """
        Execute requirement analysis pipeline for a project:
        1. Fetch project from DB
        2. Run AI Requirement Analyzer (LLM + Pydantic validation + retry)
        3. Clear old analysis artifacts if re-analyzing
        4. Normalize features via FeatureService
        5. Generate baseline engineering tasks via TaskService
        6. Persist structured output atomically in DB
        7. Return unified ProjectAnalysisResult
        """
        project = self.get_project_by_id(db, project_id)

        # Run AI requirement analyzer
        raw_analysis = await self.analyzer.analyze(
            project_name=project.name,
            description=project.description,
            platform=project.platform
        )

        try:
            # Clear previous analysis data if this project is being re-analyzed
            db.query(Requirement).filter(Requirement.project_id == project.id).delete()
            db.query(MissingInformation).filter(MissingInformation.project_id == project.id).delete()
            db.query(Assumption).filter(Assumption.project_id == project.id).delete()

            # Deleting features will cascade delete their tasks due to relationship cascade
            features_to_delete = db.query(Feature).filter(Feature.project_id == project.id).all()
            for f in features_to_delete:
                db.delete(f)
            db.flush()

            # Update project metadata
            project.project_type = raw_analysis.project_type
            project.target_users = raw_analysis.users
            db.add(project)

            # Store Requirements
            created_requirements = []
            for req in raw_analysis.requirements:
                db_req = Requirement(
                    project_id=project.id,
                    category=req.category,
                    text=req.text,
                    source="llm_analysis",
                    confidence=req.confidence,
                )
                db.add(db_req)
                created_requirements.append(db_req)

            # Store Missing Information
            created_missing_info = []
            for item in raw_analysis.missing_information:
                db_item = MissingInformation(
                    project_id=project.id,
                    question_or_detail=item
                )
                db.add(db_item)
                created_missing_info.append(item)

            # Store Assumptions
            created_assumptions = []
            for item in raw_analysis.assumptions:
                db_item = Assumption(
                    project_id=project.id,
                    assumption_text=item
                )
                db.add(db_item)
                created_assumptions.append(item)

            # Store Features & Generate Tasks
            created_features = []
            total_tasks_count = 0
            total_estimated_hours = 0.0

            for feat in raw_analysis.features:
                normalized_key = FeatureService.normalize_name(feat.name)
                db_feat = Feature(
                    project_id=project.id,
                    name=feat.name,
                    normalized_key=normalized_key,
                    description=feat.description,
                    priority=feat.priority,
                    complexity=feat.complexity,
                    confidence=feat.confidence,
                )
                db.add(db_feat)
                db.flush()  # Flush to populate db_feat.id

                # Generate deterministic baseline tasks
                baseline_tasks = TaskService.generate_tasks_for_feature(
                    normalized_key=normalized_key,
                    feature_name=feat.name,
                    description=feat.description,
                )

                feature_tasks = []
                for task_base in baseline_tasks:
                    db_task = Task(
                        feature_id=db_feat.id,
                        title=task_base.title,
                        description=task_base.description,
                        category=task_base.category,
                        estimated_hours=task_base.estimated_hours,
                    )
                    db.add(db_task)
                    feature_tasks.append(db_task)
                    total_tasks_count += 1
                    if task_base.estimated_hours:
                        total_estimated_hours += task_base.estimated_hours

                created_features.append(db_feat)

            db.commit()
            db.refresh(project)

            # Build full response schemas
            features_response = []
            for f in created_features:
                db.refresh(f)
                tasks_response = [
                    TaskResponse.model_validate(t) for t in f.tasks
                ]
                f_resp = FeatureResponse(
                    id=f.id,
                    project_id=f.project_id,
                    name=f.name,
                    normalized_key=f.normalized_key,
                    description=f.description,
                    priority=f.priority,
                    complexity=f.complexity,
                    confidence=f.confidence,
                    created_at=f.created_at,
                    tasks=tasks_response,
                )
                features_response.append(f_resp)

            requirements_response = [
                RequirementResponse.model_validate(r) for r in created_requirements
            ]

            return ProjectAnalysisResult(
                project=ProjectResponse.model_validate(project),
                project_type=project.project_type or "general",
                users=project.target_users,
                requirements=requirements_response,
                features=features_response,
                missing_information=created_missing_info,
                assumptions=created_assumptions,
                total_tasks_count=total_tasks_count,
                total_estimated_hours=total_estimated_hours,
            )

        except Exception as e:
            db.rollback()
            logger.exception(f"Failed to persist project analysis for project ID={project.id}: {e}")
            raise
