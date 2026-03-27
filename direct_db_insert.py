#!/usr/bin/env python3
"""
Direct database insertion of sample records
"""
import sys
import os
from datetime import datetime, timedelta
import random
import uuid

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.base import engine, Base
from app.models import models
from sqlalchemy.orm import sessionmaker

def create_sample_records_directly():
    """Insert sample records directly into database"""
    
    print("🏭 INSERTING SAMPLE RECORDS DIRECTLY INTO DATABASE")
    print("=" * 60)
    
    # Create database session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Standard yarn types
        yarn_types = ["Cotton Yarn 40", "Polyester Yarn"]
        
        # Clear existing data
        print("🗑️ Clearing existing data...")
        db.query(models.Purchase).delete()
        db.query(models.Sale).delete()
        db.query(models.Expense).delete()
        db.query(models.Conversion).delete()
        db.query(models.Inventory).delete()
        db.query(models.Customer).delete()
        db.query(models.Supplier).delete()
        db.commit()
        print("✅ Existing data cleared")
        
        # Insert Suppliers
        print("\n📦 INSERTING SUPPLIERS...")
        suppliers_data = [
            {
                "supplier_id": str(uuid.uuid4()),
                "supplier_name": "Mumbai Textile Mills",
                "contact_person": "Rajesh Kumar",
                "address": "123 Industrial Area, Mumbai, Maharashtra 400001",
                "phone": "9876543210",
                "email": "rajesh@mumbaitextile.com",
                "gstin": "27AAAAA0000A1Z1",
                "payment_terms": "NET 30",
                "opening_balance": 0.0,
                "status": "Active"
            },
            {
                "supplier_id": str(uuid.uuid4()),
                "supplier_name": "Delhi Fabric Suppliers",
                "contact_person": "Amit Singh",
                "address": "456 Market Complex, Delhi, Delhi 110001",
                "phone": "9876543211",
                "email": "amit@delhifabric.com",
                "gstin": "07BBBBB0000B1Z1",
                "payment_terms": "NET 45",
                "opening_balance": 0.0,
                "status": "Active"
            },
            {
                "supplier_id": str(uuid.uuid4()),
                "supplier_name": "Bangalore Yarn Co",
                "contact_person": "Priya Sharma",
                "address": "789 Tech Park, Bangalore, Karnataka 560001",
                "phone": "9876543212",
                "email": "priya@bangalorerarn.com",
                "gstin": "29CCCCC0000C1Z1",
                "payment_terms": "NET 60",
                "opening_balance": 0.0,
                "status": "Active"
            },
            {
                "supplier_id": str(uuid.uuid4()),
                "supplier_name": "Chennai Cotton Traders",
                "contact_person": "Karthik R",
                "address": "321 Port Area, Chennai, Tamil Nadu 600001",
                "phone": "9876543213",
                "email": "karthik@chennaitraders.com",
                "gstin": "33DDDDD0000D1Z1",
                "payment_terms": "NET 30",
                "opening_balance": 0.0,
                "status": "Active"
            }
        ]
        
        for supplier_data in suppliers_data:
            supplier = models.Supplier(**supplier_data)
            db.add(supplier)
        db.commit()
        print(f"✅ {len(suppliers_data)} suppliers inserted")
        
        # Insert Customers
        print("\n👥 INSERTING CUSTOMERS...")
        customers_data = [
            {
                "customer_id": str(uuid.uuid4()),
                "customer_name": "Fashion Garments Ltd",
                "contact_person": "Sanjay Reddy",
                "address": "111 Business Park, Hyderabad, Telangana 500001",
                "city": "Hyderabad",
                "country": "India",
                "phone": "9876543201",
                "email": "sanjay@fashiongarments.com",
                "gstin": "36EEEEE0000E1Z1",
                "credit_limit": 100000.0,
                "opening_balance": 0.0,
                "status": "Active"
            },
            {
                "customer_id": str(uuid.uuid4()),
                "customer_name": "Textile Exporters Inc",
                "contact_person": "Anita Patel",
                "address": "222 Export Zone, Ahmedabad, Gujarat 380001",
                "city": "Ahmedabad",
                "country": "India",
                "phone": "9876543202",
                "email": "anita@textileexporters.com",
                "gstin": "24FFFFF0000F1Z1",
                "credit_limit": 150000.0,
                "opening_balance": 0.0,
                "status": "Active"
            },
            {
                "customer_id": str(uuid.uuid4()),
                "customer_name": "Premium Clothing Co",
                "contact_person": "Vikram Malhotra",
                "address": "333 Fashion Street, Chennai, Tamil Nadu 600001",
                "city": "Chennai",
                "country": "India",
                "phone": "9876543203",
                "email": "vikram@premiumclothing.com",
                "gstin": "33GGGGG0000G1Z1",
                "credit_limit": 75000.0,
                "opening_balance": 0.0,
                "status": "Active"
            },
            {
                "customer_id": str(uuid.uuid4()),
                "customer_name": "Urban Wear Factory",
                "contact_person": "Meera Joshi",
                "address": "444 Industrial Estate, Pune, Maharashtra 411001",
                "city": "Pune",
                "country": "India",
                "phone": "9876543204",
                "email": "meera@urbanwear.com",
                "gstin": "27HHHHH0000H1Z1",
                "credit_limit": 50000.0,
                "opening_balance": 0.0,
                "status": "Active"
            }
        ]
        
        for customer_data in customers_data:
            customer = models.Customer(**customer_data)
            db.add(customer)
        db.commit()
        print(f"✅ {len(customers_data)} customers inserted")
        
        # Insert Inventory
        print("\n📊 INSERTING INVENTORY...")
        inventory_data = [
            {
                "inventory_id": str(uuid.uuid4()),
                "item_name": "Cotton Yarn 40",
                "item_type": "Yarn",
                "item_category": "Raw Material",
                "unit": "KG",
                "opening_stock": 1500,
                "stock_in": 0,
                "stock_out": 0,
                "closing_stock": 1500,
                "unit_cost": 250.0
            },
            {
                "inventory_id": str(uuid.uuid4()),
                "item_name": "Polyester Yarn",
                "item_type": "Yarn",
                "item_category": "Raw Material",
                "unit": "KG",
                "opening_stock": 1200,
                "stock_in": 0,
                "stock_out": 0,
                "closing_stock": 1200,
                "unit_cost": 180.0
            }
        ]
        
        for item_data in inventory_data:
            inventory = models.Inventory(**item_data)
            db.add(inventory)
        db.commit()
        print(f"✅ {len(inventory_data)} inventory items inserted")
        
        # Insert Purchases
        print("\n💰 INSERTING PURCHASES...")
        purchases_count = 0
        for i in range(15):
            purchase_date = datetime.now() - timedelta(days=random.randint(1, 60))
            yarn_type = random.choice(yarn_types)
            quantity = random.randint(100, 800)
            rate = random.uniform(240, 280) if yarn_type == "Cotton Yarn 40" else random.uniform(170, 200)
            total_amount = quantity * rate
            
            purchase = models.Purchase(
                purchase_id=str(uuid.uuid4()),
                supplier_id=random.choice(suppliers_data)["supplier_name"],
                invoice_number=f"PUR{2026}{str(i+1).zfill(3)}",
                date=purchase_date,
                yarn_type=yarn_type,
                quantity=quantity,
                unit="KG",
                rate=round(rate, 2),
                total_amount=round(total_amount, 2),
                cgst=0,
                sgst=0,
                igst=0,
                tax_amount=0,
                grand_total=round(total_amount, 2),
                payment_status=random.choice(["Paid", "Unpaid", "Partial"]),
                paid_amount=round(total_amount * random.uniform(0.3, 1.0), 2),
                balance=0,
                remarks=f"Purchase order {i+1}"
            )
            db.add(purchase)
            purchases_count += 1
            
        db.commit()
        print(f"✅ {purchases_count} purchases inserted")
        
        # Insert Sales
        print("\n🛍️ INSERTING SALES...")
        sales_count = 0
        for i in range(12):
            sale_date = datetime.now() - timedelta(days=random.randint(1, 45))
            yarn_type = random.choice(yarn_types)
            quantity = random.randint(50, 400)
            rate = random.uniform(300, 380) if yarn_type == "Cotton Yarn 40" else random.uniform(220, 280)
            total_amount = quantity * rate
            
            sale = models.Sale(
                sales_id=str(uuid.uuid4()),
                customer_id=random.choice(customers_data)["customer_name"],
                invoice_number=f"SAL{2026}{str(i+1).zfill(3)}",
                date=sale_date,
                product_name=yarn_type,
                product_type="Yarn",
                quantity=quantity,
                unit="KG",
                rate=round(rate, 2),
                total_amount=round(total_amount, 2),
                cgst=0,
                sgst=0,
                igst=0,
                tax_amount=0,
                grand_total=round(total_amount, 2),
                payment_status=random.choice(["Paid", "Unpaid", "Partial"]),
                paid_amount=round(total_amount * random.uniform(0.4, 1.0), 2),
                balance=0,
                remarks=f"Sale order {i+1}"
            )
            db.add(sale)
            sales_count += 1
            
        db.commit()
        print(f"✅ {sales_count} sales inserted")
        
        # Insert Expenses
        print("\n💸 INSERTING EXPENSES...")
        expense_categories = ["Electricity", "Water", "Rent", "Salaries", "Transport", "Maintenance", "Office Supplies", "Insurance"]
        expenses_count = 0
        for i in range(8):
            expense_date = datetime.now() - timedelta(days=random.randint(1, 30))
            amount = random.uniform(5000, 45000)
            
            expense = models.Expense(
                expense_id=str(uuid.uuid4()),
                expense_type="Operating",
                category=random.choice(expense_categories),
                amount=round(amount, 2),
                date=expense_date,
                description=f"Monthly {random.choice(expense_categories).lower()} payment",
                vendor_name=random.choice(["City Municipal Corp", "State Electricity Board", "Property Management", "Staff Payroll"]),
                bill_number=f"EXP{2026}{str(i+1).zfill(3)}",
                payment_mode=random.choice(["Cash", "Bank Transfer", "Cheque", "UPI"]),
                payment_reference=f"TXN{random.randint(100000, 999999)}",
                remarks=f"Monthly expense {i+1}",
                created_by="Admin"
            )
            db.add(expense)
            expenses_count += 1
            
        db.commit()
        print(f"✅ {expenses_count} expenses inserted")
        
        # Insert Conversions
        print("\n🔄 INSERTING CONVERSIONS...")
        conversions_count = 0
        for i in range(6):
            conversion_date = datetime.now() - timedelta(days=random.randint(1, 20))
            input_qty = random.randint(100, 400)
            wastage_pct = random.uniform(10, 20)
            output_qty = int(input_qty * (1 - wastage_pct/100))
            input_cost = random.uniform(240, 280) if random.choice(yarn_types) == "Cotton Yarn 40" else random.uniform(170, 200)
            labor_cost = random.uniform(2000, 5000)
            overhead_cost = random.uniform(1000, 3000)
            total_cost = input_cost * input_qty + labor_cost + overhead_cost
            
            conversion = models.Conversion(
                conversion_id=str(uuid.uuid4()),
                date=conversion_date,
                input_yarn_type=random.choice(yarn_types),
                input_quantity=input_qty,
                input_cost=round(input_cost, 2),
                output_product="Processed Yarn",
                output_quantity=output_qty,
                labor_cost=round(labor_cost, 2),
                overhead_cost=round(overhead_cost, 2),
                total_conversion_cost=round(total_cost, 2),
                wastage=round(wastage_pct, 1),
                remarks=f"Conversion batch {i+1}"
            )
            db.add(conversion)
            conversions_count += 1
            
        db.commit()
        print(f"✅ {conversions_count} conversions inserted")
        
        # Summary
        print("\n🎉 SAMPLE DATA INSERTION COMPLETE!")
        print("=" * 60)
        print(f"✅ Suppliers: {len(suppliers_data)} inserted")
        print(f"✅ Customers: {len(customers_data)} inserted")
        print(f"✅ Inventory: {len(inventory_data)} inserted")
        print(f"✅ Purchases: {purchases_count} inserted")
        print(f"✅ Sales: {sales_count} inserted")
        print(f"✅ Expenses: {expenses_count} inserted")
        print(f"✅ Conversions: {conversions_count} inserted")
        
        total_records = len(suppliers_data) + len(customers_data) + len(inventory_data) + purchases_count + sales_count + expenses_count + conversions_count
        print(f"\n📊 TOTAL RECORDS INSERTED: {total_records}")
        
        print("\n🎯 DASHBOARD WILL NOW SHOW:")
        print("📈 Real-time KPIs based on actual data")
        print("💰 Financial statistics from purchases/sales")
        print("📦 Inventory levels from stock movements")
        print("👥 Customer/supplier activity metrics")
        print("📊 Revenue and expense analytics")
        print("🔄 Dynamic updates when data changes")
        
        print("\n🌐 ACCESS YOUR DASHBOARD:")
        print("🔗 http://localhost:5173")
        print("👤 Login: admin / admin123")
        print("📊 Dashboard will show accurate statistics!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_records_directly()
