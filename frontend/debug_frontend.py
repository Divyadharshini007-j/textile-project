#!/usr/bin/env python3
"""
Debug frontend issues by checking components and API calls
"""
import subprocess
import time
import requests
import json

def check_servers():
    """Check if both servers are running"""
    print("🔍 Checking Servers...")
    
    # Check backend
    try:
        response = requests.get("http://127.0.0.1:8000/api/suppliers/", timeout=2)
        print("✅ Backend server: Running")
    except:
        print("❌ Backend server: Not running")
        return False
    
    # Check frontend
    try:
        response = requests.get("http://localhost:5173", timeout=2)
        print("✅ Frontend server: Running")
    except:
        print("❌ Frontend server: Not running")
        return False
    
    return True

def check_common_issues():
    """Check for common frontend issues"""
    print("\n🔍 Checking Common Issues...")
    
    # Check if API calls are working
    api_tests = [
        ("Suppliers", "http://127.0.0.1:8000/api/suppliers/"),
        ("Customers", "http://127.0.0.1:8000/api/customers/"),
        ("Purchases", "http://127.0.0.1:8000/api/purchases/"),
        ("Sales", "http://127.0.0.1:8000/api/sales/"),
        ("Inventory", "http://127.0.0.1:8000/api/inventory/"),
        ("Expenses", "http://127.0.0.1:8000/api/expenses/"),
        ("Conversions", "http://127.0.0.1:8000/api/conversions/"),
        ("Reports", "http://127.0.0.1:8000/api/reports/"),
        ("Predictions", "http://127.0.0.1:8000/api/predictions/yarn-types"),
    ]
    
    issues = []
    for name, url in api_tests:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code != 200:
                issues.append(f"{name}: HTTP {response.status_code}")
        except Exception as e:
            issues.append(f"{name}: {str(e)}")
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ All API endpoints working")
    
    return len(issues) == 0

def check_page_components():
    """Check if page components have any obvious issues"""
    print("\n🔍 Checking Page Components...")
    
    # Check for common React import issues
    import_issues = []
    
    # This would check for missing imports or syntax errors
    # For now, we'll just verify the build works
    try:
        result = subprocess.run(["npm", "run", "build"], 
                          capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Frontend builds successfully")
            return True
        else:
            print("❌ Frontend build errors:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Build check failed: {str(e)}")
        return False

def main():
    print("🚀 Frontend Debug Tool")
    print("=" * 40)
    
    # Check servers
    if not check_servers():
        print("\n❌ Please start both servers first:")
        print("  Backend: cd backend && venv\\Scripts\\activate && uvicorn app.main:app --reload")
        print("  Frontend: cd frontend && npm run dev")
        return
    
    # Check common issues
    api_ok = check_common_issues()
    
    # Check page components
    build_ok = check_page_components()
    
    print("\n" + "=" * 40)
    if api_ok and build_ok:
        print("🎉 Frontend appears to be working correctly!")
        print("📱 If pages still don't work, check:")
        print("  1. Browser console for JavaScript errors")
        print("  2. Network tab for failed requests")
        print("  3. Clear browser cache and refresh")
    else:
        print("⚠️  Issues found that need fixing")

if __name__ == "__main__":
    main()
