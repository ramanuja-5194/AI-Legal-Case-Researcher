
import argparse, json, os
from .schemas import CaseInput
from .crew import run_crew
from .config import settings

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, help="Path to .txt file with case text")
    parser.add_argument("--case-id", default="CASE-001", help="Case identifier")
    parser.add_argument("--use-flow", default="false", help="Use CrewAI Flows (true/false)")
    args = parser.parse_args()

    text = load_text(args.case)
    case = CaseInput(case_id=args.case_id, text=text)

    # Normal crew run
    report, report_md = run_crew(case)

    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, "report.md")
    json_path = os.path.join(out_dir, "report.json")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2, ensure_ascii=False))

    print("Saved:", md_path)
    print("Saved:", json_path)

if __name__ == "__main__":
    main()
