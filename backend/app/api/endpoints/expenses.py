from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from app.db.base import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Expense])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Expense).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseBase, db: Session = Depends(get_db)):
    expense_dict = expense.dict()
    expense_dict["expense_id"] = str(uuid.uuid4())
    
    db_expense = models.Expense(**expense_dict)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.expense_id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted"}
