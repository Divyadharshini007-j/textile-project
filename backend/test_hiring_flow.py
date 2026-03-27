import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api"

def test_hiring_flow():
    # 1. Create Admin User (Manually in DB for now or via script if endpoint exists)
    # We'll assume the tables exist and we can use the logic
    print("--- Starting Worker Hiring Flow Verification ---")
    
    # 2. Register Worker
    aadhar = str(uuid.uuid4().int)[:12]
    worker_data = {
        "aadhar_number": aadhar,
        "name": "Test Worker",
        "age": 25,
        "gender": "Male",
        "phone": str(uuid.uuid4().int)[:10],
        "email": "test@worker.com",
        "address": "123 Test St",
        "city": "Test City",
        "state": "Test State",
        "experience_years": 3.5,
        "machine_type": "Weaving Machine",
        "skill_level": "Intermediate",
        "password": "password123"
    }
    
    reg_res = requests.post(f"{BASE_URL}/worker/register", json=worker_data)
    if reg_res.status_code == 201:
        print("✅ Worker Registration Successful")
    else:
        print(f"❌ Worker Registration Failed: {reg_res.text}")
        return

    # 3. Worker Login
    login_res = requests.post(f"{BASE_URL}/worker/login", json={
        "aadhar_number": aadhar,
        "password": "password123"
    })
    if login_res.status_code == 200:
        worker_token = login_res.json()["access_token"]
        print("✅ Worker Login Successful")
    else:
        print(f"❌ Worker Login Failed: {login_res.text}")
        return

    # 4. Check Available Jobs
    jobs_res = requests.get(f"{BASE_URL}/worker/available-jobs", headers={"Authorization": f"Bearer {worker_token}"})
    if jobs_res.status_code == 200:
        print(f"✅ Available Jobs Retrieved: {len(jobs_res.json())} found")
    else:
        print(f"❌ Failed to get available jobs: {jobs_res.text}")

    print("--- Verification Script Completed (Partial Flow) ---")
    print("Note: Admin flows (Job Posting/Review) require an existing AdminUser in the database.")

if __name__ == "__main__":
    try:
        test_hiring_flow()
    except Exception as e:
        print(f"Connection error: {e}. Is the server running?")
