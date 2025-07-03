from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ResumeTailoringMode(str, Enum):
    """Resume tailoring intensity levels"""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

class ResumeSection(BaseModel):
    """Individual resume section"""
    id: Optional[str] = Field(None, description="Unique section identifier")
    title: str = Field(..., description="Section title (e.g., 'Experience', 'Education')")
    content: str = Field(..., description="Section content")
    order: int = Field(..., description="Display order")
    keywords: List[str] = Field(default_factory=list, description="Keywords in this section")
    
    # Tailoring metadata
    original_content: Optional[str] = Field(None, description="Original content before tailoring")
    tailored_for_job: Optional[str] = Field(None, description="Job ID this section was tailored for")
    tailoring_changes: List[str] = Field(default_factory=list, description="Log of changes made")
    
class Resume(BaseModel):
    """Resume data model"""
    
    # Basic Information
    id: Optional[str] = Field(None, description="Unique resume identifier")
    title: str = Field(..., description="Resume title/version")
    owner_name: str = Field(..., description="Resume owner's name")
    
    # Contact Information
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Current location")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    portfolio_url: Optional[str] = Field(None, description="Portfolio website URL")
    
    # Resume Content
    sections: List[ResumeSection] = Field(default_factory=list, description="Resume sections")
    
    # Skills and Keywords
    skills: List[str] = Field(default_factory=list, description="All skills mentioned in resume")
    keywords: List[str] = Field(default_factory=list, description="Important keywords")
    
    # Tailoring Information
    is_tailored: bool = Field(False, description="Whether this resume has been tailored")
    tailored_for_job: Optional[str] = Field(None, description="Job ID this resume was tailored for")
    tailoring_mode: Optional[ResumeTailoringMode] = Field(None, description="Tailoring mode used")
    original_resume_id: Optional[str] = Field(None, description="Original resume ID if this is tailored")
    
    # File Information
    file_format: str = Field(default="pdf", description="File format (pdf, docx, latex)")
    file_path: Optional[str] = Field(None, description="Path to resume file")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="When resume was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="When resume was last updated")
    version: int = Field(default=1, description="Resume version number")
    
    # Additional context
    context_notes: Optional[str] = Field(None, description="Additional context about work experience")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def add_section(self, title: str, content: str, order: int = None) -> ResumeSection:
        """Add a new section to the resume"""
        if order is None:
            order = len(self.sections) + 1
            
        section = ResumeSection(
            title=title,
            content=content,
            order=order
        )
        self.sections.append(section)
        self.updated_at = datetime.now()
        return section
        
    def get_section(self, title: str) -> Optional[ResumeSection]:
        """Get a section by title"""
        for section in self.sections:
            if section.title.lower() == title.lower():
                return section
        return None
        
    def update_section(self, title: str, content: str) -> bool:
        """Update a section's content"""
        section = self.get_section(title)
        if section:
            section.content = content
            self.updated_at = datetime.now()
            return True
        return False
        
    def remove_section(self, title: str) -> bool:
        """Remove a section by title"""
        for i, section in enumerate(self.sections):
            if section.title.lower() == title.lower():
                del self.sections[i]
                self.updated_at = datetime.now()
                return True
        return False
        
    def reorder_sections(self, new_order: List[str]) -> bool:
        """Reorder sections based on title list"""
        if len(new_order) != len(self.sections):
            return False
            
        section_map = {section.title: section for section in self.sections}
        reordered_sections = []
        
        for i, title in enumerate(new_order):
            if title in section_map:
                section = section_map[title]
                section.order = i + 1
                reordered_sections.append(section)
            else:
                return False
                
        self.sections = reordered_sections
        self.updated_at = datetime.now()
        return True
        
    def extract_skills(self) -> List[str]:
        """Extract all skills mentioned in the resume"""
        skills = set()
        for section in self.sections:
            skills.update(section.keywords)
        self.skills = list(skills)
        return self.skills
        
    def create_tailored_copy(self, job_id: str, tailoring_mode: ResumeTailoringMode) -> 'Resume':
        """Create a tailored copy of this resume"""
        tailored_resume = Resume(
            title=f"{self.title} - Tailored for {job_id}",
            owner_name=self.owner_name,
            email=self.email,
            phone=self.phone,
            location=self.location,
            linkedin_url=self.linkedin_url,
            portfolio_url=self.portfolio_url,
            sections=[section.copy() for section in self.sections],
            skills=self.skills.copy(),
            keywords=self.keywords.copy(),
            is_tailored=True,
            tailored_for_job=job_id,
            tailoring_mode=tailoring_mode,
            original_resume_id=self.id,
            file_format=self.file_format,
            context_notes=self.context_notes,
            metadata=self.metadata.copy()
        )
        
        # Store original content for tracking changes
        for section in tailored_resume.sections:
            section.original_content = section.content
            section.tailored_for_job = job_id
            
        return tailored_resume
        
    def get_tailoring_summary(self) -> Dict[str, Any]:
        """Get summary of tailoring changes"""
        if not self.is_tailored:
            return {}
            
        summary = {
            "tailored_for_job": self.tailored_for_job,
            "tailoring_mode": self.tailoring_mode,
            "changes_by_section": {},
            "total_changes": 0
        }
        
        for section in self.sections:
            if section.tailoring_changes:
                summary["changes_by_section"][section.title] = len(section.tailoring_changes)
                summary["total_changes"] += len(section.tailoring_changes)
                
        return summary 