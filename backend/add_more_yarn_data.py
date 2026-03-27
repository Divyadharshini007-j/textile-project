"""
Script to add more realistic yarn purchase data for better predictions.
This adds data for multiple yarn types with realistic price variations.
"""
import sqlite3
from datetime import datetime, timedelta
import random
import uuid

def add_yarn_data():
    conn = sqlite3.connect('yarn_trading.db')
    cursor = conn.cursor()
    
    # Define yarn types with base prices and trends
    yarn_configs = [
        {
            'type': 'Cotton Yarn 30s',
            'base_price': 320,
            'trend': 'rising',  # 0.5% monthly increase
            'volatility': 5,  # ±5 rupees random variation
            'months': 12
        },
        {
            'type': 'Polyester Yarn 150D',
            'base_price': 180,
            'trend': 'stable',
            'volatility': 3,
            'months': 12
        },
        {
            'type': 'Viscose Yarn',
            'base_price': 250,
            'trend': 'falling',  # 0.3% monthly decrease
            'volatility': 4,
            'months': 12
        },
        {
            'type': 'Blended Yarn (PC)',
            'base_price': 220,
            'trend': 'seasonal',  # Varies by season
            'volatility': 6,
            'months': 12
        }
    ]
    
    # Get existing supplier
    cursor.execute("SELECT supplier_id FROM suppliers LIMIT 1")
    supplier = cursor.fetchone()
    if not supplier:
        print("No suppliers found. Please add suppliers first.")
        conn.close()
        return
    
    supplier_id = supplier[0]
    
    print("Adding realistic yarn purchase data...\n")
    
    for config in yarn_configs:
        print(f"Adding data for {config['type']}...")
        
        start_date = datetime.now() - timedelta(days=30 * config['months'])
        
        for month in range(config['months']):
            purchase_date = start_date + timedelta(days=30 * month)
            
            # Calculate price based on trend
            if config['trend'] == 'rising':
                price = config['base_price'] * (1 + 0.005 * month)
            elif config['trend'] == 'falling':
                price = config['base_price'] * (1 - 0.003 * month)
            elif config['trend'] == 'seasonal':
                # Higher in winter (Nov-Feb), lower in summer (May-Aug)
                month_num = purchase_date.month
                if month_num in [11, 12, 1, 2]:
                    price = config['base_price'] * 1.08
                elif month_num in [5, 6, 7, 8]:
                    price = config['base_price'] * 0.95
                else:
                    price = config['base_price']
            else:  # stable
                price = config['base_price']
            
            # Add random volatility
            price += random.uniform(-config['volatility'], config['volatility'])
            price = round(price, 2)
            
            # Random quantity between 300-800 kg
            quantity = random.randint(300, 800)
            total_amount = price * quantity
            
            # Generate purchase record
            purchase_id = str(uuid.uuid4())
            invoice_number = f"INV-{purchase_date.strftime('%Y%m')}-{random.randint(1000, 9999)}"
            
            cursor.execute("""
                INSERT INTO purchases (
                    purchase_id, supplier_id, invoice_number, date, yarn_type,
                    quantity, unit, rate, total_amount, cgst, sgst, igst,
                    tax_amount, grand_total, payment_status, paid_amount, balance,
                    remarks, created_at, created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                purchase_id,
                supplier_id,
                invoice_number,
                purchase_date,
                config['type'],
                quantity,
                'KG',
                price,
                total_amount,
                total_amount * 0.09,  # 9% CGST
                total_amount * 0.09,  # 9% SGST
                0.0,  # IGST
                total_amount * 0.18,  # Total tax
                total_amount * 1.18,  # Grand total
                'Paid',
                total_amount * 1.18,
                0.0,
                f'Auto-generated test data - {config["trend"]} trend',
                datetime.now(),
                'system'
            ))
        
        print(f"  ✓ Added {config['months']} records")
    
    conn.commit()
    
    # Show summary
    print("\n" + "=" * 80)
    print("Summary of all yarn types:")
    print("=" * 80)
    cursor.execute("""
        SELECT yarn_type, COUNT(*), MIN(date), MAX(date), 
               AVG(rate), MIN(rate), MAX(rate)
        FROM purchases
        GROUP BY yarn_type
        ORDER BY yarn_type
    """)
    
    for row in cursor.fetchall():
        yarn_type, count, min_date, max_date, avg_rate, min_rate, max_rate = row
        print(f"\n{yarn_type}:")
        print(f"  Records: {count}")
        print(f"  Date Range: {min_date[:10]} to {max_date[:10]}")
        print(f"  Rate Range: ₹{min_rate:.2f} to ₹{max_rate:.2f}")
        print(f"  Average: ₹{avg_rate:.2f}")
    
    conn.close()
    print("\n✓ Data added successfully!")
    print("\nRun 'python test_predictions_fixed.py' to test predictions with new data.")

if __name__ == "__main__":
    add_yarn_data()
