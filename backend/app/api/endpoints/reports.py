from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.reports.report_service import ReportService
import io

from app.services.ml_service import MLService

router = APIRouter()

@router.get("/")
def get_reports_info(db: Session = Depends(get_db)):
    """Get available reports and basic stats"""
    return {
        "available_reports": [
            {"name": "Profit & Loss", "endpoint": "/profit-loss", "type": "PDF Download"},
            {"name": "Stock Valuation", "endpoint": "/stock-valuation", "type": "PDF Download"},
            {"name": "Price Prediction Analytics", "endpoint": "/prediction", "type": "PDF Download", "params": ["yarn_type", "quantity"]}
        ],
        "note": "Use specific endpoints to download reports"
    }

@router.get("/profit-loss")
def download_profit_loss(db: Session = Depends(get_db)):
    pdf_buffer = ReportService.generate_profit_loss_pdf(db)
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=profit_loss_report.pdf"}
    )

@router.get("/stock-valuation")
def download_stock_valuation(db: Session = Depends(get_db)):
    pdf_buffer = ReportService.generate_stock_valuation_pdf(db)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=stock_valuation.pdf"}
    )

@router.get("/prediction")
def download_prediction_report(
    yarn_type: str, 
    quantity: float = 1.0, 
    db: Session = Depends(get_db)
):
    ml_service = MLService(db)
    prediction = ml_service.predict_price(yarn_type, quantity)
    
    # Add historical avg for context
    df = ml_service.get_historical_prices(yarn_type)
    if not df.empty:
        prediction["historical_avg"] = round(df['rate'].mean(), 2)
        
    trends = ml_service.get_price_trends(yarn_type)
    
    pdf_buffer = ReportService.generate_prediction_report_pdf(db, yarn_type, prediction, trends)
    
    filename = f"price_analytics_{yarn_type.replace(' ', '_')}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
