# Mason Colacicco
# File to break text documents into readable chunks

# Does not change code functionality, but helps understand code
from typing import List

class TextProcessor:
    # Sets a max size for the chunks
    def __init__(self, chunk_size: int = 650, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # Splits the long string of provided text into chunks
    def split_into_chunks(self, text: str) -> List[str]:
        # All the words in the provided text
        words = text.split()
        # Create a list of chunks
        chunks = []
        # stride = 800 chunk - 200 overlap.
        # Overlap causes first 200 overlap with previous chunk, and last 200 overlap with the following chunk
        stride = self.chunk_size - self.chunk_overlap

        for start in range(0, len(text), stride):
            # Create each chunk while keeping the overlap due to the for loop jumping by stride
            chunk = text[start:start + self.chunk_size]
            # Breaks if there is an empty string
            if not chunk:
                break
            # Add the chunk to the list of chunks
            chunks.append(chunk)
            # Ends if the chunk has reached the end of the text
            if start + self.chunk_size >= len(text):
                break

        return chunks