"""
LLM Module - LLM integration with Groq for answer generation
"""

import streamlit as st
from langchain_groq import ChatGroq


class AnswerGenerator:
    """Generate answers using Groq LLM with automatic model fallback"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.llm = None
        self.connection_status = "unknown"
        self.model_used = None
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize Groq LLM, trying models in preference order.

        BUG FIX: The original model list contained several model IDs that
        Groq has deprecated or renamed:
          - "llama-3.2-90b-text"  → does not exist (only vision variant)
          - "llama-3.2-70b-text"  → does not exist
          - "llama-3.2-90b-vision-preview" → preview removed
        These caused silent failures in the try/except loop, delaying init
        and potentially landing on a much weaker fallback model.

        Updated list uses only stable, confirmed model IDs as of mid-2025.
        Also fixed: bare `except:` swallowed ALL exceptions (including
        keyboard interrupts). Changed to `except Exception`.
        """
        if not self.api_key or not self.api_key.strip():
            self.connection_status = "no_key"
            st.error(
                "❌ **Groq API Key not provided.**\n\n"
                "Get your FREE key from: https://console.groq.com"
            )
            return

        # BUG FIX: Updated model list — only confirmed stable Groq model IDs
        models_to_try = [
            "llama-3.3-70b-versatile",   # Best general-purpose
            "llama-3.1-70b-versatile",   # Solid fallback
            "llama-3.1-8b-instant",      # Fast & lightweight
            "gemma2-9b-it",              # Google Gemma 2 (note: gemma2, not gemma-2)
            "mixtral-8x7b-32768",        # Long-context fallback
        ]

        for model in models_to_try:
            try:
                candidate = ChatGroq(
                    groq_api_key=self.api_key,
                    model_name=model,
                    temperature=0.7,
                )
                # BUG FIX: Do a cheap test call to confirm the model actually
                # works with this key. The ChatGroq constructor never raises —
                # failures only surface at invoke() time, meaning the original
                # code always "succeeded" on the first model even if it would
                # fail later. We probe here so fallback actually works.
                candidate.invoke("hi")
                self.llm = candidate
                self.model_used = model
                self.connection_status = "online"
                break
            except Exception:
                continue  # try next model

        if not self.llm:
            self.connection_status = "error"
            st.error(
                "❌ **No available Groq models found.**\n\n"
                "Check current models at: https://console.groq.com/docs/models"
            )

    def generate_answer(self, query: str, context: str) -> str | None:
        """Generate a context-grounded answer for the given query.

        BUG FIX: Added explicit None-check on context so the LLM is not
        called with an empty context string (which wastes tokens and produces
        hallucinated answers that violate the strict-context prompt).
        """
        if not self.llm:
            return None

        if not context or not context.strip():
            return "I cannot find this information in the provided documents."

        prompt = f"""You are a helpful assistant that answers questions ONLY based on the provided context.

IMPORTANT RULES:
1. ONLY use information from the provided context.
2. If the context does not contain enough information, respond with: "I cannot find this information in the provided documents."
3. Do NOT use general knowledge outside the context.
4. Be specific, accurate, and cite the relevant part of the context.

Context from documents:
{context}

User Question: {query}

Your Answer (based ONLY on the context above):"""

        try:
            with st.spinner(f"Generating answer with {self.model_used}..."):
                response = self.llm.invoke(prompt)

            answer = response.content if hasattr(response, "content") else str(response)
            return answer.strip()

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                st.error("❌ Groq rate limit hit. Please wait a moment and try again.")
            elif "401" in error_msg or "authentication" in error_msg.lower():
                st.error("❌ Groq authentication failed. Check your API key.")
            else:
                st.error(f"❌ Groq error: {error_msg}")
            return None