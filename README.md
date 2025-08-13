# Resume Enhancer

An AI-powered resume enhancement tool using CrewAI multi-agent system to analyze, improve, and optimize resumes with intelligent feedback and suggestions.

## Overview

Resume Enhancer leverages a multi-agent AI system to provide comprehensive resume analysis and enhancement. The system uses specialized AI agents that work together to analyze your resume, provide feedback using the STAR methodology, and generate an improved version with actionable insights.

## Features

- **Multi-Agent AI System**: Uses CrewAI framework with specialized agents for different tasks
- **STAR Methodology**: Applies Situation, Task, Action, Result framework for better experience descriptions
- **Comprehensive Analysis**: Provides detailed feedback on resume structure, content, and presentation
- **JSON Output**: Generates structured data for easy integration with other tools
- **PDF Generation**: Supports PDF resume processing
- **Feedback Categories**: Categorized feedback (work, personal, skills, metrics, etc.)

## Architecture

The system consists of three main AI agents:

1. **Resume Analyzer**: Expert recruiter that evaluates resumes and identifies improvement areas
2. **Resume Writer**: Skilled writer that rewrites and enhances resume content
3. **JSON Builder**: Developer that structures the enhanced resume data into JSON format

The agents work together through a sequential task pipeline:

1. **Analysis**: Resume Analyzer conducts thorough analysis using STAR methodology, identifies improvement areas, and suggests enhancements
2. **Enhancement**: Resume Writer rewrites the resume based on analysis findings, applies STAR descriptions, and structures content properly
3. **Gather Feedback**: JSON Builder extracts and categorizes feedback from the analysis (positive/negative with proper categories)
4. **Build JSON**: JSON Builder creates structured JSON output combining enhanced resume data with feedback

## Installation

### Prerequisites

- Python 3.10 - 3.13
- UV package manager

### Setup

1. Clone the repository:

```bash
git clone https://github.com/guti1690/resume-enhancer-agent.git
cd resume-enhancer-agent
```

2. Install dependencies using UV:

```bash
uv sync
```

3. Set up your environment variables:

```bash
touch .env
# Edit .env with your API keys
```

### Required API Keys

You'll need to configure API keys for the LLM providers used:

- OpenRouter API key for OpenAI GPT models

### Installation on another project

```bash
uv add "resume_enhancer_agent @ git+https://github.com/guti1690/resume-enhancer-agent"
```

### Programmatic Usage

```python
from resume_enhancer import enhance_resume

# Load your resume
resume_content = "your resume content here"

# Enhance the resume
enhanced_resume = enhance_resume(resume_content)
print(enhanced_resume)
```

## Configuration

### Personal Information

Update your personal information in:

- `src/resume_enhancer/me/summary.txt` - Your personal summary
- `src/resume_enhancer/me/resume.pdf` - Your current resume
- `knowledge/user_preference.txt` - Your preferences and details

## Usage

To run the application using the "me" information:

```bash
crewai run
```

### Agent Configuration

Agents are configured in `src/resume_enhancer/config/agents.yaml`:

- Customize agent roles, goals, and backstories
- Modify LLM providers and models
- Adjust retry limits and other parameters

### Task Configuration

Tasks are defined in `src/resume_enhancer/config/tasks.yaml`:

- Modify task descriptions and expected outputs
- Adjust context dependencies between tasks
- Customize output file locations

## Output

The system generates several output files in the `output/` directory:

- `analysis.md` - Detailed resume analysis with improvement suggestions
- `resume.md` - Enhanced resume with STAR methodology applied
- `feedback.json` - Structured feedback data
- `json.json` - Complete resume data in JSON format

## Data Models

### Resume Structure

```python
class Resume(BaseModel):
    personal_information: PersonalInformation
    skills: List[str]
    languages: List[str]
    interests: List[str]
    about: str
    experiences: List[CompanyExperience]
    education: List[str]
    certifications: List[str]
    projects: List[str]
    achievements: List[str]
    additional_notes: str
    feedback: List[Feedback]
```

### Feedback Structure

```python
class Feedback(BaseModel):
    is_positive: bool
    category: str  # work, personal, skills, metrics, STAR, etc.
    description: str
```

## Development

### Project Structure

```
resume_enhancer/
├── src/resume_enhancer/
│   ├── config/           # Agent and task configurations
│   ├── me/              # Personal resume data
│   ├── pdf_generation/  # PDF processing tools
│   ├── tools/           # Custom tools for agents
│   ├── crew.py          # CrewAI setup and agents
│   ├── main.py          # CLI entry points
│   └── util.py          # Utility functions
├── knowledge/           # User preferences and context
├── output/             # Generated reports and data
├── tests/              # Test files
└── pyproject.toml      # Project configuration
```

## Requirements

- Python 3.10+
- CrewAI framework with tools
- FPDF2 for PDF generation
- LLM API access (OpenRouter, DeepSeek)

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for details.

---

**Note**: This tool uses AI agents to analyze and enhance resumes. Always review the generated content for accuracy and relevance to your specific situation before using it in actual job applications.
