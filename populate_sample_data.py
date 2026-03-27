#!/usr/bin/env python3
"""
Populate the Textile AI application with comprehensive sample data
"""
import requests
import json
from datetime import datetime, timedelta
import random

def populate_sample_data():
    """Populate all features with realistic sample data"""
    
    print("🏭 POPULATING TEXTILE AI WITH SAMPLE DATA")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000/api"
    
    # Standard yarn types
    yarn_types = ["Cotton Yarn 40", "Polyester Yarn"]
    
    # Sample suppliers
    suppliers = [
        {
            "supplier_name": "Mumbai Textile Mills",
            "contact_person": "Rajesh Kumar",
            "address": "Mumbai, Maharashtra",
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
            "address": "Delhi, NCR",
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
            "address": "Bangalore, Karnataka",
            "phone": "9876543212",
            "email": "priya@bangalorerarn.com",
            "gstin": "29CCCCC0000C1Z1",
            "payment_terms": "NET 60",
            "opening_balance": 0.0,
            "status": "Active"
        }
    ]
    
    # Sample customers
    customers = [
        {
            "customer_name": "Fashion Garments Ltd",
            "contact_person": "Sanjay Reddy",
            "address": "Hyderabad, Telangana",
            "phone": "9876543201",
            "email": "sanjay@fashiongarments.com",
            "gstin": "36DDDDD0000D1Z1",
            "payment_terms": "NET 30",
            "opening_balance": 0.0,
            "status": "Active"
        },
        {
            "customer_name": "Textile Exporters Inc",
            "contact_person": "Anita Patel",
            "address": "Ahmedabad, Gujarat",
            "phone": "9876543202",
            "email": "anita@textileexporters.com",
            "gstin": "24EEEEE0000E1Z1",
            "payment_terms": "NET 45",
            "opening_balance": 0.0,
            "status": "Active"
        },
        {
            "customer_name": "Premium Clothing Co",
            "contact_person": "Vikram Malhotra",
            "address": "Chennai, Tamil Nadu",
            "phone": "9876543203",
            "email": "vikram@premiumclothing.com",
            "gstin": "33FFFFF0000F1Z1",
            "payment_terms": "NET 30",
            "opening_balance": 0.0,
            "status": "Active"
        }
    ]
    
    # Sample inventory items
    inventory_items = [
        {
            "item_name": "Cotton Yarn 40",
            "item_type": "Yarn",
            "item_category": "Raw Material",
            "unit": "KG",
            "opening_stock": 1000,
            "stock_in": 0,
            "stock_out": 0,
            "closing_stock": 1000,
            "unit_cost": 250.0
        },
        {
            "item_name": "Polyester Yarn",
            "item_type": "Yarn",
            "item_category": "Raw Material",
            "unit": "KG",
            "opening_stock": 800,
            "stock_in": 0,
            "stock_out": 0,
            "closing_stock": 800,
            "unit_cost": 180.0
        }
    ]
    
    try:
        # 1. Add Suppliers
        print("\n📦 Adding Suppliers...")
        for supplier in suppliers:
            response = requests.post(f"{base_url}/suppliers/", json=supplier)
            if response.status_code == 200:
                print(f"✅ Added: {supplier['supplier_name']}")
            else:
                print(f"❌ Failed to add supplier: {response.status_code}")
        
        # 2. Add Customers
        print("\n👥 Adding Customers...")
        for customer in customers:
            response = requests.post(f"{base_url}/customers/", json=customer)
            if response.status_code == 200:
                print(f"✅ Added: {customer['customer_name']}")
            else:
                print(f"❌ Failed to add customer: {response.status_code}")
        
        # 3. Add Inventory Items
        print("\n📊 Adding Inventory Items...")
        for item in inventory_items:
            response = requests.post(f"{base_url}/inventory/", json=item)
            if response.status_code == 200:
                print(f"✅ Added: {item['item_name']}")
            else:
                print(f"❌ Failed to add inventory: {response.status_code}")
        
        # 4. Add Sample Purchases
        print("\n💰 Adding Sample Purchases...")
        purchase_count = 0
        for i in range(15):  # 15 sample purchases
            purchase_date = datetime.now() - timedelta(days=random.randint(1, 60))
            yarn_type = random.choice(yarn_types)
            quantity = random.randint(100, 1000)
            rate = 250 if yarn_type == "Cotton Yarn 40" else 180
            total_amount = quantity * rate
            
            purchase = {
                "supplier_id": random.choice(suppliers)["supplier_name"],
                "invoice_number": f"PUR{2026}{str(i+1).zfill(3)}",
                "date": purchase_date.isoformat(),
                "yarn_type": yarn_type,
                "quantity": quantity,
                "unit": "KG",
                "rate": rate,
                "total_amount": total_amount,
                "cgst": 0,
                "sgst": 0,
                "igst": 0,
                "tax_amount": 0,
                "grand_total": total_amount,
                "payment_status": random.choice(["Paid", "Unpaid", "Partial"]),
                "paid_amount": total_amount if random.choice([True, False]) else total_amount * 0.5,
                "balance": 0,
                "remarks": f"Sample purchase {i+1}"
            }
            
            response = requests.post(f"{base_url}/purchases/", json=purchase)
            if response.status_code == 200:
                purchase_count += 1
                print(f"✅ Purchase {i+1}: {yarn_type} - {quantity}KG")
            else:
                print(f"❌ Failed purchase {i+1}: {response.status_code}")
        
        # 5. Add Sample Sales
        print("\n🛍️ Adding Sample Sales...")
        sales_count = 0
        for i in range(12):  # 12 sample sales
            sale_date = datetime.now() - timedelta(days=random.randint(1, 45))
            yarn_type = random.choice(yarn_types)
            quantity = random.randint(50, 500)
            rate = 320 if yarn_type == "Cotton Yarn 40" else 240  # Higher selling price
            total_amount = quantity * rate
            
            sale = {
                "customer_id": random.choice(customers)["customer_name"],
                "invoice_number": f"SAL{2026}{str(i+1).zfill(3)}",
                "date": sale_date.isoformat(),
                "product_name": yarn_type,
                "product_type": "Yarn",
                "quantity": quantity,
                "unit": "KG",
                "rate": rate,
                "total_amount": total_amount,
                "cgst": 0,
                "sgst": 0,
                "igst": 0,
                "tax_amount": 0,
                "grand_total": total_amount,
                "payment_status": random.choice(["Paid", "Unpaid", "Partial"]),
                "paid_amount": total_amount if random.choice([True, False]) else total_amount * 0.6,
                "balance": 0,
                "remarks": f"Sample sale {i+1}"
            }
            
            response = requests.post(f"{base_url}/sales/", json=sale)
            if response.status_code == 200:
                sales_count += 1
                print(f"✅ Sale {i+1}: {yarn_type} - {quantity}KG")
            else:
                print(f"❌ Failed sale {i+1}: {response.status_code}")
        
        # 6. Add Sample Expenses
        print("\n💸 Adding Sample Expenses...")
        expense_categories = ["Electricity", "Water", "Rent", "Salaries", "Transport", "Maintenance", "Office Supplies"]
        expense_count = 0
        for i in range(8):  # 8 sample expenses
            expense_date = datetime.now() - timedelta(days=random.randint(1, 30))
            amount = random.randint(5000, 50000)
            
            expense = {
                "category": random.choice(expense_categories),
                "amount": amount,
                "date": expense_date.isoformat(),
                "description": f"Sample expense for {random.choice(expense_categories).lower()}",
                "payment_mode": random.choice(["Cash", "Bank Transfer", "Cheque", "UPI"]),
                "receipt_number": f"EXP{2026}{str(i+1).zfill(3)}",
                "approved_by": "Admin",
                "status": "Approved"
            }
            
            response = requests.post(f"{base_url}/expenses/", json=expense)
            if response.status_code == 200:
                expense_count += 1
                print(f"✅ Expense {i+1}: {expense['category']} - ₹{amount}")
            else:
                print(f"❌ Failed expense {i+1}: {response.status_code}")
        
        # 7. Add Sample Conversions
        print("\n🔄 Adding Sample Conversions...")
        conversion_count = 0
        for i in range(6):  # 6 sample conversions
            conversion_date = datetime.now() - timedelta(days=random.randint(1, 20))
            input_qty = random.randint(100, 500)
            output_qty = int(input_qty * 0.85)  # 15% wastage
            
            conversion = {
                "date": conversion_date.isoformat(),
                "input_item": random.choice(yarn_types),
                "input_quantity": input_qty,
                "input_unit": "KG",
                "output_item": "Processed Yarn",
                "output_quantity": output_qty,
                "output_unit": "KG",
                "wastage_percentage": 15.0,
                "process_cost": random.randint(2000, 10000),
                "remarks": f"Sample conversion {i+1}"
            }
            
            response = requests.post(f"{base_url}/conversions/", json=conversion)
            if response.status_code == 200:
                conversion_count += 1
                print(f"✅ Conversion {i+1}: {input_qty}KG → {output_qty}KG")
            else:
                print(f"❌ Failed conversion {i+1}: {response.status_code}")
        
        print("\n🎉 SAMPLE DATA POPULATION COMPLETE!")
        print(f"✅ Suppliers: {len(suppliers)} added")
        print(f"✅ Customers: {len(customers)} added")
        print(f"✅ Inventory: {len(inventory_items)} items added")
        print(f"✅ Purchases: {purchase_count} added")
        print(f"✅ Sales: {sales_count} added")
        print(f"✅ Expenses: {expense_count} added")
        print(f"✅ Conversions: {conversion_count} added")
        
        print("\n🎯 YARN TYPES STANDARDIZED:")
        for yarn in yarn_types:
            print(f"  - {yarn}")
        
        print("\n🚀 APPLICATION READY FOR USE!")
        print("🌐 Access: http://localhost:5173")
        print("👤 Login: admin / admin123")
        
    except Exception as e:
        print(f"❌ Error populating data: {e}")

if __name__ == "__main__":
    populate_sample_data()
