from pypdf import PdfReader
import os

# Get the directory where this util.py file is located
current_dir = os.path.dirname(os.path.abspath(__file__))


def extract_resume():
    resume_path = os.path.join(current_dir, "me", "resume.pdf")
    reader = PdfReader(resume_path)
    resume = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume += text

    return resume
