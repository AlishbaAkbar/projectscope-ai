# create_seed.py
from app.database.session import SessionLocal
from sqlalchemy import text

def seed_database():
    db = SessionLocal()
    try:
        # Create organization
        db.execute(text("""
            INSERT OR IGNORE INTO organizations (id, name, plan, created_at)
            VALUES (1, 'Default Organization', 'free', datetime('now'))
        """))
        
        # Create roles
        roles = [
            ('UI/UX Designer', 45.0),
            ('Frontend Developer', 50.0),
            ('Backend Developer', 55.0),
            ('Full-Stack Developer', 60.0),
            ('Mobile Developer', 55.0),
            ('QA Engineer', 40.0),
            ('DevOps Engineer', 60.0),
            ('Security Engineer', 65.0),
            ('Product Manager', 50.0),
            ('CEO/Business Owner', 75.0),
        ]
        
        for name, rate in roles:
            db.execute(text("""
                INSERT OR IGNORE INTO roles (name, hourly_rate, created_at)
                VALUES (:name, :rate, datetime('now'))
            """), {"name": name, "rate": rate})
        
        db.commit()
        print("✅ Seeded: 1 organization, 10 roles")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()