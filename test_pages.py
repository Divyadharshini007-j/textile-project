#!/usr/bin/env python3
"""
Test if the pages are loading properly by checking API endpoints
"""
import requests
import json

def test_pages():
    """Test if the backend APIs are working for purchases and sales"""
    
    print("🔍 TESTING PURCHASES AND SALES PAGES")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000/api"
    
    try:
        # Test purchases endpoint
        print("\n📦 Testing Purchases API...")
        purchases_response = requests.get(f"{base_url}/purchases/")
        if purchases_response.status_code == 200:
            purchases_data = purchases_response.json()
            print(f"✅ Purchases API working - {len(purchases_data)} records found")
            if purchases_data:
                first_purchase = purchases_data[0]
                print(f"   Sample: {first_purchase.get('invoice_number', 'N/A')} - ₹{first_purchase.get('total_amount', 0):,.2f}")
        else:
            print(f"❌ Purchases API failed: {purchases_response.status_code}")
        
        # Test sales endpoint
        print("\n🛍️ Testing Sales API...")
        sales_response = requests.get(f"{base_url}/sales/")
        if sales_response.status_code == 200:
            sales_data = sales_response.json()
            print(f"✅ Sales API working - {len(sales_data)} records found")
            if sales_data:
                first_sale = sales_data[0]
                print(f"   Sample: {first_sale.get('invoice_number', 'N/A')} - ₹{first_sale.get('total_amount', 0):,.2f}")
        else:
            print(f"❌ Sales API failed: {sales_response.status_code}")
        
        # Test yarn types endpoint
        print("\n🧶 Testing Yarn Types API...")
        yarn_response = requests.get(f"{base_url}/predictions/yarn-types")
        if yarn_response.status_code == 200:
            yarn_types = yarn_response.json()
            print(f"✅ Yarn Types API working - {len(yarn_types)} types found")
            for yarn_type in yarn_types:
                print(f"   - {yarn_type}")
        else:
            print(f"❌ Yarn Types API failed: {yarn_response.status_code}")
        
        print("\n🌐 FRONTEND URLS TO TRY:")
        print("🔗 http://localhost:5173 (main)")
        print("🔗 http://localhost:5174 (backup)")
        
        print("\n👤 LOGIN CREDENTIALS:")
        print("Username: admin")
        print("Password: admin123")
        
        print("\n🎯 IF PAGES STILL NOT WORKING:")
        print("1. Check browser console for JavaScript errors")
        print("2. Try clearing browser cache (Ctrl+F5)")
        print("3. Try different browser")
        print("4. Check network tab for failed requests")
        
    except Exception as e:
        print(f"❌ Error testing pages: {e}")

if __name__ == "__main__":
    test_pages()
