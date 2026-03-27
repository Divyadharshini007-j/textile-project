import sys
import os
import uuid
from datetime import datetime, timedelta

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.db.base import SessionLocal, engine, Base
from app.models import models

def seed_data():
    db = SessionLocal()
    try:
        # 1. Clear existing data (optional, but good for a fresh start)
        db.query(models.Sale).delete()
        db.query(models.Purchase).delete()
        db.query(models.Expense).delete()
        db.query(models.Inventory).delete()
        db.query(models.Customer).delete()
        db.query(models.Supplier).delete()
        db.commit()

        # 2. Add Suppliers
        suppliers = [
            models.Supplier(
                supplier_id="SUP001",
                supplier_name="Cotton Mills Ltd",
                contact_person="Rajesh Kumar",
                phone="9876543210",
                email="contact@cottonmills.com",
                gstin="33AAAAA0000A1Z1",
                address="Coimbatore, Tamil Nadu",
                payment_terms="NET 30"
            ),
            models.Supplier(
                supplier_id="SUP002",
                supplier_name="Global Yarns",
                contact_person="Anita Rao",
                phone="9876543211",
                email="sales@globalyarns.com",
                gstin="33BBBBB1111B1Z2",
                address="Salem, Tamil Nadu",
                payment_terms="Immediate"
            )
        ]
        db.add_all(suppliers)

        # 3. Add Customers
        customers = [
            models.Customer(
                customer_id="CUS001",
                customer_name="Trendsetters Apparels",
                contact_person="Vikas Singh",
                phone="9988776655",
                email="info@trendsetters.com",
                gstin="33CCCCC2222C1Z3",
                address="Tirupur, Tamil Nadu",
                city="Tirupur",
                country="India"
            ),
            models.Customer(
                customer_id="CUS002",
                customer_name="Elite Textiles",
                contact_person="Lakshmi Narayanan",
                phone="9988776654",
                email="admin@elitetextiles.com",
                gstin="33DDDDD3333D1Z4",
                address="Madurai, Tamil Nadu",
                city="Madurai",
                country="India"
            )
        ]
        db.add_all(customers)

        # 4. Add Inventory (Initial Stock)
        inventory_items = [
            models.Inventory(
                inventory_id=str(uuid.uuid4()),
                item_name="Cotton Yarn 40s",
                item_type="Yarn",
                item_category="Raw Material",
                unit="KG",
                opening_stock=5000,
                stock_in=0,
                stock_out=0,
                closing_stock=5000,
                unit_cost=280.0,
                total_value=5000 * 280.0
            ),
            models.Inventory(
                inventory_id=str(uuid.uuid4()),
                item_name="Polyester Yarn",
                item_type="Yarn",
                item_category="Raw Material",
                unit="KG",
                opening_stock=2000,
                stock_in=0,
                stock_out=0,
                closing_stock=2000,
                unit_cost=150.0,
                total_value=2000 * 150.0
            )
        ]
        db.add_all(inventory_items)
        db.commit()

        # 5. Add Purchases
        p1_qty = 1000
        p1_rate = 285.0
        p1_total = p1_qty * p1_rate
        purchase1 = models.Purchase(
            purchase_id=str(uuid.uuid4()),
            supplier_id="SUP001",
            invoice_number="INV-PUR-001",
            date=datetime.now() - timedelta(days=5),
            yarn_type="Cotton Yarn 40s",
            quantity=p1_qty,
            unit="KG",
            rate=p1_rate,
            total_amount=p1_total,
            grand_total=p1_total,
            payment_status="Paid",
            paid_amount=p1_total,
            balance=0.0
        )
        # Update inventory for p1
        item1 = db.query(models.Inventory).filter(models.Inventory.item_name == "Cotton Yarn 40s").first()
        item1.stock_in += p1_qty
        item1.closing_stock += p1_qty
        item1.total_value = item1.closing_stock * item1.unit_cost

        db.add(purchase1)

        # 6. Add Sales
        s1_qty = 500
        s1_rate = 320.0
        s1_total = s1_qty * s1_rate
        sale1 = models.Sale(
            sales_id=str(uuid.uuid4()),
            customer_id="CUS001",
            invoice_number="INV-SAL-001",
            date=datetime.now() - timedelta(days=2),
            product_name="Cotton Yarn 40s",
            product_type="Yarn",
            quantity=s1_qty,
            unit="KG",
            rate=s1_rate,
            total_amount=s1_total,
            grand_total=s1_total,
            payment_status="Unpaid",
            paid_amount=0.0,
            balance=s1_total
        )
        # Update inventory for s1
        item1.stock_out += s1_qty
        item1.closing_stock -= s1_qty
        item1.total_value = item1.closing_stock * item1.unit_cost

        db.add(sale1)

        # 7. Add Expenses
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
            )
        ]
        db.add_all(expenses)

        db.commit()
        print("Sample data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
