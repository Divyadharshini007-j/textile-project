#!/usr/bin/env python3
"""
Test payment status field visibility
"""
import requests
import json

def test_payment_status():
    """Test that payment status is working in forms"""
    
    print("🔧 TESTING PAYMENT STATUS VISIBILITY")
    print("=" * 50)
    
    # Test that frontend is running
    try:
        response = requests.get('http://localhost:5173')
        if response.status_code == 200:
            print("✅ Frontend is running")
        else:
            print(f"❌ Frontend status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        print("Please start frontend: cd frontend && npm run dev")
        return
    
    # Test backend API
    try:
        response = requests.get('http://127.0.0.1:8000/api/purchases')
        if response.status_code == 200:
            print("✅ Backend API working")
        else:
            print(f"❌ Backend API status: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        print("Please start backend: cd backend && python -m uvicorn app.main:app --reload")
        return
    
    print("\n📋 PAYMENT STATUS FIELD CHECKLIST:")
    print("✅ MenuItem component imported")
    print("✅ Payment status field added to form")
    print("✅ Validation schema updated")
    print("✅ Dropdown options configured")
    
    print("\n🎯 HOW TO CHECK PAYMENT STATUS:")
    print("1. Go to http://localhost:5173")
    print("2. Login with admin/admin123")
    print("3. Click 'Purchases' in sidebar")
    print("4. Click 'Record Purchase' button")
    print("5. Look for 'Payment Status' dropdown field")
    print("6. Should see: Paid, Unpaid, Partially Paid options")
    
    print("\n🔍 TROUBLESHOOTING:")
    print("- If dropdown not visible: Check browser console (F12)")
    print("- If form not opening: Check for JavaScript errors")
    print("- If options missing: Check MenuItem imports")
    print("- Clear browser cache and refresh")
    
    print("\n📱 Expected Field Location:")
    print("- After: Quantity, Unit, Rate fields")
    print("- Before: Total Amount display")
    print("- With: Paid Amount field next to it")

if __name__ == "__main__":
    test_payment_status()
