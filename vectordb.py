"""
Vector Database Module - Manages ChromaDB vector storage and document indexing
"""

import streamlit as st
from typing import List, Dict, Any
import chromadb
import uuid
import numpy as np


class VectorStoreManager:
    """Manages ChromaDB vector storage"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.collection_name = "documents"
        self.client = None
        self.collection = None
        self._initialize()

    def _initialize(self):
        """Initialize ChromaDB with persistent storage"""
        try:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        except Exception as e:
            st.error(f"Error initializing ChromaDB: {str(e)}")
            raise e

    def add_documents(
        self,
        documents: List,
        embeddings_list: List,
        source_file: str = "uploaded",
    ) -> int:
        
        if not documents:
            st.warning("No documents to add.")
            return 0

# Safe numpy-compatible check for embeddings
        if embeddings_list is None or len(embeddings_list) == 0:
            st.warning("No embeddings to add.")
            return 0

        # BUG FIX 1: Convert numpy arrays → plain Python lists of float
        converted_embeddings = []
        for emb in embeddings_list:
            if hasattr(emb, "tolist"):
                converted_embeddings.append(
                    [float(v) for v in emb.tolist()]
                )
            elif isinstance(emb, list):
                converted_embeddings.append([float(v) for v in emb])
            else:
                converted_embeddings.append(list(emb))

        texts = [
            doc.page_content if hasattr(doc, "page_content") else str(doc)
            for doc in documents
        ]

        # BUG FIX 2: Lengths must match
        if len(texts) != len(converted_embeddings):
            st.error(
                f"Mismatch: {len(texts)} chunks vs {len(converted_embeddings)} "
                "embeddings. Skipping batch."
            )
            return 0

        # Filter pairs where text is empty (extra safety)
        valid_pairs = [
            (t, e)
            for t, e in zip(texts, converted_embeddings)
            if t and t.strip()
        ]
        if not valid_pairs:
            st.warning("All chunks were empty after filtering.")
            return 0

        texts, converted_embeddings = zip(*valid_pairs)
        texts = list(texts)
        converted_embeddings = list(converted_embeddings)

        ids = [str(uuid.uuid4()) for _ in texts]
        metadatas = [{"source": source_file} for _ in texts]

        try:
            self.collection.add(
                ids=ids,
                embeddings=converted_embeddings,
                metadatas=metadatas,
                documents=texts,
            )
            return len(ids)
        except Exception as e:
            st.error(f"Error adding documents to ChromaDB: {str(e)}")
            return 0

    def search(self, query_embedding, n_results: int = 5) -> Dict:
       
        try:
            if hasattr(query_embedding, "tolist"):
                query_embedding = [float(v) for v in query_embedding.tolist()]
            elif isinstance(query_embedding, list):
                query_embedding = [float(v) for v in query_embedding]

            # BUG FIX: clamp n_results to actual collection size
            count = self.collection.count()
            if count == 0:
                return {}
            n_results = min(n_results, count)

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
            )
            return results
        except Exception as e:
            st.error(f"Error searching ChromaDB: {str(e)}")
            return {}

    def get_stats(self) -> Dict:
        """Return basic collection statistics"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": self.persist_directory,
            }
        except Exception as e:
            return {"error": str(e)}

    def clear_collection(self) -> bool:
        """Delete and recreate the collection (clears all data)"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            return True
        except Exception as e:
            st.error(f"Error clearing collection: {str(e)}")
            return False