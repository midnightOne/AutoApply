#!/usr/bin/env python3
"""
AutoApply - Automated Job Application System

Main entry point for the application.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from autoapply.models import Job, Resume, Application
from config.settings import settings, validate_settings

# Initialize Rich console
console = Console()

# Create Typer app
app = typer.Typer(
    name="autoapply",
    help="AutoApply - Automated Job Application System",
    add_completion=False
)

def print_banner():
    """Print the application banner"""
    banner = Text.from_markup("""
[bold blue]AutoApply[/bold blue] - Automated Job Application System
[dim]Streamline your job search with AI-powered automation[/dim]
""")
    console.print(Panel(banner, style="blue"))

@app.command()
def init():
    """Initialize the AutoApply system"""
    print_banner()
    
    console.print("[bold green]Initializing AutoApply system...[/bold green]")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        console.print("[yellow]No .env file found. Creating template...[/yellow]")
        create_env_template()
    
    # Validate settings
    try:
        validate_settings()
        console.print("[green]✓ Settings validated successfully[/green]")
    except Exception as e:
        console.print(f"[red]✗ Settings validation failed: {e}[/red]")
        console.print("[yellow]Please check your .env file and API keys[/yellow]")
        return
    
    # Create directories
    console.print("[blue]Creating directories...[/blue]")
    os.makedirs("data/resumes", exist_ok=True)
    os.makedirs("data/jobs", exist_ok=True)
    os.makedirs("data/applications", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    console.print("[green]✓ AutoApply system initialized successfully![/green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("1. Configure your API keys in the .env file")
    console.print("2. Upload your resume: [code]python main.py upload-resume[/code]")
    console.print("3. Start the web interface: [code]python main.py web[/code]")

@app.command()
def web(
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    debug: bool = typer.Option(False, help="Enable debug mode")
):
    """Start the web interface"""
    print_banner()
    
    console.print(f"[bold blue]Starting web interface on {host}:{port}[/bold blue]")
    
    try:
        import uvicorn
        from src.autoapply.web.main import app as web_app
        
        uvicorn.run(
            web_app,
            host=host,
            port=port,
            log_level="debug" if debug else "info"
        )
    except ImportError:
        console.print("[red]Error: Web dependencies not installed[/red]")
        console.print("Please install with: pip install -r requirements.txt")
    except Exception as e:
        console.print(f"[red]Error starting web interface: {e}[/red]")

@app.command()
def status():
    """Show system status"""
    print_banner()
    
    # Create status table
    table = Table(title="System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="dim")
    
    # Check settings
    try:
        validate_settings()
        table.add_row("Settings", "✓ Valid", "Configuration loaded successfully")
    except Exception as e:
        table.add_row("Settings", "✗ Invalid", str(e))
    
    # Check directories
    dirs_ok = all(os.path.exists(d) for d in ["data/resumes", "data/jobs", "data/applications", "logs"])
    table.add_row("Directories", "✓ Present" if dirs_ok else "✗ Missing", "All required directories exist")
    
    # Check API keys
    api_keys_ok = bool(settings.openai_api_key or settings.anthropic_api_key)
    table.add_row("API Keys", "✓ Configured" if api_keys_ok else "✗ Missing", "LLM API keys available")
    
    console.print(table)

@app.command()
def upload_resume(
    file_path: str = typer.Argument(..., help="Path to resume file"),
    name: str = typer.Option(None, help="Name for the resume"),
    set_default: bool = typer.Option(False, help="Set as default resume")
):
    """Upload a resume file"""
    print_banner()
    
    console.print(f"[blue]Uploading resume: {file_path}[/blue]")
    
    if not os.path.exists(file_path):
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        return
    
    # TODO: Implement resume upload logic
    console.print("[yellow]Resume upload functionality will be implemented in the next phase[/yellow]")
    console.print(f"[green]Resume would be uploaded from: {file_path}[/green]")

@app.command()
def apply(
    job_url: str = typer.Argument(..., help="Job posting URL"),
    test_mode: bool = typer.Option(True, help="Run in test mode (no actual application)")
):
    """Apply to a specific job"""
    print_banner()
    
    console.print(f"[blue]Processing job application for: {job_url}[/blue]")
    
    if test_mode:
        console.print("[yellow]Running in TEST MODE - no actual application will be submitted[/yellow]")
    
    # TODO: Implement job application logic
    console.print("[yellow]Job application functionality will be implemented in the next phase[/yellow]")

@app.command()
def search(
    keywords: str = typer.Option(None, help="Job search keywords"),
    location: str = typer.Option(None, help="Job location"),
    platform: str = typer.Option("linkedin", help="Platform to search on")
):
    """Search for jobs"""
    print_banner()
    
    console.print(f"[blue]Searching for jobs on {platform}[/blue]")
    
    if keywords:
        console.print(f"Keywords: {keywords}")
    if location:
        console.print(f"Location: {location}")
    
    # TODO: Implement job search logic
    console.print("[yellow]Job search functionality will be implemented in the next phase[/yellow]")

@app.command()
def config(
    key: str = typer.Option(None, help="Configuration key to view/set"),
    value: str = typer.Option(None, help="New value for the configuration key")
):
    """View or modify configuration"""
    print_banner()
    
    if key and value:
        console.print(f"[blue]Setting {key} = {value}[/blue]")
        # TODO: Implement config modification
        console.print("[yellow]Configuration modification will be implemented in the next phase[/yellow]")
    elif key:
        console.print(f"[blue]Getting value for {key}[/blue]")
        # TODO: Implement config viewing
        console.print("[yellow]Configuration viewing will be implemented in the next phase[/yellow]")
    else:
        console.print("[blue]Current configuration:[/blue]")
        console.print(f"Test Mode: {settings.test_mode}")
        console.print(f"Max Applications/Day: {settings.max_concurrent_applications}")
        console.print(f"Resume Tailoring Mode: {settings.resume_tailoring_mode}")

def create_env_template():
    """Create .env template file"""
    template_content = """# LLM API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Model Configuration
DEFAULT_ANALYSIS_MODEL=claude-3-sonnet-20240229
DEFAULT_GENERATION_MODEL=gpt-4
DEFAULT_FORM_FILLING_MODEL=gpt-3.5-turbo

# Browser Configuration
BROWSER_PATH=
BROWSER_USER_DATA=
BROWSER_HEADLESS=false

# Database
DATABASE_URL=sqlite:///./autoapply.db

# Web Interface
WEB_HOST=127.0.0.1
WEB_PORT=8000

# Application Settings
TEST_MODE=true
MAX_CONCURRENT_APPLICATIONS=3
APPLICATION_DELAY_SECONDS=30

# Platform Settings
LINKEDIN_MAX_APPLICATIONS_PER_DAY=20
LINKEDIN_DELAY_BETWEEN_APPLICATIONS=60

# Resume Settings
RESUME_TAILORING_MODE=conservative
RESUME_OUTPUT_FORMAT=pdf

# Logging
LOG_LEVEL=INFO
LOG_FILE=autoapply.log
"""
    
    with open(".env", "w") as f:
        f.write(template_content)
    
    console.print("[green]✓ .env template created[/green]")
    console.print("[yellow]Please edit .env file with your API keys and preferences[/yellow]")

if __name__ == "__main__":
    app() 