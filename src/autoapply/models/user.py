from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserProfile(BaseModel):
    """User profile with preferences and settings"""
    
    # Personal Information
    name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    phone: Optional[str] = Field(None, description="User's phone number")
    location: Optional[str] = Field(None, description="User's current location")
    
    # Professional Information
    current_title: Optional[str] = Field(None, description="Current job title")
    experience_years: Optional[int] = Field(None, description="Years of professional experience")
    industry: Optional[str] = Field(None, description="Industry/field")
    
    # Skills and Preferences
    skills: List[str] = Field(default_factory=list, description="List of user's skills")
    preferred_locations: List[str] = Field(default_factory=list, description="Preferred job locations")
    preferred_job_types: List[str] = Field(default_factory=list, description="Preferred job types (full-time, contract, etc.)")
    salary_range: Optional[str] = Field(None, description="Desired salary range")
    
    # Job Search Preferences
    job_search_status: str = Field(default="active", description="Job search status")
    target_companies: List[str] = Field(default_factory=list, description="Target companies")
    excluded_companies: List[str] = Field(default_factory=list, description="Companies to exclude")
    keywords: List[str] = Field(default_factory=list, description="Job search keywords")
    
    # Automation Preferences
    max_applications_per_day: int = Field(default=5, description="Maximum applications per day")
    preferred_tailoring_mode: str = Field(default="conservative", description="Preferred resume tailoring mode")
    auto_apply_enabled: bool = Field(default=False, description="Whether auto-apply is enabled")
    
    # Platform Preferences
    linkedin_profile_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    portfolio_url: Optional[str] = Field(None, description="Portfolio website URL")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")
    
    # Additional Context
    work_context: Optional[str] = Field(None, description="Additional work context and notes")
    career_goals: Optional[str] = Field(None, description="Career goals and aspirations")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="When profile was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When profile was last updated")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def update_skills(self, new_skills: List[str]):
        """Update user skills"""
        self.skills = list(set(self.skills + new_skills))
        self.updated_at = datetime.now()
        
    def add_target_company(self, company: str):
        """Add a target company"""
        if company not in self.target_companies:
            self.target_companies.append(company)
            self.updated_at = datetime.now()
            
    def exclude_company(self, company: str):
        """Add a company to exclusion list"""
        if company not in self.excluded_companies:
            self.excluded_companies.append(company)
            self.updated_at = datetime.now()
            
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get profile summary"""
        return {
            "name": self.name,
            "current_title": self.current_title,
            "experience_years": self.experience_years,
            "skills_count": len(self.skills),
            "preferred_locations": self.preferred_locations,
            "job_search_status": self.job_search_status,
            "auto_apply_enabled": self.auto_apply_enabled,
            "max_applications_per_day": self.max_applications_per_day
        }

class User(BaseModel):
    """Main user model"""
    
    # Basic Information
    id: Optional[str] = Field(None, description="Unique user identifier")
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="User's email address")
    
    # Profile
    profile: UserProfile = Field(..., description="User profile information")
    
    # System Settings
    is_active: bool = Field(default=True, description="Whether user account is active")
    is_premium: bool = Field(default=False, description="Whether user has premium features")
    
    # Usage Statistics
    total_applications: int = Field(default=0, description="Total number of applications submitted")
    applications_this_month: int = Field(default=0, description="Applications submitted this month")
    successful_applications: int = Field(default=0, description="Applications that led to interviews")
    
    # Dates
    created_at: datetime = Field(default_factory=datetime.now, description="When user was created")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    last_application: Optional[datetime] = Field(None, description="Last application timestamp")
    
    # Settings
    settings: Dict[str, Any] = Field(default_factory=dict, description="User-specific settings")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def update_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.now()
        
    def record_application(self, successful: bool = False):
        """Record a new application"""
        self.total_applications += 1
        self.applications_this_month += 1
        self.last_application = datetime.now()
        
        if successful:
            self.successful_applications += 1
            
    def get_success_rate(self) -> float:
        """Calculate application success rate"""
        if self.total_applications == 0:
            return 0.0
        return (self.successful_applications / self.total_applications) * 100
        
    def can_apply_today(self) -> bool:
        """Check if user can apply today based on limits"""
        # This would need to be implemented with actual daily tracking
        # For now, return True
        return True
        
    def get_user_summary(self) -> Dict[str, Any]:
        """Get user summary statistics"""
        return {
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_premium": self.is_premium,
            "total_applications": self.total_applications,
            "applications_this_month": self.applications_this_month,
            "success_rate": self.get_success_rate(),
            "last_login": self.last_login,
            "last_application": self.last_application,
            "profile_summary": self.profile.get_profile_summary()
        } 