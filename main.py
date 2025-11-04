"""
AI Legal Case Researcher - Main Application
"""
import os
from dotenv import load_dotenv
from pathlib import Path
from textwrap import dedent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from config import CaseInput, CaseType
from crew import LegalResearchCrew, QuickLegalResearchCrew

# Load environment variables
load_dotenv()

# Disable CrewAI telemetry to prevent timeout errors
os.environ['OTEL_SDK_DISABLED'] = 'true'

# Initialize Rich console for better output
console = Console()

def display_welcome():
    """Display welcome message"""
    welcome_text = """
    # 🏛️ AI Legal Case Researcher
    
    ## Powered by CrewAI & RAG Technology
    
    This system helps you conduct comprehensive legal research on Indian law cases by:
    - Analyzing case documents and extracting key information
    - Searching through Constitution, IPC, CrPC, CPC, Evidence Act, Contract Act, etc.
    - Finding relevant statutory provisions
    - Searching for applicable precedents
    - Providing detailed legal analysis and recommendations
    
    **Note**: This is an AI-powered research assistant. Always verify findings with qualified legal professionals.
    """
    console.print(Panel(Markdown(welcome_text), border_style="blue"))

def get_case_input() -> CaseInput:
    """
    Get case input from user
    
    Returns:
        CaseInput object
    """
    console.print("\n[bold cyan]CASE INPUT[/bold cyan]", style="bold")
    console.print("="*80 + "\n")
    
    # Option 1: Load from file
    use_file = Confirm.ask("Do you want to load case text from a file?", default=True)
    
    if use_file:
        file_path = Prompt.ask("Enter the path to your case file (text file)")
        
        if not os.path.exists(file_path):
            console.print(f"[red]Error: File not found: {file_path}[/red]")
            console.print("Falling back to manual input...")
            case_text = get_manual_case_input()
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                case_text = f.read()
            console.print(f"[green]✓ Loaded case from {file_path}[/green]")
            console.print(f"[dim]Preview: {case_text[:200]}...[/dim]\n")
    else:
        case_text = get_manual_case_input()
    
    # Get case type
    console.print("\n[bold]Case Type[/bold]")
    console.print("Options: criminal, civil, constitutional, contract, property, company, consumer, labour, family, tax, other")
    case_type_str = Prompt.ask("Enter case type", default="other")
    
    try:
        case_type = CaseType(case_type_str.lower())
    except ValueError:
        console.print("[yellow]Invalid case type. Using 'other'[/yellow]")
        case_type = CaseType.OTHER
    
    # Get specific queries
    console.print("\n[bold]Specific Legal Questions (Optional)[/bold]")
    console.print("Enter any specific legal questions you want answered (one per line).")
    console.print("Press Enter twice when done.\n")
    
    queries = []
    while True:
        query = Prompt.ask("Question (or press Enter to finish)", default="")
        if not query:
            break
        queries.append(query)
    
    # Create CaseInput object
    case_input = CaseInput(
        case_text=case_text,
        case_type=case_type,
        specific_queries=queries if queries else None
    )
    
    return case_input

def get_manual_case_input() -> str:
    """Get case text via manual input"""
    console.print("\n[bold]Enter Case Text[/bold]")
    console.print("Paste your case text below. Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done.\n")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    return "\n".join(lines)

def save_report(report: str, output_path: str = None):
    """
    Save research report to file
    
    Args:
        report: The research report text
        output_path: Optional custom output path
    """
    if output_path is None:
        # Create outputs directory if it doesn't exist
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"legal_research_report_{timestamp}.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    console.print(f"\n[green]✓ Report saved to: {output_path}[/green]")

def main():
    """Main application flow"""
    try:
        # Display welcome
        display_welcome()
        
        # Check for API key
        if not os.environ.get('GOOGLE_API_KEY'):
            console.print("[red]Error: GOOGLE_API_KEY not found in environment variables![/red]")
            console.print("Please set your Google API key in the .env file")
            return
        
        # Get case input
        case_input = get_case_input()
        
        # Confirm before proceeding
        console.print("\n[bold cyan]READY TO START RESEARCH[/bold cyan]")
        console.print(f"Case Type: {case_input.case_type}")
        console.print(f"Text Length: {len(case_input.case_text)} characters")
        if case_input.specific_queries:
            console.print(f"Specific Questions: {len(case_input.specific_queries)}")
        
        # Choose research mode
        console.print("\n[bold]Research Mode:[/bold]")
        console.print("1. Full Research (includes precedent search and quality review) - ~5-10 minutes")
        console.print("2. Quick Research (statutory analysis only) - ~2-3 minutes")
        
        mode = Prompt.ask("Select mode", choices=["1", "2"], default="1")
        
        if not Confirm.ask("\nProceed with research?", default=True):
            console.print("[yellow]Research cancelled.[/yellow]")
            return
        
        # Initialize and run crew
        console.print("\n[bold green]Starting legal research...[/bold green]\n")
        
        if mode == "1":
            crew = LegalResearchCrew(case_input)
        else:
            crew = QuickLegalResearchCrew(case_input)
        
        result = crew.run()
        
        # Display result
        console.print("\n" + "="*80)
        console.print("[bold green]LEGAL RESEARCH REPORT[/bold green]")
        console.print("="*80 + "\n")
        
        # Display as markdown
        console.print(Markdown(str(result)))
        
        # Save report
        if Confirm.ask("\nSave report to file?", default=True):
            custom_path = Prompt.ask("Enter custom file path (or press Enter for auto)", default="")
            save_report(str(result), custom_path if custom_path else None)
        
        console.print("\n[bold green]✓ Research Complete![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Research interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        import traceback
        console.print("[dim]" + traceback.format_exc() + "[/dim]")

if __name__ == "__main__":
    main()