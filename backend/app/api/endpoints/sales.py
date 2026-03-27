from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models import models

from typing import List
from app.schemas import schemas
import uuid

router = APIRouter()

@router.get("/", response_model=List[schemas.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Sale).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleBase, db: Session = Depends(get_db)):
    sale_dict = sale.dict()
    sale_dict["sales_id"] = str(uuid.uuid4())
    
    db_sale = models.Sale(**sale_dict)
    db.add(db_sale)
    
    # Update inventory
    item = db.query(models.Inventory).filter(models.Inventory.item_name == sale.product_name).first()
    if item:
        item.stock_out += sale.quantity
        item.closing_stock -= sale.quantity
        db.commit()
    else:
        # If item doesn't exist in inventory, we still proceed but it's a warning state
        # Usually SALES item should exist in inventory
        db.commit()
        
    db.refresh(db_sale)
    return db_sale

@router.put("/{sales_id}", response_model=schemas.Sale)
def update_sale(sales_id: str, sale: schemas.SaleBase, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.sales_id == sales_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Update fields
    for key, value in sale.dict().items():
        setattr(db_sale, key, value)
    
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.delete("/{sales_id}")
def delete_sale(sales_id: str, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.sales_id == sales_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Update inventory (reduce stock)
    item = db.query(models.Inventory).filter(models.Inventory.item_name == db_sale.product_name).first()
    if item and item.stock_out >= db_sale.quantity:
        item.stock_out -= db_sale.quantity
        item.closing_stock += db_sale.quantity
        db.commit()
    
    db.delete(db_sale)
    db.commit()
    return {"message": "Sale deleted successfully"}
