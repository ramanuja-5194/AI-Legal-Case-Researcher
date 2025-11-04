"""
Setup script to initialize the AI Legal Case Researcher
This script sets up the vector database and verifies the installation
"""
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Disable CrewAI telemetry
os.environ['OTEL_SDK_DISABLED'] = 'true'

console = Console()

def check_dependencies():
    """Check if all required dependencies are installed"""
    console.print("[bold cyan]Checking dependencies...[/bold cyan]")
    
    required_packages = [
        'crewai', 'langchain', 'langchain_google_genai', 
        'chromadb', 'sentence_transformers', 'pydantic', 
        'requests', 'rich', 'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            console.print(f"  ✓ {package}")
        except ImportError:
            console.print(f"  ✗ {package} [red](missing)[/red]")
            missing.append(package)
    
    if missing:
        console.print(f"\n[red]Missing packages: {', '.join(missing)}[/red]")
        console.print("Please run: pip install -r requirements.txt")
        return False
    
    console.print("[green]All dependencies installed![/green]\n")
    return True

def check_environment():
    """Check environment variables"""
    console.print("[bold cyan]Checking environment configuration...[/bold cyan]")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        console.print("  ✗ GOOGLE_API_KEY [red](not set)[/red]")
        console.print("\n[yellow]Please set your Google API key in .env file:[/yellow]")
        console.print("  1. Copy .env.example to .env")
        console.print("  2. Add your Google API key")
        return False
    else:
        console.print(f"  ✓ GOOGLE_API_KEY (set)")
    
    console.print("[green]Environment configured![/green]\n")
    return True

def check_legal_documents():
    """Check if legal documents are present"""
    console.print("[bold cyan]Checking legal documents...[/bold cyan]")
    
    legal_docs_path = Path("legal_documents")
    
    if not legal_docs_path.exists():
        console.print(f"  ✗ {legal_docs_path} directory [red](not found)[/red]")
        console.print("\n[yellow]Creating legal_documents directory...[/yellow]")
        legal_docs_path.mkdir(exist_ok=True)
        console.print(f"  ✓ Created {legal_docs_path}")
    
    required_docs = [
        'constitution.txt',
        'IPC.txt',
        'the_code_of_criminal_procedure._1973.txt',
        'the_code_of_civil_procedure._1908.txt',
        'iea_1872.txt',
        'ica_1872.txt',
        'the_transfer_of_property_act_1872.txt',
        'the_companies_act_2013.txt',
    ]
    
    missing_docs = []
    for doc in required_docs:
        doc_path = legal_docs_path / doc
        if doc_path.exists():
            size = doc_path.stat().st_size / 1024  # KB
            console.print(f"  ✓ {doc} ({size:.1f} KB)")
        else:
            console.print(f"  ✗ {doc} [yellow](missing)[/yellow]")
            missing_docs.append(doc)
    
    if missing_docs:
        console.print(f"\n[yellow]Missing {len(missing_docs)} document(s)[/yellow]")
        console.print("Please place your .txt legal documents in the legal_documents/ directory")
        console.print("\nExpected files:")
        for doc in missing_docs:
            console.print(f"  - {doc}")
        return False
    
    console.print("[green]All legal documents found![/green]\n")
    return True

def initialize_vector_db():
    """Initialize the vector database"""
    console.print("[bold cyan]Initializing vector database...[/bold cyan]")
    
    vector_db_path = Path("data/chroma_db")
    
    if vector_db_path.exists():
        console.print(f"  ℹ Vector database already exists at {vector_db_path}")
        from rich.prompt import Confirm
        if not Confirm.ask("Rebuild vector database?", default=False):
            console.print("[yellow]Skipping vector database initialization[/yellow]\n")
            return True
    
    try:
        console.print("  This may take a few minutes...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing legal documents...", total=None)
            
            # Import and initialize RAG tool (this will create the vector DB)
            from tools.rag_tools import LegalRAGTool
            rag_tool = LegalRAGTool()
            
            progress.update(task, description="[green]Vector database created!")
        
        console.print("[green]✓ Vector database initialized successfully![/green]\n")
        return True
        
    except Exception as e:
        console.print(f"[red]Error initializing vector database: {e}[/red]\n")
        return False

def create_directory_structure():
    """Create necessary directories"""
    console.print("[bold cyan]Creating directory structure...[/bold cyan]")
    
    directories = [
        'legal_documents',
        'data',
        'outputs',
        'tools',
        'test_cases',
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(exist_ok=True)
            console.print(f"  ✓ Created {directory}/")
        else:
            console.print(f"  ✓ {directory}/")
    
    console.print("[green]Directory structure ready![/green]\n")

def create_sample_case():
    """Create a sample case file for testing"""
    sample_case = """
CASE DETAILS

Petitioner: Rajesh Kumar
Respondent: State of Maharashtra

FACTS:
On 15th January 2024, the petitioner Rajesh Kumar was arrested by the police in Mumbai 
on allegations of theft under Section 379 of the Indian Penal Code. The complainant, 
Mr. Suresh Sharma, alleged that on 10th January 2024, his laptop worth Rs. 50,000 
was stolen from his office premises, and based on CCTV footage, the petitioner was 
identified as the person who took the laptop.

The petitioner denies the allegations and states that he was not present at the 
location on the said date. He claims that he was at his home, which is located 
approximately 20 kilometers away from the scene of the alleged theft. The petitioner 
has filed this petition seeking bail, arguing that:

1. There is no direct evidence linking him to the theft
2. The identification based on CCTV footage is unclear and disputed
3. He has strong ties to the community and is not a flight risk
4. He is willing to cooperate with the investigation

The police oppose the bail application, stating that:
1. The CCTV footage clearly shows the petitioner
2. The petitioner has a previous conviction for a similar offense in 2018
3. There is a risk that the petitioner may tamper with evidence or influence witnesses

LEGAL ISSUES:
1. Whether the petitioner is entitled to bail in the present case?
2. What are the relevant provisions of law governing bail in theft cases?
3. What factors should the court consider while deciding the bail application?

CASE TYPE: Criminal

STATUTES MENTIONED:
- Section 379 IPC (Theft)
- Section 437 CrPC (Bail in non-bailable offenses)
"""
    
    test_cases_dir = Path("test_cases")
    sample_file = test_cases_dir / "sample_bail_case.txt"
    
    if not sample_file.exists():
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_case)
        console.print(f"[green]✓ Created sample case file: {sample_file}[/green]")
    
    return sample_file

def main():
    """Main setup function"""
    console.print("\n")
    console.print("[bold blue]" + "="*80 + "[/bold blue]")
    console.print("[bold blue]AI LEGAL CASE RESEARCHER - SETUP[/bold blue]")
    console.print("[bold blue]" + "="*80 + "[/bold blue]")
    console.print("\n")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Create directory structure
    create_directory_structure()
    
    # Step 3: Check environment
    if not check_environment():
        console.print("\n[yellow]⚠ Setup incomplete. Please configure environment variables.[/yellow]")
        sys.exit(1)
    
    # Step 4: Check legal documents
    if not check_legal_documents():
        console.print("\n[yellow]⚠ Setup incomplete. Please add legal documents.[/yellow]")
        sys.exit(1)
    
    # Step 5: Initialize vector database
    if not initialize_vector_db():
        console.print("\n[yellow]⚠ Setup incomplete. Vector database initialization failed.[/yellow]")
        sys.exit(1)
    
    # Step 6: Create sample case
    sample_file = create_sample_case()
    
    # Success!
    console.print("\n[bold green]" + "="*80 + "[/bold green]")
    console.print("[bold green]✓ SETUP COMPLETE![/bold green]")
    console.print("[bold green]" + "="*80 + "[/bold green]")
    console.print("\n")
    console.print("You can now run the AI Legal Case Researcher:")
    console.print("  [cyan]python main.py[/cyan]")
    console.print("\n")
    console.print(f"A sample case file has been created at: [cyan]{sample_file}[/cyan]")
    console.print("You can use this for testing the system.")
    console.print("\n")

if __name__ == "__main__":
    main()