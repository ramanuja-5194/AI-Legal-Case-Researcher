
from typing import List
import re

def clean_legal_text(text: str) -> str:
    # Basic cleanup: normalize whitespace, remove excessive linebreaks/page numbers
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

def split_sections(text: str) -> List[str]:
    # Simple heuristic split by sections/chapters/acts
    return re.split(r"(?i)\n\s*(section\s+\d+[a-z]?|chapter\s+\w+|article\s+\d+)\s*[:.-]?\s*", text)
