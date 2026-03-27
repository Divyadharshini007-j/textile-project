from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.base import get_db
from app.models import models
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/kpi")
def get_kpis(db: Session = Depends(get_db)):
    total_purchases = db.query(func.sum(models.Purchase.grand_total)).scalar() or 0
    total_sales = db.query(func.sum(models.Sale.grand_total)).scalar() or 0
    total_expenses = db.query(func.sum(models.Expense.amount)).scalar() or 0
    
    current_stock_value = db.query(func.sum(models.Inventory.total_value)).scalar() or 0
    customer_receivables = db.query(func.sum(models.Sale.balance)).scalar() or 0
    supplier_payables = db.query(func.sum(models.Purchase.balance)).scalar() or 0
    
    # Net Profit = (Total Sales + Current Stock Value) - (Purchase Cost + Conversion Cost + Expenses)
    # Conversion cost is 0 for now as we just imported basic data
    # Ensure net profit never shows negative values
    calculated_profit = (total_sales + current_stock_value) - (total_purchases + total_expenses)
    net_profit = max(0, calculated_profit)  # Show 0 instead of negative values
    
    return {
        "total_purchases": total_purchases,
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "customer_receivables": customer_receivables,
        "supplier_payables": supplier_payables,
        "current_stock_value": current_stock_value
    }

@router.get("/charts")
def get_charts(db: Session = Depends(get_db)):
    # Monthly sales trend
    sales_trend = db.query(
        func.strftime('%m', models.Sale.date).label('month'),
        func.sum(models.Sale.grand_total).label('total')
    ).group_by('month').all()
    
    return {
        "revenue_trend": [{"month": r.month, "total": r.total} for r in sales_trend]
    }
