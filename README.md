# AutoApply - Automated Job Application System

AutoApply is a sophisticated, AI-powered system that automates the job application process by intelligently tailoring resumes to specific job postings and handling applications across multiple platforms.

## 🚀 Features

- **Multi-Agent Architecture**: Modular system with specialized agents for different tasks
- **Intelligent Resume Tailoring**: Multiple tailoring modes (conservative, moderate, aggressive)
- **Multi-Platform Support**: LinkedIn, Indeed, company websites, and email applications
- **LLM Integration**: Support for OpenAI and Anthropic models
- **Browser Automation**: Built on browser-use framework for reliable automation
- **Test Mode**: Review applications before submission
- **Comprehensive Tracking**: Full application history and analytics
- **Web Interface**: Modern web dashboard for system management
- **CLI Interface**: Command-line tools for advanced users

## 🏗️ Architecture

### Core Components

1. **Agent Framework**: Multi-agent system with specialized roles
   - Job Search Agent: Discovers and catalogs job postings
   - Analysis Agent: Extracts requirements from job descriptions
   - Resume Tailoring Agent: Customizes resumes for specific jobs
   - Application Agent: Handles form filling and submission
   - Coordinator Agent: Orchestrates the entire workflow

2. **Data Management**: Structured storage and tracking
   - Job Database: Stores job postings and requirements
   - Resume Management: Versions and tailoring history
   - Application Tracking: Complete submission history

3. **Platform Integration**: Modular platform adapters
   - LinkedIn Easy Apply
   - Indeed applications
   - Company website forms
   - Email applications

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key and/or Anthropic API key
- Chrome browser (for browser automation)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoApply
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the system**
   ```bash
   python main.py init
   ```

5. **Configure API keys**
   Edit the `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## 🚀 Quick Start

### 1. Initialize the System
```bash
python main.py init
```

### 2. Check System Status
```bash
python main.py status
```

### 3. Upload Your Resume
```bash
python main.py upload-resume path/to/your/resume.pdf
```

### 4. Start the Web Interface
```bash
python main.py web
```

### 5. Apply to a Job (Test Mode)
```bash
python main.py apply "https://linkedin.com/jobs/view/12345" --test-mode
```

## 🌐 Web Interface

The web interface provides a user-friendly dashboard for:
- Managing resumes and job applications
- Configuring system settings
- Monitoring application progress
- Reviewing tailored content before submission
- Viewing analytics and success metrics

Access the web interface at: `http://localhost:8000`

## ⚙️ Configuration

### Resume Tailoring Modes

- **Conservative**: Minor keyword optimization, preserves structure
- **Moderate**: Reorders sections, adjusts descriptions
- **Aggressive**: Significant restructuring for job alignment

### Model Selection

- **Analysis Tasks**: Claude (better reasoning)
- **Content Generation**: GPT-4 (better creativity)
- **Form Filling**: GPT-3.5 Turbo (cost-effective)

### Platform Settings

- **LinkedIn**: Easy Apply automation with rate limiting
- **Indeed**: Form parsing and completion
- **Company Websites**: Intelligent form detection
- **Email**: Automated application emails

## 📊 Data Models

### Job Model
- Basic information (title, company, location)
- Requirements and skills extraction
- Platform-specific metadata
- Analysis results and match scores

### Resume Model
- Structured sections with versioning
- Tailoring history and change tracking
- Multiple format support (PDF, DOCX, LaTeX)
- Skills and keyword extraction

### Application Model
- Complete submission tracking
- Status history and updates
- Form data and responses
- Error handling and retry logic

## 🔧 CLI Commands

```bash
# System management
python main.py init              # Initialize system
python main.py status            # Check system status
python main.py config            # View/modify configuration

# Resume management
python main.py upload-resume <file>  # Upload resume
python main.py list-resumes      # List all resumes

# Job applications
python main.py apply <url>       # Apply to specific job
python main.py search            # Search for jobs
python main.py list-jobs         # List discovered jobs

# Web interface
python main.py web               # Start web interface
```

## 🛡️ Security & Privacy

- **Local Storage**: All data remains on your machine
- **API Security**: Encrypted API key storage
- **Browser Isolation**: Separate browser contexts
- **Audit Trail**: Complete operation logging

## 📈 Analytics & Monitoring

- Application success rates
- Response time tracking
- Resume effectiveness metrics
- Platform-specific performance
- Error rate monitoring

## 🔄 Workflow

1. **Job Discovery**: Search or import job URLs
2. **Analysis**: Extract requirements and keywords
3. **Resume Tailoring**: Customize based on job requirements
4. **Review**: Preview changes in test mode
5. **Application**: Submit with platform-specific automation
6. **Tracking**: Monitor status and responses

## 🧪 Test Mode

Test mode allows you to:
- Review tailored resumes before submission
- Preview form data and cover letters
- Validate automation steps
- Ensure quality before going live

## 🌟 Advanced Features

- **Batch Processing**: Apply to multiple jobs
- **Smart Scheduling**: Optimal timing for applications
- **A/B Testing**: Compare different tailoring approaches
- **Integration APIs**: Connect with external systems
- **Custom Prompts**: Personalized LLM instructions

## 📝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: See the `/docs` directory
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Email**: support@autoapply.dev

## 🔮 Roadmap

### Phase 1: Foundation (Current)
- ✅ Multi-agent architecture
- ✅ Basic resume tailoring
- ✅ LinkedIn Easy Apply
- ✅ Web interface

### Phase 2: Enhancement
- [ ] Advanced tailoring modes
- [ ] Additional platforms
- [ ] Machine learning optimization
- [ ] Performance analytics

### Phase 3: Intelligence
- [ ] Outcome learning
- [ ] Predictive matching
- [ ] Advanced automation
- [ ] Enterprise features

## 📊 System Requirements

- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 1GB for application data
- **Network**: Stable internet connection
- **Browser**: Chrome 90+ (for automation)

---

**AutoApply** - Streamline your job search with AI-powered automation 🚀 