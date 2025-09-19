import os
import sys
from typing import List, Dict, Any

import streamlit as st
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.llms.mock import MockLLM
from llama_index.core.embeddings import BaseEmbedding
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI components
try:
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_sources.database_handler import DatabaseHandler
from data_sources.document_handler import DocumentHandler


class SimpleEmbedding(BaseEmbedding):
    """Simple embedding that just returns hash-based vectors for demo purposes."""
    
    def _get_query_embedding(self, query: str) -> List[float]:
        import hashlib
        hash_obj = hashlib.md5(query.encode())
        hash_bytes = hash_obj.digest()[:16]
        return [(b / 127.5) - 1.0 for b in hash_bytes]
    
    def _get_text_embedding(self, text: str) -> List[float]:
        return self._get_query_embedding(text)
    
    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)
    
    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)


def initialize_settings():
    """Initialize LlamaIndex settings"""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if OPENAI_AVAILABLE and openai_api_key:
        try:
            # Test OpenAI API key with a simple request
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            Settings.llm = OpenAI(model=model, api_key=openai_api_key)
            Settings.embed_model = OpenAIEmbedding(api_key=openai_api_key)
            return True, "OpenAI"
        except Exception as e:
            # If OpenAI fails (quota exceeded, invalid key, etc.), fall back to mock
            print(f"OpenAI initialization failed: {e}")
            Settings.llm = MockLLM()
            Settings.embed_model = SimpleEmbedding()
            return False, "MockLLM (OpenAI quota exceeded)"
    else:
        # Fall back to mock models
        Settings.llm = MockLLM()
        Settings.embed_model = SimpleEmbedding()
        return False, "MockLLM"


def initialize_data_sources():
    """Initialize database and document handlers"""
    try:
        db_handler = DatabaseHandler()
        st.session_state.db_handler = db_handler
        st.session_state.db_available = True
    except Exception as e:
        st.session_state.db_available = False
        st.session_state.db_error = str(e)
    
    try:
        doc_handler = DocumentHandler()
        st.session_state.doc_handler = doc_handler
        st.session_state.docs_available = True
    except Exception as e:
        st.session_state.docs_available = False
        st.session_state.docs_error = str(e)


def show_data_source_info():
    """Display information about available data sources"""
    st.sidebar.header("📊 Data Sources")
    
    # Database info
    if st.session_state.get('db_available', False):
        with st.sidebar.expander("🗄️ Database (Structured Data)", expanded=False):
            if st.button("Show Database Schema", key="show_schema"):
                table_info = st.session_state.db_handler.get_table_info()
                st.json(table_info)
    else:
        st.sidebar.error(f"❌ Database unavailable: {st.session_state.get('db_error', 'Unknown error')}")
    
    # Documents info
    if st.session_state.get('docs_available', False):
        with st.sidebar.expander("📄 Documents (Unstructured Data)", expanded=False):
            doc_info = st.session_state.doc_handler.get_document_info()
            st.write(f"**Total documents:** {doc_info['total_documents']}")
            st.write("**Categories:**")
            for category, count in doc_info['categories'].items():
                st.write(f"- {category}: {count} documents")
    else:
        st.sidebar.error(f"❌ Documents unavailable: {st.session_state.get('docs_error', 'Unknown error')}")


def show_sample_queries():
    """Display sample queries for both data sources"""
    st.sidebar.header("💡 Sample Queries")
    
    if st.session_state.get('db_available', False):
        with st.sidebar.expander("Database Questions", expanded=False):
            db_samples = st.session_state.db_handler.get_sample_queries()
            for i, query in enumerate(db_samples[:5]):  # Show first 5
                if st.button(query, key=f"db_sample_{i}"):
                    st.session_state.current_query = query
                    st.session_state.query_source = "database"
                    st.rerun()
    
    if st.session_state.get('docs_available', False):
        with st.sidebar.expander("Document Questions", expanded=False):
            doc_samples = st.session_state.doc_handler.get_sample_queries()
            
            for category, queries in doc_samples.items():
                st.write(f"**{category.title()}:**")
                for i, query in enumerate(queries[:3]):  # Show first 3 per category
                    if st.button(query, key=f"doc_sample_{category}_{i}"):
                        st.session_state.current_query = query
                        st.session_state.query_source = "documents"
                        st.session_state.query_category = category
                        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="TechAdvance Solutions - Data Intelligence Platform", 
        page_icon="⚡",
        layout="wide"
    )
    
           # Custom CSS for professional corporate styling
    st.markdown("""
    <style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
    
    /* Updated Color Palette */
    :root {
        --primary-red: #FF462D;
        --dark-red: #E63E29;
        --light-red: #FF6B52;
        --background-cream: #F2F1EE;
        --dark-gray: #2D2D2D;
        --medium-gray: #6B6B6B;
        --light-gray: #E8E7E4;
        --warm-brown: #8D6E63;
        --accent-green: #4CAF50;
        --white: #FFFFFF;
        --text-dark: #1A1A1A;
    }
    
    /* Global font styling and background */
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        background-color: var(--background-cream) !important;
    }
    
    .main .block-container {
        background-color: var(--background-cream);
    }
    
    /* Custom C Logo - Bowl Shape */
    .logo-c {
        display: inline-block;
        width: 60px;
        height: 60px;
        border: 8px solid var(--primary-red);
        border-right: 8px solid transparent;
        border-radius: 50%;
        position: relative;
        margin-right: 15px;
        vertical-align: middle;
        background: linear-gradient(135deg, var(--white) 0%, var(--background-cream) 100%);
        box-shadow: 
            0 6px 20px rgba(255, 70, 45, 0.3),
            inset 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .logo-c::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 30px;
        height: 30px;
        background: linear-gradient(135deg, var(--light-gray) 0%, var(--white) 100%);
        border-radius: 50%;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.2);
    }
    
    .logo-c::after {
        content: '';
        position: absolute;
        top: -4px;
        left: -4px;
        right: -4px;
        bottom: -4px;
        border: 2px solid rgba(255, 70, 45, 0.2);
        border-right: 2px solid transparent;
        border-radius: 50%;
        animation: logoRotate 12s linear infinite;
    }
    
    .logo-c:hover {
        transform: scale(1.05);
        box-shadow: 
            0 8px 25px rgba(255, 70, 45, 0.4),
            inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes logoRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--white) 0%, var(--light-gray) 100%);
        color: var(--text-dark);
        padding: 2.5rem 1rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.1),
            0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 70, 45, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--dark-gray);
        letter-spacing: -0.02em;
        text-shadow: none;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        font-weight: 400;
        color: var(--medium-gray);
        font-family: 'IBM Plex Sans', sans-serif;
        letter-spacing: 0.01em;
    }
    
    /* Enhanced typography */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    
    .stMarkdown p, .stMarkdown div {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Code and monospace elements */
    code, pre, .stCode {
        font-family: 'IBM Plex Mono', monospace;
    }
    
    .metric-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid var(--primary-red);
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid var(--light-gray);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(255, 70, 45, 0.15);
    }
    
    .service-category {
        background: linear-gradient(135deg, var(--white) 0%, var(--light-gray) 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(255, 70, 45, 0.1);
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .service-category:hover {
        border-color: var(--primary-red);
        background: linear-gradient(135deg, var(--white) 0%, #FFF8F6 100%);
        transform: translateX(5px);
        box-shadow: 0 4px 16px rgba(255, 70, 45, 0.1);
    }
    
    .service-category strong {
        color: var(--primary-red);
        font-size: 1.1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #D4D4D4 0%, #B8B8B8 100%);
        color: var(--dark-gray);
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'IBM Plex Sans', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(180, 180, 180, 0.25);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #C8C8C8 0%, #ACACAC 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(172, 172, 172, 0.35);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--background-cream);
    }
    
    /* Success/Info message styling */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid var(--primary-red);
        background-color: var(--white);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid var(--light-gray);
        background-color: var(--white);
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-red);
        box-shadow: 0 0 10px rgba(255, 70, 45, 0.15);
    }
    
    /* Status indicators */
    .status-connected {
        color: var(--accent-green);
        font-weight: bold;
    }
    
    .status-error {
        color: var(--primary-red);
        font-weight: bold;
    }
    
    /* Footer styling */
    .footer-branding {
        text-align: center; 
        color: var(--medium-gray); 
        padding: 2rem;
        background: linear-gradient(135deg, var(--white) 0%, var(--light-gray) 100%);
        border-radius: 15px;
        margin-top: 2rem;
        border-top: 3px solid var(--primary-red);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .footer-branding strong {
        color: var(--primary-red);
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <div class="logo-c"></div>
            <h1 style="margin: 0;">TechAdvance Solutions</h1>
        </div>
        <p>Data Intelligence Platform</p>
        <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.8;">We Deliver Digital Transformation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize settings and data sources
    if "llm_configured" not in st.session_state:
        is_openai, llm_type = initialize_settings()
        st.session_state.llm_configured = True
        st.session_state.is_openai = is_openai
        st.session_state.llm_type = llm_type
    
    # Display LLM status
    if st.session_state.is_openai:
        st.success("🤖 Using OpenAI GPT for intelligent responses")
    else:
        st.info("🔧 Using MockLLM - Add OpenAI API key for enhanced responses")
    
    if 'initialized' not in st.session_state:
        with st.spinner("Loading data sources..."):
            initialize_data_sources()
        st.session_state.initialized = True
    
    # Sidebar with data source info and samples
    show_data_source_info()
    show_sample_queries()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Ask a Question")
        
        # Query input
        query = st.text_input(
            "Your question",
            value=st.session_state.get('current_query', ''),
            placeholder="e.g., 'What is the average salary by department?' or 'What is the vacation policy?'",
            key="main_query"
        )
        
        # Data source selection
        col_db, col_docs = st.columns(2)
        
        with col_db:
            query_database = st.button(
                "🗄️ Query Database", 
                disabled=not st.session_state.get('db_available', False),
                use_container_width=True
            )
        
        with col_docs:
            query_documents = st.button(
                "📄 Query Documents", 
                disabled=not st.session_state.get('docs_available', False),
                use_container_width=True
            )
        
        # Process query
        if query.strip() and (query_database or query_documents):
            with st.spinner("Processing your question..."):
                
                if query_database:
                    st.info("🗄️ Querying structured database...")
                    response = st.session_state.db_handler.query(query)
                    source_type = "Database"
                
                elif query_documents:
                    st.info("📄 Querying unstructured documents...")
                    response = st.session_state.doc_handler.query(query)
                    source_type = "Documents"
                
                # Display response
                st.subheader("📋 Answer")
                st.info(f"**Source:** {source_type}")
                st.markdown(response)
                
                # Clear the current query
                if 'current_query' in st.session_state:
                    del st.session_state.current_query
    
    with col2:
        st.subheader("📊 System Status")
        
        # Status indicators
        if st.session_state.get('db_available', False):
            st.markdown('<p><strong>Database:</strong> <span class="status-connected">✅ Connected</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p><strong>Database:</strong> <span class="status-error">❌ Unavailable</span></p>', unsafe_allow_html=True)
            
        if st.session_state.get('docs_available', False):
            st.markdown('<p><strong>Documents:</strong> <span class="status-connected">✅ Loaded</span></p>', unsafe_allow_html=True)
        else:
            st.markdown('<p><strong>Documents:</strong> <span class="status-error">❌ Unavailable</span></p>', unsafe_allow_html=True)
        
        if st.session_state.get('db_available', False):
            table_info = st.session_state.db_handler.get_table_info()
            total_records = sum(info.get('row_count', 0) for info in table_info.values() if isinstance(info, dict))
            st.write(f"**DB Records:** {total_records:,}")
        
        if st.session_state.get('docs_available', False):
            doc_info = st.session_state.doc_handler.get_document_info()
            st.write(f"**Documents:** {doc_info['total_documents']}")
        
        st.divider()
        
        st.subheader("💡 Tips")
        st.markdown("""
        <div class="service-category">
        <strong>Database queries work well for:</strong><br>
        • Consultant and employee information<br>
        • Service delivery and revenue data<br>
        • Client engagement metrics<br>
        • Financial and operational analytics
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="service-category">
        <strong>Document queries work well for:</strong><br>
        • IT service policies and procedures<br>
        • Security and compliance guidelines<br>
        • Employee handbook and HR policies<br>
        • Consulting methodologies and frameworks
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div class="footer-branding">
        <p>⚡ <strong>TechAdvance Solutions</strong> - We Deliver Digital Transformation</p>
        <p><em>Powered by """ + (st.session_state.llm_type if 'llm_type' in st.session_state else 'MockLLM') + """ for intelligent enterprise data analysis.</em></p>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            🔧 Infrastructure Services | ☁️ Cloud Solutions | 🔒 Security & Resiliency | 🤖 Data & AI Services
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
