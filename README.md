
# AI Legal Case Researcher (CrewAI + RAG)

End-to-end local project to analyze a legal case (as text), identify key entities/issues, retrieve relevant statutes & precedents, and produce a structured research report.  
Built with **CrewAI agents**, **LangChain + FAISS** RAG, and optional **Indian Kanoon API** integration.

## Features
- Input: case text file (`.txt`) – OCR intentionally out of scope for v1.
- Preprocessing & entity/issue extraction via an agent.
- Vector DB (FAISS) over local corpus of Indian laws you already downloaded.
- External precedent retrieval (optional) via Indian Kanoon API.
- Legal reasoning & summarization agents.
- Final output: Markdown + JSON in `src/legal_ai/output/`.

## Quickstart

1) **Install Poetry** (if you don't have it):
```bash
pipx install poetry    # or: pip install poetry
```

2) **Install deps and create venv**:
```bash
poetry install
```

3) **Create `.env`** from `.env.example` and set your keys/paths.

4) **Put your statutes/books** (Constitution, IPC, CrPC, CPC, Evidence Act, Contract Act, etc.)  
as `.txt` files under `src/legal_ai/data/corpus/`. (One big TXT per act is fine.)

5) **Build vectorstore**:
```bash
poetry run python src/legal_ai/ingest.py
```

6) **Run the crew** on your case file (text input):
```bash
poetry run python src/legal_ai/main.py --case ./my_case.txt --use-flow false
# or try the Flow version:
poetry run python src/legal_ai/run_flow.py --case ./my_case.txt
```

Outputs are saved to `src/legal_ai/output/report.md` and `report.json`.

## Notes
- Uses **Gemini** via `GOOGLE_API_KEY`. Adjust `LLM_MODEL` in `.env` if needed.
- The **Indian Kanoon API** is optional; set `INDIAN_KANOON_API_KEY` to enable.
- This repo focuses on local execution. Deployment, OCR, and UI are intentionally left out.
