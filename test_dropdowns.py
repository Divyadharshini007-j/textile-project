#!/usr/bin/env python3
"""
Test that dropdown data is loading correctly
"""
import requests
import json

def test_dropdown_data():
    """Test dropdown data endpoints"""
    
    print("🔧 TESTING DROPDOWN DATA ENDPOINTS")
    print("=" * 50)
    
    # Test yarn types endpoint
    try:
        response = requests.get('http://127.0.0.1:8000/api/predictions/yarn-types')
        if response.status_code == 200:
            yarn_types = response.json()
            print(f"✅ Yarn Types ({len(yarn_types)}):")
            for i, yarn in enumerate(yarn_types, 1):
                print(f"  {i}. {yarn}")
        else:
            print(f"❌ Yarn Types failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Yarn Types error: {e}")
    
    # Test suppliers endpoint
    try:
        response = requests.get('http://127.0.0.1:8000/api/suppliers/')
        if response.status_code == 200:
            suppliers = response.json()
            print(f"\n✅ Suppliers ({len(suppliers)}):")
            for i, supplier in enumerate(suppliers, 1):
                print(f"  {i}. {supplier['supplier_name']} ({supplier['supplier_id']})")
        else:
            print(f"❌ Suppliers failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Suppliers error: {e}")
    
    # Test customers endpoint
    try:
        response = requests.get('http://127.0.0.1:8000/api/customers/')
        if response.status_code == 200:
            customers = response.json()
            print(f"\n✅ Customers ({len(customers)}):")
            for i, customer in enumerate(customers, 1):
                print(f"  {i}. {customer['customer_name']} ({customer['customer_id']})")
        else:
            print(f"❌ Customers failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Customers error: {e}")
    
    print("\n🎯 FRONTEND TESTING:")
    print("1. Open: http://localhost:5173")
    print("2. Login: admin / admin123")
    print("3. Purchases → Record Purchase:")
    print("   - Supplier dropdown should show: Cotton Mills Ltd")
    print("   - Yarn Type dropdown should show: 3 options")
    print("4. Sales → Record Sale:")
    print("   - Customer dropdown should show available customers")
    print("   - Product Name dropdown should show: 3 yarn types")
    
    print("\n🔍 TROUBLESHOOTING:")
    print("- If dropdowns empty: Check browser console (F12)")
    print("- If no data: Check network requests in dev tools")
    print("- If errors: Look at console for API errors")
    print("- Refresh page: Ctrl+F5")

if __name__ == "__main__":
    test_dropdown_data()
