#!/usr/bin/env python
import sys
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


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        ResumeEnhancer().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResumeEnhancer().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}

    try:
        ResumeEnhancer().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
