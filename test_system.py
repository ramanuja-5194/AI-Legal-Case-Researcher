"""
Test script to verify the AI Legal Case Researcher is working correctly
"""
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def test_imports():
    """Test if all required modules can be imported"""
    console.print("\n[bold cyan]Testing Imports...[/bold cyan]")
    
    tests = {
        "CrewAI": "crewai",
        "LangChain": "langchain",
        "ChromaDB": "chromadb",
        "Sentence Transformers": "sentence_transformers",
        "Google GenAI": "langchain_google_genai",
        "Pydantic": "pydantic",
        "Rich": "rich",
        "Dotenv": "dotenv",
    }
    
    all_passed = True
    for name, module in tests.items():
        try:
            __import__(module.replace('-', '_'))
            console.print(f"  ✓ {name}")
        except ImportError:
            console.print(f"  ✗ {name} [red]FAILED[/red]")
            all_passed = False
    
    return all_passed

def test_environment():
    """Test environment configuration"""
    console.print("\n[bold cyan]Testing Environment...[/bold cyan]")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    tests_passed = 0
    tests_total = 2
    
    # Test API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key and len(api_key) > 10:
        console.print(f"  ✓ GOOGLE_API_KEY configured")
        tests_passed += 1
    else:
        console.print(f"  ✗ GOOGLE_API_KEY [red]not configured[/red]")
    
    # Test .env file exists
    if Path('.env').exists():
        console.print(f"  ✓ .env file exists")
        tests_passed += 1
    else:
        console.print(f"  ✗ .env file [red]not found[/red]")
    
    return tests_passed == tests_total

def test_project_structure():
    """Test if all necessary files and directories exist"""
    console.print("\n[bold cyan]Testing Project Structure...[/bold cyan]")
    
    required_files = [
        'main.py',
        'config.py',
        'agents.py',
        'tasks.py',
        'crew.py',
        'setup.py',
        'requirements.txt',
    ]
    
    required_dirs = [
        'tools',
        'legal_documents',
    ]
    
    all_passed = True
    
    for file in required_files:
        if Path(file).exists():
            console.print(f"  ✓ {file}")
        else:
            console.print(f"  ✗ {file} [red]missing[/red]")
            all_passed = False
    
    for directory in required_dirs:
        if Path(directory).exists():
            console.print(f"  ✓ {directory}/")
        else:
            console.print(f"  ✗ {directory}/ [red]missing[/red]")
            all_passed = False
    
    return all_passed

def test_tools():
    """Test if tools can be imported"""
    console.print("\n[bold cyan]Testing Tools...[/bold cyan]")
    
    try:
        from tools.rag_tools import LegalRAGTool
        console.print(f"  ✓ RAG tools")
    except Exception as e:
        console.print(f"  ✗ RAG tools [red]FAILED: {e}[/red]")
        return False
    
    try:
        from tools.web_tools import IndianKanoonSearchTool
        console.print(f"  ✓ Web tools")
    except Exception as e:
        console.print(f"  ✗ Web tools [red]FAILED: {e}[/red]")
        return False
    
    try:
        from tools.analysis_tools import LegalEntityExtractorTool
        console.print(f"  ✓ Analysis tools")
    except Exception as e:
        console.print(f"  ✗ Analysis tools [red]FAILED: {e}[/red]")
        return False
    
    return True

def test_config():
    """Test if configuration loads correctly"""
    console.print("\n[bold cyan]Testing Configuration...[/bold cyan]")
    
    try:
        from config import CaseInput, CaseType, settings
        console.print(f"  ✓ Config module loads")
        
        # Test creating a CaseInput
        test_input = CaseInput(
            case_text="Test case text",
            case_type=CaseType.CRIMINAL
        )
        console.print(f"  ✓ CaseInput model works")
        
        # Test settings
        assert settings.LLM_MODEL
        console.print(f"  ✓ Settings configured (LLM: {settings.LLM_MODEL})")
        
        return True
    except Exception as e:
        console.print(f"  ✗ Configuration [red]FAILED: {e}[/red]")
        return False

def test_agents_and_tasks():
    """Test if agents and tasks can be created"""
    console.print("\n[bold cyan]Testing Agents & Tasks...[/bold cyan]")
    
    try:
        from agents import LegalResearchAgents
        agents = LegalResearchAgents()
        console.print(f"  ✓ Agents module loads")
        
        # Try creating an agent
        agent = agents.case_analyst()
        console.print(f"  ✓ Can create agents")
        
        from tasks import LegalResearchTasks
        tasks = LegalResearchTasks()
        console.print(f"  ✓ Tasks module loads")
        
        return True
    except Exception as e:
        console.print(f"  ✗ Agents/Tasks [red]FAILED: {e}[/red]")
        return False

def test_legal_documents():
    """Test if legal documents are present"""
    console.print("\n[bold cyan]Testing Legal Documents...[/bold cyan]")
    
    legal_docs_path = Path('legal_documents')
    
    if not legal_docs_path.exists():
        console.print(f"  ✗ legal_documents/ directory [red]not found[/red]")
        return False
    
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
    
    found = 0
    for doc in required_docs:
        if (legal_docs_path / doc).exists():
            found += 1
    
    console.print(f"  Found {found}/{len(required_docs)} legal documents")
    
    if found == len(required_docs):
        console.print(f"  ✓ All legal documents present")
        return True
    else:
        console.print(f"  ⚠ Some documents missing")
        return False

def test_vector_database():
    """Test if vector database exists"""
    console.print("\n[bold cyan]Testing Vector Database...[/bold cyan]")
    
    vector_db_path = Path('data/chroma_db')
    
    if vector_db_path.exists():
        console.print(f"  ✓ Vector database exists at {vector_db_path}")
        return True
    else:
        console.print(f"  ✗ Vector database [yellow]not initialized[/yellow]")
        console.print(f"     Run: python setup.py")
        return False

def run_all_tests():
    """Run all tests and display results"""
    console.print(Panel.fit(
        "[bold cyan]AI Legal Case Researcher - System Test[/bold cyan]",
        border_style="cyan"
    ))
    
    results = {}
    
    # Run tests
    results['imports'] = test_imports()
    results['environment'] = test_environment()
    results['structure'] = test_project_structure()
    results['tools'] = test_tools()
    results['config'] = test_config()
    results['agents'] = test_agents_and_tasks()
    results['documents'] = test_legal_documents()
    results['vector_db'] = test_vector_database()
    
    # Summary
    console.print("\n" + "="*80)
    console.print("[bold]TEST SUMMARY[/bold]")
    console.print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[green]✓ PASS[/green]" if result else "[red]✗ FAIL[/red]"
        console.print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    console.print(f"\n[bold]Result: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("\n[bold green]✓ All tests passed! System is ready to use.[/bold green]")
        console.print("\nRun: [cyan]python main.py[/cyan]")
        return True
    else:
        console.print("\n[bold yellow]⚠ Some tests failed. Please check the issues above.[/bold yellow]")
        
        if not results['vector_db']:
            console.print("\n[yellow]Tip: Run 'python setup.py' to initialize the vector database[/yellow]")
        
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        console.print(f"\n[red]Test error: {e}[/red]")
        import traceback
        console.print("[dim]" + traceback.format_exc() + "[/dim]")
        sys.exit(1)