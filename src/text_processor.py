# Mason Colacicco
# File to break text documents into readable chunks

# Does not change code functionality, but helps understand code
from typing import List

class TextProcessor:
    # Sets a max size for the chunks
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size

    # Splits the long string of provided text into chunks
    def split_into_chunks(self, text: str) -> List[str]:
        # All the words in the provided text
        words = text.split()
        # Create a list of chunks
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            # Check if the chunk will be too large if the word is added
            if current_size + len(word) > self.chunk_size:
                # List of words back into string separated by a space and add it to the chunk list
                chunks.append(' '.join(current_chunk))
                # Create a new chunk with the current word and word size
                current_chunk = [word]
                current_size = len(word)
            else:
                # Add the current word to the current chunk
                current_chunk.append(word)
                # The extra addition to size is to include the spaces
                current_size += len(word) + 1

        # Save the final chunk to the list
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks