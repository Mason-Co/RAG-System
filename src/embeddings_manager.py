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
    def __init__(self, api_key: str):
        openai.api_key = api_key

    # Take a list of chunks and returned a list of vectors
    def create_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        embeddings = []
        # Loop through each chunk
        for text in texts:
            # Input one list to OpenAI model and receive a vector
            response = openai.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            # Put the new array into the list
            embeddings.append(np.array(response.data[0].embedding))
        return embeddings