import sys
import os
from fastapi.testclient import TestClient

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.getcwd()))

from app.main import app

client = TestClient(app)

def test_endpoints():
    print("Testing /api/purchases/ ...")
    try:
        response = client.get("/api/purchases/")
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Exception calling /api/purchases/: {e}")

    print("\nTesting /api/sales/ ...")
    try:
        response = client.get("/api/sales/")
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Exception calling /api/sales/: {e}")

if __name__ == "__main__":
    test_endpoints()
