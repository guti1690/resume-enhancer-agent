from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ResumeEnhancer:
    """ResumeEnhancer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def linkedin_recruiter(self) -> Agent:
        return Agent(
            config=self.agents_config["linkedin_recruiter"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def resume_enhancer(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_enhancer"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["analysis_task"],  # type: ignore[index]
        )

    @task
    def resume_enhancer_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_enhancer_task"],  # type: ignore[index]
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
