"""
Configuration file for AI Legal Case Researcher
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class CaseType(str, Enum):
    """Types of legal cases"""
    CRIMINAL = "criminal"
    CIVIL = "civil"
    CONSTITUTIONAL = "constitutional"
    CONTRACT = "contract"
    PROPERTY = "property"
    COMPANY = "company"
    CONSUMER = "consumer"
    LABOUR = "labour"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    FAMILY = "family"
    TAX = "tax"
    OTHER = "other"

class LegalDocument(str, Enum):
    """Available legal documents"""
    CONSTITUTION = "constitution.txt"
    IPC = "IPC.txt"
    CRPC = "the_code_of_criminal_procedure._1973.txt"
    CPC = "the_code_of_civil_procedure._1908.txt"
    IEA = "iea_1872.txt"
    ICA = "ica_1872.txt"
    TPA = "the_transfer_of_property_act_1872.txt"
    COMPANIES_ACT = "the_companies_act_2013.txt"

class CaseInput(BaseModel):
    """Input model for case analysis"""
    case_text: str = Field(..., description="Full text of the case document")
    case_type: Optional[CaseType] = Field(None, description="Type of legal case")
    specific_queries: Optional[List[str]] = Field(
        default_factory=list,
        description="Specific legal questions or queries"
    )
    jurisdiction: str = Field(default="India", description="Legal jurisdiction")
    
    class Config:
        use_enum_values = True

class LegalEntity(BaseModel):
    """Extracted legal entities from case"""
    petitioner: Optional[str] = Field(None, description="Petitioner/Plaintiff name")
    respondent: Optional[str] = Field(None, description="Respondent/Defendant name")
    case_type: Optional[CaseType] = Field(None, description="Type of case")
    key_issues: List[str] = Field(default_factory=list, description="Key legal issues")
    relevant_sections: List[str] = Field(default_factory=list, description="Potentially relevant legal sections")
    
    class Config:
        use_enum_values = True

class RelevantStatute(BaseModel):
    """Model for relevant statute information"""
    act_name: str = Field(..., description="Name of the Act")
    section_number: str = Field(..., description="Section/Article number")
    section_text: str = Field(..., description="Text of the relevant section")
    relevance_explanation: str = Field(..., description="Why this section is relevant")

class Precedent(BaseModel):
    """Model for legal precedent/judgment"""
    case_name: str = Field(..., description="Name of the case")
    court: str = Field(..., description="Court that decided the case")
    year: str = Field(..., description="Year of judgment")
    citation: Optional[str] = Field(None, description="Case citation")
    summary: str = Field(..., description="Summary of the judgment")
    relevance: str = Field(..., description="How it applies to current case")

class LegalResearchOutput(BaseModel):
    """Final output model for legal research"""
    case_summary: str = Field(..., description="Summary of the input case")
    identified_parties: LegalEntity = Field(..., description="Identified parties and issues")
    relevant_statutes: List[RelevantStatute] = Field(
        default_factory=list,
        description="Relevant statutory provisions"
    )
    precedents: List[Precedent] = Field(
        default_factory=list,
        description="Relevant case precedents"
    )
    legal_reasoning: str = Field(..., description="Legal analysis and reasoning")
    recommendations: str = Field(..., description="Legal recommendations and next steps")
    research_confidence: str = Field(..., description="Confidence level and caveats")

# Configuration settings
class Settings:
    """Application settings"""
    # LLM Configuration
    LLM_MODEL = "gemini/gemini-2.5-flash"
    LLM_TEMPERATURE = 0.1  # Very low for precise legal analysis
    
    # Vector Store Configuration
    VECTOR_DB_PATH = "./data/chroma_db"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Legal Documents Path
    LEGAL_DOCS_PATH = "./legal_documents"
    
    # RAG Configuration
    TOP_K_RESULTS = 8  # Reduced from 10
    SIMILARITY_THRESHOLD = 0.6
    
    # CrewAI Configuration
    MAX_ITER = 15  # Reduced from 25 to prevent infinite loops
    VERBOSE = True

settings = Settings()