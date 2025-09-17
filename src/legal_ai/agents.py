
from crewai import Agent, LLM
from .prompts import (
    ENTITY_EXTRACTOR_ROLE, ENTITY_EXTRACTOR_GOAL, ENTITY_EXTRACTOR_BACKSTORY,
    STATUTE_RETRIEVER_ROLE, STATUTE_RETRIEVER_GOAL, STATUTE_RETRIEVER_BACKSTORY,
    PRECEDENT_RETRIEVER_ROLE, PRECEDENT_RETRIEVER_GOAL, PRECEDENT_RETRIEVER_BACKSTORY,
    REASONER_ROLE, REASONER_GOAL, REASONER_BACKSTORY,
    REPORTER_ROLE, REPORTER_GOAL, REPORTER_BACKSTORY
)
from .config import settings
from .tools.rag import RAGSearchTool
from .tools.indian_kanoon import IndianKanoonSearchTool

def make_llm() -> LLM:
    return LLM(model=f"gemini/{settings.llm_model}", api_key=settings.google_api_key)

def entity_agent() -> Agent:
    return Agent(
        role=ENTITY_EXTRACTOR_ROLE.strip(),
        goal=ENTITY_EXTRACTOR_GOAL.strip(),
        backstory=ENTITY_EXTRACTOR_BACKSTORY.strip(),
        llm=make_llm(),
        max_iter=1,
        allow_delegation=False,
        verbose=True,
    )

def statute_agent() -> Agent:
    return Agent(
        role=STATUTE_RETRIEVER_ROLE.strip(),
        goal=STATUTE_RETRIEVER_GOAL.strip(),
        backstory=STATUTE_RETRIEVER_BACKSTORY.strip(),
        tools=[RAGSearchTool()],
        llm=make_llm(),
        max_iter=1,
        allow_delegation=False,
        verbose=True,
    )

def precedent_agent() -> Agent:
    return Agent(
        role=PRECEDENT_RETRIEVER_ROLE.strip(),
        goal=PRECEDENT_RETRIEVER_GOAL.strip(),
        backstory=PRECEDENT_RETRIEVER_BACKSTORY.strip(),
        tools=[IndianKanoonSearchTool()],
        llm=make_llm(),
        max_iter=1,
        allow_delegation=False,
        verbose=True,
    )

def reasoner_agent() -> Agent:
    return Agent(
        role=REASONER_ROLE.strip(),
        goal=REASONER_GOAL.strip(),
        backstory=REASONER_BACKSTORY.strip(),
        llm=make_llm(),
        max_iter=2,
        allow_delegation=False,
        verbose=True,
    )

def reporter_agent() -> Agent:
    return Agent(
        role=REPORTER_ROLE.strip(),
        goal=REPORTER_GOAL.strip(),
        backstory=REPORTER_BACKSTORY.strip(),
        llm=make_llm(),
        max_iter=1,
        allow_delegation=False,
        verbose=True,
    )
