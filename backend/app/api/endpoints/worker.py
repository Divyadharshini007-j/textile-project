from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.base import get_db
from app.models import models
from app.schemas import hiring_schemas
from app.core import security
from app.core.config import settings

router = APIRouter()
security_bearer = HTTPBearer()

def get_current_worker(credentials: HTTPAuthorizationCredentials = Depends(security_bearer), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        aadhar_number: str = payload.get("sub")
        user_type: str = payload.get("type")
        if aadhar_number is None or user_type != "worker":
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    worker = db.query(models.Worker).filter(models.Worker.aadhar_number == aadhar_number).first()
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_worker(worker_in: hiring_schemas.WorkerRegistration, db: Session = Depends(get_db)):
    existing_worker = db.query(models.Worker).filter(models.Worker.aadhar_number == worker_in.aadhar_number).first()
    if existing_worker:
        raise HTTPException(status_code=400, detail="Aadhar number already registered")
    
    existing_phone = db.query(models.Worker).filter(models.Worker.phone == worker_in.phone).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    hashed_password = security.get_password_hash(worker_in.password)
    
    new_worker = models.Worker(
        aadhar_number=worker_in.aadhar_number,
        name=worker_in.name,
        age=worker_in.age,
        gender=worker_in.gender,
        phone=worker_in.phone,
        email=str(worker_in.email) if worker_in.email else None,
        address=worker_in.address,
        city=worker_in.city,
        state=worker_in.state,
        experience_years=worker_in.experience_years,
        previous_company=worker_in.previous_company,
        machine_type=worker_in.machine_type,
        skill_level=worker_in.skill_level,
        other_skills=worker_in.other_skills,
        expected_salary=worker_in.expected_salary,
        password_hash=hashed_password,
        availability_status="Available"
    )
    db.add(new_worker)
    db.commit()
    db.refresh(new_worker)
    
    return {"message": "Worker registered successfully", "aadhar_number": new_worker.aadhar_number}

@router.post("/login")
def login_worker(credentials: hiring_schemas.WorkerLogin, db: Session = Depends(get_db)):
    worker = db.query(models.Worker).filter(models.Worker.aadhar_number == credentials.aadhar_number).first()
    if not worker or not security.verify_password(credentials.password, worker.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Aadhar number or password")
    
    if not worker.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    
    worker.last_login = datetime.utcnow()
    db.commit()
    
    access_token = security.create_access_token(
        data={"sub": worker.aadhar_number, "type": "worker", "name": worker.name}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "aadhar_number": worker.aadhar_number,
            "name": worker.name,
            "machine_type": worker.machine_type,
            "skill_level": worker.skill_level
        }
    }

@router.get("/profile", response_model=hiring_schemas.WorkerProfile)
def get_worker_profile(current_worker: models.Worker = Depends(get_current_worker)):
    return current_worker

@router.get("/available-jobs", response_model=List[hiring_schemas.JobResponse])
def get_available_jobs(
    machine_type: Optional[str] = None,
    min_experience: Optional[float] = None,
    show_all: Optional[bool] = False,  # Debug parameter to show all open jobs
    current_worker: models.Worker = Depends(get_current_worker),
    db: Session = Depends(get_db)
):
    query = db.query(models.Job).filter(
        models.Job.status == "Open",
        models.Job.openings > models.Job.hired_count
    )
    
    # If show_all is True, don't apply machine/experience filters
    if not show_all:
        # Filter by machine type (case-insensitive and more flexible)
        if machine_type:
            query = query.filter(models.Job.required_machine.ilike(f"%{machine_type}%"))
        else:
            # Match worker's machine type with flexible matching
            query = query.filter(
                models.Job.required_machine.ilike(f"%{current_worker.machine_type}%")
            )
        
        # Filter by experience (allow workers with more experience than required)
        if min_experience is not None:
            query = query.filter(models.Job.required_experience <= min_experience)
        else:
            query = query.filter(models.Job.required_experience <= current_worker.experience_years)
    
    jobs = query.order_by(models.Job.posted_date.desc()).all()
    
    # Debug: Add worker info to response for troubleshooting
    if show_all:
        print(f"DEBUG: Worker {current_worker.name} - Machine: {current_worker.machine_type}, Experience: {current_worker.experience_years}")
        print(f"DEBUG: Found {len(jobs)} open jobs")
        for job in jobs[:3]:  # Show first 3 jobs for debug
            print(f"DEBUG: Job - {job.job_title}, Machine: {job.required_machine}, Experience: {job.required_experience}")
    
    return jobs

@router.post("/apply-job")
def apply_for_job(
    application_in: hiring_schemas.JobApplication,
    current_worker: models.Worker = Depends(get_current_worker),
    db: Session = Depends(get_db)
):
    job = db.query(models.Job).filter(models.Job.job_id == application_in.job_id, models.Job.status == "Open").first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or closed")
    
    existing_app = db.query(models.Application).filter(
        models.Application.aadhar_number == current_worker.aadhar_number,
        models.Application.job_id == application_in.job_id
    ).first()

    if existing_app:
        if existing_app.application_status == 'Rejected':
            raise HTTPException(status_code=400, detail="Your application was rejected. Reapplying is not allowed for this job.")
        if existing_app.application_status in ['Pending', 'Shortlisted', 'Hired']:
            raise HTTPException(status_code=400, detail="Already applied for this job")
    
    new_app = models.Application(
        aadhar_number=current_worker.aadhar_number,
        job_id=application_in.job_id,
        application_status="Pending",
        cover_letter=application_in.cover_letter
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    
    # Create notification
    notification = models.Notification(
        aadhar_number=current_worker.aadhar_number,
        notification_type="Application_Submitted",
        title="Application Submitted",
        message=f"Your application for {job.job_title} has been submitted successfully.",
        job_id=job.job_id,
        application_id=new_app.application_id
    )
    db.add(notification)
    db.commit()
    
    return {"message": "Application submitted successfully", "application_id": new_app.application_id}

@router.get("/reviews")
def get_worker_reviews(current_worker: models.Worker = Depends(get_current_worker), db: Session = Depends(get_db)):
    reviews = db.query(models.WorkerReview).filter(models.WorkerReview.aadhar_number == current_worker.aadhar_number).order_by(models.WorkerReview.created_at.desc()).all()
    return reviews

@router.get("/application-status", response_model=List[hiring_schemas.ApplicationResponse])
def get_application_status(current_worker: models.Worker = Depends(get_current_worker), db: Session = Depends(get_db)):
    results = db.query(
        models.Application.application_id,
        models.Application.job_id,
        models.Job.job_title,
        models.Application.application_status,
        models.Application.applied_date,
        models.Application.reviewed_date,
        models.Application.admin_notes,
        models.Application.interview_date
    ).join(models.Job, models.Application.job_id == models.Job.job_id)\
     .filter(models.Application.aadhar_number == current_worker.aadhar_number)\
     .order_by(models.Application.applied_date.desc()).all()
    
    return results

@router.get("/notifications", response_model=List[hiring_schemas.NotificationResponse])
def get_notifications(
    unread_only: bool = False,
    current_worker: models.Worker = Depends(get_current_worker),
    db: Session = Depends(get_db)
):
    query = db.query(models.Notification).filter(models.Notification.aadhar_number == current_worker.aadhar_number)
    if unread_only:
        query = query.filter(models.Notification.is_read == False)
    
    return query.order_by(models.Notification.created_at.desc()).limit(50).all()

@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_worker: models.Worker = Depends(get_current_worker),
    db: Session = Depends(get_db)
):
    notification = db.query(models.Notification).filter(
        models.Notification.notification_id == notification_id,
        models.Notification.aadhar_number == current_worker.aadhar_number
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Notification marked as read"}

from datetime import datetime
