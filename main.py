from src.rag_system import RAGSystem

# Initialize the RAG system
rag = RAGSystem()

# Ask a question
question = input("What would you like to know about the evolution of AI?\n")
answer = rag.answer_question(question)
print(answer)