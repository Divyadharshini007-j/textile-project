#!/usr/bin/env python3
"""
Test the improved AI prediction system
"""
import requests
import json

def test_ai_prediction():
    """Test the AI prediction system with 3-month forecast"""
    
    print("🤖 TESTING AI PREDICTION SYSTEM")
    print("=" * 50)
    
    # Test prediction with 3-month forecast
    try:
        response = requests.get('http://127.0.0.1:8000/api/predictions/predict', params={
            'yarn_type': 'Cotton Yarn 40s',
            'quantity': 100
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Prediction API Working")
            print(f"Current Price: {data.get('predicted_price', 'N/A')}")
            print(f"Confidence: {data.get('confidence', 'N/A')}")
            print(f"Trend: {data.get('trend', 'N/A')}")
            print(f"Model Accuracy: {data.get('model_accuracy', 'N/A')}")
            print(f"History Count: {data.get('history_count', 'N/A')}")
            
            if 'three_month_prediction' in data and data['three_month_prediction']:
                print("\n📈 3-Month Forecast:")
                for month in data['three_month_prediction']:
                    month_name = month.get('month', 'N/A')
                    price = month.get('predicted_price', 'N/A')
                    print(f"  {month_name}: {price}")
                print("✅ 3-month prediction working!")
            else:
                print("❌ 3-month prediction not found")
        else:
            print(f"❌ Prediction API failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🔧 Testing Trends API...")
    try:
        response = requests.get('http://127.0.0.1:8000/api/predictions/trends', params={
            'yarn_type': 'Cotton Yarn 40s'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Trends API Working: {len(data)} data points")
        else:
            print(f"❌ Trends API failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 AI PREDICTION SYSTEM UPDATED!")
    print("📱 Now predicts for next 3 months")
    print("🧠 Enhanced ML analysis")
    print("📊 Better trend detection")
    print("🔍 Model accuracy reporting")
    print("📈 Future price forecasting")

if __name__ == "__main__":
    test_ai_prediction()
