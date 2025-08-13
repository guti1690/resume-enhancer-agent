# Harvard-Style Resume PDF Generator

A professional Python library for generating Harvard-style resumes from JSON data using the fpdf2 library.

## Features

### 🎓 Harvard-Inspired Formatting

- Clean, professional layout following Harvard Career Services guidelines
- Proper font hierarchy (16pt name, 12pt section headers, 11pt body text)
- Section headers with underlines
- Consistent spacing and margins
- Professional bullet point formatting

### 📄 Comprehensive Resume Sections

- **Header**: Name and contact information (address, phone, email)
- **Summary**: Professional summary/about section
- **Education**: University, degree, location, dates, and relevant coursework
- **Experience**: Job titles, companies, dates, and achievement-focused bullet points
- **Skills**: Technical and soft skills with clean formatting
- **Certifications**: Professional certifications and licenses
- **Projects**: Academic and personal projects
- **Achievements**: Quantified accomplishments and awards
- **Languages**: Language proficiencies
- **Interests**: Professional and personal interests

### 🔧 Technical Features

- **Unicode Support**: Handles special characters and converts them to PDF-compatible ASCII
- **Flexible Output**: Generate PDF files or in-memory buffers for web applications
- **JSON Input**: Easy integration with existing data systems
- **Error Handling**: Robust parsing and validation of input data
- **Customizable**: Easy to modify fonts, spacing, and layout

## Installation

```bash
# Using uv (recommended)
uv add fpdf2

# Using pip
pip install fpdf2
```

## Quick Start

### Basic Usage with JSON Data

```python
from resume_enhancer.ResumePDF import create_resume_pdf
import json

# Load resume data from JSON
with open('resume_data.json', 'r') as f:
    resume_data = json.load(f)

# Generate PDF file
create_resume_pdf(resume_data, 'my_resume.pdf')

# Generate PDF buffer (for web apps)
pdf_buffer = create_resume_pdf(resume_data, output_buffer=True)
```

### Expected JSON Structure

```json
{
  "personal_information": "Jane Smith | 123 Main St, Boston, MA 02101 | (617) 555-0123 | jane.smith@email.com",
  "about": "Professional summary highlighting key qualifications...",
  "education": [
    "Harvard University – Cambridge, MA – B.A. in Computer Science (Expected 2025)",
    "Relevant Coursework: Data Structures, Algorithms, Machine Learning"
  ],
  "experiences": [
    {
      "name": "Software Engineer Intern",
      "position": "Tech Company Inc.",
      "start_date": "June 2024",
      "end_date": "August 2024",
      "descriptions": [
        "Developed web applications using React and Node.js",
        "Improved system performance by 25%"
      ]
    }
  ],
  "skills": [
    "Programming: Python, JavaScript, Java",
    "Technologies: React, Docker, AWS"
  ],
  "certifications": ["AWS Certified Developer (2024)"],
  "projects": ["Personal Finance App – Built using React and Express.js"],
  "achievements": ["Dean's List for Academic Excellence (2023-2024)"],
  "languages": ["English (native)", "Spanish (fluent)"],
  "interests": ["Machine learning research", "Open source contributions"]
}
```

## Advanced Usage

### Custom Formatting

```python
from resume_enhancer.ResumePDF import PDF, create_resume_pdf

# Create custom PDF with different margins
def create_custom_resume(resume_data):
    pdf = PDF()
    pdf.set_left_margin(25)  # Wider left margin
    pdf.set_right_margin(25)  # Wider right margin
    # ... custom formatting logic
    return pdf
```

### Web Application Integration

```python
from flask import Flask, send_file
from resume_enhancer.ResumePDF import create_resume_pdf

app = Flask(__name__)

@app.route('/generate_resume')
def generate_resume():
    # Load resume data from database or form
    resume_data = get_user_resume_data()

    # Generate PDF buffer
    pdf_buffer = create_resume_pdf(resume_data, output_buffer=True)

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='resume.pdf'
    )
```

### Email Integration

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def email_resume(resume_data, recipient_email):
    # Generate PDF buffer
    pdf_buffer = create_resume_pdf(resume_data, output_buffer=True)

    # Create email with PDF attachment
    msg = MIMEMultipart()
    msg['To'] = recipient_email
    msg['Subject'] = 'My Resume'

    # Attach PDF
    pdf_attachment = MIMEApplication(pdf_buffer.getvalue(), _subtype='pdf')
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename='resume.pdf')
    msg.attach(pdf_attachment)

    # Send email...
```

## Key Improvements Over Original

### 1. Harvard-Style Formatting

- Professional section headers with underlines
- Proper font hierarchy and spacing
- Clean, academic-style layout
- Consistent bullet point formatting

### 2. Enhanced Unicode Support

- Automatic conversion of special characters (smart quotes, em dashes, etc.)
- Support for international characters
- Robust text normalization

### 3. Better Data Handling

- Flexible JSON structure parsing
- Graceful handling of missing fields
- Improved personal information parsing

### 4. Professional Experience Section

- Company and job title formatting
- Right-aligned dates
- Achievement-focused bullet points
- Proper indentation and spacing

### 5. Comprehensive Sections

- All standard resume sections supported
- Flexible ordering and content
- Professional presentation of all data types

## File Structure

```
resume_enhancer/
├── src/
│   └── resume_enhancer/
│       └── ResumePDF.py          # Main PDF generation module
├── test_resume_generation.py     # Test script for JSON data
├── demo_harvard_resume.py        # Comprehensive demo script
└── README.md                     # This documentation
```

## Demo Scripts

### Basic Test

```bash
uv run python test_resume_generation.py
```

### Full Demo

```bash
uv run python demo_harvard_resume.py
```

The demo script showcases:

- Loading data from JSON files
- Generating PDFs with sample data
- Buffer usage for web applications
- Multiple output formats

## API Reference

### `create_resume_pdf(resume_data, output_filename="resume.pdf", output_buffer=False)`

**Parameters:**

- `resume_data` (dict): Resume data dictionary matching expected JSON structure
- `output_filename` (str): Name of output PDF file (ignored if output_buffer=True)
- `output_buffer` (bool): If True, returns BytesIO buffer instead of saving file

**Returns:**

- `None` if saving to file
- `io.BytesIO` buffer if output_buffer=True

### Helper Functions

- `parse_personal_info(info_string)`: Parse pipe-separated contact information
- `normalize_text(text)`: Convert Unicode characters to PDF-compatible ASCII
- `add_header(pdf, personal_info)`: Add formatted header section
- `add_section_title(pdf, title)`: Add section title with Harvard formatting
- `add_experience_section(pdf, experiences)`: Add professional experience section

## Best Practices

### Data Preparation

1. Use consistent date formats (e.g., "June 2024", "Present")
2. Include quantified achievements in experience descriptions
3. Keep bullet points concise and action-oriented
4. Use parallel structure in lists

### Content Guidelines

1. Start experience bullets with action verbs
2. Include metrics and results where possible
3. Tailor content to target audience
4. Keep personal information current and professional

### Technical Considerations

1. Test with various Unicode characters
2. Validate JSON structure before processing
3. Handle missing or empty fields gracefully
4. Consider PDF file size for web applications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

**Unicode Encoding Errors:**

- The library automatically converts Unicode characters to ASCII
- If you encounter encoding issues, check the `normalize_text()` function

**Missing Sections:**

- Empty or missing data fields are handled gracefully
- Check your JSON structure matches the expected format

**PDF Generation Fails:**

- Ensure all required dependencies are installed
- Check file permissions for output directory

### Support

For issues and questions, please check the demo scripts and documentation first. The comprehensive examples should cover most use cases.
