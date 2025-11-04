"""
Analysis and processing tools for legal documents
"""
import re
from typing import List, Dict, Optional
from crewai.tools import BaseTool
from config import CaseType

class LegalEntityExtractorTool(BaseTool):
    """
    Tool for extracting legal entities from case text
    """
    name: str = "Legal Entity Extractor"
    description: str = (
        "Extracts key legal entities from case text including parties involved, "
        "case type, key issues, and mentioned legal provisions. "
        "Provide the full case text as input."
    )
    
    def _run(self, case_text: str) -> str:
        """
        Extract entities from case text
        
        Args:
            case_text: Full text of the case
        
        Returns:
            Structured extraction of entities
        """
        try:
            entities = {
                "parties": self._extract_parties(case_text),
                "case_type": self._identify_case_type(case_text),
                "mentioned_sections": self._extract_sections(case_text),
                "key_terms": self._extract_legal_terms(case_text),
                "dates": self._extract_dates(case_text),
                "amounts": self._extract_amounts(case_text)
            }
            
            # Format output
            output = "EXTRACTED LEGAL ENTITIES:\n" + "="*80 + "\n\n"
            
            output += "PARTIES INVOLVED:\n"
            for party_type, party_name in entities["parties"].items():
                output += f"  {party_type}: {party_name}\n"
            
            output += f"\nIDENTIFIED CASE TYPE: {entities['case_type']}\n"
            
            if entities["mentioned_sections"]:
                output += "\nMENTIONED LEGAL PROVISIONS:\n"
                for section in entities["mentioned_sections"][:10]:
                    output += f"  - {section}\n"
            
            if entities["key_terms"]:
                output += "\nKEY LEGAL TERMS:\n"
                for term in entities["key_terms"][:10]:
                    output += f"  - {term}\n"
            
            if entities["dates"]:
                output += "\nIMPORTANT DATES:\n"
                for date in entities["dates"][:5]:
                    output += f"  - {date}\n"
            
            if entities["amounts"]:
                output += "\nMONETARY AMOUNTS:\n"
                for amount in entities["amounts"][:5]:
                    output += f"  - {amount}\n"
            
            return output
            
        except Exception as e:
            return f"Error extracting entities: {str(e)}"
    
    def _extract_parties(self, text: str) -> Dict[str, str]:
        """Extract party names"""
        parties = {}
        
        # Common patterns
        petitioner_patterns = [
            r"(?:petitioner|plaintiff|appellant)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:v\.|vs\.?|versus)"
        ]
        
        respondent_patterns = [
            r"(?:respondent|defendant|appellee)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"(?:v\.|vs\.?|versus)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
        ]
        
        for pattern in petitioner_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parties["Petitioner/Plaintiff"] = match.group(1)
                break
        
        for pattern in respondent_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                parties["Respondent/Defendant"] = match.group(1)
                break
        
        if not parties:
            parties = {"Note": "No party names clearly identified in text"}
        
        return parties
    
    def _identify_case_type(self, text: str) -> str:
        """Identify case type based on keywords"""
        text_lower = text.lower()
        
        case_type_keywords = {
            CaseType.CRIMINAL: ["murder", "theft", "robbery", "criminal", "ipc", "crpc", "fir", "cognizable"],
            CaseType.CIVIL: ["civil suit", "damages", "injunction", "specific performance", "cpc"],
            CaseType.CONSTITUTIONAL: ["article", "fundamental right", "constitution", "writ", "habeas corpus"],
            CaseType.CONTRACT: ["contract", "breach", "agreement", "consideration", "offer", "acceptance"],
            CaseType.PROPERTY: ["property", "title", "possession", "transfer", "immovable"],
            CaseType.COMPANY: ["company", "director", "shareholder", "companies act", "board"],
            CaseType.CONSUMER: ["consumer", "deficiency", "service", "goods", "consumer forum"],
            CaseType.LABOUR: ["labour", "employment", "wages", "industrial dispute", "workman"],
            CaseType.FAMILY: ["divorce", "custody", "maintenance", "marriage", "matrimonial"],
            CaseType.TAX: ["tax", "income tax", "gst", "customs", "assessment"]
        }
        
        scores = {}
        for case_type, keywords in case_type_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[case_type.value] = score
        
        if scores:
            return max(scores, key=scores.get)
        return CaseType.OTHER.value
    
    def _extract_sections(self, text: str) -> List[str]:
        """Extract mentioned legal sections"""
        sections = []
        
        # Patterns for various legal references
        patterns = [
            r"Section\s+\d+[A-Z]?(?:\(\d+\))?(?:\s+(?:of\s+)?(?:the\s+)?[\w\s]+Act(?:,\s*\d{4})?)?",
            r"Article\s+\d+[A-Z]?(?:\(\d+\))?",
            r"Rule\s+\d+",
            r"Order\s+[IVX]+\s+Rule\s+\d+",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            sections.extend(matches)
        
        return list(set(sections))  # Remove duplicates
    
    def _extract_legal_terms(self, text: str) -> List[str]:
        """Extract legal terms and phrases"""
        legal_terms = [
            "prima facie", "res judicata", "habeas corpus", "suo moto",
            "mens rea", "actus reus", "ratio decidendi", "obiter dicta",
            "natural justice", "locus standi", "caveat emptor",
            "ultra vires", "bona fide", "mala fide", "ex parte"
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in legal_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        date_patterns = [
            r"\d{1,2}[-/]\d{1,2}[-/]\d{4}",
            r"\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}"
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))[:5]  # Return unique dates, max 5
    
    def _extract_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts"""
        amount_patterns = [
            r"Rs\.?\s*[\d,]+(?:\.\d{2})?",
            r"INR\s*[\d,]+(?:\.\d{2})?",
            r"₹\s*[\d,]+(?:\.\d{2})?",
        ]
        
        amounts = []
        for pattern in amount_patterns:
            matches = re.findall(pattern, text)
            amounts.extend(matches)
        
        return list(set(amounts))[:5]  # Return unique amounts, max 5


class CaseSummarizerTool(BaseTool):
    """
    Tool for summarizing case facts
    """
    name: str = "Case Summarizer"
    description: str = (
        "Creates a concise summary of case facts, highlighting the key points, "
        "parties involved, and main legal issues. Use this to get a quick overview "
        "of a lengthy case document."
    )
    
    def _run(self, case_text: str) -> str:
        """
        Summarize case text
        
        Args:
            case_text: Full case text
        
        Returns:
            Summary of key points
        """
        # This is a basic keyword-based summarizer
        # In production, you might use the LLM itself for better summaries
        
        lines = case_text.split('\n')
        important_lines = []
        
        keywords = [
            'petitioner', 'respondent', 'plaintiff', 'defendant',
            'alleged', 'claimed', 'contention', 'issue', 'question',
            'facts', 'circumstances', 'incident', 'occurred'
        ]
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in keywords):
                if len(line.strip()) > 20:  # Avoid very short lines
                    important_lines.append(line.strip())
        
        if important_lines:
            summary = "CASE SUMMARY (Key Extracted Lines):\n" + "="*80 + "\n\n"
            summary += "\n\n".join(important_lines[:15])  # Top 15 lines
            return summary
        else:
            return "Unable to generate automatic summary. Please provide case summary manually."


class LegalIssueIdentifierTool(BaseTool):
    """
    Tool for identifying legal issues and questions
    """
    name: str = "Legal Issue Identifier"
    description: str = (
        "Identifies the key legal issues, questions, and points of law "
        "that need to be addressed in a case. Helps structure the legal analysis."
    )
    
    def _run(self, case_text: str) -> str:
        """
        Identify legal issues
        
        Args:
            case_text: Case text or summary
        
        Returns:
            List of identified legal issues
        """
        issues = []
        text_lower = case_text.lower()
        
        # Look for explicit issue statements
        issue_patterns = [
            r"(?:issue|question|point).*?is.*?whether.*?[.?]",
            r"(?:issue|question|point).*?:[^\n]+",
            r"(?:the\s+)?main\s+(?:issue|question|contention).*?[.?]"
        ]
        
        for pattern in issue_patterns:
            matches = re.findall(pattern, case_text, re.IGNORECASE | re.DOTALL)
            issues.extend([m.strip() for m in matches if len(m.strip()) > 20])
        
        # Identify based on keywords
        keyword_issues = {
            "Whether the accused is guilty": ["guilty", "committed", "offense"],
            "Validity of contract": ["contract", "valid", "void", "voidable"],
            "Breach of contract": ["breach", "violation", "non-performance"],
            "Constitutional validity": ["constitutional", "article", "fundamental right"],
            "Interpretation of statute": ["interpretation", "meaning", "section"],
            "Jurisdiction": ["jurisdiction", "competent", "authority"],
            "Natural justice": ["natural justice", "fair hearing", "bias"],
            "Limitation period": ["limitation", "barred by time", "prescribed period"],
        }
        
        identified_issues = []
        for issue_desc, keywords in keyword_issues.items():
            if all(keyword in text_lower for keyword in keywords):
                identified_issues.append(issue_desc)
        
        output = "IDENTIFIED LEGAL ISSUES:\n" + "="*80 + "\n\n"
        
        if issues:
            output += "Explicitly Stated Issues:\n"
            for i, issue in enumerate(issues[:5], 1):
                output += f"{i}. {issue}\n"
            output += "\n"
        
        if identified_issues:
            output += "Potential Issues Based on Keywords:\n"
            for i, issue in enumerate(identified_issues, 1):
                output += f"{i}. {issue}\n"
        
        if not issues and not identified_issues:
            output += "No clear issues identified. Manual analysis recommended.\n"
        
        return output