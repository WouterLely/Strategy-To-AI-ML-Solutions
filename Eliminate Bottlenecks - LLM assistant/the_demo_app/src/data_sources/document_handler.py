<<<<<<< HEAD
"""
Document handler for unstructured data using LlamaIndex
"""
import os
import glob
from typing import List, Dict, Any
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.readers.file import MarkdownReader
from pathlib import Path


class DocumentHandler:
    """Handles unstructured document queries using LlamaIndex"""
    
    def __init__(self, documents_path: str = "data/documents"):
        self.documents_path = documents_path
        self.index = None
        self.documents = []
        self._load_documents()
    
    def _load_documents(self):
        """Load all markdown documents from the documents directory"""
        if not os.path.exists(self.documents_path):
            raise FileNotFoundError(f"Documents directory not found at {self.documents_path}")
        
        # Find all markdown files recursively
        markdown_files = []
        for root, dirs, files in os.walk(self.documents_path):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        
        if not markdown_files:
            # Create some default documents if none exist
            self.documents = [Document(text="No documents found. Please add some markdown files to the documents directory.")]
        else:
            # Load documents using MarkdownReader
            reader = MarkdownReader()
            self.documents = []
            
            for file_path in markdown_files:
                try:
                    # Read the file
                    docs = reader.load_data(file=Path(file_path))
                    
                    # Add metadata about the source
                    for doc in docs:
                        # Extract category from path (hr, sales, policies, etc.)
                        relative_path = os.path.relpath(file_path, self.documents_path)
                        category = os.path.dirname(relative_path)
                        filename = os.path.basename(file_path)
                        
                        doc.metadata = {
                            "source": file_path,
                            "category": category,
                            "filename": filename,
                            "relative_path": relative_path
                        }
                        
                        self.documents.append(doc)
                        
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
                    # Add a document with error info
                    error_doc = Document(
                        text=f"Error loading document {file_path}: {str(e)}",
                        metadata={"source": file_path, "error": True}
                    )
                    self.documents.append(error_doc)
        
        # Create index from documents
        self._create_index()
    
    def _create_index(self):
        """Create a vector store index from the loaded documents"""
        if self.documents:
            self.index = VectorStoreIndex.from_documents(self.documents)
        else:
            # Create empty index with placeholder
            placeholder = Document(text="No documents available.")
            self.index = VectorStoreIndex.from_documents([placeholder])
    
    def query(self, question: str) -> str:
        """Query the document index using natural language"""
        try:
            if not self.index:
                return "No documents loaded. Please check the documents directory."
            
            query_engine = self.index.as_query_engine()
            response = query_engine.query(question)
            return str(response)
        
        except Exception as e:
            return f"Error querying documents: {str(e)}"
    
    def get_document_info(self) -> Dict[str, Any]:
        """Get information about loaded documents"""
        info = {
            "total_documents": len(self.documents),
            "categories": {},
            "files": []
        }
        
        for doc in self.documents:
            metadata = doc.metadata or {}
            
            # Count by category
            category = metadata.get("category", "unknown")
            if category not in info["categories"]:
                info["categories"][category] = 0
            info["categories"][category] += 1
            
            # Add file info
            if not metadata.get("error", False):
                info["files"].append({
                    "filename": metadata.get("filename", "unknown"),
                    "category": category,
                    "path": metadata.get("relative_path", "unknown"),
                    "length": len(doc.text)
                })
        
        return info
    
    def search_by_category(self, category: str, question: str) -> str:
        """Search within a specific category of documents"""
        try:
            # Filter documents by category
            category_docs = [
                doc for doc in self.documents 
                if doc.metadata and doc.metadata.get("category") == category
            ]
            
            if not category_docs:
                return f"No documents found in category '{category}'"
            
            # Create temporary index for this category
            category_index = VectorStoreIndex.from_documents(category_docs)
            query_engine = category_index.as_query_engine()
            response = query_engine.query(question)
            
            return str(response)
        
        except Exception as e:
            return f"Error searching category '{category}': {str(e)}"
    
    def get_sample_queries(self) -> Dict[str, List[str]]:
        """Return sample queries organized by category"""
        return {
            "hr": [
                "What is the company's vacation policy?",
                "How does the performance review process work?",
                "What are the salary ranges for different positions?",
                "What benefits does the company offer?",
                "How do I request time off?"
            ],
            "sales": [
                "What is the sales process for enterprise customers?",
                "How is sales commission calculated?",
                "What are the target customer profiles?",
                "How should I handle price objections?",
                "What tools are available for sales teams?"
            ],
            "policies": [
                "What are the information security requirements?",
                "How should I handle confidential data?",
                "What is the incident response process?",
                "What are the access control requirements?",
                "How often are security audits conducted?"
            ],
            "general": [
                "What are the company's core values?",
                "How do I report a security incident?",
                "What training opportunities are available?",
                "How does the referral program work?",
                "What is the company's mission?"
            ]
        }
    
    def reload_documents(self):
        """Reload all documents from the file system"""
        self.documents = []
        self._load_documents()
=======
"""
Document handler for unstructured data using LlamaIndex
"""
import os
import glob
from typing import List, Dict, Any
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.readers.file import MarkdownReader
from pathlib import Path


class DocumentHandler:
    """Handles unstructured document queries using LlamaIndex"""
    
    def __init__(self, documents_path: str = "data/documents"):
        self.documents_path = documents_path
        self.index = None
        self.documents = []
        self._load_documents()
    
    def _load_documents(self):
        """Load all markdown documents from the documents directory"""
        if not os.path.exists(self.documents_path):
            raise FileNotFoundError(f"Documents directory not found at {self.documents_path}")
        
        # Find all markdown files recursively
        markdown_files = []
        for root, dirs, files in os.walk(self.documents_path):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        
        if not markdown_files:
            # Create some default documents if none exist
            self.documents = [Document(text="No documents found. Please add some markdown files to the documents directory.")]
        else:
            # Load documents using MarkdownReader
            reader = MarkdownReader()
            self.documents = []
            
            for file_path in markdown_files:
                try:
                    # Read the file
                    docs = reader.load_data(file=Path(file_path))
                    
                    # Add metadata about the source
                    for doc in docs:
                        # Extract category from path (hr, sales, policies, etc.)
                        relative_path = os.path.relpath(file_path, self.documents_path)
                        category = os.path.dirname(relative_path)
                        filename = os.path.basename(file_path)
                        
                        doc.metadata = {
                            "source": file_path,
                            "category": category,
                            "filename": filename,
                            "relative_path": relative_path
                        }
                        
                        self.documents.append(doc)
                        
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
                    # Add a document with error info
                    error_doc = Document(
                        text=f"Error loading document {file_path}: {str(e)}",
                        metadata={"source": file_path, "error": True}
                    )
                    self.documents.append(error_doc)
        
        # Create index from documents
        self._create_index()
    
    def _create_index(self):
        """Create a vector store index from the loaded documents"""
        if self.documents:
            self.index = VectorStoreIndex.from_documents(self.documents)
        else:
            # Create empty index with placeholder
            placeholder = Document(text="No documents available.")
            self.index = VectorStoreIndex.from_documents([placeholder])
    
    def query(self, question: str) -> str:
        """Query the document index using natural language"""
        try:
            if not self.index:
                return "No documents loaded. Please check the documents directory."
            
            query_engine = self.index.as_query_engine()
            response = query_engine.query(question)
            return str(response)
        
        except Exception as e:
            return f"Error querying documents: {str(e)}"
    
    def get_document_info(self) -> Dict[str, Any]:
        """Get information about loaded documents"""
        info = {
            "total_documents": len(self.documents),
            "categories": {},
            "files": []
        }
        
        for doc in self.documents:
            metadata = doc.metadata or {}
            
            # Count by category
            category = metadata.get("category", "unknown")
            if category not in info["categories"]:
                info["categories"][category] = 0
            info["categories"][category] += 1
            
            # Add file info
            if not metadata.get("error", False):
                info["files"].append({
                    "filename": metadata.get("filename", "unknown"),
                    "category": category,
                    "path": metadata.get("relative_path", "unknown"),
                    "length": len(doc.text)
                })
        
        return info
    
    def search_by_category(self, category: str, question: str) -> str:
        """Search within a specific category of documents"""
        try:
            # Filter documents by category
            category_docs = [
                doc for doc in self.documents 
                if doc.metadata and doc.metadata.get("category") == category
            ]
            
            if not category_docs:
                return f"No documents found in category '{category}'"
            
            # Create temporary index for this category
            category_index = VectorStoreIndex.from_documents(category_docs)
            query_engine = category_index.as_query_engine()
            response = query_engine.query(question)
            
            return str(response)
        
        except Exception as e:
            return f"Error searching category '{category}': {str(e)}"
    
    def get_sample_queries(self) -> Dict[str, List[str]]:
        """Return sample queries organized by category"""
        return {
            "hr": [
                "What is the company's vacation policy?",
                "How does the performance review process work?",
                "What are the salary ranges for different positions?",
                "What benefits does the company offer?",
                "How do I request time off?"
            ],
            "sales": [
                "What is the sales process for enterprise customers?",
                "How is sales commission calculated?",
                "What are the target customer profiles?",
                "How should I handle price objections?",
                "What tools are available for sales teams?"
            ],
            "policies": [
                "What are the information security requirements?",
                "How should I handle confidential data?",
                "What is the incident response process?",
                "What are the access control requirements?",
                "How often are security audits conducted?"
            ],
            "general": [
                "What are the company's core values?",
                "How do I report a security incident?",
                "What training opportunities are available?",
                "How does the referral program work?",
                "What is the company's mission?"
            ]
        }
    
    def reload_documents(self):
        """Reload all documents from the file system"""
        self.documents = []
        self._load_documents()
>>>>>>> 90fd3198baf6326b2fee62bdd5459fd732dfde2c
