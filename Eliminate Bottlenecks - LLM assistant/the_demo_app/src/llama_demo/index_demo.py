from typing import List

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.llms.mock import MockLLM
from llama_index.core.embeddings import BaseEmbedding


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


def create_index(texts: List[str]) -> VectorStoreIndex:
    """Create a VectorStoreIndex from raw text snippets using mock models.

    Uses MockLLM and simple hash-based embeddings (no API keys or heavy deps required).
    Swap with real providers by setting Settings.llm and Settings.embed_model elsewhere.
    """
    Settings.llm = MockLLM()
    Settings.embed_model = SimpleEmbedding()
    
    documents = [Document(text=t) for t in texts if t and t.strip()]
    if not documents:
        documents = [Document(text="Empty corpus; using placeholder.")]
    return VectorStoreIndex.from_documents(documents)


def answer_query(index: VectorStoreIndex, question: str) -> str:
    engine = index.as_query_engine()
    response = engine.query(question)
    return str(response)



