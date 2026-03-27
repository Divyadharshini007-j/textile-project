from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.ml_service import MLService
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class PredictionResponse(BaseModel):
    predicted_price: float
    confidence: str
    trend: str
    history_count: Optional[int] = None
    historical_avg: Optional[float] = None
    three_month_prediction: Optional[List[dict]] = []
    model_accuracy: Optional[float] = None

class PriceTrendPoint(BaseModel):
    month: str
    rate: float
    is_projection: Optional[bool] = False

@router.get("/yarn-types", response_model=List[str])
def get_yarn_types(db: Session = Depends(get_db)):
    ml_service = MLService(db)
    return ml_service.get_available_yarn_types()

@router.get("/predict", response_model=PredictionResponse)
def get_prediction(
    yarn_type: str = Query(..., description="Type of yarn"),
    quantity: float = Query(1.0, description="Quantity for prediction"),
    db: Session = Depends(get_db)
):
    ml_service = MLService(db)
    prediction = ml_service.predict_price(yarn_type, quantity)
    
    # Add historical avg for context
    df = ml_service.get_historical_prices(yarn_type)
    if not df.empty:
        prediction["historical_avg"] = round(df['rate'].mean(), 2)
        
    return prediction

@router.get("/trends", response_model=List[PriceTrendPoint])
def get_trends(
    yarn_type: str = Query(..., description="Type of yarn"),
    db: Session = Depends(get_db)
):
    ml_service = MLService(db)
    trends = ml_service.get_price_trends(yarn_type)
    return trends

@router.get("/historical")
def get_historical_data(
    yarn_type: str = Query(..., description="Type of yarn"),
    db: Session = Depends(get_db)
):
    ml_service = MLService(db)
    df = ml_service.get_historical_prices(yarn_type)
    
    if df.empty:
        return []
    
    # Convert to list of dicts with relevant fields
    historical_data = []
    for _, row in df.iterrows():
        historical_data.append({
            "date": row['date'].isoformat(),
            "quantity": row['quantity'],
            "rate": row['rate'],
            "total_amount": row['total_amount']
        })
    
    # Sort by date (most recent first)
    historical_data.sort(key=lambda x: x['date'], reverse=True)
    return historical_data
