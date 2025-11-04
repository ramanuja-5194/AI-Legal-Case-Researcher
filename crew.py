"""
Legal Research Crew - Main Orchestration
"""
from crewai import Crew, Process
from agents import LegalResearchAgents
from tasks import LegalResearchTasks
from config import CaseInput, settings
from typing import Optional, List

class LegalResearchCrew:
    """
    Main crew for conducting legal research
    """
    
    def __init__(self, case_input: CaseInput):
        """
        Initialize the legal research crew
        
        Args:
            case_input: CaseInput object with case details
        """
        self.case_text = case_input.case_text
        self.case_type = case_input.case_type
        self.specific_queries = case_input.specific_queries
        self.jurisdiction = case_input.jurisdiction
        
        # Initialize agents and tasks
        self.agents = LegalResearchAgents()
        self.tasks_manager = LegalResearchTasks()
    
    def run(self) -> str:
        """
        Execute the legal research workflow
        
        Returns:
            Final legal research report
        """
        print("\n" + "="*80)
        print("AI LEGAL CASE RESEARCHER - STARTING RESEARCH")
        print("="*80 + "\n")
        
        # Define agents
        print("Initializing legal research team...")
        research_manager = self.agents.legal_research_manager()
        case_analyst = self.agents.case_analyst()
        statute_researcher = self.agents.statute_researcher()
        precedent_researcher = self.agents.precedent_researcher()
        legal_drafter = self.agents.legal_drafter()
        quality_reviewer = self.agents.quality_reviewer()
        
        print("✓ Research Manager initialized")
        print("✓ Case Analyst initialized")
        print("✓ Statute Researcher initialized")
        print("✓ Precedent Researcher initialized")
        print("✓ Legal Drafter initialized")
        print("✓ Quality Reviewer initialized\n")
        
        # Define tasks
        print("Creating research tasks...")
        
        # Task 1: Analyze case
        analyze_task = self.tasks_manager.analyze_case_task(
            agent=case_analyst,
            case_text=self.case_text,
            specific_queries=self.specific_queries
        )
        print("✓ Case analysis task created")
        
        # Task 2: Research statutes
        statutes_task = self.tasks_manager.research_statutes_task(
            agent=statute_researcher,
            case_analysis_context=analyze_task
        )
        print("✓ Statutory research task created")
        
        # Task 3: Research precedents
        precedents_task = self.tasks_manager.research_precedents_task(
            agent=precedent_researcher,
            case_analysis_context=analyze_task,
            statutes_context=statutes_task
        )
        print("✓ Precedent research task created")
        
        # Task 4: Draft report
        draft_task = self.tasks_manager.draft_legal_research_report_task(
            agent=legal_drafter,
            case_analysis_context=analyze_task,
            statutes_context=statutes_task,
            precedents_context=precedents_task
        )
        print("✓ Report drafting task created")
        
        # Task 5: Review report
        review_task = self.tasks_manager.review_research_report_task(
            agent=quality_reviewer,
            research_report_context=draft_task
        )
        print("✓ Quality review task created\n")
        
        # Create crew
        print("Assembling the legal research crew...\n")
        crew = Crew(
            agents=[
                research_manager,
                case_analyst,
                statute_researcher,
                precedent_researcher,
                legal_drafter,
                quality_reviewer
            ],
            tasks=[
                analyze_task,
                statutes_task,
                precedents_task,
                draft_task,
                review_task
            ],
            process=Process.sequential,  # Tasks execute in order
            verbose=settings.VERBOSE,
            max_rpm=10,  # Respect API rate limits
            memory=False,  # Disable memory to reduce complexity
        )
        
        # Execute the crew
        print("="*80)
        print("STARTING LEGAL RESEARCH PROCESS")
        print("="*80 + "\n")
        
        try:
            result = crew.kickoff()
            
            print("\n" + "="*80)
            print("LEGAL RESEARCH COMPLETED SUCCESSFULLY")
            print("="*80 + "\n")
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error during research: {str(e)}")
            raise


class QuickLegalResearchCrew:
    """
    Simplified crew for faster research (without quality review)
    Use this for quick analysis
    """
    
    def __init__(self, case_input: CaseInput):
        self.case_text = case_input.case_text
        self.case_type = case_input.case_type
        self.specific_queries = case_input.specific_queries
        
        self.agents = LegalResearchAgents()
        self.tasks_manager = LegalResearchTasks()
    
    def run(self) -> str:
        """Execute quick legal research"""
        print("\n" + "="*80)
        print("QUICK LEGAL RESEARCH - STARTING")
        print("="*80 + "\n")
        
        # Simplified team
        case_analyst = self.agents.case_analyst()
        statute_researcher = self.agents.statute_researcher()
        legal_drafter = self.agents.legal_drafter()
        
        # Simplified tasks
        analyze_task = self.tasks_manager.analyze_case_task(
            agent=case_analyst,
            case_text=self.case_text,
            specific_queries=self.specific_queries
        )
        
        statutes_task = self.tasks_manager.research_statutes_task(
            agent=statute_researcher,
            case_analysis_context=analyze_task
        )
        
        draft_task = self.tasks_manager.draft_legal_research_report_task(
            agent=legal_drafter,
            case_analysis_context=analyze_task,
            statutes_context=statutes_task,
            precedents_context=""  # Skip precedents for speed
        )
        
        crew = Crew(
            agents=[case_analyst, statute_researcher, legal_drafter],
            tasks=[analyze_task, statutes_task, draft_task],
            process=Process.sequential,
            verbose=settings.VERBOSE,
            memory=False,  # Disable to reduce complexity
        )
        
        result = crew.kickoff()
        
        print("\n" + "="*80)
        print("QUICK RESEARCH COMPLETED")
        print("="*80 + "\n")
        
        return result