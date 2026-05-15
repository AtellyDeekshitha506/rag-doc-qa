"""
Embeddings Module - Handles document and query embedding using sentence-transformers
"""

from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingManager:
    """Handles document embedding using sentence-transformers"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the embedding model"""
        # BUG FIX: Removed st.spinner() here — this is called during session_state init
        # BEFORE Streamlit's render context is ready, causing a ScriptRunContext error.
        # Streamlit UI calls (st.spinner, st.error, etc.) must only happen inside
        # a running render cycle, not inside __init__ of objects stored in session_state.
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            # Re-raise so app.py can catch and show the error in its own render cycle
            raise RuntimeError(f"Error loading embedding model '{self.model_name}': {e}") from e

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text string"""
        if not self.model:
            raise ValueError("Embedding model is not loaded.")
        # BUG FIX: Returns a numpy array — callers (vectordb) must convert to list.
        # Keeping as numpy here is fine; vectordb.py already handles .tolist().
        return self.model.encode(text)

    def embed_documents(self, documents: List[str]) -> List:
        """Generate embeddings for a list of document strings"""
        if not self.model:
            raise ValueError("Embedding model is not loaded.")
        if not documents:
            return []
        # BUG FIX: Filter out empty strings before encoding to avoid silent zero-vectors
        documents = [d for d in documents if d and d.strip()]
        if not documents:
            return []
        return self.model.encode(documents)