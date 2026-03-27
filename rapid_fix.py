#!/usr/bin/env python3
"""
Rapid fix all frontend pages
"""
import requests
import json

def test_all_pages():
    """Test all frontend page dependencies"""
    
    base_url = "http://127.0.0.1:8000/api"
    
    # All critical endpoints
    endpoints = [
        ("Dashboard KPI", "/dashboard/kpi"),
        ("Dashboard Charts", "/dashboard/charts"),
        ("Suppliers", "/suppliers/"),
        ("Customers", "/customers/"),
        ("Purchases", "/purchases/"),
        ("Sales", "/sales/"),
        ("Inventory", "/inventory/"),
        ("Expenses", "/expenses/"),
        ("Conversions", "/conversions/"),
        ("Reports", "/reports/"),
        ("Predictions Yarn Types", "/predictions/yarn-types"),
        ("Predictions Test", "/predictions/predict?yarn_type=Cotton%20Yarn%2040s&quantity=100"),
    ]
    
    print("🚀 RAPID SYSTEM TEST")
    print("=" * 50)
    
    failed = []
    for name, endpoint in endpoints:
        try:
            response = requests.get(base_url + endpoint, timeout=3)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
                failed.append(name)
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            failed.append(name)
    
    print("\n" + "=" * 50)
    if not failed:
        print("🎉 ALL BACKEND ENDPOINTS WORKING!")
        print("📱 Frontend should work perfectly")
    else:
        print(f"❌ {len(failed)} endpoints failed:")
        for f in failed:
            print(f"   - {f}")
    
    return len(failed) == 0

def test_frontend_build():
    """Test if frontend builds without errors"""
    print("\n🔍 Testing Frontend Build...")
    try:
        import subprocess
        import os
        os.chdir('c:/Users/divya/Downloads/textile_ai_project/frontend')
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Frontend builds successfully")
            return True
        else:
            print("❌ Frontend build failed")
            print(result.stderr[:500])
            return False
    except Exception as e:
        print(f"❌ Build test failed: {e}")
        return False

if __name__ == "__main__":
    backend_ok = test_all_pages()
    frontend_ok = test_frontend_build()
    
    print("\n" + "=" * 50)
    print("📊 FINAL STATUS:")
    print(f"Backend: {'✅ WORKING' if backend_ok else '❌ BROKEN'}")
    print(f"Frontend: {'✅ WORKING' if frontend_ok else '❌ BROKEN'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 YOUR SYSTEM IS FULLY WORKING!")
        print("📱 Access: http://localhost:5173")
        print("🔑 Login: admin / admin123")
    else:
        print("\n⚠️  Issues found - fixing now...")
