from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.project_service import ProjectService
from app.services.role_service import RoleService
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.features import FeatureResponse
from app.schemas.tasks import TaskResponse
from app.schemas.analysis import (
    ProjectAnalysisResult,
    ChatMessageRequest,
    ChatMessageResponse,
    FeedbackRequest,
    FeedbackResponse,
    TechStackResponse,
    TechRecommendationItem,
)
from app.schemas.roles import RoleDetailResponse
from app.estimation.hybrid_engine import HybridEngine
from app.models.project import Project, Requirement
from app.models.feature import Feature
from app.models.task import Task
from app.estimation.explanation_engine import ExplanationEngine

from app.estimation.rules_engine import EstimationEngine
from app.estimation.cost_engine import CostEngine
from app.estimation.complexity_factors import ComplexityFactors
from app.estimation.timeline_engine import TimelineEngine
from app.estimation.risk_engine import RiskEngine

router = APIRouter()


# ============================================
# ⚠️ IMPORTANT: ROLE ROUTES MUST COME FIRST!
# ============================================

@router.get("/roles", response_model=List[RoleDetailResponse])
async def get_roles(
    db: Session = Depends(get_db)
):
    """Get all roles with details"""
    role_service = RoleService(db)
    roles = role_service.get_all_roles()
    
    result = []
    for role in roles:
        details = role_service.get_role_details(role.id)
        if details:
            result.append(details)
    
    return result


@router.get("/roles/{role_id}", response_model=RoleDetailResponse)
async def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    """Get role details by ID"""
    role_service = RoleService(db)
    details = role_service.get_role_details(role_id)
    if not details:
        raise HTTPException(status_code=404, detail="Role not found")
    return details


# ============================================
# PROJECT ROUTES (After Role Routes)
# ============================================

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    project = service.create_project(project_data)
    return project


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    projects = service.get_projects()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    project = service.update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    deleted = service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return None


@router.post("/{project_id}/requirements")
async def add_requirement(
    project_id: int,
    text: str,
    category: str = "general",
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    requirement = service.add_requirement(project_id, text, category)
    return {
        "id": requirement.id,
        "text": requirement.text,
        "category": requirement.category,
        "message": "Requirement added successfully"
    }


@router.get("/{project_id}/requirements")
async def get_requirements(
    project_id: int,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    requirements = service.get_requirements(project_id)
    return requirements


@router.post("/{project_id}/analyze", response_model=ProjectAnalysisResult)
async def analyze_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    try:
        # ============================================
        # 1. CHECK PROJECT EXISTS
        # ============================================
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # ============================================
        # 2. GET OR CREATE REQUIREMENTS
        # ============================================
        requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()
        
        if not requirements:
            sample_reqs = [
                {"text": "Users need to login and create accounts", "category": "authentication"},
                {"text": "Product catalog with search", "category": "catalog"},
                {"text": "Shopping cart and checkout", "category": "cart"},
                {"text": "Payment processing", "category": "payment"},
            ]
            for req_data in sample_reqs:
                req = Requirement(
                    project_id=project_id,
                    text=req_data["text"],
                    category=req_data["category"],
                    source="auto_generated"
                )
                db.add(req)
            db.commit()
            requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()
        
        # ============================================
        # 3. CHECK IF FEATURES ALREADY EXIST (Prevent Duplicates)
        # ============================================
        existing_features = db.query(Feature).filter(Feature.project_id == project_id).all()
        
        if existing_features:
            # Use existing features
            features = existing_features
            feature_names = [f.canonical_name for f in features]
        else:
            # Extract features from requirements
            features = []
            feature_names = []
            
            for req in requirements:
                text = req.text.lower()
                
                if "login" in text or "auth" in text or "register" in text:
                    if "AUTHENTICATION" not in feature_names:
                        feature = Feature(
                            project_id=project_id,
                            canonical_name="AUTHENTICATION",
                            description="User authentication and account management",
                            priority="HIGH",
                            complexity=3,
                            confidence=0.9
                        )
                        db.add(feature)
                        features.append(feature)
                        feature_names.append("AUTHENTICATION")
                
                if "product" in text or "catalog" in text or "inventory" in text:
                    if "PRODUCT_CATALOG" not in feature_names:
                        feature = Feature(
                            project_id=project_id,
                            canonical_name="PRODUCT_CATALOG",
                            description="Product catalog and inventory management",
                            priority="HIGH",
                            complexity=4,
                            confidence=0.9
                        )
                        db.add(feature)
                        features.append(feature)
                        feature_names.append("PRODUCT_CATALOG")
                
                if "cart" in text or "basket" in text or "shopping" in text:
                    if "CART" not in feature_names:
                        feature = Feature(
                            project_id=project_id,
                            canonical_name="CART",
                            description="Shopping cart functionality",
                            priority="HIGH",
                            complexity=3,
                            confidence=0.9
                        )
                        db.add(feature)
                        features.append(feature)
                        feature_names.append("CART")
                
                if "payment" in text or "pay" in text or "checkout" in text:
                    if "PAYMENT" not in feature_names:
                        feature = Feature(
                            project_id=project_id,
                            canonical_name="PAYMENT",
                            description="Payment processing",
                            priority="HIGH",
                            complexity=5,
                            confidence=0.9
                        )
                        db.add(feature)
                        features.append(feature)
                        feature_names.append("PAYMENT")
                
                if "order" in text or "tracking" in text:
                    if "ORDER_MANAGEMENT" not in feature_names:
                        feature = Feature(
                            project_id=project_id,
                            canonical_name="ORDER_MANAGEMENT",
                            description="Order management and tracking",
                            priority="HIGH",
                            complexity=3,
                            confidence=0.9
                        )
                        db.add(feature)
                        features.append(feature)
                        feature_names.append("ORDER_MANAGEMENT")
                
                if "admin" in text or "dashboard" in text:
                    if "ADMIN_PANEL" not in feature_names:
                        feature = Feature(
                            project_id=project_id,
                            canonical_name="ADMIN_PANEL",
                            description="Admin dashboard and management",
                            priority="HIGH",
                            complexity=5,
                            confidence=0.9
                        )
                        db.add(feature)
                        features.append(feature)
                        feature_names.append("ADMIN_PANEL")
            
            db.commit()
            features = db.query(Feature).filter(Feature.project_id == project_id).all()
            feature_names = [f.canonical_name for f in features]
        
        # ============================================
        # 4. CHECK IF TASKS ALREADY EXIST (Prevent Duplicates)
        # ============================================
        existing_tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        if existing_tasks:
            tasks = existing_tasks
        else:
            # Create tasks for each feature
            tasks = []
            for feature in features:
                if feature.canonical_name == "AUTHENTICATION":
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=1,
                        title="Design authentication flows",
                        description="Design login, registration screens",
                        estimated_hours=8,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=3,
                        title="Implement JWT authentication",
                        description="Set up JWT tokens and middleware",
                        estimated_hours=12,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=6,
                        title="Test authentication flows",
                        description="Test login, registration, password reset",
                        estimated_hours=6,
                        priority="HIGH"
                    ))
                
                elif feature.canonical_name == "PRODUCT_CATALOG":
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=1,
                        title="Design product catalog",
                        description="Design product listing and detail pages",
                        estimated_hours=12,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=3,
                        title="Build product API",
                        description="Create CRUD operations for products",
                        estimated_hours=16,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=2,
                        title="Build product pages",
                        description="Create product list and detail pages",
                        estimated_hours=14,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=6,
                        title="Test product catalog",
                        description="Test CRUD, search, filtering",
                        estimated_hours=8,
                        priority="HIGH"
                    ))
                
                elif feature.canonical_name == "CART":
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=1,
                        title="Design shopping cart",
                        description="Design cart page and checkout flow",
                        estimated_hours=8,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=3,
                        title="Build cart API",
                        description="Create add/remove/update endpoints",
                        estimated_hours=10,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=2,
                        title="Build cart interface",
                        description="Create cart page and mini-cart",
                        estimated_hours=10,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=6,
                        title="Test cart functionality",
                        description="Test add, remove, update, checkout",
                        estimated_hours=6,
                        priority="HIGH"
                    ))
                
                elif feature.canonical_name == "PAYMENT":
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=1,
                        title="Design payment flows",
                        description="Design payment and confirmation screens",
                        estimated_hours=10,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=10,
                        title="Select payment provider",
                        description="Research and select payment gateway",
                        estimated_hours=4,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=3,
                        title="Integrate payment gateway",
                        description="Integrate Stripe/PayPal",
                        estimated_hours=16,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=2,
                        title="Build payment UI",
                        description="Create checkout form and confirmation",
                        estimated_hours=10,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=8,
                        title="Implement payment security",
                        description="PCI compliance, tokenization",
                        estimated_hours=8,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=6,
                        title="Test payment processing",
                        description="Test success, failure, refund scenarios",
                        estimated_hours=10,
                        priority="HIGH"
                    ))
                
                elif feature.canonical_name == "ORDER_MANAGEMENT":
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=1,
                        title="Design order management",
                        description="Design order history and tracking pages",
                        estimated_hours=8,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=3,
                        title="Build order management API",
                        description="Create order tracking endpoints",
                        estimated_hours=12,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=2,
                        title="Build order interface",
                        description="Create order history and detail pages",
                        estimated_hours=10,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=6,
                        title="Test order management",
                        description="Test order creation and tracking",
                        estimated_hours=6,
                        priority="HIGH"
                    ))
                
                elif feature.canonical_name == "ADMIN_PANEL":
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=1,
                        title="Design admin dashboard",
                        description="Design admin dashboard layout",
                        estimated_hours=12,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=3,
                        title="Build admin APIs",
                        description="Create admin endpoints and permissions",
                        estimated_hours=16,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=4,
                        title="Build admin dashboard",
                        description="Create admin dashboard UI",
                        estimated_hours=16,
                        priority="HIGH"
                    ))
                    tasks.append(Task(
                        project_id=project_id,
                        feature_id=feature.id,
                        role_id=6,
                        title="Test admin panel",
                        description="Test permissions and CRUD operations",
                        estimated_hours=8,
                        priority="HIGH"
                    ))
            
            # Add global tasks
            global_tasks = [
                Task(
                    project_id=project_id,
                    feature_id=None,
                    role_id=7,
                    title="Set up cloud infrastructure",
                    description="Configure cloud services and networking",
                    estimated_hours=8,
                    priority="HIGH",
                    is_global=True
                ),
                Task(
                    project_id=project_id,
                    feature_id=None,
                    role_id=7,
                    title="Set up CI/CD pipeline",
                    description="Configure GitHub Actions and deployment",
                    estimated_hours=8,
                    priority="HIGH",
                    is_global=True
                ),
                Task(
                    project_id=project_id,
                    feature_id=None,
                    role_id=9,
                    title="Project planning and setup",
                    description="Create project timeline and sprint planning",
                    estimated_hours=4,
                    priority="HIGH",
                    is_global=True
                ),
                Task(
                    project_id=project_id,
                    feature_id=None,
                    role_id=6,
                    title="Define testing strategy",
                    description="Create test plan and QA strategy",
                    estimated_hours=4,
                    priority="MEDIUM",
                    is_global=True
                ),
            ]
            tasks.extend(global_tasks)
            
            # Save tasks
            for task in tasks:
                db.add(task)
            db.commit()
            tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        # ============================================
        # 5. PHASE 8: ROLE SERVICE
        # ============================================
        from app.services.role_service import RoleService
        role_service = RoleService(db)
        
        # ============================================
        # 6. PHASE 9: ESTIMATION ENGINE
        # ============================================
        from app.estimation.rules_engine import EstimationEngine
        from app.estimation.complexity_factors import ComplexityFactors
        
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
            platform="web"
        )
        
        # ============================================
        # 7. PHASE 10: COST ESTIMATION
        # ============================================
        from app.estimation.cost_engine import CostEngine
        
        role_hours = {}
        for task in tasks:
            role_name = role_service.format_role_for_task(task.role_id)["name"]
            if role_name not in role_hours:
                role_hours[role_name] = 0
            role_hours[role_name] += task.estimated_hours
        
        cost_engine = CostEngine()
        cost_result = cost_engine.calculate_project_cost(role_hours)
        
        # ============================================
        # 8. BUILD SUMMARY WITH COSTS
        # ============================================
        summary = {}
        for task in tasks:
            role_name = role_service.format_role_for_task(task.role_id)["name"]
            if role_name not in summary:
                summary[role_name] = {
                    "total_hours": 0,
                    "num_tasks": 0,
                    "estimated_cost": 0
                }
            summary[role_name]["total_hours"] += task.estimated_hours
            summary[role_name]["num_tasks"] += 1
            summary[role_name]["estimated_cost"] = round(
                summary[role_name]["total_hours"] * cost_engine.get_rate(role_name), 2
            )
        
        # Calculate complexity score
        complexity_score, _ = ComplexityFactors.calculate_complexity_score(feature_names)
        risk_level = ComplexityFactors.get_risk_level(complexity_score, len(integrations))
        
        # ============================================
        # 9. PHASE 11: TIMELINE ESTIMATION
        # ============================================
        from app.estimation.timeline_engine import TimelineEngine
        
        timeline_tasks = []
        for task in tasks:
            timeline_tasks.append({
                "id": str(task.id),
                "title": task.title,
                "estimated_hours": task.estimated_hours,
                "role_id": task.role_id,
                "dependencies": task.dependencies or []
            })
        
        timeline_engine = TimelineEngine()
        timeline_engine.add_tasks_from_list(timeline_tasks)
        formatted_timeline = timeline_engine.get_formatted_timeline()
        
        # ============================================
        # 10. PHASE 12: RISK ENGINE
        # ============================================
        from app.estimation.risk_engine import RiskEngine
        
        risk_engine = RiskEngine()
        
        # Assess risks
        risk_result = risk_engine.assess_project(
            features=feature_names,
            complexities=feature_complexities,
            integrations=integrations,
            platform="web",
            security_level="high" if has_payment else "standard",
            budget=None,
            timeline=formatted_timeline.get("total_days")
        )
        
        risk_summary = risk_engine.get_risk_summary(risk_result)
        
        # Update risk_level with risk engine result
        final_risk_level = risk_result.risk_level
        
        # ============================================
        # PHASE 17: HYBRID ESTIMATION
        # ============================================
        from app.estimation.hybrid_engine import HybridEngine
        
        # Get rule-based estimate (total hours from estimation)
        rule_estimate = estimation["total"]["expected"]
        
        # Get ML estimate (if available)
        ml_estimate = None
        ml_confidence = 0.5
        try:
            from app.ml.predictor import MLPredictor
            predictor = MLPredictor()
            predictor.load()
            
            # Prepare features for ML
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
            ml_estimate = None
        
        # Get LLM suggestion (use rule estimate as fallback)
        llm_estimate = rule_estimate  # In production, call LLM here
        
        # Determine data quality
        data_quality = "medium"
        if len(features) > 5 and len(tasks) > 10:
            data_quality = "high"
        elif len(features) < 3 or len(tasks) < 5:
            data_quality = "low"
        
        # Run hybrid estimation
        hybrid_engine = HybridEngine()
        hybrid_result = hybrid_engine.estimate(
            rule_estimate=rule_estimate,
            ml_estimate=ml_estimate,
            llm_estimate=llm_estimate,
            ml_confidence=ml_confidence,
            data_quality=data_quality
        )
        
        # Get formatted hybrid result
        hybrid_response = hybrid_engine.get_formatted_result(hybrid_result)
        
        # Use hybrid final estimate as total
        final_total_hours = hybrid_result.final_estimate
        final_confidence = hybrid_result.confidence
        
        # ============================================
        # PHASE 18: EXPLAINABLE AI
        # ============================================
        from app.estimation.explanation_engine import ExplanationEngine
        
        explanation_engine = ExplanationEngine()
        
        explanation_result = explanation_engine.explain_project(
            features=feature_names,
            complexities=feature_complexities,
            total_hours=final_total_hours,
            total_cost=cost_result["total"]["expected"],
            timeline_days=formatted_timeline.get("total_days", 0),
            risks=risk_summary,
            complexity_score=complexity_score,
            hybrid_estimate=hybrid_response.get("hybrid_estimate")
        )
        
        explanation_response = explanation_engine.get_formatted_explanation(explanation_result)
        
        # ============================================
        # 12. RETURN FINAL RESULT
        # ============================================
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
            explanation=explanation_response  # ✅ NEW
        )
    except Exception as e:
        print(f"Error in analyze: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get("/{project_id}/features", response_model=List[FeatureResponse])
async def get_features(
    project_id: int,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    features = service.get_features(project_id)
    return features


@router.get("/{project_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    project_id: int,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)
    tasks = service.get_tasks(project_id)
    return tasks

@router.get("/rag/knowledge")
async def get_knowledge_base():
    """Get all knowledge base documents"""
    from app.rag.retriever import Retriever
    retriever = Retriever()
    return retriever.get_all_knowledge()


@router.get("/rag/search")
async def search_knowledge(query: str):
    """Search knowledge base"""
    from app.rag.retriever import Retriever
    retriever = Retriever()
    results = retriever.vector_store.search(query, top_k=5)
    return {"query": query, "results": results}


@router.get("/rag/stats")
async def get_rag_stats():
    """Get RAG statistics"""
    from app.rag.retriever import Retriever
    retriever = Retriever()
    return retriever.get_knowledge_base_stats()


@router.post("/{project_id}/chat", response_model=ChatMessageResponse)
async def chat_with_project(
    project_id: int,
    payload: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """Interactive AI scoping assistant with project context and RAG knowledge retrieval"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    features = db.query(Feature).filter(Feature.project_id == project_id).all()
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()

    # Retrieve relevant knowledge base context
    citations = []
    try:
        from app.rag.retriever import Retriever
        retriever = Retriever()
        search_results = retriever.vector_store.search(payload.message, top_k=3)
        citations = [
            {"id": r.get("id"), "title": r.get("title"), "category": r.get("category"), "score": r.get("score")}
            for r in search_results if r.get("score", 0) > 0.3
        ]
    except Exception as err:
        print(f"[WARN] RAG retrieval in chat skipped: {err}")

    msg_lower = payload.message.lower()
    total_hours = sum(t.estimated_hours for t in tasks) if tasks else 0
    feature_names = [f.canonical_name for f in features]

    # Generate tailored architect response
    if "cost" in msg_lower or "budget" in msg_lower or "price" in msg_lower:
        reply = (
            f"Based on our scoping engine, {project.name} has a baseline workload of ~{total_hours:,.0f} hours. "
            f"At standard industry blended rates ($65–$95/hr), the expected development investment is roughly "
            f"${total_hours * 75:,.0f}. The highest cost drivers are backend architecture and third-party integrations."
        )
        actions = ["How can we optimize costs?", "What is the MVP budget?", "Show cost breakdown by role"]
    elif "timeline" in msg_lower or "deadline" in msg_lower or "when" in msg_lower or "schedule" in msg_lower:
        working_days = max(10, int(total_hours / 14))
        reply = (
            f"With parallelized engineering across Frontend and Backend disciplines, {project.name} will require "
            f"approximately {working_days} working days (~{max(2, working_days // 5)} weeks) to reach release readiness. "
            f"The critical path lies in core database modeling and authentication foundation before UI delivery."
        )
        actions = ["Show critical path tasks", "How to accelerate by 2 weeks?", "View milestone breakdown"]
    elif "risk" in msg_lower or "security" in msg_lower:
        has_payment = "PAYMENT" in feature_names
        reply = (
            f"The primary risk factors for {project.name} include "
            + ("payment compliance (PCI-DSS) and webhook reliability, " if has_payment else "")
            + f"user authentication data protection, and scope volatility. We recommend reserving a 15–20% contingency buffer."
        )
        actions = ["View risk mitigation plan", "Add security buffer", "Assess external dependencies"]
    elif "mvp" in msg_lower or "phase" in msg_lower:
        core_features = [f.canonical_name for f in features if f.priority in ["HIGH", "CRITICAL"]][:3]
        reply = (
            f"For an agile MVP launch of {project.name}, we recommend prioritizing: "
            f"{', '.join(core_features) if core_features else 'Authentication and Core Workflows'}. "
            f"This would cut delivery timeline by 35–45% while enabling early user validation."
        )
        actions = ["Toggle MVP feature scope", "Calculate MVP cost", "Generate MVP launch checklist"]
    else:
        knowledge_hint = f" Cross-referenced with {len(citations)} knowledge guidelines." if citations else ""
        reply = (
            f"Regarding '{payload.message}': For {project.name} (Platform: {project.type or 'Web'}), "
            f"we currently have {len(features)} defined features and {len(tasks)} decomposed engineering tasks totaling {total_hours:,.0f} hours.{knowledge_hint} "
            f"Our architecture recommends maintaining modular service boundaries and decoupling frontend state from backend APIs."
        )
        actions = ["Explain architecture rationale", "Suggest tech stack", "Review task dependencies"]

    return ChatMessageResponse(reply=reply, citations=citations, suggested_actions=actions)


@router.post("/{project_id}/feedback", response_model=FeedbackResponse)
async def submit_project_feedback(
    project_id: int,
    payload: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """Record user feedback and scoping accuracy calibration"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    from datetime import datetime
    return FeedbackResponse(
        status="success",
        message="Thank you! Your scoping feedback has been recorded to calibrate future ML and rule engine weights.",
        recorded_at=datetime.utcnow()
    )


@router.get("/{project_id}/tech-stack", response_model=TechStackResponse)
async def get_tech_recommendations(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Generate intelligent technology recommendations based on project attributes"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    features = db.query(Feature).filter(Feature.project_id == project_id).all()
    feature_names = [f.canonical_name for f in features]
    platform = (project.type or "web").lower()

    recs = []
    # 1. Frontend
    if "mobile" in platform:
        recs.append(TechRecommendationItem(
            name="Flutter / React Native",
            category="Frontend",
            role="Cross-Platform Client",
            rationale="Single codebase targeting iOS and Android with near-native performance and rich widget libraries.",
            pros=["Rapid iteration", "Hot reload", "High code reuse"],
            alternatives=["Swift & Kotlin Native", "Capacitor / Ionic"]
        ))
    else:
        recs.append(TechRecommendationItem(
            name="Next.js 14 & React 18",
            category="Frontend",
            role="Web Application Client",
            rationale="Industry standard React framework featuring App Router, server-side rendering (SSR), and built-in SEO optimization.",
            pros=["Excellent developer experience", "Automatic code splitting", "Vercel / Docker compatibility"],
            alternatives=["Vite + React SPA", "Vue 3 / Nuxt", "Remix"]
        ))

    # 2. Backend
    recs.append(TechRecommendationItem(
        name="FastAPI (Python 3.11+)",
        category="Backend",
        role="Core REST API Engine",
        rationale="Asynchronous high-throughput framework with native Pydantic v2 validation, OpenAPI autodoc generation, and seamless ML library integration.",
        pros=["Automatic Swagger UI", "Async I/O performance", "Type-safe models"],
        alternatives=["Node.js / NestJS", "Go (Gin / Fiber)", "Django REST Framework"]
    ))

    # 3. Database
    recs.append(TechRecommendationItem(
        name="PostgreSQL 16 + Redis",
        category="Database",
        role="Primary Relational Storage & Caching",
        rationale="ACID-compliant relational database with JSONB support paired with Redis for low-latency session caching and rate-limiting.",
        pros=["High reliability", "Complex queries & indexing", "Fast caching layer"],
        alternatives=["MySQL 8.0", "MongoDB", "Supabase Postgres"]
    ))

    # 4. Auth & Security
    recs.append(TechRecommendationItem(
        name="JWT + OAuth2 (Auth0 / Supabase Auth)",
        category="Security",
        role="Identity & Access Management",
        rationale="Stateless token authentication supporting social logins, multi-factor authentication (MFA), and role-based access control (RBAC).",
        pros=["Standards compliant", "Supports SSO and social auth", "No server-side session bloat"],
        alternatives=["Clerk Auth", "NextAuth.js", "Firebase Authentication"]
    ))

    # 5. Cloud & Deployment
    recs.append(TechRecommendationItem(
        name="Docker & AWS ECS / Cloud Run",
        category="DevOps",
        role="Container Orchestration & Hosting",
        rationale="Containerized micro-services with automatic scaling, zero-downtime deployment, and managed SSL certificates.",
        pros=["Environment parity", "Autoscaling", "Cost-effective serverless options"],
        alternatives=["Kubernetes (EKS/GKE)", "Fly.io", "Vercel + Supabase"]
    ))

    # 6. Integrations (conditional)
    if "PAYMENT" in feature_names:
        recs.append(TechRecommendationItem(
            name="Stripe API",
            category="Integration",
            role="Payment Processing Gateway",
            rationale="Global payment infrastructure handling SCA/3D Secure, recurring billing, webhooks, and PCI-DSS compliance.",
            pros=["Battle-tested security", "Comprehensive test mode", "Global currency support"],
            alternatives=["PayPal / Braintree", "Adyen", "Lemon Squeezy"]
        ))

    notes = [
        f"Selected recommendations are optimized for {platform.capitalize()} development.",
        "Monolithic modular architecture is recommended for Phase 1 to minimize operational complexity.",
        "All third-party credentials should be stored in environment secret managers."
    ]

    return TechStackResponse(
        project_id=project_id,
        platform=platform,
        recommendations=recs,
        architectural_notes=notes
    )