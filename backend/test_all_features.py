#!/usr/bin/env python3
"""
Comprehensive test script for all yarn trading system features
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def test_feature(name, test_func):
    """Test a feature and print results"""
    print(f"\n🧪 Testing {name}...")
    try:
        result = test_func()
        print(f"✅ {name}: PASSED")
        return True
    except Exception as e:
        print(f"❌ {name}: FAILED - {str(e)}")
        return False

def test_auth():
    """Test authentication"""
    # Login
    data = {
        'username': 'admin',
        'password': 'admin123'
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=data)
    response.raise_for_status()
    token = response.json()['access_token']
    return token

def test_dashboard():
    """Test dashboard endpoints"""
    response = requests.get(f"{BASE_URL}/dashboard/kpi")
    response.raise_for_status()
    kpis = response.json()
    
    response = requests.get(f"{BASE_URL}/dashboard/charts")
    response.raise_for_status()
    return kpis

def test_suppliers():
    """Test suppliers"""
    response = requests.get(f"{BASE_URL}/suppliers/")
    response.raise_for_status()
    return response.json()

def test_customers():
    """Test customers"""
    response = requests.get(f"{BASE_URL}/customers/")
    response.raise_for_status()
    return response.json()

def test_purchases():
    """Test purchases"""
    response = requests.get(f"{BASE_URL}/purchases/")
    response.raise_for_status()
    return response.json()

def test_sales():
    """Test sales"""
    response = requests.get(f"{BASE_URL}/sales/")
    response.raise_for_status()
    return response.json()

def test_inventory():
    """Test inventory"""
    response = requests.get(f"{BASE_URL}/inventory/")
    response.raise_for_status()
    return response.json()

def test_expenses():
    """Test expenses"""
    response = requests.get(f"{BASE_URL}/expenses/")
    response.raise_for_status()
    return response.json()

def test_predictions():
    """Test ML predictions"""
    # Get yarn types
    response = requests.get(f"{BASE_URL}/predictions/yarn-types")
    response.raise_for_status()
    yarn_types = response.json()
    
    if yarn_types:
        # Test prediction
        response = requests.get(f"{BASE_URL}/predictions/predict", params={
            'yarn_type': yarn_types[0],
            'quantity': 100
        })
        response.raise_for_status()
        prediction = response.json()
        
        # Test trends
        response = requests.get(f"{BASE_URL}/predictions/trends", params={
            'yarn_type': yarn_types[0]
        })
        response.raise_for_status()
        trends = response.json()
        
        return {'yarn_types': yarn_types, 'prediction': prediction, 'trends': trends}
    return {'yarn_types': []}

def main():
    print("🚀 Starting Comprehensive Feature Tests")
    print("=" * 50)
    
    tests = [
        ("Authentication", test_auth),
        ("Dashboard KPIs", test_dashboard),
        ("Suppliers", test_suppliers),
        ("Customers", test_customers),
        ("Purchases", test_purchases),
        ("Sales", test_sales),
        ("Inventory", test_inventory),
        ("Expenses", test_expenses),
        ("ML Predictions", test_predictions),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        if test_feature(name, test_func):
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} features working")
    print(f"✅ Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All features are working correctly!")
    else:
        print(f"\n⚠️  {total - passed} features need attention")

if __name__ == "__main__":
    main()
