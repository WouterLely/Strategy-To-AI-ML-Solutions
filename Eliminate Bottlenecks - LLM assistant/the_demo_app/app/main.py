import os
from typing import List

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


class SimpleEmbedding(BaseEmbedding):
    """Simple embedding that just returns hash-based vectors for demo purposes."""
    
    def _get_query_embedding(self, query: str) -> List[float]:
        # Simple hash-based embedding for demo
        import hashlib
        hash_obj = hashlib.md5(query.encode())
        # Convert hash to list of floats between -1 and 1
        hash_bytes = hash_obj.digest()[:16]  # Use first 16 bytes for 128-dim vector
        return [(b / 127.5) - 1.0 for b in hash_bytes]
    
    def _get_text_embedding(self, text: str) -> List[float]:
        return self._get_query_embedding(text)
    
    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)
    
    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)


def configure_llm_settings():
    """Configure LLM and embedding settings based on available API keys."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if OPENAI_AVAILABLE and openai_api_key:
        try:
            # Use OpenAI if API key is available and valid
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

def build_index_from_texts(texts: List[str]) -> VectorStoreIndex:
    documents = [Document(text=t) for t in texts if t.strip()]
    if not documents:
        documents = [Document(text="This is a placeholder document for the demo.")]
    return VectorStoreIndex.from_documents(documents)


def main() -> None:
    st.set_page_config(page_title="TechAdvance Solutions - Demo Platform", page_icon="⚡")
    
    # Updated styling with cream background
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
    
    :root {
        --primary-red: #FF462D;
        --dark-red: #E63E29;
        --background-cream: #F2F1EE;
        --dark-gray: #2D2D2D;
        --medium-gray: #6B6B6B;
        --light-gray: #E8E7E4;
        --white: #FFFFFF;
        --text-dark: #1A1A1A;
    }
    
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        background-color: var(--background-cream) !important;
    }
    
    .main .block-container {
        background-color: var(--background-cream);
    }
    
    .logo-c {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 6px solid var(--primary-red);
        border-right: 6px solid transparent;
        border-radius: 50%;
        position: relative;
        margin-right: 15px;
        vertical-align: middle;
        background: linear-gradient(135deg, var(--white) 0%, var(--background-cream) 100%);
        box-shadow: 
            0 4px 15px rgba(255, 70, 45, 0.3),
            inset 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .logo-c::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 24px;
        height: 24px;
        background: linear-gradient(135deg, var(--light-gray) 0%, var(--white) 100%);
        border-radius: 50%;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .logo-c:hover {
        transform: scale(1.05);
        box-shadow: 
            0 6px 20px rgba(255, 70, 45, 0.4),
            inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--white) 0%, var(--light-gray) 100%);
        color: var(--text-dark);
        padding: 2rem 1rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.1),
            0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 70, 45, 0.1);
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    .main-header h1 {
        font-weight: 600;
        letter-spacing: -0.02em;
        margin: 0;
        color: var(--dark-gray);
    }
    
    .main-header p {
        font-weight: 400;
        letter-spacing: 0.01em;
        margin: 0.5rem 0 0 0;
        color: var(--medium-gray);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #D4D4D4 0%, #B8B8B8 100%);
        color: var(--dark-gray);
        border: none;
        border-radius: 10px;
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
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: var(--dark-gray);
    }
    
    .stMarkdown p, .stMarkdown div {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 400;
        line-height: 1.6;
        color: var(--text-dark);
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid var(--light-gray);
        background-color: var(--white);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-red);
        box-shadow: 0 0 10px rgba(255, 70, 45, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <div class="logo-c"></div>
            <h1 style="margin: 0;">TechAdvance Solutions</h1>
        </div>
        <p>Demo Platform</p>
        <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.8;">Advanced Data Intelligence & Document Intelligence & Knowledge Management</p>
    </div>
    """, unsafe_allow_html=True)

    # Configure LLM settings
    if "llm_configured" not in st.session_state:
        is_openai, llm_type = configure_llm_settings()
        st.session_state.llm_configured = True
        st.session_state.is_openai = is_openai
        st.session_state.llm_type = llm_type

    # Display LLM status
    if st.session_state.is_openai:
        st.success("🤖 Using OpenAI GPT for intelligent responses")
    else:
        st.info("🔧 Using MockLLM - Add OpenAI API key for enhanced responses")

    if "index" not in st.session_state:
        st.session_state.index = build_index_from_texts(["Welcome to the TechAdvance Solutions demo platform."])

    with st.sidebar:
        st.header("Corpus")
        default_text = st.text_area(
            "Enter some context text",
            value="LlamaIndex helps you build LLM apps with your data.",
            height=120,
        )
        uploaded = st.file_uploader("Or upload a .txt file", type=["txt"])
        corpus_texts: List[str] = [default_text]
        if uploaded is not None:
            try:
                corpus_texts.append(uploaded.read().decode("utf-8", errors="ignore"))
            except Exception:
                st.warning("Could not read uploaded file; using default text only.")
        if st.button("Rebuild Index"):
            st.session_state.index = build_index_from_texts(corpus_texts)
            st.success("Index rebuilt.")

    st.subheader("Ask a question")
    query = st.text_input("Your question", placeholder="What is LlamaIndex?")
    if st.button("Query") and query.strip():
        query_engine = st.session_state.index.as_query_engine()
        response = query_engine.query(query)
        st.markdown("**Answer**")
        st.write(str(response))

    st.divider()
    st.markdown("""
    <div style="text-align: center; color: var(--medium-gray); padding: 2rem; background: linear-gradient(135deg, var(--white) 0%, var(--light-gray) 100%); border-radius: 15px; border-top: 3px solid var(--primary-red); box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);">
        <p>⚡ <strong style="color: var(--primary-red);">TechAdvance Solutions</strong> - We Deliver Digital Transformation</p>
        <p><em>Tip: In production, connect to enterprise LLM services for enhanced intelligence.</em></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()



