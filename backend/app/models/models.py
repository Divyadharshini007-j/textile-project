from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class StatusEnum(str, enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class PaymentStatusEnum(str, enum.Enum):
    PAID = "Paid"
    UNPAID = "Unpaid"
    PARTIAL = "Partial"

class ExpenseCategoryEnum(str, enum.Enum):
    DIRECT = "Direct"
    INDIRECT = "Indirect"

class PaymentModeEnum(str, enum.Enum):
    CASH = "Cash"
    BANK = "Bank"
    UPI = "UPI"
    CHEQUE = "Cheque"

class ItemTypeEnum(str, enum.Enum):
    YARN = "Yarn"
    FINISHED = "Finished Product"

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    email = Column(String)
    role = Column(String) # Admin/Accountant/etc
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class Supplier(Base):
    __tablename__ = "suppliers"
    supplier_id = Column(String, primary_key=True)
    supplier_name = Column(String)
    contact_person = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    gstin = Column(String)
    payment_terms = Column(String)
    opening_balance = Column(Float, default=0.0)
    status = Column(String, default="Active")
    created_at = Column(DateTime, server_default=func.now())

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String, primary_key=True)
    customer_name = Column(String)
    contact_person = Column(String)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    phone = Column(String)
    email = Column(String)
    gstin = Column(String)
    credit_limit = Column(Float, default=0.0)
    opening_balance = Column(Float, default=0.0)
    status = Column(String, default="Active")
    created_at = Column(DateTime, server_default=func.now())

class Purchase(Base):
    __tablename__ = "purchases"
    purchase_id = Column(String, primary_key=True)
    supplier_id = Column(String, ForeignKey("suppliers.supplier_id"))
    invoice_number = Column(String)
    date = Column(DateTime)
    yarn_type = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    rate = Column(Float)
    total_amount = Column(Float)
    cgst = Column(Float, default=0.0)
    sgst = Column(Float, default=0.0)
    igst = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    grand_total = Column(Float)
    payment_status = Column(String)
    paid_amount = Column(Float, default=0.0)
    balance = Column(Float)
    remarks = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String)

class Sale(Base):
    __tablename__ = "sales"
    sales_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    invoice_number = Column(String)
    date = Column(DateTime)
    product_name = Column(String)
    product_type = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    rate = Column(Float)
    total_amount = Column(Float)
    cgst = Column(Float, default=0.0)
    sgst = Column(Float, default=0.0)
    igst = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    grand_total = Column(Float)
    payment_status = Column(String)
    paid_amount = Column(Float, default=0.0)
    balance = Column(Float)
    shipping_details = Column(String)
    remarks = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String)

class Expense(Base):
    __tablename__ = "expenses"
    expense_id = Column(String, primary_key=True)
    expense_type = Column(String)
    category = Column(String)
    amount = Column(Float)
    date = Column(DateTime)
    description = Column(String)
    vendor_name = Column(String)
    bill_number = Column(String)
    payment_mode = Column(String)
    payment_reference = Column(String)
    remarks = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String)

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(String, primary_key=True)
    reference_id = Column(String)
    reference_type = Column(String) # Purchase/Sales
    party_name = Column(String)
    amount_paid = Column(Float)
    previous_balance = Column(Float)
    new_balance = Column(Float)
    payment_mode = Column(String)
    transaction_id = Column(String)
    date = Column(DateTime)
    remarks = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String)

class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(String, primary_key=True)
    item_name = Column(String)
    item_type = Column(String) # Yarn/Finished Product
    item_category = Column(String)
    unit = Column(String)
    opening_stock = Column(Float, default=0.0)
    stock_in = Column(Float, default=0.0)
    stock_out = Column(Float, default=0.0)
    closing_stock = Column(Float, default=0.0)
    unit_cost = Column(Float, default=0.0)
    total_value = Column(Float, default=0.0)
    last_updated = Column(DateTime, onupdate=func.now())
    location = Column(String)

class Conversion(Base):
    __tablename__ = "conversions"
    conversion_id = Column(String, primary_key=True)
    date = Column(DateTime)
    input_yarn_type = Column(String)
    input_quantity = Column(Float)
    input_cost = Column(Float)
    output_product = Column(String)
    output_quantity = Column(Float)
    labor_cost = Column(Float)
    overhead_cost = Column(Float)
    total_conversion_cost = Column(Float)
    wastage = Column(Float)
    remarks = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class Worker(Base):
    __tablename__ = "workers"
    aadhar_number = Column(String(12), primary_key=True)
    name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20)) # Male/Female/Other
    phone = Column(String(15), unique=True, nullable=False)
    email = Column(String(100))
    address = Column(String)
    city = Column(String(100))
    state = Column(String(100))
    experience_years = Column(Float, nullable=False)
    previous_company = Column(String(200))
    machine_type = Column(String(100), nullable=False)
    skill_level = Column(String(50), nullable=False) # Beginner/Intermediate/Expert
    other_skills = Column(String)
    availability_status = Column(String(50), default="Available") # Available/Employed/Not_Available
    expected_salary = Column(Float)
    password_hash = Column(String(255), nullable=False)
    profile_photo_url = Column(String(500))
    resume_url = Column(String(500))
    registration_date = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String(200), nullable=False)
    job_description = Column(String)
    required_machine = Column(String(100), nullable=False)
    required_experience = Column(Float, nullable=False)
    required_skill_level = Column(String(50), nullable=False)
    openings = Column(Integer, default=1)
    hired_count = Column(Integer, default=0)
    salary_min = Column(Float)
    salary_max = Column(Float)
    location = Column(String(200))
    shift_type = Column(String(50), default="Day")
    employment_type = Column(String(50), default="Full_Time")
    status = Column(String(50), default="Open") # Open/Closed/On_Hold
    posted_date = Column(DateTime, server_default=func.now())
    closing_date = Column(DateTime)
    posted_by = Column(String) # Admin ID

class Application(Base):
    __tablename__ = "applications"
    application_id = Column(Integer, primary_key=True, autoincrement=True)
    aadhar_number = Column(String(12), ForeignKey("workers.aadhar_number"))
    job_id = Column(Integer, ForeignKey("jobs.job_id"))
    application_status = Column(String(50), default="Pending") # Pending/Shortlisted/Hired/Rejected
    applied_date = Column(DateTime, server_default=func.now())
    cover_letter = Column(String)
    worker_notes = Column(String)
    reviewed_by = Column(String)
    reviewed_date = Column(DateTime)
    admin_notes = Column(String)
    interview_date = Column(DateTime)
    hired_date = Column(DateTime)
    joining_date = Column(DateTime)
    offered_salary = Column(Float)

class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    aadhar_number = Column(String(12), ForeignKey("workers.aadhar_number"))
    notification_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(String, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.job_id"))
    application_id = Column(Integer, ForeignKey("applications.application_id"))
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    priority = Column(String(20), default="Medium")

class AdminUser(Base):
    __tablename__ = "admin_users"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="Recruiter") # Super_Admin/HR_Manager/Recruiter
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class MachineType(Base):
    __tablename__ = "machine_types"
    machine_id = Column(Integer, primary_key=True, autoincrement=True)
    machine_name = Column(String(100), unique=True, nullable=False)
    machine_category = Column(String(100))
    description = Column(String)
    is_active = Column(Boolean, default=True)

class WorkerReview(Base):
    __tablename__ = "worker_reviews"
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    aadhar_number = Column(String(12), ForeignKey("workers.aadhar_number"))
    reviewer_admin_id = Column(String)
    rating = Column(Integer)
    comments = Column(String)
    created_at = Column(DateTime, server_default=func.now())
