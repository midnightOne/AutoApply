from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List
import os

class Settings(BaseSettings):
    """Application Settings"""
    
    # LLM Configuration
    openai_api_key: Optional[str] = Field(default=None)
    anthropic_api_key: Optional[str] = Field(default=None)
    default_analysis_model: str = Field(default="claude-3-sonnet-20240229")
    default_generation_model: str = Field(default="gpt-4")
    default_form_filling_model: str = Field(default="gpt-3.5-turbo")
    llm_temperature: float = Field(default=0.7)
    llm_max_tokens: int = Field(default=4000)
    
    # Browser Configuration
    browser_path: Optional[str] = Field(default=None)
    browser_user_data: Optional[str] = Field(default=None)
    browser_headless: bool = Field(default=False)
    page_load_timeout: int = Field(default=30)
    element_timeout: int = Field(default=10)
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./autoapply.db")
    echo_sql: bool = Field(default=False)
    
    # Web Interface Configuration
    web_host: str = Field(default="127.0.0.1")
    web_port: int = Field(default=8000)
    web_debug: bool = Field(default=False)
    
    # Application Behavior
    test_mode: bool = Field(default=True)
    max_concurrent_applications: int = Field(default=3)
    application_delay_seconds: int = Field(default=30)
    linkedin_max_applications_per_day: int = Field(default=20)
    linkedin_delay_between_applications: int = Field(default=60)
    
    # Resume Settings
    resume_tailoring_mode: str = Field(default="conservative")
    resume_output_format: str = Field(default="pdf")
    
    # Logging Configuration
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="autoapply.log")
    log_rotation: bool = Field(default=True)
    max_log_size: str = Field(default="10MB")
    
    model_config = {"env_file": ".env", "extra": "ignore"}

# Global settings instance
settings = Settings()

# Validation functions
def validate_api_keys():
    """Validate that at least one LLM API key is configured"""
    if not settings.openai_api_key and not settings.anthropic_api_key:
        raise ValueError("At least one LLM API key must be configured")

def validate_resume_mode():
    """Validate resume tailoring mode"""
    valid_modes = ["conservative", "moderate", "aggressive"]
    if settings.resume_tailoring_mode not in valid_modes:
        raise ValueError(f"Invalid tailoring mode: {settings.resume_tailoring_mode}")

def validate_settings():
    """Validate all settings"""
    validate_api_keys()
    validate_resume_mode()
    
    # Create necessary directories
    os.makedirs("data/resumes", exist_ok=True)
    os.makedirs("data/jobs", exist_ok=True)
    os.makedirs("data/applications", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

# Auto-validate on import
try:
    validate_settings()
except Exception as e:
    print(f"Warning: Settings validation failed: {e}")
    print("Please check your configuration and API keys.") 