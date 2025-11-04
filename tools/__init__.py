"""
Legal Research Tools Package
"""

from tools.rag_tools import LegalRAGTool, StatuteSearchTool, PrecedentSearchTool
from tools.web_tools import IndianKanoonSearchTool, LegalWebSearchTool, LegalDictionaryTool
from tools.analysis_tools import LegalEntityExtractorTool, CaseSummarizerTool, LegalIssueIdentifierTool

__all__ = [
    'LegalRAGTool',
    'StatuteSearchTool',
    'PrecedentSearchTool',
    'IndianKanoonSearchTool',
    'LegalWebSearchTool',
    'LegalDictionaryTool',
    'LegalEntityExtractorTool',
    'CaseSummarizerTool',
    'LegalIssueIdentifierTool',
]