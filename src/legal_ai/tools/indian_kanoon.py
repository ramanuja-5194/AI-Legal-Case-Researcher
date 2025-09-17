
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests, json, os
from typing import Optional

from ..config import settings

class KanoonSearchInput(BaseModel):
    query: str = Field(..., description="Search query for Indian Kanoon (e.g., contract frustration)")
    max_results: int = Field(default=5, description="Max judgments to return (<= 20)" )

class IndianKanoonSearchTool(BaseTool):
    name: str = "indian_kanoon_search_tool"
    description: str = (
        "Search Indian Kanoon API for relevant judgments. Requires INDIAN_KANOON_API_KEY in env. "
        "Returns case name, court, year, link, and snippet when available."
    )
    args_schema = KanoonSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        api_key = settings.indian_kanoon_api_key
        if not api_key:
            return json.dumps({"error": "Set INDIAN_KANOON_API_KEY to enable this tool."})

        url = "https://api.indiankanoon.org/search/"
        params = {
            "formInput": query,
            "maxresults": max_results
        }
        headers = {"Authorization": f"Token {api_key}"}
        try:
            r = requests.get(url, params=params, headers=headers, timeout=30)
            r.raise_for_status()
            data = r.json()
            # Normalize a subset of fields
            out = []
            for hit in data.get("results", [])[:max_results]:
                out.append({
                    "source": "IndianKanoon",
                    "title": hit.get("title"),
                    "citation": hit.get("citation"),
                    "year": hit.get("year"),
                    "snippet": hit.get("snippet"),
                    "url": hit.get("link") or hit.get("doc_url"),
                    "score": hit.get("score"),
                    "metadata": {k: v for k, v in hit.items() if k not in ("snippet", "title", "citation", "year", "link", "doc_url", "score")}
                })
            return json.dumps(out, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})
