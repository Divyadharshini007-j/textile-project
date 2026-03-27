from app.db.base import SessionLocal
from app.models import models
from datetime import datetime, timedelta
import random

def insert_test_data():
    db = SessionLocal()
    try:
        # Check if we already have data
        count = db.query(models.Purchase).count()
        if count > 0:
            print(f"Database already has {count} purchase records.")
            return

        print("Inserting synthetic purchase data for 'Cotton Yarn 40s'...")
        
        # Create a supplier if none exists
        supplier = db.query(models.Supplier).first()
        if not supplier:
            supplier = models.Supplier(
                supplier_id="TEST_SUPP_1",
                supplier_name="Test Supplier",
                status="Active"
            )
            db.add(supplier)
            db.commit()
            db.refresh(supplier)

        # Insert 20 records over the last 6 months with a slight upward trend
        base_rate = 250.0
        yarn_type = "Cotton Yarn 40s"
        
        for i in range(20):
            date = datetime.now() - timedelta(days=random.randint(0, 180))
            # Upward trend: more recent = slightly higher rate
            days_ago = (datetime.now() - date).days
            trend_factor = (180 - days_ago) / 180 * 20.0 # up to +20 INR
            rate = base_rate + trend_factor + random.uniform(-5, 5)
            
            purchase = models.Purchase(
                purchase_id=f"TEST_PUR_{i}",
                supplier_id=supplier.supplier_id,
                date=date,
                yarn_type=yarn_type,
                quantity=random.uniform(50, 500),
                rate=round(rate, 2),
                grand_total=0.0, # Not needed for prediction
                paid_amount=0.0,
                balance=0.0
            )
            db.add(purchase)
        
        db.commit()
        print("Successfully inserted 20 test records.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()
