# Mason Colacicco
# File for relating the chunks to their vectors and then finding the similarity level to the user's query

# Used for vector math
import numpy as np
# Does not change code functionality, but helps understand code
from typing import List, Tuple

class RetrievalSystem:
    # Creates a connection between the chunks and embeddings that were created from each chunk
    def __init__(self, chunks: List[str], embeddings: List[np.ndarray]):
        self.chunks = chunks
        self.embeddings = embeddings

    # Input user query vector and how many results to return
    def find_similar_chunks(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
        similarities = []
        # Loop through embeddings and each index for each vector
        for i, embedding in enumerate(self.embeddings):
            # Uses cosine similarity to calculate similarity where 1 is the same and -1 is the opposite
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            # Stores the chunk of text and the similarity to the query
            similarities.append((self.chunks[i], similarity))

        # Returns a sorted list of the top_k most similar chunks
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]