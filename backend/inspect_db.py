import sys
import os
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from app.db.base import SessionLocal
from app.models import models

def inspect_db():
    db = SessionLocal()
    try:
        p_count = db.query(models.Purchase).count()
        s_count = db.query(models.Sale).count()
        e_count = db.query(models.Expense).count()
        c_count = db.query(models.Customer).count()
        sup_count = db.query(models.Supplier).count()
        inv_count = db.query(models.Inventory).count()
        
        print(f"Purchases: {p_count}")
        print(f"Sales: {s_count}")
        print(f"Expenses: {e_count}")
        print(f"Customers: {c_count}")
        print(f"Suppliers: {sup_count}")
        print(f"Inventory: {inv_count}")
        
        if p_count > 0:
            p = db.query(models.Purchase).first()
            print(f"First Purchase: {p.invoice_number} - {p.yarn_type}")
            
        if s_count > 0:
            s = db.query(models.Sale).first()
            print(f"First Sale: {s.invoice_number} - {s.product_name}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inspect_db()
