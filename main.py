from src.rag_system import RAGSystem

# Initialize the RAG system
rag = RAGSystem()

# Ask a question
while True:
    question = input("\nWhat would you like to know about the document(s)?\nNote: Enter 'quit' to exit. \n")
    if question.lower() == "quit":
        break
    answer = rag.answer_question(question)
    print(answer)