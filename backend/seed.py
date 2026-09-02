# seed.py
from app.database.session import SessionLocal
from app.models import Organization, Role
from app.services.role_service import RoleService


def seed_database():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("🌱 Seeding Database...")
        print("=" * 50)
        
        # ============================================
        # 1. Create Organization
        # ============================================
        org = db.query(Organization).first()
        if not org:
            org = Organization(name="Default Organization", plan="free")
            db.add(org)
            db.commit()
            db.refresh(org)
            print(f"✅ Created organization: {org.name} (ID: {org.id})")
        else:
            print(f"✅ Organization already exists: {org.name} (ID: {org.id})")

        # ============================================
        # 2. Create Roles using RoleService
        # ============================================
        role_service = RoleService(db)
        created_count = role_service.initialize_roles()
        print(f"✅ Created {created_count} new roles")
        
        # Show all roles
        roles = db.query(Role).all()
        print("\n📋 Available Roles:")
        print("-" * 40)
        for role in roles:
            print(f"   • {role.name} (ID: {role.id}) - ${role.hourly_rate}/hour")
        
        # ============================================
        # 3. Verify Data
        # ============================================
        print("\n" + "=" * 50)
        print("📊 Database Summary:")
        print("=" * 50)
        
        org_count = db.query(Organization).count()
        role_count = db.query(Role).count()
        
        print(f"   Organizations: {org_count}")
        print(f"   Roles: {role_count}")
        
        if role_count == 0:
            print("   ⚠️  No roles found! Something went wrong.")
        else:
            print("   ✅ All roles seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


def verify_database():
    """Verify that database is properly seeded"""
    db = SessionLocal()
    try:
        print("\n" + "=" * 50)
        print("🔍 Verifying Database...")
        print("=" * 50)
        
        # Check organizations
        orgs = db.query(Organization).all()
        print(f"\n📋 Organizations: {len(orgs)}")
        for org in orgs:
            print(f"   • {org.name} (ID: {org.id}) - Plan: {org.plan}")
        
        # Check roles
        roles = db.query(Role).all()
        print(f"\n📋 Roles: {len(roles)}")
        for role in roles:
            print(f"   • {role.name} (ID: {role.id}) - ${role.hourly_rate}/hour")
            if role.skill_metadata:
                skills = role.skill_metadata.get("skills", [])
                if skills:
                    print(f"     Skills: {', '.join(skills[:3])}{'...' if len(skills) > 3 else ''}")
        
        return len(orgs) > 0 and len(roles) > 0
        
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False
    finally:
        db.close()


def reset_and_seed():
    """Reset database and seed fresh"""
    from app.database.session import engine
    from app.models import Base
    
    print("\n" + "=" * 50)
    print("🔄 Resetting Database...")
    print("=" * 50)
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created")
        
        # Seed data
        seed_database()
        
        # Verify
        verify_database()
        
        print("\n" + "=" * 50)
        print("✅ Database reset and seeded successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Reset error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            reset_and_seed()
        elif sys.argv[1] == "--verify":
            verify_database()
        else:
            print("Usage: python seed.py [--reset | --verify]")
            print("  --reset  : Drop all tables and reseed")
            print("  --verify : Verify database contents")
    else:
        # Default: seed without reset
        seed_database()
        verify_database()
        print("\n" + "=" * 50)
        print("✅ Setup complete! You can now start the server.")
        print("=" * 50)
#  # seed.py
# from app.database.session import SessionLocal
# from app.models import Organization, Role

# def seed_database():
#     db = SessionLocal()
#     try:
#         # Create organization
#         org = db.query(Organization).first()
#         if not org:
#             org = Organization(name="Default Organization", plan="free")
#             db.add(org)
#             db.commit()
#             db.refresh(org)
#             print(f"✅ Created organization: {org.name} (ID: {org.id})")
#         else:
#             print(f"✅ Organization already exists: {org.name} (ID: {org.id})")

#         # Create roles
#         roles_data = [
#             ("UI/UX Designer", 45.0),
#             ("Frontend Developer", 50.0),
#             ("Backend Developer", 55.0),
#             ("Full-Stack Developer", 60.0),
#             ("Mobile Developer", 55.0),
#             ("QA Engineer", 40.0),
#             ("DevOps Engineer", 60.0),
#             ("Security Engineer", 65.0),
#             ("Product Manager", 50.0),
#             ("CEO/Business Owner", 75.0),
#         ]
        
#         created_count = 0
#         for name, rate in roles_data:
#             existing = db.query(Role).filter(Role.name == name).first()
#             if not existing:
#                 role = Role(name=name, hourly_rate=rate)
#                 db.add(role)
#                 created_count += 1
        
#         db.commit()
#         print(f"✅ Created {created_count} new roles")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         db.rollback()
#     finally:
#         db.close()

# if __name__ == "__main__":
#     seed_database()
#     print("\n✅ Setup complete! You can now start the server.")