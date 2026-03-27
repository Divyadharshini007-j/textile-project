from app.db.base import SessionLocal
from app.models import models

def inspect_users():
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"ID: {user.user_id}, Username: {user.username}, Hash: {user.password_hash[:20]}...")
    finally:
        db.close()

if __name__ == "__main__":
    inspect_users()
