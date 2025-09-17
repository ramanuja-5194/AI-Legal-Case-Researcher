
from crewai.flow import Flow, start, router
from pydantic import BaseModel
import json
from ..schemas import CaseInput, Report
from ..crew import run_crew

class CaseState(BaseModel):
    case_id: str
    text: str

class LegalResearchFlow(Flow[CaseState]):

    @start()
    def begin(self) -> str:
        return f"Starting legal research flow for {self.state.case_id}"

    @router(begin)
    def route(self):
        # Single path, but here you could branch by case type or length etc.
        return self.research

    def research(self):
        case = CaseInput(case_id=self.state.case_id, text=self.state.text)
        report, report_md = run_crew(case)
        self.state_report_md = report_md  # stash
        return "done"

def build_flow(case: CaseInput) -> LegalResearchFlow:
    flow = LegalResearchFlow()
    flow.state = CaseState(case_id=case.case_id, text=case.text)
    flow.setup()
    return flow
