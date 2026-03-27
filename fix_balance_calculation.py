#!/usr/bin/env python3
"""
Fix balance calculation issues - balance should be Total - Paid Amount
"""
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.base import engine, Base
from app.models import models
from sqlalchemy.orm import sessionmaker

def fix_balance_calculations():
    """Fix all balance calculations to ensure Balance = Total - Paid Amount"""
    
    print("🔧 FIXING BALANCE CALCULATIONS")
    print("=" * 50)
    
    # Create database session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Fix purchases
        print("\n💰 FIXING PURCHASE BALANCES...")
        purchases = db.query(models.Purchase).all()
        fixed_purchases = 0
        
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
                fixed_purchases += 1
                print(f"   ✅ FIXED: Balance changed from ₹{current_balance:,.2f} to ₹{correct_balance:,.2f}")
            else:
                print(f"   ✅ OK: Balance already correct")
        
        db.commit()
        print(f"\n✅ Fixed {fixed_purchases} purchases")
        
        # Fix sales
        print("\n🛍️ FIXING SALES BALANCES...")
        sales = db.query(models.Sale).all()
        fixed_sales = 0
        
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
                fixed_sales += 1
                print(f"   ✅ FIXED: Balance changed from ₹{current_balance:,.2f} to ₹{correct_balance:,.2f}")
            else:
                print(f"   ✅ OK: Balance already correct")
        
        db.commit()
        print(f"\n✅ Fixed {fixed_sales} sales")
        
        # Update payment status based on correct calculations
        print("\n🔄 UPDATING PAYMENT STATUSES...")
        
        # Update purchases status
        for purchase in purchases:
            grand_total = float(purchase.grand_total) if purchase.grand_total else 0
            paid_amount = float(purchase.paid_amount) if purchase.paid_amount else 0
            
            new_status = "Unpaid"
            if paid_amount <= 0:
                new_status = "Unpaid"
            elif paid_amount >= grand_total:
                new_status = "Paid"
            else:
                new_status = "Partial"
            
            if purchase.payment_status != new_status:
                purchase.payment_status = new_status
                print(f"   📋 Purchase {purchase.invoice_number}: Status → {new_status}")
        
        # Update sales status
        for sale in sales:
            grand_total = float(sale.grand_total) if sale.grand_total else 0
            paid_amount = float(sale.paid_amount) if sale.paid_amount else 0
            
            new_status = "Unpaid"
            if paid_amount <= 0:
                new_status = "Unpaid"
            elif paid_amount >= grand_total:
                new_status = "Paid"
            else:
                new_status = "Partial"
            
            if sale.payment_status != new_status:
                sale.payment_status = new_status
                print(f"   📋 Sale {sale.invoice_number}: Status → {new_status}")
        
        db.commit()
        
        print("\n🎉 BALANCE FIXES COMPLETE!")
        print("=" * 50)
        print(f"✅ Fixed Purchases: {fixed_purchases}")
        print(f"✅ Fixed Sales: {fixed_sales}")
        print("✅ All balances now: Total - Paid Amount")
        print("✅ All payment statuses updated")
        
        print("\n🌐 REFRESH YOUR BROWSER:")
        print("🔗 http://localhost:5173")
        print("👤 admin / admin123")
        print("💰 Balances should now be correct!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_balance_calculations()
