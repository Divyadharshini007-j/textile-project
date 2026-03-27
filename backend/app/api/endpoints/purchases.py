from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

import uuid

@router.get("/", response_model=List[schemas.Purchase])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Purchase).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseBase, db: Session = Depends(get_db)):
    purchase_dict = purchase.dict()
    purchase_dict["purchase_id"] = str(uuid.uuid4())
    
    db_purchase = models.Purchase(**purchase_dict)
    db.add(db_purchase)
    
    # Update inventory
    item = db.query(models.Inventory).filter(models.Inventory.item_name == purchase.yarn_type).first()
    if item:
        item.stock_in += purchase.quantity
        item.closing_stock += purchase.quantity
    else:
        # Create new inventory item if it doesn't exist
        new_item = models.Inventory(
            inventory_id=str(uuid.uuid4()),
            item_name=purchase.yarn_type,
            item_type="Yarn",
            item_category="Raw Material",
            unit=purchase.unit,
            opening_stock=0,
            stock_in=purchase.quantity,
            stock_out=0,
            closing_stock=purchase.quantity,
            unit_cost=purchase.rate
        )
        db.add(new_item)
        
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@router.put("/{purchase_id}", response_model=schemas.Purchase)
def update_purchase(purchase_id: str, purchase: schemas.PurchaseBase, db: Session = Depends(get_db)):
    db_purchase = db.query(models.Purchase).filter(models.Purchase.purchase_id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    # Update fields
    for key, value in purchase.dict().items():
        setattr(db_purchase, key, value)
    
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: str, db: Session = Depends(get_db)):
    db_purchase = db.query(models.Purchase).filter(models.Purchase.purchase_id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    # Update inventory (reduce stock)
    item = db.query(models.Inventory).filter(models.Inventory.item_name == db_purchase.yarn_type).first()
    if item and item.stock_in >= db_purchase.quantity:
        item.stock_in -= db_purchase.quantity
        item.closing_stock -= db_purchase.quantity
        db.commit()
    
    db.delete(db_purchase)
    db.commit()
    return {"message": "Purchase deleted successfully"}
