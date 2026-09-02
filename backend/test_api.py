# test_api.py - Run this to test if everything works
from app.database.session import SessionLocal
from app.models import Organization, Project, Role
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate

def test_create_project():
    db = SessionLocal()
    try:
        # Check if organization exists
        org = db.query(Organization).first()
        if not org:
            org = Organization(name="Test Org", plan="free")
            db.add(org)
            db.commit()
            db.refresh(org)
            print(f"✅ Created organization: {org.id}")
        
        # Create project
        service = ProjectService(db)
        project_data = ProjectCreate(
            name="Test Project",
            description="Test description",
            organization_id=org.id
        )
        project = service.create_project(project_data)
        print(f"✅ Created project: {project.id} - {project.name}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_create_project()