import streamlit as st
from src.rag_system import RAGSystem
from src.doc_loader import DocumentLoader

st.set_page_config(page_title="RAG System", layout="wide")
st.title("RAG System Capstone")

rag = RAGSystem()
loader = DocumentLoader("data/documents")
doc_names = [f for f in loader.list_document_names()]  # implement this method

tab_docs, tab_qa = st.tabs(["Loaded Documents", "Ask Questions"])

with tab_docs:
    st.subheader("Documents currently loaded")
    if doc_names:
        for name in sorted(doc_names):
            st.write(f"- {name}")
    else:
        st.info("No .txt documents found in data/documents")

with tab_qa:
    st.subheader("Ask a question")
    q = st.text_input("Your question")
    if st.button("Submit", type="primary") and q.strip():
        with st.spinner("Thinking..."):
            answer = rag.answer_question(q)
        st.markdown("### Answer")
        st.write(answer)