import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api"

def test_admin_hiring_flow():
    print("--- Starting Admin Hiring Flow Verification ---")
    
    # 1. Admin Login
    login_data = {
        "username": "hiring_admin",
        "password": "admin123"
    }
    login_res = requests.post(f"{BASE_URL}/admin/hiring/login", json=login_data)
    if login_res.status_code == 200:
        admin_token = login_res.json()["access_token"]
        print("✅ Admin Login Successful")
    else:
        print(f"❌ Admin Login Failed: {login_res.text}")
        return

    # 2. Create Job
    job_data = {
        "job_title": "Expert Weaver",
        "job_description": "Looking for an expert weaver with 5+ years experience.",
        "required_machine": "Weaving Machine",
        "required_experience": 5.0,
        "required_skill_level": "Expert",
        "openings": 2,
        "salary_min": 25000,
        "salary_max": 35000,
        "location": "Surat",
        "closing_date": (date.today() + timedelta(days=30)).isoformat()
    }
    job_res = requests.post(f"{BASE_URL}/admin/hiring/create-job", json=job_data, headers={"Authorization": f"Bearer {admin_token}"})
    if job_res.status_code == 200:
        print("✅ Job Creation Successful")
    else:
        print(f"❌ Job Creation Failed: {job_res.text}")
        return

    # 3. Get Jobs
    jobs_res = requests.get(f"{BASE_URL}/admin/hiring/jobs", headers={"Authorization": f"Bearer {admin_token}"})
    if jobs_res.status_code == 200:
        print(f"✅ Jobs Retrieved: {len(jobs_res.json())} found")
    else:
        print(f"❌ Failed to get jobs: {jobs_res.text}")

    print("--- Admin Verification Script Completed ---")

if __name__ == "__main__":
    try:
        test_admin_hiring_flow()
    except Exception as e:
        print(f"Connection error: {e}")
