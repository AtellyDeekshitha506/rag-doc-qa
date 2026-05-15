"""
Document Processing Module - Handles document loading and chunking
"""

import streamlit as st
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentProcessor:
    """Process uploaded documents"""

    @staticmethod
    def load_pdf(file_path: str) -> List:
        """Load PDF document using PyMuPDF"""
        try:
            loader = PyMuPDFLoader(file_path)
            documents = loader.load()
            return documents
        except Exception as e:
            st.error(f"Error loading PDF: {str(e)}")
            return []

    @staticmethod
    def load_text(file_path: str) -> List:
        """Load plain text document"""
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()
            return documents
        except Exception as e:
            st.error(f"Error loading text file: {str(e)}")
            return []

    @staticmethod
    def chunk_documents(
        documents: List,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> List:
        """Split documents into overlapping chunks.

        BUG FIX: Added a guard so chunk_overlap is always strictly less than
        chunk_size. RecursiveCharacterTextSplitter raises a ValueError when
        chunk_overlap >= chunk_size, which would silently swallow all chunks
        and return an empty list (breaking every downstream step).
        """
        if not documents:
            return []

        # Guard: overlap must be < chunk_size
        if chunk_overlap >= chunk_size:
            chunk_overlap = max(0, chunk_size // 10)
            st.warning(
                f"chunk_overlap was >= chunk_size. Reset to {chunk_overlap}."
            )

        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", " ", ""],
            )
            chunks = text_splitter.split_documents(documents)

            # BUG FIX: Filter out chunks with empty or whitespace-only content.
            # Empty chunks produce zero-vector embeddings that pollute similarity
            # search results — a query can match an "empty" chunk with a high score.
            chunks = [
                c for c in chunks
                if hasattr(c, "page_content") and c.page_content.strip()
            ]
            return chunks
        except Exception as e:
            st.error(f"Error chunking documents: {str(e)}")
            return []