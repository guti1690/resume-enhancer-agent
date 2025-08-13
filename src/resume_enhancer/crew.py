from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field

MAX_RETRY_LIMIT = 3


class Feedback(BaseModel):
    is_positive: bool = Field(description="Is the feedback positive?")
    category: str = Field(
        description="Type of feedback. e.g. work, personal, skills, metrics, STAR, etc"
    )
    description: str = Field(description="Description of type of feedback")


class FeedbackList(BaseModel):
    feedback: List[Feedback] = Field(description="List of feedback provided")


class PersonalInformation(BaseModel):
    name: str = Field(description="Name")
    email: str = Field(description="Email")
    phone: str = Field(description="Phone")
    location: str = Field(description="Address")
    website: str = Field(description="Website")
    linkedin: str = Field(description="LinkedIn")


class CompanyExperience(BaseModel):
    name: str = Field(description="Company name")
    position: str = Field(description="Position")
    start_date: str = Field(description="Start date")
    end_date: str = Field(description="End date")
    descriptions: List[str] = Field(description="Descriptions")


class Resume(BaseModel):
    personal_information: PersonalInformation = Field(description="Person information")
    skills: List[str] = Field(description="List of skills")
    languages: List[str] = Field(description="List of languages")
    interests: List[str] = Field(description="List of interests")
    about: str = Field(description="About me")
    experiences: List[CompanyExperience] = Field(
        description="List of experiences by job"
    )
    education: List[str] = Field(description="List of educations")
    certifications: List[str] = Field(description="List of certifications")
    projects: List[str] = Field(description="List of projects")
    achievements: List[str] = Field(description="List of achievements")
    additional_notes: str = Field(description="Additional notes")
    feedback: List[Feedback] = Field(
        description="List of feedback about the resume based on analysis"
    )


@CrewBase
class ResumeEnhancer:
    """ResumeEnhancer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def resume_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_analyzer"],  # type: ignore[index]
            verbose=True,
            max_retry_limit=MAX_RETRY_LIMIT,
        )

    @agent
    def resume_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_writer"],  # type: ignore[index]
            verbose=True,
            max_retry_limit=MAX_RETRY_LIMIT,
        )

    @agent
    def json_builder(self) -> Agent:
        return Agent(
            config=self.agents_config["json_builder"],  # type: ignore[index]
            verbose=True,
            max_retry_limit=MAX_RETRY_LIMIT,
        )

    @task
    def analysis(self) -> Task:
        return Task(
            config=self.tasks_config["analysis"],  # type: ignore[index]
        )

    @task
    def enhancer(self) -> Task:
        return Task(
            config=self.tasks_config["enhancer"],  # type: ignore[index]
        )

    @task
    def gather_feedback(self) -> Task:
        return Task(
            config=self.tasks_config["gather_feedback"],  # type: ignore[index]
            output_pydantic=FeedbackList,
        )

    @task
    def build_json(self) -> Task:
        return Task(
            config=self.tasks_config["build_json"],  # type: ignore[index]
            output_pydantic=Resume,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResumeEnhancer crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
