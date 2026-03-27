import os
import uuid
import sys
from datetime import datetime, timedelta

# This script should be run from the backend directory
from app.db.base import SessionLocal, Base
from app.models import models

def seed_data():
    db = SessionLocal()
    try:
        print("Starting seed process...")
        # 1. Clear existing data
        db.query(models.Sale).delete()
        db.query(models.Purchase).delete()
        db.query(models.Expense).delete()
        db.query(models.Inventory).delete()
        db.query(models.Customer).delete()
        db.query(models.Supplier).delete()
        db.query(models.Conversion).delete()
        db.commit()
        print("Cleared existing data.")

        # 2. Add Suppliers
        supplier = models.Supplier(
            supplier_id="SUP001",
            supplier_name="Cotton Mills Ltd",
            contact_person="Rajesh Kumar",
            phone="9876543210",
            email="contact@cottonmills.com",
            gstin="33AAAAA0000A1Z1",
            address="Coimbatore, Tamil Nadu",
            payment_terms="NET 30"
        )
        db.add(supplier)
        print("Added supplier.")

        # 3. Add Customers
        customer = models.Customer(
            customer_id="CUS001",
            customer_name="Trendsetters Apparels",
            contact_person="Vikas Singh",
            phone="9988776655",
            email="info@trendsetters.com",
            gstin="33CCCCC2222C1Z3",
            address="Tirupur, Tamil Nadu",
            city="Tirupur",
            country="India"
        )
        db.add(customer)
        print("Added customer.")

        # 4. Add Purchases (and history for ML)
        purchase_records = []
        # Cotton Yarn history (12 months)
        for i in range(12):
            month_date = datetime.now() - timedelta(days=30*i + 15)
            rate = 270.0 + (i * 2.5)
            qty = 500.0
            purchase_records.append(models.Purchase(
                purchase_id=str(uuid.uuid4()),
                supplier_id=supplier.supplier_id,
                invoice_number=f"PUR-{202400+i}",
                date=month_date,
                yarn_type="Cotton Yarn 40s",
                quantity=qty,
                unit="KG",
                rate=rate,
                total_amount=qty * rate,
                cgst=0.0, sgst=0.0, igst=0.0, tax_amount=0.0,
                grand_total=qty * rate,
                payment_status="Paid",
                paid_amount=qty * rate,
                balance=0.0,
                remarks=f"Historical stock - Month {i+1}"
            ))
        
        # Polyester Purchase
        purchase_records.append(models.Purchase(
            purchase_id=str(uuid.uuid4()),
            supplier_id=supplier.supplier_id,
            invoice_number="PUR-POLY-01",
            date=datetime.now() - timedelta(days=5),
            yarn_type="Polyester Yarn",
            quantity=1000.0,
            unit="KG",
            rate=180.0,
            total_amount=180000.0,
            cgst=9000.0, sgst=9000.0, igst=0.0, tax_amount=18000.0,
            grand_total=198000.0,
            payment_status="Partial",
            paid_amount=100000.0,
            balance=98000.0,
            remarks="Initial polyester stock"
        ))
        db.add_all(purchase_records)
        print("Added purchases.")

        # 5. Add Sales
        sale_records = [
            models.Sale(
                sales_id=str(uuid.uuid4()),
                customer_id=customer.customer_id,
                invoice_number="SAL-001",
                date=datetime.now() - timedelta(days=2),
                product_name="Cotton Fabric",
                product_type="Finished Product",
                quantity=100.0,
                unit="Units",
                rate=450.0,
                total_amount=45000.0,
                cgst=2250.0, sgst=2250.0, igst=0.0, tax_amount=4500.0,
                grand_total=49500.0,
                payment_status="Unpaid",
                paid_amount=0.0,
                balance=49500.0,
                remarks="Bulk fabric sale"
            ),
            models.Sale(
                sales_id=str(uuid.uuid4()),
                customer_id=customer.customer_id,
                invoice_number="SAL-002",
                date=datetime.now() - timedelta(days=1),
                product_name="Polyester Yarn",
                product_type="Yarn",
                quantity=600.0,
                unit="KG",
                rate=250.0,
                total_amount=150000.0,
                cgst=0.0, sgst=0.0, igst=27000.0, tax_amount=27000.0,
                grand_total=177000.0,
                payment_status="Paid",
                paid_amount=177000.0,
                balance=0.0,
                remarks="Direct yarn trading scale"
            )
        ]
        db.add_all(sale_records)
        print("Added sales.")

        # 6. Add Expenses
        expenses = [
            models.Expense(
                expense_id=str(uuid.uuid4()),
                expense_type="Warehouse Rent",
                category="Indirect",
                amount=15000.0,
                date=datetime.now() - timedelta(days=10),
                description="Monthly rent for main warehouse",
                payment_mode="Bank"
            ),
            models.Expense(
                expense_id=str(uuid.uuid4()),
                expense_type="Electricity Bill",
                category="Indirect",
                amount=4500.0,
                date=datetime.now() - timedelta(days=3),
                description="Factory power usage",
                payment_mode="UPI"
            ),
            models.Expense(
                expense_id=str(uuid.uuid4()),
                expense_type="Packing Charges",
                category="Direct",
                amount=1200.0,
                date=datetime.now() - timedelta(days=1),
                description="Carton boxes and tape",
                payment_mode="Cash"
            )
        ]
        db.add_all(expenses)
        print("Added expenses.")

        # 7. Add Conversions
        conversion1 = models.Conversion(
            conversion_id=str(uuid.uuid4()),
            date=datetime.now() - timedelta(days=7),
            input_yarn_type="Cotton Yarn 40s",
            input_quantity=200.0,
            input_cost=280.0,
            output_product="Cotton Fabric",
            output_quantity=190.0,
            labor_cost=5000.0,
            overhead_cost=2000.0,
            total_conversion_cost=7000.0,
            wastage=5.0,
            remarks="Batch 101 - Good quality"
        )
        db.add(conversion1)
        print("Added conversion.")

        # 8. Inventory reconciliation
        total_cotton_in = 12 * 500.0
        total_cotton_out = 200.0
        
        inventory_items = [
            models.Inventory(
                inventory_id=str(uuid.uuid4()),
                item_name="Cotton Yarn 40s",
                item_type="Yarn",
                item_category="Raw Material",
                unit="KG",
                opening_stock=0.0,
                stock_in=total_cotton_in,
                stock_out=total_cotton_out,
                closing_stock=total_cotton_in - total_cotton_out,
                unit_cost=285.0,
                total_value=(total_cotton_in - total_cotton_out) * 285.0
            ),
            models.Inventory(
                inventory_id=str(uuid.uuid4()),
                item_name="Polyester Yarn",
                item_type="Yarn",
                item_category="Raw Material",
                unit="KG",
                opening_stock=0.0,
                stock_in=1000.0,
                stock_out=600.0,
                closing_stock=400.0,
                unit_cost=180.0,
                total_value=400.0 * 180.0
            ),
            models.Inventory(
                inventory_id=str(uuid.uuid4()),
                item_name="Cotton Fabric",
                item_type="Finished Product",
                item_category="Fabric",
                unit="Units",
                opening_stock=0.0,
                stock_in=190.0,
                stock_out=100.0,
                closing_stock=90.0,
                unit_cost=350.0,
                total_value=90.0 * 350.0
            )
        ]
        db.add_all(inventory_items)
        print("Added inventory items.")

        db.commit()
        print("Sample data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
