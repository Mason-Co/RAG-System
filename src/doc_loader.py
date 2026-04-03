# Mason Colacicco
# File to locate and load documents

import os
from pypdf import PdfReader

class DocumentLoader:
    # Receives a string defining the document path
    def __init__(self, documents_path: str):
        self.documents_path = documents_path

    def load_pdf_text(self, file_path: str) -> str:
        if PdfReader is None:
            raise ImportError(
                "PDF support requires the 'pypdf' package. "
                "Install it with: pip install pypdf"
            )

        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages).strip()

    # Reflects back to List import to show that this returns a list of strings
    def load_documents(self) -> dict[str, str]:
        # Creates an empty dict that contains the text of each document
        doc_dict = {}

        # Loops through all the document files that will be loaded
        for filename in os.listdir(self.documents_path):
            file_path = os.path.join(self.documents_path, filename)
            # Filter to process .txt files
            if filename.endswith('.txt'):
                # Open and read the file
                # It creates a file path, opens in read mode, and then closes the document when completed
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    # Reads the whole file into a string and adds it to the list
                    document = file.read()
                doc_dict[filename] = document
            elif filename.endswith('.pdf'):
                doc_dict[filename] = self.load_pdf_text(file_path)
        # Returns the list of documents as the value of the method.
        return doc_dict

    def list_document_names(self):
        return [f for f in os.listdir(self.documents_path)]

if __name__ == '__main__':
    loader = DocumentLoader('../data/documents')
    loaded_documents = loader.load_documents()
    print(len(loaded_documents))
    print(loaded_documents)
    print(loaded_documents['chapter-2-testing-doc.pdf'])
    for doc in loaded_documents:
        print(loaded_documents[doc])