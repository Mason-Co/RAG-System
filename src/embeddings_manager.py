# Mason Colacicco
# File creates the vectors for each chunk of the text

# Does not change code functionality, but helps understand code
from typing import List
# Used for receiving vectors
import openai
# Used for arrays
import numpy as np

class EmbeddingsManager:
    # Sets a global API key for any OpenAI calls
    def __init__(self, api_type, api_key, api_base, api_version):
        openai.api_key = api_key
        openai.api_type = api_type
        openai.api_base = api_base
        openai.api_version = api_version

    # Take a list of chunks and returned a list of vectors
    def create_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        # Input one list to OpenAI model and receive a vector
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )

        # Put the new array into the list
        embeddings = [
            np.array(item.embedding)
            for item in response.data
        ]

        return embeddings