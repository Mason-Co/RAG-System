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
        self.chunks = []
        for doc in documents:
            self.chunks.extend(self.processor.split_into_chunks(doc))

        # Create embeddings
        self.embeddings = self.embeddings_manager.create_embeddings(self.chunks)

        # Initialize retrieval system
        self.retrieval_system = RetrievalSystem(self.chunks, self.embeddings)

    def answer_question(self, question: str) -> str:
        # Get question embedding
        question_embedding = self.embeddings_manager.create_embeddings([question])[0]

        # Get relevant chunks
        relevant_chunks = self.retrieval_system.find_similar_chunks(question_embedding)

        # Prepare context
        context = "\n".join([chunk[0] for chunk in relevant_chunks])

        # Create prompt
        # REPLACING THIS AREA TEMPORARILY FOR TESTING
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

        return response.choices[0].message.content