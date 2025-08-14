#!/usr/bin/env python
import warnings
from datetime import datetime

from resume_enhancer.crew import ResumeEnhancer
from resume_enhancer.util import extract_me_resume, extract_resume

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

resume = extract_me_resume()


def enhance_resume(resume):
    """
    Run the crew with the given resume.
    """
    if not resume:
        raise ValueError("Resume is required")

    resume_info = extract_resume(resume)

    inputs = {"resume": resume_info, "today": str(datetime.now())}

    try:
        result = ResumeEnhancer().crew().kickoff(inputs=inputs)
        return result.raw
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def run():
    """
    Run the crew.
    """
    inputs = {"resume": resume, "today": str(datetime.now())}

    try:
        result = ResumeEnhancer().crew().kickoff(inputs=inputs)
        return result.raw
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
