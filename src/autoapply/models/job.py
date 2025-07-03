from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    """Job posting status"""
    DISCOVERED = "discovered"
    ANALYZED = "analyzed"
    APPLIED = "applied"
    REJECTED = "rejected"
    EXPIRED = "expired"

class JobRequirement(BaseModel):
    """Individual job requirement"""
    category: str = Field(..., description="Category of requirement (e.g., 'technical', 'experience', 'education')")
    skill: str = Field(..., description="Specific skill or requirement")
    importance: str = Field(..., description="Importance level: 'required', 'preferred', 'nice-to-have'")
    years_experience: Optional[int] = Field(None, description="Years of experience required")
    
class Job(BaseModel):
    """Job posting data model"""
    
    # Basic Information
    id: Optional[str] = Field(None, description="Unique job identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    url: HttpUrl = Field(..., description="Job posting URL")
    
    # Job Details
    description: str = Field(..., description="Full job description")
    requirements: List[JobRequirement] = Field(default_factory=list, description="Extracted job requirements")
    salary_range: Optional[str] = Field(None, description="Salary range if available")
    employment_type: Optional[str] = Field(None, description="Employment type (full-time, part-time, contract)")
    experience_level: Optional[str] = Field(None, description="Experience level (entry, mid, senior)")
    
    # Platform Information
    platform: str = Field(..., description="Platform where job was found (linkedin, indeed, etc.)")
    platform_id: Optional[str] = Field(None, description="Platform-specific job ID")
    easy_apply: bool = Field(False, description="Whether job supports easy apply")
    
    # Analysis Results
    key_skills: List[str] = Field(default_factory=list, description="Key skills extracted from posting")
    keywords: List[str] = Field(default_factory=list, description="Important keywords for resume tailoring")
    match_score: Optional[float] = Field(None, description="Compatibility score with user profile")
    
    # Metadata
    status: JobStatus = Field(default=JobStatus.DISCOVERED, description="Current job status")
    discovered_at: datetime = Field(default_factory=datetime.now, description="When job was discovered")
    analyzed_at: Optional[datetime] = Field(None, description="When job was analyzed")
    applied_at: Optional[datetime] = Field(None, description="When application was submitted")
    
    # Additional data
    company_info: Optional[Dict[str, Any]] = Field(None, description="Additional company information")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def add_requirement(self, category: str, skill: str, importance: str, years_experience: Optional[int] = None):
        """Add a requirement to the job"""
        requirement = JobRequirement(
            category=category,
            skill=skill,
            importance=importance,
            years_experience=years_experience
        )
        self.requirements.append(requirement)
        
    def get_required_skills(self) -> List[str]:
        """Get all required skills"""
        return [req.skill for req in self.requirements if req.importance == "required"]
        
    def get_preferred_skills(self) -> List[str]:
        """Get all preferred skills"""
        return [req.skill for req in self.requirements if req.importance == "preferred"]
        
    def update_analysis(self, key_skills: List[str], keywords: List[str], match_score: float):
        """Update job analysis results"""
        self.key_skills = key_skills
        self.keywords = keywords
        self.match_score = match_score
        self.analyzed_at = datetime.now()
        self.status = JobStatus.ANALYZED
        
    def mark_applied(self):
        """Mark job as applied"""
        self.applied_at = datetime.now()
        self.status = JobStatus.APPLIED 