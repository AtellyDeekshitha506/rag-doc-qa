"""
Vector Search Module - RAG Retriever for similarity-based search
"""

import streamlit as st
from typing import Dict, Any
from embeddings import EmbeddingManager
from vectordb import VectorStoreManager


class RAGRetriever:
    """Main RAG retrieval system — performs similarity search against ChromaDB"""

    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        vectorstore: VectorStoreManager,
    ):
        self.embedding_manager = embedding_manager
        self.vectorstore = vectorstore

    def retrieve(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        
        formatted_results: Dict[str, Any] = {
            "query": query,
            "documents": [],
            "total_results": 0,
        }

        if not query or not query.strip():
            return formatted_results

        try:
            # 1. Embed the query
            query_embedding = self.embedding_manager.embed_text(query)

            # 2. Search the vector store
            results = self.vectorstore.search(query_embedding, n_results=top_k)

            if not results:
                return formatted_results

            # ChromaDB returns lists-of-lists; unwrap the outer list
            docs_list = (results.get("documents") or [[]])[0]
            dist_list = (results.get("distances") or [[]])[0]
            meta_list = (results.get("metadatas") or [[]])[0]

            if not docs_list:
                return formatted_results

            formatted_results["total_results"] = len(docs_list)

            for idx, doc in enumerate(docs_list):
                if not doc:  # skip empty strings
                    continue

                distance = float(dist_list[idx]) if idx < len(dist_list) else 0.0
                metadata = meta_list[idx] if idx < len(meta_list) else {}

                # BUG FIX: correct cosine-distance → similarity conversion
                similarity_score = round(1.0 - distance, 4)

                formatted_results["documents"].append(
                    {
                        "rank": idx + 1,
                        "content": doc[:300] + "..." if len(doc) > 300 else doc,
                        "full_content": doc,
                        "distance": round(distance, 4),
                        "similarity_score": similarity_score,
                        "metadata": metadata,
                    }
                )

            return formatted_results

        except Exception as e:
            st.error(f"Error retrieving documents: {str(e)}")
            return {"error": str(e), "query": query, "documents": [], "total_results": 0}