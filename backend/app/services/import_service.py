import pandas as pd
from sqlalchemy.orm import Session
from app.models import models
from datetime import datetime
import uuid

class ImportService:
    @staticmethod
    def import_all(db: Session, base_path: str):
        stats = {}
        # 1. Suppliers and Purchases (from Yarn purchase data.xlsx)
        stats['purchases'] = ImportService.import_purchases(f"{base_path}/Yarn purchase data.xlsx", db)
        
        # 2. Customers and Sales (from sales final data.xlsx)
        stats['sales'] = ImportService.import_sales(f"{base_path}/sales final data.xlsx", db)
        
        # 3. Inventory (from inventory_large.xlsx)
        stats['inventory'] = ImportService.import_inventory(f"{base_path}/inventory_large.xlsx", db)
        
        # 4. Payments (from payments_large.xlsx)
        stats['payments'] = ImportService.import_payments(f"{base_path}/payments_large.xlsx", db)
        
        return stats

    @staticmethod
    def import_purchases(file_path: str, db: Session):
        df = pd.read_excel(file_path)
        count = 0
        for _, row in df.iterrows():
            supplier_name = str(row.get('Supplier_Name', ''))
            supplier_id = f"SUP_{supplier_name.replace(' ', '_')[:20]}"
            
            # Ensure supplier exists
            supplier = db.query(models.Supplier).filter_by(supplier_id=supplier_id).first()
            if not supplier:
                supplier = models.Supplier(
                    supplier_id=supplier_id,
                    supplier_name=supplier_name,
                    contact_person="Imported",
                    address="Imported",
                    phone="0000000000",
                    email=f"{supplier_id.lower()}@example.com",
                    gstin="GSTUNKNOWN",
                    payment_terms="Net 30",
                    status="Active"
                )
                db.add(supplier)
            
            purchase = models.Purchase(
                purchase_id=str(row.get('Purchase_ID', str(uuid.uuid4())[:8])),
                supplier_id=supplier_id,
                invoice_number=str(row.get('Invoice_No', '')),
                date=pd.to_datetime(row.get('Date', datetime.now())),
                yarn_type=str(row.get('Yarn_Type', '')),
                quantity=float(row.get('Quantity_KG', 0)),
                unit="KG",
                rate=float(row.get('Rate_per_KG', 0)),
                total_amount=float(row.get('Total_Amount', 0)),
                tax_amount=0, # Not in excel
                grand_total=float(row.get('Total_Amount', 0)),
                payment_status="Unpaid",
                balance=float(row.get('Total_Amount', 0)),
                created_by="system"
            )
            db.add(purchase)
            count += 1
        db.commit()
        return count

    @staticmethod
    def import_sales(file_path: str, db: Session):
        df = pd.read_excel(file_path)
        count = 0
        for _, row in df.iterrows():
            customer_name = str(row.get('Customer_Name', ''))
            customer_id = f"CUST_{customer_name.replace(' ', '_')[:20]}"
            
            # Ensure customer exists
            customer = db.query(models.Customer).filter_by(customer_id=customer_id).first()
            if not customer:
                customer = models.Customer(
                    customer_id=customer_id,
                    customer_name=customer_name,
                    contact_person="Imported",
                    address=str(row.get('Street', 'Imported')),
                    city=str(row.get('City', 'Imported')),
                    country="India",
                    phone="0000000000",
                    email=f"{customer_id.lower()}@example.com",
                    gstin="GSTUNKNOWN",
                    status="Active"
                )
                db.add(customer)
            
            sale = models.Sale(
                sales_id=str(row.get('Invoice_No', str(uuid.uuid4())[:8])),
                customer_id=customer_id,
                invoice_number=str(row.get('Invoice_No', '')),
                date=pd.to_datetime(row.get('Date', datetime.now())),
                product_name=str(row.get('Product', '')),
                product_type=str(row.get('Category', '')),
                quantity=float(row.get('Quantity_Meters', 0)),
                unit="Meters",
                rate=float(row.get('Rate_per_Meter', 0)),
                total_amount=float(row.get('Total_Amount', 0)),
                tax_amount=0,
                grand_total=float(row.get('Total_Amount', 0)),
                payment_status="Unpaid",
                balance=float(row.get('Total_Amount', 0)),
                created_by="system"
            )
            db.add(sale)
            count += 1
        db.commit()
        return count

    @staticmethod
    def import_inventory(file_path: str, db: Session):
        df = pd.read_excel(file_path)
        count = 0
        for _, row in df.iterrows():
            inventory = models.Inventory(
                inventory_id=str(uuid.uuid4())[:8],
                item_name=str(row.get('Item_Name', '')),
                item_type=str(row.get('Item_Type', '')),
                item_category="Imported",
                unit="Unit",
                opening_stock=float(row.get('Opening_Stock', 0)),
                stock_in=float(row.get('Stock_In', 0)),
                stock_out=float(row.get('Stock_Out', 0)),
                closing_stock=float(row.get('Closing_Stock', 0)),
                last_updated=pd.to_datetime(row.get('Last_Updated', datetime.now()))
            )
            db.add(inventory)
            count += 1
        db.commit()
        return count

    @staticmethod
    def import_payments(file_path: str, db: Session):
        df = pd.read_excel(file_path)
        count = 0
        for _, row in df.iterrows():
            payment = models.Payment(
                payment_id=str(row.get('Payment_ID', str(uuid.uuid4())[:8])),
                reference_id=str(row.get('Reference_ID', '')),
                reference_type=str(row.get('Type', '')),
                party_name=str(row.get('Party_Name', '')),
                amount_paid=float(row.get('Amount_Paid', 0)),
                previous_balance=float(row.get('Total_Amount', 0)), # Approximation
                new_balance=float(row.get('Balance', 0)),
                payment_mode=str(row.get('Payment_Mode', 'Cash')),
                date=pd.to_datetime(row.get('Date', datetime.now())),
                created_by="system"
            )
            db.add(payment)
            count += 1
        db.commit()
        return count
