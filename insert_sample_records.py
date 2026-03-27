#!/usr/bin/env python3
"""
Insert comprehensive sample records into all features for accurate dashboard statistics
"""
import requests
import json
from datetime import datetime, timedelta
import random
import uuid

def insert_sample_records():
    """Insert realistic sample records for all features"""
    
    print("🏭 INSERTING COMPREHENSIVE SAMPLE RECORDS")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000/api"
    
    # Standard yarn types
    yarn_types = ["Cotton Yarn 40", "Polyester Yarn"]
    
    # Sample suppliers data
    suppliers_data = [
        {
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
    
    # Sample customers data
    customers_data = [
        {
            "customer_name": "Fashion Garments Ltd",
            "contact_person": "Sanjay Reddy",
            "address": "111 Business Park, Hyderabad, Telangana 500001",
            "phone": "9876543201",
            "email": "sanjay@fashiongarments.com",
            "gstin": "36EEEEE0000E1Z1",
            "payment_terms": "NET 30",
            "opening_balance": 0.0,
            "status": "Active"
        },
        {
            "customer_name": "Textile Exporters Inc",
            "contact_person": "Anita Patel",
            "address": "222 Export Zone, Ahmedabad, Gujarat 380001",
            "phone": "9876543202",
            "email": "anita@textileexporters.com",
            "gstin": "24FFFFF0000F1Z1",
            "payment_terms": "NET 45",
            "opening_balance": 0.0,
            "status": "Active"
        },
        {
            "customer_name": "Premium Clothing Co",
            "contact_person": "Vikram Malhotra",
            "address": "333 Fashion Street, Chennai, Tamil Nadu 600001",
            "phone": "9876543203",
            "email": "vikram@premiumclothing.com",
            "gstin": "33GGGGG0000G1Z1",
            "payment_terms": "NET 30",
            "opening_balance": 0.0,
            "status": "Active"
        },
        {
            "customer_name": "Urban Wear Factory",
            "contact_person": "Meera Joshi",
            "address": "444 Industrial Estate, Pune, Maharashtra 411001",
            "phone": "9876543204",
            "email": "meera@urbanwear.com",
            "gstin": "27HHHHH0000H1Z1",
            "payment_terms": "NET 60",
            "opening_balance": 0.0,
            "status": "Active"
        }
    ]
    
    # Sample inventory items
    inventory_data = [
        {
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
    
    try:
        success_count = {"suppliers": 0, "customers": 0, "inventory": 0, "purchases": 0, "sales": 0, "expenses": 0, "conversions": 0}
        
        # 1. Insert Suppliers
        print("\n📦 INSERTING SUPPLIERS...")
        for supplier in suppliers_data:
            try:
                response = requests.post(f"{base_url}/suppliers/", json=supplier)
                if response.status_code == 200:
                    success_count["suppliers"] += 1
                    print(f"✅ Added: {supplier['supplier_name']}")
                else:
                    print(f"❌ Failed: {supplier['supplier_name']} - {response.status_code}")
            except Exception as e:
                print(f"❌ Error adding supplier: {e}")
        
        # 2. Insert Customers
        print("\n👥 INSERTING CUSTOMERS...")
        for customer in customers_data:
            try:
                response = requests.post(f"{base_url}/customers/", json=customer)
                if response.status_code == 200:
                    success_count["customers"] += 1
                    print(f"✅ Added: {customer['customer_name']}")
                else:
                    print(f"❌ Failed: {customer['customer_name']} - {response.status_code}")
            except Exception as e:
                print(f"❌ Error adding customer: {e}")
        
        # 3. Insert Inventory
        print("\n📊 INSERTING INVENTORY...")
        for item in inventory_data:
            try:
                response = requests.post(f"{base_url}/inventory/", json=item)
                if response.status_code == 200:
                    success_count["inventory"] += 1
                    print(f"✅ Added: {item['item_name']}")
                else:
                    print(f"❌ Failed: {item['item_name']} - {response.status_code}")
            except Exception as e:
                print(f"❌ Error adding inventory: {e}")
        
        # 4. Insert Purchases (15 records over last 60 days)
        print("\n💰 INSERTING PURCHASES...")
        for i in range(15):
            try:
                purchase_date = datetime.now() - timedelta(days=random.randint(1, 60))
                yarn_type = random.choice(yarn_types)
                quantity = random.randint(100, 800)
                rate = random.uniform(240, 280) if yarn_type == "Cotton Yarn 40" else random.uniform(170, 200)
                total_amount = quantity * rate
                
                purchase = {
                    "supplier_id": random.choice(suppliers_data)["supplier_name"],
                    "invoice_number": f"PUR{2026}{str(i+1).zfill(3)}",
                    "date": purchase_date.isoformat(),
                    "yarn_type": yarn_type,
                    "quantity": quantity,
                    "unit": "KG",
                    "rate": round(rate, 2),
                    "total_amount": round(total_amount, 2),
                    "cgst": 0,
                    "sgst": 0,
                    "igst": 0,
                    "tax_amount": 0,
                    "grand_total": round(total_amount, 2),
                    "payment_status": random.choice(["Paid", "Unpaid", "Partial"]),
                    "paid_amount": round(total_amount * random.uniform(0.3, 1.0), 2),
                    "balance": 0,
                    "remarks": f"Purchase order {i+1}"
                }
                
                response = requests.post(f"{base_url}/purchases/", json=purchase)
                if response.status_code == 200:
                    success_count["purchases"] += 1
                    print(f"✅ Purchase {i+1}: {yarn_type} - {quantity}KG - ₹{total_amount:,.0f}")
                else:
                    print(f"❌ Purchase {i+1} failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Error adding purchase {i+1}: {e}")
        
        # 5. Insert Sales (12 records over last 45 days)
        print("\n🛍️ INSERTING SALES...")
        for i in range(12):
            try:
                sale_date = datetime.now() - timedelta(days=random.randint(1, 45))
                yarn_type = random.choice(yarn_types)
                quantity = random.randint(50, 400)
                rate = random.uniform(300, 380) if yarn_type == "Cotton Yarn 40" else random.uniform(220, 280)
                total_amount = quantity * rate
                
                sale = {
                    "customer_id": random.choice(customers_data)["customer_name"],
                    "invoice_number": f"SAL{2026}{str(i+1).zfill(3)}",
                    "date": sale_date.isoformat(),
                    "product_name": yarn_type,
                    "product_type": "Yarn",
                    "quantity": quantity,
                    "unit": "KG",
                    "rate": round(rate, 2),
                    "total_amount": round(total_amount, 2),
                    "cgst": 0,
                    "sgst": 0,
                    "igst": 0,
                    "tax_amount": 0,
                    "grand_total": round(total_amount, 2),
                    "payment_status": random.choice(["Paid", "Unpaid", "Partial"]),
                    "paid_amount": round(total_amount * random.uniform(0.4, 1.0), 2),
                    "balance": 0,
                    "remarks": f"Sale order {i+1}"
                }
                
                response = requests.post(f"{base_url}/sales/", json=sale)
                if response.status_code == 200:
                    success_count["sales"] += 1
                    print(f"✅ Sale {i+1}: {yarn_type} - {quantity}KG - ₹{total_amount:,.0f}")
                else:
                    print(f"❌ Sale {i+1} failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Error adding sale {i+1}: {e}")
        
        # 6. Insert Expenses (8 records)
        print("\n💸 INSERTING EXPENSES...")
        expense_categories = ["Electricity", "Water", "Rent", "Salaries", "Transport", "Maintenance", "Office Supplies", "Insurance"]
        for i in range(8):
            try:
                expense_date = datetime.now() - timedelta(days=random.randint(1, 30))
                amount = random.uniform(5000, 45000)
                
                expense = {
                    "category": random.choice(expense_categories),
                    "amount": round(amount, 2),
                    "date": expense_date.isoformat(),
                    "description": f"Monthly {random.choice(expense_categories).lower()} payment",
                    "payment_mode": random.choice(["Cash", "Bank Transfer", "Cheque", "UPI"]),
                    "receipt_number": f"EXP{2026}{str(i+1).zfill(3)}",
                    "approved_by": "Admin",
                    "status": "Approved"
                }
                
                response = requests.post(f"{base_url}/expenses/", json=expense)
                if response.status_code == 200:
                    success_count["expenses"] += 1
                    print(f"✅ Expense {i+1}: {expense['category']} - ₹{amount:,.0f}")
                else:
                    print(f"❌ Expense {i+1} failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Error adding expense {i+1}: {e}")
        
        # 7. Insert Conversions (6 records)
        print("\n🔄 INSERTING CONVERSIONS...")
        for i in range(6):
            try:
                conversion_date = datetime.now() - timedelta(days=random.randint(1, 20))
                input_qty = random.randint(100, 400)
                wastage_pct = random.uniform(10, 20)
                output_qty = int(input_qty * (1 - wastage_pct/100))
                
                conversion = {
                    "date": conversion_date.isoformat(),
                    "input_item": random.choice(yarn_types),
                    "input_quantity": input_qty,
                    "input_unit": "KG",
                    "output_item": "Processed Yarn",
                    "output_quantity": output_qty,
                    "output_unit": "KG",
                    "wastage_percentage": round(wastage_pct, 1),
                    "process_cost": round(random.uniform(2000, 8000), 2),
                    "remarks": f"Conversion batch {i+1}"
                }
                
                response = requests.post(f"{base_url}/conversions/", json=conversion)
                if response.status_code == 200:
                    success_count["conversions"] += 1
                    print(f"✅ Conversion {i+1}: {input_qty}KG → {output_qty}KG ({wastage_pct:.1f}% wastage)")
                else:
                    print(f"❌ Conversion {i+1} failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Error adding conversion {i+1}: {e}")
        
        # Summary
        print("\n🎉 SAMPLE DATA INSERTION COMPLETE!")
        print("=" * 50)
        print(f"✅ Suppliers: {success_count['suppliers']}/{len(suppliers_data)} inserted")
        print(f"✅ Customers: {success_count['customers']}/{len(customers_data)} inserted")
        print(f"✅ Inventory: {success_count['inventory']}/{len(inventory_data)} inserted")
        print(f"✅ Purchases: {success_count['purchases']}/15 inserted")
        print(f"✅ Sales: {success_count['sales']}/12 inserted")
        print(f"✅ Expenses: {success_count['expenses']}/8 inserted")
        print(f"✅ Conversions: {success_count['conversions']}/6 inserted")
        
        total_records = sum(success_count.values())
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
        print(f"❌ Error in data insertion: {e}")

if __name__ == "__main__":
    insert_sample_records()
