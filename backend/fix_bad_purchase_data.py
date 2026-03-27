"""
Script to identify and fix bad purchase data in the database.
Specifically targets records where rate * quantity doesn't match total_amount.
"""
import sqlite3
from datetime import datetime

def fix_bad_purchase_data():
    conn = sqlite3.connect('yarn_trading.db')
    cursor = conn.cursor()
    
    # Find records with data quality issues
    cursor.execute("""
        SELECT purchase_id, yarn_type, quantity, rate, total_amount, 
               (rate * quantity) as calculated_total,
               ABS((rate * quantity) - total_amount) / total_amount * 100 as diff_pct
        FROM purchases
        WHERE rate > 10000 OR ABS((rate * quantity) - total_amount) / total_amount * 100 > 10
    """)
    
    bad_records = cursor.fetchall()
    
    if not bad_records:
        print("No bad records found!")
        conn.close()
        return
    
    print(f"Found {len(bad_records)} records with data quality issues:\n")
    
    for record in bad_records:
        purchase_id, yarn_type, quantity, rate, total_amount, calc_total, diff_pct = record
        print(f"Purchase ID: {purchase_id}")
        print(f"  Yarn Type: {yarn_type}")
        print(f"  Quantity: {quantity}")
        print(f"  Rate: ₹{rate:,.2f}")
        print(f"  Total Amount: ₹{total_amount:,.2f}")
        print(f"  Calculated Total: ₹{calc_total:,.2f}")
        print(f"  Difference: {diff_pct:.2f}%")
        
        # Fix: Calculate correct rate from total_amount and quantity
        correct_rate = total_amount / quantity if quantity > 0 else 0
        
        # If the correct rate is still unreasonable (> 1000), use average from similar yarn
        if correct_rate > 1000:
            cursor.execute("""
                SELECT AVG(rate) FROM purchases 
                WHERE yarn_type LIKE ? AND rate < 1000
            """, (f"%{yarn_type.split()[0]}%",))
            avg_rate = cursor.fetchone()[0]
            
            if avg_rate:
                correct_rate = avg_rate
                correct_total = correct_rate * quantity
                print(f"  → Using average rate from similar yarn: ₹{correct_rate:.2f}")
                print(f"  → New total: ₹{correct_total:,.2f}")
                
                # Update the record
                cursor.execute("""
                    UPDATE purchases 
                    SET rate = ?, total_amount = ?, grand_total = ?
                    WHERE purchase_id = ?
                """, (correct_rate, correct_total, correct_total, purchase_id))
            else:
                print(f"  → Deleting record (no valid reference data)")
                cursor.execute("DELETE FROM purchases WHERE purchase_id = ?", (purchase_id,))
        else:
            print(f"  → Correcting rate to: ₹{correct_rate:.2f}")
            cursor.execute("""
                UPDATE purchases 
                SET rate = ?
                WHERE purchase_id = ?
            """, (correct_rate, purchase_id))
        
        print()
    
    conn.commit()
    print(f"Fixed {len(bad_records)} records!")
    
    # Verify the fix
    cursor.execute("""
        SELECT COUNT(*) FROM purchases
        WHERE rate > 10000 OR ABS((rate * quantity) - total_amount) / total_amount * 100 > 10
    """)
    remaining = cursor.fetchone()[0]
    print(f"Remaining bad records: {remaining}")
    
    conn.close()

if __name__ == "__main__":
    fix_bad_purchase_data()
