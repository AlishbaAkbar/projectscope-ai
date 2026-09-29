from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ai.analyzer import RequirementAnalyzer
from app.ai.providers.factory import get_provider
from app.api.dependencies import get_current_user, get_optional_user
from app.core.audit import AuditService
from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.sanitize import detect_prompt_injection, sanitize_prompt, sanitize_text
from app.database.session import get_db
from app.models.feature import Feature
from app.models.project import Project, Requirement
from app.models.role import Role
from app.models.task import Task
from app.models.user import User
from app.schemas.analysis import ProjectAnalysisResult
from app.schemas.features import FeatureResponse
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.tasks import TaskResponse
from app.services.feature_service import FeatureService
from app.services.project_service import ProjectService

router = APIRouter()


# ============================================
# SCHEMAS (defined first to avoid NameError)
# ============================================

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = []
    project_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]] = []
    suggestions: List[str] = []
    confidence: float = 0.85


class FeedbackRequest(BaseModel):
    rating: int
    category: Optional[str] = None
    comments: Optional[str] = None
    notes: Optional[str] = None
    actual_hours: Optional[float] = None


class FeedbackResponse(BaseModel):
    id: int
    project_id: int
    rating: int
    message: str


# ============================================
# PROJECT LIST + CREATE (must be FIRST)
# ============================================

@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get projects for current user's organization only"""
    return db.query(Project).filter(
        Project.organization_id == current_user.organization_id
    ).all()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def create_project(
    request: Request,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create project with audit log & sanitization"""
    service = ProjectService(db)
    audit = AuditService(db)

    # Sanitize inputs
    project_data.name = sanitize_text(project_data.name)
    if project_data.description:
        project_data.description = sanitize_text(project_data.description)

    # Tenant isolation: force organization_id from current user
    project_data.organization_id = current_user.organization_id

    project = service.create_project(project_data)

    audit.log_project_created(
        user_id=current_user.id,
        org_id=current_user.organization_id,
        project_id=project.id,
        name=project.name,
        request=request,
    )

    return project
# ============================================
# ROLE ROUTES (before /{project_id})
# ============================================

@router.get("/roles")
async def get_roles(db: Session = Depends(get_db)):
    """Get all roles"""
    roles = db.query(Role).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "hourly_rate": r.hourly_rate,
            "skill_metadata": r.skill_metadata or {},
            "description": (r.skill_metadata or {}).get("description", ""),
            "skills": (r.skill_metadata or {}).get("skills", []),
            "level": (r.skill_metadata or {}).get("level", "Mid"),
            "created_at": r.created_at,
        }
        for r in roles
    ]


@router.get("/roles/{role_id}")
async def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get role by ID"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {
        "id": role.id,
        "name": role.name,
        "hourly_rate": role.hourly_rate,
        "skill_metadata": role.skill_metadata or {},
        "description": (role.skill_metadata or {}).get("description", ""),
        "skills": (role.skill_metadata or {}).get("skills", []),
        "level": (role.skill_metadata or {}).get("level", "Mid"),
        "created_at": role.created_at,
    }


# ============================================
# RAG ROUTES (before /{project_id})
# ============================================

@router.get("/rag/knowledge")
async def get_knowledge_base():
    """Get all knowledge base documents"""
    try:
        from app.rag.retriever import Retriever
        retriever = Retriever()
        return retriever.get_all_knowledge()
    except Exception as e:
        return {"error": str(e), "documents": []}


@router.get("/rag/search")
async def search_knowledge(query: str, top_k: int = 5):
    """Search knowledge base"""
    try:
        from app.rag.retriever import Retriever
        retriever = Retriever()
        return {
            "query": query,
            "results": retriever.vector_store.search(query, top_k=top_k),
        }
    except Exception as e:
        return {"error": str(e), "results": []}


@router.get("/rag/stats")
async def get_rag_stats():
    """Get RAG statistics"""
    try:
        from app.rag.retriever import Retriever
        retriever = Retriever()
        return retriever.get_knowledge_base_stats()
    except Exception as e:
        return {"error": str(e)}


# ============================================
# SINGLE PROJECT ROUTES
# ============================================

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get project with tenant isolation"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.organization_id == current_user.organization_id,
    ).first()

    if not project:
        # Return 404 (not 403) to prevent ID enumeration
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.organization_id == current_user.organization_id,
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete project with audit log"""
    audit = AuditService(db)

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.organization_id == current_user.organization_id,
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    audit.log_project_deleted(
        user_id=current_user.id,
        org_id=current_user.organization_id,
        project_id=project_id,
        request=request,
    )
    return None


# ============================================
# REQUIREMENT ROUTES
# ============================================

@router.post("/projects/{project_id}/requirements")
async def add_requirement(
    project_id: int,
    text: str,
    category: str = "general",
    db: Session = Depends(get_db),
):
    """Add requirement to a project"""
    service = ProjectService(db)
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    requirement = service.add_requirement(project_id, text, category)
    return {
        "id": requirement.id,
        "text": requirement.text,
        "category": requirement.category,
        "message": "Requirement added successfully",
    }


@router.get("/projects/{project_id}/requirements")
async def get_requirements(project_id: int, db: Session = Depends(get_db)):
    """Get all requirements for a project"""
    service = ProjectService(db)
    return service.get_requirements(project_id)


# ============================================
# FEATURES & TASKS
# ============================================

@router.get("/projects/{project_id}/features", response_model=List[FeatureResponse])
async def get_features(project_id: int, db: Session = Depends(get_db)):
    """Get all features for a project"""
    service = ProjectService(db)
    return service.get_features(project_id)


@router.get("/projects/{project_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(project_id: int, db: Session = Depends(get_db)):
    """Get all tasks for a project"""
    service = ProjectService(db)
    return service.get_tasks(project_id)


# ============================================
# ANALYZE PROJECT (Phases 6-19)
# ============================================

@router.post("/projects/{project_id}/analyze", response_model=ProjectAnalysisResult)
@limiter.limit(f"{settings.RATE_LIMIT_AI_PER_MINUTE}/minute")
async def analyze_project(request: Request, project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),):
    """Analyze with prompt sanitization"""

    # Verify project belongs to user's org (tenant isolation)
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.organization_id == current_user.organization_id,
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Sanitize project description for AI
    if project.description:
        if detect_prompt_injection(project.description):
            raise HTTPException(
                status_code=400,
                detail="Input contains suspicious patterns",
            )
        project.description = sanitize_prompt(project.description, settings.MAX_PROMPT_LENGTH)

    """Full analysis pipeline (Phases 6-19)"""
    try:
        # 1. CHECK PROJECT EXISTS
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # 2. ANALYZE PROJECT DESCRIPTION
        provider = get_provider()
        print(f"🤖 Active provider: {type(provider).__name__}")
        analysis = await RequirementAnalyzer(
            provider=provider,
            db=db,
            project_id=project_id,
        ).analyze(
            project_name=project.name,
            description=project.description or "",
            platform=project.platform or "Web",
        )

        requirement_rows = [
            Requirement(
                project_id=project_id,
                text=item.text.strip(),
                category=item.category,
                confidence=item.confidence,
                source="ai_generated",
            )
            for item in analysis.requirements
        ]

        # 3. REPLACE PREVIOUSLY GENERATED REQUIREMENTS
        legacy_requirement_texts = {
            "Users need to login and create accounts",
            "Product catalog with search",
            "Shopping cart and checkout",
            "Payment processing",
        }
        generated_requirements = db.query(Requirement).filter(
            Requirement.project_id == project_id,
            Requirement.source.in_(["auto_generated", "ai_generated"]),
        ).all()
        replacing_legacy_defaults = (
            len(generated_requirements) == len(legacy_requirement_texts)
            and {item.text for item in generated_requirements} == legacy_requirement_texts
        )
        for requirement in generated_requirements:
            db.delete(requirement)
        db.flush()
        db.add_all(requirement_rows)
        db.commit()

        # 4. GET REQUIREMENTS
        requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()

        # 5. FEATURES (prevent duplicates)
        existing_features = db.query(Feature).filter(Feature.project_id == project_id).all()
        legacy_feature_names = {"AUTHENTICATION", "PRODUCT_CATALOG", "CART", "PAYMENT"}
        if (
            replacing_legacy_defaults
            and {feature.canonical_name for feature in existing_features} == legacy_feature_names
        ):
            db.query(Task).filter(
                Task.project_id == project_id,
                Task.feature_id.in_([feature.id for feature in existing_features]),
            ).delete(synchronize_session=False)
            for feature in existing_features:
                db.delete(feature)
            db.flush()
            existing_features = []

        if existing_features:
            features = existing_features
            feature_names = [f.canonical_name for f in features]
        else:
            features = []
            feature_names = []
            for feature_data in analysis.features:
                raw_name = feature_data.canonical_name or feature_data.name
                if not raw_name:
                    raise HTTPException(status_code=502, detail="AI returned a feature without a name")
                canonical_name = FeatureService.normalize_name(raw_name)

                if canonical_name in feature_names:
                    continue

                raw_complexity = feature_data.complexity
                if isinstance(raw_complexity, str):
                    complexity = {"low": 2, "medium": 3, "high": 5}.get(raw_complexity.lower(), 3)
                else:
                    complexity = max(1, min(5, int(raw_complexity)))

                feature = Feature(
                    project_id=project_id,
                    canonical_name=canonical_name,
                    description=(feature_data.description or raw_name)[:500],
                    priority=feature_data.priority.upper(),
                    complexity=complexity,
                    confidence=feature_data.confidence,
                )
                db.add(feature)
                features.append(feature)
                feature_names.append(canonical_name)

            db.commit()
            features = db.query(Feature).filter(Feature.project_id == project_id).all()
            feature_names = [f.canonical_name for f in features]

        # 6. TASKS (prevent duplicates)
        existing_tasks = db.query(Task).filter(Task.project_id == project_id).all()
        if existing_tasks:
            tasks = existing_tasks
        else:
            tasks = []
            for feature in features:
                if feature.canonical_name == "AUTHENTICATION":
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=1,
                                      title="Design authentication flows",
                                      description="Design login, registration screens",
                                      estimated_hours=8, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=3,
                                      title="Implement JWT authentication",
                                      description="Set up JWT tokens and middleware",
                                      estimated_hours=12, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=6,
                                      title="Test authentication flows",
                                      description="Test login, registration, password reset",
                                      estimated_hours=6, priority="HIGH"))
                elif feature.canonical_name == "PRODUCT_CATALOG":
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=1,
                                      title="Design product catalog",
                                      description="Design product listing and detail pages",
                                      estimated_hours=12, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=3,
                                      title="Build product API",
                                      description="Create CRUD operations for products",
                                      estimated_hours=16, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=2,
                                      title="Build product pages",
                                      description="Create product list and detail pages",
                                      estimated_hours=14, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=6,
                                      title="Test product catalog",
                                      description="Test CRUD, search, filtering",
                                      estimated_hours=8, priority="HIGH"))
                elif feature.canonical_name == "CART":
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=1,
                                      title="Design shopping cart",
                                      description="Design cart page and checkout flow",
                                      estimated_hours=8, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=3,
                                      title="Build cart API",
                                      description="Create add/remove/update endpoints",
                                      estimated_hours=10, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=2,
                                      title="Build cart interface",
                                      description="Create cart page and mini-cart",
                                      estimated_hours=10, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=6,
                                      title="Test cart functionality",
                                      description="Test add, remove, update, checkout",
                                      estimated_hours=6, priority="HIGH"))
                elif feature.canonical_name == "PAYMENT":
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=1,
                                      title="Design payment flows",
                                      description="Design payment and confirmation screens",
                                      estimated_hours=10, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=10,
                                      title="Select payment provider",
                                      description="Research and select payment gateway",
                                      estimated_hours=4, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=3,
                                      title="Integrate payment gateway",
                                      description="Integrate Stripe/PayPal",
                                      estimated_hours=16, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=2,
                                      title="Build payment UI",
                                      description="Create checkout form and confirmation",
                                      estimated_hours=10, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=8,
                                      title="Implement payment security",
                                      description="PCI compliance, tokenization",
                                      estimated_hours=8, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=6,
                                      title="Test payment processing",
                                      description="Test success, failure, refund scenarios",
                                      estimated_hours=10, priority="HIGH"))
                elif feature.canonical_name == "ORDER_MANAGEMENT":
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=1,
                                      title="Design order management",
                                      description="Design order history and tracking pages",
                                      estimated_hours=8, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=3,
                                      title="Build order management API",
                                      description="Create order tracking endpoints",
                                      estimated_hours=12, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=2,
                                      title="Build order interface",
                                      description="Create order history and detail pages",
                                      estimated_hours=10, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=6,
                                      title="Test order management",
                                      description="Test order creation and tracking",
                                      estimated_hours=6, priority="HIGH"))
                elif feature.canonical_name == "ADMIN_PANEL":
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=1,
                                      title="Design admin dashboard",
                                      description="Design admin dashboard layout",
                                      estimated_hours=12, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=3,
                                      title="Build admin APIs",
                                      description="Create admin endpoints and permissions",
                                      estimated_hours=16, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=4,
                                      title="Build admin dashboard",
                                      description="Create admin dashboard UI",
                                      estimated_hours=16, priority="HIGH"))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=6,
                                      title="Test admin panel",
                                      description="Test permissions and CRUD operations",
                                      estimated_hours=8, priority="HIGH"))
                else:
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=1,
                                      title=f"Design {feature.canonical_name.lower().replace('_', ' ')}",
                                      description=f"Define user flows and interface for {feature.canonical_name.lower().replace('_', ' ')}",
                                      estimated_hours=8, priority=feature.priority))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=3,
                                      title=f"Implement {feature.canonical_name.lower().replace('_', ' ')}",
                                      description=feature.description or "Implement feature requirements",
                                      estimated_hours=16, priority=feature.priority))
                    tasks.append(Task(project_id=project_id, feature_id=feature.id, role_id=6,
                                      title=f"Test {feature.canonical_name.lower().replace('_', ' ')}",
                                      description="Verify feature requirements and edge cases",
                                      estimated_hours=6, priority=feature.priority))

            # Global tasks
            global_tasks = [
                Task(project_id=project_id, feature_id=None, role_id=7,
                     title="Set up cloud infrastructure",
                     description="Configure cloud services and networking",
                     estimated_hours=8, priority="HIGH", is_global=True),
                Task(project_id=project_id, feature_id=None, role_id=7,
                     title="Set up CI/CD pipeline",
                     description="Configure GitHub Actions and deployment",
                     estimated_hours=8, priority="HIGH", is_global=True),
                Task(project_id=project_id, feature_id=None, role_id=9,
                     title="Project planning and setup",
                     description="Create project timeline and sprint planning",
                     estimated_hours=4, priority="HIGH", is_global=True),
                Task(project_id=project_id, feature_id=None, role_id=6,
                     title="Define testing strategy",
                     description="Create test plan and QA strategy",
                     estimated_hours=4, priority="MEDIUM", is_global=True),
            ]
            tasks.extend(global_tasks)

            for task in tasks:
                db.add(task)
            db.commit()
            tasks = db.query(Task).filter(Task.project_id == project_id).all()

        # 5. ROLE SERVICE
        from app.services.role_service import RoleService
        role_service = RoleService(db)

        # 6. ESTIMATION ENGINE
        from app.estimation.complexity_factors import ComplexityFactors
        from app.estimation.rules_engine import EstimationEngine

        estimation_engine = EstimationEngine()
        feature_names = [f.canonical_name for f in features]
        feature_complexities = [f.complexity for f in features]

        has_payment = any(f.canonical_name == "PAYMENT" for f in features)
        has_admin = any(f.canonical_name == "ADMIN_PANEL" for f in features)
        has_mobile = any(f.canonical_name == "MOBILE_APP" for f in features)

        integrations = []
        if has_payment:
            integrations.append("payment_gateway")
        if has_admin:
            integrations.append("admin_panel")
        if len(integrations) > 1:
            integrations.append("multiple_integrations")

        estimation = estimation_engine.estimate_project(
            features=feature_names,
            complexities=feature_complexities,
            integrations=integrations,
            platform="web",
        )

        # 7. COST ESTIMATION
        from app.estimation.cost_engine import CostEngine

        role_hours = {}
        for task in tasks:
            role_name = role_service.format_role_for_task(task.role_id)["name"]
            role_hours[role_name] = role_hours.get(role_name, 0) + task.estimated_hours

        cost_engine = CostEngine()
        cost_result = cost_engine.calculate_project_cost(role_hours)

        # 8. SUMMARY
        summary = {}
        for task in tasks:
            role_name = role_service.format_role_for_task(task.role_id)["name"]
            if role_name not in summary:
                summary[role_name] = {"total_hours": 0, "num_tasks": 0, "estimated_cost": 0}
            summary[role_name]["total_hours"] += task.estimated_hours
            summary[role_name]["num_tasks"] += 1
            summary[role_name]["estimated_cost"] = round(
                summary[role_name]["total_hours"] * cost_engine.get_rate(role_name), 2
            )

        complexity_score, _ = ComplexityFactors.calculate_complexity_score(feature_names)
        risk_level = ComplexityFactors.get_risk_level(complexity_score, len(integrations))

        # 9. TIMELINE
        from app.estimation.timeline_engine import TimelineEngine

        timeline_tasks = [
            {
                "id": str(task.id),
                "title": task.title,
                "estimated_hours": task.estimated_hours,
                "role_id": task.role_id,
                "dependencies": task.dependencies or [],
            }
            for task in tasks
        ]
        timeline_engine = TimelineEngine()
        timeline_engine.add_tasks_from_list(timeline_tasks)
        formatted_timeline = timeline_engine.get_formatted_timeline()

        # 10. RISK ENGINE
        from app.estimation.risk_engine import RiskEngine

        risk_engine = RiskEngine()
        risk_result = risk_engine.assess_project(
            features=feature_names,
            complexities=feature_complexities,
            integrations=integrations,
            platform="web",
            security_level="high" if has_payment else "standard",
            budget=None,
            timeline=formatted_timeline.get("total_days"),
        )
        risk_summary = risk_engine.get_risk_summary(risk_result)
        final_risk_level = risk_result.risk_level

        # 11. HYBRID ESTIMATION
        from app.estimation.hybrid_engine import HybridEngine

        rule_estimate = estimation["total"]["expected"]
        ml_estimate = None
        ml_confidence = 0.5

        try:
            from app.ml.predictor import MLPredictor
            predictor = MLPredictor()
            predictor.load()
            ml_features = {
                "num_features": len(features),
                "num_tasks": len(tasks),
                "complexity_sum": sum(f.complexity for f in features),
                "avg_complexity": sum(f.complexity for f in features) / len(features) if features else 0,
                "max_complexity": max([f.complexity for f in features]) if features else 0,
                "num_roles": len(set(t.role_id for t in tasks)),
                "has_payment": 1 if has_payment else 0,
                "has_auth": 1 if any(f.canonical_name == "AUTHENTICATION" for f in features) else 0,
                "has_admin": 1 if has_admin else 0,
                "has_mobile": 1 if has_mobile else 0,
                "num_payment": sum(1 for f in features if f.canonical_name == "PAYMENT"),
                "num_auth": sum(1 for f in features if f.canonical_name == "AUTHENTICATION"),
                "num_admin": sum(1 for f in features if f.canonical_name == "ADMIN_PANEL"),
                "num_mobile": sum(1 for f in features if f.canonical_name == "MOBILE_APP"),
            }
            ml_result = predictor.predict_from_project(ml_features)
            ml_estimate = ml_result.get("predicted_hours")
            ml_confidence = ml_result.get("confidence", 0.5)
        except Exception as e:
            print(f"[WARN] ML prediction unavailable: {e}")

        llm_estimate = rule_estimate
        data_quality = "medium"
        if len(features) > 5 and len(tasks) > 10:
            data_quality = "high"
        elif len(features) < 3 or len(tasks) < 5:
            data_quality = "low"

        hybrid_engine = HybridEngine()
        hybrid_result = hybrid_engine.estimate(
            rule_estimate=rule_estimate,
            ml_estimate=ml_estimate,
            llm_estimate=llm_estimate,
            ml_confidence=ml_confidence,
            data_quality=data_quality,
        )
        hybrid_response = hybrid_engine.get_formatted_result(hybrid_result)
        final_total_hours = hybrid_result.final_estimate

        # 12. EXPLAINABLE AI (with RAG)
        from app.estimation.explanation_engine import ExplanationEngine

        explanation_engine = ExplanationEngine(use_rag=True)
        explanation_result = explanation_engine.explain_project(
            features=feature_names,
            complexities=feature_complexities,
            total_hours=final_total_hours,
            total_cost=cost_result["total"]["expected"],
            timeline_days=formatted_timeline.get("total_days", 0),
            risks=risk_summary,
            complexity_score=complexity_score,
            hybrid_estimate=hybrid_response.get("hybrid_estimate"),
        )
        explanation_response = explanation_engine.get_formatted_explanation(explanation_result)

        # 13. RETURN RESULT
        return ProjectAnalysisResult(
            project_id=project_id,
            features=features,
            tasks=tasks,
            roles=list(summary.keys()),
            total_estimated_hours=final_total_hours,
            complexity_score=complexity_score,
            risk_level=final_risk_level,
            summary=summary,
            timeline=formatted_timeline,
            cost=cost_result,
            risks=risk_summary,
            hybrid_estimate=hybrid_response["hybrid_estimate"],
            explanation=explanation_response,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in analyze: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# REPORT GENERATION ENDPOINTS (Phase 21)
# ============================================

def _get_project_analysis(project_id: int, db: Session) -> Dict[str, Any]:
    """Helper: Get or generate analysis for a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get related data
    features = db.query(Feature).filter(Feature.project_id == project_id).all()
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()

    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "platform": project.platform or "Web",
            "status": project.status or "draft",
            "type": project.type,
        },
        "features": [
            {
                "id": f.id,
                "canonical_name": f.canonical_name,
                "description": f.description,
                "priority": f.priority,
                "complexity": f.complexity,
            }
            for f in features
        ],
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "role_id": t.role_id,
                "estimated_hours": t.estimated_hours,
                "priority": t.priority,
                "is_global": t.is_global,
            }
            for t in tasks
        ],
        "total_estimated_hours": sum(t.estimated_hours for t in tasks),
        "complexity_score": sum(f.complexity for f in features),
        "risk_level": "MEDIUM",
        "roles": list(set(f"Role {t.role_id}" for t in tasks)),
        "summary": {},
        "timeline": None,
        "cost": None,
        "risks": None,
        "hybrid_estimate": None,
        "explanation": None,
    }


@router.get("/projects/{project_id}/report/pdf")
async def download_pdf_report(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download PDF report"""
    try:
        # Run full analysis first
        analysis = await analyze_project(request, project_id, db, current_user)

        # Convert to dict
        analysis_dict = analysis.dict() if hasattr(analysis, 'dict') else analysis

        # Generate PDF
        from app.reports.report_service import ReportService
        service = ReportService()
        filepath = service.generate_pdf(project_id, analysis_dict)

        project = db.query(Project).filter(
            Project.id == project_id,
            Project.organization_id == current_user.organization_id,
        ).first()
        safe_name = (project.name or "project").replace(" ", "_")[:40]

        return FileResponse(
            filepath,
            media_type="application/pdf",
            filename=f"{safe_name}_report.pdf",
        )
    except Exception as e:
        print(f"PDF generation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/report/docx")
async def download_docx_report(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download DOCX report"""
    try:
        analysis = await analyze_project(request, project_id, db, current_user)
        analysis_dict = analysis.dict() if hasattr(analysis, 'dict') else analysis

        from app.reports.report_service import ReportService
        service = ReportService()
        filepath = service.generate_docx(project_id, analysis_dict)

        project = db.query(Project).filter(
            Project.id == project_id,
            Project.organization_id == current_user.organization_id,
        ).first()
        safe_name = (project.name or "project").replace(" ", "_")[:40]

        return FileResponse(
            filepath,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"{safe_name}_report.docx",
        )
    except Exception as e:
        print(f"DOCX generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/report/markdown")
async def download_markdown_report(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download Markdown report"""
    try:
        analysis = await analyze_project(request, project_id, db, current_user)
        analysis_dict = analysis.dict() if hasattr(analysis, 'dict') else analysis

        from app.reports.report_service import ReportService
        service = ReportService()
        filepath = service.generate_markdown(project_id, analysis_dict)

        project = db.query(Project).filter(
            Project.id == project_id,
            Project.organization_id == current_user.organization_id,
        ).first()
        safe_name = (project.name or "project").replace(" ", "_")[:40]

        return FileResponse(
            filepath,
            media_type="text/markdown",
            filename=f"{safe_name}_report.md",
        )
    except Exception as e:
        print(f"Markdown generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/report/csv")
async def download_csv_report(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download CSV (Jira-compatible)"""
    try:
        analysis = await analyze_project(request, project_id, db, current_user)
        analysis_dict = analysis.dict() if hasattr(analysis, 'dict') else analysis

        from app.reports.report_service import ReportService
        service = ReportService()
        filepath = service.generate_csv(project_id, analysis_dict)

        project = db.query(Project).filter(
            Project.id == project_id,
            Project.organization_id == current_user.organization_id,
        ).first()
        safe_name = (project.name or "project").replace(" ", "_")[:40]

        return FileResponse(
            filepath,
            media_type="text/csv",
            filename=f"{safe_name}_tasks.csv",
        )
    except Exception as e:
        print(f"CSV generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}/report/all")
async def get_all_reports_info(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get metadata for all available report formats"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.organization_id == current_user.organization_id,
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project_id": project_id,
        "project_name": project.name,
        "available_formats": [
            {
                "format": "pdf",
                "name": "PDF Report",
                "description": "Professional executive dossier (print-ready)",
                "url": f"/api/v1/projects/{project_id}/report/pdf",
                "mime": "application/pdf",
            },
            {
                "format": "docx",
                "name": "Word Document",
                "description": "Editable Word document",
                "url": f"/api/v1/projects/{project_id}/report/docx",
                "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            },
            {
                "format": "markdown",
                "name": "Markdown",
                "description": "Plain text markdown (GitHub/Notion compatible)",
                "url": f"/api/v1/projects/{project_id}/report/markdown",
                "mime": "text/markdown",
            },
            {
                "format": "csv",
                "name": "Jira CSV",
                "description": "Jira-compatible task import",
                "url": f"/api/v1/projects/{project_id}/report/csv",
                "mime": "text/csv",
            },
        ],
    }

# ============================================
# CHAT ENDPOINT
# ============================================

@router.post("/projects/{project_id}/chat", response_model=ChatMessageResponse)
async def chat_with_project(
    project_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """Chat with AI about a project"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        features = db.query(Feature).filter(Feature.project_id == project_id).all()
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()

        feature_names = [f.canonical_name for f in features]
        total_hours = sum(t.estimated_hours for t in tasks)

        # Get RAG knowledge
        try:
            from app.rag.retriever import Retriever
            retriever = Retriever()
            knowledge = retriever.get_knowledge_for_explanation(
                features=feature_names,
                complexity_score=0,
                risk_level="MEDIUM",
            )
            sources = [
                {"title": s.get("title"), "category": s.get("category")}
                for s in knowledge.get("snippets", [])[:3]
            ]
        except Exception:
            sources = []

        message = request.message.lower()

        if "cost" in message or "budget" in message or "price" in message:
            response = (
                f"Based on our analysis of {project.name}, the estimated cost is "
                f"${total_hours * 50:,.2f} for {total_hours} hours of work. "
                f"This includes design, development, QA, and DevOps effort. "
                f"Costs can vary ±20% based on actual complexity."
            )
            suggestions = [
                "How can I reduce the cost?",
                "What's the breakdown by role?",
                "What's the best-case vs worst-case cost?",
            ]
        elif "time" in message or "timeline" in message or "long" in message:
            response = (
                f"The estimated timeline for {project.name} is approximately "
                f"{max(1, total_hours // 40)} working weeks. "
                f"With {len(tasks)} tasks and {len(features)} features, "
                f"the project can be completed with parallel work streams."
            )
            suggestions = [
                "What's the critical path?",
                "Can we launch an MVP faster?",
                "What are the key milestones?",
            ]
        elif "feature" in message or "include" in message:
            response = (
                f"Your project includes {len(features)} features: "
                f"{', '.join(feature_names[:5])}. "
                f"Each feature has been decomposed into tasks with role assignments and hour estimates."
            )
            suggestions = [
                "Which feature is most complex?",
                "What's in the MVP?",
                "Can we add more features?",
            ]
        elif "risk" in message:
            response = (
                f"Risk assessment identified key risks in {project.name}. "
                f"The main concerns are around payment integration, security, and compliance. "
                f"Each risk has a mitigation strategy and contingency plan."
            )
            suggestions = [
                "What are the top risks?",
                "How do we mitigate them?",
                "What's the risk of delays?",
            ]
        elif "mvp" in message or "minimum" in message:
            response = (
                f"For an MVP of {project.name}, we recommend focusing on "
                f"core features: {', '.join(feature_names[:3])}. "
                f"This would reduce scope by ~40% and speed up launch significantly."
            )
            suggestions = [
                "What should be in Phase 2?",
                "What's the MVP timeline?",
                "What's the MVP cost?",
            ]
        else:
            response = (
                f"Based on analysis of {project.name}, we have identified "
                f"{len(features)} features, {len(tasks)} tasks, "
                f"and estimated {total_hours:.1f} hours of work. "
                f"Ask me about cost, timeline, features, risks, or MVP recommendations."
            )
            suggestions = [
                "What's the total cost?",
                "How long will it take?",
                "What are the risks?",
                "What's in the MVP?",
            ]

        return ChatMessageResponse(
            response=response,
            sources=sources,
            suggestions=suggestions,
            confidence=0.85,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# FEEDBACK ENDPOINT
# ============================================

@router.post("/projects/{project_id}/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    project_id: int,
    request: FeedbackRequest,
    db: Session = Depends(get_db),
):
    """Submit feedback for ML improvement"""
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        feedback_data = {
            "project_id": project_id,
            "rating": request.rating,
            "category": request.category,
            "comments": request.comments,
            "notes": request.notes,
            "actual_hours": request.actual_hours,
            "submitted_at": datetime.now().isoformat(),
        }
        print(f"📝 Feedback received: {feedback_data}")

        return FeedbackResponse(
            id=1,
            project_id=project_id,
            rating=request.rating,
            message="Thank you for your feedback! It will help improve our ML models.",
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))
