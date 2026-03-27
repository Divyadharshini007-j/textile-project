#!/usr/bin/env python3
"""
Test all frontend pages by checking their API dependencies
"""
import requests
import json

def test_page_dependencies():
    """Test all API endpoints that frontend pages depend on"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    # All endpoints that frontend pages use
    test_cases = [
        ("Dashboard", "/dashboard/kpi"),
        ("Dashboard Charts", "/dashboard/charts"),
        ("Purchases", "/purchases/"),
        ("Sales", "/sales/"),
        ("Customers", "/customers/"),
        ("Suppliers", "/suppliers/"),
        ("Expenses", "/expenses/"),
        ("Inventory", "/inventory/"),
        ("Conversions", "/conversions/"),
        ("Reports", "/reports/"),
        ("Predictions Yarn Types", "/predictions/yarn-types"),
        ("Predictions Test", "/predictions/predict?yarn_type=Cotton%20Yarn%2040s&quantity=100"),
    ]
    
    print("🧪 Testing Frontend Page Dependencies")
    print("=" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for name, endpoint in test_cases:
        try:
            response = requests.get(base_url + endpoint, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                passed += 1
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} endpoints working")
    print(f"✅ Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All frontend dependencies are working!")
        print("📱 All pages should load correctly")
    else:
        print(f"\n⚠️  {total - passed} endpoints need fixing")
    
    return passed == total

if __name__ == "__main__":
    test_page_dependencies()
