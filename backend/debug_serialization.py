import sys
import os
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

from app.db.base import SessionLocal
from app.models import models
from app.schemas import schemas

print(f"Models file: {models.__file__}")
print(f"Schemas file: {schemas.__file__}")

def debug_serialization():
    db = SessionLocal()
    try:
        print("Fetching a purchase...")
        p = db.query(models.Purchase).first()
        if not p:
            print("No purchases found.")
            return

        print(f"\nFull object __dict__: {p.__dict__}")
        
        print("\nAttempting Pydantic validation (model_validate)...")
        try:
            p_schema = schemas.Purchase.model_validate(p)
            print("Validation successful!")
        except Exception as e:
            print(f"Validation failed: {e}")

        print("\nAttempting manual dict conversion...")
        p_dict = {c.name: getattr(p, c.name) for c in models.Purchase.__table__.columns}
        print(f"Manual dict: {p_dict}")
        try:
            p_schema_2 = schemas.Purchase(**p_dict)
            print("Manual dict validation successful!")
        except Exception as e:
            print(f"Manual dict validation failed: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_serialization()
