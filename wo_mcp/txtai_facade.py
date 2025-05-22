from pypdf import PdfReader
from txtai import Embeddings
from search_facade import SearchFacade

class TxtAiFacade(SearchFacade):
    def __init__(self):
        self.embeddings = Embeddings(hybrid=True, path="sentence-transformers/nli-mpnet-base-v2")
        self.data = []

    def add_pages(self, pdf_file: str) -> str:
        reader = PdfReader(pdf_file)
        metadata = reader.metadata
        rv = pdf_file
        if metadata and '/Title' in metadata:
            rv = metadata['/Title']
        self.data = [ page.extract_text().replace('\n', ' ') for page in reader.pages ]
        self.embeddings.index(self.data)
        return rv

    def search(self, query: str, top_results: int, simularity: float) -> list[str]:
        return [ self.data[index] for (index, score) in self.embeddings.search(query, top_results) if score > simularity ]
