from app.db.base import SessionLocal, engine, Base
from app.models import models
from app.core import security

def seed_hiring_admin():
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        admin = db.query(models.AdminUser).filter(models.AdminUser.username == "hiring_admin").first()
        if not admin:
            admin = models.AdminUser(
                username="hiring_admin",
                full_name="Hiring Manager",
                email="hiring@example.com",
                password_hash=security.get_password_hash("admin123"),
                role="Super_Admin"
            )
            db.add(admin)
            db.commit()
            print("✅ Hiring Admin seeded: hiring_admin / admin123")
        else:
            print("ℹ️ Hiring Admin already exists")
    finally:
        db.close()

if __name__ == "__main__":
    seed_hiring_admin()
