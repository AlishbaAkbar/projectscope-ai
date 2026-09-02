from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.project_service import ProjectService
from app.services.role_service import RoleService
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.features import FeatureResponse
from app.schemas.tasks import TaskResponse
from app.schemas.analysis import ProjectAnalysisResult
from app.schemas.roles import RoleDetailResponse

from app.models.project import Project, Requirement
from app.models.feature import Feature
from app.models.task import Task

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
        # Check project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get requirements
        requirements = db.query(Requirement).filter(Requirement.project_id == project_id).all()
        
        # Create sample requirements if none
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
        
        db.commit()
        features = db.query(Feature).filter(Feature.project_id == project_id).all()
        
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
            
            elif feature.canonical_name == "PAYMENT":
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
                    role_id=1,
                    title="Design payment flows",
                    description="Design payment and confirmation screens",
                    estimated_hours=10,
                    priority="HIGH"
                ))
            
            elif feature.canonical_name == "ORDER_MANAGEMENT":
                tasks.append(Task(
                    project_id=project_id,
                    feature_id=feature.id,
                    role_id=3,
                    title="Build order management API",
                    description="Create order tracking endpoints",
                    estimated_hours=12,
                    priority="HIGH"
                ))
        
        for task in tasks:
            db.add(task)
        db.commit()
        
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        # Calculate totals
        total_hours = sum(t.estimated_hours for t in tasks)
        complexity_score = sum(f.complexity for f in features)
        
        if complexity_score > 25:
            risk_level = "HIGH"
        elif complexity_score > 15:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Create summary with role names
        summary = {}
        role_service = RoleService(db)
        for task in tasks:
            role_name = role_service.format_role_for_task(task.role_id)["name"]
            if role_name not in summary:
                summary[role_name] = {"total_hours": 0, "num_tasks": 0}
            summary[role_name]["total_hours"] += task.estimated_hours
            summary[role_name]["num_tasks"] += 1
        
        return ProjectAnalysisResult(
            project_id=project_id,
            features=features,
            tasks=tasks,
            roles=list(summary.keys()),
            total_estimated_hours=total_hours,
            complexity_score=complexity_score,
            risk_level=risk_level,
            summary=summary
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