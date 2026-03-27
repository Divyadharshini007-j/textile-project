"""
Seed demo data: 1 worker + 1 job + 1 application so admin can see and test the full hire flow.
Run: python seed_demo_hiring.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.base import SessionLocal, engine
from app.models import models
from app.core.security import get_password_hash
from datetime import datetime

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # ── 1. Ensure admin user exists ─────────────────────────────────────────
    admin = db.query(models.AdminUser).filter(models.AdminUser.username == "hiring_admin").first()
    if not admin:
        admin = models.AdminUser(
            username="hiring_admin",
            full_name="Hiring Administrator",
            email="admin@textile.com",
            password_hash=get_password_hash("admin123"),
            role="Super_Admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("✅ Admin user created: hiring_admin / admin123")
    else:
        print(f"✅ Admin already exists: {admin.username}")

    # ── 2. Create demo worker ────────────────────────────────────────────────
    worker = db.query(models.Worker).filter(models.Worker.aadhar_number == "111122223333").first()
    if not worker:
        worker = models.Worker(
            aadhar_number="111122223333",
            name="Ravi Kumar",
            age=30,
            gender="Male",
            phone="9876500001",
            email="ravi@example.com",
            address="12 Gandhi Street",
            city="Coimbatore",
            state="Tamil Nadu",
            experience_years=4.0,
            previous_company="Lakshmi Mills",
            machine_type="Weaving Machine",
            skill_level="Intermediate",
            expected_salary=18000,
            availability_status="Available",
            password_hash=get_password_hash("ravi1234"),
            is_active=True
        )
        db.add(worker)
        db.commit()
        db.refresh(worker)
        print("✅ Demo worker created: Aadhar=111122223333 / Password=ravi1234")
    else:
        print(f"✅ Worker already exists: {worker.name}")

    # ── 3. Create demo job ───────────────────────────────────────────────────
    job = db.query(models.Job).filter(models.Job.job_title == "Senior Weaving Operator").first()
    if not job:
        job = models.Job(
            job_title="Senior Weaving Operator",
            job_description="Operate and maintain weaving machines for fabric production. Ensure quality standards.",
            required_machine="Weaving Machine",
            required_experience=2.0,
            required_skill_level="Intermediate",
            openings=3,
            hired_count=0,
            salary_min=15000,
            salary_max=22000,
            location="Coimbatore",
            shift_type="Day",
            employment_type="Full_Time",
            status="Open",
            posted_by=str(admin.admin_id)
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        print(f"✅ Demo job created: [{job.job_id}] {job.job_title}")
    else:
        print(f"✅ Job already exists: {job.job_title}")

    # ── 4. Create demo application ───────────────────────────────────────────
    app = db.query(models.Application).filter(
        models.Application.aadhar_number == worker.aadhar_number,
        models.Application.job_id == job.job_id
    ).first()
    if not app:
        app = models.Application(
            aadhar_number=worker.aadhar_number,
            job_id=job.job_id,
            application_status="Pending",
            cover_letter="I have 4 years of experience with weaving machines at Lakshmi Mills. I am a quick learner and a team player.",
            applied_date=datetime.utcnow()
        )
        db.add(app)
        db.commit()
        db.refresh(app)
        print(f"✅ Demo application created: App#{app.application_id} — {worker.name} → {job.job_title}")
    else:
        print(f"✅ Application already exists: App#{app.application_id}")

    existing_review = db.query(models.WorkerReview).filter(models.WorkerReview.aadhar_number == worker.aadhar_number).first()
    if not existing_review:
        review = models.WorkerReview(
            aadhar_number=worker.aadhar_number,
            reviewer_admin_id=str(admin.admin_id),
            rating=4,
            comments="Good technical skills; punctual and reliable."
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        print(f"✅ Demo review created: Rating {review.rating}")
    else:
        print("✅ Review already exists")

    print("\n🎉 Demo data ready!")
    print("=" * 50)
    print("WORKER LOGIN:  Aadhar=111122223333  Password=ravi1234")
    print("ADMIN LOGIN:   Username=hiring_admin  Password=admin123")
    print("=" * 50)
    print("\nFlow to test:")
    print("1. Go to http://localhost:5173/admin/hiring → login as hiring_admin/admin123")
    print("2. Click 'Review Applications' tab → see Ravi Kumar's application")
    print("3. Click 'Review' → select '🎉 Hire' → enter salary → click 'Confirm Hired'")
    print("4. Go to http://localhost:5173/worker/login → login as 111122223333/ravi1234")
    print("5. Click 'Notifications' tab → see 'Congratulations! You have been hired!'")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
