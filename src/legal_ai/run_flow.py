
import argparse, os
from .schemas import CaseInput
from .flows.flow import build_flow

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, help="Path to .txt file with case text")
    parser.add_argument("--case-id", default="CASE-001", help="Case identifier")
    args = parser.parse_args()

    with open(args.case, "r", encoding="utf-8") as f:
        text = f.read()

    case = CaseInput(case_id=args.case_id, text=text)
    flow = build_flow(case)
    flow.run()
    # The flow uses the same crew under the hood; reports are saved by main.py

if __name__ == "__main__":
    main()
