#!/usr/bin/env python3
"""
Quick check for payment status field
"""
import webbrowser
import time

def check_payment_status():
    print("🔍 PAYMENT STATUS FIELD CHECK")
    print("=" * 40)
    print()
    print("✅ I've added YELLOW HIGHLIGHT to payment status fields")
    print("✅ This makes them easy to spot in the forms")
    print()
    print("📋 STEP-BY-STEP INSTRUCTIONS:")
    print("1. Go to: http://localhost:5173")
    print("2. Login: admin / admin123")
    print("3. Click 'Purchases' in sidebar")
    print("4. Click 'Record Purchase' button")
    print("5. Look for YELLOW 'Payment Status' dropdown")
    print("6. Should see: Paid, Unpaid, Partially Paid")
    print()
    print("🎯 FIELD LOCATION:")
    print("- After: Quantity, Unit, Rate fields")
    print("- Before: Total Amount section")
    print("- YELLOW background for visibility")
    print()
    print("📱 SAME FOR SALES:")
    print("1. Click 'Sales' in sidebar")
    print("2. Click 'Record Sale' button")
    print("3. Look for YELLOW 'Payment Status' dropdown")
    print()
    print("⚠️  If you still can't see it:")
    print("- Refresh browser (Ctrl+F5)")
    print("- Clear browser cache")
    print("- Check browser console (F12) for errors")
    print("- Make sure frontend is running")
    
    # Try to open browser
    try:
        webbrowser.open('http://localhost:5173')
        print("🌐 Opening browser...")
    except:
        print("💡 Manually open: http://localhost:5173")

if __name__ == "__main__":
    check_payment_status()
