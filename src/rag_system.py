# Mason Colacicco
# File

import os
from dotenv import load_dotenv
import openai

# Import other RAG files
from .doc_loader import DocumentLoader
from .text_processor import TextProcessor
from .embeddings_manager import EmbeddingsManager
from .retrieval_system import RetrievalSystem

class RAGSystem:
    def __init__(self):
        # Load .env file and retrieve the OpenAI API Key
        load_dotenv()
        self.api_type = "azure"
        self.api_key = os.getenv('AZURE_OPENAI_KEY')
        self.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_version = "2023-07-01-preview"

        self.loader = DocumentLoader('data/documents')
        self.processor = TextProcessor()
        self.embeddings_manager = EmbeddingsManager(self.api_type, self.api_key, self.api_base, self.api_version)

        # Initialize system
        self.initialize_system()

    def initialize_system(self):
        # Load and process documents
        documents = self.loader.load_documents()
        self.chunks = []  # list[dict]
        for doc in documents:
            chunk_texts = self.processor.split_into_chunks(documents[doc])
            for i, chunk_text in enumerate(chunk_texts):
                self.chunks.append({
                    "text": chunk_text,
                    "source": doc,
                    "chunk_id": i
                })

        # Create embeddings
        chunk_texts_for_embedding = [c["text"] for c in self.chunks]
        self.embeddings = self.embeddings_manager.create_embeddings(chunk_texts_for_embedding)

        # Initialize retrieval system
        self.retrieval_system = RetrievalSystem(self.chunks, self.embeddings)

    def answer_question(self, question: str) -> str:
        # Get question embedding
        question_embedding = self.embeddings_manager.create_embeddings([question])[0]

        # Get relevant chunks
        relevant_chunks = self.retrieval_system.find_similar_chunks(question_embedding)

        # Prepare context
        context = "\n\n".join([
            f"[Source: {item[0]['source']}] {item[0]['text']}"
            for item in relevant_chunks
        ])

        # Create prompt
        prompt = f"""Context: {context}\n\nQuestion: {question}\n\nAnswer:"""

        # Get response from OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful RAG assistant. Answer the question using only the provided context. "
                        "If the context is insufficient, say that clearly and suggest what information is missing. "
                        "Keep the answer concise and directly relevant to the question."
                    ),
                },
                {"role": "user", "content": prompt}
            ]
        )

        return f"{response.choices[0].message.content}\n\nContext is provided below:\n{context}"

if __name__ == "__main__":
    loader = DocumentLoader('../data/documents')
    processor = TextProcessor()
    documents = loader.load_documents()
    chunks = {}
    for doc in documents:
        chunks[doc] = processor.split_into_chunks(documents[doc])

    for chunk in chunks:
        print('\n', chunk)
        for section in chunks[chunk]:
            print(f'\n\nNEW CHUNK STARTING NOW \n\n{section}')