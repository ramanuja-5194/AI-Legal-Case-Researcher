"""
Web search and scraping tools for legal research
"""
import os
import json
import requests
from typing import Optional
from crewai.tools import BaseTool

class IndianKanoonSearchTool(BaseTool):
    """
    Tool for searching Indian Kanoon for legal precedents
    """
    name: str = "Indian Kanoon Case Search"
    description: str = (
        "Search Indian Kanoon database for relevant case law, judgments, and precedents. "
        "Provide a clear description of the legal issue or case facts."
    )
    
    def _run(self, query: str) -> str:
        """
        Search Indian Kanoon
        
        Args:
            query: Legal issue or case description
        
        Returns:
            Formatted search results with case names and summaries
        """
        try:
            # Indian Kanoon search URL (basic web scraping approach)
            base_url = "https://indiankanoon.org/search/"
            search_url = f"{base_url}?formInput={requests.utils.quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Basic response - in production, parse HTML for actual results
                return (
                    f"Indian Kanoon Search Results for: '{query}'\n\n"
                    f"Search URL: {search_url}\n\n"
                    "Note: Please visit the URL above to view actual case results. "
                    "To automate this, you can:\n"
                    "1. Use BeautifulSoup to parse the HTML results\n"
                    "2. Apply for Indian Kanoon API access\n"
                    "3. Use their RSS feed for recent judgments\n\n"
                    "Typical results include:\n"
                    "- Case names with citations\n"
                    "- Court names and judges\n"
                    "- Brief summaries of holdings\n"
                    "- Links to full judgment text"
                )
            else:
                return f"Error accessing Indian Kanoon: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error searching Indian Kanoon: {str(e)}"

class LegalWebSearchTool(BaseTool):
    """
    General web search for legal information using Serper API
    """
    name: str = "Legal Web Search"
    description: str = (
        "Search the web for legal information, recent judgments, legal articles, "
        "and expert opinions. Use this for current legal developments and news."
    )
    
    def _run(self, query: str) -> str:
        """
        Search web using Serper API
        
        Args:
            query: Search query
        
        Returns:
            Formatted search results
        """
        api_key = os.environ.get('SERPER_API_KEY')
        
        if not api_key:
            return (
                "Serper API key not configured. To enable web search:\n"
                "1. Get API key from https://serper.dev/\n"
                "2. Add SERPER_API_KEY to your .env file\n\n"
                f"Manual search suggestion: Search Google for '{query}'"
            )
        
        try:
            url = "https://google.serper.dev/search"
            payload = json.dumps({
                "q": query,
                "num": 5
            })
            headers = {
                'X-API-KEY': api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            
            if response.status_code == 200:
                results = response.json()
                
                if 'organic' not in results:
                    return "No results found."
                
                formatted_results = []
                for i, result in enumerate(results['organic'][:5], 1):
                    formatted_results.append(
                        f"\n{i}. {result.get('title', 'No title')}\n"
                        f"   Link: {result.get('link', 'No link')}\n"
                        f"   {result.get('snippet', 'No description')}\n"
                    )
                
                return "".join(formatted_results)
            else:
                return f"Search error: HTTP {response.status_code}"
                
        except Exception as e:
            return f"Error during web search: {str(e)}"

class LegalDictionaryTool(BaseTool):
    """
    Tool for explaining legal terms and concepts
    """
    name: str = "Legal Terms Dictionary"
    description: str = (
        "Provides definitions and explanations of legal terms, concepts, "
        "and Latin phrases commonly used in Indian law."
    )
    
    def _run(self, term: str) -> str:
        """
        Define legal term
        
        Args:
            term: Legal term to define
        
        Returns:
            Definition and explanation
        """
        # Common legal terms dictionary
        legal_terms = {
            "prima facie": "At first sight; on the face of it. Evidence that is sufficient to establish a fact unless disproved.",
            "res judicata": "A matter already judged. A legal doctrine that prevents re-litigation of issues already decided.",
            "habeas corpus": "You shall have the body. A writ requiring a person to be brought before a judge or court.",
            "suo moto": "On its own motion. Action taken by a court on its own initiative without formal application.",
            "ratio decidendi": "The reason for the decision. The legal principle upon which a court's decision is based.",
            "obiter dicta": "Things said by the way. Statements made by a judge that are not essential to the decision.",
            "mens rea": "Guilty mind. The mental element of a crime; criminal intent.",
            "actus reus": "Guilty act. The physical element of a crime; the actual criminal deed.",
            "cognizable offense": "An offense where police can arrest without warrant and start investigation without court permission.",
            "non-cognizable offense": "An offense where police cannot arrest without warrant and need court permission to investigate.",
            "bailable offense": "An offense where the accused has a right to be released on bail.",
            "non-bailable offense": "An offense where bail is at the discretion of the court.",
            "writ": "A formal written order issued by a court.",
            "mandamus": "We command. A writ ordering a public official to perform a mandatory duty.",
            "certiorari": "To be informed. A writ for judicial review of a lower court's decision.",
            "prohibition": "A writ preventing a lower court from exceeding its jurisdiction.",
            "quo warranto": "By what authority. A writ questioning a person's right to hold public office.",
        }
        
        term_lower = term.lower().strip()
        
        if term_lower in legal_terms:
            return f"Term: {term}\n\nDefinition: {legal_terms[term_lower]}"
        else:
            return (
                f"Definition not found in local dictionary for: {term}\n\n"
                "Consider using the Legal Web Search tool to find the definition online."
            )
    
    def add_term(self, term: str, definition: str):
        """Add new term to dictionary (for extensibility)"""
        pass