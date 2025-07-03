from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    """Application status tracking"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"

class ApplicationPlatform(str, Enum):
    """Platform where application was submitted"""
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    COMPANY_WEBSITE = "company_website"
    EMAIL = "email"
    RECRUITER = "recruiter"
    OTHER = "other"

class ApplicationFormData(BaseModel):
    """Form data submitted with application"""
    field_name: str = Field(..., description="Form field name")
    field_value: str = Field(..., description="Value entered")
    field_type: str = Field(..., description="Type of field (text, dropdown, etc.)")

class Application(BaseModel):
    """Job application data model"""
    
    # Basic Information
    id: Optional[str] = Field(None, description="Unique application identifier")
    job_id: str = Field(..., description="Associated job ID")
    resume_id: str = Field(..., description="Resume used for application")
    
    # Application Details
    platform: ApplicationPlatform = Field(..., description="Platform used for application")
    platform_application_id: Optional[str] = Field(None, description="Platform-specific application ID")
    
    # Status Tracking
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING, description="Current application status")
    status_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of status changes")
    
    # Application Content
    cover_letter: Optional[str] = Field(None, description="Cover letter content")
    custom_message: Optional[str] = Field(None, description="Custom message to recruiter")
    form_data: List[ApplicationFormData] = Field(default_factory=list, description="Additional form fields")
    
    # Submission Details
    submitted_at: Optional[datetime] = Field(None, description="When application was submitted")
    confirmation_number: Optional[str] = Field(None, description="Application confirmation number")
    
    # Response Tracking
    recruiter_response: Optional[str] = Field(None, description="Response from recruiter")
    interview_scheduled_at: Optional[datetime] = Field(None, description="Interview date/time")
    rejection_reason: Optional[str] = Field(None, description="Reason for rejection if provided")
    
    # Automation Details
    test_mode: bool = Field(True, description="Whether application was in test mode")
    automated: bool = Field(True, description="Whether application was automated")
    review_required: bool = Field(False, description="Whether human review is required")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="When application was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When application was last updated")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Error Tracking
    errors: List[str] = Field(default_factory=list, description="Any errors that occurred")
    retry_count: int = Field(default=0, description="Number of retry attempts")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def add_form_data(self, field_name: str, field_value: str, field_type: str = "text"):
        """Add form field data"""
        form_data = ApplicationFormData(
            field_name=field_name,
            field_value=field_value,
            field_type=field_type
        )
        self.form_data.append(form_data)
        self.updated_at = datetime.now()
        
    def update_status(self, new_status: ApplicationStatus, notes: Optional[str] = None):
        """Update application status with history tracking"""
        old_status = self.status
        self.status = new_status
        
        # Add to history
        status_change = {
            "from_status": old_status,
            "to_status": new_status,
            "timestamp": datetime.now().isoformat(),
            "notes": notes
        }
        self.status_history.append(status_change)
        self.updated_at = datetime.now()
        
    def mark_submitted(self, confirmation_number: Optional[str] = None):
        """Mark application as submitted"""
        self.submitted_at = datetime.now()
        self.confirmation_number = confirmation_number
        self.update_status(ApplicationStatus.SUBMITTED, "Application submitted successfully")
        
    def mark_rejected(self, reason: Optional[str] = None):
        """Mark application as rejected"""
        self.rejection_reason = reason
        self.update_status(ApplicationStatus.REJECTED, f"Application rejected: {reason}" if reason else "Application rejected")
        
    def schedule_interview(self, interview_time: datetime, notes: Optional[str] = None):
        """Schedule interview for application"""
        self.interview_scheduled_at = interview_time
        self.update_status(ApplicationStatus.INTERVIEW_SCHEDULED, notes or "Interview scheduled")
        
    def add_error(self, error_message: str):
        """Add error to application"""
        self.errors.append(f"{datetime.now().isoformat()}: {error_message}")
        self.retry_count += 1
        self.updated_at = datetime.now()
        
    def get_form_data_dict(self) -> Dict[str, str]:
        """Get form data as dictionary"""
        return {field.field_name: field.field_value for field in self.form_data}
        
    def get_status_summary(self) -> Dict[str, Any]:
        """Get application status summary"""
        return {
            "current_status": self.status,
            "submitted_at": self.submitted_at,
            "days_since_submission": (datetime.now() - self.submitted_at).days if self.submitted_at else None,
            "status_changes": len(self.status_history),
            "has_errors": len(self.errors) > 0,
            "retry_count": self.retry_count,
            "test_mode": self.test_mode
        }
        
    def is_active(self) -> bool:
        """Check if application is still active (not rejected, accepted, or withdrawn)"""
        return self.status in [
            ApplicationStatus.PENDING,
            ApplicationStatus.SUBMITTED,
            ApplicationStatus.UNDER_REVIEW,
            ApplicationStatus.INTERVIEW_SCHEDULED
        ]
        
    def requires_follow_up(self) -> bool:
        """Check if application requires follow-up"""
        if not self.submitted_at:
            return False
            
        days_since_submission = (datetime.now() - self.submitted_at).days
        return (
            self.status == ApplicationStatus.SUBMITTED and 
            days_since_submission > 7
        ) or (
            self.status == ApplicationStatus.UNDER_REVIEW and 
            days_since_submission > 14
        ) 