from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

from app.db.base import get_db
from app.models import models
from app.schemas import hiring_schemas
from app.core import security
from app.core.config import settings

router = APIRouter()
security_bearer = HTTPBearer()

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security_bearer), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        admin_id: str = payload.get("sub")
        user_type: str = payload.get("type")
        if admin_id is None or user_type != "admin":
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    admin = db.query(models.AdminUser).filter(models.AdminUser.admin_id == admin_id).first()
    if admin is None:
        # Check regular users table as well if needed, but for hiring we use AdminUser
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.post("/login")
def admin_login(credentials: dict, db: Session = Depends(get_db)):
    admin = db.query(models.AdminUser).filter(models.AdminUser.username == credentials['username']).first()
    if not admin or not security.verify_password(credentials['password'], admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    admin.last_login = datetime.utcnow()
    db.commit()
    
    access_token = security.create_access_token(
        data={"sub": str(admin.admin_id), "type": "admin", "username": admin.username, "role": admin.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "admin_id": admin.admin_id,
            "username": admin.username,
            "full_name": admin.full_name,
            "role": admin.role
        }
    }

@router.post("/create-job", response_model=hiring_schemas.JobResponse)
def create_job(
    job_in: hiring_schemas.JobCreate,
    current_admin: models.AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    new_job = models.Job(
        job_title=job_in.job_title,
        job_description=job_in.job_description,
        required_machine=job_in.required_machine,
        required_experience=job_in.required_experience,
        required_skill_level=job_in.required_skill_level,
        openings=job_in.openings,
        salary_min=job_in.salary_min,
        salary_max=job_in.salary_max,
        location=job_in.location,
        shift_type=job_in.shift_type,
        employment_type=job_in.employment_type,
        closing_date=datetime.combine(job_in.closing_date, datetime.min.time()) if job_in.closing_date else None,
        posted_by=str(current_admin.admin_id),
        status="Open"
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/jobs", response_model=List[hiring_schemas.JobResponse])
def get_all_jobs(
    status_filter: Optional[str] = None,
    current_admin: models.AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(models.Job)
    if status_filter:
        query = query.filter(models.Job.status == status_filter)
    return query.order_by(models.Job.posted_date.desc()).all()

@router.get("/applications")
def get_all_applications(
    job_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    current_admin: models.AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(
        models.Application.application_id,
        models.Application.job_id,
        models.Application.application_status,
        models.Application.applied_date,
        models.Application.cover_letter,
        models.Application.admin_notes,
        models.Application.interview_date,
        models.Job.job_title,
        models.Job.required_machine,
        models.Job.required_experience,
        models.Worker.aadhar_number,
        models.Worker.name,
        models.Worker.phone,
        models.Worker.email,
        models.Worker.age,
        models.Worker.gender,
        models.Worker.experience_years,
        models.Worker.machine_type,
        models.Worker.skill_level,
        models.Worker.expected_salary
    ).join(models.Job, models.Application.job_id == models.Job.job_id)\
     .join(models.Worker, models.Application.aadhar_number == models.Worker.aadhar_number)
    
    if job_id:
        query = query.filter(models.Application.job_id == job_id)
    if status_filter:
        query = query.filter(models.Application.application_status == status_filter)
    
    results = query.order_by(models.Application.applied_date.desc()).all()
    return [dict(row._mapping) for row in results]

@router.put("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    status_update: dict,
    current_admin: models.AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    new_status = status_update.get('status')
    if new_status not in ['Shortlisted', 'Hired', 'Rejected']:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    application = db.query(models.Application).filter(models.Application.application_id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    job = db.query(models.Job).filter(models.Job.job_id == application.job_id).first()
    worker = db.query(models.Worker).filter(models.Worker.aadhar_number == application.aadhar_number).first()
    
    application.application_status = new_status
    application.reviewed_by = str(current_admin.admin_id)
    application.reviewed_date = datetime.utcnow()
    application.admin_notes = status_update.get('admin_notes', '')
    
    if status_update.get('interview_date'):
        application.interview_date = datetime.fromisoformat(status_update['interview_date'])
    
    if new_status == 'Hired':
        application.hired_date = datetime.utcnow()
        application.offered_salary = status_update.get('offered_salary')
        job.hired_count += 1
        worker.availability_status = 'Employed'
    
    db.commit()
    
    # Send notification
    notification_messages = {
        'Shortlisted': f"Congratulations! You have been shortlisted for {job.job_title}.",
        'Hired': f"Congratulations! You have been hired for {job.job_title}. Welcome aboard!",
        'Rejected': f"Thank you for applying to {job.job_title}. We regret to inform you that we have decided to move forward with other candidates."
    }
    
    notification = models.Notification(
        aadhar_number=worker.aadhar_number,
        notification_type=new_status,
        title=f"Application {new_status}",
        message=notification_messages[new_status],
        job_id=job.job_id,
        application_id=application_id,
        priority="High"
    )
    db.add(notification)
    db.commit()
    
    return {"message": f"Application {new_status.lower()} successfully"}

@router.post("/workers/{aadhar_number}/reviews", response_model=hiring_schemas.WorkerReviewResponse)
def add_worker_review(
    aadhar_number: str,
    review_in: hiring_schemas.WorkerReviewCreate,
    current_admin: models.AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    worker = db.query(models.Worker).filter(models.Worker.aadhar_number == aadhar_number).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    review = models.WorkerReview(
        aadhar_number=aadhar_number,
        reviewer_admin_id=str(current_admin.admin_id),
        rating=review_in.rating,
        comments=review_in.comments
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("/analytics")
def get_analytics(current_admin: models.AdminUser = Depends(get_current_admin), db: Session = Depends(get_db)):
    total_workers = db.query(func.count(models.Worker.aadhar_number)).scalar()
    available_workers = db.query(func.count(models.Worker.aadhar_number)).filter(models.Worker.availability_status == 'Available').scalar()
    total_jobs = db.query(func.count(models.Job.job_id)).scalar()
    open_jobs = db.query(func.count(models.Job.job_id)).filter(models.Job.status == 'Open').scalar()
    total_applications = db.query(func.count(models.Application.application_id)).scalar()
    pending_applications = db.query(func.count(models.Application.application_id)).filter(models.Application.application_status == 'Pending').scalar()
    hired_count = db.query(func.count(models.Application.application_id)).filter(models.Application.application_status == 'Hired').scalar()
    
    workers_by_machine = db.query(models.Worker.machine_type, func.count(models.Worker.aadhar_number)).group_by(models.Worker.machine_type).all()
    
    return {
        "overview": {
            "total_workers": total_workers,
            "available_workers": available_workers,
            "total_jobs": total_jobs,
            "open_jobs": open_jobs,
            "total_applications": total_applications,
            "pending_applications": pending_applications,
            "hired_count": hired_count
        },
        "workers_by_machine": [{"machine_type": r[0], "count": r[1]} for r in workers_by_machine]
    }
