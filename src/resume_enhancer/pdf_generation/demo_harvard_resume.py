#!/usr/bin/env python3
"""
Demo script showing how to use the Harvard-style resume PDF generator.

This script demonstrates:
1. How to load JSON resume data
2. How to generate a PDF resume using the Harvard template
3. How to handle both file output and buffer output
4. Example usage with sample data
"""

import json
import os
import sys
from pathlib import Path

# Add the src directory to the path to import our module
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from .resume_pdf import create_resume_pdf


def load_resume_from_json(json_file_path):
    """
    Load resume data from a JSON file.

    Args:
        json_file_path (str): Path to the JSON file containing resume data

    Returns:
        dict: Resume data dictionary
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find JSON file at {json_file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return None


def demo_with_json_file():
    """
    Demo using actual JSON file from agents-api output.
    """
    print("=== Demo: Loading Resume from JSON File ===")

    # Try to find the JSON file
    json_paths = [
        "../agents-api/output/json.json",
        "agents-api/output/json.json",
        "json.json",
    ]

    resume_data = None
    json_file_path = None

    for path in json_paths:
        if os.path.exists(path):
            json_file_path = path
            resume_data = load_resume_from_json(path)
            break

    if resume_data:
        print(f"✓ Successfully loaded resume data from: {json_file_path}")

        # Extract name for filename
        personal_info = resume_data.get("personal_information", "")
        name = personal_info.split("|")[0].strip() if personal_info else "resume"
        filename = (
            f"{name.lower().replace(' ', '_').replace('"', '')}_harvard_resume.pdf"
        )

        # Generate PDF
        create_resume_pdf(resume_data, filename)
        print(f"✓ Harvard-style resume generated: {filename}")

        return True
    else:
        print("✗ Could not load resume data from JSON file")
        return False


def demo_with_sample_data():
    """
    Demo using sample data structure.
    """
    print("\n=== Demo: Using Sample Resume Data ===")

    sample_resume_data = {
        "personal_information": "John Smith | 123 Harvard Ave, Cambridge, MA 02138 | (617) 555-0123 | john.smith@email.com",
        "about": "Motivated computer science student with strong analytical skills and experience in software development. Passionate about creating innovative solutions and contributing to meaningful projects.",
        "education": [
            "Harvard University - Cambridge, MA - B.S. in Computer Science (Expected May 2025)",
            "Relevant Coursework: Data Structures, Algorithms, Database Systems, Machine Learning, Software Engineering",
        ],
        "experiences": [
            {
                "name": "Software Engineering Intern",
                "position": "Tech Innovations Inc.",
                "start_date": "June 2024",
                "end_date": "August 2024",
                "descriptions": [
                    "Developed and maintained web applications using React and Node.js",
                    "Collaborated with cross-functional teams to implement new features",
                    "Improved application performance by 25% through code optimization",
                ],
            },
            {
                "name": "Research Assistant",
                "position": "Harvard Computer Science Department",
                "start_date": "September 2023",
                "end_date": "Present",
                "descriptions": [
                    "Conducted research on machine learning algorithms for natural language processing",
                    "Published findings in undergraduate research symposium",
                    "Mentored junior students in research methodologies",
                ],
            },
        ],
        "skills": [
            "Programming: Python, Java, JavaScript, C++",
            "Technologies: React, Node.js, Docker, Git",
            "Databases: MySQL, MongoDB, PostgreSQL",
            "Cloud Platforms: AWS, Google Cloud Platform",
        ],
        "projects": [
            "Personal Finance Tracker - Built a web application for expense tracking using React and Express.js",
            "Machine Learning Classifier - Developed a sentiment analysis model using Python and scikit-learn",
        ],
        "certifications": [
            "AWS Certified Cloud Practitioner (2024)",
            "Google Cloud Associate Cloud Engineer (2023)",
        ],
        "achievements": [
            "Dean's List for Academic Excellence (Fall 2023, Spring 2024)",
            "Harvard Computer Science Department Outstanding Student Award (2024)",
            "Winner of Harvard Hackathon 2024 - Best Technical Implementation",
        ],
        "languages": ["English (native)", "Spanish (conversational)", "French (basic)"],
        "interests": [
            "Open source software development",
            "Artificial intelligence and machine learning",
            "Rock climbing and outdoor activities",
        ],
    }

    # Generate PDF
    filename = "john_smith_sample_harvard_resume.pdf"
    create_resume_pdf(sample_resume_data, filename)
    print(f"✓ Sample Harvard-style resume generated: {filename}")

    # Demo buffer generation
    pdf_buffer = create_resume_pdf(sample_resume_data, output_buffer=True)
    buffer_size = len(pdf_buffer.getvalue()) if pdf_buffer else 0
    print(f"✓ PDF buffer generated with {buffer_size} bytes")


def demo_buffer_usage():
    """
    Demo showing how to use the PDF buffer for web applications or email attachments.
    """
    print("\n=== Demo: PDF Buffer Usage ===")

    simple_data = {
        "personal_information": "Jane Doe | 456 College St, Boston, MA 02115 | (617) 555-0456 | jane.doe@email.com",
        "about": "Recent graduate seeking opportunities in software development.",
        "education": [
            "Boston University - Boston, MA - B.A. in Computer Science (2024)"
        ],
        "skills": ["Python", "JavaScript", "SQL"],
        "experiences": [],
    }

    # Generate PDF as buffer
    pdf_buffer = create_resume_pdf(simple_data, output_buffer=True)

    if pdf_buffer:
        buffer_size = len(pdf_buffer.getvalue())
        print(f"✓ Generated PDF buffer: {buffer_size} bytes")

        # Example: Save buffer to file (simulating web download)
        with open("jane_doe_from_buffer.pdf", "wb") as f:
            f.write(pdf_buffer.getvalue())
        print("✓ Buffer saved to file: jane_doe_from_buffer.pdf")

        # Example: Get buffer for email attachment (would pass to email library)
        pdf_buffer.seek(0)  # Reset position
        attachment_data = pdf_buffer.read()
        print(f"✓ Buffer ready for email attachment: {len(attachment_data)} bytes")


def main():
    """
    Main demo function showcasing all features.
    """
    print("🎓 Harvard-Style Resume PDF Generator Demo")
    print("=" * 50)

    # Try to load from actual JSON file first
    if not demo_with_json_file():
        print("Falling back to sample data demonstration...")

    # Show sample data demo
    demo_with_sample_data()

    # Show buffer usage demo
    demo_buffer_usage()

    print("\n" + "=" * 50)
    print("✓ Demo completed successfully!")
    print("\nGenerated files:")

    # List generated PDF files
    pdf_files = list(Path(".").glob("*.pdf"))
    for pdf_file in pdf_files:
        file_size = pdf_file.stat().st_size
        print(f"  - {pdf_file.name} ({file_size} bytes)")

    print(f"\n📝 Total PDFs generated: {len(pdf_files)}")


if __name__ == "__main__":
    main()
