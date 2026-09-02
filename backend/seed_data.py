from app.database.session import SessionLocal
from app.models.project import Organization

def create_default_org():
    db = SessionLocal()
    try:
        # Check if org exists
        org = db.query(Organization).first()
        if not org:
            org = Organization(name="Default Organization", plan="free")
            db.add(org)
            db.commit()
            db.refresh(org)
            print(f"✅ Created default organization with ID: {org.id}")
        else:
            print(f"✅ Organization already exists with ID: {org.id}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_org()