"""
RAG Tools for Legal Document Retrieval
"""
import os
from typing import List, Optional
from crewai.tools import BaseTool
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import settings, LegalDocument
import chromadb
from chromadb.config import Settings as ChromaSettings

class LegalRAGTool(BaseTool):
    """
    RAG tool for retrieving relevant legal provisions from statutes
    """
    name: str = "Legal Document Retriever"
    description: str = (
        "Retrieves relevant legal provisions, sections, and articles from "
        "Indian legal documents including Constitution, IPC, CrPC, CPC, Evidence Act, "
        "Contract Act, Transfer of Property Act, and Companies Act. "
        "Use this tool when you need to find specific legal provisions, "
        "sections, or articles relevant to a legal issue."
    )
    
    # Declare instance variables for Pydantic
    vector_store: Optional[object] = None
    embeddings: Optional[object] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_rag()
    
    def _initialize_rag(self):
        """Initialize or load the vector database"""
        try:
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'}
            )
            
            # Check if vector DB already exists
            if os.path.exists(settings.VECTOR_DB_PATH):
                print("Loading existing vector database...")
                self.vector_store = Chroma(
                    persist_directory=settings.VECTOR_DB_PATH,
                    embedding_function=self.embeddings
                )
            else:
                print("Creating new vector database from legal documents...")
                self._create_vector_db()
                
        except Exception as e:
            print(f"Error initializing RAG: {e}")
            raise
    
    def _create_vector_db(self):
        """Create vector database from legal documents"""
        all_documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        
        # Load all legal documents
        for legal_doc in LegalDocument:
            file_path = os.path.join(settings.LEGAL_DOCS_PATH, legal_doc.value)
            if os.path.exists(file_path):
                print(f"Processing {legal_doc.value}...")
                try:
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents = loader.load()
                    
                    # Add metadata
                    for doc in documents:
                        doc.metadata['source_document'] = legal_doc.name
                        doc.metadata['file_name'] = legal_doc.value
                    
                    # Split documents
                    splits = text_splitter.split_documents(documents)
                    all_documents.extend(splits)
                    print(f"  Added {len(splits)} chunks from {legal_doc.value}")
                except Exception as e:
                    print(f"  Error processing {file_path}: {e}")
            else:
                print(f"  Warning: {file_path} not found")
        
        if not all_documents:
            raise ValueError("No documents were loaded. Please check the legal_documents directory.")
        
        # Create vector store
        print(f"\nCreating vector database with {len(all_documents)} chunks...")
        self.vector_store = Chroma.from_documents(
            documents=all_documents,
            embedding=self.embeddings,
            persist_directory=settings.VECTOR_DB_PATH
        )
        self.vector_store.persist()
        print("Vector database created successfully!")
    
    def _run(self, query: str, top_k: int = None) -> str:
        """
        Retrieve relevant legal provisions
        
        Args:
            query: Legal query or issue description
            top_k: Number of results to return (default from settings)
        
        Returns:
            Formatted string of relevant legal provisions
        """
        if not self.vector_store:
            return "Error: Vector store not initialized"
        
        try:
            k = top_k if top_k else settings.TOP_K_RESULTS
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            if not results:
                return "No relevant legal provisions found for the query."
            
            formatted_results = []
            for i, (doc, score) in enumerate(results, 1):
                source = doc.metadata.get('source_document', 'Unknown')
                content = doc.page_content.strip()
                
                formatted_results.append(
                    f"\n{'='*80}\n"
                    f"RESULT {i} (Relevance Score: {1-score:.3f})\n"
                    f"Source: {source}\n"
                    f"{'='*80}\n"
                    f"{content}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error during retrieval: {str(e)}"

class StatuteSearchTool(BaseTool):
    """
    Tool for searching specific statutes by keywords
    """
    name: str = "Statute Keyword Search"
    description: str = (
        "Search for specific sections, articles, or provisions in legal statutes "
        "using keywords like 'Section 302 IPC', 'Article 21', 'Section 138 NI Act', etc. "
        "Use this when you need to find exact statute references."
    )
    
    rag_tool: Optional[object] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rag_tool = LegalRAGTool()
    
    def _run(self, statute_reference: str) -> str:
        """
        Search for specific statute
        
        Args:
            statute_reference: Reference like "Section 302 IPC" or "Article 21"
        
        Returns:
            The relevant statute text
        """
        try:
            # Use RAG tool with more focused search
            results = self.rag_tool._run(statute_reference, top_k=5)
            return results
        except Exception as e:
            return f"Error searching for statute: {str(e)}"

class PrecedentSearchTool(BaseTool):
    """
    Tool for searching legal precedents (to be implemented with external API)
    """
    name: str = "Legal Precedent Search"
    description: str = (
        "Search for relevant case law and legal precedents from Indian courts. "
        "Useful for finding similar cases and judicial interpretations. "
        "Note: This currently uses web search; integrate with Indian Kanoon API for better results."
    )
    
    def _run(self, query: str) -> str:
        """
        Search for precedents
        
        Args:
            query: Description of the legal issue
        
        Returns:
            Information about relevant precedents
        """
        try:
            # Placeholder for Indian Kanoon API integration
            # For now, provide guidance on what precedents might be relevant
            return (
                f"Precedent Search Query: {query}\n\n"
                "Note: To get actual precedents, integrate with Indian Kanoon API "
                "or use web scraping tools. For now, focus on statutory analysis.\n\n"
                "Suggested precedent search areas:\n"
                "1. Supreme Court judgments on similar issues\n"
                "2. High Court decisions in the relevant jurisdiction\n"
                "3. Landmark cases that interpret relevant statutes\n"
            )
        except Exception as e:
            return f"Error searching precedents: {str(e)}"