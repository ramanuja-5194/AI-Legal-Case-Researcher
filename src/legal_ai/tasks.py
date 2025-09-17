
from crewai import Task
from .schemas import CaseInput
from .prompts import ENTITY_TASK_DESCRIPTION, REPORT_EXPECTED_OUTPUT

def extract_entities_task(agent, case: CaseInput) -> Task:
    return Task(
        description=ENTITY_TASK_DESCRIPTION.strip() + f"\nCASE TEXT BEGIN\n{case.text[:8000]}\nCASE TEXT END",
        expected_output="JSON strictly matching EntityExtraction schema.",
        agent=agent,
    )

def find_statutes_task(agent, issues_json: str) -> Task:
    return Task(
        description=(
            "Use the RAG search tool to find the most relevant Indian statutes/sections corresponding to the extracted issues.\n"
            "Return a concise JSON list: Act/Section, short relevance snippet (<=60 words), optional citation/year, and source metadata."
            f"\nExtracted Issues JSON:\n{issues_json}"
        ),
        expected_output="JSON list of statute RetrievalHit objects.",
        agent=agent,
    )

def find_precedents_task(agent, issues_json: str, enable_api: bool = True) -> Task:
    note = "Indian Kanoon API tool is available." if enable_api else "Indian Kanoon API key missing; provide local heuristics or placeholders."
    return Task(
        description=(
            f"{note} Search the most relevant Indian judgments for the extracted issues.\n"
            "Return case name, court, year, holding summary (<=80 words), and link when available. Also include citations if present."
            f"\nExtracted Issues JSON:\n{issues_json}"
        ),
        expected_output="JSON list of precedent RetrievalHit objects.",
        agent=agent,
    )

def reasoning_task(agent, stitched_json: str) -> Task:
    return Task(
        description=(
            "Given the extracted entities/issues and the retrieved statutes and judgments, write a reasoned analysis: key principles, likely interpretations, and how courts tend to analyze such issues in India."
            f"\nDATA JSON:\n{stitched_json}"
        ),
        expected_output="Markdown prose plus a JSON block with principles and likely_interpretations.",
        agent=agent,
    )

def report_task(agent, full_bundle_json: str, case_id: str) -> Task:
    return Task(
        description=(
            f"Compose the final structured research report for case_id={case_id}.\n"
            f"Follow this strictly:\n{REPORT_EXPECTED_OUTPUT}\n"
            f"DATA JSON:\n{full_bundle_json}"
        ),
        expected_output="A polished Markdown report suitable for an advocate's brief.",
        agent=agent,
    )
