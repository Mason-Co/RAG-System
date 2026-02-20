# Mason Colacicco
# File to take documents

import os
# Does not change code functionality, but helps understand code
from typing import List

class DocumentLoader:
    # Defines what each document object will contain
    def __init__(self, documents_path: str):
        self.documents_path = documents_path

# Reflects back to List import to show that this returns a list of strings
    def load_documents(self) -> List[str]:
        # Creates an empty list that contains the text of each document
        documents = []
        # Loops through all the document files that will be loaded
        for filename in os.listdir(self.documents_path):
            # Filter to only processing .txt files
            if filename.endswith('.txt'):
                # Open and read the file
                # It creates a file path, opens in read mode, and then closes the document when completed
                with open(os.path.join(self.documents_path, filename), 'r') as file:
                    # Reads the whole file into a string and adds it to the list
                    documents.append(file.read())
        # Returns the list of documents as the value of the method.
        return documents