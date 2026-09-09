"""
Create a sample project with requirements and analyze it
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.models.project import Project, Requirement, Organization
from app.models.feature import Feature
from app.models.task import Task
from app.models.role import Role
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate


def create_sample_project():
    db = SessionLocal()
    try:
        print("🔄 Creating sample project...")
        
        # Check if organization exists
        org = db.query(Organization).first()
        if not org:
            org = Organization(name="Default Organization", plan="free")
            db.add(org)
            db.commit()
            db.refresh(org)
            print(f"✅ Created organization: {org.id}")
        else:
            print(f"✅ Organization already exists: {org.id}")
        
        # Create project
        project_service = ProjectService(db)
        project_data = ProjectCreate(
            name="E-commerce Store",
            description="Online clothing store with login, products, cart, payment",
            organization_id=org.id
        )
        project = project_service.create_project(project_data)
        print(f"✅ Created project: {project.id} - {project.name}")
        
        # Add requirements
        requirements_data = [
            {"text": "Users need to login and create accounts", "category": "authentication"},
            {"text": "Product catalog with search functionality", "category": "catalog"},
            {"text": "Shopping cart and checkout", "category": "cart"},
            {"text": "Payment processing with credit cards", "category": "payment"},
            {"text": "Order tracking and order history", "category": "orders"},
            {"text": "Admin dashboard to manage products and orders", "category": "admin"},
        ]
        
        requirements = []
        for req_data in requirements_data:
            req = Requirement(
                project_id=project.id,
                text=req_data["text"],
                category=req_data["category"],
                source="user_input"
            )
            db.add(req)
            requirements.append(req)
        db.commit()
        print(f"✅ Added {len(requirements)} requirements")
        
        # Add features
        features_data = [
            {"name": "AUTHENTICATION", "description": "User authentication", "complexity": 3},
            {"name": "PRODUCT_CATALOG", "description": "Product catalog", "complexity": 4},
            {"name": "CART", "description": "Shopping cart", "complexity": 3},
            {"name": "PAYMENT", "description": "Payment processing", "complexity": 5},
            {"name": "ORDER_MANAGEMENT", "description": "Order management", "complexity": 3},
            {"name": "ADMIN_PANEL", "description": "Admin dashboard", "complexity": 5},
        ]
        
        features = []
        for f_data in features_data:
            feature = Feature(
                project_id=project.id,
                canonical_name=f_data["name"],
                description=f_data["description"],
                priority="HIGH",
                complexity=f_data["complexity"],
                confidence=0.9
            )
            db.add(feature)
            features.append(feature)
        db.commit()
        print(f"✅ Added {len(features)} features")
        
        # Get feature IDs
        feature_ids = {f.canonical_name: f.id for f in features}
        
        # Add tasks
        tasks_data = [
            {"title": "Design authentication flows", "role_id": 1, "hours": 8, "feature": "AUTHENTICATION"},
            {"title": "Implement JWT authentication", "role_id": 3, "hours": 12, "feature": "AUTHENTICATION"},
            {"title": "Design product catalog", "role_id": 1, "hours": 12, "feature": "PRODUCT_CATALOG"},
            {"title": "Build product API", "role_id": 3, "hours": 16, "feature": "PRODUCT_CATALOG"},
            {"title": "Design shopping cart", "role_id": 1, "hours": 8, "feature": "CART"},
            {"title": "Build cart API", "role_id": 3, "hours": 10, "feature": "CART"},
            {"title": "Integrate payment gateway", "role_id": 3, "hours": 16, "feature": "PAYMENT"},
            {"title": "Design payment flows", "role_id": 1, "hours": 10, "feature": "PAYMENT"},
            {"title": "Build order management API", "role_id": 3, "hours": 12, "feature": "ORDER_MANAGEMENT"},
            {"title": "Design admin dashboard", "role_id": 1, "hours": 12, "feature": "ADMIN_PANEL"},
            {"title": "Build admin dashboard", "role_id": 4, "hours": 16, "feature": "ADMIN_PANEL"},
        ]
        
        tasks = []
        for task_data in tasks_data:
            feature_id = feature_ids.get(task_data["feature"])
            
            task = Task(
                project_id=project.id,
                feature_id=feature_id,
                role_id=task_data["role_id"],
                title=task_data["title"],
                description=f"Task: {task_data['title']}",
                estimated_hours=task_data["hours"],
                priority="HIGH"
            )
            db.add(task)
            tasks.append(task)
        db.commit()
        print(f"✅ Added {len(tasks)} tasks")
        
        # Add global tasks (as Task objects, not dicts)
        global_tasks_data = [
            {"title": "Set up cloud infrastructure", "role_id": 7, "hours": 8},
            {"title": "Set up CI/CD pipeline", "role_id": 7, "hours": 8},
            {"title": "Project planning and setup", "role_id": 9, "hours": 4},
            {"title": "Define testing strategy", "role_id": 6, "hours": 4},
        ]
        
        global_tasks = []  # ✅ Now a list of Task objects
        for task_data in global_tasks_data:
            task = Task(
                project_id=project.id,
                feature_id=None,
                role_id=task_data["role_id"],
                title=task_data["title"],
                description=f"Global task: {task_data['title']}",
                estimated_hours=task_data["hours"],
                priority="HIGH",
                is_global=True
            )
            db.add(task)
            global_tasks.append(task)  # ✅ Append Task object
        db.commit()
        print(f"✅ Added {len(global_tasks)} global tasks")
        
        # Calculate total hours
        total_task_hours = sum(t.estimated_hours for t in tasks)
        total_global_hours = sum(t.estimated_hours for t in global_tasks)  # ✅ Now works
        total_hours = total_task_hours + total_global_hours
        
        print(f"\n✅ Sample project created successfully!")
        print(f"   Project ID: {project.id}")
        print(f"   Name: {project.name}")
        print(f"   Requirements: {len(requirements)}")
        print(f"   Features: {len(features)}")
        print(f"   Tasks: {len(tasks) + len(global_tasks)}")
        print(f"   Total Estimated Hours: {total_hours}")
        
        return project.id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_project()