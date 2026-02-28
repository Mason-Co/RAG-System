from src.rag_system import RAGSystem

# Initialize the RAG system
rag = RAGSystem()

# Ask a question
question = "Who coined the term Artificial Intelligence and at what event?"
answer = rag.answer_question(question)
print(answer)