
import json
from crewai import Crew, Process
from .agents import entity_agent, statute_agent, precedent_agent, reasoner_agent, reporter_agent
from .tasks import (
    extract_entities_task, find_statutes_task, find_precedents_task, reasoning_task, report_task
)
from .schemas import CaseInput, EntityExtraction, RetrievalBundle, RetrievalHit, ReasoningOutput, Report
from .config import settings

def run_crew(case: CaseInput) -> Report:
    # Build agents
    a_entity = entity_agent()
    a_statute = statute_agent()
    a_precedent = precedent_agent()
    a_reason = reasoner_agent()
    a_report = reporter_agent()

    # Tasks
    t1 = extract_entities_task(a_entity, case)
    crew1 = Crew(agents=[a_entity], tasks=[t1], process=Process.sequential, verbose=True)
    entities_raw = crew1.kickoff()
    entities_json = entities_raw.raw if hasattr(entities_raw, 'raw') else str(entities_raw)
    entities = EntityExtraction.model_validate_json(entities_json)

    issues_json = EntityExtraction.model_dump_json(entities)

    t2 = find_statutes_task(a_statute, issues_json)
    t3 = find_precedents_task(a_precedent, issues_json, enable_api=bool(settings.indian_kanoon_api_key))
    crew2 = Crew(agents=[a_statute, a_precedent], tasks=[t2, t3], process=Process.sequential, verbose=True)
    res = crew2.kickoff()

    # Extract results
    statutes_json = t2.output.raw if hasattr(t2.output, 'raw') else str(t2.output)
    precedents_json = t3.output.raw if hasattr(t3.output, 'raw') else str(t3.output)

    try:
        statutes = [RetrievalHit.model_validate(o) for o in json.loads(statutes_json)]
    except Exception:
        statutes = []
    try:
        precedents = [RetrievalHit.model_validate(o) for o in json.loads(precedents_json)]
    except Exception:
        precedents = []

    retrievals = RetrievalBundle(statutes=statutes, precedents=precedents)
    stitched = {
        "entities": entities.model_dump(),
        "retrievals": {
            "statutes": [s.model_dump() for s in retrievals.statutes],
            "precedents": [p.model_dump() for p in retrievals.precedents],
        }
    }
    stitched_json = json.dumps(stitched, ensure_ascii=False)

    # Reasoning
    t4 = reasoning_task(a_reason, stitched_json)
    crew3 = Crew(agents=[a_reason], tasks=[t4], process=Process.sequential, verbose=True)
    _ = crew3.kickoff()
    reasoning_md = t4.output.raw if hasattr(t4.output, 'raw') else str(t4.output)

    # Report
    full_bundle = {
        "case_id": case.case_id,
        **stitched,
        "reasoning_md": reasoning_md
    }
    full_bundle_json = json.dumps(full_bundle, ensure_ascii=False)

    t5 = report_task(a_report, full_bundle_json, case.case_id)
    crew4 = Crew(agents=[a_report], tasks=[t5], process=Process.sequential, verbose=True)
    _ = crew4.kickoff()
    report_md = t5.output.raw if hasattr(t5.output, 'raw') else str(t5.output)

    reasoning = ReasoningOutput(analysis=reasoning_md, principles=[], likely_interpretations=[])
    out = Report(
        case_id=case.case_id,
        entities=entities,
        retrievals=retrievals,
        reasoning=reasoning,
        recommendations=[],
        summary=""
    )
    return out, report_md
