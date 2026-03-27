import sys
import os
from sqlalchemy import func

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

from app.db.base import SessionLocal
from app.models import models

def audit_data():
    db = SessionLocal()
    try:
        print("=== DATABASE INTEGRITY AUDIT ===\n")

        # 1. Row Counts
        tables = {
            "Users": models.User,
            "Suppliers": models.Supplier,
            "Customers": models.Customer,
            "Purchases": models.Purchase,
            "Sales": models.Sale,
            "Expenses": models.Expense,
            "Inventory": models.Inventory,
            "Conversions": models.Conversion
        }

        print("--- Table Statistics ---")
        for name, model in tables.items():
            count = db.query(func.count("*")).select_from(model).scalar()
            print(f"{name:12}: {count} records")

        # 2. Financial Audit: Purchases
        print("\n--- Purchase Calculations Audit ---")
        purchases = db.query(models.Purchase).all()
        p_errors = 0
        for p in purchases:
            expected_tax = (p.cgst or 0) + (p.sgst or 0) + (p.igst or 0)
            if abs((p.tax_amount or 0) - expected_tax) > 0.01:
                print(f"  [ERR] P-{p.invoice_number}: Tax amount mismatch. {p.tax_amount} != {expected_tax}")
                p_errors += 1
            if abs(p.grand_total - (p.total_amount + (p.tax_amount or 0))) > 0.01:
                print(f"  [ERR] P-{p.invoice_number}: Grand total mismatch. {p.grand_total} != {p.total_amount + p.tax_amount}")
                p_errors += 1
            if abs(p.balance - (p.grand_total - p.paid_amount)) > 0.01:
                print(f"  [ERR] P-{p.invoice_number}: Balance mismatch. {p.balance} != {p.grand_total - p.paid_amount}")
                p_errors += 1
        print(f"Purchase Audit Complete. Errors found: {p_errors}")

        # 3. Financial Audit: Sales
        print("\n--- Sales Calculations Audit ---")
        sales = db.query(models.Sale).all()
        s_errors = 0
        for s in sales:
            expected_tax = (s.cgst or 0) + (s.sgst or 0) + (s.igst or 0)
            if abs((s.tax_amount or 0) - expected_tax) > 0.01:
                print(f"  [ERR] S-{s.invoice_number}: Tax amount mismatch. {s.tax_amount} != {expected_tax}")
                s_errors += 1
            if abs(s.grand_total - (s.total_amount + (s.tax_amount or 0))) > 0.01:
                print(f"  [ERR] S-{s.invoice_number}: Grand total mismatch. {s.grand_total} != {s.total_amount + s.tax_amount}")
                s_errors += 1
            if abs(s.balance - (s.grand_total - s.paid_amount)) > 0.01:
                print(f"  [ERR] S-{s.invoice_number}: Balance mismatch. {s.balance} != {s.grand_total - s.paid_amount}")
                s_errors += 1
        print(f"Sales Audit Complete. Errors found: {s_errors}")

        # 4. Inventory Audit
        print("\n--- Inventory Consistency Audit ---")
        items = db.query(models.Inventory).all()
        i_errors = 0
        for item in items:
            expected_closing = item.opening_stock + item.stock_in - item.stock_out
            if abs(item.closing_stock - expected_closing) > 0.01:
                print(f"  [ERR] {item.item_name}: Closing stock mismatch. {item.closing_stock} != {expected_closing}")
                i_errors += 1
            # Check total value logic
            expected_value = item.closing_stock * item.unit_cost
            if abs(item.total_value - expected_value) > 0.1: # Allow small rounding
                 print(f"  [NOTE] {item.item_name}: Value might need update. Current: {item.total_value}, Calculated: {expected_value}")
        print(f"Inventory Audit Complete. Critical Errors found: {i_errors}")

        # 5. Conversion Audit
        print("\n--- Conversion Audit ---")
        conversions = db.query(models.Conversion).all()
        if not conversions:
             print("  [WARN] No conversion records found!")
        for c in conversions:
             print(f"  [OK] Found conversion: {c.input_yarn_type} -> {c.output_product} ({c.output_quantity})")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Audit failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    audit_data()
