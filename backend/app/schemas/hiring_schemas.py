from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# Enums
class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class SkillLevelEnum(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    EXPERT = "Expert"

class AvailabilityEnum(str, Enum):
    AVAILABLE = "Available"
    EMPLOYED = "Employed"
    NOT_AVAILABLE = "Not_Available"

class ApplicationStatusEnum(str, Enum):
    PENDING = "Pending"
    SHORTLISTED = "Shortlisted"
    HIRED = "Hired"
    REJECTED = "Rejected"

# Worker Models
class WorkerRegistration(BaseModel):
    aadhar_number: str = Field(..., min_length=12, max_length=12)
    name: str = Field(..., min_length=2, max_length=200)
    age: int = Field(..., ge=18, le=65)
    gender: str
    phone: str = Field(...)
    email: Optional[EmailStr] = None
    address: str
    city: str
    state: str
    experience_years: float = Field(..., ge=0, le=50)
    previous_company: Optional[str] = None
    machine_type: str
    skill_level: str
    other_skills: Optional[str] = None
    expected_salary: Optional[float] = None
    password: str = Field(..., min_length=6)
    
    @validator('aadhar_number')
    def validate_aadhar(cls, v):
        if not v.isdigit():
            raise ValueError('Aadhar number must contain only digits')
        return v

class WorkerLogin(BaseModel):
    aadhar_number: str
    password: str

class WorkerProfile(BaseModel):
    aadhar_number: str
    name: str
    age: int
    gender: str
    phone: str
    email: Optional[str]
    experience_years: float
    machine_type: str
    skill_level: str
    availability_status: str
    registration_date: datetime

    class Config:
        from_attributes = True

# Job Models
class JobCreate(BaseModel):
    job_title: str
    job_description: str
    required_machine: str
    required_experience: float
    required_skill_level: str
    openings: int = Field(..., gt=0)
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    location: str
    shift_type: str = "Day"
    employment_type: str = "Full_Time"
    closing_date: Optional[date] = None

class JobResponse(BaseModel):
    job_id: int
    job_title: str
    job_description: str
    required_machine: str
    required_experience: float
    required_skill_level: str
    openings: int
    hired_count: int
    salary_min: Optional[float]
    salary_max: Optional[float]
    location: str
    shift_type: Optional[str] = None
    employment_type: Optional[str] = None
    status: str
    posted_date: datetime
    closing_date: Optional[date]

    class Config:
        from_attributes = True

# Application Models
class JobApplication(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None

class ApplicationResponse(BaseModel):
    application_id: int
    job_id: int
    job_title: str
    application_status: str
    applied_date: datetime
    reviewed_date: Optional[datetime]
    admin_notes: Optional[str]
    interview_date: Optional[datetime]

    class Config:
        from_attributes = True

# Notification Models
class NotificationResponse(BaseModel):
    notification_id: int
    notification_type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    job_id: Optional[int]

    class Config:
        from_attributes = True

class WorkerReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None

class WorkerReviewResponse(BaseModel):
    review_id: int
    aadhar_number: str
    reviewer_admin_id: Optional[str]
    rating: int
    comments: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
