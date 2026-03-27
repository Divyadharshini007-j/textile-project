"""
Test script to verify the improved ML predictions.
"""
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.services.ml_service import MLService

def test_predictions():
    db = SessionLocal()
    ml_service = MLService(db)
    
    print("=" * 80)
    print("YARN PRICE PREDICTION TEST")
    print("=" * 80)
    
    # Get available yarn types
    yarn_types = ml_service.get_available_yarn_types()
    print(f"\nAvailable Yarn Types: {yarn_types}\n")
    
    for yarn_type in yarn_types:
        print(f"\n{'=' * 80}")
        print(f"Testing: {yarn_type}")
        print('=' * 80)
        
        # Get historical data summary
        df = ml_service.get_historical_prices(yarn_type)
        if not df.empty:
            print(f"\nHistorical Data Summary:")
            print(f"  Records: {len(df)}")
            print(f"  Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
            print(f"  Rate Range: ₹{df['rate'].min():.2f} to ₹{df['rate'].max():.2f}")
            print(f"  Average Rate: ₹{df['rate'].mean():.2f}")
            print(f"  Recent Avg (last 3): ₹{df.sort_values('date')['rate'].tail(3).mean():.2f}")
            
            # Show trend in data
            recent_avg = df.sort_values('date')['rate'].tail(5).mean()
            older_avg = df.sort_values('date')['rate'].head(5).mean()
            if recent_avg > older_avg * 1.03:
                data_trend = "Rising"
            elif recent_avg < older_avg * 0.97:
                data_trend = "Falling"
            else:
                data_trend = "Stable"
            print(f"  Data Trend: {data_trend} (Recent: ₹{recent_avg:.2f} vs Older: ₹{older_avg:.2f})")
        
        # Test predictions with different quantities
        quantities = [100, 500, 1000]
        print(f"\nPredictions:")
        for qty in quantities:
            prediction = ml_service.predict_price(yarn_type, qty)
            print(f"\n  Quantity: {qty} kg")
            print(f"    Predicted Price: ₹{prediction['predicted_price']:.2f}")
            print(f"    Confidence: {prediction['confidence']}")
            print(f"    Trend: {prediction['trend']}")
            print(f"    Data Points: {prediction.get('history_count', 'N/A')}")
        
        # Get price trends
        trends = ml_service.get_price_trends(yarn_type)
        if trends:
            print(f"\n  Price Trends (Historical + Projected):")
            for trend in trends:
                marker = "📊" if not trend['is_projection'] else "🔮"
                print(f"    {marker} {trend['month']}: ₹{trend['rate']:.2f}")
    
    db.close()
    print("\n" + "=" * 80)
    print("Test Complete!")
    print("=" * 80)

if __name__ == "__main__":
    test_predictions()
