from app.db.base import SessionLocal, engine, Base
from app.services.import_service import ImportService
import os

def run_import():
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        base_path = "c:/Users/divya/Downloads/textile_ai_project/data"
        print("Starting data import...")
        stats = ImportService.import_all(db, base_path)
        print("Import completed successfully!")
        for key, val in stats.items():
            print(f"- {key.capitalize()}: {val} records")
    except Exception as e:
        print(f"Error during import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_import()
