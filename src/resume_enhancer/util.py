import os

from pypdf import PdfReader

# Get the directory where this util.py file is located
current_dir = os.path.dirname(os.path.abspath(__file__))


# For testing
def extract_me_resume():
    resume_path = os.path.join(current_dir, "me", "resume.pdf")
    return extract_resume(resume_path)


def extract_resume(resume):
    reader = PdfReader(resume)
    resume = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume += text

    return resume
