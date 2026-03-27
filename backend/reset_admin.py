from app.db.base import SessionLocal
from app.models import models
from app.core import security

def reset_admin():
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if admin:
            print("Deleting existing admin user...")
            db.delete(admin)
            db.commit()
        
        print("Creating fresh admin user...")
        new_admin = models.User(
            user_id="ADMIN001",
            username="admin",
            password_hash=security.get_password_hash("admin123"),
            full_name="System Admin",
            email="admin@example.com",
            role="Admin",
            is_active=True
        )
        db.add(new_admin)
        db.commit()
        print("Admin user reset: admin / admin123")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin()
