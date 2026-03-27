import sys
import os
from pydantic import ValidationError

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

from app.db.base import SessionLocal
from app.models import models
from app.schemas import schemas

def exhaustive_debug():
    db = SessionLocal()
    try:
        ps = db.query(models.Purchase).all()
        print(f"Total purchases in DB: {len(ps)}")
        
        for i, p in enumerate(ps):
            print(f"\n--- Checking Purchase {i} ({p.purchase_id}) ---")
            print(f"  Field values in object:")
            print(f"    quantity: {p.quantity} (type: {type(p.quantity)})")
            print(f"    total_amount: {p.total_amount}")
            print(f"    grand_total: {p.grand_total}")
            print(f"    balance: {p.balance}")
            
            try:
                schemas.Purchase.model_validate(p)
                print(f"  Result: OK")
            except ValidationError as e:
                print(f"  Result: ERROR")
                for error in e.errors():
                    print(f"    {error['loc']}: {error['msg']} (input={error.get('input')})")
                    
        ss = db.query(models.Sale).all()
        print(f"\nTotal sales in DB: {len(ss)}")
        for i, s in enumerate(ss):
            print(f"\n--- Checking Sale {i} ({s.sales_id}) ---")
            try:
                schemas.Sale.model_validate(s)
                print(f"  Result: OK")
            except ValidationError as e:
                print(f"  Result: ERROR")
                for error in e.errors():
                    print(f"    {error['loc']}: {error['msg']} (input={error.get('input')})")

    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    exhaustive_debug()
