#!/usr/bin/env python3
"""
Test PUT endpoints for payment status updates
"""
import requests
import json

def test_put_endpoints():
    """Test that PUT endpoints work for updating payment status"""
    
    print("🔧 TESTING PUT ENDPOINTS FOR STATUS UPDATES")
    print("=" * 50)
    
    # Test purchases PUT endpoint
    try:
        # First get a purchase record
        response = requests.get('http://127.0.0.1:8000/api/purchases/')
        if response.status_code == 200:
            purchases = response.json()
            if purchases:
                purchase_id = purchases[0]['purchase_id']
                print(f"✅ Found purchase: {purchase_id}")
                
                # Test PUT endpoint
                update_data = {
                    "supplier_id": purchases[0]['supplier_id'],
                    "invoice_number": purchases[0]['invoice_number'],
                    "date": purchases[0]['date'],
                    "yarn_type": purchases[0]['yarn_type'],
                    "quantity": purchases[0]['quantity'],
                    "unit": purchases[0]['unit'],
                    "rate": purchases[0]['rate'],
                    "total_amount": purchases[0]['total_amount'],
                    "cgst": purchases[0].get('cgst', 0),
                    "sgst": purchases[0].get('sgst', 0),
                    "igst": purchases[0].get('igst', 0),
                    "tax_amount": purchases[0].get('tax_amount', 0),
                    "grand_total": purchases[0]['grand_total'],
                    "payment_status": "Paid",  # Change status to Paid
                    "paid_amount": purchases[0].get('paid_amount', 0),
                    "balance": purchases[0].get('balance', 0),
                    "remarks": purchases[0].get('remarks', '')
                }
                
                response = requests.put(f'http://127.0.0.1:8000/api/purchases/{purchase_id}', json=update_data)
                if response.status_code == 200:
                    print("✅ Purchases PUT endpoint working")
                else:
                    print(f"❌ Purchases PUT failed: {response.status_code}")
                    print(response.text)
            else:
                print("❌ No purchases found")
        else:
            print(f"❌ Failed to get purchases: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing purchases PUT: {e}")
    
    # Test sales PUT endpoint
    try:
        # First get a sales record
        response = requests.get('http://127.0.0.1:8000/api/sales/')
        if response.status_code == 200:
            sales = response.json()
            if sales:
                sale_id = sales[0]['sales_id']
                print(f"✅ Found sale: {sale_id}")
                
                # Test PUT endpoint
                update_data = {
                    "customer_id": sales[0]['customer_id'],
                    "invoice_number": sales[0]['invoice_number'],
                    "date": sales[0]['date'],
                    "product_name": sales[0]['product_name'],
                    "product_type": sales[0].get('product_type', 'Finished Product'),
                    "quantity": sales[0]['quantity'],
                    "unit": sales[0]['unit'],
                    "rate": sales[0]['rate'],
                    "total_amount": sales[0]['total_amount'],
                    "cgst": sales[0].get('cgst', 0),
                    "sgst": sales[0].get('sgst', 0),
                    "igst": sales[0].get('igst', 0),
                    "tax_amount": sales[0].get('tax_amount', 0),
                    "grand_total": sales[0]['grand_total'],
                    "payment_status": "Paid",  # Change status to Paid
                    "paid_amount": sales[0].get('paid_amount', 0),
                    "balance": sales[0].get('balance', 0),
                    "remarks": sales[0].get('remarks', '')
                }
                
                response = requests.put(f'http://127.0.0.1:8000/api/sales/{sale_id}', json=update_data)
                if response.status_code == 200:
                    print("✅ Sales PUT endpoint working")
                else:
                    print(f"❌ Sales PUT failed: {response.status_code}")
                    print(response.text)
            else:
                print("❌ No sales found")
        else:
            print(f"❌ Failed to get sales: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing sales PUT: {e}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Restart backend server if needed")
    print("2. Test frontend status update")
    print("3. Check browser console for errors")
    print("4. Verify status changes in database")

if __name__ == "__main__":
    test_put_endpoints()
