"""
Complete RAG System with File Upload, Vector Search, and LLM Answer Generation
================================================================================
Features:
- Upload PDF/DOC files
- Automatic document chunking
- Embedding generation (all-MiniLM-L6-v2)
- Vector storage in ChromaDB
- Query embedding and similarity search
- LLM-based answer generation (Cloud AI)
- Interactive chat interface with ChatGPT-like UX
"""

import streamlit as st
import os
import tempfile
import shutil

# Import modular components
from embeddings import EmbeddingManager
from vectordb import VectorStoreManager
from retriever import RAGRetriever
from document_processor import DocumentProcessor
from llm import AnswerGenerator


# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="RAG System - Document QA",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ================================================================
# STREAMLIT SESSION STATE INITIALIZATION
# ================================================================

if "embedding_manager" not in st.session_state:
    st.session_state.embedding_manager = None

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "rag_retriever" not in st.session_state:
    st.session_state.rag_retriever = None

if "answer_generator" not in st.session_state:
    st.session_state.answer_generator = None

if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", ""),

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "system_initialized" not in st.session_state:
    st.session_state.system_initialized = False

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None



# ================================================================
# AUTO-INIT HELPER
# ================================================================

def auto_initialize_system():
    """Auto-initialize system on first use"""
    if st.session_state.system_initialized:
        return
    
    try:
        st.session_state.embedding_manager = EmbeddingManager()
        st.session_state.vectorstore = VectorStoreManager()
        st.session_state.rag_retriever = RAGRetriever(
            st.session_state.embedding_manager,
            st.session_state.vectorstore
        )
        
        # Always use Groq with pre-filled API key
        st.session_state.answer_generator = AnswerGenerator(
            api_key=st.session_state.groq_api_key
        )
        st.session_state.system_initialized = True
    except Exception as e:
        st.error(f"Error initializing system: {str(e)}")



# ================================================================
# MAIN APP
# ================================================================

def main():
    # Header
    st.title("📚 Document Chat")
    st.markdown("Upload PDFs and ask questions to get instant answers using AI ⚡")
    
    # Sidebar - Chat History & Account
    with st.sidebar:
        st.header("💬 Chat History")
        
        if st.session_state.chat_history:
            for idx, item in enumerate(st.session_state.chat_history, 1):
                with st.container():
                    query_text = item['query'][:40] + "..." if len(item['query']) > 40 else item['query']
                    if st.button(f"Q{idx}: {query_text}", use_container_width=True, key=f"chat_{idx}"):
                        st.session_state.selected_chat = idx - 1
        else:
            st.info("💭 No chat history yet. Start by uploading a document!")
        
        st.divider()
        
        # Debug: Show collection stats
        if st.session_state.vectorstore:
            stats = st.session_state.vectorstore.get_stats()
            if "document_count" in stats:
                st.info(f"📊 **Collection Stats**\n\nDocuments: {stats.get('document_count', 0)}")
        
        st.divider()
        st.header("⚙️ Account Settings")
        
        # Initialize user profile in session state
        if "user_profile" not in st.session_state:
            st.session_state.user_profile = {
                "name": "User",
                "email": "",
                "joined": "Today"
            }
        
        # User profile form
        with st.form("user_profile_form"):
            st.write("Update your account information:")
            
            name = st.text_input(
                "Full Name",
                value=st.session_state.user_profile.get("name", "User"),
                placeholder="Enter your name"
            )
            
            email = st.text_input(
                "Email Address",
                value=st.session_state.user_profile.get("email", ""),
                placeholder="your@email.com",
                type="default"
            )
            
            if st.form_submit_button("💾 Save Profile", use_container_width=True):
                st.session_state.user_profile["name"] = name
                st.session_state.user_profile["email"] = email
                st.success("✅ Profile updated!")
        
        # Display current user info
        st.divider()
        st.write(f"**👤 Name:** {st.session_state.user_profile.get('name', 'User')}")
        if st.session_state.user_profile.get('email'):
            st.write(f"**📧 Email:** {st.session_state.user_profile.get('email')}")
        
        # Clear button
        st.subheader("⚙️ Actions")
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.session_state.vectorstore:
                st.session_state.vectorstore.clear_collection()
            st.session_state.chat_history = []
            st.session_state.system_initialized = False
            st.success("✅ Cleared!")
            st.rerun()
    
    # Constants
    chunk_size = 500
    chunk_overlap = 50
    top_k = 5
    
    # Main content - ChatGPT-like interface
    col_main = st.container()
    
    # Auto-initialize on first page load
    auto_initialize_system()
    
    # Upload section
    with col_main:
        st.subheader("📄 Upload Documents")
        
        if not st.session_state.embedding_manager:
            st.warning("❌ System not initialized. Refresh the page.")
        else:
            uploaded_files = st.file_uploader(
                "Choose PDF or TXT files",
                type=["pdf", "txt"],
                accept_multiple_files=True
            )
            
            if uploaded_files:
                col1, col2 = st.columns(2)
                with col1:
                    upload_button = st.button("⬆️ Upload & Process", use_container_width=True)
                with col2:
                    clear_button = st.button("🗑️ Clear & Start Fresh", use_container_width=True, help="Clear old data before uploading new PDF")
                
                if clear_button:
                    if st.session_state.vectorstore:
                        st.session_state.vectorstore.clear_collection()
                    st.session_state.documents_loaded = False
                    st.session_state.chat_history = []
                    st.success("✅ Database cleared! Ready for new PDF.")
                    st.rerun()
                
                if upload_button:
                    # ALWAYS clear before processing new files to avoid mixing old and new chunks
                    st.info("🔄 Clearing old data before processing new PDF...")
                    if st.session_state.vectorstore:
                        st.session_state.vectorstore.clear_collection()
                    
                    with st.spinner("Processing documents..."):
                        total_chunks = 0
                        temp_dir = tempfile.mkdtemp()
                        current_file_chunks = {}  # Track chunks by file
                        
                        try:
                            for uploaded_file in uploaded_files:
                                # Save temp file
                                temp_path = os.path.join(temp_dir, uploaded_file.name)
                                with open(temp_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                
                                # Load document
                                if uploaded_file.name.endswith('.pdf'):
                                    documents = DocumentProcessor.load_pdf(temp_path)
                                else:
                                    documents = DocumentProcessor.load_text(temp_path)
                                
                                if documents:
                                    # Chunk documents
                                    chunks = DocumentProcessor.chunk_documents(
                                        documents,
                                        chunk_size=chunk_size,
                                        chunk_overlap=chunk_overlap
                                    )
                                    
                                    if not chunks:
                                        st.warning(f"⚠️ {uploaded_file.name}: No valid chunks extracted.")
                                        continue
                                    
                                    # Generate embeddings
                                    texts = [doc.page_content for doc in chunks]
                                    
                                    if not texts:
                                        st.warning(f"⚠️ {uploaded_file.name}: No text extracted.")
                                        continue
                                    
                                    embeddings = st.session_state.embedding_manager.embed_documents(texts)
                                    
                                    if embeddings is None or len(embeddings) == 0:
                                        st.warning(f"⚠️ {uploaded_file.name}: Failed to generate embeddings.")
                                        continue
                                    
                                    # Add to vectorstore with source file name
                                    added = st.session_state.vectorstore.add_documents(chunks, embeddings, source_file=uploaded_file.name)
                                    total_chunks += added
                                    current_file_chunks[uploaded_file.name] = chunks
                                    st.success(f"✅ {uploaded_file.name}: Created {added} chunks")
                                else:
                                    st.warning(f"⚠️ {uploaded_file.name}: Could not load document.")
                            
                            st.session_state.documents_loaded = True
                            st.balloons()
                            
                            # Show final stats
                            stats = st.session_state.vectorstore.get_stats()
                            st.success(f"✅ Processing Complete! Total chunks in database: {stats.get('document_count', 0)}")
                            
                            # SHOW ALL CHUNKS FROM CURRENT UPLOAD - No hiding!
                            st.subheader("📋 Chunks Created from Your PDF")
                            st.info(f"These chunks were extracted from your document and stored in the database.")
                            
                            for file_name, chunks in current_file_chunks.items():
                                st.write(f"### 📄 From: **{file_name}**")
                                st.write(f"Total chunks: **{len(chunks)}**")
                                
                                for idx, chunk in enumerate(chunks, 1):
                                    with st.container():
                                        col1, col2 = st.columns([1, 10])
                                        with col1:
                                            st.write(f"**#{idx}**")
                                        with col2:
                                            chunk_text = chunk.page_content if hasattr(chunk, 'page_content') else str(chunk)
                                            st.text_area(
                                                f"Chunk {idx}",
                                                value=chunk_text,
                                                height=100,
                                                disabled=True,
                                                label_visibility="collapsed",
                                                key=f"chunk_{idx}"
                                            )
                                        st.divider()
                            
                            st.rerun()
                            
                        finally:
                            shutil.rmtree(temp_dir, ignore_errors=True)
    
    st.divider()
    
    # Chat section
    st.subheader("💬 Ask Questions")
    
    if not st.session_state.embedding_manager:
        st.warning("Please refresh the page to initialize the system.")
    elif not st.session_state.documents_loaded:
        st.info("👆 Upload documents above to get started")
    else:
        # Display selected chat or all history
        if st.session_state.selected_chat is not None:
            item = st.session_state.chat_history[st.session_state.selected_chat]
            st.markdown(f"**Q:** {item['query']}")
            st.markdown(f"**A:** {item['answer']}")
        elif st.session_state.chat_history:
            st.subheader("Recent Chats")
            for item in st.session_state.chat_history[-3:]:  # Show last 3
                with st.container():
                    st.markdown(f"**Q:** {item['query']}")
                    st.markdown(f"**A:** {item['answer']}")
                    st.divider()
        
        # Input section
        st.subheader("New Question")
        query = st.text_area(
            "Ask a question about your documents:",
            placeholder="What would you like to know?",
            height=80,
            label_visibility="collapsed"
        )
        
        if st.button("🔍 Get Answer", use_container_width=True):
            if query.strip():
                # Retrieve documents
                results = st.session_state.rag_retriever.retrieve(query, top_k=top_k)
                
                if results.get("error"):
                    st.error(f"Error: {results['error']}")
                elif results.get("total_results") == 0:
                    st.info("No relevant information found in documents.")
                else:
                    # Generate answer
                    context = "\n\n".join([
                        doc['full_content'] for doc in results["documents"]
                    ])
                    
                    # DEBUG: Show what context is being sent to LLM
                    with st.expander("🔍 DEBUG - Retrieved Context (Click to view)"):
                        st.write(f"**Total results:** {results.get('total_results')}")
                        st.write(f"**Context length:** {len(context)} characters")
                        st.write(f"**Context preview:**")
                        st.text(context[:500] if len(context) > 500 else context)
                    
                    answer = None
                    if st.session_state.answer_generator and st.session_state.answer_generator.llm:
                        answer = st.session_state.answer_generator.generate_answer(query, context)
                    
                    if answer:
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "query": query,
                            "answer": answer,
                            "docs_used": results["total_results"]
                        })
                        st.success("✅ Done!")
                        st.rerun()
                    else:
                        # Show retrieved documents even if LLM is not available
                        st.info(f"Retrieved {results['total_results']} relevant document(s):")
                        with st.expander("📄 View Retrieved Content"):
                            for idx, doc in enumerate(results["documents"], 1):
                                st.markdown(f"**Document {idx}** (Match: {doc['similarity_score']:.1%})")
                                st.write(doc['full_content'])
                                st.divider()


# ================================================================
# MAIN APP LOGIC - SHOW AUTH OR CHAT BASED ON LOGIN STATUS
# ================================================================

if __name__ == "__main__":
    main()
