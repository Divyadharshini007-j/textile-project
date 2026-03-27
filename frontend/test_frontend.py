#!/usr/bin/env python3
"""
Simple frontend connectivity test
"""
import requests
import subprocess
import time
import sys

def test_frontend_server():
    """Test if frontend server is running"""
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_backend_connectivity():
    """Test if frontend can reach backend"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/suppliers/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🌐 Testing Frontend Connectivity")
    print("=" * 40)
    
    # Test frontend server
    if test_frontend_server():
        print("✅ Frontend server is running")
    else:
        print("❌ Frontend server is not accessible")
        return False
    
    # Test backend connectivity from frontend perspective
    if test_backend_connectivity():
        print("✅ Backend API is accessible from frontend")
    else:
        print("❌ Backend API is not accessible from frontend")
        return False
    
    print("\n🎉 Frontend connectivity test passed!")
    print("📱 You can access the application at: http://localhost:5173")
    print("🔑 Login with: username='admin', password='admin123'")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
