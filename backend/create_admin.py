from app.db.base import SessionLocal
from app.models import models
from app.core import security

def create_admin():
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            print("Creating admin user...")
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
            print("Admin user created: admin / admin123")
        else:
            print("Admin user already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
