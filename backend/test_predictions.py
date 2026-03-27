import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/predictions"

def test_predictions():
    print("Testing Price Prediction Endpoints...")
    
    # Test Prediction
    yarn_type = "Cotton Yarn 40s"
    try:
        print(f"\n1. Testing /predict for {yarn_type}...")
        resp = requests.get(f"{BASE_URL}/predict", params={"yarn_type": yarn_type, "quantity": 100})
        if resp.status_code == 200:
            print("SUCCESS: /predict returned 200")
            print(json.dumps(resp.json(), indent=2))
        else:
            print(f"FAILED: /predict returned {resp.status_code}")
            print(resp.text)
            
        print(f"\n2. Testing /trends for {yarn_type}...")
        resp = requests.get(f"{BASE_URL}/trends", params={"yarn_type": yarn_type})
        if resp.status_code == 200:
            print("SUCCESS: /trends returned 200")
            data = resp.json()
            print(f"Received {len(data)} trend points")
            if len(data) > 0:
                print("Last point:", json.dumps(data[-1], indent=2))
        else:
            print(f"FAILED: /trends returned {resp.status_code}")
            print(resp.text)
            
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to backend. Please ensure the FastAPI server is running at http://127.0.0.1:8000")

if __name__ == "__main__":
    test_predictions()
