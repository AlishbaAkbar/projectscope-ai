"""Test auth directly"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.user import User
from app.models.project import Organization
from app.core.security import hash_password

db = SessionLocal()

try:
    # Test hash
    h = hash_password("Test1234")
    print(f"✅ Hash OK: {h[:30]}...")
    
    # Check org
    org = db.query(Organization).first()
    if not org:
        org = Organization(name="Test Org", plan="free")
        db.add(org)
        db.commit()
        db.refresh(org)
        print(f"✅ Org created: {org.id}")
    else:
        print(f"✅ Org exists: {org.id}")
    
    # Try creating user
    user = User(
        email="pyhton_test@example.com",
        password_hash=h,
        full_name="Python Test",
        organization_id=org.id,
        role="owner",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ User created: {user.id} - {user.email}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()