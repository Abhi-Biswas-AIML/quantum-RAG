import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from quantum_rag.pipeline import QuantumRAG

load_dotenv()


# Streamlit Config
st.set_page_config(page_title="Quantum RAG Chat", layout="wide")

st.title("⚛️ Quantum RAG Chat")
st.markdown("Chat with your documents using **Quantum-Enhanced Retrieval** and **Gemini AI**.")

# Sidebar: Configuration & Upload
with st.sidebar:
    st.header("Configuration")
    default_key = os.getenv("GOOGLE_API_KEY", "")
    api_key = st.text_input("Google Gemini API Key", value=default_key, type="password", placeholder="Enter your key here...")

    
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

    rag_pipeline = None
    
    if uploaded_file and api_key:
        with st.spinner("Processing document..."):
            # Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            try:
                # Initialize Pipeline
                rag_pipeline = QuantumRAG(tmp_path, noisy=True)
                rag_pipeline.set_generator(api_key)
                st.success("Document indexed successfully!")
            except Exception as e:
                st.error(f"Error loading document: {e}")
            finally:
                # Cleanup temp file
                # os.remove(tmp_path) # Keeping it for session might be safer or managing per session
                pass
    elif not api_key:
        st.warning("Please enter your Google API Key to chat.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your document..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    if rag_pipeline:
        with st.chat_message("assistant"):
            with st.spinner("Quantum RAG is thinking..."):
                try:
                    result = rag_pipeline.run(prompt, return_ids=False)
                    # Pipeline run returns dict now if generator is set, check structure
                    if isinstance(result, dict):
                        response = result.get("answer", "No answer generated.")
                    else:
                        response = str(result) # Fallback
                        
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error during generation: {e}")
    else:
        if not uploaded_file:
            st.info("Please upload a document to start chatting.")
        elif not api_key:
            st.info("Please enter your API Key to enable chat.")
