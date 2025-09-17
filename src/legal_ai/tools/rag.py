
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os, json

from ..config import settings

class RAGSearchInput(BaseModel):
    query: str = Field(..., description="Search query in natural language")
    top_k: int = Field(default=6, description="Number of passages to retrieve")

class RAGSearchTool(BaseTool):
    name: str = "rag_search_tool"
    description: str = (
        "Search the local FAISS vector DB of Indian legal texts (statutes, codes, etc.) "
        "and return the most relevant sections with metadata and short snippets."
    )
    args_schema = RAGSearchInput

    def _load_vectorstore(self) -> Optional[FAISS]:
        vector_dir = settings.vectorstore_dir
        if not os.path.exists(vector_dir):
            return None
        try:
            embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
            return FAISS.load_local(vector_dir, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"[RAGSearchTool] Failed loading vectorstore: {e}")
            return None

    def _run(self, query: str, top_k: int = 6) -> str:
        vs = self._load_vectorstore()
        if vs is None:
            return json.dumps({"error": "Vectorstore not found. Run ingest.py first."})
        docs: List[Document] = vs.similarity_search(query, k=top_k)
        results = []
        for d in docs:
            md = d.metadata or {}
            results.append({
                "source": md.get("source", "local"),
                "title": md.get("title", md.get("section", "")),
                "citation": md.get("citation"),
                "year": md.get("year"),
                "snippet": d.page_content[:500],
                "url": md.get("url"),
                "score": None,
                "metadata": md
            })
        return json.dumps(results, ensure_ascii=False, indent=2)
