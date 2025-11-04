# 🏛️ AI Legal Case Researcher

An intelligent legal research system powered by CrewAI, RAG (Retrieval-Augmented Generation), and Google Gemini that helps analyze legal cases and conduct comprehensive legal research on Indian law.

## 🎯 Features

- **Automated Case Analysis**: Extracts parties, facts, and legal issues from case documents
- **Comprehensive Statutory Research**: Searches through Constitution, IPC, CrPC, CPC, Evidence Act, Contract Act, Property Act, Companies Act
- **Precedent Search**: Finds relevant case law and judgments (with Indian Kanoon integration)
- **Legal Reasoning**: Provides detailed legal analysis connecting facts, statutes, and precedents
- **Professional Reports**: Generates well-structured legal research reports in markdown format
- **RAG Technology**: Uses vector database for efficient retrieval of relevant legal provisions
- **Multi-Agent System**: Specialized AI agents work together for thorough research

## 🏗️ System Architecture

### Agent Hierarchy
1. **Legal Research Manager** - Orchestrates the entire research process
2. **Case Analyst** - Analyzes case facts and identifies legal issues
3. **Statute Researcher** - Finds relevant statutory provisions using RAG
4. **Precedent Researcher** - Searches for applicable case law
5. **Legal Drafter** - Compiles comprehensive research reports
6. **Quality Reviewer** - Reviews final output for accuracy and completeness

### Technology Stack
- **CrewAI**: Multi-agent orchestration framework
- **LangChain**: LLM integration and document processing
- **ChromaDB**: Vector database for legal documents
- **Sentence Transformers**: Document embeddings
- **Google Gemini 2.0 Flash**: LLM for legal analysis
- **Rich**: Beautiful terminal output
- **Pydantic**: Data validation and type safety

## 📋 Prerequisites

- Python 3.10 or higher
- Google API Key (for Gemini)
- Legal documents in .txt format (see below)
- 4GB+ RAM recommended
- Internet connection for web search features

## 🚀 Installation

### Step 1: Clone/Download the Project

```bash
# Create project directory
mkdir ai-legal-researcher
cd ai-legal-researcher
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_api_key_here
```

### Step 5: Prepare Legal Documents

Place your legal document .txt files in the `legal_documents/` directory:

```
legal_documents/
├── constitution.txt
├── IPC.txt
├── the_code_of_criminal_procedure._1973.txt
├── the_code_of_civil_procedure._1908.txt
├── iea_1872.txt
├── ica_1872.txt
├── the_transfer_of_property_act_1872.txt
└── the_companies_act_2013.txt
```

**Important**: Ensure files are in UTF-8 encoded plain text format with index/contents pages removed.

### Step 6: Run Setup

```bash
python setup.py
```

This will:
- Check all dependencies
- Verify environment configuration
- Check legal documents
- Create vector database (may take 5-10 minutes)
- Create sample test case

## 💻 Usage

### Basic Usage

```bash
python main.py
```

Follow the interactive prompts to:
1. Load case from file or enter manually
2. Specify case type
3. Add specific legal questions (optional)
4. Choose research mode (Full or Quick)
5. Review results and save report

### Research Modes

**Full Research Mode** (~5-10 minutes)
- Complete case analysis
- Exhaustive statutory research
- Precedent search
- Quality review
- Best for: Important cases requiring thorough analysis

**Quick Research Mode** (~2-3 minutes)
- Case analysis
- Statutory research only
- No precedent search or quality review
- Best for: Quick preliminary analysis

### Example: Using Sample Case

```bash
python main.py

# When prompted:
# - Load from file: Yes
# - File path: test_cases/sample_bail_case.txt
# - Case type: criminal
# - Research mode: 1 (Full Research)
```

## 📁 Project Structure

```
ai-legal-researcher/
│
├── main.py                  # Main application entry point
├── setup.py                 # Setup and initialization script
├── config.py                # Configuration and data models
├── agents.py                # CrewAI agent definitions
├── tasks.py                 # CrewAI task definitions
├── crew.py                  # Crew orchestration logic
│
├── tools/
│   ├── rag_tools.py         # RAG and vector DB tools
│   ├── web_tools.py         # Web search and Indian Kanoon tools
│   └── analysis_tools.py    # Case analysis and extraction tools
│
├── legal_documents/         # Legal statutes (.txt files)
│   ├── constitution.txt
│   ├── IPC.txt
│   └── ...
│
├── data/
│   └── chroma_db/           # Vector database (auto-generated)
│
├── outputs/                 # Generated research reports
│   └── legal_research_report_YYYYMMDD_HHMMSS.md
│
├── test_cases/              # Sample test cases
│   └── sample_bail_case.txt
│
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment template
└── README.md                # This file
```

## 🔧 Configuration

### Modifying Settings

Edit `config.py` to customize:

```python
# LLM Configuration
LLM_MODEL = "gemini/gemini-2.0-flash-exp"
LLM_TEMPERATURE = 0.3

# Vector Store Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 10

# CrewAI Configuration
MAX_ITER = 25
VERBOSE = True
```

### Adding More Legal Documents

1. Convert PDF to .txt (UTF-8 encoding)
2. Remove index/contents pages
3. Place in `legal_documents/` directory
4. Add to `LegalDocument` enum in `config.py`
5. Rebuild vector database: `python setup.py`

## 📊 Output Format

The system generates comprehensive legal research reports with:

1. **Executive Summary** - Key findings at a glance
2. **Case Overview** - Parties, facts, and issues
3. **Applicable Statutory Framework** - All relevant provisions with explanations
4. **Relevant Precedents** - Case law with summaries and applications
5. **Legal Analysis** - Detailed reasoning and arguments
6. **Legal Opinion** - Assessment of merits and likelihood of success
7. **Recommendations** - Practical next steps and strategy
8. **Research Confidence** - Limitations and caveats

Reports are saved as markdown files in the `outputs/` directory.

## 🔍 Advanced Features

### Custom Agents

You can add specialized agents in `agents.py`:

```python
def constitutional_expert(self):
    return Agent(
        role="Constitutional Law Expert",
        backstory="...",
        goal="...",
        tools=[...],
        llm=self.llm
    )
```

### Custom Tools

Create custom tools in the `tools/` directory:

```python
class CustomLegalTool(BaseTool):
    name: str = "Tool Name"
    description: str = "Tool description"
    
    def _run(self, query: str) -> str:
        # Tool logic
        return result
```

### Integration with Indian Kanoon

For better precedent search, you can:
1. Get Indian Kanoon API access
2. Add API key to `.env`
3. Implement API calls in `tools/web_tools.py`

### Web Scraping for Precedents

Add Serper API key to `.env` for web search:
```
SERPER_API_KEY=your_key_here
```

## 🐛 Troubleshooting

### Vector Database Issues

```bash
# Delete and rebuild
rm -rf data/chroma_db
python setup.py
```

### Memory Issues

Reduce chunk processing:
```python
# In config.py
TOP_K_RESULTS = 5  # Reduce from 10
CHUNK_SIZE = 500   # Reduce from 1000
```

### API Rate Limits

```python
# In crew.py
max_rpm=5  # Reduce from 10
```

### Encoding Issues

Ensure all text files are UTF-8:
```bash
file -bi legal_documents/*.txt
# Should show: charset=utf-8
```

## 📝 Best Practices

1. **Case Input**: Provide clear, well-structured case facts
2. **Specific Queries**: Add specific legal questions for focused research
3. **Document Quality**: Ensure legal documents are clean and properly formatted
4. **Review Output**: Always verify AI-generated legal analysis with qualified professionals
5. **Iterative Refinement**: Use quick mode first, then full mode for important cases

## ⚠️ Limitations

- AI-generated analysis should be verified by legal professionals
- Precedent search currently limited (integrate Indian Kanoon API for better results)
- No OCR support yet (input must be text)
- Requires good quality legal document preparation
- Performance depends on LLM API availability and rate limits

## 🔮 Future Enhancements

- [ ] OCR integration for PDF/image input
- [ ] Indian Kanoon API integration
- [ ] Case law vector database
- [ ] Multi-language support
- [ ] Web interface
- [ ] Citation extraction and verification
- [ ] Automated legal opinion generation
- [ ] Integration with case management systems

## 📄 License

This project is for educational and research purposes. Always consult qualified legal professionals for legal advice.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Better precedent search integration
- Additional legal document support
- Improved entity extraction
- Enhanced analysis algorithms
- UI/UX improvements

## 📞 Support

For issues and questions:
1. Check this README
2. Review configuration in `config.py`
3. Check error messages and logs
4. Ensure API keys are correctly set

## 🙏 Acknowledgments

- CrewAI for the multi-agent framework
- LangChain for LLM integration
- Indian Kanoon for legal database inspiration
- Open-source community

---

**Disclaimer**: This is an AI-powered research tool. It does not provide legal advice. Always consult qualified legal professionals for legal matters.