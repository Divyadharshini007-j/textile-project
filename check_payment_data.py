#!/usr/bin/env python3
"""
Check current payment data and fix balance calculations
"""
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.base import engine, Base
from app.models import models
from sqlalchemy.orm import sessionmaker

def check_and_fix_payment_data():
    """Check and fix payment data issues"""
    
    print("🔍 CHECKING AND FIXING PAYMENT DATA")
    print("=" * 50)
    
    # Create database session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check purchases
        print("\n💰 CHECKING PURCHASES...")
        purchases = db.query(models.Purchase).all()
        
        for purchase in purchases:
            grand_total = float(purchase.grand_total) if purchase.grand_total else 0
            paid_amount = float(purchase.paid_amount) if purchase.paid_amount else 0
            current_balance = float(purchase.balance) if purchase.balance else 0
            correct_balance = grand_total - paid_amount
            
            print(f"\n📋 Purchase: {purchase.invoice_number}")
            print(f"   Total: ₹{grand_total:,.2f}")
            print(f"   Paid: ₹{paid_amount:,.2f}")
            print(f"   Current Balance: ₹{current_balance:,.2f}")
            print(f"   Correct Balance: ₹{correct_balance:,.2f}")
            
            # Fix balance if incorrect
            if abs(current_balance - correct_balance) > 0.01:
                purchase.balance = correct_balance
                print(f"   ✅ Fixed balance to: ₹{correct_balance:,.2f}")
            
            # Fix payment status
            new_status = "Unpaid"
            if paid_amount <= 0:
                new_status = "Unpaid"
            elif paid_amount >= grand_total:
                new_status = "Paid"
            else:
                new_status = "Partial"
            
            if purchase.payment_status != new_status:
                print(f"   ✅ Fixed status from '{purchase.payment_status}' to '{new_status}'")
                purchase.payment_status = new_status
        
        db.commit()
        print(f"\n✅ Fixed {len(purchases)} purchases")
        
        # Check sales
        print("\n🛍️ CHECKING SALES...")
        sales = db.query(models.Sale).all()
        
        for sale in sales:
            grand_total = float(sale.grand_total) if sale.grand_total else 0
            paid_amount = float(sale.paid_amount) if sale.paid_amount else 0
            current_balance = float(sale.balance) if sale.balance else 0
            correct_balance = grand_total - paid_amount
            
            print(f"\n📋 Sale: {sale.invoice_number}")
            print(f"   Total: ₹{grand_total:,.2f}")
            print(f"   Paid: ₹{paid_amount:,.2f}")
            print(f"   Current Balance: ₹{current_balance:,.2f}")
            print(f"   Correct Balance: ₹{correct_balance:,.2f}")
            
            # Fix balance if incorrect
            if abs(current_balance - correct_balance) > 0.01:
                sale.balance = correct_balance
                print(f"   ✅ Fixed balance to: ₹{correct_balance:,.2f}")
            
            # Fix payment status
            new_status = "Unpaid"
            if paid_amount <= 0:
                new_status = "Unpaid"
            elif paid_amount >= grand_total:
                new_status = "Paid"
            else:
                new_status = "Partial"
            
            if sale.payment_status != new_status:
                print(f"   ✅ Fixed status from '{sale.payment_status}' to '{new_status}'")
                sale.payment_status = new_status
        
        db.commit()
        print(f"\n✅ Fixed {len(sales)} sales")
        
        print("\n🎉 PAYMENT DATA FIXES COMPLETE!")
        print("=" * 50)
        print("✅ All balances recalculated correctly")
        print("✅ All payment statuses updated")
        print("✅ Database synchronized")
        
        print("\n🌐 TEST YOUR APPLICATION:")
        print("🔗 http://localhost:5173")
        print("👤 admin / admin123")
        print("💰 Try updating payment amounts in tables")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_fix_payment_data()
