from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class SupplierBase(BaseModel):
    supplier_name: str
    contact_person: str
    address: str
    phone: str
    email: EmailStr
    gstin: str
    payment_terms: str
    opening_balance: float = 0.0
    status: str = "Active"

class SupplierCreate(SupplierBase):
    supplier_id: str

class Supplier(SupplierBase):
    supplier_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    customer_name: str
    contact_person: str
    address: str
    city: str
    country: str
    phone: str
    email: EmailStr
    gstin: str
    credit_limit: float = 0.0
    opening_balance: float = 0.0
    status: str = "Active"

class CustomerCreate(CustomerBase):
    customer_id: str

class Customer(CustomerBase):
    customer_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PurchaseBase(BaseModel):
    supplier_id: str
    invoice_number: str
    date: datetime
    yarn_type: str
    quantity: float
    unit: str
    rate: float
    total_amount: float
    cgst: Optional[float] = 0.0
    sgst: Optional[float] = 0.0
    igst: Optional[float] = 0.0
    tax_amount: Optional[float] = 0.0
    grand_total: float
    payment_status: str = "Unpaid"
    paid_amount: float = 0.0
    balance: float
    remarks: Optional[str] = None

class PurchaseCreate(PurchaseBase):
    purchase_id: str

class Purchase(PurchaseBase):
    purchase_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    customer_id: str
    invoice_number: str
    date: datetime
    product_name: str
    product_type: str
    quantity: float
    unit: str
    rate: float
    total_amount: float
    cgst: Optional[float] = 0.0
    sgst: Optional[float] = 0.0
    igst: Optional[float] = 0.0
    tax_amount: Optional[float] = 0.0
    grand_total: float
    payment_status: str = "Unpaid"
    paid_amount: float = 0.0
    balance: float
    shipping_details: Optional[str] = None
    remarks: Optional[str] = None

class SaleCreate(SaleBase):
    sales_id: str

class Sale(SaleBase):
    sales_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class ConversionBase(BaseModel):
    date: datetime
    input_yarn_type: str
    input_quantity: float
    input_cost: float
    output_product: str
    output_quantity: float
    labor_cost: float
    overhead_cost: float
    total_conversion_cost: float
    wastage: float
    remarks: Optional[str] = None

class ConversionCreate(ConversionBase):
    conversion_id: str

class Conversion(ConversionBase):
    conversion_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    expense_type: str
    category: str
    amount: float
    date: datetime
    description: Optional[str] = None
    vendor_name: Optional[str] = None
    bill_number: Optional[str] = None
    payment_mode: str
    payment_reference: Optional[str] = None
    remarks: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    expense_id: str

class Expense(ExpenseBase):
    expense_id: str
    created_at: datetime
    class Config:
        from_attributes = True

class InventoryBase(BaseModel):
    item_name: str
    item_type: str
    item_category: str
    unit: str
    opening_stock: float = 0.0
    stock_in: float = 0.0
    stock_out: float = 0.0
    closing_stock: float = 0.0
    unit_cost: float = 0.0
    total_value: float = 0.0
    location: Optional[str] = None

class InventoryCreate(InventoryBase):
    inventory_id: str

class Inventory(InventoryBase):
    inventory_id: str
    last_updated: Optional[datetime]
    class Config:
        from_attributes = True
