#!/usr/bin/env python3
"""
Test and fix login issue
"""
import requests
import json

def test_login():
    """Test the exact login process"""
    
    print("🔍 Testing Login Process...")
    
    # Test 1: Direct form data (like frontend sends)
    print("\n1. Testing form data login:")
    try:
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = requests.post('http://127.0.0.1:8000/api/auth/login', data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            print("✅ Form data login works")
            return True
    except Exception as e:
        print(f"❌ Form data login failed: {e}")
    
    # Test 2: JSON login
    print("\n2. Testing JSON login:")
    try:
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = requests.post('http://127.0.0.1:8000/api/auth/login', json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ JSON login failed: {e}")
    
    return False

def check_user_exists():
    """Check if admin user exists in database"""
    print("\n🔍 Checking admin user...")
    try:
        from app.db.base import SessionLocal
        from app.models import models
        
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.username == "admin").first()
        if user:
            print("✅ Admin user found in database")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Role: {user.role}")
            return True
        else:
            print("❌ Admin user NOT found in database")
            return False
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Login Fix Tool")
    print("=" * 40)
    
    # Check if user exists
    user_exists = check_user_exists()
    
    # Test login
    login_works = test_login()
    
    print("\n" + "=" * 40)
    if user_exists and login_works:
        print("✅ Login system is working!")
        print("📱 Frontend should be able to login")
    else:
        print("❌ Login system has issues")
        print("🔧 Need to fix the authentication")
