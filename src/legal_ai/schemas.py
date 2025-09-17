
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CaseInput(BaseModel):
    case_id: str = Field(..., description="A unique identifier for the case") 
    text: str = Field(..., description="Raw case text input. OCR already applied.")
    jurisdiction: Optional[str] = Field(default="India", description="Jurisdiction for legal retrieval")
    hints: Optional[List[str]] = Field(default=None, description="Optional keywords or issues from user") 

class EntityExtraction(BaseModel):
    parties: List[str] = Field(default_factory=list)
    case_type: Optional[str] = None
    issues: List[str] = Field(default_factory=list)

class RetrievalHit(BaseModel):
    source: str
    title: str
    citation: Optional[str] = None
    year: Optional[int] = None
    snippet: Optional[str] = None
    url: Optional[str] = None
    score: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RetrievalBundle(BaseModel):
    statutes: List[RetrievalHit] = Field(default_factory=list)
    precedents: List[RetrievalHit] = Field(default_factory=list)

class ReasoningOutput(BaseModel):
    analysis: str
    principles: List[str] = Field(default_factory=list)
    likely_interpretations: List[str] = Field(default_factory=list)

class Report(BaseModel):
    case_id: str
    entities: EntityExtraction
    retrievals: RetrievalBundle
    reasoning: ReasoningOutput
    recommendations: List[str] = Field(default_factory=list)
    summary: str = Field(default="", description="Executive summary")
