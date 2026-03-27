from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import suppliers, customers, dashboard, sales, purchases, auth, conversions, reports, predictions, expenses, worker, admin_hiring, inventory, health
from app.db.base import engine, Base

app = FastAPI(title="Yarn Trading Accountancy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(suppliers.router, prefix="/api/suppliers", tags=["suppliers"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(sales.router, prefix="/api/sales", tags=["sales"])
app.include_router(purchases.router, prefix="/api/purchases", tags=["purchases"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(conversions.router, prefix="/api/conversions", tags=["conversions"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
app.include_router(worker.router, prefix="/api/worker", tags=["worker"])
app.include_router(admin_hiring.router, prefix="/api/admin/hiring", tags=["admin_hiring"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
app.include_router(health.router, prefix="/health", tags=["health"])


# Create tables after routers are imported (models loaded)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Yarn Trading Accountancy API"}

