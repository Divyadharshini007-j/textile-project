from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.models import models
from app.schemas import schemas
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/")
def read_conversions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Conversion).offset(skip).limit(limit).all()

@router.post("/")
def create_conversion(conversion: schemas.ConversionBase, db: Session = Depends(get_db)):
    # In a real app, this would also update Inventory stock levels
    conversion_dict = conversion.dict()
    conversion_dict["conversion_id"] = str(uuid.uuid4())
    
    # Handle date if not provided
    if not conversion_dict.get("date"):
        conversion_dict["date"] = datetime.now()
    
    db_conversion = models.Conversion(**conversion_dict)
    db.add(db_conversion)
    db.commit()
    db.refresh(db_conversion)
    return db_conversion
